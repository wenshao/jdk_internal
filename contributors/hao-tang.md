# Hao Tang

> 容器和 ZGC 贡献者，阿里巴巴

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Hao Tang |
| **当前组织** | 阿里巴巴 (Alibaba) |
| **邮箱** | albert.th@alibaba-inc.com |
| **Commits** | 2 |
| **主要领域** | 容器, ZGC |
| **活跃时间** | 2019 - 2020 |

---

## 贡献列表

| Issue | 标题 | 说明 |
|-------|------|------|
| 8265836 | OperatingSystemImpl.getCpuLoad() returns incorrect CPU load inside a container | **容器修复** |
| 8229406 | ZGC: Fix incorrect statistics | ZGC 修复 |

---

## 关键贡献

### 容器内 CPU 负载不正确修复 (JDK-8265836)

**问题**: 在容器内运行时，`OperatingSystemImpl.getCpuLoad()` 返回宿主机的 CPU 负载，而非容器的。

**解决方案**: 正确读取容器的 CPU 统计：

```java
// 变更前: 读取 /proc/stat (宿主机)
long cpuUsage = readFromProcStat();

// 变更后: 读取 cgroup 的 CPU 统计
long cpuUsage = readFromCgroup("/sys/fs/cgroup/cpuacct/cpuacct.usage");
```

**影响**: 容器内 Java 应用可以正确获取自身的 CPU 负载。

### ZGC 统计错误修复 (JDK-8229406)

**问题**: ZGC 的某些统计数据不正确。

**解决方案**: 修复统计计算：

```cpp
// 变更前
size_t allocated = _allocated - _reclaimed;

// 变更后: 正确计算
size_t allocated = _allocated_at_mark_start - _reclaimed;
```

**影响**: ZGC 统计数据更准确，便于性能分析。

---

## 相关链接

- [JBS Issues](https://bugs.openjdk.org/issues/?jql=reporter%20%3D%20albert.th)