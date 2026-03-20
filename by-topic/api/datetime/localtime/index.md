# LocalTime 源码分析

> java.time.LocalTime 的完整实现分析

---

## 类声明

```java
@jdk.internal.ValueBased
public final class LocalTime
    implements Temporal, TemporalAdjuster, Comparable<LocalTime>, Serializable {
```

**关键设计决策**:
- `final` - 不可继承
- `@jdk.internal.ValueBased` - 基于值的类
- `Comparable<LocalTime>` - 可比较排序
- `Serializable` - 支持序列化

---

## 字段存储

```java
/**
 * @serial The hour.
 */
private final byte hour;

/**
 * @serial The minute.
 */
private final byte minute;

/**
 * @serial The second.
 */
private final byte second;

/**
 * @serial The nanosecond.
 */
private final int nano;
```

**内存布局**:
- `byte hour` - 1 字节，小时 (0-23)
- `byte minute` - 1 字节，分钟 (0-59)
- `byte second` - 1 字节，秒 (0-59)
- `int nano` - 4 字节，纳秒 (0-999,999,999)
- **总计**: 7 字节 + 对象头

**设计优势**:
1. 使用 `byte` 存储时分秒，节省空间
2. 所有字段 `final`，保证不可变性
3. 纳秒精度支持

---

## 缓存优化

### 小时缓存

```java
/**
 * Constants for the local time of each hour.
 */
private static final LocalTime[] HOURS = new LocalTime[24];

static {
    for (int i = 0; i < HOURS.length; i++) {
        HOURS[i] = new LocalTime(i, 0, 0, 0);
    }
    MIDNIGHT = HOURS[0];
    NOON = HOURS[12];
    MIN = HOURS[0];
    MAX = new LocalTime(23, 59, 59, 999_999_999);
}
```

**性能优化**:
```java
public static LocalTime of(int hour, int minute) {
    HOUR_OF_DAY.checkValidValue(hour);
    if (minute == 0) {
        return HOURS[hour]; // for performance - 返回缓存对象
    }
    MINUTE_OF_HOUR.checkValidValue(minute);
    return new LocalTime(hour, minute, 0, 0);
}

private static LocalTime create(int hour, int minute, int second, int nanoOfSecond) {
    if ((minute | second | nanoOfSecond) == 0) {
        return HOURS[hour]; // 返回缓存对象，避免创建
    }
    return new LocalTime(hour, minute, second, nanoOfSecond);
}
```

**设计**:
- 预创建 24 个整点对象 (00:00, 01:00, ..., 23:00)
- 常用时间 `MIDNIGHT`, `NOON` 直接引用缓存
- `of()` 和 `create()` 方法优先返回缓存
- 减少对象分配，降低 GC 压力

---

## 工厂方法

### of() - 创建时间

```java
public static LocalTime of(int hour, int minute) {
    HOUR_OF_DAY.checkValidValue(hour);
    if (minute == 0) {
        return HOURS[hour]; // for performance
    }
    MINUTE_OF_HOUR.checkValidValue(minute);
    return new LocalTime(hour, minute, 0, 0);
}

public static LocalTime of(int hour, int minute, int second) {
    HOUR_OF_DAY.checkValidValue(hour);
    if ((minute | second) == 0) {
        return HOURS[hour]; // for performance
    }
    MINUTE_OF_HOUR.checkValidValue(minute);
    SECOND_OF_MINUTE.checkValidValue(second);
    return new LocalTime(hour, minute, second, 0);
}

public static LocalTime of(int hour, int minute, int second, int nanoOfSecond) {
    HOUR_OF_DAY.checkValidValue(hour);
    MINUTE_OF_HOUR.checkValidValue(minute);
    SECOND_OF_MINUTE.checkValidValue(second);
    NANO_OF_SECOND.checkValidValue(nanoOfSecond);
    return create(hour, minute, second, nanoOfSecond);
}
```

**重载方法**:
- `of(hour, minute)` - 时分，秒和纳秒为 0
- `of(hour, minute, second)` - 时分秒，纳秒为 0
- `of(hour, minute, second, nanoOfSecond)` - 完整时间

### ofSecondOfDay() - 从一天的第几秒

```java
public static LocalTime ofSecondOfDay(long secondOfDay) {
    SECOND_OF_DAY.checkValidValue(secondOfDay);
    int hours = (int) (secondOfDay / SECONDS_PER_HOUR);
    secondOfDay -= hours * SECONDS_PER_HOUR;
    int minutes = (int) (secondOfDay / SECONDS_PER_MINUTE);
    secondOfDay -= minutes * SECONDS_PER_MINUTE;
    return create(hours, minutes, (int) secondOfDay, 0);
}
```

### ofNanoOfDay() - 从一天的第几纳秒

```java
public static LocalTime ofNanoOfDay(long nanoOfDay) {
    NANO_OF_DAY.checkValidValue(nanoOfDay);
    int hours = (int) (nanoOfDay / NANOS_PER_HOUR);
    nanoOfDay -= hours * NANOS_PER_HOUR;
    int minutes = (int) (nanoOfDay / NANOS_PER_MINUTE);
    nanoOfDay -= minutes * NANOS_PER_MINUTE;
    int seconds = (int) (nanoOfDay / NANOS_PER_SECOND);
    nanoOfDay -= seconds * NANOS_PER_SECOND;
    return create(hours, minutes, seconds, (int) nanoOfDay);
}
```

---

## 字段访问方法

```java
public int getHour() {
    return hour;
}

public int getMinute() {
    return minute;
}

public int getSecond() {
    return second;
}

public int getNano() {
    return nano;
}
```

