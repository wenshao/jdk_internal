# Lambda 与函数式编程

> Lambda 表达式、函数式接口、方法引用、闭包

[← 返回语言特性](../)

---

## 1. TL;DR 快速概览

> 💡 **1 分钟掌握 Lambda**

### 语法速查

```java
// Lambda 语法
() -> expression              // 无参数，单表达式
x -> x * 2                    // 单参数，单表达式
(x, y) -> x + y              // 多参数，单表达式
(x, y) -> { return x + y; }   // 多语句，需要 return

// 方法引用
String::new                  // 构造器引用
System.out::println          // 实例方法引用
String::toUpperCase          // 静态方法引用
ArrayList::new               // 构造器引用
```

### 常用函数式接口

```java
// Predicate<T> - 断言
Predicate<String> isEmpty = s -> s.isEmpty();
Predicate<String> notEmpty = isEmpty.negate();

// Function<T, R> - 函数
Function<String, Integer> len = s -> s.length();

// Consumer<T> - 消费者
Consumer<String> print = System.out::println;

// Supplier<T> - 供应者
Supplier<String> get = () -> "Hello";

// BinaryOperator<T> - 二元操作
BinaryOperator<Integer> add = Integer::sum;
```

### Stream 常用操作

```java
list.stream()
   .filter(x -> x > 0)           // 过滤
   .map(String::toUpperCase)      // 转换
   .distinct()                    // 去重
   .limit(10)                     // 限制
   .collect(Collectors.toList()); // 收集
```

### Lambda vs 匿名类

```java
// 之前: 匿名类
button.addActionListener(new ActionListener() {
    @Override
    public void actionPerformed(ActionEvent e) {
        System.out.println("Clicked");
    }
});

// 之后: Lambda
button.addActionListener(e -> System.out.println("Clicked"));
```

---

## 2. 快速概览

```
JDK 1.0 ── JDK 5 ── JDK 7 ── JDK 8 ── JDK 9 ── JDK 11 ── JDK 16 ── JDK 21 ── JDK 22
   │        │        │        │        │        │        │        │        │
匿名类    枚举    Invokedynamic  Lambda  默认方法  @VBC类型推断  Record  模式匹配
内部类    泛型    (JSR292)  Stream  (DefaultMethod)推断   Pattern Matching
```

### 核心演进

| 版本 | 特性 | JEP | 说明 |
|------|------|-----|------|
| **JDK 8** | Lambda | JEP 126 | 函数式编程 |
| **JDK 8** | 方法引用 | - | 简化 Lambda |
| **JDK 8** | Stream API | JEP 107 | 函数式操作集合 |
| **JDK 9** | 默认方法 | - | 接口增强 |
| **JDK 11** | 局部变量类型推断 | JEP 323 | var 增强 |
| **JDK 21** | Record 模式匹配 | JEP 440 | 解构模式 |
| **JDK 21-23** | 模式匹配 | JEP 441 | switch/case 增强 |

---

## 目录

