# ZoneRules 源码分析

> java.time.zone.ZoneRules 的完整实现分析

---

## 类声明

```java
public final class ZoneRules implements Serializable {
```

**关键设计决策**:
- `final` - 不可继承
- `Serializable` - 支持序列化
- **不可变且线程安全**

---

## 字段存储

```java
/**
 * The transitions between standard offsets (epoch seconds), sorted.
 */
private final long[] standardTransitions;

/**
 * The standard offsets.
 */
private final ZoneOffset[] standardOffsets;

/**
 * The transitions between instants (epoch seconds), sorted.
 */
private final long[] savingsInstantTransitions;

/**
 * The transitions between local date-times, sorted.
 */
private final LocalDateTime[] savingsLocalTransitions;

/**
 * The wall offsets.
 */
private final ZoneOffset[] wallOffsets;

/**
 * The last rule.
 */
private final ZoneOffsetTransitionRule[] lastRules;

/**
 * The map of recent transitions.
 */
private final transient ConcurrentMap<Integer, ZoneOffsetTransition[]> lastRulesCache;
```

**内存布局**:
- `standardTransitions` - 标准偏移转换时间点
- `standardOffsets` - 标准偏移量数组
- `savingsInstantTransitions` - 夏令时转换时间点
- `savingsLocalTransitions` - 夏令时转换本地时间
- `wallOffsets` - 墙上时钟偏移量
- `lastRules` - 未来转换规则 (最多 16 个)
- `lastRulesCache` - 转换缓存 (2100 年前)

---

## 常量定义

```java
/**
 * The last year to have its transitions cached.
 */
private static final int LAST_CACHED_YEAR = 2100;

/**
 * The number of days in a 400 year cycle.
 */
private static final int DAYS_PER_CYCLE = 146097;

/**
 * The number of days from year zero to year 1970.
 */
private static final long DAYS_0000_TO_1970 = (DAYS_PER_CYCLE * 5L) - (30L * 365L + 7L);
```

**缓存策略**:
- 2100 年前的转换会被缓存
- 2100 年后按需计算

---

## 工厂方法

### of(ZoneOffset) - 固定偏移规则

```java
public static ZoneRules of(ZoneOffset offset) {
    Objects.requireNonNull(offset, "offset");
    return new ZoneRules(offset);
}

private ZoneRules(ZoneOffset offset) {
    this.standardOffsets = new ZoneOffset[1];
    this.standardOffsets[0] = offset;
    this.standardTransitions = EMPTY_LONG_ARRAY;
    this.savingsInstantTransitions = EMPTY_LONG_ARRAY;
    this.savingsLocalTransitions = EMPTY_LDT_ARRAY;
    this.wallOffsets = standardOffsets;
    this.lastRules = EMPTY_LASTRULES;
    this.lastRulesCache = null;
}
```

**特点**:
- 单一偏移，永不变化
- 无转换规则
- 适用于 UTC、固定偏移时区

### of(...) - 完整规则

```java
public static ZoneRules of(ZoneOffset baseStandardOffset,
                           ZoneOffset baseWallOffset,
                           List<ZoneOffsetTransition> standardOffsetTransitionList,
                           List<ZoneOffsetTransition> transitionList,
                           List<ZoneOffsetTransitionRule> lastRules) {
    Objects.requireNonNull(baseStandardOffset, "baseStandardOffset");
    Objects.requireNonNull(baseWallOffset, "baseWallOffset");
    Objects.requireNonNull(standardOffsetTransitionList, "standardOffsetTransitionList");
    Objects.requireNonNull(transitionList, "transitionList");
    Objects.requireNonNull(lastRules, "lastRules");
    return new ZoneRules(baseStandardOffset, baseWallOffset,
                        standardOffsetTransitionList, transitionList, lastRules);
}
```

**参数说明**:
- `baseStandardOffset` - 初始标准偏移
- `baseWallOffset` - 初始墙上时钟偏移
- `standardOffsetTransitionList` - 标准偏移转换历史
- `transitionList` - 夏令时转换历史
- `lastRules` - 未来转换规则 (最多 16 个)

---

## 核心方法

### isFixedOffset() - 检查是否固定偏移

```java
public boolean isFixedOffset() {
    return standardOffsets[0].equals(wallOffsets[0]) &&
           standardTransitions.length == 0 &&
           savingsInstantTransitions.length == 0 &&
           lastRules.length == 0;
}
```

