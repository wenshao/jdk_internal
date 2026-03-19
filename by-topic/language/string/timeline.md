# 字符串处理演进时间线

> Java String 从 JDK 1.0 到 JDK 26 的完整演进历程，包括内部实现、优化过程和贡献者分析

---

## 时间线概览

```
JDK 1.0 ──── JDK 5 ──── JDK 6 ──── JDK 7 ──── JDK 8 ──── JDK 9 ──── JDK 11 ──── JDK 15 ──── JDK 17 ──── JDK 21 ──── JDK 24 ──── JDK 25 ──── JDK 26
   │           │           │           │           │           │           │           │           │           │           │           │
 String     StringBuilder  Substring  invokedynamic StringJoiner Compact   repeat()   Text Blocks  transform()  String     Hidden     String     Integer/
 immutable   无同步        优化        Lambda      (JEP 254)   strip()    (JEP 378)  (JDK 12)    Templates  Class      Templates  Long
 常量池      (JDK 5)       (7u6)       链接                                  dedup                                        Strategy   (Final)    toString
                                                                                                                                                  (+40%启动)              优化
```

---

## 核心演进：存储优化

### Compact Strings (JEP 254) - JDK 9

#### 问题背景

JDK 8 及之前，String 使用 `char[]` 存储，每个字符占 2 字节 (UTF-16 BE)。对于纯 ASCII/Latin-1 文本，这造成了 50% 的内存浪费。

```java
// JDK 8 及之前
public final class String {
    private final char[] value;  // 每字符 2 字节
    private final int offset;    // 子字符串偏移 (JDK 7u6 后移除)
    private final int count;     // 字符数量 (JDK 7u6 后改用 value.length)
    private int hash;            // 延迟计算的哈希
}

// "Hello" 内存布局:
// - char[]: [H][e][l][l][o] = 10 字节
// - 对象头: 12 字节 (64-bit JVM, compressed oops)
// - 总计: 22 字节
```

#### 解决方案

改用 `byte[]` + `coder` 标志，动态选择编码：

```java
// JDK 9+ Compact Strings
public final class String implements Serializable, Comparable<String>, CharSequence {
    @Stable
    private final byte[] value;      // 实际字符存储

    private final byte coder;        // 编码标识: 0 = LATIN1, 1 = UTF16

    private int hash;                // 哈希缓存 (延迟计算)

    // 编码常量
    static final byte LATIN1 = 0;
    static final byte UTF16  = 1;

    // 可通过 VM 参数禁用
    static final boolean COMPACT_STRINGS;
    static {
        // 读取 VM 参数: -XX:-CompactStrings
        COMPACT_STRINGS = true;
    }
}
```

#### 内存影响

| 字符串类型 | JDK 8 char[] | JDK 9+ byte[] | 节省 |
|-----------|--------------|---------------|------|
| 纯 ASCII "Hello" | 10 字节 | 5 字节 | **50%** |
| Latin-1 "Café" | 8 字节 | 4 字节 | **50%** |
| 中文 "你好" | 4 字节 | 4 字节 | 0% |
| 混合 "Hi你好" | 10 字节 | 10 字节 | 0% |
| JSON 典型 | ~40% 节省 | - | **显著** |

#### 源码分析

**长度计算**：
```java
// String.java
public int length() {
    // LATIN1: value.length
    // UTF16: value.length / 2
    return value.length >> coder;
}

// 获取 code point (避免符号扩展)
public int codePointAt(int index) {
    if ((index < 0) || (index >= value.length)) {
        throw new StringIndexOutOfBoundsException(index);
    }
    return isLatin1() ? value[index] & 0xff : getUTF16CodePoint(index);
}
```

**编码检测**：
```java
// StringLatin1.java - LATIN1 编码操作
public static boolean canEncode(char c) {
    return c <= 0xFF;  // 只有前 256 个字符可用 LATIN1
}

// StringUTF16.java - UTF16 编码操作
public static byte[] toBytes(char[] value, int off, int len) {
    byte[] val = new byte[len << 1];  // 每字符 2 字节
    for (int i = 0; i < len; i++) {
        putChar(val, i, value[off++]);
    }
    return val;
}

@ForceInline
static void putChar(byte[] val, int index, int c) {
    index <<= 1;
    val[index]     = (byte)(c >> 8);  // 高字节
    val[index + 1] = (byte)c;         // 低字节
}
```

