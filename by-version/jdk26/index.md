# JDK 26

> **状态**: 已发布 (GA) | **发布日期**: 2025-09-16 | **类型**: Feature Release

[![OpenJDK](https://img.shields.io/badge/OpenJDK-26-orange)](https://openjdk.org/projects/jdk/26/)
[![License](https://img.shields.io/badge/License-GPLv2--with--Classpath--Exception-blue)](https://openjdk.org/projects/jdk/26/)

---

## 快速导航

| 我想了解 | 链接 |
|---------|------|
| 所有 JEP 详细列表 | [JEP 汇总](./jeps.md) |
| 重要 PR 分析 | [Top 50 Commits](/prs/jdk26-top-prs.md) |
| 深度技术分析 | [深度分析文档](./deep-dive/) |
| 如何试用 | [快速开始](#快速开始) |
| 从 JDK 21 升级 | [迁移指南](./migration/from-21.md) |

---

## 版本概览

JDK 26 是继 JDK 21 (LTS) 之后的首个功能版本，包含多项重要改进：

| 特性 | 影响 | 详情 |
|------|------|------|
| **HTTP/3** | ⭐⭐⭐⭐⭐ | 基于 QUIC，0-RTT 连接恢复 |
| **G1 吞吐量提升** | ⭐⭐⭐⭐⭐ | +10-20% 吞吐量 |
| **分代 Shenandoah** | ⭐⭐⭐⭐ | -30% pause 时间 |
| **结构化并发** | ⭐⭐⭐⭐ | 第六次预览 |
| **原始类型模式匹配** | ⭐⭐⭐⭐ | 第四次预览 |
| **Compact Object Headers** | ⭐⭐⭐⭐ | -16% heap 开销 |

---

## 发布时间线

```
2024-03-14    Rampdown Phase 1 (特性冻结)
2024-06-13    Rampdown Phase 2 (代码冻结)
2024-07-16    Initial Release Candidate
2025-07-18    Final Release Candidate
2025-09-16    GA 发布
```

---

## 代码示例速览

### HTTP/3

```java
// 创建支持 HTTP/3 的客户端
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_3)  // 新增
    .build();

HttpResponse<String> response = client.send(
    HttpRequest.newBuilder(URI.create("https://example.com/")).build(),
    HttpResponse.BodyHandlers.ofString()
);
```

### 原始类型模式匹配

```java
// 之前需要包装类
if (obj instanceof Integer i) {
    int value = i.intValue();
}

// 现在可以直接使用原始类型
if (obj instanceof int i) {
    process(i);  // 无需拆箱
}

// 配合 switch 使用
String result = switch (value) {
    case int i -> "int: " + i;
    case long l -> "long: " + l;
    case double d -> "double: " + d;
    default -> "unknown";
};
```

### 结构化并发

```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Future<String> user = scope.fork(() -> fetchUser());
    Future<List<Order>> orders = scope.fork(() -> fetchOrders());

    scope.join();
    scope.throwIfFailed();

    return new Response(user.resultNow(), orders.resultNow());
}  // 自动关闭，取消未完成的任务
```

---

## JEP 汇总

### 语言特性

| JEP | 标题 | 状态 | 描述 |
|-----|------|------|------|
| [JEP 530](/jeps/jep-530.md) | Primitive Types in Patterns | 🔍 预览 | 模式匹配支持原始类型 |
| [JEP 526](/jeps/jep-526.md) | Lazy Constants | 🔍 预览 | 延迟常量初始化 |
| [JEP 512](/jeps/jep-512.md) | Compact Source Files | ✅ 正式 | 简化单文件源码 |
| [JEP 511](/jeps/jep-511.md) | Module Import Declarations | ✅ 正式 | 模块导入声明 |
| [JEP 500](/jeps/jep-500.md) | Make Final Mean Final | ✅ 正式 | 严格 final 语义 |

### 性能

| JEP | 标题 | 影响 | 描述 |
|-----|------|------|------|
| [JEP 522](/jeps/jep-522.md) | G1 GC Throughput | 🚀 +10-20% | Claim Table 机制 |
| [JEP 521](/jeps/jep-521.md) | Generational Shenandoah | 🚀 -30% pause | 分代收集 |
| [JEP 519](/jeps/jep-519.md) | Compact Object Headers | 🚀 -16% heap | 压缩对象头 |
| [JEP 514](/jeps/jep-514.md) | AOT Ergonomics | ⚡ 更快启动 | 自动 AOT 优化 |
| [JEP 515](/jeps/jep-515.md) | AOT Method Profiling | ⚡ 更好性能 | 方法级 AOT |

### 网络

| JEP | 标题 | 状态 | 描述 |
|-----|------|------|------|
| [JEP 517](/jeps/jep-517.md) | HTTP/3 | ✅ 正式 | QUIC 协议支持 |

### 并发

| JEP | 标题 | 状态 | 描述 |
|-----|------|------|------|
| [JEP 525](/jeps/jep-525.md) | Structured Concurrency | 🔍 预览 | 结构化并发 (第6次) |
| [JEP 506](/jeps/jep-506.md) | Scoped Values | 🔍 预览 | 作用域值 |
| [JEP 502](/jeps/jep-502.md) | Stable Values | ✅ 正式 | 稳定值 |
| [JEP 504](/jeps/jep-504.md) | Remove Applet API | ✅ 正式 | 移除 Applet API |

### 安全

| JEP | 标题 | 状态 | 描述 |
|-----|------|------|------|
| [JEP 510](/jeps/jep-510.md) | KDF API | ✅ 正式 | 密钥派生 API |
| [JEP 470](/jeps/jep-470.md) | PEM Encodings | ✅ 正式 | PEM 格式支持 |

> 图例: ✅ 正式发布 | 🔍 预览特性 (需要 `--enable-preview`) | 🚀 性能提升 | ⚡ 启动优化

---

[查看所有 JEP 详情 →](./jeps.md)

---

## 性能改进总览

| 领域 | 改进 | 数据 |
|------|------|------|
| **G1 GC** | 吞吐量提升 | +10-20% |
| **Shenandoah** | Pause 时间 | -30% |
| **对象头** | Heap 开销 | -16% |
| **启动时间** | AOT 优化 | ~5-10% |
| **HTTP/3** | 连接建立 | 1-RTT (vs 3-RTT) |

---

## 快速开始

### 下载安装

```bash
# 使用 SDKMAN
sdk install java 26

# 或从 Oracle/OpenJDK 下载
https://openjdk.org/projects/jdk/26/
```

### 启用预览特性

```bash
# 编译时启用预览特性
javac --release 26 --enable-preview MyClass.java

# 运行时启用预览特性
java --enable-preview MyClass
```

### HTTP/3 快速体验

```java
import java.net.http.*;
import java.net.URI;

public class Http3Demo {
    public static void main(String[] args) throws Exception {
        HttpClient client = HttpClient.newBuilder()
            .version(HttpClient.Version.HTTP_3)
            .build();

        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create("https://cloudflare.com/"))
            .build();

        HttpResponse<String> response = client.send(
            request,
            HttpResponse.BodyHandlers.ofString()
        );

        System.out.println("Version: " + response.version()); // HTTP_3
        System.out.println("Status: " + response.statusCode());
    }
}
```

### JVM 参数建议

```bash
# G1 GC (默认，获得吞吐量提升)
java -XX:+UseG1GC MyApp

# 分代 Shenandoah (低延迟场景)
java -XX:+UseShenandoahGC -XX:+ShenandoahGenerationalGC MyApp

# AOT 优化 (更快启动)
java -XX:AOTLibrary+ MyApp
```

---

## 相比 JDK 21 的新特性

### 网络

- **HTTP/3** (JEP 517)：基于 QUIC 协议，提升 UDP 场景性能
- **CUBIC 拥塞控制**：改进高延迟网络

### GC

- **G1 吞吐量提升** (JEP 522)：可达 10-20%
- **分代 Shenandoah** (JEP 521)：降低 pause 时间
- **ZGC NUMA-aware**：多插槽服务器优化

### 安全

- **ML-DSA Intrinsics**：后量子密码算法硬件加速
- **KDF API**：标准化的密钥派生接口

### 其他

- **Compact Object Headers**：减少 16% heap 开销
- **AOT 改进**：更好的启动性能和运行时性能

---

## 迁移指南

### 从 JDK 21 升级

#### ✅ 兼容性

JDK 26 与 JDK 21 具有良好的二进制兼容性，大部分应用可以直接运行。

#### ⚠️ 破坏性变更

| 变更 | 影响 | 建议 |
|------|------|------|
| Applet API 移除 | 使用 `javax.swing.JApplet` 的应用 | 迁移到现代 Web 技术 |
| Final 语义更严格 | 依赖 final 字段构造行为的代码 | 检查并修复 |

#### 🚀 推荐使用的新特性

| 场景 | 推荐特性 |
|------|----------|
| 网络应用 | HTTP/3 |
| I/O 密集 | 虚拟线程 + 结构化并发 |
| 大内存 | 分代 ZGC |
| 低延迟 | 分代 Shenandoah |
| 高吞吐 | G1 GC (自动优化) |

#### 🔧 性能调优建议

```bash
# 1. 默认使用 G1，自动获得吞吐量提升
java -XX:+UseG1GC MyApp

# 2. 大内存应用启用分代 ZGC
java -XX:+UseZGC -XX:+ZGenerational MyApp

# 3. 低延迟应用使用分代 Shenandoah
java -XX:+UseShenandoahGC -XX:+ShenandoahGenerationalGC MyApp

# 4. 微服务优化启动时间
java -XX:AOTLibrary+ -XX:ArchiveClassesAtExit=app.jsa MyApp
```

---

## 重要非 JEP 改动

详见 [JDK 26 Top 50 Commits](/prs/jdk26-top-prs.md)

| Issue | 改动 | 影响 |
|-------|------|------|
| 8354548 | CLDR 48.0 | 本地化数据更新 |
| 8375057 | HarfBuzz 12.3.2 | 文本渲染优化 |
| 8373290 | FreeType 2.14.1 | 字体渲染更新 |
| 8346944 | Unicode 17.0.0 | 最新 Unicode 支持 |
| 8376186 | VectorAPI 重命名 | API 一致性改进 |
| 8351159 | 32位 x86 清理 | 移除遗留代码 |

---

## 相关链接

| 资源 | 链接 |
|------|------|
| **官方发布计划** | [openjdk.org/projects/jdk/26](https://openjdk.org/projects/jdk/26/) |
| **JEP 完整列表** | [openjdk.org/jeps/0](https://openjdk.org/jeps/0) |
| **官方下载** | [openjdk.org](https://openjdk.org/projects/jdk/26/) |
| **发布公告** | [openjdk.org/blog](https://openjdk.org/blog/) |

---

## 更多阅读

- [JDK 26 JEP 汇总](./jeps.md) - 所有 JEP 详细列表
- [Top 50 Commits](/prs/jdk26-top-prs.md) - 重要的代码变更
- [按主题浏览](/by-topic/) - 跨版本追踪技术演进
- [按贡献者浏览](../../by-contributor/) - 了解贡献者和他们的工作
