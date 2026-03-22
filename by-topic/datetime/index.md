# 日期时间 API

> JSR 310、java.time、时区处理、格式化、Stephen Colebourne 与 Joda-Time

[← 返回主题索引](../by-topic/)

---

## 1. 快速概览

```
JDK 1.0 ── JDK 1.1 ── JDK 5 ── JDK 8 ── JDK 21+
   │        │        │        │        │
Date      Calendar JSR 310  java.time 性能优化
问题      修复      预览     (JSR310) +5-40%
```

### 核心演进

| 版本 | 特性 | JEP | 说明 |
|------|------|-----|------|
| **JDK 1.0** | java.util.Date | - | 原始日期类，可变、线程不安全 |
| **JDK 1.1** | java.util.Calendar | - | 改进的日历 API，仍然笨重 |
| **JDK 8** | java.time | JSR 310 | 正式发布，不可变、ISO-8601 默认 |
| **JDK 9** | 模块化 | - | java.time 归入 java.base 模块 |
| **JDK 21+** | 性能优化 | - | toString +30%, 缓存 +15-25% |

---

## 目录

- [java.time 设计哲学](#javatime-设计哲学)
- [为什么需要 java.time](#为什么需要-javatime)
- [核心类型](#核心类型)
- [核心类型深入 — 内部表示](#核心类型深入--内部表示)
- [LocalDate/LocalTime/LocalDateTime](#localdatelocaltimelocaldatetime)
- [ZonedDateTime/OffsetDateTime](#zoneddatetimeoffsetdatetime)
- [Instant/Duration/Period](#instantdurationperiod)
- [Duration vs Period 为什么分开](#duration-vs-period-为什么分开)
- [DateTimeFormatter](#datetimeformatter)
- [TemporalAdjusters 与 TemporalQueries](#temporaladjusters-与-temporalqueries)
- [时区处理](#时区处理)
- [Clock — 测试友好的时间抽象](#clock--测试友好的时间抽象)
- [从 Date/Calendar 迁移](#从-datecalendar-迁移)
- [性能优化实战](#性能优化实战)
- [Stephen Colebourne 与 JSR 310](#stephen-colebourne-与-jsr-310)
- [最佳实践](#最佳实践)
- [核心贡献者](#核心贡献者)
- [相关链接](#相关链接)

---

## 2. java.time 设计哲学

java.time 的设计建立在四大原则 (design principles) 之上，这些原则直接源于 Joda-Time 十年的实战经验。

### 不可变 (Immutability)

所有核心类 (`LocalDate`, `Instant`, `ZonedDateTime` 等) 都是 `final` 且不可变的。每次"修改"操作都返回新实例 (new instance)，原对象不变。这保证了天然的线程安全 (thread safety) — 无需同步即可在多线程间共享。

### ISO-8601 默认 (ISO-8601 by Default)

java.time 默认使用 ISO-8601 日历系统。`LocalDate.parse("2026-03-22")` 无需指定格式即可工作。所有 `toString()` 输出也遵循 ISO-8601。非 ISO 日历 (如日本历、伊斯兰历) 通过 `java.time.chrono` 包支持，但核心 API 不依赖它们。

### 领域驱动: Human Time vs Machine Time

这是 java.time 最关键的设计区分:

| 维度 | Human Time (人类时间) | Machine Time (机器时间) |
|------|----------------------|------------------------|
| 核心类 | `LocalDate`, `LocalTime`, `LocalDateTime`, `ZonedDateTime` | `Instant` |
| 含义 | 日历上的日期/钟表上的时间 | 时间线 (timeline) 上的一个点 |
| 时区 | 可能有、可能没有 | 始终 UTC |
| 用途 | 显示给用户、业务规则 | 时间戳、日志、计算间隔 |
| 类比 | "2026年3月22日下午3点" | `1742655600` (epoch seconds) |

`Duration` 桥接两者 — 它用秒和纳秒精确度量时间量，可同时应用于 Human Time 和 Machine Time。`Period` 则纯粹属于 Human Time 领域 (年/月/日)。

### 类型安全的枚举 (Type-Safe Enums)

```java
Month month = Month.JANUARY;          // 1 月 = 1，不是 0
DayOfWeek day = DayOfWeek.MONDAY;     // 星期一 = 1
```

告别了 `Calendar.JANUARY == 0` 的陷阱。

---

## 3. 为什么需要 java.time

### 旧 API 的问题

```java
// 1. 可变 + 非线程安全 (mutable, not thread-safe)
Date date = new Date();
date.setTime(System.currentTimeMillis());  // 可变，多线程不安全

// 2. 设计混乱 — 名字是 Date 却表示日期+时间
Calendar cal = Calendar.getInstance();
cal.set(Calendar.MONTH, 12);  // 运行时错误，月份是 0-11

// 3. SimpleDateFormat 线程不安全
SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
// 多线程共享会导致数据错乱!

// 4. 奇怪的偏移量
int year = date.getYear();   // 返回 1900 年以来的年数
int month = date.getMonth(); // 0-11，容易出错
```

### java.time 的优势

```java
// 1. 不可变 - 线程安全
LocalDate date = LocalDate.now();
LocalDate date2 = date.plusDays(1);  // 返回新对象，原对象不变

// 2. 清晰的类型分离 (clear type separation)
LocalDate      date = LocalDate.now();          // 日期
LocalTime      time = LocalTime.now();          // 时间
LocalDateTime  dateTime = LocalDateTime.now();  // 日期时间
Instant        instant = Instant.now();         // 时间戳

// 3. 类型安全的枚举
Month month = Month.JANUARY;          // JANUARY = 1
DayOfWeek day = DayOfWeek.MONDAY;     // MONDAY = 1

// 4. 流式 API (fluent API)
LocalDate tomorrow = LocalDate.now()
    .plusDays(1)
    .with(TemporalAdjusters.next(DayOfWeek.MONDAY));

// 5. 线程安全的格式化
DateTimeFormatter formatter = DateTimeFormatter.ISO_LOCAL_DATE;
String formatted = LocalDate.now().format(formatter);
```

---

## 4. 核心类型

### 类型层次

```
java.time (核心包)
├── LocalDate           # 日期 (年月日) — Human Time
├── LocalTime           # 时间 (时分秒纳秒) — Human Time
├── LocalDateTime       # 日期时间 (无时区) — Human Time
├── ZonedDateTime       # 日期时间 (带时区) — Human Time
├── OffsetDateTime      # 日期时间 (带 UTC 偏移) — Human Time
├── Instant             # 时间戳 (UTC) — Machine Time
├── Duration            # 时间量 (秒/纳秒) — 跨域
├── Period              # 日期量 (年月日) — Human Time
├── ZoneId              # 时区 ID (如 "Asia/Shanghai")
├── ZoneOffset          # UTC 偏移 (如 "+08:00")
└── DateTimeFormatter   # 格式化器

java.time.temporal (扩展)
├── TemporalAdjuster    # 时间调整器 (函数式接口)
├── TemporalAdjusters   # 内置调整器工厂
├── TemporalQuery       # 时间查询 (函数式接口)
├── TemporalQueries     # 内置查询工厂
├── ChronoUnit          # 时间单位枚举
└── ChronoField         # 时间字段枚举
```

### 选择指南

| 需求 | 使用类型 | 示例 |
|------|----------|------|
| 生日、纪念日 | LocalDate | `LocalDate.of(2000, Month.JANUARY, 1)` |
| 每日提醒时间 | LocalTime | `LocalTime.of(9, 0)` |
| 本地日期时间 | LocalDateTime | `LocalDateTime.now()` |
| 全球活动时间 | ZonedDateTime | `ZonedDateTime.now(ZoneId.of("Asia/Shanghai"))` |
| 数据库 TIMESTAMP WITH TIME ZONE | OffsetDateTime | `OffsetDateTime.now(ZoneOffset.UTC)` |
| UTC 时间戳 | Instant | `Instant.now()` |
| 机器间隔 | Duration | `Duration.ofHours(2)` |
| 人类间隔 | Period | `Period.of(1, 2, 3)` — 1年2月3天 |

---

## 5. 核心类型深入 — 内部表示

从 JDK 源码 (`src/java.base/share/classes/java/time/`) 可以验证每个核心类的内部存储方式。这些字段揭示了设计取舍 (design trade-offs)。

### LocalDate — 三个字段

```java
// java/time/LocalDate.java
private final transient int year;    // 年 (int, 足够覆盖 Year.MIN_VALUE 到 MAX_VALUE)
private final transient byte month;  // 月 (byte, 1-12)
private final transient byte day;    // 日 (byte, 1-31)
```

注意 `transient` — LocalDate 不依赖默认序列化，而是通过 `writeReplace()` 使用自定义序列化格式。`month` 和 `day` 使用 `byte` 节省内存 (每个实例仅 16 bytes 对象头 + 6 bytes 字段)。

### LocalTime — 四个字段

```java
// java/time/LocalTime.java
private final byte hour;    // 小时 (0-23)
private final byte minute;  // 分钟 (0-59)
private final byte second;  // 秒 (0-59)
private final int nano;     // 纳秒 (0-999,999,999)
```

纳秒用 `int` 而非 `long` — 因为 999,999,999 < Integer.MAX_VALUE (2,147,483,647)。这是精心的空间优化。

### LocalDateTime — 组合模式

```java
// java/time/LocalDateTime.java
private final LocalDate date;
private final LocalTime time;
```

不重复存储字段，直接组合 (composition) LocalDate 和 LocalTime。这是典型的领域驱动设计 — LocalDateTime "有一个" (has-a) 日期和一个时间。

### ZonedDateTime — 三元组

```java
// java/time/ZonedDateTime.java
private final LocalDateTime dateTime;
private final ZoneOffset offset;
private final ZoneId zone;
```

同时保存 `offset` 和 `zone` 看似冗余，但这是处理 DST (夏令时) 的关键 — `zone` 包含规则，`offset` 记录当前实际偏移。在 DST overlap 时段，同一个 LocalDateTime + ZoneId 可能对应两个不同的 offset。

### Instant — 纯机器时间

```java
// java/time/Instant.java
private final long seconds;  // 距 epoch (1970-01-01T00:00:00Z) 的秒数
private final int nanos;     // 纳秒部分 (0-999,999,999)
```

最小表示: 一个 `long` + 一个 `int`，覆盖从约公元前 10 亿年到公元后 10 亿年的纳秒精度时间线。

### Duration 与 Period

```java
// java/time/Duration.java — 精确时间量
private final long seconds;   // 秒
private final int nanos;      // 纳秒部分

// java/time/Period.java — 日期量
private final int years;
private final int months;
private final int days;
```

Duration 与 Instant 结构相同 (seconds + nanos)，因为它度量的是绝对时间差。Period 使用三个独立的 `int` 字段，因为"1个月"的实际天数取决于具体月份 — 它不能归约为秒。

---

## 6. LocalDate/LocalTime/LocalDateTime

### LocalDate - 日期

```java
// 创建 LocalDate

// 1. 当前日期
LocalDate today = LocalDate.now();  // 2026-03-22

// 2. 指定日期
LocalDate date1 = LocalDate.of(2026, 3, 22);
LocalDate date2 = LocalDate.of(2026, Month.MARCH, 22);
LocalDate date3 = LocalDate.ofYearDay(2026, 81);  // 2026 年第 81 天

// 3. 从文本解析
LocalDate date4 = LocalDate.parse("2026-03-22");
LocalDate date5 = LocalDate.parse("20260322", DateTimeFormatter.BASIC_ISO_DATE);

// 日期操作
LocalDate date = LocalDate.of(2026, 3, 22);

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

// 调整器 (TemporalAdjusters)
LocalDate nextMonday = date.with(TemporalAdjusters.next(DayOfWeek.MONDAY));
LocalDate firstDayOfMonth = date.with(TemporalAdjusters.firstDayOfMonth());
LocalDate lastDayOfYear = date.with(TemporalAdjusters.lastDayOfYear());

// 获取信息
int year = date.getYear();              // 2026
Month month = date.getMonth();          // MARCH
int dayOfMonth = date.getDayOfMonth();  // 22
DayOfWeek dayOfWeek = date.getDayOfWeek(); // SUNDAY
int dayOfYear = date.getDayOfYear();    // 81
boolean isLeap = date.isLeapYear();     // false

// 日期计算
long daysBetween = ChronoUnit.DAYS.between(date1, date2);
long monthsBetween = ChronoUnit.MONTHS.between(date1, date2);

Period period = Period.between(date1, date2);

// 判断
boolean isBefore = date1.isBefore(date2);
boolean isAfter = date1.isAfter(date2);
boolean isEqual = date1.isEqual(date2);
```

### LocalTime - 时间

```java
// 创建
LocalTime now = LocalTime.now();
LocalTime time1 = LocalTime.of(9, 30);              // 09:30
LocalTime time2 = LocalTime.of(9, 30, 45);          // 09:30:45
LocalTime time3 = LocalTime.of(9, 30, 45, 123456789); // 含纳秒

// 截断 (truncation)
LocalTime truncated = time2.truncatedTo(ChronoUnit.MINUTES);  // 09:30

// 时间计算
Duration duration = Duration.between(time1, time2);
```

### LocalDateTime - 日期时间

```java
// 创建
LocalDateTime now = LocalDateTime.now();
LocalDateTime dt1 = LocalDateTime.of(2026, 3, 22, 9, 30);
LocalDateTime dt2 = LocalDateTime.of(LocalDate.now(), LocalTime.now());
LocalDateTime dt3 = LocalDate.now().atStartOfDay();  // 当天 00:00

// 分解
LocalDate datePart = dt1.toLocalDate();
LocalTime timePart = dt1.toLocalTime();
```

---

## 7. ZonedDateTime/OffsetDateTime

### 时区基础

```java
// ZoneId — 基于区域的时区标识符 (region-based zone ID)
ZoneId shanghai = ZoneId.of("Asia/Shanghai");
ZoneId newyork = ZoneId.of("America/New_York");
ZoneId systemDefault = ZoneId.systemDefault();

// ZoneOffset — 固定的 UTC 偏移 (fixed offset)
ZoneOffset offsetPlus8 = ZoneOffset.of("+08:00");
ZoneOffset utc = ZoneOffset.UTC;
```

**ZoneId vs ZoneOffset 的区别**: `ZoneId` 是逻辑时区，包含 DST 规则 (通过 `ZoneRules`)；`ZoneOffset` 是物理偏移量，不知道 DST。`ZoneOffset` 是 `ZoneId` 的子类，但语义完全不同。

### ZonedDateTime - 带时区日期时间

```java
// 创建
ZonedDateTime shanghaiNow = ZonedDateTime.now(ZoneId.of("Asia/Shanghai"));
ZonedDateTime newyorkNow = ZonedDateTime.now(ZoneId.of("America/New_York"));

// 从 LocalDateTime 附加时区
LocalDateTime dt = LocalDateTime.of(2026, 3, 22, 9, 30);
ZonedDateTime shanghai = dt.atZone(ZoneId.of("Asia/Shanghai"));

// 从 Instant 转换
Instant instant = Instant.now();
ZonedDateTime zdt = instant.atZone(ZoneId.of("Asia/Shanghai"));

// 时区转换 — 保持同一瞬间 (same instant)
ZonedDateTime newyork = shanghai.withZoneSameInstant(ZoneId.of("America/New_York"));

// 保留本地时间，更改时区 — 不同瞬间 (different instant)
ZonedDateTime sameLocal = shanghai.withZoneSameLocal(ZoneId.of("America/New_York"));
```

### OffsetDateTime — 数据库友好

```java
// OffsetDateTime 使用固定偏移，不考虑夏令时
OffsetDateTime now = OffsetDateTime.now();
OffsetDateTime utcNow = OffsetDateTime.now(ZoneOffset.UTC);

// 适合场景: SQL TIMESTAMP WITH TIME ZONE
// JDBC 4.2+ 原生支持 OffsetDateTime
PreparedStatement ps = conn.prepareStatement("INSERT INTO events(ts) VALUES(?)");
ps.setObject(1, OffsetDateTime.now(ZoneOffset.UTC));
```

**何时用哪个**: `ZonedDateTime` 用于需要 DST 感知的场景 (如调度任务、用户界面显示)；`OffsetDateTime` 用于需要确定偏移的场景 (如数据库存储、REST API 传输)。

---

## 8. Instant/Duration/Period

### Instant - 时间戳

```java
// Instant 表示 UTC 时间线上的一个点 (a point on the timeline)
Instant now = Instant.now();

// 从 epoch 秒/毫秒创建
Instant fromEpoch = Instant.ofEpochSecond(1742655600);
Instant fromEpochMilli = Instant.ofEpochMilli(1742655600000L);

// 从文本解析 (必须是 UTC 格式)
Instant parsed = Instant.parse("2026-03-22T09:00:00Z");

// 获取 epoch 值
long epochSecond = now.getEpochSecond();
long epochMilli = now.toEpochMilli();
int nano = now.getNano();  // 纳秒部分 (0-999,999,999)

// 转换到 Human Time
ZonedDateTime userTime = now.atZone(ZoneId.of("Asia/Shanghai"));
OffsetDateTime utcTime = now.atOffset(ZoneOffset.UTC);
```

### Duration - 时间量

```java
// Duration — 基于秒的精确时间量
Duration d1 = Duration.ofHours(2);
Duration d2 = Duration.ofMinutes(120);
Duration d3 = Duration.between(instant1, instant2);

// 获取值
long totalSeconds = d1.getSeconds();
long totalMinutes = d1.toMinutes();
long totalMillis = d1.toMillis();

// JDK 9+ 分解方法
long hours = d1.toHoursPart();     // 小时部分
int minutes = d1.toMinutesPart();  // 分钟部分
int seconds = d1.toSecondsPart();  // 秒部分
```

### Period - 日期量

```java
// Period — 基于日期的量 (年/月/日)
Period p1 = Period.of(1, 2, 3);          // 1年2月3天
Period p2 = Period.ofWeeks(2);           // 2周 = 14天
Period p3 = Period.between(date1, date2);

// 标准化 (normalized): 将月数溢出转为年
Period p4 = Period.of(0, 14, 0).normalized();  // P1Y2M

// 应用到日期
LocalDate date = LocalDate.of(2026, 3, 22);
LocalDate future = date.plus(Period.of(1, 2, 3));  // 2027-05-25
```

---

## 9. Duration vs Period 为什么分开

这是 java.time 初学者最常问的设计问题之一。

### 根本原因: 时间不是均匀的

```java
// "1 个月"有多少天？
LocalDate jan = LocalDate.of(2026, 1, 31);
LocalDate feb = jan.plusMonths(1);  // 2026-02-28 (28 天)
LocalDate mar = feb.plusMonths(1);  // 2026-03-28 (28 天)

LocalDate mar31 = LocalDate.of(2026, 3, 31);
LocalDate apr = mar31.plusMonths(1);  // 2026-04-30 (30 天)

// 同一个"1个月"在不同月份代表不同的天数!
// 因此 Period 无法精确转换为秒/天
```

### 对比

| 特性 | Duration | Period |
|------|----------|--------|
| 内部字段 | `long seconds` + `int nanos` | `int years` + `int months` + `int days` |
| 精确性 | 绝对精确 | 相对的 (依赖起始日期) |
| 可比较 | `d1.compareTo(d2)` 有意义 | 无法比较 (1个月 vs 30天?) |
| 适用类型 | `Instant`, `LocalTime`, `LocalDateTime` | `LocalDate`, `LocalDateTime` |
| ISO 表示 | `PT2H30M` | `P1Y2M3D` |

```java
// Duration 用于精确计时
Duration timeout = Duration.ofSeconds(30);
Duration elapsed = Duration.between(startInstant, endInstant);

// Period 用于业务日期间隔
Period subscriptionLength = Period.ofMonths(12);
Period age = Period.between(birthday, LocalDate.now());
```

---

## 10. DateTimeFormatter

### 预定义格式化器 (Predefined Formatters)

```java
// ISO 格式 — 最常用
String isoDate = LocalDate.now().format(DateTimeFormatter.ISO_LOCAL_DATE);
// "2026-03-22"

String isoTime = LocalTime.now().format(DateTimeFormatter.ISO_LOCAL_TIME);
// "09:30:45"

String isoDateTime = LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);
// "2026-03-22T09:30:45"

// ISO_INSTANT 用于 Instant
String isoInstant = Instant.now().atOffset(ZoneOffset.UTC)
    .format(DateTimeFormatter.ISO_INSTANT);
// "2026-03-22T01:00:00Z"
```

### 自定义 Pattern

```java
DateTimeFormatter custom = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
String formatted = LocalDateTime.now().format(custom);
// "2026-03-22 09:30:45"

// 常用模式
DateTimeFormatter.ofPattern("yyyy年MM月dd日");       // 2026年03月22日
DateTimeFormatter.ofPattern("MM/dd/yyyy");            // 03/22/2026
DateTimeFormatter.ofPattern("dd-MMM-yyyy", Locale.ENGLISH); // 22-Mar-2026
```

### 本地化格式 (Localized Formatting)

```java
// ofLocalizedDate/ofLocalizedTime/ofLocalizedDateTime
DateTimeFormatter localized = DateTimeFormatter
    .ofLocalizedDate(FormatStyle.FULL)
    .withLocale(Locale.CHINESE);
String chinese = LocalDate.now().format(localized);
// "2026年3月22日星期日"

DateTimeFormatter french = DateTimeFormatter
    .ofLocalizedDate(FormatStyle.LONG)
    .withLocale(Locale.FRENCH);
String frenchDate = LocalDate.now().format(french);
// "22 mars 2026"
```

### 格式化模式速查

| 字母 | 含义 | 示例 | 输出 |
|------|------|------|------|
| y | 年 | yyyy | 2026 |
| M | 月 | MM / MMM / MMMM | 03 / Mar / March |
| d | 日 | dd | 22 |
| E | 星期 | E / EEEE | Sun / Sunday |
| a | AM/PM | a | AM |
| H | 小时 (24h) | HH | 09 |
| h | 小时 (12h) | hh | 09 |
| m | 分钟 | mm | 30 |
| s | 秒 | ss | 45 |
| S | 毫秒分数 | SSS | 123 |
| n | 纳秒 | nnnnnnnnn | 123456789 |
| z | 时区名 | z | CST |
| Z | 时区偏移 | Z | +0800 |
| X | ISO 偏移 | XXX | +08:00 |

### ResolverStyle — 解析严格度

DateTimeFormatter 有三种解析模式 (resolver style)，控制无效日期的处理方式:

```java
// STRICT — 严格模式: 所有字段必须合法
DateTimeFormatter strict = DateTimeFormatter.ofPattern("yyyy-MM-dd")
    .withResolverStyle(ResolverStyle.STRICT)
    .withChronology(IsoChronology.INSTANCE);
// LocalDate.parse("2026-02-29", strict) → 异常! 2026 不是闰年

// SMART — 智能模式 (默认): 自动调整到合法值
DateTimeFormatter smart = DateTimeFormatter.ofPattern("yyyy-MM-dd")
    .withResolverStyle(ResolverStyle.SMART);
// LocalDate.parse("2026-02-29", smart) → 2026-02-28 (调整到最后一天)

// LENIENT — 宽容模式: 允许溢出
DateTimeFormatter lenient = DateTimeFormatter.ofPattern("yyyy-MM-dd")
    .withResolverStyle(ResolverStyle.LENIENT);
// LocalDate.parse("2026-02-30", lenient) → 2026-03-02 (溢出到 3 月)
```

**注意**: ISO_LOCAL_DATE 等预定义格式化器使用 STRICT 模式；`ofPattern()` 创建的默认使用 SMART 模式。

---

## 11. TemporalAdjusters 与 TemporalQueries

### TemporalAdjusters — 函数式时间调整

`TemporalAdjuster` 是一个函数式接口 (functional interface): `Temporal adjustInto(Temporal temporal)`。`TemporalAdjusters` 工具类提供了丰富的内置实现。

```java
LocalDate date = LocalDate.of(2026, 3, 22);

// 内置调整器 (Built-in Adjusters)
date.with(TemporalAdjusters.firstDayOfMonth());      // 2026-03-01
date.with(TemporalAdjusters.lastDayOfMonth());        // 2026-03-31
date.with(TemporalAdjusters.firstDayOfYear());        // 2026-01-01
date.with(TemporalAdjusters.lastDayOfYear());         // 2026-12-31
date.with(TemporalAdjusters.firstDayOfNextMonth());   // 2026-04-01
date.with(TemporalAdjusters.firstDayOfNextYear());    // 2027-01-01

// 星期相关
date.with(TemporalAdjusters.next(DayOfWeek.MONDAY));         // 下一个周一
date.with(TemporalAdjusters.nextOrSame(DayOfWeek.MONDAY));   // 当天或下一个周一
date.with(TemporalAdjusters.previous(DayOfWeek.FRIDAY));     // 上一个周五
date.with(TemporalAdjusters.previousOrSame(DayOfWeek.FRIDAY));

// 月内第 N 个星期几
date.with(TemporalAdjusters.firstInMonth(DayOfWeek.MONDAY));   // 本月第一个周一
date.with(TemporalAdjusters.lastInMonth(DayOfWeek.FRIDAY));    // 本月最后一个周五
date.with(TemporalAdjusters.dayOfWeekInMonth(3, DayOfWeek.WEDNESDAY)); // 第三个周三
```

### 自定义 TemporalAdjuster

```java
// 方式一: Lambda 表达式
TemporalAdjuster nextWorkday = temporal -> {
    LocalDate d = LocalDate.from(temporal);
    DayOfWeek dow = d.getDayOfWeek();
    if (dow == DayOfWeek.FRIDAY) return d.plusDays(3);
    if (dow == DayOfWeek.SATURDAY) return d.plusDays(2);
    return d.plusDays(1);
};
LocalDate nextWork = date.with(nextWorkday);

// 方式二: ofDateAdjuster 工厂方法
TemporalAdjuster endOfQuarter = TemporalAdjusters.ofDateAdjuster(d -> {
    int month = d.getMonthValue();
    int quarterEnd = ((month - 1) / 3 + 1) * 3;
    return d.withMonth(quarterEnd).with(TemporalAdjusters.lastDayOfMonth());
});
LocalDate qEnd = date.with(endOfQuarter);  // 2026-03-31
```

### TemporalQueries — 从时间对象提取信息

`TemporalQuery<R>` 也是函数式接口: `R queryFrom(TemporalAccessor temporal)`。

```java
// 内置查询 (Built-in Queries)
ZoneId zone = ZonedDateTime.now().query(TemporalQueries.zoneId());
// Asia/Shanghai

ZoneOffset offset = OffsetDateTime.now().query(TemporalQueries.offset());
// +08:00

LocalDate date = LocalDateTime.now().query(TemporalQueries.localDate());
LocalTime time = LocalDateTime.now().query(TemporalQueries.localTime());

TemporalUnit precision = LocalDate.now().query(TemporalQueries.precision());
// DAYS (LocalDate 的精度是天)

// 自定义查询: 判断是否工作日
TemporalQuery<Boolean> isWorkday = temporal -> {
    DayOfWeek dow = DayOfWeek.from(temporal);
    return dow != DayOfWeek.SATURDAY && dow != DayOfWeek.SUNDAY;
};
boolean workday = LocalDate.of(2026, 3, 22).query(isWorkday);  // true (周日 → false)
```

---

## 12. 时区处理

### ZoneId vs ZoneOffset 深入

```java
// ZoneId 包含 ZoneRules — 历史和未来的偏移规则
ZoneId shanghai = ZoneId.of("Asia/Shanghai");
ZoneRules rules = shanghai.getRules();

// 查询某一瞬间的偏移
ZoneOffset offset = rules.getOffset(Instant.now());  // +08:00

// 查询标准偏移 (不含 DST)
ZoneOffset standardOffset = rules.getStandardOffset(Instant.now());

// 检查某一瞬间是否在夏令时
boolean isDST = rules.isDaylightSavings(Instant.now());
```

### DST 陷阱: Gap 与 Overlap

夏令时 (Daylight Saving Time) 产生两种特殊情况:

```java
// === Gap (间隙) — 时钟前拨，某些时间不存在 ===
// 美国东部 2026-03-08 02:00 → 03:00 (春季前拨)
LocalDateTime gapTime = LocalDateTime.of(2026, 3, 8, 2, 30);
ZonedDateTime gapZdt = gapTime.atZone(ZoneId.of("America/New_York"));
// 2:30 AM 不存在! java.time 自动调整为 3:30 AM (向后推)
System.out.println(gapZdt);
// 2026-03-08T03:30-04:00[America/New_York]

// === Overlap (重叠) — 时钟后拨，某些时间出现两次 ===
// 美国东部 2026-11-01 02:00 → 01:00 (秋季后拨)
LocalDateTime overlapTime = LocalDateTime.of(2026, 11, 1, 1, 30);
ZonedDateTime overlapZdt = overlapTime.atZone(ZoneId.of("America/New_York"));
// 1:30 AM 出现两次! 默认选择较早的偏移 (EDT, -04:00)

// 显式选择较晚的偏移 (EST, -05:00)
ZonedDateTime laterOffset = overlapZdt.withLaterOffsetAtOverlap();

// 检查是否处于 overlap
ZoneOffsetTransition transition = rules.getTransition(overlapTime);
if (transition != null && transition.isOverlap()) {
    // 处理重叠
}
```

### 时区转换最佳实践

```java
// 跨时区会议安排
ZonedDateTime shanghaiMeeting = ZonedDateTime.of(2026, 3, 22, 14, 0, 0, 0,
    ZoneId.of("Asia/Shanghai"));

ZonedDateTime newyorkMeeting = shanghaiMeeting.withZoneSameInstant(
    ZoneId.of("America/New_York"));
ZonedDateTime londonMeeting = shanghaiMeeting.withZoneSameInstant(
    ZoneId.of("Europe/London"));

// Shanghai: 2026-03-22 14:00 CST
// New York: 2026-03-22 02:00 EDT
// London:   2026-03-22 06:00 GMT
```

### ZoneOffset 缓存优化 (JDK-8348880)

```java
// PR: https://github.com/openjdk/jdk/pull/23337

// 问题: QUARTER_CACHE 使用 ConcurrentMap<Integer, ZoneOffset>
//       每次 int → Integer 装箱 (autoboxing) 产生临时对象

// 优化: 改为 AtomicReferenceArray<ZoneOffset>
//       消除装箱，无锁读取

// 性能影响:
// - 吞吐量: +15-25%
// - 内存占用: -85% (1KB vs 6.8KB)
// - GC 压力: 大幅降低 (无装箱对象)
```

---

## 13. Clock — 测试友好的时间抽象

`Clock` 是 java.time 中容易被忽视但极其重要的抽象类 (abstract class)。它的核心价值在于: **将"获取当前时间"这个副作用 (side effect) 变成可注入、可替换的依赖**。

### 内置 Clock 实现

```java
// 1. systemUTC() / systemDefaultZone() — 生产环境使用
Clock systemClock = Clock.systemUTC();
Clock defaultClock = Clock.systemDefaultZone();
Instant now = systemClock.instant();

// 2. fixed() — 冻结时间，适合单元测试
Clock fixedClock = Clock.fixed(
    Instant.parse("2026-03-22T09:00:00Z"),
    ZoneId.of("Asia/Shanghai")
);
LocalDateTime frozen = LocalDateTime.now(fixedClock);
// 永远返回 2026-03-22T17:00:00 (UTC+8)

// 3. offset() — 在基础时钟上加减偏移
Clock future = Clock.offset(Clock.systemUTC(), Duration.ofHours(24));
Instant tomorrowNow = future.instant();  // 明天的这个时刻

// 4. tick() — 按指定精度截断
Clock tickClock = Clock.tick(Clock.systemUTC(), Duration.ofSeconds(1));
// 只精确到秒，纳秒部分始终为 0

// 5. tickMillis() / tickSeconds() / tickMinutes() — 预定义精度
Clock millisClock = Clock.tickMillis(ZoneId.of("UTC"));
Clock secondsClock = Clock.tickSeconds(ZoneId.of("UTC"));
```

### 测试模式 (Testability Pattern)

```java
// ❌ 不可测试 — 直接调用 now()
public boolean isExpired(Order order) {
    return order.getExpireDate().isBefore(LocalDate.now());
}

// ✅ 注入 Clock — 可测试
public class OrderService {
    private final Clock clock;
    public OrderService(Clock clock) { this.clock = clock; }
    public boolean isExpired(Order order) {
        return order.getExpireDate().isBefore(LocalDate.now(clock));
    }
}

// 测试代码
Clock fixed = Clock.fixed(Instant.parse("2026-06-01T00:00:00Z"), ZoneOffset.UTC);
OrderService service = new OrderService(fixed);
```

---

## 14. 从 Date/Calendar 迁移

### 桥接方法 (Bridge Methods)

JDK 8 在旧类上添加了桥接方法，实现新旧 API 互操作:

```java
// === Date ↔ Instant ===
// Date → Instant
Date oldDate = new Date();
Instant instant = oldDate.toInstant();

// Instant → Date
Instant now = Instant.now();
Date newDate = Date.from(now);

// === Calendar ↔ Instant ===
Calendar cal = Calendar.getInstance();
Instant calInstant = cal.toInstant();

// === Calendar ↔ ZonedDateTime ===
// GregorianCalendar → ZonedDateTime
GregorianCalendar gcal = new GregorianCalendar();
ZonedDateTime zdt = gcal.toZonedDateTime();

// ZonedDateTime → GregorianCalendar
GregorianCalendar backToGcal = GregorianCalendar.from(zdt);

// === TimeZone ↔ ZoneId ===
TimeZone tz = TimeZone.getTimeZone("Asia/Shanghai");
ZoneId zoneId = tz.toZoneId();
TimeZone backToTz = TimeZone.getTimeZone(zoneId);

// === java.sql 类型 ===
// java.sql.Date ↔ LocalDate
java.sql.Date sqlDate = java.sql.Date.valueOf(LocalDate.now());
LocalDate localDate = sqlDate.toLocalDate();

// java.sql.Time ↔ LocalTime
java.sql.Time sqlTime = java.sql.Time.valueOf(LocalTime.now());
LocalTime localTime = sqlTime.toLocalTime();

// java.sql.Timestamp ↔ LocalDateTime / Instant
java.sql.Timestamp ts = java.sql.Timestamp.valueOf(LocalDateTime.now());
LocalDateTime ldt = ts.toLocalDateTime();
Instant tsInstant = ts.toInstant();
```

### 常见迁移陷阱

```java
// 陷阱 1: Date.toInstant() 丢失时区
Date date = new Date();
Instant instant = date.toInstant();
// 正确做法: 显式指定时区转换
ZonedDateTime zdt = instant.atZone(ZoneId.systemDefault());

// 陷阱 2: java.sql.Date.toInstant() 抛异常!
java.sql.Date sqlDate = java.sql.Date.valueOf("2026-03-22");
// sqlDate.toInstant();  // UnsupportedOperationException!
LocalDate ld = sqlDate.toLocalDate();  // ✅ 正确做法

// 陷阱 3: "YYYY" vs "yyyy"
DateTimeFormatter.ofPattern("yyyy-MM-dd");  // ✅ calendar year
DateTimeFormatter.ofPattern("YYYY-MM-dd");  // ⚠️ week-based year

// 陷阱 4: 月份偏移
// Calendar: JANUARY = 0;  java.time: Month.JANUARY.getValue() = 1
```

---

## 15. 性能优化实战

### toString 优化 (JDK-8337832)

```java
// PR: https://github.com/openjdk/jdk/pull/20368
// 贡献者: Shaojin Wen (温绍锦)

// 问题: 复合类的 toString() 创建多个临时字符串 (temporary strings)

// 优化前
public String toString() {
    return date.toString() + 'T' + time.toString();
}
// 分配: date.toString() 临时串 + time.toString() 临时串 + 拼接结果串

// 优化后 — 使用 formatTo(StringBuilder)
public String toString() {
    var buf = new StringBuilder(29);
    date.formatTo(buf);  // 直接写入 buffer
    buf.append('T');
    time.formatTo(buf);  // 直接写入 buffer
    return buf.toString();
}

// 性能提升:
// | 类型           | 优化前 (ns) | 优化后 (ns) | 提升  |
// |----------------|-------------|-------------|-------|
// | LocalDateTime  | 180 ± 15    | 125 ± 10    | +30%  |
// | ZonedDateTime  | 320 ± 25    | 220 ± 18    | +31%  |
// | OffsetDateTime | 240 ± 20    | 165 ± 12    | +31%  |
//
// 内存分配减少约 50%
```

这一优化与 Compact Strings (JEP 254, JDK 9) 配合良好: 日期时间的 toString() 输出全部是 Latin-1 字符，StringBuilder 内部使用 `byte[]` 而非 `char[]`，每字符仅占 1 byte。`formatTo()` 避免创建临时 String 对象，进一步减少了从 `byte[]` 到 `char[]` 再到 `byte[]` 的无谓拷贝。

### 性能基准 (典型 JMH 结果, ns/op)

```
Benchmark                 Mode  Cnt    Score   Units
instantNow                avgt   10    ~30     ns/op
localDateNow              avgt   10    ~50     ns/op
localDateTimeNow          avgt   10    ~60     ns/op
zonedDateTimeNow          avgt   10   ~150     ns/op  ← 需要查 ZoneRules
parseDate                 avgt   10    ~80     ns/op
formatDate                avgt   10   ~100     ns/op
```
```

### 优化清单

| 操作 | 优化方式 | 提升 |
|------|----------|------|
| toString | 复用 StringBuilder (formatTo) | +30% |
| ZoneOffset 缓存 | AtomicReferenceArray 替代 ConcurrentHashMap | +15-25% |
| 避免重复创建 | 复用 DateTimeFormatter (声明为 static final) | +20-50% |
| 选择精确类型 | LocalDate 替代 LocalDateTime (减少计算) | +10-20% |
| Compact Strings | Latin-1 编码的 toString 输出受益 | 内存 -50% |

---

## 16. Stephen Colebourne 与 JSR 310

### 从 Joda-Time 到 java.time

Stephen Colebourne 是 java.time 的总设计师 (specification lead)，也是 Joda-Time 的创建者。

**时间线 (Timeline)**:

| 年份 | 事件 |
|------|------|
| 2002 | Colebourne 创建 Joda-Time，解决 java.util.Date/Calendar 的痛点 |
| 2007 | JSR 310 (Date and Time API) 正式提交 JCP，Colebourne 任 spec lead |
| 2008-2013 | JSR 310 经历多轮设计迭代，吸收 Joda-Time 经验教训 |
| 2014 | JDK 8 发布，java.time 作为 JSR 310 的实现正式入 JDK |
| 2014+ | ThreeTen-Extra 项目提供额外的时间类型 (如 `YearQuarter`, `Interval`) |

### Joda-Time vs java.time 的关键区别

| 方面 | Joda-Time | java.time |
|------|-----------|-----------|
| 空值处理 | 允许 null，常有 NPE | 全面拒绝 null，fail-fast |
| 日历系统 | 插件式，复杂 | chrono 包分离，核心 API 默认 ISO |
| 可扩展性 | 继承模型 | 接口 + 函数式 (TemporalAdjuster, TemporalQuery) |
| 格式化 | 自有 API | 独立的 DateTimeFormatter，线程安全 |
| 包结构 | `org.joda.time` | `java.time` (标准库，无额外依赖) |
| 精度 | 毫秒 | 纳秒 |

Colebourne 明确表示: java.time 不是 Joda-Time 的简单移植，而是基于其经验的"从头重新设计" (clean-room redesign)。核心原则: 不可变优先、清晰类型边界、ISO-8601 默认、拒绝 null、函数式扩展 (TemporalAdjuster/TemporalQuery 而非继承)。

---

## 17. 最佳实践

### 类型选择

```java
// ✅ 推荐

// 1. 存储时间 — 使用 Instant (UTC)
Instant eventTime = Instant.now();

// 2. 显示本地时间 — 转换为 ZonedDateTime
ZonedDateTime userTime = eventTime.atZone(ZoneId.systemDefault());

// 3. 数据库存储
//    Instant / OffsetDateTime(UTC): 需要全球统一的时间戳
//    LocalDateTime: 不关心时区的业务时间

// 4. 日期计算 — 使用 LocalDate
LocalDate tomorrow = LocalDate.now().plusDays(1);

// 5. 时间量 — Duration (秒级精度), Period (日期级)
Duration duration = Duration.between(instant1, instant2);
Period period = Period.between(date1, date2);

// ❌ 避免

// 1. 不要使用 Date/Calendar (旧 API)
Date date = new Date();  // ❌

// 2. 不要对 LocalDateTime 假设时区
LocalDateTime now = LocalDateTime.now();  // ❌ 无时区信息，不适合全球化

// 3. 不要每次创建 DateTimeFormatter
DateTimeFormatter.ofPattern("yyyy-MM-dd").format(date);  // ❌ 每次创建
private static final DateTimeFormatter FMT =
    DateTimeFormatter.ofPattern("yyyy-MM-dd");  // ✅ 复用
```

### 线程安全

```java
// ✅ java.time 所有类都是不可变的，天然线程安全
private static final DateTimeFormatter FORMATTER =
    DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

public String formatDateTime(LocalDateTime dateTime) {
    return dateTime.format(FORMATTER);  // 安全，可并发调用
}

// ❌ SimpleDateFormat 不是线程安全的
private static final SimpleDateFormat SDF =
    new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");

public String formatDate(Date date) {
    return SDF.format(date);  // ❌ 多线程下会产生错误结果!
}
```

### 异常处理

```java
// 用 try-catch 或 Optional 处理解析
Optional<LocalDate> parseDate(String text) {
    try {
        return Optional.of(LocalDate.parse(text));
    } catch (DateTimeParseException e) {
        return Optional.empty();
    }
}

// 使用语义化方法
if (date1.isBefore(date2)) { /* ... */ }  // ✅ 清晰
if (date1.compareTo(date2) < 0) { /* ... */ }  // ❌ 不清晰
```

---

## 18. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-22

### java.time 实现 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Stephen Colebourne | 50+ | Joda | JSR 310 规范负责人，核心设计者 |
| 2 | Roger Riggs | 30+ | Oracle | java.time 实现、集成 |
| 3 | Joe Darcy | 15+ | Oracle | 集成到 JDK |
| 4 | [Shaojin Wen (温绍锦)](../../by-contributor/profiles/shaojin-wen.md) | 5+ | Alibaba | 性能优化 (toString, ZoneOffset cache) |

### 性能优化贡献者

| 贡献者 | 组织 | 主要优化 |
|--------|------|----------|
| [**Shaojin Wen (温绍锦)**](../../by-contributor/profiles/shaojin-wen.md) | Alibaba | DateTime toString (+30%), ZoneOffset 缓存 (+15-25%) |

---

## 19. 相关链接

### 内部文档

- [语言特性](../language/) - 语言特性总览
- [并发编程](../concurrency/) - 并发时间处理

### 外部资源

- [JSR 310: Date and Time API](https://jcp.org/en/jsr/detail?id=310)
- [java.time Package (Javadoc)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/time/package-summary.html)
- [ThreeTen-Extra](https://www.threeten.org/threeten-extra/) - 扩展工具类 (YearQuarter, Interval 等)
- [Joda-Time](https://www.joda.org/joda-time/) - java.time 的前身
- [Stephen Colebourne's Blog](https://blog.joda.org/) - JSR 310 设计思考

---

**最后更新**: 2026-03-22
