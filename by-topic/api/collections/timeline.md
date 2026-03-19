# 集合框架演进时间线

Java 集合框架从 JDK 1.0 到 JDK 26 的完整演进历程。

---

## 时间线概览

```
JDK 1.0 ──── JDK 1.2 ──── JDK 5 ──── JDK 6 ──── JDK 8 ──── JDK 16 ──── JDK 21 ──── JDK 26
 │             │             │            │           │            │            │            │
Vector/       Collections  Generics    Queue       Stream      Sealed      Stream      链式
Hashtable     Framework    (泛型)      接口        API         Foreign     Gatherers   元素
              (List/Set/   增强循环    Deque       (Lambda)    Access                  方法
              Map)         EnumMap/    Navigable
                           EnumSet      Map
```

---

## 集合框架体系

```
┌─────────────────────────────────────────────────────────┐
│                 Collection Framework                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│                  Iterable                               │
│                       │                                 │
│        ┌──────────────┴──────────────┐                  │
│        │                             │                  │
│   Collection                    Map (N/A)              │
│        │                             │                  │
│   ┌────┴────┬────────┬────────┐      │                  │
│   │         │        │        │      │                  │
│  List    Set    Queue   Deque    HashMap                │
│   │       │       │       │      TreeMap                │
│   │       │       │       │      LinkedHashMap          │
│ ArrayList HashSet│    │      ConcurrentHashMap        │
│ LinkedListLinked  PriorityBlockingQueue               │
│          Set     Queue                                  │
│          TreeSet                                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## JDK 1.0 - 原始集合

### Vector 和 Hashtable

```java
// Vector - 线程安全的动态数组
Vector<String> vector = new Vector<>();
vector.add("Hello");
vector.add("World");
String element = vector.get(0);

// Hashtable - 线程安全的哈希表
Hashtable<String, Integer> table = new Hashtable<>();
table.put("one", 1);
table.put("two", 2);
Integer value = table.get("one");
```

**特点**：
- 所有方法都同步 (线程安全)
- 性能较差 (锁开销大)
- 已被 ArrayList 和 HashMap 取代

---

## JDK 1.2 - Collections Framework

### 核心接口

```java
// Collection - 集合根接口
Collection<String> collection = new ArrayList<>();

// List - 有序集合，允许重复
List<String> list = new ArrayList<>();
list.add("A");
list.add("B");
list.add("A");  // 允许重复
String first = list.get(0);

// Set - 无序集合，不允许重复
Set<String> set = new HashSet<>();
set.add("A");
set.add("B");
set.add("A");  // 重复，不会添加

// Map - 键值对映射
Map<String, Integer> map = new HashMap<>();
map.put("one", 1);
map.put("two", 2);
```

### ArrayList vs LinkedList

| 特性 | ArrayList | LinkedList |
|------|-----------|------------|
| 底层实现 | 数组 | 双向链表 |
| 随机访问 | O(1) | O(n) |
| 头部插入 | O(n) | O(1) |
| 尾部插入 | O(1) amortized | O(1) |
| 内存占用 | 较低 | 较高 (节点指针) |
| 适用场景 | 随机访问多 | 频繁插入删除 |

### HashSet vs TreeSet

| 特性 | HashSet | TreeSet |
|------|---------|---------|
| 底层实现 | HashMap | TreeMap (红黑树) |
| 有序性 | 无序 | 自然排序 |
| 插入/查找 | O(1) | O(log n) |
| null 允许 | 允许 | 不允许 |
| 适用场景 | 快速查找 | 需要排序 |

### HashMap vs TreeMap

| 特性 | HashMap | TreeMap |
|------|---------|---------|
| 底层实现 | 哈希表 | 红黑树 |
| 有序性 | 无序 | 键排序 |
| 插入/查找 | O(1) | O(log n) |
| null 键 | 允许一个 | 不允许 |
| 适用场景 | 快速查找 | 需要排序 |

### Collections 工具类

```java
// 排序
List<Integer> numbers = Arrays.asList(3, 1, 4, 1, 5);
Collections.sort(numbers);

