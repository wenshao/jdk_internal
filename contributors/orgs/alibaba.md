# 阿里巴巴

> 核心库性能优化和 C2 编译器改进

---

## 概览

阿里巴巴通过 Dragonwell 团队参与 OpenJDK 开发，专注于核心库性能优化、字符串处理和 C2 编译器改进。

| 指标 | 值 |
|------|-----|
| **总 Commits** | 72 |
| **贡献者数** | 16 |
| **主要领域** | 核心库、C2 编译器、AArch64 |

---

## 影响的模块分布

基于 git 修改文件统计：

| 模块 | 文件数 | 说明 |
|------|--------|------|
| java.lang | 23 | 核心类库 |
| AArch64 移植 | 21 | ARM 架构优化 |
| java.util | 14 | 集合框架 |
| java.text | 14 | 文本格式化 |
| jdk.internal.util | 10 | 内部工具类 |
| java.time | 9 | 日期时间 |
| ADLC | 9 | 架构描述语言编译器 |
| C2 编译器 | 8 | 服务端编译器 |
| G1 GC | 8 | G1 垃圾收集器 |
| JFR | 5 | Java Flight Recorder |

---

## Top 贡献者

| 排名 | 贡献者 | Commits | 领域 |
|------|--------|---------|------|
| 1 | [Shaojin Wen](../shaojin-wen.md) | 28 | 核心库优化 |
| 2 | [Kuai Wei](../kuai-wei.md) | 13 | C2 编译器 |
| 3 | Yude Lin | 8 | 测试 |
| 4 | Zhuoren Wang | 3 | 测试 |
| 5 | Xiaowei Lu | 3 | 测试 |

---

## 关键贡献

### 核心库优化

| Issue | 标题 | 性能影响 |
|-------|------|----------|
| 8336856 | 高效的隐藏类字符串拼接策略 | 启动优化 |
| 8338936 | StringConcatFactory MethodType 优化 | 启动优化 |
| 8338532 | ClassFile API MethodTypeDesc 优化 | 启动优化 |
| 8337832 | DateTime toString 优化 | +10% |
| 8336831 | StringConcatHelper.simpleConcat 优化 | +5% |

### 字符串处理

| Issue | 标题 | 说明 |
|-------|------|------|
| 8336706 | LocalDate.toString 使用 StringBuilder.repeat | 减少分配 |
| 8336741 | LocalTime.toString 使用 StringBuilder.repeat | 减少分配 |
| 8337168 | LocalDateTime.toString 优化 | 性能提升 |
| 8333833 | UUID::toString 移除 ByteArrayLittleEndian | 简化代码 |

### 文本格式化

| Issue | 标题 | 说明 |
|-------|------|------|
| 8333396 | Format 使用 StringBuilder 内部实现 | 减少分配 |
| 8335645 | Formatter trailingZeros 使用 String repeat | 性能提升 |
| 8335802 | HexFormat 使用 boolean 替代 enum | 启动优化 |

### C2 编译器

| Issue | 标题 | 说明 |
|-------|------|------|
| 8356328 | C2 IR 节点 size_of() 函数 | 正确性修复 |
| 8347405 | MergeStores 反向字节顺序 | 正确性修复 |
| 8339299 | C1 内联 final 方法丢失类型 profile | 性能修复 |

### AArch64 优化

| Issue | 标题 | 说明 |
|-------|------|------|
| 8325821 | AArch64 release barrier 优化 | 性能提升 |
| 8333410 | AArch64 清理未使用的类 | 代码清理 |

---

## 技术特点

### 性能优化导向

阿里巴巴的贡献以性能优化为主：
- 字符串拼接优化
- 日期时间格式化优化
- 启动时间优化

### 实际场景驱动

优化基于实际生产场景：
- Dragonwell 在阿里巴巴大规模部署
- 针对电商、支付等场景优化

---

## Alibaba Dragonwell

阿里巴巴维护自己的 JDK 发行版 Dragonwell：

| 特性 | 说明 |
|------|------|
| 基于 | OpenJDK |
| 支持 | 长期支持 (LTS) |
| 许可 | GPLv2 |
| 平台 | Linux, Windows, macOS |

**特点**:
- 生产环境验证
- 性能优化
- 安全补丁
- 阿里云集成

---

## 数据来源

- **统计方法**: `git log upstream_master --author="alibaba"`
- **模块分析**: 基于修改文件路径统计
- **贡献者**: 16 位阿里巴巴员工

---

## 相关链接

- [Alibaba Dragonwell](https://github.com/alibaba/dragonwell8)
- [Dragonwell 文档](https://dragonwell-jdk.io/)
- [阿里云 Java](https://www.aliyun.com/product/dragonwell)