# LoongArch 架构支持

> 龙芯中科自主指令集架构的 OpenJDK 移植

[← 返回 CPU 架构](./)

---

## 1. 概述

LoongArch (龙架构) 是龙芯中科自主研发的指令集架构，OpenJDK 从 JDK 21 开始支持 LoongArch 64位平台。

```
┌─────────────────────────────────────────────────────────────┐
│                    LoongArch 生态                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   OpenJDK LoongArch Port                                    │
│   ┌─────────────────────────────────────────────────────┐  │
│   │                  HotSpot VM                          │  │
│   │  ┌─────────┐  ┌─────────┐  ┌─────────┐              │  │
│   │  │   C1    │  │   C2    │  │ 解释器   │              │  │
│   │  │ Compiler│  │ Compiler│  │         │              │  │
│   │  └────┬────┘  └────┬────┘  └────┬────┘              │  │
│   │       │            │            │                    │  │
│   │       └────────────┼────────────┘                    │  │
│   │                    │                                  │  │
│   │                    ▼                                  │  │
│   │  ┌─────────────────────────────────────────────┐    │  │
│   │  │         loongarch.ad (汇编模板)              │    │  │
│   │  └─────────────────────────────────────────────┘    │  │
│   │                    │                                  │  │
│   │                    ▼                                  │  │
│   │  ┌─────────────────────────────────────────────┐    │  │
│   │  │        LoongArch 指令集                       │    │  │
│   │  │  LA32 LA64 LSX LASX                          │    │  │
│   │  └─────────────────────────────────────────────┘    │  │
│   └─────────────────────────────────────────────────────┘  │
│                                                             │
│   主要贡献者: 龙芯中科                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. 版本演进

### 时间线

| 版本 | 时间 | 说明 |
|------|------|------|
| **JDK 17** | 2021-09 | 龙芯开始移植工作 |
| **JDK 21** | 2023-09 | 正式合并到 OpenJDK |
| **JDK 22** | 2024-03 | 稳定性改进 |
| **JDK 23** | 2024-09 | 性能优化 |
| **JDK 24** | 2025-03 | LSX/LASX 向量支持 |
| **JDK 25** | 2025-09 | 持续优化 |
| **JDK 26** | 2026-03 | 紧凑对象头支持 |

---

## 3. 指令集

### 基础指令集

| 扩展 | 名称 | 说明 | 支持 |
|------|------|------|------|
| **LA32** | 32位 | 32位基础指令集 | ✅ |
| **LA64** | 64位 | 64位基础指令集 | ✅ |

### 向量扩展

| 扩展 | 名称 | 说明 | 支持 |
|------|------|------|------|
| **LSX** | 128位向量 | 128位 SIMD 指令 | ✅ JDK 24 |
| **LASX** | 256位向量 | 256位 SIMD 指令 | ✅ JDK 24 |

---

## 目录结构

```
src/hotspot/
├── cpu/loongarch/
│   ├── assembler_loongarch.cpp      # 汇编器
│   ├── assembler_loongarch.hpp
│   ├── compiledIC_loongarch.cpp     # 内联缓存
│   ├── interpreter_loongarch.cpp    # 解释器
│   ├── interpreterRT_loongarch.cpp
│   ├── methodHandles_loongarch.cpp  # 方法句柄
│   ├── nativeInst_loongarch.cpp     # 本地指令
│   ├── register_loongarch.hpp       # 寄存器定义
│   ├── stubGenerator_loongarch.cpp  # 存根生成
│   ├── templateTable_loongarch.cpp  # 模板表
│   └── vm_version_loongarch.cpp     # 版本检测
│
├── cpu/loongarch/gc/
│   ├── g1/
│   │   └── g1BarrierSetAssembler_loongarch.cpp
│   └── ...
│
└── os_cpu/linux_loongarch/
    ├── atomic_linux_loongarch.hpp
    ├── os_linux_loongarch.cpp
    └── ...
```

---

## 4. 寄存器

### 通用寄存器

```
┌─────────────────────────────────────────────────────────────┐
│                LoongArch 通用寄存器                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   $r0  ($zero)  - 硬连线为 0                                 │
│   $r1  ($ra)    - 返回地址                                   │
│   $r2  ($tp)    - 线程指针                                   │
│   $r3  ($sp)    - 栈指针                                     │
│   $r4-$r11      - 参数/返回值 ($a0-$a7)                       │
│   $r12-$r20     - 临时寄存器 ($t0-$t8)                        │
│   $r21          - 保留                                       │
│   $r22          - 帧指针 ($fp)                               │
│   $r23-$r31     - 保存寄存器 ($s0-$s8)                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 浮点寄存器