**构造器**：
```java
// String.java - 从 char[] 构造
public String(char[] value) {
    this(value, 0, value.length, null);
}

String(char[] value, int off, int len, Void sig) {
    if (len == 0) {
        this.value = EMPTY_VALUE;
        this.coder = LATIN1;  // 空字符串用 LATIN1
        return;
    }

    // 检测是否可以用 LATIN1 编码
    if (COMPACT_STRINGS) {
        byte[] val = StringUTF16.compress(value, off, len);
        if (val != null) {
            this.value = val;
            this.coder = LATIN1;
            return;
        }
    }

    // 使用 UTF16
    this.coder = UTF16;
    this.value = StringUTF16.toBytes(value, off, len);
}
```

**压缩检测**：
```java
// StringUTF16.java
public static byte[] compress(char[] val, int off, int len) {
    byte[] ret = new byte[len];
    for (int i = 0; i < len; i++) {
        char c = val[off++];
        if (c > 0xFF) {
            return null;  // 无法压缩，需要 UTF16
        }
        ret[i] = (byte)c;
    }
    return ret;
}
```

#### VM 参数

```bash
# 启用 Compact Strings (默认)
-XX:+CompactStrings

# 禁用 Compact Strings
-XX:-CompactStrings

# 禁用后所有字符串都用 UTF16，可能增加内存但避免编码转换开销
```

#### 性能权衡

| 场景 | LATIN1 | UTF16 | 权衡 |
|------|--------|-------|------|
| 内存占用 | 少 50% | 基准 | LATIN1 胜 |
| 访问速度 | 快 | 需要位移 | LATIN1 略胜 |
| 编码转换 | 无需转换 | 无需转换 | - |
| 混合场景 | 需要 recoder | 无需转换 | UTF16 胜 |

---

## 时间线详情

### JDK 1.0 (1996) - String 诞生

#### 设计决策

```java
// JDK 1.0 String 设计
public final class String {
    private char[] value;      // UTF-16 存储
    private int offset;        // 子字符串偏移
    private int count;         // 字符数量
    private int hash;          // 延迟计算

    // 不可变设计
    public final class String {
        // 所有字段都是 final (除 hash 延迟计算)
        // 所有修改方法都返回新 String
    }

    // 字符串常量池
    // - 编译期字面量进入常量池
    // - intern() 方法运行时加入常量池
}
```

#### substring() 内存泄漏问题

```java
// JDK 1.0 - JDK 6u31
public String substring(int beginIndex, int endIndex) {
    // 共享原 char[]，只改变 offset 和 count
    return new String(offset + beginIndex, endIndex - beginIndex, value);
}

// 问题：大字符串的小子串会持有整个原 char[]
String big = new String(new char[1000000]);  // 2MB
String small = big.substring(0, 1);           // 持有 2MB!
big = null;  // big 仍不会被 GC，因为 small 引用其 value[]
```

### JDK 5 (2004) - StringBuilder

#### 背景

JDK 1.0 引入的 `StringBuffer` 是同步的，但大多数字符串拼接是单线程操作，synchronized 开销不必要。

#### 实现

```java
// StringBuffer (同步，JDK 1.0)
public final class StringBuffer extends AbstractStringBuilder
    implements java.io.Serializable, CharSequence {

    @Override
    public synchronized StringBuffer append(String str) {
        super.append(str);
        return this;
    }

    // 所有方法都 synchronized
}

// StringBuilder (非同步，JDK 5+)
public final class StringBuilder extends AbstractStringBuilder
    implements java.io.Serializable, CharSequence {

    @Override
    public StringBuilder append(String str) {
        super.append(str);
        return this;
    }

    // 无 synchronized
}
```

#### 性能对比

| 操作 | StringBuffer | StringBuilder | 提升 |
|------|-------------|----------------|------|
| 单线程拼接 | 1000 ms | 350 ms | **2.8x** |
| 多线程拼接 | 1000 ms | 不安全 | - |

