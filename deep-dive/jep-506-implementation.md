# JEP 506: Scoped Values 实现分析

> 基于 JDK 25 源码的 Scoped Values 内部实现深度解析

---

## 1. 背景与设计动机

### ThreadLocal 的固有问题

ThreadLocal 在 Java 1.2 引入，长期作为线程局部存储（thread-local storage）的标准方案。但其设计存在多个根本性缺陷：

```java
// 文件: 典型 ThreadLocal 使用模式
public class RequestContext {
    private static final ThreadLocal<User> currentUser = new ThreadLocal<>();

    public void handleRequest(User user) {
        currentUser.set(user);
        try {
            processRequest();
        } finally {
            currentUser.remove();  // 容易忘记！导致内存泄漏
        }
    }
}
```

问题总结：
1. **内存泄漏（memory leak）**: 忘记调用 `remove()` 导致值一直驻留，尤其在线程池场景
2. **可变性（mutability）**: 任何持有 ThreadLocal 引用的代码都可以 `set()` 修改值，破坏不变性约束
3. **虚拟线程不友好**: 百万级虚拟线程时，每个线程都有独立的 ThreadLocalMap 副本，内存占用巨大
4. **继承代价高**: `InheritableThreadLocal` 在创建子线程时必须完整复制整个 map

### ScopedValue 的设计目标

ScopedValue（@since 25）提供了一种结构化的、不可变的、自动管理生命周期的线程上下文传递机制：

```java
// 文件: ScopedValue 使用模式
private static final ScopedValue<User> CURRENT_USER = ScopedValue.newInstance();

public void handleRequest(User user) {
    ScopedValue.where(CURRENT_USER, user).run(() -> {
        processRequest();  // 作用域内自动可见，退出自动清理
    });
}
```

核心优势：
1. **自动清理**: 作用域（dynamic scope）结束后绑定自动失效，无需手动 remove
2. **不可变**: 绑定建立后无法修改，只能通过嵌套 rebind 创建新的遮蔽绑定
3. **虚拟线程友好**: 继承仅需复制一个指针，而非复制整个 map
4. **结构化并发集成**: 与 `StructuredTaskScope` 天然配合

---

## 2. 核心数据结构

### ScopedValue 类本身

```java
// 文件: src/java.base/share/classes/java/lang/ScopedValue.java

public final class ScopedValue<T> {
    private final int hash;

    @Override
    public int hashCode() { return hash; }

    @Stable
    static IntSupplier hashGenerator;

    private ScopedValue() {
        IntSupplier nextHash = hashGenerator;
        this.hash = nextHash != null ? nextHash.getAsInt() : generateKey();
    }

    public static <T> ScopedValue<T> newInstance() {
        return new ScopedValue<T>();
    }
}
```

关键实现细节：
- **无全局 ID 计数器**: 没有使用 `AtomicInteger` 做自增 ID，而是使用**哈希值**（hash）标识
- **哈希生成器（hash generator）**: 初始化前使用 Marsaglia xor-shift 生成器 `generateKey()`，初始化后切换为 `ThreadLocalRandom` 提供的种子
- **`@Stable` 注解**: `hashGenerator` 字段标注 `@Stable`，使得 JIT 可以将其视为常量折叠优化
- **哈希约束**: 生成器保证 `primarySlot(hash) != secondarySlot(hash)`，即同一个 ScopedValue 的两个缓存槽位不会冲突

哈希生成算法（Marsaglia xor-shift）：

```java
// 文件: src/java.base/share/classes/java/lang/ScopedValue.java

private static int nextKey = 0xf0f0_f0f0;

// 满周期（full period）xor-shift 生成器，生成 2^32-1 个哈希后才会重复
private static synchronized int generateKey() {
    int x = nextKey;
    do {
        x ^= x >>> 12;
        x ^= x << 9;
        x ^= x >>> 23;
    } while (((Cache.primaryIndex(x) ^ Cache.secondaryIndex(x)) & 1) == 0);
    return (nextKey = x);
}
```

