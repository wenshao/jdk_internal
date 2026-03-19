# 按版本浏览

选择你使用的 JDK 版本，查看该版本的特性、问题和迁移指南。

---

## 版本概览

| 版本 | 类型 | 发布时间 | 支持截止 | 状态 |
|------|------|----------|----------|------|
| **JDK 8** | LTS | 2014-03 | 2030-12 (付费) | 稳定 |
| **JDK 11** | LTS | 2018-09 | 2032-01 | 稳定 |
| **JDK 17** | LTS | 2021-09 | 2029-10 | 稳定 |
| **JDK 21** | LTS | 2023-09 | 2031-10 | 当前 LTS |
| **JDK 26** | Feature | 2025-09 | - | 开发中 |

---

## 快速对比

### GC 默认选择

| 版本 | 默认 GC | 可选 GC |
|------|---------|---------|
| JDK 8 | ParallelGC | G1, CMS, ZGC(实验) |
| JDK 11 | G1 | ZGC(实验), Shenandoah |
| JDK 17 | G1 | ZGC, Shenandoah |
| JDK 21 | G1 | 分代 ZGC, 分代 Shenandoah |
| JDK 26 | G1 | ZGC(NUMA), Shenandoah |

### 主要特性

| 特性 | JDK 8 | JDK 11 | JDK 17 | JDK 21 | JDK 26 |
|------|-------|--------|--------|--------|--------|
| Lambda | ✅ | ✅ | ✅ | ✅ | ✅ |
| var | ❌ | ✅ | ✅ | ✅ | ✅ |
| Records | ❌ | ❌ | ✅ | ✅ | ✅ |
| Pattern Matching | ❌ | ❌ | 预览 | ✅ | ✅ |
| Virtual Threads | ❌ | ❌ | ❌ | ✅ | ✅ |
| Structured Concurrency | ❌ | ❌ | ❌ | 预览 | 预览 |
| HTTP/3 | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## 各版本文档

### [JDK 8](jdk8/) - LTS 2014
- 核心特性：Lambda、Stream、Date/Time API
- GC：ParallelGC (默认)、G1、CMS
- [已知问题](jdk8/known-issues.md)
- [迁移到 JDK 11](jdk8/migration/to-11.md)

### [JDK 11](jdk11/) - LTS 2018
- 新特性：var、HTTP Client、Flight Recorder
- GC：G1 (默认)、ZGC (实验)
- [相比 JDK 8 的新特性](jdk11/new-since-8.md)
- [迁移指南](jdk11/migration/)

### [JDK 17](jdk17/) - LTS 2021
- 新特性：Records、Pattern Matching、Sealed Classes
- 强封装：JDK 内部 API 默认不可访问
- [相比 JDK 11 的新特性](jdk17/new-since-11.md)
- [迁移指南](jdk17/migration/)

### [JDK 21](jdk21/) - LTS 2023
- 新特性：Virtual Threads、Scoped Values、Structured Concurrency
- Pattern Matching 最终版
- [相比 JDK 17 的新特性](jdk21/new-since-17.md)
- [迁移指南](jdk21/migration/)

### [JDK 26](jdk26/) - 开发中
- 新特性：HTTP/3、分代 ZGC、分代 Shenandoah
- [JEP 汇总](jdk26/jeps.md)
- [前瞻特性](jdk26/preview.md)

---

## 迁移路径

```
JDK 8 ───────► JDK 11 ───────► JDK 17 ───────► JDK 21 ───────► JDK 26
 │              │               │               │               │
 │              │               │               │               │
 ├─ 3年免费     ├─ 8年LTS       ├─ 5年LTS       ├─ 8年LTS       └─ 开发中
 └─ 付费延长    └─ 2029 EOL     └─ 2026 EOL     └─ 2031 EOL
```

---

## 选择建议

| 当前版本 | 推荐升级 | 理由 |
|----------|----------|------|
| JDK 8 | → JDK 11 或 17 | 长期支持成本，性能提升 |
| JDK 11 | → JDK 17 或 21 | 新特性，更好的 GC |
| JDK 17 | → JDK 21 | 虚拟线程，结构化并发 |
| JDK 21 | 保持或 → JDK 26 | 当前 LTS，或体验新特性 |
