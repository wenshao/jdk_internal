# Zhuo Wang

> Unsafe 修复专家，阿里巴巴

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Zhuo Wang |
| **当前组织** | 阿里巴巴 (Alibaba) |
| **邮箱** | zhuoren.wz@alibaba-inc.com |
| **Commits** | 3 |
| **主要领域** | Unsafe, 内存操作 |
| **活跃时间** | 2020 |

---

## 贡献列表

| Issue | 标题 | 说明 |
|-------|------|------|
| 8248570 | Incorrect copyright header in TestUnsafeUnalignedSwap | 文档修复 |
| 8246051 | SIGBUS by unaligned Unsafe compare_and_swap | **崩溃修复** |

---

## 关键贡献

### Unsafe 非对齐访问 SIGBUS 修复 (JDK-8246051)

**问题**: 在某些平台上，Unsafe.compareAndSwap 操作非对齐内存地址时触发 SIGBUS。

**解决方案**: 检测并处理非对齐访问：

```cpp
// 变更前: 直接访问可能导致 SIGBUS
bool Unsafe::compareAndSwap(...) {
  return *addr == expected ? (*addr = new_value, true) : false;
}

// 变更后: 检查对齐
bool Unsafe::compareAndSwap(...) {
  if (!is_aligned(addr, sizeof(int))) {
    // 使用字节级操作或抛出异常
    return handle_unaligned_access(addr, expected, new_value);
  }
  return *addr == expected ? (*addr = new_value, true) : false;
}
```

**影响**: 修复了在 SPARC 等严格对齐平台上的崩溃问题。

---

## 相关链接

- [JBS Issues](https://bugs.openjdk.org/browse/JDK-8246051)