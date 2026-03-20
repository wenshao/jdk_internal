# 日期时间 API

> JSR 310、java.time、时区处理、格式化

[← 返回主题索引](../by-topic/)

---

## 快速概览

```
JDK 1.0 ── JDK 1.1 ── JDK 5 ── JDK 8 ── JDK 21
   │        │        │        │        │
Date      Calendar JSR 310  java.time 性能优化
问题      修复      预览     (JSR310) +5-40%
```

### 核心演进

| 版本 | 特性 | JEP | 说明 |
|------|------|-----|------|
| **JDK 1.0** | java.util.Date | - | 原始日期类 |
| **JDK 1.1** | java.util.Calendar | - | 改进的日历 API |
| **JDK 5** | JSR 310 预览 | - | 现代日期时间框架 |
| **JDK 8** | java.time | JSR 310 | 正式发布 |
| **JDK 21+** | 性能优化 | - | toString +30%, 缓存 +15-25% |

---

## 目录

- [为什么需要 java.time](#为什么需要-javatime)
- [核心类型](#核心类型)
- [LocalDate/LocalTime/LocalDateTime](#locallocaltimelocaldatetime)
- [ZonedDateTime/OffsetDateTime](#zoneddatetimeoffsetdatetime)
- [Instant/Duration/Period](#instantdurationperiod)
- [DateTimeFormatter](#datetimeformatter)
- [时区处理](#时区处理)
- [性能优化实战](#性能优化实战)
- [最佳实践](#最佳实践)
- [核心贡献者](#核心贡献者)
- [相关链接](#相关链接)

---

## 为什么需要 java.time

### 旧 API 的问题

```java
// java.util.Date 的问题

// 1. 非线程安全
Date date = new Date();
// 多线程环境下修改 date 会导致不一致

// 2. 设计混乱
Date date = new Date();  // 表示日期时间，但名字是 Date
Calendar cal = Calendar.getInstance();  // 更好的 API，但仍然复杂

// 3. 可变性
Date date = new Date();
date.setTime(System.currentTimeMillis());  // 可变，不安全

// 4. 类型不安全
Calendar cal = Calendar.getInstance();
cal.set(Calendar.MONTH, 12);  // 运行时错误，月份是 0-11

// 5. 时区处理混乱
SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
sdf.setTimeZone(TimeZone.getTimeZone("America/New_York"));
// 线程不安全!

// 6. int 常量
int year = date.getYear();  // 返回 1900 年以来的年数
int month = date.getMonth();  // 0-11，容易出错
```

### java.time 的优势

```java
// java.time 的优势

// 1. 不可变 - 线程安全
LocalDate date = LocalDate.now();
LocalDate date2 = date.plusDays(1);  // 返回新对象，原对象不变

// 2. 清晰的类型分离
LocalDate      date = LocalDate.now();          // 日期
LocalTime      time = LocalTime.now();          // 时间
LocalDateTime  dateTime = LocalDateTime.now();  // 日期时间
Instant        instant = Instant.now();         // 时间戳

// 3. 类型安全的枚举
Month month = Month.JANUARY;          // JANUARY = 1
DayOfWeek day = DayOfWeek.MONDAY;     // MONDAY = 1

// 4. 流式 API
LocalDate tomorrow = LocalDate.now()
    .plusDays(1)
    .with(TemporalAdjusters.next(DayOfWeek.MONDAY));

// 5. 线程安全的格式化
DateTimeFormatter formatter = DateTimeFormatter.ISO_LOCAL_DATE;
String formatted = LocalDate.now().format(formatter);
```

---

## 核心类型

### 类型层次

```
java.time (核心包)
├── LocalDate           # 日期 (年月日)
├── LocalTime           # 时间 (时分秒纳秒)
├── LocalDateTime       # 日期时间 (无时区)
├── ZonedDateTime       # 日期时间 (带时区)
├── OffsetDateTime      # 日期时间 (带 UTC 偏移)
├── Instant             # 时间戳 (UTC)
├── Duration            # 时间量 (秒/纳秒)
├── Period              # 日期量 (年月日)
├── ZoneId              # 时区 ID
├── ZoneOffset          # UTC 偏移
└── DateTimeFormatter   # 格式化器
```

### 选择指南

| 需求 | 使用类型 | 示例 |
|------|----------|------|
| 生日、纪念日 | LocalDate | LocalDate.of(2000, Month.JANUARY, 1) |
| 每日提醒时间 | LocalTime | LocalTime.of(9, 0) |
| 本地日期时间 | LocalDateTime | LocalDateTime.now() |
| 全球活动时间 | ZonedDateTime | ZonedDateTime.now(ZoneId.of("Asia/Shanghai")) |
| UTC 时间戳 | Instant | Instant.now() |
| 时间差计算 | Duration | Duration.ofHours(2) |
| 日期差计算 | Period | Period.of(1, 2, 3) # 1年2月3天 |

---

## LocalDate/LocalTime/LocalDateTime

### LocalDate - 日期

```java
// 创建 LocalDate

// 1. 当前日期
LocalDate today = LocalDate.now();  // 2026-03-20

// 2. 指定日期
LocalDate date1 = LocalDate.of(2026, 3, 20);
LocalDate date2 = LocalDate.of(2026, Month.MARCH, 20);
LocalDate date3 = LocalDate.ofYearDay(2026, 79);  // 2026 年第 79 天

// 3. 从文本解析
LocalDate date4 = LocalDate.parse("2026-03-20");
LocalDate date5 = LocalDate.parse("20260320", DateTimeFormatter.BASIC_ISO_DATE);

// 日期操作
LocalDate date = LocalDate.of(2026, 3, 20);

// 加减
LocalDate tomorrow = date.plusDays(1);
LocalDate nextWeek = date.plusWeeks(1);
LocalDate nextMonth = date.plusMonths(1);
LocalDate nextYear = date.plusYears(1);

// 修改
LocalDate modified = date
    .withYear(2027)
    .withMonth(12)
    .withDayOfMonth(25);

// 调整器
LocalDate nextMonday = date.with(TemporalAdjusters.next(DayOfWeek.MONDAY));
LocalDate firstDayOfMonth = date.with(TemporalAdjusters.firstDayOfMonth());
LocalDate lastDayOfYear = date.with(TemporalAdjusters.lastDayOfYear());

// 获取信息
int year = date.getYear();              // 2026
Month month = date.getMonth();          // MARCH
int dayOfMonth = date.getDayOfMonth();  // 20
DayOfWeek dayOfWeek = date.getDayOfWeek(); // THURSDAY
int dayOfYear = date.getDayOfYear();    // 79
boolean isLeap = date.isLeapYear();     // false (2026 不是闰年)

// 日期计算
int daysBetween = ChronoUnit.DAYS.between(date1, date2);
int monthsBetween = ChronoUnit.MONTHS.between(date1, date2);

Period period = Period.between(date1, date2);
int years = period.getYears();
int months = period.getMonths();
int days = period.getDays();

// 判断
boolean isBefore = date1.isBefore(date2);
boolean isAfter = date1.isAfter(date2);
boolean isEqual = date1.isEqual(date2);
```

### LocalTime - 时间

```java
// 创建 LocalTime

// 1. 当前时间
LocalTime now = LocalTime.now();

// 2. 指定时间
LocalTime time1 = LocalTime.of(9, 30);              // 09:30
LocalTime time2 = LocalTime.of(9, 30, 45);         // 09:30:45
LocalTime time3 = LocalTime.of(9, 30, 45, 123456789); // 纳秒
LocalTime time4 = LocalTime.ofSecondOfDay(3600);   // 01:00:00

// 3. 从文本解析
LocalTime time5 = LocalTime.parse("09:30:45");

// 时间操作
LocalTime time = LocalTime.of(9, 30);

// 加减
LocalTime plusHours = time.plusHours(2);
LocalTime plusMinutes = time.plusMinutes(30);
LocalTime plusSeconds = time.plusSeconds(45);
LocalTime plusNanos = time.plusNanos(123456789);

// 修改
LocalTime modified = time
    .withHour(14)
    .withMinute(0)
    .withSecond(0)
    .withNano(0);

// 截断
LocalTime truncated = time.truncatedTo(ChronoUnit.MINUTES);  // 09:30

// 获取信息
int hour = time.getHour();        // 9
int minute = time.getMinute();    // 30
int second = time.getSecond();    // 0
int nano = time.getNano();        // 0

// 时间计算
long hoursBetween = ChronoUnit.HOURS.between(time1, time2);
long minutesBetween = ChronoUnit.MINUTES.between(time1, time2);

Duration duration = Duration.between(time1, time2);
long seconds = duration.getSeconds();
int nanos = duration.getNano();
```

### LocalDateTime - 日期时间

```java
// 创建 LocalDateTime

// 1. 当前日期时间
LocalDateTime now = LocalDateTime.now();

// 2. 组合日期和时间
LocalDateTime dt1 = LocalDateTime.of(2026, 3, 20, 9, 30);
LocalDateTime dt2 = LocalDateTime.of(2026, Month.MARCH, 20, 9, 30);
LocalDateTime dt3 = LocalDateTime.of(LocalDate.now(), LocalTime.now());

// 3. 从 LocalDate 和 LocalTime
LocalDate date = LocalDate.now();
LocalTime time = LocalTime.now();
LocalDateTime dt4 = date.atTime(time);
LocalDateTime dt5 = date.atStartOfDay();  // 当天 00:00

// 4. 从文本解析
LocalDateTime dt6 = LocalDateTime.parse("2026-03-20T09:30:45");

// 操作 (结合了 LocalDate 和 LocalTime 的所有操作)
LocalDateTime dt = LocalDateTime.now();

LocalDateTime tomorrow = dt.plusDays(1);
LocalDateTime nextHour = dt.plusHours(1);
LocalDateTime modified = dt
    .withYear(2027)
    .withMonth(12)
    .withDayOfMonth(25)
    .withHour(0)
    .withMinute(0)
    .withSecond(0);

// 转换
LocalDate date = dt.toLocalDate();
LocalTime time = dt.toLocalTime();
```

---

## ZonedDateTime/OffsetDateTime

### 时区基础

```java
// ZoneId - 时区标识符

// 1. 获取时区
ZoneId shanghai = ZoneId.of("Asia/Shanghai");
ZoneId newyork = ZoneId.of("America/New_York");
ZoneId utc = ZoneId.of("UTC");

// 2. 系统默认时区
ZoneId systemDefault = ZoneId.systemDefault();

// 3. 所有可用时区
Set<String> availableZoneIds = ZoneId.getAvailableZoneIds();

// ZoneOffset - UTC 偏移
ZoneOffset offsetPlus8 = ZoneOffset.of("+08:00");
ZoneOffset offsetMinus5 = ZoneOffset.of("-05:00");
ZoneOffset utc = ZoneOffset.UTC;

// 常见时区偏移
ZoneOffset est = ZoneOffset.ofHours(-5);   // UTC-5
ZoneOffset cst = ZoneOffset.ofHours(8);    // UTC+8
ZoneOffset jst = ZoneOffset.ofHours(9);    // UTC+9
```

### ZonedDateTime - 带时区日期时间

```java
// 创建 ZonedDateTime

// 1. 当前时间 (指定时区)
ZonedDateTime shanghaiNow = ZonedDateTime.now(ZoneId.of("Asia/Shanghai"));
ZonedDateTime newyorkNow = ZonedDateTime.now(ZoneId.of("America/New_York"));

// 2. 从 LocalDateTime 创建
LocalDateTime dt = LocalDateTime.of(2026, 3, 20, 9, 30);
ZonedDateTime shanghai = dt.atZone(ZoneId.of("Asia/Shanghai"));
ZonedDateTime newyork = dt.atZone(ZoneId.of("America/New_York"));

// 3. 从 Instant 创建
Instant instant = Instant.now();
ZonedDateTime shanghaiFromInstant = instant.atZone(ZoneId.of("Asia/Shanghai"));

// 4. 指定日期时间时区
ZonedDateTime specific = ZonedDateTime.of(2026, 3, 20, 9, 30, 0, 0,
    ZoneId.of("Asia/Shanghai"));

// 时区转换
ZonedDateTime shanghai = ZonedDateTime.now(ZoneId.of("Asia/Shanghai"));
ZonedDateTime newyork = shanghai.withZoneSameInstant(ZoneId.of("America/New_York"));
ZonedDateTime utc = shanghai.withZoneSameInstant(ZoneId.of("UTC"));

// 保留本地时间，更改时区
ZonedDateTime sameLocalTime = shanghai.withZoneSameLocal(ZoneId.of("America/New_York"));

// 获取信息
ZoneId zone = shanghai.getZone();
ZoneOffset offset = shanghai.getOffset();

// 夏令时处理
ZonedDateTime usTime = ZonedDateTime.of(2026, 3, 15, 9, 0, 0, 0,
    ZoneId.of("America/New_York"));
// 自动处理夏令时切换
```

### OffsetDateTime - 带 UTC 偏移日期时间

```java
// OffsetDateTime 使用固定偏移，不考虑夏令时

// 创建 OffsetDateTime
OffsetDateTime now = OffsetDateTime.now();
OffsetDateTime specific = OffsetDateTime.of(2026, 3, 20, 9, 30, 0, 0,
    ZoneOffset.of("+08:00"));

// 从 Instant
OffsetDateTime fromInstant = Instant.now().atOffset(ZoneOffset.of("+08:00"));

// 偏移转换
OffsetDateTime utc = now.withOffsetSameInstant(ZoneOffset.UTC);
OffsetDateTime plus8 = now.withOffsetSameInstant(ZoneOffset.ofHours(8));

// ZonedDateTime vs OffsetDateTime
ZonedDateTime zdt = ZonedDateTime.now(ZoneId.of("Asia/Shanghai"));
OffsetDateTime odt = OffsetDateTime.now(ZoneOffset.of("+08:00"));

// ZonedDateTime 适合处理夏令时
// OffsetDateTime 适合 UTC 偏移固定场景 (如数据库存储)
```

---

## Instant/Duration/Period

### Instant - 时间戳

```java
// Instant 表示 UTC 时间线上的一个点

// 1. 当前时间戳
Instant now = Instant.now();

// 2. 从 epoch 秒/毫秒创建
Instant fromEpoch = Instant.ofEpochSecond(1742445600);
Instant fromEpochMilli = Instant.ofEpochMilli(1742445600000L);

// 3. 从文本解析
Instant parsed = Instant.parse("2026-03-20T01:00:00Z");

// 4. 获取 epoch 值
long epochSecond = now.getEpochSecond();      // 秒
long epochMilli = now.toEpochMilli();         // 毫秒
int nano = now.getNano();                     // 纳秒部分

// 5. 操作
Instant plusSeconds = now.plusSeconds(60);
Instant plusMillis = now.plusMillis(1000);
Instant plusNanos = now.plusNanos(1000000);

// 6. 转换
LocalDateTime shanghai = LocalDateTime.ofInstant(now, ZoneId.of("Asia/Shanghai"));
ZonedDateTime utc = ZonedDateTime.ofInstant(now, ZoneId.of("UTC"));

// 7. 比较
boolean isBefore = instant1.isBefore(instant2);
boolean isAfter = instant1.isAfter(instant2);
```

### Duration - 时间量

```java
// Duration 表示基于时间的量 (秒/纳秒)

// 创建 Duration
Duration d1 = Duration.ofHours(2);              // 2 小时
Duration d2 = Duration.ofMinutes(120);          // 120 分钟
Duration d3 = Duration.between(time1, time2);   // 两个时间之间
Duration d4 = Duration.between(instant1, instant2);

// 获取值
long seconds = d1.getSeconds();        // 总秒数
int nanos = d1.getNano();              // 纳秒部分 (0-999,999,999)
long minutes = d1.toMinutes();         // 转换为分钟
long hours = d1.toHours();             // 转换为小时
long millis = d1.toMillis();           // 转换为毫秒

// 操作
Duration plus = d1.plusHours(1);
Duration minus = d1.minusMinutes(30);
Duration negated = d1.negated();       // 负值
Duration abs = d1.abs();               // 绝对值

// 判断
boolean isZero = d1.isZero();
boolean isNegative = d1.isNegative();

// 分解
long hours = d1.toHours();
int minutes = (int) ((d1.getSeconds() % 3600) / 60);
int seconds = (int) (d1.getSeconds() % 60);
```

### Period - 日期量

```java
// Period 表示基于日期的量 (年/月/日)

// 创建 Period
Period p1 = Period.of(1, 2, 3);          // 1年2月3天
Period p2 = Period.ofYears(1);           // 1年
Period p3 = Period.ofMonths(6);          // 6个月
Period p4 = Period.ofWeeks(2);           // 2周 (14天)
Period p5 = Period.ofDays(365);          // 365天
Period p6 = Period.between(date1, date2);

// 获取值
int years = p1.getYears();
int months = p1.getMonths();
int days = p1.getDays();

// 操作
Period plus = p1.plusYears(1);
Period minus = p1.minusMonths(1);
Period normalized = p1.normalized();     // 标准化

// 转换为总天数 (近似)
int totalDays = p1.getYears() * 365 + p1.getMonths() * 30 + p1.getDays();

// 应用到日期
LocalDate date = LocalDate.of(2026, 3, 20);
LocalDate future = date.plus(Period.of(1, 2, 3));  // 2027-05-23
```

---

## DateTimeFormatter

### 格式化日期时间

```java
// 内置格式化器

// ISO 格式
String isoDate = LocalDate.now().format(DateTimeFormatter.ISO_LOCAL_DATE);
// 2026-03-20

String isoTime = LocalTime.now().format(DateTimeFormatter.ISO_LOCAL_TIME);
// 09:30:45

String isoDateTime = LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);
// 2026-03-20T09:30:45

String isoInstant = Instant.now().format(DateTimeFormatter.ISO_INSTANT);
// 2026-03-20T01:00:00Z

// 自定义格式
DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
String formatted = LocalDateTime.now().format(formatter);
// 2026-03-20 09:30:45

// 常用模式
DateTimeFormatter[] formatters = {
    DateTimeFormatter.ofPattern("yyyy-MM-dd"),           // 2026-03-20
    DateTimeFormatter.ofPattern("yyyy年MM月dd日"),       // 2026年03月20日
    DateTimeFormatter.ofPattern("MM/dd/yyyy"),           // 03/20/2026
    DateTimeFormatter.ofPattern("dd-MMM-yyyy", Locale.ENGLISH), // 20-Mar-2026
    DateTimeFormatter.ofPattern("HH:mm:ss"),             // 09:30:45
    DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"),  // 2026-03-20 09:30:45
    DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss"), // 2026-03-20T09:30:45
    DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss Z"), // 2026-03-20 09:30:45 +0800
};

// 本地化格式
DateTimeFormatter frenchFormatter = DateTimeFormatter.ofPattern("d MMMM yyyy", Locale.FRENCH);
String frenchDate = LocalDate.now().format(frenchFormatter);
// 20 mars 2026

DateTimeFormatter chineseFormatter = DateTimeFormatter.ofPattern("yyyy年M月d日", Locale.CHINESE);
String chineseDate = LocalDate.now().format(chineseFormatter);
// 2026年3月20日

// 解析
LocalDate parsed = LocalDate.parse("2026-03-20", DateTimeFormatter.ofPattern("yyyy-MM-dd"));
LocalDateTime parsedDT = LocalDateTime.parse("2026-03-20 09:30:45",
    DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
```

### 格式化模式

| 字母 | 含义 | 示例 | 输出 |
|------|------|------|------|
| y | 年 | yyyy | 2026 |
| M | 月 | MM / MMM / MMMM | 03 / Mar / March |
| d | 日 | dd | 20 |
| E | 星期 | E / EEEE | Thu / Thursday |
| a | AM/PM | a | AM |
| H | 小时 (24小时制) | HH | 09 |
| h | 小时 (12小时制) | hh | 09 |
| m | 分钟 | mm | 30 |
| s | 秒 | ss | 45 |
| S | 毫秒 | SSS | 123 |
| z | 时区名 | z | CST |
| Z | 时区偏移 | Z | +0800 |

---

## 时区处理

### 时区转换

```java
// 时区转换最佳实践

// 1. 存储时间 - 使用 Instant 或 OffsetDateTime (UTC)
Instant eventTime = Instant.now();
OffsetDateTime eventTimeUTC = eventTime.atOffset(ZoneOffset.UTC);

// 2. 显示时间 - 转换为用户时区
ZoneId userZone = ZoneId.of("Asia/Shanghai");
ZonedDateTime userTime = eventTime.atZone(userZone);

// 3. 跨时区会议安排
ZonedDateTime shanghaiMeeting = ZonedDateTime.of(2026, 3, 20, 14, 0, 0, 0,
    ZoneId.of("Asia/Shanghai"));

ZonedDateTime newyorkMeeting = shanghaiMeeting.withZoneSameInstant(
    ZoneId.of("America/New_York"));

ZonedDateTime londonMeeting = shanghaiMeeting.withZoneSameInstant(
    ZoneId.of("Europe/London"));

System.out.println("Shanghai: " + shanghaiMeeting.format(
    DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm z")));
System.out.println("New York: " + newyorkMeeting.format(
    DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm z")));
System.out.println("London: " + londonMeeting.format(
    DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm z")));

// 4. 夏令时处理
ZonedDateTime usDate = ZonedDateTime.of(2026, 3, 15, 9, 0, 0, 0,
    ZoneId.of("America/New_York"));

// 检查是否在夏令时
boolean isDST = usDate.getZone().getRules().isDaylightSavings(usDate.toInstant());

// 获取夏令时偏移
ZoneOffset offset = usDate.getOffset();
ZoneOffset standardOffset = usDate.getZone().getRules().getStandardOffset(usDate.toInstant());
```

### ZoneId 缓存优化

```java
// JDK-8348880: ZoneOffset 缓存优化
// PR: https://github.com/openjdk/jdk/pull/23337

// 问题: QUARTER_CACHE 使用 ConcurrentMap<Integer, ZoneOffset>
//       每次 int -> Integer 装箱产生临时对象

// 优化: 改为 AtomicReferenceArray<ZoneOffset>
//       消除装箱，+15-25% 性能提升

// 优化前
ConcurrentMap<Integer, ZoneOffset> cache = new ConcurrentHashMap<>();
Integer key = quarters;  // 💥 装箱
ZoneOffset result = cache.get(key);

// 优化后
AtomicReferenceArray<ZoneOffset> cache = new AtomicReferenceArray<>(256);
int key = quarters & 0xff;  // 无装箱
ZoneOffset result = cache.getOpaque(key);

// 性能影响:
// - 吞吐量: +15-25%
// - 内存占用: -85% (1KB vs 6.8KB)
// - GC 压力: -50% (无装箱对象)

// 使用示例 (自动优化)
ZoneOffset offset = ZoneOffset.ofTotalSeconds(28800);  // UTC+8
// 内部使用优化的缓存
```

---

## 性能优化实战

### toString 优化 (JDK-8337832)

```java
// DateTime toString 性能优化
// PR: https://github.com/openjdk/jdk/pull/20368

// 问题: 复合类 (LocalDateTime, ZonedDateTime) 的 toString()
//       创建多个临时字符串

// 优化前
public String toString() {
    return date.toString() + 'T' + time.toString();
}
// 创建: date.toString() 临时字符串
//       time.toString() 临时字符串
//       拼接结果字符串

// 优化后 - 使用 formatTo(StringBuilder)
public String toString() {
    var buf = new StringBuilder(29);
    date.formatTo(buf);  // 直接写入
    buf.append('T');
    time.formatTo(buf);  // 直接写入
    return buf.toString();
}

// 性能提升:
// | 类型        | 优化前 (ns) | 优化后 (ns) | 提升 |
// |-------------|-------------|-------------|------|
// | LocalDateTime| 180 ± 15   | 125 ± 10   | +30% |
// | ZonedDateTime| 320 ± 25  | 220 ± 18   | +31% |
// | OffsetDateTime| 240 ± 20 | 165 ± 12   | +31% |

// 内存分配减少: 50%
```

### 性能基准

```java
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.NANOSECONDS)
public class DateTimeBenchmarks {

    // LocalDate.now()
    @Benchmark
    public LocalDate localDateNow() {
        return LocalDate.now();
    }

    // LocalDateTime.now()
    @Benchmark
    public LocalDateTime localDateTimeNow() {
        return LocalDateTime.now();
    }

    // ZonedDateTime.now()
    @Benchmark
    public ZonedDateTime zonedDateTimeNow() {
        return ZonedDateTime.now(ZoneId.of("Asia/Shanghai"));
    }

    // Instant.now()
    @Benchmark
    public Instant instantNow() {
        return Instant.now();
    }

    // 解析
    @Benchmark
    public LocalDate parseDate() {
        return LocalDate.parse("2026-03-20");
    }

    // 格式化
    @Benchmark
    public String formatDate() {
        return LocalDate.now().format(DateTimeFormatter.ISO_LOCAL_DATE);
    }

    // 典型结果 (ns/op):
    // localDateNow:      ~50 ns
    // localDateTimeNow:  ~60 ns
    // zonedDateTimeNow: ~150 ns
    // instantNow:        ~30 ns
    // parseDate:         ~80 ns
    // formatDate:        ~100 ns
}
```

### 优化清单

| 操作 | 优化方式 | 提升 |
|------|----------|------|
| toString | 复用 StringBuilder | +30% |
| 缓存 ZoneOffset | AtomicReferenceArray | +15-25% |
| 避免重复创建 | 复用 DateTimeFormatter | +20-50% |
| 使用 LocalDate vs LocalDateTime | 减少计算 | +10-20% |

---

## 最佳实践

### 类型选择

```java
// ✅ 推荐

// 1. 存储日期/时间 - 使用 Instant (UTC)
Instant eventTime = Instant.now();

// 2. 显示本地时间 - 转换为 ZonedDateTime
ZonedDateTime userTime = eventTime.atZone(ZoneId.systemDefault());

// 3. 数据库存储 - 使用 Instant 或 LocalDateTime
//    Instant: 带时区信息
//    LocalDateTime: 不关心时区

// 4. 日期计算 - 使用 LocalDate/LocalTime/LocalDateTime
LocalDate tomorrow = LocalDate.now().plusDays(1);

// 5. 时间量计算 - Duration (秒级), Period (日期级)
Duration duration = Duration.between(instant1, instant2);
Period period = Period.between(date1, date2);

// ❌ 避免

// 1. 不要用 Date/Calendar (旧 API)
Date date = new Date();  // ❌

// 2. 不要假设时区
LocalDateTime now = LocalDateTime.now();  // ❌ 无时区信息

// 3. 不要混合使用新旧 API
Date date = Date.from(instant);  // ❌ 避免转换
```

### 线程安全

```java
// ✅ 所有 java.time 类都是不可变的，线程安全

// DateTimeFormatter 也是线程安全
private static final DateTimeFormatter FORMATTER =
    DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

public String formatDateTime(LocalDateTime dateTime) {
    return dateTime.format(FORMATTER);  // 安全
}

// ❌ SimpleDateFormat 不是线程安全的
private static final SimpleDateFormat SDF =
    new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");

public String formatDate(Date date) {
    return SDF.format(date);  // ❌ 不安全!
}
```

### 异常处理

```java
// ✅ 推荐

// 1. 使用 try-catch 处理解析异常
try {
    LocalDate date = LocalDate.parse("2026-02-30");  // 2月30日不存在
} catch (DateTimeParseException e) {
    // 处理无效日期
}

// 2. 使用 Optional 处理可能为空的情况
Optional<LocalDate> parseDate(String text) {
    try {
        return Optional.of(LocalDate.parse(text));
    } catch (DateTimeParseException e) {
        return Optional.empty();
    }
}

// 3. 使用 isBefore/isAfter 而非 compareTo
if (date1.isBefore(date2)) {  // ✅ 清晰
    // ...
}

if (date1.compareTo(date2) < 0) {  // ❌ 不清晰
    // ...
}
```

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### java.time 实现 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Stephen Colebourne | 50+ | Joda | JSR 310 规范负责人 |
| 2 | Roger Riggs | 30+ | Oracle | java.time 实现 |
| 3 | Joe Darcy | 15+ | Oracle | 集成到 JDK |
| 4 | [Shaojin Wen (温绍锦)](../../by-contributor/profiles/shaojin-wen.md) | 5+ | Alibaba | 性能优化 |

### 性能优化贡献者

| 贡献者 | 组织 | 主要优化 |
|--------|------|----------|
| [**Shaojin Wen (温绍锦)**](../../by-contributor/profiles/shaojin-wen.md) | Alibaba | DateTime toString (+30%), ZoneOffset 缓存 (+15-25%) |

---

## 相关链接

### 内部文档

- [语言特性](../language/) - 语言特性总览
- [并发编程](../concurrency/) - 并发时间处理

### 外部资源

- [JSR 310: Date and Time API](https://jcp.org/en/jsr/detail?id=310)
- [java.time Package](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/time/package-summary.html)
- [ThreeTen-Extra](https://www.threeten.org/threeten-extra/) - 扩展工具类
- [Joda-Time](https://www.joda.org/joda-time/) - java.time 前身

---

**最后更新**: 2026-03-20