### Carrier 链表（绑定载体）

`Carrier` 是 ScopedValue 绑定的不可变链表节点，每次调用 `where()` 创建一个新节点：

```java
// 文件: src/java.base/share/classes/java/lang/ScopedValue.java

public static final class Carrier {
    // 位掩码（bit mask）: 1 表示此绑定集合命中缓存中的该槽位
    final int bitmask;
    final ScopedValue<?> key;
    final Object value;
    final Carrier prev;

    Carrier(ScopedValue<?> key, Object value, Carrier prev) {
        this.key = key;
        this.value = value;
        this.prev = prev;
        int bits = key.bitmask();
        if (prev != null) {
            bits |= prev.bitmask;
        }
        this.bitmask = bits;
    }

    // 创建单个绑定
    static <T> Carrier of(ScopedValue<T> key, T value) {
        return where(key, value, null);
    }

    // 链式追加绑定 —— 返回新的 Carrier（不可变）
    public <T> Carrier where(ScopedValue<T> key, T value) {
        return where(key, value, this);
    }

    private static <T> Carrier where(ScopedValue<T> key, T value, Carrier prev) {
        return new Carrier(key, value, prev);
    }

    Object get() { return value; }
    ScopedValue<?> getKey() { return key; }
}
```

关键设计点：
- **不可变链表**: 每次 `where()` 创建新 `Carrier` 节点，`prev` 指向前一个节点，形成单向链表
- **bitmask 累积**: 每个 `Carrier` 的 `bitmask` 是自身 key 的 bitmask 与 `prev.bitmask` 的 OR 结果，用于快速判断是否可能包含某个 key
- **值类型为 Object**: `value` 存储为 `Object`，在 `get()` 时通过泛型转换还原类型

### Snapshot（绑定快照）

`Snapshot` 是一个不可变的映射（immutable map），记录某一时刻所有 ScopedValue 的绑定状态：

```java
// 文件: src/java.base/share/classes/java/lang/ScopedValue.java

static final class Snapshot {
    final Snapshot prev;        // 前一个 Snapshot（外层作用域）
    final Carrier bindings;    // 此作用域的绑定链
    final int bitmask;         // 累积 bitmask

    private static final Object NIL = new Object();  // 哨兵值：表示"未找到"

    static final Snapshot EMPTY_SNAPSHOT = new Snapshot();

    Snapshot(Carrier bindings, Snapshot prev) {
        this.prev = prev;
        this.bindings = bindings;
        this.bitmask = bindings.bitmask | prev.bitmask;
    }

    protected Snapshot() {
        this.prev = null;
        this.bindings = null;
        this.bitmask = 0;
    }

    Object find(ScopedValue<?> key) {
        int bits = key.bitmask();
        for (Snapshot snapshot = this;
             containsAll(snapshot.bitmask, bits);
             snapshot = snapshot.prev) {
            for (Carrier carrier = snapshot.bindings;
                 carrier != null && containsAll(carrier.bitmask, bits);
                 carrier = carrier.prev) {
                if (carrier.getKey() == key) {
                    Object value = carrier.get();
                    return value;
                }
            }
        }
        return NIL;
    }
}
```

查找算法的核心优化 —— **bitmask 快速剪枝（bloom filter 风格）**：
- 每个 `ScopedValue` 根据其 hash 计算一个 bitmask（在缓存槽位上的投影）
- `Snapshot` 和 `Carrier` 的 bitmask 是所有子项 bitmask 的 OR 累积
- `containsAll(bitmask, targetBits)` 检查 `(bitmask & targetBits) == targetBits`
- 如果 Snapshot 的 bitmask 不包含目标 key 的 bits，可以立即跳过该层及所有外层 —— 避免不必要的链表遍历

### 数据结构关系图

