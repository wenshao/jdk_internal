# 字符串处理演进时间线

> Java String 从 JDK 1.0 到 JDK 26 的完整演进历程

---

## 时间线概览

```
JDK 1.0 ──── JDK 5 ──── JDK 8 ──── JDK 9 ──── JDK 11 ──── JDK 15 ──── JDK 17 ──── JDK 21 ──── JDK 24 ──── JDK 25 ──── JDK 26
   │           │           │           │           │           │           │           │           │           │           │
 String     StringBuilder  StringJoiner Compact   repeat()   Text Blocks  transform()  String     Hidden     String     Integer/
 immutable               (JEP 254)    strip()    (JEP 378)  (JDK 12)    Templates  Class      Templates  Long
                                                                                      (JEP 430)  Concat     (Final)    toString
                                                                                                 Strategy              优化
                                                                                              (+40%启动)
```

---

## 核心演进：存储优化

### Compact Strings (JEP 254) - JDK 9

**问题**：JDK 8 及之前，String 使用 `char[]` 存储，每个字符占 2 字节 (UTF-16)，即使纯 ASCII 也如此。

**解决方案**：改用 `byte[]` + `coder` 标志，动态选择编码。

```java
// JDK 8 及之前
private final char[] value;  // 每字符 2 字节

// JDK 9+ (Compact Strings)
private final byte[] value;  // 实际存储
private final byte coder;    // 0 = LATIN1, 1 = UTF16

static final boolean COMPACT_STRINGS = true;  // 可通过 -XX:-CompactStrings 禁用
```

**内存影响**：

| 字符串类型 | JDK 8 | JDK 9+ | 节省 |
|-----------|-------|--------|------|
| 纯 ASCII "Hello" | 10 字节 + 对象头 | 5 字节 + 对象头 | **50%** |
| Latin-1 "Café" | 8 字节 + 对象头 | 4 字节 + 对象头 | **50%** |
| 中文 "你好" | 4 字节 + 对象头 | 4 字节 + 对象头 | 0% |
| 混合 "Hi你好" | 10 字节 + 对象头 | 10 字节 + 对象头 | 0% |

**VM 参数**：
```bash
-XX:+CompactStrings   # 启用 (默认)
-XX:-CompactStrings   # 禁用 (回退到 UTF-16)
```

**源码位置**：`src/java.base/share/classes/java/lang/String.java`

```java
// coder 常量定义
static final byte LATIN1 = 0;
static final byte UTF16  = 1;

// 长度计算
public int length() {
    return value.length >> coder;  // LATIN1: /1, UTF16: /2
}

// 编码检查
boolean isLatin1() {
    return COMPACT_STRINGS && coder == LATIN1;
}
```

---

## 时间线详情

### JDK 1.0 (1996) - String 诞生

- **不可变设计**：String 一旦创建不可修改
- **字符串常量池**：编译期字符串字面量进入常量池
- **`+` 操作符**：编译为 StringBuilder (JDK 1.0-1.4) 或 StringBuffer

```java
// JDK 1.0 设计
public final class String {
    private final char[] value;  // UTF-16 存储
    private final int offset;    // 子字符串共享数组
    private final int count;
    private final int hash;      // 延迟计算
}
```

### JDK 5 (2004) - StringBuilder

- **StringBuilder**：非同步的可变字符串，替代 StringBuffer
- **性能提升**：单线程场景下比 StringBuffer 快 2-3 倍

```java
// StringBuffer (同步，JDK 1.0)
public synchronized StringBuffer append(String str) { ... }

// StringBuilder (非同步，JDK 5+)
public StringBuilder append(String str) { ... }  // 无 synchronized
```

### JDK 6 - 性能优化

- **字符串去重**：G1 GC 可自动去重相同内容的字符串
- **子字符串优化**：`substring()` 不再共享数组 (JDK 7u6)

```bash
# G1 字符串去重 (JDK 8u20+)
-XX:+UseStringDeduplication
```

### JDK 8 (2014) - StringJoiner

- **StringJoiner**：便捷的字符串连接器
- **String.join()**：静态方法

```java
// StringJoiner
StringJoiner joiner = new StringJoiner(", ", "[", "]");
joiner.add("Apple").add("Banana").add("Cherry");
// "[Apple, Banana, Cherry]"

// String.join()
String result = String.join("-", "2024", "03", "20");
// "2024-03-20"
```

