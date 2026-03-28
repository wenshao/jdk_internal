# JDK Internal Docs

> 分析 OpenJDK 源码、Issue、PR，沉淀便于人类和 AI 阅读的文档

> **数据规模**: 43,394 PRs / 25 仓库 / 22,560 PR 分析 / 387 JEP / 260 贡献者档案 / 21 组织 / 13 发行版

---

## 1. 你在用哪个版本？

| 版本 | 类型 | 发布时间 | 支持截止 | 文档 |
|------|------|----------|----------|------|
| **JDK 8** | LTS | 2014-03 | 2030-12 (付费) | [进入](by-version/jdk8/) |
| **JDK 11** | LTS | 2018-09 | 2027-10 | [进入](by-version/jdk11/) |
| **JDK 17** | LTS | 2021-09 | 2029-10 | [进入](by-version/jdk17/) |
| **JDK 21** | LTS | 2023-09 | 2031-10 | [进入](by-version/jdk21/) |
| **JDK 25** | LTS | 2025-09-16 | 2032+ | [进入](by-version/jdk25/) |
| **JDK 26** | Feature | 2026-03-17 | - | [进入](by-version/jdk26/) |

---

## 2. 我想了解...

### 核心平台

| 主题 | 版本范围 | 查看 | 亮点 |
|------|----------|------|------|
| **GC 演进** | 8 → 26 | [G1/ZGC/Shenandoah 时间线](by-topic/core/gc/) | 分代 ZGC, G1 +10-20% |
| **内存管理** | 8 → 26 | [堆/栈/Metaspace/Compressed Oops](by-topic/core/memory/) | 紧凑对象头 -33% (12→8字节) |
| **JIT 编译** | 8 → 26 | [C1/C2/Graal 分层编译](by-topic/core/jit/) | 内联优化, 逃逸分析 |
| **类加载器** | 8 → 26 | [双亲委派/模块化/CDS](by-topic/core/classloading/) | AppCDS 启动 +20% |
| **模式匹配** | 14 → 26 | [类型模式/Record 模式/守卫](by-topic/core/patterns/) | instanceof/switch/解构 |
| **泛型系统** | 5 → 26 | [类型参数/通配符/类型擦除](by-topic/core/generics/) | PECS 原则 |
| **Record 类型** | 14 → 26 | [不可变数据载体/解构](by-topic/core/records/) | 字节码 -30% |
| **模块系统** | 9+ | [JPMS/module-info/jlink](by-topic/core/modules/) | 强封装 |

### 语言特性

| 主题 | 版本范围 | 查看 | 亮点 |
|------|----------|------|------|
| **语法演进** | 8 → 26 | [泛型/Lambda/Record/Pattern Matching](by-topic/language/syntax/) | Switch 表达式, 密封类 |
| **Lambda** | 8 → 26 | [函数式编程/invokedynamic](by-topic/language/lambda/) | 生成优化 +15-20% |
| **Stream API** | 8 → 26 | [函数式数据处理/并行流](by-topic/language/streams/) | Gatherers (JDK 22+) |
| **字符串处理** | 8 → 26 | [String 优化历程](by-topic/language/string/) | Compact Strings 节省 20-30% 堆内存 |
| **Class File API** | 22 → 26 | [标准字节码 API](by-topic/language/classfile/) | 替代 ASM |
| **反射与元数据** | 8 → 26 | [反射/注解/MethodHandle](by-topic/language/reflection/) | 变量引用 |

### 并发网络

| 主题 | 版本范围 | 查看 | 亮点 |
|------|----------|------|------|
| **并发编程** | 8 → 26 | [Thread → VirtualThread](by-topic/concurrency/concurrency/) | 虚拟线程 (JDK 21) |
| **HTTP 客户端** | 11+ | [HttpURLConnection → HTTP/3](by-topic/concurrency/http/) | HTTP/3 正式版 (JDK 26) |
| **网络编程** | 8 → 26 | [Socket/NIO/Unix Domain](by-topic/concurrency/network/) | 异步 I/O |
| **日期时间** | 8+ | [JSR 310/LocalDate/ZonedDateTime](by-topic/datetime/) | 不可变 API |

