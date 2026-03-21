# 内存管理

> 堆、栈、Metaspace、Compressed Oops 演进历程

[← 返回核心平台](../)

---

## 1. 快速概览

```
JDK 1.0 ── JDK 6u23 ── JDK 7 ── JDK 8 ── JDK 11 ── JDK 17 ── JDK 21 ── JDK 24 ── JDK 25
   │         │        │        │        │        │        │        │        │
堆/栈    Compressed  默认启用  元空间  ZGC    分代    AOT缓存  紧凑对象头
PermGen   Oops     Oops   字符串  低延迟  ZGC   JEP483   JEP519正式
```

### 核心演进

| 版本 | 特性 | 说明 | 内存节省 |
|------|------|------|----------|
| **JDK 6u23** | Compressed Oops | 压缩普通对象指针 | ~20-30% |
| **JDK 7** | Compressed Oops 默认 | 64位默认启用 | ~20-30% |
| **JDK 8** | 元空间 | 移除永久代 | 动态扩展 |
| **JDK 8u20** | String Deduplication | 字符串去重 | ~10% |
| **JDK 11** | ZGC | 低延迟 GC | 大内存友好 |
| **JDK 15** | ZGC 生产可用 | 正式版 | 稳定 |
| **JDK 21** | 分代 ZGC | 降低 GC 频率 | 更高效 |
| **JDK 24** | AOT 缓存 (JEP 483) | 预加载类链接 | 减少运行时分配 |
| **JDK 24** | 紧凑对象头实验 (JEP 450) | 实验性压缩对象头 | 需 UnlockExperimentalVMOptions |
| **JDK 25** | 紧凑对象头正式 (JEP 519) | 对象头 12→8 字节，生产就绪 | ~10-20% 堆内存节省 |

---

## 目录