// 二分查找
int index = Collections.binarySearch(numbers, 4);

// 打乱
Collections.shuffle(numbers);

// 不可修改视图
List<String> immutable = Collections.unmodifiableList(list);

// 空集合
List<String> empty = Collections.emptyList();

// 单例集合
Set<String> singleton = Collections.singleton("Hello");

// 同步包装
List<String> syncList = Collections.synchronizedList(new ArrayList<>());
```

---

## JDK 5 - Generics 和增强

### 泛型

```java
// 泛型集合
List<String> strings = new ArrayList<String>();
strings.add("Hello");
// strings.add(123);  // 编译错误

// 类型推断 (Diamond Operator, JDK 7+)
List<String> strings = new ArrayList<>();

// 泛型方法
public static <T> T first(List<T> list) {
    return list.get(0);
}

// 有界类型参数
public static <T extends Number> double sum(List<T> list) {
    double sum = 0;
    for (T t : list) {
        sum += t.doubleValue();
    }
    return sum;
}
```

### EnumSet 和 EnumMap

```java
enum Color { RED, GREEN, BLUE }

// EnumSet - 高效的枚举集合
Set<Color> colors = EnumSet.of(Color.RED, Color.GREEN);
Set<Color> allColors = EnumSet.allOf(Color.class);
Set<Color> range = EnumSet.range(Color.RED, Color.BLUE);

// EnumMap - 高效的枚举键映射
Map<Color, String> colorMap = new EnumMap<>(Color.class);
colorMap.put(Color.RED, "#FF0000");
```

### Queue 和 Deque

```java
// Queue - 队列接口
Queue<String> queue = new LinkedList<>();
queue.offer("A");  // 添加
String head = queue.poll();  // 移除并返回头部
String peek = queue.peek();  // 返回头部但不移除

// Deque - 双端队列
Deque<String> deque = new ArrayDeque<>();
deque.addFirst("A");
deque.addLast("B");
String first = deque.removeFirst();
String last = deque.removeLast();

// PriorityQueue - 优先队列
Queue<Integer> pq = new PriorityQueue<>();
pq.offer(3);
pq.offer(1);
pq.offer(2);
Integer min = pq.poll();  // 1
```

### ConcurrentHashMap

```java
// ConcurrentHashMap - 线程安全的哈希表
ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
map.put("key", 1);
Integer value = map.get("key");
map.remove("key");

// 原子操作
map.computeIfAbsent("key", k -> 0);
map.computeIfPresent("key", (k, v) -> v + 1);
map.merge("key", 1, Integer::sum);

// JDK 8+ 新方法
map.forEach((k, v) -> System.out.println(k + "=" + v));
map.replaceAll((k, v) -> v * 2);
Map<String, Integer> snapshot = map.snapshot();
```

---

## JDK 6 - Navigable 和 Blocking

### NavigableSet 和 NavigableMap

```java
// NavigableSet - 可导航集合
NavigableSet<Integer> set = new TreeSet<>();
set.addAll(Arrays.asList(1, 3, 5, 7, 9));

Integer lower = set.lower(5);    // 3 (小于 5 的最大值)
Integer floor = set.floor(5);    // 5 (小于等于 5 的最大值)
Integer ceiling = set.ceiling(5); // 5 (大于等于 5 的最小值)
Integer higher = set.higher(5);  // 7 (大于 5 的最小值)

// 子集
SortedSet<Integer> headSet = set.headSet(5);      // < 5
SortedSet<Integer> tailSet = set.tailSet(5);      // >= 5
SortedSet<Integer> subSet = set.subSet(3, 7);     // [3, 7)

// NavigableMap
NavigableMap<String, String> map = new TreeMap<>();
map.put("a", "A");
map.put("b", "B");
map.put("c", "C");

