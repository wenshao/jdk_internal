# Instant 源码分析

> java.time.Instant 的完整实现分析

---

## 类声明

```java
@jdk.internal.ValueBased
public final class Instant
    implements Temporal, TemporalAdjuster, Comparable<Instant>, Serializable {
```

**关键设计决策**:
- `final` - 不可继承
- `@jdk.internal.ValueBased` - 基于值的类
- `Comparable<Instant>` - 时间线顺序比较
- 表示时间线上的单一瞬时点

---

## 字段存储

### 两字段组合

```java
/**
 * @serial The number of seconds from the epoch of 1970-01-01T00:00:00Z.
 */
private final long seconds;

/**
 * @serial The number of nanoseconds, later along the time-line, from the seconds field.
 * This is always positive, and never exceeds 999,999,999.
 */
private final int nanos;
```

**内存布局**:
- `long seconds` - 8 字节，从 1970-01-01T00:00:00Z 开始的秒数
- `int nanos` - 4 字节，纳秒调整 (0 到 999,999,999)

**设计优势**:
1. 分离秒和纳秒，避免溢出
2. 纳秒始终为正，简化比较逻辑
3. 支持纳秒级精度的时间戳

---

## 常量定义

### MIN / MAX / EPOCH

```java
/**
 * The minimum supported epoch second.
 */
private static final long MIN_SECOND = -31557014167219200L;

/**
 * The maximum supported epoch second.
 */
private static final long MAX_SECOND = 31556889864403199L;

/**
 * Constant for the 1970-01-01T00:00:00Z epoch instant.
 */
public static final Instant EPOCH = new Instant(0, 0);

/**
 * The minimum supported {@code Instant}, '-1000000000-01-01T00:00Z'.
 */
public static final Instant MIN = Instant.ofEpochSecond(MIN_SECOND, 0);

/**
 * The maximum supported {@code Instant}, '1000000000-12-31T23:59:59.999999999Z'.
 */
public static final Instant MAX = Instant.ofEpochSecond(MAX_SECOND, 999_999_999);
```

**范围说明**:

| 常量 | 值 | 说明 |
|------|-----|------|
| `EPOCH` | 1970-01-01T00:00:00Z | Unix 纪元起点 |
| `MIN` | -1000000000-01-01T00:00Z | 公元前 10 亿年 |
| `MAX` | +1000000000-12-31T23:59:59.999999999Z | 公元 10 亿年后 |

**为什么是 ±10 亿年？**
- LocalDateTime 范围是 ±999,999,999 年
- Instant 额外扩展 1 年以处理最大时区偏移 (±18:00)
- 年份仍适合 int 存储

---

## Java 时间标度

### 时间标度定义

```java
/**
 * The Java Time-Scale divides each calendar day into exactly 86,400
 * subdivisions, known as seconds.
 *
 * For the segment from 1972-11-03 until further notice:
 * - Identical to UTC-SLS
 * - Leap seconds spread equally over last 1000 seconds of the day
 *
 * For the segment prior to 1972-11-03:
 * - Identical to UT1 (mean solar time at Greenwich)
 */
```

**关键概念**:

| 时间标度 | 说明 | 处理闰秒 |
|----------|------|----------|
| **TAI** | 国际原子时间 | 不插入闰秒 |
| **UT1** | 平均太阳时间 | 无闰秒概念 |
| **UTC** | 协调世界时 | 插入闰秒 (23:59:60) |
| **UTC-SLS** | UTC 平滑线性标度 | 闰秒分散到最后 1000 秒 |
| **Java Time-Scale** | Java 定义的时间标度 | 1972-11-03 后使用 UTC-SLS |

**闰秒处理**:

```
UTC 有闰秒的日:
23:59:58
23:59:59
23:59:60  ← 闰秒
00:00:00

Java Time-Scale (UTC-SLS):
23:59:58.000
23:59:58.001  ← 闰秒分散
23:59:58.002
...
23:59:59.999
00:00:00.000
```

