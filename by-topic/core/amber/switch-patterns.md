# Switch 表达式与模式匹配演进

Switch Expressions, Pattern Matching for instanceof, Pattern Matching for switch,
Record Patterns, Unnamed Patterns 的完整演进历程。

[← 返回 Project Amber 概览](README.md)

---

## 演进路线 (Evolution Roadmap)

Switch 在 Amber 项目下经历了**最长的演进链**，从简单的语法改进到完整的模式匹配系统：

```
JEP 325 (Preview)    JDK 12   Switch Expressions (第一预览)
    |
JEP 354 (2nd Preview) JDK 13  Switch Expressions (第二预览, 引入 yield)
    |
JEP 361 (Final)       JDK 14  Switch Expressions (正式发布)
    |
JEP 394 (Final)       JDK 16  Pattern Matching for instanceof (正式)
    |
JEP 406 (Preview)     JDK 17  Pattern Matching for switch (第一预览)
    |
JEP 440 (Final)       JDK 21  Record Patterns (正式)
    |
JEP 441 (Final)       JDK 21  Pattern Matching for switch (正式)
    |
JEP 456 (Final)       JDK 22  Unnamed Patterns & Variables (正式)
    |
JEP 455->488->507->530   JDK 23-26  Primitive Patterns (预览中)
```

---

## 阶段 1: Switch Expressions (JEP 325 -> 354 -> 361)

```java
// ===== JEP 325 (JDK 12 Preview): 引入 arrow syntax =====
// 旧写法 - 语句形式, 需要 break, 容易 fall-through 出错
int result;
switch (day) {
    case MONDAY:
    case FRIDAY:
    case SUNDAY:
        result = 6;
        break;        // 忘记 break 就 fall-through!
    case TUESDAY:
        result = 7;
        break;
    default:
        result = 0;
}

// JDK 12 新写法 - 表达式形式
int result = switch (day) {
    case MONDAY, FRIDAY, SUNDAY -> 6;    // 多标签, 无 fall-through
    case TUESDAY                -> 7;
    default                     -> 0;
};  // 注意分号 - 因为整个 switch 是一个表达式

// ===== JEP 354 (JDK 13 Preview): break 改为 yield =====
// JDK 12 中使用 break value 返回值，JDK 13 改为 yield 更清晰
String message = switch (status) {
    case 0 -> {
        log("Processing...");
        yield "OK";       // yield 用于代码块中返回值 (替代了 JDK 12 的 break value)
    }
    case 1 -> "Warning";  // 单行表达式不需要 yield
    case 2 -> "Error";
    default -> "Unknown";
};

// ===== JEP 361 (JDK 14 Final): 正式发布 =====
// 语义与 JDK 13 相同, 两种形式都可用：
// 1) arrow 形式 (推荐, 无 fall-through)
int numLetters = switch (day) {
    case MONDAY, FRIDAY, SUNDAY -> 6;
    case TUESDAY                -> 7;
    case THURSDAY, SATURDAY     -> 8;
    case WEDNESDAY              -> 9;
};

// 2) colon 形式 + yield (兼容旧语法, 仍有 fall-through 风险)
int numLetters = switch (day) {
    case MONDAY:
    case FRIDAY:
    case SUNDAY:
        yield 6;          // 用 yield 替代 break
    case TUESDAY:
        yield 7;
    default:
        yield 0;
};
```

---

## 阶段 2: Pattern Matching for instanceof (JEP 394)

```java
// JDK 16 正式 - 消除冗余的类型转换
// 旧写法
if (obj instanceof String) {
    String s = (String) obj;     // 冗余的强制转换
    System.out.println(s.length());
}

// 新写法 - 模式变量 (pattern variable)
if (obj instanceof String s) {
    System.out.println(s.length());  // s 已自动绑定
}

// 模式变量的作用域 (flow scoping) - 编译器根据控制流推断
if (obj instanceof String s && s.length() > 5) {
    // s 在 && 后面可用 (因为 && 只在左边为 true 时计算右边)
}

if (!(obj instanceof String s)) {
    return;
}
// s 在这里可用 (因为如果 obj 不是 String, 已经 return 了)
System.out.println(s.toUpperCase());

// 编译错误 - 在 || 后面不安全
if (obj instanceof String s || s.length() > 5) {  // 编译错误！
    // s 可能没有被绑定
}
```

---

## 阶段 3: Pattern Matching for switch (JEP 406 -> 441)

