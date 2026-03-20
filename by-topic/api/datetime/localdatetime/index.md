# LocalDateTime 源码分析

> java.time.LocalDateTime 的完整实现分析

---

## 类声明

```java
@jdk.internal.ValueBased
public final class LocalDateTime
implements Temporal, TemporalAdjuster, ChronoLocalDateTime, Serializable {

    /**
     * @serial The date part.
     */
    private final LocalDate date;

    /**
     * @serial The time part.
     */
    private final LocalTime time;
}
```

**关键设计决策**:
- `final` - 不可继承
- `@jdk.internal.ValueBased` - 基于值的类
- `implements ChronoLocalDateTime` - 支持多种日历系统
- **组合设计** - 包含 LocalDate + LocalTime

---

## 字段存储

### 两字段组合

```java
private final LocalDate date;  // 日期部分
private final LocalTime time;   // 时间部分
```

**内存布局**:
- `LocalDate` - int year (4) + byte month (1) + byte day (1) = 6 字节 + 对象头
- `LocalTime` - byte hour (1) + byte minute (1) + byte second (1) + int nano (4) = 7 字节 + 对象头

**为什么使用组合？**

| 设计选择 | 优势 |
|----------|------|
| 组合 LocalDate + LocalTime | 代码复用，职责分离 |
| 单独存储所有字段 | 紧凑存储，但代码重复 |

LocalDateTime 选择组合设计，通过委托模式实现大多数操作：
```java
public int getYear() {
    return date.getYear();  // 委托给 LocalDate
}

public int getHour() {
    return time.getHour();  // 委托给 LocalTime
}
```

---

## 常量定义

### MIN / MAX

```java
/**
 * The minimum supported {@code LocalDateTime}, '-999999999-01-01T00:00:00'.
 */
public static final LocalDateTime MIN = LocalDateTime.of(LocalDate.MIN, LocalTime.MIN);

/**
 * The maximum supported {@code LocalDateTime}, '+999999999-12-31T23:59:59.999999999'.
 */
public static final LocalDateTime MAX = LocalDateTime.of(LocalDate.MAX, LocalTime.MAX);
```

**范围说明**:

| 常量 | 值 | 说明 |
|------|-----|------|
| `MIN` | -999999999-01-01T00:00:00 | 公元前 10 亿年 |
| `MAX` | +999999999-12-31T23:59:59.999999999 | 公元 10 亿年后 |

**为什么是 ±10 亿年？**
- LocalDate 范围是 ±999,999,999 年
- LocalTime 范围是 00:00 到 23:59:59.999999999
- 组合后直接取两者的 MIN 和 MAX

---

## 工厂方法

### now() - 当前时间

```java
public static LocalDateTime now() {
    return now(Clock.systemDefaultZone());
}

public static LocalDateTime now(ZoneId zone) {
    return now(Clock.system(zone));
}

public static LocalDateTime now(Clock clock) {
    Objects.requireNonNull(clock, "clock");
    final Instant now = clock.instant(); // called once
    ZoneOffset offset = clock.getZone().getRules().getOffset(now);
    return ofEpochSecond(now.getEpochSecond(), now.getNano(), offset);
}
```

**关键**: `clock.instant()` 只调用一次，确保时间一致

### of() - 指定时间

```java
public static LocalDateTime of(int year, Month month, int dayOfMonth, int hour, int minute) {
    LocalDate date = LocalDate.of(year, month, dayOfMonth);
    LocalTime time = LocalTime.of(hour, minute);
    return new LocalDateTime(date, time);
}

public static LocalDateTime of(int year, int month, int dayOfMonth,
                               int hour, int minute, int second, int nanoOfSecond) {
    LocalDate date = LocalDate.of(year, month, dayOfMonth);
    LocalTime time = LocalTime.of(hour, minute, second, nanoOfSecond);
    return new LocalDateTime(date, time);
}

public static LocalDateTime of(LocalDate date, LocalTime time) {
    Objects.requireNonNull(date, "date");
    Objects.requireNonNull(time, "time");
    return new LocalDateTime(date, time);
}
```

**重载方法**:
- `of(year, month, dayOfMonth, hour, minute)` - 日期 + 时分
- `of(year, month, dayOfMonth, hour, minute, second)` - 日期 + 时分秒
- `of(year, month, dayOfMonth, hour, minute, second, nanoOfSecond)` - 完整日期时间
- `of(LocalDate, LocalTime)` - 组合现有对象

