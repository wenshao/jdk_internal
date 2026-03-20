# Vector API 平台支持

> 详细分析各 CPU 架构的 SIMD 指令支持

[← 返回 Vector API](./)

---

## 平台架构支持

### x86-64 (Intel/AMD)

**指令集演进**:

| 指令集 | 位宽 | 引入年份 | JDK 支持 |
|--------|------|----------|----------|
| SSE | 128 | 1999 | ✅ 完整 |
| SSE2 | 128 | 2001 | ✅ 完整 |
| SSE3 | 128 | 2004 | ✅ 完整 |
| SSE4.1 | 128 | 2006 | ✅ 完整 |
| AVX | 256 | 2011 | ✅ 完整 |
| AVX2 | 256 | 2013 | ✅ 完整 |
| AVX-512F | 512 | 2016 | ✅ 完整 |
| AVX-512BW | 512 | 2016 | ✅ 完整 |
| AVX-512VL | 128/256/512 | 2016 | ✅ 完整 |
| AVX-512DQ | 512 | 2016 | ✅ 完整 |
| AVX-512IFMA | 512 | 2017 | 🔄 部分 |
| AVX-512VBMI | 512 | 2017 | 🔄 部分 |
| AVX-512VNNI | 512 | 2018 | ✅ AI 优化 |

**HotSpot 源码位置**:
```
src/hotspot/cpu/x86/
├── assembler_x86.cpp       # 汇编指令生成
├── c2_MacroAssembler_x86.cpp  # C2 编译器宏汇编
├── vm_version_x86.cpp      # CPU 特性检测
└── x86.ad                 # 指令匹配规则
```

**关键检测代码** (`vm_version_x86.cpp`):
```cpp
// 特性检测
if (UseAVX > 2) {
  if (supports_avx512()) {
    // AVX-512 支持
  }
}

// 向量宽度选择
int MaxVectorSize = VM_Version::get_max_vector_size();
```

**JVM 参数**:
```bash
-XX:UseAVX=3          # 启用 AVX-512
-XX:MaxVectorSize=512 # 最大向量宽度
-XX:+UseVectorStubs   # 使用向量存根
```

---

### AArch64 (ARM 64-bit)

**指令集演进**:

| 指令集 | 位宽 | 引入年份 | JDK 支持 |
|--------|------|----------|----------|
| NEON | 128 | 2011 | ✅ 完整 |
| SVE | 可变 | 2016 | ✅ JDK 21+ |
| SVE2 | 可变 | 2020 | 🔄 JDK 24+ |

**SVE 特点**:
- **可变向量长度** (VL): 128-2048 bits
- 软件无需重编译即可利用更宽向量
- Predicate 寄存器控制活跃通道

**HotSpot 源码位置**:
```
src/hotspot/cpu/aarch64/
├── assembler_aarch64.cpp       # NEON/SVE 汇编
├── c2_MacroAssembler_aarch64.cpp
├── vm_version_aarch64.cpp      # SVE 检测
└── aarch64.ad                  # 指令匹配
```

**SVE 检测代码** (`vm_version_aarch64.cpp`):
```cpp
// SVE 特性检测
bool has_sve = VM_Version::supports_sve();
int sve_vl = VM_Version::get_sve_vector_length();  // 字节

// SVE2 检测
bool has_sve2 = VM_Version::supports_sve2();
```

**NEON vs SVE 对比**:

| 特性 | NEON | SVE |
|------|------|-----|
| 向量宽度 | 固定 128-bit | 可变 128-2048-bit |
| Mask 支持 | 无原生 | Predicate 寄存器 |
| Gather/Scatter | 无 | ✅ |
| Permute | 有限 | ✅ 强大 |

---

### RISC-V (V 扩展)

**指令集**:

| 指令集 | 位宽 | JDK 支持 |
|--------|------|----------|
| V 扩展 | 可变 | ✅ JDK 21+ |

**V 扩展特点**:
- 可变向量长度 (VLEN): 32-65536 bits
- 32 个向量寄存器
- 7 种向量元素类型

**HotSpot 源码位置**:
```
src/hotspot/cpu/riscv/
├── assembler_riscv.cpp
├── c2_MacroAssembler_riscv.cpp
├── vm_version_riscv.cpp
└── riscv.ad
```

**V 扩展检测**:
```cpp
// RISC-V V 扩展检测
bool has_v_extension = VM_Version::supports_vector();
int vlen = VM_Version::get_vlen();  // bits
```

---

### 其他平台

| 平台 | SIMD 支持 | JDK 状态 |
|------|-----------|----------|
| **PPC64** | VSX/AltiVec | ✅ 支持 |
| **s390x** | Vector Facility | ✅ 支持 |
| **LoongArch** | LSX/LASX | ✅ JDK 21+ |

