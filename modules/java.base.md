# java.base 模块分析

> Java 平台的核心模块，包含最基础的 API

---

## 1. 模块概述

`java.base` 是 Java 平台的基础模块，所有其他模块都隐式依赖它。

### 模块定义

**文件**: `src/java.base/share/classes/module-info.java`

```java
module java.base {
    // 导出的包
    exports java.io;
    exports java.lang;
    exports java.lang.annotation;
    exports java.lang.constant;
    exports java.lang.invoke;
    exports java.lang.module;
    exports java.lang.ref;
    exports java.lang.reflect;
    exports java.math;
    exports java.net;
    exports java.nio;
    exports java.nio.channels;
    exports java.nio.charset;
    exports java.nio.file;
    exports java.security;
    exports java.security.cert;
    exports java.security.spec;
    exports java.text;
    exports java.text.spi;
    exports java.time;
    exports java.time.format;
    exports java.time.temporal;
    exports java.time.zone;
    exports java.util;
    exports java.util.concurrent;
    exports java.util.concurrent.atomic;
    exports java.util.concurrent.locks;
    exports java.util.function;
    exports java.util.jar;
    exports java.util.random;
    exports java.util.regex;
    exports java.util.spi;
    exports java.util.stream;
    exports java.util.zip;

    // 限定的导出
    exports com.sun.crypto.provider to jdk.crypto.cryptoki;
    exports jdk.internal to jdk.incubator.vector;
    exports jdk.internal.access to java.desktop, java.logging;
    exports jdk.internal.event to jdk.jfr;
    exports jdk.internal.javac to jdk.compiler, jdk.jshell;
    exports jdk.internal.jimage to jdk.jlink;
    exports jdk.internal.jrtfs to jdk.zipfs;
    exports jdk.internal.loader to java.logging, java.naming;
    exports jdk.internal.logger to java.logging;
    exports jdk.internal.math to jdk.compiler;
    exports jdk.internal.misc to java.desktop, java.logging;
    exports jdk.internal.module to jdk.incubator.vector, jdk.jlink;
    exports jdk.internal.org.objectweb.asm to jdk.compiler, jdk.jfr;
    exports jdk.internal.org.xml.sax to java.desktop;
    exports jdk.internal.perf to java.management, jdk.management.agent;
    exports jdk.internal.platform to jdk.management;
    exports jdk.internal.ref to java.desktop;
    exports jdk.internal.reflect to java.logging, java.sql;
    exports jdk.internal.util to jdk.compiler, jdk.jfr;
    exports jdk.internal.util.jar to jdk.jartool;
    exports jdk.internal.vm to jdk.internal.vm.ci, jdk.jfr;
    exports jdk.internal.vm.annotation to jdk.internal.vm.ci, jdk.jfr;
    exports jdk.internal.vm.vector to jdk.incubator.vector;
    exports sun.net.dns to java.security.jgss;
    exports sun.net.util to java.desktop, jdk.jconsole;
    exports sun.net.www to java.desktop;
    exports sun.nio.ch to jdk.crypto.cryptoki;
    exports sun.nio.cs to jdk.charsets;
    exports sun.reflect.annotation to jdk.compiler;
    exports sun.reflect.generics.reflectiveObjects to java.desktop;
    exports sun.reflect.misc to java.desktop;
    exports sun.security.action to java.security.jgss;
    exports sun.security.internal.interfaces to jdk.crypto.cryptoki;
    exports sun.security.jca to java.smartcardio;
    exports sun.security.pkcs to jdk.crypto.ec;
    exports sun.security.provider to jdk.crypto.cryptoki;
    exports sun.security.rsa to jdk.crypto.cryptoki;
    exports sun.security.ssl to java.security.jgss;
    exports sun.security.tools to jdk.jartool;
    exports sun.security.util to java.desktop, java.security.jgss;
    exports sun.security.x509 to jdk.crypto.ec;
    exports sun.text.resources to jdk.localedata;
    exports sun.util.cldr to jdk.jlink;
    exports sun.util.locale.provider to java.desktop;
    exports sun.util.logging to java.desktop, java.logging;
    exports sun.util.resources to jdk.localedata;

    // 服务
    uses java.lang.constant.ConstantDescs;
    uses java.nio.file.spi.FileSystemProvider;
    uses java.security.Provider;
    uses java.text.spi.BreakIteratorProvider;
    uses java.text.spi.CollatorProvider;
    uses java.time.zone.ZoneRulesProvider;
    uses java.util.spi.CalendarDataProvider;
    uses java.util.spi.CalendarNameProvider;
    uses java.util.spi.CurrencyNameProvider;
    uses java.util.spi.LocaleNameProvider;
    uses java.util.spi.ResourceBundleControlProvider;
    uses java.util.spi.ResourceBundleProvider;
    uses java.util.spi.TimeZoneNameProvider;
    uses jdk.internal.javac.PartnerProvider;

    // 提供的服务
    provides java.nio.file.spi.FileSystemProvider with
        jdk.internal.jrtfs.JrtFileSystemProvider;
}
```