### 安全特性

| 主题 | 版本范围 | 查看 |
|------|----------|------|
| **安全特性** | 8 → 26 | [TLS/加密/后量子密码](by-topic/security/security/) |
| **国际化** | 8 → 26 | [Locale/ResourceBundle/Unicode](by-topic/security/i18n/) |

### 实战案例

| 案例 | 场景 | 核心技术 |
|------|------|---------|
| [GC 调优实战](cases/gc-tuning-case.md) | G1→ZGC 迁移, P99 200ms→5ms | GC 日志分析, ZGC |
| [虚拟线程迁移](cases/virtual-threads-migration.md) | Spring Boot 线程池→虚拟线程 | Virtual Threads, Semaphore |
| [启动优化](cases/startup-optimization.md) | 12s→1.5s, CDS/AOT | AppCDS, AOT Cache |
| [内存泄漏排查](cases/memory-leak-diagnosis.md) | JFR+NMT+MAT 排查 | OldObjectSample, NMT |

### 源码深入分析

| 主题 | JEP | 核心内容 |
|------|-----|---------|
| [Virtual Thread 实现](deep-dive/virtual-thread-implementation.md) | JEP 444 | 20 状态机, mount/unmount, ForkJoinPool |
| [Scoped Values 实现](deep-dive/jep-506-implementation.md) | JEP 506 | Carrier 链表, 2-way cache, ScopedValueContainer |
| [Compact Object Headers](deep-dive/jep-519-implementation.md) | JEP 519 | mark word 位布局, narrowKlass 编码 |
| [HTTP/3 实现](deep-dive/jep-517-implementation.md) | JEP 517 | QUIC, QPACK, Http3Connection |
| [G1 吞吐量优化](deep-dive/jep-522-implementation.md) | JEP 522 | 双卡表, ClaimTable |
| [Module Import 编译器实现](deep-dive/jep-511-implementation.md) | JEP 511 | JCModuleImport, TypeEnter |

---

## 3. 贡献者与组织分析

### 数据资产

| 数据 | 规模 | 入口 |
|------|------|------|
| **PR 分析** | 22,560 文档 (P1-P4 含描述/文件/评论) | [by-pr/](by-pr/) |
| **JEP 分析** | 387 文档 (含关联 PR) | [jeps/](jeps/) |
| **贡献者档案** | 260 人 (含审查统计/CFV 晋升) | [by-contributor/profiles/](by-contributor/profiles/) |
| **组织页面** | 21 个 (含 LTS 维护/审查网络) | [contributors/orgs/](contributors/orgs/) |
| **发行版文档** | 17 个 (含维护团队/Docker 统计) | [distributions/](distributions/) |
| **统计报告** | 23 个 (全量 43K 数据) | [contributors/stats/](contributors/stats/) |

### 实验性项目

| 项目 | 主导 | PRs | 目标 | 文档 |
|------|------|-----|------|------|
| [Valhalla](valhalla/contributors.md) | Oracle | 2,082 | Value Types | [分析](valhalla/contributors.md) |
| [Panama](panama-foreign/contributors.md) | Oracle | 817 | FFM API | [分析](panama-foreign/contributors.md) |
| [Babylon](babylon/contributors.md) | Oracle | 910 | GPU/Code Reflection | [分析](babylon/contributors.md) |
| [Shenandoah](shenandoah/contributors.md) | Amazon | 482 | Low-pause GC | [分析](shenandoah/contributors.md) |
| [CRaC](crac/contributors.md) | Azul | 251 | 检查点恢复 | [分析](crac/contributors.md) |
| [Lilliput](lilliput/contributors.md) | Datadog | 147 | Compact Headers | [分析](lilliput/contributors.md) |
| [JFX](jfx/contributors.md) | Oracle | 1,782 | JavaFX GUI | [分析](jfx/contributors.md) |
| [JMC](jmc/contributors.md) | Datadog | 626 | Mission Control | [分析](jmc/contributors.md) |

### 重点报告

