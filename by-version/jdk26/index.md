# JDK 26

> **状态**: 已发布 (GA) | **发布日期**: 2026-03-17 | **类型**: Feature Release

[![OpenJDK](https://img.shields.io/badge/OpenJDK-26-orange)](https://openjdk.org/projects/jdk/26/)
[![License](https://img.shields.io/badge/License-GPLv2--with--Classpath--Exception-blue)](https://openjdk.org/projects/jdk/26/)

---
## 目录

1. [快速导航](#1-快速导航)
2. [版本概览](#2-版本概览)
3. [发布时间线](#3-发布时间线)
4. [代码示例速览](#4-代码示例速览)
5. [JEP 汇总](#5-jep-汇总)
6. [性能改进总览](#6-性能改进总览)
7. [快速开始](#7-快速开始)
8. [相比 JDK 21 的新特性](#8-相比-jdk-21-的新特性)
9. [迁移指南](#9-迁移指南)
10. [核心贡献者](#10-核心贡献者)
11. [相关主题](#11-相关主题)
12. [贡献者统计](#12-贡献者统计)
13. [重要非 JEP 改动](#13-重要非-jep-改动)
14. [重要 PR 分析](#14-重要-pr-分析)
15. [相关链接](#15-相关链接)
16. [更多阅读](#16-更多阅读)

---


## 1. 快速导航

| 我想了解 | 链接 |
|---------|------|
| 所有 JEP 详细列表 | [JEP 汇总](./jeps.md) |
| 重要 PR 分析 | [Top 50 Commits](/by-pr/jdk26-top-prs.md) |
| 深度技术分析 | [深度分析文档](./deep-dive/) |
| 发布说明 | [完整 Release Notes](./release-notes.md) |
| 贡献者排名 | [Top 贡献者](/by-contributor/profiles/jdk26-top-contributors.md) |
| 如何试用 | [快速开始](#快速开始) |
| 从 JDK 21 升级 | [迁移指南](./migration/from-21.md) |

### 深度分析文章

| 主题 | 链接 |
|------|------|
| HTTP/3 实现原理 | [→](./deep-dive/http3-implementation.md) |
| G1 GC 吞吐量提升 | [→](./deep-dive/g1-gc-throughput.md) |
| AOT 对象缓存详解 | [→](./deep-dive/aot-improvements.md) |
| String 构造函数优化 | [→](./deep-dive/string-constructor-optimization.md) |
| 结构化并发详解 | [→](./deep-dive/structured-concurrency.md) |
| 原始类型模式匹配 | [→](./deep-dive/primitive-pattern-matching.md) |
| Vector API 改进 | [→](./deep-dive/vectorapi-improvements.md) |

---

## 2. 版本概览

JDK 26 是继 JDK 25 (LTS) 之后的首个功能版本，包含多项重要改进：

| 特性 | 影响 | 详情 |
|------|------|------|
| **HTTP/3** | ⭐⭐⭐⭐⭐ | 基于 QUIC，支持会话恢复时 0-RTT |
| **G1 吞吐量提升** | ⭐⭐⭐⭐⭐ | 特定工作负载下 +10-20% 吞吐量 |
| **AOT 对象缓存** | ⭐⭐⭐⭐ | 任意 GC 的 AOT 支持 |
| **结构化并发** | ⭐⭐⭐⭐ | 第六次预览 |
| **原始类型模式匹配** | ⭐⭐⭐⭐ | 第四次预览 |
| **延迟常量** | ⭐⭐⭐ | 第二次预览 |
| **Vector API** | ⭐⭐⭐ | 第十一次孵化 |
| **严格 final 语义** | ⭐⭐⭐ | 准备未来版本 |

---

## 3. 发布时间线

```
2025-12-04    Rampdown Phase 1 (特性冻结)
2026-01-15    Rampdown Phase 2 (代码冻结)
2026-02-05    Initial Release Candidate
2026-02-19    Final Release Candidate
2026-03-17    GA 发布
```

---

## 4. 代码示例速览

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

// 配合 switch 使用 (value 类型为 long)
String result = switch (value) {
    case int i -> "int: " + i;    // 窄化匹配
    case long l -> "long: " + l;
    default -> "other";
};
```

### 结构化并发

```java
try (var scope = StructuredTaskScope.open(Joiner.allSuccessfulOrThrow())) {
    Subtask<String> user = scope.fork(() -> fetchUser());
    Subtask<List<Order>> orders = scope.fork(() -> fetchOrders());

    scope.join();

    return new Response(user.get(), orders.get());
}  // 自动关闭，取消未完成的任务
```

---

## 5. JEP 汇总

### 语言特性

| JEP | 标题 | 状态 | 描述 |
|-----|------|------|------|
| [JEP 530](https://openjdk.org/jeps/530) | Primitive Types in Patterns | 🔍 预览 | 模式匹配支持原始类型 (第4次) |
| [JEP 526](https://openjdk.org/jeps/526) | Lazy Constants | 🔍 预览 | 延迟常量初始化 (第2次) |
| [JEP 500](https://openjdk.org/jeps/500) | Prepare to Make Final Mean Final | ✅ 正式 | 严格 final 语义 |

### 并发

| JEP | 标题 | 状态 | 描述 |
|-----|------|------|------|
| [JEP 525](https://openjdk.org/jeps/525) | Structured Concurrency | 🔍 预览 | 结构化并发 (第6次预览) |

### 性能

| JEP | 标题 | 影响 | 描述 |
|-----|------|------|------|
| [JEP 522](https://openjdk.org/jeps/522) | G1 GC Throughput | 🚀 特定工作负载下 +10-20% | 减少同步提升吞吐量 |
| [JEP 516](https://openjdk.org/jeps/516) | AOT Object Caching | ⚡ 更快启动 | 任意 GC 的 AOT 缓存 |
| [JEP 529](https://openjdk.org/jeps/529) | Vector API | 🔬 孵化 | 向量 API (第11次) |

### 网络

| JEP | 标题 | 状态 | 描述 |
|-----|------|------|------|
| [JEP 517](https://openjdk.org/jeps/517) | HTTP/3 Client | ✅ 正式 | QUIC 协议支持 |

### 安全

| JEP | 标题 | 状态 | 描述 |
|-----|------|------|------|
| [JEP 524](https://openjdk.org/jeps/524) | PEM Encodings | 🔍 预览 | PEM 格式支持 (第2次) |

### 移除功能

| JEP | 标题 | 状态 | 描述 |
|-----|------|------|------|
| [JEP 504](https://openjdk.org/jeps/504) | Remove Applet API | ✅ 正式 | 移除过时的 Applet API |

> 图例: ✅ 正式发布 | 🔍 预览特性 (需要 `--enable-preview`) | 🚀 性能提升 | ⚡ 启动优化

---

[查看所有 JEP 详情 →](./jeps.md)

---

## 6. 性能改进总览

| 领域 | 改进 | 数据 |
|------|------|------|
| **G1 GC** | 吞吐量提升 | 特定工作负载下 +10-20% (减少同步) |
| **启动时间** | AOT 对象缓存 | 减少类加载和对象初始化开销 |
| **HTTP/3** | 连接建立 | 会话恢复时 0-RTT (vs TCP+TLS 1.3 新连接 2-3 RTT) |

---

## 7. 快速开始

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

# AOT 对象缓存 (更快启动，支持任意 GC)
java -XX:AOTCache=app.aot MyApp

# 查看实际使用的 HTTP 版本
java -Djdk.httpclient.HttpClient.log=all,headers:verbose MyApp
```

---

## 8. 相比 JDK 21 的新特性

### 网络

- **HTTP/3** (JEP 517)：基于 QUIC 协议，支持会话恢复时 0-RTT

### GC

- **G1 吞吐量提升** (JEP 522)：减少同步开销，特定工作负载下提升 10-20% 吞吐量
- **AOT 对象缓存** (JEP 516)：支持任意 GC 的 AOT 缓存

### 安全

- **PEM 编码格式** (JEP 524)：标准化密钥和证书的 PEM 编码

### 语言

- **原始类型模式匹配** (JEP 530)：支持 int/long/double 等原始类型
- **延迟常量** (JEP 526)：按需延迟初始化的常量
- **严格 final 语义** (JEP 500)：禁止深度反射修改 final 字段

### 并发

- **结构化并发** (JEP 525)：第六次预览，API 更稳定

### 其他

- **Vector API** (JEP 529)：第十一次孵化，SIMD 编程支持
- **移除 Applet API** (JEP 504)：清理过时代码

---

## 9. 迁移指南

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
| 网络应用 | HTTP/3 (QUIC 协议) |
| I/O 密集 | 虚拟线程 + 结构化并发 |
| 微服务 | AOT 对象缓存 |
| 高吞吐 | G1 GC (自动优化) |

#### 🔧 性能调优建议

```bash
# 1. 默认使用 G1，自动获得吞吐量提升
java -XX:+UseG1GC MyApp

# 2. 启用 AOT 对象缓存 (所有 GC)
java -XX:AOTCache=app.aot MyApp

# 3. 微服务优化启动时间 (先录制，再使用)
java -XX:AOTConfiguration=app.aotconf MyApp
java -XX:AOTCache=app.aot -XX:AOTConfiguration=app.aotconf MyApp

# 4. 启用 HTTP/3 (HttpClient 自动协商)
# 无需额外参数，确保服务端支持 QUIC
```

---

## 10. 核心贡献者

> **相关链接**: [JDK 26 Top 贡献者详解](/by-contributor/profiles/jdk26-top-contributors.md)

### Oracle 核心开发者

| 贡献者 | 专长领域 | 详细资料 |
|--------|----------|----------|
| [Brian Goetz](/by-contributor/profiles/brian-goetz.md) | Java 语言架构师、结构化并发 | → |
| [Joe Darcy](/by-contributor/profiles/joe-darcy.md) | 语言特性、JEP 领导 | → |
| [Coleen Phillimore](/by-contributor/profiles/coleen-phillimore.md) | 类加载、运行时 | → |
| [David Holmes](/by-contributor/profiles/david-holmes.md) | 并发、线程 | → |
| [Ioi Lam](/by-contributor/profiles/ioi-lam.md) | CDS、类加载 | → |

### GC 团队

| 贡献者 | 专长 | 详细资料 |
|--------|------|----------|
| [Thomas Stuefe](/by-contributor/profiles/thomas-stuefe.md) | Metaspace、CDS | → |
| [Kim Barrett](/by-contributor/profiles/kim-barrett.md) | GC 架构 | → |
| Per Lofgren | G1 GC | → |

### JIT/编译器团队

| 贡献者 | 专长 | 详细资料 |
|--------|------|----------|
| [Roland Westrelin](/by-contributor/profiles/rooland-westrelin.md) | C2 JIT、循环优化 | → |
| [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | MergeStore 优化 | → |
| Vladimir Kozlov | C2 编译器负责人 | → |

### 中国贡献者

| 贡献者 | 组织 | 专长 | 详细资料 |
|--------|------|------|----------|
| [Shaojin Wen (温绍锦)](/by-contributor/profiles/shaojin-wen.md) | Alibaba | JIT 优化、字符串 | → |

### Red Hat 贡献者

| 贡献者 | 专长 | 详细资料 |
|--------|------|----------|
| [Andrew Dinn](/by-contributor/profiles/andrew-dinn.md) | JIT 编译 | → |

### Datadog 贡献者

| 贡献者 | 专长 | 详细资料 |
|--------|------|----------|
| [Roman Kennke](/by-contributor/profiles/roman-kennke.md) | Shenandoah GC | → |

---

## 11. 相关主题

| 主题 | 说明 | 链接 |
|------|------|------|
| **GC 演进** | G1、ZGC、Shenandoah | [→](/by-topic/core/gc/) |
| **JIT 编译** | C2、MergeStore、分层编译 | [→](/by-topic/core/jit/) |
| **并发编程** | 虚拟线程、结构化并发 | [→](/by-topic/concurrency/concurrency/) |
| **网络编程** | HTTP/3、HttpClient | [→](/by-topic/concurrency/network/) |
| **安全特性** | KDF API、后量子密码 | [→](/by-topic/security/security/) |

---

## 12. 贡献者统计

> **数据来源**: Oracle 官方博客 "The Arrival of Java 26"
> **统计时间**: JDK 26 GA 发布 (2026-03-17)

### JDK 26 贡献分布

| 组织 | JIRA 问题数 | 占比 | 说明 |
|------|------------|------|------|
| **Oracle** | 1,729 | 68.2% | 主要贡献者 |
| **其他社区** | 806 | 31.8% | 社区联合贡献 |

### Top 10 贡献组织

> **统计时间**: 2025-06 至 2026-03 (JDK 26 开发周期)
> **总提交数**: 3,936 | **活跃贡献者**: ~380 人

| 排名 | 组织 | 提交数 | 贡献者数 | 主要贡献领域 |
|------|------|--------|----------|-------------|
| 1 | **Oracle** | ~3,200 | ~60 | 全栈 JVM、GC、语言特性、核心库 |
| 2 | **SAP** | 73 | 2 | ZGC、JFR、性能分析 |
| 3 | **Alibaba** | 74 | 8 | JIT 优化、字符串处理、GC、测试 |
| 4 | **Red Hat** | 69 | 3 | Shenandoah、RISC-V、Linux 支持 |
| 5 | **Amazon** | 43 | 1 | Shenandoah GC |
| 6 | **NTT DATA** | 32 | 1 | 服务能力、工具 |
| 7 | **Google** | 14 | 3 | 构建系统、javac、并发 |
| 8 | **ARM** | 4 | 1 | ARM 架构构建支持 |
| 9 | **Oracle Labs** | 15 | 2 | Graal、Truffle |
| 10 | **独立贡献者** | ~300 | ~280 | 测试、安全、各领域 |

### 重点组织贡献详情

#### Oracle (68.2%)
- **3,200+ 提交**，~60 位核心开发者
- 主要领域: G1 GC、C2 编译器、核心库、HTTP/3、类加载

#### Alibaba (1.9%)
- **74 提交**，8 位贡献者
- 代表: Shaojin Wen (11), Yude Lin (10), Xiaowei Lu (10), Tongbao Zhang (9)
- 主要领域: JIT 优化、字符串处理、GC、测试

#### Red Hat (1.0%)
- **39 提交**，2 位贡献者
- 代表: Andrew Haley (20)
- 主要领域: RISC-V 架构

#### Datadog
- **30 提交**，1 位贡献者
- 代表: Roman Kennke (30)
- 主要领域: Shenandoah GC

#### SAP (1.9%)
- **73 提交**，2 位贡献者
- 代表: Axel Boldt-Christmas (52)
- 主要领域: ZGC、JFR

#### Amazon (1.1%)
- **43 提交**，1 位贡献者 (William Kemper)
- 主要领域: Shenandoah GC

### 其他贡献组织

| 组织 | 提交数 | 贡献者数 | 说明 |
|------|--------|----------|------|
| **ISCAS (中科院软件所)** | - | - | PLCT 实验室、LoongArch 移植 |
| **Rivos** | - | - | RISC-V 架构支持 |
| **Bellsoft** | - | - | Liberica JDK 发行版维护 |
| **Loongson (龙芯)** | - | - | 国产 CPU 架构支持 |
| **University of Washington** | 4 | 1 | javac 编译器研究 |

### 独立贡献者

**独立/未归属贡献者** 占比约 7.6%，~300 位贡献者：

| 贡献者 | 提交数 | 主要领域 |
|--------|--------|----------|
| SendaoYan | 71 | 测试 |
| Quan Anh Mai | 26 | 类型系统 |
| Anton Seoane Ampudia | 24 | x86 清理 |
| Artur Barashev | 18 | 安全 |
| Oleg Pekhovskiy | 7 | 测试 |
| Sergey Tsypanov | 6 | 安全 |
| Pavel Rappo | 6 | 核心库 |
| Peter Levart | 5 | 核心库 |

### 历史对比 (JDK 11 - JDK 26)

| 指标 | 数值 | Oracle | 社区 |
|------|------|--------|------|
| 总 JIRA 问题 | 36,328 | 25,491 (70.2%) | 10,837 (29.8%) |

> **说明**: 从 JDK 11 到 JDK 26，Oracle 贡献约 70% 的代码，社区贡献约 30%。JDK 26 的社区贡献比例 (31.8%) 略高于历史平均水平，显示出 OpenJDK 社区的持续增长。

### 社区质量贡献特别感谢

Oracle 特别感谢以下个人和项目对 JDK 26 质量保证的贡献：

| 个人/项目 | 贡献 |
|-----------|------|
| **Lukas Eder** | JOOQ |
| **Marc Hoffmann** | JaCoCo |
| **Ben Evans** | Java Champion |
| **Simon Steiner** | Apache Batik |
| **Uwe Schindler** | Apache Lucene |
| **Yoann Rodiere** | Hibernate ORM |
| **Apache Ant** | Jaikiran Pai |
| **Apache Tomcat** | Mark Thomas |
| **Parallel Collectors & Vavr** | Grzegorz Piwowarek |

---

## 13. 重要非 JEP 改动

详见 [JDK 26 Top 50 Commits](/by-pr/jdk26-top-prs.md)

| Issue | 改动 | 影响 |
|-------|------|------|
| 8346944 | Unicode 17.0.0 | 最新 Unicode 支持 |
| 8354548 | CLDR 48.0 | 本地化数据更新 |
| 8375057 | HarfBuzz 12.3.2 | 文本渲染优化 |
| 8373290 | FreeType 2.14.1 | 字体渲染更新 |

---

## 14. 重要 PR 分析

> **完整列表**: [JDK 26 Top 50 Commits](/by-pr/jdk26-top-prs.md)

### JEP 实现

| PR | 标题 | 贡献者 | 分析 |
|----|------|--------|------|
| JDK-8349910 | HTTP/3 (JEP 517) | [Daniel Fuchs](/by-contributor/profiles/daniel-fuchs.md) | [→](./deep-dive/http3-implementation.md) |
| JDK-8342382 | G1 GC Throughput (JEP 522) | Thomas Schatzl | [→](./deep-dive/g1-gc-throughput.md) |
| JDK-8365932 | AOT Caching (JEP 516) | Erik Österlund | [→](./deep-dive/aot-improvements.md) |
| JDK-8366178 | Lazy Constants (JEP 526) | [Per Minborg](/by-contributor/profiles/per-minborg.md) | [→](/by-pr/) |
| JDK-8353835 | Final Mean Final (JEP 500) | Alan Bateman | [→](/by-pr/) |

### JIT 优化

| PR | 标题 | 贡献者 | 分析 |
|----|------|--------|------|
| JDK-8318446 | MergeStore 初始实现 | [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | [→](/by-topic/core/jit/mergestore.md) |
| JDK-8333893 | StringBuilder boolean/null | [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) | [→](/by-pr/8333/8333893.md) |
| JDK-8336856 | 隐藏类拼接策略 | Shaojin Wen | [→](/by-pr/8336/8336856.md) |

---

## 15. 相关链接

| 资源 | 链接 |
|------|------|
| **官方发布计划** | [openjdk.org/projects/jdk/26](https://openjdk.org/projects/jdk/26/) |
| **JEP 完整列表** | [openjdk.org/jeps/0](https://openjdk.org/jeps/0) |
| **官方下载** | [openjdk.org](https://openjdk.org/projects/jdk/26/) |
| **发布公告** | [openjdk.org/blog](https://openjdk.org/blog/) |

---

## 16. 更多阅读

### 版本相关

- [JDK 26 JEP 汇总](./jeps.md) - 所有 JEP 详细列表
- [JDK 26 Release Notes](./release-notes.md) - 完整发布说明
- [JDK 26 Top 50 Commits](/prs/jdk26-top-prs.md) - 重要的代码变更
- [从 JDK 21 迁移](./migration/from-21.md) - 升级指南

### 深度分析

- [HTTP/3 实现原理](./deep-dive/http3-implementation.md) - QUIC 协议详解
- [G1 GC 吞吐量提升](./deep-dive/g1-gc-throughput.md) - Claim Table 机制
- [结构化并发详解](./deep-dive/structured-concurrency.md) - API 设计与使用
- [原始类型模式匹配](./deep-dive/primitive-pattern-matching.md) - 语言特性演进
- [AOT 改进详解](./deep-dive/aot-improvements.md) - 启动性能优化
- [Vector API 改进](./deep-dive/vectorapi-improvements.md) - SIMD 编程

### 按主题浏览

- [JIT 编译优化](/by-topic/core/jit/) - C2 编译器、MergeStore
- [GC 演进历史](/by-topic/core/gc/) - G1、ZGC、Shenandoah
- [并发编程](/by-topic/concurrency/concurrency/) - 虚拟线程、结构化并发
- [网络编程](/by-topic/concurrency/network/) - HTTP/3、HttpClient
- [安全特性](/by-topic/security/security/) - KDF API、后量子密码
- [语言特性](/by-topic/language/) - 模式匹配、Records

### 贡献者

- [JDK 26 Top 贡献者](/by-contributor/profiles/jdk26-top-contributors.md)
- [所有贡献者列表](/by-contributor/)
- [中国贡献者](/by-contributor/profiles/chinese-contributors.md)

---

**Sources**:
- [OpenJDK JDK 26 Project](https://openjdk.org/projects/jdk/26/)
- [JDK 26 JEPs](https://openjdk.org/jeps/)
