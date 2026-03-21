# JDK 26 速查表

快速参考卡片，一页掌握 JDK 26 关键信息。

---
## 目录

1. [🎯 新特性速览](#1--新特性速览)
2. [📝 代码片段](#2--代码片段)
3. [⚙️ JVM 参数](#3--jvm-参数)
4. [🔄 迁移检查清单](#4--迁移检查清单)
5. [📊 性能对比](#5--性能对比)
6. [🛠️ IDE 支持](#6--ide-支持)
7. [📚 相关链接](#7--相关链接)
8. [⚠️ 注意事项](#8--注意事项)

---


## 1. 🎯 新特性速览

| JEP | 特性 | 一句话描述 |
|-----|------|-----------|
| 511 | 模块导入 | `import module java.base;` |
| 512 | 紧凑源文件 | `void main() { println("Hi"); }` |
| 502 | Stable Values | 线程安全的一次写入值 |
| 506 | Scoped Values | 有作用域的线程局部变量 |
| 517 | HTTP/3 | HTTP Client 支持 QUIC |
| 522 | G1 优化 | 吞吐量提升 10-15% |
| 521 | 分代 Shenandoah | 低延迟 + 高吞吐 |

---

## 2. 📝 代码片段

### 最简 Java 程序

```java
// Hello.java
import module java.base;

void main() {
    println("Hello, World!");
}
```

```bash
java Hello.java  # 直接运行
```

### 模块导入

```java
// 以前
import java.util.List;
import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;

// 现在
import module java.base;
```

### Stable Value

```java
private final StableValue<Logger> logger = StableValue.of();

public Logger getLogger() {
    return logger.orElseSet(() -> Logger.getLogger("MyApp"));
}
```

### Scoped Value

```java
private static final ScopedValue<User> CURRENT_USER = ScopedValue.create();

ScopedValue.where(CURRENT_USER, user).run(() -> {
    processRequest();  // 内部可访问 CURRENT_USER.get()
});
```

### 结构化并发

```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Future<String> user = scope.fork(() -> fetchUser());
    Future<List<Order>> orders = scope.fork(() -> fetchOrders());
    
    scope.join();
    scope.throwIfFailed();
    
    return new Response(user.resultNow(), orders.resultNow());
}
```

### HTTP/3 客户端

```java
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_3_AUTO)  // 自动协商
    .connectTimeout(Duration.ofSeconds(10))
    .build();

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://example.com"))
    .build();

HttpResponse<String> response = client.send(
    request, HttpResponse.BodyHandlers.ofString()
);
```

### KDF 密钥派生

```java
KDF kdf = KDF.getInstance("HKDF-SHA256");

HKDFParameterSpec params = HKDFParameterSpec.ofExtract()
    .addSalt(salt)
    .extract(ikm)
    .expand(info, 32);

SecretKey key = kdf.deriveKey("AES", params);
```

### PEM 编解码

```java
// 编码
PEMEncoder encoder = new PEMEncoder();
String pem = encoder.encode(privateKey);

// 解码
PEMDecoder decoder = new PEMDecoder();
PrivateKey key = decoder.decode(pem, PrivateKey.class);
```

---

## 3. ⚙️ JVM 参数

### GC 配置

```bash
# G1 GC (推荐)
-XX:+UseG1GC
-XX:+G1UseClaimTable              # 启用 Claim Table 优化
-XX:G1HeapRegionSize=32m          # Region 大小
-XX:MaxGCPauseMillis=200          # 目标暂停时间

# Shenandoah 分代模式
-XX:+UseShenandoahGC
-XX:ShenandoahGCMode=generational
-XX:ShenandoahYoungGenerationSize=25%

# ZGC (JDK 21+ 已支持分代)
-XX:+UseZGC
-XX:+ZGenerational
```

### 内存配置

```bash
# 堆内存
-Xms4g                           # 初始堆大小
-Xmx4g                           # 最大堆大小

# 压缩指针
-XX:+UseCompressedOops           # 压缩对象指针
-XX:+UseCompressedClassPointers  # 压缩类指针
-XX:+UseCompactObjectHeaders     # 紧凑对象头 (JDK 26)
```

### JFR 配置

```bash
# 启动时开始录制
-XX:StartFlightRecording=settings=profile,filename=recording.jfr,duration=60s

# 常用配置
-XX:FlightRecorderOptions=stackdepth=256

# CPU 时间采样 (JDK 26)
# 在 JFC 配置文件中启用 jdk.CPUTimeSample
```

### AOT 配置

```bash
# 创建 AOT 缓存
-XX:ArchiveClassesAtExit=app.aot

# 使用 AOT 缓存
-XX:SharedArchiveFile=app.aot

# 方法分析数据
-XX:ProfileAtExit=profile.prof   # 收集
-XX:ProfileData=profile.prof     # 使用
```

---

## 4. 🔄 迁移检查清单

### 升级前检查

```bash
# 1. 检查 32位依赖
uname -m                          # 确认是 x86_64/aarch64

# 2. 检查 Applet API 使用
grep -r "java.applet" src/
grep -r "JApplet" src/

# 3. 检查 final 字段修改
grep -r "setAccessible" src/ | grep -v "final"
grep -r "Field.set" src/

# 4. 检查 JNI 代码
# 检查是否修改 final 字段
```

### 升级后验证

```bash
# 1. 编译测试
javac --release 26 --enable-preview src/**/*.java

# 2. 运行测试
java --enable-preview -jar myapp.jar

# 3. 性能基准
# 对比升级前后性能
```

---

## 5. 📊 性能对比

### GC 性能

| GC | 暂停时间 | 吞吐量 | 内存开销 | 适用场景 |
|----|----------|--------|----------|----------|
| G1 (优化后) | 50-200ms | 高 | 中 | 通用 |
| Shenandoah (分代) | <10ms | 中高 | 中 | 低延迟 |
| ZGC (分代) | <1ms | 中高 | 高 | 极低延迟 |

### 启动性能

| 优化 | 启动时间改进 |
|------|-------------|
| CDS | -30% |
| AOT 缓存 | -50% |
| AOT 方法分析 | -20% |

### 内存效率

| 优化 | 内存节省 |
|------|----------|
| 紧凑对象头 | 20-40% |
| 压缩指针 | ~50% |

---

## 6. 🛠️ IDE 支持

| IDE | 版本要求 | 预览特性支持 |
|-----|----------|-------------|
| IntelliJ IDEA | 2025.1+ | ✅ |
| Eclipse | 2025-03+ | ✅ |
| VS Code | 最新 | ✅ |
| NetBeans | 25+ | ✅ |

### IntelliJ IDEA 配置

```
Settings → Build → Compiler → Java Compiler
└── Project bytecode version: 26
└── Preview features: Enabled

Settings → Build → Compiler → Java Compiler
└── Additional command line parameters: --enable-preview
```

---

## 7. 📚 相关链接

| 资源 | 链接 |
|------|------|
| OpenJDK JDK 26 | https://openjdk.org/projects/jdk/26/ |
| JEP 列表 | https://openjdk.org/projects/jdk/26/spec/ |
| API 文档 | https://download.java.net/java/early_access/jdk26/docs/api/ |
| GitHub | https://github.com/openjdk/jdk |

---

## 8. ⚠️ 注意事项

### 预览特性

以下特性需要 `--enable-preview`：

```
JEP 502: Stable Values
JEP 525: Structured Concurrency
JEP 530: Primitive Types in Patterns
JEP 526: Lazy Constants
JEP 470: PEM Encodings
```

### 移除特性

```
JEP 503: 32位 x86 支持
JEP 504: Applet API
```

### 行为变更

```
JEP 500: final 字段修改默认禁止
  └── 使用 --finalization=enabled 临时启用
```