```
Thread
  └── scopedValueBindings: Object  ──→  Snapshot
                                          ├── bindings: Carrier → Carrier → Carrier → null
                                          │               (key3,v3)  (key2,v2)  (key1,v1)
                                          ├── prev ──→ Snapshot (外层作用域)
                                          │              ├── bindings: Carrier → ...
                                          │              └── prev ──→ ...
                                          └── bitmask: int (累积)
```

---

## 3. Thread 集成：线程侧存储

### Thread 中的字段

```java
// 文件: src/java.base/share/classes/java/lang/Thread.java

public class Thread implements Runnable {
    // ScopedValue 绑定 —— 声明为 Object（实际类型为 Snapshot 或哨兵值）
    private Object scopedValueBindings;

    // 新线程的初始哨兵值（special sentinel）
    private static final Object NEW_THREAD_BINDINGS = Thread.class;

    // 获取当前线程的绑定
    static Object scopedValueBindings() {
        return currentThread().scopedValueBindings;
    }

    // 设置当前线程的绑定
    static void setScopedValueBindings(Object bindings) {
        currentThread().scopedValueBindings = bindings;
    }

    // JVM 内部方法：获取 per-thread 缓存数组
    @IntrinsicCandidate
    static native Object[] scopedValueCache();

    // JVM 内部方法：设置 per-thread 缓存数组
    @IntrinsicCandidate
    static native void setScopedValueCache(Object[] cache);
}
```

**绑定状态机**（binding state machine）：
1. **`Thread.class`（`NEW_THREAD_BINDINGS`）**: 新创建的线程，从未绑定过任何 ScopedValue
2. **`Snapshot.EMPTY_SNAPSHOT`**: 明确为空的绑定（已经查找过，确认为空）
3. **`Snapshot` 实例**: 包含一个或多个绑定
4. **`null`**: 可能存在绑定但位置未知，需要**栈遍历**（stack walk）查找

`scopedValueBindings` 为 `null` 时的处理：

```java
// 文件: src/java.base/share/classes/java/lang/ScopedValue.java

private static Snapshot scopedValueBindings() {
    Object bindings = Thread.scopedValueBindings();
    if (bindings == NEW_THREAD_BINDINGS) {
        return Snapshot.EMPTY_SNAPSHOT;
    }
    if (bindings == null) {
        // 搜索栈帧（stack walk）—— 这是 JVM 实现的 native 方法
        bindings = Thread.findScopedValueBindings();
        if (bindings == NEW_THREAD_BINDINGS || bindings == null) {
            bindings = Snapshot.EMPTY_SNAPSHOT;
        }
        Thread.setScopedValueBindings(bindings);
    }
    assert (bindings != null);
    return (Snapshot) bindings;
}
```

`Thread.findScopedValueBindings()` 执行栈遍历（stack walk），查找 `Carrier.runWith()` 方法的栈帧以恢复绑定。这在虚拟线程 unmount/remount 后特别重要。

---

## 4. 绑定与执行机制

### where() 入口方法

```java
// 文件: src/java.base/share/classes/java/lang/ScopedValue.java

// 静态入口 —— 创建第一个 Carrier
public static <T> Carrier where(ScopedValue<T> key, T value) {
    return Carrier.of(key, value);
}
```

### Carrier.run() 执行流程

```java
// 文件: src/java.base/share/classes/java/lang/ScopedValue.java

public void run(Runnable op) {
    Objects.requireNonNull(op);
    Cache.invalidate(bitmask);          // 1. 使受影响的缓存槽失效
    var prevSnapshot = scopedValueBindings();  // 2. 获取当前绑定
    var newSnapshot = new Snapshot(this, prevSnapshot);  // 3. 创建新 Snapshot
    runWith(newSnapshot, op);           // 4. 在新绑定下执行
}

@Hidden
@ForceInline
private void runWith(Snapshot newSnapshot, Runnable op) {
    try {
        Thread.setScopedValueBindings(newSnapshot);             // 设置新绑定
        Thread.ensureMaterializedForStackWalk(newSnapshot);     // 确保 GC 可达
        ScopedValueContainer.run(op);                           // 通过容器执行
    } finally {
        Reference.reachabilityFence(newSnapshot);               // 防止提前 GC
        Thread.setScopedValueBindings(newSnapshot.prev);        // 恢复前一个绑定
        Cache.invalidate(bitmask);                              // 再次使缓存失效
    }
}
```

