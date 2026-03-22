# Java 平台变体

> OpenJDK 之外的 Java 平台：Android、GraalVM Native Image、WebAssembly 等

[← 返回发行版](README.md)

---
## 目录

1. [概述](#1-概述)
2. [Android](#2-android)
3. [GraalVM Native Image](#3-graalvm-native-image)
4. [WebAssembly (Wasm)](#4-webassembly-wasm)
5. [其他 JVM 语言](#5-其他-jvm-语言)
6. [选择指南](#6-选择指南)
7. [相关文档](#7-相关文档)

---


## 1. 概述

OpenJDK + HotSpot 是 Java 的官方参考实现，但生态中存在多种运行 Java 代码的平台：

```
┌─────────────────────────────────────────────────────────────────┐
│                    Java 平台生态                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                    Java 源代码 (.java)                           │
│                         │                                        │
│                         ▼                                        │
│                    Java 字节码 (.class)                          │
│                         │                                        │
│     ┌───────────┬───────┴───────┬───────────┐                  │
│     │           │               │           │                  │
│     ▼           ▼               ▼           ▼                  │
│  HotSpot     ART (Android)  Native Image  WASM                 │
│  (OpenJDK)   (Google)       (GraalVM)     (CheerpJ, TeaVM)     │
│                                                                 │
│     │           │               │           │                  │
│     ▼           ▼               ▼           ▼                  │
│  JVM 进程    DEX + ART      原生可执行    浏览器/WebAssembly    │
│  (~100ms)    (移动端)       (~5ms)        (浏览器)              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Android

### 平台对比

| 特性 | OpenJDK (HotSpot) | Android (ART) |
|------|-------------------|---------------|
| **VM 架构** | 栈式 JVM | 寄存器型 ART |
| **字节码** | JVM bytecode (.class) | Dalvik bytecode (.dex) |
| **编译** | JIT + AOT (分层编译) | AOT (安装时编译) |
| **GC** | G1/ZGC/Shenandoah | Generational GC (Android 13+) |
| **启动** | ~100ms | ~10ms (已 AOT) |
| **内存** | ~35MB 基础 | ~10MB 基础 |

### API Level → JDK 版本映射

Android 基于 OpenJDK 构建核心库，但版本不同步：

| Android 版本 | API Level | OpenJDK 基础版本 | 发布年份 |
|--------------|-----------|------------------|----------|
| Android 7.0 | 24 | OpenJDK 8 | 2016 |
| Android 8.0 | 26 | OpenJDK 8 | 2017 |
| Android 9 | 28 | OpenJDK 8 | 2018 |
| Android 10 | 29 | OpenJDK 9 (部分) | 2019 |
| Android 11 | 30 | OpenJDK 9/11 (部分) | 2020 |
| Android 12 | 31 | OpenJDK 11 (部分) | 2021 |
| Android 13 | 33 | OpenJDK 11/17 (部分) | 2022 |
| Android 14 | 34 | OpenJDK 17 (部分) | 2023 |
| Android 15 | 35 | OpenJDK 17/21 (部分) | 2024 |

> ⚠️ **注意**: Android 只包含 OpenJDK 的子集，许多 API 不可用或行为不同。

### 不可用/受限的 API

#### 完全不可用

| JDK API | 说明 |
|---------|------|
| `java.awt.*` | 无 GUI 工具包 |
| `javax.swing.*` | 无 Swing |
| `java.desktop` 模块 | 整个模块缺失 |
| `javax.management.*` | 无 JMX |
| `java.rmi.*` | 无 RMI |
| `javax.sound.*` | 无 Java Sound |
| `java.applet.*` | 无 Applet |

#### 行为不同

| JDK API | Android 行为 |
|---------|-------------|
| `java.lang.reflect.Proxy` | 只支持接口代理，不支持类代理 |
| `java.util.concurrent` | 部分类实现不同 |
| `java.nio.file.*` | 功能受限 |
| `javax.crypto.*` | 使用 Android Keystore |
| `java.net.*` | 使用 OkHttp 推荐替代 |

#### Android 特有

| Android API | 说明 |
|-------------|------|
| `android.*` | Android SDK |
| `kotlin.*` | Kotlin 标准库 (推荐) |
| `kotlinx.coroutines` | 协程 (推荐替代线程) |

### 迁移指南：Android → OpenJDK

#### 从 Android 代码迁移到服务端

```java
// Android
runOnUiThread(() -> updateUI());

// OpenJDK
Platform.runLater(() -> updateUI());  // JavaFX
SwingUtilities.invokeLater(() -> updateUI());  // Swing
```

```java
// Android - SharedPreferences
SharedPreferences prefs = getSharedPreferences("name", MODE_PRIVATE);
String value = prefs.getString("key", "default");

// OpenJDK - Preferences
Preferences prefs = Preferences.userNodeForPackage(MyClass.class);
String value = prefs.get("key", "default");
```

```java
// Android - Room/SQLite
@Dao
interface UserDao {
    @Query("SELECT * FROM user")
    List<User> getAll();
}

// OpenJDK - JDBC/Hibernate
@Entity
@Table(name = "user")
public class User { ... }

// 使用 JPA
List<User> users = entityManager.createQuery("SELECT u FROM User u", User.class).getResultList();
```

### 迁移指南：OpenJDK → Android

#### 服务端代码移植到 Android

1. **替换不可用 API**:
   - `java.awt` → Android View 系统
   - `javax.swing` → Android View 系统
   - `java.util.logging` → `android.util.Log`

2. **网络请求**:
   ```java
   // 服务端
   HttpClient client = HttpClient.newHttpClient();
   
   // Android - 推荐 OkHttp 或 Retrofit
   OkHttpClient client = new OkHttpClient();
   ```

3. **JSON 处理**:
   ```java
   // 服务端
   // Jackson/Gson 均可
   
   // Android - 推荐 Moshi 或 Kotlin Serialization
   val json = Json { ignoreUnknownKeys = true }
   ```

4. **异步处理**:
   ```java
   // 服务端
   CompletableFuture.supplyAsync(() -> fetchData())
   
   // Android - Kotlin 协程
   lifecycleScope.launch {
       val data = withContext(Dispatchers.IO) { fetchData() }
   }
   ```

### 工具链对比

| 工具 | OpenJDK | Android |
|------|---------|---------|
| 构建工具 | Maven/Gradle | Gradle (Android Plugin) |
| IDE | IntelliJ IDEA | Android Studio |
| 测试 | JUnit 5 | JUnit 4 + AndroidX Test |
| 依赖管理 | Maven Central | Google Maven + Maven Central |
| Lint | Checkstyle/SpotBugs | Android Lint |

### 相关资源

| 资源 | 链接 |
|------|------|
| Android 开发者文档 | https://developer.android.com/ |
| Android JDK 版本 | https://developer.android.com/about/versions |
| API 差异报告 | https://developer.android.com/sdk/api_diff |
| desugar_jdk_libs | https://github.com/google/desugar_jdk_libs |

---

## 3. GraalVM Native Image

### 与 HotSpot 对比

| 特性 | HotSpot JVM | GraalVM Native Image |
|------|-------------|---------------------|
| **启动** | ~100ms | ~5ms |
| **内存** | ~35MB | ~5MB |
| **预热** | 需要 JIT 预热 | 无预热 |
| **反射** | 完全支持 | 需要配置 |
| **动态类加载** | 完全支持 | 受限 |
| **C2 编译器** | 有 | 无 (AOT 编译) |

### 适用场景

| 场景 | 推荐平台 |
|------|----------|
| 长运行服务 | HotSpot (吞吐量更高) |
| Serverless | Native Image (启动快) |
| CLI 工具 | Native Image (响应快) |
| 微服务 | Native Image (资源少) |

### 迁移注意事项

1. **反射配置**: 需要 `reflect-config.json`
2. **动态代理**: 需要 `proxy-config.json`
3. **资源文件**: 需要 `resource-config.json`
4. **序列化**: 需要 `serialization-config.json`

> 详见 [GraalVM 文档](graalvm.md)

---

## 4. WebAssembly (Wasm)

Java 代码可编译为 WebAssembly 在浏览器中运行。

### 方案对比

| 方案 | 原理 | 状态 |
|------|------|------|
| **CheerpJ** | JVM → WASM + AOT | 活跃 |
| **TeaVM** | 字节码 → JavaScript/Wasm | 活跃 |
| **JWebAssembly** | 字节码 → Wasm | 维护中 |
| **Bytecoder** | 字节码 → Wasm | 活跃 |

### CheerpJ 示例

```html
<!-- 在浏览器中运行 Java Swing 应用 -->
<script src="cheerpj.js"></script>
<script>
cheerpjInit();
cheerpjRunMain("com.example.Main", "/app.jar");
</script>
```

### 限制

- 性能: 比 JVM 慢 2-10x
- 内存: 浏览器内存限制
- API: 部分 JDK API 不支持
- 调试: 体验较差

### 相关资源

| 资源 | 链接 |
|------|------|
| CheerpJ | https://leaningtech.com/cheerpj/ |
| TeaVM | https://teavm.org/ |
| Bytecoder | https://github.com/mirkosertic/Bytecoder |

---

## 5. 其他 JVM 语言

### 编译到 JVM 字节码

| 语言 | 特点 | 互操作性 |
|------|------|----------|
| **Kotlin** | Android 官方语言 | 100% 与 Java 互操作 |
| **Scala** | 函数式 + 面向对象 | 100% 与 Java 互操作 |
| **Groovy** | 动态类型 | 100% 与 Java 互操作 |
| **Clojure** | Lisp 方言 | 100% 与 Java 互操作 |

### 非 JVM 目标

| 语言 | 可编译目标 |
|------|-----------|
| **Kotlin** | JVM, Native, JavaScript |
| **Scala Native** | LLVM (无 JVM) |
| **GraalWasm** | Wasm 运行时 |

---

## 6. 选择指南

### 按目标平台选择

| 目标 | 推荐方案 |
|------|----------|
| 服务端/后端 | OpenJDK (HotSpot) |
| Android 应用 | Android SDK + Kotlin |
| iOS 应用 | Kotlin Multiplatform / Flutter |
| Serverless | GraalVM Native Image |
| CLI 工具 | GraalVM Native Image |
| 浏览器 | CheerpJ / TeaVM |
| 嵌入式 | Liberica Lite / Semeru |

### 按性能需求选择

| 需求 | 推荐方案 |
|------|----------|
| 最大吞吐量 | HotSpot + G1GC |
| 最低延迟 | Azul Prime (C4 GC) |
| 最快启动 | GraalVM Native Image |
| 最小内存 | GraalVM Native / OpenJ9 |
| 移动端性能 | Android ART |

---

## 7. 相关文档

- [JDK 发行版对比](README.md)
- [GraalVM 详细文档](graalvm.md)
- [性能优化指南](../by-topic/core/performance/)
- [云原生 Java](../by-topic/core/cloud-native/)

---

**最后更新**: 2026-03-21

**Sources**:
- [Android Developer Documentation](https://developer.android.com/)
- [GraalVM Native Image](https://www.graalvm.org/native-image/)
- [CheerpJ](https://leaningtech.com/cheerpj/)
- [TeaVM](https://teavm.org/)
