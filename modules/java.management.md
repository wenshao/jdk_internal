# java.management 模块分析 (Java Management Extensions)

> JMX (Java Management Extensions) 监控与管理框架，328 个源文件

---

## 1. 模块概述 (Overview)

`java.management` 提供 JMX 核心功能和平台 MXBean，用于监控和管理 JVM 运行状态。

### 模块定义 (Module Declaration)

**源码**: `src/java.management/share/classes/module-info.java`

```java
/**
 * Defines the Java Management Extensions (JMX) API.
 * The JMX API consists of interfaces for monitoring and management of the
 * JVM and other components in the Java runtime.
 */
module java.management {
    // 公开 API 包
    exports java.lang.management;
    exports javax.management;
    exports javax.management.loading;
    exports javax.management.modelmbean;
    exports javax.management.monitor;
    exports javax.management.openmbean;
    exports javax.management.relation;
    exports javax.management.remote;
    exports javax.management.timer;

    // 内部包 (限定导出)
    exports com.sun.jmx.remote.internal to java.management.rmi;
    exports com.sun.jmx.remote.security to java.management.rmi;
    exports com.sun.jmx.remote.util to java.management.rmi;
    exports sun.management to
        jdk.management, jdk.management.agent, jdk.management.jfr, jdk.jconsole;
    exports sun.management.counter to jdk.management.agent;
    exports sun.management.counter.perf to jdk.management.agent;
    exports sun.management.spi to jdk.management, jdk.internal.jvmstat;
}
```

### 包结构与文件统计 (Package Structure)

| 包 | 文件数 | 说明 |
|---|---|---|
| `java.lang.management` | 22 | 平台 MXBean 接口 |
| `javax.management` | 87 | JMX 核心 API (MBeanServer, ObjectName, ...) |
| `javax.management.loading` | 4 | MBean 类加载器 |
| `javax.management.modelmbean` | ~15 | Model MBean |
| `javax.management.monitor` | ~12 | 监控 MBean (计数器/仪表/字符串监视器) |
| `javax.management.openmbean` | ~25 | 开放类型 MBean |
| `javax.management.relation` | ~18 | MBean 关系服务 |
| `javax.management.remote` | ~19 | JMX 远程连接 |
| `javax.management.timer` | ~3 | 定时器 MBean |
| `com.sun.jmx.mbeanserver` | 35 | MBeanServer 内部实现 |
| `com.sun.jmx.interceptor` | 2 | MBeanServer 拦截器 |
| `com.sun.jmx.defaults` | 2 | JMX 默认属性 |
| `com.sun.jmx.remote.*` | ~8 | 远程连接内部实现 |
| `sun.management` | ~30 | 平台 MXBean 实现 (HotSpot) |
| `sun.management.counter` | ~8 | 性能计数器 |
| **合计** | **328** | |

### JMX 三层架构 (Three-Layer Architecture)

```
┌──────────────────────────────────────────────────────────┐
│               远程管理层 (Remote Management)              │
│  JConsole / VisualVM / 自定义客户端 (Custom Client)       │
│  通过 JMXConnector (RMI/JMXMP) 远程连接                  │
├──────────────────────────────────────────────────────────┤
│                代理层 (Agent Level)                       │
│  MBeanServer — MBean 注册中心 (Registry)                 │
│  ├─ registerMBean()    注册 MBean                        │
│  ├─ getAttribute()     获取属性                           │
│  ├─ setAttribute()     设置属性                           │
│  ├─ invoke()           调用操作                           │
│  └─ queryNames()       查询 MBean                        │
├──────────────────────────────────────────────────────────┤
│              插桩层 (Instrumentation Level)               │
│  MBean (被管理的资源)                                     │
│  ├─ Standard MBean    (接口约定: XXXMBean)                │
│  ├─ MXBean            (开放类型映射, 推荐)                 │
│  ├─ Dynamic MBean     (运行时定义属性/操作)                │
│  └─ Model MBean       (通用可配置 MBean)                  │
└──────────────────────────────────────────────────────────┘
```

---

## 2. java.lang.management 平台 MXBean (22 files)

### 2.1 平台 MXBean 接口

