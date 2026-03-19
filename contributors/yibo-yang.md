# Yibo Yang

> 内存优化和 Apple M1 贡献者，阿里巴巴

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Yibo Yang |
| **当前组织** | 阿里巴巴 (Alibaba) |
| **邮箱** | yibo.yl@alibaba-inc.com |
| **Commits** | 2 |
| **主要领域** | 内存优化, Apple M1 |
| **活跃时间** | 2024 |

---

## 贡献列表

| Issue | 标题 | 说明 |
|-------|------|------|
| 8326446 | The User and System of jdk.CPULoad on Apple M1 are inaccurate | **Apple M1 修复** |
| 8319876 | Reduce memory consumption of VM_ThreadDump::doit | **内存优化** |

---

## 关键贡献

### Apple M1 CPU 负载不准确修复 (JDK-8326446)

**问题**: 在 Apple M1 上，`jdk.CPULoad` 返回的 User 和 System 值不准确。

**解决方案**: 正确处理 Apple M1 的 CPU 统计：

```cpp
// 变更前: 使用通用实现
double user_load = cpu_time.user / total_time;

// 变更后: Apple M1 特殊处理
#ifdef __APPLE__
  if (is_apple_silicon()) {
    // Apple M1 使用不同的统计方式
    user_load = get_apple_silicon_cpu_load(CPU_STATE_USER);
    system_load = get_apple_silicon_cpu_load(CPU_STATE_SYSTEM);
  }
#endif
```

**影响**: Apple M1 用户可以正确监控 CPU 负载。

### VM_ThreadDump 内存优化 (JDK-8319876)

**问题**: `VM_ThreadDump::doit` 在处理大量线程时内存消耗过高。

**解决方案**: 优化内存分配：

```cpp
// 变更前: 一次性分配大数组
GrowableArray<StackFrameInfo*>* frames = new GrowableArray<>(max_threads * max_depth);

// 变更后: 按需分配
GrowableArray<StackFrameInfo*>* frames = new GrowableArray<>(initial_size);
frames->grow_to_fit(actual_size);
```

**影响**: 减少线程转储时的内存峰值消耗。

---

## 相关链接

- [JBS Issues](https://bugs.openjdk.org/issues/?jql=reporter%20%3D%20yibo.yl)