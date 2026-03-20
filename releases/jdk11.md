# JDK 11 发布说明

> **版本类型**: LTS (长期支持) | **发布日期**: 2018-09-25 | **支持截止**: 2032-01

[![OpenJDK](https://img.shields.io/badge/OpenJDK-11-orange)](https://openjdk.org/projects/jdk/11/)
[![License](https://img.shields.io/badge/License-GPLv2--with--Classpath--Exception-blue)](https://openjdk.org/projects/jdk/11/)

---

## 概述

JDK 11 是第一个在 6 个月发布周期下的 LTS 版本，引入了 **HTTP Client** 正式版、**var** 局部变量类型推断、**Flight Recorder** 等重要特性。

---

## 语言特性

### JEP 323: Local-Variable Syntax for Lambda Parameters ⭐

**状态**: 正式发布
**概述**: 允许在 Lambda 表达式中使用 `var` 声明参数。

```java
// 之前
Consumer<String> c = (String s) -> System.out.println(s);

// 现在
Consumer<String> c = (var s) -> System.out.println(s);

// 可以添加注解
Consumer<String> c = (@Nullable var s) -> System.out.println(s);
```

---

### JEP 181: Nest-Based Access Control

**状态**: 正式发布
**概述**: 基于嵌套的访问控制，允许嵌套类之间的私有成员访问。

```java
public class Outer {
    private int x;

    class Inner {
        void accessOuter() {
            // 直接访问外部类的私有成员
            System.out.println(x);
        }
    }
}
```

---

## 核心库

### JEP 321: HTTP Client (正式版) ⭐⭐

**状态**: 正式发布
**概述**: 新的 HTTP Client API 正式版，支持 HTTP/2。

```java
import java.net.http.*;
import java.net.URI;

// 创建 HTTP Client
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_2)
    .connectTimeout(Duration.ofSeconds(10))
    .build();

// 同步请求
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://example.com/"))
    .GET()
    .build();

HttpResponse<String> response = client.send(
    request,
    HttpResponse.BodyHandlers.ofString()
);

System.out.println(response.statusCode());
System.out.println(response.body());

// 异步请求
CompletableFuture<HttpResponse<String>> future = client.sendAsync(
    request,
    HttpResponse.BodyHandlers.ofString()
);

future.thenAccept(res -> {
    System.out.println(res.statusCode());
    System.out.println(res.body());
});
```

**特性**:
- HTTP/2 支持
- WebSocket 支持
- 同步和异步 API
- 响应式流 (Reactive Streams)

---

### JEP 328: Flight Recorder ⭐

**状态**: 正式发布
**概述**: Java Flight Recorder (JFR) 开源并集成到 OpenJDK。

```bash
# 启动 JFR 记录
java -XX:StartFlightRecording=duration=60s,filename=recording.jfr MyApp

# 使用 jcmd 控制录制
jcmd <pid> JFR.start name=profile settings=profile
jcmd <pid> JFR.dump name=profile filename=recording.jfr
jcmd <pid> JFR.stop name=profile
```

---

### JEP 333: ZGC: A Scalable Low-Latency Garbage Collector (实验) ⭐

**状态**: 实验性
**概述**: ZGC 垃圾收集器首次引入。

```bash
# 启用 ZGC (实验性)
java -XX:+UnlockExperimentalVMOptions -XX:+UseZGC MyApp
```

**特性**:
- Pause 时间 < 10ms
- 支持 TB 级堆内存
- 彩色指针 (Colored Pointers)
- 读屏障 (Load Barrier)

---

### JEP 309: Dynamic Class-File Constants

**状态**: 正式发布
**概述**: 动态类文件常量，支持更高效的字节码生成。

---

### JEP 315: Improve Aarch64 Intrinsics

**状态**: 正式发布
**概述**: 改进 AArch64 内置函数。

---

### JEP 329: ChaCha20 and Poly1305 Cryptographic Algorithms

**状态**: 正式发布
**概述**: ChaCha20 和 Poly1305 加密算法支持。

```java
Cipher cipher = Cipher.getInstance("ChaCha20-Poly1305");
cipher.init(Cipher.ENCRYPT_MODE, secretKey, parameterSpec);
byte[] encrypted = cipher.doFinal(plaintext);
```

---

### JEP 332: Transport Layer Security (TLS) 1.3

**状态**: 正式发布
**概述**: TLS 1.3 支持。

```java
// 默认启用 TLS 1.3
SSLContext sslContext = SSLContext.getInstance("TLS");
sslContext.init(null, null, null);

// 可以指定协议版本
SSLContext sslContext = SSLContext.getInstance("TLSv1.3");
```

---

## 工具

### JEP 330: Launch Single-File Source-Code Programs ⭐

**状态**: 正式发布
**概述**: 直接运行单文件 Java 程序，无需先编译。

```bash
# 直接运行 Java 文件
java HelloWorld.java

# 带参数
java HelloWorld.java arg1 arg2

# 使用 Shebang (Unix)
#!/path/to/java --source 11
void main() {
    System.out.println("Hello!");
}
```

---

### JEP 335: Deprecate the Nashorn JavaScript Engine

**状态**: 正式发布
**概述**: 废弃 Nashorn JavaScript 引擎。

---

## 移除

### JEP 335: Deprecate the Nashorn JavaScript Engine

**状态**: 正式发布
**概述**: 废弃 Nashorn，计划在未来的版本中移除。

---

### JEP 336: Deprecate Pack200 Tools and API

**状态**: 正式发布
**概述**: 废弃 Pack200 工具和 API。

---

## JEP 汇总

| 类别 | JEP | 标题 | 状态 |
|------|-----|------|------|
| **语言** | JEP 323 | Lambda 参数 var | ✅ 正式 |
| | JEP 181 | Nest-Based Access | ✅ 正式 |
| **核心库** | JEP 321 | HTTP Client | ✅ 正式 |
| | JEP 328 | Flight Recorder | ✅ 正式 |
| | JEP 309 | Dynamic Class-File Constants | ✅ 正式 |
| | JEP 315 | AArch64 Intrinsics | ✅ 正式 |
| | JEP 329 | ChaCha20-Poly1305 | ✅ 正式 |
| | JEP 332 | TLS 1.3 | ✅ 正式 |
| **GC** | JEP 333 | ZGC (实验) | 🧪 实验 |
| **工具** | JEP 330 | 单文件程序 | ✅ 正式 |
| **废弃** | JEP 335 | 废弃 Nashorn | ✅ 正式 |
| | JEP 336 | 废弃 Pack200 | ✅ 正式 |

> ✅ 正式版 | 🧪 实验性

---

## 相比 JDK 8 的新特性

### 新增正式特性

| 特性 | 说明 |
|------|------|
| **HTTP Client** | 新的 HTTP 客户端，支持 HTTP/2 |
| **var (Lambda)** | Lambda 参数支持 var |
| **Flight Recorder** | 低开销性能分析工具 |
| **TLS 1.3** | 最新 TLS 协议 |
| **单文件程序** | 直接运行 Java 源文件 |
| **ChaCha20-Poly1305** | 现代加密算法 |

### 新增实验特性

| 特性 | 说明 |
|------|------|
| **ZGC** | 可扩展低延迟 GC |

---

## 升级建议

### 从 JDK 8 升级

JDK 11 与 JDK 8 具有良好的二进制兼容性：

```bash
# 直接替换 JDK 版本即可
java -version
# openjdk version "11" 2018-09-25
```

### 破坏性变更

| 变更 | 影响 | 建议 |
|------|------|------|
| JavaFX 移除 | 使用 JavaFX 的应用 | 单独引入 JavaFX 依赖 |
| Java EE 模块移除 | 使用相关 API 的应用 | 添加独立依赖 |
| Nashorn 废弃 | 使用 JavaScript 的应用 | 迁移到 GraalJS |

### 推荐使用的新特性

| 场景 | 推荐特性 |
|------|----------|
| HTTP 调用 | HTTP Client |
| 性能分析 | Flight Recorder |
| 快速测试 | 单文件程序 |
| 加密 | ChaCha20-Poly1305 |

---

## 性能改进

| 领域 | 改进 |
|------|------|
| G1 GC | 更好的并行性 |
| 字符串 | 优化字符串拼接 |
| 类加载 | 改进类加载性能 |
| 加密 | AES 硬件加速 |

---

## 相关链接

- [OpenJDK JDK 11 项目页面](https://openjdk.org/projects/jdk/11/)
- [JDK 11 JEP 列表](https://openjdk.org/projects/jdk/11/spec/)
- [GitHub: openjdk/jdk](https://github.com/openjdk/jdk)
- [JDK 11 迁移指南](/by-version/jdk11/migration/from-8.md)