| 报告 | 说明 |
|------|------|
| [跨仓库全景](contributors/stats/cross-repo-overview.md) | 25 仓库 43,394 PRs 完整分析 |
| [组织间审查矩阵](contributors/stats/cross-org-collaboration.md) | 谁审查谁的代码 |
| [Top 50 贡献者](contributors/stats/top50.md) | 全仓库排名 (GoeLin 3,927 居首) |
| [LTS 维护分析](contributors/stats/lts-maintenance.md) | SAP 5,264 PRs 主导 LTS 维护 |
| [角色晋升网络](contributors/stats/role-promotions.md) | 193 CFV 提名 + 投票者分析 |
| [JEP 领导力](contributors/stats/jep-tracking.md) | 500 JEPs / 161 owners |
| [Docker 下载量](distributions/docker-popularity.md) | Temurin 8.5 亿次居首 |
| [GitHub 社区热度](distributions/github-popularity.md) | Dragonwell 4,319 stars 居首 |

---

## 4. 快速导航

### 按浏览方式

| 方式 | 说明 | 链接 |
|------|------|------|
| **按版本** | 从你使用的 JDK 版本切入 | [浏览版本](by-version/) |
| **按主题** | 跨版本追踪某个技术演进 | [浏览主题](by-topic/) |
| **按贡献者** | 了解贡献者和他们的工作 | [浏览贡献者](by-contributor/) |
| **按 PR** | 深入具体 Issue/PR | [浏览 PR](by-pr/) |
| **按 JEP** | JDK Enhancement Proposals | [浏览 JEP](jeps/) |
| **按 JSR** | Java Specification Requests | [浏览 JSR](jsr/) |
| **技术演讲** | JVMLS 等会议演讲 | [浏览演讲](talks/) |
| **实战案例** | GC 调优、虚拟线程迁移等 | [浏览案例](cases/) |
| **源码深入** | JEP 实现源码分析 | [浏览深入分析](deep-dive/) |
| **Issue 分析** | 性能/稳定性问题深度分析 | [浏览 Issue](issues/) |
| **性能基准** | Benchmark 方法论与结果 | [浏览基准](benchmarks/) |
| **故障排查** | JVM 问题诊断与修复 | [浏览排查指南](troubleshooting/) |
| **最佳实践** | 生产环境实践建议 | [浏览最佳实践](best-practices/) |
| **技术对比** | 锁/CDS/Profiler/IO 对比 | [浏览对比](guides/comparisons/) |

### 按角色

| 角色 | 推荐阅读 |
|------|----------|
| **开发者** | [学习路径](guides/learning-path.md) |
| **架构师** | [主题演进](by-topic/) |
| **运维** | [版本迁移](guides/migration-guide.md) · [JDK 17→25 直升](by-version/jdk25/migration/from-17.md) |
| **初学者** | [JDK 8 入门](by-version/jdk8/) |
| **研究者** | [Agent 研究方法](AGENTS.md) |

---

## 目录结构