### ofInstant() - 从时间戳创建

```java
public static LocalDateTime ofInstant(Instant instant, ZoneId zone) {
    Objects.requireNonNull(instant, "instant");
    Objects.requireNonNull(zone, "zone");
    ZoneRules rules = zone.getRules();
    ZoneOffset offset = rules.getOffset(instant);
    return ofEpochSecond(instant.getEpochSecond(), instant.getNano(), offset);
}
```

**转换流程**:
1. 从 `Instant` 获取纪元秒和纳秒
2. 根据 `ZoneRules` 获取偏移
3. 转换为本地日期时间

### ofEpochSecond() - 从纪元秒创建

```java
public static LocalDateTime ofEpochSecond(long epochSecond, int nanoOfSecond, ZoneOffset offset) {
    Objects.requireNonNull(offset, "offset");
    NANO_OF_SECOND.checkValidValue(nanoOfSecond);
    long localSecond = epochSecond + offset.getTotalSeconds(); // overflow caught later
    long localEpochDay = Math.floorDiv(localSecond, SECONDS_PER_DAY);
    int secsOfDay = Math.floorMod(localSecond, SECONDS_PER_DAY);
    LocalDate date = LocalDate.ofEpochDay(localEpochDay);
    LocalTime time = LocalTime.ofNanoOfDay(secsOfDay * NANOS_PER_SECOND + nanoOfSecond);
    return new LocalDateTime(date, time);
}
```

**计算过程**:
```
例如: epochSecond = 1710939600, offset = +08:00

localSecond = 1710939600 + 28800 = 1710968400
localEpochDay = floorDiv(1710968400, 86400) = 19802
secsOfDay = floorMod(1710968400, 86400) = 36000 (即 10:00:00)

date = LocalDate.ofEpochDay(19802)  // 2024-03-20
time = LocalTime.ofNanoOfDay(36000 * 1_000_000_000)  // 10:00:00

结果: 2024-03-20T10:00:00
```

### from() - 从 TemporalAccessor 转换

```java
public static LocalDateTime from(TemporalAccessor temporal) {
    if (temporal instanceof LocalDateTime) {
        return (LocalDateTime) temporal;
    } else if (temporal instanceof ZonedDateTime) {
        return ((ZonedDateTime) temporal).toLocalDateTime();
    } else if (temporal instanceof OffsetDateTime) {
        return ((OffsetDateTime) temporal).toLocalDateTime();
    }
    try {
        LocalDate date = LocalDate.from(temporal);
        LocalTime time = LocalTime.from(temporal);
        return new LocalDateTime(date, time);
    } catch (DateTimeException ex) {
        throw new DateTimeException("Unable to obtain LocalDateTime from TemporalAccessor: " +
            temporal + " of type " + temporal.getClass().getName(), ex);
    }
}
```

**支持的转换**:
- `ZonedDateTime` → 提取本地部分
- `OffsetDateTime` → 提取本地部分
- 其他 `TemporalAccessor` → 分别提取日期和时间

### parse() - 解析 ISO-8601

```java
public static LocalDateTime parse(CharSequence text) {
    return parse(text, DateTimeFormatter.ISO_LOCAL_DATE_TIME);
}

public static LocalDateTime parse(CharSequence text, DateTimeFormatter formatter) {
    Objects.requireNonNull(formatter, "formatter");
    return formatter.parse(text, LocalDateTime::from);
}
```

**支持的格式**:
```
2024-03-20T14:30:00
2024-03-20T14:30:00.123
2024-03-20T14:30:00.123456789
```

---

## 核心方法

### toLocalDate() / toLocalTime()

```java
@Override
public LocalDate toLocalDate() {
    return date;
}

@Override
public LocalTime toLocalTime() {
    return time;
}
```

### 字段访问方法 (委托模式)

```java
public int getYear() {
    return date.getYear();
}

public int getMonthValue() {
    return date.getMonthValue();
}

public Month getMonth() {
    return date.getMonth();
}

public int getDayOfMonth() {
    return date.getDayOfMonth();
}

public int getDayOfYear() {
    return date.getDayOfYear();
}

public DayOfWeek getDayOfWeek() {
    return date.getDayOfWeek();
}

public int getHour() {
    return time.getHour();
}

public int getMinute() {
    return time.getMinute();
}

public int getSecond() {
    return time.getSecond();
}

public int getNano() {
    return time.getNano();
}
```