| MXBean 接口 | ObjectName | 说明 |
|---|---|---|
| `ClassLoadingMXBean` | `java.lang:type=ClassLoading` | 类加载统计 (已加载/卸载类数) |
| `CompilationMXBean` | `java.lang:type=Compilation` | JIT 编译统计 (编译时间) |
| `MemoryMXBean` | `java.lang:type=Memory` | 堆/非堆内存使用 |
| `MemoryPoolMXBean` | `java.lang:type=MemoryPool,name=*` | 各内存池详情 (Eden, Old Gen, ...) |
| `MemoryManagerMXBean` | `java.lang:type=MemoryManager,name=*` | 内存管理器 |
| `GarbageCollectorMXBean` | `java.lang:type=GarbageCollector,name=*` | GC 统计 (次数/时间) |
| `ThreadMXBean` | `java.lang:type=Threading` | 线程统计 (数量/死锁检测) |
| `RuntimeMXBean` | `java.lang:type=Runtime` | 运行时信息 (启动时间/JVM 参数) |
| `OperatingSystemMXBean` | `java.lang:type=OperatingSystem` | 操作系统信息 (CPU/内存) |
| `BufferPoolMXBean` | `java.nio:type=BufferPool,name=*` | NIO 缓冲池统计 |
| `PlatformLoggingMXBean` | `java.util.logging:type=Logging` | 日志管理 (需 java.logging) |

### 2.2 辅助类

| 类 | 说明 |
|---|---|
| `ManagementFactory` | 平台 MXBean 获取的入口工厂类 |
| `ManagementPermission` | JMX 操作权限 |
| `PlatformManagedObject` | 所有平台 MXBean 的基接口 |
| `MemoryUsage` | 内存使用数据 (init/used/committed/max) |
| `MemoryType` | 内存类型枚举 (HEAP / NON_HEAP) |
| `MemoryNotificationInfo` | 内存阈值通知信息 |
| `ThreadInfo` | 线程状态快照 (含堆栈、锁信息) |
| `LockInfo` | 锁信息 |
| `MonitorInfo` | 监视器锁信息 |

### 2.3 ManagementFactory 工厂方法

**源码**: `src/java.management/share/classes/java/lang/management/ManagementFactory.java`

```java
public class ManagementFactory {
    // 获取平台 MBeanServer
    public static MBeanServer getPlatformMBeanServer()

    // 获取各类 MXBean
    public static ClassLoadingMXBean getClassLoadingMXBean()
    public static CompilationMXBean getCompilationMXBean()
    public static MemoryMXBean getMemoryMXBean()
    public static ThreadMXBean getThreadMXBean()
    public static RuntimeMXBean getRuntimeMXBean()
    public static OperatingSystemMXBean getOperatingSystemMXBean()
    public static List<MemoryPoolMXBean> getMemoryPoolMXBeans()
    public static List<MemoryManagerMXBean> getMemoryManagerMXBeans()
    public static List<GarbageCollectorMXBean> getGarbageCollectorMXBeans()

    // 通过 MBeanServerConnection 创建远程代理
    public static <T> T newPlatformMXBeanProxy(
        MBeanServerConnection connection,
        String mxbeanName,
        Class<T> mxbeanInterface)

    // 获取指定类型的平台 MXBean
    public static <T extends PlatformManagedObject> T getPlatformMXBean(Class<T> mxbeanInterface)
    public static <T extends PlatformManagedObject> List<T> getPlatformMXBeans(Class<T> mxbeanInterface)
}
```

---

## 3. javax.management 核心 API (87 files)

### 3.1 MBeanServer

**源码**: `src/java.management/share/classes/javax/management/MBeanServer.java`

```java
public interface MBeanServer extends MBeanServerConnection {
    // 注册/注销 MBean
    ObjectInstance registerMBean(Object object, ObjectName name)
        throws InstanceAlreadyExistsException, MBeanRegistrationException, NotCompliantMBeanException;
    void unregisterMBean(ObjectName name)
        throws InstanceNotFoundException, MBeanRegistrationException;

    // 属性访问
    Object getAttribute(ObjectName name, String attribute)
    void setAttribute(ObjectName name, Attribute attribute)
    AttributeList getAttributes(ObjectName name, String[] attributes)
    AttributeList setAttributes(ObjectName name, AttributeList attributes)

    // 操作调用
    Object invoke(ObjectName name, String operationName,
                  Object[] params, String[] signature)

    // 查询
    Set<ObjectName> queryNames(ObjectName name, QueryExp query)
    Set<ObjectInstance> queryMBeans(ObjectName name, QueryExp query)

    // 实例化
    Object instantiate(String className)
    ObjectInstance createMBean(String className, ObjectName name)

    // 通知
    void addNotificationListener(ObjectName name, NotificationListener listener,
                                 NotificationFilter filter, Object handback)
}
```

