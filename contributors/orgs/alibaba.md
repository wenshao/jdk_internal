# 阿里巴巴

> 核心库性能优化和 C2 编译器改进

---

## 概览

阿里巴巴通过 Dragonwell 团队参与 OpenJDK 开发，专注于核心库性能优化、字符串处理和 C2 编译器改进。

| 指标 | 值 |
|------|-----|
| **Integrated PRs** | 110 |
| **贡献者数** | 2+ |
| **主要领域** | 核心库、C2 编译器 |

---

## Top 贡献者

| 排名 | 贡献者 | GitHub | PRs | 领域 |
|------|--------|--------|-----|------|
| 1 | [Shaojin Wen](../shaojin-wen.md) | [@wenshao](https://github.com/wenshao) | 97 | 核心库优化 |
| 2 | [Kuai Wei](../kuai-wei.md) | [@kuaiwei](https://github.com/kuaiwei) | 13 | C2 编译器 |

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

## 关键贡献

### 核心库优化

| Issue | 标题 | 性能影响 |
|-------|------|----------|
| 8355177 | StringBuilder::append(char[]) 优化 | +15% |
| 8370503 | Integer/Long.toString 简化 | +10% |
| 8370013 | Double.toHexString 重构 | +20% |
| 8353741 | UUID.toString 优化 | +8% |
| 8349400 | 消除嵌套类提升启动速度 | +5% |

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

## Alibaba Dragonwell

阿里巴巴维护自己的 JDK 发行版 Dragonwell：

| 特性 | 说明 |
|------|------|
| 基于 | OpenJDK |
| 支持 | 长期支持 (LTS) |
| 许可 | GPLv2 |
| 平台 | Linux, Windows, macOS |

**特点**:
- 免费生产就绪
- 长期支持
- AWS 优化
- 安全补丁

---

## 数据来源

- **统计方法**: GitHub PR search `repo:openjdk/jdk author:xxx type:pr label:integrated`
- **统计时间**: 2026-03-19

---

## 相关链接

- [Alibaba Dragonwell](https://github.com/alibaba/dragonwell8)
- [Dragonwell 文档](https://dragonwell-jdk.io/)
- [阿里云 Java](https://www.aliyun.com/product/dragonwell)