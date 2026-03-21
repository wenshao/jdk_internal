# RISC-V 架构支持

> 开源指令集架构的 OpenJDK 移植

[← 返回 CPU 架构](./)

---

## 1. 概述

RISC-V 是一个开源的指令集架构 (ISA)，OpenJDK 从 JDK 19 开始正式支持 RISC-V 64位平台。

```
┌─────────────────────────────────────────────────────────────┐
│                    RISC-V 生态                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   OpenJDK RISC-V Port                                       │
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
│   │  │           riscv.ad (汇编模板)                │    │  │
│   │  └─────────────────────────────────────────────┘    │  │
│   │                    │                                  │  │
│   │                    ▼                                  │  │
│   │  ┌─────────────────────────────────────────────┐    │  │
│   │  │        RISC-V 指令集扩展                      │    │  │
│   │  │  I M A F D C V Zvbb Zfa Zvkn                 │    │  │
│   │  └─────────────────────────────────────────────┘    │  │
│   └─────────────────────────────────────────────────────┘  │
│                                                             │
│   主要贡献者: ISCAS, 阿里巴巴, 字节跳动                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. 版本演进

### 时间线

| 版本 | 时间 | JEP | 说明 |
|------|------|-----|------|
| **JDK 19** | 2022-09 | JEP 422 | RISC-V Linux 移植 |
| **JDK 20** | 2023-03 | - | 向量 intrinsic 初步支持 |
| **JDK 21** | 2023-09 | - | Zvbb/Zfa 扩展支持 |
| **JDK 22** | 2024-03 | - | 性能优化 |
| **JDK 23** | 2024-09 | - | 更多向量指令 |
| **JDK 24** | 2025-03 | - | 向量支持完善 |
| **JDK 25** | 2025-09 | - | 继续优化 |
| **JDK 26** | 2026-03 | - | 紧凑对象头支持 |

---

## 3. 指令集扩展

### 基础扩展

| 扩展 | 名称 | 说明 | 支持 |
|------|------|------|------|
| **I** | 整数 | 基础整数指令 | ✅ JDK 19 |
| **M** | 乘除法 | 乘法和除法指令 | ✅ JDK 19 |
| **A** | 原子 | 原子内存操作 | ✅ JDK 19 |
| **F** | 单精度浮点 | 单精度浮点运算 | ✅ JDK 19 |
| **D** | 双精度浮点 | 双精度浮点运算 | ✅ JDK 19 |
| **C** | 压缩 | 压缩指令 | ✅ JDK 19 |
| **V** | 向量 | 向量扩展 | ✅ JDK 20 |

### 高级扩展

| 扩展 | 名称 | 说明 | 支持 |
|------|------|------|------|
| **Zvbb** | 向量位操作 | 向量位操作指令 | ✅ JDK 21 |
| **Zfa** | 浮点附加 | 附加浮点指令 | ✅ JDK 21 |
| **Zvkn** | 向量加密 | 向量加密指令 | ✅ JDK 24 |

---

## 目录结构

```
src/hotspot/
├── cpu/riscv/
│   ├── assembler_riscv.cpp      # 汇编器
│   ├── assembler_riscv.hpp
│   ├── compiledIC_riscv.cpp     # 内联缓存
│   ├── interpreter_riscv.cpp    # 解释器
│   ├── interpreterRT_riscv.cpp
│   ├── methodHandles_riscv.cpp  # 方法句柄
│   ├── nativeInst_riscv.cpp     # 本地指令
│   ├── register_riscv.hpp       # 寄存器定义
│   ├── stubGenerator_riscv.cpp  # 存根生成
│   ├── templateTable_riscv.cpp  # 模板表
│   └── vm_version_riscv.cpp     # 版本检测
│
├── cpu/riscv/gc/
│   ├── g1/
│   │   └── g1BarrierSetAssembler_riscv.cpp
│   └── z/
│       └── zBarrierSetAssembler_riscv.cpp
│
└── os_cpu/linux_riscv/
    ├── atomic_linux_riscv.hpp   # 原子操作
    ├── bytes_linux_riscv.hpp
    ├── os_linux_riscv.cpp       # OS 接口
    ├── prefetch_linux_riscv.hpp
    └── thread_linux_riscv.cpp
```

---

## 4. 代码示例

### 扩展检测

```cpp
// vm_version_riscv.cpp
bool VM_Version::supports_vector() {
    return _features & CPU_FEATURE_V;
}

bool VM_Version::supports_zvbb() {
    return _features & CPU_FEATURE_ZVBB;
}

bool VM_Version::supports_zfa() {
    return _features & CPU_FEATURE_ZFA;
}
```

### 向量指令示例

```cpp
// riscv.ad - 向量加法
instruct vAdd(vReg dst, vReg src1, vReg src2) %{
    match(Set dst (AddVB src1 src2));
    ins_cost(INSN_COST);
    format %{ "vadd.vv $dst, $src1, $src2" %}
    ins_encode %{
        __ vadd_vv(as_FloatRegister($dst$$reg),
                   as_FloatRegister($src1$$reg),
                   as_FloatRegister($src2$$reg));
    %}
%}
```

### Zvbb 指令示例

```cpp
// 向量 AND-NOT 指令
instruct vAndNot(vReg dst, vReg src1, vReg src2) %{
    predicate(UseZvbb);
    match(Set dst (AndNotV src1 src2));
    format %{ "vandn.vv $dst, $src1, $src2" %}
    ins_encode %{
        __ vandn_vv(as_FloatRegister($dst$$reg),
                    as_FloatRegister($src1$$reg),
                    as_FloatRegister($src2$$reg));
    %}
%}
```

---

## 5. JVM 参数

### RISC-V 特定参数

```bash
# 查看支持的扩展
java -XX:+PrintFlagsFinal -version | grep -i riscv