### 3.2 ObjectName 命名

**源码**: `src/java.management/share/classes/javax/management/ObjectName.java`

```java
public class ObjectName implements Comparable<ObjectName>, QueryExp {
    // 格式: domain:key1=value1,key2=value2,...
    public ObjectName(String name) throws MalformedObjectNameException
    public ObjectName(String domain, String key, String value)
    public ObjectName(String domain, Hashtable<String,String> table)

    public String getDomain()
    public String getKeyProperty(String property)
    public boolean isPattern()  // 是否包含通配符
}
```

**命名示例**:

```
java.lang:type=Memory
java.lang:type=GarbageCollector,name=G1 Young Generation
java.lang:type=MemoryPool,name=G1 Eden Space
com.example:type=UserService,name=default
```

### 3.3 MBean 类型对比

| 特性 | Standard MBean | MXBean (推荐) | Dynamic MBean |
|---|---|---|---|
| 接口约定 | `XXXMBean` 接口 | `@MXBean` 注解或 `XXXMXBean` 接口 | `DynamicMBean` 接口 |
| 类型映射 | Java 类型 | 自动映射为开放类型 (Open Type) | 手动 |
| 远程兼容 | 需要客户端有接口类 | 开放类型，无需客户端类 | 自描述 |
| 适用场景 | 简单管理 | 推荐用于所有新代码 | 运行时动态定义 |

### 3.4 javax.management 子包

**openmbean (开放类型)**:

| 类 | 说明 |
|---|---|
| `OpenType` | 开放类型基类 |
| `SimpleType` | 简单类型 (String, Integer, ...) |
| `CompositeType` / `CompositeData` | 复合类型 (结构体) |
| `TabularType` / `TabularData` | 表格类型 |
| `ArrayType` | 数组类型 |

**remote (远程连接)**:

| 类 | 说明 |
|---|---|
| `JMXServiceURL` | JMX 服务地址 |
| `JMXConnector` | 客户端连接器 |
| `JMXConnectorFactory` | 连接器工厂 |
| `JMXConnectorServer` | 服务端连接器 |
| `JMXConnectorServerFactory` | 服务端工厂 |
| `JMXConnectionNotification` | 连接通知 |

**monitor (监控)**:

| 类 | 说明 |
|---|---|
| `Monitor` | 监控基类 |
| `CounterMonitor` | 计数器监视器 |
| `GaugeMonitor` | 仪表监视器 |
| `StringMonitor` | 字符串监视器 |

**relation (关系)**:

| 类 | 说明 |
|---|---|
| `RelationService` | MBean 间关系管理 |
| `Role` / `RoleInfo` | 角色定义 |
| `RelationType` | 关系类型 |

---

## 4. sun.management 内部实现 (HotSpot)

### 4.1 MXBean 实现类

| 实现类 | 对应接口 | 说明 |
|---|---|---|
| `ClassLoadingImpl` | `ClassLoadingMXBean` | 类加载统计实现 |
| `CompilationImpl` | `CompilationMXBean` | JIT 编译统计实现 |
| `GarbageCollectorImpl` | `GarbageCollectorMXBean` | GC 统计实现 |
| `BaseOperatingSystemImpl` | `OperatingSystemMXBean` | 操作系统信息基础实现 |

### 4.2 HotSpot 诊断 MBean

| 类 | 说明 |
|---|---|
| `HotspotClassLoading` | HotSpot 类加载内部统计 |
| `HotspotCompilation` | HotSpot JIT 编译内部统计 |
| `HotspotMemory` | HotSpot 内存内部统计 |
| `HotspotRuntime` | HotSpot 运行时内部统计 |
| `HotspotThread` | HotSpot 线程内部统计 |
| `HotspotInternal` | HotSpot 内部综合 MBean |