关键注解含义：
- **`@Hidden`**: 标记此方法在 stack trace 中不可见，JVM 在栈遍历时识别该方法
- **`@ForceInline`**: 强制 JIT 编译器内联此方法，避免方法调用开销
- **`Thread.ensureMaterializedForStackWalk()`**: 确保 `newSnapshot` 不被 JIT 优化掉（escape analysis 可能将其标量替换），因为 JVM 需要通过栈帧找到它
- **`Reference.reachabilityFence()`**: 防止 GC 在 finally 块执行前回收 `newSnapshot`

### Carrier.call() 执行流程

```java
// 文件: src/java.base/share/classes/java/lang/ScopedValue.java

public <R, X extends Throwable> R call(CallableOp<? extends R, X> op) throws X {
    Objects.requireNonNull(op);
    Cache.invalidate(bitmask);
    var prevSnapshot = scopedValueBindings();
    var newSnapshot = new Snapshot(this, prevSnapshot);
    return runWith(newSnapshot, op);
}

@Hidden
@ForceInline
private <R, X extends Throwable> R runWith(Snapshot newSnapshot, CallableOp<R, X> op) {
    try {
        Thread.setScopedValueBindings(newSnapshot);
        Thread.ensureMaterializedForStackWalk(newSnapshot);
        return ScopedValueContainer.call(op);
    } finally {
        Reference.reachabilityFence(newSnapshot);
        Thread.setScopedValueBindings(newSnapshot.prev);
        Cache.invalidate(bitmask);
    }
}
```

### CallableOp 函数式接口

```java
// 文件: src/java.base/share/classes/java/lang/ScopedValue.java

@FunctionalInterface
public interface CallableOp<T, X extends Throwable> {
    T call() throws X;
}
```

与 `java.util.concurrent.Callable` 不同，`CallableOp` 可以声明受检异常类型，提供更好的类型安全性。

---

## 5. ScopedValueContainer：结构化执行容器

### 容器的角色

`ScopedValueContainer` 继承 `StackableScope`，在作用域栈（scope stack）上管理 ScopedValue 的绑定生命周期，并检测结构违规（structure violation）：

```java
// 文件: src/java.base/share/classes/jdk/internal/vm/ScopedValueContainer.java

public class ScopedValueContainer extends StackableScope {

    public static void run(Runnable op) {
        if (head() == null) {
            // 栈为空时无需 push scope
            runWithoutScope(op);
        } else {
            new ScopedValueContainer().doRun(op);
        }
    }

    private void doRun(Runnable op) {
        Throwable ex;
        boolean atTop;
        push();                     // 将容器推入作用域栈
        try {
            op.run();
            ex = null;
        } catch (Throwable e) {
            ex = e;
        } finally {
            atTop = popForcefully();  // 弹出容器（可能阻塞等待子作用域关闭）
        }
        throwIfFailed(ex, atTop);
    }
}
```

**结构违规检测（structure violation detection）**：
- `popForcefully()` 如果发现此容器不在栈顶（说明有未关闭的 `StructuredTaskScope`），则关闭所有中间作用域
- `throwIfFailed()` 在 `atTop == false` 时抛出 `StructureViolationException`

```java
// 文件: src/java.base/share/classes/jdk/internal/vm/ScopedValueContainer.java

private static void throwIfFailed(Throwable ex, boolean atTop) {
    if (ex != null || !atTop) {
        if (!atTop) {
            var sve = new StructureViolationException();
            if (ex == null) {
                ex = sve;
            } else {
                ex.addSuppressed(sve);
            }
        }
        Unsafe.getUnsafe().throwException(ex);
    }
}
```