### JDK 6u32 (2012) - substring() 修复

#### 问题解决

```java
// JDK 6u32+ substring() 不再共享数组
public String substring(int beginIndex, int endIndex) {
    // 复制数组，不再共享
    return new String(value, beginIndex, endIndex - beginIndex);
}

// 内存影响：
// - 之前：小 substring 会导致大数组无法 GC
// - 之后：substring 独立拥有自己的数组，内存可正确释放
```

### JDK 7 (2011) - invokedynamic 字符串拼接

#### 背景

JDK 7 引入 `invokedynamic` (JSR 292)，为动态语言提供支持。JDK 9 利用它优化字符串拼接。

#### 演进

```java
// JDK 8: 字节码
// "a" + b + "c" 编译为:
   new java/lang/StringBuilder
   dup
   invokespecial java/lang/StringBuilder.<init>()V
   ldc "a"
   invokevirtual java/lang/StringBuilder.append(Ljava/lang/String;)Ljava/lang/StringBuilder;
   aload_1  // b
   invokevirtual java/lang/StringBuilder.append(Ljava/lang/String;)Ljava/lang/StringBuilder;
   ldc "c"
   invokevirtual java/lang/StringBuilder.append(Ljava/lang/String;)Ljava/lang/StringBuilder;
   invokevirtual java/lang/StringBuilder.toString()Ljava/lang/String;

// JDK 9+: invokedynamic
// "a" + b + "c" 编译为:
   invokedynamic makeConcatWithConstants(Ljava/lang/String;)Ljava/lang/String;
      // BootstrapMethods:
      // 0: #REF_invokeStatic java/lang/invoke/StringConcatFactory.makeConcatWithConstants
```

#### StringConcatFactory

```java
// StringConcatFactory.java
public static CallSite makeConcatWithConstants(
    MethodLookup lookup,
    String name,
    MethodType concatType,
    String recipe,
    Object... constants
) {
    // 根据参数类型选择最优策略
    // - 简单拼接: 直接 new String
    // - 少量参数: 使用 StringBuilder
    // - 大量参数: 使用私有拼接类

    StringStrategy strategy = getStringStrategy(concatType);
    return strategy.generate(concatType, recipe, constants);
}
```

### JDK 8 (2014) - StringJoiner

#### 设计

```java
// StringJoiner.java
public final class StringJoiner {
    private final String prefix;      // 前缀
    private final String delimiter;   // 分隔符
    private final String suffix;      // 后缀
    private String[] emptyValue;      // 空值

    private StringBuilder value;      // 存储当前值

    public StringJoiner(CharSequence delimiter,
                         CharSequence prefix,
                         CharSequence suffix) {
        this.prefix = prefix.toString();
        this.delimiter = delimiter.toString();
        this.suffix = suffix.toString();
    }

    public StringJoiner add(CharSequence newElement) {
        prepareBuilder().append(newElement);
        return this;
    }
}
```

### JDK 9 (2017) - Compact Strings (JEP 254)

#### 贡献者

| 贡献者 | 公司 | 角色 |
|--------|------|------|
| Vladimir Kozlov | Oracle | 架构设计 |
| Aleksey Shipilev | Oracle | 实现与测试 |
| Claes Redestad | Oracle | 性能优化 |

#### 实现细节

**coder 传播**：
```java
// 拼接时 coder 传播规则
// LATIN1 + LATIN1 = LATIN1
// LATIN1 + UTF16  = UTF16
// UTF16  + UTF16  = UTF16

// StringConcatHelper.java
static String concat(String first, String second, String third) {
    byte coder = first.coder | second.coder | third.coder;
    if (coder == 0) {
        // 全 LATIN1
        byte[] buf = new byte[first.len + second.len + third.len];
        // 复制到 buf
        return new String(buf, LATIN1);
    }
    // 需要 UTF16
    // ...
}
```

### JDK 11 (2018) - 新增方法

#### repeat() 实现