---

## 工厂方法

### now() - 当前时间

```java
public static Instant now() {
    return Clock.currentInstant();
}

public static Instant now(Clock clock) {
    Objects.requireNonNull(clock, "clock");
    return clock.instant();
}
```

### ofEpochSecond() - 从纪元秒创建

```java
public static Instant ofEpochSecond(long epochSecond) {
    return create(epochSecond, 0);
}

public static Instant ofEpochSecond(long epochSecond, long nanoAdjustment) {
    long secs = Math.addExact(epochSecond, Math.floorDiv(nanoAdjustment, NANOS_PER_SECOND));
    int nos = (int)Math.floorMod(nanoAdjustment, NANOS_PER_SECOND);
    return create(secs, nos);
}
```

**处理纳秒调整**:
```java
// 以下三者等价:
Instant.ofEpochSecond(3, 1);           // 3秒 + 1纳秒
Instant.ofEpochSecond(4, -999_999_999); // 4秒 - 999,999,999纳秒
Instant.ofEpochSecond(2, 1_000_000_001); // 2秒 + 1,000,000,001纳秒
```

### ofEpochMilli() - 从毫秒创建

```java
public static Instant ofEpochMilli(long epochMilli) {
    long secs = Math.floorDiv(epochMilli, 1000);
    int mos = Math.floorMod(epochMilli, 1000);
    return create(secs, mos * 1000_000);
}
```

### from() - 从 TemporalAccessor 转换

```java
public static Instant from(TemporalAccessor temporal) {
    if (temporal instanceof Instant) {
        return (Instant) temporal;
    }
    Objects.requireNonNull(temporal, "temporal");
    try {
        long instantSecs = temporal.getLong(INSTANT_SECONDS);
        int nanoOfSecond = temporal.get(NANO_OF_SECOND);
        return Instant.ofEpochSecond(instantSecs, nanoOfSecond);
    } catch (DateTimeException ex) {
        throw new DateTimeException("Unable to obtain Instant from TemporalAccessor: " +
            temporal + " of type " + temporal.getClass().getName(), ex);
    }
}
```

### parse() - 解析 ISO-8601

```java
public static Instant parse(final CharSequence text) {
    return DateTimeFormatter.ISO_INSTANT.parse(text, Instant::from);
}
```

**支持的格式**:
```
2024-03-20T14:30:00Z
2024-03-20T14:30:00.123Z
2024-03-20T14:30:00.123456789Z
2024-03-20T14:30:00+08:00
```

---

## 核心方法

### getEpochSecond() / getNano()

```java
public long getEpochSecond() {
    return seconds;
}

public int getNano() {
    return nanos;
}
```

### toEpochMilli() - 转换为毫秒

```java
public long toEpochMilli() {
    if (seconds < 0 && nanos > 0) {
        long millis = Math.multiplyExact(seconds+1, 1000);
        long adjustment = nanos / 1000_000 - 1000;
        return Math.addExact(millis, adjustment);
    } else {
        long millis = Math.multiplyExact(seconds, 1000);
        return Math.addExact(millis, nanos / 1000_000);
    }
}
```

**特殊处理**: 负秒数时的纳舍入

```
例如: seconds = -1, nanos = 500_000_000
-1.5 秒 = -1500 毫秒

公式:
millis = (-1 + 1) * 1000 = 0
adjustment = 500 - 1000 = -500
result = 0 + (-500) = -500 ✓
```

---

## 时间计算

### plusSeconds() / plusMillis() / plusNanos()

```java
public Instant plusSeconds(long secondsToAdd) {
    if (secondsToAdd == 0) {
        return this;
    }
    long epochSec = Math.addExact(seconds, secondsToAdd);
    return create(epochSec, nanos);
}

public Instant plusMillis(long millisToAdd) {
    return plus(millisToAdd / 1000, (millisToAdd % 1000) * 1000_000);
}

public Instant plusNanos(long nanosToAdd) {
    return plus(0, nanosToAdd);
}
```