### 绑定快照捕获

```java
// 文件: src/java.base/share/classes/jdk/internal/vm/ScopedValueContainer.java

public record BindingsSnapshot(Object scopedValueBindings,
                               ScopedValueContainer container) { }

public static BindingsSnapshot captureBindings() {
    return new BindingsSnapshot(JLA.scopedValueBindings(), latest());
}
```

`captureBindings()` 用于 `StructuredTaskScope` 在 fork 子任务时捕获当前线程的 ScopedValue 绑定。

---

## 6. 缓存实现（per-thread cache）

### Cache 内部类

缓存是 ScopedValue 性能的关键。每个线程维护一个 `Object[]` 数组作为 2-way set-associative 缓存：

```java
// 文件: src/java.base/share/classes/java/lang/ScopedValue.java

private static final class Cache {
    static final int INDEX_BITS = 4;                   // 必须是 2 的幂
    static final int TABLE_SIZE = 1 << INDEX_BITS;     // 16
    static final int TABLE_MASK = TABLE_SIZE - 1;      // 0xF
    static final int PRIMARY_MASK = (1 << TABLE_SIZE) - 1;  // 0xFFFF

    private static class Constants {
        private static final int CACHE_TABLE_SIZE, SLOT_MASK;
        private static final int MAX_CACHE_SIZE = 16;
        // ...

        static {
            final String propertyName = "java.lang.ScopedValue.cacheSize";
            var sizeString = System.getProperty(propertyName, "16");
            var cacheSize = Integer.valueOf(sizeString);
            if (cacheSize < 2 || cacheSize > MAX_CACHE_SIZE) {
                cacheSize = MAX_CACHE_SIZE;
            }
            if ((cacheSize & (cacheSize - 1)) != 0) {  // 必须是 2 的幂
                cacheSize = MAX_CACHE_SIZE;
            }
            CACHE_TABLE_SIZE = cacheSize;
            SLOT_MASK = cacheSize - 1;
        }
    }
}
```

**缓存结构**: `Object[]` 数组，大小为 `CACHE_TABLE_SIZE * 2`（默认 32 个元素）。偶数索引存 key（ScopedValue），奇数索引存 value。

### 2-way Set-Associative 查找

每个 ScopedValue 有两个可能的缓存位置（primary slot 和 secondary slot）：

```java
// 文件: src/java.base/share/classes/java/lang/ScopedValue.java

// get() 方法 —— 热路径，@ForceInline 强制内联
@ForceInline
@SuppressWarnings("unchecked")
public T get() {
    Object[] objects;
    if ((objects = scopedValueCache()) != null) {
        // 检查 primary slot
        int n = (hash & Cache.Constants.SLOT_MASK) * 2;
        if (objects[n] == this) {
            return (T)objects[n + 1];
        }
        // 检查 secondary slot
        n = ((hash >>> Cache.INDEX_BITS) & Cache.Constants.SLOT_MASK) * 2;
        if (objects[n] == this) {
            return (T)objects[n + 1];
        }
    }
    return slowGet();
}
```

缓存未命中时的慢速路径：

```java
// 文件: src/java.base/share/classes/java/lang/ScopedValue.java

private T slowGet() {
    Object value = scopedValueBindings().find(this);  // 遍历 Snapshot 链
    if (value == Snapshot.NIL) {
        throw new NoSuchElementException("ScopedValue not bound");
    }
    Cache.put(this, value);  // 更新缓存
    return (T)value;
}
```

### 缓存插入策略