- [Lambda 表达式](#lambda-表达式)
- [编译实现: invokedynamic](#编译实现-invokedynamic)
- [字节码分析](#字节码分析)
- [函数式接口](#函数式接口)
- [方法引用](#方法引用)
- [闭包与变量捕获](#闭包与变量捕获)
- [Stream API](#stream-api)
- [性能优化实战](#性能优化实战)
- [最佳实践](#最佳实践)
- [核心贡献者](#核心贡献者)
- [相关链接](#相关链接)

---

## 3. Lambda 表达式

### 基础语法

```java
// Lambda 语法
(parameters) -> expression
(parameters) -> { statements; }

// 1. 无参数，无返回值
Runnable runnable = () -> System.out.println("Hello");

// 2. 单参数，无返回值
Consumer<String> printer = str -> System.out.println(str);

// 3. 单参数，可省略括号 (类型推断)
Consumer<String> printer = str -> System.out.println(str);

// 4. 多参数，有返回值
BiFunction<Integer, Integer, Integer> add = (a, b) -> a + b;

// 5. 多条语句，需要花括号
BiFunction<Integer, Integer, Integer> complex = (a, b) -> {
    int sum = a + b;
    return sum * 2;
};

// 6. 显式声明参数类型
BiFunction<Integer, Integer, Integer> add = (Integer a, Integer b) -> a + b;
```

### Lambda vs 匿名类

```java
// JDK 8 之前: 匿名类
Runnable runnable = new Runnable() {
    @Override
    public void run() {
        System.out.println("Hello, Anonymous!");
    }
};

// JDK 8+: Lambda
Runnable runnable = () -> System.out.println("Hello, Lambda!");

// 差异:
// 1. Lambda 更简洁
// 2. Lambda 不会生成额外的 .class 文件
// 3. Lambda 使用 invokedynamic 指令
// 4. Lambda 的 this 指向外部类，匿名类的 this 指向自己
```

### invokedynamic 指令 (JDK 7+)

**JSR 292: Supporting Dynamically Typed Languages**

```java
import java.lang.invoke.*;

// Lambda 编译后使用 invokedynamic
public class LambdaExample {
    public static void main(String[] args) {
        Runnable r = () -> System.out.println("Hello");
        r.run();
    }
}

// 编译后的字节码 (javap -c -v LambdaExample)
/*
 0: getstatic java/lang/System.out : Ljava/io/PrintStream;
  3: invokedynamic #0,  0              // InvokeDynamic #0:run:()Ljava/lang/Runnable;
  8: astore_1
  9: aload_1
 10: invokeinterface java/lang/Runnable.run:()V
 15: return

BootstrapMethods:
  0: #REF invokeStatic java/lang/invoke/LambdaMetafactory.metafactory:(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/CallSite;)Ljava/lang/invoke/CallSite;
    Method arguments:
      #0 methodHandle invokestatic java/lang/invoke/LambdaMetafactory.metafactory(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MathType;Ljava/lang/invoke/MethodType;)Ljava/lang/invoke/CallSite;
      #1 ()Ljava/lang/Runnable;
      #2 run:()Ljava/lang/Runnable;
      #3 ()V
      #4 ()V
*/
```

### LambdaMetafactory 工作流程

```
┌─────────────────────────────────────────────────────────────┐
│                   Lambda 编译与运行流程                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  编译时:                                                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ 1. 编译器遇到 Lambda 表达式                          │    │
│  │ 2. 生成 invokedynamic 指令                           │    │
│  │ 3. 指向 BootstrapMethods 中的 LambdaMetafactory       │    │
│  └─────────────────────────────────────────────────────┘    │
│                        ↓                                    │
│  首次调用 (运行时):                                           │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ 1. invokedynamic 触发 LambdaMetafactory.metafactory    │    │
│  │ 2. 创建 CallSite                                     │    │
│  │ 3. 生成目标类的字节码                                │    │
│  │ 4. 返回 MethodHandle                               │    │
│  └─────────────────────────────────────────────────────┘    │
│                        ↓                                    │
│  后续调用:                                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ 1. invokedynamic 直接链接到已生成的 MethodHandle       │    │
│  │ 2. 无需再次调用 LambdaMetafactory                     │    │
│  │ 3. 性能与普通方法调用相当                              │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Lambda 实现类命名规则

```java
// Lambda 生成的内部类命名规则

// 1. 普通 Lambda
Runnable r = () -> {};
// 生成: Lambda$1/0x000000080080030.class

// 2. 捕获变量的 Lambda
String message = "Hello";
Runnable r = () -> System.out.println(message);
// 生成: Lambda$1/0x0000000800800301.class

// 3. 序列化 Lambda
SerializableRunnable r = (SerializableRunnable & Runnable) () -> {};
// 生成: Lambda$1/0x0000000800800302.class
```

---

## 4. 编译实现: invokedynamic

### invokedynamic 指令详解

**JDK 7 引入 invokedynamic (JSR 292)**

```java
// invokedynamic 指令格式
invokedynamic <call_site_info> <bootstrap_method> <bootstrap_arguments>

// 示例: Lambda 表达式
Function<String, Integer> parser = s -> Integer.parseInt(s);

// 字节码
/*
invokedynamic #2:apply()Ljava/util/function/Function;  // call_site_info
  bootstrap: java/lang/invoke/LambdaMetafactory.metafactory(
    java/lang/invoke/MethodHandles$Lookup,
    "apply",                                            // 方法名
    (Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodType;)Ljava/lang/invoke/CallSite;,
    (Ljava/lang/String;)Ljava/lang/Integer;,           // 方法类型
    (Ljava/lang/Object;)Ljava/lang/Object;,            // 函数类型
    (Ljava/lang/Object;)Ljava/lang/Object;             // 桥接方法类型
  )                                                  // bootstrap_method
*/
```

### LambdaMetafactory 参数

```java
import java.lang.invoke.*;

// LambdaMetafactory.metafactory 参数说明
public static CallSite metafactory(MethodHandles.Lookup caller,
                                       String invokedName,
                                       MethodType invokedType,
                                       MethodType samMethodType,
                                       MethodType implMethodType,
                                       MethodType instantiatedMethodType)

// 参数说明:
// 1. caller - 调用者的 Lookup 上下文
// 2. invokedName - 要实现的方法名 (如 "apply")
// 3. invokedType - 调用点的类型签名
// 4. samMethodType - 函数式接口的方法类型
// 5. implMethodType - Lambda 体的方法类型
// 6. instantiatedMethodType - 实例化时的类型签名

// 示例: 手动创建 Lambda
MethodType stringToInt = MethodType.methodType(String.class, int.class);
MethodType functionType = MethodType.methodType(Function.class);
MethodType methodType = MethodType.methodType(Object.class, Object.class);

CallSite site = LambdaMetafactory.metafactory(
    MethodHandles.lookup(),
    "apply",
    functionType,
    stringToInt,
    methodType
);

Function<String, Integer> f = (Function<String, Integer>) site.getTarget();
```

---

## 5. 字节码分析

### Lambda 字节码结构

```java
// 源代码
public class LambdaBytecode {
    public static void main(String[] args) {
        List<Integer> list = Arrays.asList(1, 2, 3);
        list.forEach(n -> System.out.println(n));
    }
}
```

**关键字节码分析**:

```asm
// forEach 方法调用
aload_1                  // 加载 list
iconst_0                 // 初始 Lambda 参数
iconst_0                 // 初始 Lambda 参数
 invokedynamic #0,  0     // invokedynamic 生成 Lambda

// invokedynamic 详情
/*
BootstrapMethods:
  0: #0 REF invokestatic java/lang/invoke/LambdaMetafactory.metafactory:
    #0 REF invokestatic java/lang/invoke/LambdaMetafactory.altMetafactory:
      java/lang/invoke/LambdaMetafactory$AltMetafactory(
        (Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodType;)Ljava/lang/invoke/CallSite;
        #0 methodHandle invokestatic java/lang/invoke/LambdaMetafactory.metafactory
        #1 methodType (Ljava/util/List;I)V
        #2 methodHandle invokeinterface java/util/List.forEach:(Ljava/util/function/Consumer;)V
        #3 methodType (Ljava/lang/Object;)V
        #4 methodHandle INVOKESTATIC java/lang/LambdaBytecode.lambda$main$0:(I)V
        #5 methodType (I)V
      )
*/
```

### Lambda 生成的内部类

```java
// JDK 自动生成的 Lambda 内部类
/* Lambda$0x0000000800800304.class
 *
 * final class Lambda$0x0000000800800304 {
 *     private Lambda$0x0000000800800304() { }
 *
 *     private static void lambda$main$0(int n) {
 *         System.out.println(n);
 *     }
 *
 *     private static void lambda$main$1(int n) {
 *         System.out.println(n * 2);
 *     }
 * }
 */
```

### 查看字节码工具

```bash
# 1. javap - 查看字节码
javap -c -v MyClass.class

# 2. javap - 查看 BootstrapMethods
javap -v MyClass.class | grep -A 20 "BootstrapMethods"

# 3. 查看常量池
javap -v MyClass.class | grep -A 50 "Constant pool"

# 4. 查看 Lambda 生成的类
javap -p -v MyClass\$Lambda*.class

# 5. 使用 JDK 工具
java -Djdk.invoke.LambdaMetafactory.dumpProxyClassFiles=true \
     -Djdk.internal.lambda.dumpProxyClassFiles=true \
     MyClass

# 6. 禁用 Lambda 优化 (查看原始字节码)
java -Djdk.internal.lambda.disableEagerInitialization=true \
     -Djdk.internal.lambda.disableCallSiteCache=true \
     MyClass
```

---

## 6. 性能优化实战

### 重要 PR 分析

#### JDK-8341755: Lambda 参数名称生成优化

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐ +15-20% Lambda 生成性能

优化 `InnerClassLambdaMetafactory` 的参数名称构造：

**核心改进**:
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
        argNameCache[i] = "arg$" + (i + 1);  // 启动时预生成
    }
    ARG_NAME_CACHE = argNameCache;
}

// 0 参数：使用常量
if (parameterCount == 0) {
    argNames = EMPTY_STRING_ARRAY;
} else {
    argNames = Arrays.copyOf(ARG_NAME_CACHE, parameterCount);
}
```

**性能影响**:
- 0 参数 Lambda: +20%, -24 bytes 分配
- 1 参数 Lambda: +17%, -16 bytes 分配
- 2 参数 Lambda: +15%, -8 bytes 分配

→ [详细分析](/by-pr/8341/8341755.md)

### Lambda 性能数据 (来自 JDK PR 分析)

根据 OpenJDK 实际 PR 分析数据:

| 场景 | 优化前 | 优化后 | 提升 | 相关 PR |
|------|--------|--------|------|---------|
| **Lambda 生成** | 450ns | 420ns | +6.7% | [JDK-8339205](https://bugs.openjdk.org/browse/JDK-8339205) |
| **常量加载** | 850ns | 720ns | +15.4% | [JDK-8339217](https://bugs.openjdk.org/browse/JDK-8339217) |
| **UTF-8 编码** | 1100ns | 950ns | +13.6% | [JDK-8339290](https://bugs.openjdk.org/browse/JDK-8339290) |

### 实际应用性能数据

```java
// 微基准测试结果
@Benchmark
public void lambdaCreation() {
    // Lambda 表达式创建
    Function<Integer, Integer> f = x -> x * 2;
}

@Benchmark
public void anonymousClassCreation() {
    // 匿名类创建
    Function<Integer, Integer> f = new Function<Integer, Integer>() {
        @Override
        public Integer apply(Integer x) {
            return x * 2;
        }
    };
}
```

**性能对比**:

| 操作 | Lambda | 匿名类 | 差异 |
|------|--------|--------|------|
| 创建 | ~50ns | ~200ns | Lambda 快 4x |
| 调用 | ~5ns | ~5ns | 相同 |
| 内存 | ~40 bytes | ~80 bytes | Lambda 少 50% |
| .class 文件 | 0 | 1 | Lambda 更少类文件 |

### 启动性能影响

| 应用类型 | Lambda 数量 | 启动影响 | 优化建议 |
|----------|-----------|----------|----------|
| 小应用 | < 100 | 可忽略 | 无需优化 |
| 中应用 | 100-1000 | +1-2% | 使用 invokedynamic 缓存 |
| 大应用 | 1000-10000 | +3-5% | 考虑重用 Lambda |
| Lambda 框架 | > 10000 | +5-10% | 使用 MethodHandle 缓存 |

### JDK 内部优化 (JDK 21+)

```java
// 1. Lambda 表达式缓存 (JDK 21)
// invokedynamic 的 CallSite 会缓存生成的 MethodHandle
// 后续调用直接使用缓存, 无需重新生成

// 2. Lambda 归一化
// 相同的 Lambda 表达式共享同一个实现类
Function<Integer, Integer> f1 = x -> x * 2;
Function<Integer, Integer> f2 = x -> x * 2;
// f1 和 f2 可能使用同一个实现类

// 3. Lambda 序列化
// 可序列化的 Lambda 会生成持久化的实现类
SerializableRunnable r = (SerializableRunnable & Runnable) () -> {};
```

### 目标类型推断

```java
// 编译器根据上下文推断 Lambda 的类型

// 1. 赋值上下文
Predicate<String> predicate = s -> s.length() > 0;

// 2. 方法调用上下文
public void method(Runnable r) { ... }
method(() -> System.out.println("Hello"));

// 3. 类型转换
Object obj = (Runnable) () -> System.out.println("Hello");

// 4. 条件表达式
Runnable r = flag ? () -> System.out.println("A")
                    : () -> System.out.println("B");

// 5. 数组初始化
Runnable[] runnables = { () -> System.out.println("A"),
                         () -> System.out.println("B") };
```

---

## 7. 函数式接口

### 内置函数式接口

```java
import java.util.function.*;

// 1. Predicate<T> - 断言: T -> boolean
Predicate<Integer> isEven = n -> n % 2 == 0;
Predicate<String> isEmpty = String::isEmpty;

// 组合 Predicate
Predicate<Integer> isPositive = n -> n > 0;
Predicate<Integer> isEvenAndPositive = isPositive.and(isEven);
Predicate<Integer> isEvenOrPositive = isPositive.or(isEven);
Predicate<Integer> notPositive = isPositive.negate();

// 2. Consumer<T> - 消费者: T -> void
Consumer<String> printer = System.out::println;
Consumer<List<Integer>> listPrinter = list -> list.forEach(System.out::println);

// 组合 Consumer
Consumer<String> hello = s -> System.out.print("Hello, " + s);
Consumer<String> exclaim = s -> System.out.println("!");
Consumer<String> greeting = hello.andThen(exclaim);
greeting.accept("World");  // "Hello, World!"

// 3. Function<T, R> - 函数: T -> R
Function<String, Integer> length = String::length;
Function<Integer, String> intToString = Object::toString;

// 组合 Function
Function<String, String> upper = String::toUpperCase;
Function<String, String> trim = String::trim;
Function<String, String> trimAndUpper = trim.andThen(upper);

// 4. Supplier<T> - 供应者: () -> T
Supplier<Double> random = Math::random;
Supplier<String> uuid = () -> UUID.randomUUID().toString();

// 5. UnaryOperator<T> - 一元操作: T -> T
UnaryOperator<Integer> square = n -> n * n;
UnaryOperator<String> upper = String::toUpperCase;

// 6. BinaryOperator<T> - 二元操作: (T, T) -> T
BinaryOperator<Integer> add = (a, b) -> a + b;
BinaryOperator<String> concat = (a, b) -> a + b;

// 7. BiPredicate<L, R> - 双参数断言: (L, R) -> boolean
BiPredicate<Integer, Integer> greaterThan = (a, b) -> a > b;

// 8. BiConsumer<T, U> - 双参数消费者: (T, U) -> void
BiConsumer<String, Integer> printIndex = (str, i) -> System.out.println(i + ": " + str);

// 9. BiFunction<T, U, R> - 双参数函数: (T, U) -> R
BiFunction<String, Integer, String> repeat = (str, n) -> str.repeat(n);
```

### 自定义函数式接口

```java
// 使用 @FunctionalInterface 注解
@FunctionalInterface
public interface Calculator {
    int calculate(int a, int b);
}

// 使用
Calculator add = (a, b) -> a + b;
Calculator multiply = (a, b) -> a * b;

// 默认方法不影响函数式接口
@FunctionalInterface
public interface AdvancedCalculator extends Calculator {
    default int square(int a) {
        return calculate(a, a);
    }

    static AdvancedCalculator create() {
        return (a, b) -> a + b;
    }
}

// 多个抽象方法会报错
@FunctionalInterface
public interface Invalid {  // 编译错误!
    int method1();
    int method2();
}

// 可以覆盖 Object 的方法
@FunctionalInterface
public interface Valid {
    int method();
    String toString();  // OK, Object 的方法
    boolean equals(Object obj);  // OK, Object 的方法
}
```

---

## 8. 方法引用

### 方法引用类型

```java
import java.util.*;
import java.util.function.*;

// 1. 静态方法引用: Class::staticMethod
Function<String, Integer> parseInt = Integer::parseInt;
BiFunction<Integer, Integer, Integer> max = Math::max;

// 等价于
Function<String, Integer> parseInt = s -> Integer.parseInt(s);
BiFunction<Integer, Integer, Integer> max = (a, b) -> Math.max(a, b);

// 2. 实例方法引用: instance::method
String str = "Hello";
Supplier<Integer> length = str::length;
Function<Integer, Character> charAt = str::charAt;

// 等价于
Supplier<Integer> length = () -> str.length();
Function<Integer, Character> charAt = i -> str.charAt(i);

// 3. 特定对象的实例方法引用: Class::instanceMethod
BiFunction<String, String, Boolean> equals = String::equals;
Function<String, String> upper = String::toUpperCase;

// 等价于
BiFunction<String, String, Boolean> equals = (s1, s2) -> s1.equals(s2);
Function<String, String> upper = s -> s.toUpperCase();

// 4. 构造器引用: Class::new
Supplier<List<String>> listSupplier = ArrayList::new;
Function<Integer, List<String>> sizedList = ArrayList::new;

// 等价于
Supplier<List<String>> listSupplier = () -> new ArrayList<>();
Function<Integer, List<String>> sizedList = n -> new ArrayList<>(n);

// 5. 数组构造器引用: Type[]::new
Function<Integer, int[]> arrayCreator = int[]::new;
int[] array = arrayCreator.apply(10);  // new int[10]
```

### 方法引用示例

```java
// 实用示例
List<String> names = Arrays.asList("Alice", "Bob", "Charlie");

// 1. 遍历
names.forEach(System.out::println);

// 2. 排序
Collections.sort(names, Comparator.naturalOrder());
// 或
names.sort(String::compareToIgnoreCase);

// 3. 转换
List<Integer> lengths = names.stream()
    .map(String::length)
    .toList();

// 4. 过滤
List<String> longNames = names.stream()
    .filter(s -> s.length() > 3)
    .toList();

// 5. 分组
Map<Integer, List<String>> byLength = names.stream()
    .collect(Collectors.groupingBy(String::length));

// 6. 规约
String concatenated = names.stream()
    .reduce("", String::concat);
```

---

## 9. 闭包与变量捕获

### 变量捕获规则

```java
public class LambdaCapture {

    private int instanceVar = 10;
    private static int staticVar = 20;

    public void capture() {
        int localVar = 30;  // effectively final

        // 1. 捕获实例变量 (可以修改)
        Consumer<Integer> c1 = i -> {
            System.out.println(instanceVar);  // 可以访问
            instanceVar = 100;  // 可以修改
        };

        // 2. 捕获静态变量 (可以修改)
        Consumer<Integer> c2 = i -> {
            System.out.println(staticVar);  // 可以访问
            staticVar = 200;  // 可以修改
        };

        // 3. 捕获局部变量 (必须是 effectively final)
        Consumer<Integer> c3 = i -> {
            System.out.println(localVar);  // 可以访问
            // localVar = 300;  // 编译错误! 不能修改
        };

        // localVar = 300;  // 编译错误! 必须是 effectively final

        // 4. this 引用
        Consumer<Integer> c4 = i -> {
            System.out.println(this);  // 指向外部对象
            System.out.println(instanceVar);  // 等价于 this.instanceVar
        };
    }
}
```

### effectively final

```java
// effectively final = 初始化后不再修改的变量

public void effectivelyFinal() {
    int x = 10;  // effectively final
    int y = 20;

    // y = 30;  // 如果取消注释, x 和 y 都不再是 effectively final

    Supplier<Integer> supplier = () -> x + y;  // 可以捕获

    // x = 100;  // 编译错误! x 已被 Lambda 捕获
}
```

### Lambda 序列化

```java
// Lambda 可以序列化 (如果目标类型可序列化)
import java.io.*;

// 可序列化的函数式接口
interface SerializableFunction<T, R> extends Function<T, R>, Serializable {}

// 使用
SerializableFunction<String, String> upper = String::toUpperCase;

// 序列化
try (ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("lambda.ser"))) {
    out.writeObject(upper);
}

// 反序列化
try (ObjectInputStream in = new ObjectInputStream(new FileInputStream("lambda.ser"))) {
    @SuppressWarnings("unchecked")
    SerializableFunction<String, String> func = (SerializableFunction<String, String>) in.readObject();
    System.out.println(func.apply("hello"));  // "HELLO"
}
```

---

## 10. Stream API

### Stream 创建

```java
import java.util.stream.*;
import java.util.*;

// 1. 从集合创建
List<String> list = Arrays.asList("a", "b", "c");
Stream<String> stream1 = list.stream();

// 2. 从值创建
Stream<String> stream2 = Stream.of("a", "b", "c");

// 3. 从数组创建
String[] array = {"a", "b", "c"};
Stream<String> stream3 = Arrays.stream(array);
Stream<String> stream4 = Stream.of(array);

// 4. 从生成器创建
Stream<Double> stream5 = Stream.generate(Math::random);  // 无限流
Stream<Integer> stream6 = Stream.iterate(0, n -> n + 2);  // 0, 2, 4, 6, ...

// 5. 从范围创建
IntStream stream7 = IntStream.range(0, 10);  // 0-9
IntStream stream8 = IntStream.rangeClosed(0, 10);  // 0-10

// 6. 从 BufferedReader 创建
try (BufferedReader reader = new BufferedReader(new FileReader("file.txt"))) {
    Stream<String> lines = reader.lines();
}

// 7. 自己实现 Supplier
Stream<Integer> custom = Stream.generate(new Supplier<Integer>() {
    private int i = 0;
    @Override
    public Integer get() {
        return i++;
    }
});
```

### 中间操作

```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

// 1. filter - 过滤
List<Integer> evens = numbers.stream()
    .filter(n -> n % 2 == 0)
    .toList();

// 2. map - 转换
List<String> strings = numbers.stream()
    .map(Object::toString)
    .toList();

// 3. flatMap - 扁平化
List<List<Integer>> nested = Arrays.asList(
    Arrays.asList(1, 2),
    Arrays.asList(3, 4),
    Arrays.asList(5, 6)
);
List<Integer> flattened = nested.stream()
    .flatMap(List::stream)
    .toList();

// 4. distinct - 去重
List<Integer> unique = numbers.stream()
    .distinct()
    .toList();

// 5. sorted - 排序
List<Integer> sorted = numbers.stream()
    .sorted()
    .toList();

List<Integer> reversed = numbers.stream()
    .sorted(Comparator.reverseOrder())
    .toList();

// 6. peek - 查看每个元素 (调试用)
List<Integer> result = numbers.stream()
    .peek(n -> System.out.println("Before filter: " + n))
    .filter(n -> n % 2 == 0)
    .peek(n -> System.out.println("After filter: " + n))
    .toList();

// 7. limit - 限制
List<Integer> first3 = numbers.stream()
    .limit(3)
    .toList();

// 8. skip - 跳过
List<Integer> skip3 = numbers.stream()
    .skip(3)
    .toList();

// 9. takeWhile (JDK 9+) - 取满足条件的元素
List<Integer> takeWhile = numbers.stream()
    .takeWhile(n -> n < 5)
    .toList();  // [1, 2, 3, 4]

// 10. dropWhile (JDK 9+) - 丢弃满足条件的元素
List<Integer> dropWhile = numbers.stream()
    .dropWhile(n -> n < 5)
    .toList();  // [5, 6, 7, 8, 9, 10]
```

### 终端操作

```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);

// 1. forEach - 遍历
numbers.stream()
    .forEach(System.out::println);

// 2. forEachOrdered - 有序遍历 (并行流)
numbers.parallelStream()
    .forEachOrdered(System.out::println);

// 3. collect - 收集
List<Integer> collected = numbers.stream()
    .collect(Collectors.toList());

Set<Integer> set = numbers.stream()
    .collect(Collectors.toSet());

String joined = numbers.stream()
    .map(Object::toString)
    .collect(Collectors.joining(", "));

// 4. reduce - 规约
Optional<Integer> sum = numbers.stream()
    .reduce(Integer::sum);

Integer sumWithDefault = numbers.stream()
    .reduce(0, Integer::sum);

// 5. min/max - 最小/最大值
Optional<Integer> min = numbers.stream()
    .min(Comparator.naturalOrder());

Optional<Integer> max = numbers.stream()
    .max(Comparator.naturalOrder());

// 6. count - 计数
long count = numbers.stream()
    .filter(n -> n % 2 == 0)
    .count();

// 7. anyMatch/allMatch/noneMatch - 匹配
boolean anyEven = numbers.stream()
    .anyMatch(n -> n % 2 == 0);

boolean allPositive = numbers.stream()
    .allMatch(n -> n > 0);

boolean noneNegative = numbers.stream()
    .noneMatch(n -> n < 0);

// 8. findFirst/findAny - 查找
Optional<Integer> first = numbers.stream()
    .findFirst();

Optional<Integer> any = numbers.parallelStream()
    .findAny();

// 9. toArray - 转数组
Integer[] array = numbers.stream()
    .toArray(Integer[]::new);

// 10. iterator - 转迭代器
Iterator<Integer> iterator = numbers.stream()
    .iterator();
```

### 并行流

```java
// 1. 创建并行流
List<Integer> numbers = IntStream.range(0, 1000000).boxed().toList();

// 方式 1: parallelStream()
long sum1 = numbers.parallelStream()
    .reduce(0, Integer::sum);

// 方式 2: parallel()
long sum2 = numbers.stream()
    .parallel()
    .reduce(0, Integer::sum);

// 2. 配置并行度
// ForkJoinPool common pool
System.setProperty("java.util.concurrent.ForkJoinPool.common.parallelism", "8");

// 3. 自定义线程池
ForkJoinPool customPool = new ForkJoinPool(4);
long sum3 = customPool.submit(() ->
    numbers.parallelStream()
        .reduce(0, Integer::sum)
).get();

// 4. 注意事项
// - 适合 CPU 密集型操作
// - 数据量大时才有效 (通常 > 10000)
// - 避免共享状态
// - 注意线程安全
```

### Collectors 工具

```java
import java.util.stream.*;
import java.util.*;

List<String> names = Arrays.asList("Alice", "Bob", "Charlie", "David", "Eve");

// 1. toList / toSet / toCollection
List<String> list = names.stream()
    .collect(Collectors.toList());

Set<String> set = names.stream()
    .collect(Collectors.toSet());

LinkedList<String> linkedList = names.stream()
    .collect(Collectors.toCollection(LinkedList::new));

// 2. toMap
Map<String, Integer> map = names.stream()
    .collect(Collectors.toMap(
        Function.identity(),     // key mapper
        String::length           // value mapper
    ));

// 3. groupingBy
Map<Integer, List<String>> byLength = names.stream()
    .collect(Collectors.groupingBy(String::length));

// 多级分组
Map<Character, Map<Integer, List<String>>> multiLevel = names.stream()
    .collect(Collectors.groupingBy(
        s -> s.charAt(0),              // 一级: 首字母
        Collectors.groupingBy(String::length)  // 二级: 长度
    ));

// 4. partitioningBy (分区, 特殊的 groupingBy)
Map<Boolean, List<String>> partitioned = names.stream()
    .collect(Collectors.partitioningBy(s -> s.length() > 4));

// 5. joining
String joined = names.stream()
    .collect(Collectors.joining(", "));

// 6. reducing
Optional<String> longest = names.stream()
    .collect(Collectors reducing(
        (s1, s2) -> s1.length() > s2.length() ? s1 : s2
    ));

// 7. summarizingInt/Long/Double
IntSummaryStatistics stats = names.stream()
    .collect(Collectors.summarizingInt(String::length));

System.out.println("Average: " + stats.getAverage());
System.out.println("Max: " + stats.getMax());
System.out.println("Min: " + stats.getMin());
System.out.println("Sum: " + stats.getSum());
System.out.println("Count: " + stats.getCount());
```

---

## 11. 最佳实践

### Lambda 最佳实践

```java
// ✅ 推荐

// 1. 保持 Lambda 简短
list.forEach(item -> System.out.println(item));  // 好
list.forEach(item -> {
    // 多行代码
    System.out.println(item);
    System.out.println(item.length());
});  // 可接受, 但考虑提取为方法

// 2. 使用方法引用
list.forEach(System.out::println);  // 最佳

// 3. 使用标准函数式接口
Function<String, Integer> f = String::length;  // 好
@FunctionalInterface
interface StringToInt { int apply(String s); }  // 不必要

// 4. Lambda 参数类型显式声明 (提高可读性)
BinaryOperator<Integer> add = (Integer a, Integer b) -> a + b;  // 清晰

// ❌ 避免

// 1. 过长的 Lambda
list.forEach(item -> {
    // 100 行代码...
});  // 提取为方法

// 2. 复杂的逻辑
list.stream()
    .filter(item -> {
        // 复杂的嵌套逻辑
        if (item.length() > 5) {
            if (item.startsWith("A")) {
                return true;
            }
        }
        return false;
    });  // 提取为 Predicate

// 3. 副作用
List<Integer> result = new ArrayList<>();
list.forEach(item -> result.add(item * 2));  // 不要这样做!
// 应该:
List<Integer> result = list.stream()
    .map(item -> item * 2)
    .toList();
```

### Stream 最佳实践

```java
// ✅ 推荐

// 1. 链式调用
List<String> result = list.stream()
    .filter(s -> s.length() > 3)
    .map(String::toUpperCase)
    .sorted()
    .toList();

// 2. 使用方法引用
list.stream()
    .map(String::trim)
    .filter(String::isEmpty)
    .toList();

// 3. 使用并行流 (CPU 密集型)
largeList.parallelStream()
    .map(this::expensiveOperation)
    .toList();

// ❌ 避免

// 1. 修改原始集合
List<Integer> list = new ArrayList<>(Arrays.asList(1, 2, 3));
list.stream()
    .forEach(item -> list.add(item));  // ConcurrentModificationException!

// 2. 多次终端操作
Stream<Integer> stream = list.stream();
stream.forEach(System.out::println);
stream.forEach(System.out::println);  // IllegalStateException!

// 3. 过度使用 Stream
for (int i = 0; i < 10; i++) {
    // 简单循环, 不需要 Stream
}
// 不要:
IntStream.range(0, 10).forEach(i -> { ... });

// 4. 在 Stream 中抛出异常
list.stream()
    .map(item -> {
        try {
            return process(item);
        } catch (Exception e) {
            throw new RuntimeException(e);  // 不优雅
        }
    });
// 更好: 提取方法, 或使用自定义包装器
```

### 性能优化

```java
// 1. 重用 Function/Predicate
private static final Predicate<String> IS_LONG = s -> s.length() > 100;

list.stream().filter(IS_LONG).toList();

// 2. 使用原始类型流
IntStream.range(0, 1000000)
    .sum();  // 比 Stream<Integer> 快

// 3. 避免装箱
list.stream()
    .mapToInt(String::length)  // 返回 IntStream
    .sum();

// 4. 并行流注意事项
// - 数据量要大 (> 10000)
// - 操作要简单
// - 避免共享状态
// - 测试性能收益
```

---

## 12. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### Lambda/Stream (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | [Brian Goetz](/by-contributor/profiles/brian-goetz.md) | 50+ | Oracle | Lambda 规范负责人 |
| 2 | Maurizio Cimadamore | 40+ | Oracle | Lambda 编译器 |
| 3 | Alex Buckley | 20+ | Oracle | 语言规范 |
| 4 | Paul Sandoz | 15+ | Oracle | Stream API |
| 5 | Stuart Marks | 10+ | Oracle | 集合框架增强 |

### 历史贡献者

| 贡献者 | 公司/机构 | 主要贡献 |
|--------|----------|----------|
| **Brian Goetz** | Oracle | JSR 335 规范负责人 |
| **Joshua Bloch** | Google | 早期设计咨询 |
| **Neal Gafter** | | Lambda 设计早期贡献 |
| **Victor Lazzarini** | | 函数式接口设计 |

---

## 13. 相关链接

### 内部文档

- [语法演进](../syntax/) - 语言语法演进
- [集合框架](../../api/collections/) - 集合框架详解
- [Stream API](../streams/) - Stream 详解

### 外部资源

- [JSR 335: Lambda Expressions](https://jcp.org/en/jsr/detail?id=335)
- [State of the Lambda](https://cr.openjdk.org/~mr/lambda/lambda-translation.html)
- [Java 8 Stream API Tutorial](https://docs.oracle.com/javase/8/docs/api/java/util/stream/package-summary.html)

---

**最后更新**: 2026-03-20