---

## 时间调整

### with() - 通用调整

```java
@Override
public LocalDateTime with(TemporalAdjuster adjuster) {
    // optimizations
    if (adjuster instanceof LocalDate) {
        return with((LocalDate) adjuster, time);
    } else if (adjuster instanceof LocalTime) {
        return with(date, (LocalTime) adjuster);
    } else if (adjuster instanceof LocalDateTime) {
        return (LocalDateTime) adjuster;
    }
    return (LocalDateTime) adjuster.adjustInto(this);
}
```

**优化**: 类型检查避免不必要的对象创建

### with(TemporalField, long) - 字段调整

```java
@Override
public LocalDateTime with(TemporalField field, long newValue) {
    if (field instanceof ChronoField chronoField) {
        if (chronoField.isTimeBased()) {
            return with(date, time.with(field, newValue));
        } else {
            return with(date.with(field, newValue), time);
        }
    }
    return field.adjustInto(this, newValue);
}
```

**分类处理**:
- 时间字段 → 委托给 LocalTime
- 日期字段 → 委托给 LocalDate

### withYear() / withMonth() / withDayOfMonth()

```java
public LocalDateTime withYear(int year) {
    return with(date.withYear(year), time);
}

public LocalDateTime withMonth(int month) {
    return with(date.withMonth(month), time);
}

public LocalDateTime withDayOfMonth(int dayOfMonth) {
    return with(date.withDayOfMonth(dayOfMonth), time);
}

public LocalDateTime withDayOfYear(int dayOfYear) {
    return with(date.withDayOfYear(dayOfYear), time);
}
```

### withHour() / withMinute() / withSecond() / withNano()

```java
public LocalDateTime withHour(int hour) {
    LocalTime newTime = time.withHour(hour);
    return with(date, newTime);
}

public LocalDateTime withMinute(int minute) {
    LocalTime newTime = time.withMinute(minute);
    return with(date, newTime);
}

public LocalDateTime withSecond(int second) {
    LocalTime newTime = time.withSecond(second);
    return with(date, newTime);
}

public LocalDateTime withNano(int nanoOfSecond) {
    LocalTime newTime = time.withNano(nanoOfSecond);
    return with(date, newTime);
}
```

### 私有辅助方法

```java
private LocalDateTime with(LocalDate newDate, LocalTime newTime) {
    if (date == newDate && time == newTime) {
        return this;  // 优化: 值相同时返回 this
    }
    return new LocalDateTime(newDate, newTime);
}
```

**不变性保证**:
- 值相同时返回 `this`，避免创建新对象
- 值不同时创建新对象，原对象不变

---

## 时间计算

### plus() - 通用加法

```java
@Override
public LocalDateTime plus(long amountToAdd, TemporalUnit unit) {
    if (unit instanceof ChronoUnit chronoUnit) {
        return switch (chronoUnit) {
            case NANOS -> plusNanos(amountToAdd);
            case MICROS -> plusDays(amountToAdd / MICROS_PER_DAY)
                           .plusNanos((amountToAdd % MICROS_PER_DAY) * 1000);
            case MILLIS -> plusDays(amountToAdd / MILLIS_PER_DAY)
                           .plusNanos((amountToAdd % MILLIS_PER_DAY) * 1000_000);
            case SECONDS -> plusSeconds(amountToAdd);
            case MINUTES -> plusMinutes(amountToAdd);
            case HOURS -> plusHours(amountToAdd);
            case HALF_DAYS -> plusDays(amountToAdd / 256)
                              .plusHours((amountToAdd % 256) * 12);
            default -> with(date.plus(amountToAdd, unit), time);
        };
    }
    return unit.addTo(this, amountToAdd);
}
```

**使用 switch 表达式 (JDK 21+)**:
- 纳秒/微秒/毫秒 → 需要处理跨日
- 秒/分/小时 → 直接相加
- 半天 → 256 个单位 = 128 天，避免溢出
- 天/周/月/年 → 委托给 LocalDate