# 禁用向量扩展 (调试用)
-XX:-UseRISCVVector

# 启用 Zvbb (默认自动检测)
-XX:+UseZvbb

# 启用 Zfa (默认自动检测)
-XX:+UseZfa
```

### 性能调优

```bash
# 大页内存
-XX:+UseLargePages

# 压缩指针 (默认启用)
-XX:+UseCompressedOops

# 向量化
-XX:+UseSuperWord
```

---

## 6. 贡献者

### 核心贡献者

| 贡献者 | 组织 | PRs | 主要贡献 |
|--------|------|-----|----------|
| [Fei Yang](/by-contributor/profiles/fei-yang.md) | Huawei | 100+ | RISC-V Port Lead |
| [Hamlin Li](/by-contributor/profiles/hamlin-li.md) | Rivos | 65+ | RISC-V 向量 |
| [Anjian Wen](/by-contributor/profiles/anjian-wen.md) | 字节跳动 | 25+ | Zvbb/Zfa 指令 |
| Dingli Zhang | ISCAS | 50+ | RISC-V 测试 |

### 组织贡献

| 组织 | 贡献者 | 主要领域 |
|------|--------|----------|
| **Huawei** | Fei Yang | Port 维护 |
| **ISCAS/PLCT** | Dingli Zhang | 测试 |
| **Oracle** | Hamlin Li | 向量扩展 |
| **字节跳动** | Anjian Wen | Zvbb/Zfa |
| **阿里巴巴** | - | RISC-V 优化 |

---

## 7. 构建 RISC-V JDK

### 前置条件

```bash
# Ubuntu/Debian
sudo apt-get install gcc-riscv64-linux-gnu g++-riscv64-linux-gnu

# 或使用 QEMU 模拟
sudo apt-get install qemu-user-static
```

### 编译步骤

```bash
# 获取源码
git clone https://github.com/openjdk/jdk.git
cd jdk

# 配置 (交叉编译)
bash configure \
    --openjdk-target=riscv64-linux-gnu \
    --with-boot-jdk=$JAVA_HOME

# 编译
make images

# 输出位置
# build/linux-riscv64-server-release/images/jdk/
```

### 运行

```bash
# 在 RISC-V 硬件上
./build/linux-riscv64-server-release/images/jdk/bin/java -version

# 使用 QEMU 模拟
qemu-riscv64-static -L /usr/riscv64-linux-gnu \
    ./build/linux-riscv64-server-release/images/jdk/bin/java -version
```

---

## 8. 硬件支持

### 开发板

| 开发板 | CPU | 核心 | 状态 |
|--------|-----|------|------|
| **SiFive HiFive Unmatched** | SiFive U74 | 4核 | ✅ 支持 |
| **SiFive HiFive Premier P550** | SiFive P550 | 8核 | ✅ 支持 |
| **BeagleV** | JH7100 | 2核 | ✅ 支持 |
| **VisionFive 2** | JH7110 | 4核 | ✅ 支持 |
| **Milk-V Duo** | C906 | 1核 | ✅ 支持 |
| **Milk-V Pioneer** | SG2042 | 64核 | ✅ 支持 |
| **Banana Pi BPI-F3** | SpacemiT K1 | 8核 | ✅ 支持 |
| **LicheePi 4A** | TH1520 | 4核 | ✅ 支持 |

### 云服务

| 云服务商 | 实例 | 状态 |
|----------|------|------|
| **阿里云** | RISC-V ECS | ✅ 可用 |
| **华为云** | RISC-V 实例 | ✅ 可用 |

### RISC-V CPU 架构

| CPU | 厂商 | 架构 | 向量支持 |
|-----|------|------|----------|
| **SiFive P550** | SiFive | RV64GC | V |
| **SiFive U74** | SiFive | RV64GC | - |
| **SG2042** | 算能 | RV64GC | V |
| **C920** | 平头哥 | RV64GCV | V |
| **TH1520** | 平头哥 | RV64GCV | V |
| **XuanTie C910** | 平头哥 | RV64GC | V |
| **SpacemiT K1** | SpacemiT | RV64GC | V |
| **T-Head C906** | 平头哥 | RV64GC | V |

---

## 9. 相关 JEP

| JEP | 版本 | 标题 |
|-----|------|------|
| JEP 422 | JDK 19 | Linux/RISC-V Port |
| JEP 439 | JDK 20 | Generational ZGC (所有平台) |
| JEP 413 | JDK 19 | Vector API (Incubator) - 包含 RISC-V 向量 |

---

## 10. 相关链接

- [RISC-V International](https://riscv.org/)
- [OpenJDK RISC-V Port 项目](https://openjdk.org/projects/riscv-port/)
- [ISCAS PLCT 实验室](https://github.com/plctlab)
- [RISC-V 指令集手册](https://riscv.org/technical/specifications/)

---

## 11. 相关主题

- [CPU 架构](./) - 其他架构支持
- [JIT 编译](../jit/) - 架构特定的编译优化
- [向量 API](/jeps/performance/jep-509.md) - 向量计算
