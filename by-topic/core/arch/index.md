# CPU 架构支持

> OpenJDK 支持的 CPU 架构演进

[← 返回核心平台](../)

---
## 目录

1. [概述](#1-概述)
2. [架构对比](#2-架构对比)
3. [详细介绍](#3-详细介绍)
4. [按版本演进](#4-按版本演进)
5. [架构特定优化](#5-架构特定优化)
6. [贡献者](#6-贡献者)
7. [相关链接](#7-相关链接)
8. [相关主题](#8-相关主题)

---


## 1. 概述

OpenJDK 支持多种 CPU 架构，从最初的 x86/x64 扩展到 ARM、RISC-V、LoongArch 等新兴架构。

```
┌─────────────────────────────────────────────────────────────┐
│                    OpenJDK 架构支持                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   x86/x64        AArch64        RISC-V        LoongArch     │
│   (主流)         (移动/云)       (新兴)        (中国)         │
│                                                             │
│   JDK 1.0        JDK 9          JDK 19        JDK 21        │
│   ────────       ────────       ────────      ────────      │
│   x86_32         arm64          riscv64       loongarch64   │
│   x86_64         aarch64        rv64gc        la64          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. 架构对比

| 架构 | 位数 | 引入版本 | 状态 | 主要贡献者 |
|------|------|----------|------|------------|
| **x86_64** | 64-bit | JDK 5 | ✅ 主流 | Oracle |
| **x86_32** | 32-bit | JDK 1.0 | ⚠️ JDK 26 移除 (JEP 503) | Oracle |
| **AArch64** | 64-bit | JDK 9 | ✅ 主流 | Oracle, Red Hat, Arm |
| **ARM32** | 32-bit | JDK 9 | ⚠️ JDK 26 移除 | Arm |
| **RISC-V** | 64-bit | JDK 19 | ✅ 活跃 | ISCAS, 阿里巴巴, 字节跳动 |
| **LoongArch** | 64-bit | JDK 21 | ✅ 活跃 | 龙芯 |
| **PPC64/PPC64LE** | 64-bit | JDK 9/11 | ✅ 维护 | IBM |
| **s390x** | 64-bit | JDK 9 | ✅ 维护 | IBM |

---

## 3. 详细介绍

### [x86/x64](x86.md)

Intel/AMD x86 架构，OpenJDK 的主要开发平台。

| 属性 | 值 |
|------|-----|
| **引入版本** | JDK 1.0 (32-bit), JDK 5 (64-bit) |
| **状态** | ✅ 主流支持 |
| **32位支持** | ⚠️ JDK 26 移除 (JEP 503) |
| **主要贡献者** | Oracle |

---

### [AArch64](aarch64.md)

ARM 64位架构，广泛用于移动设备、云服务器和 Apple Silicon。

| 属性 | 值 |
|------|-----|
| **引入版本** | JDK 9 (JEP 237) |
| **macOS 支持** | JDK 17 (JEP 391) |
| **状态** | ✅ 主流支持 |
| **主要贡献者** | Oracle, Red Hat, Arm, Amazon |

**里程碑**:
| 版本 | JEP | 说明 |
|------|-----|------|
| JDK 9 | JEP 237 | AArch64 Linux 移植 |
| JDK 17 | JEP 391 | macOS/AArch64 (Apple Silicon) |
| JDK 18 | - | Windows/AArch64 |

---

### [RISC-V](riscv.md)

开源指令集架构，中国厂商重点投入方向。

| 属性 | 值 |
|------|-----|
| **引入版本** | JDK 19 (JEP 422) |
| **向量支持** | JDK 21+ |
| **状态** | ✅ 活跃开发 |
| **主要贡献者** | ISCAS, 阿里巴巴, 字节跳动 |

**里程碑**:
| 版本 | JEP | 说明 |
|------|-----|------|
| JDK 19 | JEP 422 | RISC-V Linux 移植 |
| JDK 20 | - | 向量 intrinsic 初步支持 |
| JDK 21 | - | Zvbb/Zfa 扩展 |
| JDK 24 | - | 向量支持完善 |
| JDK 26 | - | 紧凑对象头支持 |

---

### [LoongArch](loongarch.md)

龙芯中科自主指令集架构。

| 属性 | 值 |
|------|-----|
| **引入版本** | JDK 21 |
| **状态** | ✅ 活跃开发 |
| **主要贡献者** | 龙芯中科 |

---

### PPC64/PPC64LE

IBM PowerPC 64位架构，主要用于 IBM Power Systems 和 AIX。

| 属性 | 值 |
|------|-----|
| **引入版本** | JDK 9 (PPC64), JDK 11 (PPC64LE) |
| **状态** | ✅ 维护模式 |
| **主要贡献者** | IBM |

**主要平台**:
- IBM Power Systems (AIX/Linux)
- OpenPOWER 服务器

---

### s390x

IBM System z 大型机架构，主要用于企业级后端系统。

| 属性 | 值 |
|------|-----|
| **引入版本** | JDK 9 |
| **状态** | ✅ 维护模式 |
| **主要贡献者** | IBM |

**主要平台**:
- IBM Z Mainframe (Linux on System z)
- 银行/金融系统

---

## 4. 按版本演进

### x86/x64

| 版本 | 变化 |
|------|------|
| JDK 1.0 | x86_32 支持 |
| JDK 5 | x86_64 支持 |
| JDK 9 | 改进 AVX 支持 |
| JDK 26 | **移除 x86_32** (JEP 503) |

### AArch64

| 版本 | 变化 | JEP |
|------|------|-----|
| JDK 9 | AArch64 Linux | JEP 237 |
| JDK 11 | Intrinsics 改进 | JEP 315 |
| JDK 17 | macOS/AArch64 | JEP 391 |
| JDK 18 | Windows/AArch64 | - |

### RISC-V

| 版本 | 变化 | JEP |
|------|------|-----|
| JDK 19 | RISC-V Linux | JEP 422 |
| JDK 20 | 向量 intrinsic | - |
| JDK 21 | Zvbb/Zfa 扩展 | - |
| JDK 24 | 完善向量支持 | - |
| JDK 26 | 紧凑对象头支持 | - |

### LoongArch

| 版本 | 变化 |
|------|------|
| JDK 21 | 初始移植 |
| JDK 22 | 稳定性改进 |
| JDK 24 | LSX/LASX 向量支持 |
| JDK 26 | 紧凑对象头支持 |

### PPC64/PPC64LE

| 版本 | 变化 |
|------|------|
| JDK 9 | PPC64 支持 (AIX/Linux) |
| JDK 11 | PPC64LE 支持 (Little Endian) |
| JDK 17+ | 持续维护 |

### s390x

| 版本 | 变化 |
|------|------|
| JDK 9 | s390x 支持 (Linux on System z) |
| JDK 17+ | 持续维护 |

---

## 5. 架构特定优化

### x86/x64

```bash
# AVX 支持
-XX:UseAVX=3

# 向量优化
-XX:+UseVectorCmov
```

### AArch64

```bash
# LSE 原子指令
-XX:+UseLSE
```

### RISC-V

```bash
# 向量扩展检测 (自动)
# 支持: V, Zvbb, Zfa, Zvkn

# 查看支持的扩展
java -XX:+PrintFlagsFinal -version | grep -i riscv
```

---

## 6. 贡献者

### RISC-V 团队

| 贡献者 | 组织 | 主要贡献 |
|--------|------|----------|
| [Fei Yang](/by-contributor/profiles/fei-yang.md) | Huawei | RISC-V Port Lead |
| [Hamlin Li](/by-contributor/profiles/hamlin-li.md) | Rivos | RISC-V 向量 |
| [Anjian Wen](/by-contributor/profiles/anjian-wen.md) | 字节跳动 | Zvbb/Zfa 指令 |
| Dingli Zhang | ISCAS | RISC-V 测试 |

### AArch64 团队

| 贡献者 | 组织 | 主要贡献 |
|--------|------|----------|
| Andrew Dinn | Red Hat | AArch64 移植 |
| Nick Gasson | Arm | AArch64 优化 |
| David Holmes | Oracle | AArch64 运行时 |

### LoongArch 团队

| 贡献者 | 组织 |
|--------|------|
| sunguoyun | 龙芯 |
| Ao Qi | 龙芯 |
| Jie Fu | Huawei |

---

## 7. 相关链接

### RISC-V

- [RISC-V International](https://riscv.org/)
- [OpenJDK RISC-V Port](https://openjdk.org/projects/riscv-port/)
- [ISCAS PLCT 实验室](https://github.com/plctlab)

### AArch64

- [Arm Developer](https://developer.arm.com/)
- [OpenJDK AArch64](https://openjdk.org/projects/aarch64-port/)

### LoongArch

- [龙芯中科](https://www.loongson.cn/)
- [LoongArch 架构手册](https://loongson.github.io/LoongArch-Documentation/)

---

## 8. 相关主题

- [JIT 编译](../jit/) - 架构特定的编译优化
- [性能优化](../performance/) - 平台性能调优
- [GC](../gc/) - 架构特定的 GC 优化
