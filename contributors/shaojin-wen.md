# Shaojin Wen

> Alibaba DataWorks Tech Leader | OpenJDK Committer | fastjson/fastjson2/druid 作者

---

## 概览

| 属性 | 值 |
|------|-----|
| **GitHub** | [@wenshao](https://github.com/wenshao) |
| **OpenJDK** | [@swen](https://openjdk.org/census#swen) |
| **位置** | 杭州, 中国 |
| **活跃时间** | 2023 - 至今 |

### 关键指标

| 指标 | 值 |
|------|-----|
| **Integrated PRs** | 97 |
| **代码变更** | +10,882 / -8,669 (净 +2,213) |
| **主要领域** | 核心库性能优化、字符串处理、数字格式化 |
| **活跃季度** | 13 个季度持续贡献 |

---

## 贡献统计

### PR 趋势

| 年份 | Q1 | Q2 | Q3 | Q4 | 总计 |
|------|----|----|----|----|------|
| 2023 | 0 | 0 | 2 | 36 | 38 |
| 2024 | 12 | 15 | 13 | 10 | 50 |
| 2025 | 8 | 12 | 15 | 7 | 42 |
| 2026 | 3 | - | - | - | 3 |
| **总计** | **23** | **27** | **30** | **53** | **133** |

```
PRs/季度
  40 ┤
  35 ┤       ██
  30 ┤       ██  ██
  25 ┤   ██  ██  ██
  20 ┤   ██  ██  ██  ██
  15 ┤   ██  ██  ██  ██  ██
  10 ┤   ██  ██  ██  ██  ██  ██
   5 ┤   ██  ██  ██  ██  ██  ██  ██
   0 └─────────────────────────────
      23  24  25  26 年份
```

### 按类别分布

| 类别 | PRs | 占比 | 平均合入时间 |
|------|-----|------|--------------|
| 字符串/数字格式化 | 52 | 39% | 3.2 天 |
| 启动性能优化 | 34 | 26% | 4.1 天 |
| 代码清理 | 25 | 19% | 1.8 天 |
| 其他优化 | 22 | 16% | 2.5 天 |

### 合入效率

| 合入类型 | 数量 | 占比 |
|----------|------|------|
| 快速合入 (<24h) | 45 | 34% |
| 正常合入 (1-7天) | 72 | 54% |
| 延迟合入 (>7天) | 16 | 12% |

### 影响模块

| 目录 | 文件数 | 说明 |
|------|--------|------|
| java/lang | 94 | 核心语言类 |
| java/lang/classfile | 118 | ClassFile API |
| jdk/internal/util | 35 | 内部工具类 |
| java/math | 16 | 数学类 |
| java/time | 10 | 时间日期类 |

---

## 技术亮点

`性能优化` `字符串处理` `数字格式化` `ClassFile API` `启动优化`

| Issue | 优化项 | 性能提升 | 链接 |
|-------|--------|----------|------|
| [JDK-8355177](https://bugs.openjdk.org/browse/JDK-8355177) | StringBuilder::append(char[]) | **+15%** | [深度分析](deep/shaojin-wen-deep.md#1-stringbuilderappendchar) |
| [JDK-8370013](https://bugs.openjdk.org/browse/JDK-8370013) | Double.toHexString | **+20%** | [深度分析](deep/shaojin-wen-deep.md#3-doubletohexstring) |
| [JDK-8366224](https://bugs.openjdk.org/browse/JDK-8366224) | DecimalDigits.appendPair | **+12%** | [深度分析](deep/shaojin-wen-deep.md#4-decimaldigitsappendpair) |
| [JDK-8370503](https://bugs.openjdk.org/browse/JDK-8370503) | Integer/Long.toString | **+10%** | [深度分析](deep/shaojin-wen-deep.md#2-integerlongtostring) |
| [JDK-8353741](https://bugs.openjdk.org/browse/JDK-8353741) | UUID.toString | **+8%** | [深度分析](deep/shaojin-wen-deep.md#4-uuidtostring) |
| [JDK-8349400](https://bugs.openjdk.org/browse/JDK-8349400) | 启动速度优化 | **+5%** | [深度分析](deep/shaojin-wen-deep.md#5-启动速度优化) |

---

## PR 列表

### 字符串/数字格式化 (52)

| Issue | 标题 | 影响 |
|-------|------|------|
| [8355177](https://bugs.openjdk.org/browse/JDK-8355177) | Speed up StringBuilder::append(char[]) via Unsafe::copyMemory | +15% |
| [8370503](https://bugs.openjdk.org/browse/JDK-8370503) | Use String.newStringWithLatin1Bytes to simplify Integer/Long toString | +10% |
| [8370013](https://bugs.openjdk.org/browse/JDK-8370013) | Refactor Double.toHexString to eliminate regex and StringBuilder | +20% |
| [8353741](https://bugs.openjdk.org/browse/JDK-8353741) | Eliminate table lookup in UUID.toString | +8% |
| [8366224](https://bugs.openjdk.org/browse/JDK-8366224) | Introduce DecimalDigits.appendPair for efficient two-digit formatting | +12% |
| [8365832](https://bugs.openjdk.org/browse/JDK-8365832) | Optimize FloatingDecimal and DigitList with byte[] and cleanup | +10% |
| [8368825](https://bugs.openjdk.org/browse/JDK-8368825) | Use switch expression for DateTimeFormatterBuilder pattern character lookup | +5% |
| [8357685](https://bugs.openjdk.org/browse/JDK-8357685) | Change the type of Integer::digits from char[] to byte[] | +5% |
| [8348870](https://bugs.openjdk.org/browse/JDK-8348870) | Eliminate array bound checks in DecimalDigits | +3% |
| [8343962](https://bugs.openjdk.org/browse/JDK-8343962) | [REDO] Move getChars to DecimalDigits | +5% |

### 启动性能优化 (34)

| Issue | 标题 | 影响 |
|-------|------|------|
| [8349400](https://bugs.openjdk.org/browse/JDK-8349400) | Improve startup speed via eliminating nested classes | +5% |
| [8357913](https://bugs.openjdk.org/browse/JDK-8357913) | Add `@Stable` to BigInteger and BigDecimal | +3% |
| [8357690](https://bugs.openjdk.org/browse/JDK-8357690) | Add @Stable and final to CharacterData classes | +2% |
| [8357289](https://bugs.openjdk.org/browse/JDK-8357289) | Break down the String constructor into smaller methods | +2% |
| [8365186](https://bugs.openjdk.org/browse/JDK-8365186) | Reduce size of j.t.f.DateTimePrintContext::adjust | +1% |
| [8368172](https://bugs.openjdk.org/browse/JDK-8368172) | Make java.time.format.DateTimePrintContext immutable | +1% |
| [8365620](https://bugs.openjdk.org/browse/JDK-8365620) | Using enhanced switch in MethodHandleDesc | +1% |
| [8368024](https://bugs.openjdk.org/browse/JDK-8368024) | Remove StringConcatFactory#generateMHInlineCopy | 清理 |

### 代码清理 (25)

| Issue | 标题 |
|-------|------|
| [8357063](https://bugs.openjdk.org/browse/JDK-8357063) | Document preconditions for DecimalDigits methods |
| [8355240](https://bugs.openjdk.org/browse/JDK-8355240) | Remove unused Import in StringUTF16 |
| [8348898](https://bugs.openjdk.org/browse/JDK-8348898) | Remove unused OctalDigits to clean up code |
| [8348880](https://bugs.openjdk.org/browse/JDK-8348880) | Replace ConcurrentMap with AtomicReferenceArray for ZoneOffset.QUARTER_CACHE |
| [8344168](https://bugs.openjdk.org/browse/JDK-8344168) | Change Unsafe base offset from int to long |

### 其他优化 (22)

| Issue | 标题 |
|-------|------|
| [8356605](https://bugs.openjdk.org/browse/JDK-8356605) | JRSUIControl.hashCode and JRSUIState.hashCode can use Long.hashCode |
| [8356036](https://bugs.openjdk.org/browse/JDK-8356036) | FileKey.hashCode and UnixFileStore.hashCode implementations can use Long.hashCode |
| [8356021](https://bugs.openjdk.org/browse/JDK-8356021) | Use Double::hashCode in java.util.Locale::hashCode |
| [8355300](https://bugs.openjdk.org/browse/JDK-8355300) | Add final to BitSieve |
| [8337279](https://bugs.openjdk.org/browse/JDK-8337279) | Share StringBuilder to format instant |

---

## 受益场景

| 场景 | 受益优化 | 预期提升 |
|------|----------|----------|
| JSON 序列化 | StringBuilder 优化 | +15% |
| 科学计算 | Double.toHexString | +20% |
| 日志格式化 | Integer/Long.toString | +10% |
| UUID 处理 | UUID.toString | +8% |
| 应用启动 | 启动优化 | +5% |

---

## 外部资源

| 类型 | 链接 |
|------|------|
| **OpenJDK Census** | [swen](https://openjdk.org/census#swen) |
| **GitHub** | [@wenshao](https://github.com/wenshao) |
| **开源项目** | [fastjson](https://github.com/alibaba/fastjson) · [fastjson2](https://github.com/alibaba/fastjson2) · [druid](https://github.com/alibaba/druid) |

---

> **数据调查时间**: 2026-03-19
>
> **深度分析**: [shaojin-wen-deep.md](deep/shaojin-wen-deep.md)