---

## CPU 特性检测

### API 层面 (JDK 21+)

```java
import jdk.incubator.vector.CPUFeatures;

// 获取 CPU 特性
Set<String> features = CPUFeatures.getCPUFeatures();

// x86-64 示例输出
// "avx", "avx2", "avx512f", "avx512dq", "avx512vl", "sse", "sse2", "sse3"

// AArch64 示例输出
// "neon", "sve", "sve2", "asimd"
```

### HotSpot 内部检测

**x86-64** (`vm_version_x86.cpp`):
```cpp
// 特性标志
uint32_t _features;
uint32_t _features_ext;

#define CPU_SSE           (1 << 0)
#define CPU_SSE2          (1 << 1)
#define CPU_SSE3          (1 << 2)
#define CPU_SSSE3         (1 << 3)
#define CPU_SSE4A         (1 << 4)
#define CPU_SSE4_1        (1 << 5)
#define CPU_AVX           (1 << 6)
#define CPU_AVX2          (1 << 7)
#define CPU_AVX512F       (1 << 8)
#define CPU_AVX512DQ      (1 << 9)
#define CPU_AVX512BW      (1 << 10)
#define CPU_AVX512VL      (1 << 11)
```

**AArch64** (`vm_version_aarch64.cpp`):
```cpp
// 特性标志
#define CPU_ASIMD          (1 << 0)   // NEON
#define CPU_SVE            (1 << 1)   // SVE
#define CPU_SVE2           (1 << 2)   // SVE2
#define CPU_SVE_AES        (1 << 3)   // SVE AES
#define CPU_SVE_BITPERM    (1 << 4)   // SVE Bitperm
```

---

## 向量宽度选择逻辑

### 优先级算法

```java
// VectorShape.java
public static VectorShape preferredShape() {
    // 1. 首先检查缓存
    VectorShape shape = PREFERRED_SHAPE;
    if (shape != null) return shape;
    
    // 2. 计算所有元素类型的最小支持宽度
    int prefBitSize = Integer.MAX_VALUE;
    for (LaneType type : LaneType.values()) {
        prefBitSize = Math.min(prefBitSize, getMaxVectorBitSize(type.carrierType));
    }
    
    // 3. 选择对应位宽的 Shape
    VectorShape shape = VectorShape.forBitSize(prefBitSize);
    return shape;
}
```

### 各平台默认宽度

| 平台 | 默认宽度 | 条件 |
|------|----------|------|
| x86-64 (AVX-512) | 512-bit | UseAVX >= 3 |
| x86-64 (AVX2) | 256-bit | UseAVX >= 2 |
| x86-64 (SSE) | 128-bit | 默认 |
| AArch64 (SVE) | 硬件 VL | SVE 可用 |
| AArch64 (NEON) | 128-bit | 默认 |
| RISC-V (V) | 硬件 VLEN | V 扩展可用 |

---

## 汇编指令映射

### x86-64 示例

**Java 代码**:
```java
FloatVector va = FloatVector.fromArray(species, a, 0);
FloatVector vb = FloatVector.fromArray(species, b, 0);
FloatVector vc = va.add(vb);
vc.intoArray(c, 0);
```

**生成的 AVX-512 汇编**:
```asm
; 加载向量
vmovups   zmm0, [rdi + rax*4]     ; va = a[0..15]
vmovups   zmm1, [rdi + rdx*4]     ; vb = b[0..15]

; 向量加法
vaddps    zmm0, zmm0, zmm1        ; vc = va + vb

; 存储结果
vmovups   [rdi + rcx*4], zmm0    ; c[0..15] = vc
```

### AArch64 SVE 示例

**Java 代码**:
```java
FloatVector va = FloatVector.fromArray(species, a, 0);
FloatVector vc = va.mul(2.0f);  // 标量乘向量
```

**生成的 SVE 汇编**:
```asm
; 加载向量
ld1w     z0.d, p0/zr, [x0, x1, lsl #1]  ; 加载 a[] (可变长度)

; 广播标量
fmov    s0, #2.0

; 向量乘法
fmul    z0.s, z0.s, s0.s          ; va * 2.0

; 存储结果
st1w    z0.d, p0/zr, [x0, x1]    ; 存储 c[]
```

---

## 性能特性对比

### 各平台操作支持矩阵

| 操作 | x86-64 (AVX-512) | AArch64 (SVE) | RISC-V (V) |
|------|------------------|--------------|-------------|
| 基础算术 | ✅ | ✅ | ✅ |
| 比较 | ✅ | ✅ | ✅ |
| 逻辑运算 | ✅ | ✅ | ✅ |
| 位移 | ✅ | ✅ | ✅ |
| Gather | ✅ | ✅ | 🔄 |
| Scatter | ✅ | ✅ | 🔄 |
| Mask 操作 | ✅ | ✅ (Predicate) | ✅ |
| 转换 | ✅ | ✅ | ✅ |
| 数学函数 | ✅ | 🔄 | 🔄 |
| 点积 | ✅ (VNNI) | ✅ | ❌ |

