# Yude Lin

> G1 GC 和 AArch64 贡献者，阿里巴巴

---
## 目录

1. [基本信息](#1-基本信息)
2. [PR 列表](#2-pr-列表)
3. [关键贡献](#3-关键贡献)
4. [数据来源](#4-数据来源)
5. [相关链接](#5-相关链接)

---


## 1. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Yude Lin |
| **当前组织** | 阿里巴巴 (Alibaba) |
| **GitHub** | [@linade](https://github.com/linade) |
| **Integrated PRs** | [8](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Alinade+is%3Aclosed+label%3Aintegrated) |
| **主要领域** | G1 GC, AArch64 |
| **活跃时间** | 2021 - 2024 |

---

## 2. PR 列表

| Issue | 标题 | 合入时间 |
|-------|------|----------|
| 8334810 | Redo: Un-ProblemList LocaleProvidersRun | 2024-09 |
| 8328064 | Remove obsolete comments in constantPool | 2024-06 |
| 8323122 | AArch64: Increase itable stub size estimate | 2024-03 |
| 8298521 | Rename members in G1MonitoringSupport | 2022-09 |
| 8297247 | Add GarbageCollectorMXBean for Remark and Cleanup | 2022-08 |
| 8274546 | Shenandoah: Remove unused ShenandoahUpdateRootsTask | 2021-09 |
| 8266963 | Remove safepoint poll due to reentrance issue | 2021-05 |
| 8266185 | Shenandoah: Fix incorrect comment/assertion | 2021-04 |

---

## 3. 关键贡献

### G1 GC 监控增强 (JDK-8297247)

为 G1 GC 添加 Remark 和 Cleanup 阶段的暂停时间 MXBean：

```java
// 新增的 MXBean 支持
public interface G1GarbageCollectorMXBean extends GarbageCollectorMXBean {
    long getRemarkPauseTime();
    long getCleanupPauseTime();
}
```

**影响**: 用户可以更精确地监控 G1 GC 各阶段耗时。

### AArch64 itable stub 修复 (JDK-8323122)

修复 AArch64 平台上 itable stub 大小估算不足的问题：

```cpp
// 变更前
static int itable_stub_size = 0x50;

// 变更后
static int itable_stub_size = 0x60;  // 增加估算大小
```

**影响**: 修复了 AArch64 平台上的崩溃问题。

---

## 4. 数据来源

- **统计方法**: GitHub PR search `repo:openjdk/jdk author:linade type:pr label:integrated`
- **统计时间**: 2026-03-19

---

## 5. 相关链接

- [GitHub Profile](https://github.com/linade)
- [OpenJDK PRs](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Alinade)