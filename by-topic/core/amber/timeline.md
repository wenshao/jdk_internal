# Project Amber 时间线

Java 语言特性演进完整历史。

[← 返回 Amber](./)

---

## 2017: 项目启动

### 项目宣布

- **日期**: 2017-06
- **事件**: Project Amber 正式宣布
- **目标**: "让 Java 更简洁、更安全、更易表达"
- **初始 JEPs**:
  - JEP 286: Local-Variable Type Inference
  - JEP 323: Lambda Parameter Names
  - JEP 301: Enhanced Enums (未完成)

---

## 2018: JDK 10 - var 关键字

### JEP 286: Local-Variable Type Inference

- **日期**: 2018-03
- **特性**: `var` 关键字
- **示例**:

```java
// 旧写法
ArrayList<String> list = new ArrayList<String>();
HashMap<String, Integer> map = new HashMap<String, Integer>();

// 新写法
var list = new ArrayList<String>();
var map = new HashMap<String, Integer>();
```

- **约束**: 仅限局部变量，不能用于字段、方法参数

---

## 2019: JDK 14 - Switch 表达式

### JEP 361: Switch Expressions (正式)

- **日期**: 2019-06 (预览) → 2020-03 (正式)
- **特性**:
  - switch 作为表达式
  - 箭头语法
  - 多标签 case

```java
// 预览阶段 (JDK 12-13)
int result;
switch (day) {
    case MONDAY, FRIDAY, SUNDAY -> result = 6;
    case TUESDAY -> result = 7;
    // ...
}

// 正式版本 (JDK 14)
int result = switch (day) {
    case MONDAY, FRIDAY, SUNDAY -> 6;
    case TUESDAY -> 7;
    default -> 0;
};
```

---

## 2020: JDK 14-15 - instanceof 模式

### JEP 305: Pattern Matching for instanceof

- **日期**: 2020-03 (预览) → 2021-03 (正式, JDK 16)
- **特性**: 类型测试后自动绑定变量

```java
// 旧写法
if (obj instanceof String) {
    String s = (String) obj;
    // 使用 s
}

// 新写法
if (obj instanceof String s) {
    // s 自动可用
}
```

### JEP 378: Text Blocks (正式)

- **日期**: 2020-06 (预览) → 2021-03 (正式, JDK 15)
- **特性**: 多行字符串字面量

```java
String html = """
    <html>
        <body>
            <p>Hello, World</p>
        </body>
    </html>
    """;
```

---

## 2021: JDK 16-17 - Records 和 Sealed

### JEP 395: Records (正式)

- **日期**: 2021-03 (正式, JDK 16)
- **特性**: 不可变数据类

```java
public record Point(int x, int y) {}
```

### JEP 394: instanceof Pattern Matching (正式)

- **日期**: 2021-03 (正式, JDK 16)
- **里程碑**: 首个模式匹配特性正式交付

### JEP 409: Sealed Classes (正式)

- **日期**: 2021-09 (正式, JDK 17)
- **特性**: 密封类，限制继承

```java
public sealed interface Shape
    permits Circle, Rectangle, Square {}
```

---

## 2022-2023: Record Patterns

### JEP 405: Record Patterns (预览)

- **日期**: 2022-09 (预览, JDK 19)
- **特性**: 解构 Record 模式

```java
record Point(int x, int y) {}

if (obj instanceof Point(int x, int y)) {
    System.out.println("x=" + x + ", y=" + y);
}
```

### JEP 440: Record Patterns (正式)

- **日期**: 2023-09 (正式, JDK 21)

---

## 2023: JDK 21 - Amber 大版本

### JEP 441: Pattern Matching for switch (正式)

- **日期**: 2023-09 (正式, JDK 21)
- **特性**: switch 语句的模式匹配

```java
String formatted = switch (obj) {
    case Integer i -> String.format("int %d", i);
    case Long l    -> String.format("long %d", l);
    case String s  -> String.format("String %s", s);
    default        -> obj.toString();
};
```

### JEP 443: Unnamed Patterns & Variables

- **日期**: 2023-09 (正式, JDK 21)
- **特性**: 使用 `_` 忽略不关心的值

```java
// 忽略组件
if (obj instanceof Point(int x, _)) {
    // 只关心 x
}

// Lambda 参数
stream.map(_ -> "constant")
```

### JEP 451: Prepare to Disallow the Dynamic Loading of Agents

- **日期**: 2023-09 (正式, JDK 21)
- **特性**: 为未来禁用动态 Agent 加载做准备

---

## 2024: JDK 22 - 构造器改进

### JEP 448: Flexible Constructor Bodies

- **日期**: 2024-03 (正式, JDK 22)
- **特性**: 构造器中可以在 super() 前执行语句

```java
public class Sub extends Super {
    private final int x;

    public Sub(int x) {
        // 可以在 super() 前执行
        int size = calculateSize();
        super(size);
        this.x = x;
    }
}
```

### JEP 447: Statements before super (Preview)

- **日期**: 2024-03 (预览, JDK 22)
- **特性**: 更灵活的构造器语法

---

## 2024: String Templates 撤回

### JEP 430: String Templates (预览后撤回)

- **日期**: 2024-06
- **状态**: 撤回，重新设计
- **原因**: 社区反馈需要更多讨论

```java
// 原计划语法 (未交付)
String name = "World";
String message = STR."Hello, \{name}!";
```

---

## 2025: JDK 26 - Primitive Patterns

### JEP 455: Primitive Patterns

- **日期**: 2025 (正式, JDK 26)
- **特性**: 原始类型模式匹配

```java
switch (value) {
    case int i    -> "Integer: " + i;
    case long l   -> "Long: " + l;
    case double d -> "Double: " + d;
    default       -> "Other";
}
```

---

## 未来计划

### 阶段性进行中的 JEP

| JEP | 标题 | 状态 |
|-----|------|------|
| JEP 463 | Implicit Classes | 预览中 |
| JEP 465 | String Templates (第二版) | 重新设计中 |

---

## 时间线总览

```
2017 ── 2018 ── 2020 ── 2021 ── 2023 ── 2025 ── 2026
  │        │        │        │        │        │        │
启动     var      Switch   Records  Pattern  Primitive  未来
        JDK10    表达式   Sealed   Matching  Patterns   优化
                  JDK14    JDK17    JDK21     JDK26
                           JDK16
```

---

## 里程碑总结

| 版本 | 主要特性 | 影响 |
|------|----------|------|
| **JDK 10** | var | 减少 20-30% 变量声明代码 |
| **JDK 14** | Switch 表达式 | 减少 50% switch 代码 |
| **JDK 15** | Text Blocks | 简化多行字符串 90% |
| **JDK 16** | Records | 数据类减少 95% 代码 |
| **JDK 17** | Sealed Classes | 代数数据类型 |
| **JDK 21** | 模式匹配 | 类型安全 + 简洁 |
| **JDK 26** | Primitive Patterns | 泛型特化配合 |

→ [返回 Amber](./)
