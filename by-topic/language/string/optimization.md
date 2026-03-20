# String 性能优化

> String Deduplication、VM 调优、最佳实践

---

## TL;DR 快速概览

> 💡 **1 分钟了解 String 性能优化**

### 关键优化汇总

| 优化项 | JDK | 性能提升 | 适用场景 |
|--------|-----|----------|----------|
| **Compact Strings** | 9 | 内存 -50% | ASCII 字符串 |
| **String Deduplication** | 8u20 | 内存 10-40% | 重复字符串 |
| **invokedynamic 拼接** | 9 | 启动 +10% | 字符串拼接 |
| **隐藏类策略** | 24 | 启动 +40% | 拼接优化 |
| **StringBuilder 优化** | 24 | 吞吐 +15-40% | append(char[]) |

### 快速决策

```java
// 简单拼接 → 直接用 +
String s = "Hello " + name;

// 循环拼接 → StringBuilder
StringBuilder sb = new StringBuilder(size);
for (String s : list) sb.append(s);

// 处理重复字符串 → 启用 Deduplication
-XX:+UseStringDeduplication

// 内存敏感 → Compact Strings (JDK 9+ 默认)
```

### VM 参数速查

```bash
# 启用 String 去重 (G1 GC)
-XX:+UseG1GC -XX:+UseStringDeduplication

# 查看去重统计
-XX:+PrintStringDeduplicationStatistics

# 调整字符串表大小
-XX:StringTableSize=10000
```

---

## String Deduplication (JEP 192)

### 工作原理

G1 GC 自动识别并合并堆中重复的 String：

```java
// 去重前
String s1 = "Hello";  // value@0x1000
String s2 = "Hello";  // value@0x2000

// 去重后
String s1 = "Hello";  // value@0x1000
String s2 = "Hello";  // value@0x1000 (共享)
```

### VM 配置

```bash
# 启用 (仅 G1 GC)
-XX:+UseG1GC -XX:+UseStringDeduplication

# 年龄阈值 (默认 3)
-XX:StringDeduplicationAgeThreshold=3

# 查看统计
-XX:+PrintStringDeduplicationStatistics
```

### 性能影响

| 场景 | 内存节省 | CPU 开销 |
|------|----------|----------|
| JSON 处理 | 20-40% | 低 |
| XML 解析 | 15-25% | 低 |
| 大量重复 | 10-30% | 低 |

### 与 intern() 对比

| 特性 | String Deduplication | intern() |
|------|---------------------|----------|
| 自动程度 | 完全自动 | 手动调用 |
| 存储位置 | 堆 | Metaspace |
| 适用场景 | 大量堆字符串 | 少量常量 |

---

## 字符串拼接优化

### JDK 9+ invokedynamic

```java
// 编译前
String result = "Hello " + name + "!";

// 编译后 (JDK 9+)
invokedynamic makeConcatWithConstants(Ljava/lang/String;)Ljava/lang/String;
```

### JDK 24+ 隐藏类策略

按"形状"共享类，+40% 启动性能：

```java
// 之前: 每个调用点一个类
class StringConcat$1 { ... }
class StringConcat$2 { ... }

// 之后: 按参数类型共享
class Concat3String { ... }  // 所有 String+String+String
```

### 最佳实践

```java
// ✅ 简单拼接
String result = "Hello " + name;

// ✅ 循环拼接
StringBuilder sb = new StringBuilder(estimatedSize);
for (String s : list) {
    sb.append(s);
}

// ✅ JDK 8+ 批量拼接
String result = String.join(", ", list);
String result = list.stream().collect(Collectors.joining(", "));

// ✅ JDK 21+ 模板
String result = STR."Hello \{name}!";

// ❌ 避免
String result = "";
for (String s : list) {
    result += s;  // 每次创建新对象
}
```

---

## VM 参数汇总

### Compact Strings

```bash
-XX:+CompactStrings   # 启用 (默认)
-XX:-CompactStrings   # 禁用
```

### String Deduplication

```bash
-XX:+UseG1GC
-XX:+UseStringDeduplication
-XX:StringDeduplicationAgeThreshold=3
```

### 字符串拼接 (JDK 24+)

```bash
-Djava.lang.invoke.StringConcat.cacheThreshold=256
-Djava.lang.invoke.StringConcat.inlineThreshold=16
```

---

## 性能对比

| 版本 | 特性 | 内存 | 启动 | 运行时 |
|------|------|------|------|--------|
| JDK 8 | char[] | 基准 | 基准 | 基准 |
| JDK 9 | Compact Strings | -50% (ASCII) | +5% | +2% |
| JDK 9 | invokedynamic | - | +10% | +3% |
| JDK 24 | 隐藏类拼接 | - | +40% | +5% |
| JDK 25 | StringBuilder 优化 | - | - | +15% |
| JDK 26 | toString 优化 | - | - | +16% (C1) |

---

## 最佳实践

### 字符串比较

```java
// ✅ 使用 equals
if (str1.equals(str2)) { }

// ✅ 空安全
if (Objects.equals(str1, str2)) { }

// ✅ 常量放前面
if ("known".equals(str)) { }

// ❌ 不要用 == 比较内容
if (str1 == str2) { }  // 仅比较引用
```

### 内存优化

```java
// ✅ 复用常量
private static final String PREFIX = "prefix:";

// ✅ 预分配容量
StringBuilder sb = new StringBuilder(1024);

// ✅ Text Blocks (JDK 15+)
String json = """
    {"name": "John"}
    """;
```

### 空白处理

```java
// JDK 11+
str.strip();    // Unicode 感知
str.stripLeading();
str.stripTrailing();
str.isBlank();  // 检查是否全空白

// JDK 1.0+
str.trim();     // 仅 ASCII
```

---

## 贡献者

### String 拼接优化演进

| 版本 | 特性 | 贡献者 | 说明 |
|------|------|--------|------|
| JDK 9 | invokedynamic | Aleksey Shipilev | JEP 280 作者 |
| JDK 24 | 隐藏类拼接 | **Shaojin Wen**, Claes Redestad | JDK-8336856 |
| JDK 25 | StringBuilder 优化 | **Shaojin Wen** | JDK-8355177 |
| JDK 26 | toString 优化 | **Shaojin Wen** | JDK-8370503 |

### Shaojin Wen (温绍锦)

- **公司**: Alibaba
- **身份**: OpenJDK Committer (2024-)
- **开源作品**: fastjson, druid
- **主要贡献**:
  - JDK-8336856: 隐藏类拼接策略 (+40% 启动性能)
  - JDK-8355177: StringBuilder Unsafe.copyMemory 优化
  - JDK-8370503: Integer/Long.toString LATIN1 路径
  - 25+ PR 合并到 OpenJDK 主线

> "The key insight is that string concatenation sites with the same 'shape' (argument types) can share the same hidden class."
> — Shaojin Wen, PR #20273 discussion

### Claes Redestad

- **公司**: Oracle
- **专长**: String/性能优化
- **主要贡献**: String 压缩、字节码优化

---

## 相关资源

- [JEP 192: String Deduplication](https://openjdk.org/jeps/192)
- [JDK-8336856: 隐藏类拼接策略](https://bugs.openjdk.org/browse/JDK-8336856)
- [PR #20273: String Concatenation with Hidden Classes](https://github.com/openjdk/jdk/pull/20273)
- [String Concatenation Evolution](https://shipilev.net/blog/2016/string-concatenation/)