---

## 2. 包结构

### 核心包

| 包 | 描述 | 重要类 |
|-----|------|--------|
| `java.lang` | 语言核心 | Object, String, Class, Thread, Math |
| `java.util` | 工具类 | List, Map, Set, Collections, Arrays |
| `java.io` | 输入输出 | InputStream, OutputStream, File |
| `java.nio` | 新 I/O | Buffer, Channel, Selector |
| `java.time` | 时间 API | LocalDate, Instant, Duration |
| `java.math` | 数学运算 | BigInteger, BigDecimal |
| `java.net` | 网络 | Socket, URL, URI |
| `java.security` | 安全 | MessageDigest, Signature, Key |

### 并发包

| 包 | 描述 | 重要类 |
|-----|------|--------|
| `java.util.concurrent` | 并发工具 | ExecutorService, Future, CompletableFuture |
| `java.util.concurrent.atomic` | 原子类 | AtomicInteger, AtomicReference |
| `java.util.concurrent.locks` | 锁 | ReentrantLock, ReadWriteLock |
| `java.lang.invoke` | 方法句柄 | MethodHandle, VarHandle |

### 内部包

| 包 | 描述 | 用途 |
|-----|------|------|
| `jdk.internal.misc` | 内部工具 | Unsafe, 共享秘密 |
| `jdk.internal.access` | 访问控制 | 跨模块访问 |
| `jdk.internal.loader` | 类加载 | 模块加载器 |
| `jdk.internal.vm` | VM 接口 | 虚拟线程支持 |

---

## 3. 核心类分析

### java.lang.String

**文件**: `src/java.base/share/classes/java/lang/String.java`

```java
public final class String
    implements java.io.Serializable, Comparable<String>, CharSequence,
               Constable, ConstantDesc {

    // JDK 9+: 使用 byte[] 存储字符串
    // Latin1: 每字符 1 byte
    // UTF16: 每字符 2 bytes
    private final byte[] value;

    // 编码标识: 0 = Latin1, 1 = UTF16
    private final byte coder;

    // 哈希值缓存
    private int hash;

    // JDK 26 新增: 高效复制到 byte[]
    void getBytes(byte[] dst, int dstBegin, int length) {
        if (length > 0) {
            UNSAFE.copyMemory(
                value,
                CHAR_ARRAY_BASE_OFFSET,
                dst,
                CHAR_ARRAY_BASE_OFFSET + (dstBegin << 1),
                length << 1
            );
        }
    }

    // JDK 26 新增: 直接创建 Latin1 字符串
    static String newStringWithLatin1Bytes(byte[] bytes) {
        return new String(bytes, LATIN1);
    }
}
```

### java.lang.Thread

**文件**: `src/java.base/share/classes/java/lang/Thread.java`

```java
public class Thread implements Runnable {
    // 线程名称
    private volatile String name;

    // 线程优先级
    private int priority;

    // 线程状态
    private volatile int threadStatus;

    // JDK 21+: 虚拟线程支持
    private final boolean virtual;

    // 线程局部变量
    ThreadLocal.ThreadLocalMap threadLocals;
    ThreadLocal.ThreadLocalMap inheritableThreadLocals;

    // JDK 26: Scoped Values 支持
    private ScopedValue.Bindings scopedValueBindings;

    // 构建器模式 (JDK 21+)
    public static Builder ofVirtual() { ... }
    public static Builder ofPlatform() { ... }

    // 启动虚拟线程
    public void start() {
        if (virtual) {
            // 委托给虚拟线程调度器
            VirtualThread.start(this);
        } else {
            // 传统平台线程
            start0();
        }
    }
}
```

### java.util.concurrent.StructuredTaskScope

**文件**: `src/java.base/share/classes/java/util/concurrent/StructuredTaskScope.java`

```java
// JDK 26: 第六次预览
public class StructuredTaskScope<T> implements AutoCloseable {

    // 成功策略: 等待所有任务完成
    public static final class ShutdownOnSuccess<T> extends StructuredTaskScope<T> {
        private static final int SUCCESS = 1;
        private static final int FAILED = 2;
        private volatile int state;
        private T result;
        private Throwable exception;

        public ShutdownOnSuccess() {
            super(null, Thread.ofVirtual().factory());
        }

        @Override
        protected void handleComplete(Future<T> future) {
            if (future.state() == Future.State.SUCCESS) {
                result = future.resultNow();
                shutdown();  // 成功后立即关闭
            }
        }

        public T result() throws ExecutionException {
            if (state == FAILED) {
                throw new ExecutionException(exception);
            }
            return result;
        }
    }

    // 失败策略: 任一失败即关闭
    public static final class ShutdownOnFailure extends StructuredTaskScope<Object> {
        private final ConcurrentHashMap<Future<?>, Throwable> exceptions;

        @Override
        protected void handleComplete(Future<?> future) {
            if (future.state() == Future.State.FAILED) {
                exceptions.put(future, future.exceptionNow());
                shutdown();  // 失败后立即关闭
            }
        }

        public void throwIfFailed() throws ExecutionException {
            if (!exceptions.isEmpty()) {
                throw new ExecutionException(exceptions.values().iterator().next());
            }
        }
    }
}
```

