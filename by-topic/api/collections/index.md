# 集合框架

> Collection、List、Set、Map、Stream、SequencedCollection 演进历程

[← 返回 API 框架](../)

---

## 1. 快速概览

```
JDK 1.0 ── JDK 1.2 ── JDK 5 ── JDK 8 ── JDK 9 ── JDK 16 ── JDK 21 ── JDK 22 ── JDK 24
   │         │        │        │        │        │        │         │         │
Vector   Collection  泛型   Stream  不可变   toList  Sequenced  Gatherers
HashTable  List/Set   增强循环 Optional 集合   (正式) Collection  (正式)
          Map        for                                     (JEP 431)  (JEP 485)
```

### 核心演进

| 版本 | 特性 | JEP | 说明 |
|------|------|-----|------|
| **JDK 1.0** | Vector/Hashtable | - | 原始集合 |
| **JDK 1.2** | 集合框架 | - | Collection/List/Set/Map |
| **JDK 5** | 泛型 | JSR 14 | 类型安全 |
| **JDK 5** | 增强循环 | - | for-each |
| **JDK 5** | EnumSet/EnumMap | - | 枚举专用集合 |
| **JDK 6** | NavigableSet/Map | - | 导航集合 |
| **JDK 6** | Deque | - | 双端队列 |
| **JDK 8** | Stream API | JEP 107 | 函数式操作 |
| **JDK 8** | CompletableFuture | - | 异步编程 |
| **JDK 9** | 不可变集合 | JEP 269 | List.of/Set.of/Map.of |
| **JDK 16** | Stream.toList() | - | 简化收集 |
| **JDK 17** | 增强伪随机数发生器 | - | RandomGenerator |
| **JDK 21** | SequencedCollection | JEP 431 | 有序集合统一 API |
| **JDK 22** | Stream Gatherers | JEP 461 | 自定义中间操作 (预览) |
| **JDK 24** | Stream Gatherers | JEP 485 | 正式版 |

---

## 目录

