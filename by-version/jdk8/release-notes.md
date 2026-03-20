# JDK 8 发布说明

> **版本类型**: LTS (长期支持) | **发布日期**: 2014-03-18 | **支持截止**: 2030-12 (付费)

[![OpenJDK](https://img.shields.io/badge/OpenJDK-8-orange)](https://openjdk.org/projects/jdk8/)
[![License](https://img.shields.io/badge/License-GPLv2--with--Classpath--Exception-blue)](https://openjdk.org/projects/jdk8/)

---

## 概述

JDK 8 是 Java 历史上最重要的版本之一，引入了 **Lambda 表达式**、**Stream API**、**Date/Time API** 等革命性特性，彻底改变了 Java 编程风格。

---

## 语言特性

### Lambda 表达式 (JSR 335) ⭐⭐⭐

**状态**: 正式发布
**概述**: 引入 Lambda 表达式，支持函数式编程。

```java
// 之前：匿名内部类
Runnable r1 = new Runnable() {
    @Override
    public void run() {
        System.out.println("Hello!");
    }
};

// 现在：Lambda 表达式
Runnable r2 = () -> System.out.println("Hello!");

// 带参数的 Lambda
Comparator<String> comparator = (s1, s2) -> s1.compareTo(s2);

// 方法引用
List<String> list = Arrays.asList("a", "b", "c");
list.forEach(System.out::println);

// 构造函数引用
Supplier<List<String>> supplier = ArrayList::new;
```

---

### Default Methods (JSR 335) ⭐

**状态**: 正式发布
**概述**: 接口支持默认方法实现。

```java
public interface Collection<E> extends Iterable<E> {
    // 新方法，提供默认实现
    default void forEach(Consumer<? super E> action) {
        Objects.requireNonNull(action);
        for (E t : this) {
            action.accept(t);
        }
    }

    default Spliterator<E> spliterator() {
        return Spliterators.spliterator(this, 0);
    }
}
```

---

### Type Annotations (JSR 308)

**状态**: 正式发布
**概述**: 类型注解，允许在任何使用类型的地方添加注解。

```java
// 泛型类型参数
List<@NonNull String> strings;

// 类型转换
String s = (@NonNull String) obj;

// implements
class MyList implements List<@NonNull String> { }

// 异常声明
void monitor() throws @Critical Exception { }
```

---

### Repeating Annotations (JSR 337)

**状态**: 正式发布
**概述**: 重复注解，允许在同一位置使用多个相同的注解。

```java
@Schedule(day = "Mon")
@Schedule(day = "Wed")
@Schedule(day = "Fri")
void runTask() { }
```

---

## 核心库

### Stream API (JSR 335) ⭐⭐⭐

**状态**: 正式发布
**概述**: Stream API，支持函数式数据处理。

```java
// 创建 Stream
Stream<String> stream = list.stream();
Stream<Integer> infinite = Stream.iterate(0, n -> n + 1);

// 中间操作
Stream<String> filtered = stream.filter(s -> s.length() > 3);
Stream<String> mapped = stream.map(String::toUpperCase);
Stream<String> sorted = stream.sorted();

// 终端操作
Optional<String> first = stream.findFirst();
long count = stream.count();
List<String> result = stream.collect(Collectors.toList());

// 实际示例
List<Person> people = getPeople();

// 过滤和收集
List<String> adultNames = people.stream()
    .filter(p -> p.getAge() >= 18)
    .map(Person::getName)
    .sorted()
    .collect(Collectors.toList());

// 分组
Map<Integer, List<Person>> byAge = people.stream()
    .collect(Collectors.groupingBy(Person::getAge));

// 并行处理
long count = people.parallelStream()
    .filter(p -> p.getAge() > 30)
    .count();
```

---

### Date/Time API (JSR 310) ⭐⭐

**状态**: 正式发布
**概述**: 全新的日期时间 API，替代 `Date` 和 `Calendar`。

```java
import java.time.*;
import java.time.format.*;

// LocalDate - 日期
LocalDate date = LocalDate.now();
LocalDate birthday = LocalDate.of(1990, 3, 15);
LocalDate nextWeek = date.plusWeeks(1);

// LocalTime - 时间
LocalTime time = LocalTime.now();
LocalTime meeting = LocalTime.of(14, 30);

// LocalDateTime - 日期时间
LocalDateTime dateTime = LocalDateTime.now();
LocalDateTime appointment = LocalDateTime.of(2024, 3, 15, 14, 30);

// ZonedDateTime - 带时区
ZonedDateTime zoned = ZonedDateTime.now(ZoneId.of("Asia/Shanghai"));

// Instant - 时间戳
Instant instant = Instant.now();
long epochMilli = instant.toEpochMilli();

// Duration - 时间间隔
Duration duration = Duration.between(startTime, endTime);

// Period - 日期间隔
Period period = Period.between(startDate, endDate);

// 格式化
DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
String formatted = dateTime.format(formatter);
LocalDateTime parsed = LocalDateTime.parse("2024-03-15 14:30:00", formatter);
```

---

### Optional ⭐

**状态**: 正式发布
**概述**: Optional 类，优雅处理空值。

```java
import java.util.Optional;

// 创建 Optional
Optional<String> opt1 = Optional.of("Hello");       // 非空
Optional<String> opt2 = Optional.ofNullable(value); // 可空
Optional<String> opt3 = Optional.empty();           // 空

// 使用 Optional
Optional<String> name = getName();
String result = name.orElse("default");
String result2 = name.orElseGet(() -> computeDefault());
String result3 = name.orElseThrow(() -> new RuntimeException());

// 链式调用
String upper = name
    .filter(s -> s.length() > 3)
    .map(String::toUpperCase)
    .orElse("");

// ifPresent
name.ifPresent(System.out::println);

// ifPresentOrElse
name.ifPresentOrElse(
    System.out::println,
    () -> System.out.println("Empty")
);
```

---

### CompletableFuture ⭐

**状态**: 正式发布
**概述**: CompletableFuture，支持异步编程。

```java
// 创建 CompletableFuture
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
    return computeResult();
});

// 链式调用
CompletableFuture<Integer> result = future
    .thenApply(String::length)
    .thenApply(len -> len * 2);

// 组合多个 Future
CompletableFuture<String> future1 = CompletableFuture.supplyAsync(() -> "Hello");
CompletableFuture<String> future2 = CompletableFuture.supplyAsync(() -> "World");

CompletableFuture<String> combined = future1
    .thenCombine(future2, (s1, s2) -> s1 + " " + s2);

// 等待完成
String value = combined.get(1, TimeUnit.SECONDS);

// 异常处理
CompletableFuture<String> handled = future
    .exceptionally(ex -> "Error: " + ex.getMessage());
```

---

## 安全

### Nashorn JavaScript Engine

**状态**: 正式发布
**概述**: 新的 JavaScript 引擎，替代 Rhino。

```java
import javax.script.*;

ScriptEngine engine = new ScriptEngineManager()
    .getEngineByName("nashorn");

// 执行 JavaScript
engine.eval("print('Hello from JavaScript!')");

// 调用 JavaScript 函数
engine.eval("function add(a, b) { return a + b; }");
Invocable invocable = (Invocable) engine;
Number result = (Number) invocable.invokeFunction("add", 1, 2);
```

---

## JVM 改进

### PermGen 移除

**状态**: 正式发布
**概述**: 移除永久代 (PermGen)，引入 Metaspace。

```bash
# 之前 (JDK 7)
-XX:PermSize=256m -XX:MaxPermSize=512m

# 现在 (JDK 8)
-XX:MetaspaceSize=256m -XX:MaxMetaspaceSize=512m
```

**优势**:
- Metaspace 使用本地内存，不占用堆内存
- 默认无上限，更灵活
- 减少内存溢出问题

---

### G1 GC 增强

**状态**: 正式发布
**概述**: G1 GC 成为成熟的垃圾收集器。

```bash
# 启用 G1 GC
java -XX:+UseG1GC MyApp

# G1 配置
-XX:MaxGCPauseMillis=200       # 最大暂停时间
-XX:G1HeapRegionSize=16m       # Region 大小
-XX:InitiatingHeapOccupancyPercent=45  # 触发并发标记的堆占用率
```

---

## 其他特性

### String.join()

```java
String joined = String.join(", ", "a", "b", "c");  // "a, b, c"
String joined = String.join("-", list);             // "a-b-c"
```

### Base64 编解码

```java
import java.util.Base64;

String encoded = Base64.getEncoder().encodeToString(bytes);
byte[] decoded = Base64.getDecoder().decode(encoded);

// URL 安全编码
String urlEncoded = Base64.getUrlEncoder().encodeToString(bytes);
```

### 方法参数名反射

```java
// 编译时需要添加 -parameters 参数
javac -parameters MyClass.java

// 运行时获取参数名
Method method = MyClass.class.getMethod("myMethod", String.class, int.class);
Parameter[] params = method.getParameters();
for (Parameter param : params) {
    System.out.println(param.getName());
}
```

---

## 特性汇总

| 类别 | 特性 | 说明 |
|------|------|------|
| **语言** | Lambda 表达式 | 函数式编程支持 |
| | Default Methods | 接口默认方法 |
| | Type Annotations | 类型注解 |
| | Repeating Annotations | 重复注解 |
| **核心库** | Stream API | 函数式数据处理 |
| | Date/Time API | 全新日期时间 API |
| | Optional | 空值处理 |
| | CompletableFuture | 异步编程 |
| | Nashorn | JavaScript 引擎 |
| | Base64 | 编解码 |
| **JVM** | Metaspace | 替代 PermGen |
| | G1 GC 增强 | 更成熟的 G1 |

---

## 升级建议

### 从 JDK 7 升级

JDK 8 与 JDK 7 具有良好的二进制兼容性：

```bash
# 直接替换 JDK 版本即可
java -version
# java version "1.8.0_xxx"
```

### 推荐使用的新特性

| 场景 | 推荐特性 |
|------|----------|
| 数据处理 | Stream API |
| 日期时间 | Date/Time API |
| 空值处理 | Optional |
| 异步编程 | CompletableFuture |
| 集合遍历 | Lambda + forEach |

### 代码迁移示例

```java
// 之前 (JDK 7)
List<String> filtered = new ArrayList<>();
for (String s : list) {
    if (s.length() > 3) {
        filtered.add(s.toUpperCase());
    }
}
Collections.sort(filtered);

// 现在 (JDK 8)
List<String> filtered = list.stream()
    .filter(s -> s.length() > 3)
    .map(String::toUpperCase)
    .sorted()
    .collect(Collectors.toList());
```

---

## 性能改进

| 领域 | 改进 |
|------|------|
| JVM | Metaspace 使用本地内存 |
| GC | G1 GC 更成熟稳定 |
| Stream | 并行流利用多核 |
| Lambda | 调用点优化 |

---

## 相关链接

- [OpenJDK JDK 8 项目页面](https://openjdk.org/projects/jdk8/)
- [Java SE 8 文档](https://docs.oracle.com/javase/8/docs/)
- [GitHub: openjdk/jdk8](https://github.com/openjdk/jdk8)
- [JDK 8 迁移指南](/by-version/jdk8/migration/)