### 性能基准

**测试**: SAXPY (单精度浮点乘加)

| 平台 | 向量宽度 | 加速比 |
|------|----------|--------|
| x86-64 (SSE) | 128-bit | 4x |
| x86-64 (AVX2) | 256-bit | 8x |
| x86-64 (AVX-512) | 512-bit | 16x |
| AArch64 (NEON) | 128-bit | 4x |
| AArch64 (SVE-256) | 256-bit | 8x |
| AArch64 (SVE-512) | 512-bit | 16x |

*加速比 = 向量宽度 / 标量宽度*

---

## JVM 调优参数

### x86-64 专用参数

```bash
# AVX 控制
-XX:UseAVX=0           # 禁用 AVX
-XX:UseAVX=1           # 启用 AVX (SSE 混合)
-XX:UseAVX=2           # 启用 AVX2
-XX:UseAVX=3           # 启用 AVX-512

# 向量大小控制
-XX:MaxVectorSize=128  # 限制 128-bit
-XX:MaxVectorSize=256  # 限制 256-bit
-XX:MaxVectorSize=512  # 限制 512-bit

# 向量化控制
-XX:+UseVectorStubs   # 使用向量存根 (调试)
-XX:-UseVectorStubs   # 禁用向量存根
```

### AArch64 专用参数

```bash
# SVE 控制
-XX:UseSVE=0            # 禁用 SVE，使用 NEON
-XX:UseSVE=1            # 启用 SVE
-XX:UseSVE=2            # 启用 SVE2

# SVE 向量长度
-XX:InitialSVEVectorLength=256  # 初始 VL (bits)
```

### 通用参数

```bash
# 自动向量化
-XX:+CompileThresholdScaling  # 启用编译阈值缩放

# 打印向量化信息
-XX:+PrintCompilation   # 打印编译信息
-XX:+PrintAssembly      # 打印汇编 (需要 hsdis)
```

---

## 调试技巧

### 检测当前平台支持

```java
import jdk.incubator.vector.*;

public class VectorInfo {
    public static void main(String[] args) {
        VectorSpecies<Float> species = FloatVector.SPECIES_PREFERRED;
        
        System.out.println("Preferred species: " + species);
        System.out.println("Vector length: " + species.length());
        System.out.println("Vector bit size: " + species.vectorBitSize());
        System.out.println("Element size: " + species.elementSize());
        
        // 尝试不同宽度
        for (int bits : new int[]{64, 128, 256, 512}) {
            try {
                VectorSpecies<Float> s = FloatVector.species(VectorShape.forBitSize(bits));
                System.out.println(bits + "-bit species available: " + s);
            } catch (Exception e) {
                System.out.println(bits + "-bit species NOT available");
            }
        }
    }
}
```

### 打印生成的汇编

```bash
# 需要 hsdis.so
java -XX:+UnlockDiagnosticVMOptions \
     -XX:+PrintAssembly \
     -XX:+PrintCompilation \
     --add-modules jdk.incubator.vector \
     VectorBench
```

### 使用 JFR 监控

```bash
# 启用 JFR 向量事件
jcmd <pid> JFR.start \
    settings=+jdk.VectorAPI#enabled=true \
    filename=vector.jfr
```

---

## 源码参考

### 关键源文件

| 文件 | 作用 |
|------|------|
| `src/jdk.incubator.vector/share/classes/jdk/incubator/vector/VectorSpecies.java` | Species 定义 |
| `src/jdk.incubator.vector/share/classes/jdk/incubator/vector/VectorShape.java` | Shape 定义 |
| `src/jdk.incubator.vector/share/classes/jdk/incubator/vector/CPUFeatures.java` | CPU 特性检测 |
| `src/hotspot/share/prims/vectorSupport.hpp` | HotSpot Vector 支持 |
| `src/hotspot/share/prims/vectorSupport.cpp` | 实现 |
| `src/hotspot/share/classfile/vmIntrinsics.hpp` | Intrinsic 定义 |

### 平台特定文件

| 平台 | 文件 |
|------|------|
| x86-64 | `src/hotspot/cpu/x86/vm_version_x86.cpp` |
| AArch64 | `src/hotspot/cpu/aarch64/vm_version_aarch64.cpp` |
| RISC-V | `src/hotspot/cpu/riscv/vm_version_riscv.cpp` |

---

> **最后更新**: 2026-03-20 | **数据来源**: JDK 源码 `/root/git/jdk`
