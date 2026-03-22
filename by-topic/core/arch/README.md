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
7. [x86-64 后端深入](#7-x86-64-后端深入-x86-64-backend-internals)
8. [AArch64 后端深入](#8-aarch64-后端深入-aarch64-backend-internals)
9. [RISC-V 后端深入](#9-risc-v-后端深入-risc-v-backend-internals)
10. [跨平台挑战](#10-跨平台挑战-cross-platform-challenges)
11. [CPU 特性检测](#11-cpu-特性检测-cpu-feature-detection)
12. [平台特定优化](#12-平台特定优化-platform-specific-optimizations)
13. [贡献者](#13-贡献者)
14. [相关链接](#14-相关链接)
15. [相关主题](#15-相关主题)

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
| **x86_32** | 32-bit | JDK 21.0 | **JDK 25 已移除** | Oracle | JEP 449/479/501/503 |
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
- **审阅者**: Aleksey Shipilev (formerly Red Hat, now Amazon), Magnus Ihse Bursie (Oracle)

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

**实现者**: Aleksey Shipilev (Amazon) -- [PR #23906](https://github.com/openjdk/jdk/pull/23906)

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

## 7. x86-64 后端深入 (x86-64 Backend Internals)

### 寄存器分配 (Register Allocation)

x86-64 提供 16 个通用寄存器 (GPR: RAX-R15) 和 16/32 个 SIMD 寄存器 (XMM/YMM/ZMM)。C2 编译器使用 **线性扫描寄存器分配** (Linear Scan Register Allocation) 将虚拟寄存器映射到物理寄存器。

**寄存器约定 (Register Convention)**:

| 寄存器 | HotSpot 用途 | 说明 |
|--------|-------------|------|
| `RSP` | Java 栈指针 (Stack Pointer) | 不可用于分配 |
| `RBP` | 帧指针 (Frame Pointer) | `-XX:+PreserveFramePointer` 时保留 |
| `R15` | Java 堆基址 (Heap Base) | 压缩指针 (Compressed Oops) 模式下存放 narrow oop base |
| `R12` | Java Thread 指针 | 指向当前 JavaThread 结构体 |
| `RAX` | 返回值 / 临时寄存器 | C2 也用作 method handle 调用临时寄存器 |
| `XMM0-XMM15` | 浮点 / SIMD 操作 | AVX-512 扩展到 ZMM0-ZMM31 (32 个 512-bit 寄存器) |

### 指令选择 (Instruction Selection)

C2 使用 **AD 文件** (Architecture Description File, `x86_64.ad`) 描述指令选择规则，将 Ideal IR 节点匹配到机器指令:

```
// x86_64.ad 中的指令模式示例 (Instruction Pattern Example)
// 匹配 AddI 节点 → 生成 x86 ADD 指令
instruct addI_rReg(rRegI dst, rRegI src, rFlagsReg cr)
%{
  match(Set dst (AddI dst src));
  effect(KILL cr);
  format %{ "addl   $dst, $src" %}
  ins_encode %{ __ addl($dst$$Register, $src$$Register); %}
%}
```

**关键 AD 文件**: `src/hotspot/cpu/x86/x86_64.ad` — 超过 12,000 行的指令模式定义。

### SIMD/AVX 向量化支持 (SIMD/AVX Vectorization)

x86-64 的 SIMD 支持分为多个层级:

| 指令集 | 寄存器宽度 | UseAVX 值 | 典型处理器 |
|--------|-----------|-----------|-----------|
| SSE2 | 128-bit (XMM) | 0 | Pentium 4+ (2001) |
| AVX | 256-bit (YMM) | 1 | Sandy Bridge (2011) |
| AVX2 | 256-bit (YMM) | 2 | Haswell (2013) |
| AVX-512 | 512-bit (ZMM) | 3 | Skylake-SP (2017) |

**AVX-512 降频问题 (Throttling Issue)**:
- 使用 512-bit ZMM 寄存器时，部分 Intel 处理器会降低核心频率 (license-based frequency throttling)
- C2 的 SuperWord 自动向量化使用成本模型 (cost model) 评估是否使用 AVX-512
- `-XX:UseAVX=2` 可强制限制在 AVX2，避免降频风险
- Ice Lake (2019) 及之后的处理器已大幅缓解降频问题

### 内存模型: TSO (Total Store Order)

x86-64 实现 **TSO (Total Store Order)** 内存模型，这是一种相对较强的内存序:

```
┌──────────────────────────────────────────────────────┐
│  x86-64 TSO 保证 (TSO Guarantees)                      │
├──────────────────────────────────────────────────────┤
│  ✓ Store-Store 有序 (stores not reordered with stores) │
│  ✓ Load-Load 有序 (loads not reordered with loads)     │
│  ✓ Load-Store 有序 (loads not reordered with stores)   │
│  ✗ Store-Load 可重排 (stores CAN be reordered with     │
│    subsequent loads → 需要 MFENCE/LOCK 前缀)           │
└──────────────────────────────────────────────────────┘
```

**对 JIT 编译的影响**:
- Java 的 `volatile` 写操作编译为 `MOV` + `LOCK ADDL [RSP], 0` (StoreLoad barrier)
- 大多数其他 JMM (Java Memory Model) 操作在 x86 上无需额外内存屏障指令
- `VarHandle` 的 `setRelease` 在 x86 上是免费的 (free)，因为 TSO 已保证 Store-Store 顺序

---

## 8. AArch64 后端深入 (AArch64 Backend Internals)

### ARM 特性利用 (ARM Feature Utilization)

AArch64 提供 31 个通用寄存器 (X0-X30) 和 32 个 SIMD/FP 寄存器 (V0-V31)，寄存器资源比 x86-64 更丰富。

**寄存器约定**:

| 寄存器 | HotSpot 用途 |
|--------|-------------|
| `X28` (R28) | Java Thread 指针 |
| `X27` (RHeapBase) | 压缩指针堆基址 |
| `X29` (FP) | 帧指针 |
| `X30` (LR) | 链接寄存器 (返回地址) |
| `X8` (Rscratch1) | 临时寄存器 1 |
| `X9` (Rscratch2) | 临时寄存器 2 |

**条件指令 (Conditional Instructions)**:
- AArch64 支持条件选择 (`CSEL`)、条件递增 (`CINC`) 等指令
- C2 可将简单的 `if-else` 模式编译为无分支代码 (branchless code)，避免分支预测失败的性能损失

### W^X: Write-XOR-Execute (JEP 391)

macOS/AArch64 (Apple Silicon) 强制执行 W^X 内存策略 — 内存页不能同时拥有写 (W) 和执行 (X) 权限。这对 JIT 编译器是根本性挑战，因为 JIT 需要先写入机器码再执行。

**HotSpot 解决方案**:

```
┌──────────────────────────────────────────────────────┐
│  W^X 实现流程 (W^X Implementation Flow)                │
├──────────────────────────────────────────────────────┤
│                                                       │
│  1. pthread_jit_write_protect_np(false)               │
│     → 切换到 可写模式 (writable)                        │
│                                                       │
│  2. 写入 JIT 编译后的机器码                              │
│     → memcpy() / Code emission                         │
│                                                       │
│  3. pthread_jit_write_protect_np(true)                │
│     → 切换到 可执行模式 (executable)                     │
│                                                       │
│  4. sys_icache_invalidate()                           │
│     → 刷新指令缓存 (flush I-cache)                      │
│                                                       │
│  注意: 此 API 是 per-thread 的，不影响其他线程             │
└──────────────────────────────────────────────────────┘
```

**关键实现细节**:
- Apple 的 `MAP_JIT` 标志用于分配 JIT 内存区域
- `pthread_jit_write_protect_np` 基于 ARM 的 TPIDR_EL0 寄存器切换，开销极低 (纳秒级)
- Linux/AArch64 不需要 W^X — 使用标准的 `mprotect()` 即可
- 指令缓存 (I-cache) 与数据缓存 (D-cache) 在 AArch64 上不保证一致性，必须显式刷新

### LSE 原子操作 (Large System Extensions Atomics)

ARMv8.1 引入的 LSE (Large System Extensions) 提供硬件原子指令，替代传统的 LL/SC (Load-Linked/Store-Conditional) 循环:

| 传统 LL/SC | LSE 原子指令 | 用途 |
|-----------|-------------|------|
| `LDXR`+`STXR` 循环 | `LDADD` | 原子加法 |
| `LDXR`+`STXR` 循环 | `SWPAL` | 原子交换 (acquire-release) |
| `LDXR`+`STXR` 循环 | `CAS` / `CASAL` | 比较并交换 (CAS) |

**性能影响**:
- 高竞争场景 (high contention): LSE 原子操作比 LL/SC 快 **3-10 倍**
- 低竞争场景: 性能差异较小
- HotSpot 通过 `-XX:+UseLSE` 控制 (默认在支持的硬件上启用)
- AWS Graviton2+、Apple M1+ 等现代 ARM 处理器均支持 LSE

### NEON/SVE 向量化 (NEON/SVE Vectorization)

**NEON (固定 128-bit)**:
- 所有 AArch64 处理器均支持，是 Vector API 在 ARM 上的基线实现
- 32 个 128-bit 向量寄存器 (V0-V31)
- 缺少原生谓词 (predicate) 支持 — VectorMask 需要编译为普通向量寄存器 + blend

**SVE (可伸缩 128-2048 bit)**:
- 向量长度在硬件层面确定，软件无需修改即可利用不同宽度
- 引入专用谓词寄存器 (P0-P15)，天然支持 VectorMask
- AWS Graviton3: 256-bit SVE; Fujitsu A64FX: 512-bit SVE
- C2 编译时调用 `VM_Version::sve_vector_length()` 获取运行时向量长度

**SVE2 关键优化实例**:
- `BEXT` (Bit Extract): 将位域提取操作从 240+ 条指令降至 1 条
- `BDEP` (Bit Deposit): 位域存放操作同样大幅简化
- `HISTCNT` (Histogram Count): 向量化直方图统计

---

## 9. RISC-V 后端深入 (RISC-V Backend Internals)

### JEP 422 Port 架构

RISC-V 移植基于 **RV64GV** 配置 — 即 RV64I (基础整数) + M (乘除) + A (原子) + F (单精度浮点) + D (双精度浮点) + C (压缩指令) + V (向量扩展):

```
RV64GV = RV64I + M + A + F + D + C + V
         │       │   │   │   │   │   └─ Vector 扩展 (可变长 SIMD)
         │       │   │   │   │   └─ Compressed 指令 (16-bit 编码)
         │       │   │   │   └─ Double-precision 浮点
         │       │   │   └─ Single-precision 浮点
         │       │   └─ Atomic 指令 (LR/SC, AMO)
         │       └─ Multiply/Divide
         └─ Base Integer (64-bit)
```

**寄存器资源**:
- 32 个通用寄存器 (x0-x31), 其中 x0 硬连线为零
- 32 个浮点寄存器 (f0-f31)
- 32 个向量寄存器 (v0-v31), 宽度由硬件决定 (VLEN)

**HotSpot RISC-V 寄存器约定**:

| 寄存器 | ABI 名称 | HotSpot 用途 |
|--------|---------|-------------|
| `x2` | sp | 栈指针 |
| `x4` | tp | Java Thread 指针 |
| `x8` | s0/fp | 帧指针 |
| `x27` | s11 | 堆基址 (Heap Base) |
| `x10-x17` | a0-a7 | 参数传递 / 返回值 |
| `x28` | t3 | 临时寄存器 |

### RVV 向量扩展 (RISC-V Vector Extension)

RVV 采用与 ARM SVE 类似的 **可伸缩向量** (scalable vector) 设计，但有独特的 LMUL (Length Multiplier) 机制:

**LMUL 分组 (Register Grouping)**:
- LMUL=1: 每个向量操作使用 1 个向量寄存器
- LMUL=2: 每个向量操作使用 2 个相邻寄存器 (有效宽度翻倍)
- LMUL=4/8: 使用 4/8 个寄存器组成更宽的逻辑向量
- 这允许软件在向量宽度和可用寄存器数量之间权衡

**Vector API 映射**:
- Vector API 的 `SPECIES_PREFERRED` 映射到硬件的 VLEN × LMUL
- `VectorMask` 利用 RVV 的 `v0.t` 谓词机制
- C2 向量化通过 `vsetvli` 指令设置向量长度和元素类型

**当前支持的 RVV intrinsics (JDK 25)**:
- `Arrays.fill` / `Arrays.copyOf` 向量化
- `String.indexOf` / `String.compareTo` 加速
- 密码学: Zvkn (向量化 AES/SHA)
- 位操作: Zvbb (字节反转、位计数)

### 当前状态和限制 (Current Status & Limitations)

**已完成**:
- 模板解释器 (Template Interpreter) — 完整实现
- C1 JIT 编译器 — 完整实现
- C2 JIT 编译器 — 基本实现，持续优化中
- RVV 向量化 — 基础支持，核心 intrinsics 已覆盖

**已知限制 (JDK 25 时间点)**:
- **硬件可用性**: 高性能 RISC-V 硬件 (SiFive P870, SpacemiT K1) 仍在早期阶段
- **C2 优化深度**: 与 x86-64 相比，RISC-V 的指令调度和窥孔优化 (peephole optimization) 仍不完善
- **向量化覆盖率**: RVV intrinsics 覆盖面不如 x86 AVX 和 ARM NEON 广泛
- **Graal 支持**: RISC-V 尚无 Graal JIT 支持 (仅 C1 + C2)
- **紧凑对象头**: Compact Object Headers (JEP 519) 的 RISC-V 支持正在开发中
- **测试基础设施**: CI 硬件资源有限，部分测试通过 QEMU 模拟运行

---

## 10. 跨平台挑战 (Cross-Platform Challenges)

### 内存模型差异 (Memory Model Differences)

不同 CPU 架构的内存模型强弱差异显著，这是 JVM 移植的核心挑战之一:

```
强 ←────────────────────────────────────────────────→ 弱
  x86-64 (TSO)    RISC-V (RVWMO)   AArch64 (弱序)
  ─────────       ──────────       ──────────
  仅 Store→Load   大部分操作       所有操作
  可重排           可重排           可重排
  │               │                │
  │  volatile 写:  │  volatile 写:  │  volatile 写:
  │  MOV+LOCK ADD  │  FENCE rw,rw   │  STLR
  │               │  +SW            │  (store-release)
  │               │  +FENCE rw,rw   │
  │               │                │
  │  acquire:     │  acquire:      │  acquire:
  │  免费 (free)   │  FENCE r,rw    │  LDAR
  │               │                │  (load-acquire)
  │               │                │
  │  release:     │  release:      │  release:
  │  免费 (free)   │  FENCE rw,w    │  STLR
  │               │                │
```

**JMM (Java Memory Model) 到硬件指令的映射**:

| JMM 操作 | x86-64 | AArch64 | RISC-V |
|----------|--------|---------|--------|
| Normal Load | `MOV` | `LDR` | `LW/LD` |
| Normal Store | `MOV` | `STR` | `SW/SD` |
| Volatile Load | `MOV` | `LDAR` (load-acquire) | `FENCE iorw,iorw` + `LW` + `FENCE r,rw` |
| Volatile Store | `MOV` + `LOCK ADDL [RSP],0` | `STLR` (store-release) + `DMB ISH` | `FENCE rw,w` + `SW` + `FENCE rw,rw` |
| CAS | `LOCK CMPXCHG` | `LDAXR`+`STLXR` 或 `CASAL` (LSE) | `LR.W.AQ` + `SC.W.RL` 或 `AMOSWAP` |

### 原子操作映射 (Atomic Operation Mapping)

`Unsafe.compareAndSwap` (以及 `VarHandle.compareAndSet`) 在不同架构上的实现差异:

- **x86-64**: 单条 `LOCK CMPXCHG` 指令，天然提供 sequential consistency
- **AArch64 (无 LSE)**: `LDXR`/`STXR` 循环 + 内存屏障，失败时需要重试
- **AArch64 (有 LSE)**: 单条 `CASAL` 指令，类似 x86 的简洁性
- **RISC-V**: `LR.W.AQ`/`SC.W.RL` (Load-Reserved/Store-Conditional) 循环

### 信号处理差异 (Signal Handling Differences)

HotSpot 使用操作系统信号实现多种运行时功能:

| 功能 | 信号 (Linux) | x86-64 | AArch64 | RISC-V |
|------|-------------|--------|---------|--------|
| NullPointerException | `SIGSEGV` | 访问地址 0 触发 | 相同 | 相同 |
| StackOverflowError | `SIGSEGV` | 红区/黄区保护页 | 相同 | 相同 |
| Safepoint polling | `SIGSEGV` | 读取受保护的 polling 页 | 相同 | 相同 |
| 隐式除零 | `SIGFPE` | 硬件自动触发 | **需要软件检查** (ARM 无除零异常) | **需要软件检查** |

**AArch64/RISC-V 除零处理**: 这两种架构的整数除零不会产生硬件异常，HotSpot 需要在除法操作前插入显式的零检查指令 (explicit zero-check)。

---

## 11. CPU 特性检测 (CPU Feature Detection)

### VM_Version 机制

HotSpot 在启动时通过 `VM_Version` 类检测 CPU 能力，各架构有独立实现:

```
src/hotspot/cpu/x86/vm_version_x86.cpp     // CPUID 指令检测
src/hotspot/cpu/aarch64/vm_version_aarch64.cpp  // /proc/cpuinfo 或 MRS 指令
src/hotspot/cpu/riscv/vm_version_riscv.cpp  // /proc/cpuinfo 解析
```

**x86-64 检测流程**:
1. 执行 `CPUID` 指令获取处理器特性叶 (feature leaves)
2. 检测 SSE, AVX, AVX2, AVX-512 等指令集支持
3. 检测 XSAVE 支持 (OS 是否保存 AVX 寄存器状态)
4. 根据检测结果设置 `UseAVX`、`UseSSE42`、`UseAES` 等标志

**AArch64 检测流程**:
1. Linux: 读取 `/proc/cpuinfo` 的 `Features` 字段或使用 `getauxval(AT_HWCAP)`
2. macOS: 使用 `sysctlbyname("hw.optional.arm.*")` 查询
3. 检测 NEON (始终可用)、CRC32、SHA、AES、SVE、LSE 等特性

### 关键 JVM 特性标志 (Key JVM Feature Flags)

**x86-64 标志**:

| 标志 | 默认值 | 说明 |
|------|--------|------|
| `-XX:UseAVX=N` | 自动检测 | AVX 级别: 0 (无), 1 (AVX), 2 (AVX2), 3 (AVX-512) |
| `-XX:UseSSE=N` | 自动检测 | SSE 级别 |
| `-XX:+UseAES` | 自动 | AES-NI 硬件加速 |
| `-XX:+UseAESCTRIntrinsics` | 自动 | AES-CTR 模式 intrinsic |
| `-XX:+UseSHA` | 自动 | SHA 硬件加速 |
| `-XX:+UseAdler32Intrinsics` | true | Adler32 校验和 intrinsic |

**AArch64 标志**:

| 标志 | 默认值 | 说明 |
|------|--------|------|
| `-XX:UseSVE=N` | 自动检测 | SVE 级别: 0 (NEON only), 1 (SVE), 2 (SVE2) |
| `-XX:+UseLSE` | 自动 | LSE 原子指令 |
| `-XX:+UseNeon` | true | NEON SIMD (始终启用) |
| `-XX:+UseSIMDForMemoryOps` | true | 使用 SIMD 指令进行内存操作 |
| `-XX:+UseCRC32` | 自动 | CRC32 硬件加速 |

**RISC-V 标志**:

| 标志 | 默认值 | 说明 |
|------|--------|------|
| `-XX:+UseRVV` | 自动检测 | RVV 向量扩展 |
| `-XX:+UseZba` | 自动 | 地址生成加速扩展 |
| `-XX:+UseZbb` | 自动 | 基础位操作扩展 |
| `-XX:+UseZbs` | 自动 | 单比特操作扩展 |
| `-XX:+UseZicboz` | 自动 | 缓存行清零扩展 |

### 运行时特性查询

```bash
# 查看 JVM 检测到的 CPU 特性
java -XX:+PrintFlagsFinal -version 2>&1 | grep -E "UseAVX|UseSVE|UseLSE|UseAES|UseRVV"

# 打印详细 CPU 特性检测结果
java -XX:+UnlockDiagnosticVMOptions -XX:+PrintCPUFeatures -version
```

---

## 12. 平台特定优化 (Platform-Specific Optimizations)

### Intrinsics 机制 (Intrinsics Mechanism)

HotSpot **intrinsics** 是 JIT 编译器对特定 Java 方法的手写汇编替换，绕过常规编译流程以获得最佳性能。每个架构有各自的 intrinsic 实现:

```
src/hotspot/cpu/x86/stubGenerator_x86_64.cpp        // x86-64 intrinsic stubs
src/hotspot/cpu/aarch64/stubGenerator_aarch64.cpp    // AArch64 intrinsic stubs
src/hotspot/cpu/riscv/stubGenerator_riscv.cpp        // RISC-V intrinsic stubs
```

**intrinsic 注册流程**:
1. `vmIntrinsics.hpp` 定义全局 intrinsic ID 枚举
2. `c2_MacroAssembler_<arch>.cpp` 实现架构特定的代码生成
3. C2 编译时检查方法是否有 `@IntrinsicCandidate` 注解 + 是否有对应平台实现
4. 若匹配，替换为手写汇编；否则回退到正常编译

**各架构 intrinsic 覆盖率对比 (JDK 25)**:

| 方法类别 | x86-64 | AArch64 | RISC-V |
|---------|--------|---------|--------|
| `String` 操作 | 完整 | 完整 | 部分 |
| `Math` 函数 | 完整 | 完整 | 基本 |
| `Arrays` 操作 | 完整 | 完整 | 部分 |
| AES/SHA 加密 | 完整 (AES-NI) | 完整 (ARMv8 Crypto) | 部分 (Zvkn) |
| Base64 编解码 | AVX-512 优化 | NEON 优化 | 基本 |
| CRC32/CRC32C | 硬件加速 | 硬件加速 | 软件实现 |
| ML-DSA 后量子密码学 | AVX-512 (JDK 25) | 开发中 | 无 |

### Unsafe → VarHandle 迁移 (Migration from Unsafe to VarHandle)

`sun.misc.Unsafe` 提供底层内存操作 (CAS、内存屏障、直接内存访问)，长期以来是高性能库的核心依赖。JDK 9 引入 `VarHandle` 作为标准替代:

**迁移对照**:

| Unsafe 方法 | VarHandle 等价 | 内存序语义 |
|------------|---------------|-----------|
| `compareAndSwapInt` | `VarHandle.compareAndSet` | volatile (sequential consistency) |
| `compareAndSwapObject` | `VarHandle.compareAndSet` | volatile |
| `getIntVolatile` | `VarHandle.getVolatile` | volatile load |
| `putIntVolatile` | `VarHandle.setVolatile` | volatile store |
| `putOrderedInt` | `VarHandle.setRelease` | release (写屏障) |
| `getObject` | `VarHandle.get` | plain (无屏障) |
| `loadFence` | `VarHandle.loadLoadFence` | LoadLoad + LoadStore |
| `storeFence` | `VarHandle.storeStoreFence` | StoreStore |
| `fullFence` | `VarHandle.fullFence` | Full fence |

**VarHandle 的架构优势**:
- 提供细粒度的内存序语义 (`getAcquire`/`setRelease`/`getOpaque` 等)
- 在弱序架构 (AArch64, RISC-V) 上可选择更轻量的屏障，而非总是使用最重的 volatile
- 例如: `VarHandle.setRelease` 在 x86 上是 free (TSO 保证)，在 AArch64 上生成 `STLR` (比 `DMB ISH` + `STR` 更轻量)
- JIT 编译器可根据具体访问模式和目标架构选择最优指令

**迁移现状 (JDK 25)**:
- JDK 内部代码已大量使用 `VarHandle` 替代 `Unsafe`
- `java.util.concurrent` 包已完全迁移到 `VarHandle`
- `Unsafe` 的内存访问方法标记为 `@Deprecated(forRemoval=true)` (JEP 471)
- 第三方库 (Netty, Disruptor, Caffeine) 逐步迁移中

---

## 13. 贡献者

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
| Aleksey Shipilev | Amazon (formerly Red Hat) | JEP 422 代码审阅; JEP 503 实现 |

### LoongArch 团队

| 贡献者 | 组织 | 主要贡献 |
|--------|------|----------|
| sunguoyun | 龙芯中科 | LoongArch 移植核心实现 |
| Ao Qi | 龙芯中科 | LoongArch 移植实现 |
| Jie Fu | Huawei | LoongArch 支持、代码审阅 |

### 32 位 x86 移除

| 贡献者 | 组织 | 主要贡献 |
|--------|------|----------|
| Aleksey Shipilev | Amazon | JEP 503 实现 (32-bit x86 移除) |
| Magnus Ihse Bursie | Oracle | 构建系统清理 |

---

## 14. 相关链接

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

## 15. 相关主题

- [JIT 编译](../jit/) - 架构特定的编译优化和向量化
- [性能优化](../performance/) - 平台性能调优
- [GC](../gc/) - 架构特定的 GC 优化
- [安全](../../security/security/) - 后量子密码学的架构特定 intrinsics