### plusYears() / plusMonths() / plusWeeks() / plusDays()

```java
public LocalDateTime plusYears(long years) {
    LocalDate newDate = date.plusYears(years);
    return with(newDate, time);
}

public LocalDateTime plusMonths(long months) {
    LocalDate newDate = date.plusMonths(months);
    return with(newDate, time);
}

public LocalDateTime plusWeeks(long weeks) {
    LocalDate newDate = date.plusWeeks(weeks);
    return with(newDate, time);
}

public LocalDateTime plusDays(long days) {
    LocalDate newDate = date.plusDays(days);
    return with(newDate, time);
}
```

**闰年/月份处理**:
- 2008-02-29 + 1年 = 2009-02-28 (自动调整)
- 2007-03-31 + 1月 = 2007-04-30 (自动调整)

### plusHours() / plusMinutes() / plusSeconds() / plusNanos()

```java
public LocalDateTime plusHours(long hours) {
    return plusWithOverflow(date, hours, 0, 0, 0, 1);
}

public LocalDateTime plusMinutes(long minutes) {
    return plusWithOverflow(date, 0, minutes, 0, 0, 1);
}

public LocalDateTime plusSeconds(long seconds) {
    return plusWithOverflow(date, 0, 0, seconds, 0, 1);
}

public LocalDateTime plusNanos(long nanos) {
    return plusWithOverflow(date, 0, 0, 0, nanos, 1);
}
```

### plusWithOverflow() - 核心计算

```java
private LocalDateTime plusWithOverflow(LocalDate newDate, long hours, long minutes,
                                       long seconds, long nanos, int sign) {
    if ((hours | minutes | seconds | nanos) == 0) {
        return with(newDate, time);
    }

    // 计算总天数
    long totDays = nanos / NANOS_PER_DAY +
                   seconds / SECONDS_PER_DAY +
                   minutes / MINUTES_PER_DAY +
                   hours / HOURS_PER_DAY;
    totDays *= sign;

    // 计算剩余纳秒
    long totNanos = nanos % NANOS_PER_DAY +
                   (seconds % SECONDS_PER_DAY) * NANOS_PER_SECOND +
                   (minutes % MINUTES_PER_DAY) * NANOS_PER_MINUTE +
                   (hours % HOURS_PER_DAY) * NANOS_PER_HOUR;
    long curNoD = time.toNanoOfDay();
    totNanos = totNanos * sign + curNoD;

    // 处理纳秒溢出
    totDays += Math.floorDiv(totNanos, NANOS_PER_DAY);
    long newNoD = Math.floorMod(totNanos, NANOS_PER_DAY);

    LocalTime newTime = (newNoD == curNoD ? time : LocalTime.ofNanoOfDay(newNoD));
    return with(newDate.plusDays(totDays), newTime);
}
```

**示例计算**:
```
初始: 2024-03-20T23:30:00
加: 2 小时

hours = 2, sign = 1
totDays = 0
totNanos = 2 * 3_600_000_000_000 = 7_200_000_000_000
curNoD = 23 * 3600 + 30 * 60 = 84600 秒 = 84_600_000_000_000 纳秒
totNanos = 7_200_000_000_000 + 84_600_000_000_000 = 91_800_000_000_000

floorDiv(91_800_000_000_000, 86_400_000_000_000) = 1
floorMod(91_800_000_000_000, 86_400_000_000_000) = 5_400_000_000_000

totDays = 1
newNoD = 5_400_000_000_000 = 01:30:00

结果: 2024-03-21T01:30:00
```

### minus() - 减法

```java
@Override
public LocalDateTime minus(long amountToSubtract, TemporalUnit unit) {
    return (amountToSubtract == Long.MIN_VALUE
            ? plus(Long.MAX_VALUE, unit).plus(1, unit)
            : plus(-amountToSubtract, unit));
}
```

**Long.MIN_VALUE 处理**:
- 直接取反会溢出
- 拆分为 MAX_VALUE + 1

---

## until() - 时间差计算

