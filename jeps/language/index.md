# 语言特性 JEPs

> JDK 21-26 语言特性相关 JEP 汇总

---

## 概览

```
JDK 21 ───── JDK 22 ───── JDK 23 ───── JDK 24 ───── JDK 25 ───── JDK 26
   │            │            │            │            │            │
String     Unnamed    Implicit    String     Pattern      Primitive
Templates  Variables  Classes     Templates  Matching   Patterns
(撤回)      (正式)      (正式)      (预览)      (预览)        (预览)
```

---

## String Templates

### 演进历程

| 版本 | JEP | 状态 | 说明 |
|------|-----|------|------|
| JDK 21 | 430 | 🔍 预览 | 首次预览 |
| JDK 22 | 459 | 🔍 预览 | 第二次预览 |
| JDK 23 | 465 | 🔍 预览 | 第三次预览 |
| **JDK 25** | 471 | 🔍 预览 | 第四次预览 (或正式?) |

### 核心语法

```java
// 基本用法
String name = "World";
int count = 42;
String message = STR."Hello \{name}! You count is \{count}";

// 多行文本块
String json = STR."""
    {
        "name": "\{name}",
        "count": \{count}
    }
    """;

// 表达式嵌入
int x = 10, y = 20;
String result = STR."\{x} + \{y} = \{x + y}";  // "10 + 20 = 30"
```

**注意**: JEP 430 在 JDK 25 之前被撤回，参见 [JDK-8343684](https://bugs.openjdk.org/browse/JDK-8343684)

**详见**：[String Templates 分析](string-templates.md) | [JEP 430](jep-430.md) | [JEP 459](jep-459.md) | [JEP 471](jep-471.md)
---

## Pattern Matching

### 演进历程

| 版本 | JEP | 状态 | 说明 |
|------|-----|------|------|
| JDK 16 | 394 | ✅ 正式 | Pattern Matching for instanceof |
| JDK 17 | 406 | ✅ 正式 | Record Patterns |
| JDK 18 | 420 | 🔍 预览 | Record Patterns (Second Preview) |
| JDK 19 | 427 | 🔍 预览 | Record Patterns (Third Preview) |
| JDK 20 | 432 | 🔍 预览 | Unnamed Variables and Patterns |
| JDK 21 | 441 | ✅ 正式 | Pattern Matching for switch |
| JDK 22 | 456 | ✅ 正式 | Unnamed Variables & Patterns |
| JDK 25 | 507 | 🔍 预览 | Primitive Types in Patterns (Third Preview) |
| JDK 26 | 530 | 🔍 预览 | Primitive Types in Patterns (Fourth Preview) |

### 核心语法

```java
// 类型模式匹配
Object obj = "Hello";
if (obj instanceof String s) {
    System.out.println(s.toUpperCase());
}

// 模式匹配 for switch
String formatted = switch (obj) {
    case String s -> s.toUpperCase();
    default -> obj.toString();
}

// 模式匹配 for记录
record Point(int x, int y) {}
if (obj instanceof Point(int x, int y)) {
    // 自动解构
}
```

**详见**：[Pattern Matching 分析](pattern-matching.md) | [JEP 456](jep-456.md) | [JEP 507](jep-507.md) | [JEP 530](jep-530.md)
---

## Implicit Classes (隐式类)

### 演进历程
| 版本 | JEP | 状态 | 说明 |
|------|-----|------|------|
| JDK 21 | 445 | 🔍 预览 | Unnamed Classes and Instance Main Methods |
| JDK 22 | 463 | 🔍 预览 | Implicit Classes and Instance Main Methods (Second Preview) |
| JDK 23 | 477 | ✅ 正式 | Implicitly Declared Classes and Instance Main Methods |

| JDK 26 | 512 | ✅ 正式 | Compact Source Files and Instance Main Methods |

### 核心语法
```java
// JDK 21 之前
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}

// JDK 21+ 隐式类
void main() {
    System.out.println("Hello, World!");
}

```
**详见**：[Implicit Classes 分析](implicit-classes.md) | [JEP 445](jep-445.md) | [JEP 463](jep-463.md) | [JEP 477](jep-477.md) | [JEP 512](jep-512.md)
---

## 相关链接

- [语言特性演进时间线](/by-topic/language/)
- [Java Language Updates](https://openjdk.org/projects/jdk/)
