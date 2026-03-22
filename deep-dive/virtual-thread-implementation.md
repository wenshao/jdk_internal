# Virtual Thread 源码级深度解析

> 基于 JDK 源码 `java.lang.VirtualThread`（1445 行）、`jdk.internal.vm.Continuation`（507 行）、
> `jdk.internal.misc.CarrierThread` 的实际实现。所有代码引用均来自真实源码。

---

## 目录

1. [类继承结构与核心字段](#1-类继承结构与核心字段)
2. [20 个状态常量详解](#2-20-个状态常量详解)
3. [状态转换图](#3-状态转换图)
4. [生命周期：从 start 到 terminate](#4-生命周期从-start-到-terminate)
5. [mount/unmount 机制](#5-mountunmount-机制)
6. [Continuation 运行原理](#6-continuation-运行原理)
7. [ForkJoinPool 调度器](#7-forkjoinpool-调度器)
8. [park/unpark 实现](#8-parkunpark-实现)
9. [JEP 491 monitor 支持](#9-jep-491-monitor-支持)
10. [Object.wait/notify 支持](#10-objectwaitnotify-支持)
11. [中断机制](#11-中断机制)
12. [Pinning 机制](#12-pinning-机制)
13. [定时任务调度](#13-定时任务调度)
14. [关键设计总结](#14-关键设计总结)

---

## 1. 类继承结构与核心字段

### 继承层次 (Inheritance Hierarchy)

```
java.lang.Thread
  └── java.lang.BaseVirtualThread  (abstract sealed class)
        ├── java.lang.VirtualThread           (final class, 主实现)
        └── ThreadBuilders.BoundVirtualThread  (测试/内部用)
```

`BaseVirtualThread` 是一个 `sealed` 抽象类，定义了虚拟线程的核心抽象方法：

```java
abstract sealed class BaseVirtualThread extends Thread
        permits VirtualThread, ThreadBuilders.BoundVirtualThread {
    abstract void park();
    abstract void parkNanos(long nanos);
    abstract void unpark();
    abstract void tryYield();
}
```

`VirtualThread` 是 `final class`——不可被继承，所有虚拟线程都是同一个实现。

### 静态常量 (Static Constants)

```java
final class VirtualThread extends BaseVirtualThread {
    private static final Unsafe U = Unsafe.getUnsafe();
    private static final ContinuationScope VTHREAD_SCOPE = new ContinuationScope("VirtualThreads");
    private static final ForkJoinPool DEFAULT_SCHEDULER = createDefaultScheduler();
```

- **`VTHREAD_SCOPE`**：所有虚拟线程共享同一个 `ContinuationScope`，名为 `"VirtualThreads"`。
  `Continuation.yield(VTHREAD_SCOPE)` 时以此 scope 为边界暂停执行。
- **`DEFAULT_SCHEDULER`**：全局唯一的 `ForkJoinPool`，在类加载时通过 `createDefaultScheduler()` 创建。

### 字段偏移量 (Field Offsets for CAS)

```java
private static final long STATE = U.objectFieldOffset(VirtualThread.class, "state");
private static final long PARK_PERMIT = U.objectFieldOffset(VirtualThread.class, "parkPermit");
private static final long CARRIER_THREAD = U.objectFieldOffset(VirtualThread.class, "carrierThread");
private static final long ON_WAITING_LIST = U.objectFieldOffset(VirtualThread.class, "onWaitingList");
```

这些偏移量用于 `Unsafe.compareAndSet*` 操作，实现无锁的状态转换。

### 实例字段 (Instance Fields)

| 字段 | 类型 | 说明 |
|------|------|------|
| `scheduler` | `Executor` | 调度器（scheduler），通常是 `DEFAULT_SCHEDULER` |
| `cont` | `Continuation` | 封装了线程执行体的 continuation 对象 |
| `runContinuation` | `Runnable` | `this::runContinuation` 方法引用，提交给调度器的任务 |
| `state` | `volatile int` | 虚拟线程状态，VM 直接访问 |
| `parkPermit` | `volatile boolean` | parking 许可（permit），类似 `LockSupport` 的 permit |
| `blockPermit` | `volatile boolean` | monitor blocking 许可，由 unblocker 线程设置 |
| `carrierThread` | `volatile Thread` | 当前绑定的载体线程（carrier thread），VM 直接访问 |
| `onWaitingList` | `volatile boolean` | 是否在等待 unblock 的链表上 |
| `next` | `volatile VirtualThread` | 等待 unblock 链表的下一个节点 |
| `notified` | `volatile boolean` | 是否被 `Object.notify/notifyAll` 唤醒 |
| `interruptibleWait` | `volatile boolean` | 是否在可中断的 `Object.wait` 中 |
| `timedWaitSeqNo` | `byte` | timed-wait 序列号，防止过期 timeout 误唤醒 |
| `timeout` | `long` | timed-park/timed-wait 的超时时间 |
| `timeoutTask` | `Future<?>` | 定时任务引用，用于取消 |
| `notifyAllAfterTerminate` | `volatile boolean` | 终止后是否 notifyAll（支持 `Thread.join`） |

### 构造函数 (Constructor)

```java
VirtualThread(Executor scheduler, String name, int characteristics, Runnable task) {
    super(name, characteristics, /*bound*/ false);
    Objects.requireNonNull(task);

    // 如果未指定 scheduler，继承父虚拟线程的 scheduler 或使用默认
    if (scheduler == null) {
        Thread parent = Thread.currentThread();
        if (parent instanceof VirtualThread vparent) {
            scheduler = vparent.scheduler;
        } else {
            scheduler = DEFAULT_SCHEDULER;
        }
    }

    this.scheduler = scheduler;
    this.cont = new VThreadContinuation(this, task);
    this.runContinuation = this::runContinuation;
}
```

关键点：
- `bound = false`——虚拟线程不绑定 OS 线程（与 `BoundVirtualThread` 相反）。
- `VThreadContinuation` 是内部类，包装了用户任务。
- 虚拟线程可以继承父虚拟线程的自定义 scheduler。

---

## 2. 20 个状态常量详解

源码定义了 20 个状态常量，通过 `volatile int state` 字段表示：

### 基础生命周期状态

| 常量 | 值 | 含义 | mounted? |
|------|-----|------|----------|
| `NEW` | 0 | 新建，尚未启动 | N/A |
| `STARTED` | 1 | 已调用 `start()`，已提交到调度器，等待首次运行 | No |
| `RUNNING` | 2 | 正在载体线程上运行 | **Yes** |
| `TERMINATED` | 99 | 已终止，最终状态 | No |

### Park 相关状态（LockSupport.park）

| 常量 | 值 | 含义 | mounted? |
|------|-----|------|----------|
| `PARKING` | 3 | 正在执行 park 过渡，准备 yield | **Yes** (过渡中) |
| `PARKED` | 4 | 已暂停，无限期等待 unpark | No |
| `PINNED` | 5 | 被 pin 住无法 yield，在载体线程上 park | **Yes** |
| `TIMED_PARKING` | 6 | 正在执行定时 park 过渡 | **Yes** (过渡中) |
| `TIMED_PARKED` | 7 | 已暂停，定时等待 | No |
| `TIMED_PINNED` | 8 | 被 pin 住，在载体线程上定时 park | **Yes** |
| `UNPARKED` | 9 | 已被 unpark，等待调度器重新调度 | No |

### Thread.yield 相关状态

| 常量 | 值 | 含义 | mounted? |
|------|-----|------|----------|
| `YIELDING` | 10 | 正在执行 yield 过渡 | **Yes** (过渡中) |
| `YIELDED` | 11 | 已 yield，等待重新调度 | No |

### Monitor Enter 相关状态（JEP 491）

| 常量 | 值 | 含义 | mounted? |
|------|-----|------|----------|
| `BLOCKING` | 12 | 正在执行 monitor enter 阻塞过渡 | **Yes** (过渡中) |
| `BLOCKED` | 13 | 在 monitor enter 上阻塞 | No |
| `UNBLOCKED` | 14 | 已解除 monitor 阻塞，等待重新调度 | No |

### Object.wait 相关状态

| 常量 | 值 | 含义 | mounted? |
|------|-----|------|----------|
| `WAITING` | 15 | 正在进入 Object.wait 的过渡状态 | **Yes** (过渡中) |
| `WAIT` | 16 | 在 Object.wait 中等待 | No |
| `TIMED_WAITING` | 17 | 正在进入定时 Object.wait 的过渡状态 | **Yes** (过渡中) |
| `TIMED_WAIT` | 18 | 在定时 Object.wait 中等待 | No |

### 状态值设计规律

- **偶数/奇数无规律**——按功能分组排列。
- **过渡状态**（transitional）：`PARKING`、`TIMED_PARKING`、`YIELDING`、`BLOCKING`、`WAITING`、`TIMED_WAITING`
  表示虚拟线程正在 mount 状态下执行 `yieldContinuation()`，是瞬态。
- **稳定未挂载状态**（stable unmounted）：`PARKED`、`TIMED_PARKED`、`YIELDED`、`BLOCKED`、`WAIT`、`TIMED_WAIT`
  表示 continuation 已 yield，虚拟线程脱离载体线程。
- **可运行未挂载状态**（runnable unmounted）：`UNPARKED`、`UNBLOCKED`、`YIELDED`
  表示虚拟线程可以被调度运行，但尚未 mount。
- **TERMINATED = 99** 远离其他值，作为明确的终止标记。

---

## 3. 状态转换图

源码中的完整状态转换注释（VirtualThread.java 第 80-123 行）：

```
      NEW -> STARTED         // Thread.start, 提交到调度器
  STARTED -> TERMINATED      // 启动失败
  STARTED -> RUNNING         // 首次运行

  RUNNING -> TERMINATED      // 任务完成

  RUNNING -> PARKING         // LockSupport.park
  PARKING -> PARKED          // cont.yield 成功，无限期暂停
   PARKED -> UNPARKED        // 被 unpark，可能提交重新调度
 UNPARKED -> RUNNING         // 在载体线程上恢复执行

  PARKING -> RUNNING         // cont.yield 失败（pinned）
  RUNNING -> PINNED          // 在载体线程上 park（被 pin 住）
   PINNED -> RUNNING         // unpark，在同一载体线程上恢复

  RUNNING -> TIMED_PARKING   // LockSupport.parkNanos
  TIMED_PARKING -> TIMED_PARKED  // cont.yield 成功，定时暂停
  TIMED_PARKED -> UNPARKED       // unpark 或超时

  TIMED_PARKING -> RUNNING       // cont.yield 失败（pinned）
  RUNNING -> TIMED_PINNED        // 在载体线程上定时 park
  TIMED_PINNED -> RUNNING        // unpark

  RUNNING -> BLOCKING        // 尝试进入 synchronized（monitor enter）
  BLOCKING -> BLOCKED        // cont.yield 成功，在 monitor 上阻塞
  BLOCKED -> UNBLOCKED       // monitor 所有者退出，unblock
  UNBLOCKED -> RUNNING       // 恢复执行

  RUNNING -> WAITING         // Object.wait 过渡
  WAITING -> WAIT            // 在 Object.wait 中等待
  WAIT -> BLOCKED            // 被 notify，等待重新获取 monitor
  WAIT -> UNBLOCKED          // 被 interrupt

  RUNNING -> TIMED_WAITING   // 定时 Object.wait 过渡
  TIMED_WAITING -> TIMED_WAIT    // 定时等待中
  TIMED_WAIT -> BLOCKED          // 被 notify
  TIMED_WAIT -> UNBLOCKED        // 超时或 interrupt

  RUNNING -> YIELDING        // Thread.yield
  YIELDING -> YIELDED        // cont.yield 成功
  YIELDING -> RUNNING        // cont.yield 失败
  YIELDED -> RUNNING         // 重新调度后恢复
```

### 映射到 Thread.State

`threadState()` 方法将内部状态映射到公共 API 的 `Thread.State` 枚举：

| Thread.State | 对应内部状态 |
|-------------|------------|
| `NEW` | `NEW`；`STARTED`（容器未设置时） |
| `RUNNABLE` | `STARTED`（容器已设置）、`RUNNING`、`UNPARKED`、`UNBLOCKED`、`YIELDED`、`PARKING`、`TIMED_PARKING`、`WAITING`、`TIMED_WAITING`、`YIELDING` |
| `WAITING` | `PARKED`、`PINNED`、`WAIT` |
| `TIMED_WAITING` | `TIMED_PARKED`、`TIMED_PINNED`、`TIMED_WAIT` |
| `BLOCKED` | `BLOCKING`、`BLOCKED` |
| `TERMINATED` | `TERMINATED` |

注意：过渡状态（`PARKING` 等）对外报告为 `RUNNABLE`，因为线程仍在执行中。

---

## 4. 生命周期：从 start 到 terminate

### 4.1 start() — 启动虚拟线程

```java
@Override
void start(ThreadContainer container) {
    if (!compareAndSetState(NEW, STARTED)) {
        throw new IllegalThreadStateException("Already started");
    }

    // 绑定到线程容器
    setThreadContainer(container);

    boolean addedToContainer = false;
    boolean started = false;
    try {
        container.add(this);    // 加入容器（可能抛异常）
        addedToContainer = true;

        inheritScopedValueBindings(container);  // 继承 ScopedValue

        // 提交任务到调度器
        externalSubmitRunContinuationOrThrow();
        started = true;
    } finally {
        if (!started) {
            afterDone(addedToContainer);  // 启动失败 → TERMINATED
        }
    }
}
```

流程：
1. CAS `NEW → STARTED`——保证只能启动一次。
2. 注册到 `ThreadContainer`。
3. 继承 `ScopedValue` 绑定。
4. 通过 `externalSubmitRunContinuationOrThrow()` 将 `runContinuation` 任务提交到调度器。
5. 失败时直接进入 `TERMINATED`。

### 4.2 runContinuation() — 在载体线程上执行

```java
@ChangesCurrentThread
private void runContinuation() {
    // 载体必须是平台线程
    if (Thread.currentThread().isVirtual()) {
        throw new WrongThreadException();
    }

    // CAS 设置状态为 RUNNING
    int initialState = state();
    if (initialState == STARTED || initialState == UNPARKED
            || initialState == UNBLOCKED || initialState == YIELDED) {
        if (!compareAndSetState(initialState, RUNNING)) {
            return;
        }
        // 消费 permit 并取消 timeout
        if (initialState == UNPARKED) {
            cancelTimeoutTask();
            setParkPermit(false);
        } else if (initialState == UNBLOCKED) {
            cancelTimeoutTask();
            blockPermit = false;
        }
    } else {
        return;  // 不可运行
    }

    mount();
    try {
        cont.run();  // 运行或恢复 continuation
    } finally {
        unmount();
        if (cont.isDone()) {
            afterDone();      // 任务完成 → TERMINATED
        } else {
            afterYield();     // continuation 暂停 → 处理后续状态
        }
    }
}
```

关键点：
- 只有从 `STARTED`/`UNPARKED`/`UNBLOCKED`/`YIELDED` 才能 CAS 到 `RUNNING`。
- `mount()` → `cont.run()` → `unmount()` 是核心的 mount-run-unmount 循环。
- `cont.run()` 返回时，要么 continuation 完成（`isDone()`），要么 yield 了。

### 4.3 VThreadContinuation — 任务包装

```java
private static class VThreadContinuation extends Continuation {
    VThreadContinuation(VirtualThread vthread, Runnable task) {
        super(VTHREAD_SCOPE, wrap(vthread, task));
    }
    @Override
    protected void onPinned(Continuation.Pinned reason) {
        // 不抛异常！虚拟线程允许 pinned yield 失败
    }
    private static Runnable wrap(VirtualThread vthread, Runnable task) {
        return new Runnable() {
            @Hidden
            @JvmtiHideEvents
            public void run() {
                vthread.endFirstTransition();
                try {
                    vthread.run(task);      // 执行用户任务
                } finally {
                    vthread.startFinalTransition();
                }
            }
        };
    }
}
```

注意 `onPinned` 覆盖为空方法——基类 `Continuation.onPinned()` 会抛出 `IllegalStateException`，
但虚拟线程需要优雅地处理 pinning（退回到在载体线程上 park）。

### 4.4 run(task) — 用户任务执行

```java
private void run(Runnable task) {
    assert Thread.currentThread() == this && state == RUNNING;

    // JFR VirtualThreadStart 事件
    if (VirtualThreadStartEvent.isTurnedOn()) {
        var event = new VirtualThreadStartEvent();
        event.javaThreadId = threadId();
        event.commit();
    }

    Object bindings = Thread.scopedValueBindings();
    try {
        runWith(bindings, task);   // 带 ScopedValue 绑定运行
    } catch (Throwable exc) {
        dispatchUncaughtException(exc);
    } finally {
        StackableScope.popAll();   // 弹出剩余 scope（可能阻塞）
        // JFR VirtualThreadEnd 事件
    }
}
```

### 4.5 afterDone() — 终止处理

```java
private void afterDone(boolean notifyContainer) {
    assert carrierThread == null;
    setState(TERMINATED);

    // 唤醒所有等待此线程终止的线程（Thread.join）
    if (notifyAllAfterTerminate) {
        synchronized (this) {
            notifyAll();
        }
    }

    // 从容器移除
    if (notifyContainer) {
        threadContainer().remove(this);
    }

    // 清除 ThreadLocal 引用
    clearReferences();
}
```

---

## 5. mount/unmount 机制

mount/unmount 是虚拟线程的核心操作——将虚拟线程绑定到/解绑于载体线程。

### 5.1 mount() — 挂载到载体线程

```java
@ChangesCurrentThread
@ReservedStackAccess
private void mount() {
    startTransition(/*mount*/true);   // 通知 VM 开始 mount 过渡

    // 设置载体线程
    Thread carrier = Thread.currentCarrierThread();
    setCarrierThread(carrier);

    // 同步中断状态
    if (interrupted) {
        carrier.setInterrupt();
    } else if (carrier.isInterrupted()) {
        synchronized (interruptLock) {
            if (!interrupted) {
                carrier.clearInterrupt();
            }
        }
    }

    // 关键：设置 Thread.currentThread() 返回虚拟线程
    carrier.setCurrentThread(this);
}
```

`@ChangesCurrentThread` 注解告诉编译器此方法会改变 `Thread.currentThread()` 的返回值，
防止编译器错误地缓存线程标识。

`@ReservedStackAccess` 保证 mount/unmount 操作即使在栈空间不足时也能完成。

mount 的关键效果：
1. **`carrierThread` 字段**指向载体线程。
2. **`carrier.setCurrentThread(this)`** 使载体线程上的 `Thread.currentThread()` 返回虚拟线程。
3. **中断状态同步**——虚拟线程的中断标志传播到载体线程（因为 I/O 操作检查载体线程的中断）。

### 5.2 unmount() — 从载体线程卸载

```java
@ChangesCurrentThread
@ReservedStackAccess
private void unmount() {
    assert !Thread.holdsLock(interruptLock);

    // 恢复 Thread.currentThread() 返回载体线程
    Thread carrier = this.carrierThread;
    carrier.setCurrentThread(carrier);

    // 断开与载体线程的连接，与 interrupt 同步
    synchronized (interruptLock) {
        setCarrierThread(null);
    }
    carrier.clearInterrupt();

    endTransition(/*mount*/false);   // 通知 VM mount 过渡结束
}
```

unmount 操作：
1. 恢复 `Thread.currentThread()` 为载体线程自身。
2. 在 `interruptLock` 同步块中将 `carrierThread` 置 `null`——与 `interrupt()` 方法协调。
3. 清除载体线程的中断标志。

### 5.3 yieldContinuation() — 暂停执行

```java
@Hidden
private boolean yieldContinuation() {
    startTransition(/*mount*/false);
    try {
        return Continuation.yield(VTHREAD_SCOPE);
    } finally {
        endTransition(/*mount*/true);
    }
}
```

`Continuation.yield(VTHREAD_SCOPE)` 是 JVM 内部操作：
- 将当前线程的栈帧保存到 `StackChunk` 堆对象中。
- 控制流返回到 `Continuation.run()` 的调用者（即 `runContinuation()` 中 `cont.run()` 之后）。
- 返回 `true` 表示 yield 成功，`false` 表示被 pin 住无法 yield。

### 5.4 Transition 通知方法

```java
@IntrinsicCandidate @JvmtiMountTransition
private native void startTransition(boolean mount);

@IntrinsicCandidate @JvmtiMountTransition
private native void endTransition(boolean mount);

@IntrinsicCandidate @JvmtiMountTransition
private native void endFirstTransition();

@IntrinsicCandidate @JvmtiMountTransition
private native void startFinalTransition();
```

这些 native 方法通知 VM（主要是 JVMTI）正在进行线程身份切换。
`@IntrinsicCandidate` 表示 JIT 编译器可以将它们替换为内联的高效实现。

---

## 6. Continuation 运行原理

`jdk.internal.vm.Continuation` 是 one-shot delimited continuation 的实现，
是虚拟线程能暂停/恢复执行的底层机制。

### 6.1 核心字段

```java
public class Continuation {
    private final Runnable target;           // continuation 的执行体
    private final ContinuationScope scope;   // 作用域
    private Continuation parent;             // 父 continuation（native stack）
    private Continuation child;              // yield 到子 continuation 时设置

    private StackChunk tail;      // 保存的栈帧链表（heap-stored stack frames）
    private boolean done;         // 是否已完成
    private volatile boolean mounted;  // 是否已 mount
    private Object yieldInfo;     // yield 传递信息
    private boolean preempted;    // 是否被强制抢占

    private Object[] scopedValueCache;  // ScopedValue 缓存
}
```

### 6.2 Continuation.run() — 运行/恢复

```java
public final void run() {
    while (true) {
        mount();                    // CAS mounted = true
        JLA.setScopedValueCache(scopedValueCache);

        if (done)
            throw new IllegalStateException("Continuation terminated");

        Thread t = currentCarrierThread();
        if (parent != null) {
            if (parent != JLA.getContinuation(t))
                throw new IllegalStateException();
        } else
            this.parent = JLA.getContinuation(t);
        JLA.setContinuation(t, this);  // 将 continuation 设为当前线程的 continuation

        try {
            boolean isVirtualThread = (scope == JLA.virtualThreadContinuationScope());
            if (!isStarted()) {
                // 首次运行：进入 entry frame
                enterSpecial(this, false, isVirtualThread);
            } else {
                // 恢复：从上次 yield 点继续
                enterSpecial(this, true, isVirtualThread);
            }
        } finally {
            // yield 返回后的清理
            JLA.setContinuation(currentCarrierThread(), this.parent);
            if (parent != null) parent.child = null;
            postYieldCleanup();
            unmount();
            // 保存/清除 ScopedValue 缓存
        }

        // 检查是否 yield 到了正确的 scope
        if (yieldInfo == null || yieldInfo == scope) {
            this.parent = null;
            this.yieldInfo = null;
            return;  // 正常返回
        } else {
            // 嵌套 scope 的 yield 传播
            parent.child = this;
            parent.yield0((ContinuationScope)yieldInfo, this);
            parent.child = null;
        }
    }
}
```

### 6.3 enterSpecial / enter / enter0 — 入口帧

```java
@IntrinsicCandidate
private static native void enterSpecial(Continuation c, boolean isContinue, boolean isVirtualThread);

@Hidden @DontInline @IntrinsicCandidate @JvmtiHideEvents
private static void enter(Continuation c, boolean isContinue) {
    try {
        c.enter0();
    } finally {
        c.finish();
    }
}

@Hidden @JvmtiHideEvents
private void enter0() {
    target.run();    // 执行 continuation 的 body
}
```

- `enterSpecial` 是 native/intrinsic 方法，建立一个特殊的"entry frame"。
- yield 时会跳转到 `enterSpecial` 的调用者，就像 `enterSpecial` 正常返回一样。
- `enter0()` 中 `target.run()` 就是执行虚拟线程包装后的用户任务。

### 6.4 Continuation.yield() — 静态暂停方法

```java
@Hidden @JvmtiHideEvents
public static boolean yield(ContinuationScope scope) {
    Continuation cont = JLA.getContinuation(currentCarrierThread());
    Continuation c;
    for (c = cont; c != null && c.scope != scope; c = c.parent)
        ;
    if (c == null)
        throw new IllegalStateException("Not in scope " + scope);
    return cont.yield0(scope, null);
}
```

沿 continuation 链向上查找匹配的 scope，然后调用 `yield0`。

### 6.5 yield0 / doYield — 底层 yield

```java
private boolean yield0(ContinuationScope scope, Continuation child) {
    if (scope != this.scope)
        this.yieldInfo = scope;
    int res = doYield();            // native 方法，执行栈拷贝
    U.storeFence();

    if (child != null) {
        // 嵌套 yield 处理...
    } else {
        if (res == 0 && yieldInfo != null) {
            res = (Integer)yieldInfo;
        }
        this.yieldInfo = null;
        if (res == 0)
            onContinue();       // yield 成功后恢复时调用
        else
            onPinned0(res);     // yield 失败（pinned）
    }
    return res == 0;  // 0 = 成功
}
```

`doYield()` 是 `@IntrinsicCandidate` 的 native 方法。JVM 实现中，它将当前线程的栈帧
拷贝到堆上的 `StackChunk` 对象中，然后跳转回 entry frame。

### 6.6 Pinned 枚举 — yield 失败原因

```java
public enum Pinned {
    NATIVE,            // 栈上有 native 帧
    CRITICAL_SECTION,  // 在 Continuation.pin() 的临界区中
    EXCEPTION          // 异常（OOME/SOE）
}
```

当 `doYield()` 返回非零值时，表示 continuation 被 pin 住：
- `2` → `CRITICAL_SECTION`
- `3` → `NATIVE`
- `4` → `EXCEPTION`

---

## 7. ForkJoinPool 调度器

### 7.1 createDefaultScheduler() — 创建默认调度器

```java
private static ForkJoinPool createDefaultScheduler() {
    ForkJoinWorkerThreadFactory factory = pool -> new CarrierThread(pool);
    int parallelism, maxPoolSize, minRunnable;

    // 系统属性配置
    String parallelismValue = System.getProperty("jdk.virtualThreadScheduler.parallelism");
    String maxPoolSizeValue = System.getProperty("jdk.virtualThreadScheduler.maxPoolSize");
    String minRunnableValue = System.getProperty("jdk.virtualThreadScheduler.minRunnable");

    if (parallelismValue != null) {
        parallelism = Integer.parseInt(parallelismValue);
    } else {
        parallelism = Runtime.getRuntime().availableProcessors();
    }
    if (maxPoolSizeValue != null) {
        maxPoolSize = Integer.parseInt(maxPoolSizeValue);
        parallelism = Integer.min(parallelism, maxPoolSize);
    } else {
        maxPoolSize = Integer.max(parallelism, 256);
    }
    if (minRunnableValue != null) {
        minRunnable = Integer.parseInt(minRunnableValue);
    } else {
        minRunnable = Integer.max(parallelism / 2, 1);
    }

    Thread.UncaughtExceptionHandler handler = (t, e) -> { };
    boolean asyncMode = true; // FIFO
    return new ForkJoinPool(parallelism, factory, handler, asyncMode,
                 0, maxPoolSize, minRunnable, pool -> true, 30, SECONDS);
}
```

### 配置参数

| 系统属性 | 默认值 | 说明 |
|---------|--------|------|
| `jdk.virtualThreadScheduler.parallelism` | `availableProcessors()` | 并行度（parallelism），即核心载体线程数 |
| `jdk.virtualThreadScheduler.maxPoolSize` | `max(parallelism, 256)` | 最大线程数（含补偿线程） |
| `jdk.virtualThreadScheduler.minRunnable` | `max(parallelism/2, 1)` | 最少可运行线程数（触发补偿的阈值） |

### 关键设计选择

- **`asyncMode = true`**：使用 FIFO 模式而非 LIFO。通常 ForkJoinPool 默认 LIFO（优化递归分治），
  但虚拟线程调度需要公平性，所以使用 FIFO。
- **`pool -> true`** (saturate predicate)：始终返回 `true`，表示不拒绝任务。
- **`30, SECONDS`**：空闲载体线程 30 秒后回收。
- **`CarrierThread` 作为 worker**：每个 ForkJoinWorkerThread 都是 `CarrierThread` 实例。

### 7.2 任务提交策略

VirtualThread 有多种提交方法，针对不同场景优化：

```java
// 通用提交：ForkJoinPool 用 ForkJoinTask.adapt，其他用 execute
private void submit(Executor executor, Runnable task) {
    if (executor instanceof ForkJoinPool pool) {
        pool.submit(ForkJoinTask.adapt(task));
    } else {
        executor.execute(task);
    }
}

// 惰性提交：载体线程本地队列为空时，惰性推入
private void lazySubmitRunContinuation() {
    if (currentThread() instanceof CarrierThread ct && ct.getQueuedTaskCount() == 0) {
        ForkJoinPool pool = ct.getPool();
        pool.lazySubmit(ForkJoinTask.adapt(runContinuation));
    } else {
        submitRunContinuation();
    }
}

// 外部提交：强制使用外部提交队列（避免 work-stealing 干扰）
private void externalSubmitRunContinuation(ForkJoinPool pool) {
    assert Thread.currentThread() instanceof CarrierThread;
    pool.externalSubmit(ForkJoinTask.adapt(runContinuation));
}
```

**`lazySubmit` vs `submit` vs `externalSubmit`**：
- `lazySubmit`：当载体线程本地队列为空时使用，减少 work-stealing 的开销。用于 unpark 和 unblock 场景。
- `submit`：通用提交，推入本地队列（如果在 worker 线程上）或外部队列。
- `externalSubmit`：强制推入外部提交队列。用于 `Thread.yield` 后的重新调度，
  确保任务不会立即被同一载体线程执行（实现真正的让出 CPU）。

### 7.3 CarrierThread 补偿机制 (Compensation)

当虚拟线程在载体线程上被 pin 住（无法 yield）时，`CarrierThread` 提供补偿机制：

```java
// CarrierThread.java
private int compensating;  // NOT_COMPENSATING / COMPENSATE_IN_PROGRESS / COMPENSATING
private long compensateValue;

public boolean beginBlocking() {
    if (compensating == NOT_COMPENSATING) {
        Continuation.pin();
        try {
            compensating = COMPENSATE_IN_PROGRESS;
            compensateValue = ForkJoinPools.beginCompensatedBlock(getPool());
            compensating = COMPENSATING;
            return true;
        } catch (Throwable e) {
            compensating = NOT_COMPENSATING;
            throw e;
        } finally {
            Continuation.unpin();
        }
    }
    return false;
}

public void endBlocking() {
    if (compensating == COMPENSATING) {
        ForkJoinPools.endCompensatedBlock(getPool(), compensateValue);
        compensating = NOT_COMPENSATING;
    }
}
```

补偿原理：
1. `ForkJoinPool.tryCompensate()` 启动或唤醒一个备用线程来替代被阻塞的载体线程。
2. 保持 pool 的有效并行度不变。
3. `endBlocking()` 在 `afterYield()` 中调用（continuation yield 后恢复时）。

`afterYield()` 中的补偿回收：
```java
private void afterYield() {
    assert carrierThread == null;
    // 如果 yield 时正在补偿，取消补偿
    if (currentThread() instanceof CarrierThread ct) {
        ct.endBlocking();
    }
    // ... 状态处理
}
```

---

## 8. park/unpark 实现

### 8.1 park() — 暂停虚拟线程

```java
@Override
void park() {
    assert Thread.currentThread() == this;

    // 快速路径：permit 已可用或已中断 → 立即返回
    if (getAndSetParkPermit(false) || interrupted)
        return;

    // 设置状态为 PARKING，尝试 yield
    boolean yielded = false;
    setState(PARKING);
    try {
        yielded = yieldContinuation();
    } catch (OutOfMemoryError e) {
        // OOME → 退回到载体线程 park
    } finally {
        if (!yielded) {
            assert state() == PARKING;
            setState(RUNNING);
        }
    }

    // yield 失败（pinned）→ 在载体线程上 park
    if (!yielded) {
        parkOnCarrierThread(false, 0);
    }
}
```

park 流程：
1. **快速检查**：如果 `parkPermit` 已设置或已中断，不阻塞直接返回。
2. **设置 PARKING 状态**。
3. **尝试 yield continuation**——成功则虚拟线程脱离载体线程，控制返回到 `runContinuation()`。
4. **yield 失败**（pinned）——退回到 `parkOnCarrierThread()`，在载体线程上使用 `Unsafe.park()` 阻塞。

### 8.2 parkOnCarrierThread() — Pinned 场景的退路

```java
private void parkOnCarrierThread(boolean timed, long nanos) {
    assert state() == RUNNING;

    setState(timed ? TIMED_PINNED : PINNED);
    try {
        if (!parkPermit) {
            if (!timed) {
                U.park(false, 0);
            } else if (nanos > 0) {
                U.park(false, nanos);
            }
        }
    } finally {
        setState(RUNNING);
    }

    setParkPermit(false);
    postPinnedEvent("LockSupport.park");  // 记录 JFR 事件
}
```

在 `PINNED`/`TIMED_PINNED` 状态下，虚拟线程占用载体线程，直到被 unpark。
此时会产生 `jdk.VirtualThreadPinned` JFR 事件。

### 8.3 unpark() — 唤醒虚拟线程

```java
private void unpark(boolean lazySubmit) {
    if (!getAndSetParkPermit(true) && currentThread() != this) {
        int s = state();

        // 正常 unpark：PARKED/TIMED_PARKED → UNPARKED，提交到调度器
        if ((s == PARKED || s == TIMED_PARKED) && compareAndSetState(s, UNPARKED)) {
            if (lazySubmit) {
                lazySubmitRunContinuation();
            } else {
                submitRunContinuation();
            }
            return;
        }

        // Pinned unpark：PINNED/TIMED_PINNED → unpark 载体线程
        if (s == PINNED || s == TIMED_PINNED) {
            disableSuspendAndPreempt();
            try {
                synchronized (carrierThreadAccessLock()) {
                    Thread carrier = carrierThread;
                    if (carrier != null && ((s = state()) == PINNED || s == TIMED_PINNED)) {
                        U.unpark(carrier);  // 直接 unpark 载体线程
                    }
                }
            } finally {
                enableSuspendAndPreempt();
            }
            return;
        }
    }
}
```

两条路径：
1. **正常路径**：CAS `PARKED → UNPARKED`，重新提交 `runContinuation` 到调度器。
2. **Pinned 路径**：`PINNED`/`TIMED_PINNED` 时，通过 `Unsafe.unpark(carrier)` 直接唤醒载体线程。

### 8.4 与 LockSupport 的关系

`LockSupport.park()/unpark()` 的虚拟线程分发：

```java
// LockSupport.java (简化)
public static void park() {
    if (Thread.currentThread() instanceof BaseVirtualThread vt) {
        vt.park();       // 调用 VirtualThread.park()
    } else {
        U.park(false, 0);
    }
}

public static void unpark(Thread thread) {
    if (thread instanceof BaseVirtualThread vt) {
        vt.unpark();     // 调用 VirtualThread.unpark()
    } else if (thread != null) {
        U.unpark(thread);
    }
}
```

`java.util.concurrent` 中所有基于 `LockSupport` 的同步器（`ReentrantLock`、`Semaphore`、
`CountDownLatch` 等）自动支持虚拟线程——当虚拟线程 park 时，它会 yield continuation
释放载体线程，而不是阻塞载体线程。

### 8.5 afterYield() — yield 后的状态处理

```java
private void afterYield() {
    assert carrierThread == null;

    // 补偿回收
    if (currentThread() instanceof CarrierThread ct) {
        ct.endBlocking();
    }

    int s = state();

    // LockSupport.park/parkNanos
    if (s == PARKING || s == TIMED_PARKING) {
        int newState;
        if (s == PARKING) {
            setState(newState = PARKED);
        } else {
            // 定时 park → 安排 timeout 任务
            timeoutTask = schedule(this::parkTimeoutExpired, timeout, NANOSECONDS);
            setState(newState = TIMED_PARKED);
        }
        // 可能在 parking 过程中已被 unpark
        if (parkPermit && compareAndSetState(newState, UNPARKED)) {
            lazySubmitRunContinuation();
        }
        return;
    }

    // Thread.yield
    if (s == YIELDING) {
        setState(YIELDED);
        // 外部提交以避免立即被同一载体执行
        if (currentThread() instanceof CarrierThread ct && ct.getQueuedTaskCount() == 0) {
            externalSubmitRunContinuation(ct.getPool());
        } else {
            submitRunContinuation();
        }
        return;
    }

    // monitor enter blocking
    if (s == BLOCKING) {
        setState(BLOCKED);
        if (blockPermit && compareAndSetState(BLOCKED, UNBLOCKED)) {
            lazySubmitRunContinuation();
        }
        return;
    }

    // Object.wait
    if (s == WAITING || s == TIMED_WAITING) {
        // ... 详见第 10 节
    }
}
```

`afterYield()` 在 `unmount()` 之后、在载体线程的上下文中运行。
它根据 yield 前设置的状态决定后续操作。

---

## 9. JEP 491 monitor 支持

JEP 491（Synchronize Virtual Threads without Pinning）是 JDK 24 的关键改进。
在此之前，虚拟线程进入 `synchronized` 块时会 pin 住载体线程。
JEP 491 使虚拟线程能在 monitor contention 时 yield，释放载体线程。

### 9.1 BLOCKING/BLOCKED/UNBLOCKED 状态

当虚拟线程尝试进入一个已被其他线程持有的 monitor 时：

```
RUNNING → BLOCKING      // VM 检测到 monitor contention，触发 yield
BLOCKING → BLOCKED       // continuation yield 成功，虚拟线程脱离载体
BLOCKED → UNBLOCKED      // monitor 所有者退出，unblocker 线程唤醒
UNBLOCKED → RUNNING      // 重新调度，重新尝试 enter monitor
```

### 9.2 Unblocker 线程

```java
private static void unblockVirtualThreads() {
    while (true) {
        VirtualThread vthread = takeVirtualThreadListToUnblock();  // native，阻塞等待
        while (vthread != null) {
            VirtualThread nextThread = vthread.next;

            // 从链表移除并 unblock
            vthread.next = null;
            vthread.compareAndSetOnWaitingList(true, false);
            vthread.unblock();

            vthread = nextThread;
        }
    }
}

static {
    var unblocker = InnocuousThread.newThread("VirtualThread-unblocker",
            VirtualThread::unblockVirtualThreads);
    unblocker.setDaemon(true);
    unblocker.start();
}
```

关键设计：
- **`VirtualThread-unblocker`** 是一个专用守护线程，在 `VirtualThread` 类初始化时启动。
- **`takeVirtualThreadListToUnblock()`** 是 native 方法，阻塞等待 VM 提供需要 unblock 的虚拟线程链表。
- VM 在 monitor 所有者退出 `synchronized` 块时，将等待的虚拟线程放入链表。
- 通过 `next` 字段形成单向链表，`onWaitingList` 标记是否在链表上。

### 9.3 unblock() 方法

```java
private void unblock() {
    assert !Thread.currentThread().isVirtual();
    blockPermit = true;
    if (state() == BLOCKED && compareAndSetState(BLOCKED, UNBLOCKED)) {
        submitRunContinuation();
    }
}
```

设置 `blockPermit = true`，CAS `BLOCKED → UNBLOCKED`，然后提交到调度器重新运行。

### 9.4 afterYield 中的 BLOCKING 处理

```java
if (s == BLOCKING) {
    setState(BLOCKED);

    // 可能在 blocking 过程中已被 unblock
    if (blockPermit && compareAndSetState(BLOCKED, UNBLOCKED)) {
        lazySubmitRunContinuation();
    }
    return;
}
```

与 park/unpark 类似的竞态处理：在状态转换过程中 unblock 可能已经发生。

### 9.5 与 Pinning 的关系

JEP 491 之前，`synchronized` 块会 pin 住 continuation，因为 monitor 的 ownership
记录在 OS 线程上。JEP 491 修改了 VM 的 monitor 实现，允许虚拟线程在 monitor contention
时 yield continuation。具体来说：

- VM 在 `monitorenter` 字节码执行时检测到 contention。
- 如果当前线程是虚拟线程，VM 设置虚拟线程状态为 `BLOCKING`。
- VM 冻结虚拟线程的 `LockStack`（lock stack 是 JDK 中轻量级锁的栈数据结构）。
- 调用 `yieldContinuation()` 释放载体线程。
- 当 monitor 可用时，VM 将虚拟线程加入 unblocker 链表。

---

## 10. Object.wait/notify 支持

### 10.1 状态转换

```
RUNNING → WAITING → WAIT                    // Object.wait()
RUNNING → TIMED_WAITING → TIMED_WAIT        // Object.wait(timeout)

WAIT → BLOCKED          // notify/notifyAll
WAIT → UNBLOCKED        // interrupt

TIMED_WAIT → BLOCKED    // notify/notifyAll
TIMED_WAIT → UNBLOCKED  // timeout 或 interrupt
```

注意：从 `WAIT`/`TIMED_WAIT` 被 notify 后，不是直接到 `UNBLOCKED`，而是到 `BLOCKED`——
因为从 `Object.wait` 返回需要重新获取 monitor（`re-enter monitor`）。

### 10.2 afterYield 中的 WAITING/TIMED_WAITING 处理

```java
if (s == WAITING || s == TIMED_WAITING) {
    int newState;
    boolean blocked;
    boolean interruptible = interruptibleWait;
    if (s == WAITING) {
        setState(newState = WAIT);
        // 可能在过渡中已被 notify
        blocked = notified && compareAndSetState(WAIT, BLOCKED);
    } else {
        long timeout = this.timeout;
        synchronized (timedWaitLock()) {
            byte seqNo = ++timedWaitSeqNo;
            timeoutTask = schedule(() -> waitTimeoutExpired(seqNo), timeout, MILLISECONDS);
            setState(newState = TIMED_WAIT);
            blocked = notified && compareAndSetState(TIMED_WAIT, BLOCKED);
        }
    }

    if (blocked) {
        if (blockPermit && compareAndSetState(BLOCKED, UNBLOCKED)) {
            lazySubmitRunContinuation();
        }
    } else {
        // 过渡到 wait 状态期间可能被 interrupt
        if (interruptible && interrupted && compareAndSetState(newState, UNBLOCKED)) {
            lazySubmitRunContinuation();
        }
    }
}
```

### 10.3 waitTimeoutExpired — 定时等待超时

```java
private void waitTimeoutExpired(byte seqNo) {
    assert !Thread.currentThread().isVirtual();

    synchronized (timedWaitLock()) {
        if (seqNo != timedWaitSeqNo) {
            return;  // 这是过去的 timed-wait 的超时任务
        }
        if (!compareAndSetState(TIMED_WAIT, UNBLOCKED)) {
            return;  // 已被 notify 或 interrupt
        }
    }

    lazySubmitRunContinuation();
}
```

`timedWaitSeqNo` 是一个 `byte` 序列号，每次 timed-wait 递增。
当超时任务执行时，检查序列号是否匹配，避免过期的超时任务影响新的 wait。
`timedWaitLock()` 返回 `runContinuation` 对象作为锁，复用已有对象避免额外开销。

---

## 11. 中断机制

### 11.1 interrupt() 方法

```java
@Override
public void interrupt() {
    if (Thread.currentThread() != this) {
        Interruptible blocker;
        disableSuspendAndPreempt();
        try {
            synchronized (interruptLock) {
                interrupted = true;
                blocker = nioBlocker();
                if (blocker != null) {
                    blocker.interrupt(this);
                }
                // 中断载体线程（如果已 mount）
                Thread carrier = carrierThread;
                if (carrier != null) carrier.setInterrupt();
            }
        } finally {
            enableSuspendAndPreempt();
        }

        if (blocker != null) {
            blocker.postInterrupt();
        }

        // 使 parkPermit 可用，unpark 线程
        unpark();

        // 如果在 Object.wait 中，安排重新进入
        int s = state();
        if ((s == WAIT || s == TIMED_WAIT) && compareAndSetState(s, UNBLOCKED)) {
            submitRunContinuation();
        }
    } else {
        // 自我中断
        interrupted = true;
        carrierThread.setInterrupt();
        setParkPermit(true);
    }
}
```

中断处理层次：
1. 设置 `interrupted = true`。
2. 如果有 NIO blocker，中断它。
3. 如果已 mount，中断载体线程。
4. `unpark()` 唤醒 parked 的虚拟线程。
5. 如果在 `Object.wait` 中，CAS 到 `UNBLOCKED` 并重新提交。

---

## 12. Pinning 机制

### 12.1 什么是 Pinning

当 `Continuation.yield()` 无法成功时（返回非零值），虚拟线程被"pin"住，
无法从载体线程卸载。`doYield()` native 方法检测到以下情况时返回非零值：

```java
public enum Pinned {
    NATIVE,            // 栈上有 native 帧（JNI 调用等）
    CRITICAL_SECTION,  // Continuation.pin() 被调用（引用计数 > 0）
    EXCEPTION          // OOME/SOE 等异常状态
}
```

### 12.2 pin/unpin API

```java
// Continuation.java
@IntrinsicCandidate
public static native void pin();

@IntrinsicCandidate
public static native void unpin();
```

`pin()` 递增一个内部信号量，`unpin()` 递减。当信号量 > 0 时，`doYield()` 会失败。

### 12.3 VirtualThread 中 pin 的使用

```java
// disableSuspendAndPreempt — 在访问 interruptLock 等敏感操作前
private void disableSuspendAndPreempt() {
    notifyJvmtiDisableSuspend(true);
    Continuation.pin();
}

private void enableSuspendAndPreempt() {
    Continuation.unpin();
    notifyJvmtiDisableSuspend(false);
}
```

`disableSuspendAndPreempt()` 在以下场景使用：
- `interrupt()` 方法中访问 `interruptLock`。
- `unpark()` 中 pinned 路径访问 `carrierThreadAccessLock`。
- `threadState()` 和 `toString()` 中读取 `carrierThread`。
- `submitRunContinuation()` 中提交任务到调度器（防止提交期间 unmount）。

### 12.4 Pinned 时的降级处理

当 `yieldContinuation()` 返回 `false`（yield 失败）时，各操作的处理：

- **park()**：调用 `parkOnCarrierThread()`，在载体线程上 `Unsafe.park()`，
  进入 `PINNED`/`TIMED_PINNED` 状态。
- **tryYield()**：恢复 `RUNNING` 状态，yield 操作变成空操作。
- **BLOCKING（JEP 491 后不再常见）**：理论上不会发生，因为 JEP 491 改变了 VM 的 monitor 实现。

---

## 13. 定时任务调度

### 13.1 ForkJoinPool 内置调度

```java
private Future<?> schedule(Runnable command, long delay, TimeUnit unit) {
    if (scheduler instanceof ForkJoinPool pool) {
        return pool.schedule(command, delay, unit);
    } else {
        return DelayedTaskSchedulers.schedule(command, delay, unit);
    }
}
```

JDK 24+ 的 `ForkJoinPool` 直接支持 `schedule()` 方法，无需外部定时器。

### 13.2 DelayedTaskSchedulers — 自定义调度器的退路

当使用自定义 scheduler（非 `ForkJoinPool`）时，使用 `ScheduledThreadPoolExecutor` 池：

```java
private static class DelayedTaskSchedulers {
    private static final ScheduledExecutorService[] INSTANCE = createDelayedTaskSchedulers();

    static Future<?> schedule(Runnable command, long delay, TimeUnit unit) {
        long tid = Thread.currentThread().threadId();
        int index = (int) tid & (INSTANCE.length - 1);
        return INSTANCE[index].schedule(command, delay, unit);
    }

    private static ScheduledExecutorService[] createDelayedTaskSchedulers() {
        String propValue = System.getProperty("jdk.virtualThreadScheduler.timerQueues");
        int queueCount;
        if (propValue != null) {
            queueCount = Integer.parseInt(propValue);  // 必须是 2 的幂
        } else {
            int ncpus = Runtime.getRuntime().availableProcessors();
            queueCount = Math.max(Integer.highestOneBit(ncpus / 4), 1);
        }
        // 创建多个 STPE 实例减少竞争
        var schedulers = new ScheduledExecutorService[queueCount];
        for (int i = 0; i < queueCount; i++) {
            ScheduledThreadPoolExecutor stpe = (ScheduledThreadPoolExecutor)
                Executors.newScheduledThreadPool(1, task -> {
                    Thread t = InnocuousThread.newThread("VirtualThread-unparker", task);
                    t.setDaemon(true);
                    return t;
                });
            stpe.setRemoveOnCancelPolicy(true);
            schedulers[i] = stpe;
        }
        return schedulers;
    }
}
```

设计要点：
- 多个 `ScheduledThreadPoolExecutor` 实例，按线程 ID 分桶，减少延迟队列的竞争。
- 数量为 `max(highestOneBit(ncpus/4), 1)`，即 CPU 核数的 1/4（取最近的 2 的幂）。
- 每个实例单线程，线程名 `"VirtualThread-unparker"`。
- `setRemoveOnCancelPolicy(true)`——取消的任务立即从队列移除，避免内存泄漏。

---

## 14. 关键设计总结

### 14.1 核心架构

```
┌──────────────────────────────────────────────────────────────┐
│                       用户代码层                              │
│   Thread.start() / LockSupport.park() / synchronized / ...  │
├──────────────────────────────────────────────────────────────┤
│                    VirtualThread 调度层                       │
│   state machine (20 states) + mount/unmount + park/unpark   │
├──────────────────────────────────────────────────────────────┤
│                    Continuation 层                            │
│   yield/resume + StackChunk (heap-stored frames) + pinning  │
├──────────────────────────────────────────────────────────────┤
│                  ForkJoinPool 调度器                          │
│   work-stealing + carrier threads + compensation            │
├──────────────────────────────────────────────────────────────┤
│                      JVM / OS 层                             │
│   enterSpecial/doYield intrinsics + monitor support         │
└──────────────────────────────────────────────────────────────┘
```

### 14.2 设计原则总结

| 原则 | 实现 |
|------|------|
| **M:N 线程模型** | 多个虚拟线程复用少量载体线程（carrier threads） |
| **协作式调度** | 通过 `Continuation.yield()` 在阻塞点让出载体线程 |
| **无锁状态机** | 20 个状态 + CAS 操作，避免锁竞争 |
| **优雅降级** | yield 失败（pinned）时退回到载体线程上阻塞 |
| **竞态安全** | 每个状态转换都检查在转换过程中可能已发生的 unpark/unblock/interrupt |
| **最小化载体占用** | park/block/wait 时 yield continuation，释放载体线程 |
| **公平调度** | ForkJoinPool FIFO 模式（`asyncMode = true`） |
| **补偿机制** | pinned 阻塞时启动额外载体线程维持并行度 |

### 14.3 关键源码文件

| 文件 | 行数 | 职责 |
|------|------|------|
| `java.lang.VirtualThread` | 1445 | 虚拟线程核心实现：状态机、调度、park/unpark |
| `jdk.internal.vm.Continuation` | 507 | Delimited continuation：yield/resume、栈管理 |
| `jdk.internal.misc.CarrierThread` | ~150 | ForkJoinWorkerThread 子类：补偿机制 |
| `jdk.internal.vm.ContinuationScope` | ~60 | Continuation 作用域标识 |
| `java.lang.BaseVirtualThread` | ~80 | 抽象基类，定义 park/unpark/yield 接口 |
| `jdk.internal.vm.StackChunk` | (native) | 堆上的栈帧存储 |

### 14.4 运行时实体关系

```
VirtualThread (1个)
  ├── Continuation (1个) ── 封装了用户任务
  │     ├── ContinuationScope ── VTHREAD_SCOPE (共享)
  │     └── StackChunk* ── 堆上的栈帧链表 (yield 时保存)
  ├── Executor scheduler ── 通常是 DEFAULT_SCHEDULER (共享)
  └── carrierThread ── mount 时指向 CarrierThread (临时绑定)

ForkJoinPool DEFAULT_SCHEDULER (1个)
  ├── CarrierThread[0..maxPoolSize] ── ForkJoinWorkerThread 子类
  │     └── work queue ── 本地任务队列 (work-stealing)
  └── external submission queue ── 外部提交队列

VirtualThread-unblocker (1个) ── 处理 monitor unblock 链表
VirtualThread-unparker[0..N] ── 定时任务线程 (用于自定义 scheduler)
```

---

*源码引用基于 `src/java.base/share/classes/java/lang/VirtualThread.java`（1445 行）
和 `src/java.base/share/classes/jdk/internal/vm/Continuation.java`（507 行）。*
