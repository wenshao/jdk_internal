# ConcurrentHashMap 演进全解析

> 基于 JDK 最新源码 (6413 行) 的 ConcurrentHashMap 内部实现深度解析，涵盖 JDK 7 → JDK 8 重写及后续改进

---

## 1. 总览

ConcurrentHashMap 是 `java.util.concurrent` 包的核心数据结构，经历了两次重大设计变革：

| 版本 | 设计 | 锁粒度 | 数据结构 |
|------|------|--------|----------|
| JDK 5-7 | 分段锁（Segment-based locking） | 每 Segment 一把 ReentrantLock | 数组 + 链表 |
| JDK 8+ | CAS + synchronized per-bucket | 每个桶（bin）独立锁 | 数组 + 链表 + 红黑树 |
| JDK 9+ | 底层原子操作迁移 | 同 JDK 8 | 同 JDK 8，Unsafe API 更新 |

源码位置: `src/java.base/share/classes/java/util/concurrent/ConcurrentHashMap.java`

---

## 2. JDK 7 分段锁设计 (Segment-Based Locking)

JDK 7 将哈希表分为多个 **Segment**（默认 16 个），每个 Segment 继承 ReentrantLock，本质是独立的小型 HashMap。并发度 = Segment 数量，创建后不可变。

```
┌─────────────────────────────────────────────────────┐
│  ConcurrentHashMap (JDK 7)                          │
│                                                     │
│  Segment[0]        Segment[1]       Segment[N-1]    │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐     │
│  │ Lock     │     │ Lock     │     │ Lock     │     │
│  │ table[]  │     │ table[]  │     │ table[]  │     │
│  │ ┌─┬─┬─┐  │     │ ┌─┬─┬─┐  │     │ ┌─┬─┬─┐  │     │
│  │ │ │ │ │  │     │ │ │ │ │  │     │ │ │ │ │  │     │
│  │ └─┴─┴─┘  │     │ └─┴─┴─┘  │     │ └─┴─┴─┘  │     │
│  └──────────┘     └──────────┘     └──────────┘     │
└─────────────────────────────────────────────────────┘
```

```java
// 行 531: 保留用于兼容
private static final int DEFAULT_CONCURRENCY_LEVEL = 16;

// 行 613-627: JDK 8 中 Segment 仅作序列化兼容的占位
private static final ObjectStreamField[] serialPersistentFields = {
    new ObjectStreamField("segments", Segment[].class),
    new ObjectStreamField("segmentMask", Integer.TYPE),
    new ObjectStreamField("segmentShift", Integer.TYPE),
};
```

**分段锁的固有缺陷**:
1. **内存浪费**: 每个 Segment 维护独立数组，空间利用率低
2. **并发度固定**: 创建后 Segment 数量不可变
3. **跨段操作代价高**: `size()` 需遍历所有 Segment
4. **纯链表退化**: 极端情况查找 O(n)

---

## 3. JDK 8 重写：CAS + synchronized per-bucket

### 3.1 放弃分段锁的原因

1. **锁粒度更细**: 从 Segment 级别细化到单个桶（bin）级别
2. **synchronized 优化**: JDK 6+ 的偏向锁/轻量级锁/锁膨胀优化使其性能接近 ReentrantLock
3. **红黑树**: 链表过长时转树，最坏查找从 O(n) 降至 O(log n)
4. **内存效率**: 去掉 Segment 中间层

### 3.2 核心常量（均来自实际源码）

```java
private static final int DEFAULT_CAPACITY = 16;            // 行 519
private static final float LOAD_FACTOR = 0.75f;            // 行 540
static final int TREEIFY_THRESHOLD = 8;                     // 行 550
static final int UNTREEIFY_THRESHOLD = 6;                   // 行 557
static final int MIN_TREEIFY_CAPACITY = 64;                 // 行 565
private static final int MIN_TRANSFER_STRIDE = 16;          // 行 574

// 特殊哈希编码（行 596-599）
static final int MOVED     = -1; // ForwardingNode
static final int TREEBIN   = -2; // TreeBin 根
static final int RESERVED  = -3; // ReservationNode
static final int HASH_BITS = 0x7fffffff; // 正常节点可用哈希位
```

### 3.3 核心字段（行 792-829）

