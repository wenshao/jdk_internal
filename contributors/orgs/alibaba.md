# 阿里巴巴

> 核心库性能优化和 C2 编译器改进

---

## 概览

阿里巴巴通过 Dragonwell 团队参与 OpenJDK 开发，专注于核心库性能优化、字符串处理和 C2 编译器改进。

| 指标 | 值 |
|------|-----|
| **Integrated PRs** | 121 |
| **贡献者数** | 4 |
| **活跃时间** | 2021 - 至今 |
| **主要领域** | 核心库、C2 编译器、AArch64、ZGC |

> **统计说明**: 使用 GitHub Integrated PRs 作为贡献指标。查询方式：`repo:openjdk/jdk author:xxx type:pr label:integrated`

---

## 贡献者

| 贡献者 | GitHub | PRs | 主要领域 |
|--------|--------|-----|----------|
| [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | [@wenshao](https://github.com/wenshao) | 97 | 核心库优化 |
| [Kuai Wei](../../by-contributor/profiles/kuai-wei.md) | [@kuaiwei](https://github.com/kuaiwei) | 13 | C2 编译器 |
| [Yude Lin](../../by-contributor/profiles/yude-lin.md) | [@linade](https://github.com/linade) | 8 | G1 GC, AArch64 |
| [Xiaowei Lu](../../by-contributor/profiles/xiaowei-lu.md) | [@weixlu](https://github.com/weixlu) | 3 | ZGC |

---

## 贡献时间线

```
2021: █████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 7 PRs
2022: ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 2 PRs
2023: ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 8 PRs
2024: ███████████████████████████████████████████████████████████████░░ 68 PRs (高峰期)
2025: █████████████████████████████████████████████████████████░░░░░░░░ 35 PRs
2026: █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 1 PR
```

> **总计**: 121 PRs (2021-2026)

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

### 核心库性能优化 (Shaojin Wen)

| Issue | 标题 | 性能影响 |
|-------|------|----------|
| 8337832 | DateTime toString 优化 | +10% |
| 8338936 | StringConcatFactory MethodType 优化 | 启动优化 |
| 8338532 | ClassFile API MethodTypeDesc 优化 | 启动优化 |
| 8336856 | 高效的隐藏类字符串拼接策略 | 启动优化 |
| 8336831 | StringConcatHelper.simpleConcat 优化 | +5% |
| 8310929 | Integer.toString 优化 | +10% |
| 8310502 | Long.fastUUID 优化 | +8% |

### C2 编译器 (Kuai Wei)

| Issue | 标题 | 说明 |
|-------|------|------|
| 8356328 | C2 IR 节点 size_of() 函数 | 正确性修复 |
| 8347405 | MergeStores 反向字节顺序 | 正确性修复 |
| 8339299 | C1 内联 final 方法丢失类型 profile | 性能修复 |
| 8326135 | ADLC 报告未使用的操作数 | 工具改进 |

### G1 GC 和 AArch64 (Yude Lin)

| Issue | 标题 | 说明 |
|-------|------|------|
| 8297247 | G1 添加 Remark 和 Cleanup 暂停时间 MXBean | **监控增强** |
| 8298521 | G1MonitoringSupport 成员重命名 | 代码清理 |
| 8323122 | AArch64 itable stub 大小估算 | 正确性修复 |

### ZGC 优化 (Xiaowei Lu)

| Issue | 标题 | 说明 |
|-------|------|------|
| 8272138 | ZGC 采用宽松顺序进行自愈 | **性能优化** |
| 8270347 | ZGC 转发表采用 release-acquire 顺序 | 正确性修复 |
| 8273112 | -Xloggc 应覆盖 -verbose:gc | 功能修复 |

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
- **架构**: AArch64
- **GC**: G1, ZGC

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