**判断条件**:
- 标准偏移等于墙上时钟偏移
- 无标准偏移转换
- 无夏令时转换
- 无未来规则

### getOffset(Instant) - 获取时刻偏移

```java
public ZoneOffset getOffset(Instant instant) {
    if (savingsInstantTransitions.length == 0) {
        return wallOffsets[0];
    }
    long epochSec = instant.getEpochSecond();

    // 检查是否使用未来规则
    if (lastRules.length > 0 &&
        epochSec > savingsInstantTransitions[savingsInstantTransitions.length - 1]) {
        int year = findYear(epochSec, wallOffsets[wallOffsets.length - 1]);
        ZoneOffsetTransition[] transArray = findTransitionArray(year);
        ZoneOffsetTransition trans = null;
        for (int i = 0; i < transArray.length; i++) {
            trans = transArray[i];
            if (epochSec < trans.toEpochSecond()) {
                return trans.getOffsetBefore();
            }
        }
        return trans.getOffsetAfter();
    }

    // 使用历史规则 - 二分查找
    int index = Arrays.binarySearch(savingsInstantTransitions, epochSec);
    if (index < 0) {
        index = -index - 2;
    }
    return wallOffsets[index + 1];
}
```

**查找策略**:
1. 无转换 → 返回唯一偏移
2. 超出历史记录 → 使用未来规则
3. 历史范围内 → 二分查找

### getOffset(LocalDateTime) - 获取本地时间偏移

```java
public ZoneOffset getOffset(LocalDateTime localDateTime) {
    Object info = getOffsetInfo(localDateTime);
    if (info instanceof ZoneOffsetTransition) {
        return ((ZoneOffsetTransition) info).getOffsetBefore();
    }
    return (ZoneOffset) info;
}
```

**三种情况**:

| 情况 | 有效偏移数 | 说明 |
|------|-----------|------|
| **Normal** | 1 | 绝大多数时间 |
| **Gap** | 0 | 春季夏令时开始 (时钟前跳) |
| **Overlap** | 2 | 秋季夏令时结束 (时钟回拨) |

### getValidOffsets() - 获取所有有效偏移

```java
public List<ZoneOffset> getValidOffsets(LocalDateTime localDateTime) {
    Object info = getOffsetInfo(localDateTime);
    if (info instanceof ZoneOffsetTransition) {
        return ((ZoneOffsetTransition) info).getValidOffsets();
    }
    return Collections.singletonList((ZoneOffset) info);
}
```

**返回**:
- Normal: 单元素列表
- Gap: 空列表
- Overlap: 两元素列表 (先早期偏移，后晚期偏移)

### getTransition() - 获取转换信息

```java
public ZoneOffsetTransition getTransition(LocalDateTime localDateTime) {
    Object info = getOffsetInfo(localDateTime);
    return (info instanceof ZoneOffsetTransition ? (ZoneOffsetTransition) info : null);
}
```

**返回**:
- Normal: `null`
- Gap/Overlap: `ZoneOffsetTransition` 对象

---

## 夏令时检测

### getDaylightSavings() - 获取夏令时量

```java
public Duration getDaylightSavings(Instant instant) {
    if (isFixedOffset()) {
        return Duration.ZERO;
    }
    ZoneOffset standardOffset = getStandardOffset(instant);
    ZoneOffset actualOffset = getOffset(instant);
    return Duration.ofSeconds(actualOffset.getTotalSeconds() - standardOffset.getTotalSeconds());
}
```

**计算**: 实际偏移 - 标准偏移

### isDaylightSavings() - 检查是否夏令时

```java
public boolean isDaylightSavings(Instant instant) {
    return (getStandardOffset(instant).equals(getOffset(instant)) == false);
}
```

**判断**: 标准偏移 ≠ 实际偏移

---

## 转换查询

### nextTransition() - 下一个转换

```java
public ZoneOffsetTransition nextTransition(Instant instant) {
    if (savingsInstantTransitions.length == 0) {
        return null;
    }
    long epochSec = instant.getEpochSecond();

    // 检查是否在未来规则范围
    if (epochSec >= savingsInstantTransitions[savingsInstantTransitions.length - 1]) {
        if (lastRules.length == 0) {
            return null;
        }
        int year = findYear(epochSec, wallOffsets[wallOffsets.length - 1]);
        ZoneOffsetTransition[] transArray = findTransitionArray(year);
        for (ZoneOffsetTransition trans : transArray) {
            if (epochSec < trans.toEpochSecond()) {
                return trans;
            }
        }
        // 使用下一年第一个转换
        if (year < Year.MAX_VALUE) {
            transArray = findTransitionArray(year + 1);
            return transArray[0];
        }
        return null;
    }

    // 历史范围 - 二分查找
    int index = Arrays.binarySearch(savingsInstantTransitions, epochSec);
    if (index < 0) {
        index = -index - 1;
    } else {
        index += 1;
    }
    return new ZoneOffsetTransition(savingsInstantTransitions[index],
                                    wallOffsets[index], wallOffsets[index + 1]);
}
```