```java
transient volatile Node<K,V>[] table;          // 桶数组，延迟初始化
private transient volatile Node<K,V>[] nextTable; // 扩容时的新数组
private transient volatile long baseCount;      // 基础计数，无竞争时 CAS 更新
private transient volatile int sizeCtl;         // -1=初始化; -(1+N)=N线程扩容; 正数=扩容阈值
private transient volatile int transferIndex;   // 扩容时待迁移桶索引
private transient volatile int cellsBusy;       // CounterCell 操作的自旋锁
private transient volatile CounterCell[] counterCells; // 分片计数数组
```

---

## 4. Node 类型体系

### 4.1 Node — 链表节点（行 639-690）

```java
static class Node<K,V> implements Map.Entry<K,V> {
    final int hash;
    final K key;
    volatile V val;          // volatile 保证读可见性
    volatile Node<K,V> next; // volatile 支持无锁遍历
}
```

`key`/`hash` 为 final 不可变；`val`/`next` 为 volatile 使 `get()` 无需加锁。

### 4.2 TreeNode — 红黑树节点（行 2739-2788）

```java
static final class TreeNode<K,V> extends Node<K,V> {
    TreeNode<K,V> parent, left, right;
    TreeNode<K,V> prev;    // 用于删除时断开链接
    boolean red;
}
```

同时维护树结构（parent/left/right）和链表结构（next/prev），便于树化/退化转换。

### 4.3 TreeBin — 树根容器（行 2799-2807）

```java
static final class TreeBin<K,V> extends Node<K,V> {
    TreeNode<K,V> root;
    volatile TreeNode<K,V> first;
    volatile Thread waiter;
    volatile int lockState;
    static final int WRITER = 1, WAITER = 2, READER = 4;
}
```

**为什么需要 TreeBin？** 红黑树旋转会改变根节点，但桶数组中的引用不能变。TreeBin 作为稳定头节点，内部 `root` 指向实际树根。它还维护寄生读写锁（parasitic read-write lock），树重组时写者等待读者完成。

### 4.4 ForwardingNode — 扩容转发（行 2258-2290）

```java
static final class ForwardingNode<K,V> extends Node<K,V> {
    final Node<K,V>[] nextTable;
    ForwardingNode(Node<K,V>[] tab) {
        super(MOVED, null, null);  // hash = -1
        this.nextTable = tab;
    }
    // find() 转发到新表查找，支持连续扩容的循环跟踪
}
```

### 4.5 ReservationNode — 计算占位（行 2295-2303）

`computeIfAbsent`/`compute` 在空桶上先 CAS 放入 ReservationNode（hash = RESERVED = -3），防止其他线程同时操作。

### 4.6 hash 值分发逻辑

`get()` 通过 hash 符号位快速分发（行 949-967）：

```java
public V get(Object key) {
    Node<K,V>[] tab; Node<K,V> e, p; int n, eh; K ek;
    int h = spread(key.hashCode());
    if ((tab = table) != null && (n = tab.length) > 0 &&
        (e = tabAt(tab, (n - 1) & h)) != null) {
        if ((eh = e.hash) == h) {            // 首节点直接命中
            if ((ek = e.key) == key || (ek != null && key.equals(ek)))
                return e.val;
        }
        else if (eh < 0)                     // 特殊节点，多态 find()
            return (p = e.find(h, key)) != null ? p.val : null;
        while ((e = e.next) != null) {       // 链表遍历
            if (e.hash == h &&
                ((ek = e.key) == key || (ek != null && key.equals(ek))))
                return e.val;
        }
    }
    return null;
}
```

`hash >= 0` 走链表遍历；`hash < 0` 调用多态 `find()` 方法（ForwardingNode 转发新表、TreeBin 走树查找）。**get() 全程无锁（lock-free）**，依赖 volatile 语义和 `tabAt()` 的 acquire 读。

---

## 5. 哈希扰动 (Hash Spreading)

```java
// 行 710-712
static final int spread(int h) {
    return (h ^ (h >>> 16)) & HASH_BITS;  // HASH_BITS = 0x7fffffff
}
```

`h ^ (h >>> 16)` 将高 16 位混入低位减少碰撞；`& 0x7fffffff` 清除最高位保证非负，使负 hash 专用于特殊节点。

---

## 6. putVal 流程详解（行 1025-1092）

```
putVal(key, value)
  ├─ null check → NullPointerException（不允许 null key/value）
  ├─ hash = spread(key.hashCode())
  └─ for(;;) 自旋:
       ├─ table 未初始化 → initTable()
       ├─ 目标桶为空 → CAS 插入新 Node（无锁快速路径）
       ├─ 桶头 hash == MOVED → helpTransfer() 协助扩容后重试
       └─ synchronized(桶头节点 f) {
            ├─ double-check: tabAt(tab, i) == f
            ├─ fh >= 0: 链表遍历，找到更新/没找到尾插
            ├─ f instanceof TreeBin: putTreeVal() 插入树节点
            └─ f instanceof ReservationNode: 抛异常
          }
          binCount >= TREEIFY_THRESHOLD(8) → treeifyBin()
  addCount(1L, binCount)  // 更新计数，可能触发扩容
```

