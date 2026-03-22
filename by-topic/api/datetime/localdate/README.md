# LocalDate 源码分析

> java.time.LocalDate 的完整实现分析

---
## 目录

1. [类声明](#1-类声明)
2. [字段存储](#2-字段存储)
3. [常量定义](#3-常量定义)
4. [工厂方法](#4-工厂方法)
5. [核心方法](#5-核心方法)
6. [闰年处理](#6-闰年处理)
7. [时间计算](#7-时间计算)
8. [until() - 时间差计算](#8-until---时间差计算)
9. [JDK 9 新增: datesUntil()](#9-jdk-9-新增-datesuntil)
10. [atTime() - 组合时间](#10-attime---组合时间)
11. [比较方法](#11-比较方法)
12. [Epoch Day 转换](#12-epoch-day-转换)
13. [序列化机制](#13-序列化机制)
14. [使用示例](#14-使用示例)
15. [性能特性](#15-性能特性)
16. [常见陷阱](#16-常见陷阱)
17. [与其他类的关系](#17-与其他类的关系)
18. [相关文档](#18-相关文档)

---


## 1. 类声明

```java
@jdk.internal.ValueBased
public final class LocalDate
    implements Temporal, TemporalAdjuster, ChronoLocalDate, Serializable {

    /**
     * @serial The year.
     */
    private final transient int year;

    /**
     * @serial The month-of-year.
     */
    private final transient byte month;

    /**
     * @serial The day-of-month.
     */
    private final transient byte day;
}
```

**关键设计决策**:
- `final` - 不可继承
- `@jdk.internal.ValueBased` - 基于值的类
- `implements ChronoLocalDate` - 支持多种日历系统
- **超紧凑存储** - 仅 6 字节数据

---

## 2. 字段存储

### 三字段紧凑设计

```java
private final transient int year;   // 4 字节
private final transient byte month; // 1 字节
private final transient byte day;   // 1 字节
```

**内存布局**:
- `int year` - 年份 (从 -999,999,999 到 +999,999,999)
- `byte month` - 月份 (1-12)
- `byte day` - 日期 (1-31)

**总大小**: 6 字节 + 对象头 (~16 字节) = ~22 字节

**设计优势**:
1. 极度紧凑的内存占用
2. byte 类型足以存储月份和日期
3. 使用 `transient` 避免默认序列化

---

## 3. 常量定义

### MIN / MAX / EPOCH

```java
/**
 * The minimum supported {@code LocalDate}, '-999999999-01-01'.
 */
public static final LocalDate MIN = LocalDate.of(Year.MIN_VALUE, 1, 1);

/**
 * The maximum supported {@code LocalDate}, '+999999999-12-31'.
 */
public static final LocalDate MAX = LocalDate.of(Year.MAX_VALUE, 12, 31);

/**
 * The epoch year {@code LocalDate}, '1970-01-01'.
 * @since 9
 */
public static final LocalDate EPOCH = LocalDate.of(1970, 1, 1);
```

**范围说明**:

| 常量 | 值 | 说明 |
|------|-----|------|
| `EPOCH` | 1970-01-01 | Unix 纪元起点 |
| `MIN` | -999999999-01-01 | 公元前 10 亿年 |
| `MAX` | +999999999-12-31 | 公元 10 亿年后 |

### 计算常量

```java
/**
 * The number of days in a 400 year cycle.
 */
private static final int DAYS_PER_CYCLE = 146097;

/**
 * The number of days from year zero to year 1970.
 */
static final long DAYS_0000_TO_1970 = (DAYS_PER_CYCLE * 5L) - (30L * 365L + 7L);
```

**400 年周期**:
- 400 年 = 146,097 天
- 包含 97 个闰年
- 用于快速日期计算

---

## 4. 工厂方法

### now() - 当前日期

```java
public static LocalDate now() {
    return now(Clock.systemDefaultZone());
}

public static LocalDate now(ZoneId zone) {
    return now(Clock.system(zone));
}

public static LocalDate now(Clock clock) {
    Objects.requireNonNull(clock, "clock");
    final Instant now = clock.instant();
    return ofInstant(now, clock.getZone());
}
```

### of() - 指定日期

```java
public static LocalDate of(int year, Month month, int dayOfMonth) {
    YEAR.checkValidValue(year);
    Objects.requireNonNull(month, "month");
    DAY_OF_MONTH.checkValidValue(dayOfMonth);
    return create(year, month.getValue(), dayOfMonth);
}

public static LocalDate of(int year, int month, int dayOfMonth) {
    YEAR.checkValidValue(year);
    MONTH_OF_YEAR.checkValidValue(month);
    DAY_OF_MONTH.checkValidValue(dayOfMonth);
    return create(year, month, dayOfMonth);
}
```

### ofYearDay() - 从年份的第几天创建

```java
public static LocalDate ofYearDay(int year, int dayOfYear) {
    YEAR.checkValidValue(year);
    DAY_OF_YEAR.checkValidValue(dayOfYear);
    boolean leap = IsoChronology.INSTANCE.isLeapYear(year);
    if (dayOfYear == 366 && leap == false) {
        throw new DateTimeException("Invalid date 'DayOfYear 366' as '" + year + "' is not a leap year");
    }
    Month moy = Month.of((dayOfYear - 1) / 31 + 1);
    int monthEnd = moy.firstDayOfYear(leap) + moy.length(leap) - 1;
    if (dayOfYear > monthEnd) {
        moy = moy.plus(1);
    }
    int dom = dayOfYear - moy.firstDayOfYear(leap) + 1;
    return new LocalDate(year, moy.getValue(), dom);
}
```

**使用示例**:
```java
// 一年的第 60 天
LocalDate day60 = LocalDate.ofYearDay(2024, 60);  // 2024-02-29 (闰年)
LocalDate day60_2023 = LocalDate.ofYearDay(2023, 60);  // 2023-03-01 (非闰年)
```

### ofInstant() - 从时间戳创建

```java
public static LocalDate ofInstant(Instant instant, ZoneId zone) {
    Objects.requireNonNull(instant, "instant");
    Objects.requireNonNull(zone, "zone");
    ZoneRules rules = zone.getRules();
    ZoneOffset offset = rules.getOffset(instant);
    long localSecond = instant.getEpochSecond() + offset.getTotalSeconds();
    long localEpochDay = Math.floorDiv(localSecond, SECONDS_PER_DAY);
    return ofEpochDay(localEpochDay);
}
```

### ofEpochDay() - 从纪元日创建

```java
public static LocalDate ofEpochDay(long epochDay) {
    EPOCH_DAY.checkValidValue(epochDay);
    long zeroDay = epochDay + DAYS_0000_TO_1970;
    // find the march-based year
    zeroDay -= 60; // adjust to 0000-03-01 so leap day is at end of four year cycle
    long adjust = 0;
    if (zeroDay < 0) {
        // adjust negative years to positive for calculation
        long adjustCycles = (zeroDay + 1) / DAYS_PER_CYCLE - 1;
        adjust = adjustCycles * 400;
        zeroDay += -adjustCycles * DAYS_PER_CYCLE;
    }
    long yearEst = (400 * zeroDay + 591) / DAYS_PER_CYCLE;
    long doyEst = zeroDay - (365 * yearEst + yearEst / 4 - yearEst / 100 + yearEst / 400);
    if (doyEst < 0) {
        // fix estimate
        yearEst--;
        doyEst = zeroDay - (365 * yearEst + yearEst / 4 - yearEst / 100 + yearEst / 400);
    }
    yearEst += adjust; // reset any negative year
    int marchDoy0 = (int) doyEst;
    // convert march-based values back to january-based
    int marchMonth0 = (marchDoy0 * 5 + 2) / 153;
    int month = marchMonth0 + 3;
    if (month > 12) {
        month -= 12;
    }
    int dom = marchDoy0 - (marchMonth0 * 306 + 5) / 10 + 1;
    if (marchDoy0 >= 306) {
        yearEst++;
    }
    return new LocalDate((int)yearEst, month, dom);
}
```

**算法说明**:
1. 调整到以 3 月 1 日为起点 (闰日在周期末尾)
2. 使用 400 年周期估算年份
3. 转换回 1 月起始的日期

### from() - 从 TemporalAccessor 转换

```java
public static LocalDate from(TemporalAccessor temporal) {
    Objects.requireNonNull(temporal, "temporal");
    LocalDate date = temporal.query(TemporalQueries.localDate());
    if (date == null) {
        throw new DateTimeException("Unable to obtain LocalDate from TemporalAccessor: " +
            temporal + " of type " + temporal.getClass().getName());
    }
    return date;
}
```

### parse() - 解析 ISO-8601

```java
public static LocalDate parse(CharSequence text) {
    return parse(text, DateTimeFormatter.ISO_LOCAL_DATE);
}

public static LocalDate parse(CharSequence text, DateTimeFormatter formatter) {
    Objects.requireNonNull(formatter, "formatter");
    return formatter.parse(text, LocalDate::from);
}
```

**支持的格式**:
```
2024-03-20
2024-03-20+08:00
```

---

## 5. 核心方法

### getYear() / getMonth() / getDayOfMonth()

```java
public int getYear() {
    return year;
}

public int getMonthValue() {
    return month;
}

public Month getMonth() {
    return Month.of(month);
}

public int getDayOfMonth() {
    return day;
}
```

### getDayOfYear() / getDayOfWeek()

```java
public int getDayOfYear() {
    return getMonth().firstDayOfYear(isLeapYear()) + day - 1;
}

public DayOfWeek getDayOfWeek() {
    int dow0 = Math.floorMod(toEpochDay() + 3, 7);
    return DayOfWeek.of(dow0 + 1);
}
```

**算法**:
- `toEpochDay() + 3` 调整到周一开始
- 使用 `Math.floorMod` 正确处理负数

### get0() - 内部字段获取

```java
private int get0(TemporalField field) {
    return switch ((ChronoField) field) {
        case DAY_OF_WEEK -> getDayOfWeek().getValue();
        case ALIGNED_DAY_OF_WEEK_IN_MONTH -> ((day - 1) % 7) + 1;
        case ALIGNED_DAY_OF_WEEK_IN_YEAR -> ((getDayOfYear() - 1) % 7) + 1;
        case DAY_OF_MONTH -> day;
        case DAY_OF_YEAR -> getDayOfYear();
        case ALIGNED_WEEK_OF_MONTH -> ((day - 1) / 7) + 1;
        case ALIGNED_WEEK_OF_YEAR -> ((getDayOfYear() - 1) / 7) + 1;
        case MONTH_OF_YEAR -> month;
        case YEAR_OF_ERA -> (year >= 1 ? year : 1 - year);
        case YEAR -> year;
        case ERA -> (year >= 1 ? 1 : 0);
        default -> throw new UnsupportedTemporalTypeException("Unsupported field: " + field);
    };
}
```

---

## 6. 闰年处理

### isLeapYear()

```java
@Override
public boolean isLeapYear() {
    return IsoChronology.INSTANCE.isLeapYear(year);
}
```

**闰年规则** (ISO-8601):
- 能被 4 整除但不能被 100 整除，**或**
- 能被 400 整除

```java
// IsoChronology 实现
public boolean isLeapYear(long prolepticYear) {
    return ((prolepticYear & 3) == 0) &&
           ((prolepticYear % 100) != 0 || (prolepticYear % 400) == 0);
}
```

**位运算优化**:
- `(prolepticYear & 3) == 0` 等价于 `prolepticYear % 4 == 0`

**示例**:
```java
LocalDate.of(2000, 1, 1).isLeapYear();  // true (能被400整除)
LocalDate.of(1900, 1, 1).isLeapYear();  // false (能被100整除但不能被400整除)
LocalDate.of(2024, 1, 1).isLeapYear();  // true (能被4整除)
LocalDate.of(2023, 1, 1).isLeapYear();  // false
```

### lengthOfMonth() / lengthOfYear()

```java
@Override
public int lengthOfMonth() {
    return switch (month) {
        case 2 -> (isLeapYear() ? 29 : 28);
        case 4, 6, 9, 11 -> 30;
        default -> 31;
    };
}

@Override
public int lengthOfYear() {
    return (isLeapYear() ? 366 : 365);
}
```

---

## 7. 时间计算

### withYear() / withMonth() / withDayOfMonth()

```java
public LocalDate withYear(int year) {
    if (this.year == year) {
        return this;
    }
    YEAR.checkValidValue(year);
    return resolvePreviousValid(year, month, day);
}

public LocalDate withMonth(int month) {
    if (this.month == month) {
        return this;
    }
    MONTH_OF_YEAR.checkValidValue(month);
    return resolvePreviousValid(year, month, day);
}

public LocalDate withDayOfMonth(int dayOfMonth) {
    if (this.day == dayOfMonth) {
        return this;
    }
    return of(year, month, dayOfMonth);
}
```

### resolvePreviousValid() - 解析为有效日期

```java
private static LocalDate resolvePreviousValid(int year, int month, int day) {
    switch (month) {
        case 2 -> day = Math.min(day, isLeapYearHelper(year) ? 29 : 28);
        case 4, 6, 9, 11 -> day = Math.min(day, 30);
    }
    return new LocalDate(year, month, day);
}
```

**处理策略**: 当日期无效时，调整为该月的最后一天

**示例**:
```java
LocalDate date = LocalDate.of(2024, 1, 31);
date.withMonth(2);  // 2024-02-29 (闰年，调整到29日)
date.withMonth(4);  // 2024-04-30 (4月只有30日)
```

### plusYears() / plusMonths()

```java
public LocalDate plusYears(long yearsToAdd) {
    if (yearsToAdd == 0) {
        return this;
    }
    int newYear = YEAR.checkValidIntValue(year + yearsToAdd);
    return resolvePreviousValid(newYear, month, day);
}

public LocalDate plusMonths(long monthsToAdd) {
    if (monthsToAdd == 0) {
        return this;
    }
    long monthCount = year * 12L + (month - 1);
    long calcMonths = monthCount + monthsToAdd;
    int newYear = YEAR.checkValidIntValue(Math.floorDiv(calcMonths, 12));
    int newMonth = Math.floorMod(calcMonths, 12) + 1;
    return resolvePreviousValid(newYear, newMonth, day);
}
```

### plusDays() - 优化的加法

```java
public LocalDate plusDays(long daysToAdd) {
    if (daysToAdd == 0) {
        return this;
    }
    long dom = day + daysToAdd;
    if (dom > 0) {
        if (dom <= 28) {
            return new LocalDate(year, month, (int) dom);
        } else if (dom <= 59) { // 59th Jan is 28th Feb, 59th Feb is 31st Mar
            long monthLen = lengthOfMonth();
            if (dom <= monthLen) {
                return new LocalDate(year, month, (int) dom);
            } else if (month < 12) {
                return new LocalDate(year, month + 1, (int) (dom - monthLen));
            } else {
                YEAR.checkValidValue(year + 1);
                return new LocalDate(year + 1, 1, (int) (dom - monthLen));
            }
        }
    }
    long mjDay = Math.addExact(toEpochDay(), daysToAdd);
    return LocalDate.ofEpochDay(mjDay);
}
```

**优化路径**:
1. 小变化 (≤28 天): 直接创建新对象
2. 中等变化 (≤59 天): 检查月份边界
3. 大变化: 使用 epoch day 计算

---

## 8. until() - 时间差计算

### until(Temporal, TemporalUnit) → long

```java
@Override
public long until(Temporal endExclusive, TemporalUnit unit) {
    LocalDate end = LocalDate.from(endExclusive);
    if (unit instanceof ChronoUnit chronoUnit) {
        return switch (chronoUnit) {
            case DAYS -> daysUntil(end);
            case WEEKS -> daysUntil(end) / 7;
            case MONTHS -> monthsUntil(end);
            case YEARS -> monthsUntil(end) / 12;
            case DECADES -> monthsUntil(end) / 120;
            case CENTURIES -> monthsUntil(end) / 1200;
            case MILLENNIA -> monthsUntil(end) / 12000;
            case ERAS -> end.getLong(ERA) - getLong(ERA);
            default -> throw new UnsupportedTemporalTypeException("Unsupported unit: " + unit);
        };
    }
    return unit.between(this, end);
}

long daysUntil(LocalDate end) {
    return end.toEpochDay() - toEpochDay();
}

private long monthsUntil(LocalDate end) {
    long packed1 = getProlepticMonth() * 32L + getDayOfMonth();
    long packed2 = end.getProlepticMonth() * 32L + end.getDayOfMonth();
    return (packed2 - packed1) / 32;
}
```

**打包算法**:
- 将月份和日期打包到一个 long: `month * 32 + day`
- 差值除以 32 得到月数

### until(ChronoLocalDate) → Period

```java
@Override
public Period until(ChronoLocalDate endDateExclusive) {
    LocalDate end = LocalDate.from(endDateExclusive);
    long totalMonths = end.getProlepticMonth() - this.getProlepticMonth();
    int days = end.day - this.day;
    if (totalMonths > 0 && days < 0) {
        totalMonths--;
        LocalDate calcDate = this.plusMonths(totalMonths);
        days = (int) (end.toEpochDay() - calcDate.toEpochDay());
    } else if (totalMonths < 0 && days > 0) {
        totalMonths++;
        days -= end.lengthOfMonth();
    }
    long years = totalMonths / 12;
    int months = (int) (totalMonths % 12);
    return Period.of(Math.toIntExact(years), months, days);
}
```

**使用示例**:
```java
LocalDate start = LocalDate.of(2024, 1, 15);
LocalDate end = LocalDate.of(2024, 6, 20);

Period period = start.until(end);
// P5M5D (5个月5天)

long days = start.until(end, ChronoUnit.DAYS);
// 157 天
```

---

## 9. JDK 9 新增: datesUntil()

### datesUntil(LocalDate) - 流式日期

```java
public Stream<LocalDate> datesUntil(LocalDate endExclusive) {
    long end = endExclusive.toEpochDay();
    long start = toEpochDay();
    if (end < start) {
        throw new IllegalArgumentException(endExclusive + " < " + this);
    }
    return LongStream.range(start, end).mapToObj(LocalDate::ofEpochDay);
}
```

### datesUntil(LocalDate, Period) - 自定义步长

```java
public Stream<LocalDate> datesUntil(LocalDate endExclusive, Period step) {
    // ... 复杂的步长计算逻辑 ...
    return LongStream.rangeClosed(0, steps).mapToObj(
        n -> this.plusMonths(months * n).plusDays(days * n));
}
```

**使用示例**:
```java
LocalDate start = LocalDate.of(2024, 3, 1);
LocalDate end = LocalDate.of(2024, 3, 31);

// 每日流
start.datesUntil(end)
     .filter(d -> d.getDayOfWeek() == DayOfWeek.SATURDAY)
     .forEach(System.out::println);

// 每周流
start.datesUntil(end, Period.ofWeeks(1))
     .forEach(System.out::println);

// 每月流 (处理月末)
LocalDate.of(2024, 1, 31)
    .datesUntil(LocalDate.of(2024, 6, 1), Period.ofMonths(1))
    .forEach(System.out::println);
// 2024-01-31, 2024-02-29, 2024-03-31, 2024-04-30, 2024-05-31
```

---

## 10. atTime() - 组合时间

### atTime(LocalTime) → LocalDateTime

```java
@Override
public LocalDateTime atTime(LocalTime time) {
    return LocalDateTime.of(this, time);
}

public LocalDateTime atTime(int hour, int minute) {
    return atTime(LocalTime.of(hour, minute));
}

public LocalDateTime atTime(int hour, int minute, int second) {
    return atTime(LocalTime.of(hour, minute, second));
}

public LocalDateTime atTime(int hour, int minute, int second, int nanoOfSecond) {
    return atTime(LocalTime.of(hour, minute, second, nanoOfSecond));
}
```

### atTime(OffsetTime) → OffsetDateTime

```java
public OffsetDateTime atTime(OffsetTime time) {
    return OffsetDateTime.of(LocalDateTime.of(this, time.toLocalTime()), time.getOffset());
}
```

### atStartOfDay()

```java
public LocalDateTime atStartOfDay() {
    return LocalDateTime.of(this, LocalTime.MIDNIGHT);
}

public ZonedDateTime atStartOfDay(ZoneId zone) {
    Objects.requireNonNull(zone, "zone");
    LocalDateTime ldt = atTime(LocalTime.MIDNIGHT);
    if (!(zone instanceof ZoneOffset)) {
        ZoneRules rules = zone.getRules();
        ZoneOffsetTransition trans = rules.getTransition(ldt);
        if (trans != null && trans.isGap()) {
            ldt = trans.getDateTimeAfter();
        }
    }
    return ZonedDateTime.of(ldt, zone);
}
```

**处理夏令时 Gap**:
- 在夏令时开始时，午夜可能不存在
- 自动调整到 Gap 之后的时间

---

## 11. 比较方法

### compareTo()

```java
@Override
public int compareTo(ChronoLocalDate other) {
    if (other instanceof LocalDate) {
        return compareTo0((LocalDate) other);
    }
    return ChronoLocalDate.super.compareTo(other);
}

int compareTo0(LocalDate otherDate) {
    int cmp = (year - otherDate.year);
    if (cmp == 0) {
        cmp = (month - otherDate.month);
        if (cmp == 0) {
            cmp = (day - otherDate.day);
        }
    }
    return cmp;
}
```

### isAfter() / isBefore() / isEqual()

```java
@Override
public boolean isAfter(ChronoLocalDate other) {
    if (other instanceof LocalDate) {
        return compareTo0((LocalDate) other) > 0;
    }
    return ChronoLocalDate.super.isAfter(other);
}

@Override
public boolean isBefore(ChronoLocalDate other) {
    if (other instanceof LocalDate) {
        return compareTo0((LocalDate) other) < 0;
    }
    return ChronoLocalDate.super.isBefore(other);
}

@Override
public boolean isEqual(ChronoLocalDate other) {
    if (other instanceof LocalDate) {
        return compareTo0((LocalDate) other) == 0;
    }
    return ChronoLocalDate.super.isEqual(other);
}
```

### equals() / hashCode()

```java
@Override
public boolean equals(Object obj) {
    if (this == obj) {
        return true;
    }
    if (obj instanceof LocalDate) {
        return compareTo0((LocalDate) obj) == 0;
    }
    return false;
}

@Override
public int hashCode() {
    return (year & 0xFFFFF800) ^ ((year << 11) + (month << 6) + day);
}
```

**hashCode 设计**:
- 使用位运算混合年月日
- 高位屏蔽避免溢出

---

## 12. Epoch Day 转换

### toEpochDay()

```java
@Override
public long toEpochDay() {
    long y = year;
    long m = month;
    long total = 0;
    total += 365 * y;
    if (y >= 0) {
        total += (y + 3) / 4 - (y + 99) / 100 + (y + 399) / 400;
    } else {
        total -= y / -4 - y / -100 + y / -400;
    }
    total += ((367 * m - 362) / 12);
    total += day - 1;
    if (m > 2) {
        total--;
        if (isLeapYear() == false) {
            total--;
        }
    }
    return total - DAYS_0000_TO_1970;
}
```

**算法说明**:
1. 计算年份贡献的天数 (365 × year)
2. 加上闰年天数
3. 加上月份贡献的天数
4. 加上日期
5. 调整到 1970 纪元

### toEpochSecond() - JDK 9

```java
public long toEpochSecond(LocalTime time, ZoneOffset offset) {
    Objects.requireNonNull(time, "time");
    Objects.requireNonNull(offset, "offset");
    long secs = toEpochDay() * SECONDS_PER_DAY + time.toSecondOfDay();
    secs -= offset.getTotalSeconds();
    return secs;
}
```

---

## 13. 序列化机制

### writeReplace()

```java
@java.io.Serial
private Object writeReplace() {
    return new Ser(Ser.LOCAL_DATE_TYPE, this);
}

@java.io.Serial
private void readObject(ObjectInputStream s) throws InvalidObjectException {
    throw new InvalidObjectException("Deserialization via serialization delegate");
}
```

### writeExternal()

```java
void writeExternal(DataOutput out) throws IOException {
    out.writeInt(year);
    out.writeByte(month);
    out.writeByte(day);
}

static LocalDate readExternal(DataInput in) throws IOException {
    int year = in.readInt();
    int month = in.readByte();
    int dayOfMonth = in.readByte();
    return LocalDate.of(year, month, dayOfMonth);
}
```

**序列化格式**:
```
out.writeByte(3);   // LocalDate 类型标识
out.writeInt(year);  // 4 字节
out.writeByte(month); // 1 字节
out.writeByte(day);   // 1 字节
```

**总大小**: 6 字节

---

## 14. 使用示例

### 创建

```java
// 当前日期
LocalDate now = LocalDate.now();

// 指定日期
LocalDate date = LocalDate.of(2024, 3, 20);
LocalDate date2 = LocalDate.of(2024, Month.MARCH, 20);

// 从年份的第几天
LocalDate day60 = LocalDate.ofYearDay(2024, 60);

// 从纪元日
LocalDate fromEpoch = LocalDate.ofEpochDay(20000);

// 解析
LocalDate parsed = LocalDate.parse("2024-03-20");
```

### 计算

```java
LocalDate date = LocalDate.of(2024, 3, 20);

// 加减时间
LocalDate plus1Year = date.plusYears(1);
LocalDate plus2Months = date.plusMonths(2);
LocalDate plus3Weeks = date.plusWeeks(3);
LocalDate plus10Days = date.plusDays(10);

// 修改字段
LocalDate newYear = date.withYear(2025);
LocalDate newMonth = date.withMonth(6);
LocalDate newDay = date.withDayOfMonth(15);

// 使用 TemporalAdjuster
LocalDate nextMonday = date.with(TemporalAdjusters.next(DayOfWeek.MONDAY));
LocalDate lastDayOfMonth = date.with(TemporalAdjusters.lastDayOfMonth());
```

### 时间差

```java
LocalDate start = LocalDate.of(2024, 1, 1);
LocalDate end = LocalDate.of(2024, 12, 31);

// 计算天数
long days = start.until(end, ChronoUnit.DAYS);  // 365

// 计算 Period
Period period = start.until(end);  // P11M30D (11个月30天)

// 或使用 Period.between
period = Period.between(start, end);  // P11M30D
```

### 流式操作 (JDK 9+)

```java
LocalDate start = LocalDate.of(2024, 3, 1);
LocalDate end = LocalDate.of(2024, 3, 31);

// 所有日期
start.datesUntil(end)
     .forEach(System.out::println);

// 只显示周五
start.datesUntil(end)
     .filter(d -> d.getDayOfWeek() == DayOfWeek.FRIDAY)
     .forEach(System.out::println);

// 每周一
start.datesUntil(end, Period.ofWeeks(1))
     .filter(d -> d.getDayOfWeek() == DayOfWeek.MONDAY)
     .forEach(System.out::println);
```

### 组合时间

```java
LocalDate date = LocalDate.of(2024, 3, 20);

// 与 LocalTime 组合
LocalDateTime ldt = date.atTime(LocalTime.of(14, 30));
LocalDateTime ldt2 = date.atTime(14, 30, 0);

// 与 OffsetTime 组合
OffsetTime ot = OffsetTime.of(LocalTime.of(14, 30), ZoneOffset.ofHours(8));
OffsetDateTime odt = date.atTime(ot);

// 一天的开始
LocalDateTime startOfDay = date.atStartOfDay();

// 时区的一天开始 (处理夏令时)
ZonedDateTime startOfDayInZone = date.atStartOfDay(ZoneId.of("America/New_York"));
```

---

## 15. 性能特性

### 紧凑存储

```java
// 仅 6 字节数据
private final transient int year;   // 4 字节
private final transient byte month; // 1 字节
private final transient byte day;   // 1 字节
```

### 快路优化

```java
public LocalDate plusDays(long daysToAdd) {
    if (daysToAdd == 0) {
        return this;
    }
    long dom = day + daysToAdd;
    if (dom > 0) {
        if (dom <= 28) {
            return new LocalDate(year, month, (int) dom);  // 快速路径
        } else if (dom <= 59) {
            // 中等路径
        }
    }
    // 慢速路径: 使用 epoch day
    long mjDay = Math.addExact(toEpochDay(), daysToAdd);
    return LocalDate.ofEpochDay(mjDay);
}
```

### hashCode 优化

```java
public int hashCode() {
    return (year & 0xFFFFF800) ^ ((year << 11) + (month << 6) + day);
}
```

- 单次计算
- 位运算混合
- 无需对象创建

---

## 16. 常见陷阱

### 1. 月末日期调整

```java
// ❌ 可能不符合预期
LocalDate jan31 = LocalDate.of(2024, 1, 31);
LocalDate feb = jan31.withMonth(2);  // 2024-02-29 (闰年)
LocalDate feb2 = jan31.withMonth(2);  // 2023-02-28 (非闰年)

// ✅ 明确处理
LocalDate lastDay = date.with(TemporalAdjusters.lastDayOfMonth());
```

### 2. 时间差计算

```java
LocalDate start = LocalDate.of(2024, 1, 31);
LocalDate end = LocalDate.of(2024, 2, 29);

// until() 使用完整月份
start.until(end, ChronoUnit.MONTHS);  // 0 (不足一个月)

// Period 显示月数差异
Period.between(start, end);  // P0M29D (0个月29天)
```

### 3. 年份范围

```java
// Year 范围
LocalDate.MIN.getYear();   // -999999999
LocalDate.MAX.getYear();   // 999999999

// 注意溢出
LocalDate.now().plusYears(Long.MAX_VALUE);  // ArithmeticException
```

---

## 17. 与其他类的关系

```
LocalDate (不带时间的日期)
    │
    ├─→ atTime(LocalTime) → LocalDateTime
    ├─→ atTime(OffsetTime) → OffsetDateTime
    ├─→ atStartOfDay(ZoneId) → ZonedDateTime
    │
    ├─→ toEpochDay() → long (纪元日)
    ├─→ toEpochSecond(LocalTime, ZoneOffset) → long (纪元秒)
    │
    └─→ until(ChronoLocalDate) → Period
```

**选择指南**:

| 需求 | 使用 |
|------|------|
| 仅日期 (生日、纪念日) | `LocalDate` |
| 日期时间 | `LocalDateTime` |
| 带时区的日期时间 | `ZonedDateTime` |
| 带偏移的日期时间 | `OffsetDateTime` |
| 时间戳 | `Instant` |

---

## 18. 相关文档

- [LocalDateTime 实现](../localdatetime/README.md)
- [LocalTime 实现](../localtime/README.md)
- [Period 实现](../period/README.md)
- [主索引](../README.md)

---

> **更新时间**: 2026-03-20
> **源码版本**: OpenJDK 23
> **文件路径**: `src/java.base/share/classes/java/time/LocalDate.java`
