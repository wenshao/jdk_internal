# JDK Internal Docs

> 分析 OpenJDK 源码、Issue、PR，沉淀便于人类和 AI 阅读的文档

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

| 主题 | 版本范围 | 查看 |
|------|----------|------|
| **GC 演进** | 8 → 26 | [G1/ZGC/Shenandoah 时间线](by-topic/core/gc/) |
| **并发编程** | 8 → 26 | [Thread → VirtualThread](by-topic/concurrency/concurrency/) |
| **HTTP 客户端** | 11+ | [HttpURLConnection → HTTP/3](by-topic/concurrency/http/) |
| **字符串处理** | 8 → 26 | [String 优化历程](by-topic/language/string/) |
| **安全特性** | 8 → 26 | [TLS/加密/后量子密码](by-topic/security/security/) |
| **语言语法** | 8 → 26 | [泛型/Lambda/Record/Pattern Matching](by-topic/language/syntax/) |
| **内存管理** | 8 → 26 | [堆/栈/Metaspace/Compressed Oops](by-topic/core/memory/) |
| **模块系统** | 9+ | [JPMS/module-info/jlink](by-topic/core/modules/) |

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
│   │   ├── gc/            # GC 演进
│   │   ├── memory/        # 内存管理
│   │   ├── performance/   # 性能优化
│   │   ├── classloading/  # 类加载器
│   │   └── modules/       # 模块系统
│   ├── language/          # 语言特性
│   │   ├── syntax/        # 语法演进
│   │   ├── string/        # 字符串处理
│   │   ├── reflection/    # 反射与元数据
│   │   └── classfile/     # Class File API
│   ├── api/               # API 框架
│   │   ├── collections/   # 集合框架
│   │   ├── io/            # I/O 处理
│   │   └── datetime/      # 日期时间
│   ├── concurrency/       # 并发网络
│   │   ├── concurrency/   # 并发编程
│   │   ├── http/          # HTTP 客户端
│   │   └── network/       # 网络编程
│   └── security/          # 安全国际化
│       ├── security/      # 安全特性
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
| 2026-03-20 | 新增技术演讲 (talks/) 和 JVMLS 资料 |
| 2026-03-20 | 新增研究方法论 (AGENTS.md)，修复主题链接 |
| 2026-03-19 | 新增 JSR 文档 |
| 2026-03-18 | 新增 Class File API 主题 |
| 2026-03-17 | 新增 JDK 26 PR 分析 |

---

> **项目状态**: 持续更新中
>
> **最后更新**: 2026-03-20