**空桶用 CAS**: 最常见场景，避免 synchronized 的对象头开销。
**非空桶用 synchronized**: 链表/树的多步修改无法用单次 CAS 完成。锁对象是桶头节点本身——最细粒度。
**double-check**: synchronized 获取前桶可能被扩容替换为 ForwardingNode，必须重新验证。

---

## 7. 扩容机制：并发迁移 (transfer)（行 2451-2584）

### 7.1 触发

`addCount()` 中元素总数 >= `sizeCtl` 时触发。首个线程 CAS `sizeCtl` 为负数发起扩容，后续线程可 CAS 加入协助。

### 7.2 stride 计算

```java
stride = (NCPU > 1) ? (n >>> 3) / NCPU : n;
if (stride < MIN_TRANSFER_STRIDE) stride = MIN_TRANSFER_STRIDE; // 最小 16
```

### 7.3 任务分配

新表容量翻倍（`n << 1`）。每个线程通过 CAS `transferIndex` 从右往左领取一段桶：

```
Thread-A: [48,63]  transferIndex: 64→48
Thread-B: [32,47]  transferIndex: 48→32
Thread-C: [16,31]  transferIndex: 32→16
Thread-D: [0, 15]  transferIndex: 16→0
```

### 7.4 链表桶迁移 — lastRun 优化

容量翻倍时，每个节点新位置仅两种：`hash & n == 0` 留原索引 `i`，否则去 `i + n`。

```java
// 找到最后一段连续同去向的链尾（lastRun），整体复用无需新建
int runBit = fh & n;
Node<K,V> lastRun = f;
for (Node<K,V> p = f.next; p != null; p = p.next) {
    int b = p.hash & n;
    if (b != runBit) { runBit = b; lastRun = p; }
}
// lastRun 之前的节点复制到 ln（低位链）或 hn（高位链）
setTabAt(nextTab, i, ln);
setTabAt(nextTab, i + n, hn);
setTabAt(tab, i, fwd);  // 原桶标记为 ForwardingNode
```

### 7.5 树桶迁移

按高低位拆分后，若节点数 <= `UNTREEIFY_THRESHOLD(6)` 则退化为链表：

```java
ln = (lc <= UNTREEIFY_THRESHOLD) ? untreeify(lo) :
    (hc != 0) ? new TreeBin<K,V>(lo) : t;
```

### 7.6 完成切换

```java
if (finishing) {
    nextTable = null;
    table = nextTab;
    sizeCtl = (n << 1) - (n >>> 1);  // 新阈值 = 1.5n = 2n * 0.75
}
```

### 7.7 helpTransfer（行 2390-2408）

`putVal()` 遇到 ForwardingNode 时调用，CAS `sizeCtl + 1` 加入扩容。

---

## 8. 树化与退化 (Treeification)

### 8.1 treeifyBin（行 2692-2716）

```java
private final void treeifyBin(Node<K,V>[] tab, int index) {
    if ((n = tab.length) < MIN_TREEIFY_CAPACITY)  // < 64
        tryPresize(n << 1);    // 优先扩容而非树化！
    else {
        synchronized (b) {
            // 链表 Node → TreeNode 双向链表 → new TreeBin(hd)
            setTabAt(tab, index, new TreeBin<K,V>(hd));
        }
    }
}
```

**MIN_TREEIFY_CAPACITY = 64**: 小表中长链更可能是容量不足（而非哈希质量差），扩容即可解决。源码注释要求 "at least 4 * TREEIFY_THRESHOLD"。

### 8.2 阈值设计原理

- **TREEIFY_THRESHOLD = 8**: 理想随机哈希下，桶中 8 个元素的泊松概率约 0.00000006。一旦发生说明哈希质量差或遭攻击，树化保护将查找从 O(n) 降至 O(log n)
- **UNTREEIFY_THRESHOLD = 6**: 与 8 留出间隔 2，避免临界点反复树化/退化的抖动（thrashing）

---

## 9. computeIfAbsent 死锁陷阱

### 9.1 问题