```java
// String.java
public String repeat(int count) {
    if (count < 0) {
        throw new IllegalArgumentException("count is negative: " + count);
    }
    if (count == 0 || value.length == 0) {
        return EMPTY;
    }
    if (count == 1) {
        return this;
    }

    // 计算最终长度
    final int len = value.length;
    final long longLen = (long)len * (long)count;
    if (longLen != (int)longLen) {
        throw new OutOfMemoryError("Repeating string overflows");
    }

    // 使用 Arrays.copyOf 或 System.arraycopy 复制
    byte[] result = StringConcatHelper.newArray(len * count);
    if (coder == LATIN1) {
        for (int i = 0; i < count; i++) {
            System.arraycopy(value, 0, result, i * len, len);
        }
    } else {
        for (int i = 0; i < count; i++) {
            System.arraycopy(value, 0, result, i * len * 2, len * 2);
        }
    }
    return new String(result, coder);
}
```

#### strip() vs trim()

```java
// strip() - Unicode 感知
public String strip() {
    int left = 0;
    int right = length();
    while (left < right) {
        int codePoint = codePointAt(left);
        if (!Character.isWhitespace(codePoint)) {
            break;
        }
        left += Character.charCount(codePoint);
    }
    while (left < right) {
        int codePoint = codePointBefore(right);
        if (!Character.isWhitespace(codePoint)) {
            break;
        }
        right -= Character.charCount(codePoint);
    }
    return substring(left, right);
}

// trim() - 仅 ASCII (<= ' ')
public String trim() {
    int len = value.length;
    int st = 0;
    while ((st < len) && ((value[st] & 0xff) <= ' ')) {
        st++;
    }
    while ((st < len) && ((value[len - 1] & 0xff) <= ' ')) {
        len--;
    }
    return ((st > 0) || (len < value.length)) ? substring(st, len) : this;
}
```

### JDK 15 (2020) - Text Blocks (JEP 378)

#### 贡献者

| 贡献者 | 公司 | 角色 |
|--------|------|------|
| Jim Laskey | Oracle | JEP 作者 |
| Brian Goetz | Oracle | 架构指导 |

#### 实现细节

```java
// 编译时处理
// 源代码:
String html = """
              <html>
                  <body>Hello</body>
              </html>
              """;

// 编译器转换为:
String html = "<html>\n    <body>Hello</body>\n</html>\n";

// 处理步骤:
// 1. 去除换行符前的空白
// 2. 去除每行末尾的空白
// 3. 添加换行符
// 4. 调用 stripIndent() 和 translateEscapes()
```

### JDK 21 (2023) - String Templates (JEP 430)

#### 贡献者

| 贡献者 | 公司 | 角色 |
|--------|------|------|
| Gavin Bierman | Oracle | JEP 领导 |
| Jim Laskey | Oracle | 实现 |

#### 模板表达式

```java
// STR 模板处理器
StringTemplate.Processor<String, RuntimeException> STR = ...;

// 模板表达式语法
StringTemplate message = STR."Hello \{name}, you have \{count} messages.";

// 编译为:
// 1. 创建 StringTemplate 对象
// 2. 传递给 STR 处理器
// 3. 处理器生成结果

// StringTemplate 接口
public interface StringTemplate {
    List<Object> fragments();  // "Hello ", ", you have ", " messages."
    List<Object> values();     // [name, count]
    String interpolate();       // 默认插值
    ProcessKind processKind();  // STR, FMT, RAW
}
```

### JDK 24 (2025) - 隐藏类拼接策略

#### 贡献者

| 贡献者 | GitHub | 贡献 |
|--------|--------|------|
| Shaojin Wen | @shaojin-wen | JDK-8336856 |
| Claes Redestad | @cl4es | 性能分析 |

#### 实现细节

**问题**：JDK 9-23 每个字符串拼接点生成一个独立的隐藏类

```java
// 之前策略
class StringConcat1 { String concat(String a, String b) { ... } }
class StringConcat2 { String concat(String a, String b, String c) { ... } }
class StringConcat3 { String concat(String a, int b) { ... } }
// ... 每个调用点 = 一个类
```

**新策略**：按"形状"(shape) 共享类

```java
// 按参数类型和常量分组
// "a" + b + "c"  → Concat1StringConstConst  (shape: String, String, String)
//  x + y + z      → Concat3String          (shape: String, String, String)
//  x + 42         → Concat1StringInt       (shape: String, int)

// 大幅减少类数量
// 之前: 1000 个拼接点 → 1000 个类
// 之后: 1000 个拼接点 → ~20 个类
```

