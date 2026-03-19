# SendaoYan

> JDK 测试稳定性专家，202 integrated PRs

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | SendaoYan |
| **当前组织** | 海光信息 (Hygon) |
| **GitHub** | [@SendaoYan](https://github.com/SendaoYan) |
| **OpenJDK** | [@syan](https://openjdk.org/census#syan) |
| **角色** | JDK Committer |
| **PRs** | [202 integrated](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3ASendaoYan+is%3Aclosed+label%3Aintegrated) |
| **主要领域** | 测试稳定性、测试修复、Docker 容器测试 |
| **活跃时间** | 2022 - 至今 |

### 组织历史

| 时间段 | 组织 | 邮箱 |
|--------|------|------|
| 2022 - 2024 | 阿里巴巴 (Alibaba) | yansendao.ysd@alibaba-inc.com |
| 2025 - 至今 | 海光信息 (Hygon) | yansendao@hygon.cn |

> **数据调查时间**: 2026-03-19

---

## 技术影响力

| 指标 | 值 |
|------|-----|
| **代码行数** | +3,982 / -3,541 (净 +441) |
| **影响模块** | test (测试) |
| **主要贡献** | 测试稳定性修复、测试跳过改进 |

### 影响的主要目录

| 目录 | 文件数 | 说明 |
|------|--------|------|
| test/.../BasicFileAttributeView | 39 | 文件属性测试 |
| test/.../docker | 32 | Docker 容器测试 |
| test/.../SctpChannel | 30 | SCTP 测试 |
| test/.../foreign | 18 | Foreign API 测试 |
| test/.../jfr | 14 | JFR 测试 |

---

## 贡献时间线

```
2022: ░░░░░░░░░░░░░░░░░░░░   1 commit
2023: ░░░░░░░░░░░░░░░░░░░░   0 commits
2024: ████████████████░░░░ 106 commits
2025: ████████████████████ 131 commits (峰值)
2026: █████████░░░░░░░░░░░  61 commits (进行中)
```

---

## 技术特长

`测试稳定性` `Docker 测试` `SCTP` `JFR 测试` `测试跳过` `间歇性失败修复`

---

## 代表性工作

### 1. 测试稳定性专家
202 个 integrated PRs，专注于修复间歇性测试失败，提升 CI/CD 稳定性。

### 2. Docker 容器测试
大量 Docker 相关测试的修复和改进，确保容器环境下的测试稳定性。

### 3. SCTP 测试
SCTP (Stream Control Transmission Protocol) 相关测试的修复。

### 4. JFR 测试
Java Flight Recorder 测试的稳定性改进。

### 5. 测试跳过逻辑
改进测试跳过逻辑，确保测试在特定条件下正确跳过。

---

## 外部资源

| 类型 | 链接 |
|------|------|
| **GitHub** | [@SendaoYan](https://github.com/SendaoYan) |
| **OpenJDK Census** | [syan](https://openjdk.org/census#syan) |

---

### 按类别统计

| 类别 | 数量 | 占比 |
|------|------|------|
| 测试超时修复 | 35 | 40% |
| 测试跳过修复 | 25 | 28% |
| 测试问题列表 | 15 | 17% |
| 构建修复 | 8 | 9% |
| 其他 | 5 | 6% |

### 关键成就

- 修复了大量间歇性测试失败
- 改进了测试跳过逻辑
- 提升了测试稳定性

---

## PR 列表

### 测试超时修复

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8370501 | vmTestbase/vm/gc/compact/Humongous_NonbranchyTree5M/TestDescription.java intermittent timed out | [JBS-8370501](https://bugs.openjdk.org/browse/JDK-8370501) |
| 8368866 | compiler/codecache/stress/UnexpectedDeoptimizationTest.java intermittent timed out | [JBS-8368866](https://bugs.openjdk.org/browse/JDK-8368866) |
| 8354894 | java/lang/Thread/virtual/Starvation.java timeout on server with high CPUs | [JBS-8354894](https://bugs.openjdk.org/browse/JDK-8354894) |
| 8368668 | Several vmTestbase/vm/gc/compact tests timed out on large memory machine | [JBS-8368668](https://bugs.openjdk.org/browse/JDK-8368668) |
| 8368552 | H3ErrorHandlingTest.testCloseControlStream intermittent timed out | [JBS-8368552](https://bugs.openjdk.org/browse/JDK-8368552) |
| 8368373 | Test H3MalformedResponseTest.testMalformedResponse intermittent timed out | [JBS-8368373](https://bugs.openjdk.org/browse/JDK-8368373) |
| 8367869 | Test java/io/FileDescriptor/Sync.java timed out | [JBS-8367869](https://bugs.openjdk.org/browse/JDK-8367869) |
| 8366695 | Test sun/jvmstat/monitor/MonitoredVm/MonitorVmStartTerminate.java timed out | [JBS-8366695](https://bugs.openjdk.org/browse/JDK-8366695) |
| 8366694 | Test JdbStopInNotificationThreadTest.java timed out after 60 second | [JBS-8366694](https://bugs.openjdk.org/browse/JDK-8366694) |
| 8366692 | Several gc/shenandoah tests timed out | [JBS-8366692](https://bugs.openjdk.org/browse/JDK-8366692) |
| 8359272 | Several vmTestbase/compact tests timed out on large memory machine | [JBS-8359272](https://bugs.openjdk.org/browse/JDK-8359272) |

### 测试跳过修复

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8368677 | acvp test should throw SkippedException when no ACVP-Server available | [JBS-8368677](https://bugs.openjdk.org/browse/JDK-8368677) |
| 8367904 | Test java/net/InetAddress/ptr/Lookup.java should throw SkippedException | [JBS-8367904](https://bugs.openjdk.org/browse/JDK-8367904) |
| 8365983 | Tests should throw SkippedException when SCTP not supported | [JBS-8365983](https://bugs.openjdk.org/browse/JDK-8365983) |
| 8366359 | Test should throw SkippedException when there is no lpstat | [JBS-8366359](https://bugs.openjdk.org/browse/JDK-8366359) |
| 8362855 | Test java/net/ipv6tests/TcpTest.java should report SkippedException | [JBS-8362855](https://bugs.openjdk.org/browse/JDK-8362855) |
| 8359402 | Test CloseDescriptors.java should throw SkippedException when there is no lsof/sctp | [JBS-8359402](https://bugs.openjdk.org/browse/JDK-8359402) |
| 8359182 | Use @requires instead of SkippedException for MaxPath.java | [JBS-8359182](https://bugs.openjdk.org/browse/JDK-8359182) |
| 8359083 | Test jdkCheckHtml.java should report SkippedException rather than report fails | [JBS-8359083](https://bugs.openjdk.org/browse/JDK-8359083) |

### 测试问题列表

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8370649 | Add intermittent tag for gc/shenandoah/generational/TestOldGrowthTriggers.java | [JBS-8370649](https://bugs.openjdk.org/browse/JDK-8370649) |
| 8366849 | Problemlist jdk/jshell/ToolSimpleTest.java as generic-all | [JBS-8366849](https://bugs.openjdk.org/browse/JDK-8366849) |
| 8366768 | Problemlist jdk/jshell/ToolSimpleTest.java | [JBS-8366768](https://bugs.openjdk.org/browse/JDK-8366768) |
| 8366031 | Mark com/sun/nio/sctp/SctpChannel/CloseDescriptors.java as intermittent | [JBS-8366031](https://bugs.openjdk.org/browse/JDK-8366031) |
| 8365834 | Mark java/net/httpclient/ManyRequests.java as intermittent | [JBS-8365834](https://bugs.openjdk.org/browse/JDK-8365834) |
| 8359207 | Remove runtime/signal/TestSigusr2.java since it is always skipped | [JBS-8359207](https://bugs.openjdk.org/browse/JDK-8359207) |

### 构建修复

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8372125 | containers/docker/TestPids.java fails after 8365606 | [JBS-8372125](https://bugs.openjdk.org/browse/JDK-8372125) |
| 8371697 | test/jdk/java/nio/file/FileStore/Basic.java fails after 8360887 on linux | [JBS-8371697](https://bugs.openjdk.org/browse/JDK-8371697) |
| 8366777 | Build fails unknown pseudo-op with old AS on linux-aarch64 | [JBS-8366777](https://bugs.openjdk.org/browse/JDK-8366777) |
| 8354766 | Test TestUnexported.java javac build fails | [JBS-8354766](https://bugs.openjdk.org/browse/JDK-8354766) |
| 8353189 | [ASAN] memory leak after 8352184 | [JBS-8353189](https://bugs.openjdk.org/browse/JDK-8353189) |
| 8304674 | File java.c compile error with -fsanitize=address -O0 | [JBS-8304674](https://bugs.openjdk.org/browse/JDK-8304674) |

### 其他修复

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8371682 | Suppress javac warning from ThreadPoolExecutorSubclassTest.java | [JBS-8371682](https://bugs.openjdk.org/browse/JDK-8371682) |
| 8370732 | Use WhiteBox.getWhiteBox().fullGC() to provoking gc for nsk/jvmti tests | [JBS-8370732](https://bugs.openjdk.org/browse/JDK-8370732) |
| 8343340 | Swapping checking do not work for MetricsMemoryTester failcount | [JBS-8343340](https://bugs.openjdk.org/browse/JDK-8343340) |
| 8369490 | Remove unused Runinfo parameters in compiler/c2/gvn/TestBitCompressValueTransform.java | [JBS-8369490](https://bugs.openjdk.org/browse/JDK-8369490) |
| 8366476 | Test gc/z/TestSmallHeap.java fails OOM with many NUMA nodes | [JBS-8366476](https://bugs.openjdk.org/browse/JDK-8366476) |
| 8362501 | Update test/hotspot/jtreg/applications/jcstress/README | [JBS-8362501](https://bugs.openjdk.org/browse/JDK-8362501) |
| 8364114 | Test TestHugePageDecisionsAtVMStartup.java#LP_enabled fails when no free hugepage | [JBS-8364114](https://bugs.openjdk.org/browse/JDK-8364114) |
| 8359827 | Test runtime/Thread/ThreadCountLimit.java need loop increasing the limit | [JBS-8359827](https://bugs.openjdk.org/browse/JDK-8359827) |
| 8362834 | Several runtime/Thread tests should mark as /native | [JBS-8362834](https://bugs.openjdk.org/browse/JDK-8362834) |
| 8362379 | Test serviceability/HeapDump/UnmountedVThreadNativeMethodAtTop.java should mark as /native | [JBS-8362379](https://bugs.openjdk.org/browse/JDK-8362379) |
| 8361869 | Tests which call ThreadController should mark as /native | [JBS-8361869](https://bugs.openjdk.org/browse/JDK-8361869) |
| 8359181 | Error messages generated by configure --help after 8301197 | [JBS-8359181](https://bugs.openjdk.org/browse/JDK-8359181) |
| 8350386 | Test TestCodeCacheFull.java fails with option -XX:-UseCodeCacheFlushing | [JBS-8350386](https://bugs.openjdk.org/browse/JDK-8350386) |
| 8353235 | Test jdk/jfr/api/metadata/annotations/TestPeriod.java fails with IllegalArgumentException | [JBS-8353235](https://bugs.openjdk.org/browse/JDK-8353235) |

---

## 开发风格

SendaoYan 的贡献特点:

1. **测试专家**: 专注于测试稳定性和可靠性
2. **问题定位**: 快速定位测试失败根因
3. **渐进修复**: 小步快跑，每个 commit 聚焦单一问题
4. **跨平台**: 修复涉及 Linux、Docker、NUMA 等多种环境

---

## 相关链接

- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=SendaoYan)
- [JBS Issues](https://bugs.openjdk.org/issues/?jql=assignee%20%3D%20syan)