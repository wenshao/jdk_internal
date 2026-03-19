# 阿里巴巴

> 核心库性能优化和 C2 编译器改进

---

## 概览

阿里巴巴通过 Dragonwell 团队参与 OpenJDK 开发，专注于核心库性能优化、字符串处理和 C2 编译器改进。

| 指标 | 值 |
|------|-----|
| **Integrated PRs** | 110 |
| **贡献者数** | 2+ |
| **活跃时间** | 2018 - 至今 |
| **主要领域** | 核心库、C2 编译器、AArch64 |

> **统计说明**: 使用 GitHub Integrated PRs 作为贡献指标。OpenJDK Committer 使用 `@openjdk.org` 邮箱提交代码，因此 git commits 按邮箱统计不准确。

---

## 贡献者

| 贡献者 | GitHub | PRs | 主要领域 |
|--------|--------|-----|----------|
| [Shaojin Wen](../shaojin-wen.md) | [@wenshao](https://github.com/wenshao) | 97 | 核心库优化 |
| [Kuai Wei](../kuai-wei.md) | [@kuaiwei](https://github.com/kuaiwei) | 13 | C2 编译器 |

---

## 贡献时间线

```
2018-2022: 早期贡献
2023:      核心库优化加速
2024:      高峰期 (大量 PR 合并)
2025:      持续贡献
```

---

## 影响的模块

| 目录 | 修改次数 | 说明 |
|------|----------|------|
| java.lang | 23 | 核心类库 |
| AArch64 移植 | 21 | ARM 架构优化 |
| java.util | 14 | 集合框架 |
| java.text | 14 | 文本格式化 |
| jdk.internal.util | 10 | 内部工具类 |
| java.time | 9 | 日期时间 |
| C2 编译器 | 8 | 服务端编译器 |
| G1 GC | 8 | G1 垃圾收集器 |

---

## 关键贡献

### 核心库性能优化

| Issue | 标题 | 性能影响 |
|-------|------|----------|
| 8337832 | DateTime toString 优化 | +10% |
| 8338936 | StringConcatFactory MethodType 优化 | 启动优化 |
| 8338532 | ClassFile API MethodTypeDesc 优化 | 启动优化 |
| 8336856 | 高效的隐藏类字符串拼接策略 | 启动优化 |
| 8336831 | StringConcatHelper.simpleConcat 优化 | +5% |
| 8310929 | Integer.toString 优化 | +10% |
| 8310502 | Long.fastUUID 优化 | +8% |

### 字符串处理优化

| Issue | 标题 | 说明 |
|-------|------|------|
| 8337168 | LocalDateTime.toString 优化 | 使用 StringBuilder.repeat |
| 8336741 | LocalTime.toString 优化 | 使用 StringBuilder.repeat |
| 8336706 | LocalDate.toString 优化 | 使用 StringBuilder.repeat |
| 8333833 | UUID.toString 移除 ByteArrayLittleEndian | 简化代码 |
| 8333396 | Format 使用 StringBuilder 内部实现 | 减少分配 |

### 格式化优化

| Issue | 标题 | 说明 |
|-------|------|------|
| 8335645 | Formatter trailingZeros 使用 String repeat | 性能提升 |
| 8335802 | HexFormat 使用 boolean 替代 enum | 启动优化 |
| 8335252 | Formatter.Conversion#isValid 简化 | 代码清理 |
| 8316426 | HexFormat.formatHex 优化 | 性能提升 |
| 8316704 | Formatter 和 FormatProcessor 解析优化 | 无正则表达式 |

### C2 编译器

| Issue | 标题 | 说明 |
|-------|------|------|
| 8356328 | C2 IR 节点 size_of() 函数 | 正确性修复 |
| 8347405 | MergeStores 反向字节顺序 | 正确性修复 |
| 8339299 | C1 内联 final 方法丢失类型 profile | 性能修复 |
| 8326135 | ADLC 报告未使用的操作数 | 工具改进 |

### AArch64 优化

| Issue | 标题 | 说明 |
|-------|------|------|
| 8325821 | AArch64 release barrier 优化 | 性能提升 |
| 8331558 | AArch64 整数取余优化 | 性能提升 |
| 8333410 | AArch64 清理未使用的类 | 代码清理 |
| 8323122 | AArch64 itable stub 大小估算 | 正确性修复 |
| 8242449 | AArch64 r27 在 CompressedOops 模式下可分配 | Bug 修复 |

### RISC-V 修复

| Issue | 标题 | 说明 |
|-------|------|------|
| 8326936 | RISC-V Shenandoah GC 原子操作崩溃修复 | **崩溃修复** |
| 8324280 | RISC-V VM_Version::parse_satp_mode 实现错误 | 正确性修复 |

---

## 技术特点

### 性能优化导向

- **字符串处理**: StringBuilder.repeat、减少分配
- **数字格式化**: Integer/Long.toString、UUID.toString
- **启动优化**: 消除嵌套类、@Stable 注解

### 实际场景驱动

- Dragonwell 在阿里巴巴大规模部署
- 针对电商、支付等场景优化
- 性能数据来自真实业务

### 多领域覆盖

- **核心库**: java.lang, java.util, java.time
- **编译器**: C2 IR 优化
- **架构**: AArch64, RISC-V
- **GC**: G1, Shenandoah, ZGC

---

## Alibaba Dragonwell

阿里巴巴维护自己的 JDK 发行版 Dragonwell：

| 特性 | 说明 |
|------|------|
| 基于 | OpenJDK |
| 支持 | 长期支持 (LTS) |
| 许可 | GPLv2 |
| 平台 | Linux, Windows, macOS |

**版本**: Dragonwell 8 / 11 / 17 / 21

---

## 影响评估

| 场景 | 受益优化 | 预期提升 |
|------|----------|----------|
| JSON 序列化 | 字符串拼接优化 | +10% |
| 日志格式化 | DateTime toString | +10% |
| UUID 处理 | UUID.toString | +8% |
| 应用启动 | 启动优化 | +5% |
| 数字转换 | Integer/Long.toString | +10% |

---

## 数据来源

- **统计方法**: GitHub PR search `repo:openjdk/jdk author:xxx type:pr label:integrated`
- **统计时间**: 2026-03-19

---

## 相关链接

- [Alibaba Dragonwell](https://github.com/alibaba/dragonwell8)
- [Dragonwell 文档](https://dragonwell-jdk.io/)
- [阿里云 Java](https://www.aliyun.com/product/dragonwell)
- [OpenJDK Census - swen](https://openjdk.org/census#swen)