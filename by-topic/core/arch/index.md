# CPU 架构支持

> OpenJDK 支持的 CPU 架构全面解析与演进历史

[← 返回核心平台](../)

---
## 目录

1. [概述](#1-概述)
2. [架构支持矩阵](#2-架构支持矩阵)
3. [详细介绍](#3-详细介绍)
4. [32 位 x86 移除时间线](#4-32-位-x86-移除时间线)
5. [按版本演进](#5-按版本演进)
6. [架构特定 JIT 优化](#6-架构特定-jit-优化)
7. [贡献者](#7-贡献者)
8. [相关链接](#8-相关链接)
9. [相关主题](#9-相关主题)

---


## 1. 概述

OpenJDK 支持多种 CPU 架构，从最初的 x86/x64 逐步扩展到 AArch64、RISC-V、LoongArch 等架构。
随着云计算和物联网的发展，多架构支持已成为 JDK 平台的关键能力。

```
┌───────────────────────────────────────────────────────────────────────┐
│                       OpenJDK 架构支持全景                             │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│   x86/x64          AArch64          RISC-V          LoongArch         │
│   (主流桌面/服务器)  (移动/云/Mac)     (开源新兴)       (中国自主)        │
│                                                                       │
│   JDK 1.0+         JDK 9+           JDK 19+         JDK 21+          │
│   ──────────       ──────────       ──────────      ──────────       │
│   x86_32 (已移除)   Linux(JEP 237)   riscv64         loongarch64      │
│   x86_64            macOS(JEP 391)   rv64gc          la64             │
│                     Windows(JDK 18)                                   │
│                                                                       │
│   PPC64/PPC64LE              s390x                                    │
│   (IBM Power)                (IBM Z 大型机)                            │
│   JDK 9/11+                 JDK 9+                                    │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

### 架构演进简史

- **1996 (JDK 1.0)**: 最初仅支持 x86_32 和 SPARC
- **2004 (JDK 5)**: 加入 x86_64 (AMD64) 支持
- **2017 (JDK 9)**: 多架构扩展 -- AArch64 (JEP 237)、PPC64、s390x 正式进入主线
- **2021 (JDK 17)**: AArch64 扩展至 macOS (JEP 391)，支持 Apple Silicon
- **2022 (JDK 19)**: RISC-V 移植 (JEP 422)，开源架构进入 Java 生态
- **2023 (JDK 21)**: LoongArch 移植，中国自主架构获得支持
- **2025 (JDK 25)**: 移除 32 位 x86 (JEP 503)，全面拥抱 64 位时代

---

## 2. 架构支持矩阵

### 各架构总览

| 架构 | 位数 | 引入版本 | 当前状态 | 主要推动者 | 关键 JEP |
|------|------|----------|----------|------------|----------|
| **x86_64** | 64-bit | JDK 5 | 主流 | Oracle, Intel | - |
| **x86_32** | 32-bit | JDK 1.0 | **JDK 25 已移除** | Oracle | JEP 449/479/501/503 |
| **AArch64** | 64-bit | JDK 9 | 主流 | Red Hat, Arm, Oracle | JEP 237/315/340/391 |
| **ARM32** | 32-bit | JDK 9 | 已移除 | Arm | - |
| **RISC-V** | 64-bit | JDK 19 | 活跃开发 | Huawei, ISCAS, 阿里巴巴 | JEP 422 |
| **LoongArch** | 64-bit | JDK 21 | 活跃开发 | 龙芯中科 | - |
| **PPC64/PPC64LE** | 64-bit | JDK 9/11 | 维护 | IBM, SAP | - |
| **s390x** | 64-bit | JDK 9 | 维护 | IBM | - |

### JDK 版本 x 架构支持矩阵

下表展示各 JDK LTS 版本及重要版本对各架构的支持情况：

| JDK 版本 | x86_64 | x86_32 | AArch64 Linux | AArch64 macOS | AArch64 Win | RISC-V | LoongArch | PPC64 | s390x |
|----------|--------|--------|---------------|---------------|-------------|--------|-----------|-------|-------|
| **JDK 8** (LTS) | Y | Y | 外部 | - | - | - | - | 外部 | - |
| **JDK 9** | Y | Y | **JEP 237** | - | - | - | - | Y | Y |
| **JDK 11** (LTS) | Y | Y | Y | - | - | - | - | Y | Y |
| **JDK 12** | Y | Y | Y (统一) | - | - | - | - | Y | Y |
| **JDK 17** (LTS) | Y | Y | Y | **JEP 391** | - | - | - | Y | Y |
| **JDK 18** | Y | Y | Y | Y | Y | - | - | Y | Y |
| **JDK 19** | Y | Y | Y | Y | Y | **JEP 422** | - | Y | Y |
| **JDK 21** (LTS) | Y | Y* | Y | Y | Y | Y | **初始** | Y | Y |
| **JDK 24** | Y | Y** | Y | Y | Y | Y | Y | Y | Y |
| **JDK 25** (LTS) | Y | **移除** | Y | Y | Y | Y | Y | Y | Y |

> `*` JDK 21: JEP 449 废弃 Windows 32-bit x86
> `**` JDK 24: JEP 479 移除 Windows 32-bit x86; JEP 501 废弃 Linux 32-bit x86
> `外部` 表示非主线支持，由第三方维护

---

## 3. 详细介绍

### [x86/x64](x86.md)

Intel/AMD x86 架构，OpenJDK 最成熟的开发平台，拥有最完善的 JIT 优化。

| 属性 | 值 |
|------|-----|
| **引入版本** | JDK 1.0 (32-bit), JDK 5 (64-bit) |
| **状态** | x86_64 主流支持; x86_32 已在 JDK 25 移除 |
| **指令集扩展** | SSE, SSE2, AVX, AVX2, AVX-512 |
| **JIT 支持** | C1 + C2 完整支持，Graal 支持 |
| **主要贡献者** | Oracle, Intel |

**关键特性**:
- 最完善的 auto-vectorization 支持
- AVX-512 intrinsics (Base64 编解码、ML-DSA 加密算法加速)
- 完整的 Vector API 支持（SPECIES_512 对应 AVX-512 ZMM 寄存器）

---

### [AArch64](aarch64.md)

ARM 64 位架构，广泛用于移动设备、云服务器 (AWS Graviton)、Apple Silicon Mac。
由 Red Hat 的 Andrew Haley 和 Andrew Dinn 于 2012 年启动移植工作。

| 属性 | 值 |
|------|-----|
| **引入版本** | JDK 9 (Linux, JEP 237) |
| **macOS 支持** | JDK 17 (JEP 391, Apple Silicon) |
| **Windows 支持** | JDK 18 |
| **指令集扩展** | NEON, SVE, SVE2, LSE |
| **JIT 支持** | C1 + C2 完整支持，Graal 支持 |
| **主要贡献者** | Red Hat, Arm, Oracle, Amazon, Azul, Microsoft |

**里程碑 JEP**:

| 版本 | JEP | 说明 | 推动者 |
|------|-----|------|--------|
| JDK 9 | **JEP 237** | AArch64 Linux 移植 -- 首次将 AArch64 引入 OpenJDK 主线 | Red Hat, Linaro |
| JDK 11 | **JEP 315** | 改进 AArch64 Intrinsics -- 优化 String::compareTo、String::indexOf、StringCoding::hasNegatives、Arrays::equals 等操作，利用 NEON SIMD 指令提升性能 | Red Hat |
| JDK 12 | **JEP 340** | 统一为一个 AArch64 端口 -- 移除冗余的 arm64 端口，保留 aarch64 端口，避免重复维护 | Red Hat |
| JDK 17 | **JEP 391** | macOS/AArch64 移植 (Apple Silicon) -- 解决 macOS W^X 安全限制，使用 pthread_jit_write_protect_np 实现可写/可执行内存切换 | Azul, Microsoft |
| JDK 18 | - | Windows/AArch64 移植 | Microsoft |

**macOS/AArch64 技术要点 (JEP 391)**:
- macOS/AArch64 禁止内存段同时可写和可执行 (Write-XOR-Execute, W^X)
- HotSpot 通过 Apple 提供的 `pthread_jit_write_protect_np` API 实现 W^X 支持
- 虽然可通过 Rosetta 2 运行 x64 版 JDK，但会带来显著性能损失
- Azul 在 2020 年 8 月发起 JEP 391 社区移植工作

---

### [RISC-V](riscv.md)

开源指令集架构 (ISA)，中国厂商重点投入方向，由 Huawei 主导移植。
RISC-V 是完全开放的处理器指令集，无需支付许可费用，被视为芯片领域的"Linux"。

| 属性 | 值 |
|------|-----|
| **引入版本** | JDK 19 (JEP 422) |
| **支持配置** | RV64GV (64 位通用 + 向量指令) |
| **向量支持** | JDK 20+ (V, Zvbb, Zfa, Zvkn 扩展) |
| **JIT 支持** | C1 + C2 模板解释器 |
| **状态** | 活跃开发 |
| **主要贡献者** | Huawei, ISCAS, 阿里巴巴, Rivos |

**JEP 422 (Linux/RISC-V Port) 详解**:
- 仅支持 RV64GV 配置 -- 通用 64 位 ISA，包含向量指令
- Huawei 承诺长期维护、增强和测试该移植代码
- Huawei、阿里巴巴和 Red Hat 定期构建和测试，确保不引入回归问题
- 初始实现包含模板解释器和 C1/C2 JIT 编译器

**主要实现贡献者 (JEP 422 集成提交)**:
- **Huawei**: Yadong Wang, Fei Yang, Yanhong Zhu, Feilong Jiang, Kun Wang, Zhuxuan Ni, Taiping Guo, Kang He
- **阿里巴巴**: Xiaolin Zheng, Kuai Wei
- **审阅者**: Aleksey Shipilev (Red Hat), Magnus Ihse Bursie (Oracle)

**里程碑**:

| 版本 | 说明 |
|------|------|
| JDK 19 | **JEP 422**: RISC-V Linux 移植进入主线 |
| JDK 20 | 向量 intrinsic 初步支持 |
| JDK 21 | Zvbb (位操作) / Zfa (浮点) 扩展支持 |
| JDK 24 | 向量支持完善，性能优化 |
| JDK 25+ | 紧凑对象头 (Compact Object Headers) 支持 |

---

### [LoongArch](loongarch.md)

龙芯中科自主设计的指令集架构，基于 MIPS 架构经验发展而来。
龙芯此前已为 OpenJDK 8 完成了 MIPS64 移植（包含模板解释器和 C2 编译器）。

| 属性 | 值 |
|------|-----|
| **引入版本** | JDK 21 |
| **指令集扩展** | LSX (128-bit SIMD), LASX (256-bit SIMD) |
| **JIT 支持** | C1 + C2 |
| **状态** | 活跃开发 |
| **主要贡献者** | 龙芯中科 |
| **维护版本** | JDK 17u, JDK 21u, JDK 25u |

**关键进展**:

| 版本 | 说明 |
|------|------|
| JDK 21 | 初始移植进入主线 |
| JDK 22 | 稳定性改进，Bug 修复 |
| JDK 24 | LSX/LASX 向量指令支持 |
| JDK 25+ | 紧凑对象头支持 |

**生态建设**:
- 龙芯维护 LoongArch 版 JDK 17u/21u/25u 多版本仓库
- 推动 Adoptium Temurin 构建支持 LoongArch 平台
- 在 Alpine Linux 等发行版中提供 LoongArch JDK 包

---

### PPC64/PPC64LE

IBM PowerPC 64 位架构，主要用于 IBM Power Systems 和 AIX。

| 属性 | 值 |
|------|-----|
| **引入版本** | JDK 9 (PPC64 Big Endian), JDK 11 (PPC64LE Little Endian) |
| **状态** | 维护模式 |
| **主要贡献者** | IBM, SAP |

**主要平台**: IBM Power Systems (AIX/Linux), OpenPOWER 服务器

---

### s390x

IBM System z 大型机架构，主要用于企业级后端系统。

| 属性 | 值 |
|------|-----|
| **引入版本** | JDK 9 |
| **状态** | 维护模式 |
| **主要贡献者** | IBM |

**主要平台**: IBM Z Mainframe (Linux on System z), 银行/金融系统

---

## 4. 32 位 x86 移除时间线

32 位 x86 端口的移除是一个分阶段推进的过程，涉及多个 JEP，横跨 JDK 21 到 JDK 25。

```
JDK 21 ──── JDK 23 ──── JDK 24 ──────────────── JDK 25
  │            │           │                        │
  │            │           ├─ JEP 479: 移除          │
  │            │           │  Windows 32-bit x86     │
  │            │           │                        │
  │            │           ├─ JEP 501: 废弃          ├─ JEP 503: 移除
  │            │           │  全部 32-bit x86         │  全部 32-bit x86
  │            │           │  (Linux 剩余端口)        │  源代码和构建支持
  │            │           │                        │
  ├─ JEP 449   │           │                        │
  │  废弃 Windows           │                        │
  │  32-bit x86             │                        │
  │                         │                        │
```

| JEP | JDK 版本 | 动作 | 说明 |
|-----|----------|------|------|
| **JEP 449** | JDK 21 | 废弃 Windows 32-bit x86 | 首次发出废弃信号; 可用 `--enable-deprecated-ports=yes` 继续构建 |
| **JEP 479** | JDK 24 | **移除** Windows 32-bit x86 | Windows 10 (最后支持 32 位的 Windows) 将于 2025 年 10 月 EOL |
| **JEP 501** | JDK 24 | 废弃全部 32-bit x86 | Linux 32-bit x86 是最后的 32 位端口 |
| **JEP 503** | JDK 25 | **移除**全部 32-bit x86 | 清除所有 32 位 x86 源代码和构建支持 |

**移除原因**:
- 不再生产 32 位独占 x86 硬件，现存部署均为遗留系统
- 32 位端口无法完整支持 Virtual Threads (Loom)、Foreign Function & Memory API、Vector API 等新特性
- 维护 32 位回退代码的成本超过收益
- 移除后，仅可通过架构无关的 Zero 端口在 32 位 x86 上运行 Java（性能较低）

**实现者**: Aleksey Shipilev (Red Hat) -- [PR #23906](https://github.com/openjdk/jdk/pull/23906)

---

## 5. 按版本演进

### x86/x64

| 版本 | 变化 | JEP |
|------|------|-----|
| JDK 1.0 | x86_32 初始支持 | - |
| JDK 5 | x86_64 支持 | - |
| JDK 9 | 改进 AVX 支持 | - |
| JDK 16 | Vector API 孵化，支持 AVX-512 | JEP 338 |
| JDK 21 | 废弃 Windows 32-bit x86 | JEP 449 |
| JDK 24 | 移除 Windows 32-bit x86; 废弃 Linux 32-bit x86 | JEP 479/501 |
| JDK 25 | **移除全部 32-bit x86**; AVX-512 intrinsics 扩展 (ML-DSA) | JEP 503 |

### AArch64

| 版本 | 变化 | JEP |
|------|------|-----|
| JDK 9 | AArch64 Linux 移植 | JEP 237 |
| JDK 11 | AArch64 Intrinsics 改进 (String/Math 操作优化) | JEP 315 |
| JDK 12 | 合并为一个 AArch64 端口，移除冗余 arm64 端口 | JEP 340 |
| JDK 16 | SVE 后端初步支持; UseSVE JVM 选项引入 | - |
| JDK 17 | macOS/AArch64 (Apple Silicon) | JEP 391 |
| JDK 18 | Windows/AArch64 | - |
| JDK 21+ | SVE2 优化; Vector API 完善 NEON/SVE 支持 | - |

### RISC-V

| 版本 | 变化 | JEP |
|------|------|-----|
| JDK 19 | RISC-V Linux 移植 (RV64GV) | JEP 422 |
| JDK 20 | 向量 intrinsic 初步支持 | - |
| JDK 21 | Zvbb/Zfa 扩展支持 | - |
| JDK 24 | 向量支持完善，性能优化 | - |
| JDK 25+ | 紧凑对象头支持 | - |

### LoongArch

| 版本 | 变化 |
|------|------|
| JDK 21 | 初始移植进入主线 |
| JDK 22 | 稳定性改进 |
| JDK 24 | LSX/LASX 向量指令支持 |
| JDK 25+ | 紧凑对象头支持 |

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

## 6. 架构特定 JIT 优化

### x86/x64 -- AVX/AVX-512

```bash
# AVX 指令集版本控制 (0=无AVX, 1=AVX, 2=AVX2, 3=AVX-512)
-XX:UseAVX=3

# 向量优化
-XX:+UseVectorCmov

# 查看使用的 AVX 级别
java -XX:+PrintFlagsFinal -version 2>&1 | grep UseAVX
```

**AVX-512 优化场景**:
- Vector API 利用 512-bit ZMM 寄存器（SPECIES_512）
- Base64 编解码 intrinsic 加速
- ML-DSA 后量子密码学 intrinsic (JDK 25)
- Arrays.sort 向量化排序

**注意事项**:
- AVX-512 可能导致处理器降频，C2 编译器使用成本模型决策是否向量化
- 并非所有场景都适合 AVX-512，需根据具体工作负载评估

### AArch64 -- NEON/SVE/SVE2

```bash
# LSE 原子指令 (Large System Extensions，改善多核同步性能)
-XX:+UseLSE

# SVE 指令集版本控制 (0=仅NEON, 1=SVE, 2=SVE2)
-XX:UseSVE=2

# 查看 SVE 配置
java -XX:+PrintFlagsFinal -version 2>&1 | grep -i sve
```

**NEON (128-bit SIMD)**:
- 所有 AArch64 处理器标配
- String/Array 操作优化 (JEP 315)
- VectorMask 编译到向量寄存器

**SVE (Scalable Vector Extension)**:
- 支持 128 位到 2048 位可变向量长度
- JIT 编译时获取实际硬件 SVE 寄存器大小，寄存器分配器无需大规模修改
- 长度无关 (scalable) 向量类型设计

**SVE2 优化**:
- BEXT 指令可将 240+ 条指令降至单条指令，性能提升超 70 倍
- 针对 Vector API 的深度优化

**Predicate (谓词) 支持**:
- SVE 原生支持谓词寄存器 (predicate registers)
- NEON 平台: VectorMask 编译为普通向量寄存器，通过 blend 操作模拟掩码

### RISC-V -- V/Zvbb/Zfa 扩展

```bash
# 向量扩展自动检测
# 支持的扩展: V (基础向量), Zvbb (位操作), Zfa (浮点), Zvkn (密码学)

# 查看支持的 RISC-V 扩展
java -XX:+PrintFlagsFinal -version 2>&1 | grep -i riscv
```

**V 扩展 (基础向量)**:
- 可变长向量寄存器，类似 SVE 的 scalable 设计
- 支持 C2 向量化

**Zvbb (向量位操作)**:
- 位反转、字节反转等操作加速

**Zfa (浮点附加指令)**:
- 浮点常量加载优化

### LoongArch -- LSX/LASX

```bash
# LSX: 128-bit SIMD (Loongson SIMD Extension)
# LASX: 256-bit SIMD (Loongson Advanced SIMD Extension)
# 自动检测，无需手动配置
```

---

## 7. 贡献者

### AArch64 团队

| 贡献者 | 组织 | 主要贡献 |
|--------|------|----------|
| **[Andrew Haley](/by-contributor/profiles/andrew-haley.md)** | **Red Hat** | AArch64 移植项目发起人和领导者; OpenJDK Governing Board 成员; 与 Andrew Dinn 于 2012 年启动移植工作 |
| Andrew Dinn | Red Hat | AArch64 移植联合发起人 |
| **[Nick Gasson](/by-contributor/profiles/nick-gasson.md)** | **Arm** | AArch64 后端优化，SVE/SVE2 支持 |
| David Holmes | Oracle | AArch64 运行时支持 |
| Anton Kozlov | Azul | JEP 391 macOS/AArch64 实现主力 |
| Monica Beckwith | Microsoft | Windows/AArch64 移植推动 |

### RISC-V 团队

| 贡献者 | 组织 | 主要贡献 |
|--------|------|----------|
| **[Fei Yang (杨飞)](/by-contributor/profiles/fei-yang.md)** | **Huawei** | RISC-V Port Lead; JEP 422 主要推动者 |
| Yadong Wang | Huawei | JEP 422 核心实现 |
| Feilong Jiang | Huawei | RISC-V 后端实现 |
| Yanhong Zhu | Huawei | RISC-V 后端实现 |
| Xiaolin Zheng | 阿里巴巴 | JEP 422 实现贡献 |
| Kuai Wei | 阿里巴巴 | JEP 422 实现贡献 |
| **[Hamlin Li](/by-contributor/profiles/hamlin-li.md)** | Rivos | RISC-V 向量扩展支持 |
| **[Anjian Wen](/by-contributor/profiles/anjian-wen.md)** | 字节跳动 | Zvbb/Zfa 指令支持 |
| Dingli Zhang | ISCAS | RISC-V 测试 |
| Aleksey Shipilev | Red Hat | JEP 422 代码审阅; JEP 503 实现 |

### LoongArch 团队

| 贡献者 | 组织 | 主要贡献 |
|--------|------|----------|
| sunguoyun | 龙芯中科 | LoongArch 移植核心实现 |
| Ao Qi | 龙芯中科 | LoongArch 移植实现 |
| Jie Fu | Huawei | LoongArch 支持、代码审阅 |

### 32 位 x86 移除

| 贡献者 | 组织 | 主要贡献 |
|--------|------|----------|
| Aleksey Shipilev | Red Hat | JEP 503 实现 (32-bit x86 移除) |
| Magnus Ihse Bursie | Oracle | 构建系统清理 |

---

## 8. 相关链接

### AArch64

- [OpenJDK AArch64 Port Project](https://openjdk.org/projects/aarch64-port/)
- [JEP 237: Linux/AArch64 Port](https://openjdk.org/jeps/237)
- [JEP 315: Improve Aarch64 Intrinsics](https://openjdk.org/jeps/315)
- [JEP 340: One AArch64 Port, Not Two](https://openjdk.org/jeps/340)
- [JEP 391: macOS/AArch64 Port](https://openjdk.org/jeps/391)
- [Arm Developer -- Java Vector API on AArch64](https://developer.arm.com/community/arm-community-blogs/b/servers-and-cloud-computing-blog/posts/java-vector-api-on-aarch64)

### RISC-V

- [OpenJDK RISC-V Port Project](https://openjdk.org/projects/riscv-port/)
- [JEP 422: Linux/RISC-V Port](https://openjdk.org/jeps/422)
- [RISC-V International](https://riscv.org/)
- [ISCAS PLCT 实验室](https://github.com/plctlab)
- [JCP: State of Java on RISC-V (2024-04)](https://jcp.org/aboutJava/communityprocess/ec-public/materials/2024-04-24/JCP-State_of_OpenJDK_on_RISC-V.pdf)

### LoongArch

- [龙芯中科](https://www.loongson.cn/)
- [LoongArch 架构手册](https://loongson.github.io/LoongArch-Documentation/)
- [Loongson JDK 仓库 (GitHub)](https://github.com/loongson/jdk)

### 32 位移除

- [JEP 449: Deprecate the Windows 32-bit x86 Port for Removal](https://openjdk.org/jeps/449)
- [JEP 479: Remove the Windows 32-bit x86 Port](https://openjdk.org/jeps/479)
- [JEP 501: Deprecate the 32-bit x86 Port for Removal](https://openjdk.org/jeps/501)
- [JEP 503: Remove the 32-bit x86 Port](https://openjdk.org/jeps/503)

### Vector API

- [JEP 338: Vector API (Incubator)](https://openjdk.org/jeps/338)
- [JEP 508: Vector API (Tenth Incubator)](https://openjdk.org/jeps/508)

---

## 9. 相关主题

- [JIT 编译](../jit/) - 架构特定的编译优化和向量化
- [性能优化](../performance/) - 平台性能调优
- [GC](../gc/) - 架构特定的 GC 优化
- [安全](../security/) - 后量子密码学的架构特定 intrinsics
