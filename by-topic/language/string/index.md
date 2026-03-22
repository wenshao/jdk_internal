# 字符串处理

> Java String 从 JDK 1.0 到 JDK 26 的演进历程

[← 返回语言特性](../)

---

## 1. TL;DR 快速概览

### 核心特性

| 特性 | 版本 | JEP | 内存/性能影响 | 说明 |
|------|------|-----|-------------|------|
| **Compact Strings** | JDK 9 | JEP 254 | 内存 -50% (ASCII) | byte[] + coder 替换 char[] |
| **invokedynamic 拼接** | JDK 9 | JEP 280 | 启动 +10% | invokedynamic 替代 StringBuilder |
| **String Deduplication** | JDK 8u20 | JEP 192 | 内存 -10~40% | GC 自动去重 |
| **Text Blocks** | JDK 15 | JEP 378 | - | 多行字符串 `"""..."""` |
| **隐藏类拼接** | JDK 24 | JDK-8227379 | 启动 +40% | 共享隐藏类减少元空间 |

### 字符串拼接最佳实践

```java
// 简单拼接 — 编译器通过 invokedynamic 优化
String s = "Hello " + name;

// 循环拼接 — 用 StringBuilder
StringBuilder sb = new StringBuilder();
for (String item : list) sb.append(item);

// 格式化
String s = "Hello %s, age %d".formatted("Alice", 25);  // JDK 15+

// 避免: 循环中用 + (每次迭代生成新拼接点)
String s = "";
for (String item : list) { s = s + item; }  // 性能差
```

### 性能提示

| 场景 | 推荐 | 避免 |
|------|------|------|
| 编译时常量拼接 | `+` 操作符 | StringBuilder |
| 循环中拼接 | StringBuilder | `+` 操作符 |
| 大量字符串去重 | `-XX:+UseStringDeduplication` | 手动 intern() |
| 运行时格式化 | `formatted()` / `String.format()` | 手动拼接 |

---

## 2. 快速概览

```
JDK 1.0 ── JDK 5 ── JDK 7u6 ── JDK 9 ── JDK 11 ── JDK 15 ── JDK 21 ── JDK 24 ── JDK 26
   │         │         │          │         │          │          │         │         │
 String   String-   Substring  Compact   repeat()  Text Blocks  String   隐藏类    Shaojin
  诞生    Builder    修复内存   Strings   strip()    (JEP 378)  Templates  拼接优化  Wen 优化
 常量池   (无同步)   泄漏      + indy     isBlank()            (撤回)    (+40%启动) 系列
```

### 核心演进

| 特性 | 版本 | JEP | 说明 |
|------|------|-----|------|
| **String 常量池** | JDK 1.0 | - | 字符串字面量自动 intern |
| **StringBuilder** | JDK 5 | - | 非同步版本, 替代 StringBuffer |
| **Compact Strings** | JDK 9 | JEP 254 | byte[] 存储, ASCII 内存节省 50% |
| **invokedynamic 拼接** | JDK 9 | JEP 280 | 编译时优化, +10% 启动性能 |
| **Text Blocks** | JDK 15 | JEP 378 | 多行字符串 `"""..."""` |
| **String Templates** | JDK 21 | JEP 430 | **已撤回** (JDK 23 移除) |
| **隐藏类拼接** | JDK 24 | JDK-8227379 | +40% 启动性能 |

---

## 目录

