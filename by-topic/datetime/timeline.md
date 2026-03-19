# 日期时间 API 演进时间线

Java 日期时间 API 从 JDK 1.0 到 JDK 26 的完整演进历程。

---

## 时间线概览

```
JDK 1.0 ──── JDK 1.1 ──── JDK 5 ──── JDK 8 ──── JDK 16 ──── JDK 21 ──── JDK 26
 │             │             │            │           │            │            │
Date          Calendar      Scanner     java.time   Timeline    传统日期    增强
              Formatter    (Joda)     (JSR 310)   格式化      包废弃      功能
```

---

## 旧 API 问题

### Date 和 Calendar 的缺陷

```java
// JDK 1.0 - Date (大部分已废弃)
Date date = new Date();  // 当前时间
date.getTime();          // 毫秒数
// date.getHours();      // 已废弃!

// JDK 1.1 - Calendar
Calendar calendar = Calendar.getInstance();
calendar.set(2024, Calendar.MARCH, 20);  // 月份从 0 开始!
int year = calendar.get(Calendar.YEAR);   // 返回 int
int month = calendar.get(Calendar.MONTH); // 0-11

// 问题:
// 1. 月份从 0 开始 (容易出错)
// 2. 不是线程安全
// 3. API 设计混乱
// 4. 时区处理复杂
// 5. Date 和 Calendar 不一致
```

### SimpleDateFormat 问题

```java
// SimpleDateFormat - 非线程安全!
SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
Date date = sdf.parse("2024-03-20");

// ❌ 多线程环境下不安全
// 需要每次创建新实例或使用 ThreadLocal
```

---

## JDK 8 - java.time (JSR 310)

### 核心类

```
┌─────────────────────────────────────────────────────────┐
│                 java.time 架构                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────┐        │
│  │         基础类型                             │        │
│  │  LocalDate  - 日期 (年月日)                 │        │
│  │  LocalTime  - 时间 (时分秒)                 │        │
│  │  LocalDateTime - 日期时间                   │        │
│  │  Instant    - 时间戳 (UTC)                  │        │
│  │  ZonedDateTime - 带时区的日期时间           │        │
│  └─────────────────────────────────────────────┘        │
│                                                         │
│  ┌─────────────────────────────────────────────┐        │
│  │         工具类型                             │        │
│  │  Duration  - 时间段 (时分秒)                │        │
│  │  Period    - 日期段 (年月日)                │        │
│  │  ZoneId    - 时区                           │        │
│  │  ZoneOffset - 时区偏移                      │        │
│  │  Clock     - 时钟                           │        │
│  └─────────────────────────────────────────────┘        │
│                                                         │
│  ┌─────────────────────────────────────────────┐        │
│  │         格式化                               │        │
│  │  DateTimeFormatter - 格式化器               │        │
│  └─────────────────────────────────────────────┘        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### LocalDate

```java
// LocalDate - 日期 (不包含时间和时区)
LocalDate now = LocalDate.now();              // 2026-03-20
LocalDate date = LocalDate.of(2024, 3, 20);   // 2024-03-20
LocalDate date2 = LocalDate.of(2024, Month.MARCH, 20);

// 解析
LocalDate parsed = LocalDate.parse("2024-03-20");

// 获取字段
int year = date.getYear();           // 2024
Month month = date.getMonth();       // MARCH
int day = date.getDayOfMonth();      // 20
DayOfWeek dow = date.getDayOfWeek(); // WEDNESDAY
int dayOfYear = date.getDayOfYear(); // 80 (闰年)

// 计算
LocalDate tomorrow = now.plusDays(1);
LocalDate nextWeek = now.plusWeeks(1);
LocalDate nextMonth = now.plusMonths(1);
LocalDate nextYear = now.plusYears(1);

LocalDate yesterday = now.minusDays(1);

// 修改
LocalDate modified = now.withYear(2025)
                         .withMonth(6)
                         .withDayOfMonth(15);

// 比较
boolean isBefore = date.isBefore(now);
boolean isAfter = date.isAfter(now);
boolean isEqual = date.isEqual(now);