```java
// JEP 406 (JDK 17 Preview) -> JEP 420 (JDK 18) -> JEP 427 (JDK 19)
// -> JEP 433 (JDK 20) -> JEP 441 (JDK 21 Final)
// 经过了 4 轮预览才最终定稿

// 类型模式 (type pattern) 在 switch 中
String formatted = switch (obj) {
    case Integer i -> String.format("int %d", i);
    case Long l    -> String.format("long %d", l);
    case Double d  -> String.format("double %f", d);
    case String s  -> String.format("String %s", s);
    default        -> obj.toString();
};

// 守卫模式 (guarded pattern) - when 子句
String check = switch (obj) {
    case String s when s.length() > 5 -> "Long string: " + s;
    case String s                     -> "Short string: " + s;
    case Integer i when i > 0         -> "Positive int";
    case Integer i                    -> "Non-positive int";
    default                           -> "Unknown";
};
// 注意: case 的顺序重要! 有守卫的 case 必须在无守卫的同类型 case 之前

// null 处理 (不再需要在 switch 外检查 null)
String result = switch (obj) {
    case null      -> "null value";        // 显式处理 null
    case String s  -> "String: " + s;
    default        -> "Other type";
};

// null + default 合并
String result = switch (obj) {
    case String s  -> "String: " + s;
    case null, default -> "null or other";  // null 和 default 可以合并
};

// 穷尽性检查 (exhaustiveness) - 密封类不需要 default
sealed interface Shape permits Circle, Rectangle {}
record Circle(double r) implements Shape {}
record Rectangle(double w, double h) implements Shape {}

double area = switch (shape) {
    case Circle c    -> Math.PI * c.r() * c.r();
    case Rectangle r -> r.w() * r.h();
    // 无需 default - 编译器知道所有子类型都已覆盖
};
```

---

## 阶段 4: Record Patterns (JEP 440)

```java
// Record Patterns (JDK 21) - 解构 Record 组件
record Point(int x, int y) {}
record Rectangle(Point topLeft, Point bottomRight) {}

// 旧写法
void printOld(Rectangle r) {
    Point tl = r.topLeft();
    int x = tl.x();
    int y = tl.y();
    System.out.println("Top-left: (" + x + ", " + y + ")");
}

// 新写法 - Record Pattern
void printNew(Rectangle r) {
    if (r instanceof Rectangle(Point(int x, int y), Point bottomRight)) {
        System.out.println("Top-left: (" + x + ", " + y + ")");
    }
}

// 嵌套解构 (nested deconstruction) 在 switch 中
String describe(Object obj) {
    return switch (obj) {
        case Rectangle(Point(int x1, int y1), Point(int x2, int y2)) ->
            "Rectangle from (%d,%d) to (%d,%d)".formatted(x1, y1, x2, y2);
        case Point(int x, int y) ->
            "Point at (%d,%d)".formatted(x, y);
        default -> "Unknown shape";
    };
}

// 结合 unnamed pattern
void extractX(Object obj) {
    if (obj instanceof Point(int x, _)) {
        // 只关心 x 坐标，忽略 y
        System.out.println("X coordinate: " + x);
    }
}
```

---

## 阶段 5: Unnamed Patterns & Variables (JEP 456)

```java
// JDK 22 正式 - 使用 _ 忽略不关心的值

// instanceof 中忽略变量
if (obj instanceof String _) {
    // 只关心类型，不关心具体值
    System.out.println("It's a string!");
}

// Lambda 中忽略参数
stream.map(_ -> "constant")  // 所有元素映射为 "constant"

// Record 模式中忽略组件
if (obj instanceof Point(int x, _)) {
    // 只关心 x 坐标，忽略 y
    System.out.println("X: " + x);
}

// 异常处理中忽略异常对象
try {
    riskyOperation();
} catch (Exception _) {
    logger.error("Failed");
}

// try-with-resources 中忽略资源变量
try (var _ = ScopedContext.open()) {
    doWork();
}
```

---

## 相关 JEP

| JEP | 版本 | 状态 | 说明 |
|-----|------|------|------|
| [JEP 325](/jeps/language/jep-325.md) | JDK 12 | Preview | Switch Expressions 第一预览 |
| [JEP 354](/jeps/language/jep-354.md) | JDK 13 | Preview | Switch Expressions 第二预览 |
| [JEP 361](/jeps/language/jep-361.md) | JDK 14 | Final | Switch Expressions 正式 |
| [JEP 394](/jeps/language/jep-394.md) | JDK 16 | Final | Pattern Matching for instanceof |
| [JEP 441](/jeps/language/jep-441.md) | JDK 21 | Final | Pattern Matching for switch |
| [JEP 440](/jeps/language/jep-440.md) | JDK 21 | Final | Record Patterns |
| [JEP 456](https://openjdk.org/jeps/456) | JDK 22 | Final | Unnamed Patterns & Variables |