```java
ConcurrentHashMap<String, String> map = new ConcurrentHashMap<>();
// 如果 "AaAa" 和 "BBBB" 哈希到同一个桶 → 死锁或异常
map.computeIfAbsent("AaAa", k -> {
    map.computeIfAbsent("BBBB", k2 -> "v2");  // 危险！
    return "v1";
});
```

### 9.2 原因

`computeIfAbsent`（行 1718-1805）在 synchronized 块内调用 `mappingFunction.apply(key)`。如果 lambda 中对同 map 的操作命中同一个桶，会因锁竞争导致死锁或触发递归检测：

```java
// 行 1768-1769: 递归修改检测
if (pred.next != null)
    throw new IllegalStateException("Recursive update");
```

空桶路径中，先 CAS 放入 ReservationNode 再在 synchronized(r) 内执行 lambda；非空桶路径中，直接在 synchronized(f) 内执行。`putVal` 遇到 ReservationNode 同样抛异常（行 1077-1078）。

### 9.3 建议

mapping function 中**不要修改同一个 map**。需要复合操作时，先计算值再单独 put。

---

## 10. size() 实现：分片计数 (Striped Counting)

### 10.1 CounterCell（行 2592-2595）

```java
@jdk.internal.vm.annotation.Contended  // 防止伪共享（false sharing）
static final class CounterCell {
    volatile long value;
    CounterCell(long x) { value = x; }
}
```

`@Contended` 在对象前后填充 padding，确保不同 cell 不在同一缓存行（cache line）。

### 10.2 addCount 三级递进策略（行 2351-2366）

1. **无竞争**: 直接 CAS `baseCount`
2. **轻度竞争**: 通过 `ThreadLocalRandom.getProbe()` 散列到某个 CounterCell，CAS 其 value
3. **重度竞争**: `fullAddCount()` 自适应扩容 CounterCell 数组（最大不超过 NCPU）

### 10.3 sumCount（行 2597-2606）

```java
final long sumCount() {
    CounterCell[] cs = counterCells;
    long sum = baseCount;
    if (cs != null) {
        for (CounterCell c : cs)
            if (c != null)
                sum += c.value;
    }
    return sum;
}
```

`size()` 返回 `(int) sumCount()` 截断到 `Integer.MAX_VALUE`（行 924-929）。
`mappingCount()` 返回 `long`（行 2201-2203），推荐使用以避免 int 溢出。

**注意**: 高并发下 `size()` 是近似值，遍历 cell 期间其他线程可能在修改。

---

## 11. 底层原子操作与 JDK 9+ 改进

### 11.1 tabAt / casTabAt / setTabAt（行 773-784）

```java
static final <K,V> Node<K,V> tabAt(Node<K,V>[] tab, int i) {
    return (Node<K,V>)U.getReferenceAcquire(tab, ((long)i << ASHIFT) + ABASE);
}
static final <K,V> boolean casTabAt(Node<K,V>[] tab, int i, Node<K,V> c, Node<K,V> v) {
    return U.compareAndSetReference(tab, ((long)i << ASHIFT) + ABASE, c, v);
}
static final <K,V> void setTabAt(Node<K,V>[] tab, int i, Node<K,V> v) {
    U.putReferenceRelease(tab, ((long)i << ASHIFT) + ABASE, v);
}
```

Java 的 `volatile` 不能作用于数组元素（只保证引用本身），必须通过 Unsafe 实现元素级原子/有序访问。

### 11.2 Unsafe 字段偏移量（行 6385-6404）

```java
private static final Unsafe U = Unsafe.getUnsafe();
private static final long SIZECTL    = U.objectFieldOffset(ConcurrentHashMap.class, "sizeCtl");
private static final long TRANSFERINDEX = U.objectFieldOffset(ConcurrentHashMap.class, "transferIndex");
private static final long BASECOUNT  = U.objectFieldOffset(ConcurrentHashMap.class, "baseCount");
private static final long CELLSBUSY  = U.objectFieldOffset(ConcurrentHashMap.class, "cellsBusy");
private static final long CELLVALUE  = U.objectFieldOffset(CounterCell.class, "value");
```

### 11.3 JDK 9+ VarHandle 迁移状态

JDK 9 引入 `VarHandle` 作为 Unsafe 的标准替代品。许多 JDK 类已迁移（如 AtomicInteger/AtomicReference），但 ConcurrentHashMap **仍使用 `jdk.internal.misc.Unsafe`**。原因：