### previousTransition() - 上一个转换

```java
public ZoneOffsetTransition previousTransition(Instant instant) {
    if (savingsInstantTransitions.length == 0) {
        return null;
    }
    long epochSec = instant.getEpochSecond();
    if (instant.getNano() > 0 && epochSec < Long.MAX_VALUE) {
        epochSec += 1;  // 向上取整到秒
    }

    // 检查是否在未来规则范围
    long lastHistoric = savingsInstantTransitions[savingsInstantTransitions.length - 1];
    if (lastRules.length > 0 && epochSec > lastHistoric) {
        ZoneOffset lastHistoricOffset = wallOffsets[wallOffsets.length - 1];
        int year = findYear(epochSec, lastHistoricOffset);
        ZoneOffsetTransition[] transArray = findTransitionArray(year);
        for (int i = transArray.length - 1; i >= 0; i--) {
            if (epochSec > transArray[i].toEpochSecond()) {
                return transArray[i];
            }
        }
        // 使用前一年最后一个转换
        int lastHistoricYear = findYear(lastHistoric, lastHistoricOffset);
        if (--year > lastHistoricYear) {
            transArray = findTransitionArray(year);
            return transArray[transArray.length - 1];
        }
    }

    // 历史范围 - 二分查找
    int index = Arrays.binarySearch(savingsInstantTransitions, epochSec);
    if (index < 0) {
        index = -index - 1;
    }
    if (index <= 0) {
        return null;
    }
    return new ZoneOffsetTransition(savingsInstantTransitions[index - 1],
                                    wallOffsets[index - 1], wallOffsets[index]);
}
```

---

## 内部辅助方法

### findTransitionArray() - 查找年份转换

```java
private ZoneOffsetTransition[] findTransitionArray(int year) {
    Integer yearObj = year;
    ZoneOffsetTransition[] transArray = lastRulesCache.get(yearObj);
    if (transArray != null) {
        return transArray;
    }

    ZoneOffsetTransitionRule[] ruleArray = lastRules;
    transArray = new ZoneOffsetTransition[ruleArray.length];
    for (int i = 0; i < ruleArray.length; i++) {
        transArray[i] = ruleArray[i].createTransition(year);
    }

    if (year < LAST_CACHED_YEAR) {
        lastRulesCache.putIfAbsent(yearObj, transArray);
    }
    return transArray;
}
```

**缓存策略**:
- 2100 年前: 缓存转换数组
- 2100 年后: 不缓存 (避免无限增长)

### findYear() - 计算年份

```java
private int findYear(long epochSecond, ZoneOffset offset) {
    long localSecond = epochSecond + offset.getTotalSeconds();
    long zeroDay = Math.floorDiv(localSecond, 86400) + DAYS_0000_TO_1970;

    // 调整到 3月为基础年
    zeroDay -= 60;

    long adjust = 0;
    if (zeroDay < 0) {
        long adjustCycles = (zeroDay + 1) / DAYS_PER_CYCLE - 1;
        adjust = adjustCycles * 400;
        zeroDay += -adjustCycles * DAYS_PER_CYCLE;
    }

    long yearEst = (400 * zeroDay + 591) / DAYS_PER_CYCLE;
    long doyEst = zeroDay - (365 * yearEst + yearEst / 4 - yearEst / 100 + yearEst / 400);
    if (doyEst < 0) {
        yearEst--;
        doyEst = zeroDay - (365 * yearEst + yearEst / 4 - yearEst / 100 + yearEst / 400);
    }
    yearEst += adjust;

    if (doyEst >= 306) {
        yearEst++;
    }

    return (int)Math.min(yearEst, Year.MAX_VALUE);
}
```

**算法**: 使用"3月为基础年"简化闰年计算

---

## 序列化机制

### writeExternal() - 压缩存储

