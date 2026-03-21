# ZoneOffset 源码分析

> java.time.ZoneOffset 的完整实现分析

---
## 目录

1. [类声明](#1-类声明)
2. [字段存储](#2-字段存储)
3. [常量定义](#3-常量定义)
4. [缓存机制](#4-缓存机制)
5. [工厂方法](#5-工厂方法)
6. [ID 构建算法](#6-id-构建算法)
7. [字段访问方法](#7-字段访问方法)
8. [TemporalAccessor 实现](#8-temporalaccessor-实现)
9. [TemporalAdjuster 实现](#9-temporaladjuster-实现)
10. [比较](#10-比较)
11. [序列化机制](#11-序列化机制)
12. [性能特性](#12-性能特性)
13. [使用示例](#13-使用示例)
14. [与 ZoneId 关系](#14-与-zoneid-关系)
15. [常见偏移速查表](#15-常见偏移速查表)
16. [相关文档](#16-相关文档)

---


## 1. 类声明

```java
@jdk.internal.ValueBased
public final class ZoneOffset
    extends ZoneId
    implements TemporalAccessor, TemporalAdjuster, Comparable<ZoneOffset>, Serializable {
```

**关键设计决策**:
- `final` - 不可继承
- `extends ZoneId` - ZoneId 的两个密封子类之一
- `@jdk.internal.ValueBased` - 基于值的类
- `Comparable<ZoneOffset>` - 可比较排序

---

## 2. 字段存储

```java
/**
 * @serial The total offset in seconds.
 */
private final int totalSeconds;

/**
 * The string form of the time-zone offset.
 */
private final transient String id;

/**
 * The zone rules for an offset will always return this offset. Cache it for efficiency.
 */
@Stable
private transient ZoneRules rules;
```

**内存布局**:
- `int totalSeconds` - 4 字节，总偏移秒数 (-64800 到 +64800)
- `String id` - 引用，延迟初始化
- `ZoneRules rules` - 引用，延迟初始化

**设计优势**:
1. 单一 `int` 存储偏移量，高效紧凑
2. ID 和 Rules 按需计算，减少内存占用
3. `@Stable` 注解允许 JVM 优化

---

## 3. 常量定义

```java
/**
 * The abs maximum seconds.
 */
private static final int MAX_SECONDS = 18 * SECONDS_PER_HOUR;  // 64800

/**
 * The time-zone offset for UTC, with an ID of 'Z'.
 */
public static final ZoneOffset UTC = ZoneOffset.ofTotalSeconds(0);

/**
 * Constant for the minimum supported offset.
 */
public static final ZoneOffset MIN = ZoneOffset.ofTotalSeconds(-MAX_SECONDS);  // -18:00

/**
 * Constant for the maximum supported offset.
 */
public static final ZoneOffset MAX = ZoneOffset.ofTotalSeconds(MAX_SECONDS);   // +18:00
```

**偏移范围**: -18:00 到 +18:00

**为什么是 ±18:00?**
- 2008 年实际世界时区范围: -12:00 到 +14:00
- 预留扩展空间到 ±18:00
- 覆盖所有理论上可能的偏移量

---

## 4. 缓存机制

### QUARTER_CACHE - 15分钟增量缓存

```java
/** Cache of time-zone offset by offset in quarters. */
private static final int SECONDS_PER_QUARTER = 15 * SECONDS_PER_MINUTE;  // 900
private static final AtomicReferenceArray<ZoneOffset> QUARTER_CACHE = new AtomicReferenceArray<>(256);
```

**设计特点**:
- 缓存 15 分钟 (900 秒) 倍数的偏移量
- `AtomicReferenceArray` - 无锁并发安全
- 大小 256 = 72 (负) + 1 (零) + 72 (正) + 111 (未使用)

**索引算法**:
```java
int quarters = totalSeconds / SECONDS_PER_QUARTER;  // -72 到 +72
int key = quarters & 0xff;  // 映射到 0-255
```

**缓存覆盖范围**: -18:00 到 +18:00，每 15 分钟一个

### ID_CACHE - 字符串 ID 缓存

```java
/** Cache of time-zone offset by ID. */
private static final ConcurrentMap<String, ZoneOffset> ID_CACHE = new ConcurrentHashMap<>(16, 0.75f, 4);
```

**用途**: 缓存常用 ID (如 "Z", "+08:00", "-05:00")

**初始化**: "Z" (UTC) 始终在缓存中

---

## 5. 工厂方法

### of(String) - 从字符串解析

```java
public static ZoneOffset of(String offsetId) {
    Objects.requireNonNull(offsetId, "offsetId");
    // "Z" is always in the cache
    ZoneOffset offset = ID_CACHE.get(offsetId);
    if (offset != null) {
        return offset;
    }
    // parse - +h, +hh, +hhmm, +hh:mm, +hhmmss, +hh:mm:ss
    final int hours, minutes, seconds;
    switch (offsetId.length()) {
        case 2:  // +h
            offsetId = offsetId.charAt(0) + "0" + offsetId.charAt(1); // fallthru
        case 3:  // +hh
            hours = parseNumber(offsetId, 1, false);
            minutes = 0;
            seconds = 0;
            break;
        case 5:  // +hh:mm
            hours = parseNumber(offsetId, 1, false);
            minutes = parseNumber(offsetId, 3, false);
            seconds = 0;
            break;
        case 6:  // +hhmm
            hours = parseNumber(offsetId, 1, false);
            minutes = parseNumber(offsetId, 4, true);
            seconds = 0;
            break;
        case 7:  // +hh:mm:ss
            hours = parseNumber(offsetId, 1, false);
            minutes = parseNumber(offsetId, 3, false);
            seconds = parseNumber(offsetId, 5, false);
            break;
        case 9:  // +hhmmss
            hours = parseNumber(offsetId, 1, false);
            minutes = parseNumber(offsetId, 4, true);
            seconds = parseNumber(offsetId, 7, true);
            break;
        default:
            throw new DateTimeException("Invalid ID for ZoneOffset, invalid format: " + offsetId);
    }
    char first = offsetId.charAt(0);
    if (first != '+' && first != '-') {
        throw new DateTimeException("Invalid ID for ZoneOffset, plus/minus not found when expected: " + offsetId);
    }
    if (first == '-') {
        return ofHoursMinutesSeconds(-hours, -minutes, -seconds);
    } else {
        return ofHoursMinutesSeconds(hours, minutes, seconds);
    }
}
```

**支持的格式**:

| 格式 | 示例 | 长度 |
|------|------|------|
| `Z` | `Z` | 1 |
| `+h` | `+8` | 2 |
| `+hh` | `+08` | 3 |
| `+hhmm` | `+0800` | 5 |
| `+hh:mm` | `+08:00` | 6 |
| `+hhmmss` | `+080000` | 7 |
| `+hh:mm:ss` | `+08:00:00` | 9 |

### ofHours() / ofHoursMinutes() / ofHoursMinutesSeconds()

```java
public static ZoneOffset ofHours(int hours) {
    return ofHoursMinutesSeconds(hours, 0, 0);
}

public static ZoneOffset ofHoursMinutes(int hours, int minutes) {
    return ofHoursMinutesSeconds(hours, minutes, 0);
}

public static ZoneOffset ofHoursMinutesSeconds(int hours, int minutes, int seconds) {
    validate(hours, minutes, seconds);
    int totalSeconds = totalSeconds(hours, minutes, seconds);
    return ofTotalSeconds(totalSeconds);
}
```

**验证规则**:
- 小时: -18 到 +18
- 分钟: -59 到 +59
- 秒: -59 到 +59
- 符号必须一致 (正数或负数)

### ofTotalSeconds() - 从总秒数创建

```java
public static ZoneOffset ofTotalSeconds(int totalSeconds) {
    if (totalSeconds < -MAX_SECONDS || totalSeconds > MAX_SECONDS) {
        throw new DateTimeException("Zone offset not in valid range: -18:00 to +18:00");
    }
    int quarters = totalSeconds / SECONDS_PER_QUARTER;
    if (totalSeconds - quarters * SECONDS_PER_QUARTER == 0) {
        // quarters range from -72 to 72, & 0xff maps them to 0-72 and 184-255.
        int key = quarters & 0xff;
        ZoneOffset result = QUARTER_CACHE.getOpaque(key);
        if (result == null) {
            result = new ZoneOffset(totalSeconds);
            var existing = QUARTER_CACHE.compareAndExchange(key, null, result);
            if (existing != null) {
                result = existing;
            }
            ID_CACHE.putIfAbsent(result.getId(), result);
        }
        return result;
    } else {
        return new ZoneOffset(totalSeconds);
    }
}
```

**缓存策略**:
- 15 分钟倍数的偏移 → 使用缓存
- 其他偏移 → 创建新对象
- `compareAndExchange` - 无锁线程安全

---

## 6. ID 构建算法

### buildId() - 生成标准化 ID

```java
private static String buildId(int totalSeconds) {
    if (totalSeconds == 0) {
        return "Z";
    } else {
        int absTotalSeconds = Math.abs(totalSeconds);
        StringBuilder buf = new StringBuilder();
        int absHours = absTotalSeconds / SECONDS_PER_HOUR;
        int absMinutes = (absTotalSeconds / SECONDS_PER_MINUTE) % MINUTES_PER_HOUR;
        buf.append(totalSeconds < 0 ? '-' : '+');
        DecimalDigits.appendPair(buf, absHours);
        buf.append(':');
        DecimalDigits.appendPair(buf, absMinutes);
        int absSeconds = absTotalSeconds % SECONDS_PER_MINUTE;
        if (absSeconds != 0) {
            buf.append(':');
            DecimalDigits.appendPair(buf, absSeconds);
        }
        return buf.toString();
    }
}
```

**输出格式**:

| 总秒数 | ID |
|--------|-----|
| 0 | `Z` |
| 28800 | `+08:00` |
| -3600 | `-01:00` |
| 34200 | `+09:30` |
| 34245 | `+09:30:45` |

---

## 7. 字段访问方法

```java
/**
 * Gets the total zone offset in seconds.
 */
public int getTotalSeconds() {
    return totalSeconds;
}

/**
 * Gets the normalized zone offset ID.
 */
@Override
public String getId() {
    return id;
}

/**
 * Gets the associated time-zone rules.
 */
@Override
public ZoneRules getRules() {
    ZoneRules rules = this.rules;
    if (rules == null) {
        rules = this.rules = ZoneRules.of(this);
    }
    return rules;
}
```

**延迟初始化**:
- `id` 在构造时计算
- `rules` 首次访问时创建，固定返回此偏移

---

## 8. TemporalAccessor 实现

### isSupported()

```java
@Override
public boolean isSupported(TemporalField field) {
    if (field instanceof ChronoField) {
        return field == OFFSET_SECONDS;
    }
    return field != null && field.isSupportedBy(this);
}
```

**支持的字段**: 仅 `OFFSET_SECONDS`

### get() / getLong()

```java
@Override
public int get(TemporalField field) {
    if (field == OFFSET_SECONDS) {
        return totalSeconds;
    } else if (field instanceof ChronoField) {
        throw new UnsupportedTemporalTypeException("Unsupported field: " + field);
    }
    return range(field).checkValidIntValue(getLong(field), field);
}

@Override
public long getLong(TemporalField field) {
    if (field == OFFSET_SECONDS) {
        return totalSeconds;
    } else if (field instanceof ChronoField) {
        throw new UnsupportedTemporalTypeException("Unsupported field: " + field);
    }
    return field.getFrom(this);
}
```

---

## 9. TemporalAdjuster 实现

```java
@Override
public Temporal adjustInto(Temporal temporal) {
    return temporal.with(OFFSET_SECONDS, totalSeconds);
}
```

**使用示例**:
```java
ZonedDateTime now = ZonedDateTime.now();
ZonedDateTime utc = now.with(ZoneOffset.UTC);
// 等价于
ZonedDateTime utc = ZoneOffset.UTC.adjustInto(now);
```

---

## 10. 比较

### compareTo()

```java
@Override
public int compareTo(ZoneOffset other) {
    // abs(totalSeconds) <= MAX_SECONDS, so no overflow can happen here
    return other.totalSeconds - totalSeconds;
}
```

**排序顺序**: 从东到西 (降序)
- `+14:00` 最小
- `Z` (UTC) 中间
- `-18:00` 最大

### equals() / hashCode()

```java
@Override
public boolean equals(Object obj) {
    if (this == obj) {
        return true;
    }
    if (obj instanceof ZoneOffset) {
        return totalSeconds == ((ZoneOffset) obj).totalSeconds;
    }
    return false;
}

@Override
public int hashCode() {
    return totalSeconds;
}
```

**相等性**: 基于总秒数，缓存对象和新建对象相等

---

## 11. 序列化机制

### 压缩存储

```java
void writeExternal(DataOutput out) throws IOException {
    final int offsetSecs = totalSeconds;
    int offsetByte = offsetSecs % 900 == 0 ? offsetSecs / 900 : 127;  // compress to -72 to +72
    out.writeByte(offsetByte);
    if (offsetByte == 127) {
        out.writeInt(offsetSecs);
    }
}

static ZoneOffset readExternal(DataInput in) throws IOException {
    int offsetByte = in.readByte();
    return (offsetByte == 127
            ? ZoneOffset.ofTotalSeconds(in.readInt())
            : ZoneOffset.ofTotalSeconds(offsetByte * 900));
}
```

**压缩算法**:
- 15 分钟倍数 (900 秒): 存储为单字节 (-72 到 +72)
- 其他偏移: 存储字节 127 + 4 字节 int

**节省空间**:
- 常用偏移: 1 字节
- 罕见偏移: 5 字节

---

## 12. 性能特性

### 缓存命中率

```java
// 以下调用返回同一个缓存对象
ZoneOffset z1 = ZoneOffset.of("Z");
ZoneOffset z2 = ZoneOffset.ofTotalSeconds(0);
ZoneOffset z3 = ZoneOffset.UTC;
// z1 == z2 == z3

// 15 分钟倍数也被缓存
ZoneOffset o1 = ZoneOffset.of("+08:00");
ZoneOffset o2 = ZoneOffset.ofHours(8);
ZoneOffset o3 = ZoneOffset.ofHoursMinutes(8, 0);
// o1 == o2 == o3
```

### 内存效率

| 类型 | 大小 |
|------|------|
| 单个 ZoneOffset | ~24 字节 (头 + int + 引用) |
| QUARTER_CACHE | ~2 KB (145 个对象) |
| ID_CACHE | 动态增长 |

### 计算效率

- `getTotalSeconds()`: 直接字段读取
- `getId()`: 直接返回缓存的 ID
- `getRules()`: 单次延迟初始化
- `equals()`: 单次 int 比较

---

## 13. 使用示例

### 创建偏移

```java
// UTC
ZoneOffset utc = ZoneOffset.UTC;
ZoneOffset utc2 = ZoneOffset.of("Z");
ZoneOffset utc3 = ZoneOffset.ofTotalSeconds(0);

// 正偏移
ZoneOffset beijing = ZoneOffset.of("+08:00");
ZoneOffset tokyo = ZoneOffset.ofHours(9);
ZoneOffset india = ZoneOffset.ofHoursMinutesSeconds(5, 30, 0);

// 负偏移
ZoneOffset ny = ZoneOffset.of("-05:00");
ZoneOffset la = ZoneOffset.ofHours(-8);
```

### 转换时间

```java
Instant instant = Instant.now();

// 转换为带偏移的时间
OffsetDateTime utcTime = instant.atOffset(ZoneOffset.UTC);
OffsetDateTime beijingTime = instant.atOffset(ZoneOffset.of("+08:00"));

// 计算时差
ZoneOffset offset1 = ZoneOffset.of("+08:00");
ZoneOffset offset2 = ZoneOffset.of("-05:00");
int diffHours = (offset1.getTotalSeconds() - offset2.getTotalSeconds()) / 3600;  // 13
```

### 验证偏移

```java
// 检查范围
try {
    ZoneOffset invalid = ZoneOffset.ofHours(19);  // 超出 ±18
} catch (DateTimeException e) {
    // "Zone offset hours not in valid range: value 19 is not in the range -18 to 18"
}

// 检查符号一致性
try {
    ZoneOffset invalid = ZoneOffset.ofHoursMinutesSeconds(1, -30, 0);
} catch (DateTimeException e) {
    // "Zone offset minutes and seconds must be positive because hours is positive"
}
```

---

## 14. 与 ZoneId 关系

```java
ZoneId zone1 = ZoneId.of("Z");           // 返回 ZoneOffset
ZoneId zone2 = ZoneId.of("+08:00");      // 返回 ZoneOffset
ZoneId zone3 = ZoneId.of("UTC");         // 返回 ZoneRegion

// ZoneId.normalized() 将固定偏移转换为 ZoneOffset
ZoneId zone = ZoneId.of("UTC");
ZoneOffset offset = (ZoneOffset) zone.normalized();  // Z
```

---

## 15. 常见偏移速查表

| 地区 | 偏移 | 代码 |
|------|------|------|
| UTC | 00:00 | `ZoneOffset.UTC` |
| 北京 | +08:00 | `ZoneOffset.ofHours(8)` |
| 东京 | +09:00 | `ZoneOffset.ofHours(9)` |
| 印度 | +05:30 | `ZoneOffset.ofHoursMinutes(5, 30)` |
| 悉尼 | +10:00/11:00 | `ZoneId.of("Australia/Sydney")` |
| 伦敦 | +00:00/+01:00 | `ZoneId.of("Europe/London")` |
| 纽约 | -05:00/-04:00 | `ZoneId.of("America/New_York")` |
| 洛杉矶 | -08:00/-07:00 | `ZoneId.of("America/Los_Angeles")` |

**注意**: 有夏令时的地区应使用 `ZoneId` 而非 `ZoneOffset`

---

## 16. 相关文档

- [ZoneId 实现](zoneid.md)
- [ZoneRules 实现](zonerules.md)
- [OffsetDateTime 实现](../offsetdatetime/index.md)
- [主索引](../index.md)

---

> **更新时间**: 2026-03-20
> **源码版本**: OpenJDK 23
> **文件路径**: `src/java.base/share/classes/java/time/ZoneOffset.java`
