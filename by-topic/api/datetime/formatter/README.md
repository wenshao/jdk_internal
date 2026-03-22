# DateTimeFormatter 源码分析

> java.time.format.DateTimeFormatter 的完整实现分析

---
## 目录

1. [类声明](#1-类声明)
2. [预定义格式化器](#2-预定义格式化器)
3. [模式字母表](#3-模式字母表)
4. [创建格式化器](#4-创建格式化器)
5. [格式化方法](#5-格式化方法)
6. [解析方法](#6-解析方法)
7. [ResolverStyle 解析风格](#7-resolverstyle-解析风格)
8. [性能特性](#8-性能特性)
9. [线程安全保证](#9-线程安全保证)
10. [与 SimpleDateFormat 对比](#10-与-simpledateformat-对比)
11. [扩展功能](#11-扩展功能)
12. [相关文档](#12-相关文档)

---


## 1. 类声明

```java
public final class DateTimeFormatter {
    /**
     * The printer and/or parser to use, not null.
     */
    private final CompositePrinterParser printerParser;

    /**
     * The locale to use for formatting, not null.
     */
    private final Locale locale;

    /**
     * The symbols to use for formatting, not null.
     */
    private final DecimalStyle decimalStyle;

    /**
     * The resolver style to use, not null.
     */
    private final ResolverStyle resolverStyle;

    /**
     * The fields to use in resolving, null for all fields.
     */
    private final Set<TemporalField> resolverFields;

    /**
     * The chronology to use for formatting, null for no override.
     */
    private final Chronology chrono;

    /**
     * The zone to use for formatting, null for no override.
     */
    private final ZoneId zone;
}
```

**关键设计**:
- `final` 类，所有字段 `final` - 完全不可变
- 线程安全 - 可在多线程环境共享
- 解析器和格式化器合二为一 - `CompositePrinterParser`

---

## 2. 预定义格式化器

### ISO 格式化器

```java
// ISO_LOCAL_DATE: 2011-12-03
public static final DateTimeFormatter ISO_LOCAL_DATE;
static {
    ISO_LOCAL_DATE = new DateTimeFormatterBuilder()
        .appendValue(YEAR, 4, 10, SignStyle.EXCEEDS_PAD)
        .appendLiteral('-')
        .appendValue(MONTH_OF_YEAR, 2)
        .appendLiteral('-')
        .appendValue(DAY_OF_MONTH, 2)
        .toFormatter(ResolverStyle.STRICT, IsoChronology.INSTANCE);
}

// ISO_LOCAL_TIME: 10:15:30
public static final DateTimeFormatter ISO_LOCAL_TIME;
static {
    ISO_LOCAL_TIME = new DateTimeFormatterBuilder()
        .appendValue(HOUR_OF_DAY, 2)
        .appendLiteral(':')
        .appendValue(MINUTE_OF_HOUR, 2)
        .optionalStart()
        .appendLiteral(':')
        .appendValue(SECOND_OF_MINUTE, 2)
        .optionalStart()
        .appendFraction(NANO_OF_SECOND, 0, 9, true)
        .toFormatter(ResolverStyle.STRICT, null);
}

// ISO_LOCAL_DATE_TIME: 2011-12-03T10:15:30
public static final DateTimeFormatter ISO_LOCAL_DATE_TIME;
static {
    ISO_LOCAL_DATE_TIME = new DateTimeFormatterBuilder()
        .append(ISO_LOCAL_DATE)
        .appendLiteral('T')
        .append(ISO_LOCAL_TIME)
        .toFormatter(ResolverStyle.STRICT, IsoChronology.INSTANCE);
}
```

**设计特点**:
- 使用 `DateTimeFormatterBuilder` 构建
- `optionalStart()` 支持可选字段
- 预定义，线程安全，可重用

### RFC_1123 格式化器

```java
// RFC_1123_DATE_TIME: Tue, 3 Jun 2008 11:05:30 GMT
public static final DateTimeFormatter RFC_1123_DATE_TIME;
static {
    RFC_1123_DATE_TIME = new DateTimeFormatterBuilder()
        .parseCaseInsensitive()
        .appendText(DAY_OF_WEEK, TextStyle.SHORT)
        .appendLiteral(", ")
        .appendValue(DAY_OF_MONTH, 1, 2, SignStyle.NOT_NEGATIVE)
        .appendLiteral(' ')
        .appendText(MONTH_OF_YEAR, TextStyle.SHORT)
        .appendLiteral(' ')
        .appendValue(YEAR, 4)  // 2 digit year not allowed
        .appendLiteral(' ')
        .appendValue(HOUR_OF_DAY, 2)
        .appendLiteral(':')
        .appendValue(MINUTE_OF_HOUR, 2)
        .appendLiteral(':')
        .appendValue(SECOND_OF_MINUTE, 2)
        .appendLiteral(' ')
        .appendOffsetId()
        .toFormatter(ResolverStyle.STRICT, null);
}
```

---

## 3. 模式字母表

### 日期模式

| 字母 | 含义 | 示例 |
|------|------|------|
| `G` | 纪元 | AD; Anno Domini |
| `u` | 年 | 2004 |
| `y` | 年份 | 2004 |
| `D` | 年中第几天 | 189 |
| `M` | 月 | 7; 07; Jul; July |
| `d` | 月中第几天 | 10 |
| `Q/q` | 季度 | 3; Q3 |

### 时间模式

| 字母 | 含义 | 示例 |
|------|------|------|
| `a` | 上午/下午 | PM |
| `B` | 一天中的时段 | in the morning |
| `h` | 上午小时 (1-12) | 12 |
| `K` | 上午小时 (0-11) | 0 |
| `k` | 时钟小时 (1-24) | 24 |
| `H` | 小时 (0-23) | 0 |
| `m` | 分钟 | 30 |
| `s` | 秒 | 55 |
| `S` | 秒的小数 | .978 |

### 时区模式

| 字母 | 含义 | 示例 |
|------|------|------|
| `V` | 时区 ID | America/Los_Angeles |
| `z` | 时区名称 | Pacific Standard Time |
| `O` | 本地化偏移 | GMT+8 |
| `X` | 偏移 (零时为 Z) | Z; -08; -08:30 |
| `x` | 偏移 | +0000; -08:30 |
| `Z` | 偏移 | +0000; -0800 |

---

## 4. 创建格式化器

### ofPattern() - 从模式字符串

```java
public static DateTimeFormatter ofPattern(String pattern) {
    return new DateTimeFormatterBuilder().appendPattern(pattern).toFormatter();
}

public static DateTimeFormatter ofPattern(String pattern, Locale locale) {
    return new DateTimeFormatterBuilder().appendPattern(pattern).toFormatter(locale);
}
```

**使用示例**:
```java
// 简单模式
DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
String formatted = LocalDateTime.now().format(formatter);  // 2026-03-20 14:30:45

// 带本地化
DateTimeFormatter frenchFormatter = DateTimeFormatter.ofPattern("d MMMM yyyy", Locale.FRENCH);
String frenchDate = LocalDate.now().format(frenchFormatter);  // 20 mars 2026
```

### ofLocalizedDate() / ofLocalizedTime()

```java
public static DateTimeFormatter ofLocalizedDate(FormatStyle dateStyle) {
    Objects.requireNonNull(dateStyle, "dateStyle");
    return new DateTimeFormatterBuilder()
        .appendLocalized(dateStyle, null)
        .toFormatter(ResolverStyle.SMART, IsoChronology.INSTANCE);
}

public static DateTimeFormatter ofLocalizedTime(FormatStyle timeStyle) {
    Objects.requireNonNull(timeStyle, "timeStyle");
    return new DateTimeFormatterBuilder()
        .appendLocalized(null, timeStyle)
        .toFormatter(ResolverStyle.SMART, IsoChronology.INSTANCE);
}
```

**FormatStyle 选项**:
- `FULL` - 完整格式
- `LONG` - 长格式
- `MEDIUM` - 中等格式
- `SHORT` - 短格式

---

## 5. 格式化方法

```java
public String format(TemporalAccessor temporal) {
    StringBuilder buf = new StringBuilder(32);
    formatTo(temporal, buf);
    return buf.toString();
}

public void formatTo(TemporalAccessor temporal, Appendable appendable) {
    Objects.requireNonNull(temporal, "temporal");
    Objects.requireNonNull(appendable, "appendable");
    try {
        printerParser.format(printerParser.parseQueries(temporal), appendable, symbols);
    } catch (IOException e) {
        throw new DateTimeException(e);
    }
}
```

**流程**:
1. 解析 TemporalAccessor 获取字段值
2. 应用格式化规则
3. 写入输出目标

---

## 6. 解析方法

```java
public TemporalAccessor parse(CharSequence text) {
    Objects.requireNonNull(text, "text");
    try {
        return parseResolved0(text, null);
    } catch (DateTimeParseException ex) {
        throw ex;
    }
}

public <T> T parse(CharSequence text, TemporalQuery<T> query) {
    Objects.requireNonNull(text, "text");
    Objects.requireNonNull(query, "query");
    try {
        return parseResolved0(text, query);
    } catch (DateTimeParseException ex) {
        throw ex;
    }
}

private TemporalAccessor parseResolved0(CharSequence text, TemporalQuery<?> query) {
    ParsePosition pos = new ParsePosition(0);
    TemporalAccessor parsed = parseUnresolved0(text, pos);
    if (pos.getIndex() == 0) {
        throw new DateTimeParseException("Text '" + text + "' could not be parsed: " +
            (pos.getErrorIndex() >= 0 ? "parse error at index " + pos.getErrorIndex() : "not parsed"),
            text, pos.getErrorIndex());
    }
    if (pos.getIndex() < text.length()) {
        throw new DateTimeParseException("Text '" + text + "' could not be parsed: unparsed characters found at index " + pos.getIndex(),
            text, pos.getIndex());
    }
    return resolve(parsed, query);
}
```

**两阶段解析**:
1. **解析阶段**: 文本 → 字段值映射
2. **解析阶段**: 字段值 → 完整日期时间对象

---

## 7. ResolverStyle 解析风格

### STRICT (严格)

```java
public static enum ResolverStyle {
    STRICT,
    SMART,
    LENIENT
}
```

**STRICT**:
- 严格要求所有字段有效
- 不进行任何推断或调整
- 例如: 2月30日会抛出异常

**SMART** (默认):
- 智能处理
- 例如: 2月30日 → 2月28/29日

**LENIENT** (宽松):
- 最大程度接受输入
- 自动调整无效值

---

## 8. 性能特性

### 缓存建议

```java
// ❌ 不推荐 - 每次创建新格式化器
for (int i = 0; i < 1000; i++) {
    DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
    formatter.format(date);
}

// ✅ 推荐 - 复用格式化器
private static final DateTimeFormatter DATE_FORMATTER =
    DateTimeFormatter.ofPattern("yyyy-MM-dd");

for (int i = 0; i < 1000; i++) {
    DATE_FORMATTER.format(date);
}
```

### 性能对比

| 操作 | SimpleDateFormat | DateTimeFormatter |
|------|-----------------|-------------------|
| 线程安全 | ❌ 非线程安全 | ✅ 线程安全 |
| 创建开销 | 中等 | 较高 (一次性) |
| 格式化性能 | 中等 | 快 (预编译) |
| 解析性能 | 中等 | 快 |

---

## 9. 线程安全保证

```java
// 所有字段都是 final
private final CompositePrinterParser printerParser;
private final Locale locale;
private final DecimalStyle decimalStyle;
private final ResolverStyle resolverStyle;
private final Set<TemporalField> resolverFields;
private final Chronology chrono;
private final ZoneId zone;

// 所有方法返回新对象
public DateTimeFormatter withLocale(Locale locale) {
    Objects.requireNonNull(locale, "locale");
    if (this.locale.equals(locale)) {
        return this;
    }
    return new DateTimeFormatter(printerParser, locale, decimalStyle,
                                resolverStyle, resolverFields, chrono, zone);
}
```

**线程安全策略**:
1. 不可变对象
2. 所有修改操作返回新对象
3. 无同步开销

---

## 10. 与 SimpleDateFormat 对比

### SimpleDateFormat 问题

```java
// ❌ 非线程安全
SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
// 多线程环境下会抛出异常或产生错误结果

// 需要同步
synchronized (sdf) {
    sdf.format(date);
}
```

### DateTimeFormatter 解决

```java
// ✅ 完全线程安全
private static final DateTimeFormatter FORMATTER =
    DateTimeFormatter.ofPattern("yyyy-MM-dd");

// 多线程安全，无需同步
FORMATTER.format(date);
```

---

## 11. 扩展功能

### 自定义模式

```java
// 复杂模式
DateTimeFormatter complexFormatter =
    DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS");

// 带时区
DateTimeFormatter withZone =
    DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss z");
```

### 本地化

```java
// 法语格式
DateTimeFormatter french =
    DateTimeFormatter.ofPattern("d MMMM yyyy")
        .withLocale(Locale.FRENCH);

// 德语格式
DateTimeFormatter german =
    DateTimeFormatter.ofPattern("d. MMMM yyyy")
        .withLocale(Locale.GERMAN);
```

---

## 12. 相关文档

- [LocalDate 实现](../localdate/README.md)
- [LocalTime 实现](../localtime/README.md)
- [JDK-8046707 性能问题](../issues/jdk-8046707.md)
- [主索引](../README.md)

---

> **更新时间**: 2026-03-20
> **源码版本**: OpenJDK 23
> **文件路径**: `src/java.base/share/classes/java/time/format/DateTimeFormatter.java`