```java
void writeExternal(DataOutput out) throws IOException {
    out.writeInt(standardTransitions.length);
    for (long trans : standardTransitions) {
        Ser.writeEpochSec(trans, out);
    }
    for (ZoneOffset offset : standardOffsets) {
        Ser.writeOffset(offset, out);
    }
    // ... 其他字段
}

static void writeEpochSec(long epochSec, DataOutput out) throws IOException {
    // 1825-2300 年间的 15 分钟倍数: 3 字节
    if (epochSec >= -4575744000L && epochSec < 10413792000L && epochSec % 900 == 0) {
        int store = (int) ((epochSec + 4575744000L) / 900);
        out.writeByte((store >>> 16) & 255);
        out.writeByte((store >>> 8) & 255);
        out.writeByte(store & 255);
    } else {
        // 其他: 1 + 8 字节
        out.writeByte(255);
        out.writeLong(epochSec);
    }
}
```

**压缩策略**:
- 常见时间 (1825-2300): 3 字节
- 罕见时间: 9 字节
- 偏移量: 1 或 5 字节

### readExternal() - 反序列化

```java
static ZoneRules readExternal(DataInput in) throws IOException, ClassNotFoundException {
    int stdSize = in.readInt();
    if (stdSize > 1024) {
        throw new InvalidObjectException("Too many transitions");
    }
    // ... 读取并重建对象
    return new ZoneRules(stdTrans, stdOffsets, savTrans, savOffsets, rules);
}
```

**限制**: 最多 1024 个转换 (当前 TZDB 约 203 个)

---

## 性能特性

### 二分查找

```java
int index = Arrays.binarySearch(savingsInstantTransitions, epochSec);
```

**时间复杂度**: O(log n)

### 转换缓存

```java
private final transient ConcurrentMap<Integer, ZoneOffsetTransition[]> lastRulesCache;
```

**缓存策略**:
- 2100 年前: 按年缓存
- 2100 年后: 按需计算
- 使用 `ConcurrentHashMap` 保证线程安全

---

## 使用示例

### 检查夏令时

```java
ZoneId zone = ZoneId.of("America/New_York");
ZoneRules rules = zone.getRules();

Instant now = Instant.now();
if (rules.isDaylightSavings(now)) {
    Duration savings = rules.getDaylightSavings(now);
    System.out.println("夏令时生效，偏移: " + savings);  // PT1H
}
```

### 查找转换

```java
ZoneId zone = ZoneId.of("America/New_York");
ZoneRules rules = zone.getRules();

Instant now = Instant.now();
ZoneOffsetTransition next = rules.nextTransition(now);
if (next != null) {
    System.out.println("下一个转换: " + next);
    System.out.println("时间: " + next.getDateTimeBefore() + " → " + next.getDateTimeAfter());
    System.out.println("偏移: " + next.getOffsetBefore() + " → " + next.getOffsetAfter());
}
```

### 处理 Gap/Overlap

```java
ZoneId zone = ZoneId.of("America/New_York");
ZoneRules rules = zone.getRules();

// 秋季回退时的重叠时间
LocalDateTime overlap = LocalDateTime.of(2024, 11, 3, 1, 30);  // 1:30 AM
List<ZoneOffset> validOffsets = rules.getValidOffsets(overlap);

if (validOffsets.size() > 1) {
    System.out.println("重叠时间，两个有效偏移:");
    for (ZoneOffset offset : validOffsets) {
        System.out.println("  " + offset);
    }
}
```

---

## Gap 和 Overlap 详解

### Gap (春季夏令时开始)

```
2024-03-10 01:59:59 → 2024-03-10 03:00:00
   -05:00                 -04:00
```

**特点**:
- 时钟前跳 1 小时
- 2:00-2:59 不存在
- `getValidOffsets()` 返回空列表

### Overlap (秋季夏令时结束)

```
2024-11-03 01:59:59 → 2024-11-03 01:00:00
   -04:00                 -05:00
```

**特点**:
- 时钟回拨 1 小时
- 1:00-1:59 出现两次
- `getValidOffsets()` 返回两个偏移

---

## 相关文档

- [ZoneId 实现](zoneid.md)
- [ZoneOffset 实现](zoneoffset.md)
- [ZoneOffsetTransition 实现](transition.md)
- [主索引](../index.md)

---

> **更新时间**: 2026-03-20
> **源码版本**: OpenJDK 23
> **文件路径**: `src/java.base/share/classes/java/time/zone/ZoneRules.java`
