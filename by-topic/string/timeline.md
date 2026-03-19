# 字符串处理演进时间线

字符串相关的优化和新特性。

---

## 时间线概览

```
JDK 8 ───── JDK 11 ───── JDK 17 ───── JDK 21 ───── JDK 26
│              │              │              │              │
StringJoiner   Compact       String        内部优化      性能优化
StringBuilder   Strings      Templates     (Compact
改进          (紧凑字符串)   (预览)       Object Headers)
```

---

## JDK 8 - 字符串基础

### StringJoiner

```java
StringJoiner joiner = new StringJoiner(", ");
joiner.add("Apple").add("Banana").add("Cherry");
String result = joiner.toString();  // "Apple, Banana, Cherry"
```

### StringBuilder 增强

```java
// StringBuilder 新增方法
sb.repeat("*", 3);  // "***"
```

---

## JDK 11 - Compact Strings (紧凑字符串)

### 变更

- **JDK 8**: `char[]` 存储 (UTF-16, 每字符 2 字节)
- **JDK 9+**: `byte[]` 存储 (ASCII 1 字节, Latin-1 1 字节, UTF-16 2 字节)

### 影响

```
纯 ASCII 字符串: 内存占用减半
混合内容字符串: 动态选择编码
```

### VM 参数

```bash
-XX:+CompactStrings    # 启用 (默认)
-XX:-CompactStrings    # 禁用 (回退到 char[])
```

---

## JDK 17 - 字符串内部优化

### 重复字符串去重

```java
// "hello" 和 "world" 可能共享底层存储
String a = "hello" + " " + "world";
String b = "hello world";  // 可能共享同一个 char[]
```

---

## JDK 21 - String Templates (预览)

### 模板表达式

```java
// 之前: 字符串拼接
String message = "Hello " + name + ", you have " + count + " messages.";

// JDK 21: 模板表达式 (预览)
String message = STR."Hello \{name}, you have \{count} messages.";
```

### STR 模板处理器

```java
String JSON = STR."""
    {
        "name": "\{name}",
        "age": \{age}
    }
    """;
```

---

## JDK 26 - 字符串性能优化

### StringBuilder 优化

| 优化项 | 提升 |
|--------|------|
| `append(char[])` | +15% |
| `append(String)` | +10% |
| `toString()` | +5% |

### 其他字符串相关优化

- `Integer.toString` 优化 (+10%)
- `Double.toHexString` 优化 (+20%)
- `UUID.toString` 优化 (+8%)

---

## Compact Strings 原理

```java
// coder 字节: 0 = Latin-1, 1 = UTF-16
byte[] value;     // 实际存储
byte coder;        // 编码标识

// 存储 ASCII "Hello" (5 字节)
value = [0x48, 0x65, 0x6C, 0x6C, 0x6F]
coder = 0  // Latin-1

// 存储 "你好" (4 字节)
value = [0x4F, 0x60, 0x59, 0x7D]  // UTF-16BE
coder = 1  // UTF-16
```

---

## 最佳实践

### 字符串拼接

```java
// ✅ 推荐: 使用 +
String result = "Hello " + name;

// ✅ 推荐: StringBuilder (循环中)
StringBuilder sb = new StringBuilder();
for (String s : list) {
    sb.append(s);
}

// ❌ 避免: 循环中使用 +
for (String s : list) {
    result += s;  // 每次创建新对象
}
```

### 字符串比较

```java
// ✅ 使用 equals()
if (str1.equals(str2)) { }

// ✅ 使用 Objects.equals() (避免 NPE)
if (Objects.equals(str1, str2)) { }

// ❌ 不要使用 ==
// "hello" == "hello" 可能返回 false (不同实例)
```

---

## 时间线总结

| 版本 | 特性 | 说明 |
|------|------|------|
| JDK 6 | StringBuilder | 可变字符串 |
| JDK 8 | StringJoiner | 便捷拼接 |
| JDK 9 | Compact Strings | 内存优化 |
| JDK 11 | String.repeat() | 重复方法 |
| JDK 21 | String Templates (预览) | 模板表达式 |
| JDK 26 | 性能优化 | StringBuilder +10-15% |

---

## 相关链接

- [Compact Strings JEP](https://openjdk.org/jeps/254)
- [String Templates JEP](https://openjdk.org/jeps/430)
- [StringBuilder 源码分析](/by-version/jdk26/deep-dive/)
