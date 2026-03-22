# Stream Gatherers (JEP 485)

JDK 24 正式发布。Gatherers 是 Stream API 的扩展，
允许定义**自定义中间操作** (custom intermediate operations)，
弥补了 Stream API 只能通过 `Collector` 自定义终端操作的不足。

[← 返回 Project Amber 概览](index.md)

---

## 演进历程

```
JEP 461 (Preview)     JDK 22   Stream Gatherers 第一预览
    |
JEP 473 (2nd Preview) JDK 23   Stream Gatherers 第二预览
    |
JEP 485 (Final)       JDK 24   Stream Gatherers 正式发布
```

---

## 核心概念 (Core Concepts)

```java
// Stream 管道: source -> intermediate ops -> terminal op
// 内置中间操作: map, filter, flatMap, sorted, distinct, limit...
// 自定义终端操作: Collector (JDK 8)
// 自定义中间操作: Gatherer (JDK 24) <-- 新增！

// 使用方式: stream.gather(myGatherer)
// Gatherer 接口: Gatherer<T, A, R>
//   T = 输入元素类型 (input type)
//   A = 中间状态类型 (state type)
//   R = 输出元素类型 (output type)
```

---

## 内置 Gatherers (Built-in Gatherers)

```java
import java.util.stream.Gatherers;

// 1. windowFixed(int size) - 固定大小的窗口 (fixed-size window)
List<List<Integer>> windows = Stream.of(1, 2, 3, 4, 5, 6, 7)
    .gather(Gatherers.windowFixed(3))
    .toList();
// [[1, 2, 3], [4, 5, 6], [7]]

// 2. windowSliding(int size) - 滑动窗口 (sliding window)
List<List<Integer>> sliding = Stream.of(1, 2, 3, 4, 5)
    .gather(Gatherers.windowSliding(3))
    .toList();
// [[1, 2, 3], [2, 3, 4], [3, 4, 5]]

// 3. fold(init, folder) - 有状态的归约, 输出单个结果
// 类似 reduce, 但初始值可以是不同类型
Optional<String> csv = Stream.of("a", "b", "c")
    .gather(Gatherers.fold(() -> "", (acc, el) -> acc.isEmpty() ? el : acc + "," + el))
    .findFirst();
// "a,b,c"

// 4. scan(init, scanner) - 有状态的累积, 输出每步结果
// 类似 fold, 但每步都输出中间结果
List<Integer> runningSum = Stream.of(1, 2, 3, 4, 5)
    .gather(Gatherers.scan(() -> 0, Integer::sum))
    .toList();
// [1, 3, 6, 10, 15]

// 5. mapConcurrent(maxConcurrency, mapper) - 并发映射
// 自动使用虚拟线程, 限制最大并发数
List<String> results = urls.stream()
    .gather(Gatherers.mapConcurrent(10, url -> fetchContent(url)))
    .toList();
// 最多 10 个虚拟线程同时执行 fetchContent
```

---

## 自定义 Gatherer (Custom Gatherer)

```java
// Gatherer 由 4 个函数组成:
// 1. initializer  - 创建初始状态 (可选)
// 2. integrator   - 处理每个输入元素 (必需)
// 3. combiner     - 合并并行状态 (可选, 并行流需要)
// 4. finisher     - 处理最终状态 (可选)

// 示例 1: distinctBy - 按某个属性去重
static <T, K> Gatherer<T, ?, T> distinctBy(Function<T, K> keyExtractor) {
    return Gatherer.ofSequential(
        HashSet<K>::new,                         // initializer: 创建 Set 记录已见的 key
        (seen, element, downstream) -> {         // integrator
            K key = keyExtractor.apply(element);
            if (seen.add(key)) {                 // 如果 key 是新的
                return downstream.push(element); // 推送到下游
            }
            return true;                         // 继续处理 (返回 false 则短路)
        }
    );
}

// 使用
record Employee(String name, String dept) {}
var unique = employees.stream()
    .gather(distinctBy(Employee::dept))  // 每个部门只保留第一个
    .toList();

// 示例 2: takeWhileInclusive - 类似 takeWhile 但包含第一个不满足条件的元素
static <T> Gatherer<T, ?, T> takeWhileInclusive(Predicate<T> predicate) {
    return Gatherer.ofSequential(
        () -> new Object() { boolean done = false; },
        (state, element, downstream) -> {
            if (state.done) return false;        // 已结束, 短路
            if (!predicate.test(element)) {
                state.done = true;
            }
            return downstream.push(element);     // 包含不满足条件的那个元素
        }
    );
}

// 使用
var result = Stream.of(1, 2, 3, 10, 4, 5)
    .gather(takeWhileInclusive(n -> n < 10))
    .toList();
// [1, 2, 3, 10]  <-- 包含了 10

// 示例 3: 带 finisher 的 Gatherer - 批量收集后在结束时输出最后一批
static <T> Gatherer<T, ?, List<T>> batch(int size) {
    return Gatherer.ofSequential(
        ArrayList<T>::new,                       // initializer
        (buffer, element, downstream) -> {       // integrator
            buffer.add(element);
            if (buffer.size() >= size) {
                var batch = List.copyOf(buffer);
                buffer.clear();
                return downstream.push(batch);
            }
            return true;
        },
        (buffer, downstream) -> {                // finisher
            if (!buffer.isEmpty()) {
                downstream.push(List.copyOf(buffer));  // 输出最后不足 size 的一批
            }
        }
    );
}
```

---

## Gatherer 组合 (Composition)

```java
// Gatherer 可以通过 andThen 组合
var pipeline = Gatherers.<String>windowSliding(3)
    .andThen(Gatherers.mapConcurrent(4, window ->
        window.stream().mapToInt(String::length).average().orElse(0)));

var movingAvgLengths = words.stream()
    .gather(pipeline)
    .toList();
```

---

## 相关 JEP

| JEP | 版本 | 状态 | 说明 |
|-----|------|------|------|
| [JEP 461](https://openjdk.org/jeps/461) | JDK 22 | Preview | Stream Gatherers 第一预览 |
| [JEP 473](https://openjdk.org/jeps/473) | JDK 23 | Preview | Stream Gatherers 第二预览 |
| [JEP 485](https://openjdk.org/jeps/485) | JDK 24 | Final | Stream Gatherers 正式 |