```
jdk_internal/
├── AGENTS.md              # Agent 研究方法论
├── README.md              # 项目概览（本文件）
│
├── by-version/            # 按版本浏览
│   ├── README.md           # 版本概览和对比
│   ├── jdk8/              # JDK 8 (LTS 2014)
│   ├── jdk9-24/           # JDK 9-24 (中间版本)
│   ├── jdk25/             # JDK 25 (LTS 2025)
│   └── jdk26/             # JDK 26 (Feature 2026-03)
│
├── by-topic/              # 按主题跨版本
│   ├── README.md           # 主题索引
│   ├── core/              # 核心平台
│   │   ├── gc/            # GC 演进 (G1/ZGC/Shenandoah)
│   │   ├── memory/        # 内存管理 (堆/栈/Metaspace)
│   │   ├── jit/           # JIT 编译 (C1/C2/Graal)
│   │   ├── performance/   # 性能优化 (JFR/调优)
│   │   ├── classloading/  # 类加载器 (双亲委派/CDS)
│   │   ├── patterns/      # 模式匹配 (类型/Record/守卫)
│   │   ├── generics/      # 泛型系统 (类型参数/通配符)
│   │   ├── records/       # Record 类型 (不可变数据)
│   │   ├── enums/         # 枚举类型 (switch 表达式)
│   │   ├── modules/       # 模块系统 (JPMS/jlink)
│   │   ├── amber/         # Project Amber (语言特性)
│   │   ├── loom/          # Project Loom (虚拟线程)
│   │   ├── panama/        # Project Panama (Foreign Function)
│   │   ├── valhalla/      # Project Valhalla (值类型)
│   │   └── vector-api/    # Vector API
│   ├── language/          # 语言特性
│   │   ├── syntax/        # 语法演进 (泛型/Lambda/Record)
│   │   ├── lambda/        # Lambda 表达式 (函数式编程)
│   │   ├── streams/       # Stream API (流式处理)
│   │   ├── string/        # 字符串处理 (优化历程)
│   │   ├── reflection/    # 反射与元数据
│   │   ├── annotations/   # 注解与元编程
│   │   └── classfile/     # Class File API
│   ├── api/               # API 框架
│   │   ├── collections/   # 集合框架
│   │   ├── io/            # I/O 处理
│   │   ├── datetime/      # 日期时间 (JSR 310)
│   │   ├── jdbc/          # JDBC
│   │   ├── logging/       # 日志 API
│   │   └── xml-json/      # XML/JSON 处理
│   ├── concurrency/       # 并发网络
│   │   ├── concurrency/   # 并发编程 (Thread/VirtualThread)
│   │   ├── http/          # HTTP 客户端 (HTTP/3)
│   │   ├── network/       # 网络编程 (NIO/Unix Socket)
│   │   └── serialization/ # 序列化
│   ├── crypto/            # 加密
│   ├── math/              # 数学 API
│   ├── net/               # 网络基础
│   ├── nio/               # NIO
│   ├── platform/          # 平台特性
│   ├── datetime/          # 日期时间 (顶级)
│   └── security/          # 安全国际化
│       ├── security/      # 安全特性 (TLS/加密)
│       └── i18n/          # 国际化
│
├── by-contributor/        # 按贡献者
│   ├── README.md           # 贡献者索引
│   └── profiles/          # 个人详细页面
│
├── by-pr/                 # 按 PR/Issue 深度分析
│   ├── README.md           # PR 索引
│   └── {issue}/           # 按 issue 号分组
│
├── jeps/                  # JEP 详细分析
│   ├── README.md           # JEP 索引
│   ├── language/          # 语言相关 JEP
│   ├── core/              # 核心平台 JEP
│   ├── concurrency/       # 并发相关 JEP
│   ├── gc/                # GC 相关 JEP
│   ├── security/          # 安全相关 JEP
│   ├── network/           # 网络相关 JEP
│   ├── performance/       # 性能相关 JEP
│   ├── ffi/               # Foreign Function JEP
│   ├── jfr/               # JFR 相关 JEP
│   ├── tools/             # 工具相关 JEP
│   └── removed/           # 已移除特性 JEP
│
├── jsr/                   # JSR (Java Specification Requests)
│   ├── README.md           # JSR 索引
│   ├── language/          # 语言规范
│   ├── api/               # API 规范
│   └── platform/          # 平台规范
│
├── cases/                 # 实战案例 (GC 调优/虚拟线程/启动优化)
├── deep-dive/             # 源码深入分析 (JEP 实现细节)
├── issues/                # Issue 深度分析 (性能/稳定性)
├── benchmarks/            # 性能基准测试方法论
├── troubleshooting/       # 故障排查指南
├── best-practices/        # 最佳实践
│
├── guides/                # 通用指南
│   ├── learning-path.md   # 学习路径
│   ├── migration-guide.md # 迁移指南
│   ├── faq.md             # 常见问题
│   ├── cheat-sheet.md     # 速查表
│   ├── jdk-distributions.md # JDK 发行版
│   └── comparisons/       # 技术对比 (锁/CDS/Profiler/IO)
│
├── contributors/          # 贡献者统计
│   ├── orgs/              # 组织页面
│   └── stats/             # 统计数据
├── distributions/          # JDK 发行版分析 (Docker 统计/维护团队)
├── valhalla/              # Valhalla 项目数据 (2,082 PRs)
├── shenandoah/            # Shenandoah 项目数据 (482 PRs)
├── jfx/                   # JavaFX 项目数据 (1,782 PRs)
├── jmc/                   # JMC 项目数据 (626 PRs)
├── modules/               # 模块/组件分析
├── scripts/               # 数据获取脚本
└── talks/                 # 技术演讲 (JVMLS 等)
```

