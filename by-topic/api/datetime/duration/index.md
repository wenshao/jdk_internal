# Duration 源码分析

> java.time.Duration 的完整实现分析

---
## 目录

1. [类声明](#1-类声明)
2. [字段存储](#2-字段存储)
3. [常量定义](#3-常量定义)
4. [工厂方法](#4-工厂方法)
5. [核心方法](#5-核心方法)
6. [时间计算](#6-时间计算)
7. [转换方法](#7-转换方法)
8. [部分提取 (JDK 9+)](#8-部分提取-jdk-9)
9. [截断操作](#9-截断操作)
10. [TemporalAmount 实现](#10-temporalamount-实现)
11. [比较](#11-比较)
12. [序列化机制](#12-序列化机制)
13. [toString() - ISO-8601 输出](#13-tostring---iso-8601-输出)
14. [性能特性](#14-性能特性)
15. [使用示例](#15-使用示例)
16. [与 Period 对比](#16-与-period-对比)
17. [相关文档](#17-相关文档)

---


## 1. 类声明

```java
@jdk.internal.ValueBased
public final class Duration
    implements TemporalAmount, Comparable<Duration>, Serializable {
```

**关键设计决策**:
- `final` - 不可继承
- `@jdk.internal.ValueBased` - 基于值的类
- `implements TemporalAmount` - 支持时间量的通用接口
- `Comparable<Duration>` - 可比较排序
- `Serializable` - 支持序列化

**与 Period 的区别**:
- `Duration` - 基于时间的量（秒、纳秒），适用于计时、延迟
- `Period` - 基于日期的量（年、月、日），适用于日历计算

---

## 2. 字段存储

### 两字段组合

```java
/**
 * @serial The number of seconds in the duration.
 */
private final long seconds;

/**
 * @serial The number of nanoseconds in the duration, expressed as a fraction of the
 * number of seconds. This is always positive, and never exceeds 999,999,999.
 */
private final int nanos;
```

**内存布局**:
- `long seconds` - 8 字节，总秒数
- `int nanos` - 4 字节，纳秒调整 (0 到 999,999,999)

**为什么需要两个字段？**

| 字段 | 作用 | 范围 |
|------|------|------|
| `seconds` | 整秒部分 | -2^63 到 2^63-1 |
| `nanos` | 纳秒调整 | 0 到 999,999,999 |

**设计优势**:
1. 单一 `long` 不足以存储纳秒精度（最大约 292 年）
2. `long + int` 组合可存储约 ±5.8 亿年
3. 纳秒部分始终为正，简化计算逻辑

**负数表示**:
- 负号由 `seconds` 的符号表示
- 例如: -1.5 秒 = `seconds = -2`, `nanos = 500,000,000`

---

## 3. 常量定义

### 预定义常量

```java
/**
 * Constant for a duration of zero.
 */
public static final Duration ZERO = new Duration(0, 0);

/**
 * The minimum supported {@code Duration}, which is {@link Long#MIN_VALUE}
 * seconds.
 * @since 26
 */
public static final Duration MIN = new Duration(Long.MIN_VALUE, 0);

/**
 * The maximum supported {@code Duration}, which is {@link Long#MAX_VALUE}
 * seconds and {@code 999,999,999} nanoseconds.
 * @since 26
 */
public static final Duration MAX = new Duration(Long.MAX_VALUE, 999_999_999);
```

**范围说明**:
- `MIN`: 约 -292 亿年（-2^63 秒）
- `MAX`: 约 +292 亿年（2^63-1 秒 + 999,999,999 纳秒）
- 远超宇宙年龄（约 138 亿年）

---

## 4. 工厂方法

### ofDays() / ofHours() / ofMinutes() / ofSeconds()

```java
public static Duration ofDays(long days) {
    return create(Math.multiplyExact(days, SECONDS_PER_DAY), 0);
}

public static Duration ofHours(long hours) {
    return create(Math.multiplyExact(hours, SECONDS_PER_HOUR), 0);
}

public static Duration ofMinutes(long minutes) {
    return create(Math.multiplyExact(minutes, SECONDS_PER_MINUTE), 0);
}

public static Duration ofSeconds(long seconds) {
    return create(seconds, 0);
}

public static Duration ofSeconds(long seconds, long nanoAdjustment) {
    long secs = Math.addExact(seconds, Math.floorDiv(nanoAdjustment, NANOS_PER_SECOND));
    int nos = (int) Math.floorMod(nanoAdjustment, NANOS_PER_SECOND);
    return create(secs, nos);
}
```

**转换系数**:
- 1 天 = 86,400 秒 (24 × 60 × 60)
- 1 小时 = 3,600 秒 (60 × 60)
- 1 分钟 = 60 秒
- 1 秒 = 1,000,000,000 纳秒

**溢出保护**: 使用 `Math.multiplyExact()` 防止溢出

### ofMillis() / ofNanos()

```java
public static Duration ofMillis(long millis) {
    long secs = millis / 1000;
    int mos = (int) (millis % 1000);
    if (mos < 0) {
        mos += 1000;
        secs--;
    }
    return create(secs, mos * 1000_000);
}

public static Duration ofNanos(long nanos) {
    long secs = nanos / NANOS_PER_SECOND;
    int nos = (int) (nanos % NANOS_PER_SECOND);
    if (nos < 0) {
        nos += (int) NANOS_PER_SECOND;
        secs--;
    }
    return create(secs, nos);
}
```

**负数处理**: 负数取模时需要调整，确保 `nanos` 始终为正

### parse() - ISO-8601 格式解析

```java
public static Duration parse(CharSequence text) {
    Objects.requireNonNull(text, "text");
    Matcher matcher = Lazy.PATTERN.matcher(text);
    if (matcher.matches()) {
        if (!charMatch(text, matcher.start(3), matcher.end(3), 'T')) {
            boolean negate = charMatch(text, matcher.start(1), matcher.end(1), '-');
            long daysAsSecs = parseNumber(text, dayStart, dayEnd, SECONDS_PER_DAY, "days");
            long hoursAsSecs = parseNumber(text, hourStart, hourEnd, SECONDS_PER_HOUR, "hours");
            long minsAsSecs = parseNumber(text, minuteStart, minuteEnd, SECONDS_PER_MINUTE, "minutes");
            long seconds = parseNumber(text, secondStart, secondEnd, 1, "seconds");
            boolean negativeSecs = secondStart >= 0 && text.charAt(secondStart) == '-';
            int nanos = parseFraction(text, fractionStart, fractionEnd, negativeSecs ? -1 : 1);
            try {
                return create(negate, daysAsSecs, hoursAsSecs, minsAsSecs, seconds, nanos);
            } catch (ArithmeticException ex) {
                throw new DateTimeParseException("Text cannot be parsed to a Duration: overflow", text, 0, ex);
            }
        }
    }
    throw new DateTimeParseException("Text cannot be parsed to a Duration", text, 0);
}
```

**正则表达式**:
```regex
([-+]?)P(?:([-+]?[0-9]+)D)?(T(?:([-+]?[0-9]+)H)?(?:([-+]?[0-9]+)M)?(?:([-+]?[0-9]+)(?:[.,]([0-9]{0,9}))?S)?)?
```

**支持的格式**:

| 格式 | 示例 | 说明 |
|------|------|------|
| `PT20.345S` | 20.345 秒 | 带小数秒 |
| `PT15M` | 15 分钟 | 900 秒 |
| `PT10H` | 10 小时 | 36,000 秒 |
| `P2D` | 2 天 | 172,800 秒 |
| `P2DT3H4M` | 2 天 3 小时 4 分钟 | 组合 |
| `PT-6H3M` | -6 小时 +3 分钟 | 各部分独立符号 |
| `-PT6H3M` | -(6 小时 + 3 分钟) | 整体负号 |

**扩展特性** (非标准 ISO-8601):
- 各部分可独立带符号: `PT-6H+3M`
- 整体负号: `-PT6H3M`
- 组合负号: `-PT-6H+3M` = +6小时-3分钟

### between() - 计算时间差

```java
public static Duration between(Temporal startInclusive, Temporal endExclusive) {
    long secs = startInclusive.until(endExclusive, SECONDS);
    if (secs == 0) {
        return ofNanos(startInclusive.until(endExclusive, NANOS));
    }
    long nanos;
    try {
        nanos = endExclusive.getLong(NANO_OF_SECOND) - startInclusive.getLong(NANO_OF_SECOND);
    } catch (DateTimeException ex2) {
        nanos = 0;
    }
    if (nanos < 0 && secs > 0) {
        secs++;
    } else if (nanos > 0 && secs < 0) {
        secs--;
    }
    return ofSeconds(secs, nanos);
}
```

**使用场景**:
```java
Duration d = Duration.between(LocalTime.NOON, LocalTime.MIDNIGHT);  // PT12H
Duration d = Duration.between(Instant.now().minusSeconds(60), Instant.now());  // PT1M
```

---

## 5. 核心方法

### get() / getUnits()

```java
@Override
public long get(TemporalUnit unit) {
    if (unit == SECONDS) {
        return seconds;
    } else if (unit == NANOS) {
        return nanos;
    } else {
        throw new UnsupportedTemporalTypeException("Unsupported unit: " + unit);
    }
}

@Override
public List<TemporalUnit> getUnits() {
    return DurationUnits.UNITS;
}
```

**支持的单位**: 仅 `SECONDS` 和 `NANOS`

### 判断方法

```java
public boolean isPositive() {
    return (seconds | nanos) > 0;
}

public boolean isZero() {
    return (seconds | nanos) == 0;
}

public boolean isNegative() {
    return seconds < 0;
}
```

**位运算优化**: 使用 `|` 而非 `+` 避免溢出

### 访问方法

```java
public long getSeconds() {
    return seconds;
}

public int getNano() {
    return nanos;
}
```

---

## 6. 时间计算

### plus() - 加法

```java
public Duration plus(long amountToAdd, TemporalUnit unit) {
    Objects.requireNonNull(unit, "unit");
    if (unit == DAYS) {
        return plus(Math.multiplyExact(amountToAdd, SECONDS_PER_DAY), 0);
    }
    if (unit.isDurationEstimated()) {
        throw new UnsupportedTemporalTypeException("Unit must not have an estimated duration");
    }
    if (amountToAdd == 0) {
        return this;
    }
    if (unit instanceof ChronoUnit chronoUnit) {
        return switch (chronoUnit) {
            case NANOS -> plusNanos(amountToAdd);
            case MICROS -> plusSeconds((amountToAdd / (1000_000L * 1000)) * 1000)
                           .plusNanos((amountToAdd % (1000_000L * 1000)) * 1000);
            case MILLIS -> plusMillis(amountToAdd);
            case SECONDS -> plusSeconds(amountToAdd);
            default -> plusSeconds(Math.multiplyExact(unit.getDuration().seconds, amountToAdd));
        };
    }
    Duration duration = unit.getDuration().multipliedBy(amountToAdd);
    return plusSeconds(duration.getSeconds()).plusNanos(duration.getNano());
}

private Duration plus(long secondsToAdd, long nanosToAdd) {
    if ((secondsToAdd | nanosToAdd) == 0) {
        return this;
    }
    long epochSec = Math.addExact(seconds, secondsToAdd);
    epochSec = Math.addExact(epochSec, nanosToAdd / NANOS_PER_SECOND);
    nanosToAdd = nanosToAdd % NANOS_PER_SECOND;
    long nanoAdjustment = nanos + nanosToAdd;
    return ofSeconds(epochSec, nanoAdjustment);
}
```

### minus() - 减法

```java
public Duration minus(long amountToSubtract, TemporalUnit unit) {
    return (amountToSubtract == Long.MIN_VALUE
        ? plus(Long.MAX_VALUE, unit).plus(1, unit)
        : plus(-amountToSubtract, unit));
}
```

**Long.MIN_VALUE 处理**: 避免直接取反溢出

### multipliedBy() / dividedBy()

```java
public Duration multipliedBy(long multiplicand) {
    if (multiplicand == 0) {
        return ZERO;
    }
    if (multiplicand == 1) {
        return this;
    }
    return create(toBigDecimalSeconds().multiply(BigDecimal.valueOf(multiplicand)));
}

public Duration dividedBy(long divisor) {
    if (divisor == 0) {
        throw new ArithmeticException("Cannot divide by zero");
    }
    if (divisor == 1) {
        return this;
    }
    return create(toBigDecimalSeconds().divide(BigDecimal.valueOf(divisor), RoundingMode.DOWN));
}

public long dividedBy(Duration divisor) {
    Objects.requireNonNull(divisor, "divisor");
    BigDecimal dividendBigD = toBigDecimalSeconds();
    BigDecimal divisorBigD = divisor.toBigDecimalSeconds();
    return dividendBigD.divideToIntegralValue(divisorBigD).longValueExact();
}
```

**BigDecimal 使用**: 避免精度损失

### negated() / abs()

```java
public Duration negated() {
    return multipliedBy(-1);
}

public Duration abs() {
    return isNegative() ? negated() : this;
}
```

---

## 7. 转换方法

### toDays() / toHours() / toMinutes() / toSeconds()

```java
public long toDays() {
    return seconds / SECONDS_PER_DAY;
}

public long toHours() {
    return seconds / SECONDS_PER_HOUR;
}

public long toMinutes() {
    return seconds / SECONDS_PER_MINUTE;
}

public long toSeconds() {
    return seconds;
}
```

**注意**: 纳秒部分被忽略

### toMillis() / toNanos()

```java
public long toMillis() {
    long tempSeconds = seconds;
    long tempNanos = nanos;
    if (tempSeconds < 0) {
        // 处理 Long.MIN_VALUE 情况
        tempSeconds = tempSeconds + 1;
        tempNanos = tempNanos - NANOS_PER_SECOND;
    }
    long millis = Math.multiplyExact(tempSeconds, 1000);
    millis = Math.addExact(millis, tempNanos / NANOS_PER_MILLI);
    return millis;
}

public long toNanos() {
    long tempSeconds = seconds;
    long tempNanos = nanos;
    if (tempSeconds < 0) {
        // 处理 Long.MIN_VALUE 情况
        tempSeconds = tempSeconds + 1;
        tempNanos = tempNanos - NANOS_PER_SECOND;
    }
    long totalNanos = Math.multiplyExact(tempSeconds, NANOS_PER_SECOND);
    totalNanos = Math.addExact(totalNanos, tempNanos);
    return totalNanos;
}
```

**Long.MIN_VALUE 特殊处理**: 避免 `-MIN_VALUE` 溢出

---

## 8. 部分提取 (JDK 9+)

### to*Part() 方法

```java
public long toDaysPart() {
    return seconds / SECONDS_PER_DAY;
}

public int toHoursPart() {
    return (int) (toHours() % 24);
}

public int toMinutesPart() {
    return (int) (toMinutes() % MINUTES_PER_HOUR);
}

public int toSecondsPart() {
    return (int) (seconds % SECONDS_PER_MINUTE);
}

public int toMillisPart() {
    return nanos / 1000_000;
}

public int toNanosPart() {
    return nanos;
}
```

**使用场景**: 格式化显示

```java
Duration d = Duration.ofHours(26).plusMinutes(15).plusSeconds(30);
// toDaysPart() = 1
// toHoursPart() = 2
// toMinutesPart() = 15
// toSecondsPart() = 30
// 格式化: "1d 2h 15m 30s"
```

---

## 9. 截断操作

### truncatedTo()

```java
public Duration truncatedTo(TemporalUnit unit) {
    Objects.requireNonNull(unit, "unit");
    if (unit == ChronoUnit.SECONDS && (seconds >= 0 || nanos == 0)) {
        return new Duration(seconds, 0);
    } else if (unit == ChronoUnit.NANOS) {
        return this;
    }
    Duration unitDur = unit.getDuration();
    if (unitDur.getSeconds() > LocalTime.SECONDS_PER_DAY) {
        throw new UnsupportedTemporalTypeException("Unit is too large to be used for truncation");
    }
    long dur = unitDur.toNanos();
    if ((LocalTime.NANOS_PER_DAY % dur) != 0 {
        throw new UnsupportedTemporalTypeException("Unit must divide into a standard day without remainder");
    }
    long nod = (seconds % LocalTime.SECONDS_PER_DAY) * LocalTime.NANOS_PER_SECOND + nanos;
    long result = (nod / dur) * dur;
    return plusNanos(result - nod);
}
```

**支持的单位**: NANOS, MICROS, MILLIS, SECONDS, MINUTES, HOURS, DAYS

**使用示例**:
```java
Duration d = Duration.ofHours(2).plusMinutes(45).plusSeconds(30);
d.truncatedTo(ChronoUnit.HOURS);  // PT2H
d.truncatedTo(ChronoUnit.MINUTES);  // PT2H45M
```

---

## 10. TemporalAmount 实现

### addTo() / subtractFrom()

```java
@Override
public Temporal addTo(Temporal temporal) {
    if (seconds != 0) {
        temporal = temporal.plus(seconds, SECONDS);
    }
    if (nanos != 0) {
        temporal = temporal.plus(nanos, NANOS);
    }
    return temporal;
}

@Override
public Temporal subtractFrom(Temporal temporal) {
    if (seconds != 0) {
        temporal = temporal.minus(seconds, SECONDS);
    }
    if (nanos != 0) {
        temporal = temporal.minus(nanos, NANOS);
    }
    return temporal;
}
```

**使用示例**:
```java
LocalTime time = LocalTime.of(10, 30);
Duration d = Duration.ofHours(2);
LocalTime result = d.addTo(time);  // 12:30
```

---

## 11. 比较

### compareTo()

```java
@Override
public int compareTo(Duration otherDuration) {
    int cmp = Long.compare(seconds, otherDuration.seconds);
    if (cmp != 0) {
        return cmp;
    }
    return nanos - otherDuration.nanos;
}
```

**比较顺序**: 先比较秒，再比较纳秒

### equals() / hashCode()

```java
@Override
public boolean equals(Object other) {
    if (this == other) {
        return true;
    }
    return (other instanceof Duration otherDuration)
        && this.seconds == otherDuration.seconds
        && this.nanos == otherDuration.nanos;
}

@Override
public int hashCode() {
    return Long.hashCode(seconds) + (51 * nanos);
}
```

---

## 12. 序列化机制

### writeExternal() / readExternal()

```java
void writeExternal(DataOutput out) throws IOException {
    out.writeLong(seconds);
    out.writeInt(nanos);
}

static Duration readExternal(DataInput in) throws IOException {
    long seconds = in.readLong();
    int nanos = in.readInt();
    return Duration.ofSeconds(seconds, nanos);
}
```

**序列化格式**: 8 字节秒 + 4 字节纳秒 = 12 字节

---

## 13. toString() - ISO-8601 输出

```java
@Override
public String toString() {
    if (this == ZERO) {
        return "PT0S";
    }
    long effectiveTotalSecs = seconds;
    if (seconds < 0 && nanos > 0) {
        effectiveTotalSecs++;
    }
    long hours = effectiveTotalSecs / SECONDS_PER_HOUR;
    int minutes = (int) ((effectiveTotalSecs % SECONDS_PER_HOUR) / SECONDS_PER_MINUTE);
    int secs = (int) (effectiveTotalSecs % SECONDS_PER_MINUTE);
    StringBuilder buf = new StringBuilder(24);
    buf.append("PT");
    if (hours != 0) {
        buf.append(hours).append('H');
    }
    if (minutes != 0) {
        buf.append(minutes).append('M');
    }
    if (secs == 0 && nanos == 0 && buf.length() > 2) {
        return buf.toString();
    }
    // ... 处理秒和纳秒
    buf.append('S');
    return buf.toString();
}
```

**输出示例**:

| Duration | toString() |
|----------|------------|
| ZERO | PT0S |
| ofSeconds(20) | PT20S |
| ofSeconds(20).plusNanos(345_000_000) | PT20.345S |
| ofMinutes(15) | PT15M |
| ofHours(10) | PT10H |
| ofDays(2) | PT48H |

**注意**: 不输出天数（避免与 Period 混淆）

---

## 14. 性能特性

### 对象复用

```java
private static Duration create(long seconds, int nanoAdjustment) {
    if ((seconds | nanoAdjustment) == 0) {
        return ZERO;
    }
    return new Duration(seconds, nanoAdjustment);
}
```

**ZERO 常量**: 零值始终返回同一个实例

### 精确计算

```java
// 所有算术运算使用 Math.addExact() / Math.multiplyExact()
// 防止静默溢出
return create(Math.multiplyExact(days, SECONDS_PER_DAY), 0);
```

---

## 15. 使用示例

### 创建

```java
// 零值
Duration zero = Duration.ZERO;

// 从单位创建
Duration d1 = Duration.ofDays(2);
Duration d2 = Duration.ofHours(5);
Duration d3 = Duration.ofMinutes(30);
Duration d4 = Duration.ofSeconds(90);
Duration d5 = Duration.ofMillis(500);
Duration d6 = Duration.ofNanos(1000);

// 带纳秒调整
Duration d7 = Duration.ofSeconds(1, 500_000_000);  // 1.5 秒

// 解析
Duration d8 = Duration.parse("PT20.345S");
Duration d9 = Duration.parse("P2DT3H4M");

// 计算差值
Duration d10 = Duration.between(LocalTime.NOON, LocalTime.MIDNIGHT);
```

### 计算

```java
Duration base = Duration.ofHours(2);

// 加法
Duration d1 = base.plusHours(1);          // PT3H
Duration d2 = base.plusMinutes(30);       // PT2H30M
Duration d3 = base.plusSeconds(90);       // PT2H1M30S
Duration d4 = base.plus(Duration.ofMillis(500));  // PT2H0.5S

// 减法
Duration d5 = base.minusHours(1);         // PT1H
Duration d6 = base.minusMinutes(30);      // PT1H30M

// 乘法
Duration d7 = base.multipliedBy(3);       // PT6H
Duration d8 = base.multipliedBy(-1);      // PT-2H

// 除法
Duration d9 = base.dividedBy(2);          // PT1H
long count = base.dividedBy(Duration.ofMinutes(30));  // 4

// 取反
Duration d10 = base.negated();            // PT-2H

// 绝对值
Duration d11 = Duration.ofHours(-5).abs();  // PT5H

// 截断
Duration d12 = Duration.ofHours(2).plusMinutes(45);
Duration d13 = d12.truncatedTo(ChronoUnit.HOURS);  // PT2H
```

### 转换

```java
Duration d = Duration.ofHours(26).plusMinutes(15).plusSeconds(30);

// 总量
long days = d.toDays();        // 1
long hours = d.toHours();      // 26
long minutes = d.toMinutes();  // 1575
long seconds = d.toSeconds();  // 94530
long millis = d.toMillis();    // 94530000
long nanos = d.toNanos();      // 94530000000000

// 部分
long daysPart = d.toDaysPart();       // 1
int hoursPart = d.toHoursPart();      // 2
int minutesPart = d.toMinutesPart();  // 15
int secondsPart = d.toSecondsPart();  // 30
int millisPart = d.toMillisPart();    // 0
int nanosPart = d.toNanosPart();      // 0
```

### 判断

```java
Duration d = Duration.ofSeconds(60);

d.isPositive();  // true
d.isZero();      // false
d.isNegative();  // false

Duration.ZERO.isZero();  // true
Duration.ofSeconds(-1).isNegative();  // true
```

### 格式化

```java
Duration d = Duration.ofHours(26).plusMinutes(15).plusSeconds(30);

// 自定义格式化
String formatted = String.format("%dd %dh %dm %ds",
    d.toDaysPart(),
    d.toHoursPart(),
    d.toMinutesPart(),
    d.toSecondsPart()
);  // "1d 2h 15m 30s"

// 使用 toString()
System.out.println(d);  // PT26H15M30S
```

---

## 16. 与 Period 对比

| 特性 | Duration | Period |
|------|----------|--------|
| 基础单位 | 秒 + 纳秒 | 年 + 月 + 日 |
| 适用场景 | 计时、延迟、时间差 | 日历日期计算 |
| 精度 | 纳秒级 | 天级 |
| 日期相关性 | 无（固定秒数） | 有（考虑日历） |
| ISO-8601 | PTnHnMnS | PnYnMnD |
| 大小 | 16 字节 | ~24 字节 |

**选择建议**:
```java
// 使用 Duration: 时间量
Duration timeout = Duration.ofSeconds(30);
Duration elapsed = Duration.between(start, end);

// 使用 Period: 日期量
Period age = Period.between(birthDate, today);
Period p = Period.of(2, 3, 4);  // 2年3月4天
```

---

## 17. 相关文档

- [Period 实现](../period/index.md)
- [Instant 实现](../instant/index.md)
- [LocalTime 实现](../localtime/index.md)
- [基础 API](../basics.md)
- [主索引](../index.md)

---

> **更新时间**: 2026-03-20
> **源码版本**: OpenJDK 23
> **文件路径**: `src/java.base/share/classes/java/time/Duration.java`
