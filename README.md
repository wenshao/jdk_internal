# JDK Internal Docs

> 分析 OpenJDK 源码、Issue、PR，沉淀便于人类和 AI 阅读的文档

> **🎉 最新动态**: 28 个主题文档增强完成，新增 PR 性能分析系列 (Lambda +15-20%, 元空间 -82%)

---

## 你在用哪个版本？

| 版本 | 类型 | 发布时间 | 支持截止 | 文档 |
|------|------|----------|----------|------|
| **JDK 8** | LTS | 2014-03 | 2030-12 (付费) | [进入](by-version/jdk8/) |
| **JDK 11** | LTS | 2018-09 | 2032-01 | [进入](by-version/jdk11/) |
| **JDK 17** | LTS | 2021-09 | 2029-10 | [进入](by-version/jdk17/) |
| **JDK 21** | LTS | 2023-09 | 2031-10 | [进入](by-version/jdk21/) |
| **JDK 25** | LTS | 2025-09-16 | 2032+ | [进入](by-version/jdk25/) |
| **JDK 26** | Feature | 2026-03-17 | - | [进入](by-version/jdk26/) |

---

## 我想了解...

### 核心平台

| 主题 | 版本范围 | 查看 | 亮点 |
|------|----------|------|------|
| **GC 演进** | 8 → 26 | [G1/ZGC/Shenandoah 时间线](by-topic/core/gc/) | 分代 ZGC, G1 +10-20% |
| **内存管理** | 8 → 26 | [堆/栈/Metaspace/Compressed Oops](by-topic/core/memory/) | 紧凑对象头 -8-16字节 |
| **JIT 编译** | 8 → 26 | [C1/C2/Graal 分层编译](by-topic/core/jit/) | 内联优化, 逃逸分析 |
| **类加载器** | 8 → 26 | [双亲委派/模块化/CDS](by-topic/core/classloading/) | AppCDS 启动 +20% |
| **模式匹配** | 14 → 26 | [类型模式/Record 模式/守卫](by-topic/core/patterns/) | 性能提升 20-30% |
| **泛型系统** | 5 → 26 | [类型参数/通配符/类型擦除](by-topic/core/generics/) | PECS 原则 |
| **Record 类型** | 14 → 26 | [不可变数据载体/解构](by-topic/core/records/) | 字节码 -30% |
| **模块系统** | 9+ | [JPMS/module-info/jlink](by-topic/core/modules/) | 强封装 |

### 语言特性

| 主题 | 版本范围 | 查看 | 亮点 |
|------|----------|------|------|
| **语法演进** | 8 → 26 | [泛型/Lambda/Record/Pattern Matching](by-topic/language/syntax/) | Enum 优化 -82% 内存 |
| **Lambda** | 8 → 26 | [函数式编程/invokedynamic](by-topic/language/lambda/) | 生成优化 +15-20% |
| **Stream API** | 8 → 26 | [函数式数据处理/并行流](by-topic/language/streams/) | Gatherers (JDK 21+) |
| **字符串处理** | 8 → 26 | [String 优化历程](by-topic/language/string/) | Compact Strings -50% |
| **Class File API** | 22 → 26 | [标准字节码 API](by-topic/language/classfile/) | 替代 ASM |
| **反射与元数据** | 8 → 26 | [反射/注解/MethodHandle](by-topic/language/reflection/) | 变量引用 |

### 并发网络

| 主题 | 版本范围 | 查看 | 亮点 |
|------|----------|------|------|
| **并发编程** | 8 → 26 | [Thread → VirtualThread](by-topic/concurrency/concurrency/) | 虚拟线程 (JDK 21) |
| **HTTP 客户端** | 11+ | [HttpURLConnection → HTTP/3](by-topic/concurrency/http/) | HTTP/3 预览 (JDK 26) |
| **网络编程** | 8 → 26 | [Socket/NIO/Unix Domain](by-topic/concurrency/network/) | 异步 I/O |
| **日期时间** | 8+ | [JSR 310/LocalDate/ZonedDateTime](by-topic/datetime/) | 不可变 API |

### 安全特性

| 主题 | 版本范围 | 查看 |
|------|----------|------|
| **安全特性** | 8 → 26 | [TLS/加密/后量子密码](by-topic/security/security/) |
| **国际化** | 8 → 26 | [Locale/ResourceBundle/Unicode](by-topic/security/i18n/) |

