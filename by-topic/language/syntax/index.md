# 语法演进

> 泛型、枚举、Lambda、模式匹配、记录类演进历程

[← 返回语言特性](../)

---

## 1. TL;DR 快速概览

> 💡 **1 分钟掌握 Java 语法演进**

### 语法速查

```java
// 泛型 (JDK 5+)
List<String> list = new ArrayList<>();
Map<String, Integer> map = new HashMap<>();

// 枚举 (JDK 5+)
enum Status { PENDING, RUNNING, COMPLETED }

// 变长参数 (JDK 5+)
void varargs(String... args) { }

// Diamond (JDK 7+)
List<String> list = new ArrayList<>();

// Lambda (JDK 8+)
Runnable r = () -> System.out.println("Hello");

// 方法引用 (JDK 8+)
list.forEach(System.out::println);

// var 类型推断 (JDK 10+)
var name = "Alice";  // 推断为 String

// Records (JDK 16+)
record Point(int x, int y) { }

// 模式匹配 (JDK 21+)
if (obj instanceof String s) { }

// Switch 表达式 (JDK 14+)
int result = switch (day) {
    case MONDAY, FRIDAY -> 1;
    default -> 0;
};
```

### 关键版本选择

| JDK | 新增特性 | 推荐 |
|-----|----------|------|
| **8** | Lambda, Stream | 函数式编程 |
| **11** | var, G1 GC | LTS (至 2026) |
| **17** | Record, Sealed Class | LTS (至 2029) |
| **21** | Pattern Matching, Virtual Threads | **当前 LTS** |

---

## 2. 快速概览

```
JDK 1.0 ── JDK 5 ── JDK 8 ── JDK 14 ── JDK 16 ── JDK 17 ── JDK 21 ── JDK 23 ── JDK 26
   │         │        │        │        │        │        │        │        │
基础语法  泛型    Lambda   Records  Sealed   模式匹配  Switch   原始类型  模块导入
类/接口  枚举    Stream   Pattern  Classes  for      Guards   Patterns  (JEP 511)
        变长    Optional  Matching  (JEP     instanceof  (JEP    (JEP 530) 紧凑源文件
        参数    方法引用            409)    (JEP 394/  305)              (JEP 512)
                                            441)
```

### 核心演进

| 版本 | 特性 | JEP | 说明 |
|------|------|-----|------|
| **JDK 5** | 泛型 | JSR 14 | 类型参数化 |
| **JDK 5** | 枚举 | - | enum 关键字 |
| **JDK 5** | 变长参数 | - | Method(...) |
| **JDK 8** | Lambda | JSR 335 | 函数式编程 |
| **JDK 8** | 方法引用 | - | :: 操作符 |
| **JDK 10** | 局部变量类型推断 | JEP 286 | var |
| **JDK 14** | Records (预览) | JEP 395 | 不可变类 |
| **JDK 15** | Sealed Classes (预览) | JEP 360 | 密封类 |
| **JDK 16** | Records (正式) | JEP 395 | 不可变数据类 |
| **JDK 16** | instanceof 模式匹配 | JEP 394 | 简化类型检查 |
| **JDK 17** | Sealed Classes (正式) | JEP 409 | 控制继承 |
| **JDK 21** | 模式匹配 for switch | JEP 441 | switch 表达式 |
| **JDK 21** | Record Patterns | JEP 440 | 记录解构 |
| **JDK 23** | Switch Guards | JEP 456 | 守卫子句 |
| **JDK 26** | 原始类型模式 | JEP 530 | primitive patterns |
| **JDK 26** | 模块导入 | JEP 511 | import module |
| **JDK 26** | 紧凑源文件 | JEP 512 | 简化入门 |

---

## 目录