```java
// 文件: src/java.base/share/classes/java/lang/ScopedValue.java

static void put(ScopedValue<?> key, Object value) {
    Object[] theCache = scopedValueCache();
    if (theCache == null) {
        theCache = new Object[Constants.CACHE_TABLE_SIZE * 2];
        setScopedValueCache(theCache);
    }
    // 两个候选位置中随机选择一个作为牺牲者（victim）
    int k1 = primarySlot(key);
    int k2 = secondarySlot(key);
    var usePrimaryIndex = chooseVictim();
    int victim = usePrimaryIndex ? k1 : k2;
    int other = usePrimaryIndex ? k2 : k1;
    setKeyAndObjectAt(victim, key, value);
    if (getKey(theCache, other) == key) {
        setKeyAndObjectAt(other, key, value);
    }
}

// 伪随机选择，偏向于选择 primary slot（约 2:1 的偏向比）
private static boolean chooseVictim() {
    int r = Constants.THREAD_LOCAL_RANDOM_ACCESS.nextSecondaryThreadLocalRandomSeed();
    return (r & 15) >= 5;  // 11/16 概率选 primary
}
```

### 缓存失效

绑定变更时，通过 bitmask 精确失效受影响的缓存条目：

```java
// 文件: src/java.base/share/classes/java/lang/ScopedValue.java

static void invalidate(int toClearBits) {
    toClearBits = ((toClearBits >>> Cache.TABLE_SIZE) | toClearBits) & PRIMARY_MASK;
    Object[] objects;
    if ((objects = scopedValueCache()) != null) {
        for (int bits = toClearBits; bits != 0; ) {
            int index = Integer.numberOfTrailingZeros(bits);
            setKeyAndObjectAt(objects, index & Constants.SLOT_MASK, null, null);
            bits &= ~1 << index;
        }
    }
}
```

失效策略的精妙之处：
- **不是全量清除**: 只清除与变更绑定的 ScopedValue 的 bitmask 关联的槽位
- **在 run/call 的入口和出口都执行**: 入口失效确保新绑定生效；出口失效确保旧绑定恢复

### bitmask 计算

```java
// 文件: src/java.base/share/classes/java/lang/ScopedValue.java

int bitmask() {
    return (1 << Cache.primaryIndex(hash))
         | (1 << (Cache.secondaryIndex(hash) + Cache.TABLE_SIZE));
}

static int primaryIndex(int hash) {
    return hash & Cache.TABLE_MASK;    // 低 4 位
}

static int secondaryIndex(int hash) {
    return (hash >> INDEX_BITS) & Cache.TABLE_MASK;  // 次低 4 位
}
```

bitmask 是一个 32-bit 值：低 16 位对应 primary slot 索引，高 16 位对应 secondary slot 索引。

### 缓存的 JVM intrinsic 实现

`Thread.scopedValueCache()` 和 `Thread.setScopedValueCache()` 是 `@IntrinsicCandidate` 方法，由 JVM 直接在 native 层实现，访问线程对象中的专用字段，无需 JNI 开销。

```java
// 文件: src/java.base/share/classes/java/lang/Thread.java

@IntrinsicCandidate
static native Object[] scopedValueCache();

@IntrinsicCandidate
static native void setScopedValueCache(Object[] cache);
```

系统属性 `jdk.preserveScopedValueCache`（默认 `true`）控制虚拟线程阻塞时是否保留缓存。设为 `false` 可以在大量虚拟线程阻塞场景下节省内存，但每次 remount 时需要重建缓存。

---

## 7. 值读取 API

### get() 方法

```java
// 文件: src/java.base/share/classes/java/lang/ScopedValue.java

@ForceInline
public T get() {
    // ... 缓存查找（见上文）...
    return slowGet();
}
```

### orElse() 方法

```java
// 文件: src/java.base/share/classes/java/lang/ScopedValue.java

public T orElse(T other) {
    Objects.requireNonNull(other);
    Object obj = findBinding();
    if (obj != Snapshot.NIL) {
        @SuppressWarnings("unchecked")
        T value = (T) obj;
        return value;
    } else {
        return other;
    }
}
```

### orElseThrow() 方法

