# OffsetDateTime 源码分析

> java.time.OffsetDateTime 的完整实现分析

---
## 目录

1. [类声明](#1-类声明)
2. [字段存储](#2-字段存储)
3. [常量定义](#3-常量定义)
4. [工厂方法](#4-工厂方法)
5. [核心方法](#5-核心方法)
6. [比较方法](#6-比较方法)
7. [转换方法](#7-转换方法)
8. [Temporal 实现](#8-temporal-实现)
9. [时间计算](#9-时间计算)
10. [序列化机制](#10-序列化机制)
11. [使用示例](#11-使用示例)
12. [与 ZonedDateTime 区别](#12-与-zoneddatetime-区别)
13. [数据库存储建议](#13-数据库存储建议)
14. [性能特性](#14-性能特性)
15. [常见陷阱](#15-常见陷阱)
16. [相关文档](#16-相关文档)

---


## 1. 类声明

```java
@jdk.internal.ValueBased
public final class OffsetDateTime
    implements Temporal, TemporalAdjuster, Comparable<OffsetDateTime>, Serializable {
```

**关键设计决策**:
- `final` - 不可继承
- `@jdk.internal.ValueBased` - 基于值的类
- 组合设计 - 包含 LocalDateTime + ZoneOffset
- `Comparable<OffsetDateTime>` - 可比较排序

---

## 2. 字段存储

### 两字段组合

```java
/**
 * @serial The local date-time.
 */
private final LocalDateTime dateTime;

/**
 * @serial The offset from UTC/Greenwich.
 */
private final ZoneOffset offset;
```

**内存布局**:
- `LocalDateTime` - 包含 LocalDate + LocalTime (~48 字节)
- `ZoneOffset` - int 存储秒数 (~24 字节)

**设计优势**:
1. 组合而非继承 - 复用现有类的功能
2. 单一职责 - LocalDateTime 处理日期时间，ZoneOffset 处理偏移
3. 固定偏移 - 无需处理复杂的时区规则

---

## 3. 常量定义

### MIN / MAX

```java
/**
 * The minimum supported {@code OffsetDateTime}, '-999999999-01-01T00:00:00+18:00'.
 * This is the local date-time of midnight at the start of the minimum date
 * in the maximum offset (larger offsets are earlier on the time-line).
 */
public static final OffsetDateTime MIN = LocalDateTime.MIN.atOffset(ZoneOffset.MAX);

/**
 * The maximum supported {@code OffsetDateTime}, '+999999999-12-31T23:59:59.999999999-18:00'.
 * This is the local date-time just before midnight at the end of the maximum date
 * in the minimum offset (larger negative offsets are later on the time-line).
 */
public static final OffsetDateTime MAX = LocalDateTime.MAX.atOffset(ZoneOffset.MIN);
```

**设计考虑**:

| 常量 | 值 | 说明 |
|------|-----|------|
| `MIN` | `-999999999-01-01T00:00:00+18:00` | 最早时间 = LocalDateTime.MIN + 最大偏移 |
| `MAX` | `+999999999-12-31T23:59:59.999999999-18:00` | 最晚时间 = LocalDateTime.MAX + 最小偏移 |

**为什么 MIN 用 +18:00 而 MAX 用 -18:00？**

```
时间线上:
+18:00 偏移 → 时间线较早 (更早到达同一瞬间)
-18:00 偏移 → 时间线较晚 (更晚到达同一瞬间)

例如:
2024-01-01T00:00+18:00 = 2023-12-31T06:00Z
2024-01-01T00:00-18:00 = 2024-01-01T18:00Z
```

---

## 4. 工厂方法

### now() - 当前时间

```java
public static OffsetDateTime now() {
    return now(Clock.systemDefaultZone());
}

public static OffsetDateTime now(ZoneId zone) {
    return now(Clock.system(zone));
}

public static OffsetDateTime now(Clock clock) {
    Objects.requireNonNull(clock, "clock");
    final Instant now = clock.instant();
    return ofInstant(now, clock.getZone().getRules().getOffset(now));
}
```

### of() - 指定时间

```java
public static OffsetDateTime of(LocalDate date, LocalTime time, ZoneOffset offset) {
    LocalDateTime dt = LocalDateTime.of(date, time);
    return new OffsetDateTime(dt, offset);
}

public static OffsetDateTime of(LocalDateTime dateTime, ZoneOffset offset) {
    return new OffsetDateTime(dateTime, offset);
}

public static OffsetDateTime of(
    int year, int month, int dayOfMonth,
    int hour, int minute, int second, int nanoOfSecond, ZoneOffset offset) {
    LocalDateTime dt = LocalDateTime.of(year, month, dayOfMonth, hour, minute, second, nanoOfSecond);
    return new OffsetDateTime(dt, offset);
}
```

### ofInstant() - 从时间戳创建

```java
public static OffsetDateTime ofInstant(Instant instant, ZoneId zone) {
    Objects.requireNonNull(instant, "instant");
    Objects.requireNonNull(zone, "zone");
    ZoneRules rules = zone.getRules();
    ZoneOffset offset = rules.getOffset(instant);
    LocalDateTime ldt = LocalDateTime.ofEpochSecond(instant.getEpochSecond(), instant.getNano(), offset);
    return new OffsetDateTime(ldt, offset);
}
```

**转换流程**:
1. 从 `ZoneId` 获取 `ZoneRules`
2. 根据 `Instant` 获取偏移
3. 转换为 `LocalDateTime`

### from() - 从 TemporalAccessor 转换

```java
public static OffsetDateTime from(TemporalAccessor temporal) {
    if (temporal instanceof OffsetDateTime) {
        return (OffsetDateTime) temporal;
    }
    try {
        ZoneOffset offset = ZoneOffset.from(temporal);
        LocalDate date = temporal.query(TemporalQueries.localDate());
        LocalTime time = temporal.query(TemporalQueries.localTime());
        if (date != null && time != null) {
            return OffsetDateTime.of(date, time, offset);
        } else {
            Instant instant = Instant.from(temporal);
            return OffsetDateTime.ofInstant(instant, offset);
        }
    } catch (DateTimeException ex) {
        throw new DateTimeException("Unable to obtain OffsetDateTime from TemporalAccessor: " +
            temporal + " of type " + temporal.getClass().getName(), ex);
    }
}
```

**转换策略**:
1. 优先尝试提取 LocalDate + LocalTime
2. 回退到 Instant 转换
3. 始终提取 ZoneOffset

---

## 5. 核心方法

### 偏移变更方法

#### withOffsetSameLocal() - 保留本地时间

```java
public OffsetDateTime withOffsetSameLocal(ZoneOffset offset) {
    return with(dateTime, offset);
}
```

**行为**: 只改变偏移，本地时间不变

```java
OffsetDateTime odt = OffsetDateTime.of(
    LocalDateTime.of(2024, 3, 20, 14, 0),
    ZoneOffset.ofHours(8)
);  // 2024-03-20T14:00+08:00

OffsetDateTime changed = odt.withOffsetSameLocal(ZoneOffset.ofHours(9));
// 2024-03-20T14:00+09:00 (本地时间不变，但瞬间变化!)
```

#### withOffsetSameInstant() - 保留瞬间

```java
public OffsetDateTime withOffsetSameInstant(ZoneOffset offset) {
    if (offset.equals(this.offset)) {
        return this;
    }
    int difference = offset.getTotalSeconds() - this.offset.getTotalSeconds();
    LocalDateTime adjusted = dateTime.plusSeconds(difference);
    return new OffsetDateTime(adjusted, offset);
}
```

**行为**: 调整本地时间，保持同一瞬间

```java
OffsetDateTime odt = OffsetDateTime.of(
    LocalDateTime.of(2024, 3, 20, 14, 0),
    ZoneOffset.ofHours(8)
);  // 2024-03-20T14:00+08:00

OffsetDateTime changed = odt.withOffsetSameInstant(ZoneOffset.ofHours(9));
// 2024-03-20T15:00+09:00 (本地时间调整，瞬间不变)
```

---

## 6. 比较方法

### compareTo() - 自然顺序

```java
@Override
public int compareTo(OffsetDateTime other) {
    int cmp = getOffset().compareTo(other.getOffset());
    if (cmp != 0) {
        cmp = Long.compare(toEpochSecond(), other.toEpochSecond());
        if (cmp == 0) {
            cmp = toLocalTime().getNano() - other.toLocalTime().getNano();
        }
    }
    if (cmp == 0) {
        cmp = toLocalDateTime().compareTo(other.toLocalDateTime());
    }
    return cmp;
}
```

**比较顺序**:
1. 首先按偏移排序
2. 偏移不同时，按瞬间排序
3. 相同瞬间时，按本地时间排序

**排序示例**:

```
1. 2008-12-03T10:30+01:00
2. 2008-12-03T11:00+01:00
3. 2008-12-03T12:00+02:00  ← 与 #2 相同瞬间
4. 2008-12-03T11:30+01:00
5. 2008-12-03T12:00+01:00
6. 2008-12-03T12:30+01:00
```

### timeLineOrder() - 时间线比较器

```java
public static Comparator<OffsetDateTime> timeLineOrder() {
    return OffsetDateTime::compareInstant;
}

private static int compareInstant(OffsetDateTime datetime1, OffsetDateTime datetime2) {
    if (datetime1.getOffset().equals(datetime2.getOffset())) {
        return datetime1.toLocalDateTime().compareTo(datetime2.toLocalDateTime());
    }
    int cmp = Long.compare(datetime1.toEpochSecond(), datetime2.toEpochSecond());
    if (cmp == 0) {
        cmp = datetime1.toLocalTime().getNano() - datetime2.toLocalTime().getNano();
    }
    return cmp;
}
```

**用途**: 纯粹按时间线顺序比较，忽略本地时间

### isAfter() / isBefore() / isEqual()

```java
public boolean isAfter(OffsetDateTime other) {
    long thisEpochSec = toEpochSecond();
    long otherEpochSec = other.toEpochSecond();
    return thisEpochSec > otherEpochSec ||
        (thisEpochSec == otherEpochSec && toLocalTime().getNano() > other.toLocalTime().getNano());
}

public boolean isBefore(OffsetDateTime other) {
    long thisEpochSec = toEpochSecond();
    long otherEpochSec = other.toEpochSecond();
    return thisEpochSec < otherEpochSec ||
        (thisEpochSec == otherEpochSec && toLocalTime().getNano() < other.toLocalTime().getNano());
}

public boolean isEqual(OffsetDateTime other) {
    return toEpochSecond() == other.toEpochSecond() &&
        toLocalTime().getNano() == other.toLocalTime().getNano();
}
```

**比较的是瞬间，而非本地时间**:

```java
OffsetDateTime beijing = OffsetDateTime.of(
    LocalDateTime.of(2024, 3, 20, 14, 0),
    ZoneOffset.ofHours(8)
);  // 2024-03-20T14:00+08:00

OffsetDateTime tokyo = OffsetDateTime.of(
    LocalDateTime.of(2024, 3, 20, 15, 0),
    ZoneOffset.ofHours(9)
);  // 2024-03-20T15:00+09:00

// isEqual 返回 true - 同一瞬间!
beijing.isEqual(tokyo);  // true
beijing.equals(tokyo);    // false - 本地时间和偏移都不同
```

---

## 7. 转换方法

### atZoneSameInstant() - 转换为 ZonedDateTime (保留瞬间)

```java
public ZonedDateTime atZoneSameInstant(ZoneId zone) {
    return ZonedDateTime.ofInstant(dateTime, offset, zone);
}
```

**行为**: 忽略本地时间，使用底层瞬间

```java
OffsetDateTime odt = OffsetDateTime.of(
    LocalDateTime.of(2024, 3, 10, 2, 30),  // 可能不存在的时间
    ZoneOffset.ofHours(-5)
);

ZonedDateTime zdt = odt.atZoneSameInstant(ZoneId.of("America/New_York"));
// 使用瞬间转换，避免 Gap/Overlap 问题
```

### atZoneSimilarLocal() - 转换为 ZonedDateTime (保留本地时间)

```java
public ZonedDateTime atZoneSimilarLocal(ZoneId zone) {
    return ZonedDateTime.ofLocal(dateTime, zone, offset);
}
```

**行为**: 尝试保留本地时间，可能遇到 Gap/Overlap

### toInstant() / toEpochSecond()

```java
public Instant toInstant() {
    return dateTime.toInstant(offset);
}

public long toEpochSecond() {
    return dateTime.toEpochSecond(offset);
}
```

---

## 8. Temporal 实现

### isSupported()

```java
@Override
public boolean isSupported(TemporalField field) {
    return field instanceof ChronoField || (field != null && field.isSupportedBy(this));
}
```

**支持的字段**: 所有 `ChronoField`，除了 `FOREVER`

### get() / getLong()

```java
@Override
public int get(TemporalField field) {
    if (field instanceof ChronoField chronoField) {
        return switch (chronoField) {
            case INSTANT_SECONDS -> throw new UnsupportedTemporalTypeException(
                "Invalid field 'InstantSeconds' for get() method, use getLong() instead");
            case OFFSET_SECONDS -> getOffset().getTotalSeconds();
            default -> dateTime.get(field);
        };
    }
    return Temporal.super.get(field);
}

@Override
public long getLong(TemporalField field) {
    if (field instanceof ChronoField chronoField) {
        return switch (chronoField) {
            case INSTANT_SECONDS -> toEpochSecond();
            case OFFSET_SECONDS -> getOffset().getTotalSeconds();
            default -> dateTime.getLong(field);
        };
    }
    return field.getFrom(this);
}
```

### with() - 修改字段

```java
@Override
public OffsetDateTime with(TemporalField field, long newValue) {
    if (field instanceof ChronoField chronoField) {
        return switch (chronoField) {
            case INSTANT_SECONDS -> ofInstant(Instant.ofEpochSecond(newValue, getNano()), offset);
            case OFFSET_SECONDS ->
                with(dateTime, ZoneOffset.ofTotalSeconds(chronoField.checkValidIntValue(newValue)));
            default -> with(dateTime.with(field, newValue), offset);
        };
    }
    return field.adjustInto(this, newValue);
}
```

**特殊处理**:
- `INSTANT_SECONDS`: 改变瞬间，偏移不变
- `OFFSET_SECONDS`: 改变偏移，本地时间不变 (等同于 `withOffsetSameLocal`)

---

## 9. 时间计算

### plus() / minus()

```java
@Override
public OffsetDateTime plus(long amountToAdd, TemporalUnit unit) {
    if (unit instanceof ChronoUnit) {
        return with(dateTime.plus(amountToAdd, unit), offset);
    }
    return unit.addTo(this, amountToAdd);
}
```

**关键**: 时间计算不影响偏移

```java
OffsetDateTime odt = OffsetDateTime.of(
    LocalDateTime.of(2024, 3, 10, 1, 30),
    ZoneOffset.ofHours(-5)
);  // 2024-03-10T01:30-05:00

OffsetDateTime plus1Hour = odt.plusHours(1);
// 2024-03-10T02:30-05:00 (偏移不变!)
```

**与 ZonedDateTime 的区别**:

| 类 | 加 1 小时行为 |
|-----|--------------|
| `OffsetDateTime` | 本地时间 +1，偏移不变 |
| `ZonedDateTime` | 可能因夏令时调整偏移 |

---

## 10. 序列化机制

### writeReplace()

```java
private Object writeReplace() {
    return new Ser(Ser.OFFSET_DATE_TIME_TYPE, this);
}

private void readObject(ObjectInputStream s) throws InvalidObjectException {
    throw new InvalidObjectException("Deserialization via serialization delegate");
}
```

### writeExternal()

```java
void writeExternal(ObjectOutput out) throws IOException {
    dateTime.writeExternal(out);
    offset.writeExternal(out);
}

static OffsetDateTime readExternal(ObjectInput in) throws IOException, ClassNotFoundException {
    LocalDateTime dateTime = LocalDateTime.readExternal(in);
    ZoneOffset offset = ZoneOffset.readExternal(in);
    return OffsetDateTime.of(dateTime, offset);
}
```

**序列化格式**:
- LocalDateTime (约 12 字节)
- ZoneOffset (1 或 5 字节)

---

## 11. 使用示例

### 创建

```java
// 当前时间
OffsetDateTime now = OffsetDateTime.now();

// 指定日期时间和偏移
OffsetDateTime meeting = OffsetDateTime.of(
    LocalDateTime.of(2024, 6, 15, 14, 30),
    ZoneOffset.ofHours(-4)
);

// 从 Instant 创建
Instant instant = Instant.now();
OffsetDateTime fromInstant = instant.atOffset(ZoneOffset.ofHours(8));

// 解析
OffsetDateTime parsed = OffsetDateTime.parse("2024-06-15T14:30:00+08:00");
```

### 偏移转换

```java
OffsetDateTime odt = OffsetDateTime.parse("2024-06-15T14:30:00+08:00");

// 保留本地时间，改变偏移
OffsetDateTime sameLocal = odt.withOffsetSameLocal(ZoneOffset.ofHours(-5));
// 2024-06-15T14:30:00-05:00 (不同瞬间)

// 保留瞬间，改变偏移
OffsetDateTime sameInstant = odt.withOffsetSameInstant(ZoneOffset.ofHours(-5));
// 2024-06-15T01:30:00-05:00 (同一瞬间)
```

### 比较

```java
OffsetDateTime beijing = OffsetDateTime.parse("2024-06-15T14:00+08:00");
OffsetDateTime tokyo = OffsetDateTime.parse("2024-06-15T15:00+09:00");

// equals 比较本地时间和偏移
beijing.equals(tokyo);  // false

// isEqual 比较瞬间
beijing.isEqual(tokyo);  // true

// compareTo 首先比较偏移
beijing.compareTo(tokyo);  // +08:00 < +09:00，返回正数

// timeLineOrder 只比较瞬间
Comparator<OffsetDateTime> comparator = OffsetDateTime.timeLineOrder();
comparator.compare(beijing, tokyo);  // 0 - 同一瞬间
```

### 转换

```java
OffsetDateTime odt = OffsetDateTime.parse("2024-06-15T14:30:00+08:00");

// 转为 Instant
Instant instant = odt.toInstant();

// 转为 ZonedDateTime (保留瞬间)
ZonedDateTime sameInstant = odt.atZoneSameInstant(ZoneId.of("America/New_York"));

// 转为 ZonedDateTime (保留本地时间)
ZonedDateTime sameLocal = odt.atZoneSimilarLocal(ZoneId.of("America/New_York"));

// 转为 LocalDateTime
LocalDateTime ldt = odt.toLocalDateTime();
```

---

## 12. 与 ZonedDateTime 区别

| 特性 | OffsetDateTime | ZonedDateTime |
|------|----------------|---------------|
| 偏移 | 固定偏移 | 可变偏移 |
| 夏令时 | ❌ 不处理 | ✅ 自动处理 |
| 数据库存储 | ✅ 推荐 | ❌ 不推荐 |
| 用户界面 | ⚠️ 不够直观 | ✅ 推荐 |
| 时区规则 | ❌ 无 | ✅ 完整规则 |
| 序列化大小 | 小 (~13 字节) | 大 (~17 字节) |

**选择建议**:
- 使用 `OffsetDateTime`: 数据库存储、API 传输、固定偏移场景
- 使用 `ZonedDateTime`: 用户界面、日程安排、需要时区规则

---

## 13. 数据库存储建议

### 为什么 OffsetDateTime 更适合数据库？

```java
// JDBC TIMESTAMP WITH TIME ZONE 映射到 OffsetDateTime
OffsetDateTime odt = resultSet.getObject("timestamp_column", OffsetDateTime.class);

// 存储时保留偏移信息
preparedStatement.setObject(1, OffsetDateTime.now());
```

**优势**:
1. 固定偏移，存储后语义不变
2. 序列化更紧凑
3. 数据库 `TIMESTAMP WITH TIME ZONE` 的自然映射
4. 避免时区规则更新导致的历史数据变化

---

## 14. 性能特性

### 对象复用

```java
// 相同偏移的 ZoneOffset 被缓存
ZoneOffset offset = ZoneOffset.ofHours(8);
OffsetDateTime odt1 = OffsetDateTime.of(LocalDateTime.now(), offset);
OffsetDateTime odt2 = OffsetDateTime.of(LocalDateTime.now(), offset);
// offset 字段指向同一个 ZoneOffset 实例
```

### 快路优化

```java
private OffsetDateTime with(LocalDateTime dateTime, ZoneOffset offset) {
    if (this.dateTime == dateTime && this.offset.equals(offset)) {
        return this;
    }
    return new OffsetDateTime(dateTime, offset);
}
```

---

## 15. 常见陷阱

### 1. 混淆 equals 和 isEqual

```java
OffsetDateTime beijing = OffsetDateTime.parse("2024-06-15T14:00+08:00");
OffsetDateTime tokyo = OffsetDateTime.parse("2024-06-15T15:00+09:00");

// ✅ 正确：检查是否同一瞬间
beijing.isEqual(tokyo);  // true

// ❌ 错误：检查值相等性
beijing.equals(tokyo);   // false
```

### 2. 时间计算不处理夏令时

```java
// 跨越夏令时转换
OffsetDateTime odt = OffsetDateTime.parse("2024-03-10T01:30-05:00");
OffsetDateTime plus1Hour = odt.plusHours(1);
// 结果: 2024-03-10T02:30-05:00
// 实际纽约时间: 2024-03-10T03:30-04:00 (因为夏令时开始)

// 如需处理夏令时，使用 ZonedDateTime
ZonedDateTime zdt = odt.atZoneSameInstant(ZoneId.of("America/New_York"));
ZonedDateTime result = zdt.plusHours(1);
// 结果: 2024-03-10T03:30-04:00
```

### 3. compareTo 的排序行为

```java
OffsetDateTime odt1 = OffsetDateTime.parse("2024-06-15T14:00+08:00");
OffsetDateTime odt2 = OffsetDateTime.parse("2024-06-15T14:00+09:00");

// compareTo 首先比较偏移
odt1.compareTo(odt2);  // +08:00 < +09:00，返回正数

// 如需按时间线排序
Comparator<OffsetDateTime> comparator = OffsetDateTime.timeLineOrder();
comparator.compare(odt1, odt2);  // 按瞬间比较
```

---

## 16. 相关文档

- [ZonedDateTime 实现](../zonedatetime/README.md)
- [ZoneOffset 实现](../zone/zoneoffset.md)
- [Instant 实现](../instant/README.md)
- [LocalDateTime 实现](../localdatetime/README.md)
- [主索引](../README.md)

---

> **更新时间**: 2026-03-20
> **源码版本**: OpenJDK 23
> **文件路径**: `src/java.base/share/classes/java/time/OffsetDateTime.java`