```java
@Override
public long until(Temporal endExclusive, TemporalUnit unit) {
    LocalDateTime end = LocalDateTime.from(endExclusive);
    if (unit instanceof ChronoUnit chronoUnit) {
        if (unit.isTimeBased()) {
            long amount = date.daysUntil(end.date);
            if (amount == 0) {
                return time.until(end.time, unit);
            }
            long timePart = end.time.toNanoOfDay() - time.toNanoOfDay();
            if (amount > 0) {
                amount--;
                timePart += NANOS_PER_DAY;
            } else {
                amount++;
                timePart -= NANOS_PER_DAY;
            }
            switch (chronoUnit) {
                case NANOS -> amount = Math.multiplyExact(amount, NANOS_PER_DAY);
                case MICROS -> {
                    amount = Math.multiplyExact(amount, MICROS_PER_DAY);
                    timePart = timePart / 1000;
                }
                case MILLIS -> {
                    amount = Math.multiplyExact(amount, MILLIS_PER_DAY);
                    timePart = timePart / 1_000_000;
                }
                case SECONDS -> {
                    amount = Math.multiplyExact(amount, SECONDS_PER_DAY);
                    timePart = timePart / NANOS_PER_SECOND;
                }
                case MINUTES -> {
                    amount = Math.multiplyExact(amount, MINUTES_PER_DAY);
                    timePart = timePart / NANOS_PER_MINUTE;
                }
                case HOURS -> {
                    amount = Math.multiplyExact(amount, HOURS_PER_DAY);
                    timePart = timePart / NANOS_PER_HOUR;
                }
                case HALF_DAYS -> {
                    amount = Math.multiplyExact(amount, 2);
                    timePart = timePart / (NANOS_PER_HOUR * 12);
                }
                default -> throw new UnsupportedTemporalTypeException("Unsupported unit: " + unit);
            }
            return Math.addExact(amount, timePart);
        }
        LocalDate endDate = end.date;
        if (endDate.isAfter(date) && end.time.isBefore(time)) {
            endDate = endDate.minusDays(1);
        } else if (endDate.isBefore(date) && end.time.isAfter(time)) {
            endDate = endDate.plusDays(1);
        }
        return date.until(endDate, unit);
    }
    return unit.between(this, end);
}
```

**时间单位计算示例**:
```
start: 2024-03-20T23:00:00
end:   2024-03-21T01:30:00

amount = date.daysUntil(end.date) = 1
timePart = 5400000000000 - 82800000000000 = -77400000000000

amount > 0:
  amount = 0
  timePart = -77400000000000 + 86400000000000 = 9000000000000

HOURS:
  amount = 0 * 24 = 0
  timePart = 9000000000000 / 3600000000000 = 2.5

结果: 2.5 小时
```

---

## 比较方法

### compareTo()

```java
@Override
public int compareTo(ChronoLocalDateTime<?> other) {
    if (other instanceof LocalDateTime) {
        return compareTo0((LocalDateTime) other);
    }
    return ChronoLocalDateTime.super.compareTo(other);
}

private int compareTo0(LocalDateTime other) {
    int cmp = date.compareTo0(other.toLocalDate());
    if (cmp == 0) {
        cmp = time.compareTo(other.toLocalTime());
    }
    return cmp;
}
```

**比较顺序**: 先日期后时间

### isAfter() / isBefore() / isEqual()

```java
@Override
public boolean isAfter(ChronoLocalDateTime<?> other) {
    if (other instanceof LocalDateTime) {
        return compareTo0((LocalDateTime) other) > 0;
    }
    return ChronoLocalDateTime.super.isAfter(other);
}

@Override
public boolean isBefore(ChronoLocalDateTime<?> other) {
    if (other instanceof LocalDateTime) {
        return compareTo0((LocalDateTime) other) < 0;
    }
    return ChronoLocalDateTime.super.isBefore(other);
}

@Override
public boolean isEqual(ChronoLocalDateTime<?> other) {
    if (other instanceof LocalDateTime) {
        return compareTo0((LocalDateTime) other) == 0;
    }
    return ChronoLocalDateTime.super.isEqual(other);
}
```

### equals() / hashCode()

```java
@Override
public boolean equals(Object obj) {
    if (this == obj) {
        return true;
    }
    return (obj instanceof LocalDateTime other)
        && date.equals(other.date)
        && time.equals(other.time);
}

@Override
public int hashCode() {
    return date.hashCode() ^ time.hashCode();
}
```

---

## 转换方法

### atOffset() - 转换为 OffsetDateTime