```java
// 文件: src/java.base/share/classes/java/lang/ScopedValue.java

public <X extends Throwable> T orElseThrow(Supplier<? extends X> exceptionSupplier) throws X {
    Objects.requireNonNull(exceptionSupplier);
    Object obj = findBinding();
    if (obj != Snapshot.NIL) {
        @SuppressWarnings("unchecked")
        T value = (T) obj;
        return value;
    } else {
        throw exceptionSupplier.get();
    }
}
```

### isBound() 方法

```java
// 文件: src/java.base/share/classes/java/lang/ScopedValue.java

public boolean isBound() {
    Object obj = findBinding();
    return obj != Snapshot.NIL;
}
```

`findBinding()` 是所有读取 API 的统一入口，先查缓存、后查 Snapshot 链：

```java
// 文件: src/java.base/share/classes/java/lang/ScopedValue.java

private Object findBinding() {
    Object[] objects = scopedValueCache();
    if (objects != null) {
        int n = (hash & Cache.Constants.SLOT_MASK) * 2;
        if (objects[n] == this) {
            return objects[n + 1];
        }
        n = ((hash >>> Cache.INDEX_BITS) & Cache.Constants.SLOT_MASK) * 2;
        if (objects[n] == this) {
            return objects[n + 1];
        }
    }
    Object value = scopedValueBindings().find(this);
    boolean found = (value != Snapshot.NIL);
    if (found)  Cache.put(this, value);
    return value;
}
```

---

## 8. 与结构化并发集成

### StructuredTaskScope 中的继承

`StructuredTaskScope` 在创建时捕获当前线程的 ScopedValue 绑定，fork 的子任务自动继承：

```java
// 使用示例
private static final ScopedValue<User> CURRENT_USER = ScopedValue.newInstance();
private static final ScopedValue<Database> DB = ScopedValue.newInstance();

public Response handleRequest(User user, Request request) throws Exception {
    return ScopedValue.where(CURRENT_USER, user)
        .where(DB, Database.connect())
        .call(() -> {
            try (var scope = StructuredTaskScope.open()) {
                // 子任务自动继承 CURRENT_USER 和 DB 的绑定
                var order = scope.fork(() -> fetchOrder(request.orderId()));
                var inventory = scope.fork(() -> checkInventory(request.itemId()));
                scope.join();
                return new Response(order.get(), inventory.get());
            }
        });
}
```

继承机制的实现核心：
- `StructuredTaskScope` 在构造时调用 `ScopedValueContainer.captureBindings()` 捕获 `BindingsSnapshot`
- fork 的子虚拟线程在启动时将父线程的 `scopedValueBindings` 设置为自己的初始绑定
- 继承成本极低：本质上是复制一个指针（`Snapshot` 引用），而非复制整个 map

```java
// 文件: src/java.base/share/classes/java/lang/Thread.java
// 线程验证 scoped value bindings 一致性

void setScopedValueBindings(ScopedValueContainer container) {
    ScopedValueContainer.BindingsSnapshot snapshot;
    if (container.owner() != null
            && (snapshot = container.scopedValueBindings()) != null) {
        Object bindings = snapshot.scopedValueBindings();
        if (currentThread().scopedValueBindings != bindings) {
            throw new StructureViolationException("Scoped value bindings have changed");
        }
        this.scopedValueBindings = bindings;
    }
}
```

### Rebinding（嵌套重绑定）

在子作用域中可以为同一个 ScopedValue 绑定新值，退出后自动恢复：

```java
private static final ScopedValue<String> NAME = ScopedValue.newInstance();

ScopedValue.where(NAME, "duke").run(() -> {
    System.out.println(NAME.get());  // "duke"

    ScopedValue.where(NAME, "duchess").run(() -> {
        System.out.println(NAME.get());  // "duchess" —— 内层遮蔽外层
    });

    System.out.println(NAME.get());  // "duke" —— 自动恢复
});
```

实现原理：`Snapshot` 的 `find()` 从内层向外层遍历，找到的第一个匹配即返回。外层的同名绑定被遮蔽（shadowed），但并未被修改。

---

## 9. 性能分析

### 缓存命中时的 get() 成本

