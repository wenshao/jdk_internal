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
| **JDK 26** | Feature | 2025-09 | - | [进入](by-version/jdk26/) |

---

## 我想了解...

| 主题 | 版本范围 | 查看 |
|------|----------|------|
| **GC 演进** | 8 → 26 | [G1/ZGC/Shenandoah 时间线](by-topic/gc/) |
| **并发编程** | 8 → 26 | [Thread → VirtualThread](by-topic/concurrency/) |
| **HTTP 客户端** | 11+ | [HttpURLConnection → HTTP/3](by-topic/http/) |
| **字符串处理** | 8 → 26 | [String 优化历程](by-topic/string/) |
| **安全特性** | 8 → 26 | [TLS/加密/后量子密码](by-topic/security/) |

---

## 快速导航

### 按浏览方式

| 方式 | 说明 | 链接 |
|------|------|------|
| **按版本** | 从你使用的 JDK 版本切入 | [浏览版本](by-version/) |
| **按主题** | 跨版本追踪某个技术演进 | [浏览主题](by-topic/) |
| **按贡献者** | 了解贡献者和他们的工作 | [浏览贡献者](by-contributor/) |
| **按 PR** | 深入具体 Issue/PR | [浏览 PR](by-pr/) |

### 按角色

| 角色 | 推荐阅读 |
|------|----------|
| **开发者** | [学习路径](guides/learning-path.md) |
| **架构师** | [主题演进](by-topic/) |
| **运维** | [版本迁移](by-version/jdk11/migration/) |
| **初学者** | [JDK 8 入门](by-version/jdk8/) |

---

## 目录结构

```
jdk_internal/
├── by-version/          # 按版本浏览
│   ├── jdk8/           # JDK 8 (LTS 2014)
│   ├── jdk11/          # JDK 11 (LTS 2018)
│   ├── jdk17/          # JDK 17 (LTS 2021)
│   ├── jdk21/          # JDK 21 (LTS 2023)
│   └── jdk26/          # JDK 26 (开发中)
├── by-topic/           # 按主题跨版本
│   ├── gc/             # GC 演进
│   ├── concurrency/    # 并发编程
│   ├── string/         # 字符串处理
│   ├── http/           # HTTP 客户端
│   └── security/       # 安全特性
├── by-contributor/     # 按贡献者
├── by-pr/              # 按 PR/Issue
└── guides/             # 通用指南
```

---

## 相关链接

- [OpenJDK 官网](https://openjdk.org/)
- [GitHub: openjdk/jdk](https://github.com/openjdk/jdk)
- [JDK Bug System (JBS)](https://bugs.openjdk.org/)
- [JDK 版本历史](https://openjdk.org/projects/jdk/)

---

> **数据来源**: GitHub PR、OpenJDK Commit、JBS Issue
>
> **更新时间**: 2026-03-19
