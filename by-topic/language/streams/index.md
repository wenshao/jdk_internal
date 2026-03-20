# Stream API 详解

> 函数式数据处理、流式操作、并行处理

[← 返回语言特性](../)

---

## 快速概览

```
JDK 1.0 ── JDK 5 ── JDK 8 ── JDK 9 ── JDK 16 ── JDK 21
   │        │        │        │        │        │
集合循环   增强 for  Stream  takeWhile  toList   gatherers
迭代器    foreach  lambda  dropWhile  (JEP)   (JEP)
```

### 核心演进

| 版本 | 特性 | JEP | 说明 |
|------|------|-----|------|
| **JDK 8** | Stream API | JEP 107 | 函数式集合操作 |
| **JDK 9** | takeWhile/dropWhile | - | 惰性操作增强 |
| **JDK 9** | iterate 重载 | - | 支持 Predicate |
| **JDK 9** | ofNullable | - | 空 Stream 处理 |
| **JDK 16** | toList() | - | 简化收集 |
| **JDK 21** | Gatherers (预览) | JEP 461 | 自定义中间操作 |

---

## 目录

- [Stream 基础](#stream-基础)
- [中间操作](#中间操作)
- [终端操作](#终端操作)
- [Collectors](#collectors)
- [并行流](#并行流)
- [原始类型流](#原始类型流)
- [Gatherers (JDK 21+)](#gatherers-jdk-21)
- [最佳实践](#最佳实践)
- [核心贡献者](#核心贡献者)
- [相关链接](#相关链接)

---

## Stream 基础

### Stream 特性

```java
// Stream 特性:
// 1. 不存储数据
// 2. 不修改源数据
// 3. 惰性执行
// 4. 只能消费一次

// 创建 Stream
import java.util.stream.*;

// 1. 从集合
List<String> list = Arrays.asList("a", "b", "c");
Stream<String> stream1 = list.stream();
Stream<String> parallelStream = list.parallelStream();

// 2. 从值
Stream<String> stream2 = Stream.of("a", "b", "c");
Stream<String> stream3 = Stream.empty();  // 空 Stream

// 3. 从数组
String[] array = {"a", "b", "c"};
Stream<String> stream4 = Arrays.stream(array);
Stream<String> stream5 = Stream.of(array);

// 4. 从生成器
Stream<Double> stream6 = Stream.generate(Math::random);  // 无限
Stream<Integer> stream7 = Stream.iterate(0, n -> n + 2);  // 0, 2, 4, ...

// 5. 从范围 (JDK 8)
IntStream range1 = IntStream.range(0, 10);  // 0-9
IntStream range2 = IntStream.rangeClosed(0, 10);  // 0-10

// 6. 从 Builder (JDK 8)
Stream<String> builder = Stream.<String>builder()
    .add("a")
    .add("b")
    .add("c")
    .build();

// 7. 从文件 (JDK 8)
try (Stream<String> lines = Files.lines(Paths.get("file.txt"))) {
    lines.forEach(System.out::println);
}

// 8. 拆分字符串 (JDK 8)
"hello world".lines().forEach(System.out::println);
```

### Stream 流水线

```java
// Stream 操作分类:
// 1. 中间操作 (Intermediate) - 返回 Stream, 惰性执行
// 2. 终端操作 (Terminal) - 返回非 Stream 结果, 立即执行

List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

// 典型流水线
List<Integer> result = numbers.stream()
    .filter(n -> n % 2 == 0)      // 中间操作
    .map(n -> n * 2)               // 中间操作
    .limit(3)                      // 中间操作
    .toList();                     // 终端操作

// 结果: [4, 8, 12]
// 流程: 1,2,3,4,5,6,7,8,9,10 → 2,4,6,8,10 → 4,8,12,16,20 → 4,8,12
```

---

## 中间操作

### filter 和 map

```java
// filter - 过滤元素
Stream<Integer> s1 = Stream.of(1, 2, 3, 4, 5)
    .filter(n -> n % 2 == 0);  // [2, 4]

// map - 转换元素
Stream<String> s2 = Stream.of(1, 2, 3)
    .map(Object::toString);  // ["1", "2", "3"]

// mapToInt/Long/Double - 避免装箱
IntStream s3 = Stream.of("a", "bb", "ccc")
    .mapToInt(String::length);  // [1, 2, 3]

// flatMap - 扁平化嵌套结构
List<List<Integer>> nested = Arrays.asList(
    Arrays.asList(1, 2),
    Arrays.asList(3, 4),
    Arrays.asList(5, 6)
);

Stream<Integer> flattened = nested.stream()
    .flatMap(List::stream);  // [1, 2, 3, 4, 5, 6]

// flatMapToInt/Long/Double
List<String> strings = Arrays.asList("1,2", "3,4", "5,6");
IntStream numbers = strings.stream()
    .flatMapToInt(s -> {
        String[] parts = s.split(",");
        return Arrays.stream(parts)
            .mapToInt(Integer::parseInt);
    });  // [1, 2, 3, 4, 5, 6]
```

### 转换操作

```java
// distinct - 去重 (基于 equals)
Stream.of(1, 2, 2, 3, 3, 3)
    .distinct();  // [1, 2, 3]

// sorted - 排序
Stream.of(3, 1, 4, 1, 5)
    .sorted();  // [1, 1, 3, 4, 5]

Stream.of("banana", "apple", "cherry")
    .sorted(Comparator.comparingInt(String::length));  // [apple, banana, cherry]

// peek - 调试操作 (查看每个元素)
List<Integer> result = Stream.of(1, 2, 3)
    .peek(n -> System.out.println("Before map: " + n))
    .map(n -> n * 2)
    .peek(n -> System.out.println("After map: " + n))
    .toList();
// Before map: 1
// After map: 2
// Before map: 2
// After map: 4
// Before map: 3
// After map: 6
```

### 截断操作

```java
// limit - 限制元素数量
Stream.of(1, 2, 3, 4, 5)
    .limit(3);  // [1, 2, 3]

// skip - 跳过元素
Stream.of(1, 2, 3, 4, 5)
    .skip(2);  // [3, 4, 5]

// takeWhile (JDK 9+) - 取满足条件的元素
Stream.of(1, 2, 3, 4, 5, 1, 2)
    .takeWhile(n -> n < 4);  // [1, 2, 3]

// dropWhile (JDK 9+) - 丢弃满足条件的元素
Stream.of(1, 2, 3, 4, 5, 1, 2)
    .dropWhile(n -> n < 4);  // [4, 5, 1, 2]
```

---

## 终端操作

### 遍历与查找

```java
// forEach - 遍历 (不保证顺序)
Stream.of(1, 2, 3)
    .forEach(System.out::println);

// forEachOrdered - 有序遍历
Stream.of(3, 1, 2)
    .unordered()
    .forEachOrdered(System.out::println);  // 3, 1, 2

// findFirst - 查找第一个元素
Optional<Integer> first = Stream.of(3, 1, 2)
    .findFirst();  // Optional[3]

// findAny - 查找任意元素 (并行流更快)
Optional<Integer> any = Stream.of(3, 1, 2)
    .findAny();  // Optional[3] (可能是任意)
```

### 匹配操作

```java
// anyMatch - 任意匹配
boolean hasEven = Stream.of(1, 2, 3)
    .anyMatch(n -> n % 2 == 0);  // true

// allMatch - 全部匹配
boolean allPositive = Stream.of(1, 2, 3)
    .allMatch(n -> n > 0);  // true

// noneMatch - 全部不匹配
boolean noneNegative = Stream.of(1, 2, 3)
    .noneMatch(n -> n < 0);  // true

// 短路操作
boolean result = Stream.of(1, 2, 3, 4, 5)
    .peek(n -> System.out.println("Checking: " + n))
    .anyMatch(n -> n > 3);
// 只打印: Checking: 1, Checking: 2, Checking: 3, Checking: 4
```

### 规约操作

```java
// reduce - 规约为一个值

// 1. 无初始值
Optional<Integer> sum = Stream.of(1, 2, 3, 4, 5)
    .reduce(Integer::sum);  // Optional[15]

// 2. 有初始值
Integer sum = Stream.of(1, 2, 3, 4, 5)
    .reduce(0, Integer::sum);  // 15

// 3. 更复杂的规约
String result = Stream.of("a", "b", "c")
    .reduce("", (s1, s2) -> s1 + "," + s2);  // ",a,b,c"

// 4. 并行安全的规约 (combiner)
Integer sumParallel = Stream.of(1, 2, 3, 4, 5)
    .parallel()
    .reduce(0,
        Integer::sum,      // accumulator
        Integer::sum);     // combiner

// 5. 计算字符串总长度
int totalLength = Stream.of("hello", "world", "java")
    .reduce(0,
        (len, str) -> len + str.length(),   // accumulator
        Integer::sum);                      // combiner
```

### 收集操作

```java
// collect - 收集结果

// 1. 转集合
List<String> list = Stream.of("a", "b", "c")
    .collect(Collectors.toList());

Set<String> set = Stream.of("a", "b", "c")
    .collect(Collectors.toSet());

// 2. 转特定集合
LinkedList<String> linkedList = Stream.of("a", "b", "c")
    .collect(Collectors.toCollection(LinkedList::new));

// 3. 转数组
String[] array = Stream.of("a", "b", "c")
    .toArray(String[]::new);

// 4. 转字符串
String joined = Stream.of("a", "b", "c")
    .collect(Collectors.joining(", "));  // "a, b, c"

// 5. 转 Map
Map<String, Integer> map = Stream.of("a", "bb", "ccc")
    .collect(Collectors.toMap(
        Function.identity(),     // key mapper
        String::length            // value mapper
    ));  // {a=1, bb=2, ccc=3}

// 6. 分组
Map<Integer, List<String>> grouped = Stream.of("a", "bb", "ccc", "dd")
    .collect(Collectors.groupingBy(String::length));
// {1=[a], 2=[bb, dd], 3=[ccc]}

// 7. 分区
Map<Boolean, List<String>> partitioned = Stream.of("a", "bb", "ccc", "dd")
    .collect(Collectors.partitioningBy(s -> s.length() > 2));
// {false=[a, bb, dd], true=[ccc]}
```

---

## Collectors

### 分组与分区

```java
import java.util.stream.*;
import java.util.*;

List<String> words = Arrays.asList("apple", "banana", "cherry", "date", "elderberry");

// 1. 简单分组
Map<Integer, List<String>> byLength = words.stream()
    .collect(Collectors.groupingBy(String::length));
// {5=[apple, date], 6=[banana, cherry], 9=[elderberry]}

// 2. 分组后计数
Map<Integer, Long> countByLength = words.stream()
    .collect(Collectors.groupingBy(
        String::length,
        Collectors.counting()
    ));
// {5=2, 6=2, 9=1}

// 3. 分组后转换值
Map<Integer, Set<String>> setByLength = words.stream()
    .collect(Collectors.groupingBy(
        String::length,
        Collectors.toSet()
    ));

// 4. 多级分组
Map<Character, Map<Integer, List<String>>> multiLevel = words.stream()
    .collect(Collectors.groupingBy(
        s -> s.charAt(0),           // 一级: 首字母
        Collectors.groupingBy(String::length)  // 二级: 长度
    ));

// 5. 分区 (特殊的分组, key 只有 true/false)
Map<Boolean, List<String>> partitioned = words.stream()
    .collect(Collectors.partitioningBy(s -> s.length() > 5));
// {false=[apple, date], true=[banana, cherry, elderberry]}
```

### 聚合操作

```java
// 1. 统计
IntSummaryStatistics stats = IntStream.range(1, 101)
    .summaryStatistics();

System.out.println("Count: " + stats.getCount());    // 100
System.out.println("Sum: " + stats.getSum());        // 5050
System.out.println("Average: " + stats.getAverage()); // 50.5
System.out.println("Min: " + stats.getMin());        // 1
System.out.println("Max: " + stats.getMax());        // 100

// 2. 求和
Integer sum = Stream.of(1, 2, 3, 4, 5)
    .collect(Collectors.summingInt(Integer::intValue));

// 3. 平均值
Double average = Stream.of(1, 2, 3, 4, 5)
    .collect(Collectors.averagingInt(Integer::intValue));

// 4. 最大/最小
Optional<String> max = Stream.of("apple", "banana", "cherry")
    .collect(Collectors.maxBy(Comparator.comparingInt(String::length)));

// 5. 规约
String concatenated = Stream.of("a", "b", "c")
    .collect(Collectors.reducing("", (s1, s2) -> s1 + s2));
```

### 自定义 Collector

```java
// 自定义 Collector 示例
import java.util.stream.*;
import java.util.*;

class CustomCollector {

    // 实现一个只保留前 N 个元素的 Collector
    public static <T> Collector<T, ?, List<T>> firstN(int n) {
        return Collector.of(
            () -> new ArrayList<T>(n),      // supplier
            (list, item) -> {               // accumulator
                if (list.size() < n) {
                    list.add(item);
                }
            },
            (list1, list2) -> {             // combiner
                List<T> result = new ArrayList<>(n);
                result.addAll(list1);
                for (T item : list2) {
                    if (result.size() >= n) break;
                    result.add(item);
                }
                return result;
            },
            Collector.Characteristics.IDENTITY_FINISH
        );
    }

    public static void main(String[] args) {
        List<Integer> result = IntStream.range(0, 1000)
            .boxed()
            .collect(firstN(5));
        System.out.println(result);  // [0, 1, 2, 3, 4]
    }
}
```

---

## 并行流

### 创建并行流

```java
import java.util.concurrent.*;

// 1. parallelStream()
List<Integer> list = IntStream.range(0, 1000000).boxed().toList();
long sum = list.parallelStream()
    .reduce(0, Integer::sum);

// 2. parallel()
long sum2 = IntStream.range(0, 1000000)
    .parallel()
    .sum();

// 3. 自定义 ForkJoinPool
ForkJoinPool customPool = new ForkJoinPool(4);
long sum3 = customPool.submit(() ->
    list.parallelStream()
        .reduce(0, Integer::sum)
).get();
```

### 并行流特性

```java
// 并行流特点:
// - 使用 ForkJoinPool.commonPool()
// - 默认线程数 = CPU 核心数
// - 适合 CPU 密集型操作
// - 数据量大时才有优势

// 1. 操作是无状态的
List<Integer> result = IntStream.range(0, 10000)
    .parallel()
    .filter(n -> n % 2 == 0)
    .boxed()
    .toList();

// 2. 避免共享可变状态
List<Integer> numbers = IntStream.range(0, 1000).boxed().toList();
List<Integer> result = new ArrayList<>();  // 不安全!

// ❌ 错误
numbers.parallelStream()
    .forEach(n -> result.add(n * 2));  // 并发问题!

// ✅ 正确
List<Integer> result = numbers.parallelStream()
    .map(n -> n * 2)
    .toList();

// 3. 注意顺序
List<Integer> unordered = IntStream.range(0, 100)
    .parallel()
    .boxed()
    .collect(Collectors.toList());  // 顺序不确定

List<Integer> ordered = IntStream.range(0, 100)
    .parallel()
    .boxed()
    .collect(Collectors.toCollection(ArrayList::new));  // 保证顺序
```

### 并行流性能

```java
// 何时使用并行流?

// ✅ 适合
// 1. 数据量大 (通常 > 10000)
// 2. 操作简单
// 3. CPU 密集型
// 4. 无共享状态

// ❌ 不适合
// 1. 数据量小
// 2. I/O 密集型
// 3. 操作复杂
// 4. 有共享状态

// 性能测试
public class ParallelPerformance {

    public static void main(String[] args) {
        List<Integer> data = IntStream.range(0, 10_000_000)
            .boxed()
            .toList();

        // 顺序流
        long start1 = System.nanoTime();
        long sum1 = data.stream()
            .mapToLong(n -> expensiveOperation(n))
            .sum();
        long time1 = System.nanoTime() - start1;

        // 并行流
        long start2 = System.nanoTime();
        long sum2 = data.parallelStream()
            .mapToLong(n -> expensiveOperation(n))
            .sum();
        long time2 = System.nanoTime() - start2;

        System.out.println("Sequential: " + time1 / 1_000_000 + "ms");
        System.out.println("Parallel: " + time2 / 1_000_000 + "ms");
        System.out.println("Speedup: " + (double) time1 / time2);
    }

    private static long expensiveOperation(int n) {
        // 模拟 CPU 密集操作
        return n * n;
    }
}
```

---

## 原始类型流

### 原始类型流类型

```java
// 避免装箱开销
// IntStream, LongStream, DoubleStream

// 1. 创建
IntStream range = IntStream.range(0, 100);
IntStream rangeClosed = IntStream.rangeClosed(0, 100);
IntStream of = IntStream.of(1, 2, 3);
IntStream generate = IntStream.generate(() -> ThreadLocalRandom.current().nextInt());
IntStream iterate = IntStream.iterate(0, n -> n + 2);

// 2. 从 Stream 转换
IntStream intStream = Stream.of("1", "2", "3")
    .mapToInt(Integer::parseInt);

LongStream longStream = Stream.of(1L, 2L, 3L)
    .mapToLong(Long::longValue);

DoubleStream doubleStream = Stream.of(1.0, 2.0, 3.0)
    .mapToDouble(Double::doubleValue);

// 3. 转回 Stream
Stream<Integer> boxed = IntStream.range(0, 10)
    .boxed();

// 4. 转数组
int[] array = IntStream.range(0, 10).toArray();

// 5. range vs rangeClosed
IntStream.range(0, 5).toArray();      // [0, 1, 2, 3, 4]
IntStream.rangeClosed(0, 5).toArray(); // [0, 1, 2, 3, 4, 5]
```

### 原始类型流操作

```java
// 1. 特有操作
IntStream.of(1, 2, 3, 4, 5)
    .summaryStatistics();  // IntSummaryStatistics

IntStream.of(1, 2, 3, 4, 5)
    .average();  // OptionalDouble[3.0]

IntStream.of(1, 2, 3, 4, 5)
    .max();  // OptionalInt[5]

IntStream.of(1, 2, 3, 4, 5)
    .min();  // OptionalInt[1]

IntStream.of(1, 2, 3, 4, 5)
    .sum();  // 15

// 2. 转换
IntStream.of(1, 2, 3)
    .asLongStream();   // LongStream

IntStream.of(1, 2, 3)
    .asDoubleStream(); // DoubleStream

IntStream.of(1, 2, 3)
    .boxed();          // Stream<Integer>

// 3. mapToObj
Stream<String> strings = IntStream.range(0, 5)
    .mapToObj(i -> "Num: " + i);

// 4. map (原始类型)
IntStream.of(1, 2, 3)
    .map(n -> n * 2);  // IntStream

// 5. flatMap
IntStream.range(1, 4)
    .flatMap(i -> IntStream.range(0, i));  // 0, 0,1, 0,1,2

// 6. iterate (JDK 8)
IntStream.iterate(0, n -> n + 2)
    .limit(10)
    .toArray();  // [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

// 7. iterate (JDK 9+)
IntStream.iterate(0, n -> n < 20, n -> n + 2)
    .toArray();  // [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

---

## Gatherers (JDK 21+)

**JEP 461: Gatherers (Preview)**

### Gatherer 基础

```java
// Gatherer 是 JDK 21 引入的预览特性
// 用于自定义中间操作

import java.util.stream.gather.*;

// 1. 内置 Gatherer

// fold - 折叠操作
List<Integer> runningSum = IntStream.rangeClosed(1, 5)
    .boxed()
    .gather(Gatherers.fold(
        () -> 0,               // 初始值
        (sum, value) -> sum + value,  // 累加器
        (sum1, sum2) -> sum1 + sum2   // 合并器
    ))
    .toList();

// scan - 扫描操作 (保留中间结果)
List<Integer> runningSums = IntStream.rangeClosed(1, 5)
    .boxed()
    .gather(Gatherers.scan(
        () -> 0,
        (sum, value) -> sum + value
    ))
    .toList();  // [1, 3, 6, 10, 15]

// windowSliding - 滑动窗口
List<List<Integer>> windows = IntStream.rangeClosed(1, 5)
    .boxed()
    .gather(Gatherers.windowSliding(3))
    .toList();  // [[1,2,3], [2,3,4], [3,4,5]]

// windowFixed - 固定窗口
List<List<Integer>> fixedWindows = IntStream.rangeClosed(1, 10)
    .boxed()
    .gather(Gatherers.windowFixed(3))
    .toList();  // [[1,2,3], [4,5,6], [7,8,9], [10]]
```

### 自定义 Gatherer

```java
// 自定义 Gatherer 接口
public interface Gatherer<T, A, R> {
    // 整合器
    interface Integrator<A, T> {
        boolean integrate(A state, T element);
    }

    // 下游
    @FunctionalInterface
    interface Downstream<R> {
        boolean push(R element);
    }

    // 创建 Gatherer
    static <T, A, R> Gatherer<T, ?, R> of(
        Supplier<A> initializer,
        Integrator<A, T> integrator,
        BinaryOperator<A> combiner,
        Function<A, R> finisher,
        Gatherer.Characteristics... characteristics
    ) { ... }
}

// 自定义 Gatherer 示例: 批处理
public class BatchGatherer {

    public static <T> Gatherer<T, List<T>, List<T>> ofSize(int batchSize) {
        return Gatherer.of(
            // initializer
            () -> new ArrayList<T>(batchSize),

            // integrator
            (batch, element, downstream) -> {
                batch.add(element);
                if (batch.size() >= batchSize) {
                    downstream.push(new ArrayList<>(batch));
                    batch.clear();
                }
                return true;  // 继续处理
            },

            // combiner
            (batch1, batch2) -> {
                batch1.addAll(batch2);
                return batch1;
            },

            // finisher
            batch -> {
                if (!batch.isEmpty()) {
                    return batch;
                }
                return Collections.emptyList();
            }
        );
    }

    public static void main(String[] args) {
        List<Integer> batches = IntStream.rangeClosed(1, 10)
            .boxed()
            .gather(BatchGatherer.ofSize(3))
            .flatMap(List::stream)
            .toList();

        System.out.println(batches);  // [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]
    }
}
```

---

## 最佳实践

### 性能优化

```java
// 1. 使用原始类型流避免装箱
// ❌ 慢
Stream<Integer> stream = IntStream.range(0, 1000000).boxed();
int sum = stream.mapToInt(Integer::intValue).sum();

// ✅ 快
int sum = IntStream.range(0, 1000000).sum();

// 2. 重用 Predicate/Function
private static final Predicate<String> IS_LONG = s -> s.length() > 100;

list.stream().filter(IS_LONG).toList();

// 3. 并行流谨慎使用
// 只有在大数据量 + CPU 密集型时才有效

// 4. 避免在 Stream 中进行外部修改
List<Integer> result = new ArrayList<>();
// ❌ 错误
list.stream().forEach(item -> result.add(process(item)));
// ✅ 正确
List<Integer> result = list.stream()
    .map(this::process)
    .toList();

// 5. 使用 toList() 而非 collect(Collectors.toList())
// JDK 16+
List<Integer> list1 = stream.toList();  // 更快, 不可变
List<Integer> list2 = stream.collect(Collectors.toList());  // 较慢, 可变
```

### 可读性

```java
// 1. 每个操作一行
List<String> result = list.stream()
    .filter(s -> s.length() > 3)
    .map(String::toUpperCase)
    .sorted()
    .toList();

// 2. 提取复杂 Lambda
// ❌ 难读
list.stream()
    .filter(s -> {
        if (s == null) return false;
        if (s.length() < 5) return false;
        if (s.startsWith("test")) return false;
        return true;
    })
    .toList();

// ✅ 清晰
private static boolean isValid(String s) {
    return s != null && s.length() >= 5 && !s.startsWith("test");
}

list.stream().filter(MyClass::isValid).toList();

// 3. 使用方法引用
list.stream()
    .map(String::trim)       // 而非 s -> s.trim()
    .filter(String::isEmpty) // 而非 s -> s.isEmpty()
    .toList();
```

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### Stream API (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Brian Goetz | 30+ | Oracle | Lambda/Stream 规范 |
| 2 | Paul Sandoz | 25+ | Oracle | Stream API 实现 |
| 3 | Stuart Marks | 15+ | Oracle | 集合框架 |
| 4 | Maurice Naftalin | | 技术写作 | Stream 指南 |

---

## 相关链接

### 内部文档

- [Lambda](../lambda/) - Lambda 表达式
- [集合框架](../../api/collections/) - 集合详解

### 外部资源

- [JEP 107: Collections](https://openjdk.org/jeps/107)
- [JEP 461: Gatherers](https://openjdk.org/jeps/461)
- [Stream API Javadoc](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/stream/package-summary.html)

---

**最后更新**: 2026-03-20