### plus() - 核心加法

```java
private Instant plus(long secondsToAdd, long nanosToAdd) {
    if ((secondsToAdd | nanosToAdd) == 0) {
        return this;
    }
    long epochSec = Math.addExact(seconds, secondsToAdd);
    epochSec = Math.addExact(epochSec, nanosToAdd / NANOS_PER_SECOND);
    nanosToAdd = nanosToAdd % NANOS_PER_SECOND;
    long nanoAdjustment = nanos + nanosToAdd; // safe int+NANOS_PER_SECOND
    return ofEpochSecond(epochSec, nanoAdjustment);
}
```

**溢出保护**:
- 使用 `Math.addExact` 检测溢出
- 纳秒部分通过 `ofEpochSecond` 自动规范化

### truncatedTo() - 截断

```java
public Instant truncatedTo(TemporalUnit unit) {
    if (unit == ChronoUnit.NANOS) {
        return this;
    }
    Duration unitDur = unit.getDuration();
    if (unitDur.getSeconds() > LocalTime.SECONDS_PER_DAY) {
        throw new UnsupportedTemporalTypeException("Unit is too large to be used for truncation");
    }
    long dur = unitDur.toNanos();
    if ((LocalTime.NANOS_PER_DAY % dur) != 0) {
        throw new UnsupportedTemporalTypeException("Unit must divide into a standard day without remainder");
    }
    long nod = (seconds % LocalTime.SECONDS_PER_DAY) * LocalTime.NANOS_PER_SECOND + nanos;
    long result = Math.floorDiv(nod, dur) * dur;
    return plusNanos(result - nod);
}
```

**使用示例**:
```java
Instant instant = Instant.parse("2024-03-20T14:35:42.123456789Z");

instant.truncatedTo(ChronoUnit.HOURS);   // 2024-03-20T14:00:00Z
instant.truncatedTo(ChronoUnit.MINUTES); // 2024-03-20T14:35:00Z
instant.truncatedTo(ChronoUnit.SECONDS); // 2024-03-20T14:35:42Z
instant.truncatedTo(ChronoUnit.MILLIS);  // 2024-03-20T14:35:42.123Z
```

---

## JDK 26 新增: plusSaturating()

```java
/**
 * Returns a copy of this instant with the specified duration added, with
 * saturated semantics.
 */
public Instant plusSaturating(Duration duration) {
    if (duration.isNegative()) {
        return until(Instant.MIN).compareTo(duration) >= 0 ? Instant.MIN : plus(duration);
    } else {
        return until(Instant.MAX).compareTo(duration) <= 0 ? Instant.MAX : plus(duration);
    }
}
```

**饱和语义**:
- 结果早于 MIN → 返回 MIN
- 结果晚于 MAX → 返回 MAX
- 其他情况 → 正常加法

**使用场景**:
```java
// 计算截止时间，避免溢出异常
Instant deadline = Instant.now().plusSaturating(Duration.ofDays(Long.MAX_VALUE));
```

---

## 比较方法

### compareTo()

```java
@Override
public int compareTo(Instant otherInstant) {
    int cmp = Long.compare(seconds, otherInstant.seconds);
    if (cmp != 0) {
        return cmp;
    }
    return nanos - otherInstant.nanos;
}
```

**比较顺序**: 先秒后纳秒

### isAfter() / isBefore()

```java
public boolean isAfter(Instant otherInstant) {
    return compareTo(otherInstant) > 0;
}

public boolean isBefore(Instant otherInstant) {
    return compareTo(otherInstant) < 0;
}
```

### equals() / hashCode()

```java
@Override
public boolean equals(Object other) {
    if (this == other) {
        return true;
    }
    return (other instanceof Instant otherInstant)
        && this.seconds == otherInstant.seconds
        && this.nanos == otherInstant.nanos;
}

@Override
public int hashCode() {
    return Long.hashCode(seconds) + 51 * nanos;
}
```