---

## 快速导航

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

### 按角色

| 角色 | 推荐阅读 |
|------|----------|
| **开发者** | [学习路径](guides/learning-path.md) |
| **架构师** | [主题演进](by-topic/) |
| **运维** | [版本迁移](guides/migration-guide.md) |
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
│   ├── index.md           # 版本概览和对比
│   ├── jdk8/              # JDK 8 (LTS 2014)
│   ├── jdk11/             # JDK 11 (LTS 2018)
│   ├── jdk17/             # JDK 17 (LTS 2021)
│   ├── jdk21/             # JDK 21 (LTS 2023)
│   ├── jdk25/             # JDK 25 (LTS 2025)
│   └── jdk26/             # JDK 26 (Feature 2026-03)
│
├── by-topic/              # 按主题跨版本
│   ├── index.md           # 主题索引
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
│   │   └── modules/       # 模块系统 (JPMS/jlink)
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
│   │   └── datetime/      # 日期时间 (JSR 310)
│   ├── concurrency/       # 并发网络
│   │   ├── concurrency/   # 并发编程 (Thread/VirtualThread)
│   │   ├── http/          # HTTP 客户端 (HTTP/3)
│   │   └── network/       # 网络编程 (NIO/Unix Socket)
│   └── security/          # 安全国际化
│       ├── security/      # 安全特性 (TLS/加密)
│       └── i18n/          # 国际化
│
├── by-contributor/        # 按贡献者
│   ├── index.md           # 贡献者索引
│   └── profiles/          # 个人详细页面
│
├── by-pr/                 # 按 PR/Issue 深度分析
│   ├── index.md           # PR 索引
│   └── {issue}/           # 按 issue 号分组
│
├── jeps/                  # JEP 详细分析
│   ├── index.md           # JEP 索引
│   ├── language/          # 语言相关 JEP
│   ├── core/              # 核心平台 JEP
│   └── concurrency/       # 并发相关 JEP
│
├── jsr/                   # JSR (Java Specification Requests)
│   ├── index.md           # JSR 索引
│   ├── language/          # 语言规范
│   ├── api/               # API 规范
│   └── platform/          # 平台规范
│
├── guides/                # 通用指南
│   ├── learning-path.md   # 学习路径
│   ├── migration-guide.md # 迁移指南
│   ├── faq.md             # 常见问题
│   └── cheat-sheet.md     # 速查表
│
├── contributors/          # 贡献者统计
├── modules/               # 模块/组件分析
├── scripts/               # 数据获取脚本
└── talks/                 # 技术演讲 (JVMLS 等)
```

---

## ⭐ 精选 PR 分析

### 性能优化系列

| PR | 影响 | 分析 |
|----|------|------|
| [JDK-8341755](by-pr/8341/8341755.md) | Lambda 生成 +15-20% | 参数名称缓存优化 |
| [JDK-8349400](by-pr/8349/8349400.md) | 元空间 -82% | 消除匿名内部类 |
| [JDK-8339217](by-pr/8339/8339217.md) | 常量加载 +5-15% | ClassFile API 优化 |
| [JDK-8339290](by-pr/8339/8339290.md) | UTF-8 编码 +15-30% | 批量扫描优化 |
| [JDK-8341906](by-pr/8341/8341906.md) | 字节码写入 +28% | BufWriter 合并 |
| [JDK-8341859](by-pr/8341/8341859.md) | 基准稳定性 +63% | ClassFile 测试优化 |

**查看更多**: [PR 分析索引](by-pr/)

---

## 数据来源

- **GitHub PRs**: [openjdk/jdk](https://github.com/openjdk/jdk) - 代码变更和讨论
- **JBS Issues**: [bugs.openjdk.org](https://bugs.openjdk.org/) - 问题追踪
- **Mailing Lists**: [jdk-dev](https://mail.openjdk.org/pipermail/jdk-dev/) - 设计决策讨论
- **JEP Docs**: [openjdk.org/jeps](https://openjdk.org/jeps/) - 特性规范
- **JSR Docs**: [jcp.org](https://jcp.org/) - Java 规范请求

---

## 更新日志

| 日期 | 更新内容 |
|------|----------|
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
> **最后更新**: 2026-03-20
>
> **文档统计**: 537 个文档文件 | 8,337 个链接 | 覆盖 JDK 8/11/17/21/25/26
