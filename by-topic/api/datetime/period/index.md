# Period 源码分析

> java.time.Period 的完整实现分析

---
## 目录

1. [类声明](#1-类声明)
2. [字段存储](#2-字段存储)
3. [常量定义](#3-常量定义)
4. [工厂方法](#4-工厂方法)
5. [核心方法](#5-核心方法)
6. [时间计算](#6-时间计算)
7. [归一化](#7-归一化)
8. [TemporalAmount 实现](#8-temporalamount-实现)
9. [比较](#9-比较)
10. [序列化机制](#10-序列化机制)
11. [toString() - ISO-8601 输出](#11-tostring---iso-8601-输出)
12. [使用示例](#12-使用示例)
13. [与 Duration 对比](#13-与-duration-对比)
14. [归一化策略](#14-归一化策略)
15. [常见陷阱](#15-常见陷阱)
16. [相关文档](#16-相关文档)

---


## 1. 类声明

```java
@jdk.internal.ValueBased
public final class Period
    implements ChronoPeriod, Serializable {
```

**关键设计决策**:
- `final` - 不可继承
- `@jdk.internal.ValueBased` - 基于值的类
- `implements ChronoPeriod` - 支持多种日历系统的日期量
- `Serializable` - 支持序列化

**与 Duration 的区别**:
- `Period` - 基于日期的量（年、月、日），适用于日历计算
- `Duration` - 基于时间的量（秒、纳秒），适用于计时、延迟

---

## 2. 字段存储

### 三字段组合

```java
/**
 * @serial The number of years.
 */
private final int years;

/**
 * @serial The number of months.
 */
private final int months;

/**
 * @serial The number of days.
 */
private final int days;
```

**内存布局**:
- `int years` - 4 字节，年数
- `int months` - 4 字节，月数
- `int days` - 4 字节，天数

**为什么需要三个字段？**

| 字段 | 作用 | 范围 |
|------|------|------|
| `years` | 年份部分 | -2^31 到 2^31-1 |
| `months` | 月份部分 | -2^31 到 2^31-1 |
| `days` | 天数部分 | -2^31 到 2^31-1 |

**设计特点**:
1. 不自动归一化 - "15个月" ≠ "1年3个月"
2. 各字段独立 - 可以表示任意组合
3. 灵活表达 - 适合业务场景（如订阅期、合同期）

---

## 3. 常量定义

### 预定义常量

```java
/**
 * A constant for a period of zero.
 */
public static final Period ZERO = new Period(0, 0, 0);
```

**注意**: Period 没有 MIN/MAX 常量（不像 Duration）

---

## 4. 工厂方法

### ofYears() / ofMonths() / ofDays() / ofWeeks()

```java
public static Period ofYears(int years) {
    return create(years, 0, 0);
}

public static Period ofMonths(int months) {
    return create(0, months, 0);
}

public static Period ofDays(int days) {
    return create(0, 0, days);
}

public static Period ofWeeks(int weeks) {
    return create(0, 0, Math.multiplyExact(weeks, 7));
}
```

**溢出保护**: 使用 `Math.multiplyExact()` 防止溢出

### of() - 指定年月日

```java
public static Period of(int years, int months, int days) {
    return create(years, months, days);
}
```

**使用示例**:
```java
Period p1 = Period.of(2, 3, 4);    // 2年3月4天
Period p2 = Period.of(1, 15, 0);   // 1年15月（不归一化）
Period p3 = Period.of(0, 15, 0);   // 15个月
```

### parse() - ISO-8601 格式解析

```java
public static Period parse(CharSequence text) {
    Objects.requireNonNull(text, "text");
    Matcher matcher = PATTERN.matcher(text);
    if (matcher.matches()) {
        int negate = (charMatch(text, matcher.start(1), matcher.end(1), '-') ? -1 : 1);
        int yearStart = matcher.start(2), yearEnd = matcher.end(2);
        int monthStart = matcher.start(3), monthEnd = matcher.end(3);
        int weekStart = matcher.start(4), weekEnd = matcher.end(4);
        int dayStart = matcher.start(5), dayEnd = matcher.end(5);
        if (yearStart >= 0 || monthStart >= 0 || weekStart >= 0 || dayStart >= 0) {
            try {
                int years = parseNumber(text, yearStart, yearEnd, negate);
                int months = parseNumber(text, monthStart, monthEnd, negate);
                int weeks = parseNumber(text, weekStart, weekEnd, negate);
                int days = parseNumber(text, dayStart, dayEnd, negate);
                days = Math.addExact(days, Math.multiplyExact(weeks, 7));
                return create(years, months, days);
            } catch (NumberFormatException ex) {
                throw new DateTimeParseException("Text cannot be parsed to a Period", text, 0, ex);
            }
        }
    }
    throw new DateTimeParseException("Text cannot be parsed to a Period", text, 0);
}
```

**正则表达式**:
```regex
([-+]?)P(?:([-+]?[0-9]+)Y)?(?:([-+]?[0-9]+)M)?(?:([-+]?[0-9]+)W)?(?:([-+]?[0-9]+)D)?
```

**支持的格式**:

| 格式 | 示例 | 说明 |
|------|------|------|
| `P2Y` | 2 年 | 仅年 |
| `P3M` | 3 个月 | 仅月 |
| `P4W` | 4 周 | 转换为 28 天 |
| `P5D` | 5 天 | 仅天 |
| `P1Y2M3D` | 1年2月3天 | 完整格式 |
| `P1Y2M3W4D` | 1年2月25天 | 包含周 |
| `P-1Y2M` | -1年2月 | 年负数 |
| `-P1Y2M` | -(1年2月) | 整体负号 |

**扩展特性** (非标准 ISO-8601):
- 各部分可独立带符号: `P-1Y2M` = -1年 +2月
- 整体负号: `-P1Y2M` = -(1年2月)
- 支持周 (W): 转换为 7 天

### between() - 计算日期差

```java
public static Period between(LocalDate startDateInclusive, LocalDate endDateExclusive) {
    return startDateInclusive.until(endDateExclusive);
}
```

**计算逻辑** (在 LocalDate 中实现):
1. 计算完整年数
2. 计算剩余完整月数
3. 计算剩余天数
4. 确保符号一致

**使用示例**:
```java
LocalDate start = LocalDate.of(2020, 1, 15);
LocalDate end = LocalDate.of(2023, 5, 20);
Period p = Period.between(start, end);
// 结果: P3Y4M5D (3年4月5天)
```

---

## 5. 核心方法

### get() / getUnits()

```java
@Override
public long get(TemporalUnit unit) {
    if (unit == ChronoUnit.YEARS) {
        return getYears();
    } else if (unit == ChronoUnit.MONTHS) {
        return getMonths();
    } else if (unit == ChronoUnit.DAYS) {
        return getDays();
    } else {
        throw new UnsupportedTemporalTypeException("Unsupported unit: " + unit);
    }
}

@Override
public List<TemporalUnit> getUnits() {
    return SUPPORTED_UNITS;
}
```

**支持的单位**: YEARS, MONTHS, DAYS

### 判断方法

```java
public boolean isZero() {
    return (this == ZERO);
}

public boolean isNegative() {
    return years < 0 || months < 0 || days < 0;
}
```

### 访问方法

```java
public int getYears() {
    return years;
}

public int getMonths() {
    return months;
}

public int getDays() {
    return days;
}
```

---

## 6. 时间计算

### plus() - 加法

```java
public Period plus(TemporalAmount amountToAdd) {
    Period isoAmount = Period.from(amountToAdd);
    return create(
        Math.addExact(years, isoAmount.years),
        Math.addExact(months, isoAmount.months),
        Math.addExact(days, isoAmount.days));
}

public Period plusYears(long yearsToAdd) {
    if (yearsToAdd == 0) {
        return this;
    }
    return create(Math.toIntExact(Math.addExact(years, yearsToAdd)), months, days);
}

public Period plusMonths(long monthsToAdd) {
    if (monthsToAdd == 0) {
        return this;
    }
    return create(years, Math.toIntExact(Math.addExact(months, monthsToAdd)), days);
}

public Period plusDays(long daysToAdd) {
    if (daysToAdd == 0) {
        return this;
    }
    return create(years, months, Math.toIntExact(Math.addExact(days, daysToAdd)));
}
```

**特点**: 各字段独立相加，不归一化

### minus() - 减法

```java
public Period minusYears(long yearsToSubtract) {
    return (yearsToSubtract == Long.MIN_VALUE
        ? plusYears(Long.MAX_VALUE).plusYears(1)
        : plusYears(-yearsToSubtract));
}
```

**Long.MIN_VALUE 处理**: 避免直接取反溢出

### multipliedBy() / negated()

```java
public Period multipliedBy(int scalar) {
    if (this == ZERO || scalar == 1) {
        return this;
    }
    return create(
        Math.multiplyExact(years, scalar),
        Math.multiplyExact(months, scalar),
        Math.multiplyExact(days, scalar));
}

public Period negated() {
    return multipliedBy(-1);
}
```

**使用示例**:
```java
Period base = Period.of(1, 2, 3);
base.multipliedBy(3);  // P3Y6M9D
base.negated();        // P-1Y-2M-3D
```

---

## 7. 归一化

### normalized() - 年月归一化

```java
public Period normalized() {
    long totalMonths = toTotalMonths();
    long splitYears = totalMonths / 12;
    int splitMonths = (int) (totalMonths % 12);
    if (splitYears == years && splitMonths == months) {
        return this;
    }
    return create(Math.toIntExact(splitYears), splitMonths, days);
}
```

**行为**:
- 仅归一化年和月
- 天数保持不变
- 符号保持一致

**示例**:
```java
Period.of(1, 15, 0).normalized();   // P2Y3M (1年15月 → 2年3月)
Period.of(1, -25, 0).normalized();  // P-1Y-1M (1年-25月 → -1年-1月)
Period.of(0, 25, 40).normalized();  // P2Y1M40D (25月 → 2年1月，40天不变)
```

### toTotalMonths() - 总月数

```java
public long toTotalMonths() {
    return years * 12L + months;
}
```

**使用场景**: 比较不同表示的 Period

```java
Period p1 = Period.of(1, 3, 0);   // 1年3月
Period p2 = Period.of(0, 15, 0);  // 15个月

p1.equals(p2);          // false
p1.toTotalMonths() == p2.toTotalMonths();  // true (都是 15)
```

---

## 8. TemporalAmount 实现

### addTo() / subtractFrom()

```java
@Override
public Temporal addTo(Temporal temporal) {
    validateChrono(temporal);
    if (months == 0) {
        if (years != 0) {
            temporal = temporal.plus(years, YEARS);
        }
    } else {
        long totalMonths = toTotalMonths();
        if (totalMonths != 0) {
            temporal = temporal.plus(totalMonths, MONTHS);
        }
    }
    if (days != 0) {
        temporal = temporal.plus(days, DAYS);
    }
    return temporal;
}
```

**关键设计**:
- 年和月一起添加（确保月末正确处理）
- 天单独添加
- 验证日历系统

**使用示例**:
```java
LocalDate date = LocalDate.of(2024, 1, 31);
Period p = Period.of(1, 1, 0);

date.plus(p);  // 2025-02-28 (正确处理月末)
```

---

## 9. 比较

### equals() / hashCode()

```java
@Override
public boolean equals(Object obj) {
    if (this == obj) {
        return true;
    }
    return (obj instanceof Period other)
        && years == other.years
        && months == other.months
        && days == other.days;
}

@Override
public int hashCode() {
    return years + Integer.rotateLeft(months, 8) + Integer.rotateLeft(days, 16);
}
```

**相等性**: 三个字段必须完全相等

```java
Period.of(1, 3, 0).equals(Period.of(0, 15, 0));  // false
// 虽然 toTotalMonths() 相等，但表示不同
```

---

## 10. 序列化机制

### writeExternal() / readExternal()

```java
void writeExternal(DataOutput out) throws IOException {
    out.writeInt(years);
    out.writeInt(months);
    out.writeInt(days);
}

static Period readExternal(DataInput in) throws IOException {
    int years = in.readInt();
    int months = in.readInt();
    int days = in.readInt();
    return Period.of(years, months, days);
}
```

**序列化格式**: 3 个 int = 12 字节

---

## 11. toString() - ISO-8601 输出

```java
@Override
public String toString() {
    if (this == ZERO) {
        return "P0D";
    } else {
        StringBuilder buf = new StringBuilder();
        buf.append('P');
        if (years != 0) {
            buf.append(years).append('Y');
        }
        if (months != 0) {
            buf.append(months).append('M');
        }
        if (days != 0) {
            buf.append(days).append('D');
        }
        return buf.toString();
    }
}
```

**输出示例**:

| Period | toString() |
|--------|------------|
| ZERO | P0D |
| of(2, 0, 0) | P2Y |
| of(0, 3, 0) | P3M |
| of(0, 0, 5) | P5D |
| of(1, 2, 3) | P1Y2M3D |
| of(0, 0, 0) | P0D |

**注意**: 零值字段被省略，但零 Period 输出 "P0D"

---

## 12. 使用示例

### 创建

```java
// 零值
Period zero = Period.ZERO;

// 从单位创建
Period p1 = Period.ofYears(2);
Period p2 = Period.ofMonths(15);
Period p3 = Period.ofWeeks(3);
Period p4 = Period.ofDays(10);

// 组合创建
Period p5 = Period.of(1, 2, 3);

// 解析
Period p6 = Period.parse("P2Y3M4D");
Period p7 = Period.parse("P1Y2M");
Period p8 = Period.parse("P-1Y+2M");

// 计算差值
Period p9 = Period.between(
    LocalDate.of(2020, 1, 1),
    LocalDate.of(2023, 6, 15)
);  // P3Y5M14D
```

### 计算

```java
Period base = Period.of(1, 2, 3);

// 加法
Period p1 = base.plusYears(1);        // P2Y2M3D
Period p2 = base.plusMonths(6);       // P1Y8M3D
Period p3 = base.plusDays(10);        // P1Y2M13D
Period p4 = base.plus(Period.of(0, 6, 0));  // P1Y8M3D

// 减法
Period p5 = base.minusYears(1);       // P0Y2M3D
Period p6 = base.minusMonths(3);      // P1Y-1M3D

// 乘法
Period p7 = base.multipliedBy(3);     // P3Y6M9D

// 取反
Period p8 = base.negated();           // P-1Y-2M-3D

// 归一化
Period p9 = Period.of(1, 15, 0).normalized();  // P2Y3M
```

### 应用到日期

```java
LocalDate date = LocalDate.of(2024, 1, 15);
Period p = Period.of(1, 2, 3);

// 添加
LocalDate result1 = date.plus(p);     // 2025-03-18
LocalDate result2 = p.addTo(date);   // 同上

// 减去
LocalDate result3 = date.minus(p);    // 2022-11-12

// 特殊情况处理
LocalDate endOfMonth = LocalDate.of(2024, 1, 31);
endOfMonth.plus(Period.ofMonths(1));  // 2024-02-29 (闰年)
endOfMonth.plus(Period.ofMonths(1));  // 2024-02-29 → 2024-03-31
```

### 判断

```java
Period p = Period.of(1, 2, 3);

p.isZero();      // false
p.isNegative();  // false

Period.ZERO.isZero();  // true
Period.of(-1, 0, 0).isNegative();  // true
Period.of(0, -2, 0).isNegative();  // true
```

### 转换

```java
Period p = Period.of(2, 15, 25);

// 访问各部分
int years = p.getYears();        // 2
int months = p.getMonths();      // 15
int days = p.getDays();          // 25

// 总月数
long totalMonths = p.toTotalMonths();  // 39 (2*12 + 15)

// 归一化
Period normalized = p.normalized();
// normalized.getYears() = 3
// normalized.getMonths() = 3
// normalized.getDays() = 25
```

---

## 13. 与 Duration 对比

| 特性 | Period | Duration |
|------|--------|----------|
| 基础单位 | 年 + 月 + 日 | 秒 + 纳秒 |
| 适用场景 | 日历日期计算 | 计时、延迟、时间差 |
| 精度 | 天级 | 纳秒级 |
| 日期相关性 | 有（考虑日历） | 无（固定秒数） |
| ISO-8601 | PnYnMnD | PTnHnMnS |
| 归一化 | 需要手动调用 | 自动 |
| 大小 | 12 字节 | 16 字节 |
| 夏令时 | ✅ 正确处理 | ❌ 不处理 |

### 夏令时场景

```java
// 2024-03-09 18:00 (夏令时开始前)
ZonedDateTime before = ZonedDateTime.of(
    LocalDateTime.of(2024, 3, 9, 18, 0),
    ZoneId.of("America/New_York")
);  // 2024-03-09T18:00-05:00

// 加上 Period（1天）
ZonedDateTime p1 = before.plus(Period.ofDays(1));
// 结果: 2024-03-10T18:00-04:00
// 保持本地时间 18:00

// 加上 Duration（24小时）
ZonedDateTime p2 = before.plus(Duration.ofDays(1));
// 结果: 2024-03-10T19:00-04:00
// 精确 24 小时，但本地时间变为 19:00
```

**选择建议**:
```java
// 使用 Period: 日期量
Period age = Period.between(birthDate, today);
Period subscription = Period.ofMonths(12);
Period warranty = Period.of(1, 0, 0);  // 1年

// 使用 Duration: 时间量
Duration timeout = Duration.ofMinutes(30);
Duration elapsed = Duration.between(start, end);
Duration delay = Duration.ofSeconds(10);
```

---

## 14. 归一化策略

### 为什么不自动归一化？

**设计原因**:
1. **业务语义**: "15个月订阅期" ≠ "1年3月"
2. **明确性**: 保留原始输入，避免混淆
3. **灵活性**: 允许特定表示

**示例**:
```java
// 场景：订阅期
Period subscription = Period.ofMonths(15);
// 明确表示 15 个月订阅期
// 不应该自动变成 1年3月

// 需要归一化时
Period normalized = subscription.normalized();
// 用于比较或显示时使用
```

### 自定义归一化

```java
// 归一化所有字段（包括天转月）
public static Period fullyNormalized(Period period) {
    // 天数不归一化到月（因为每月天数不同）
    // 只归一化年月
    return period.normalized();
}

// 计算总天数（近似值）
public static long toTotalDaysEstimate(Period period) {
    long years = period.getYears();
    long months = period.getMonths();
    long days = period.getDays();

    // 近似：一年 365.25 天，一月 30.44 天
    long yearDays = (long) (years * 365.25);
    long monthDays = (long) (months * 30.44);
    return yearDays + monthDays + days;
}
```

---

## 15. 常见陷阱

### 1. 不自动归一化

```java
// ❌ 错误理解
Period.of(0, 15, 0).equals(Period.of(1, 3, 0));  // false

// ✅ 正确比较
Period p1 = Period.of(0, 15, 0);
Period p2 = Period.of(1, 3, 0);
p1.toTotalMonths() == p2.toTotalMonths();  // true
```

### 2. 月份天数可变

```java
// 2024-01-31 + 1个月 = 2024-02-29（闰年）
// 2023-01-31 + 1个月 = 2023-02-28（非闰年）
LocalDate.of(2024, 1, 31).plus(Period.ofMonths(1));  // 2024-02-29
LocalDate.of(2023, 1, 31).plus(Period.ofMonths(1));  // 2023-02-28
```

### 3. 负数处理

```java
// 各部分独立处理
Period p = Period.of(1, -2, 3);
// 1年 -2月 +3天
// 不等于 Period.of(0, 10, 3)
```

---

## 16. 相关文档

- [Duration 实现](../duration/index.md)
- [LocalDate 实现](../localdate/index.md)
- [基础 API](../basics.md)
- [主索引](../index.md)

---

> **更新时间**: 2026-03-20
> **源码版本**: OpenJDK 23
> **文件路径**: `src/java.base/share/classes/java/time/Period.java`