---

## 4. JDK 26 变更

### 新增 API

#### StableValue (JEP 502)

```java
// 文件: src/java.base/share/classes/java/lang/StableValue.java
public final class StableValue<T> {
    private static final VarHandle VALUE;
    private static final Object EMPTY = new Object();

    private volatile Object value = EMPTY;

    private StableValue() {}

    public static <T> StableValue<T> of() {
        return new StableValue<>();
    }

    public T orElseSet(IntFunction<? extends T> supplier) {
        Object v = value;
        if (v == EMPTY) {
            synchronized (this) {
                v = value;
                if (v == EMPTY) {
                    v = supplier.apply();
                    VALUE.setRelease(this, v);
                }
            }
        }
        @SuppressWarnings("unchecked")
        T result = (T) v;
        return result;
    }

    public T get() {
        Object v = value;
        if (v == EMPTY) {
            throw new IllegalStateException("value not set");
        }
        @SuppressWarnings("unchecked")
        T result = (T) v;
        return result;
    }
}
```

#### Scoped Values 增强

```java
// 文件: src/java.base/share/classes/java/lang/ScopedValue.java
public final class ScopedValue<T> {

    // JDK 26: 支持多个绑定
    public static <T> T get(ScopedValue<T> key) {
        Bindings bindings = Thread.currentScopedValueBindings();
        while (bindings != null) {
            if (bindings.key == key) {
                @SuppressWarnings("unchecked")
                T value = (T) bindings.value;
                return value;
            }
            bindings = bindings.next;
        }
        throw new NoSuchElementException("No binding for " + key);
    }

    // JDK 26: 改进的 where 方法
    public static <T> Where<T> where(ScopedValue<T> key, T value) {
        return new Where<>(key, value);
    }

    public static final class Where<T> {
        private final ScopedValue<T> key;
        private final T value;

        public void run(Runnable op) {
            Bindings bindings = new Bindings(key, value,
                Thread.currentScopedValueBindings());
            Thread.setCurrentScopedValueBindings(bindings);
            try {
                op.run();
            } finally {
                Thread.setCurrentScopedValueBindings(bindings.next);
            }
        }

        public <R> R call(Callable<R> op) throws Exception {
            Bindings bindings = new Bindings(key, value,
                Thread.currentScopedValueBindings());
            Thread.setCurrentScopedValueBindings(bindings);
            try {
                return op.call();
            } finally {
                Thread.setCurrentScopedValueBindings(bindings.next);
            }
        }
    }
}
```

### 性能优化

#### StringBuilder 优化

```java
// 文件: src/java.base/share/classes/java/lang/AbstractStringBuilder.java
public AbstractStringBuilder append(char[] str) {
    int len = str.length;
    ensureCapacityInternal(count + len);

    // JDK 26: 使用 Unsafe 批量复制
    UNSAFE.copyMemory(
        str,
        CHAR_ARRAY_BASE_OFFSET,
        value,
        CHAR_ARRAY_BASE_OFFSET + (count << 1),
        len << 1
    );

    count += len;
    return this;
}
```

---

## 5. 性能特性

### 内存布局优化

```
对象内存布局 (JDK 26 紧凑对象头):
┌─────────────────────────────────────────────────────┐
│ 对象头 (8-12 bytes, 压缩后)                         │
│ ├── 标记字 (4-8 bytes)                              │
│ └── 类指针 (4 bytes, 压缩)                          │
├─────────────────────────────────────────────────────┤
│ 实例数据                                            │
│ ├── 基本类型字段 (按大小对齐)                        │
│ └── 引用字段 (4 bytes, 压缩)                        │
├─────────────────────────────────────────────────────┤
│ 对齐填充 (8 字节对齐)                               │
└─────────────────────────────────────────────────────┘
```

### 字符串压缩

```java
// 字符串编码选择
static byte coder(byte[] bytes) {
    // 检查是否所有字符都是 Latin1
    for (byte b : bytes) {
        if ((b & 0xFF) > 0x7F) {
            return UTF16;  // 需要 UTF-16
        }
    }
    return LATIN1;  // 可以使用 Latin1
}
```

---

## 6. 相关链接

- [java.base API 文档](https://download.java.net/java/early_access/jdk26/docs/api/java.base/module-summary.html)
- [源码浏览](https://github.com/openjdk/jdk/tree/master/src/java.base)