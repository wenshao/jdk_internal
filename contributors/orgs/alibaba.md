# 阿里巴巴

> 核心库性能优化和 C2 编译器改进

---

## 概览

阿里巴巴通过 Dragonwell 团队参与 OpenJDK 开发，专注于核心库性能优化、字符串处理和 C2 编译器改进。

| 指标 | 值 |
|------|-----|
| **Integrated PRs** | 110 |
| **Git Commits** | 73 |
| **贡献者数** | 16 |
| **活跃时间** | 2018 - 至今 |
| **主要领域** | 核心库、C2 编译器、AArch64 |

> **统计说明**: 使用 GitHub Integrated PRs 作为主要贡献指标。部分贡献者通过其他方式提交代码，统计在 Git Commits 中。

---

## 贡献者

### GitHub PR 贡献者

| 贡献者 | GitHub | PRs | 主要领域 |
|--------|--------|-----|----------|
| [Shaojin Wen](../shaojin-wen.md) | [@wenshao](https://github.com/wenshao) | 97 | 核心库优化 |
| [Kuai Wei](../kuai-wei.md) | [@kuaiwei](https://github.com/kuaiwei) | 13 | C2 编译器 |

**小计**: 110 PRs

### 其他贡献者 (Git Commits)

| 贡献者 | Commits | 主要贡献 |
|--------|---------|----------|
| Yude Lin | 8 | G1 GC, Shenandoah, AArch64 |
| Zhuo Wang | 3 | Unsafe 修复 |
| Xiaowei Lu | 3 | ZGC, GC 日志 |
| Hao Tang | 2 | 容器 CPU, ZGC |
| Yibo Yang | 2 | 内存优化, Apple M1 |
| Sendao Yan | 2 | 测试修复 |
| Xingqi Zheng | 2 | RISC-V 修复 |
| Yang Yi | 2 | Metaspace, 文件流 |
| lingjun.cg | 2 | 测试 |
| MaxXSoft | 2 | 测试 |
| yibo.yl | 2 | 测试 |
| Quan Zhang | 1 | 测试 |
| gaogao-mem | 1 | 测试 |
| yifeng.jyf | 1 | 测试 |
| 释天 | 1 | 测试 |

**小计**: 35 commits

---

## 贡献时间线

```
2018: █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 1 commit
2019: ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 2 commits
2020: █████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 5 commits
2021: ██████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 10 commits
2022: ███░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 3 commits
2023: ██████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 10 commits
2024: ████████████████████████████████████████████████████████████████████ 38 commits (高峰期)
2025: ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 4 commits
```

> **总计**: 73 commits (2018-2025)

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

### GC 优化

| Issue | 标题 | 说明 | 贡献者 |
|-------|------|------|--------|
| 8297247 | G1 添加 Remark 和 Cleanup 暂停时间 MXBean | 监控增强 | Yude Lin |
| 8298521 | G1MonitoringSupport 成员重命名 | 代码清理 | Yude Lin |
| 8270347 | ZGC 采用 release-acquire 顺序 | 正确性 | Xiaowei Lu |
| 8272138 | ZGC 采用宽松顺序进行自愈 | 性能优化 | Xiaowei Lu |
| 8229406 | ZGC 修复统计错误 | 正确性 | Hao Tang |

### RISC-V 修复

| Issue | 标题 | 说明 | 贡献者 |
|-------|------|------|--------|
| 8326936 | RISC-V Shenandoah GC 原子操作崩溃修复 | **崩溃修复** | Xingqi Zheng |
| 8324280 | RISC-V VM_Version::parse_satp_mode 实现错误 | 正确性修复 | Xingqi Zheng |

### 容器与平台

| Issue | 标题 | 说明 | 贡献者 |
|-------|------|------|--------|
| 8265836 | 容器内 CPU 负载不正确 | Bug 修复 | Hao Tang |
| 8326446 | Apple M1 CPU 负载不准确 | Bug 修复 | Yibo Yang |
| 8319876 | VM_ThreadDump 内存消耗优化 | 性能优化 | Yibo Yang |

### 其他修复

| Issue | 标题 | 说明 | 贡献者 |
|-------|------|------|--------|
| 8246051 | Unsafe 非对齐 compare_and_swap 导致 SIGBUS | **崩溃修复** | Zhuo Wang |
| 8273112 | -Xloggc 应覆盖 -verbose:gc | 功能修复 | Xiaowei Lu |
| 8262099 | VM.metaspace 应报告无限制大小 | 功能修复 | Yang Yi |

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

- **PR 统计**: GitHub PR search `repo:openjdk/jdk author:xxx type:pr label:integrated`
- **Commit 统计**: `git log upstream_master --author="alibaba-inc.com"`
- **统计时间**: 2026-03-19

---

## 相关链接

- [Alibaba Dragonwell](https://github.com/alibaba/dragonwell8)
- [Dragonwell 文档](https://dragonwell-jdk.io/)
- [阿里云 Java](https://www.aliyun.com/product/dragonwell)
- [OpenJDK Census - swen](https://openjdk.org/census#swen)