### JDK 9 (2017) - Compact Strings (JEP 254)

- **存储优化**：`char[]` → `byte[]` + `coder`
- **JEP 280**：`invokedynamic` 字符串拼接

```java
// JDK 8 编译
"a" + b + "c"
// → new StringBuilder().append("a").append(b).append("c").toString()

// JDK 9+ 编译 (invokedynamic)
"a" + b + "c"
// → invokedynamic StringConcatFactory.makeConcatWithConstants(...)
```

### JDK 11 (2018) - 新方法

- **repeat(int)**：重复字符串
- **strip()/stripLeading()/stripTrailing()**：Unicode 感知的空白处理
- **isBlank()**：检查是否为空白
- **lines()**：返回行流

```java
// repeat
"ab".repeat(3);  // "ababab"

// strip vs trim
"  hello  ".strip();           // "hello"
"  hello  ".trim();            // "hello"
"\u2000hello\u2000".strip();   // "hello" (Unicode 空白)
"\u2000hello\u2000".trim();    // "\u2000hello\u2000" (仅 ASCII)

// isBlank
"  ".isBlank();   // true
"".isBlank();     // true
"hello".isBlank(); // false

// lines
"a\nb\nc".lines().collect(Collectors.toList());  // ["a", "b", "c"]
```

### JDK 12 (2019) - transform()

- **transform()**：函数式字符串转换

```java
// transform (JDK 12+)
String result = "hello".transform(s -> s.toUpperCase() + "!");
// "HELLO!"
```

### JDK 13/14 (2020) - Text Blocks 预览

- **文本块**：多行字符串字面量

### JDK 15 (2020) - Text Blocks 正式 (JEP 378)

```java
// 传统方式
String json = "{\n" +
              "  \"name\": \"John\",\n" +
              "  \"age\": 30\n" +
              "}";

// Text Blocks (JDK 15+)
String json = """
    {
        "name": "John",
        "age": 30
    }
    """;

// stripIndent() - 自动去除公共缩进
String html = """
    <html>
        <body>Hello</body>
    </html>
    """.stripIndent();

// formatted() - 格式化
String msg = """
    Hello %s!
    You have %d messages.
    """.formatted(name, count);
```

### JDK 16 (2021) - 常量 API

- **describeConstable()**：返回常量描述
- **resolveConstantDesc()**：解析常量

```java
// JDK 12+ Constable 接口
Optional<String> desc = "hello".describeConstable();
// Optional["hello"]

// 在 ClassDesc 中使用
ClassDesc cd = ClassDesc.of("java.lang.String");
```

### JDK 17 (2021) - LTS 稳定版

- 整合 JDK 11-16 所有字符串特性
- 内部优化：字符串去重增强

### JDK 21 (2023) - String Templates 预览 (JEP 430)

- **模板表达式**：安全、可读的字符串插值
- **内置处理器**：STR, FMT, RAW

```java
// 传统拼接
String msg = "Hello " + name + ", you have " + count + " messages.";

// String Templates (JDK 21 预览)
String msg = STR."Hello \{name}, you have \{count} messages.";

// FMT 处理器 (格式化)
String pi = FMT."Pi is approximately \{Math.PI}%.2f";
// "Pi is approximately 3.14"

// 多行模板
String json = STR."""
    {
        "name": "\{name}",
        "age": \{age},
        "email": "\{email}"
    }
    """;
```

### JDK 24 (2025) - 隐藏类拼接策略 (JDK-8336856)

**重大优化**：统一字符串拼接策略，启动性能 **+40%**

| 指标 | 改善 |
|------|------|
| 启动性能 | **+40%** |
| 类生成数量 | **-50%** |

**原理**：按"形状"生成拼接类，而非每个调用点独立类

```
之前：1000 个拼接点 → 1000 个类
之后：1000 个拼接点 → ~20 个类（按参数类型共享）
```

**源码变更**：