```
┌─────────────────────────────────────────────────────────────┐
│                LoongArch 浮点寄存器                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   $f0-$f7       - 参数/返回值 ($fa0-$fa7)                     │
│   $f8-$f23      - 临时寄存器 ($ft0-$ft15)                     │
│   $f24-$f31     - 保存寄存器 ($fs0-$fs7)                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. 汇编示例

### 基础指令

```cpp
// src/hotspot/cpu/loongarch/assembler_loongarch.hpp

// 加法
void add_w(Register Rd, Register Rj, Register Rk);
void add_d(Register Rd, Register Rj, Register Rk);  // 64位

// 乘法
void mul_w(Register Rd, Register Rj, Register Rk);
void mul_d(Register Rd, Register Rj, Register Rk);

// 分支
void jirl(Register Rd, Register Rj, int32_t offset);
void b(Label& L);
void bl(Label& L);

// 比较并分支
void beq(Register Rj, Register Rk, Label& L);
void bne(Register Rj, Register Rk, Label& L);
```

### LSX 向量指令

```cpp
// LSX 128位向量指令
void vadd_w(VectorRegister Vd, VectorRegister Vj, VectorRegister Vk);
void vmul_w(VectorRegister Vd, VectorRegister Vj, VectorRegister Vk);
void vld(VectorRegister Vd, Register Rj, int32_t offset);
void vst(VectorRegister Vd, Register Rj, int32_t offset);
```

### LASX 256位向量指令

```cpp
// LASX 256位向量指令
void xvadd_w(VectorRegister Vd, VectorRegister Vj, VectorRegister Vk);
void xvmul_w(VectorRegister Vd, VectorRegister Vj, VectorRegister Vk);
void xvld(VectorRegister Vd, Register Rj, int32_t offset);
void xvst(VectorRegister Vd, Register Rj, int32_t offset);
```

---

## 6. JVM 参数

### LoongArch 特定参数

```bash
# 查看 LoongArch 特定参数
java -XX:+PrintFlagsFinal -version | grep -i loong

# 启用 LSX (128位向量)
-XX:+UseLSX

# 启用 LASX (256位向量)
-XX:+UseLASX
```

### 性能调优

```bash
# 推荐参数
java -XX:+UseG1GC \
     -XX:+UseCompressedOops \
     -XX:+UseLargePages \
     -Xms2g -Xmx2g \
     MyApp
```

---

## 7. 贡献者

### 龙芯团队

| 贡献者 | 主要贡献 |
|--------|----------|
| sunguoyun | LoongArch Port Lead |
| Ao Qi | 编译器移植 |
| Jie Fu | 运行时移植 |
| Wang Xingang | GC 移植 |
| Chen Haoran | 测试 |

### 相关链接

| 资源 | 链接 |
|------|------|
| **龙芯官网** | https://www.loongson.cn/ |
| **GitHub** | https://github.com/loongson |
| **架构手册** | https://loongson.github.io/LoongArch-Documentation/ |
| **龙芯 JDK** | https://github.com/loongson/jdk |

---

## 8. 构建 LoongArch JDK

### 原生编译

```bash
# 在 LoongArch 机器上
bash configure
make images

# 输出
build/linux-loongarch64-server-release/images/jdk/
```

### 交叉编译

```bash
# 从 x86_64 交叉编译
bash configure \
    --openjdk-target=loongarch64-linux-gnu \
    --with-boot-jdk=$JAVA_HOME
make images
```

---

## 9. 龙芯 CPU 型号

| 型号 | 架构 | 主频 | 特点 |
|------|------|------|------|
| **龙芯 3A5000** | LA464 | 2.3-2.5GHz | 4核，桌面/服务器 |
| **龙芯 3A6000** | LA664 | 2.5GHz | 4核，高性能 |
| **龙芯 3C5000** | LA464 | 2.1GHz | 16核，服务器 |
| **龙芯 3C6000** | LA664 | 2.5GHz | 16核，高性能服务器 |

---

## 10. 性能特性

### LSX/LASX 向量优化

```bash
# 启用向量优化
java -XX:+UseSuperWord \
     -XX:+UseLSX \
     MyApp

# 256位向量
java -XX:+UseSuperWord \
     -XX:+UseLASX \
     MyApp
```

---

## 11. 已知问题

| 问题 | 状态 | 说明 |
|------|------|------|
| Zero VM | ✅ 支持 | 解释器模式 |
| Minimal VM | ✅ 支持 | 最小虚拟机 |
| Client VM (C1) | ✅ 支持 | 快速编译 |
| Server VM (C2) | ✅ 支持 | 深度优化 |
| ZGC | ✅ 支持 | 低延迟 GC |
| Shenandoah | ✅ 支持 | 低延迟 GC |

---

## 12. 相关主题

- [CPU 架构](./) - 其他架构支持
- [JIT 编译](../jit/) - 架构特定的编译优化
- [GC](../gc/) - GC Barrier 实现