- [集合框架架构](#集合框架架构)
- [核心实现与性能选择](#核心实现与性能选择)
- [JDK 9 工厂方法](#jdk-9-工厂方法)
- [不可变集合](#不可变集合)
- [并发集合](#并发集合)
- [Stream API 与集合](#stream-api-与集合)
- [SequencedCollection](#sequencedcollection)
- [Stream Gatherers](#stream-gatherers)
- [核心贡献者](#核心贡献者)
- [相关链接](#相关链接)

---

## 2. 集合框架架构

### Collection/Map 接口层次图

```
┌─────────────────────────────────────────────────────────────────────┐
│                    集合框架接口层次 (Interface Hierarchy)             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Iterable<T>                                                       │
│    │                                                               │
│    └── Collection<T>                                               │
│         │                                                          │
│         ├── List<T>          (ordered, duplicates allowed)          │
│         │    ├── ArrayList         ← 动态数组 (dynamic array)       │
│         │    ├── LinkedList        ← 双向链表 (doubly-linked list) │
│         │    ├── Vector (旧, legacy) ← 同步数组                    │
│         │    └── CopyOnWriteArrayList ← 写时复制                   │
│         │                                                          │
│         ├── Set<T>           (no duplicates)                       │
│         │    ├── HashSet           ← 哈希表 (hash table)           │
│         │    ├── LinkedHashSet     ← 哈希表 + 插入顺序链表          │
│         │    ├── TreeSet           ← 红黑树 (red-black tree)       │
│         │    └── EnumSet           ← 位向量 (bit vector)            │
│         │                                                          │
│         ├── Queue<T>         (FIFO 队列)                           │
│         │    ├── PriorityQueue     ← 二叉堆 (binary heap)          │
│         │    └── Deque<T>          (双端队列, double-ended queue)   │
│         │        ├── ArrayDeque    ← 循环数组                      │
│         │        └── LinkedList    ← 同时实现 List 和 Deque         │
│         │                                                          │
│         └── SequencedCollection<T>    (JDK 21, JEP 431)            │
│              └── SequencedSet<T>                                   │
│                                                                     │
│  Map<K,V>              (键值对, 不继承 Collection)                  │
│    ├── HashMap              ← 数组+链表/红黑树                     │
│    ├── LinkedHashMap        ← HashMap + 双向链表维护顺序            │
│    ├── TreeMap              ← 红黑树 (SortedMap/NavigableMap)      │
│    ├── EnumMap              ← 数组 (enum ordinal 做索引)            │
│    ├── WeakHashMap          ← 弱引用键 (weak reference keys)       │
│    ├── IdentityHashMap      ← 引用相等 (==) 而非 equals()          │
│    └── ConcurrentHashMap    ← 线程安全 (thread-safe)               │
│                                                                     │
│  SequencedMap<K,V>         (JDK 21, JEP 431)                       │
│    ├── LinkedHashMap                                                │
│    └── SortedMap (putFirst/putLast 抛 UnsupportedOperationException)│
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 基础操作

```java
// List - 有序可重复
List<String> list = new ArrayList<>();
list.add("A");
list.add("B");
list.get(0);              // "A"
list.remove(0);           // 移除第一个

// Set - 无序不可重复
Set<String> set = new HashSet<>();
set.add("A");
set.add("A");             // 重复, 不会添加
set.contains("A");        // true

// Map - 键值对
Map<String, Integer> map = new HashMap<>();
map.put("one", 1);
map.get("one");           // 1
map.getOrDefault("two", 0); // 0
```

---

## 3. 核心实现与性能选择

### ArrayList vs LinkedList

```java
// ArrayList - 动态数组, 随机访问 O(1)
List<String> arrayList = new ArrayList<>(100);  // 指定初始容量 (initial capacity)

// LinkedList - 双向链表, 头尾插入 O(1)
List<String> linkedList = new LinkedList<>();
```

**性能对比 (Performance Comparison)**:

| 操作 | ArrayList | LinkedList | 说明 |
|------|-----------|------------|------|
| `get(index)` 随机访问 | **O(1)** | O(n) | ArrayList 数组下标直接访问 |
| `add(E)` 尾部追加 | **O(1) 均摊** | O(1) | ArrayList 偶尔需要扩容 (grow) |
| `add(0, E)` 头部插入 | O(n) | **O(1)** | ArrayList 需要移动所有元素 |
| `remove(index)` | O(n) | O(n) | LinkedList 需先遍历找到节点 |
| 内存 (memory overhead) | 紧凑 | 每节点额外 2 指针 | LinkedList 缓存局部性差 |
| Iterator 遍历 | **快** | 慢 | CPU 缓存行 (cache line) 友好度 |

> **实践建议**: 绝大多数场景优先选择 ArrayList。LinkedList 的理论优势 (头部插入 O(1)) 在实际应用中往往被缓存不友好抵消。ArrayDeque 是更好的队列/栈实现。

### HashMap vs TreeMap vs LinkedHashMap

| 特性 | HashMap | TreeMap | LinkedHashMap |
|------|---------|---------|---------------|
| 底层结构 | 数组+链表/红黑树 | 红黑树 | HashMap+双向链表 |
| 键排序 | 无序 | 自然序/Comparator | **插入顺序**/访问顺序 |
| `get`/`put` | **O(1)** | O(log n) | O(1) |
| null 键 | 允许 1 个 | 不允许 | 允许 1 个 |
| 线程安全 | 否 | 否 | 否 |
| 用途 | 通用查找 | 需要排序时 | 需要保持顺序时 |

```java
// HashMap - 通用哈希表 (general-purpose)
Map<String, Integer> map = new HashMap<>(16, 0.75f);

// 遍历
// 1. entrySet (推荐)
for (Map.Entry<String, Integer> entry : map.entrySet()) {
    String key = entry.getKey();
    Integer value = entry.getValue();
}

// 2. forEach (JDK 8+)
map.forEach((key, value) -> System.out.println(key + "=" + value));

// TreeMap - 红黑树, 按键排序 (sorted by keys)
TreeMap<String, Integer> sorted = new TreeMap<>();
sorted.put("C", 3);
sorted.put("A", 1);
sorted.put("B", 2);
// 遍历顺序: {A=1, B=2, C=3}

// 导航操作 (navigation)
sorted.firstKey();            // "A"
sorted.lastKey();             // "C"
sorted.headMap("C");          // {A=1, B=2}
sorted.floorEntry("B");      // B=2  (小于等于 B 的最大条目)
sorted.ceilingEntry("B");    // B=2  (大于等于 B 的最小条目)

// LinkedHashMap - 保持插入顺序 (insertion order)
Map<String, Integer> linked = new LinkedHashMap<>();
linked.put("B", 2);
linked.put("A", 1);
// 遍历顺序: {B=2, A=1}

// LinkedHashMap 作 LRU 缓存 (Least Recently Used cache)
Map<String, Integer> lru = new LinkedHashMap<>(16, 0.75f, true) { // accessOrder=true
    @Override
    protected boolean removeEldestEntry(Map.Entry<String, Integer> eldest) {
        return size() > 100;  // 最多保留 100 个条目
    }
};
```

### 遍历方式 (Iteration Methods)

```java
List<String> list = new ArrayList<>();

// 1. 传统 for
for (int i = 0; i < list.size(); i++) {
    String s = list.get(i);
}

// 2. 增强 for (JDK 5+, enhanced for-each)
for (String s : list) {
    // ...
}

// 3. Iterator
Iterator<String> it = list.iterator();
while (it.hasNext()) {
    String s = it.next();
    it.remove();  // 安全删除 (safe removal during iteration)
}

// 4. forEach (JDK 8+)
list.forEach(s -> System.out.println(s));
```

---

## 4. JDK 9 工厂方法

**JEP 269: Convenience Factory Methods for Collections**

### List.of / Set.of / Map.of

```java
// JDK 9 引入不可变集合工厂方法 (immutable collection factory methods)

// List.of - 不可变列表
List<String> list = List.of("A", "B", "C");
// list.add("D");   // 抛出 UnsupportedOperationException

// Set.of - 不可变集合 (不允许 null, 不允许重复)
Set<String> set = Set.of("A", "B", "C");
// Set.of("A", "A"); // 抛出 IllegalArgumentException: duplicate element

// Map.of - 不可变 Map (最多 10 对)
Map<String, Integer> map = Map.of("A", 1, "B", 2, "C", 3);

// Map.ofEntries - 超过 10 对使用
Map<String, Integer> bigMap = Map.ofEntries(
    Map.entry("A", 1),
    Map.entry("B", 2),
    Map.entry("C", 3)
    // ... 可以传入任意多对
);
```

### 内部实现 (Internal Implementation)

JDK 针对小集合做了特化优化 (specialization):

```
List.of()        → ListN.EMPTY_LIST    (空列表单例)
List.of(e1)      → List12             (1 个 final 字段, 无数组分配)
List.of(e1, e2)  → List12             (2 个 final 字段, 无数组分配)
List.of(e1..eN)  → ListN              (N≥3, 内部 Object[] 数组)
```

```java
// 源码视角 (source perspective): java.util.ImmutableCollections
// List12 - 专为 1-2 个元素优化, 避免数组开销
static final class List12<E> extends AbstractImmutableList<E> {
    private final E e0;           // 第一个元素
    private final @Stable E e1;   // 第二个元素 (1 元素时为 EMPTY)

    @Override public int size() {
        return e1 != EMPTY ? 2 : 1;
    }
}

// ListN - 3+ 个元素, 使用数组
static final class ListN<E> extends AbstractImmutableList<E> {
    private final @Stable E[] elements;

    @Override public int size() {
        return elements.length;
    }
}
```

**Set.of 的去重检测**: 内部使用探测哈希表 (probe hash table), 在创建时即检测重复, 发现重复立即抛 `IllegalArgumentException`。

**Map.of 的特化**: 类似地, `Map1` 用于单键值对, `MapN` 用于多键值对, 内部使用扁平化数组 `Object[] table` 存储 key-value 交替排列。

---

## 5. 不可变集合

### 三种不可变方式对比

| 方式 | 引入版本 | null 元素 | 真正不可变 | 性能 |
|------|---------|-----------|-----------|------|
| `Collections.unmodifiableList()` | JDK 1.2 | 允许 | 否 (视图) | 包装开销 |
| `List.of()` | JDK 9 | 不允许 | **是** | 最优 |
| `List.copyOf()` | JDK 10 | 不允许 | **是** | 复制开销 |

```java
// 1. Collections.unmodifiableList - 不可变视图 (unmodifiable view)
// 底层列表修改会反映到视图, 只是视图本身不可修改
List<String> mutable = new ArrayList<>(List.of("A", "B"));
List<String> view = Collections.unmodifiableList(mutable);
// view.add("C");    // UnsupportedOperationException
mutable.add("C");    // OK! view 也会看到 "C"
System.out.println(view.size());  // 3 — 不是真正的不可变!

// 2. List.of - 真正不可变 (truly immutable), 不允许 null
List<String> immutable = List.of("A", "B");
// immutable.add("C");  // UnsupportedOperationException
// List.of("A", null);  // NullPointerException

// 3. List.copyOf - 复制为不可变 (copy into immutable)
List<String> original = new ArrayList<>(List.of("A", "B"));
List<String> copy = List.copyOf(original);
original.add("C");
System.out.println(copy.size());  // 2 — 与原列表解耦
// 优化: 如果原列表已经是不可变实现, copyOf 直接返回原引用
List<String> same = List.copyOf(List.of("X"));  // 不会产生新副本
```

### 选择建议

- **API 返回值**: 使用 `List.of()` 或 `List.copyOf()`, 防止调用者修改
- **防御性复制 (defensive copy)**: 使用 `List.copyOf(input)`, 与输入参数解耦
- **需要 null 元素**: 被迫使用 `Collections.unmodifiableList(new ArrayList<>(src))`
- **Stream 收集**: 使用 `Collectors.toUnmodifiableList()` (JDK 10+)

---

## 6. 并发集合

### ConcurrentHashMap 深入

**JDK 8 重写**: 将 JDK 7 的分段锁 (Segment lock) 改为 **CAS + synchronized** 锁粒度为桶 (bucket-level locking)。

```
ConcurrentHashMap 内部结构 (JDK 8+):
┌─────────────────────────────────────────┐
│  Node[] table   (volatile)              │
│  ┌───┬───┬───┬───┬───┬───┬───┬───┐      │
│  │ 0 │ 1 │ 2 │ 3 │ 4 │ 5 │...│ n │      │
│  └─┬─┴───┴─┬─┴───┴───┴─┬─┴───┴───┘      │
│    │       │           │                 │
│    ▼       ▼           ▼                 │
│  Node → Node        TreeBin → TreeNode  │
│    │                     │               │
│    ▼                     ▼               │
│  Node (链表)          TreeNode (红黑树)   │
│                                          │
│  链表 → 红黑树: 链表长度 ≥ 8 且 table ≥ 64 │
│  红黑树 → 链表: 树节点 ≤ 6                 │
└─────────────────────────────────────────┘
```

**树化阈值 (Treeify Threshold)**:
- `TREEIFY_THRESHOLD = 8`: 链表长度达到 8 时转为红黑树
- `UNTREEIFY_THRESHOLD = 6`: 红黑树节点减少到 6 时退化为链表
- `MIN_TREEIFY_CAPACITY = 64`: table 容量小于 64 时优先扩容而非树化

```java
ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();

// 原子操作 (atomic operations)
map.putIfAbsent("key", 1);
map.compute("key", (k, v) -> v == null ? 1 : v + 1);
map.merge("key", 1, Integer::sum);

// JDK 8+ 批量操作 (bulk operations)
// parallelismThreshold: 元素数超过此值时并行执行
map.forEach(1000, (key, value) -> {
    // 并行处理, threshold = 1000
});

long count = map.reduceValuesToLong(1000, Integer::longValue, 0L, Long::sum);
```

**computeIfAbsent 使用陷阱**:

```java
// 陷阱 1: mappingFunction 内不要修改同一个 Map — 可能死锁!
ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
// 以下代码在同一个桶上可能产生死锁 (deadlock on same bucket):
map.computeIfAbsent("key", k -> {
    map.put("key2", 2);   // 如果 key 和 key2 在同一桶, 可能死锁
    return 1;
});

// 陷阱 2: 递归 computeIfAbsent 会死锁
// (fixed in JDK 9, 抛出 IllegalStateException 而非死锁)
map.computeIfAbsent("A", k -> map.computeIfAbsent("A", k2 -> 1));

// 正确用法: mappingFunction 应是简单的、无副作用的
map.computeIfAbsent("key", k -> expensiveCompute(k));
```

### CopyOnWriteArrayList

```java
// 写时复制 (copy-on-write), 适合读多写少 (read-heavy, write-rare)
CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();

// 读操作无锁 (lock-free reads)
for (String s : list) {
    // 迭代期间不会抛 ConcurrentModificationException
}

// 写操作复制整个数组 (full array copy on write)
list.add("new");  // 内部: 加锁 → 复制数组 → 追加元素 → 替换引用
```

### BlockingQueue

```java
// 阻塞队列 (blocking queue) — 生产者-消费者模式的核心
BlockingQueue<String> queue = new LinkedBlockingQueue<>(100);

queue.put("item");    // 队列满时阻塞 (blocks when full)
String item = queue.take();  // 队列空时阻塞 (blocks when empty)

// 带超时 (with timeout)
boolean success = queue.offer("item", 1, TimeUnit.SECONDS);
String polled = queue.poll(1, TimeUnit.SECONDS);
```

---

## 7. Stream API 与集合

**JDK 8 引入 (JEP 107)**

### 基础操作

```java
List<String> list = Arrays.asList("a", "bb", "ccc");

// 过滤 (filter)
list.stream()
    .filter(s -> s.length() > 1)
    .toList();

// 转换 (map)
list.stream()
    .map(String::toUpperCase)
    .toList();

// 扁平化 (flatMap)
List<List<Integer>> nested = List.of(List.of(1, 2), List.of(3, 4));
nested.stream()
    .flatMap(List::stream)
    .toList();  // [1, 2, 3, 4]

// 去重 (distinct) / 排序 (sorted) / 限制 (limit)
list.stream().distinct().sorted().limit(2).toList();
```

### Collectors 详解

```java
// Collectors.toList() — 返回可变 ArrayList (JDK 8+)
List<String> mutableList = stream.collect(Collectors.toList());
mutableList.add("ok");  // 允许

// Stream.toList() — 返回不可变列表 (JDK 16+, unmodifiable)
List<String> immutableList = stream.toList();
// immutableList.add("fail"); // UnsupportedOperationException

// Collectors.toUnmodifiableList() — 返回不可变列表 (JDK 10+)
// 与 stream.toList() 区别: 不允许 null 元素
List<String> unmod = stream.collect(Collectors.toUnmodifiableList());

// groupingBy — 分组
Map<Integer, List<String>> byLength = strings.stream()
    .collect(Collectors.groupingBy(String::length));

// groupingBy + downstream — 多级分组/聚合
Map<Integer, Long> countByLength = strings.stream()
    .collect(Collectors.groupingBy(String::length, Collectors.counting()));

Map<Integer, Set<String>> setByLength = strings.stream()
    .collect(Collectors.groupingBy(String::length, Collectors.toSet()));

// partitioningBy — 二分区
Map<Boolean, List<String>> partitioned = strings.stream()
    .collect(Collectors.partitioningBy(s -> s.length() > 2));

// joining — 连接字符串
String joined = strings.stream()
    .collect(Collectors.joining(", ", "[", "]"));  // [a, bb, ccc]

// toMap — 收集为 Map
Map<String, Integer> nameLen = names.stream()
    .collect(Collectors.toMap(
        Function.identity(),    // key
        String::length,         // value
        (v1, v2) -> v1          // merge function (处理键冲突)
    ));
```

### toArray

```java
// 收集为数组
String[] array = list.stream().toArray(String[]::new);

// 基本类型数组
int[] ints = list.stream().mapToInt(Integer::intValue).toArray();
```

### 并行 Stream (Parallel Stream)

```java
// 并行处理 — 使用 ForkJoinPool.commonPool()
long sum = list.parallelStream()
    .mapToLong(Long::parseLong)
    .sum();

// 自定义并行度 (custom parallelism)
ForkJoinPool customPool = new ForkJoinPool(4);
List<String> result = customPool.submit(
    () -> list.parallelStream().filter(s -> s.length() > 1).toList()
).get();
```

> **注意**: 并行 Stream 在元素少、IO 密集或共享可变状态场景下反而更慢。仅在 CPU 密集型且数据量大时考虑。

---

## 8. SequencedCollection

**JDK 21 引入 (JEP 431)**

### 新增接口层次

```
             SequencedCollection<E>
              /                \
    SequencedSet<E>         (List, Deque 也继承)
         |
    SortedSet<E>

             SequencedMap<K,V>
              |
         SortedMap<K,V>
```

### 有序集合统一 API

JEP 431 解决的核心问题: 在 JDK 21 之前, 访问集合首尾元素的方式不统一:

| 操作 | List | Deque | SortedSet | 统一前? |
|------|------|-------|-----------|---------|
| 获取首元素 | `list.get(0)` | `deque.getFirst()` | `set.first()` | 3 种 API |
| 获取尾元素 | `list.get(size-1)` | `deque.getLast()` | `set.last()` | 3 种 API |
| 反转遍历 | `listIterator(size)` | `descendingIterator()` | 无 | 不统一 |

JEP 431 统一为:

```java
// SequencedCollection 统一接口
interface SequencedCollection<E> extends Collection<E> {
    SequencedCollection<E> reversed();
    void addFirst(E e);
    void addLast(E e);
    E getFirst();
    E getLast();
    E removeFirst();
    E removeLast();
}
```

```java
// 使用示例
List<String> list = new ArrayList<>(List.of("A", "B", "C"));

String first = list.getFirst();      // "A"
String last = list.getLast();        // "C"

list.addFirst("Z");                  // [Z, A, B, C]
list.addLast("D");                   // [Z, A, B, C, D]

list.removeFirst();                  // [A, B, C, D]
list.removeLast();                   // [A, B, C]

// 反转视图 (reversed view) — 不复制, O(1)
List<String> reversed = list.reversed();  // [C, B, A]
// 对 reversed 的修改会反映到原列表

// SequencedSet
SequencedSet<String> set = new LinkedHashSet<>(List.of("A", "B", "C"));
set.addFirst("Z");                 // [Z, A, B, C]

// 注意: SortedSet/TreeSet 的 addFirst/addLast 会抛 UnsupportedOperationException
// 因为排序由 Comparator 决定, 不能人为指定位置
// 但 getFirst()/getLast()/reversed() 等只读操作可用
```

### 既有类的集成

JEP 431 将以下既有类纳入 Sequenced 体系 (通过默认方法, 完全向后兼容):

| 既有类/接口 | 新增超接口 |
|-------------|-----------|
| `List` | `SequencedCollection` |
| `Deque` | `SequencedCollection` |
| `LinkedHashSet` | `SequencedSet` |
| `SortedSet` | `SequencedSet` (addFirst/addLast 抛异常) |
| `LinkedHashMap` | `SequencedMap` |
| `SortedMap` | `SequencedMap` (putFirst/putLast 抛异常) |

### SequencedMap

```java
SequencedMap<String, Integer> map = new LinkedHashMap<>();
map.put("A", 1);
map.put("B", 2);

Map.Entry<String, Integer> first = map.firstEntry();   // A=1
Map.Entry<String, Integer> last = map.lastEntry();     // B=2

map.putFirst("Z", 0);              // {Z=0, A=1, B=2}
map.putLast("C", 3);               // {Z=0, A=1, B=2, C=3}

Map.Entry<String, Integer> polled = map.pollFirstEntry(); // Z=0
SequencedMap<String, Integer> reversed = map.reversed();

// sequencedKeySet / sequencedValues / sequencedEntrySet
SequencedSet<String> keys = map.sequencedKeySet();
```

---

## 9. Stream Gatherers

**JDK 22 预览 (JEP 461), JDK 23 第二次预览 (JEP 473), JDK 24 正式 (JEP 485)**

### 为什么需要 Gatherers

Stream API 提供了丰富的内置中间操作 (filter/map/flatMap 等), 但无法自定义中间操作。Gatherers 填补了这一空白, 类似于 Collector 之于终端操作。

```
Stream 操作扩展点:
  Source → [中间操作: Gatherer] → [终端操作: Collector] → 结果
               ↑ JEP 485 新增          ↑ JDK 8 既有
```

### 自定义 Gatherer

```java
// Gatherer<T, A, R> 的四个组件:
// 1. initializer  — 初始化状态 (Supplier<A>)
// 2. integrator   — 处理每个元素 (Integrator<A, T, R>)
// 3. combiner     — 合并并行状态 (BinaryOperator<A>), 可选
// 4. finisher     — 最终处理 (BiConsumer<A, Downstream<R>>), 可选

// 示例: 去重相邻元素 (distinct consecutive)
Gatherer<String, ?, String> distinctConsecutive = Gatherer.ofSequential(
    () -> new Object[]{ null },   // 状态: 上一个元素
    (state, element, downstream) -> {
        if (!element.equals(state[0])) {
            state[0] = element;
            return downstream.push(element);
        }
        return true;
    }
);

Stream.of("A", "A", "B", "B", "A")
    .gather(distinctConsecutive)
    .toList();  // ["A", "B", "A"]
```

### 内置 Gatherers (5 个)

| Gatherer | 类型 | 说明 |
|----------|------|------|
| `fold` | 多对一 (many-to-one) | 增量聚合, 输入耗尽后输出 |
| `scan` | 一对一 (one-to-one) | 前缀扫描, 输出每步中间结果 |
| `mapConcurrent` | 一对一 | 并发映射, 可限制并发数 (uses virtual threads) |
| `windowFixed` | 多对多 (many-to-many) | 固定大小窗口分组 |
| `windowSliding` | 多对多 | 滑动窗口分组 |

```java
// fold - 归约 (全部消费后输出单一结果)
Stream.of(1, 2, 3, 4, 5)
    .gather(Gatherers.fold(() -> 0, Integer::sum))
    .findFirst();  // Optional[15]

// scan - 前缀和 (每步输出中间结果)
Stream.of(1, 2, 3, 4)
    .gather(Gatherers.scan(() -> 0, Integer::sum))
    .toList();  // [1, 3, 6, 10]

// windowFixed - 固定窗口
Stream.of(1, 2, 3, 4, 5)
    .gather(Gatherers.windowFixed(3))
    .toList();  // [[1, 2, 3], [4, 5]]

// windowSliding - 滑动窗口
Stream.of(1, 2, 3, 4, 5)
    .gather(Gatherers.windowSliding(3))
    .toList();  // [[1, 2, 3], [2, 3, 4], [3, 4, 5]]

// mapConcurrent - 并发映射 (使用虚拟线程)
Stream.of("url1", "url2", "url3")
    .gather(Gatherers.mapConcurrent(4, url -> fetchData(url)))
    .toList();
```

### Gatherer 组合

```java
// Gatherers 可通过 andThen 链式组合
Gatherer<Integer, ?, List<Integer>> windowThenFilter =
    Gatherers.<Integer>windowFixed(3)
        .andThen(Gatherers.of(
            (unused, window, downstream) -> {
                if (window.stream().mapToInt(i -> i).sum() > 5) {
                    return downstream.push(window);
                }
                return true;
            }
        ));
```

---

## 10. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 集合框架 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Stuart Marks | 30+ | Oracle | 集合 API 设计 |
| 2 | Martin Buchholz | 20+ | Oracle | Collections 实现 |
| 3 | [Brian Goetz](/by-contributor/profiles/brian-goetz.md) | 15+ | Oracle | Stream API |
| 4 | Henry Jen | 12 | Oracle | 集合增强 |
| 5 | Paul Sandoz | 10 | Oracle | Stream/Optional |

### 历史贡献者

| 贡献者 | 公司/机构 | 主要贡献 |
|--------|----------|----------|
| **Joshua Bloch** | Google/Sun | Collections Framework 设计 |
| **Doug Lea** | SUNY Oswego | 并发集合、ConcurrentHashMap |
| **Guy Steele** | Oracle | Stream API (JEP 107) |

---

## 11. Git 提交历史

> 基于 OpenJDK master 分支分析

### 集合框架改进 (2024-2026)

```bash
# 查看集合相关提交
cd /path/to/jdk
git log --oneline -- src/java.base/share/classes/java/util/

# 最近的重要提交
08c8520 8378698: Optimize Base64.Encoder#encodeToString
324524b JDK-8266431: Dual-Pivot Quicksort improvements
b9e7ca1 8379344: Compact the Unicode/CLDR version tables
```

---

## 12. 相关链接

### 内部文档

- [集合时间线](timeline.md) - 详细的历史演进
- [核心 API](../)
- [并发编程](../../concurrency/)

### 外部资源

- [JEP 107](/jeps/language/jep-107.md)
- [JEP 269: Convenience Factory Methods for Collections](https://openjdk.org/jeps/269)
- [JEP 431: Sequenced Collections](/jeps/language/jep-431.md)
- [JEP 461](/jeps/language/jep-461.md)
- [JEP 473: Stream Gatherers (Second Preview)](https://openjdk.org/jeps/473)
- [JEP 485: Stream Gatherers (Final)](/jeps/tools/jep-485.md)
- [SequencedCollection JavaDoc](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/SequencedCollection.html)
- [Gatherers JavaDoc](https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/util/stream/Gatherers.html)
- [Stream Gatherers Guide](https://docs.oracle.com/en/java/javase/24/core/stream-gatherers.html)

### Git 仓库

```bash
# 查看集合相关提交
git log --oneline -- src/java.base/share/classes/java/util/
git log --oneline -- src/java.base/share/classes/java/util/stream/
```

---

**最后更新**: 2026-03-22

**Sources**:
- [JEP 107](/jeps/language/jep-107.md)
- [JEP 269](https://openjdk.org/jeps/269)
- [JEP 431](/jeps/language/jep-431.md)
- [JEP 461](/jeps/language/jep-461.md)
- [JEP 485](/jeps/tools/jep-485.md)
- [Stream Gatherers in Practice](https://softwaremill.com/stream-gatherers-in-practice-part-1/)
- [Gatherers Tutorial](https://codewiz.info/blog/stream-gatherers/)