```java
public OffsetDateTime atOffset(ZoneOffset offset) {
    return OffsetDateTime.of(this, offset);
}
```

### atZone() - 转换为 ZonedDateTime

```java
@Override
public ZonedDateTime atZone(ZoneId zone) {
    return ZonedDateTime.of(this, zone);
}
```

**Gap 和 Overlap 处理**:
- Gap (春季夏令时开始): 自动调整到稍后时间
- Overlap (秋季夏令时结束): 使用早期偏移

---

## 序列化机制

### writeReplace()

```java
private Object writeReplace() {
    return new Ser(Ser.LOCAL_DATE_TIME_TYPE, this);
}

private void readObject(ObjectInputStream s) throws InvalidObjectException {
    throw new InvalidObjectException("Deserialization via serialization delegate");
}
```

### writeExternal()

```java
void writeExternal(DataOutput out) throws IOException {
    date.writeExternal(out);
    time.writeExternal(out);
}

static LocalDateTime readExternal(DataInput in) throws IOException {
    LocalDate date = LocalDate.readExternal(in);
    LocalTime time = LocalTime.readExternal(in);
    return LocalDateTime.of(date, time);
}
```

**序列化格式**:
```
// 类型标识
out.writeByte(5);  // LocalDateTime 类型

// LocalDate 部分 (4 字节)
out.writeInt(date.year);
out.writeByte(date.month);
out.writeByte(date.day);

// LocalTime 部分 (6 字节)
out.writeByte(time.hour);
out.writeByte(time.minute);
out.writeByte(time.second);
out.writeInt(time.nano);
```

**总大小**: 11 字节

---

## 性能特性

### 类型检查优化

```java
@Override
public LocalDateTime with(TemporalAdjuster adjuster) {
    if (adjuster instanceof LocalDate) {
        return with((LocalDate) adjuster, time);
    } else if (adjuster instanceof LocalTime) {
        return with(date, (LocalTime) adjuster);
    } else if (adjuster instanceof LocalDateTime) {
        return (LocalDateTime) adjuster;
    }
    return (LocalDateTime) adjuster.adjustInto(this);
}
```

**优势**:
- 避免 `adjustInto` 调用开销
- 直接访问字段，快速构建结果

### 快路优化

```java
private LocalDateTime with(LocalDate newDate, LocalTime newTime) {
    if (date == newDate && time == newTime) {
        return this;  // 返回 this，避免创建新对象
    }
    return new LocalDateTime(newDate, newTime);
}
```

### hashCode 计算

```java
@Override
public int hashCode() {
    return date.hashCode() ^ time.hashCode();
}
```

**XOR 操作**:
- 简单快速
- 低碰撞概率（假设 date 和 time 的 hashCode 分布均匀）

---

## 使用示例

### 创建

```java
// 当前时间
LocalDateTime now = LocalDateTime.now();

// 指定日期时间
LocalDateTime appointment = LocalDateTime.of(2024, 6, 15, 14, 30);
LocalDateTime meeting = LocalDateTime.of(2024, Month.JUNE, 15, 14, 30, 0);

// 组合日期和时间
LocalDateTime dt = LocalDateTime.of(LocalDate.now(), LocalTime.now());

// 从 Instant 创建
Instant instant = Instant.now();
LocalDateTime fromInstant = LocalDateTime.ofInstant(instant, ZoneId.of("Asia/Shanghai"));

// 解析
LocalDateTime parsed = LocalDateTime.parse("2024-03-20T14:30:00");
```

### 计算

```java
LocalDateTime now = LocalDateTime.now();

// 加减日期
LocalDateTime tomorrow = now.plusDays(1);
LocalDateTime nextWeek = now.plusWeeks(1);
LocalDateTime nextMonth = now.plusMonths(1);
LocalDateTime nextYear = now.plusYears(1);

// 加减时间
LocalDateTime in2Hours = now.plusHours(2);
LocalDateTime in30Minutes = now.plusMinutes(30);

// 修改字段
LocalDateTime newYear = now.withYear(2025);
LocalDateTime firstOfMonth = now.withDayOfMonth(1);
LocalDateTime atNoon = now.with(LocalTime.of(12, 0));

// 调整器
LocalDateTime firstMondayOfNextMonth = now
    .plusMonths(1)
    .with(TemporalAdjusters.firstInMonth(DayOfWeek.MONDAY));
```