缓存命中时，`get()` 只需要：
1. 一次 native 调用获取 `Object[]` 缓存数组（JVM intrinsic，极快）
2. 一次哈希计算和数组索引
3. 一次引用比较（`objects[n] == this`）
4. 一次数组元素读取

这在 JIT 编译后几乎等价于一次数组访问，远快于 ThreadLocal 的 `ThreadLocalMap.getEntry()` 查找。

### ScopedValue vs ThreadLocal 对比

```
┌─────────────────────────┬──────────────┬──────────────┬─────────────┐
│ 特性                     │ ThreadLocal  │ ScopedValue  │ 说明        │
├─────────────────────────┼──────────────┼──────────────┼─────────────┤
│ get() 缓存命中           │ ~5 ns        │ ~2-3 ns      │ SV 更快     │
│ 绑定/解绑                │ set+remove   │ 自动         │ SV 无泄漏   │
│ 继承成本（per-thread）   │ O(n) 复制    │ O(1) 指针    │ SV 显著优势 │
│ 100万虚拟线程内存        │ 100万份副本  │ 共享同一份   │ SV 节省99%+ │
│ 可变性                   │ 可变         │ 不可变       │ SV 更安全   │
│ 结构化并发               │ 不支持       │ 原生支持     │ SV 独有     │
└─────────────────────────┴──────────────┴──────────────┴─────────────┘
```

### 缓存大小调优

系统属性 `java.lang.ScopedValue.cacheSize` 控制缓存大小（默认 16，范围 2-16，必须为 2 的幂）：

```bash
# 减小缓存以节省内存（适合少量 ScopedValue）
-Djava.lang.ScopedValue.cacheSize=4

# 使用最大缓存（默认值）
-Djava.lang.ScopedValue.cacheSize=16
```

设计建议：若需传递多个值，建议将它们打包到一个 record 中，只使用一个 ScopedValue 绑定，以减少缓存压力。

---

## 10. 迁移指南

### 从 ThreadLocal 迁移到 ScopedValue

```java
// === 迁移前: ThreadLocal ===
private static final ThreadLocal<User> currentUser = new ThreadLocal<>();

public void handle(User user) {
    currentUser.set(user);
    try {
        process();
    } finally {
        currentUser.remove();  // 必须手动清理
    }
}
public User getCurrentUser() {
    return currentUser.get();  // 可能返回 null
}

// === 迁移后: ScopedValue ===
private static final ScopedValue<User> CURRENT_USER = ScopedValue.newInstance();

public void handle(User user) {
    ScopedValue.where(CURRENT_USER, user).run(() -> {
        process();  // 退出自动清理
    });
}
public User getCurrentUser() {
    return CURRENT_USER.get();  // 未绑定抛 NoSuchElementException
}
```

### 不适合迁移的场景

ScopedValue 不能替代 ThreadLocal 的所有用途：
- **需要在作用域内修改值的场景**: ScopedValue 绑定不可变
- **需要无限生命周期的场景**: ScopedValue 严格绑定到作用域
- **需要在非结构化并发中共享的场景**: ScopedValue 仅支持通过 `StructuredTaskScope` 继承

---

## 11. 源码文件索引

| 文件路径 | 内容 |
|---------|------|
| `src/java.base/share/classes/java/lang/ScopedValue.java` | ScopedValue 主类、Carrier、Snapshot、Cache |
| `src/java.base/share/classes/java/lang/Thread.java` | `scopedValueBindings` 字段、cache native 方法 |
| `src/java.base/share/classes/jdk/internal/vm/ScopedValueContainer.java` | 结构化执行容器、BindingsSnapshot |

---

## 12. 相关链接

- [JEP 506: Scoped Values](/jeps/concurrency/jep-506.md)
- [JEP 525: Structured Concurrency](/jeps/concurrency/jep-525.md)
- [源码浏览](https://github.com/openjdk/jdk/tree/master/src/java.base/share/classes/java/lang)