---

## 5. 精选 PR 分析

### 性能优化系列

| PR | 影响 | 分析 |
|----|------|------|
| [JDK-8341755](by-pr/8341/8341755.md) | Lambda 生成 +15-20% | 参数名称缓存优化 |
| [JDK-8349400](by-pr/8349/8349400.md) | 启动速度 +5% | 消除嵌套类优化 |
| [JDK-8339217](by-pr/8339/8339217.md) | 常量加载 +5-15% | ClassFile API 优化 |
| [JDK-8339290](by-pr/8339/8339290.md) | UTF-8 编码 +15-30% | 批量扫描优化 |
| [JDK-8341906](by-pr/8341/8341906.md) | 字节码写入 +28% | BufWriter 合并 |
| [JDK-8341859](by-pr/8341/8341859.md) | 基准稳定性 +63% | ClassFile 测试优化 |

**查看更多**: [PR 分析索引](by-pr/)

---

## 6. 数据来源

- **GitHub PRs**: [openjdk/jdk](https://github.com/openjdk/jdk) - 代码变更和讨论
- **JBS Issues**: [bugs.openjdk.org](https://bugs.openjdk.org/) - 问题追踪
- **Mailing Lists**: [jdk-dev](https://mail.openjdk.org/pipermail/jdk-dev/) - 设计决策讨论
- **JEP Docs**: [openjdk.org/jeps](https://openjdk.org/jeps/) - 特性规范
- **JSR Docs**: [jcp.org](https://jcp.org/) - Java 规范请求

---

## 7. 更新日志

| 日期 | 更新内容 |
|------|----------|
| 2026-03-28 | ✨ 新增 issues/ 深度分析 (5 篇)、benchmarks/、troubleshooting/、best-practices/ 目录，4 篇技术对比指南，3 篇模块分析，3 篇 JEP 深度分析，6 篇案例研究；清理 prs/ 过时目录 |
| 2026-03-25 | 📊 **重大更新**: 43,394 PRs/25 仓库完整采集, 22,560 PR 深度分析, 387 JEP 文档, 72,789 审查记录, CFV 投票网络, Docker/GitHub 统计 |
| 2026-03-22 | 📊 统计更新: 856 文档 / 17,505+ 链接，一致性扫描修正 |
| 2026-03-21 | 📊 统计更新: 733 文档 / 17,505 链接，完善目录结构文档 |
| 2026-03-20 | ✨ **重大更新**: 28 个主题文档增强，新增 4215+ 行 PR 分析和最佳实践 |
| 2026-03-20 | ✨ 新增 Lambda/Stream/Enum/Generics/Patterns/Records 深度分析 |
| 2026-03-20 | ✨ 新增 JIT 编译、内存管理、性能优化专题 |
| 2026-03-20 | ✨ 新增 Class File API 9 个 PR 分析 |
| 2026-03-20 | ✨ 修复贡献者档案链接，更新主题索引 |
| 2026-03-20 | 新增技术演讲 (talks/) 和 JVMLS 资料 |
| 2026-03-20 | 新增研究方法论 (AGENTS.md)，修复主题链接 |
| 2026-03-19 | 新增 JSR 文档 |
| 2026-03-18 | 新增 Class File API 主题 |
| 2026-03-17 | 新增 JDK 26 PR 分析 |

---

> **项目状态**: 持续更新中
>
> **最后更新**: 2026-03-28
>
> **文档统计**: 1016 个文档文件 | 17,505+ 个链接 | 覆盖 JDK 8/11/17/21/25/26