### 转换

```java
LocalDateTime ldt = LocalDateTime.now();

// 转为 OffsetDateTime
OffsetDateTime odt = ldt.atOffset(ZoneOffset.ofHours(8));

// 转为 ZonedDateTime
ZonedDateTime zdt = ldt.atZone(ZoneId.of("Asia/Shanghai"));

// 转为 Instant (需要时区)
Instant instant = ldt.atZone(ZoneId.systemDefault()).toInstant();

// 提取日期或时间
LocalDate date = ldt.toLocalDate();
LocalTime time = ldt.toLocalTime();
```

### 时间差

```java
LocalDateTime start = LocalDateTime.of(2024, 3, 20, 14, 0);
LocalDateTime end = LocalDateTime.of(2024, 3, 20, 16, 30);

// 计算小时数
long hours = start.until(end, ChronoUnit.HOURS);  // 2

// 计算分钟数
long minutes = start.until(end, ChronoUnit.MINUTES);  // 150

// 计算天数
long days = start.until(end, ChronoUnit.DAYS);  // 0
```

---

## 与其他类的关系

```
LocalDateTime (本地日期时间)
    │
    ├─→ toLocalDate() → LocalDate
    │
    ├─→ toLocalTime() → LocalTime
    │
    ├─→ atOffset(ZoneOffset) → OffsetDateTime
    │
    ├─→ atZone(ZoneId) → ZonedDateTime
    │
    └─→ atZone(ZoneId).toInstant() → Instant
```

**选择指南**:

| 需求 | 使用 |
|------|------|
| 仅日期 | `LocalDate` |
| 仅时间 | `LocalTime` |
| 本地日期时间 | `LocalDateTime` |
| UTC 时间戳 | `Instant` |
| 带时区的日期时间 | `ZonedDateTime` |
| 固定偏移的日期时间 | `OffsetDateTime` |

---

## 常见陷阱

### 1. 没有时区信息

```java
// ❌ 错误: LocalDateTime 不包含时区
LocalDateTime ldt = LocalDateTime.now();
// "2024-03-20T14:30:00" — 这是哪个时区的时间？

// ✅ 正确: 明确时区
ZonedDateTime zdt = ZonedDateTime.now(ZoneId.of("Asia/Shanghai"));
LocalDateTime ldt = zdt.toLocalDateTime();
```

### 2. 跨时区转换

```java
// ❌ 错误: 直接转换丢失时区
LocalDateTime shanghai = LocalDateTime.now();  // 假设是上海时间
LocalDateTime newYork = shanghai.minusHours(12);  // 错误的时差

// ✅ 正确: 使用 ZonedDateTime 转换
ZonedDateTime shanghai = ZonedDateTime.now(ZoneId.of("Asia/Shanghai"));
ZonedDateTime newYork = shanghai.withZoneSameInstant(ZoneId.of("America/New_York"));
LocalDateTime newYorkLocal = newYork.toLocalDateTime();
```

### 3. 夏令时处理

```java
// LocalDateTime 无法表示夏令时跳跃
LocalDateTime gap = LocalDateTime.of(2024, 3, 10, 2, 30);
// 这个时间在美国东部时区不存在!

// 转换为 ZonedDateTime 会自动调整
ZonedDateTime zdt = gap.atZone(ZoneId.of("America/New_York"));
// 结果: 2024-03-10T03:30-04:00 (自动调整到 3:30)
```

### 4. 月份索引

```java
// ✅ 正确: 月份从 1 开始
LocalDateTime dt = LocalDateTime.of(2024, 3, 20, 14, 0);  // 3月

// 使用枚举更清晰
LocalDateTime dt = LocalDateTime.of(2024, Month.MARCH, 20, 14, 0);
```

---

## 相关文档

- [LocalDate 实现](../localdate/index.md)
- [LocalTime 实现](../localtime/index.md)
- [ZonedDateTime 实现](../zonedatetime/index.md)
- [OffsetDateTime 实现](../offsetdatetime/index.md)
- [Instant 实现](../instant/index.md)
- [主索引](../index.md)

---

> **更新时间**: 2026-03-20
> **源码版本**: OpenJDK 23
> **文件路径**: `src/java.base/share/classes/java/time/LocalDateTime.java`
