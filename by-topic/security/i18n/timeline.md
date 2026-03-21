# 国际化演进时间线

Java 国际化 (i18n) 从 JDK 1.0 到 JDK 26 的完整演进历程。

---
## 目录

1. [时间线概览](#1-时间线概览)
2. [Locale](#2-locale)
3. [ResourceBundle](#3-resourcebundle)
4. [JDK 5 - Formatter](#4-jdk-5---formatter)
5. [JDK 6 - Unicode 增强](#5-jdk-6---unicode-增强)
6. [JDK 8+ - CLDR](#6-jdk-8---cldr)
7. [JDK 13+ - Unicode 增强](#7-jdk-13---unicode-增强)
8. [JDK 18+ - Unicode Extensions](#8-jdk-18---unicode-extensions)
9. [最佳实践](#9-最佳实践)
10. [时间线总结](#10-时间线总结)
11. [相关链接](#11-相关链接)

---


## 1. 时间线概览

```
JDK 1.0 ──── JDK 5 ──── JDK 6 ──── JDK 8 ──── JDK 13 ──── JDK 18 ──── JDK 26
 │             │           │           │           │           │           │
Locale       Formatter    Unicode    CLDR      Unicode    Unicode    BCP 47
Resource     增强        6.0       Locale     13.0      Extensions  标签
Bundle                                    Data       (EAI/EAO)
```

---

## 2. Locale

### 基础使用

```java
import java.util.*;

// Locale 创建
Locale zhCN = Locale.CHINA;               // zh_CN
Locale enUS = Locale.US;                   // en_US
Locale custom = new Locale("zh", "TW");   // zh_TW

// 获取默认 Locale
Locale default = Locale.getDefault();

// 设置默认 Locale
Locale.setDefault(new Locale("zh", "CN"));

// 可用 Locale
Locale[] availableLocales = Locale.getAvailableLocales();
for (Locale locale : availableLocales) {
    System.out.println(locale.getDisplayName() + ": " + locale);
}
```

### Locale 组成部分

```java
// Locale 构成
// language 语言代码 (ISO 639)
// country 国家/地区代码 (ISO 3166)
// variant 变体代码

Locale locale = new Locale("zh", "CN", "HK");
// 语言: zh
// 国家: CN
// 变体: HK (香港)

// 获取组成部分
String language = locale.getLanguage();    // zh
String country = locale.getCountry();      // CN
String variant = locale.getVariant();      // HK

// 显示信息
String displayName = locale.getDisplayName();  // Chinese (China,HK)
String displayLanguage = locale.getDisplayLanguage(locale);  // Chinese
String displayCountry = locale.getDisplayCountry(locale);    // China
```

---

## 3. ResourceBundle

### 基础使用

```java
import java.util.*;

// 资源文件
// Messages.properties
//   greeting=Hello
// Messages_zh_CN.properties
//   greeting=你好

// 加载资源
ResourceBundle bundle = ResourceBundle.getBundle("Messages", Locale.CHINA);

// 获取值
String greeting = bundle.getString("greeting");

// 处理缺失值
String value;
if (bundle.containsKey("key")) {
    value = bundle.getString("key");
} else {
    value = "default";
}
```

### 命名约定

```
资源文件命名:
- baseName.properties
- baseName_language.properties
- baseName_language_COUNTRY.properties
- baseName_language_COUNTRY_VARIANT.properties

示例:
- Messages.properties
- Messages_zh.properties
- Messages_zh_CN.properties
- Messages_zh_TW_HK.properties
```

### ResourceBundle.Control

```java
// 自定义资源加载控制
ResourceBundle bundle = ResourceBundle.getBundle(
    "Messages",
    Locale.CHINA,
    new ResourceBundle.Control() {
        @Override
        public List<Locale> getCandidateLocales(String baseName, Locale locale) {
            // 自定义候选 Locale
            return List.of(locale, Locale.ENGLISH);
        }

        @Override
        public long getTimeToLive(String baseName, Locale locale) {
            // 缓存时间 (毫秒)
            return 3600000;  // 1小时
        }

        @Override
        public boolean needsReload(String baseName, Locale locale) {
            // 是否需要重新加载
            return false;
        }
    }
);
```

---

## 4. JDK 5 - Formatter

### 数字格式化

```java
import java.text.*;

// 数字格式化
NumberFormat nf = NumberFormat.getInstance(Locale.US);

// 整数
String integer = nf.format(1234567);  // 1,234,567

// 货币
NumberFormat cf = NumberFormat.getCurrencyInstance(Locale.US);
String currency = cf.format(1234.56);  // $1,234.56

// 百分比
NumberFormat pf = NumberFormat.getPercentInstance(Locale.US);
String percent = pf.format(0.75);  // 75%

// 自定义
DecimalFormat df = new DecimalFormat("#,###0.00");
String custom = df.format(1234.5);  // 1,234.50
```

### 日期格式化

```java
// 日期格式化
SimpleDateFormat sdf = new SimpleDateFormat(
    "yyyy-MM-dd HH:mm:ss",
    Locale.CHINA
);

String formatted = sdf.format(new Date());

// 不同地区的日期格式
Locale us = Locale.US;
Locale fr = Locale.FRANCE;

SimpleDateFormat usFormat = new SimpleDateFormat("MM/dd/yyyy", us);
SimpleDateFormat frFormat = new SimpleDateFormat("dd/MM/yyyy", fr);

System.out.println(usFormat.format(new Date()));  // 03/20/2026
System.out.println(frFormat.format(new Date()));  // 20/03/2026
```

### MessageFormat

```java
// MessageFormat - 参数化消息
String pattern = "Hello {0}, you have {1} messages.";

// 格式化
String result = MessageFormat.format(pattern, "Alice", 5);
// Hello Alice, you have 5 messages.

// 不同语言
String patternUS = "Hello {0}, you have {1} messages.";
String patternCN = "你好 {0}，您有 {1} 条消息。";
```

---

## 5. JDK 6 - Unicode 增强

### Unicode 支持

```java
// Unicode 字符处理
String emoji = "😀";  // U+1F600

// 代码点数量
int codePointCount = emoji.codePointCount(0, emoji.length());  // 1

// 遍历代码点
emoji.codePoints().forEach(cp -> {
    System.out.println(Integer.toHexString(cp));  // 1f600
});

// 按代码点反转
String reversed = new StringBuilder(emoji)
    .reverse()
    .toString();
```

### Normalizer

```java
import java.text.*;

// Unicode 规范化
String text1 = "é";  // 可以是一个字符或组合字符
String text2 = "e\u0301";  // e + combining acute accent

// 规范化
// NFC - 规范化形式 C (组合)
String nfc = Normalizer.normalize(text2, Normalizer.Form.NFC);

// NFD - 规范化形式 D (分解)
String nfd = Normalizer.normalize(text1, Normalizer.Form.NFD);

// 比较
boolean equals = nfc.equals(nfd);  // true
```

---

## 6. JDK 8+ - CLDR

### CLDR (Unicode Common Locale Data Repository)

```java
// JDK 8+ 使用 CLDR 数据
// 更准确的本地化信息

// 货币符号
String cny = NumberFormat.getCurrencyInstance(
    Locale.CHINA
).getCurrency().getSymbol(Locale.CHINA);  // CN¥

// 星期几
DateFormatSymbols dfs = DateFormatSymbols.getInstance(Locale.CHINA);
String[] weekdays = dfs.getWeekdays();  // [星期日, 星期一, ...]
String[] shortWeekdays = dfs.getShortWeekdays();  // [周日, 周一, ...]
```

---

## 7. JDK 13+ - Unicode 增强

### Unicode 13

```java
// JDK 13 支持 Unicode 13
// 新增字符和脚本

// 检测字符支持
if (Character.isISOControl(c)) {
    // 控制字符
}

if (Character.isUnicodeIdentifierStart(c)) {
    // 可作为标识符开头
}
```

---

## 8. JDK 18+ - Unicode Extensions

### Unicode 扩展

```java
// Unicode 扩展 (EAI - Emoji)
// 扩展字母数字

// 判断字母
if (Character.isLetter(c)) {
    // 包括扩展字母
}

// Unicode 脚本
if (Character.isIdeograph(c)) {
    // 表意文字 (中文、日文等)
}
```

---

## 9. 最佳实践

### 资源文件管理

```
resources/
├── Messages.properties           # 默认 (en_US)
├── Messages_zh_CN.properties      # 简体中文
├── Messages_zh_TW.properties      # 繁体中文
└── Messages_ja_JP.properties      # 日文
```

### 文件编码

```java
// ✅ 推荐: 使用 UTF-8
// 资源文件使用 UTF-8 编码

// Properties 文件编码
Properties prop = new Properties();
try (InputStream is = getClass().getResourceAsStream("/messages_zh_CN.properties")) {
    // 使用 ISO-8859-1 读取，文件需要 native2ascii
    prop.load(is);
}

// ✅ 推荐: 使用 ResourceBundle
// 自动处理编码
```

---

## 10. 时间线总结

| 版本 | 特性 | 说明 |
|------|------|------|
| JDK 1.0 | Locale, ResourceBundle | 基础 i18n |
| JDK 1.1 | DecimalFormat, SimpleDateFormat | 格式化 |
| JDK 5 | Formatter, MessageFormat | 增强格式化 |
| JDK 6 | Unicode 4.0 | 规范化 |
| JDK 8 | CLDR 数据 | 更准确本地化 |
| JDK 13 | Unicode 13 | 新字符支持 |
| JDK 18 | Unicode 扩展 | EAI 支持 |

---

## 11. 相关链接

- [Locale](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Locale.html)
- [ResourceBundle](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/ResourceBundle.html)