```java
// StringConcatHelper.java (新增)
static abstract class StringConcatBase {
    @Stable final String[] constants;
    final int length;
    final byte coder;
}

static final class Concat1 extends StringConcatBase {
    @ForceInline
    String concat0(String value) {
        int length = stringSize(this.length, value);
        byte coder = (byte) (this.coder | value.coder());
        byte[] buf = newArray(length << coder);
        // 直接复制，避免 StringBuilder
        ...
        return new String(buf, coder);
    }
}
```

**详细分析**：[JDK-8336856: 高效隐藏类字符串拼接策略](/by-pr/8336/8336856.md)

### JDK 25 (2025) - String Templates 正式 + StringBuilder 优化

**1. String Templates 正式发布 (JEP 459)**

```java
// JSON 处理器 (需要自定义)
StringTemplate.Processor<String, RuntimeException> JSON = ...;
String json = JSON."""
    {"user": "\{user}", "data": \{data}}
    """;
```

**2. StringBuilder.append(char[]) 优化 (JDK-8355177)**

| 数组大小 | 优化前 | 优化后 | 提升 |
|----------|--------|--------|------|
| 10 chars | 132 ops/ms | 152 ops/ms | **+15%** |
| 100 chars | 14.5 ops/ms | 16.8 ops/ms | **+15%** |

**原理**：使用 `Unsafe.copyMemory` 替代 `System.arraycopy`

```java
// 优化前
System.arraycopy(str, 0, value, count, len);

// 优化后 (JDK 25)
UNSAFE.copyMemory(
    str, CHAR_ARRAY_BASE_OFFSET,
    value, CHAR_ARRAY_BASE_OFFSET + (count << 1),
    len << 1  // char = 2 bytes
);
```

**详细分析**：[JDK-8355177: StringBuilder append 优化](/by-pr/8355/8355177.md)

### JDK 26 (2026) - Compact Strings 清理 + toString 优化

**1. Integer/Long.toString 优化 (JDK-8370503)**

移除 `COMPACT_STRINGS = false` 代码路径，使用新 API：

```java
// 优化后
private static String toString(int i) {
    // 数字永远是 LATIN1
    return String.newStringWithLatin1Bytes(DecimalDigits.digitPair(i));
}
```

| 场景 | 提升 |
|------|------|
| 解释器 | +6% |
| C1 编译 | **+16%** (方法可内联) |
| C2 编译 | +7% |

**2. ClassDesc 字符串拼接优化 (JDK-8338937)**

| 操作 | 提升 |
|------|------|
| `ClassDesc.of()` | **+29%** |
| `ofInternalName()` | **+27%** |
| `displayName()` | **+17%** |

---

## 源码结构

### 核心文件

```
src/java.base/share/classes/java/lang/
├── String.java              # 核心 String 类 (216,787 行)
├── StringBuilder.java       # 可变字符串 (16,121 行)
├── StringBuffer.java        # 同步可变字符串 (25,340 行)
├── StringConcatHelper.java  # 拼接辅助类 (18,087 行)
├── StringLatin1.java        # LATIN1 编码操作 (42,048 行)
├── StringUTF16.java         # UTF16 编码操作 (76,697 行)
└── StringCoding.java        # 编码转换 (7,711 行)

src/java.base/share/classes/java/lang/invoke/
└── StringConcatFactory.java # invokedynamic 拼接工厂
```

### String 类关键字段

```java
public final class String
    implements java.io.Serializable, Comparable<String>, CharSequence,
               Constable, ConstantDesc {

    // 存储优化 (JDK 9+)
    @Stable
    private final byte[] value;  // 实际字符存储

    private final byte coder;    // 编码: LATIN1(0) 或 UTF16(1)

    // 哈希缓存
    private int hash;            // 延迟计算，缓存

    // 常量
    static final byte LATIN1 = 0;
    static final byte UTF16  = 1;
    static final boolean COMPACT_STRINGS = true;
}
```

---

## 性能对比总结

| 版本 | 特性 | 性能影响 |
|------|------|----------|
| **JDK 9** | Compact Strings | ASCII 内存 **-50%** |
| **JDK 9** | invokedynamic 拼接 | 启动性能提升 |
| **JDK 21** | String Templates | 开发效率 + 安全性 |
| **JDK 24** | 隐藏类拼接策略 | 启动 **+40%**，类数量 **-50%** |
| **JDK 25** | StringBuilder.append | **+15%** |
| **JDK 25** | String Templates 正式 | 标准化 |
| **JDK 26** | Integer/Long.toString | C1 **+16%** |

