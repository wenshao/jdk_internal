# java.management 模块分析

> JMX (Java Management Extensions)，Java 监控和管理 API

---

## 1. 模块概述

`java.management` 提供了 JMX 核心功能，允许运行中的应用程序被监控和管理。它是 Java 应用性能监控、故障诊断的标准方式。

### 模块定义

**文件**: `src/java.management/share/classes/module-info.java`

```java
module java.management {
    exports javax.management;
    exports javax.management.loading;
    exports javax.management.modelmbean;
    exports javax.management.monitor;
    exports javax.management.openmbean;
    exports javax.management.relation;
    exports javax.management.remote;
    exports javax.management.timer;
}
```

### 架构

```
┌─────────────────────────────────────────────────────────┐
│                   管理客户端                              │
│  JConsole / VisualVM / 自定义客户端                       │
├─────────────────────────────────────────────────────────┤
│                 JMX Connector                            │
│  RMI / JMXMP 协议                                        │
├─────────────────────────────────────────────────────────┤
│                 MBeanServer                              │
│  (MBean 注册和访问中心)                                    │
├─────────────────────────────────────────────────────────┤
│                   MBean                                  │
│  Standard MBean / Dynamic MBean / MXBean / Model MBean   │
│  (被管理的资源)                                           │
└─────────────────────────────────────────────────────────┘
```

---

## 2. 核心类分析

### 2.1 MBeanServer

**源码**: `src/java.management/share/classes/javax/management/MBeanServer.java`

```java
public interface MBeanServer extends MBeanServerConnection {
    // 注册 MBean
    public ObjectInstance registerMBean(Object object, ObjectName name)

    // 注销 MBean
    public void unregisterMBean(ObjectName name)

    // 获取 MBean
    public Object getAttribute(ObjectName name, String attribute)
    public void setAttribute(ObjectName name, Attribute attribute)
    public Object invoke(ObjectName name, String operationName,
                        Object[] params, String[] signature)

    // 查询 MBean
    public Set<ObjectName> queryNames(ObjectName pattern, QueryExp query)
}
```

### 2.2 ObjectName

**源码**: `src/java.management/share/classes/javax/management/ObjectName.java`

```java
public class ObjectName implements Comparable<ObjectName> {
    // 创建 ObjectName
    public ObjectName(String name)

    // 格式: domain:key=value,key=value,...
    // 例如: com.example:type=Hello,name=World
}
```

**命名规范**:
```
domain:type=Type,name=Name
com.example.web:type=Servlet,name=LoginServlet
java.lang:type=Memory
```

### 2.3 MBean 类型

#### Standard MBean

```java
// 接口: XXXMBean
public interface HelloMBean {
    String getName();
    void setName(String name);
    String sayHello();
}

// 实现: XXX
public class Hello implements HelloMBean {
    private String name = "World";

    @Override
    public String getName() { return name; }

    @Override
    public void setName(String name) { this.name = name; }

    @Override
    public String sayHello() { return "Hello, " + name; }
}
```

#### MXBean (推荐)

```java
// 使用 @MXBean 注解或 MXBean 后缀
@MXBean
public interface MemoryMXBean {
    MemoryUsage getHeapMemoryUsage();
    MemoryUsage getNonHeapMemoryUsage();
    int getObjectPendingFinalizationCount();
    void gc();
}
```

#### Dynamic MBean

```java
public class DynamicExample implements DynamicMBean {
    private Map<String, Object> attributes = new HashMap<>();

    @Override
    public Object getAttribute(String attr) throws AttributeNotFoundException {
        if (!attributes.containsKey(attr))
            throw new AttributeNotFoundException(attr);
        return attributes.get(attr);
    }

    @Override
    public void setAttribute(Attribute attr) throws AttributeNotFoundException {
        attributes.put(attr.getName(), attr.getValue());
    }

    // ... 其他方法
}
```

---

## 3. JDK 26 内置 MBean

### 3.1 平台 MBean

| MBean | ObjectName | 用途 |
|-------|-----------|------|
| ClassLoadingMXBean | `java.lang:type=ClassLoading` | 类加载统计 |
| CompilationMXBean | `java.lang:type=Compilation` | JIT 编译统计 |
| MemoryMXBean | `java.lang:type=Memory` | 内存使用 |
| MemoryPoolMXBean | `java.lang:type=MemoryPool,name=*` | 内存池详情 |
| GarbageCollectorMXBean | `java.lang:type=GarbageCollector,name=*` | GC 统计 |
| ThreadMXBean | `java.lang:type=Threading` | 线程统计 |
| RuntimeMXBean | `java.lang:type=Runtime` | 运行时信息 |
| OperatingSystemMXBean | `java.lang:type=OperatingSystem` | 操作系统信息 |

### 3.2 使用示例

```java
// 获取 MBeanServer
MBeanServer mbs = ManagementFactory.getPlatformMBeanServer();

// 获取内存 MBean
MemoryMXBean memory = ManagementFactory.newPlatformMXBeanProxy(
    mbs,
    "java.lang:type=Memory",
    MemoryMXBean.class
);

// 获取堆内存使用
MemoryUsage heapUsage = memory.getHeapMemoryUsage();
System.out.println("Used: " + heapUsage.getUsed() / 1024 / 1024 + " MB");
System.out.println("Max: " + heapUsage.getMax() / 1024 / 1024 + " MB");

// 获取所有 GC MBean
List<GarbageCollectorMXBean> gcBeans = ManagementFactory.getGarbageCollectorMXBeans();
for (GarbageCollectorMXBean gc : gcBeans) {
    System.out.println(gc.getName() + ": " + gc.getCollectionCount() + " collections");
}

// 获取线程 MBean
ThreadMXBean thread = ManagementFactory.getThreadMXBean();
System.out.println("Thread count: " + thread.getThreadCount());
System.out.println("Peak thread count: " + thread.getPeakThreadCount());
```

