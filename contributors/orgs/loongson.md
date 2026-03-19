# 龙芯 (Loongson)

> LoongArch 架构支持和测试修复

---

## 概览

龙芯中科参与 OpenJDK 开发，专注于 LoongArch 架构支持、测试修复和编译器改进。

| 指标 | 值 |
|------|-----|
| **总 Commits** | 52 |
| **贡献者数** | 9 |
| **主要领域** | LoongArch、测试、编译器 |

---

## 影响的模块分布

基于 git 修改文件统计：

| 模块 | 文件数 | 说明 |
|------|--------|------|
| 文档 | 11 | 测试文档更新 |
| GC 测试 | 8 | GC 参数测试 |
| HTTP 客户端测试 | 7 | HttpClient 测试 |
| C2 编译器 | 5 | 服务端编译器 |
| Shenandoah GC | 5 | Shenandoah 测试 |
| C1 编译器 | 5 | 客户端编译器 |
| 编译器共享 | 4 | 编译器共享代码 |
| RISC-V 移植 | 3 | RISC-V 架构代码 |
| AArch64 移植 | 3 | AArch64 架构代码 |

---

## Top 贡献者

| 排名 | 贡献者 | Commits | 领域 |
|------|--------|---------|------|
| 1 | Guoyun Sun | 14 | 测试、文档 |
| 2 | Qi Ao | 11 | 测试、编译器 |
| 3 | Jie Fu | 8 | 测试 |
| 4 | Haomin Wang | 6 | 测试 |
| 5 | Yaqi Sun | 4 | 测试 |
| 6 | Jia Huang | 3 | 测试 |
| 7 | Xue Wang | 2 | 测试 |
| 8 | Xu Sun | 2 | 测试 |
| 9 | Tian Jing | 2 | 测试 |

---

## 关键贡献

### LoongArch 架构支持

| Issue | 标题 | 说明 |
|-------|------|------|
| 8270517 | 添加 LoongArch Zero 支持 | **重要** - LoongArch Zero VM 移植 |
| 8310105 | LoongArch64 构建修复 | JDK-8304913 后构建失败修复 |
| 8315020 | LoongArch64 Zero 构建宏定义修正 | 构建配置修复 |
| 8364177 | LoongArch64 libpng 构建修复 | 符号未定义修复 |

**LoongArch 支持**:
- Zero VM 移植完成
- 构建系统配置
- 持续的构建修复

### 编译器修复

| Issue | 标题 | 说明 |
|-------|------|------|
| 8298813 | C2 double 转 float 精度丢失 | **性能修复** - crypto.aes 分数波动 |
| 8286847 | 旋转向量不支持 byte 或 short | 向量化修复 |
| 8273317 | cmovP_cmpP_zero_zeroNode 崩溃 | **崩溃修复** |
| 8279956 | Scheduling::ComputeLocalLatenciesForward 无用方法 | 代码清理 |

### C1 编译器

| Issue | 标题 | 说明 |
|-------|------|------|
| 8302369 | 减少 C1 编译器栈大小 | 内存优化 |
| 8305236 | 解释器 LoadLoad 屏障优化 | 性能优化 |

### 测试修复

| Issue | 标题 | 说明 |
|-------|------|------|
| 8322881 | Files.CopyMoveVariations 权限问题 | 测试修复 |
| 8316563 | LinuxResourceTest 失败 | 测试修复 |
| 8311631 | LicenseTest 多用户权限问题 | 测试修复 |
| 8309778 | Files.CopyAndMove 测试目录问题 | 测试修复 |
| 8301942 | DigestEchoClientSSL 测试失败 | 测试修复 |
| 8301306 | HttpClient 测试失败 | 测试修复 |

### GC 相关

| Issue | 标题 | 说明 |
|-------|------|------|
| 8305944 | assert(is_aligned(ref, HeapWordSize)) | 正确性修复 |
| 8231242 | G1CollectedHeap::print_regions_on 输出改进 | 可读性改进 |

---

## 技术特点

### LoongArch 架构

龙芯专注于 LoongArch 架构支持：
- **Zero VM**: 解释器模式 JVM
- **构建系统**: 持续的构建修复
- **兼容性**: 确保在新架构上正常工作

### 测试稳定性

大量测试修复贡献：
- 多平台测试兼容
- 权限问题修复
- 测试文档更新

### 编译器改进

- C2 编译器正确性修复
- C1 编译器优化
- 向量化支持改进

---

## LoongArch 背景

LoongArch 是龙芯中科开发的指令集架构：

| 特性 | 说明 |
|------|------|
| 类型 | RISC 指令集 |
| 位宽 | 32/64 位 |
| 开发者 | 龙芯中科 |
| 许可 | 开源 |

**OpenJDK 支持状态**:
- Zero VM: 已支持
- JIT 移植: 进行中 (社区/龙芯团队)

---

## 数据来源

- **统计方法**: `git log upstream_master --author="loongson"`
- **模块分析**: 基于修改文件路径统计
- **贡献者**: 9 位龙芯员工

---

## 相关链接

- [龙芯官网](https://www.loongson.cn/)
- [Loongson JDK](https://github.com/loongson/jdk)
- [LoongArch 架构](https://loongarch.dev/)