---

## until() - 时间差计算

```java
@Override
public long until(Temporal endExclusive, TemporalUnit unit) {
    Instant end = Instant.from(endExclusive);
    if (unit instanceof ChronoUnit chronoUnit) {
        return switch (chronoUnit) {
            case NANOS -> nanosUntil(end);
            case MICROS -> microsUntil(end);
            case MILLIS -> millisUntil(end);
            case SECONDS -> secondsUntil(end);
            case MINUTES -> secondsUntil(end) / SECONDS_PER_MINUTE;
            case HOURS -> secondsUntil(end) / SECONDS_PER_HOUR;
            case HALF_DAYS -> secondsUntil(end) / (12 * SECONDS_PER_HOUR);
            case DAYS -> secondsUntil(end) / (SECONDS_PER_DAY);
            default -> throw new UnsupportedTemporalTypeException("Unsupported unit: " + unit);
        };
    }
    return unit.between(this, end);
}
```

### JDK 23 新增: until(Instant) → Duration

```java
/**
 * Calculates the {@code Duration} until another {@code Instant}.
 */
public Duration until(Instant endExclusive) {
    Objects.requireNonNull(endExclusive, "endExclusive");
    long secsDiff = Math.subtractExact(endExclusive.seconds, seconds);
    int nanosDiff = endExclusive.nanos - nanos;
    return Duration.ofSeconds(secsDiff, nanosDiff);
}
```

**使用示例**:
```java
Instant start = Instant.parse("2024-03-20T14:00:00Z");
Instant end = Instant.parse("2024-03-20T16:30:00Z");

Duration duration = start.until(end);
// PT2H30M (2小时30分钟)
```

---

## 转换方法

### atOffset() - 转换为 OffsetDateTime

```java
public OffsetDateTime atOffset(ZoneOffset offset) {
    return OffsetDateTime.ofInstant(this, offset);
}
```

### atZone() - 转换为 ZonedDateTime

```java
public ZonedDateTime atZone(ZoneId zone) {
    return ZonedDateTime.ofInstant(this, zone);
}
```

---

## 序列化机制

### writeReplace()

```java
private Object writeReplace() {
    return new Ser(Ser.INSTANT_TYPE, this);
}

private void readObject(ObjectInputStream s) throws InvalidObjectException {
    throw new InvalidObjectException("Deserialization via serialization delegate");
}
```

### writeExternal()

```java
void writeExternal(DataOutput out) throws IOException {
    out.writeLong(seconds);
    out.writeInt(nanos);
}

static Instant readExternal(DataInput in) throws IOException {
    long seconds = in.readLong();
    int nanos = in.readInt();
    return Instant.ofEpochSecond(seconds, nanos);
}
```

**序列化格式**:
```
out.writeByte(2);     // Instant 类型标识
out.writeLong(seconds); // 8 字节
out.writeInt(nanos);    // 4 字节
```

**总大小**: 13 字节

---

## 使用示例

### 创建

```java
// 当前时间 (UTC)
Instant now = Instant.now();

// 从纪元秒
Instant fromEpoch = Instant.ofEpochSecond(1710939600L);

// 从毫秒
Instant fromMillis = Instant.ofEpochMilli(1710939600000L);

// 解析 ISO-8601
Instant parsed = Instant.parse("2024-03-20T14:00:00Z");
```

### 计算

```java
Instant now = Instant.now();

// 加减时间
Instant plus1Hour = now.plusSeconds(3600);
Instant plus1Day = now.plus(Duration.ofDays(1));
Instant minus1Week = now.minus(7, ChronoUnit.DAYS);

// 饱和加法 (JDK 26+)
Instant farFuture = now.plusSaturating(Duration.ofDays(Long.MAX_VALUE));

// 截断
Instant truncated = now.truncatedTo(ChronoUnit.MINUTES);
```

