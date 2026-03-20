# 阿里巴巴

> 核心库性能优化和 C2 编译器改进

[← 返回组织索引](../../by-contributor/index.md)

---

## 概览

阿里巴巴通过 Dragonwell 团队参与 OpenJDK 开发，专注于核心库性能优化、字符串处理和 C2 编译器改进。

| 指标 | 值 |
|------|-----|
| **Integrated PRs** | 121 |
| **贡献者数** | 4 |
| **活跃时间** | 2021 - 至今 |
| **主要领域** | 核心库、C2 编译器、AArch64、ZGC |
| **Dragonwell** | [Alibaba Dragonwell](https://github.com/alibaba/dragonwell8) |

> **统计说明**: 使用 GitHub Integrated PRs 作为贡献指标。查询方式：`repo:openjdk/jdk author:xxx type:pr label:integrated`

---

## 贡献者

| 贡献者 | GitHub | PRs | 角色 | 主要领域 |
|--------|--------|-----|------|----------|
| [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | [@wenshao](https://github.com/wenshao) | 97 | Committer | 核心库优化 |
| [Kuai Wei](../../by-contributor/profiles/kuai-wei.md) | [@kuaiwei](https://github.com/kuaiwei) | 13 | Author | C2 编译器 |
| [Yude Lin](../../by-contributor/profiles/yude-lin.md) | [@linade](https://github.com/linade) | 8 | Author | G1 GC, AArch64 |
| [Xiaowei Lu](../../by-contributor/profiles/xiaowei-lu.md) | [@weixlu](https://github.com/weixlu) | 3 | Author | ZGC |

---

## 技术领域

| 领域 | 贡献者数 | 关键 PR | 相关文档 |
|------|---------|---------|----------|
| **核心库优化** | 1 | 60+ | [字符串优化](../../by-topic/core/performance/string-optimization.md) |
| **C2 编译器** | 1 | 4 | [C2 优化阶段](../../by-topic/core/jit/c2-phases.md) |
| **G1 GC** | 1 | 3 | [G1 GC](../../by-topic/core/gc/g1-gc.md) |
| **ZGC** | 1 | 2 | [ZGC](../../by-topic/core/gc/zgc.md) |
| **AArch64** | 1 | 2 | [AArch64](../../by-topic/core/arch/aarch64.md) |

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

| Issue | 标题 | 性能影响 | 深度分析 |
|-------|------|----------|----------|
| 8337832 | DateTime toString 优化 | +10% | [分析](../../by-pr/8337/8337832.md) |
| 8338936 | StringConcatFactory MethodType 优化 | 启动优化 | [分析](../../by-pr/8338/8338936.md) |
| 8338532 | ClassFile API MethodTypeDesc 优化 | 启动优化 | [分析](../../by-pr/8338/8338532.md) |
| 8336856 | 高效的隐藏类字符串拼接策略 | 启动优化 | [分析](../../by-pr/8336/8336856.md) |
| 8336831 | StringConcatHelper.simpleConcat 优化 | +5% | [分析](../../by-pr/8336/8336831.md) |
| 8310929 | Integer.toString 优化 | +10% | [分析](../../by-pr/8310/8310929.md) |
| 8310502 | Long.fastUUID 优化 | +8% | [分析](../../by-pr/8310/8310502.md) |
| 8370013 | ArraysSupport big endian 支持 | 新功能 | - |
| 8365832 | HexFormat boolean 替换 enum | 启动优化 | [分析](../../by-pr/8365/8365832.md) |
| 8366224 | Character checkTitleCase 优化 | 性能优化 | - |
| 8368825 | StringBuilder CharSequence 支持 | API 增强 | - |
| 8357685 | String indexOf.last 优化 | +5% | [分析](../../by-pr/8357/8357685.md) |
| 8353741 | HexFormat toUpper/toLower 优化 | 性能优化 | [分析](../../by-pr/8353/8353741.md) |
| 8348870 | ByteOrder.toString 优化 | 性能优化 | - |
| 8343962 | ArraysSupport.arrayToString 优化 | +3% | [分析](../../by-pr/8343/8343962.md) |
| 8343984 | Unsafe 越界检查优化 | 安全性 | - |
| 8316426 | HexFormat 实现 | 新功能 | [分析](../../by-pr/8316/8316426.md) |
| 8316704 | HexFormat fromHexDigit 实现 | 新功能 | - |
| 8335802 | Formatter formatSpecifier 优化 | 性能优化 | - |
| 8335645 | Formatter parseType 优化 | 性能优化 | - |
| 8335252 | Formatter formatWith 优化 | 性能优化 | - |
| 8334328 | Formatter isFixed 优化 | 性能优化 | - |
| 8337168 | Formatter minIntegerDigits 优化 | 性能优化 | - |
| 8337167 | Formatter parse 优化 | 性能优化 | - |

> **更多**: [Shaojin Wen 贡献者档案](../../by-contributor/profiles/shaojin-wen.md) | [完整 PR 列表](../../by-contributor/profiles/shaojin-wen.md#complete-pr-list)

### C2 编译器 (Kuai Wei)

| Issue | 标题 | 说明 |
|-------|------|------|
| 8356328 | C2 IR 节点 size_of() 函数 | 正确性修复 |
| 8347405 | MergeStores 反向字节顺序 | 正确性修复 |
| 8339299 | C1 内联 final 方法丢失类型 profile | 性能修复 |
| 8326135 | ADLC 报告未使用的操作数 | 工具改进 |

> **更多**: [Kuai Wei 贡献者档案](../../by-contributor/profiles/kuai-wei.md)

### G1 GC 和 AArch64 (Yude Lin)

| Issue | 标题 | 说明 |
|-------|------|------|
| 8297247 | G1 添加 Remark 和 Cleanup 暂停时间 MXBean | **监控增强** |
| 8298521 | G1MonitoringSupport 成员重命名 | 代码清理 |
| 8323122 | AArch64 itable stub 大小估算 | 正确性修复 |

> **更多**: [Yude Lin 贡献者档案](../../by-contributor/profiles/yude-lin.md)

### ZGC 优化 (Xiaowei Lu)

| Issue | 标题 | 说明 |
|-------|------|------|
| 8272138 | ZGC 采用宽松顺序进行自愈 | **性能优化** |
| 8270347 | ZGC 转发表采用 release-acquire 顺序 | 正确性修复 |
| 8273112 | -Xloggc 应覆盖 -verbose:gc | 功能修复 |

> **更多**: [Xiaowei Lu 贡献者档案](../../by-contributor/profiles/xiaowei-lu.md) |

---

## 相关 PR 分析文档

### 核心性能优化 (Shaojin Wen)

| PR | 标题 | 性能影响 | 分析文档 |
|----|------|----------|----------|
| JDK-8336856 | Inline concat with InlineHiddenClassStrategy | 启动优化 | [详情](../../by-pr/8336/8336856.md) |
| JDK-8337832 | DateTime toString 优化 | +10% | [详情](../../by-pr/8337/8337832.md) |
| JDK-8310929 | Integer.toString() 优化 | +10% | [详情](../../by-pr/8310/8310929.md) |
| JDK-8310502 | Long.fastUUID() 优化 | +8% | [详情](../../by-pr/8310/8310502.md) |
| JDK-8357685 | String.indexOf.last() 优化 | +5% | [详情](../../by-pr/8357/8357685.md) |
| JDK-8343962 | ArraysSupport.arrayToString() 优化 | +3% | [详情](../../by-pr/8343/8343962.md) |

### ClassFile API 优化 (Shaojin Wen)

| PR | 标题 | 影响 | 分析文档 |
|----|------|------|----------|
| JDK-8338936 | StringConcatFactory MethodType 优化 | 启动优化 | [详情](../../by-pr/8338/8338936.md) |
| JDK-8338532 | MethodTypeDesc 实现优化 | 启动优化 | [详情](../../by-pr/8338/8338532.md) |

### Formatter/HexFormat (Shaojin Wen)

| PR | 标题 | 分析文档 |
|----|------|----------|
| JDK-8335802 | Formatter formatSpecifier 优化 | [详情](../../by-pr/8335/8335802.md) |
| JDK-8335645 | Formatter parseType 优化 | [详情](../../by-pr/8335/8335645.md) |
| JDK-8335252 | Formatter formatWith 优化 | [详情](../../by-pr/8335/8335252.md) |
| JDK-8334328 | Formatter isFixed 优化 | [详情](../../by-pr/8334/8334328.md) |
| JDK-8337168 | Formatter minIntegerDigits 优化 | [详情](../../by-pr/8337/8337168.md) |
| JDK-8337167 | Formatter parse 优化 | [详情](../../by-pr/8337/8337167.md) |
| JDK-8316426 | HexFormat 实现 | [详情](../../by-pr/8316/8316426.md) |
| JDK-8316704 | HexFormat fromHexDigit 实现 | [详情](../../by-pr/8316/8316704.md) |
| JDK-8353741 | HexFormat toUpper/toLower() 优化 | [详情](../../by-pr/8353/8353741.md) |
| JDK-8365832 | HexFormat boolean 替换 enum | [详情](../../by-pr/8365/8365832.md) |

### C2 编译器 (Kuai Wei)

| PR | 标题 | 说明 | 分析文档 |
|----|------|------|----------|
| JDK-8356328 | C2 IR 节点 size_of() 函数 | 正确性修复 | [详情](../../by-pr/8356/8356328.md) |
| JDK-8347405 | MergeStores 反向字节顺序 | 正确性修复 | - |

### GC (Yude Lin, Xiaowei Lu)

| PR | 标题 | 贡献者 | 说明 |
|----|------|--------|------|
| JDK-8297247 | G1 Remark/Cleanup MXBean | [Yude Lin](../../by-contributor/profiles/yude-lin.md) | 监控增强 |
| JDK-8272138 | ZGC 自愈宽松顺序 | [Xiaowei Lu](../../by-contributor/profiles/xiaowei-lu.md) | 性能优化 |
| JDK-8270347 | ZGC 转发表 release-acquire | [Xiaowei Lu](../../by-contributor/profiles/xiaowei-lu.md) | 正确性修复 |
| JDK-8323122 | AArch64 itable stub 大小 | [Yude Lin](../../by-contributor/profiles/yude-lin.md) | 正确性修复 |

---

## 技术深度分析

### 字符串拼接优化 (JDK-8336856)

**问题**: Java 9 的 `invokedynamic` 字符串拼接在高参数场景存在扩展性问题

**解决方案**: 引入 `InlineHiddenClassStrategy`，消除大量嵌套类生成

**技术细节**:
- 减少类加载开销
- 提升 C2 编译器内存效率
- 保持向后兼容性

→ [完整分析](../../by-pr/8336/8336856.md) | [String "+" 运算符](../../by-topic/core/performance/string-concat.md)

### DateTime 格式化优化 (JDK-8337832)

**优化点**: `DateTimeFormatter.toString()` 性能提升 10%

**技术手段**:
- 减少方法调用开销
- 优化格式化逻辑
- 缓存常用格式

→ [完整分析](../../by-pr/8337/8337832.md) | [日期时间 API](../../by-topic/core/library/datetime.md)

### C2 IR 节点修复 (JDK-8356328)

**问题**: 部分 C2 IR 节点缺少 `size_of()` 函数实现

**影响**: 导致编译器断言失败

**解决方案**: 为缺失节点添加正确的 `size_of()` 实现

→ [完整分析](../../by-pr/8356/8356328.md) | [C2 编译器](../../by-topic/core/jit/c2-phases.md)

---

## 相关主题文档

### 核心库

| 主题 | 描述 | 链接 |
|------|------|------|
| 字符串处理 | String, StringBuilder 优化 | [字符串优化](../../by-topic/core/performance/string-optimization.md) |
| 数字格式化 | Integer/Long toString 优化 | [数字格式化](../../by-topic/core/performance/number-formatting.md) |
| ClassFile API | 字节码操作 API | [ClassFile API](../../by-topic/core/classfile/index.md) |

### 编译器

| 主题 | 描述 | 链接 |
|------|------|------|
| C2 编译器 | 服务端编译器优化阶段 | [C2 阶段](../../by-topic/core/jit/c2-phases.md) |
| JIT 编译 | 即时编译器概述 | [JIT 编译](../../by-topic/core/jit/index.md) |
| IR 节点 | 中间表示节点 | [C2 IR](../../by-topic/core/jit/c2-ir.md) |

### 垃圾收集

| 主题 | 描述 | 链接 |
|------|------|------|
| G1 GC | Garbage First 收集器 | [G1 GC](../../by-topic/core/gc/g1-gc.md) |
| ZGC | Z Garbage Collector | [ZGC](../../by-topic/core/gc/zgc.md) |
| Shenandoah | 低暂停 GC | [Shenandoah](../../by-topic/core/gc/shenandoah.md) |

### 架构

| 主题 | 描述 | 链接 |
|------|------|------|
| AArch64 | ARM 64 位架构 | [AArch64](../../by-topic/core/arch/aarch64.md) |
| x86/x64 | Intel/AMD 架构 | [x86/x64](../../by-topic/core/arch/x86.md) |

---

[→ 返回组织索引](../../by-contributor/index.md)

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

| 场景 | 受益优化 | 预期提升 | 相关 PR |
|------|----------|----------|---------|
| JSON 序列化 | 字符串拼接优化 | +10% | [8336856](../../by-pr/8336/8336856.md) |
| 日志格式化 | DateTime toString | +10% | [8337832](../../by-pr/8337/8337832.md) |
| UUID 处理 | UUID.toString | +8% | [8310502](../../by-pr/8310/8310502.md) |
| 应用启动 | 启动优化 | +5% | [8338936](../../by-pr/8338/8338936.md) |
| 数字转换 | Integer/Long.toString | +10% | [8310929](../../by-pr/8310/8310929.md) |
| 数组操作 | ArraysSupport 优化 | +3% | [8343962](../../by-pr/8343/8343962.md) |

> **了解更多**: [JDK 性能优化](../../by-topic/core/performance/index.md)

---

## 数据来源

- **统计方法**: GitHub PR search `repo:openjdk/jdk author:xxx type:pr label:integrated`
- **统计时间**: 2026-03-19
- **分析工具**: [PR Analysis Tool](../../tools/pr-analysis.md)

---

## 相关链接

### 外部资源

- [Alibaba Dragonwell](https://github.com/alibaba/dragonwell8)
- [Dragonwell 文档](https://dragonwell-jdk.io/)
- [阿里云 Java](https://www.aliyun.com/product/dragonwell)
- [OpenJDK Census - swen](https://openjdk.org/census#swen)

### 内部文档

- [Shaojin Wen 贡献者档案](../../by-contributor/profiles/shaojin-wen.md) - 核心库优化专家
- [Kuai Wei 贡献者档案](../../by-contributor/profiles/kuai-wei.md) - C2 编译器专家
- [Yude Lin 贡献者档案](../../by-contributor/profiles/yude-lin.md) - G1 GC 专家
- [Xiaowei Lu 贡献者档案](../../by-contributor/profiles/xiaowei-lu.md) - ZGC 专家
- [中囯贡献者索引](../../by-contributor/profiles/chinese-contributors.md)