1. 性能极度敏感的热路径，VarHandle 的方法句柄分派有微小开销
2. 作为 `java.base` 模块可直接使用 internal Unsafe
3. 数组元素的泛型访问模式不如 Unsafe raw offset 灵活

不过已使用较新 API（`getReferenceAcquire`/`putReferenceRelease` 而非旧的 `getObjectVolatile`/`putObjectVolatile`），体现分步迁移过程。

地址计算公式: `address = ABASE + (index << ASHIFT)`，其中 ASHIFT = `log2(arrayIndexScale)`。

```java
// 行 6400-6404
static {
    int scale = U.arrayIndexScale(Node[].class);
    if ((scale & (scale - 1)) != 0)
        throw new ExceptionInInitializerError("array index scale not a power of two");
    ASHIFT = 31 - Integer.numberOfLeadingZeros(scale);
}
```

---

## 12. 并发语义保证

### 12.1 get() 的无锁读

- `table` 字段是 `volatile`，保证读到最新的数组引用
- `tabAt()` 用 acquire 语义读桶头，保证看到最新的节点
- `Node.val` 和 `Node.next` 是 `volatile`，遍历期间能看到最新值

### 12.2 put() 的一致性

- 空桶: CAS 保证原子写入
- 非空桶: `synchronized(f)` 保证互斥 + 内存可见性
- 扩容期间: ForwardingNode 转发到新表，保证读者不丢失数据

### 12.3 弱一致性迭代器 (Weakly Consistent Iterator)

ConcurrentHashMap 的迭代器不会抛出 `ConcurrentModificationException`，但：
- 可能反映也可能不反映迭代开始后的修改
- 保证每个元素最多返回一次
- 这是 **弱一致性**（weakly consistent）而非快照（snapshot）语义

---

## 13. 性能特征与最佳实践

### 13.1 时间复杂度

| 操作 | 无竞争 | 有竞争 | 最坏情况 |
|------|--------|--------|----------|
| get() | O(1) 无锁 | O(1) 无锁 | O(log n) 树查找 |
| put() 空桶 | O(1) CAS | O(1) CAS 重试 | O(1) |
| put() 链表桶 | O(k) synchronized | O(k) + 锁等待 | O(k) k=链长 |
| put() 树桶 | O(log k) synchronized | O(log k) + 锁等待 | O(log k) |
| size() | O(1) 读 baseCount | O(c) 遍历 cells | O(c) c=cell数 |
| 扩容 | 均摊 O(1) per put | 多线程并行 | O(n) 总迁移量 |

### 13.2 与 HashMap 关键差异

| 特性 | HashMap | ConcurrentHashMap |
|------|---------|-------------------|
| 线程安全 | 否 | 是 |
| null key/value | 允许 | 不允许 |
| 哈希扰动 | `h ^ (h >>> 16)` | `(h ^ (h >>> 16)) & 0x7fffffff` |
| 迭代器 | fail-fast | weakly consistent |
| size() | 精确 O(1) | 近似 O(cells) |
| Node.val/next | 非 volatile | volatile |
| 锁机制 | 无 | CAS + synchronized per-bin |

### 13.3 最佳实践

1. **预估容量**: `new ConcurrentHashMap<>(expectedSize)` 减少扩容次数
2. **避免频繁 size()**: 高频调用有遍历 cell 的开销
3. **使用 computeIfAbsent**: 原子的「查不到就算」，但不要在 lambda 中修改同 map
4. **不要包装 synchronizedMap**: ConcurrentHashMap 本身线程安全
5. **null 值替代**: 不支持 null，需要时用 `Optional` 或哨兵对象
6. **优先用 mappingCount()**: 返回 long，避免 `size()` 的 int 溢出截断

---

## 14. 源码导航索引

| 内容 | 起始行 |
|------|--------|
| 常量定义 (DEFAULT_CAPACITY 等) | 519 |
| 哈希编码 (MOVED/TREEBIN/RESERVED) | 596 |
| Node 类 | 639 |
| spread() 哈希扰动 | 710 |
| tabAt / casTabAt / setTabAt | 773 |
| 字段声明 (table/sizeCtl 等) | 786 |
| get() | 949 |
| putVal() | 1025 |
| computeIfAbsent() | 1718 |
| mappingCount() | 2201 |
| ForwardingNode | 2258 |
| ReservationNode | 2295 |
| addCount() | 2351 |
| transfer() | 2451 |
| CounterCell / sumCount() | 2592 |
| treeifyBin() | 2692 |
| TreeNode | 2739 |
| TreeBin | 2799 |
| Unsafe 字段偏移量 | 6385 |