- [字符串 API](#3-字符串-api)
- [String 常量池与 intern()](#4-string-常量池与-intern)
- [Compact Strings (JEP 254)](#5-compact-strings-jep-254)
- [String Concatenation (JEP 280)](#6-string-concatenation-jep-280)
- [StringBuilder vs StringBuffer](#7-stringbuilder-vs-stringbuffer)
- [String Deduplication (JEP 192)](#8-string-deduplication-jep-192)
- [Text Blocks (JEP 378)](#9-text-blocks-jep-378)
- [Shaojin Wen 的优化系列](#10-shaojin-wen-的优化系列)
- [版本演进](#11-版本演进)
- [性能优化实战](#12-性能优化实战)
- [VM 参数](#13-vm-参数)
- [内部详情](#14-内部详情)
- [核心贡献者](#15-核心贡献者)
- [相关链接](#16-相关链接)

---

## 3. 字符串 API

### 基础操作

```java
// 创建字符串 (String creation)
String s1 = "Hello";                    // 字符串字面量 (string literal) — 入常量池
String s2 = new String("Hello");        // 新对象 (new object) — 堆上分配
String s3 = String.valueOf(123);         // 从其他类型转换

// 比较 (Comparison)
s1.equals("Hello");                     // 内容相等 (content equality)
s1 == "Hello";                          // 引用相等 (reference equality) — 字面量池中相同
"Hello".equalsIgnoreCase("hello");       // 忽略大小写

// 连接 (Concatenation)
String result = "Hello " + "World";     // 编译器优化为常量
String joined = String.join(", ", "A", "B", "C");  // JDK 8+: "A, B, C"
```

### 空白处理 (Whitespace Handling)

```java
String text = "  Hello World  ";

// JDK 11+ 新方法 — Unicode 感知 (Unicode-aware)
text.strip();                            // "Hello World" — 识别所有 Unicode 空白
text.stripLeading();                     // "Hello World  "
text.stripTrailing();                    // "  Hello World"
text.isBlank();                          // false — 是否为空或仅空白

// 传统方法 — 仅识别 ASCII 空白 (codepoint <= U+0020)
text.trim();                             // "Hello World"

// 区别示例:
String unicode = "\u2000Hello\u2000";    // \u2000 = EN QUAD (Unicode 空白)
unicode.trim();                          // "\u2000Hello\u2000" — trim 不识别
unicode.strip();                         // "Hello" — strip 正确处理
```

### 其他常用方法

```java
// JDK 11+
"abc".repeat(3);                         // "abcabcabc"
"Line1\nLine2".lines();                  // Stream<String>

// JDK 12+
"Line1\nLine2".indent(4);               // 每行增加 4 空格缩进

// JDK 15+
"Hello %s, age %d".formatted("Alice", 25); // "Hello Alice, age 25"

// JDK 8+
"Hello World".chars();                   // IntStream of char values
"Hello World".codePoints();              // IntStream of code points
```

---

## 4. String 常量池与 intern()

### 常量池机制 (String Constant Pool)

```
┌───────────────────────────────────────────────────────────┐
│              String 常量池 (String Constant Pool)          │
├───────────────────────────────────────────────────────────┤
│                                                             │
│  字符串字面量 (String literals):                            │
│  String s1 = "Hello";   // → 常量池                        │
│  String s2 = "Hello";   // → 同一引用, s1 == s2            │
│  String s3 = new String("Hello"); // → 堆上新对象          │
│  s1 == s3;               // false (不同引用)                │
│  s1 == s3.intern();      // true  (intern 返回池中引用)     │
│                                                             │
│  存储位置演进:                                              │
│  JDK 6 及之前: PermGen (永久代) — 容量有限, 容易 OOM       │
│  JDK 7+: Heap (堆) — 可被 GC 回收, 容量更大               │
│                                                             │
│  编译时常量折叠 (Constant Folding):                        │
│  String s = "Hello" + " World";  // 编译期合并为 "Hello World" │
│  // 等价于 String s = "Hello World";                        │
│                                                             │
│  运行时拼接不入池:                                          │
│  String name = getName();                                   │
│  String s = "Hello " + name;  // 运行时计算, 不在常量池    │
│                                                             │
└───────────────────────────────────────────────────────────┘
```

### intern() 方法

```java
// intern() 将字符串放入常量池并返回池中引用
String s1 = new String("hello");       // 堆上对象
String s2 = s1.intern();               // 返回常量池引用
String s3 = "hello";                   // 常量池引用
System.out.println(s2 == s3);          // true

// 何时使用 intern():
// - 大量重复字符串需要节省内存 (如 XML 属性名、JSON key)
// - 需要快速引用比较 (== 代替 equals())

// 何时避免 intern():
// - 大量不重复字符串 (intern 维护哈希表, 有开销)
// - JDK 8u20+ 有 String Deduplication, 通常更好
```

### 常量池调优

```bash
# 常量池哈希表大小 (bucket count)
-XX:StringTableSize=65536        # 默认值因版本不同
# 增大可减少哈希冲突, 加速 intern()
# JDK 7+: 默认 60013
# JDK 11+: 默认 65536

# 查看常量池统计
-XX:+PrintStringTableStatistics  # JVM 退出时输出统计信息
```

---

## 5. Compact Strings (JEP 254)

### 内部表示

JDK 9 将 `String` 的内部存储从 `char[]` 改为 `byte[]` + `coder` 字段:

```java
// JDK 8 及之前:
class String {
    final char[] value;           // 每个字符占 2 字节 (UTF-16)
}

// JDK 9+:
class String {
    final byte[] value;           // 字节数组
    final byte coder;             // 编码标识: 0 = LATIN1, 1 = UTF16

    static final byte LATIN1 = 0; // 单字节编码 (ISO-8859-1), 覆盖 ASCII + 西欧字符
    static final byte UTF16 = 1;  // 双字节编码 (UTF-16)
}
```

### LATIN1 vs UTF16 编码选择

```
┌──────────────────────────────────────────────────────────────┐
│              Compact Strings 编码选择逻辑                    │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  创建字符串时, JVM 检查所有字符:                               │
│                                                                │
│  所有字符 <= 0xFF (Latin-1 范围)?                              │
│    YES → coder = LATIN1, 每字符 1 字节                        │
│    NO  → coder = UTF16,  每字符 2 字节                        │
│                                                                │
│  示例:                                                        │
│  "Hello"    → LATIN1, 5 bytes  (对比 JDK 8: 10 bytes)       │
│  "café"     → LATIN1, 4 bytes  (é = U+00E9 ≤ 0xFF)          │
│  "你好"     → UTF16,  4 bytes  (中文字符 > 0xFF)             │
│  "Hello你好" → UTF16, 14 bytes (混合则全部用 UTF16)          │
│                                                                │
│  内存节省:                                                    │
│  典型英文应用: 约 50% 字符串内存节省                           │
│  中文应用: 无节省 (已经是 UTF16)                               │
│  混合应用: 约 20-40% 节省                                     │
│                                                                │
└──────────────────────────────────────────────────────────────┘
```

### StringLatin1 和 StringUTF16

```java
// 内部实现类 (包级访问, package-private)
// String 方法根据 coder 分发到对应实现:

class StringLatin1 {
    // LATIN1 (单字节) 优化路径
    static int indexOf(byte[] value, int ch) { ... }      // 单字节搜索, 更快
    static boolean equals(byte[] a, byte[] b) { ... }     // 字节比较
    static int compareTo(byte[] a, byte[] b) { ... }
    static String replace(byte[] value, char oldChar, char newChar) { ... }
    static void inflate(byte[] src, char[] dst, int off, int len) { ... } // 扩展到 char[]
}

class StringUTF16 {
    // UTF16 (双字节) 路径
    static int indexOf(byte[] value, int ch) { ... }      // 双字节搜索
    static boolean equals(byte[] a, byte[] b) { ... }
    static int compareTo(byte[] a, byte[] b) { ... }
    static byte[] compress(char[] val, int off, int len) { ... } // 尝试压缩到 LATIN1
    static byte[] toBytes(char[] value, int off, int len) { ... }
}

// 分发示例 (String.indexOf 内部):
public int indexOf(int ch, int fromIndex) {
    return isLatin1()
        ? StringLatin1.indexOf(value, ch, fromIndex)
        : StringUTF16.indexOf(value, ch, fromIndex);
}
```

**启用/禁用**:

```bash
# 启用 Compact Strings (默认开启)
-XX:+CompactStrings

# 禁用 (所有字符串强制 UTF16)
-XX:-CompactStrings
```

---

## 6. String Concatenation (JEP 280)

### invokedynamic 替代 StringBuilder

JDK 9 之前, `+` 拼接编译为 `StringBuilder` 链; JDK 9+ 编译为 `invokedynamic` 调用:

```java
// 源代码
String result = "Hello " + name + "!";

// JDK 8 编译结果 (javac 生成):
String result = new StringBuilder()
    .append("Hello ")
    .append(name)
    .append("!")
    .toString();

// JDK 9+ 编译结果 (javac 生成):
// invokedynamic #0:makeConcatWithConstants:(Ljava/lang/String;)Ljava/lang/String;
//   Bootstrap: StringConcatFactory.makeConcatWithConstants
//   Template:  "Hello \u0001!"     (\u0001 是参数占位符)
```

### 为什么 invokedynamic 更好?

```
┌──────────────────────────────────────────────────────────────┐
│        StringBuilder vs invokedynamic 拼接对比               │
├────────────────────────┬─────────────────────────────────────┤
│ StringBuilder (JDK 8)  │ invokedynamic (JDK 9+)              │
├────────────────────────┼─────────────────────────────────────┤
│ 编译时策略固定          │ 运行时策略可优化                    │
│ 总是创建 StringBuilder  │ JVM 选择最优实现                    │
│ 可能多次扩容 + 复制     │ 预计算总长度, 一次分配             │
│ 字节码体积大            │ 单条 invokedynamic 指令             │
│ 无法利用未来 JVM 优化   │ JVM 升级自动受益                    │
├────────────────────────┼─────────────────────────────────────┤
│ 优点: 简单直接          │ 优点: 更快启动, 更小字节码,        │
│                        │       运行时自适应优化               │
└────────────────────────┴─────────────────────────────────────┘
```

### 策略与配置

```bash
# 调试信息
-Djava.lang.invoke.StringConcat.DEBUG=true

# 缓存阈值 (参数数 >= 此值时跳过缓存)
-Djava.lang.invoke.StringConcat.cacheThreshold=256

# 策略选择 (历史选项, JDK 24+ 部分已移除):
# - BC_SB: 字节码生成 StringBuilder (JDK 8 风格)
# - MH_SB_SIZED: MethodHandle + sized StringBuilder
# - MH_SB_SIZED_EXACT: MethodHandle + exact sized
# - MH_INLINE_SIZED_EXACT: MethodHandle inline (JDK 9 默认)
```

### JDK 24: 隐藏类策略 (Hidden Class Strategy)

```java
// JDK 24 (JDK-8227379): 拼接点共享隐藏类
// 相同"形状"的拼接表达式共享同一个生成的类

// 例如这两个拼接点形状相同 (String + int → String):
String a = "x=" + x;     // 形状: (String, int) → String
String b = "y=" + y;     // 形状: (String, int) → String
// → 共享同一个隐藏类

// 性能提升:
// - 启动性能 +40% (减少类生成)
// - 元空间 (Metaspace) 占用 -60%
```

---

## 7. StringBuilder vs StringBuffer

### 核心区别

| 特性 | StringBuilder (JDK 5+) | StringBuffer (JDK 1.0) |
|------|------------------------|------------------------|
| **线程安全** | 不安全 (not thread-safe) | 安全 (synchronized) |
| **性能** | 更快 (无锁开销) | 较慢 (每次操作加锁) |
| **推荐场景** | 单线程拼接 (绝大多数场景) | 多线程共享 (极少需要) |
| **内部存储** | byte[] (JDK 9+) | byte[] (JDK 9+) |

```java
// StringBuilder — 推荐用法
StringBuilder sb = new StringBuilder(256); // 预分配容量, 避免扩容
sb.append("Hello").append(' ').append("World");
String result = sb.toString();

// StringBuffer — 线程安全但通常不需要
// 如果真需要多线程拼接, 通常有更好的设计:
// 1. 每个线程用自己的 StringBuilder, 最后合并
// 2. 使用 StringJoiner / Collectors.joining()
```

### 扩容机制 (Growth Policy)

```java
// 初始容量: 16 (无参构造) 或 s.length() + 16 (传入字符串)
// 扩容策略: (旧容量 + 1) * 2
// 例如: 16 → 34 → 70 → 142 → ...

// 最佳实践: 如果能预估大小, 提供初始容量
StringBuilder sb = new StringBuilder(estimatedSize);

// 避免: 默认容量 + 大量 append → 多次扩容 + 数组复制
```

### StringBuilder 批量复制优化 (JDK 内部)

JDK 内部对 `StringBuilder.append(char[])` 等方法做了批量复制优化:

```java
// JDK-8355177 (JDK 25): StringBuilder.append(char[]) 批量复制
// 优化前: 逐个字符处理
for (int i = 0; i < len; i++) {
    append(str[i]);  // 每次调用有方法开销
}

// 优化后: 批量复制 (MergeStore pattern)
if (isLatin1()) {
    // 尝试 compress: 如果所有 char 都 <= 0xFF, 直接压缩为 LATIN1
    // 否则 inflate 整个 StringBuilder 到 UTF16, 再批量复制
    StringLatin1.getChars(str, 0, len, value, count);
} else {
    StringUTF16.getChars(str, 0, len, value, count);
}
// 性能提升: +15-40% 吞吐量
```

---

## 8. String Deduplication (JEP 192)

### 工作原理

```
┌─────────────────────────────────────────────────────────────┐
│              String Deduplication 工作原理                   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  触发条件:                                                    │
│  1. 使用支持的 GC (G1, ZGC, Shenandoah)                      │
│  2. 启用 -XX:+UseStringDeduplication                         │
│  3. String 对象存活超过 age 阈值 (默认 3 次 GC)              │
│                                                               │
│  过程:                                                        │
│  1. GC 标记存活的 String 对象                                 │
│  2. 对存活且达到年龄的 String, 计算 value[] 的哈希值          │
│  3. 在全局哈希表中查找相同内容的 byte[]                       │
│  4. 如果找到 → 将当前 String 的 value 引用指向已有的 byte[]  │
│  5. 原 byte[] 变为无引用, 下次 GC 回收                       │
│                                                               │
│  注意:                                                        │
│  - 去重的是底层 byte[] 数组, 不是 String 对象本身             │
│  - String 对象的引用 (==) 不会改变, 只是内部 value 共享       │
│  - 不影响 equals() 行为                                       │
│                                                               │
│  开销:                                                        │
│  - GC 停顿时间略微增加 (需要计算哈希、查表)                   │
│  - 维护全局哈希表消耗少量内存                                 │
│  - CPU 开销: 在 GC 线程中执行, 对应用线程影响小               │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### 配置与监控

```bash
# 启用 (需要 G1/ZGC/Shenandoah)
-XX:+UseStringDeduplication

# 年龄阈值 (String 存活多少次 GC 后才去重)
-XX:StringDeduplicationAgeThreshold=3  # 默认 3

# 统计信息 (JDK 11 之前)
-XX:+PrintStringDeduplicationStatistics

# JDK 11+ 使用 JFR (Java Flight Recorder) 监控
# 事件: jdk.StringDeduplication
```

### intern() vs Deduplication 对比

| 特性 | intern() | String Deduplication |
|------|----------|---------------------|
| **触发方式** | 应用代码显式调用 | GC 自动执行 |
| **去重粒度** | String 对象引用 (同一引用) | byte[] 数组 (内容共享) |
| **使用 `==` 比较** | 可以 (同一对象) | 不可以 (不同对象) |
| **适用 GC** | 所有 GC | G1, ZGC, Shenandoah |
| **性能开销** | 哈希表查找 (应用线程) | GC 暂停中处理 (GC 线程) |
| **适用场景** | 已知重复的少量字符串 | 大量未知重复字符串 |

---

## 9. Text Blocks (JEP 378)

### 基础语法

```java
// JDK 15 正式特性 (JDK 13 预览, JDK 14 第二预览)
// 使用三引号 (triple quotes) 包围多行字符串

String json = """
    {
        "name": "John",
        "age": 30,
        "address": {
            "city": "Beijing"
        }
    }
    """;
// 注意: 开头 """ 后必须换行
// 结尾 """ 的位置决定缩进基准
```

### stripIndent 算法 (Incidental Whitespace Removal)

```
┌──────────────────────────────────────────────────────────────┐
│              Text Block stripIndent 算法                     │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  1. 将文本按行分割                                             │
│  2. 忽略全空白行 (blank lines)                                 │
│  3. 找出所有非空行的最小前导空白数 (common leading whitespace) │
│  4. 从每行开头移除该数量的空白                                 │
│  5. 移除末尾空白                                               │
│                                                                │
│  示例:                                                        │
│  String s = """                                                │
│  ····{                      ← 4 空格前导                       │
│  ········"name": "John"     ← 8 空格前导                       │
│  ····}                      ← 4 空格前导                       │
│  ····""";                   ← 结尾 """ 有 4 空格               │
│                                                                │
│  最小前导空白 = 4                                              │
│  结果:                                                        │
│  {                                                             │
│      "name": "John"                                            │
│  }                                                             │
│                                                                │
│  结尾 """ 控制缩进:                                           │
│  String s1 = """                                               │
│      Hello                                                     │
│      """;           → "Hello\n"      (""" 对齐, 无缩进)       │
│                                                                │
│  String s2 = """                                               │
│      Hello                                                     │
│  """;               → "    Hello\n"  (""" 靠左, 保留缩进)     │
│                                                                │
└──────────────────────────────────────────────────────────────┘
```

### 转义序列 (Escape Sequences)

```java
// Text Block 专用转义序列 (JDK 14+):

// \s — 空格 (保留尾随空白, 防止被 stripIndent 移除)
String s = """
    item1  \s
    item2  \s
    """;
// 每行末尾保留 3 个空格 (2 原始 + 1 \s)

// \ (行尾反斜杠) — 续行符, 不产生换行
String longLine = """
    This is a very long line that \
    we want to keep as a single line \
    in the resulting string.""";
// 结果: "This is a very long line that we want to keep as a single line in the resulting string."

// 传统转义在 Text Block 中同样有效:
// \n \t \r \\ \" \uXXXX
String s = """
    Line1\tTabbed
    Line2\nExtra line
    Quotes: \"""
    """;
```

### Text Block 实战模式

```java
// SQL
String sql = """
    SELECT u.name, u.email
    FROM users u
    WHERE u.active = true
      AND u.created_at > ?
    ORDER BY u.name
    """;

// HTML
String html = """
    <html>
        <body>
            <h1>%s</h1>
            <p>%s</p>
        </body>
    </html>
    """.formatted(title, content);

// 正则表达式 (避免双重转义)
String regex = """
    \\d{4}-\\d{2}-\\d{2}""";  // 日期模式
// 注意: Text Block 不是 raw string, \\ 仍需转义
```

---

## 10. Shaojin Wen 的优化系列

[Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) (Alibaba) 为 JDK 25/26 贡献了多项字符串相关性能优化:

### Integer/Long.toString 优化

```java
// JDK-8370503: Integer.toString LATIN1 快速路径
// PR: https://github.com/openjdk/jdk/pull/23638

// 优化前: toString 统一走 getChars() → 复杂的除法/取模循环
// 优化后: LATIN1 编码路径直接写 byte[], 避免 char[] → byte[] 转换

// 性能提升:
// Integer.toString(): +10-20%
// Long.toString(): +10-15%
```

### UUID.toString 优化

```java
// JDK-8353741: UUID.toString() 从查表法到位运算
// PR: https://github.com/openjdk/jdk/pull/24625

// 优化前: 使用查表法 (lookup table) 将每个 nibble 转为 hex 字符
// 优化后: 使用位运算 (bit manipulation) 批量转换

// 核心思路:
// 1. 将 4-bit nibble 扩展为 8-bit
// 2. 加上 '0' 基准值
// 3. 对 > 9 的值加上 'a' - '0' - 10 的偏移

// 性能提升: ~30% (避免数组边界检查和缓存未命中)
```

### parseInt/parseLong 优化

```java
// JDK-8340552: Integer.parseInt/Long.parseLong 快速路径

// 优化: 对常见的短数字字符串 (1-9 位) 提供优化的解析路径
// 避免通用循环中的乘法溢出检查

// 性能提升:
// 1-2 位数字: +20-30%
// 3-9 位数字: +10-15%
```

### DateTimeFormatter 优化

```java
// JDK-8348545: DateTimeFormatter 字符串构建优化
// PR: https://github.com/openjdk/jdk/pull/23535

// 优化: 在格式化日期/时间时, 避免不必要的 StringBuilder 操作
// 直接将数字写入目标 byte[]

// 性能提升: ISO_LOCAL_DATE_TIME 格式化 +15-25%
```

### 优化方法论

Shaojin Wen 系列优化的共同特点:

| 技术 | 说明 | 典型收益 |
|------|------|---------|
| **LATIN1 快速路径** | 对纯 ASCII 结果直接操作 byte[] | 减少编码转换开销 |
| **位运算替代查表** | 用算术运算替代数组查找 | 避免缓存未命中 |
| **批量操作** | 一次处理多个字节/字符 | 减少循环迭代 |
| **消除中间分配** | 避免临时 char[]/String 对象 | 减少 GC 压力 |

---

## 11. 版本演进

### JDK 1.0 - String 诞生

```java
// 基础功能: 不可变字符串 (immutable)
String s = "Hello";
s.length();
s.charAt(0);
s.substring(1, 3);

// StringBuffer: 同步的可变字符串
StringBuffer sb = new StringBuffer("Hello");
sb.append(" World");
```

### JDK 5 - StringBuilder

```java
// StringBuilder: 非同步版本, 性能更好
// 绝大多数场景应替代 StringBuffer
StringBuilder sb = new StringBuilder();
sb.append("Hello").append(" World");
```

### JDK 7u6 - substring 修复

```java
// JDK 7u6 之前: substring 共享原 char[] (可能导致内存泄漏)
String large = readLargeFile();          // 10MB 字符串
String small = large.substring(0, 10);   // small 持有 10MB char[] 的引用!
large = null;                            // 10MB 无法回收

// JDK 7u6 之后: substring 复制新 char[]
String small = large.substring(0, 10);   // 新的 char[], 仅 10 字符
// large 可被正常 GC
```

### JDK 11 - 新方法

```java
"  text  ".strip();          // "text"
"  text  ".stripLeading();   // "text  "
"  text  ".stripTrailing();  // "  text"
"".isBlank();                // true
"abc".repeat(3);             // "abcabcabc"
"Line1\nLine2".lines();      // Stream<String>
```

### JDK 21 - String Templates (已撤回)

```java
// JEP 430: 在 JDK 21 预览, JDK 22 第二预览, JDK 23 移除
// 原计划语法:
String name = "World";
String message = STR."Hello \{name}!";

// 撤回原因:
// - STR 处理器的类型安全设计争议
// - 模板表达式的语义讨论未达成共识
// - 社区反馈需要更多考虑
// - 没有确定何时会重新引入
```

---

## 12. 性能优化实战

### StringConcatHelper 优化 (JDK-8336831)

```java
// PR: https://github.com/openjdk/jdk/pull/20253
// 性能提升: +10-15%

// 优化前: 使用复杂的 mix/prepend 机制 (反向填充)
long indexCoder = mix(initialCoder(), s1);
indexCoder = mix(indexCoder, s2);
byte[] buf = newArray(indexCoder);
indexCoder = prepend(indexCoder, buf, s2, s1);

// 优化后: 使用直接的正向复制 (forward copy)
byte coder = (byte) (s1.coder() | s2.coder());
byte[] buf = newArray(s1.length() + s2.length() << coder);
s1.getBytes(buf, 0, coder);         // 正向复制
s2.getBytes(buf, s1.length(), coder);
```

### Unsafe 优化陷阱与回退 (JDK-8343925)

```java
// PR: https://github.com/openjdk/jdk/pull/22012
// 回退 JDK-8342650 的优化 (JVM 崩溃修复)

// 问题: ByteArrayLittleEndian.setInt() 地址溢出
int charPos = spaceNeeded;  // 接近 Integer.MAX_VALUE
ByteArrayLittleEndian.setInt(buf, charPos << 1, inflated);
//                                ^^^^^^^^^^^
//                    charPos << 1 溢出 → 负数 → 非法内存访问 → JVM 崩溃

// 教训:
// 1. Unsafe 操作需要充分测试边界条件
// 2. 整数溢出在位移运算中特别危险
// 3. 快速回退比带病上线更重要
```

### Lambda 生成优化 (JDK-8341755)

```java
// PR: https://github.com/openjdk/jdk/pull/21399
// InnerClassLambdaMetafactory: 缓存参数名称字符串

// 优化前: 每次创建 Lambda 都生成新字符串
String[] argNames = new String[parameterCount];
for (int i = 0; i < parameterCount; i++) {
    argNames[i] = "arg$" + (i + 1);  // 每次分配新 String
}

// 优化后: 预缓存前 8 个参数名
private static final @Stable String[] ARG_NAME_CACHE = {
    "arg$1", "arg$2", "arg$3", "arg$4",
    "arg$5", "arg$6", "arg$7", "arg$8"
};

// 性能: 0参数 Lambda +20%, 1参数 +17%
```

---

## 13. VM 参数

### Compact Strings

```bash
-XX:+CompactStrings              # 启用 (默认)
-XX:-CompactStrings              # 禁用 (强制 UTF16)
```

### String Deduplication

```bash
-XX:+UseStringDeduplication      # 启用去重 (需要 G1/ZGC/Shenandoah)
-XX:StringDeduplicationAgeThreshold=3  # 年龄阈值 (默认 3)
```

### String Constant Pool

```bash
-XX:StringTableSize=65536        # 常量池哈希表大小
-XX:+PrintStringTableStatistics  # 打印统计信息
```

### String Concatenation

```bash
-Djava.lang.invoke.StringConcat.DEBUG=true          # 调试信息
-Djava.lang.invoke.StringConcat.cacheThreshold=256  # 缓存阈值
```

---

## 14. 内部详情

### 源码结构

```
src/java.base/share/classes/java/lang/
├── String.java              # 主类 (~3500 行)
├── StringConcatHelper.java  # 拼接辅助 (JDK 9+)
├── StringBuilder.java       # 可变字符串 (非同步)
├── StringBuffer.java        # 可变字符串 (同步)
├── StringLatin1.java        # LATIN1 编码操作
├── StringUTF16.java         # UTF16 编码操作
└── AbstractStringBuilder.java # StringBuilder/Buffer 公共基类

src/java.base/share/classes/java/lang/invoke/
└── StringConcatFactory.java # invokedynamic 拼接工厂

src/hotspot/share/oops/
├── instanceKlass.cpp        # String 类元数据
└── stringTable.cpp          # String 常量池实现 (C++)

src/hotspot/share/gc/
├── stringdedup/             # String 去重实现
│   ├── stringDedup.cpp      # 去重入口
│   └── stringDedupTable.cpp # 去重哈希表
└── g1/g1StringDedup.cpp     # G1 GC 去重集成
```

### 关键内部类

| 类 | 作用 | 所在包 |
|---|------|--------|
| `StringLatin1` | LATIN1 编码操作 (单字节优化路径) | `java.lang` |
| `StringUTF16` | UTF16 编码操作 (双字节路径) | `java.lang` |
| `StringConcatHelper` | 拼接 helper 方法 | `java.lang` |
| `StringConcatFactory` | invokedynamic 工厂 | `java.lang.invoke` |
| `AbstractStringBuilder` | StringBuilder/Buffer 共享实现 | `java.lang` |

### 关键 JDK Bug IDs

| Bug ID | 描述 | 修复版本 |
|--------|------|----------|
| JDK-8054307 | substring 内存泄漏修复 | JDK 7u6 |
| JDK-8077559 | Compact Strings 实现 | JDK 9 |
| JDK-8227379 | StringConcat 隐藏类策略 | JDK 24 |
| JDK-8336831 | StringConcatHelper 正向复制优化 | JDK 24 |
| JDK-8355177 | StringBuilder.append(char[]) 批量优化 | JDK 25 |
| JDK-8370503 | Integer.toString LATIN1 路径 | JDK 26 |
| JDK-8353741 | UUID.toString 位运算优化 | JDK 26 |

---

## 15. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### String 处理 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Claes Redestad | 101 | Oracle | Compact Strings, 启动优化, StringConcat |
| 2 | Mandy Chung | 54 | Oracle | String 内部实现 |
| 3 | Chen Liang | 35 | Oracle | invokedynamic, ClassFile |
| 4 | Jim Laskey | 29 | Oracle | String Templates (JEP 430), Text Blocks |
| 5 | Joe Darcy | 20 | Oracle | Text Blocks (JEP 378) |
| 6 | Jorn Vernee | 19 | Oracle | Foreign Memory, 拼接优化 |
| 7 | Paul Sandoz | 17 | Oracle | 字符串格式化 |
| 8 | Pavel Rappo | 15 | Oracle | 文档, 工具 |
| 9 | Maurizio Cimadamore | 15 | Oracle | javac, 模板 |
| 10 | [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) | 14 | [Alibaba](/contributors/orgs/alibaba.md) | toString/parseInt/UUID 性能优化 |

---

## 16. 相关链接

### 本地文档

- [时间线](timeline.md) - 完整版本演进历史
- [内部实现](implementation.md) - Compact Strings、StringLatin1、StringUTF16
- [性能优化](optimization.md) - String Deduplication、VM 调优参数
- [UUID.toString() 优化](uuid-toString-optimization.md) - 从查表法到位运算 (JDK-8353741)

### 相关主题

- [日期时间 API](../../api/datetime/) - DateTimeHelper 字符串格式化
- [集合框架](../../api/collections/) - StringBuilder 与集合
- [性能优化](../../core/performance/) - 字符串性能基准
- [内存管理](../../core/memory/) - String Deduplication
- [语法演进](../syntax/) - 语言特性

### 外部参考

#### 本地 JEP 文档

| JEP | 标题 | 版本 |
|-----|------|------|
| [JEP 192](/jeps/language/jep-192.md) | String Deduplication in G1 | JDK 8u20 |
| [JEP 254](/jeps/language/jep-254.md) | Compact Strings | JDK 9 |
| [JEP 280](/jeps/language/jep-280.md) | Indify String Concatenation | JDK 9 |
| [JEP 378](/jeps/language/jep-378.md) | Text Blocks | JDK 15 |
| [JEP 430](/jeps/language/jep-430.md) | String Templates (Preview) | 已撤回 |

#### 外部链接

- [OpenJDK String 源码](https://github.com/openjdk/jdk/blob/master/src/java.base/share/classes/java/lang/String.java)
- [Inside Java Newscast #71](https://nipafx.dev/inside-java-newscast-71/) - String Templates 撤回说明

---

**最后更新**: 2026-03-22

**Sources**:
- [JEP 192](/jeps/language/jep-192.md)
- [JEP 254](/jeps/language/jep-254.md)
- [JEP 280](/jeps/language/jep-280.md)
- [JEP 378](/jeps/language/jep-378.md)
- [JEP 430](/jeps/language/jep-430.md)
