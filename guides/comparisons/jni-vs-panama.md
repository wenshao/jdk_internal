# JNI vs Panama (Foreign Function & Memory API): 原生互操作对比

> **一句话总结**: Panama FFM API 让你在纯 Java 中安全、高效地调用原生函数,
> 取代了繁琐且易出错的 JNI. JNI 正在走向限制和淘汰 (JEP 472).

---

## 目录

1. [开发体验对比](#开发体验对比)
2. [完整代码对比: 调用 strlen](#完整代码对比-调用-strlen)
3. [安全性对比](#安全性对比)
4. [性能对比](#性能对比)
5. [代码量对比](#代码量对比)
6. [jextract 工具](#jextract-工具)
7. [迁移路径: JNI → Panama](#迁移路径)
8. [JEP 472: JNI 限制路线图](#jep-472)
9. [总结与推荐](#总结与推荐)

---

## 开发体验对比

### JNI 的开发流程 (6 步)

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ 1. 写    │───►│ 2. 编译  │───►│ 3. 生成  │───►│ 4. 写    │
│ Java     │    │ Java     │    │ .h 头文件│    │ C 实现   │
│ native   │    │ class    │    │ (javah)  │    │          │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                                                     │
┌──────────┐    ┌──────────┐                         │
│ 6. 运行  │◄───│ 5. 编译  │◄────────────────────────┘
│ Java     │    │ .so/.dll │
│ -Djava   │    │ (gcc/cl) │
│ .library │    └──────────┘
│ .path    │
└──────────┘
```

### Panama FFM 的开发流程 (1 步)

```
┌──────────────────────────────┐
│ 1. 写 Java (全部在 Java 中)  │───► 运行
│    - 定义函数签名 (Java)      │
│    - 调用原生函数 (Java)      │
│    - 管理原生内存 (Java)      │
└──────────────────────────────┘
```

### 对比总结

| 方面                    | JNI                            | Panama FFM API                  |
|------------------------|--------------------------------|--------------------------------|
| **需要的语言**          | Java + C/C++                   | 纯 Java                        |
| **需要的工具链**        | javah + gcc/cl + make          | javac 即可                     |
| **头文件管理**          | 手动生成和维护 .h 文件          | 不需要                         |
| **构建系统复杂度**      | 需要 native build (CMake 等)   | 标准 Java 构建                  |
| **跨平台编译**          | 每个平台单独编译 .so/.dll/.dylib| 纯 Java, 自动跨平台             |
| **IDE 支持**            | C 代码需要 CLion/VS 等         | 标准 Java IDE                   |
| **类型安全**            | 手动确保 Java ↔ C 类型匹配     | 编译期 + 运行期检查             |
| **内存管理**            | 手动 malloc/free               | try-with-resources (Arena)     |

---

## 完整代码对比: 调用 strlen

### 目标: 从 Java 调用 C 标准库的 `strlen` 函数

### JNI 实现 (4 个文件)

**文件 1: Java 声明 (NativeHelper.java)**

```java
public class NativeHelper {
    static {
        System.loadLibrary("nativehelper");  // 加载 libnativehelper.so
    }

    // native 方法声明 — 实现在 C 中
    public static native long strlen(String s);

    public static void main(String[] args) {
        System.out.println(strlen("Hello"));  // 输出: 5
    }
}
```

**文件 2: 生成头文件 (命令行)**

```bash
javac NativeHelper.java
javac -h . NativeHelper.java  # 生成 NativeHelper.h
```

**文件 3: C 实现 (NativeHelper.c)**

```c
#include <jni.h>
#include <string.h>
#include "NativeHelper.h"

JNIEXPORT jlong JNICALL Java_NativeHelper_strlen(
    JNIEnv *env,
    jclass cls,
    jstring jstr)
{
    // 1. 从 Java String 获取 C 字符串 (需要内存拷贝)
    const char *cstr = (*env)->GetStringUTFChars(env, jstr, NULL);
    if (cstr == NULL) return -1;  // OOM

    // 2. 调用真正的 strlen
    jlong len = (jlong)strlen(cstr);

    // 3. 必须释放! 忘了就内存泄漏
    (*env)->ReleaseStringUTFChars(env, jstr, cstr);

    return len;
}
```

**文件 4: 编译脚本 (build.sh)**

```bash
# Linux
gcc -shared -fPIC \
    -I"$JAVA_HOME/include" \
    -I"$JAVA_HOME/include/linux" \
    -o libnativehelper.so \
    NativeHelper.c

# 运行
java -Djava.library.path=. NativeHelper
```

### Panama FFM 实现 (1 个文件)

```java
import java.lang.foreign.*;
import java.lang.invoke.MethodHandle;

public class PanamaHelper {
    public static void main(String[] args) throws Throwable {
        // 1. 获取 native linker
        Linker linker = Linker.nativeLinker();

        // 2. 查找 strlen 函数符号
        SymbolLookup stdlib = linker.defaultLookup();
        MemorySegment strlenAddr = stdlib.find("strlen").orElseThrow();

        // 3. 定义函数签名: long strlen(char*)
        MethodHandle strlen = linker.downcallHandle(
            strlenAddr,
            FunctionDescriptor.of(ValueLayout.JAVA_LONG, ValueLayout.ADDRESS)
        );

        // 4. 调用! 使用 Arena 管理内存生命周期
        try (Arena arena = Arena.ofConfined()) {
            MemorySegment cstr = arena.allocateFrom("Hello");  // 自动分配+拷贝
            long len = (long) strlen.invoke(cstr);
            System.out.println(len);  // 输出: 5
        }  // arena 关闭, 自动释放 cstr 内存
    }
}
```

```bash
# 编译和运行 — 无需 gcc, 无需 .so 文件
javac PanamaHelper.java
java PanamaHelper
# JDK 24+: FFM API 已 finalize, 无需额外标志
```

---

## 安全性对比

### JNI 的安全隐患

```c
// 隐患 1: 忘记释放 — 内存泄漏 (memory leak)
const char *cstr = (*env)->GetStringUTFChars(env, jstr, NULL);
strlen(cstr);
// 忘了 ReleaseStringUTFChars! — 没有编译警告, 运行时静默泄漏

// 隐患 2: 悬空指针 (dangling pointer)
jarray arr = (*env)->NewByteArray(env, 100);
jbyte *buf = (*env)->GetByteArrayElements(env, arr, NULL);
(*env)->ReleaseByteArrayElements(env, arr, buf, 0);
buf[0] = 42;  // 已释放! Use-after-free, 可能导致 JVM 崩溃

// 隐患 3: 缓冲区溢出 (buffer overflow)
char buffer[10];
const char *input = (*env)->GetStringUTFChars(env, jstr, NULL);
strcpy(buffer, input);  // 如果 input > 10 字节 — 缓冲区溢出!

// 隐患 4: JNI 引用管理错误
jobject ref = (*env)->NewGlobalRef(env, obj);
// 忘了 DeleteGlobalRef — GC 永远无法回收这个对象
```

### Panama FFM 的安全保障

```java
// 保障 1: Arena 自动管理内存生命周期
try (Arena arena = Arena.ofConfined()) {
    MemorySegment buf = arena.allocate(100);
    // 使用 buf...
}  // 自动释放, 无法泄漏

// 保障 2: 边界检查 (bounds checking)
MemorySegment buf = arena.allocate(10);
buf.setAtIndex(ValueLayout.JAVA_BYTE, 20, (byte)42);
// → IndexOutOfBoundsException! 而不是 JVM 崩溃

// 保障 3: 生命周期检查 (temporal safety)
MemorySegment buf;
try (Arena arena = Arena.ofConfined()) {
    buf = arena.allocate(100);
}
buf.get(ValueLayout.JAVA_BYTE, 0);
// → IllegalStateException: "Already closed"! 而不是 use-after-free

// 保障 4: 线程约束 (thread confinement)
Arena confined = Arena.ofConfined();
MemorySegment seg = confined.allocate(100);
// 在其他线程访问 seg → WrongThreadException
```

### 安全性对比表

| 风险类型             | JNI                          | Panama FFM                    |
|---------------------|------------------------------|-------------------------------|
| **内存泄漏**         | 常见, 无自动检测              | Arena + try-with-resources    |
| **悬空指针**         | 可能导致 JVM 崩溃            | IllegalStateException         |
| **缓冲区溢出**       | 可能导致安全漏洞              | IndexOutOfBoundsException     |
| **类型不匹配**       | 运行时崩溃                   | 编译期 MethodType 检查         |
| **线程安全**         | 开发者自己保证               | Confined Arena 自动保证        |
| **JVM 崩溃风险**     | 高 — 任何 C 错误都可能       | 低 — 只有 MemorySegment.NULL  |

---

## 性能对比

### Marshalling 开销 (数据转换)

```
调用 strlen("Hello World") 10,000,000 次:

JNI:         [████████████████████]     ~850 ns/call
Panama FFM:  [████████████████]         ~680 ns/call
直接 C:      [██████████████]           ~600 ns/call

JNI 的额外开销来源:
1. JNI 方法查找 (method resolution)
2. JNIEnv* 获取和验证
3. GetStringUTFChars / ReleaseStringUTFChars (拷贝)
4. 参数 marshalling (Java 类型 → C 类型)

Panama 的优势:
1. MethodHandle 直接绑定 (no lookup overhead)
2. 内存可以直接传递 (zero-copy 场景)
3. JIT 可以内联 downcall stub
```

### 批量数据传递

```java
// JNI — 需要 GetArrayElements / ReleaseArrayElements (可能拷贝)
// C 侧:
jfloat *arr = (*env)->GetFloatArrayElements(env, jarray, &isCopy);
// isCopy 可能为 true — 意味着整个数组被拷贝了!

// Panama — 直接操作 off-heap 内存, 零拷贝
try (Arena arena = Arena.ofConfined()) {
    MemorySegment nativeArray = arena.allocate(
        ValueLayout.JAVA_FLOAT, 1_000_000);

    // 直接写入 native 内存, 无拷贝
    for (int i = 0; i < 1_000_000; i++) {
        nativeArray.setAtIndex(ValueLayout.JAVA_FLOAT, i, computeValue(i));
    }

    // 直接传给 native 函数, 无拷贝
    nativeFunction.invoke(nativeArray, 1_000_000);
}
```

### 性能对比表

| 场景                  | JNI             | Panama FFM        | 差异        |
|----------------------|-----------------|-------------------|------------|
| 简单函数调用          | ~850 ns         | ~680 ns           | FFM 快 ~20% |
| 字符串传递            | 需拷贝          | 可零拷贝           | FFM 优      |
| 大数组传递            | 可能拷贝        | 零拷贝 (off-heap)  | FFM 大幅优  |
| 回调 (upcall)        | 较慢            | 更快 (method handle)| FFM 优     |
| JIT 优化             | 有限            | 深度优化           | FFM 优      |

---

## 代码量对比

### 场景: 调用 libcurl 执行 HTTP GET

```
文件数量:
JNI:     [████]  4 个文件 (Java + .h + .c + build script)
Panama:  [█]     1 个文件 (纯 Java)

代码行数 (含错误处理):
JNI:     [████████████████████████████████████████]  ~120 行 (Java 30 + C 70 + build 20)
Panama:  [████████████████████]                      ~60 行 (纯 Java)

构建步骤:
JNI:     [████]  4 步 (javac → javac -h → gcc → java)
Panama:  [█]     1 步 (javac + java)
```

### 场景: 调用 OpenSSL 计算 SHA-256

#### JNI 版本 (~80 行, 跨 3 个文件)

```java
// Java 部分 (~15 行)
public class NativeSha256 {
    static { System.loadLibrary("sha256jni"); }
    private static native byte[] sha256(byte[] input);
}
```

```c
// C 部分 (~50 行)
#include <jni.h>
#include <openssl/sha.h>
#include "NativeSha256.h"

JNIEXPORT jbyteArray JNICALL Java_NativeSha256_sha256(
    JNIEnv *env, jclass cls, jbyteArray jinput)
{
    jsize len = (*env)->GetArrayLength(env, jinput);
    jbyte *input = (*env)->GetByteArrayElements(env, jinput, NULL);
    if (!input) return NULL;

    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256((unsigned char*)input, len, hash);

    (*env)->ReleaseByteArrayElements(env, jinput, input, JNI_ABORT);

    jbyteArray jresult = (*env)->NewByteArray(env, SHA256_DIGEST_LENGTH);
    if (!jresult) return NULL;
    (*env)->SetByteArrayRegion(env, jresult, 0, SHA256_DIGEST_LENGTH, (jbyte*)hash);

    return jresult;
}
```

#### Panama 版本 (~35 行, 1 个文件)

```java
import java.lang.foreign.*;
import java.lang.invoke.MethodHandle;

public class PanamaSha256 {
    private static final int SHA256_DIGEST_LENGTH = 32;

    public static byte[] sha256(byte[] input) throws Throwable {
        Linker linker = Linker.nativeLinker();
        SymbolLookup openssl = SymbolLookup.libraryLookup("libssl.so", Arena.global());

        MethodHandle sha256 = linker.downcallHandle(
            openssl.find("SHA256").orElseThrow(),
            FunctionDescriptor.of(
                ValueLayout.ADDRESS,           // 返回值: unsigned char*
                ValueLayout.ADDRESS,           // data
                ValueLayout.JAVA_LONG,         // len
                ValueLayout.ADDRESS            // md (output buffer)
            )
        );

        try (Arena arena = Arena.ofConfined()) {
            MemorySegment nativeInput = arena.allocateFrom(ValueLayout.JAVA_BYTE, input);
            MemorySegment nativeOutput = arena.allocate(SHA256_DIGEST_LENGTH);

            sha256.invoke(nativeInput, (long) input.length, nativeOutput);

            return nativeOutput.toArray(ValueLayout.JAVA_BYTE);
        }
    }
}
```

---

## jextract 工具

`jextract` 是 Panama 生态的代码生成工具, 从 C 头文件自动生成 Java 绑定代码.

### 使用流程

```bash
# 1. 安装 jextract (独立下载, 非 JDK 内置)
# https://jdk.java.net/jextract/

# 2. 从头文件生成 Java 绑定
jextract --output src \
         --target-package com.example.curl \
         /usr/include/curl/curl.h

# 3. 生成的代码可以直接在 Java 中使用
```

### 生成的代码示例

```java
// jextract 自动生成 — 无需手写任何 native 代码
import com.example.curl.*;

public class CurlExample {
    public static void main(String[] args) {
        // 自动生成的 Java 方法, 与 C API 一一对应
        curl_h.curl_global_init(curl_h.CURL_GLOBAL_DEFAULT());

        var handle = curl_h.curl_easy_init();
        try (Arena arena = Arena.ofConfined()) {
            var url = arena.allocateFrom("https://example.com");
            curl_h.curl_easy_setopt(handle, curl_h.CURLOPT_URL(), url);
            curl_h.curl_easy_perform(handle);
        }
        curl_h.curl_easy_cleanup(handle);
        curl_h.curl_global_cleanup();
    }
}
```

### jextract vs 手写绑定

| 方面            | 手写 Panama 绑定         | jextract 生成             |
|----------------|--------------------------|--------------------------|
| **开发速度**    | 慢 (逐个函数定义)         | 快 (一个命令)             |
| **正确性**      | 容易出错 (类型/签名)      | 自动正确 (从头文件解析)    |
| **大型库**      | 不现实 (数百个函数)       | 几秒钟生成                |
| **维护**        | 库更新需手动同步          | 重新运行 jextract          |
| **可读性**      | 更好 (自定义命名)         | 生成代码较机械             |
| **适用场景**    | 少量函数调用              | 大型 C 库绑定              |

---

## 迁移路径

### JNI → Panama FFM 迁移步骤

#### Step 1: 审计现有 JNI 代码

```bash
# 找出所有 native 方法声明
grep -rn "native " --include="*.java" src/
# 结果示例:
# src/NativeHelper.java:12:  public static native long strlen(String s);
# src/CryptoNative.java:8:   private native byte[] encrypt(byte[] data, byte[] key);
```

#### Step 2: 逐个函数替换

```java
// JNI 原始代码
public class NativeHelper {
    static { System.loadLibrary("helper"); }
    public static native long strlen(String s);
}

// Panama 替换代码
public class NativeHelper {
    private static final MethodHandle STRLEN;

    static {
        Linker linker = Linker.nativeLinker();
        STRLEN = linker.downcallHandle(
            linker.defaultLookup().find("strlen").orElseThrow(),
            FunctionDescriptor.of(ValueLayout.JAVA_LONG, ValueLayout.ADDRESS)
        );
    }

    public static long strlen(String s) {
        try (Arena arena = Arena.ofConfined()) {
            return (long) STRLEN.invoke(arena.allocateFrom(s));
        } catch (Throwable t) {
            throw new RuntimeException(t);
        }
    }
}
```

#### Step 3: 移除 C 代码和构建脚本

```bash
# 可以删除的文件:
rm src/main/c/NativeHelper.c
rm src/main/c/NativeHelper.h
rm CMakeLists.txt  # 或 Makefile 中的 native 部分
```

#### Step 4: 更新构建配置

```xml
<!-- Maven: 移除 native 编译插件 -->
<!-- 删除 maven-native-plugin 或 cmake-maven-plugin -->

<!-- 无需添加新依赖 — FFM API 是 java.base 的一部分 -->
```

### 迁移注意事项

1. **回调函数 (Callbacks / Upcalls)**:
   ```java
   // JNI: 在 C 中回调 Java 方法
   // (*env)->CallVoidMethod(env, obj, methodID, ...);

   // Panama: 使用 upcall stub
   MethodHandle callback = MethodHandles.lookup()
       .findStatic(MyClass.class, "myCallback",
           MethodType.methodType(void.class, int.class));
   MemorySegment upcallStub = linker.upcallStub(
       callback,
       FunctionDescriptor.ofVoid(ValueLayout.JAVA_INT),
       arena
   );
   // 将 upcallStub 传给 native 函数作为函数指针
   ```

2. **结构体 (Structs)**:
   ```java
   // Panama 中定义 C struct 布局
   // struct Point { int x; int y; };
   StructLayout POINT = MemoryLayout.structLayout(
       ValueLayout.JAVA_INT.withName("x"),
       ValueLayout.JAVA_INT.withName("y")
   );
   VarHandle xHandle = POINT.varHandle(MemoryLayout.PathElement.groupElement("x"));
   VarHandle yHandle = POINT.varHandle(MemoryLayout.PathElement.groupElement("y"));

   try (Arena arena = Arena.ofConfined()) {
       MemorySegment point = arena.allocate(POINT);
       xHandle.set(point, 0L, 10);
       yHandle.set(point, 0L, 20);
   }
   ```

---

## JEP 472

### JNI 限制路线图 (Restricting JNI)

JEP 472 (JDK 24) 开始对 JNI 使用施加限制, 与 FFM API 的限制对齐:

```
JNI 限制时间线:

JDK 24:   JNI native 方法触发警告 (warning)
          └── 启动时: WARNING: JNI access by module X is restricted
          └── 可通过 --enable-native-access=module 消除警告

JDK 26+:  默认抛出异常 (预期)
(预期)    └── 必须显式授权: --enable-native-access=module
          └── 或使用 Panama FFM API 替代

未来:     JNI 可能被完全废弃 (deprecated for removal)
```

### 影响和应对

```bash
# JDK 24 运行包含 JNI 的应用
java --enable-native-access=com.example.mymodule -jar app.jar

# 或允许所有模块 (不推荐, 仅过渡用)
java --enable-native-access=ALL-UNNAMED -jar app.jar
```

### 为什么限制 JNI?

| 原因                    | 说明                                              |
|------------------------|--------------------------------------------------|
| **安全性**              | JNI 可以绕过所有 Java 安全检查                      |
| **完整性 (Integrity)** | JNI 代码可以访问任意内存, 破坏 JVM 内部状态          |
| **可维护性**            | JNI 使 JVM 优化 (如 Valhalla value types) 更困难    |
| **替代方案已就绪**       | Panama FFM API 已 finalize (JDK 22, JEP 454)      |

---

## 总结与推荐

### 全面对比

| 方面              | JNI                  | Panama FFM API           | 胜出     |
|------------------|----------------------|--------------------------|---------|
| **开发效率**      | 低 (多语言, 多工具)   | 高 (纯 Java)              | Panama  |
| **安全性**        | 低 (手动内存管理)     | 高 (Arena + 边界检查)      | Panama  |
| **性能**          | 良好                 | 更好 (~20% faster)        | Panama  |
| **调试**          | 困难 (跨语言)         | 容易 (标准 Java 调试)      | Panama  |
| **代码量**        | 多 (~2-3x)           | 少                        | Panama  |
| **跨平台**        | 需每平台编译          | 自动跨平台                 | Panama  |
| **生态/工具**     | 成熟但停滞            | jextract + 持续改进        | Panama  |
| **未来支持**      | 将被限制 (JEP 472)   | JDK 标准 API              | Panama  |
| **向后兼容**      | 现有代码可运行         | 需要 JDK 22+              | JNI     |
| **社区资源**      | 大量既有文档           | 快速增长中                 | JNI     |

### 决策建议

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   新项目:  使用 Panama FFM API (JDK 22+)                    │
│   既有项目: 计划迁移到 Panama, 利用 JEP 472 的过渡窗口       │
│   大型 C 库: 使用 jextract 自动生成绑定                      │
│   JDK < 22: 继续使用 JNI, 但准备迁移计划                    │
│                                                             │
│   Panama FFM API 在每个维度都优于 JNI,                      │
│   而且 JNI 正在被逐步限制. 迁移不是"是否"的问题, 而是"何时". │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
