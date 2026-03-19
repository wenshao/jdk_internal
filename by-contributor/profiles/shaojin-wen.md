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
| **Integrated PRs** | 97+ |
| **代码变更** | +10,882 / -8,669 (净 +2,213) |
| **主要领域** | 核心库性能优化、字符串处理、ClassFile API |
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
| 字符串/数字格式化 | 52 | 25% | 3.2 天 |
| ClassFile API 优化 | 35 | 17% | 2.1 天 |
| 启动性能优化 | 34 | 16% | 4.1 天 |
| StringConcatFactory | 10 | 5% | 3.5 天 |
| 代码清理 | 25 | 12% | 1.8 天 |
| Formatter/HexFormat | 8 | 4% | 2.3 天 |
| 其他字符串/数据流 | 15 | 7% | 2.0 天 |
| 其他优化 | 22 | 11% | 2.5 天 |
| **总计** | **201** | **100%** | - |

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
| [8355177](https://bugs.openjdk.org/browse/JDK-8355177) | Speed up StringBuilder::append(char[]) via Unsafe::copyMemory | +15% [🔗](../../by-pr/8355/8355177.md) |
| [8370503](https://bugs.openjdk.org/browse/JDK-8370503) | Use String.newStringWithLatin1Bytes to simplify Integer/Long toString | +10% [🔗](../../by-pr/8370/8370503.md) |
| [8370013](https://bugs.openjdk.org/browse/JDK-8370013) | Refactor Double.toHexString to eliminate regex and StringBuilder | +20% [🔗](../../by-pr/8370/8370013.md) |
| [8353741](https://bugs.openjdk.org/browse/JDK-8353741) | Eliminate table lookup in UUID.toString | +8% [🔗](../../by-pr/8355/8353741.md) |
| [8366224](https://bugs.openjdk.org/browse/JDK-8366224) | Introduce DecimalDigits.appendPair for efficient two-digit formatting | +12% [🔗](../../by-pr/8366/8366224.md) |
| [8365832](https://bugs.openjdk.org/browse/JDK-8365832) | Optimize FloatingDecimal and DigitList with byte[] and cleanup | +10% [🔗](../../by-pr/8366/8365832.md) |
| [8368825](https://bugs.openjdk.org/browse/JDK-8368825) | Use switch expression for DateTimeFormatterBuilder pattern character lookup | +5% [🔗](../../by-pr/8368/8368825.md) |
| [8357685](https://bugs.openjdk.org/browse/JDK-8357685) | Change the type of Integer::digits from char[] to byte[] | +5% [🔗](../../by-pr/8355/8357685.md) |
| [8348870](https://bugs.openjdk.org/browse/JDK-8348870) | Eliminate array bound checks in DecimalDigits | +3% [🔗](../../by-pr/8348/8348870.md) |
| [8343962](https://bugs.openjdk.org/browse/JDK-8343962) | [REDO] Move getChars to DecimalDigits | +5% [🔗](../../by-pr/8349/8343962.md) |

### 启动性能优化 (34)

| Issue | 标题 | 影响 |
|-------|------|------|
| [8336856](https://bugs.openjdk.org/browse/JDK-8336856) | Efficient hidden class-based string concatenation strategy | 启动+ warmup [🔗](../../by-pr/8336/8336856.md) |
| [8349400](https://bugs.openjdk.org/browse/JDK-8349400) | Improve startup speed via eliminating nested classes | +5% [🔗](../../by-pr/8349/8349400.md) |
| [8357913](https://bugs.openjdk.org/browse/JDK-8357913) | Add `@Stable` to BigInteger and BigDecimal | +3% [🔗](../../by-pr/8355/8357913.md) |
| [8357690](https://bugs.openjdk.org/browse/JDK-8357690) | Add @Stable and final to CharacterData classes | +2% [🔗](../../by-pr/8355/8357690.md) |
| [8357289](https://bugs.openjdk.org/browse/JDK-8357289) | Break down the String constructor into smaller methods | +2% [🔗](../../by-pr/8355/8357289.md) |
| [8365186](https://bugs.openjdk.org/browse/JDK-8365186) | Reduce size of j.t.f.DateTimePrintContext::adjust | +1% [🔗](../../by-pr/8365/8365186.md) |
| [8368172](https://bugs.openjdk.org/browse/JDK-8368172) | Make java.time.format.DateTimePrintContext immutable | +1% [🔗](../../by-pr/8368/8368172.md) |
| [8365620](https://bugs.openjdk.org/browse/JDK-8365620) | Using enhanced switch in MethodHandleDesc | +1% [🔗](../../by-pr/8365/8365620.md) |
| [8368024](https://bugs.openjdk.org/browse/JDK-8368024) | Remove StringConcatFactory#generateMHInlineCopy | 清理 [🔗](../../by-pr/8368/8368024.md) |

### 代码清理 (30+)

| Issue | 标题 | 链接 |
|-------|------|------|
| [8357063](https://bugs.openjdk.org/browse/JDK-8357063) | Document preconditions for DecimalDigits methods | [🔗](../../by-pr/8355/8357063.md) |
| [8355240](https://bugs.openjdk.org/browse/JDK-8355240) | Remove unused Import in StringUTF16 | [🔗](../../by-pr/8355/8355240.md) |
| [8348898](https://bugs.openjdk.org/browse/JDK-8348898) | Remove unused OctalDigits to clean up code | [🔗](../../by-pr/8348/8348898.md) |
| [8348880](https://bugs.openjdk.org/browse/JDK-8348880) | Replace ConcurrentMap with AtomicReferenceArray for ZoneOffset.QUARTER_CACHE | [🔗](../../by-pr/8348/8348880.md) |
| [8344168](https://bugs.openjdk.org/browse/JDK-8344168) | Change Unsafe base offset from int to long | [🔗](../../by-pr/8344/8344168.md) |

### 其他优化 (25+)

| Issue | 标题 | 链接 |
|-------|------|------|
| [8356605](https://bugs.openjdk.org/browse/JDK-8356605) | JRSUIControl.hashCode and JRSUIState.hashCode can use Long.hashCode | [🔗](../../by-pr/8355/8356605.md) |
| [8356036](https://bugs.openjdk.org/browse/JDK-8356036) | FileKey.hashCode and UnixFileStore.hashCode implementations can use Long.hashCode | [🔗](../../by-pr/8355/8356036.md) |
| [8356021](https://bugs.openjdk.org/browse/JDK-8356021) | Use Double::hashCode in java.util.Locale::hashCode | [🔗](../../by-pr/8355/8356021.md) |
| [8355300](https://bugs.openjdk.org/browse/JDK-8355300) | Add final to BitSieve | [🔗](../../by-pr/8355/8355300.md) |
| [8337279](https://bugs.openjdk.org/browse/JDK-8337279) | Share StringBuilder to format instant | [🔗](../../by-pr/8337/8337279.md) |

### ClassFile API 优化 (35)

| Issue | 标题 | 链接 |
|-------|------|------|
| [8342336](https://bugs.openjdk.org/browse/JDK-8342336) | Optimize ClassFile imports | [🔗](../../by-pr/8342/8342336.md) |
| [8341900](https://bugs.openjdk.org/browse/JDK-8341900) | Optimize DirectCodeBuilder writeBody | [🔗](../../by-pr/8341/8341900.md) |
| [8341906](https://bugs.openjdk.org/browse/JDK-8341906) | Optimize ClassFile writing BufBuffer | [🔗](../../by-pr/8341/8341906.md) |
| [8341859](https://bugs.openjdk.org/browse/JDK-8341859) | Optimize ClassFile Benchmark Write | [🔗](../../by-pr/8341/8341859.md) |
| [8341755](https://bugs.openjdk.org/browse/JDK-8341755) | Optimize argNames in InnerClassLambdaMetafactory | [🔗](../../by-pr/8341/8341755.md) |
| [8341664](https://bugs.openjdk.org/browse/JDK-8341664) | ReferenceClassDescImpl cache internalName | [🔗](../../by-pr/8341/8341664.md) |
| [8341581](https://bugs.openjdk.org/browse/JDK-8341581) | Optimize BytecodeHelpers validate slot | [🔗](../../by-pr/8341/8341581.md) |
| [8341548](https://bugs.openjdk.org/browse/JDK-8341548) | More concise use of classfile API | [🔗](../../by-pr/8341/8341548.md) |
| [8341510](https://bugs.openjdk.org/browse/JDK-8341510) | Optimize StackMapGenerator::processFieldInstructions | [🔗](../../by-pr/8341/8341510.md) |
| [8341512](https://bugs.openjdk.org/browse/JDK-8341512) | Optimize StackMapGenerator::processInvokeInstructions | [🔗](../../by-pr/8341/8341512.md) |
| [8341415](https://bugs.openjdk.org/browse/JDK-8341415) | Optimize RawBytecodeHelper::next | [🔗](../../by-pr/8341/8341415.md) |
| [8341199](https://bugs.openjdk.org/browse/JDK-8341199) | Use ClassFile's new API loadConstant(int) | [🔗](../../by-pr/8341/8341199.md) |
| [8341141](https://bugs.openjdk.org/browse/JDK-8341141) | Optimize DirectCodeBuilder | [🔗](../../by-pr/8341/8341141.md) |
| [8341136](https://bugs.openjdk.org/browse/JDK-8341136) | Optimize StackMapGenerator::trimAndCompress | [🔗](../../by-pr/8341/8341136.md) |
| [8341006](https://bugs.openjdk.org/browse/JDK-8341006) | Optimize StackMapGenerator detect frames | [🔗](../../by-pr/8341/8341006.md) |
| [8340708](https://bugs.openjdk.org/browse/JDK-8340708) | Optimize StackMapGenerator::processMethod | [🔗](../../by-pr/8340/8340708.md) |
| [8340587](https://bugs.openjdk.org/browse/JDK-8340587) | Optimize StackMapGenerator$Frame::checkAssignableTo | [🔗](../../by-pr/8340/8340587.md) |
| [8340710](https://bugs.openjdk.org/browse/JDK-8340710) | Optimize DirectClassBuilder::build | [🔗](../../by-pr/8340/8340710.md) |
| [8340544](https://bugs.openjdk.org/browse/JDK-8340544) | Optimize setLocalsFromArg | [🔗](../../by-pr/8340/8340544.md) |
| [8339401](https://bugs.openjdk.org/browse/JDK-8339401) | Optimize ClassFile load and store instructions | [🔗](../../by-pr/8339/8339401.md) |
| [8339317](https://bugs.openjdk.org/browse/JDK-8339317) | Optimize ClassFile writeBuffer | [🔗](../../by-pr/8339/8339317.md) |
| [8339290](https://bugs.openjdk.org/browse/JDK-8339290) | Optimize ClassFile Utf8EntryImpl#writeTo | [🔗](../../by-pr/8339/8339290.md) |
| [8339320](https://bugs.openjdk.org/browse/JDK-8339320) | Optimize ClassFile Utf8EntryImpl#inflate | [🔗](../../by-pr/8339/8339320.md) |
| [8339217](https://bugs.openjdk.org/browse/JDK-8339217) | Optimize ClassFile API loadConstant | [🔗](../../by-pr/8339/8339217.md) |
| [8339205](https://bugs.openjdk.org/browse/JDK-8339205) | Optimize StackMapGenerator | [🔗](../../by-pr/8339/8339205.md) |
| [8339196](https://bugs.openjdk.org/browse/JDK-8339196) | Optimize BufWriterImpl#writeU1/U2/Int/Long | [🔗](../../by-pr/8339/8339196.md) |
| [8339168](https://bugs.openjdk.org/browse/JDK-8339168) | Optimize ClassFile Util slotSize | [🔗](../../by-pr/8339/8339168.md) |
| [8338532](https://bugs.openjdk.org/browse/JDK-8338532) | Speed up the ClassFile API MethodTypeDesc#ofDescriptor | [🔗](../../by-pr/8338/8338532.md) |
| [8338409](https://bugs.openjdk.org/browse/JDK-8338409) | Use record to simplify code | [🔗](../../by-pr/8338/8338409.md) |
| [8338937](https://bugs.openjdk.org/browse/JDK-8338937) | Optimize the string concatenation of ClassDesc | [🔗](../../by-pr/8338/8338937.md) |
| [8338936](https://bugs.openjdk.org/browse/JDK-8338936) | StringConcatFactory optimize construction of MethodType and MethodTypeDesc | [🔗](../../by-pr/8338/8338936.md) |
| [8343500](https://bugs.openjdk.org/browse/JDK-8343500) | Optimize ArrayClassDescImpl computeDescriptor | [🔗](../../by-pr/8343/8343500.md) |

### StringConcatFactory 优化 (10)

| Issue | 标题 | 链接 |
|-------|------|------|
| [8339635](https://bugs.openjdk.org/browse/JDK-8339635) | StringConcatFactory optimization for CompactStrings off | [🔗](../../by-pr/8339/8339635.md) |
| [8338930](https://bugs.openjdk.org/browse/JDK-8338930) | StringConcatFactory hardCoded string concatenation strategy | [🔗](../../by-pr/8338/8338930.md) |
| [8336831](https://bugs.openjdk.org/browse/JDK-8336831) | Optimize StringConcatHelper.simpleConcat | [🔗](../../by-pr/8336/8336831.md) |
| [8337245](https://bugs.openjdk.org/browse/JDK-8337245) | Fix wrong comment of StringConcatHelper | [🔗](../../by-pr/8337/8337245.md) |
| [8337167](https://bugs.openjdk.org/browse/JDK-8337167) | StringSize deduplication | [🔗](../../by-pr/8337/8337167.md) |
| [8336792](https://bugs.openjdk.org/browse/JDK-8336792) | DateTimeFormatterBuilder append zeros based on StringBuilder.repeat | [🔗](../../by-pr/8336/8336792.md) |
| [8336741](https://bugs.openjdk.org/browse/JDK-8336741) | Optimize LocalTime.toString with StringBuilder.repeat | [🔗](../../by-pr/8336/8336741.md) |
| [8336706](https://bugs.openjdk.org/browse/JDK-8336706) | Optimize LocalDate.toString with StringBuilder.repeat | [🔗](../../by-pr/8336/8336706.md) |
| [8336278](https://bugs.openjdk.org/browse/JDK-8336278) | Micro-optimize Replace String.format("%n") to System.lineSeparator | [🔗](../../by-pr/8336/8336278.md) |
| [8333893](https://bugs.openjdk.org/browse/JDK-8333893) | Optimization for StringBuilder append boolean & null | [🔗](../../by-pr/8333/8333893.md) |

### Formatter/HexFormat 优化 (8)

| Issue | 标题 | 链接 |
|-------|------|------|
| [8335802](https://bugs.openjdk.org/browse/JDK-8335802) | Improve startup speed HexFormat uses boolean instead of enum | [🔗](../../by-pr/8335/8335802.md) |
| [8335645](https://bugs.openjdk.org/browse/JDK-8335645) | j.u.Formatter#trailingZeros improved with String repeat | [🔗](../../by-pr/8335/8335645.md) |
| [8335252](https://bugs.openjdk.org/browse/JDK-8335252) | Reduce size of j.u.Formatter.Conversion#isValid | [🔗](../../by-pr/8335/8335252.md) |
| [8334328](https://bugs.openjdk.org/browse/JDK-8334328) | Reduce object allocation for FloatToDecimal and DoubleToDecimal | [🔗](../../by-pr/8334/8334328.md) |
| [8337832](https://bugs.openjdk.org/browse/JDK-8337832) | Optimize datetime toString | [🔗](../../by-pr/8337/8337832.md) |
| [8337168](https://bugs.openjdk.org/browse/JDK-8337168) | Optimize LocalDateTime.toString | [🔗](../../by-pr/8337/8337168.md) |
| [8316704](https://bugs.openjdk.org/browse/JDK-8316704) | Regex-free parsing of Formatter and FormatProcessor specifiers | [🔗](../../by-pr/8316/8316704.md) |
| [8316426](https://bugs.openjdk.org/browse/JDK-8316426) | Optimization for HexFormat.formatHex | [🔗](../../by-pr/8316/8316426.md) |

### 其他字符串/数据流优化 (15)

| Issue | 标题 | 链接 |
|-------|------|------|
| [8343650](https://bugs.openjdk.org/browse/JDK-8343650) | Reuse StringLatin1::putCharsAt and StringUTF16::putCharsAt | [🔗](../../by-pr/8343/8343650.md) |
| [8340232](https://bugs.openjdk.org/browse/JDK-8340232) | Optimize DataInputStream::readUTF | [🔗](../../by-pr/8340/8340232.md) |
| [8339699](https://bugs.openjdk.org/browse/JDK-8339699) | Optimize DataOutputStream writeUTF | [🔗](../../by-pr/8339/8339699.md) |
| [8337279](https://bugs.openjdk.org/browse/JDK-8337279) | Share StringBuilder to format instant | [🔗](../../by-pr/8337/8337279.md) |
| [8333833](https://bugs.openjdk.org/browse/JDK-8333833) | Remove the use of ByteArrayLittleEndian from UUID::toString | [🔗](../../by-pr/8333/8333833.md) |
| [8317742](https://bugs.openjdk.org/browse/JDK-8317742) | ISO Standard Date Format consistency on DateTimeFormatter and String.format | [🔗](../../by-pr/8317/8317742.md) |
| [8315968](https://bugs.openjdk.org/browse/JDK-8315968) | Move java.util.Digits to jdk.internal.util and refactor | [🔗](../../by-pr/8315/8315968.md) |
| [8311207](https://bugs.openjdk.org/browse/JDK-8311207) | Cleanup for Optimization for UUID.toString | [🔗](../../by-pr/8311/8311207.md) |
| [8310929](https://bugs.openjdk.org/browse/JDK-8310929) | Optimization for Integer.toString | [🔗](../../by-pr/8311/8310929.md) |
| [8310502](https://bugs.openjdk.org/browse/JDK-8310502) | Optimization for j.l.Long.fastUUID | [🔗](../../by-pr/8311/8310502.md) |
| [8343629](https://bugs.openjdk.org/browse/JDK-8343629) | More MergeStore benchmark | [🔗](../../by-pr/8343/8343629.md) |
| [8334342](https://bugs.openjdk.org/browse/JDK-8334342) | Add MergeStore JMH benchmarks | [🔗](../../by-pr/8334/8334342.md) |
| [8343984](https://bugs.openjdk.org/browse/JDK-8343984) | Fix Unsafe address overflow | [🔗](../../by-pr/8349/8343984.md) |
| [8343925](https://bugs.openjdk.org/browse/JDK-8343925) | [BACKOUT] JDK-8342650 Move getChars to DecimalDigits | [🔗](../../by-pr/8349/8343925.md) |
| [8315970](https://bugs.openjdk.org/browse/JDK-8315970) | Big-endian issues after JDK-8310929 | [🔗](../../by-pr/8315/8315970.md) |

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