**性能提升**：
- 启动性能: **+40%**
- 类加载时间: **-50%**
- 元空间占用: **-60%**

### JDK 25 (2025) - StringBuilder 优化

#### 贡献者

| 贡献者 | GitHub | 贡献 |
|--------|--------|------|
| Shaojin Wen | @shaojin-wen | JDK-8355177 |

#### 实现细节

```java
// StringBuilder.append(char[]) 优化
// 之前:
public StringBuilder append(char[] str) {
    int len = str.length;
    ensureCapacityInternal(count + len);
    System.arraycopy(str, 0, value, count, len);  // Java 数组复制
    count += len;
    return this;
}

// 优化后:
public StringBuilder append(char[] str) {
    int len = str.length;
    ensureCapacityInternal(count + len);
    // 使用 Unsafe.copyMemory，更快
    UNSAFE.copyMemory(str,
        CHAR_ARRAY_BASE_OFFSET,
        value,
        BYTE_ARRAY_BASE_OFFSET + (count << 1),  // byte[] 偏移
        len << 1);  // char = 2 bytes
    count += len;
    return this;
}
```

### JDK 26 (2026) - toString 优化

#### 贡献者

| 贡献者 | GitHub | 贡献 |
|--------|--------|------|
| Shaojin Wen | @shaojin-wen | JDK-8370503 |

#### Integer.toString 优化

```java
// Integer.java
static String toString(int x) {
    // 数字总是 LATIN1，使用专用路径
    byte[] bytes = new byte[11];  // 最大 11 位 (含符号)
    int charPos = Integer.getChars(x, 10, bytes);

    // 使用新 API 直接创建 LATIN1 String
    return String.newStringWithLatin1Bytes(bytes, charPos, 11 - charPos);
}

// String.java - 新增包私有构造器
static String newStringWithLatin1Bytes(byte[] bytes, int offset, int length) {
    // 直接使用传入的 byte[]，避免复制
    return new String(bytes, LATIN1, offset, length, true);  // share = true
}
```

---

## 源码结构

### 核心文件

```
src/java.base/share/classes/java/lang/
├── String.java                    # 核心 String 类 (~3500 行)
├── AbstractStringBuilder.java     # StringBuilder/StringBuffer 基类
├── StringBuilder.java             # 非同步可变字符串
├── StringBuffer.java              # 同步可变字符串
├── StringConcatHelper.java        # 拼接辅助类 (JDK 9+)
├── StringLatin1.java              # LATIN1 编码操作 (~500 行)
├── StringUTF16.java               # UTF16 编码操作 (~800 行)
└── StringCoding.java              # 编码转换 (~300 行)

src/java.base/share/classes/java/lang/invoke/
└── StringConcatFactory.java       # invokedynamic 拼接工厂 (~500 行)

src/java.base/share/classes/java/util/
├── StringJoiner.java              # JDK 8+
└── FormattedString.java           # JDK 21+ 模板
```

### String 类字段

```java
public final class String
    implements java.io.Serializable,
               Comparable<String>,
               CharSequence,
               Constable,
               ConstantDesc {

    /** 缓存的哈希值 */
    private int hash;  // Default to 0

    /** JDK 9+: 字节数组存储 */
    @Stable
    private final byte[] value;

    /** JDK 9+: 编码标识符 */
    private final byte coder;

    /** 编码常量 */
    static final byte LATIN1 = 0;
    static final byte UTF16  = 1;

    /** Compact Strings 开关 */
    static final boolean COMPACT_STRINGS;

    /** 空字符串 (LATIN1) */
    private static final Object[] EMPTY_VALUE;

    static {
        COMPACT_STRINGS = true;
    }
}
```

### StringLatin1 关键方法

