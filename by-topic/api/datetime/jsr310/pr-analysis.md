# JSR 310 PR 分析

> java.time API 的实现历史和关键 PR

---
## 目录

1. [JSR 310: Date and Time API](#1-jsr-310-date-and-time-api)
2. [设计目标](#2-设计目标)
3. [背景历史](#3-背景历史)
4. [核心设计决策](#4-核心设计决策)
5. [关键 Issue 和 PR](#5-关键-issue-和-pr)
6. [与 Joda-Time 的差异](#6-与-joda-time-的差异)
7. [ThreeTen-Extra 扩展](#7-threeten-extra-扩展)
8. [社区反馈](#8-社区反馈)
9. [源码位置](#9-源码位置)
10. [性能特性](#10-性能特性)
11. [贡献者](#11-贡献者)
12. [相关资源](#12-相关资源)
13. [时间线](#13-时间线)
14. [与 JDK 21 的变化](#14-与-jdk-21-的变化)

---


## 1. JSR 310: Date and Time API

**JSR**: [JSR 310: Date and Time API](https://jcp.org/en/jsr/detail?id=310)
**集成版本**: JDK 8 (2014)
**规范负责人**: Stephen Colebourne

---

## 2. 设计目标

JSR 310 的主要目标是为 Java 提供一个现代化的日期时间 API：

1. **不可变性** - 所有类都是不可变的
2. **线程安全** - 完全线程安全
3. **清晰的 API** - 每个类有明确的用途
4. **基于 Joda-Time** - 继承 Joda-Time 的设计经验

---

## 3. 背景历史

### Joda-Time 时代

**项目**: [Joda-Time](https://www.joda.org/joda-time/)

**作者**: Stephen Colebourne

**发布**: 2002

**为什么需要 JSR 310?**

> The existing `Date` and `Calendar` classes are widely considered to be poorly designed, difficult to use, and flawed in various ways.

**Joda-Time 成为事实标准**:

```java
// JDK 8 之前，开发者使用 Joda-Time
DateTime dateTime = new DateTime();  // Joda-Time
DateTimeFormatter formatter = DateTimeFormat.forPattern("yyyy-MM-dd");
```

### JSR 310 提案

**2007**: JSR 310 提案启动

**设计挑战** (来自 Stephen Colebourne 博客):

> Part of the difficulty I'm finding with designing JSR-310 (Dates and Times) is that I constantly come across gaps in the language of Java.

**2010**: 几乎放弃

**博客**: ["What about JSR-310?"](https://blog.joda.org/2010/12/what-about-jsr-310_153.html)

> The question arises as to whether I should cut my ties with the JCP and terminate JSR-310. The reasons to abandon the JSR are quite compelling.

**原因**:
- 资源不足
- 进展缓慢
- 语言限制

---

## 4. 核心设计决策

### 1. 不可变性

```java
// 所有类都是 final + 不可变
public final class LocalDate
    implements Temporal, TemporalAdjuster, ChronoLocalDate, Serializable {

    private final int year;
    private final int month;
    private final int day;

    // 所有操作返回新对象
    public LocalDate plusDays(long daysToAdd) {
        return LocalDate.ofYearDay(this.year, this.dayOfYear + daysToAdd);
    }
}
```

### 2. 分离关注点

```java
// 清晰的类职责
LocalDate      // 仅日期 (年月日)
LocalTime      // 仅时间 (时分秒)
LocalDateTime  // 日期时间 (无时区)
Instant        // 时间戳 (UTC)
ZonedDateTime  // 带时区的日期时间
```

### 3. 使用枚举

```java
// 月份使用枚举，不是 int
public enum Month {
    JANUARY, FEBRUARY, MARCH, APRIL, MAY, JUNE,
    JULY, AUGUST, SEPTEMBER, OCTOBER, NOVEMBER, DECEMBER;
}

// 星期使用枚举
public enum DayOfWeek {
    MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY;
}
```

---

## 5. 关键 Issue 和 PR

### JDK-8046707: 性能优化

**JBS**: [JDK-8046707](https://bugs.openjdk.org/browse/JDK-8046707)

**问题**: java.time 性能可以更好

**描述**:
> In the java.time library three performance improvements can be noted:
> 1) In the Parsed class crossCheck() method, an exception is used for control flow.

**修复**: JDK 8u20

**问题分析**:
- 使用异常进行控制流是性能反模式
- 影响解析性能

**解决方案**:
```java
// 修复前: 使用异常
try {
    crossCheck(...);
} catch (DateTimeException e) {
    // 处理
}

// 修复后: 避免异常
if (!isValid) {
    return null;
}
```

### JDK-8048443: 相关性能问题

**JBS**: [JDK-8048443](https://bugs.openjdk.org/browse/JDK-8048443)

**描述**: java.time 性能改进

**关联**: 引用 JDK-8046707

### 邮件列表讨论

**主题**: JSR-310 设计讨论

**关键邮件列表**:
- [threeTen-dev](https://lists.sourceforge.net/lists/listinfo/threeten-dev)
- [jdk8-dev](https://mail.openjdk.org/pipermail/jdk8-dev/)

---

## 6. 与 Joda-Time 的差异

### API 差异

| 特性 | Joda-Time | java.time |
|------|-----------|-----------|
| 包名 | `org.joda.time` | `java.time` |
| 月份 | 1-12 (int) | Month 枚举 |
| 可空性 | 支持null | 不支持null |
| 格式化 | DateTimeFormat | DateTimeFormatter |

### 迁移指南

```java
// Joda-Time
DateTime dateTime = new DateTime();
DateTimeFormatter formatter = DateTimeFormat.forPattern("yyyy-MM-dd");
String formatted = formatter.print(dateTime);

// java.time
LocalDateTime dateTime = LocalDateTime.now();
DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
String formatted = formatter.format(dateTime);
```

---

## 7. ThreeTen-Extra 扩展

**项目**: [ThreeTen-Extra](https://www.threeten.org/threeten-extra/)

**作者**: Stephen Colebourne

**发布**: 2014

**目的**: 扩展 java.time API

**额外类**:
- `YearQuarter` - 年季度
- `Quarter` - 季度
- `DayOfWeek` 扩展
- `Amount` - 货币/金额相关

```xml
<dependency>
    <groupId>org.threeten</groupId>
    <artifactId>threeten-extra</artifactId>
    <version>1.7.2</version>
</dependency>
```

---

## 8. 社区反馈

### StackOverflow 讨论

**问题**: [Differences between java.time and Joda-Time](https://stackoverflow.com/questions/24631909)

**关键答案**:

> The java.time API is heavily inspired by Joda-Time, but with many refinements based on experience.

**主要改进**:
1. 更清晰的包结构
2. 更好的空值处理
3. 与 JDK 集成更好

### Reddit 讨论

**主题**: [Thread-safe equivalent for SimpleDateFormat](https://www.reddit.com/r/java/comments/1zcn9t/)

**关键反馈**:

> DateTimeFormatter is immutable and thread-safe!

**对比**:
- `SimpleDateFormat`: ❌ 非线程安全
- `DateTimeFormatter`: ✅ 完全线程安全

---

## 9. 源码位置

| 文件 | 路径 |
|------|------|
| LocalDate | `java.base/java/time/LocalDate.java` |
| LocalTime | `java.base/java/time/LocalTime.java` |
| LocalDateTime | `java.base/java/time/LocalDateTime.java` |
| Instant | `java.base/java/time/Instant.java` |
| ZonedDateTime | `java.base/java/time/ZonedDateTime.java` |
| ZoneId | `java.base/java/time/ZoneId.java` |
| Duration | `java.base/java/time/Duration.java` |
| Period | `java.base/java/time/Period.java` |
| DateTimeFormatter | `java.base/java/time/format/DateTimeFormatter.java` |
| DateTimeFormatterBuilder | `java.base/java/time/format/DateTimeFormatterBuilder.java` |

---

## 10. 性能特性

### 解析性能

```java
@Benchmark
public LocalDate parseISO() {
    return LocalDate.parse("2024-03-20");
}

@Benchmark
public LocalDate parseCustom() {
    return LocalDate.parse("2024/03/20",
        DateTimeFormatter.ofPattern("yyyy/MM/dd"));
}

// 结果: ISO 格式解析最快 (内置优化)
// 自定义格式约慢 2-3 倍
```

### 格式化性能

```java
@Benchmark
public String formatISO() {
    return LocalDate.now().format(DateTimeFormatter.ISO_DATE);
}

@Benchmark
public String formatCustom() {
    return LocalDate.now().format(
        DateTimeFormatter.ofPattern("yyyy-MM-dd")
    );
}

// 结果: 预定义格式化器最快
// 建议缓存自定义格式化器
```

---

## 11. 贡献者

| 贡献者 | 角色 | 说明 |
|--------|------|------|
| **Stephen Colebourne** | 规范负责人 | JSR 310 规范负责人, Joda-Time 作者 |
| **Michael Nascimento** | 实现 | java.time 核心实现 |
| **Roger Riggs** | 实现 | Oracle 工程师 |
| **Stephen Flores** | 测试 | 测试覆盖 |

---

## 12. 相关资源

### 官方文档
- [JSR 310: Date and Time API](https://jcp.org/en/jsr/detail?id=310)
- [java.time JavaDoc](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/time/package-summary.html)
- [Oracle Java SE 8 Date and Time](https://www.oracle.com/java/technologies/jf14-date-time.html)

### 社区资源
- [Joda-Time](https://www.joda.org/joda-time/)
- [ThreeTen-Extra](https://www.threeten.org/threeten-extra/)
- [Stephen Colebourne's Blog](https://blog.joda.org/)

### 文章
- [Baeldung: Java 8 Date/Time Intro](https://www.baeldung.com/java-8-date-time-intro)
- [Differences between java.time and Joda-Time](https://stackoverflow.com/questions/24631909)

---

## 13. 时间线

| 日期 | 事件 |
|------|------|
| 2002 | Joda-Time 1.0 发布 |
| 2007 | JSR 310 提案启动 |
| 2010-12 | Stephen 考虑放弃 JSR 310 |
| 2013 | JSR 310 集成到 JDK 8 |
| 2014-03 | JDK 8 GA 发布 |
| 2014-06 | JDK 8u20 性能修复 |
| 2014-02 | ThreeTen-Extra 项目启动 |
| 2021 | ThreeTen-Extra 1.7 发布 |
| 2023 | JDK 21 标记旧 API 废弃 |

---

## 14. 与 JDK 21 的变化

### Date/Calendar 废弃

```java
// JDK 21
@Deprecated(since = "21")
public class Date {
    /**
     * @deprecated This class is deprecated for removal.
     * Use {@link java.time.Instant} instead.
     */
    @Deprecated(since = "21", forRemoval = true)
    public Date() {
    }
}
```

**迁移指南**:

| 旧类 | 新类 |
|------|------|
| `java.util.Date` | `java.time.Instant` |
| `java.util.Calendar` | `java.time.ZonedDateTime` |
| `java.util.GregorianCalendar` | `java.time.ZonedDateTime` |
| `java.text.SimpleDateFormat` | `java.time.format.DateTimeFormatter` |

---

**Sources:**
- [JSR 310: Date and Time API](https://jcp.org/en/jsr/detail?id=310)
- [JDK-8046707: Performance of java.time could be better](https://bugs.openjdk.org/browse/JDK-8046707)
- [Stephen Colebourne's Blog: What about JSR-310?](https://blog.joda.org/2010/12/what-about-jsr-310_153.html)
- [ThreeTen-Extra Project](https://www.threeten.org/threeten-extra/)
