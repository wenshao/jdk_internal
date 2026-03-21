# AArch64 (ARM64)

> ARM 64位架构支持

[← 返回 CPU 架构](./)

---
## 目录

1. [概述](#1-概述)
2. [版本历史](#2-版本历史)
3. [平台支持](#3-平台支持)
4. [核心特性](#4-核心特性)
5. [汇编模板](#5-汇编模板)
6. [JVM 参数](#6-jvm-参数)
7. [贡献者](#7-贡献者)
8. [构建 AArch64 JDK](#8-构建-aarch64-jdk)
9. [性能特性](#9-性能特性)
10. [已知问题](#10-已知问题)
11. [相关 JEP](#11-相关-jep)
12. [相关链接](#12-相关链接)
13. [相关主题](#13-相关主题)

---


## 1. 概述

AArch64 是 ARM 64位架构，广泛用于移动设备、云服务器和 Apple Silicon Mac。OpenJDK 从 JDK 9 开始支持 AArch64。

```
┌─────────────────────────────────────────────────────────────┐
│                    AArch64 支持矩阵                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Linux AArch64     macOS AArch64     Windows AArch64       │
│   (JDK 9)           (JDK 17)          (JDK 18)              │
│                                                             │
│   ┌─────────┐       ┌─────────┐       ┌─────────┐          │
│   │ AWS     │       │ Apple   │       │ Surface │          │
│   │ Graviton│       │ Silicon │       │ Pro X   │          │
│   │ Ampere  │       │ M1/M2/M3│       │ Snapdragon│         │
│   └─────────┘       └─────────┘       └─────────┘          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. 版本历史

| 版本 | JEP | 平台 | 说明 |
|------|-----|------|------|
| **JDK 9** | JEP 237 | Linux/AArch64 | 首次引入 |
| **JDK 17** | JEP 383 | macOS/AArch64 | Apple Silicon 支持 |
| **JDK 18** | - | Windows/AArch64 | Windows ARM 支持 |
| **JDK 19** | - | 改进 | 性能优化 |
| **JDK 21** | - | 改进 | 向量 intrinsic 增强 |

---

## 3. 平台支持

### Linux/AArch64 (JDK 9+)

主要服务器平台：

| 服务器 | CPU | 状态 |
|--------|-----|------|
| **AWS Graviton** | Graviton2/3 | ✅ 完全支持 |
| **Ampere Altra** | Neoverse N1 | ✅ 完全支持 |
| **Oracle Cloud** | Ampere A1 | ✅ 完全支持 |
| **华为鲲鹏** | Kunpeng 920 | ✅ 完全支持 |
| **飞腾** | FT-2000 | ✅ 完全支持 |

### macOS/AArch64 (JDK 17+)

Apple Silicon 支持：

| 设备 | 芯片 | 状态 |
|------|------|------|
| **MacBook Pro** | M1/M2/M3/M4 | ✅ 原生支持 |
| **MacBook Air** | M1/M2/M3/M4 | ✅ 原生支持 |
| **Mac mini** | M1/M2/M4 | ✅ 原生支持 |
| **Mac Studio** | M1/M2 Ultra | ✅ 原生支持 |
| **iMac** | M1/M3/M4 | ✅ 原生支持 |
| **iPad Pro** | M1/M2/M4 | ⚠️ 间接 (iOS) |

### Windows/AArch64 (JDK 18+)

Windows ARM 设备：

| 设备 | CPU | 状态 |
|------|-----|------|
| **Surface Pro X** | SQ1/SQ2 | ✅ 支持 |
| **Surface Pro 9** | SQ3 | ✅ 支持 |
| **Surface Pro 11** | Snapdragon X Elite | ✅ 支持 |
| **ThinkPad X13s** | Snapdragon 8cx | ✅ 支持 |
| **Dell XPS 13** | Snapdragon X Elite | ✅ 支持 |
| **Samsung Galaxy Book4 Edge** | Snapdragon X Elite | ✅ 支持 |

---

## 4. 核心特性

### NEON 向量

AArch64 的 SIMD 指令集：

```asm
// NEON 向量加法
fadd v0.4s, v1.4s, v2.4s

// NEON 向量乘法
fmul v0.4s, v1.4s, v2.4s

// NEON 向量加载
ld1 {v0.4s}, [x0]
```

### SVE (Scalable Vector Extension)

可扩展向量扩展：

```asm
// SVE 向量加载
ld1w z0.s, p0/z, [x0]

// SVE 向量加法
fadd z0.s, p0/m, z1.s, z2.s
```

**SVE 支持状态**:
| 版本 | 状态 |
|------|------|
| JDK 17 | 实验性 |
| JDK 21 | 部分支持 |
| JDK 26 | 增强支持 |

### SVE2 (Scalable Vector Extension 2)

SVE2 是 SVE 的扩展，增加了更多指令：

| 特性 | 说明 | JDK 支持 |
|------|------|----------|
| **整数分解** | 向量分解指令 | JDK 24+ |
| **矩阵乘法** | 向量矩阵指令 | JDK 25+ |
| **加密** | 向量加密指令 | JDK 26+ |

**支持硬件**:
- Apple M4 (SVE2)
- Arm Neoverse V2/V3
- AWS Graviton 4

### PAC/BTI

指针认证和分支目标识别（安全特性）：

```bash
# 启用 PAC (指针认证)
-XX:+UsePAC

# 启用 BTI (分支目标识别)
-XX:+UseBTI
```

---

## 5. 汇编模板

### 基本指令

```cpp
// src/hotspot/cpu/aarch64/assembler_aarch64.hpp

// 加法
void add(Register Rd, Register Rn, Register Rm);
void add(Register Rd, Register Rn, int imm);

// 乘法
void mul(Register Rd, Register Rn, Register Rm);

// 分支
void br(Register Rn);
void blr(Register Rn);

// 比较并分支
void cmp(Register Rn, Register Rm);
void b(Condition cond, Label& L);
```

### 内存屏障

```cpp
// 内存屏障
void membar(Membar_mask_bits order_constraint);

// DMB (Data Memory Barrier)
void dmb(BarrierKind kind);

// DSB (Data Synchronization Barrier)
void dsb(BarrierKind kind);
```

### GC Barrier

```cpp
// G1 Barrier 示例
void g1_write_barrier_pre(Register pre_val,
                          Register obj,
                          Register tmp1,
                          Register tmp2);

void g1_write_barrier_post(Register store_addr,
                           Register new_val,
                           Register tmp1,
                           Register tmp2);
```

---

## 6. JVM 参数

### AArch64 特定参数

```bash
# 查看 AArch64 特定参数
java -XX:+PrintFlagsFinal -version | grep -i aarch64

# 启用 NEON (默认)
-XX:+UseNEON

# 启用 SVE (实验性)
-XX:+UseSVE

# 启用 PAC (指针认证)
-XX:+UsePAC

# 启用 BTI (分支目标识别)
-XX:+UseBTI

# 禁用 LSE (大系统扩展)
-XX:-UseLSE
```

### 性能调优

```bash
# 大页内存
-XX:+UseLargePages

# 压缩指针 (默认启用)
-XX:+UseCompressedOops

# 向量化
-XX:+UseSuperWord

# 逃逸分析
-XX:+DoEscapeAnalysis
```

---

## 7. 贡献者

### 核心贡献者

| 贡献者 | 组织 | 主要贡献 |
|--------|------|----------|
| Andrew Dinn | Red Hat | AArch64 Port |
| Nick Gasson | - | macOS/AArch64 |
| Stuart Monteith | - | AArch64 优化 |
| Adhemerval Zanella | Linaro | Linux/AArch64 |

### 组织贡献

| 组织 | 贡献者 | 主要领域 |
|------|--------|----------|
| **Oracle** | - | Port 维护 |
| **Red Hat** | Andrew Dinn | Linux/AArch64 |
| **Arm** | - | 架构优化 |
| **Apple** | - | macOS/AArch64 |
| **Amazon** | - | Graviton 优化 |
| **Linaro** | - | 生态系统 |

---

## 8. 构建 AArch64 JDK

### Linux/AArch64

```bash
# 原生编译 (在 AArch64 机器上)
bash configure
make images

# 交叉编译 (从 x86_64)
bash configure \
    --openjdk-target=aarch64-linux-gnu \
    --with-boot-jdk=$JAVA_HOME
make images
```

### macOS/AArch64

```bash
# 在 Apple Silicon Mac 上
bash configure
make images

# 输出 Universal Binary
bash configure \
    --with-macosx-cpu-arch=universal
make images
```

### Windows/AArch64

```bash
# 交叉编译
bash configure \
    --openjdk-target=aarch64-windows-msvc \
    --with-boot-jdk=$JAVA_HOME
make images
```

---

## 9. 性能特性

### AWS Graviton 优化

```bash
# Graviton 2/3 推荐参数
java -XX:+UseG1GC \
     -XX:+UseStringDeduplication \
     -XX:+UseCompressedOops \
     -XX:+UseLargePages \
     -Xms4g -Xmx4g \
     MyApp
```

### Apple Silicon 优化

```bash
# M1/M2/M3 推荐参数
java -XX:+UseZGC \
     -XX:+ZGenerational \
     -XX:+UseCompressedOops \
     -Xms2g -Xmx2g \
     MyApp
```

---

## 10. 已知问题

### macOS/AArch64

| 问题 | 状态 | 说明 |
|------|------|------|
| Rosetta 2 性能 | ✅ 已解决 | 原生 AArch64 |
| JNI 库兼容 | ⚠️ 注意 | 需要 ARM64 库 |
| Native Image | ✅ 支持 | GraalVM 支持 |

### Windows/AArch64

| 问题 | 状态 | 说明 |
|------|------|------|
| x86 模拟 | ✅ 支持 | 可运行 x86 应用 |
| JNI 库兼容 | ⚠️ 注意 | 需要 ARM64 库 |

---

## 11. 相关 JEP

| JEP | 版本 | 标题 |
|-----|------|------|
| JEP 237 | JDK 9 | Linux/AArch64 Port |
| JEP 315 | JDK 11 | Improve AArch64 Intrinsics |
| JEP 383 | JDK 17 | macOS/AArch64 Port |

---

## 12. 相关链接

- [ARM Developer](https://developer.arm.com/)
- [OpenJDK AArch64 Port](https://openjdk.org/projects/aarch64-port/)
- [AWS Graviton](https://aws.amazon.com/ec2/graviton/)
- [Apple Silicon](https://developer.apple.com/silicon/)

---

## 13. 相关主题

- [CPU 架构](./) - 其他架构支持
- [JIT 编译](../jit/) - 架构特定的编译优化
- [GC](../gc/) - GC Barrier 实现
