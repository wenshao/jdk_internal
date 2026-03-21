# 日期时间 API 基础

> java.time API 完整指南

---
## 目录

1. [核心类](#1-核心类)
2. [LocalDate - 日期](#2-localdate---日期)
3. [LocalTime - 时间](#3-localtime---时间)
4. [LocalDateTime - 日期时间](#4-localdatetime---日期时间)
5. [Instant - 时间戳](#5-instant---时间戳)
6. [ZonedDateTime - 带时区日期时间](#6-zoneddatetime---带时区日期时间)
7. [ZoneId - 时区](#7-zoneid---时区)
8. [Duration - 时间段](#8-duration---时间段)
9. [Period - 日期段](#9-period---日期段)
10. [DateTimeFormatter - 格式化](#10-datetimeformatter---格式化)
11. [旧 API vs 新 API](#11-旧-api-vs-新-api)
12. [线程安全](#12-线程安全)
13. [ThreeTen-Extra 扩展](#13-threeten-extra-扩展)
14. [API 废弃](#14-api-废弃)
15. [内部实现](#15-内部实现)
16. [性能优化技术](#16-性能优化技术)
17. [VM 诊断参数](#17-vm-诊断参数)
18. [源码位置](#18-源码位置)
19. [相关文档](#19-相关文档)

---


## 1. 核心类

### 类层次结构

```
java.time
├── LocalDate          # 日期 (年月日)
├── LocalTime          # 时间 (时分秒)
├── LocalDateTime      # 日期时间 (无时区)
├── Instant            # 时间戳 (UTC)
├── ZonedDateTime      # 带时区日期时间
├── OffsetDateTime     # 带偏移日期时间
├── ZoneId             # 时区
├── ZoneOffset         # 时区偏移
├── Duration           # 时间段 (时分秒)
├── Period             # 日期段 (年月日)
├── Year               # 年
├── YearMonth          # 年月
├── MonthDay           # 月日
└── Month              # 月枚举

java.time.format
└── DateTimeFormatter  # 格式化器

java.time.chrono
├── JapaneseDate       # 日本历
├── MinguoDate         # 民国历
├── ThaiBuddhistDate   # 佛历
└── HijrahDate         # 伊斯兰历

java.time.temporal
├── TemporalAdjuster   # 时间调整器
├── TemporalAdjusters  # 预定义调整器
└── ChronoUnit         # 时间单位
```

---

## 2. LocalDate - 日期

### 创建

```java
// 当前日期
LocalDate now = LocalDate.now();              // 2026-03-20

// 指定日期
LocalDate date1 = LocalDate.of(2024, 3, 20);  // 2024-03-20
LocalDate date2 = LocalDate.of(2024, Month.MARCH, 20);

// 解析
LocalDate parsed = LocalDate.parse("2024-03-20");

// 年份第几天
LocalDate dayOfYear = LocalDate.ofYearDay(2024, 80);  // 2024-03-20

// 从纪元日计算
LocalDate epochDay = LocalDate.ofEpochDay(10000);  // 1997-05-19
```

### 获取字段

```java
LocalDate date = LocalDate.of(2024, 3, 20);

int year = date.getYear();              // 2024
int monthValue = date.getMonthValue();  // 3
Month month = date.getMonth();          // MARCH
int day = date.getDayOfMonth();         // 20
DayOfWeek dow = date.getDayOfWeek();    // WEDNESDAY
int dayOfYear = date.getDayOfYear();    // 80 (闰年)
int lengthOfMonth = date.lengthOfMonth();   // 31
int lengthOfYear = date.lengthOfYear();     // 366 (闰年)
boolean isLeap = date.isLeapYear();         // true
```

### 计算

```java
LocalDate date = LocalDate.of(2024, 3, 20);

// 加减
LocalDate plusDays = date.plusDays(1);
LocalDate plusWeeks = date.plusWeeks(1);
LocalDate plusMonths = date.plusMonths(1);
LocalDate plusYears = date.plusYears(1);

LocalDate minusDays = date.minusDays(1);
LocalDate minusWeeks = date.minusWeeks(1);
LocalDate minusMonths = date.minusMonths(1);
LocalDate minusYears = date.minusYears(1);

// 使用 TemporalAmount
LocalDate plusPeriod = date.plus(Period.ofDays(5));
LocalDate plusDuration = date.plus(Duration.ofDays(5));
```

### 修改

```java
LocalDate date = LocalDate.of(2024, 3, 20);

// 修改字段
LocalDate withYear = date.withYear(2025);
LocalDate withMonth = date.withMonth(6);
LocalDate withDay = date.withDayOfMonth(15);

// 链式调用
LocalDate modified = date.withYear(2025)
                        .withMonth(6)
                        .withDayOfMonth(15);  // 2025-06-15
```

### 调整

```java
LocalDate date = LocalDate.of(2024, 3, 20);

// 第一天/最后一天
LocalDate firstDayOfMonth = date.with(TemporalAdjusters.firstDayOfMonth());
LocalDate lastDayOfMonth = date.with(TemporalAdjusters.lastDayOfMonth());
LocalDate firstDayOfYear = date.with(TemporalAdjusters.firstDayOfYear());
LocalDate lastDayOfYear = date.with(TemporalAdjusters.lastDayOfYear());

// 下一个/上一个工作日
LocalDate nextMonday = date.with(TemporalAdjusters.next(DayOfWeek.MONDAY));
LocalDate previousFriday = date.with(TemporalAdjusters.previous(DayOfWeek.FRIDAY));

// 本月第几个星期几
LocalDate firstSunday = date.with(TemporalAdjusters.firstInMonth(DayOfWeek.SUNDAY));
LocalDate lastTuesday = date.with(TemporalAdjusters.lastInMonth(DayOfWeek.TUESDAY));
LocalDate nextWednesday = date.with(TemporalAdjusters.nextOrSame(DayOfWeek.WEDNESDAY));
```

### 比较

```java
LocalDate date1 = LocalDate.of(2024, 3, 20);
LocalDate date2 = LocalDate.of(2024, 3, 21);

boolean isBefore = date1.isBefore(date2);  // true
boolean isAfter = date1.isAfter(date2);   // false
boolean isEqual = date1.isEqual(date2);   // false

// 比较返回负数、0、正数
int cmp = date1.compareTo(date2);  // -1
```

---

## 3. LocalTime - 时间

### 创建

```java
// 当前时间
LocalTime now = LocalTime.now();  // 12:34:56.789

// 指定时间
LocalTime time1 = LocalTime.of(12, 30);           // 12:30
LocalTime time2 = LocalTime.of(12, 30, 45);       // 12:30:45
LocalTime time3 = LocalTime.of(12, 30, 45, 123456789);  // 纳秒

// 解析
LocalTime parsed = LocalTime.parse("12:30:45");

// 秒/纳秒
LocalTime ofSecondOfDay = LocalTime.ofSecondOfDay(45000);  // 12:30:00
LocalTime ofNanoOfDay = LocalTime.ofNanoOfDay(45000000000000L);
```

### 获取字段

```java
LocalTime time = LocalTime.of(12, 30, 45, 123456789);

int hour = time.getHour();        // 12
int minute = time.getMinute();    // 30
int second = time.getSecond();    // 45
int nano = time.getNano();        // 123456789
```

### 特殊值

```java
LocalTime minTime = LocalTime.MIN;    // 00:00
LocalTime maxTime = LocalTime.MAX;    // 23:59:59.999999999
LocalTime midnight = LocalTime.MIDNIGHT;  // 00:00
LocalTime noon = LocalTime.NOON;      // 12:00

// 时间从 00:00 到指定时间
LocalTime halfDay = LocalTime.of(12, 0);  // 12:00
```

---

## 4. LocalDateTime - 日期时间

### 创建

```java
// 当前日期时间
LocalDateTime now = LocalDateTime.now();

// 指定日期时间
LocalDateTime dt1 = LocalDateTime.of(2024, 3, 20, 12, 30);
LocalDateTime dt2 = LocalDateTime.of(2024, Month.MARCH, 20, 12, 30, 45);

// 从 LocalDate + LocalTime
LocalDate date = LocalDate.of(2024, 3, 20);
LocalTime time = LocalTime.of(12, 30);
LocalDateTime dt3 = LocalDateTime.of(date, time);

// 解析
LocalDateTime parsed = LocalDateTime.parse("2024-03-20T12:30:45");
```

### 转换

```java
LocalDateTime ldt = LocalDateTime.now();

// 转为 LocalDate/LocalTime
LocalDate date = ldt.toLocalDate();
LocalTime time = ldt.toLocalTime();

// 加上时区
ZonedDateTime zdt = ldt.atZone(ZoneId.of("Asia/Shanghai"));
OffsetDateTime odt = ldt.atOffset(ZoneOffset.ofHours(8));

// 从 Instant 转换
Instant instant = Instant.now();
LocalDateTime fromInstant = LocalDateTime.ofInstant(instant,
    ZoneId.of("Asia/Shanghai"));
```

---

## 5. Instant - 时间戳

### 创建

```java
// 当前时间戳
Instant now = Instant.now();

// 纪元时间
Instant epoch = Instant.EPOCH;  // 1970-01-01T00:00:00Z
Instant min = Instant.MIN;      // -1000000000-01-01T00:00:00Z
Instant max = Instant.MAX;      // 1000000000-12-31T23:59:59.999999999Z

// 从毫秒/秒
Instant fromMillis = Instant.ofEpochMilli(1710902400000L);
Instant fromSeconds = Instant.ofEpochSecond(1710902400L);
```

### 转换

```java
Instant instant = Instant.now();

// 转毫秒/秒
long millis = instant.toEpochMilli();
long seconds = instant.getEpochSecond();

// 转 LocalDateTime
LocalDateTime ldt = LocalDateTime.ofInstant(instant,
    ZoneId.of("Asia/Shanghai"));
```

---

## 6. ZonedDateTime - 带时区日期时间

### 创建

```java
// 当前时区
ZonedDateTime now = ZonedDateTime.now();

// 指定时区
ZonedDateTime paris = ZonedDateTime.now(ZoneId.of("Europe/Paris"));
ZonedDateTime shanghai = ZonedDateTime.now(ZoneId.of("Asia/Shanghai"));

// 从 LocalDateTime 创建
LocalDateTime ldt = LocalDateTime.of(2024, 3, 20, 12, 30);
ZonedDateTime zdt = ldt.atZone(ZoneId.of("Asia/Shanghai"));

// 从 Instant 创建
Instant instant = Instant.now();
ZonedDateTime zdt2 = instant.atZone(ZoneId.of("Asia/Shanghai"));
```

### 时区转换

```java
ZonedDateTime shanghai = ZonedDateTime.now(ZoneId.of("Asia/Shanghai"));

// 保留瞬间，转换时区
ZonedDateTime tokyo = shanghai.withZoneSameInstant(ZoneId.of("Asia/Tokyo"));
ZonedDateTime newyork = shanghai.withZoneSameInstant(ZoneId.of("America/New_York"));

// 保留本地时间，改变时区
ZonedDateTime sameLocalTime = shanghai.withZoneSameLocal(ZoneId.of("Asia/Tokyo"));
```

### 时区信息

```java
ZonedDateTime zdt = ZonedDateTime.now(ZoneId.of("Asia/Shanghai"));

ZoneId zone = zdt.getZone();
ZoneOffset offset = zdt.getOffset();

// 时区偏移
String offsetStr = offset.getId();  // +08:00
int offsetHours = offset.getTotalSeconds() / 3600;  // 8
```

---

## 7. ZoneId - 时区

### 常用时区

```java
// 常用城市时区
ZoneId shanghai = ZoneId.of("Asia/Shanghai");
ZoneId tokyo = ZoneId.of("Asia/Tokyo");
ZoneId newyork = ZoneId.of("America/New_York");
ZoneId london = ZoneId.of("Europe/London");
ZoneId paris = ZoneId.of("Europe/Paris");

// 固定偏移
ZoneOffset utc = ZoneOffset.UTC;
ZoneOffset utcPlus8 = ZoneOffset.ofHours(8);
ZoneOffset utcMinus5 = ZoneOffset.of("-05:00");

// 系统默认
ZoneId system = ZoneId.systemDefault();

// 所有可用时区
Set<String> availableZoneIds = ZoneId.getAvailableZoneIds();
```

---

## 8. Duration - 时间段

### 创建

```java
// 两个时间之间
LocalTime start = LocalTime.of(10, 0);
LocalTime end = LocalTime.of(12, 30);
Duration duration = Duration.between(start, end);  // PT2H30M

// 直接创建
Duration ofHours = Duration.ofHours(2);
Duration ofMinutes = Duration.ofMinutes(30);
Duration ofSeconds = Duration.ofSeconds(90);
Duration ofMillis = Duration.ofMillis(1000);
Duration ofNanos = Duration.ofNanos(1000000000);

// 文本解析
Duration parsed = Duration.parse("PT2H30M");  // 2小时30分钟
```

### 获取值

```java
Duration duration = Duration.ofHours(2).plusMinutes(30);

long seconds = duration.getSeconds();     // 9000 (2.5小时)
int nanos = duration.getNano();           // 0
long toHours = duration.toHours();        // 2
long toMinutes = duration.toMinutes();    // 150
long toMillis = duration.toMillis();      // 9000000
long toDays = duration.toDays();          // 0
```

### 操作

```java
Duration duration = Duration.ofHours(2);

// 加减
Duration plus = duration.plusHours(1);
Duration minus = duration.minusMinutes(30);

// 乘除
Duration multiplied = duration.multipliedBy(2);
Duration divided = duration.dividedBy(2);
Duration negated = duration.negated();

// 绝对值
Duration abs = duration.negated().abs();
```

---

## 9. Period - 日期段

### 创建

```java
// 两个日期之间
LocalDate start = LocalDate.of(2024, 1, 1);
LocalDate end = LocalDate.of(2024, 3, 20);
Period period = Period.between(start, end);  // P2M19D

// 直接创建
Period ofYears = Period.ofYears(1);
Period ofMonths = Period.ofMonths(6);
Period ofDays = Period.ofDays(30);
Period ofWeeks = Period.ofWeeks(2);

// 组合
Period combined = Period.of(1, 2, 3);  // 1年2月3天

// 文本解析
Period parsed = Period.parse("P1Y2M3D");  // 1年2月3天
```

### 获取值

```java
Period period = Period.of(1, 2, 3);

int years = period.getYears();    // 1
int months = period.getMonths();  // 2
int days = period.getDays();      // 3

// 总月数
int totalMonths = period.toTotalMonths();  // 14
```

### 操作

```java
Period period = Period.of(1, 2, 3);

// 加减
Period plus = period.plusYears(1);
Period minus = period.minusMonths(1);

// 取负
Period negated = period.negated();  // P-1Y-2M-3D
```

### 计算年龄

```java
LocalDate birth = LocalDate.of(1990, 5, 15);
LocalDate today = LocalDate.now();
Period age = Period.between(birth, today);

System.out.printf("%d岁%d个月%n",
    age.getYears(), age.getMonths());
```

---

## 10. DateTimeFormatter - 格式化

### 预定义格式化器

```java
LocalDateTime now = LocalDateTime.now();

// ISO 格式
String isoDate = now.format(DateTimeFormatter.ISO_DATE);  // 2026-03-20
String isoTime = now.format(DateTimeFormatter.ISO_TIME);  // 12:34:56.789
String isoDateTime = now.format(DateTimeFormatter.ISO_DATE_TIME);  // 2026-03-20T12:34:56.789
```

### 自定义格式

```java
// 创建格式化器
DateTimeFormatter formatter =
    DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

// 格式化
String formatted = LocalDateTime.now().format(formatter);

// 解析
LocalDateTime parsed = LocalDateTime.parse("2024-03-20 12:30:45", formatter);
```

### 本地化格式

```java
// 本地化
DateTimeFormatter french =
    DateTimeFormatter.ofPattern("d MMMM yyyy", Locale.FRENCH);
String frenchDate = LocalDate.now().format(french);  // 20 mars 2026

DateTimeFormatter german =
    DateTimeFormatter.ofPattern("d. MMMM yyyy", Locale.GERMAN);
String germanDate = LocalDate.now().format(german);  // 20. März 2026
```

### 常用模式

| 模式 | 说明 | 示例 |
|------|------|------|
| `yyyy` | 年 | 2026 |
| `MM` | 月 | 03 |
| `dd` | 日 | 20 |
| `HH` | 小时 (24) | 13 |
| `hh` | 小时 (12) | 01 |
| `mm` | 分钟 | 30 |
| `ss` | 秒 | 45 |
| `SSS` | 毫秒 | 123 |
| `a` | 上午/下午 | 下午 |
| `EEEE` | 星期 | 星期四 |
| `MMM` | 月 (简写) | 3月 |
| `MMMM` | 月 (全称) | 三月 |

---

## 11. 旧 API vs 新 API

### 旧 API 问题

```java
// 问题 1: 月份从 0 开始
Calendar calendar = Calendar.getInstance();
calendar.set(2024, 2, 20);  // 实际是 3月! (2 = March)

// 问题 2: 非线程安全
SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
// 多线程不安全!

// 问题 3: 类型不明确
Date date = new Date();  // 同时包含日期和时间
```

### 新 API 解决

```java
// 解决 1: 月份使用枚举
LocalDate date = LocalDate.of(2024, Month.MARCH, 20);
Month month = date.getMonth();  // 返回 MARCH

// 解决 2: 完全线程安全
DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
// 所有类都是不可变的

// 解决 3: 类型明确
LocalDate onlyDate = LocalDate.now();        // 仅日期
LocalTime onlyTime = LocalTime.now();        // 仅时间
LocalDateTime dateTime = LocalDateTime.now(); // 日期时间
```

---

## 12. 线程安全

### SimpleDateFormat 问题

```java
// ❌ 不安全: 多线程环境下 SimpleDateFormat 会出错
private static final SimpleDateFormat SDF =
    new SimpleDateFormat("yyyy-MM-dd");

// 需要同步或每次创建新对象
synchronized (SDF) {
    Date date = SDF.parse("2024-03-20");
}
```

### DateTimeFormatter 解决

```java
// ✅ 安全: DateTimeFormatter 是不可变的
private static final DateTimeFormatter FORMATTER =
    DateTimeFormatter.ofPattern("yyyy-MM-dd");

// 多线程安全，无需同步
LocalDate date = LocalDate.parse("2024-03-20", FORMATTER);
```

---

## 13. ThreeTen-Extra 扩展

**项目**: [ThreeTen-Extra](https://www.threeten.org/threeten-extra/)

```xml
<dependency>
    <groupId>org.threeten</groupId>
    <artifactId>threeten-extra</artifactId>
    <version>1.7.2</version>
</dependency>
```

### 额外类

```java
// YearQuarter - 年季度
YearQuarter q1 = YearQuarter.of(2024, 1);  // 2024 Q1

// Quarter - 季度
Quarter quarter = Quarter.Q1;  // 第一季度

// Amount - 货币/金额
```

---

## 14. API 废弃

### JDK 21 废弃

```java
// JDK 21 标记为 deprecated for removal
@Deprecated(since = "21", forRemoval = true)
public class Date extends Object implements java.io.Serializable, Cloneable, Comparable<Date> {
    /**
     * @deprecated This class is deprecated for removal.
     * Use {@link java.time.Instant} instead.
     */
    @Deprecated(since = "21", forRemoval = true)
    public Date() {
    }
}
```

### 迁移映射

| 旧类 | 新类 |
|------|------|
| `java.util.Date` | `java.time.Instant` |
| `java.util.Calendar` | `java.time.ZonedDateTime` |
| `java.util.GregorianCalendar` | `java.time.ZonedDateTime` |
| `java.text.SimpleDateFormat` | `java.time.format.DateTimeFormatter` |

---

## 15. 内部实现

### 内存布局

```
LocalDate (24 bytes):
┌─────────────┬──────────┬──────────┐
│ year (int)  │ month    │ day      │
│ 4 bytes     │ (byte)   │ (byte)   │
├─────────────┴──────────┴──────────┤
│ 剩余 16 字节用于对象头和对齐       │
└────────────────────────────────────┘

LocalTime (24 bytes):
┌──────────┬──────────┬──────────┬──────────┐
│ hour     │ minute   │ second   │ nano     │
│ (byte)   │ (byte)   │ (byte)   │ (int)    │
└──────────┴──────────┴──────────┴──────────┘

LocalDateTime (48 bytes):
┌─────────────────┬─────────────────┐
│ LocalDate (24)  │ LocalTime (24)   │
└─────────────────┴─────────────────┘

Instant (16 bytes):
┌───────────────────┬─────────────┐
│ seconds (long)    │ nanos (int) │
└───────────────────┴─────────────┘
```

### DateTimeHelper 内部工具 (JDK 23+)

```java
// jdk.internal.util.DateTimeHelper
// 专门优化日期时间格式化

public static void formatTo(StringBuilder buf, LocalDate date) {
    int year = date.getYear();
    int absYear = Math.abs(year);

    if (absYear < 10000) {
        if (year < 0) buf.append('-');
        DecimalDigits.appendQuad(buf, absYear);  // 使用查找表
    } else {
        buf.append(year);
    }
    buf.append('-');
    DecimalDigits.appendPair(buf, date.getMonthValue());  // 使用查找表
    buf.append('-');
    DecimalDigits.appendPair(buf, date.getDayOfMonth());   // 使用查找表
}
```

### DecimalDigits 查找表 (JDK 24+)

```java
// jdk.internal.util.DecimalDigits
// 预计算查找表：0-99 的数字对

@Stable
private static final short[] DIGITS;  // 128 元素，支持 & 0x7f 消除边界检查

static {
    short[] digits = new short[128];
    for (int i = 0; i < 10; i++) {
        short hi = (short) (i + '0');
        for (int j = 0; j < 10; j++) {
            short lo = (short) ((j + '0') << 8);
            digits[i * 10 + j] = (short) (hi | lo);
        }
    }
    DIGITS = digits;
}

// 示例: DIGITS[47] = 0x3739
// 0x37 = '7', 0x39 = '9'
// 小端序打包两个 ASCII 字符
```

### ZoneOffset 缓存策略

```java
// ZoneOffset 使用缓存优化常用偏移
private static final int MAX_CACHE = 600;  // ±600 秒 (±10 分钟)

// 预缓存 Quarter (15 分钟) 偏移
private static final ZoneOffset[] QUARTER_CACHE;  // ±12 小时，15 分钟间隔

// 总偏移缓存
private static final ConcurrentHashMap<Integer, ZoneOffset> CACHE;
```

### DateTimePrintContext 不可变优化 (JDK 24)

```java
// java.time.format.DateTimePrintContext
// 优化后: 所有字段都是 final

final class DateTimePrintContext {
    private final TemporalAccessor temporal;
    private final DateTimeFormatter formatter;
    // 无可变字段 → 便于逃逸分析优化
}
```

---

## 16. 性能优化技术

### 1. 查找表替代除法

```java
// 优化前: 使用除法和模运算
int hi = value / 10;
int lo = value % 10;
buf.append(hi).append(lo);

// 优化后: 使用查找表 (JDK-8366224)
DecimalDigits.appendPair(buf, value);
// 性能提升: +12%
```

### 2. 方法拆分促进内联

```java
// 优化前: 单一方法 382 字节 (JDK-8365186)
private static TemporalAccessor adjust(...) { /* 382 字节 */ }

// 优化后: 拆分为 3 个方法
private static TemporalAccessor adjust(...) { /* 27 字节 - 可内联 */ }
private static TemporalAccessor adjustWithOverride(...) { /* 123 字节 */ }
private static TemporalAccessor adjustSlow(...) { /* 232 字节 */ }
// 性能提升: +3-12%
```

### 3. StringBuilder 复用

```java
// 优化前: 每次创建新 StringBuilder
new StringBuilder(32).append(year).append('-')...

// 优化后: 共享 StringBuilder (JDK-8337279)
// 对于连续格式化操作，复用 StringBuilder
// 减少分配压力
```

### 4. 逃逸分析

```java
// 不可变对象 → JIT 可以在栈上分配
LocalDate date = LocalDate.now();
String str = date.toString();

// JIT 优化:
// 1. 检测到 StringBuilder 不逃逸
// 2. 在栈上分配 StringBuilder
// 3. 直接提取字符数组，创建 String
// 零 GC 压力!
```

---

## 17. VM 诊断参数

### JIT 编译诊断

```bash
# 监控 C2 内联决策
-XX:+PrintInlining

# 查看编译任务
-XX:+PrintCompilation

# 方法内联阈值（影响 DateTimePrintContext）
-XX:MaxFreqInlineSize=325             # 热方法内联阈值
-XX:MaxInlineSize=35                  # 常规方法内联阈值

# 逃逸分析（影响 StringBuilder 优化）
-XX:+DoEscapeAnalysis                 # 启用逃逸分析
-XX:+EliminateAllocations             # 消除分配
-XX:+PrintEliminateAllocations        # 打印分配消除信息
```

---

## 18. 源码位置

### 核心类

| 类 | 路径 |
|----|------|
| LocalDate | `java.base/java/time/LocalDate.java` |
| LocalTime | `java.base/java/time/LocalTime.java` |
| LocalDateTime | `java.base/java/time/LocalDateTime.java` |
| Instant | `java.base/java/time/Instant.java` |
| ZonedDateTime | `java.base/java/time/ZonedDateTime.java` |
| ZoneId | `java.base/java/time/ZoneId.java` |
| Duration | `java.base/java/time/Duration.java` |
| Period | `java.base/java/time/Period.java` |
| DateTimeFormatter | `java.base/java/time/format/DateTimeFormatter.java` |

### 内部工具

| 类 | 路径 |
|----|------|
| DateTimeHelper | `jdk/internal/util/DateTimeHelper.java` |
| DecimalDigits | `jdk/internal/util/DecimalDigits.java` |

---

## 19. 相关文档

- [完整时间线](timeline.md)
- [JSR 310 PR 分析](jsr310/pr-analysis.md)
- [贡献者](contributors.md)
- [主索引](index.md)

---

> **更新时间**: 2026-03-20