- [内存区域](#内存区域)
- [内存分配](#内存分配)
- [内存优化](#内存优化)
- [最新增强](#最新增强)
- [核心贡献者](#核心贡献者)
- [相关链接](#相关链接)

---

## 2. 内存区域

### JVM 内存结构

```
┌─────────────────────────────────────────────────────────┐
│                     JVM 内存结构                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────┐       │
│  │              堆内存 (Heap)                 │       │
│  │  ├── 年轻代 (Young Generation)              │       │
│  │  │   ├── Eden 区                            │       │
│  │  │   └── Survivor 区 (S0, S1)               │       │
│  │  └── 老年代 (Old Generation)                │       │
│  │      ├── 存活期长的对象                      │       │
│  │      └── 大对象直接分配                      │       │
│  └─────────────────────────────────────────────┘       │
│                                                         │
│  ┌─────────────────────────────────────────────┐       │
│  │            栈内存 (Stack)                   │       │
│  │  ├── Java 栈 (每线程一个)                   │       │
│  │  │   ├── 栈帧 (方法调用)                    │       │
│  │  │   ├── 局部变量                           │       │
│  │  │   └── 操作数栈                           │       │
│  │  └── 本地方法栈 (Native Stack)              │       │
│  └─────────────────────────────────────────────┘       │
│                                                         │
│  ┌─────────────────────────────────────────────┐       │
│  │          方法区 (Method Area)               │       │
│  │  ├── 元空间 (Metaspace, JDK 8+)            │       │
│  │  │   ├── 类元数据                           │       │
│  │  │   ├── 方法元数据                         │       │
│  │  │   └── 常量池                             │       │
│  │  └── 永久代 (PermGen, JDK 7-)              │       │
│  └─────────────────────────────────────────────┘       │
│                                                         │
│  ┌─────────────────────────────────────────────┐       │
│  │         本地内存 (Native Memory)            │       │
│  │  ├── 直接内存 (Direct Memory)               │       │
│  │  │   └── NIO 缓冲区                         │       │
│  │  ├── 线程栈                                 │       │
│  │  ├── 代码缓存 (Code Cache)                  │       │
│  │  └── GC 工作内存                            │       │
│  └─────────────────────────────────────────────┘       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 堆内存

**特点**:
- 线程共享
- 存储对象实例
- GC 主要区域

**配置参数**:

```bash
# 堆内存大小
-Xms4g          # 初始堆大小
-Xmx4g          # 最大堆大小
-XX:NewRatio=2  # 年轻代/老年代比例

# 年轻代配置
-Xmn2g          # 年轻代大小
-XX:SurvivorRatio=8    # Eden/S0/S1 比例

# 大对象直接进入老年代
-XX:PretenureSizeThreshold=3m  # 大对象阈值
```

### 栈内存

**特点**:
- 线程私有
- 存储局部变量和方法调用
- 自动管理 (方法出栈自动释放)

**配置参数**:

```bash
# 栈内存大小
-Xss1m          # 每线程栈大小 (JDK 8+)
-XX:ThreadStackSize=1024  # 每线程栈大小 (KB)

# 栈深度监控
-XX:MaxRecursiveInlineLevel=20  # 最大递归内联层级
```

**栈溢出 (StackOverflowError)**:

```java
// 递归过深导致栈溢出
public class StackOverflow {
    public static void recursive() {
        recursive();  // 无限递归
    }

    public static void main(String[] args) {
        recursive();  // StackOverflowError
    }
}
```

### 元空间 (Metaspace)

**JDK 8+ 变化**:

| 特性 | 永久代 (PermGen) | 元空间 (Metaspace) |
|------|------------------|-------------------|
| 位置 | 堆内 | 本地内存 |
| 大小 | 固定 | 动态扩展 |
| 垃圾回收 | 需要Full GC | 自动触发 |
| 默认大小 | 固定 | 无限制 |
| 调整困难 | 是 | 否 |

**配置参数**:

```bash
# 元空间大小
-XX:MetaspaceSize=256m           # 初始元空间大小
-XX:MaxMetaspaceSize=512m        # 最大元空间大小
-XX:CompressedClassSpaceSize=1g  # 压缩类空间大小

# 监控元空间
-XX:+PrintGCDetails              # 打印 GC 详情
-XX:+PrintGCTimeStamps           # 打印 GC 时间戳
```

**类卸载**:

```java
// 类卸载条件:
// 1. 类的所有实例被回收
// 2. 加载该类的 ClassLoader 被回收
// 3. 该类的 Class 对象没有被引用

// 自定义 ClassLoader 可实现类卸载
public class UnloadableClassLoader extends ClassLoader {
    public Class<?> loadClass(String name) throws ClassNotFoundException {
        // 自定义加载逻辑
        return super.loadClass(name);
    }
}
```

### 直接内存

**特点**:
- 不在堆上分配
- 避免 JVM 堆与本地内存之间复制
- 用于 NIO 操作

**配置参数**:

```bash
# 直接内存大小
-XX:MaxDirectMemorySize=1g  # 最大直接内存 (默认 ≈ 堆大小)

# 监控直接内存
-XX:+PrintGCDetails         # 包含直接内存信息
```

**使用示例**:

```java
// 分配直接内存
ByteBuffer buffer = ByteBuffer.allocateDirect(1024 * 1024);

// vs 堆内存
ByteBuffer heapBuffer = ByteBuffer.allocate(1024 * 1024);
```

---

## 3. 内存分配

### 对象分配过程

```
┌─────────────────────────────────────────────────────────┐
│                 对象分配过程                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. 类加载检查                                          │
│     ├── 类是否已加载                                   │
│     └── 类元数据是否准备                               │
│                                                         │
│  2. 对象大小计算                                        │
│     ├── 实例数据大小                                   │
│     ├── 对象头大小                                     │
│     └── 对齐填充                                       │
│                                                         │
│  3. 选择分配方式                                        │
│     ├── TLAB (线程本地分配缓冲)                        │
│     └── 直接在 Eden 分配                               │
│                                                         │
│  4. 内存空间初始化                                      │
│     ├── 清零内存                                       │
│     └── 设置对象头                                     │
│                                                         │
│  5. 构造方法调用                                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### TLAB (Thread-Local Allocation Buffer)

**特点**:
- 线程私有
- 无锁分配
- 提高分配效率

**配置参数**:

```bash
# TLAB 配置
-XX:+UseTLAB                     # 启用 TLAB (默认)
-XX:TLABSize=256k                # TLAB 初始大小
-XX:TLABWasteTargetPercent=1     # TLAB 浪费目标比例
-XX:ResizeTLAB                   # 动态调整 TLAB 大小
```

### 对象内存布局

```
┌─────────────────────────────────────────────────────────┐
│                  对象内存布局                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  普通对象 (JDK 25 JEP 519 紧凑对象头, 需 -XX:+UseCompactObjectHeaders): │
│  ┌───────────────────────────────────────────┐         │
│  │  Mark Word (8 bytes, 含类信息)            │         │
│  │  ├── 锁状态                               │         │
│  │  ├── GC 标记                              │         │
│  │  ├── HashCode                             │         │
│  │  └── 类指针 (合并在 Mark Word 中)         │         │
│  ├───────────────────────────────────────────┤         │
│  │  Fields                                  │         │
│  │  ├── 实例数据                             │         │
│  │  └── 对齐填充                             │         │
│  └───────────────────────────────────────────┘         │
│                                                         │
│  数组对象:                                              │
│  ┌───────────────────────────────────────────┐         │
│  │  Mark Word (8 bytes, 含类信息)            │         │
│  ├───────────────────────────────────────────┤         │
│  │  Array Length (4 bytes)                   │         │
│  ├───────────────────────────────────────────┤         │
│  │  Array Elements                          │         │
│  │  └── 数组元素                             │         │
│  └───────────────────────────────────────────┘         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 对象头 (Mark Word)

```
┌─────────────────────────────────────────────────────────┐
│                 Mark Word 结构                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  64 位 JVM:                                            │
│  │ unused:25│ hashcode:31│ unused:1│ age:4│ biased:1│01││
│                                                         │
│  32 位 JVM:                                            │
│  │ thread:13│ epoch:2│ age:4│ biased:1│01│ size:1│00││
│                                                         │
│  锁状态:                                               │
│  ├── 01 - 无锁或偏向锁                                  │
│  ├── 00 - 轻量级锁                                      │
│  ├── 10 - 重量级锁 (Monitor)                            │
│  └── 11 - GC 标记                                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 4. 内存优化

### Compressed Oops

**压缩普通对象指针**

**原理**:
- 64 位 JVM 使用 32 位指针
- 利用对象 8 字节对齐特性
- 指针左移 3 位，寻址范围扩大 8 倍

**配置参数**:

```bash
# 启用压缩指针 (默认启用)
-XX:+UseCompressedOops

# 堆大小限制
# < 32GB: 32 位指针
# >= 32GB: 64 位指针

# 调整压缩阈值
-XX:CompressedClassSpaceSize=1g  # 压缩类空间大小
```

**内存节省**:
- 每个对象引用节省 4 字节
- 每个对象节省 8-12 字节
- 整体内存节省约 20-30%

### String Deduplication

**字符串去重**

**原理**:
- G1 GC 识别重复字符串
- 保留一个副本，其他指向该副本
- 减少内存占用

**配置参数**:

```bash
# 启用字符串去重 (默认未启用)
-XX:+UseStringDeduplication

# 去重阈值
-XX:StringDeduplicationAgeThreshold=3

# 支持 G1、ZGC 和 Parallel GC (JDK 18+)
-XX:+UseG1GC
```

### 对象池

**重用对象减少分配**

```java
// ✅ 推荐: 使用对象池
private static final DateFormat DATE_FORMAT =
    new SimpleDateFormat("yyyy-MM-dd");

// ❌ 避免: 重复创建
for (int i = 0; i < 1000; i++) {
    DateFormat df = new SimpleDateFormat("yyyy-MM-dd");
    df.format(date);
}
```

### 集合初始化

**指定初始容量避免扩容**

```java
// ✅ 推荐: 指定初始容量
List<String> list = new ArrayList<>(1000);
Map<String, Integer> map = new HashMap<>(1000);

// ❌ 避免: 默认容量导致扩容
List<String> list = new ArrayList<>();
for (int i = 0; i < 1000; i++) {
    list.add("item");  // 多次扩容
}
```

### 弱引用

**避免内存泄漏**

```java
// WeakReference - GC 时回收
WeakReference<byte[]> ref = new WeakReference<>(new byte[1024 * 1024]);

// SoftReference - 内存不足时回收
SoftReference<byte[]> softRef = new SoftReference<>(new byte[1024 * 1024]);

// PhantomReference - 用于跟踪对象回收
ReferenceQueue<byte[]> queue = new ReferenceQueue<>();
PhantomReference<byte[]> phantomRef = new PhantomReference<>(new byte[1024 * 1024], queue);
```

---

## 5. 最新增强

### JDK 24: AOT 缓存

**JEP 483: Ahead-of-Time Class Loading & Linking**

减少运行时内存分配：

```bash
# 创建 AOT 缓存
java -XX:AOTCacheConfiguration=aot_config.txt \
     -XX:StoreAOTCacheConfiguration \
     MyApp

# 使用 AOT 缓存
java -XX:AOTCacheConfiguration=aot_config.txt \
     MyApp
```

**内存优势**:
- 减少类加载期间内存分配
- 减少元空间使用
- 降低 GC 压力

### JDK 24: 紧凑对象头 (实验)

**JEP 450: Compact Object Headers (Experimental)**

```bash
# JDK 24: 需要 UnlockExperimentalVMOptions
-XX:+UnlockExperimentalVMOptions -XX:+UseCompactObjectHeaders
```

### JDK 25: 紧凑对象头 (正式)

**JEP 519: Compact Object Headers** — Project Lilliput 首个正式集成特性

```bash
# JDK 25+: 生产就绪，不再需要 UnlockExperimentalVMOptions
# 注意: 非默认启用，需显式开启
-XX:+UseCompactObjectHeaders
```

**演进路线**:
- JDK 22: Object Monitor Tables 基础设施
- JDK 24 (JEP 450): 实验性紧凑对象头
- JDK 25 (JEP 519): 正式生产就绪特性 (非默认启用)
- 未来版本: 计划默认启用

**内存节省**:
- 对象头从 12 字节减少到 8 字节 (类指针合并到 Mark Word)
- SPECjbb2015: 堆空间减少 **22%**, CPU 时间减少 **8%**
- 含大量小对象的应用: 总活跃数据内存减少 **10-20%**
- GC 改进: SPECjbb2015 中 G1/Parallel 收集器 GC 周期减少约 **15%**, 标记阶段缩短, GC 暂停减少 **10-15%**

**生产验证**: Amazon 已将此特性反向移植至 JDK 17/21 并在数百个生产服务中部署，测量到一致的效率提升且无回归

---

## 6. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 内存管理 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | [Coleen Phillimore](/by-contributor/profiles/coleen-phillimore.md) | 317 | Oracle | 类加载, 运行时 |
| 2 | [Ioi Lam](/by-contributor/profiles/ioi-lam.md) | 215 | Oracle | CDS, AOT, 内存 |
| 3 | [David Holmes](/by-contributor/profiles/david-holmes.md) | 174 | Oracle | 并发, 线程 |
| 4 | Thomas Stuefe | 163 | Red Hat | 内存, 跨平台 |
| 5 | Stefan Karlsson | 149 | Oracle | 并发 GC |
| 6 | Kim Barrett | 113 | Oracle | C++ 现代化 |
| 7 | [Aleksey Shipilev](/by-contributor/profiles/aleksey-shipilev.md) | 112 | Amazon | 性能基准 |
| 8 | Robbin Ehn | 77 | Oracle | 并发, 锁 |
| 9 | Calvin Cheung | 77 | Oracle | 类加载 |
| 10 | Patricio Chilano Mateo | 76 | Oracle | 运行时 |

---

## 7. 重要 PR 分析

### 元空间优化

#### JDK-8349400: 消除匿名内部类

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐ 元空间占用 -82%

通过消除枚举中的匿名内部类来减少元空间占用：

**问题**: `KnownOIDs` 枚举有 10 个匿名内部类，每个占用约 1-2KB 元空间

**解决方案**: 将方法覆盖转换为构造函数参数

```java
// 优化前：匿名内部类
KP_TimeStamping("1.3.6.1.5.5.7.3.8", "timeStamping") {
    @Override
    boolean registerNames() { return false; }
}

// 优化后：构造函数参数
KP_TimeStamping("1.3.6.1.5.5.7.3.8", "timeStamping", false)
```

**效果**:
- 类加载数量：11 → 1（-90%）
- 元空间占用：22KB → 4KB（-82%）

→ [详细分析](/by-pr/8349/8349400.md)

### 字符串内存优化

#### JDK-8334328: FloatToDecimal/DoubleToDecimal 优化

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐⭐ +30-50% 性能提升

重构浮点数转字符串实现，减少对象分配：

**优化点**:
- 创建共享实例 (`LATIN1`, `UTF16`)
- 无状态方法设计
- 直接写入 StringBuilder 内部数组

→ [详细分析](/by-pr/8334/8334328.md)

### StringBuilder 内存优化

#### JDK-8355177: append(char[]) 优化

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐⭐ +15% 性能提升

使用 `Unsafe.copyMemory` 替代 `System.arraycopy`：

**内存优势**:
- 减少临时对象创建
- 消除 JNI 边界跨越
- 更好的缓存局部性

→ [详细分析](/by-pr/8355/8355177.md)

---

## 8. 内存优化最佳实践

### 减少元空间占用

```java
// ❌ 避免：匿名内部类
enum MyEnum {
    VALUE {
        @Override
        void method() { /* ... */ }
    }
}

// ✅ 推荐：使用枚举字段或构造函数参数
enum MyEnum {
    VALUE(false);  // 通过参数控制行为
    final boolean flag;
    MyEnum(boolean flag) { this.flag = flag; }
}
```

### 减少对象分配

```java
// ❌ 避免：循环内创建对象
for (int i = 0; i < 1000; i++) {
    String result = prefix + i + suffix;  // 每次创建新对象
}

// ✅ 推荐：使用 StringBuilder
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 1000; i++) {
    sb.setLength(0);
    sb.append(prefix).append(i).append(suffix);
}
```

### 使用对象池

```java
// ✅ 推荐：重用昂贵对象
private static final DateTimeFormatter DATE_FORMATTER =
    DateTimeFormatter.ofPattern("yyyy-MM-dd");

// ❌ 避免：重复创建
for (LocalDate date : dates) {
    DateTimeFormatter formatter =
        DateTimeFormatter.ofPattern("yyyy-MM-dd");  // 每次创建
}
```

---

## 9. 相关链接

### 内部文档

- [内存时间线](timeline.md) - 详细的历史演进
- [Arena 详解](../panama/arena.md) - 堆外内存生命周期管理
- [GC 演进](../gc/) - 垃圾回收器
- [JVM 调优](../jvm/) - JVM 参数调优
- [性能优化](../performance/) - JIT 编译

### 外部资源

- [Tuning Garbage Collectors](https://docs.oracle.com/en/java/javase/21/gctuning/)
- [Java HotSpot VM Options](https://docs.oracle.com/en/java/javase/21/vm-options/)
- [Understanding Metaspace](https://oracle.com/technical-resources/articles/java/javadependencies.html)

### Git 仓库

```bash
# 查看内存管理相关提交
git log --oneline -- src/hotspot/share/memory/
git log --oneline -- src/hotspot/share/oops/
git log --oneline -- src/hotspot/share/classfile/
```

---

**最后更新**: 2026-03-20