```java
// StringLatin1.java - LATIN1 专用操作
final class StringLatin1 {

    // indexOf
    public static int indexOf(byte[] value, int ch, int fromIndex) {
        int max = value.length;
        if (ch < 0) {
            ch = ch + 256;  // 处理负数
        }
        for (int i = fromIndex; i < max; i++) {
            if (value[i] == ch) {
                return i;
            }
        }
        return -1;
    }

    // lastIndexOf
    public static int lastIndexOf(byte[] value, int ch) {
        if (ch < 0) {
            ch = ch + 256;
        }
        for (int i = value.length - 1; i >= 0; i--) {
            if (value[i] == ch) {
                return i;
            }
        }
        return -1;
    }

    // compareTo
    public static int compareTo(byte[] value, byte[] other) {
        int len1 = value.length;
        int len2 = other.length;
        int lim = Math.min(len1, len2);
        for (int k = 0; k < lim; k++) {
            if (value[k] != other[k]) {
                return getChar(value, k) - getChar(other, k);
            }
        }
        return len1 - len2;
    }

    // hashCode
    public static int hashCode(byte[] value) {
        int h = 0;
        for (byte v : value) {
            h = 31 * h + (v & 0xff);
        }
        return h;
    }

    // 压缩检测
    public static int compress(char[] src, int srcOff, byte[] dst, int dstOff, int len) {
        for (int i = 0; i < len; i++) {
            char c = src[srcOff++];
            if (c > 0xFF) {
                return 0;  // 无法压缩
            }
            dst[dstOff++] = (byte)c;
        }
        return 1;  // 压缩成功
    }
}
```

### StringUTF16 关键方法

```java
// StringUTF16.java - UTF16 专用操作
final class StringUTF16 {

    // 每字符 2 字节
    public static int length(byte[] value) {
        return value.length >> 1;
    }

    // 获取 char
    @ForceInline
    public static char getChar(byte[] value, int index) {
        index <<= 1;
        return (char)((value[index] & 0xff) << 8 | (value[index + 1] & 0xff));
    }

    // 设置 char
    @ForceInline
    public static void putChar(byte[] value, int index, int c) {
        index <<= 1;
        value[index]     = (byte)(c >> 8);
        value[index + 1] = (byte)c;
    }

    // 压缩检测 (能否转为 LATIN1)
    public static boolean canEncode(char[] src, int off, int len) {
        for (int i = 0; i < len; i++) {
            if (src[off++] > 0xFF) {
                return false;
            }
        }
        return true;
    }

    // codePoint 操作
    public static int codePointAt(byte[] value, int index, int end) {
        char c1 = getChar(value, index);
        if (Character.isHighSurrogate(c1) && ++index < end) {
            char c2 = getChar(value, index);
            if (Character.isLowSurrogate(c2)) {
                return Character.toCodePoint(c1, c2);
            }
        }
        return c1;
    }
}
```

---

## 性能对比总结

| 版本 | 特性 | 内存 | 启动 | 运行时 |
|------|------|------|------|--------|
| **JDK 8** | char[] | 基准 | 基准 | 基准 |
| **JDK 9** | Compact Strings | **-50%** (ASCII) | +5% | +2% |
| **JDK 9** | invokedynamic 拼接 | - | +10% | +3% |
| **JDK 11** | StringJoiner | - | - | +5% (批量) |
| **JDK 17** | 优化 LATIN1 路径 | - | +5% | +5% |
| **JDK 21** | String Templates | - | - | +10% (可读性) |
| **JDK 24** | 隐藏类拼接 | - | **+40%** | +5% |
| **JDK 25** | StringBuilder 优化 | - | - | +15% |
| **JDK 26** | toString 优化 | - | - | +16% (C1) |

---

## 最佳实践

### 字符串拼接

```java
// ✅ 简单拼接：使用 + (编译器优化为 invokedynamic)
String result = "Hello " + name;

// ✅ 循环拼接：使用 StringBuilder
StringBuilder sb = new StringBuilder(estimatedSize);  // 指定容量
for (String s : list) {
    sb.append(s);
}

// ✅ JDK 8+：使用 StringJoiner 或 Collectors.joining
String result = String.join(", ", list);
String result = list.stream().collect(Collectors.joining(", "));

// ✅ JDK 21+：使用 String Templates
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

// ✅ 常量放前面 (避免 NPE)
if ("known".equals(str)) { }

// ✅ compareTo 用于排序
if (str1.compareTo(str2) > 0) { }

// ✅ JDK 11+ isBlank()
if (str.isBlank()) { }

// ❌ 不要使用 == 比较内容
if (str1 == str2) { }  // 仅比较引用
```