**性能优化**:
- 所有方法直接返回字段值，无计算开销
- 无需类型转换（byte → int 自动提升）

---

## 时间计算

### plusHours() - 加小时

```java
public LocalTime plusHours(long hoursToAdd) {
    return plusWithOverflow(this.hour + hoursToAdd, 0, 0);
}

private LocalTime plusWithOverflow(long newHour, long newMinute, long newSecond) {
    // 滚动处理
    if ((newHour | newMinute | newSecond) == 0) {
        return HOURS[0];
    }
    if (newHour >= 0 && newHour < 24) {
        return create((int) newHour, (int) newMinute, (int) newSecond, 0);
    }
    long totalDecaNanos = Math.multiplyExact(newHour, 36_000_000_000L);
    totalDecaNanos = Math.addExact(totalDecaNanos, Math.multiplyExact(newMinute, 600_000_000L));
    totalDecaNanos = Math.addExact(totalDecaNanos, Math.multiplyExact(newSecond, 1_000_000_000L));
    int hour = (int) ((totalDecaNanos / (36_000_000_000L % 864000000000L)) % 24);
    int minute = (int) ((totalDecaNanos / 600_000_000L) % 60);
    int second = (int) ((totalDecaNanos / 1_000_000_000L) % 60);
    return create(hour, minute, second, 0);
}
```

**实现细节**:
1. 使用 `Math.addExact()` 防止溢出
2. 滚动处理跨日情况
3. 转换为纳秒计算，再转回时分秒

### plusMinutes() / plusSeconds() / plusNanos()

类似实现模式，最终调用 `plusWithOverflow()` 统一处理。

---

## 时间比较

```java
@Override
public int compareTo(LocalTime other) {
    int compare = Integer.compare(this.hour, other.hour);
    if (compare == 0) {
        compare = Integer.compare(this.minute, other.minute);
        if (compare == 0) {
            compare = Integer.compare(this.second, other.second);
            if (compare == 0) {
                compare = Integer.compare(this.nano, other.nano);
            }
        }
    }
    return compare;
}

public boolean isBefore(LocalTime other) {
    return compareTo(other) < 0;
}

public boolean isAfter(LocalTime other) {
    return compareTo(other) > 0;
}
```

**比较策略**:
- 按小时 → 分钟 → 秒 → 纳秒 顺序比较
- 短路优化，一旦确定结果立即返回

---

## 时间调整

```java
public LocalTime withHour(int hour) {
    if (this.hour == hour) {
        return this;
    }
    HOUR_OF_DAY.checkValidValue(hour);
    return create(hour, minute, second, nano);
}

public LocalTime withMinute(int minute) {
    if (this.minute == minute) {
        return this;
    }
    MINUTE_OF_HOUR.checkValidValue(minute);
    return create(hour, minute, second, nano);
}
```

**不变性保证**:
- 值相同时返回 `this`，避免创建新对象
- 值不同时创建新对象，原对象不变

---

## 截断操作

```java
public LocalTime truncatedTo(TemporalUnit unit) {
    if (unit == ChronoUnit.NANOS) {
        return this;
    }
    Duration unitDur = unit.getDuration();
    if (unitDur.getSeconds() > SECONDS_PER_DAY) {
        throw new UnsupportedTemporalTypeException("Unit is too large to be used for truncation");
    }
    long dur = unitDur.toNanos();
    if ((NANOS_PER_DAY % dur) != 0) {
        throw new UnsupportedTemporalTypeException("Unit must divide into a standard day without remainder");
    }
    long nod = toNanoOfDay();
    return ofNanoOfDay((nod / dur) * dur);
}
```

**使用示例**:
```java
LocalTime time = LocalTime.of(12, 30, 45, 123_456_789);

// 截断到分钟
LocalTime truncated = time.truncatedTo(ChronoUnit.MINUTES);  // 12:30

// 截断到小时
LocalDate truncatedHour = time.truncatedTo(ChronoUnit.HOURS);  // 12:00
```

---

## 性能特性

### 对象复用

```java
// 以下调用都返回同一个缓存对象
LocalTime t1 = LocalTime.of(12, 0);
LocalTime t2 = LocalTime.of(12, 0, 0);
LocalTime t3 = LocalTime.NOON;  // 引用 HOURS[12]
// t1 == t2 == t3 为 true
```

### 快路优化

1. **值相同时返回 this**
2. **整点时间返回缓存**
3. **直接字段访问，无计算**

### 内存效率

- 单个 LocalTime 对象仅占用 ~24 字节（12 字节头 + 7 字节数据 + 对齐）
- 24 个缓存对象共占用 ~576 字节
- 相比旧 API 的 `Date` 对象更轻量

---

## 与旧 API 对比

| 特性 | LocalTime | Date |
|------|-----------|-----|
| 时分秒 | 分离字段 | 需要计算 |
| 纳秒精度 | 支持 | 毫秒精度 |
| 线程安全 | ✅ 完全线程安全 | ❌ 可变 |
| 不可变性 | ✅ 不可变 | ❌ 可变 |
| 时区 | 无时区 | 包含时区信息 |
| 缓存 | ✅ 小时缓存 | ❌ 无缓存 |

---

## 相关文档

- [LocalDate 实现](../localdate/index.md)
- [DateTimeFormatter 实现](../formatter/index.md)
- [主索引](../index.md)

---

> **更新时间**: 2026-03-20
> **源码版本**: OpenJDK 23
> **文件路径**: `src/java.base/share/classes/java/time/LocalTime.java`
