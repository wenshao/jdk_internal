# 字符串处理

> Java String 从 JDK 1.0 到 JDK 26 的演进历程

[← 返回语言特性](../)

---

## 快速概览

```
JDK 1.0 ── JDK 5 ── JDK 7u6 ── JDK 9 ── JDK 11 ── JDK 15 ── JDK 21 ── JDK 24 ── JDK 25 ── JDK 26
   │         │         │          │         │          │          │         │         │         │
 String   StringBuilder Substring Compact  repeat()  Text Blocks  String   Hidden   String   toString
  诞生      无同步      修复     Strings   strip()    (JEP 378)  Templates Class    repeat   优化
 常量池                                            (JEP 378)  (撤回)    Strategy  优化    (JDK 25)
(+40%启动)
```

### 核心特性

| 特性 | 版本 | JEP | 说明 |
|------|------|-----|------|
| **Compact Strings** | JDK 9 | JEP 254 | byte[] 存储，ASCII 内存节省 50% |
| **String Deduplication** | JDK 8u20 | - | GC 自动去重，节省 10-30% 内存 |
| **invokedynamic 拼接** | JDK 9 | JEP 280 | 编译时优化，+10% 启动性能 |
| **Text Blocks** | JDK 15 | JEP 378 | 多行字符串 `"""..."""` |
| **String Templates** | JDK 21 | JEP 430 | **已撤回** (JDK 23 移除) |
| **隐藏类拼接** | JDK 24 | - | +40% 启动性能 |

---

## 目录