Map.Entry<String, String> lowerEntry = map.lowerEntry("b");  // a=A
Map.Entry<String, String> floorEntry = map.floorEntry("b");  // b=B
```

### BlockingQueue

```java
// ArrayBlockingQueue - 有界阻塞队列
BlockingQueue<String> queue = new ArrayBlockingQueue<>(10);

// 生产者
queue.put("item");  // 队列满时阻塞

// 消费者
String item = queue.take();  // 队列空时阻塞

// LinkedBlockingQueue - 可选有界
BlockingQueue<String> unbounded = new LinkedBlockingQueue<>();
BlockingQueue<String> bounded = new LinkedBlockingQueue<>(100);

// PriorityBlockingQueue - 优先级阻塞队列
BlockingQueue<Integer> pq = new PriorityBlockingQueue<>();

// DelayQueue - 延迟队列
class DelayedTask implements Delayed {
    private final long delayTime;
    private final long expireTime;

    public long getDelay(TimeUnit unit) {
        return unit.convert(expireTime - System.currentTimeMillis(),
                           TimeUnit.MILLISECONDS);
    }

    public int compareTo(Delayed other) {
        return Long.compare(this.expireTime,
            ((DelayedTask) other).expireTime);
    }
}
```

---

## JDK 8 - Stream API

### Stream 基础

```java
List<String> list = Arrays.asList("a", "b", "c", "d");

// 创建 Stream
Stream<String> stream = list.stream();
Stream<String> parallelStream = list.parallelStream();

// 中间操作
list.stream()
    .filter(s -> s.startsWith("a"))    // 过滤
    .map(String::toUpperCase)          // 转换
    .sorted()                          // 排序
    .distinct()                        // 去重
    .limit(10)                         // 限制
    .skip(5)                           // 跳过

// 终端操作
    .collect(Collectors.toList());     // 收集到 List
    .collect(Collectors.toSet());      // 收集到 Set
    .collect(Collectors.joining(", ")); // 连接字符串
    .count();                          // 计数
    .findFirst();                      // 第一个
    .findAny();                        // 任意一个
    .anyMatch(s -> s.equals("a"));     // 任意匹配
    .allMatch(s -> s.length() > 0);    // 全部匹配
    .noneMatch(s -> s.isEmpty());      // 无匹配
```

### Collectors

```java
List<Person> people = Arrays.asList(
    new Person("Alice", 25),
    new Person("Bob", 30),
    new Person("Charlie", 25)
);

// 分组
Map<Integer, List<Person>> byAge = people.stream()
    .collect(Collectors.groupingBy(Person::getAge));

// 分组计数
Map<Integer, Long> countByAge = people.stream()
    .collect(Collectors.groupingBy(
        Person::getAge,
        Collectors.counting()
    ));

// 分区 (布尔分组)
Map<Boolean, List<Person>> partitioned = people.stream()
    .collect(Collectors.partitioningBy(p -> p.getAge() >= 30));

// 转换值
Map<Integer, List<String>> namesByAge = people.stream()
    .collect(Collectors.groupingBy(
        Person::getAge,
        Collectors.mapping(Person::getName, Collectors.toList())
    ));

// 求和
int totalAge = people.stream()
    .collect(Collectors.summingInt(Person::getAge));

// 求平均
double avgAge = people.stream()
    .collect(Collectors.averagingInt(Person::getAge));

// 统计
IntSummaryStatistics stats = people.stream()
    .collect(Collectors.summarizingInt(Person::getAge));
System.out.println(stats.getAverage());
System.out.println(stats.getMax());
System.out.println(stats.getCount());
```

### Map 新方法

```java
Map<String, Integer> map = new HashMap<>();

