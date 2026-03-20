# 近期改进

> JDK 21-26 JIT 编译器改进汇总

[← 返回 JIT 编译](../)

---

## SuperWord 向量化改进

### JDK-8340093: SuperWord 成本模型

**状态**: 已集成 (2024年11月)

**PR**: [openjdk/jdk#20964](https://github.com/openjdk/jdk/pull/20964)

**改进内容**:
- 实现智能成本模型，判断向量化是否收益
- 优化归约 (reduction) 向量化
- 改进 shuffle/pack/unpack 操作处理
- 修复小循环向量化问题

**影响**:
- 某些场景性能提升 10-30%
- 避免无效向量化的性能损失

**相关链接**:
- [Bug Report](https://bugs.openjdk.org/browse/JDK-8340093)
- [Mail List](https://mail.openjdk.org/pipermail/hotspot-compiler-dev/2024-November/081976.html)

### JDK-8344085: 小循环向量化优化

**改进内容**:
- 扩展向量化到小迭代次数循环
- 改善边界情况处理
- 优化 2-4 元素向量

---

## C2 性能修复

### JDK-8325497: C2 性能调查总纲

**状态**: 活跃 (Umbrella Issue)

**链接**: [JDK-8325497](https://bugs.openjdk.org/browse/JDK-8325497)

**范围**: 追踪 JDK 21 C2 性能问题

**子问题**:
- [JDK-8329777](https://bugs.openjdk.org/browse/JDK-8329777): GVN hash collision robustness
- [JDK-8336000](https://bugs.openjdk.org/browse/JDK-8336000): 2-element reduction profitability
- 多个其他性能修复

### JDK-8325495: Add 系列优化

**作者**: Roland Westrelin

**状态**: 8 个版本迭代 (2024年)

**链接**: [RFR v8](https://mail.openjdk.org/pipermail/hotspot-compiler-dev/2024-October/080608.html)

**改进内容**:
```java
// 优化前
int result = 0;
result += x;
result += x;
result += x;

// 优化后
int result = x * 3;
```

**模式**: 识别连续的相同值加法，转换为乘法

---

## 编译器稳定性

### JDK-8360035: PhaseIterGVN 崩溃修复

**影响版本**: JDK 11.0.27

**问题**: PhaseIterGVN 无限循环优化导致崩溃

**链接**: [JDK-8360035](https://bugs.openjdk.org/browse/JDK-8360035)

**修复**: 改进无限循环检测和处理

### JDK-8317349: 宏节点扩展随机化

**PR**: [8317349](https://mail.openjdk.org/pipermail/jdk-changes/2024-February/025917.html)

**改进内容**:
- 随机化宏节点扩展顺序
- 改善编译确定性
- 避免特定顺序触发的 bug

---

## 编译吞吐量

### JDK-8366118: 修复 DontCompileHugeMethods

**问题**: 分层编译下大方法未正确处理

**修复**: 确保分层编译正确处理大方法

### JDK-8368071: 编译吞吐量回归修复

**影响**: 编译性能下降 2-8X

**原因**: JDK-8355003 引入的回归

**修复**: 恢复编译吞吐量

### JDK-8365407: 方法训练数据竞争

**问题**: MethodTrainingData::verify() 竞争条件

**修复**: 改进并发访问处理

---

## 分层编译改进

### JDK-8368321: 重新思考温热方法编译延迟

**作者**: Igor Veresov

**改进内容**:
- 优化 lukewarm methods 编译策略
- 避免过早或过晚编译
- 改进启动性能

### JDK-8355003: 编译队列改进

**改进内容**:
- 优化编译任务调度
- 减少编译队列开销

---

## 平台特定改进

### AArch64

**JDK-8328306**: MacOS lazy JIT "write xor execute" 切换

**作者**: Andrew Haley

**改进内容**:
- 支持 Apple Silicon W^X 切换
- 符合 Apple 平台安全要求

### RISC-V

**JDK-8360520**: 修复 primitive array clone 回归

**作者**: Feilong Jiang

### s390x

**JDK-8377863**: 提高内联阈值

**作者**: Amit Kumar

**改进内容**: 内联阈值与其他平台一致

### PowerPC

**JDK-8188131**: 提高内联阈值

**作者**: David Briemann

---

## 标量替换改进

### JDConf 2024: Improving HotSpot Scalar Replacement

**演讲者**: Soares

**PDF**: [Improving HotSpot Scalar Replacement](https://jdconf.com/2024/downloads/JDConf%20202024-Improving%20HotSpot%20Scalar%20Replacement-Soares.pdf)

**改进内容**:
- 更多对象可标量替换
- 更激进的逃逸分析
- 转换内存访问为寄存器访问

---

## 代码生成改进

### MergeStore 优化专题

> **完整文档**: [MergeStore 优化](mergestore.md)

MergeStore 是 C2 JIT 编译器的重要优化，将多次连续的内存写入合并为单次宽写入。

**相关 PR**:
- [JDK-8333893](/by-pr/8333/8333893.md): StringBuilder append(boolean/null) 优化 (+5-15%)
- [JDK-8334342](/by-pr/8334/8334342.md): JMH 基准测试
- [PR #28228](https://github.com/openjdk/jdk/pull/28228): 合并两个 append(char)
- [PR #29688](https://github.com/openjdk/jdk/pull/29688): Latin1 字符优化
- [PR #29699](https://github.com/openjdk/jdk/pull/29699): StringBuilder char 优化

### JDK-8347405: MergeStores with Reverse Bytes Order

**版本**: JDK 23

**改进内容**: 字节序优化存储合并

### JDK-8366461: 移除过时的 MethodHandle invoke 逻辑

**作者**: Dean Long

**改进内容**: 简化代码生成，提高性能

---

## 工具和诊断改进

### JDK-8365891: 已完成任务不应在队列中

**作者**: Vladimir Kozlov

**问题**: 已完成的编译任务仍在队列

**修复**: 正确清理已完成任务

### JDK-8308094: 编译超时标志

**作者**: Manuel Hässig

**改进内容**:
- 添加编译超时检测
- 捕获长时间运行的编译

---

## 版本对比

| 版本 | 主要 JIT 改进 |
|------|--------------|
| **JDK 21** | 虚拟线程支持、Record 支持 |
| **JDK 22** | 未指定 (LTS 前夕) |
| **JDK 23** | SuperWord 改进、MergeStores |
| **JDK 24** | 编译器稳定性、性能修复 |
| **JDK 25** | 编译吞吐量、代码生成 |
| **JDK 26** | SuperWord 成本模型集成 |

---

## 邮件列表讨论

### hotspot-compiler-dev (2024)

**关键讨论**:
1. C2 SuperWord 成本模型设计
2. Add 系列优化 (多轮 RFR)
3. 编译吞吐量问题
4. PhaseIterGVN 稳定性

**存档**: [mail.openjdk.org/pipermail/hotspot-compiler-dev/](https://mail.openjdk.org/pipermail/hotspot-compiler-dev/)

---

## 相关链接

### Bug 追踪

- [JDK-8325497: C2 性能调查](https://bugs.openjdk.org/browse/JDK-8325497) - 总纲
- [JDK-8340093: SuperWord 成本模型](https://bugs.openjdk.org/browse/JDK-8340093)
- [JDK-8340238: C2 CPU 卡死](https://bugs.openjdk.org/browse/JDK-8340238)

### 技术博客

- [Emanuel's C2 Blog](https://eme64.github.io/blog/) - 2024-2025 新增 4 篇深入文章

### 学术论文

- [Understanding JIT Compiler Performance Bugs](https://arxiv.org/html/2603.06551v1) - 2025年发布
- [Translation Validation for HotSpot C2 Compiler](https://www.diva-portal.org/smash/get/diva2:1987997/FULLTEXT01.pdf)

---

## 参与贡献

### 如何报告 C2 问题

1. 收集信息:
   ```bash
   -XX:+PrintCompilation -XX:+PrintInlining -XX:+CITime
   ```

2. 最小化测试用例

3. 在 [bugs.openjdk.org](https://bugs.openjdk.org) 提交

4. 邮件发送到 hotspot-compiler-dev

### 贡献者指南

- [OpenJDK Contributing Guide](https://openjdk.org/contribute/)
- [HotSpot Project Page](https://openjdk.org/projects/hotspot/)
