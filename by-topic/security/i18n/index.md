# 国际化

> Locale、ResourceBundle、Unicode、字符编码演进历程

[← 返回安全](../)

---
## 目录

1. [快速概览](#1-快速概览)
2. [核心贡献者](#2-核心贡献者)
3. [Locale](#3-locale)
4. [ResourceBundle](#4-resourcebundle)
5. [字符编码](#5-字符编码)
6. [格式化](#6-格式化)
7. [Unicode 支持](#7-unicode-支持)
8. [ICU4J 集成](#8-icu4j-集成)
9. [Bidi (双向文本)](#9-bidi-双向文本)
10. [最佳实践](#10-最佳实践)
11. [相关链接](#11-相关链接)

---


## 1. 快速概览

```
JDK 1.0 ── JDK 1.1 ── JDK 5 ── JDK 6 ── JDK 8 ── JDK 17 ── JDK 21 ── JDK 24
   │         │        │        │        │        │        │        │
Locale   ResourceBundle Unicode Formatter Locale ICU4J   Unicode  Bidi
          Properties   4.0    增强    增强    兼容层  15.1    增强
          UTF-8                (JEP   增强   (CLDR)  (JEP   文本
                               252)                           方向
```

### 核心演进

| 版本 | 特性 | 说明 | JEP |
|------|------|------|-----|
| **JDK 1.0** | Locale | 地区设置 | - |
| **JDK 1.1** | ResourceBundle | 资源绑定 | - |
| **JDK 1.1** | UTF-8 | 字符编码 | - |
| **JDK 5** | Unicode 4.0 | 完整 Unicode | - |
| **JDK 6** | Formatter | 格式化增强 | - |
| **JDK 8** | ICU4J | 国际化组件库 | JEP 252 |
| **JDK 17** | Locale 增强 | 更多语言 | - |
| **JDK 22** | Unicode 15.1 | 最新标准 | JEP 457 |
| **JDK 24** | Bidi 文本方向 | 双向文本 | - |

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

## 3. Locale

### 创建 Locale

```java
import java.util.*;

// 默认 Locale
Locale defaultLocale = Locale.getDefault();

// 使用常量
Locale US = Locale.US;
Locale CHINA = Locale.CHINA;
Locale FRANCE = Locale.FRANCE;

// 使用语言代码 (JDK 19+, Locale.of 替代已弃用的构造函数)
Locale japanese = Locale.of("ja");
Locale korean = Locale.of("ko");

// 语言 + 国家
Locale canadianFrench = Locale.of("fr", "CA");

// 语言 + 国家 + 变体
Locale customLocale = Locale.of("zh", "CN", "WIN");

// Builder (JDK 7+)
Locale locale = new Locale.Builder()
    .setLanguage("en")
    .setRegion("US")
    .setVariant("NY")
    .build();
```

### 设置默认 Locale

```java
// 设置默认 Locale
Locale.setDefault(Locale.US);

// 设置显示格式 Locale
Locale.setDefault(Locale.Category.DISPLAY, Locale.JAPAN);

// 设置格式 Locale
Locale.setDefault(Locale.Category.FORMAT, Locale.GERMANY);
```

---

## 4. ResourceBundle

### 属性文件资源

```properties
# messages_zh_CN.properties
greeting=你好
welcome=欢迎

# messages_en_US.properties
greeting=Hello
welcome=Welcome

# messages_ja_JP.properties
greeting=こんにちは
welcome=ようこそ
```

### 使用 ResourceBundle

```java
import java.util.*;

// 加载资源包
ResourceBundle bundle = ResourceBundle.getBundle(
    "messages",
    Locale.CHINA);

// 获取消息
String greeting = bundle.getString("greeting");
System.out.println(greeting);  // 你好

// 遍历所有键
Enumeration<String> keys = bundle.getKeys();
while (keys.hasMoreElements()) {
    String key = keys.nextElement();
    String value = bundle.getString(key);
    System.out.println(key + " = " + value);
}
```

### 缺失资源处理

```java
// 加载时指定控制
ResourceBundle bundle = ResourceBundle.getBundle(
    "messages",
    Locale.CHINA,
    ResourceBundle.Control.getControl(
        ResourceBundle.Control.FORMAT_PROPERTIES));

// 无资源时使用默认
try {
    ResourceBundle bundle = ResourceBundle.getBundle("messages");
} catch (MissingResourceException e) {
    // 使用默认值
}
```

---

## 5. 字符编码

### 编码转换

```java
import java.nio.charset.*;

// 字符串编码
String str = "你好世界";

// UTF-8 编码
byte[] utf8 = str.getBytes(StandardCharsets.UTF_8);

// GBK 编码
byte[] gbk = str.getBytes(Charset.forName("GBK"));

// 解码
String decoded = new String(utf8, StandardCharsets.UTF_8);
```

### 读写文件编码

```java
import java.nio.file.*;
import java.nio.charset.*;

// 写入文件 (UTF-8)
Files.writeString(Paths.get("output.txt"),
    "你好世界",
    StandardCharsets.UTF_8);

// 读取文件 (UTF-8)
String content = Files.readString(
    Paths.get("input.txt"),
    StandardCharsets.UTF_8);

// 指定编码
Files.write(Paths.get("gbk.txt"),
    "GBK 内容".getBytes("GBK"));
```

---

## 6. 格式化

### 数字格式化

```java
import java.text.*;
import java.util.*;

// 数字格式
NumberFormat nf = NumberFormat.getInstance(Locale.FRANCE);
String number = nf.format(1234.56);  // 1 234,56

// 货币格式
NumberFormat cf = NumberFormat.getCurrencyInstance(Locale.JAPAN);
String currency = cf.format(1234.56);  // ￥1,235

// 百分比
NumberFormat pf = NumberFormat.getPercentInstance(Locale.ITALY);
String percent = pf.format(0.75);  // 75%
```

### 日期时间格式化 (JDK 8+)

```java
import java.time.*;
import java.time.format.*;

// 本地化日期
LocalDate date = LocalDate.now();
DateTimeFormatter formatter =
    DateTimeFormatter.ofLocalizedDate(FormatStyle.FULL)
        .withLocale(Locale.CHINA);

String formatted = date.format(formatter);
// 2026年3月20日 星期五

// 自定义格式
DateTimeFormatter customFormatter =
    DateTimeFormatter.ofPattern("yyyy年MM月dd日 EEEE")
        .withLocale(Locale.CHINESE);
```

### 旧版日期格式化

```java
import java.text.*;

// 日期格式
DateFormat df = DateFormat.getDateInstance(
    DateFormat.FULL,
    Locale.FRANCE);
String dateStr = df.format(new Date());

// 时间格式
DateFormat tf = DateFormat.getTimeInstance(
    DateFormat.LONG,
    Locale.JAPAN);

// 日期时间格式
DateFormat dtf = DateFormat.getDateTimeInstance(
    DateFormat.LONG,
    DateFormat.LONG,
    Locale.GERMANY);
```

---

## 7. Unicode 支持

### Unicode 版本

| JDK | Unicode 版本 | 说明 |
|-----|--------------|------|
| JDK 1.4 | 3.0 | 基础支持 |
| JDK 5 | 4.0 | 完整支持 |
| JDK 7 | 6.0 | 脚本增强 |
| JDK 8 | 6.2 | 更多字符 |
| JDK 17 | 13.0 | 表情符号 |
| JDK 21 | 15.0 | 最新标准 |

### Unicode 字符

```java
// 基本多文种平面 (BMP)
char c1 = 'A';  // U+0041
char c2 = '中'; // U+4E2D

// 补充平面 (需要代理对)
String emoji = "😀";  // U+1F600

// 代码点
int codePoint = emoji.codePointAt(0);  // 128512

// 遍历代码点
String str = "Hello 👋 世界";
str.codePoints().forEach(cp -> {
    System.out.println(Integer.toHexString(cp));
});
```

### 正则表达式 Unicode

```java
// Unicode 类别
String text = "Hello 世界 123";
text.matches(".*\\p{L}.*");  // 包含字母

// 匹配中文
text.matches(".*\\p{script=Han}.*");

// 匹配表情符号
String emoji = "😀";
emoji.matches(".*\\p{So}.*");  // Symbol Other
```

---

## 8. ICU4J 集成

### CLDR 数据

```java
import com.ibm.icu.text.*;
import com.ibm.icu.util.*;
import com.ibm.icu.lang.*;

// ICU Locale
ULocale ulocale = ULocale.CHINA;

// ICU NumberFormat
NumberFormat nf = NumberFormat.getInstance(ulocale);

// ICU DateFormat
com.ibm.icu.text.DateFormat df =
    com.ibm.icu.text.DateFormat.getDateInstance(
        com.ibm.icu.text.DateFormat.FULL,
        ulocale);

// ICU BreakIterator (文本边界)
BreakIterator bi = BreakIterator.getWordInstance(ulocale);
bi.setText("Hello世界");
int start = bi.first();
int end = bi.next();
```

---

## 9. Bidi (双向文本)

### 文本方向

```java
import java.text.*;

// 检测文本方向
String arabic = "مرحبا";
String hebrew = "שלום";
String mixed = "Hello مرحبا שלום";

Bidi bidi = new Bidi(mixed, Bidi.DIRECTION_DEFAULT_LEFT_TO_RIGHT);
boolean isRTL = bidi.isMixed() || bidi.getDirection() == Bidi.DIRECTION_RIGHT_TO_LEFT;

// 获取方向
int direction = bidi.getBaseLevel();  // 0 = LTR, 1 = RTL
```

### Bidi 格式化

```java
import java.awt.font.*;
import java.awt.*;

// 文本布局
String text = "Hello \u05D0\u05D1\u05D2";  // 混合 LTR/RTL
Font font = new Font("Arial", Font.PLAIN, 12);
FontRenderContext frc = new FontRenderContext(null, true, true);

TextLayout layout = new TextLayout(text, font, frc);
layout.draw(graphics, x, y);
```

---

## 10. 最佳实践

### 1. 使用 UTF-8

```java
// ✅ 推荐
Files.writeString(path, content, StandardCharsets.UTF_8);
new String(bytes, StandardCharsets.UTF_8);

// ❌ 避免平台默认编码
Files.writeString(path, content);  // 依赖平台
new String(bytes);                 // 依赖平台
```

### 2. 资源文件命名

```
messages.properties              # 默认
messages_zh.properties           # 中文 (通用)
messages_zh_CN.properties        # 简体中文
messages_zh_TW.properties        # 繁体中文
messages_en.properties           # 英文 (通用)
messages_en_US.properties        # 美式英语
```

### 3. Locale 敏感操作

```java
// 总是显式指定 Locale
NumberFormat.getInstance(Locale.US);
DateFormat.getDateInstance(DateFormat.SHORT, Locale.JAPAN);
String.toUpperCase(Locale.ENGLISH);  // 而非 toUpperCase()
```

---

## 11. 相关链接

### 本地文档

- [安全](../security/) - 加密
- [字符串](../../language/string/) - 字符处理

### 外部参考

**技术文档:**
- [ICU User Guide](https://unicode-org.github.io/icu/userguide/)
- [CLDR (Unicode Common Locale Data Repository)](https://cldr.unicode.org/)
- [Unicode Standard](https://www.unicode.org/standard/standard.html)