// JDK 8 新增
map.getOrDefault("key", 0);          // 不存在返回默认值
map.putIfAbsent("key", 1);           // 不存在才放入
map.computeIfAbsent("key", k -> 0);  // 不存在才计算
map.computeIfPresent("key", (k, v) -> v + 1);  // 存在才计算
map.compute("key", (k, v) -> v == null ? 1 : v + 1);  // 总是计算
map.merge("key", 1, Integer::sum);   // 合并值
map.replace("key", 2);               // 替换
map.replace("key", 1, 2);            // 值匹配才替换
map.replaceAll((k, v) -> v * 2);     // 批量替换
```

---

## JDK 9 - 不可变集合和 List.of

### 不可变集合工厂方法

```java
// List.of - 创建不可变列表
List<String> empty = List.of();
List<String> one = List.of("A");
List<String> several = List.of("A", "B", "C");

// Set.of - 创建不可变集合
Set<String> set = Set.of("A", "B", "C");

// Map.of - 创建不可变映射
Map<String, Integer> map = Map.of("A", 1, "B", 2);

// Map.ofEntries - 超过 10 个键值对
Map<String, Integer> largeMap = Map.ofEntries(
    Map.entry("A", 1),
    Map.entry("B", 2),
    Map.entry("C", 3),
    // ... 最多可创建任意大小的映射
);
```

### List.of vs Arrays.asList

| 特性 | List.of | Arrays.asList |
|------|---------|---------------|
| 可变性 | 完全不可变 | 长度不可变，元素可变 |
| null 允许 | 不允许 | 允许 |
| 序列化 | 支持 | 支持 |

### 新增集合方法

```java
// List 新增
List<Integer> list = Arrays.asList(1, 2, 3, 4, 5);
list.stream().takeWhile(n -> n < 4).toList();  // [1, 2, 3]
list.stream().dropWhile(n -> n < 3).toList();  // [3, 4, 5]

// Set.of 创建
Set<String> set = Set.of("A", "B", "C");

// 不可变集合特性
// list.add(6);  // UnsupportedOperationException
```

---

## JDK 10-17 - 持续改进

### List.copyOf (JDK 10)

```java
List<String> mutable = new ArrayList<>(List.of("A", "B"));
List<String> immutable = List.copyOf(mutable);

// 如果源已经是不可变，直接返回源
List<String> immutable2 = List.copyOf(immutable);
System.out.println(immutable == immutable2);  // true
```

### Stream.toList() (JDK 16)

```java
// JDK 16 之前
list.stream().collect(Collectors.toList());

// JDK 16+
list.stream().toList();
```

### SealedCollection (JDK 17)

```java
// 创建受保护的集合
List<String> original = new ArrayList<>(List.of("A", "B", "C"));
List<String> sealed = Collections.sealedList(original);

// sealedList 只能通过提供的视图修改
sealed.add("D");  // 可以
original.add("E");  // 也可以
```

---

## JDK 21 - Stream Gatherers

### Gatherers (预览)

```java
// JDK 21 引入 Stream Gatherers (预览)
// 允许自定义中间操作

// 固定窗口
List<List<Integer>> windows = Stream.of(1, 2, 3, 4, 5, 6)
    .gather(Gatherers.windowFixed(3))
    .toList();
// [[1, 2, 3], [4, 5, 6]]

// 滑动窗口
List<List<Integer>> sliding = Stream.of(1, 2, 3, 4, 5)
    .gather(Gatherers.windowSliding(3))
    .toList();
// [[1, 2, 3], [2, 3, 4], [3, 4, 5]]

// 扫描 (fold)
List<Integer> scan = Stream.of(1, 2, 3, 4)
    .gather(Gatherers.scan(() -> 0, Integer::sum))
    .toList();
// [1, 3, 6, 10]
```

---

## JDK 21+ - 链式元素方法

### 链式添加方法

```java
// JDK 21+ 允许链式添加元素
List<String> list = new ArrayList<>();
list.add("A")
   .add("B")
   .add("C");

// Map 链式添加
Map<String, Integer> map = new HashMap<>();
map.put("A", 1)
   .put("B", 2)
   .put("C", 3);