- [字符串 API](#字符串-api)
- [内部实现](#内部实现)
- [性能优化](#性能优化)
- [版本演进](#版本演进)
- [最新增强](#最新增强)
- [核心贡献者](#核心贡献者)
- [相关链接](#相关链接)

---

## 字符串 API

### 基础操作

```java
// 创建字符串
String s1 = "Hello";                    // 字符串字面量
String s2 = new String("Hello");        // 新对象
String s3 = String.valueOf(123);         // 从其他类型

// 比较
s1.equals("Hello");                     // 内容相等
s1 == "Hello";                          // 引用相等 (字面量池)
"Hello".equalsIgnoreCase("hello");       // 忽略大小写

// 连接
String result = "Hello " + "World";     // 编译器优化
String joined = String.join(", ", "A", "B", "C");  // JDK 8+
```

### 空白处理

```java
String text = "  Hello World  ";

// JDK 11+ 新方法
text.strip();                            // Unicode 感知去空格
text.stripLeading();                     // 去前导空格
text.stripTrailing();                    // 去尾随空格
text.isBlank();                          // 是否为空或仅空白

// 传统方法
text.trim();                             // ASCII 空白 (≤ U+0020)
```

### 字符串重复

```java
// JDK 11+
String repeated = "abc".repeat(3);       // "abcabcabc"

// JDK 8 方式
String repeated = Collections.nCopies(3, "abc")
    .stream()
    .collect(Collectors.joining());
```

### 缩进处理

```java
// JDK 12+ indent() - 相对缩进
String indented = "Line1\nLine2".indent(4);

String result = """
    Line1
    Line2
    """.stripIndent().indent(2);         // JDK 15+ Text Blocks
```

### 字符串格式化

```java
// 格式化字符串
String formatted = String.format("Hello %s, age %d", "Alice", 25);

// formatted() - JDK 16+
String formatted = "Hello %s, age %d".formatted("Alice", 25);
```

---

## 内部实现

### Compact Strings (JDK 9)

**JEP 254: Compact Strings**

```java
// JDK 9 之前: char[] 存储
// JDK 9 之后: byte[] 存储 + coder 标识

class String {
    final byte[] value;      // 字节数组
    final byte coder;        // 0 = LATIN1, 1 = UTF16
    // ...
}

// 内存优势:
// - ASCII 字符串节省 50% 内存
// - 更好的缓存局部性
```

**启用/禁用**:

```bash
# 启用 Compact Strings (默认)
-XX:+CompactStrings

# 禁用
-XX:-CompactStrings
```

### StringLatin1 和 StringUTF16

```java
// 内部实现类 (包级访问)
class StringLatin1 {
    static int indexOf(byte[] value, int ch) {}
    static void inflate(byte[] src, char[] dst) {}
    // ... LATIN1 (单字节) 操作
}

class StringUTF16 {
    static int indexOf(byte[] value, int ch) {}
    static byte[] toBytes(char[] value) {}
    // ... UTF16 (双字节) 操作
}
```

### invokedynamic 拼接

**JEP 280: Indify String Concatenation**

```java
// JDK 9 之前: StringBuilder
String result = a + b + c;
// 编译为:
// new StringBuilder().append(a).append(b).append(c).toString();

// JDK 9+: invokedynamic
// 编译为:
// invokedynamic makeConcatWithConstants(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;
```

**策略选择**:

```bash
# 查看当前策略
-Djava.lang.invoke.StringConcat.DEBUG=true
-Djava.lang.invoke.StringConcat.cacheThreshold=256

# 策略:
# - BC: StringBuilder (JDK 8 风格)
# - HB: handleInline (少量字符串)
# - HM: inline (中等数量)
# - MC: mixin (大量字符串, 隐藏类)
```

---

## 性能优化

### String Deduplication

```bash
# 启用字符串去重
-XX:+UseStringDeduplication
-XX:+UseG1GC
-XX:StringDeduplicationAgeThreshold=3

# 统计信息
-XX:+PrintStringDeduplicationStatistics
```

**工作原理**:

```
┌─────────────────────────────────────────────────────────┐
│              String Deduplication 过程                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. GC 标记存活对象                                     │
│  2. 识别重复字符串 (通过哈希表)                          │
│  3. 保留一个副本, 其他指向该副本                         │
│  4. 原字节数组可被 GC 回收                               │
│                                                         │
│  节省: 10-30% 堆内存                                     │
│  开销: GC 停顿时间略微增加                               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### StringBuilder 优化 (JDK 25)

```java
// JDK 25 Unsafe 优化
// StringBuilder.append(char) 使用 sun.misc.Unsafe

// 性能提升: +15% 吞吐量
// 相关: JDK-8355177
```

### toString 优化 (JDK 26)

```java
// Integer.toString LATIN1 路径优化
// 性能提升: +16% C1 编译

// 相关: JDK-8370503
```

---

## 版本演进

### JDK 1.0 - String 诞生

```java
// 基础功能
String s = "Hello";
s.length();
s.charAt(0);
s.substring(1, 3);
```

### JDK 5 - StringBuilder

```java
// StringBuilder 替代 StringBuffer
// 非同步版本, 性能更好

StringBuilder sb = new StringBuilder();
sb.append("Hello").append(" World");
```

### JDK 7u6 - substring 修复

```java
// JDK 7u6 之前: substring 共享 char[]
String s1 = "Hello World";
String s2 = s1.substring(0, 5);  // 引用原 char[], 可能导致内存泄漏

// JDK 7u6 之后: 复制 char[]
String s2 = s1.substring(0, 5);  // 新的 char[]
```

### JDK 9 - Compact Strings

```java
// ASCII 字符串内存节省 50%
// 启动性能 +10%

// 检查是否启用
System.out.println("COMPACT_STRINGS: " +
    sun.misc.VM.isCompactStringsEnabled());
```

### JDK 11 - 新方法

```java
// 空白处理
"  text  ".strip();          // "text"
"  text  ".stripLeading();   // "text  "
"  text  ".stripTrailing();  // "  text"
"".isBlank();                // true

// 重复
"abc".repeat(3);             // "abcabcabc"

// 行处理
"Line1\nLine2".lines();     // Stream<String>
```

### JDK 15 - Text Blocks

```java
// 多行字符串 (JEP 378)
String json = """
    {
        "name": "John",
        "age": 30
    }
    """;

// 自动格式化
String text = """
    Hello
    World
    """.stripIndent();       // 去除统一缩进
```

### JDK 21 - String Templates (已撤回)

```java
// ⚠️ 此功能在 JDK 21-22 预览后, 已从 JDK 23 移除

// 原计划语法 (JEP 430):
String name = "World";
String message = STR."Hello \{name}!";  // 使用 STR 模板处理器

// 其他处理器:
// FMT."Value: \{value}%.2f"           // 格式化
// RAW."Text: \{value}"                  // 原始字符串
```

**撤回原因**:
- 设计需要进一步讨论
- 社区反馈需要更多考虑
- 没有确定何时会重新引入

### JDK 24 - 隐藏类拼接

```java
// StringConcat 使用隐藏类策略
// 每个"形状"的拼接点共享同一个类

// 性能提升:
// - 启动性能 +40%
// - 元空间占用 -60%
// - 相关: JDK-8227379
```

### JDK 25 - String repeat 优化

```java
// String.repeat() 性能优化
// JDK-8357288

// 新实现更高效:
String repeated = "abc".repeat(1000);
```

---

## 最新增强

### JDK 25: StringBuilder Unsafe 优化

```java
// JDK-8355177: StringBuilder 使用 Unsafe 操作
// append(char) 性能提升 15%

// 优化前: 使用数组 + 范围检查
// 优化后: 使用 Unsafe.putByte()
```

### JDK 26: Integer.toString LATIN1 路径

```java
// JDK-8370503: Integer.toString 优化
// 当目标字符串是 LATIN1 时, 使用优化路径

// 性能提升: C1 编译后 +16%
```

### JDK 26: String.format() C2 优化

```java
// JDK-8367129: String.format() JIT 优化
// C2 编译器优化

// 性能提升: 显著提升 (取决于场景)
```

---

## 文档导航

### [时间线](timeline.md)

完整的版本演进历史，从 JDK 1.0 到 JDK 26。

→ [查看时间线](timeline.md)

### [内部实现](implementation.md)

Compact Strings、StringLatin1、StringUTF16 的详细实现。

→ [查看实现](implementation.md)

### [性能优化](optimization.md)

String Deduplication、VM 调优参数、最佳实践。

→ [查看优化](optimization.md)

---

## VM 参数

### Compact Strings

```bash
# 启用 (默认)
-XX:+CompactStrings

# 禁用
-XX:-CompactStrings

# 查看状态
-XX:+PrintCompactStringsInfo
```

### String Deduplication

```bash
# 启用
-XX:+UseStringDeduplication
-XX:+UseG1GC
-XX:StringDeduplicationAgeThreshold=3

# 统计
-XX:+PrintStringDeduplicationStatistics
```

### String Concatenation

```bash
# 调试信息
-Djava.lang.invoke.StringConcat.DEBUG=true
-Djava.lang.invoke.StringConcat.cacheThreshold=256

# 策略选择
-Djava.lang.invoke.StringConcat.factory=BC|HB|HM|MC
```

---

## 内部详情

### 源码结构

```
src/java.base/share/classes/java/lang/
├── String.java              # 主类 (~3500 行)
├── StringConcatHelper.java  # 拼接辅助 (JDK 9+)
├── StringBuilder.java       # 可变字符串
└── StringBuffer.java        # 同步版本

src/java.base/share/classes/java/lang/invoke/
└── StringConcatFactory.java # invokedynamic 拼接工厂

src/java.base/share/classes/jdk/internal/
├── StringConcatHelper.java  # 内部辅助方法
└── VMAnnotations.java       # VM 相关注解

src/hotspot/share/oops/
├── instanceKlass.cpp        # String 类元数据
└── stringTable.cpp          # String 常量池实现

src/hotspot/share/gc/
├── stringdedup/             # String 去重实现
└── g1/g1StringDedup.cpp     # G1 GC 去重
```

### 关键内部类

| 类 | 作用 | 包级访问 |
|---|------|----------|
| `StringLatin1` | LATIN1 编码操作 | `java.lang` |
| `StringUTF16` | UTF16 编码操作 | `java.lang` |
| `StringConcatHelper` | 拼接 helper 方法 | `jdk.internal` |
| `StringConcatFactory` | invokedynamic 工厂 | `java.lang.invoke` |

### 关键 JDK Bug IDs

| Bug ID | 描述 | 修复版本 |
|--------|------|----------|
| JDK-8054307 | substring 内存泄漏 | JDK 7u6 |
| JDK-8077559 | Compact Strings 实现 | JDK 9 |
| JDK-8227379 | StringConcat 隐藏类策略 | JDK 24 |
| JDK-8355177 | StringBuilder Unsafe 优化 | JDK 25 |
| JDK-8370503 | Integer.toString LATIN1 路径 | JDK 26 |

---

## 相关链接

### 本地文档

- [时间线](timeline.md) - 完整版本演进历史
- [内部实现](implementation.md) - Compact Strings、StringLatin1、StringUTF16
- [性能优化](optimization.md) - String Deduplication、VM 调优参数

### 相关主题

- [日期时间 API](../../api/datetime/) - DateTimeHelper 字符串格式化
- [集合框架](../../api/collections/) - StringBuilder 与集合
- [性能优化](../../core/performance/) - 字符串性能基准
- [内存管理](../../core/memory/) - String Deduplication
- [语法演进](../syntax/) - 语言特性

### 外部参考

- [JEP 254: Compact Strings](https://openjdk.org/jeps/254)
- [JEP 280: Indify String Concatenation](https://openjdk.org/jeps/280)
- [JEP 378: Text Blocks](https://openjdk.org/jeps/378)
- [JEP 430: String Templates (Preview)](https://openjdk.org/jeps/430) ⚠️ 已撤回
- [Inside Java Newscast #71](https://nipafx.dev/inside-java-newscast-71/) - String Templates 撤回说明
- [OpenJDK String 源码](https://github.com/openjdk/jdk/blob/master/src/java.base/share/classes/java/lang/String.java)

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### String 处理 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Claes Redestad | 101 | Oracle | Compact Strings, 启动优化 |
| 2 | Mandy Chung | 54 | Oracle | String 模板 |
| 3 | Chen Liang | 35 | Oracle | invokedynamic, ClassFile |
| 4 | Jim Laskey | 29 | Oracle | String Templates (JEP 430) |
| 5 | Joe Darcy | 20 | Oracle | Text Blocks (JEP 378) |
| 6 | Jorn Vernee | 19 | Oracle | Foreign Memory |
| 7 | Paul Sandoz | 17 | Oracle | 字符串格式化 |
| 8 | Pavel Rappo | 15 | Oracle | 文档, 工具 |
| 9 | Maurizio Cimadamore | 15 | Oracle | javac, 模板 |
| 10 | Shaojin Wen | 14 | Alibaba | 性能优化 |

---

**最后更新**: 2026-03-20

**Sources**:
- [JEP 254: Compact Strings](https://openjdk.org/jeps/254)
- [JEP 280: Indify String Concatenation](https://openjdk.org/jeps/280)
- [JEP 378: Text Blocks](https://openjdk.org/jeps/378)
- [JEP 430: String Templates](https://openjdk.org/jeps/430)
- [Inside Java: What Happened to String Templates](https://nipafx.dev/inside-java-newscast-71/)
- [Baeldung: String Templates](https://www.baeldung.com/java-21-string-templates)