// 调整
LocalDate firstDayOfMonth = now.with(TemporalAdjusters.firstDayOfMonth());
LocalDate lastDayOfMonth = now.with(TemporalAdjusters.lastDayOfMonth());
LocalDate nextMonday = now.with(TemporalAdjusters.next(DayOfWeek.MONDAY));
LocalDate firstDayOfNextYear = now.with(TemporalAdjusters.firstDayOfNextYear());
```

### LocalTime

```java
// LocalTime - 时间 (不包含日期和时区)
LocalTime now = LocalTime.now();              // 12:34:56.789
LocalTime time = LocalTime.of(12, 30);        // 12:30
LocalTime time2 = LocalTime.of(12, 30, 45);   // 12:30:45
LocalTime time3 = LocalTime.of(12, 30, 45, 123456789); // 纳秒

// 解析
LocalTime parsed = LocalTime.parse("12:30:45");

// 获取字段
int hour = time.getHour();       // 12
int minute = time.getMinute();   // 30
int second = time.getSecond();   // 45
int nano = time.getNano();       // 纳秒

// 计算
LocalTime plusHours = time.plusHours(2);
LocalTime plusMinutes = time.plusMinutes(30);
LocalTime plusSeconds = time.plusSeconds(45);

// 最大/最小
LocalTime minTime = LocalTime.MIN;  // 00:00
LocalTime maxTime = LocalTime.MAX;  // 23:59:59.999999999
LocalTime midnight = LocalTime.MIDNIGHT;  // 00:00
LocalTime noon = LocalTime.NOON;    // 12:00
```

### LocalDateTime

```java
// LocalDateTime - 日期时间 (不包含时区)
LocalDateTime now = LocalDateTime.now();
LocalDateTime dateTime = LocalDateTime.of(2024, 3, 20, 12, 30);
LocalDateTime dateTime2 = LocalDateTime.of(date, time);

// 解析
LocalDateTime parsed = LocalDateTime.parse("2024-03-20T12:30:45");

// 转换
LocalDate date = dateTime.toLocalDate();
LocalTime time = dateTime.toLocalTime();

// LocalDateTime + 时区 = ZonedDateTime
ZonedDateTime zdt = dateTime.atZone(ZoneId.of("Asia/Shanghai"));

// LocalDateTime + 偏移 = OffsetDateTime
OffsetDateTime odt = dateTime.atOffset(ZoneOffset.ofHours(8));
```

### Instant

```java
// Instant - 时间戳 (UTC)
Instant now = Instant.now();
Instant epoch = Instant.EPOCH;  // 1970-01-01T00:00:00Z

// 从毫秒/秒创建
Instant fromMillis = Instant.ofEpochMilli(System.currentTimeMillis());
Instant fromSeconds = Instant.ofEpochSecond(1710902400L);

// 转换
long millis = now.toEpochMilli();
long seconds = now.getEpochSecond();

// 转换为 LocalDateTime
LocalDateTime ldt = LocalDateTime.ofInstant(now, ZoneId.systemDefault());
```

### ZonedDateTime

```java
// ZonedDateTime - 带时区的日期时间
ZonedDateTime now = ZonedDateTime.now();
ZonedDateTime paris = ZonedDateTime.now(ZoneId.of("Europe/Paris"));
ZonedDateTime shanghai = ZonedDateTime.now(ZoneId.of("Asia/Shanghai"));

// 从 LocalDateTime 创建
LocalDateTime ldt = LocalDateTime.of(2024, 3, 20, 12, 30);
ZonedDateTime zdt = ldt.atZone(ZoneId.of("Asia/Shanghai"));

// 从 Instant 创建
Instant instant = Instant.now();
ZonedDateTime zdt2 = instant.atZone(ZoneId.of("Asia/Shanghai"));

// 时区转换
ZonedDateTime tokyo = shanghai.withZoneSameInstant(ZoneId.of("Asia/Tokyo"));

// 获取时区信息
ZoneId zone = zdt.getZone();
ZoneOffset offset = zdt.getOffset();
```

### ZoneId

```java
// ZoneId - 时区
ZoneId shanghai = ZoneId.of("Asia/Shanghai");
ZoneId tokyo = ZoneId.of("Asia/Tokyo");
ZoneId newyork = ZoneId.of("America/New_York");

// 系统默认
ZoneId system = ZoneId.systemDefault();

// 所有可用时区
Set<String> availableZoneIds = ZoneId.getAvailableZoneIds();

// ZoneOffset - 时区偏移
ZoneOffset offset = ZoneOffset.ofHours(8);      // UTC+8
ZoneOffset offset2 = ZoneOffset.of("+08:00");
ZoneOffset utc = ZoneOffset.UTC;
```

### Duration 和 Period

```java
// Duration - 时间段 (时分秒纳秒)
Duration duration = Duration.between(LocalTime.of(10, 0),
                                     LocalTime.of(12, 30));