---

## 最佳实践

### 字符串拼接

```java
// ✅ 简单拼接：使用 + (编译器优化)
String result = "Hello " + name;

// ✅ 循环拼接：使用 StringBuilder
StringBuilder sb = new StringBuilder();
for (String s : list) {
    sb.append(s);
}

// ✅ JDK 8+：使用 StringJoiner 或 Collectors.joining
String result = list.stream().collect(Collectors.joining(", "));

// ✅ JDK 25+：使用 String Templates
String result = STR."Hello \{name}!";

// ❌ 避免：循环中使用 +
String result = "";
for (String s : list) {
    result += s;  // 每次创建新 String 和 StringBuilder
}
```

### 字符串比较

```java
// ✅ 使用 equals()
if (str1.equals(str2)) { }

// ✅ 空安全比较
if (Objects.equals(str1, str2)) { }

// ✅ 空白检查 (JDK 11+)
if (str.isBlank()) { }

// ❌ 不要使用 == 比较内容
if (str1 == str2) { }  // 仅比较引用，可能失败
```

### 字符串空白处理

```java
// JDK 11+ 推荐
str.strip();         // Unicode 感知
str.stripLeading();
str.stripTrailing();
str.isBlank();       // 检查是否全为空白

// 传统方式 (仅 ASCII 空白)
str.trim();
```

### VM 调优

```bash
# Compact Strings (默认启用)
-XX:+CompactStrings

# G1 字符串去重
-XX:+UseStringDeduplication

# 字符串拼接调优 (JDK 24+)
-Djava.lang.invoke.StringConcat.highArityThreshold=0
-Djava.lang.invoke.StringConcat.cacheThreshold=256
-Djava.lang.invoke.StringConcat.inlineThreshold=16
```

---

## 相关 JEP

| JEP | 标题 | 版本 | 说明 |
|-----|------|------|------|
| [JEP 254](https://openjdk.org/jeps/254) | Compact Strings | JDK 9 | 内存优化存储 |
| [JEP 280](https://openjdk.org/jeps/280) | Indify String Concatenation | JDK 9 | invokedynamic 拼接 |
| [JEP 371](https://openjdk.org/jeps/371) | Hidden Classes | JDK 15 | 动态类生成 |
| [JEP 378](https://openjdk.org/jeps/378) | Text Blocks | JDK 15 | 多行字符串 |
| [JEP 430](https://openjdk.org/jeps/430) | String Templates (Preview) | JDK 21 | 字符串插值 |
| [JEP 459](https://openjdk.org/jeps/459) | String Templates (Second Preview) | JDK 23 | 改进 |

---

## 相关 PR 分析

| PR | 标题 | 版本 | 影响 |
|----|------|------|------|
| [JDK-8336856](/by-pr/8336/8336856.md) | 隐藏类拼接策略 | JDK 24 | ⭐⭐⭐⭐⭐ 启动+40% |
| [JDK-8355177](/by-pr/8355/8355177.md) | StringBuilder.append 优化 | JDK 25 | ⭐⭐⭐⭐ +15% |
| [JDK-8338937](/by-pr/8338/8338937.md) | ClassDesc 拼接优化 | JDK 24 | ⭐⭐⭐ +20-30% |
| [JDK-8370503](/by-pr/8370/8370503.md) | Integer/Long.toString | JDK 26 | ⭐⭐⭐ +16% C1 |
| [JDK-8368024](/by-pr/8368/8368024.md) | 移除 MH InlineCopy | JDK 26 | ⭐⭐ 代码清理 |

---

## 参考资源

- [OpenJDK: String 源码](https://github.com/openjdk/jdk/blob/master/src/java.base/share/classes/java/lang/String.java)
- [JEP 254: Compact Strings](https://openjdk.org/jeps/254)
- [JEP 430: String Templates](https://openjdk.org/jeps/430)
- [Inside Java: Performance Improvements in JDK 24](https://inside.java/2025/03/19/performance-improvements-in-jdk24/)
- [Contributor: Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) - 主要字符串优化贡献者

---

> **文档版本**: 3.0
> **最后更新**: 2026-03-20
> **数据来源**: JDK 源码、JEP、GitHub PR 分析
