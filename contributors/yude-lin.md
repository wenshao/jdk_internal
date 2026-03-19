# Yude Lin

> G1 GC 和 Shenandoah 贡献者，阿里巴巴

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Yude Lin |
| **当前组织** | 阿里巴巴 (Alibaba) |
| **邮箱** | yude.lyd@alibaba-inc.com |
| **Commits** | 8 |
| **主要领域** | G1 GC, Shenandoah, AArch64 |
| **活跃时间** | 2020 - 2024 |

---

## 贡献列表

| Issue | 标题 | 说明 |
|-------|------|------|
| 8334810 | Redo: Un-ProblemList LocaleProvidersRun | 测试修复 |
| 8328064 | Remove obsolete comments in constantPool | 代码清理 |
| 8323122 | AArch64: Increase itable stub size estimate | AArch64 修复 |
| 8298521 | Rename members in G1MonitoringSupport | G1 重构 |
| 8297247 | Add GarbageCollectorMXBean for Remark and Cleanup | **G1 监控增强** |
| 8274546 | Shenandoah: Remove unused ShenandoahUpdateRootsTask | 代码清理 |
| 8266963 | Remove safepoint poll due to reentrance issue | 正确性修复 |
| 8266185 | Shenandoah: Fix incorrect comment/assertion | 文档修复 |

---

## 关键贡献

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

## 相关链接

- [JBS Issues](https://bugs.openjdk.org/issues/?jql=reporter%20%3D%20yude.lyd)