---

## 5. JMX 远程连接 (Remote Access)

### 5.1 启用 JMX 远程监控

```bash
# 基本启用 (仅限本地测试，无认证)
java -Dcom.sun.management.jmxremote.port=9010 \
     -Dcom.sun.management.jmxremote.authenticate=false \
     -Dcom.sun.management.jmxremote.ssl=false \
     -jar app.jar

# 生产环境 (认证 + SSL)
java -Dcom.sun.management.jmxremote.port=9010 \
     -Dcom.sun.management.jmxremote.authenticate=true \
     -Dcom.sun.management.jmxremote.password.file=jmxremote.password \
     -Dcom.sun.management.jmxremote.access.file=jmxremote.access \
     -Dcom.sun.management.jmxremote.ssl=true \
     -jar app.jar
```

### 5.2 客户端连接代码

```java
JMXServiceURL url = new JMXServiceURL(
    "service:jmx:rmi:///jndi/rmi://localhost:9010/jmxrmi");

// 带认证的连接
Map<String, Object> env = new HashMap<>();
env.put(JMXConnector.CREDENTIALS, new String[]{"admin", "password"});

JMXConnector connector = JMXConnectorFactory.connect(url, env);
MBeanServerConnection mbs = connector.getMBeanServerConnection();
```

---

## 6. 使用示例 (Usage Examples)

### 6.1 获取内存使用信息

```java
MemoryMXBean memory = ManagementFactory.getMemoryMXBean();
MemoryUsage heap = memory.getHeapMemoryUsage();

System.out.printf("Heap: used=%dMB, committed=%dMB, max=%dMB%n",
    heap.getUsed() / 1024 / 1024,
    heap.getCommitted() / 1024 / 1024,
    heap.getMax() / 1024 / 1024);

MemoryUsage nonHeap = memory.getNonHeapMemoryUsage();
System.out.printf("Non-Heap: used=%dMB%n", nonHeap.getUsed() / 1024 / 1024);
```

### 6.2 GC 统计

```java
List<GarbageCollectorMXBean> gcBeans = ManagementFactory.getGarbageCollectorMXBeans();
for (GarbageCollectorMXBean gc : gcBeans) {
    System.out.printf("GC '%s': count=%d, time=%dms%n",
        gc.getName(),
        gc.getCollectionCount(),
        gc.getCollectionTime());
}
// 输出示例:
// GC 'G1 Young Generation': count=42, time=156ms
// GC 'G1 Old Generation': count=2, time=89ms
```

### 6.3 线程监控与死锁检测

```java
ThreadMXBean thread = ManagementFactory.getThreadMXBean();
System.out.println("线程总数: " + thread.getThreadCount());
System.out.println("峰值线程数: " + thread.getPeakThreadCount());
System.out.println("守护线程数: " + thread.getDaemonThreadCount());

// 死锁检测 (Deadlock Detection)
long[] deadlocked = thread.findDeadlockedThreads();
if (deadlocked != null) {
    ThreadInfo[] infos = thread.getThreadInfo(deadlocked, true, true);
    for (ThreadInfo info : infos) {
        System.out.println("死锁线程: " + info.getThreadName());
        System.out.println("等待锁: " + info.getLockInfo());
        System.out.println("锁持有者: " + info.getLockOwnerName());
    }
}
```

### 6.4 内存池监控

```java
List<MemoryPoolMXBean> pools = ManagementFactory.getMemoryPoolMXBeans();
for (MemoryPoolMXBean pool : pools) {
    MemoryUsage usage = pool.getUsage();
    System.out.printf("Pool '%s' (%s): used=%dKB, max=%dKB%n",
        pool.getName(),
        pool.getType(),
        usage.getUsed() / 1024,
        usage.getMax() / 1024);
}
// 输出示例:
// Pool 'G1 Eden Space' (HEAP): used=12288KB, max=-1KB
// Pool 'G1 Old Gen' (HEAP): used=8192KB, max=262144KB
// Pool 'Metaspace' (NON_HEAP): used=32768KB, max=-1KB
```

### 6.5 注册自定义 MXBean

