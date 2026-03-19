# 字符串处理

> Java String 从 JDK 1.0 到 JDK 26 的演进历程

---

## 快速概览

```
JDK 1.0 ── JDK 5 ── JDK 7u6 ── JDK 9 ── JDK 11 ── JDK 15 ── JDK 21 ── JDK 24 ── JDK 26
   │         │         │          │         │          │          │         │         │
 String   StringBuilder Substring Compact  repeat()  Text Blocks  String   Hidden   toString
 诞生      无同步      修复     Strings   strip()    (JEP 378)  Templates  Class    优化
 常量池                                            (JEP 430)   Strategy
(+40%启动)
```

### 核心特性

| 特性 | 版本 | 说明 |
|------|------|------|
| **Compact Strings** | JDK 9 | byte[] 存储，ASCII 内存节省 50% |
| **String Deduplication** | JDK 8u20 | GC 自动去重，节省 10-30% 内存 |
| **invokedynamic 拼接** | JDK 9 | 编译时优化，+10% 启动性能 |
| **Text Blocks** | JDK 15 | 多行字符串 `"""..."""` |
| **String Templates** | JDK 21 | 模板表达式 `STR."Hello \{name}"` |
| **隐藏类拼接** | JDK 24 | +40% 启动性能 |

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

## 版本速查

### JDK 8 → JDK 11

| 变化 | 说明 |
|------|------|
| Compact Strings | 默认启用，ASCII 内存 -50% |
| invokedynamic | 字符串拼接使用 invokedynamic |

### JDK 11 → JDK 17

| 变化 | 说明 |
|------|------|
| Text Blocks | 多行字符串 |
| strip() | Unicode 感知的去空格 |

### JDK 17 → JDK 21

| 变化 | 说明 |
|------|------|
| String Templates | 模板表达式 (预览) |
| repeat() | 字符串重复 |

### JDK 21 → JDK 26

| 变化 | 说明 |
|------|------|
| 隐藏类拼接 | +40% 启动性能 |
| StringBuilder 优化 | +15% 吞吐量 |
| toString 优化 | +16% C1 编译 |

---

## 常用方法

```java
// 拼接
String result = "Hello " + name;  // 简单
String joined = String.join(", ", list);  // JDK 8+

// 空白处理
str.strip();    // JDK 11+ Unicode 感知
str.trim();     // ASCII 空白
str.isBlank();  // JDK 11+

// 重复
str.repeat(3);  // JDK 11+

// 多行
String json = """
    {"name": "John"}
    """;  // JDK 15+

// 模板 (JDK 21+ 预览)
String result = STR."Hello \{name}!";
```

---

## VM 参数

```bash
# Compact Strings
-XX:+CompactStrings    # 启用 (默认)
-XX:-CompactStrings    # 禁用

# String Deduplication
-XX:+UseStringDeduplication
-XX:+UseG1GC
-XX:StringDeduplicationAgeThreshold=3

# 字符串拼接 (JDK 24+)
-Djava.lang.invoke.StringConcat.cacheThreshold=256
```

---

## 相关链接

- [JEP 254: Compact Strings](https://openjdk.org/jeps/254)
- [JEP 280: Indify String Concatenation](https://openjdk.org/jeps/280)
- [JEP 378: Text Blocks](https://openjdk.org/jeps/378)
- [JEP 430: String Templates](https://openjdk.org/jeps/430)
- [OpenJDK String 源码](https://github.com/openjdk/jdk/blob/master/src/java.base/share/classes/java/lang/String.java)