### 转换

```java
Instant instant = Instant.now();

// 转为 OffsetDateTime
OffsetDateTime odt = instant.atOffset(ZoneOffset.ofHours(8));

// 转为 ZonedDateTime
ZonedDateTime zdt = instant.atZone(ZoneId.of("Asia/Shanghai"));

// 获取纪元秒/毫秒
long epochSecond = instant.getEpochSecond();
long epochMilli = instant.toEpochMilli();
```

### 时间差

```java
Instant start = Instant.parse("2024-03-20T14:00:00Z");
Instant end = Instant.parse("2024-03-20T16:30:00Z");

// 计算秒数
long seconds = start.until(end, ChronoUnit.SECONDS);  // 9000

// 计算天数
long days = start.until(end, ChronoUnit.DAYS);        // 0

// 计算 Duration (JDK 23+)
Duration duration = start.until(end);  // PT2H30M
```

---

## 性能特性

### 快路优化

```java
private static Instant create(long seconds, int nanoOfSecond) {
    if ((seconds | nanoOfSecond) == 0) {
        return EPOCH;  // 返回缓存的 EPOCH 常量
    }
    if (seconds < MIN_SECOND || seconds > MAX_SECOND) {
        throw new DateTimeException("Instant exceeds minimum or maximum instant");
    }
    return new Instant(seconds, nanoOfSecond);
}
```

### 位运算优化

```java
public Instant plusSeconds(long secondsToAdd) {
    if (secondsToAdd == 0) {
        return this;
    }
    // ...
}

private Instant plus(long secondsToAdd, long nanosToAdd) {
    if ((secondsToAdd | nanosToAdd) == 0) {
        return this;  // 位运算检查两者是否都为 0
    }
    // ...
}
```

---

## 常见陷阱

### 1. 忽略时区

```java
// ❌ 错误: Instant 没有/不需要时区
Instant instant = Instant.now();
ZonedDateTime wrong = instant.atZone(ZoneId.of("Asia/Shanghai"));

// ✅ 正确: 直接使用 Instant
Instant instant = Instant.now();  // 已经是 UTC
```

### 2. 溢出问题

```java
// ❌ 可能溢出
Instant result = Instant.now().plus(Long.MAX_VALUE, ChronoUnit.DAYS);

// ✅ 使用饱和加法 (JDK 26+)
Instant result = Instant.now().plusSaturating(Duration.ofDays(Long.MAX_VALUE));
```

### 3. 比较精度

```java
Instant i1 = Instant.parse("2024-03-20T14:00:00.123456789Z");
Instant i2 = Instant.parse("2024-03-20T14:00:00.123456788Z");

// equals 比较完整精度
i1.equals(i2);  // false

// toEpochMilli 丢失精度
i1.toEpochMilli() == i2.toEpochMilli();  // true (都截断到毫秒)
```

---

## 与其他类的关系

```
Instant (时间线上的点)
    │
    ├─→ atOffset(ZoneOffset) → OffsetDateTime
    │
    ├─→ atZone(ZoneId) → ZonedDateTime
    │
    ├─→ toEpochMilli() → long (毫秒)
    │
    └─→ getEpochSecond() + getNano() → 秒 + 纳秒
```

**选择指南**:

| 需求 | 使用 |
|------|------|
| UTC 时间戳 | `Instant` |
| 数据库时间戳 | `Instant` 或 `OffsetDateTime` |
| 带时区的日期时间 | `ZonedDateTime` |
| 本地日期时间 | `LocalDateTime` |

---

## 相关文档

- [OffsetDateTime 实现](../offsetdatetime/index.md)
- [ZonedDateTime 实现](../zonedatetime/index.md)
- [Duration 实现](../duration/index.md)
- [主索引](../index.md)

---

> **更新时间**: 2026-03-20
> **源码版本**: OpenJDK 23
> **文件路径**: `src/java.base/share/classes/java/time/Instant.java`
