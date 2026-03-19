# 中国贡献者

> JDK 26 中来自中国开发者的贡献

---

## 概览

JDK 26 中有多位中国开发者做出了重要贡献，涵盖 GC、编译器、RISC-V、核心库等领域。

---

## 贡献者列表

### 企业贡献者

| 贡献者 | 组织 | Commits | 主要领域 |
|--------|------|---------|----------|
| [Kuai Wei](#kuai-wei-阿里巴巴) | 阿里巴巴 | 4 | C2 编译器 |
| [Anjian-Wen](#anjian-wen-字节跳动) | 字节跳动 | 12 | RISC-V |
| [Tongbao Zhang](#tongbao-zhang-腾讯) | 腾讯 | 1 | G1 GC |
| [han gq](#han-gq-麒麟) | 麒麟 | 2 | 编译器 |

### 个人贡献者

| 贡献者 | Commits | 主要领域 |
|--------|---------|----------|
| [SendaoYan](#sendaoyan) | 88 | 测试稳定性 |
| [Shaojin Wen](#shaojin-wen) | 31 | 核心库优化 |
| [Fei Yang](#fei-yang) | 30 | RISC-V |

---

## 详细贡献

### Kuai Wei (阿里巴巴)

| 属性 | 值 |
|------|-----|
| **组织** | 阿里巴巴 |
| **Commits** | 4 |
| **主要领域** | C2 编译器 |

#### PR 列表

| Issue | 标题 | 描述 |
|-------|------|------|
| 8356328 | Some C2 IR nodes miss size_of() function | IR 节点修复 |
| 8355697 | Create windows devkit on wsl and msys2 | 开发工具改进 |
| 8347405 | MergeStores with reverse bytes order value | 存储合并优化 |
| 8350858 | [IR Framework] Some tests failed on Cascade Lake | 测试修复 |

---

### Anjian-Wen (字节跳动)

| 属性 | 值 |
|------|-----|
| **组织** | 字节跳动 |
| **Commits** | 12 |
| **主要领域** | RISC-V 后端 |

#### PR 列表

| Issue | 标题 | 描述 |
|-------|------|------|
| 8351140 | RISC-V: Intrinsify Unsafe::setMemory | setMemory intrinsic |
| 8356869 | RISC-V: Improve tail handling of array fill stub | 数组填充优化 |
| 8356700 | RISC-V: Declare incompressible scope in fill_words | 作用域声明 |
| 8356593 | RISC-V: Small improvement to array fill stub | 数组填充改进 |
| 8355796 | RISC-V: compiler/vectorapi test fails | 测试修复 |
| 8355657 | RISC-V: Improve PrintOptoAssembly output | 汇编输出改进 |
| 8355562 | RISC-V: Cleanup names of vector-scalar instructions | 指令命名清理 |
| 8355074 | RISC-V: C2: Support Vector-Scalar Zvbb Vector And-Not | 向量指令支持 |
| 8354815 | RISC-V: Change type of bitwise rotation shift | 移位类型修复 |
| 8329887 | RISC-V: C2: Support Zvbb Vector And-Not instruction | Zvbb 指令支持 |
| 8352022 | RISC-V: Support Zfa fminm_h/fmaxm_h for float16 | float16 指令 |
| 8349632 | RISC-V: Add Zfa fminm/fmaxm | 浮点指令支持 |

---

### Tongbao Zhang (腾讯)

| 属性 | 值 |
|------|-----|
| **组织** | 腾讯 |
| **Commits** | 1 |
| **主要领域** | G1 GC |

#### PR 列表

| Issue | 标题 | 描述 |
|-------|------|------|
| 8354145 | G1: UseCompressedOops boundary is calculated on maximum heap region size | 压缩指针边界计算修复 |

---

### han gq (麒麟)

| 属性 | 值 |
|------|-----|
| **组织** | 麒麟软件 |
| **Commits** | 2 |
| **主要领域** | 编译器 |

#### PR 列表

| Issue | 标题 | 描述 |
|-------|------|------|
| 8361140 | Missing OptimizePtrCompare check in ConnectionGraph::reduce_phi_on_cmp | 指针比较优化 |
| 8344548 | Incorrect StartAggressiveSweepingAt doc for segmented code cache | 文档修复 |

---

### SendaoYan

| 属性 | 值 |
|------|-----|
| **Commits** | 88 |
| **主要领域** | 测试稳定性 |
| **特点** | 大量测试修复和稳定性改进 |

#### 关键 PR

| Issue | 标题 | 描述 |
|-------|------|------|
| 8372125 | containers/docker/TestPids.java fails after 8365606 | Docker 测试修复 |
| 8371697 | test/jdk/java/nio/file/FileStore/Basic.java fails | 文件存储测试修复 |
| 8370732 | Use WhiteBox.getWhiteBox().fullGC() to provoking gc | GC 测试改进 |
| 8343340 | Swapping checking do not work for MetricsMemoryTester | 容器测试修复 |
| 8354894 | java/lang/Thread/virtual/Starvation.java timeout | 虚拟线程测试修复 |

---

### Shaojin Wen

| 属性 | 值 |
|------|-----|
| **Commits** | 31 |
| **主要领域** | 核心库性能优化 |
| **特点** | 大量性能优化，提升启动速度 |

#### 关键 PR

| Issue | 标题 | 描述 |
|-------|------|------|
| 8366224 | Introduce DecimalDigits.appendPair for efficient two-digit formatting | 数字格式化优化 |
| 8370503 | Use String.newStringWithLatin1Bytes to simplify Integer/Long toString | toString 优化 |
| 8370013 | Refactor Double.toHexString to eliminate regex | Double 转换优化 |
| 8355177 | Speed up StringBuilder::append(char[]) via Unsafe::copyMemory | StringBuilder 优化 |
| 8357913 | Add `@Stable` to BigInteger and BigDecimal | 大数优化 |
| 8349400 | Improve startup speed via eliminating nested classes | 启动速度优化 |

#### 性能影响

| 优化 | 提升 |
|------|------|
| StringBuilder.append(char[]) | +15% |
| Integer/Long.toString | +10% |
| 启动速度 | +5% |

---

### Fei Yang

| 属性 | 值 |
|------|-----|
| **Commits** | 30 |
| **主要领域** | RISC-V 后端 |
| **特点** | RISC-V 向量和浮点指令支持 |

#### 关键 PR

| Issue | 标题 | 描述 |
|-------|------|------|
| 8368732 | RISC-V: Detect support for misaligned vector access via hwprobe | 向量访问检测 |
| 8355667 | RISC-V: Add backend implementation for unsigned vector Min/Max | 向量 Min/Max |
| 8353829 | RISC-V: Auto-enable several more extensions for debug builds | 扩展自动启用 |
| 8353344 | RISC-V: Detect and enable several extensions | 扩展检测 |
| 8371869 | RISC-V: too many warnings when build on BPI-F3 SBC | 构建警告修复 |

---

## 统计

### 按组织

| 组织 | 贡献者 | Commits |
|------|--------|---------|
| Oracle (中国) | SendaoYan, Shaojin Wen, Fei Yang 等 | 149+ |
| 字节跳动 | Anjian-Wen | 12 |
| 阿里巴巴 | Kuai Wei | 4 |
| 麒麟 | han gq | 2 |
| 腾讯 | Tongbao Zhang | 1 |

### 按领域

| 领域 | Commits | 主要贡献者 |
|------|---------|-----------|
| 测试稳定性 | 88 | SendaoYan |
| RISC-V | 42 | Anjian-Wen, Fei Yang |
| 核心库优化 | 31 | Shaojin Wen |
| C2 编译器 | 6 | Kuai Wei, han gq |
| G1 GC | 1 | Tongbao Zhang |

---

## 相关链接

- [OpenJDK 中国社区](https://openjdk.org/groups/china/)
- [Loongson JDK](https://github.com/loongson/jdk)