// PT2H30M (2小时30分钟)

long hours = duration.toHours();      // 2
long minutes = duration.toMinutes();   // 150
long seconds = duration.toSeconds();   // 9000

// 创建 Duration
Duration d1 = Duration.ofHours(2);
Duration d2 = Duration.ofMinutes(30);
Duration d3 = Duration.between(start, end);

// 计算
Duration plus = duration.plusHours(1);
Duration multiplied = duration.multipliedBy(2);
Duration negated = duration.negated();

// Period - 日期段 (年月日)
Period period = Period.between(
    LocalDate.of(2024, 1, 1),
    LocalDate.of(2024, 3, 20)
); // P2M19D (2个月19天)

int years = period.getYears();    // 0
int months = period.getMonths();  // 2
int days = period.getDays();      // 19

// 创建 Period
Period p1 = Period.ofYears(1);
Period p2 = Period.ofMonths(6);
Period p3 = Period.of(1, 2, 3);  // 1年2月3天

// 计算年龄
LocalDate birth = LocalDate.of(1990, 5, 15);
Period age = Period.between(birth, LocalDate.now());
System.out.println(age.getYears());  // 年龄
```

### DateTimeFormatter

```java
// DateTimeFormatter - 格式化器 (线程安全!)
DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

// 格式化
LocalDateTime now = LocalDateTime.now();
String formatted = now.format(formatter);  // 2026-03-20 12:34:56

// 解析
LocalDateTime parsed = LocalDateTime.parse("2024-03-20 12:30:45", formatter);

// 预定义格式化器
String isoDate = LocalDate.now().format(DateTimeFormatter.ISO_DATE);
String isoTime = LocalTime.now().format(DateTimeFormatter.ISO_TIME);
String isoDateTime = LocalDateTime.now().format(DateTimeFormatter.ISO_DATE_TIME);

// 本地化格式
String french = DateTimeFormatter.ofPattern("d MMMM yyyy", Locale.FRENCH)
    .format(LocalDate.now());

// 自定义格式
DateTimeFormatter custom = DateTimeFormatter.ofPattern("yyyy年MM月dd日 EEEE a hh:mm");
String formatted2 = now.format(custom);
// 2026年03月20日 星期四 下午 12:34
```

### TemporalAdjusters

```java
// TemporalAdjusters - 时间调整器
import java.time.temporal.TemporalAdjusters;

LocalDate date = LocalDate.now();

// 第一天/最后一天
LocalDate firstDayOfMonth = date.with(TemporalAdjusters.firstDayOfMonth());
LocalDate lastDayOfMonth = date.with(TemporalAdjusters.lastDayOfMonth());
LocalDate firstDayOfYear = date.with(TemporalAdjusters.firstDayOfYear());
LocalDate lastDayOfYear = date.with(TemporalAdjusters.lastDayOfYear());

// 下一个/上一个
LocalDate nextMonday = date.with(TemporalAdjusters.next(DayOfWeek.MONDAY));
LocalDate previousFriday = date.with(TemporalAdjusters.previous(DayOfWeek.FRIDAY));

// 第几个星期
LocalDate firstSunday = date.with(TemporalAdjusters.firstInMonth(DayOfWeek.SUNDAY));
LocalDate lastTuesday = date.with(TemporalAdjusters.lastInMonth(DayOfWeek.TUESDAY));
LocalDate nextWednesday = date.with(TemporalAdjusters.nextOrSame(DayOfWeek.WEDNESDAY));

// 自定义调整器
TemporalAdjuster nextWorkDay = temporal -> {
    LocalDate result = (LocalDate) temporal;
    do {
        result = result.plusDays(1);
    } while (result.getDayOfWeek() == DayOfWeek.SATURDAY ||
             result.getDayOfWeek() == DayOfWeek.SUNDAY);
    return result;
};

LocalDate nextWorkDayDate = date.with(nextWorkDay);
```

---

## JDK 8-21 - 持续改进

### Clock (JDK 8)

```java
// Clock - 时钟 (用于测试)
Clock defaultClock = Clock.systemDefaultZone();
Clock utcClock = Clock.systemUTC();

// 固定时钟 (用于测试)
Clock fixedClock = Clock.fixed(
    Instant.parse("2024-03-20T12:00:00Z"),
    ZoneOffset.UTC
);

// 偏移时钟 (用于测试)
Clock offsetClock = Clock.offset(defaultClock, Duration.ofHours(1));