---

## 4. JMX 连接

### 4.1 本地连接

```java
// JConsole / VisualVM 自动检测本地应用
// 或通过 Attach API 连接
import com.sun.management.AttachProvider;

List<VirtualMachineDescriptor> vms = AttachProvider.provider().listVirtualMachines();
for (VirtualMachineDescriptor vmd : vms) {
    VirtualMachine vm = VirtualMachine.attach(vmd);
    System.out.println("PID: " + vm.id() + ", Display: " + vmd.displayName());
    vm.detach();
}
```

### 4.2 远程连接

**启动应用时启用 JMX**:

```bash
# 无认证 (仅测试)
java -Dcom.sun.management.jmxremote.port=9010 \
     -Dcom.sun.management.jmxremote.authenticate=false \
     -Dcom.sun.management.jmxremote.ssl=false \
     -jar app.jar

# 带认证
java -Dcom.sun.management.jmxremote.port=9010 \
     -Dcom.sun.management.jmxremote.authenticate=true \
     -Dcom.sun.management.jmxremote.password.file=jmxremote.password \
     -Dcom.sun.management.jmxremote.access.file=jmxremote.access \
     -Dcom.sun.management.jmxremote.ssl=true \
     -jar app.jar
```

**客户端连接**:

```java
JMXServiceURL url = new JMXServiceURL(
    "service:jmx:rmi:///jndi/rmi://localhost:9010/jmxrmi"
);
JMXConnector connector = JMXConnectorFactory.connect(url);
MBeanServerConnection mbs = connector.getMBeanServerConnection();

// 使用 MBeanServerConnection
MemoryMXBean memory = ManagementFactory.newPlatformMXBeanProxy(
    mbs,
    "java.lang:type=Memory",
    MemoryMXBean.class
);
```

---

## 5. JDK 26 变更

### 5.1 虚拟线程监控

```java
ThreadMXBean thread = ManagementFactory.getThreadMXBean();

// JDK 21+ 新方法
if (thread instanceof com.sun.management.ThreadMXBean ext) {
    // 获取虚拟线程信息
    long[] threadIds = ext.getAllThreadIds();
    for (long tid : threadIds) {
        ThreadInfo info = ext.getThreadInfo(tid);
        if (info.isVirtual()) {
            System.out.println("Virtual thread: " + info.getThreadName());
        }
    }
}
```

### 5.2 新增 MBean

| MBean | JDK | 说明 |
|-------|-----|------|
| CpuTimeMXBean | 26+ | CPU 时间统计增强 |

### 5.3 性能改进

- 减少 JMX 通知的延迟
- 优化 MBean 查询性能

---

## 6. 使用示例

### 6.1 注册自定义 MBean

```java
public class Agent {
    public static void premain(String agentArgs, Instrumentation inst) {
        try {
            MBeanServer mbs = ManagementFactory.getPlatformMBeanServer();

            // 创建并注册 MBean
            ObjectName name = new ObjectName("com.example:type=Hello");
            Hello mbean = new Hello();
            mbs.registerMBean(mbean, name);

            System.out.println("Hello MBean registered...");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

### 6.2 监听 MBean 通知

```java
// 内存使用警告
NotificationListener listener = (notification, handback) -> {
    if (notification.getType().equals(MemoryNotificationInfo.MEMORY_THRESHOLD_EXCEEDED)) {
        MemoryNotificationInfo info = MemoryNotificationInfo.from((CompositeData) notification.getUserData());
        System.out.println("Memory threshold exceeded: " + info.getPoolName());
    }
};

MemoryMXBean memory = ManagementFactory.getMemoryMXBean();
NotificationEmitter emitter = (NotificationEmitter) memory;
emitter.addNotificationListener(listener, null, null);
```

### 6.3 查询 MBean

```java
MBeanServer mbs = ManagementFactory.getPlatformMBeanServer();

// 查询所有 GC MBean
Set<ObjectName> gcNames = mbs.queryNames(
    new ObjectName("java.lang:type=GarbageCollector,*"),
    null
);

// 查询特定条件的 MBean
QueryExp query = Query.eq("CollectionCount", Query.value(0));
Set<ObjectName> result = mbs.queryNames(null, query);
```

### 6.4 JMX MP (JMX Message Protocol)

```java
// JDK 26 改进的 JMX 远程连接
Map<String, Object> env = Map.of(
    "jmx.remote.x.client.connection.check.period", 60000,
    "jmx.remote.x.request.timeout", 5000
);

JMXConnector connector = JMXConnectorFactory.connect(url, env);
```

---

## 7. JMX 最佳实践

### 7.1 命名规范

```
domain:type=Type,name=Name
domain:type=Type,name=Name,category=Category
```

### 7.2 MXBean vs Standard MBean

| 特性 | MXBean | Standard MBean |
|------|--------|----------------|
| 类型映射 | 自动映射开放类型 | 直接使用 Java 类型 |
| 远程调用 | ✓ 友好 | 需要客户端类路径 |
| 推荐 | ✓ | ✗ |

### 7.3 性能考虑

```java
// 避免: 频繁调用 MBean
for (int i = 0; i < 1000000; i++) {
    mbs.getAttribute(name, "Count");  // 慢
}

// 推荐: 批量获取
mbs.getAttributes(name, new String[]{"Count", "Total"});
```

---

## 8. 相关链接

- [JMX 技术白皮书](https://www.oracle.com/java/technologies/javase/tech/jmx.html)
- [JMX 教程](https://docs.oracle.com/en/java/javase/26/management/jmx technology.html)
- [源码](https://github.com/openjdk/jdk/tree/master/src/java.management/share/classes/javax/management)