```

---

## 集合选择指南

### List 选择

| 场景 | 推荐实现 | 理由 |
|------|----------|------|
| 随机访问多 | ArrayList | O(1) 访问 |
| 频繁头插 | LinkedList | O(1) 头插 |
| 线程安全 | Collections.synchronizedList | 简单同步 |
| 高并发读写 | CopyOnWriteArrayList | 读写分离 |

### Set 选择

| 场景 | 推荐实现 | 理由 |
|------|----------|------|
| 快速查找 | HashSet | O(1) 查找 |
| 需要排序 | TreeSet | 有序集合 |
| 枚举集合 | EnumSet | 高效枚举 |
| 插入顺序 | LinkedHashSet | 保持顺序 |
| 线程安全 | ConcurrentHashMap.newKeySet() | 高并发 |

### Map 选择

| 场景 | 推荐实现 | 理由 |
|------|----------|------|
| 快速查找 | HashMap | O(1) 查找 |
| 需要排序 | TreeMap | 有序映射 |
| 枚举键 | EnumMap | 高效枚举 |
| 插入顺序 | LinkedHashMap | 保持顺序 |
| 高并发 | ConcurrentHashMap | 线程安全 |

### Queue 选择

| 场景 | 推荐实现 | 理由 |
|------|----------|------|
| 普通队列 | ArrayDeque | 高效双端队列 |
| 优先队列 | PriorityQueue | 堆排序 |
| 阻塞队列 | LinkedBlockingQueue | 生产消费 |
| 延迟任务 | DelayQueue | 定时任务 |
| 高并发 | ConcurrentLinkedQueue | 无锁队列 |

---

## 性能优化建议

### 初始化容量

```java
// ✅ 推荐: 指定初始容量
List<String> list = new ArrayList<>(1000);
Map<String, Integer> map = new HashMap<>(1000);

// ❌ 避免: 默认容量可能导致扩容
List<String> list = new ArrayList<>();
for (int i = 0; i < 1000; i++) {
    list.add("item");  // 多次扩容
}
```

### 遍历方式

```java
// ArrayList - 随机访问最快
for (int i = 0; i < list.size(); i++) {
    String s = list.get(i);
}

// LinkedList - 迭代器最快
for (String s : linkedList) {
    // 使用
}

// 或使用迭代器
Iterator<String> it = linkedList.iterator();
while (it.hasNext()) {
    String s = it.next();
}
```

### 避免并发修改异常

```java
// ❌ 错误: 遍历时修改会抛异常
for (String s : list) {
    if (s.equals("target")) {
        list.remove(s);  // ConcurrentModificationException
    }
}

// ✅ 正确: 使用迭代器
Iterator<String> it = list.iterator();
while (it.hasNext()) {
    String s = it.next();
    if (s.equals("target")) {
        it.remove();  // OK
    }
}

// ✅ 正确: 使用 removeIf
list.removeIf(s -> s.equals("target"));
```

---

## 时间线总结

| 版本 | 特性 | 说明 |
|------|------|------|
| JDK 1.0 | Vector, Hashtable | 原始线程安全集合 |
| JDK 1.2 | Collections Framework | List, Set, Map 接口 |
| JDK 5 | Generics, EnumSet/EnumMap | 泛型，增强循环 |
| JDK 6 | NavigableSet/Map, BlockingQueue | 可导航集合，阻塞队列 |
| JDK 8 | Stream API | 函数式集合操作 |
| JDK 9 | List.of/Set.of/Map.of | 不可变集合工厂 |
| JDK 10 | List.copyOf | 不可变集合拷贝 |
| JDK 16 | Stream.toList() | 简化收集 |
| JDK 21 | Stream Gatherers | 自定义中间操作 |

---

## 相关链接

- [Collection Interface](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Collection.html)
- [Stream API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/stream/package-summary.html)
