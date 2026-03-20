# JDK 发布说明

OpenJDK 各版本的发布说明汇总。

---

## 版本时间线

```
2014 ─────── 2017 ─────── 2018 ─────── 2021 ─────── 2023 ─────── 2025 ─────── 2026
   │            │            │            │            │            │            │
   ▼            ▼            ▼            ▼            ▼            ▼            ▼
 JDK 8        JDK 9        JDK 11       JDK 17       JDK 21       JDK 25       JDK 26
 (LTS)        (Feature)    (LTS)        (LTS)        (LTS)        (LTS)        (Feature)
```

---

## LTS 版本（长期支持）

| 版本 | 发布日期 | 支持截止 | 发布说明 | 主要特性 |
|------|----------|----------|----------|----------|
| **JDK 8** | 2014-03 | 2030-12 (付费) | [发布说明](jdk8.md) | Lambda、Stream、Date/Time API |
| **JDK 11** | 2018-09 | 2032-01 | [发布说明](jdk11.md) | HTTP Client、var、Flight Recorder |
| **JDK 17** | 2021-09 | 2029-10 | [发布说明](jdk17.md) | Records、Sealed Classes、Pattern Matching |
| **JDK 21** | 2023-09 | 2031-10 | [发布说明](jdk21.md) | Virtual Threads、Scoped Values、分代 ZGC |
| **JDK 25** | 2025-09 | 2032+ | [发布说明](jdk25.md) | String Templates、Compact Object Headers |

---

## Feature 版本（短期支持）

| 版本 | 发布日期 | 发布说明 | 主要特性 |
|------|----------|----------|----------|
| **JDK 9** | 2017-09 | [发布说明](jdk9.md) | 模块系统 (JPMS)、jshell |
| **JDK 10** | 2018-03 | [发布说明](jdk10.md) | var 类型推断 |
| **JDK 12** | 2019-03 | [发布说明](jdk12.md) | Switch 表达式 (预览) |
| **JDK 13** | 2019-09 | [发布说明](jdk13.md) | 文本块 (预览) |
| **JDK 14** | 2020-03 | [发布说明](jdk14.md) | Records (预览)、Helpful NPE |
| **JDK 15** | 2020-09 | [发布说明](jdk15.md) | Text Blocks、Sealed Classes (预览) |
| **JDK 16** | 2021-03 | [发布说明](jdk16.md) | Records 正式版、instanceof 模式匹配 |
| **JDK 18** | 2022-03 | [发布说明](jdk18.md) | UTF-8 默认、Simple Web Server |
| **JDK 19** | 2022-09 | [发布说明](jdk19.md) | Virtual Threads (预览) |
| **JDK 20** | 2023-03 | [发布说明](jdk20.md) | Virtual Threads (第2次预览) |
| **JDK 22** | 2024-03 | [发布说明](jdk22.md) | String Templates (预览)、Implicit Classes |
| **JDK 23** | 2024-09 | [发布说明](jdk23.md) | Markdown 文档注释、Flexible Constructors |
| **JDK 24** | 2025-03 | [发布说明](jdk24.md) | String Templates (第3次预览) |
| **JDK 26** | 2025-09 | [发布说明](jdk26.md) | HTTP/3、G1 吞吐量提升 |

---

## 快速对比

### GC 默认选择

| 版本 | 默认 GC | 可选 GC |
|------|---------|---------|
| JDK 8 | ParallelGC | G1, CMS |
| JDK 9-10 | G1 | ZGC(实验) |
| JDK 11-16 | G1 | ZGC(11+), Shenandoah(12+) |
| JDK 17-20 | G1 | ZGC, Shenandoah |
| JDK 21-24 | G1 | 分代 ZGC, 分代 Shenandoah |
| JDK 25-26 | G1 | 分代 ZGC, 分代 Shenandoah |

### 语言特性演进

| 特性 | JDK 8 | 11 | 17 | 21 | 25 | 26 |
|------|-------|----|----|----|----|----|
| Lambda | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| var | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Records | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Text Blocks | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Pattern Matching | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Virtual Threads | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| String Templates | ❌ | ❌ | ❌ | 🔍 | ✅ | ✅ |
| HTTP/3 | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

> ✅ 正式版 | 🔍 预览版

---

## 版本选择指南

### 按场景选择

| 场景 | 推荐版本 | 理由 |
|------|----------|------|
| 遗留系统维护 | JDK 8 | 最大兼容性 |
| 稳定生产环境 | JDK 11 或 17 | 长期支持 |
| 现代应用首选 | JDK 17 | Records、Sealed Classes |
| 虚拟线程生产 | JDK 21 | Virtual Threads 正式版 |
| 最新 LTS | JDK 25 | 当前 LTS |
| 体验新特性 | JDK 26 | HTTP/3、最新优化 |

### 升级路径

```
JDK 8 ─────► JDK 11 ─────► JDK 17 ─────► JDK 21 ─────► JDK 25
   │            │            │            │            │
   │            │            │            │            │
   ▼            ▼            ▼            ▼            ▼
 var       Records      Virtual     String      HTTP/3
 HTTP      Sealed       Threads     Templates   G1 +20%
 Client    Classes      分代ZGC     Compact
```

---

## 发布节奏

OpenJDK 采用 6 个月的固定发布周期：

```
┌─────────────────────────────────────────────────────────────┐
│                    OpenJDK 发布节奏                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  每 6 个月发布一个新版本                                     │
│  每 2 年发布一个 LTS 版本 (9月)                              │
│                                                             │
│  2023-09 ─── JDK 21 (LTS)                                   │
│  2024-03 ─── JDK 22                                         │
│  2024-09 ─── JDK 23                                         │
│  2025-03 ─── JDK 24                                         │
│  2025-09 ─── JDK 25 (LTS)                                   │
│  2026-03 ─── JDK 26                                         │
│  ...                                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 相关链接

- [OpenJDK 官网](https://openjdk.org/)
- [JDK 版本历史](https://openjdk.org/projects/jdk/)
- [JEP 索引](https://openjdk.org/jeps/0)
- [GitHub: openjdk/jdk](https://github.com/openjdk/jdk)