```java
// 定义 MXBean 接口
@MXBean
public interface AppStatusMXBean {
    int getActiveConnections();
    long getRequestCount();
    String getStatus();
    void resetCounters();
}

// 实现
public class AppStatus implements AppStatusMXBean {
    private final AtomicInteger connections = new AtomicInteger();
    private final AtomicLong requests = new AtomicLong();

    public int getActiveConnections() { return connections.get(); }
    public long getRequestCount() { return requests.get(); }
    public String getStatus() { return connections.get() > 100 ? "OVERLOADED" : "OK"; }
    public void resetCounters() { requests.set(0); }
}

// 注册
MBeanServer mbs = ManagementFactory.getPlatformMBeanServer();
ObjectName name = new ObjectName("com.example:type=AppStatus");
mbs.registerMBean(new AppStatus(), name);
```

### 6.6 内存阈值通知 (Memory Threshold Notification)

```java
MemoryMXBean memory = ManagementFactory.getMemoryMXBean();
NotificationEmitter emitter = (NotificationEmitter) memory;

emitter.addNotificationListener((notification, handback) -> {
    if (MemoryNotificationInfo.MEMORY_THRESHOLD_EXCEEDED
            .equals(notification.getType())) {
        CompositeData cd = (CompositeData) notification.getUserData();
        MemoryNotificationInfo info = MemoryNotificationInfo.from(cd);
        System.out.printf("内存阈值警告! 池: %s, 使用: %d bytes%n",
            info.getPoolName(), info.getUsage().getUsed());
    }
}, null, null);

// 设置内存池使用阈值 (90%)
for (MemoryPoolMXBean pool : ManagementFactory.getMemoryPoolMXBeans()) {
    if (pool.isUsageThresholdSupported() && pool.getType() == MemoryType.HEAP) {
        long max = pool.getUsage().getMax();
        if (max > 0) {
            pool.setUsageThreshold((long) (max * 0.9));
        }
    }
}
```

### 6.7 查询 MBean

```java
MBeanServer mbs = ManagementFactory.getPlatformMBeanServer();

// 查询所有 GC MBean
Set<ObjectName> gcNames = mbs.queryNames(
    new ObjectName("java.lang:type=GarbageCollector,*"), null);

// 查询所有内存池
Set<ObjectName> poolNames = mbs.queryNames(
    new ObjectName("java.lang:type=MemoryPool,*"), null);

// 查询自定义域的所有 MBean
Set<ObjectName> appBeans = mbs.queryNames(
    new ObjectName("com.example:*"), null);
```

---

## 7. 相关模块 (Related Modules)

| 模块 | 说明 |
|---|---|
| `java.management.rmi` | JMX RMI 连接器 (远程连接) |
| `jdk.management` | 扩展 MXBean (HotSpotDiagnosticMXBean, com.sun.management) |
| `jdk.management.agent` | JMX Agent (远程管理代理) |
| `jdk.management.jfr` | JFR 管理 MXBean |
| `jdk.jconsole` | JConsole 监控工具 |

---

## 8. MXBean vs Standard MBean 最佳实践

| 考虑因素 | MXBean | Standard MBean |
|---|---|---|
| 远程兼容性 | 开放类型自动映射，客户端无需类路径 | 需要客户端持有接口类 |
| 复杂类型支持 | CompositeData/TabularData 自动转换 | 需要序列化 |
| 推荐使用 | **新代码首选** | 遗留兼容 |
| 注解方式 | `@MXBean` | 接口名以 `MBean` 结尾 |

**命名规范**:

```
domain:type=Type,name=Name
com.example.web:type=ConnectionPool,name=primary
com.example.cache:type=Cache,name=userCache
```

---

## 9. 相关链接 (References)

- [JMX Technology Overview](https://docs.oracle.com/en/java/javase/21/jmx/introduction-jmx-technology.html)
- [Monitoring and Management Guide](https://docs.oracle.com/en/java/javase/21/management/)
- [源码 javax.management](https://github.com/openjdk/jdk/tree/master/src/java.management/share/classes/javax/management)
- [源码 java.lang.management](https://github.com/openjdk/jdk/tree/master/src/java.management/share/classes/java/lang/management)
- 本地源码: `src/java.management/share/classes/`
