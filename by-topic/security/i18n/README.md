# 国际化

> Locale、ResourceBundle、Unicode、字符编码演进历程

[← 返回安全](../)

---
## 目录

1. [快速概览](#1-快速概览)
2. [核心贡献者](#2-核心贡献者)
3. [Locale 架构](#3-locale-架构)
4. [ResourceBundle 资源绑定](#4-resourcebundle-资源绑定)
5. [字符编码与 UTF-8 默认化](#5-字符编码与-utf-8-默认化)
6. [Unicode 演进](#6-unicode-演进)
7. [格式化](#7-格式化)
8. [CLDR 数据源](#8-cldr-数据源)
9. [文本处理](#9-文本处理)
10. [Bidi (双向文本)](#10-bidi-双向文本)
11. [最佳实践](#11-最佳实践)
12. [相关链接](#12-相关链接)

---


## 1. 快速概览

```
JDK 1.0 ── JDK 1.1 ── JDK 5 ── JDK 8 ── JDK 9 ── JDK 18 ── JDK 21 ── JDK 24
   │         │        │        │        │        │        │        │
Locale   ResourceBundle Unicode CLDR    CLDR    UTF-8    Unicode  Bidi
          Properties   4.0    数据纳入  默认    默认     15.1    增强
          UTF-8              (JEP252) 提供者  (JEP400) (JEP457)
```

### 核心演进

| 版本 | 特性 | 说明 | JEP |
|------|------|------|-----|
| **JDK 1.0** | Locale | 地区设置 (locale settings) | - |
| **JDK 1.1** | ResourceBundle | 资源绑定 (resource bundle) | - |
| **JDK 1.1** | UTF-8 | 字符编码 (character encoding) | - |
| **JDK 5** | Unicode 4.0 | 完整 Unicode 支持 | - |
| **JDK 6** | Formatter | 格式化增强 (formatter enhancements) | - |
| **JDK 7** | Locale.Builder | 构建器模式创建 Locale | - |
| **JDK 8** | CLDR 默认数据源 | Unicode 公共区域数据仓库 | JEP 252 |
| **JDK 9** | CLDR 默认提供者 | CLDR 成为默认 locale 数据提供者 | JEP 252 |
| **JDK 12** | CompactNumberFormat | 紧凑数字格式化 (compact number formatting) | - |
| **JDK 17** | Locale 增强 | 更多语言支持 | - |
| **JDK 18** | UTF-8 默认编码 | 标准字符集默认为 UTF-8 | JEP 400 |
| **JDK 22** | Unicode 15.1 | 最新标准 | JEP 457 |
| **JDK 24** | Bidi 文本方向 | 双向文本 (bidirectional text) | - |

---

## 2. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 国际化团队 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | [Naoto Sato](/by-contributor/profiles/naoto-sato.md) | 87 | Oracle | 日期, 国际化 |
| 2 | [Justin Lu](/by-contributor/profiles/justin-lu.md) | 81 | Oracle | Locale, ResourceBundle |
| 3 | Andrey Turbanov | 12 | Independent | 格式化 |
| 4 | Pavel Rappo | 8 | Oracle | API 设计 |
| 5 | Rachna Goel | 7 | Oracle | 国际化 |
| 6 | Nishit Jain | 7 | Oracle | Locale |
| 7 | Xueming Shen | 7 | Oracle | 字符编码 |

---

## 3. Locale 架构

Locale 是 JDK 国际化的核心抽象 (core abstraction)，表示特定的地理、政治或文化区域。

### Locale 组成结构

```
Locale 结构:
  Language (语言代码)     zh, en, ja, ko
  Country  (国家/地区)    CN, US, JP, KR
  Variant  (变体)        WIN, POSIX
  Script   (书写系统)     Hans, Hant (JDK 7+)
  Extensions (扩展)       u-ca-japanese (JDK 7+)

BCP 47 语言标签示例:
  zh-Hans-CN     简体中文(中国)     zh-Hant-TW  繁体中文(台湾)
  en-US          美式英语          ja-JP-u-ca-japanese  日语(日本历)
```

### 创建 Locale

```java
import java.util.*;

// 默认 Locale (default locale)
Locale defaultLocale = Locale.getDefault();

// 使用常量 (predefined constants)
Locale US = Locale.US;
Locale CHINA = Locale.CHINA;
Locale FRANCE = Locale.FRANCE;

// 使用 Locale.of (JDK 19+，替代已弃用的构造函数)
Locale japanese = Locale.of("ja");
Locale korean = Locale.of("ko");

// 语言 + 国家 (language + country)
Locale canadianFrench = Locale.of("fr", "CA");

// 语言 + 国家 + 变体 (language + country + variant)
Locale customLocale = Locale.of("zh", "CN", "WIN");

// Builder 模式 (JDK 7+)
Locale locale = new Locale.Builder()
    .setLanguage("en")
    .setRegion("US")
    .setVariant("NY")
    .build();

// 从 BCP 47 语言标签解析 (parse from language tag)
Locale fromTag = Locale.forLanguageTag("zh-Hans-CN");
```

### Locale 分类 (Locale Categories)

```java
// JDK 7+ 引入 Locale.Category，将 Locale 分为两个用途

// 设置显示格式 Locale (display locale — 用于 UI 文本)
Locale.setDefault(Locale.Category.DISPLAY, Locale.JAPAN);

// 设置格式化 Locale (format locale — 用于日期/数字/货币)
Locale.setDefault(Locale.Category.FORMAT, Locale.GERMANY);

// 过滤和查找 (filtering and lookup, JDK 8+)
List<Locale.LanguageRange> ranges =
    Locale.LanguageRange.parse("zh-Hans-CN, en-US;q=0.8");
Locale best = Locale.lookup(ranges,
    Arrays.asList(Locale.getAvailableLocales()));
```

### Locale 数据提供者 (Locale Data Provider)

通过 `-Djava.locale.providers=CLDR,COMPAT,SPI` 控制优先级。JDK 9+ 默认 CLDR，JDK 8 默认 COMPAT (旧称 JRE)。SPI 支持自定义实现。

---

## 4. ResourceBundle 资源绑定

ResourceBundle 是 JDK 实现多语言文本 (multilingual text) 的标准机制。

### 属性文件资源 (Properties File Resources)

```properties
# messages_zh_CN.properties
greeting=你好
welcome=欢迎
items.count=共 {0} 项

# messages_en_US.properties
greeting=Hello
welcome=Welcome
items.count={0} items total

# messages_ja_JP.properties
greeting=こんにちは
welcome=ようこそ
items.count=合計 {0} 件
```

### 使用 ResourceBundle

```java
import java.util.*;
import java.text.*;

// 加载资源包 (load resource bundle)
ResourceBundle bundle = ResourceBundle.getBundle(
    "messages",
    Locale.CHINA);

// 获取消息 (get message)
String greeting = bundle.getString("greeting");
System.out.println(greeting);  // 你好

// 带参数的消息格式化 (parameterized message formatting)
String pattern = bundle.getString("items.count");
String result = MessageFormat.format(pattern, 42);
// 中文: "共 42 项"  英文: "42 items total"

// 遍历所有键 (iterate all keys)
Enumeration<String> keys = bundle.getKeys();
while (keys.hasMoreElements()) {
    String key = keys.nextElement();
    String value = bundle.getString(key);
    System.out.println(key + " = " + value);
}
```

### 资源查找链 (Resource Lookup Chain)

```
请求 Locale: zh_CN_WIN → 查找顺序 (lookup order):
  1. messages_zh_CN_WIN.properties
  2. messages_zh_CN.properties
  3. messages_zh.properties
  4. messages.properties  (默认 fallback)
  全部未找到 → MissingResourceException
```

### 缺失资源处理 (Missing Resource Handling)

```java
// 加载时指定控制 (load with control)
ResourceBundle bundle = ResourceBundle.getBundle(
    "messages",
    Locale.CHINA,
    ResourceBundle.Control.getControl(
        ResourceBundle.Control.FORMAT_PROPERTIES));

// 无资源时使用默认 (fallback to default)
try {
    ResourceBundle bundle = ResourceBundle.getBundle("messages");
} catch (MissingResourceException e) {
    // 使用默认值
}

// 自定义 Control 实现 UTF-8 加载 (JDK 8 及更早)
// JDK 9+ 的 properties 文件默认使用 UTF-8 编码
```

---

## 5. 字符编码与 UTF-8 默认化

### JEP 400: UTF-8 by Default (JDK 18)

JEP 400 是 JDK 国际化的里程碑 (milestone)，将默认字符集 (default charset) 从平台相关 (platform-dependent) 改为 UTF-8。

```
JDK 17 及之前:
  Linux/macOS → 通常是 UTF-8
  Windows     → 通常是 GBK / MS932 / Windows-1252
  → 跨平台行为不一致 (inconsistent cross-platform behavior)

JDK 18+ (JEP 400):
  所有平台    → UTF-8
  → 跨平台行为一致 (consistent cross-platform behavior)
```

**受影响的 API (affected APIs)**:

| API | JDK 17 行为 | JDK 18+ 行为 |
|-----|-------------|--------------|
| `FileReader` / `FileWriter` | 平台编码 | UTF-8 |
| `InputStreamReader` / `OutputStreamWriter` (无参) | 平台编码 | UTF-8 |
| `PrintStream` (无参) | 平台编码 | UTF-8 |
| `Formatter` (无参) | 平台编码 | UTF-8 |
| `Scanner` (无参) | 平台编码 | UTF-8 |
| `URLEncoder` / `URLDecoder` (无参) | 平台编码 | UTF-8 |

```java
// JDK 18+ 默认 UTF-8，以下代码在所有平台上行为一致
Charset defaultCharset = Charset.defaultCharset();
// 始终返回 UTF-8

// 如需恢复旧行为 (restore old behavior)
// 启动参数: -Dfile.encoding=COMPAT
// 不推荐，仅用于迁移过渡
```

### 编码转换 (Encoding Conversion)

```java
import java.nio.charset.*;

// 字符串编码 (string encoding)
String str = "你好世界";

// UTF-8 编码 (最推荐)
byte[] utf8 = str.getBytes(StandardCharsets.UTF_8);

// GBK 编码 (中文 Windows 遗留系统)
byte[] gbk = str.getBytes(Charset.forName("GBK"));

// 解码 (decoding)
String decoded = new String(utf8, StandardCharsets.UTF_8);
```

### 读写文件编码 (File I/O Encoding)

```java
import java.nio.file.*;
import java.nio.charset.*;

// JDK 18+ 默认 UTF-8 (write file)
Files.writeString(Paths.get("output.txt"), "你好世界");

// 显式指定 UTF-8 (推荐，向后兼容)
Files.writeString(Paths.get("output.txt"),
    "你好世界", StandardCharsets.UTF_8);

// 读取文件 (read file)
String content = Files.readString(Paths.get("input.txt"),
    StandardCharsets.UTF_8);

// 处理旧编码文件 (handle legacy encoded files)
String gbkContent = Files.readString(Paths.get("legacy.txt"),
    Charset.forName("GBK"));
```

---

## 6. Unicode 演进

### Unicode 版本支持历史 (Unicode Version History)

| JDK | Unicode 版本 | 主要新增内容 | JEP |
|-----|--------------|-------------|-----|
| JDK 1.4 | 3.0 | 基础支持 (basic support) | - |
| JDK 5 | 4.0 | 补充平面 (supplementary planes) | - |
| JDK 7 | 6.0 | 脚本增强 (script enhancements) | - |
| JDK 8 | 6.2 | 更多字符 (more characters) | - |
| JDK 11 | 10.0 | 表情符号 2.0 (emoji 2.0) | - |
| JDK 12 | 11.0 | 格鲁吉亚文等 | - |
| JDK 13 | 12.1 | 日本令和 (Reiwa era) | - |
| JDK 15 | 13.0 | 更多表情符号 | - |
| JDK 17 | 13.0 | 同 JDK 15 | - |
| JDK 20 | 15.0 | 最新标准 | - |
| JDK 21 | 15.0 | 同 JDK 20 | - |
| JDK 22 | 15.1 | 最新标准 | JEP 457 |

### Unicode 字符处理 (Character Handling)

```java
// 基本多文种平面 BMP (Basic Multilingual Plane)
char c1 = 'A';  // U+0041
char c2 = '中'; // U+4E2D

// 补充平面 (Supplementary Plane，需要代理对 surrogate pair)
String emoji = "😀";  // U+1F600
int length = emoji.length();        // 2 (char 计数)
int cpCount = emoji.codePointCount(0, emoji.length()); // 1 (代码点计数)

// 代码点 (code point)
int codePoint = emoji.codePointAt(0);  // 128512

// 遍历代码点 (iterate code points) — 推荐方式
String str = "Hello 👋 世界";
str.codePoints().forEach(cp -> {
    System.out.printf("U+%04X %s%n", cp,
        new String(Character.toChars(cp)));
});

// Character 属性查询 (character property queries)
Character.isLetter('中');          // true
Character.isIdeographic('中');     // true (JDK 7+，表意文字)
Character.UnicodeBlock.of('中');   // CJK_UNIFIED_IDEOGRAPHS
Character.UnicodeScript.of('中'); // HAN
```

### 正则表达式 Unicode (Regex Unicode Support)

```java
// Unicode 类别 (Unicode categories)
String text = "Hello 世界 123";
text.matches(".*\\p{L}.*");  // 包含字母 (contains letter)

// 匹配中文 (match Chinese)
text.matches(".*\\p{script=Han}.*");

// Unicode 块 (Unicode blocks)
text.matches(".*\\p{InCJK_Unified_Ideographs}.*");

// 匹配表情符号 (match emoji)
String emoji = "😀";
emoji.matches(".*\\p{So}.*");  // Symbol Other

// JDK 20+ 扩展图形簇匹配 (extended grapheme cluster)
// \X 匹配完整的 Unicode 字素簇
```

---

## 7. 格式化

### 数字格式化 (Number Formatting)

```java
import java.text.*;
import java.util.*;

// 数字格式 (number format)
NumberFormat nf = NumberFormat.getInstance(Locale.FRANCE);
String number = nf.format(1234.56);  // 1 234,56

// 货币格式 (currency format)
NumberFormat cf = NumberFormat.getCurrencyInstance(Locale.JAPAN);
String currency = cf.format(1234.56);  // ￥1,235

// 百分比 (percentage)
NumberFormat pf = NumberFormat.getPercentInstance(Locale.ITALY);
String percent = pf.format(0.75);  // 75%
```

### CompactNumberFormat 紧凑数字格式 (JDK 12+)

```java
import java.text.*;
import java.util.*;

// 紧凑数字格式 — 将大数字缩写显示
// SHORT 风格 (short style)
NumberFormat compact = NumberFormat.getCompactNumberInstance(
    Locale.US, NumberFormat.Style.SHORT);
compact.format(1000);      // "1K"
compact.format(1000000);   // "1M"
compact.format(1000000000); // "1B"

// 中文紧凑格式
NumberFormat cnCompact = NumberFormat.getCompactNumberInstance(
    Locale.CHINA, NumberFormat.Style.SHORT);
cnCompact.format(1000);      // "1千"
cnCompact.format(10000);     // "1万"
cnCompact.format(100000000); // "1亿"

// LONG 风格 (long style)
NumberFormat longCompact = NumberFormat.getCompactNumberInstance(
    Locale.US, NumberFormat.Style.LONG);
longCompact.format(1000);      // "1 thousand"
longCompact.format(1000000);   // "1 million"

// 设置精度 (set precision)
compact.setMaximumFractionDigits(2);
compact.format(1234);    // "1.23K"
compact.format(1234567); // "1.23M"
```

### 日期时间格式化 (Date/Time Formatting, JDK 8+)

```java
import java.time.*;
import java.time.format.*;

// 本地化日期 (localized date)
LocalDate date = LocalDate.now();
DateTimeFormatter formatter =
    DateTimeFormatter.ofLocalizedDate(FormatStyle.FULL)
        .withLocale(Locale.CHINA);

String formatted = date.format(formatter);
// 2026年3月20日 星期五

// 自定义格式 (custom format)
DateTimeFormatter customFormatter =
    DateTimeFormatter.ofPattern("yyyy年MM月dd日 EEEE")
        .withLocale(Locale.CHINESE);
```

### 旧版日期格式化 (Legacy Date Formatting)

```java
import java.text.*;

// 日期格式 (date format)
DateFormat df = DateFormat.getDateInstance(
    DateFormat.FULL,
    Locale.FRANCE);
String dateStr = df.format(new Date());

// 时间格式 (time format)
DateFormat tf = DateFormat.getTimeInstance(
    DateFormat.LONG,
    Locale.JAPAN);

// 日期时间格式 (date-time format)
DateFormat dtf = DateFormat.getDateTimeInstance(
    DateFormat.LONG,
    DateFormat.LONG,
    Locale.GERMANY);
```

---

## 8. CLDR 数据源

CLDR (Unicode Common Locale Data Repository) 是 Unicode 联盟维护的区域数据仓库，JDK 9+ 默认使用 CLDR 作为 locale 数据源。

### CLDR 提供的数据类型 (Data Types Provided by CLDR)

JDK 8 (JEP 252) 引入 CLDR 数据，JDK 9 起 CLDR 成为默认 locale 数据提供者。JDK 21 使用 CLDR 43，覆盖 700+ 语言和地区。

| 数据类型 | 说明 | 示例 |
|---------|------|------|
| **日期格式** (date patterns) | 本地化日期模式 | "yyyy年M月d日" |
| **数字格式** (number patterns) | 分隔符、分组规则 | "#,##0.###" |
| **货币** (currencies) | 货币符号、名称 | ¥, 人民币 |
| **时区名称** (time zone names) | 本地化时区 | "中国标准时间" |
| **日历数据** (calendar data) | 月份名、星期名 | "星期一" |
| **排序规则** (collation rules) | 语言排序顺序 | 中文拼音排序 |
| **紧凑数字** (compact decimals) | 缩写模式 | "1万", "1亿" |

### 切换 Locale 数据提供者

```java
// -Djava.locale.providers=CLDR,COMPAT,SPI
// CLDR:   Unicode CLDR 数据 (JDK 9+ 默认)
// COMPAT: 旧 JRE 数据 (兼容旧行为)
// SPI:    自定义 LocaleServiceProvider 实现
// HOST:   使用操作系统的 locale 设置

// CLDR 与 COMPAT 差异: 日期分隔符等可能不同
// CLDR: 2026/3/20    COMPAT: 2026-3-20
```

### ICU4J 集成

ICU (International Components for Unicode) 是 CLDR 的参考实现。JDK 内部使用部分 ICU 代码，但 API 不同。如需完整 ICU 功能，可直接依赖 `com.ibm.icu:icu4j`。

---

## 9. 文本处理

JDK 提供了多个文本处理 API，用于断词 (word breaking)、规范化 (normalization)、排序 (collation) 等操作。

### BreakIterator 文本边界迭代器

```java
import java.text.*;
import java.util.*;

// BreakIterator 用于检测文本中的逻辑边界 (logical boundaries)
// 四种类型: 字符 / 词 / 句 / 行

// 词边界 (word boundary)
BreakIterator wordIter = BreakIterator.getWordInstance(Locale.CHINA);
wordIter.setText("Hello世界Java编程");
int start = wordIter.first();
for (int end = wordIter.next();
     end != BreakIterator.DONE;
     start = end, end = wordIter.next()) {
    String word = "Hello世界Java编程".substring(start, end);
    if (!word.isBlank()) {
        System.out.println("词: " + word);
    }
}
// 输出: "Hello", "世界", "Java", "编程"

// 其他类型 (other types):
// getSentenceInstance() — 句边界 (sentence boundary)
// getCharacterInstance() — 字符边界 (character boundary，对 emoji 有意义)
// getLineInstance()      — 行边界 (line break opportunity，用于文本排版)
```

### Normalizer 文本规范化

```java
import java.text.*;

// Unicode 规范化 (Unicode normalization)
// 同一个字符可能有多种表示方式

// 示例: "é" 可以是:
// 1. U+00E9 (预组合形式 precomposed form)
// 2. U+0065 + U+0301 (分解形式 decomposed form: e + 组合重音符)

String precomposed = "\u00E9";       // é (1 个代码点)
String decomposed  = "e\u0301";     // é (2 个代码点)

// NFC: 规范分解后再规范组合 (Canonical Decomposition + Canonical Composition)
String nfc = Normalizer.normalize(decomposed, Normalizer.Form.NFC);
// 结果: "\u00E9"

// NFD: 规范分解 (Canonical Decomposition)
String nfd = Normalizer.normalize(precomposed, Normalizer.Form.NFD);
// 结果: "e\u0301"

// NFKC / NFKD: 兼容性分解 (Compatibility Decomposition)
// 将 "ﬁ" (U+FB01) 分解为 "fi"
String nfkc = Normalizer.normalize("\uFB01", Normalizer.Form.NFKC);
// 结果: "fi"

// 检查是否已规范化 (check if normalized)
boolean isNFC = Normalizer.isNormalized(nfc, Normalizer.Form.NFC);

// 最佳实践: 在比较或存储前先规范化
// 推荐使用 NFC (大多数系统的默认形式)
```

### Collator 排序器

```java
import java.text.*;
import java.util.*;

// Collator 提供语言敏感的字符串比较和排序
// (locale-sensitive string comparison and sorting)

// 创建 Collator
Collator cnCollator = Collator.getInstance(Locale.CHINA);
Collator deCollator = Collator.getInstance(Locale.GERMANY);

// 比较字符串 (compare strings)
int result = cnCollator.compare("张", "李");
// 按拼音排序: 李 < 张 (L < Z)

// 排序强度 (collation strength)
cnCollator.setStrength(Collator.PRIMARY);
// PRIMARY:   忽略大小写和重音 (base characters only)
// SECONDARY: 区分重音，忽略大小写 (+ accents)
// TERTIARY:  区分大小写 (+ case) — 默认
// IDENTICAL: 完全区分 (bit-level)

// 德语示例: ä 的排序
deCollator.setStrength(Collator.PRIMARY);
deCollator.compare("ä", "a");  // 0 (相等)
deCollator.setStrength(Collator.SECONDARY);
deCollator.compare("ä", "a");  // != 0 (不等)

// 使用 CollationKey 优化批量排序
// (use CollationKey for efficient bulk sorting)
List<String> names = List.of("张三", "李四", "王五", "赵六");
List<String> sorted = names.stream()
    .sorted(cnCollator)
    .toList();
// 按拼音排序: 李四, 王五, 赵六, 张三

// CollationKey: 批量排序优化 (bulk sort optimization)
CollationKey key1 = cnCollator.getCollationKey("张三");
CollationKey key2 = cnCollator.getCollationKey("李四");
key1.compareTo(key2); // 基于字节数组比较，比反复 compare 快
```

---

## 10. Bidi (双向文本)

### 文本方向 (Text Direction)

```java
import java.text.*;

// 检测文本方向 (detect text direction)
String arabic = "مرحبا";
String hebrew = "שלום";
String mixed = "Hello مرحبا שלום";

Bidi bidi = new Bidi(mixed, Bidi.DIRECTION_DEFAULT_LEFT_TO_RIGHT);
boolean isRTL = bidi.isMixed() || bidi.getDirection() == Bidi.DIRECTION_RIGHT_TO_LEFT;

// 获取方向 (get direction)
int direction = bidi.getBaseLevel();  // 0 = LTR, 1 = RTL
```

### Bidi 格式化 (Bidi Formatting)

```java
import java.awt.font.*;
import java.awt.*;

// 文本布局 (text layout)
String text = "Hello \u05D0\u05D1\u05D2";  // 混合 LTR/RTL
Font font = new Font("Arial", Font.PLAIN, 12);
FontRenderContext frc = new FontRenderContext(null, true, true);

TextLayout layout = new TextLayout(text, font, frc);
layout.draw(graphics, x, y);
```

---

## 11. 最佳实践

### 1. 使用 UTF-8

```java
// 推荐: 显式指定 UTF-8 (explicit UTF-8)
Files.writeString(path, content, StandardCharsets.UTF_8);
new String(bytes, StandardCharsets.UTF_8);

// 避免: 依赖平台默认编码 (avoid platform-dependent encoding)
// JDK 18+ 默认 UTF-8，但显式指定更安全
Files.writeString(path, content);  // JDK 18+ 安全
new String(bytes);                 // JDK 18+ 安全
```

### 2. 资源文件命名

```
messages.properties              # 默认 (default)
messages_zh.properties           # 中文 (通用)
messages_zh_CN.properties        # 简体中文
messages_zh_TW.properties        # 繁体中文
messages_en.properties           # 英文 (通用)
messages_en_US.properties        # 美式英语
```

### 3. Locale 敏感操作

```java
// 总是显式指定 Locale (always specify locale explicitly)
NumberFormat.getInstance(Locale.US);
DateFormat.getDateInstance(DateFormat.SHORT, Locale.JAPAN);
String.toUpperCase(Locale.ENGLISH);  // 而非 toUpperCase()

// 土耳其 I 问题 (Turkish I problem)
// "I".toLowerCase(Locale.ENGLISH)  → "i"
// "I".toLowerCase(Locale.forLanguageTag("tr"))  → "ı" (无点 i)
```

### 4. 文本处理建议

```java
// 比较前先规范化 (normalize before comparison)
String normalized = Normalizer.normalize(input, Normalizer.Form.NFC);

// 使用 Collator 排序而非 String.compareTo (use Collator for locale-aware sorting)
Collator collator = Collator.getInstance(locale);
list.sort(collator);

// 用 codePoints() 遍历而非 charAt (use codePoints() instead of charAt)
str.codePoints().forEach(cp -> { /* ... */ });
```

---

## 12. 相关链接

### 本地文档

- [安全](../security/) - 加密
- [字符串](../../language/string/) - 字符处理

### 外部参考

**技术文档:**
- [ICU User Guide](https://unicode-org.github.io/icu/userguide/)
- [CLDR (Unicode Common Locale Data Repository)](https://cldr.unicode.org/)
- [Unicode Standard](https://www.unicode.org/standard/standard.html)
- [JEP 400: UTF-8 by Default](https://openjdk.org/jeps/400)
- [JEP 252: Use CLDR Locale Data by Default](https://openjdk.org/jeps/252)
