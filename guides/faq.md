# JDK 26 常见问题 (FAQ)

---
## 目录

1. [一般问题](#1-一般问题)
2. [语言特性](#2-语言特性)
3. [并发编程](#3-并发编程)
4. [性能优化](#4-性能优化)
5. [网络](#5-网络)
6. [安全](#6-安全)
7. [兼容性](#7-兼容性)
8. [工具支持](#8-工具支持)
9. [更多问题？](#9-更多问题)

---


## 1. 一般问题

### Q: JDK 26 什么时候发布？

JDK 26 计划于 **2026年9月** 发布（GA）。目前可通过 [jdk.java.net](https://jdk.java.net/26/) 获取早期访问版本。

### Q: JDK 26 是 LTS 版本吗？

不是。JDK 26 是非 LTS 版本。最近的 LTS 版本是：
- JDK 21 (2023年9月)
- JDK 25 (2025年9月，下一个 LTS)

### Q: 我应该升级到 JDK 26 吗？

| 场景 | 建议 |
|------|------|
| 生产环境 | 等待 LTS 版本 (JDK 25) |
| 开发/测试 | 可以升级，体验新特性 |
| 新项目 | 可以使用，但考虑 LTS |
| 学习 | 推荐升级 |

---

## 2. 语言特性

### Q: `import module` 和普通 import 有什么区别？

```java
// 普通 import - 导入单个类或包
import java.util.List;
import java.util.ArrayList;

// 模块 import - 导入模块的所有导出包
import module java.base;  // 自动导入 java.util.*, java.io.* 等
```

**区别**:
- 模块导入更简洁，但可能导致命名冲突
- 模块导入只导入导出的包，不导入内部 API
- 编译后效果相同

### Q: 紧凑源文件适合生产代码吗？

```java
// 紧凑源文件 - 适合简单脚本
void main() {
    println("Hello");
}

// 传统类 - 适合生产代码
public class Application {
    public static void main(String[] args) {
        System.out.println("Hello");
    }
}
```

**建议**:
- ✅ 适合：脚本、工具、教学示例
- ⚠️ 谨慎：库代码（考虑兼容性）
- ❌ 不适合：复杂企业应用

### Q: StableValue 和 AtomicReference 有什么区别？

| 特性 | StableValue | AtomicReference |
|------|-------------|-----------------|
| 写入次数 | 一次 | 多次 |
| 读性能 | 极快 | 中等 |
| 用途 | 延迟初始化 | 并发修改 |

```java
// StableValue - 一次写入
StableValue<Logger> logger = StableValue.of();
logger.orElseSet(() -> Logger.getLogger("app"));  // 只能设置一次

// AtomicReference - 多次修改
AtomicReference<Integer> counter = new AtomicReference<>(0);
counter.updateAndGet(i -> i + 1);  // 可以多次修改
```

### Q: Scoped Values 什么时候能替代 ThreadLocal？

**现状**:
- JDK 26: Scoped Values 正式发布
- ThreadLocal: 未废弃，继续支持

**建议**:
- 新代码: 使用 Scoped Values
- 现有代码: 可以保留 ThreadLocal
- 虚拟线程场景: 强烈推荐 Scoped Values

---

## 3. 并发编程

### Q: Structured Concurrency 什么时候正式发布？

JEP 525 在 JDK 26 是**第六次预览**。预计在 JDK 27 或 28 正式发布。

### Q: 如何在虚拟线程中使用 Structured Concurrency？

```java
// 推荐: 虚拟线程 + Structured Concurrency
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
        // 每个子任务在独立虚拟线程中运行
        scope.fork(() -> blockingIO());
        scope.fork(() -> blockingIO());
        scope.join();
    }
}
```

### Q: StructuredTaskScope 和 CompletableFuture 有什么区别？

| 特性 | StructuredTaskScope | CompletableFuture |
|------|---------------------|-------------------|
| 生命周期 | 结构化，自动取消 | 非结构化，需手动取消 |
| 异常处理 | 统一处理 | 需要链式处理 |
| 可读性 | 高 | 中等 |
| 灵活性 | 中等 | 高 |

```java
// StructuredTaskScope - 任一失败自动取消其他
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    scope.fork(() -> task1());
    scope.fork(() -> task2());
    scope.join();
    scope.throwIfFailed();
}

// CompletableFuture - 需要手动处理
CompletableFuture<String> f1 = CompletableFuture.supplyAsync(() -> task1());
CompletableFuture<String> f2 = CompletableFuture.supplyAsync(() -> task2());
// 如果 f1 失败，f2 不会自动取消
```

---

## 4. 性能优化

### Q: G1 GC 的 Claim Table 是什么？

Claim Table 是 JEP 522 引入的优化机制：

```
传统方式:
- 多线程更新卡表需要同步
- 存在竞争开销

Claim Table:
- 每个线程"认领"卡表区域
- 减少跨线程同步
- 吞吐量提升 10-15%
```

**启用方式**: 默认启用，无需配置

### Q: 分代 Shenandoah 和传统 Shenandoah 有什么区别？

| 特性 | 传统 | 分代 |
|------|------|------|
| 年轻代处理 | 与老年代相同 | 独立回收 |
| 短命对象 | 效率较低 | 高效处理 |
| 吞吐量 | 中等 | 高 |
| 暂停时间 | <10ms | <10ms |

**建议**: 新项目使用分代模式

### Q: 紧凑对象头能节省多少内存？

```
对象类型          传统      紧凑      节省
-----------------------------------------
空对象            16 bytes  8-12 bytes  25-50%
Point (2 int)     24 bytes  16 bytes    33%
String (小)       40 bytes  32 bytes    20%
```

**启用方式**: 默认启用

```bash
# 禁用（如遇兼容性问题）
-XX:-UseCompactObjectHeaders
```

### Q: AOT 缓存如何创建和使用？

```bash
# 1. 训练运行，创建缓存
java -XX:ArchiveClassesAtExit=app.aot -cp myapp.jar MyApp

# 2. 使用缓存启动
java -XX:SharedArchiveFile=app.aot -cp myapp.jar MyApp

# 效果: 启动时间减少 30-50%
```

---

## 5. 网络

### Q: HTTP/3 和 HTTP/2 有什么区别？

| 特性 | HTTP/2 | HTTP/3 |
|------|--------|--------|
| 传输层 | TCP | UDP (QUIC) |
| 队头阻塞 | TCP 层存在 | 完全消除 |
| 连接建立 | 2-3 RTT | 0-1 RTT |
| 网络切换 | 需要重连 | 无缝迁移 |

### Q: 如何检查服务器是否支持 HTTP/3？

```java
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_3_AUTO)
    .build();

HttpResponse<String> response = client.send(request, handler);

// 检查实际使用的版本
if (response.version() == HttpClient.Version.HTTP_3) {
    System.out.println("服务器支持 HTTP/3");
} else {
    System.out.println("使用 " + response.version());
}
```

### Q: HTTP/3 连接失败怎么办？

```java
// 使用自动协商模式，自动降级
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_3_AUTO)  // 自动选择最佳版本
    .build();

// 检查防火墙是否阻止 UDP
// HTTP/3 使用 UDP，可能被防火墙阻止
```

---

## 6. 安全

### Q: 为什么 final 字段不能修改了？

JEP 500 的目标：
- **安全性**: 防止敏感数据被篡改
- **优化**: JVM 可以假设 final 字段不变
- **语义**: final 应该意味着真正不可变

**临时方案**:
```bash
# --finalization=enabled 用于重新启用已废弃的 Object.finalize() 机制，
# 与 JEP 500 final 字段修改限制无关。
# 如需临时允许反射修改 final 字段，请参考 JEP 500 文档中的迁移选项。
```

### Q: KDF API 支持哪些算法？

```
JDK 26 内置支持:
- HKDF-SHA256
- HKDF-SHA384
- HKDF-SHA512

第三方 Provider 可能支持:
- PBKDF2
- Argon2
- Scrypt
```

### Q: PEM 编码支持哪些格式？

```
支持:
- PRIVATE KEY
- PUBLIC KEY
- CERTIFICATE
- ENCRYPTED PRIVATE KEY
- PKCS#7
- X.509 CRL
```

---

## 7. 兼容性

### Q: JDK 26 支持哪些平台？

| 平台 | 架构 | 状态 |
|------|------|------|
| Linux | x86_64 | ✅ |
| Linux | aarch64 | ✅ |
| Linux | riscv64 | ✅ |
| macOS | x86_64 | ✅ |
| macOS | aarch64 | ✅ |
| Windows | x86_64 | ✅ |
| Windows | aarch64 | ✅ |
| Linux | x86 (32位) | ❌ 已移除 |

### Q: 如何检查代码是否受影响？

```bash
# 检查 32位依赖
uname -m

# 检查 Applet API
grep -r "java.applet\|JApplet" src/

# 检查 final 字段修改
grep -r "setAccessible\|Field.set" src/

# 使用 jdeps 分析
jdeps --jdk-internals myapp.jar
```

### Q: 预览特性需要什么配置？

```bash
# 编译时
javac --release 26 --enable-preview MyClass.java

# 运行时
java --enable-preview MyClass

# Maven
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <configuration>
        <release>26</release>
        <compilerArgs>
            <arg>--enable-preview</arg>
        </compilerArgs>
    </configuration>
</plugin>
```

---

## 8. 工具支持

### Q: IntelliJ IDEA 支持 JDK 26 吗？

需要 **IntelliJ IDEA 2025.1** 或更高版本。

配置步骤：
1. File → Project Structure → Project
2. SDK: 选择 JDK 26
3. Language level: 26 (Preview features)

### Q: Maven 如何配置 JDK 26？

```xml
<properties>
    <maven.compiler.source>26</maven.compiler.source>
    <maven.compiler.target>26</maven.compiler.target>
</properties>

<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <version>3.13.0</version>
    <configuration>
        <release>26</release>
        <compilerArgs>
            <arg>--enable-preview</arg>
        </compilerArgs>
    </configuration>
</plugin>
```

### Q: Gradle 如何配置 JDK 26？

```groovy
java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(26)
    }
}

tasks.withType(JavaCompile) {
    options.compilerArgs += '--enable-preview'
}

tasks.withType(JavaExec) {
    jvmArgs += '--enable-preview'
}
```

---

## 9. 更多问题？

如果你的问题没有在这里找到答案：

1. 查看 [学习路径](learning-path.md)
2. 查看 [迁移指南](migration-guide.md)
3. 查看 [速查表](cheat-sheet.md)
4. 访问 [OpenJDK 社区](https://openjdk.org/)