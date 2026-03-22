# ZonedDateTime 源码分析

> java.time.ZonedDateTime 的完整实现分析

---
## 目录

1. [类声明](#1-类声明)
2. [字段存储](#2-字段存储)
3. [工厂方法](#3-工厂方法)
4. [核心方法](#4-核心方法)
5. [时间计算](#5-时间计算)
6. [方法引用优化](#6-方法引用优化)
7. [序列化机制](#7-序列化机制)
8. [性能特性](#8-性能特性)
9. [Gap 和 Overlap 详解](#9-gap-和-overlap-详解)
10. [使用示例](#10-使用示例)
11. [与 OffsetDateTime 区别](#11-与-offsetdatetime-区别)
12. [相关文档](#12-相关文档)

---


## 1. 类声明

```java
@jdk.internal.ValueBased
public final class ZonedDateTime
    implements Temporal, ChronoZonedDateTime<LocalDate>, Serializable {

    /**
     * The local date-time.
     */
    private final LocalDateTime dateTime;

    /**
     * The zone offset.
     */
    private final ZoneOffset offset;

    /**
     * The time-zone.
     */
    private final ZoneId zone;
}
```

**关键设计决策**:
- `final` - 不可继承
- `@jdk.internal.ValueBased` - 基于值的类
- `implements ChronoZonedDateTime` - 支持多种日历系统
- 组合设计 - 包含 LocalDateTime + ZoneOffset + ZoneId

---

## 2. 字段存储

### 三字段组合

```java
private final LocalDateTime dateTime;  // 本地日期时间
private final ZoneOffset offset;       // 当前偏移量
private final ZoneId zone;             // 时区规则
```

**内存布局**:
- `LocalDateTime` - 包含 LocalDate + LocalTime (~24 字节)
- `ZoneOffset` - int 存储秒数 (~24 字节)
- `ZoneId` - 引用 (~8 字节)

**为什么需要三个字段？**

| 字段 | 作用 | 变化 |
|------|------|------|
| `dateTime` | 本地时间表示 | 随操作变化 |
| `offset` | 当前瞬时偏移 | 随夏令时变化 |
| `zone` | 时区规则 | 永不变化 |

**示例**:
```java
// 纽约时区，夏令时开始时
ZonedDateTime before = ZonedDateTime.of(
    LocalDateTime.of(2024, 3, 10, 1, 30),  // 本地时间 1:30
    ZoneId.of("America/New_York")
);
// dateTime = 2024-03-10T01:30
// offset = -05:00 (冬季标准时间)
// zone = America/New_York

// 加上 1 小时后
ZonedDateTime after = before.plusHours(1);
// dateTime = 2024-03-10T03:30  (注意：跳过了 2:00-3:00!)
// offset = -04:00 (夏令时)
// zone = America/New_York
```

---

## 3. 工厂方法

### now() - 当前时间

```java
public static ZonedDateTime now() {
    return now(Clock.systemDefaultZone());
}

public static ZonedDateTime now(ZoneId zone) {
    return now(Clock.system(zone));
}

public static ZonedDateTime now(Clock clock) {
    Objects.requireNonNull(clock, "clock");
    return ofInstant(Instant.now(clock), clock.getZone());
}
```

### of() - 指定时间

```java
public static ZonedDateTime of(LocalDateTime localDateTime, ZoneId zone) {
    return ofLocal(localDateTime, zone, null);
}

public static ZonedDateTime of(LocalDate date, LocalTime time, ZoneId zone) {
    return of(LocalDateTime.of(date, time), zone);
}

public static ZonedDateTime of(int year, int month, int dayOfMonth,
                               int hour, int minute, int second, int nanoOfSecond, ZoneId zone) {
    LocalDateTime dt = LocalDateTime.of(year, month, dayOfMonth, hour, minute, second, nanoOfSecond);
    return ofLocal(dt, zone, null);
}
```

### ofLocal() - 从本地时间创建

```java
public static ZonedDateTime ofLocal(LocalDateTime localDateTime, ZoneId zone, ZoneOffset preferredOffset) {
    Objects.requireNonNull(localDateTime, "localDateTime");
    Objects.requireNonNull(zone, "zone");
    if (zone instanceof ZoneOffset) {
        return new ZonedDateTime(localDateTime, (ZoneOffset) zone, zone);
    }
    ZoneRules rules = zone.getRules();
    List<ZoneOffset> validOffsets = rules.getValidOffsets(localDateTime);
    if (validOffsets.size() == 1) {
        // Normal: 唯一有效偏移
        return new ZonedDateTime(localDateTime, validOffsets.get(0), zone);
    }
    if (validOffsets.size() == 0) {
        // Gap: 春季夏令时开始，本地时间不存在
        ZoneOffset offsetAfter = rules.getOffset(localDateTime.plusSeconds(1));
        ZoneOffset offsetBefore = rules.getOffset(localDateTime.minusSeconds(1));
        return new ZonedDateTime(localDateTime.plusSeconds(offsetAfter.getTotalSeconds() - offsetBefore.getTotalSeconds()),
                                offsetAfter, zone);
    }
    // Overlap: 秋季夏令时结束，两个有效偏移
    if (preferredOffset != null && validOffsets.contains(preferredOffset)) {
        return new ZonedDateTime(localDateTime, preferredOffset, zone);
    }
    return new ZonedDateTime(localDateTime, validOffsets.get(0), zone);
}
```

**处理三种情况**:

1. **Normal** (绝大多数时间): 唯一偏移
2. **Gap** (春季时钟前跳): 时间不存在，自动调整
3. **Overlap** (秋季时钟回拨): 使用首选偏移或早期偏移

### ofInstant() - 从时间戳创建

```java
public static ZonedDateTime ofInstant(Instant instant, ZoneId zone) {
    Objects.requireNonNull(instant, "instant");
    Objects.requireNonNull(zone, "zone");
    return create(instant.getEpochSecond(), instant.getNano(), zone);
}

private static ZonedDateTime create(long epochSecond, int nanoOfSecond, ZoneId zone) {
    ZoneRules rules = zone.getRules();
    ZoneOffset offset = rules.getOffset(epochSecond);
    LocalDateTime localDateTime = LocalDateTime.ofEpochSecond(epochSecond, nanoOfSecond, offset);
    return new ZonedDateTime(localDateTime, offset, zone);
}
```

**转换流程**:
1. 从 `Instant` 获取纪元秒
2. 根据 `ZoneRules` 获取偏移
3. 转换为 `LocalDateTime`

---

## 4. 核心方法

### getZone() / getOffset()

```java
@Override
public ZoneId getZone() {
    return zone;
}

public ZoneOffset getOffset() {
    return offset;
}
```

### withZoneSameInstant() - 保留瞬间，转换时区

```java
public ZonedDateTime withZoneSameInstant(ZoneId newZone) {
    Objects.requireNonNull(newZone, "newZone");
    return this.zone.equals(newZone) ? this :
        create(dateTime.toEpochSecond(offset), dateTime.getNano(), newZone);
}
```

**使用场景**: 全球会议时间转换

```java
ZonedDateTime shanghai = ZonedDateTime.of(
    LocalDateTime.of(2024, 3, 20, 14, 0),
    ZoneId.of("Asia/Shanghai")
);  // 2024-03-20T14:00+08:00

// 同一瞬间，纽约时间
ZonedDateTime newyork = shanghai.withZoneSameInstant(ZoneId.of("America/New_York"));
// 2024-03-20T02:00-04:00 (凌晨 2 点)
```

### withZoneSameLocal() - 保留本地时间，改变时区

```java
public ZonedDateTime withZoneSameLocal(ZoneId newZone) {
    Objects.requireNonNull(newZone, "newZone");
    return this.zone.equals(newZone) ? this :
        ofLocal(dateTime, newZone, offset);
}
```

**使用场景**: 改变时区但保持本地时间

```java
ZonedDateTime shanghai = ZonedDateTime.of(
    LocalDateTime.of(2024, 3, 20, 14, 0),
    ZoneId.of("Asia/Shanghai")
);  // 2024-03-20T14:00+08:00

// 相同本地时间，东京时区
ZonedDateTime tokyo = shanghai.withZoneSameLocal(ZoneId.of("Asia/Tokyo"));
// 2024-03-20T14:00+09:00 (仍然是下午 2 点，但不同瞬间)
```

---

## 5. 时间计算

### plusHours() - 加小时

```java
@Override
public ZonedDateTime plusHours(long hours) {
    return plusWithOverflow(dateTime, hours, 0, 0, 0);
}

private ZonedDateTime plusWithOverflow(LocalDateTime newDateTime, long hours, long minutes,
                                       long seconds, long nanos) {
    // 1. 先加上时间量
    if (minutes == 0 && seconds == 0 && nanos == 0) {
        if (hours == 0) {
            return this;
        }
        newDateTime = newDateTime.plusHours(hours);
    } else {
        newDateTime = newDateTime.plusHours(hours).plusMinutes(minutes).plusSeconds(seconds).plusNanos(nanos);
    }

    // 2. 重新计算偏移 (可能因夏令时转换而变化)
    ZoneRules rules = zone.getRules();
    ZoneOffset newOffset = rules.getOffset(newDateTime);

    // 3. 处理 Gap 和 Overlap
    if (!newOffset.equals(offset)) {
        ZoneOffset offsetAtStart = rules.getOffset(newDateTime.minusHours(1));
        ZoneOffset offsetAtEnd = rules.getOffset(newDateTime.plusHours(1));
        if (!offsetAtStart.equals(offsetAtEnd)) {
            // 处理转换边界
            newDateTime = newDateTime.withOffsetSameInstant(offset, newOffset);
        }
    }

    return new ZonedDateTime(newDateTime, newOffset, zone);
}
```

**关键**: 跨越夏令时转换时，偏移量会自动调整

### plusDays() / plusWeeks() / plusMonths() / plusYears()

类似实现，最终调用 `plusWithOverflow()`

---

## 6. 方法引用优化

### from() - 静态工厂

```java
public static ZonedDateTime from(TemporalAccessor temporal) {
    if (temporal instanceof ZonedDateTime) {
        return (ZonedDateTime) temporal;
    }
    Objects.requireNonNull(temporal, "temporal");
    try {
        ZoneId zone = ZoneId.from(temporal);
        if (temporal.isSupported(INSTANT_SECONDS)) {
            long epochSecond = temporal.getLong(INSTANT_SECONDS);
            int nanoOfSecond = temporal.get(NANO_OF_SECOND);
            return create(epochSecond, nanoOfSecond, zone);
        } else {
            LocalDateTime ldt = LocalDateTime.from(temporal);
            return ofLocal(ldt, zone, null);
        }
    } catch (DateTimeException ex) {
        throw new DateTimeException("Unable to obtain ZonedDateTime from TemporalAccessor: " +
            temporal + " of type " + temporal.getClass().getName(), ex);
    }
}
```

---

## 7. 序列化机制

### writeReplace()

```java
private Object writeReplace() {
    return new Ser(Ser.ZONE_DATE_TIME_TYPE, this);
}

private void readObject(ObjectInputStream s) throws InvalidObjectException {
    throw new InvalidObjectException("Deserialization via serialization delegate");
}
```

### 序列化格式

```
// 写入
out.writeByte(3);  // ZonedDateTime 类型
// LocalDateTime
dateTime.writeExternal(out);
// ZoneOffset
Ser.writeOffset(offset, out);
// ZoneId
out.writeUTF(zone.getId());
```

---

## 8. 性能特性

### 对象复用

```java
// 相同偏移的 ZoneOffset 被缓存
ZoneOffset offset = ZoneOffset.ofHours(8);
ZonedDateTime zdt1 = ZonedDateTime.of(LocalDateTime.now(), ZoneId.of("Asia/Shanghai"));
ZonedDateTime zdt2 = ZonedDateTime.of(LocalDateTime.now(), ZoneId.of("Asia/Shanghai"));
// offset 字段可能指向同一个 ZoneOffset 实例
```

### 快路优化

```java
public ZonedDateTime withZoneSameInstant(ZoneId newZone) {
    return this.zone.equals(newZone) ? this :
        create(dateTime.toEpochSecond(offset), dateTime.getNano(), newZone);
}

public ZonedDateTime withZoneSameLocal(ZoneId newZone) {
    return this.zone.equals(newZone) ? this :
        ofLocal(dateTime, newZone, offset);
}
```

---

## 9. Gap 和 Overlap 详解

### Gap (春季夏令时开始)

```
2024-03-10 美国东部时间
┌─────────────────────────────────────────────┐
│ 01:00 ──→ 01:59:59 ──→ 03:00 (跳跃!)       │
│   -05:00 (EST)         -04:00 (EDT)         │
│                                             │
│  02:00 - 02:59 不存在!                       │
└─────────────────────────────────────────────┘
```

**行为**:
```java
ZonedDateTime gap = ZonedDateTime.of(
    LocalDateTime.of(2024, 3, 10, 2, 30),  // 不存在的时间!
    ZoneId.of("America/New_York")
);
// 实际结果: 2024-03-10T03:30-04:00
// 自动调整到 3:30 EDT
```

### Overlap (秋季夏令时结束)

```
2024-11-03 美国东部时间
┌─────────────────────────────────────────────┐
│ 01:00 ──→ 01:59:59 ──→ 01:00 (回拨!)       │
│   -04:00 (EDT)         -05:00 (EST)         │
│                                             │
│  01:00 - 01:59 出现两次!                     │
└─────────────────────────────────────────────┘
```

**行为**:
```java
ZonedDateTime overlap = ZonedDateTime.of(
    LocalDateTime.of(2024, 11, 3, 1, 30),
    ZoneId.of("America/New_York")
);
// 默认使用早期偏移: 2024-11-03T01:30-04:00

// 使用首选偏移
ZonedDateTime overlap2 = ZonedDateTime.ofLocal(
    LocalDateTime.of(2024, 11, 3, 1, 30),
    ZoneId.of("America/New_York"),
    ZoneOffset.ofHours(-5)  // 首选 EST
);
// 结果: 2024-11-03T01:30-05:00
```

---

## 10. 使用示例

### 创建

```java
// 当前时间，系统时区
ZonedDateTime now = ZonedDateTime.now();

// 当前时间，指定时区
ZonedDateTime paris = ZonedDateTime.now(ZoneId.of("Europe/Paris"));
ZonedDateTime shanghai = ZonedDateTime.now(ZoneId.of("Asia/Shanghai"));

// 指定日期时间和时区
ZonedDateTime appointment = ZonedDateTime.of(
    LocalDateTime.of(2024, 6, 15, 14, 30),
    ZoneId.of("America/New_York")
);

// 从 Instant 创建
Instant instant = Instant.now();
ZonedDateTime fromInstant = instant.atZone(ZoneId.of("Asia/Tokyo"));
```

### 时区转换

```java
ZonedDateTime meeting = ZonedDateTime.of(
    LocalDateTime.of(2024, 6, 15, 14, 0),
    ZoneId.of("Asia/Shanghai")
);

// 转换为其他时区 (保留瞬间)
ZonedDateTime inLondon = meeting.withZoneSameInstant(ZoneId.of("Europe/London"));
ZonedDateTime inNewYork = meeting.withZoneSameInstant(ZoneId.of("America/New_York"));
ZonedDateTime inTokyo = meeting.withZoneSameInstant(ZoneId.of("Asia/Tokyo"));

System.out.println("上海: " + meeting);      // 2024-06-15T14:00+08:00
System.out.println("伦敦: " + inLondon);      // 2024-06-15T07:00+01:00
System.out.println("纽约: " + inNewYork);     // 2024-06-15T02:00-04:00
System.out.println("东京: " + inTokyo);       // 2024-06-15T15:00+09:00
```

### 计算

```java
ZonedDateTime now = ZonedDateTime.now(ZoneId.of("America/New_York"));

// 加减时间
ZonedDateTime tomorrow = now.plusDays(1);
ZonedDateTime nextWeek = now.plusWeeks(1);
ZonedDateTime nextMonth = now.plusMonths(1);
ZonedDateTime in2Hours = now.plusHours(2);

// 修改字段
ZonedDateTime nextYear = now.withYear(2025);
ZonedDateTime firstOfMonth = now.withDayOfMonth(1);
ZonedDateTime atNoon = now.with(LocalTime.of(12, 0));

// 调整器
ZonedDateTime firstMondayOfNextMonth = now
    .plusMonths(1)
    .with(TemporalAdjusters.firstInMonth(DayOfWeek.MONDAY));
```

### 与 Instant 互转

```java
// ZonedDateTime → Instant
ZonedDateTime zdt = ZonedDateTime.now(ZoneId.of("Asia/Shanghai"));
Instant instant = zdt.toInstant();

// Instant → ZonedDateTime
ZonedDateTime back = instant.atZone(ZoneId.of("America/New_York"));
```

---

## 11. 与 OffsetDateTime 区别

| 特性 | ZonedDateTime | OffsetDateTime |
|------|---------------|----------------|
| 时区 | 完整时区 (可变偏移) | 固定偏移 |
| 夏令时 | ✅ 自动处理 | ❌ 不处理 |
| 数据库存储 | 不推荐 | ✅ 推荐 |
| 时区转换 | ✅ 支持 | ⚠️ 需手动处理 |

**选择建议**:
- 使用 `ZonedDateTime`: 用户界面、日程安排
- 使用 `OffsetDateTime`: 数据库存储、API 传输

---

## 12. 相关文档

- [ZoneId 实现](../zone/zoneid.md)
- [ZoneOffset 实现](../zone/zoneoffset.md)
- [ZoneRules 实现](../zone/zonerules.md)
- [OffsetDateTime 实现](../offsetdatetime/README.md)
- [主索引](../README.md)

---

> **更新时间**: 2026-03-20
> **源码版本**: OpenJDK 23
> **文件路径**: `src/java.base/share/classes/java/time/ZonedDateTime.java`
