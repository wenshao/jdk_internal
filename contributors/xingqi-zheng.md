# Xingqi Zheng

> RISC-V 修复专家，阿里巴巴

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Xingqi Zheng |
| **当前组织** | 阿里巴巴 (Alibaba) |
| **邮箱** | xingqizheng.xqz@alibaba-inc.com |
| **GitHub** | [@MaxXSoft](https://github.com/MaxXSoft) |
| **Commits** | 2 |
| **主要领域** | RISC-V |
| **活跃时间** | 2024 |

---

## 贡献列表

| Issue | 标题 | 说明 |
|-------|------|------|
| 8326936 | RISC-V: Shenandoah GC crashes due to incorrect atomic memory operations | **崩溃修复** |
| 8324280 | RISC-V: Incorrect implementation in VM_Version::parse_satp_mode | 正确性修复 |

---

## 关键贡献

### RISC-V Shenandoah GC 崩溃修复 (JDK-8326936)

**问题**: Shenandoah GC 在 RISC-V 平台上因原子内存操作错误而崩溃。

**解决方案**: 修复 RISC-V 原子操作的内存顺序：

```cpp
// 变更前: 使用错误的内存顺序
Atomic::cmpxchg(addr, expected, new_value);

// 变更后: 使用正确的内存顺序
Atomic::cmpxchg(addr, expected, new_value, memory_order_conservative);
```

**影响**: 修复了 RISC-V 平台上 Shenandoah GC 的崩溃问题。

### RISC-V VM_Version::parse_satp_mode 修复 (JDK-8324280)

**问题**: RISC-V 的 `VM_Version::parse_satp_mode` 实现错误。

**解决方案**: 正确解析 satp 寄存器：

```cpp
// 变更前: 错误的位操作
int mode = (satp >> 60) & 0xF;

// 变更后: 正确的位操作
int mode = (satp >> SATP_MODE_SHIFT) & SATP_MODE_MASK;
```

**影响**: 确保 RISC-V 虚拟内存模式正确检测。

---

## 相关链接

- [JBS Issues](https://bugs.openjdk.org/issues/?jql=reporter%20%3D%20xingqizheng.xqz)