// 使用 Clock
Instant now = defaultClock.instant();
```

### MonthDay 和 YearMonth (JDK 8)

```java
// MonthDay - 月日 (用于重复事件，如生日)
MonthDay birthday = MonthDay.of(3, 20);
LocalDate date = birthday.atYear(2024);  // 2024-03-20

// YearMonth - 年月 (用于账单等)
YearMonth ym = YearMonth.of(2024, 3);
LocalDate firstDay = ym.atDay(1);        // 2024-03-01
LocalDate lastDay = ym.atEndOfMonth();   // 2024-03-31
int lengthOfMonth = ym.lengthOfMonth();  // 31
```

### Year 和 Month (JDK 8)

```java
// Year - 年
Year year = Year.of(2024);
boolean isLeap = year.isLeap();  // true (闰年)

// Month - 月
Month month = Month.MARCH;
int length = month.length(false);  // 31 (非闰年)
int maxLength = month.maxLength();  // 31
Month firstQuarter = month.firstMonthOfQuarter();  // JANUARY
```

### MinguoDate 等 (JDK 8)

```java
// 其他日历系统
MinguoDate minguo = MinguoDate.now();  // 民国历
JapaneseDate japanese = JapaneseDate.now();  // 日本历
ThaiBuddhistDate thai = ThaiBuddhistDate.now();  // 佛历
HijrahDate hijrah = HijrahDate.now();  // 伊斯兰历
```

### Date 与 Instant 转换 (JDK 8)

```java
// 旧 API 与新 API 互转
Date date = new Date();
Instant instant = date.toInstant();
LocalDateTime ldt = LocalDateTime.ofInstant(instant,
    ZoneId.systemDefault());

// 反向转换
Date toDate = Date.from(ldt.atZone(ZoneId.systemDefault()).toInstant());
```

---

## JDK 16 - Timeline Format

### Timeline Format

```java
// 新的时间线格式化方法
LocalDateTime now = LocalDateTime.now();

// format(DateTimeFormatter) 的简化
String formatted = now.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);
```

---

## JDK 21 - 传统日期包废弃

### java.util.Date 废弃

```java
// JDK 21 标记 java.util.Date 为 deprecated
@Deprecated(since = "21")
public class Date {
    // ...
}

// 推荐使用 java.time
LocalDate.now();
```

---

## 日期时间选择指南

### 类选择

| 需求 | 推荐类 | 说明 |
|------|--------|------|
| 仅日期 | LocalDate | 不包含时间 |
| 仅时间 | LocalTime | 不包含日期 |
| 日期时间 | LocalDateTime | 不包含时区 |
| 时间戳 | Instant | UTC 时间 |
| 带时区日期时间 | ZonedDateTime | 完整日期时间 |
| 时长 (时分秒) | Duration | 时间段 |
| 日期段 (年月日) | Period | 日期段 |

### 格式化选择

| 需求 | 格式化器 |
|------|----------|
| ISO 标准 | DateTimeFormatter.ISO_* |
| 自定义 | DateTimeFormatter.ofPattern() |
| 本地化 | DateTimeFormatter.withLocale() |

---

## 最佳实践

### 使用新 API

```java
// ✅ 推荐: 使用 java.time
LocalDate now = LocalDate.now();

// ❌ 避免: 使用旧 API
Date date = new Date();
Calendar calendar = Calendar.getInstance();
```

### 使用不可变对象

```java
// ✅ 推荐: 所有类都是不可变的
LocalDate date = LocalDate.now();
LocalDate tomorrow = date.plusDays(1);  // 返回新对象

// ✅ 线程安全
// 所有日期时间类都是线程安全的
```

### 使用枚举

```java
// ✅ 推荐: 使用枚举
Month month = Month.MARCH;
DayOfWeek dow = DayOfWeek.WEDNESDAY;

// ❌ 避免: 使用数字
int month = 2;  // 容易出错 (3月应该是 2 还是 3?)
```

---

## 时间线总结

| 版本 | 特性 | 说明 |
|------|------|------|
| JDK 1.0 | Date | 最初的时间类 |
| JDK 1.1 | Calendar | 改进的时间类 |
| JDK 8 | **java.time** | 现代日期时间 API (JSR 310) |
| JDK 16 | Timeline Format | 时间线格式化 |
| JDK 21 | Date/Calendar 废弃 | 标记旧 API 为废弃 |

---

## 相关链接

- [java.time 包](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/time/package-summary.html)
- [JSR 310: Date and Time API](https://jcp.org/en/jsr/detail?id=310)