- [基础语法](#基础语法)
- [泛型](#泛型)
- [枚举](#枚举)
- [Lambda 表达式](#lambda-表达式)
- [Records](#records)
- [Sealed Classes](#sealed-classes)
- [模式匹配](#模式匹配)
- [最新增强](#最新增强)
- [核心贡献者](#核心贡献者)
- [相关链接](#相关链接)

---

## 3. 基础语法

### 类和接口

```java
// 基础类定义
public class Person {
    // 字段
    private String name;
    private int age;

    // 构造方法
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    // 方法
    public String getName() {
        return name;
    }
}

// 接口
interface Runnable {
    void run();
}

// 抽象类
abstract class Animal {
    abstract void makeSound();
}
```

### 变长参数

```java
// 变长参数 (JDK 5+)
public void printNames(String... names) {
    for (String name : names) {
        System.out.println(name);
    }
}

// 使用
printNames("Alice", "Bob", "Charlie");
printNames("Single");
```

### 增强 for 循环

```java
// 增强 for 循环 (JDK 5+)
List<String> names = List.of("Alice", "Bob", "Charlie");

for (String name : names) {
    System.out.println(name);
}
```

---

## 4. 泛型

**JDK 5 引入**

### 基础泛型

```java
// 泛型类
public class Box<T> {
    private T value;

    public void set(T value) {
        this.value = value;
    }

    public T get() {
        return value;
    }
}

// 使用
Box<String> stringBox = new Box<>();
stringBox.set("Hello");
String str = stringBox.get();

Box<Integer> intBox = new Box<>();
intBox.set(123);
Integer num = intBox.get();
```

### 泛型方法

```java
// 泛型方法
public static <T> T getFirst(List<T> list) {
    if (list.isEmpty()) {
        return null;
    }
    return list.get(0);
}

// 类型推断
List<String> names = List.of("Alice", "Bob");
String first = getFirst(names);  // 推断为 String
```

### 通配符

```java
// 上界通配符
public void process(List<? extends Number> list) {
    // 只能读取, 不能写入
    Number num = list.get(0);
}

// 下界通配符
public void addNumbers(List<? super Integer> list) {
    // 只能写入 Integer 或其子类
    list.add(123);
}
```

### 类型擦除

```java
// 编译前
public class Box<T> {
    private T value;
    public T get() { return value; }
}

// 编译后 (类型擦除)
public class Box {
    private Object value;
    public Object get() { return value; }
}
```

---

## 5. 枚举

**JDK 5 引入**

### 基础枚举

```java
// 简单枚举
enum Day {
    MONDAY, TUESDAY, WEDNESDAY,
    THURSDAY, FRIDAY, SATURDAY, SUNDAY
}

// 使用
Day today = Day.MONDAY;
```

### 带方法和字段的枚举

```java
// 增强枚举
enum Planet {
    MERCURY(3.30e23, 2.44e6),
    VENUS(4.87e24, 6.05e6),
    EARTH(5.97e24, 6.37e6),
    MARS(6.42e23, 3.39e6);

    private final double mass;
    private final double radius;

    Planet(double mass, double radius) {
        this.mass = mass;
        this.radius = radius;
    }

    public double mass() { return mass; }
    public double radius() { return radius; }
}
```

### 枚举实现接口

```java
// 枚举实现接口
interface Operable {
    int apply(int a, int b);
}

enum Operation implements Operable {
    ADD {
        public int apply(int a, int b) { return a + b; }
    },
    SUBTRACT {
        public int apply(int a, int b) { return a - b; }
    };
}
```

---

## 6. Lambda 表达式

**JDK 8 引入 (JSR 335)**

### 基础 Lambda

```java
// Lambda 表达式
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);

// 匿名类方式 (旧)
Collections.sort(numbers, new Comparator<Integer>() {
    @Override
    public int compare(Integer a, Integer b) {
        return a.compareTo(b);
    }
});

// Lambda 方式 (新)
Collections.sort(numbers, (a, b) -> a.compareTo(b));

// 方法引用
Collections.sort(numbers, Integer::compareTo);
```

### 函数式接口

```java
// 常用函数式接口
Function<String, Integer> length = s -> s.length();
Predicate<Integer> isEven = n -> n % 2 == 0;
Consumer<String> printer = s -> System.out.println(s);
Supplier<Integer> supplier = () -> 42;

// 组合
Predicate<Integer> isPositive = n -> n > 0;
Predicate<Integer> isEvenAndPositive = isEven.and(isPositive);
```

### Stream API

```java
// Stream 操作
List<String> names = List.of("Alice", "Bob", "Charlie");

List<String> filtered = names.stream()
    .filter(name -> name.length() > 3)
    .map(String::toUpperCase)
    .sorted()
    .toList();
```

---

## 7. Records

**JDK 14 预览, JDK 16 正式 (JEP 395)**

### 基础 Record

```java
// Record - 不可变数据类
public record Point(int x, int y) { }

// 使用
Point p = new Point(1, 2);
System.out.println(p.x());  // 1
System.out.println(p.y());  // 2

// 自动生成:
// - 构造方法
// - getter 方法 (x(), y())
// - equals()
// - hashCode()
// - toString()
```

### 带方法的 Record

```java
// 带方法的 Record
public record Rectangle(int width, int height) {
    // 紧凑构造方法
    public Rectangle {
        if (width <= 0 || height <= 0) {
            throw new IllegalArgumentException();
        }
    }

    // 自定义方法
    public int area() {
        return width * height;
    }
}
```

### Record Patterns (JDK 21)

```java
// Record 模式匹配
record Point(int x, int y) { }

static void printPoint(Object obj) {
    if (obj instanceof Point(int x, int y)) {
        System.out.println("x=" + x + ", y=" + y);
    }
}

// 嵌套模式
record Circle(Point center, int radius) { }

static void printCircle(Object obj) {
    if (obj instanceof Circle(Point(int x, int y), int r)) {
        System.out.println("Center: (" + x + ", " + y + "), Radius: " + r);
    }
}
```

---

## 8. Sealed Classes

**JDK 15 预览, JDK 17 正式 (JEP 409)**

### 基础 Sealed Class

```java
// 密封类 - 控制继承
public sealed class Shape
    permits Circle, Rectangle, Triangle {

    public abstract double area();
}

// 允许的子类
public final class Circle extends Shape {
    private final double radius;
    public Circle(double radius) { this.radius = radius; }
    public double area() { return Math.PI * radius * radius; }
}

public final class Rectangle extends Shape {
    private final double width, height;
    public Rectangle(double width, double height) {
        this.width = width;
        this.height = height;
    }
    public double area() { return width * height; }
}

public final class Triangle extends Shape {
    private final double base, height;
    public Triangle(double base, double height) {
        this.base = base;
        this.height = height;
    }
    public double area() { return 0.5 * base * height; }
}
```

### Sealed Interface

```java
// 密封接口
public sealed interface Vehicle
    permits Car, Truck, Motorcycle {

    String getType();
}

// 实现类可以是 final 或 sealed
public final class Car implements Vehicle {
    public String getType() { return "Car"; }
}
```

### 与模式匹配结合

```java
// Sealed Classes + Pattern Matching
public double calculateArea(Shape shape) {
    return switch (shape) {
        case Circle(double r) -> Math.PI * r * r;
        case Rectangle(double w, double h) -> w * h;
        case Triangle(double b, double h) -> 0.5 * b * h;
        // 编译器确保所有子类都被覆盖
    };
}
```

---

## 9. 模式匹配

### instanceof 模式匹配

**JDK 14 预览, JDK 16 正式 (JEP 394)**

```java
// 传统方式
if (obj instanceof String) {
    String str = (String) obj;
    System.out.println(str.length());
}

// 模式匹配方式 (JDK 16+)
if (obj instanceof String str) {
    System.out.println(str.length());
}

// 嵌套模式
if (obj instanceof String s && s.length() > 5) {
    System.out.println(s);
}
```

### Switch 表达式

**JDK 12 预览, JDK 14 预览, JDK 14 正式 (JEP 361)**

```java
// 传统 switch 语句
int result;
switch (day) {
    case MONDAY:
    case FRIDAY:
    case SUNDAY:
        result = 6;
        break;
    case TUESDAY:
        result = 7;
        break;
    default:
        result = 0;
}

// Switch 表达式 (JDK 14+)
int result = switch (day) {
    case MONDAY, FRIDAY, SUNDAY -> 6;
    case TUESDAY -> 7;
    default -> 0;
};

// 带标签的 switch
int result = switch (day) {
    case MONDAY, FRIDAY, SUNDAY -> {
        System.out.println("Midday");
        yield 6;
    }
    default -> 0;
};
```

### 模式匹配 for Switch

**JDK 17 预览, JDK 18 第二次预览, JDK 19 第三次预览, JDK 21 正式 (JEP 441)**

```java
// 类型模式匹配
static String formatter(Object obj) {
    return switch (obj) {
        case Integer i -> String.format("int %d", i);
        case Long l    -> String.format("long %d", l);
        case Double d  -> String.format("double %f", d);
        case String s  -> String.format("String %s", s);
        default        -> obj.toString();
    };
}

// 守卫模式 (JDK 23+)
static String formatterWithGuard(Object obj) {
    return switch (obj) {
        case String s when s.length() > 5 -> "Long string: " + s;
        case String s -> "Short string: " + s;
        default -> obj.toString();
    };
}
```

### 原始类型模式

**JDK 26 第四次预览 (JEP 530)**

```java
// 原始类型模式匹配 (JDK 26+)
switch (value) {
    case int i -> System.out.println("int: " + i);
    case long l -> System.out.println("long: " + l);
    case double d -> System.out.println("double: " + d);
    default -> System.out.println("other");
}
```

---

## 10. 最新增强

### JDK 23: Switch Guards

**JEP 456: Unnamed Patterns and Variables (Preview)**

```java
// 守卫子句 - when 关键字
String result = switch (obj) {
    case String s when s.length() > 5 -> "Long string";
    case String s -> "Short string";
    case Integer i when i > 0 -> "Positive integer";
    case Integer i -> "Non-positive integer";
    default -> "Unknown";
};
```

### JDK 26: 模块导入

**JEP 511: Module Import Declarations**

```java
// 导入整个模块
import module java.base;

void main() {
    List<String> list = new ArrayList<>();  // 无需单独导入
}
```

### JDK 26: 紧凑源文件

**JEP 512: Compact Source Files and Instance Main Methods**

```java
// 最简形式 - Hello.java
void main() {
    println("Hello, World!");
}

// 或带参数
void main(String[] args) {
    println("Hello " + args[0]);
}
```

### JDK 26: Lazy Constants

**JEP 526: Lazy Constants (Second Preview)**

```java
// 延迟初始化常量
private static lazy ExpensiveObject CACHE = new ExpensiveObject();

// 首次访问时初始化
// 线程安全
// 性能优于双重检查锁
```

---

## 11. 重要 PR 分析

### 枚举优化

#### JDK-8349400: 消除匿名内部类优化启动

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐ 减少 10 个类加载，元空间占用减少 82%

将 `KnownOIDs` 枚举中的匿名内部类转换为构造函数参数：

**核心改进**:
- 消除 10 个匿名内部类
- 减少启动时的类加载开销
- 元空间占用减少 82%

```java
// 优化前：使用匿名内部类覆盖方法
KP_TimeStamping("1.3.6.1.5.5.7.3.8", "timeStamping") {
    @Override
    boolean registerNames() { return false; }
}

// 优化后：使用构造函数参数
KP_TimeStamping("1.3.6.1.5.5.7.3.8", "timeStamping", false),
```

→ [详细分析](/by-pr/8349/8349400.md)

### Lambda 表达式优化

#### JDK-8341755: Lambda 参数名称生成优化

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐ +15-20% Lambda 生成性能

优化 `InnerClassLambdaMetafactory` 的参数名称构造：

**优化点**:
- 0 参数 Lambda 使用常量（消除数组分配）
- 缓存常见参数名称（1-8 参数）
- 使用 `@Stable` 注解启用 JIT 优化

```java
// 优化前：每次创建新数组
String[] argNames = new String[parameterCount];
for (int i = 0; i < parameterCount; i++) {
    argNames[i] = "arg$" + (i + 1);  // 字符串拼接
}

// 优化后：使用缓存
private static final @Stable String[] ARG_NAME_CACHE;
static {
    var argNameCache = new String[8];
    for (int i = 0; i < 8; i++) {
        argNameCache[i] = "arg$" + (i + 1);
    }
    ARG_NAME_CACHE = argNameCache;
}
```

→ [详细分析](/by-pr/8341/8341755.md)

---

## 12. 语法特性最佳实践

### 枚举设计优化

```java
// ✅ 推荐：避免匿名内部类
enum Operation {
    ADD, SUBTRACT, MULTIPLY, DIVIDE;

    // 使用枚举实例字段替代方法覆盖
    private final boolean isBinary;

    Operation() {
        this.isBinary = true;
    }

    // 或使用构造函数参数控制行为
    enum SpecialEnum {
        VALUE1("oid1", false),  // registerNames = false
        VALUE2("oid2", true);   // registerNames = true

        private final String oid;
        private final boolean registerNames;

        SpecialEnum(String oid, boolean registerNames) {
            this.oid = oid;
            this.registerNames = registerNames;
        }
    }
}

// ❌ 避免：不必要的匿名内部类
enum BadEnum {
    VALUE {
        @Override
        void someMethod() { }  // 匿名类增加类加载开销
    };
}
```

### Lambda 表达式最佳实践

```java
// ✅ 推荐：使用方法引用
list.stream()
    .map(Object::toString)  // 比 lambda 更高效
    .filter(Objects::nonNull);

// ✅ 推荐：使用标准函数式接口
Function<String, Integer> parser = Integer::parseInt;
Predicate<Integer> isPositive = n -> n > 0;
Supplier<List<String>> supplier = ArrayList::new;

// ❌ 避免：不必要的 lambda 语法
list.stream()
    .map(s -> s.toString())  // 方法引用更清晰
    .filter(s -> s != null); // Objects::nonNull 更标准
```

### 泛型最佳实践

```java
// ✅ 推荐：使用泛型方法避免类型转换
public static <T> List<T> singletonList(T item) {
    return Collections.singletonList(item);
}

// ✅ 推荐：使用通配符提高 API 灵活性
public void processList(List<? extends Number> list) {
    // 只能读取，不能写入
    Number first = list.get(0);
}

// ❌ 避免：不必要的类型参数
public <T> void print(T item) {  // T 可以用 Object 替代
    System.out.println(item);
}
```

---

## 13. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 语法特性 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Joe Darcy | 11 | Oracle | 类型系统, 语法 |
| 2 | Vicente Romero | 7 | Oracle | javac 编译器 |
| 3 | Pavel Rappo | 2 | Oracle | API 设计 |
| 4 | Julia Boes | 2 | Oracle | Records |
| 5 | Jonathan Gibbons | 2 | Oracle | javac |

---

## 14. 相关链接

### 内部文档

- [语法时间线](timeline.md) - 详细的历史演进
- [字符串处理](../string/) - String 演进
- [反射与元数据](../reflection/) - 反射 API
- [Class File API](../classfile/) - 字节码操作

### 外部资源

- [JEP 395](/jeps/language/jep-395.md)
- [JEP 394](/jeps/language/jep-394.md)
- [JEP 409: Sealed Classes](https://openjdk.org/jeps/409)
- [JEP 441](/jeps/language/jep-441.md)
- [JEP 440](/jeps/language/jep-440.md)
- [JEP 456](/jeps/language/jep-456.md)
- [JEP 530](/jeps/language/jep-530.md)
- [JEP 511](/jeps/tools/jep-511.md)
- [JEP 512](/jeps/language/jep-512.md)
- [JEP 526](/jeps/tools/jep-526.md)

### Git 仓库

```bash
# 查看语法相关提交
git log --oneline -- src/java.base/share/classes/java/lang/
git log --oneline -- src/jdk.compiler/share/classes/com/sun/tools/javac/
```

---

**最后更新**: 2026-03-20

**Sources**:
- [JEP 395](/jeps/language/jep-395.md)
- [JEP 409: Sealed Classes](https://openjdk.org/jeps/409)
- [JEP 441](/jeps/language/jep-441.md)
- [JEP 530](/jeps/language/jep-530.md)
- [Records Sealed Classes Pattern Matching](https://blog.csdn.net/qq_42055933/article/details/156172037)
- [Java 8 to 17 New Features Guide](https://medium.com/@shankar.singla1709/from-java-8-to-17-a-comprehensive-guide-to-new-features-354759b59350)