### 内存优化

```java
// ✅ 复用常量字符串
private static final String PREFIX = "prefix:";

// ✅ 使用 intern() 谨慎
// - 适合: 少量、长期存在的字符串
// - 避免: 大量、短生命周期的字符串 (会撑爆 Perm/Metaspace)

// ✅ 使用 StringBuilder 预分配容量
StringBuilder sb = new StringBuilder(1024);  // 避免扩容

// ✅ 使用 text blocks 避免转义
String json = """
    {"name": "John", "age": 30}
    """;
```

### VM 调优

```bash
# Compact Strings (默认启用)
-XX:+CompactStrings    # 启用 (推荐)
-XX:-CompactStrings    # 禁用 (纯 UTF16)

# G1 字符串去重
-XX:+UseStringDeduplication
-XX:StringDeduplicationAgeThreshold=3

# 字符串拼接调优 (JDK 24+)
-Djava.lang.invoke.StringConcat.highArityThreshold=0
-Djava.lang.invoke.StringConcat.cacheThreshold=256
-Djava.lang.invoke.StringConcat.inlineThreshold=16

# 查看字符串拼接统计
-XX:+PrintStringDeduplicationStatistics
```

---

## 贡献者分析

### 主要贡献者

| 贡献者 | GitHub | 主要贡献 | 时期 |
|--------|--------|----------|------|
| **Shaojin Wen** | @shaojin-wen | 字符串拼接优化 (+40% 启动), toString 优化 | JDK 24-26 |
| Claes Redestad | @cl4es | Compact Strings, 性能优化 | JDK 9+ |
| Vladimir Kozlov | @vnk | Compact Strings 架构 | JDK 9 |
| Aleksey Shipilev | @shade | Compact Strings 实现 | JDK 9 |
| Jim Laskey | @jimlaskey | Text Blocks, String Templates | JDK 15-21 |
| Gavin Bierman | @gmbierman | String Templates | JDK 21 |
| Brian Goetz | @briangoetz | 架构指导 | 所有版本 |

### Shaojin Wen 贡献详情

```bash
# JDK 24 (2025)
JDK-8336856  # 隐藏类拼接策略 (+40% 启动性能)
JDK-8338937  # ClassDesc 拼接优化 (+20-30%)

# JDK 25 (2025)
JDK-8355177  # StringBuilder.append 优化 (+15%)

# JDK 26 (2026)
JDK-8370503  # Integer/Long.toString 优化 (+16% C1)
JDK-8368024  # 移除 MH InlineCopy
```

详细贡献分析: [Shaojin Wen Profile](/by-contributor/profiles/shaojin-wen.md)

---

## 相关 JEP

| JEP | 标题 | 版本 | 说明 |
|-----|------|------|------|
| [JEP 254](https://openjdk.org/jeps/254) | Compact Strings | JDK 9 | 内存优化存储 |
| [JEP 280](https://openjdk.org/jeps/280) | Indify String Concatenation | JDK 9 | invokedynamic 拼接 |
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

### 官方文档
- [OpenJDK: String 源码](https://github.com/openjdk/jdk/blob/master/src/java.base/share/classes/java/lang/String.java)
- [JEP 254: Compact Strings](https://openjdk.org/jeps/254)
- [JEP 430: String Templates](https://openjdk.org/jeps/430)

### 文章
- [Inside Java: Performance Improvements in JDK 24](https://inside.java/2025/03/19/performance-improvements-in-jdk24/)
- [Compact Strings in JDK 9](https://openjdk.org/projects/jdk9/)
- [String Concatenation Evolution](https://shipilev.net/blog/2016/string-concatenation/)

### 贡献者
- [Contributor: Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) - 主要字符串优化贡献者
- [Claes Redestad](https://github.com/cl4es) - Oracle 工程师

---

> **文档版本**: 4.0
> **最后更新**: 2026-03-20
> **数据来源**: JDK 源码、JEP、GitHub PR 分析
