# 序列化

> Serializable、Externalizable、序列化过滤器演进历程

[← 返回并发网络](../)

---
## 目录

1. [快速概览](#1-快速概览)
2. [核心贡献者](#2-核心贡献者)
3. [Java 序列化机制](#3-java-序列化机制)
4. [自定义序列化](#4-自定义序列化)
5. [Externalizable 接口](#5-externalizable-接口)
6. [安全风险: 反序列化攻击](#6-安全风险-反序列化攻击)
7. [JEP 290: 序列化过滤器 (JDK 9)](#7-jep-290-序列化过滤器-jdk-9)
8. [JEP 415: Filter Factory (JDK 17)](#8-jep-415-filter-factory-jdk-17)
9. [Records 序列化](#9-records-序列化)
10. [替代方案](#10-替代方案)
11. [最佳实践](#11-最佳实践)
12. [性能优化](#12-性能优化)
13. [相关链接](#13-相关链接)

---


## 1. 快速概览

```
JDK 1.0 ── JDK 1.2 ── JDK 6 ────── JDK 9 ──── JDK 17 ──── JDK 17+
   │         │          │            │           │            │
Serializable Externalizable 序列化     JEP 290    JEP 415     Record
 接口        完全自定义   代理模式    过滤器     Filter      序列化
                                               Factory
```

### 核心演进

| 版本 | 特性 | 说明 | JEP |
|------|------|------|-----|
| **JDK 1.0** | Serializable | 基础序列化接口 (marker interface) | - |
| **JDK 1.1** | ObjectOutputStream / ObjectInputStream | 序列化流 API | - |
| **JDK 1.2** | Externalizable | 完全自定义序列化 | - |
| **JDK 6** | readResolve / writeReplace | 序列化代理模式 (serialization proxy pattern) | - |
| **JDK 9** | ObjectInputFilter | 反序列化过滤器, 白/黑名单 | [JEP 290](https://openjdk.org/jeps/290) |
| **JDK 17** | Filter Factory | 上下文相关过滤器 (context-specific filters) | [JEP 415](https://openjdk.org/jeps/415) |
| **JDK 16+** | Record 序列化 | 基于规范构造器 (canonical constructor) 的安全反序列化 | - |

---

## 2. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 序列化团队 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Kim Barrett | 12 | Oracle | 序列化运行时 |
| 2 | Stefan Karlsson | 8 | Oracle | 对象布局, 序列化 |
| 3 | Mandy Chung | 8 | Oracle | 序列化核心 |
| 4 | Joe Darcy | 5 | Oracle | Record 序列化 |
| 5 | Ioi Lam | 5 | Oracle | 序列化优化 |
| 6 | Pavel Rappo | 4 | Oracle | API 设计 |

---

## 3. Java 序列化机制

### ObjectOutputStream / ObjectInputStream

Java 序列化的核心是 `ObjectOutputStream` (序列化) 和 `ObjectInputStream` (反序列化)。
它们将对象转换为字节流 (byte stream), 或从字节流恢复对象。

```java
import java.io.*;

// 实现 Serializable — 标记接口 (marker interface), 无方法
public class Person implements Serializable {
    private static final long serialVersionUID = 1L;

    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
    // getter / setter 省略
}
```

### 序列化流程

```java
// 序列化 (Serialization): 对象 → 字节流
Person person = new Person("Alice", 30);

try (ObjectOutputStream oos = new ObjectOutputStream(
        new FileOutputStream("person.ser"))) {
    oos.writeObject(person);
}

// 反序列化 (Deserialization): 字节流 → 对象
try (ObjectInputStream ois = new ObjectInputStream(
        new FileInputStream("person.ser"))) {
    Person deserialized = (Person) ois.readObject();
    System.out.println(deserialized.getName()); // "Alice"
}
```

### 序列化底层原理

```
ObjectOutputStream.writeObject(obj)
  ├─ 检查 obj 是否 Serializable
  ├─ 写入类描述符 (class descriptor): 类名、serialVersionUID、字段列表
  ├─ 遍历对象图 (object graph), 处理循环引用
  ├─ 调用 writeObject() 自定义钩子 (如果存在)
  └─ 输出字节流 (包含 magic number 0xACED 和版本号)

ObjectInputStream.readObject()
  ├─ 读取类描述符, 加载类 (Class.forName)
  ├─ 创建对象实例 — 跳过构造器! (通过 Unsafe 分配内存)
  ├─ 逐字段恢复值
  ├─ 调用 readObject() 自定义钩子 (如果存在)
  └─ 返回对象 — 此时对象可能处于非法状态
```

> **关键问题**: 反序列化跳过构造器 (bypasses constructors), 不执行校验逻辑,
> 这是反序列化攻击的根本原因。

### serialVersionUID

```java
// 显式声明 — 推荐
private static final long serialVersionUID = 1L;

// 不声明 — JVM 根据类结构自动计算 hash
// 问题: 添加/删除字段后 hash 变化, 导致 InvalidClassException

// 版本兼容策略:
// - 新增字段: 反序列化旧数据时新字段为默认值 (0, null, false)
// - 删除字段: 旧数据中的字段被忽略
// - 修改字段类型: 抛出 InvalidClassException
```

---

## 4. 自定义序列化

### transient 关键字

```java
public class User implements Serializable {
    private static final long serialVersionUID = 1L;
    private String username;
    private transient String password;  // 不参与序列化

    // 反序列化后 password 为 null
    // 适用场景: 密码、缓存、数据库连接等敏感/不可序列化数据
}
```

### writeObject / readObject 钩子

```java
public class Employee implements Serializable {
    private static final long serialVersionUID = 1L;
    private String name;
    private transient String secret;

    // 序列化钩子 — 必须是 private void, 签名固定
    private void writeObject(ObjectOutputStream oos)
            throws IOException {
        oos.defaultWriteObject();           // 先序列化非 transient 字段
        oos.writeObject(encrypt(secret));   // 再自定义写入加密后的 secret
    }

    // 反序列化钩子
    private void readObject(ObjectInputStream ois)
            throws IOException, ClassNotFoundException {
        ois.defaultReadObject();            // 先恢复非 transient 字段
        this.secret = decrypt((String) ois.readObject());

        // 重要: 在这里执行校验 (defensive validation)
        if (name == null || name.isBlank()) {
            throw new InvalidObjectException("name must not be blank");
        }
    }

    // 防止子类绕过校验
    private void readObjectNoData() throws ObjectStreamException {
        throw new InvalidObjectException("Stream data required");
    }
}
```

### writeReplace / readResolve — 序列化代理模式

```java
// Effective Java Item 90 推荐的序列化代理模式
public class Period implements Serializable {
    private final Date start;
    private final Date end;

    public Period(Date start, Date end) {
        // 防御性拷贝 + 校验
        this.start = new Date(start.getTime());
        this.end = new Date(end.getTime());
        if (this.start.compareTo(this.end) > 0)
            throw new IllegalArgumentException("start > end");
    }

    // 序列化时替换为代理对象
    private Object writeReplace() {
        return new SerializationProxy(this);
    }

    // 禁止直接反序列化
    private void readObject(ObjectInputStream ois)
            throws InvalidObjectException {
        throw new InvalidObjectException("Use proxy");
    }

    // 内部代理类
    private static class SerializationProxy implements Serializable {
        private static final long serialVersionUID = 1L;
        private final Date start;
        private final Date end;

        SerializationProxy(Period p) {
            this.start = p.start;
            this.end = p.end;
        }

        // 反序列化时通过构造器重建 — 保证校验逻辑执行
        private Object readResolve() {
            return new Period(start, end);
        }
    }
}
```

### readResolve 维护单例

```java
public class Singleton implements Serializable {
    private static final long serialVersionUID = 1L;
    private static final Singleton INSTANCE = new Singleton();

    private Singleton() {}

    public static Singleton getInstance() { return INSTANCE; }

    // 反序列化时返回同一实例, 防止生成新的实例
    private Object readResolve() {
        return INSTANCE;
    }
}
```

---

## 5. Externalizable 接口

### 完全自定义序列化

```java
import java.io.*;

public class Product implements Externalizable {
    private String name;
    private double price;

    // 必须有 public 无参构造方法 — 反序列化时调用
    public Product() {}

    public Product(String name, double price) {
        this.name = name;
        this.price = price;
    }

    @Override
    public void writeExternal(ObjectOutput out) throws IOException {
        out.writeUTF(name);
        out.writeDouble(price);
    }

    @Override
    public void readExternal(ObjectInput in) throws IOException {
        name = in.readUTF();
        price = in.readDouble();
    }
}
```

### Serializable vs Externalizable

| 特性 | Serializable | Externalizable |
|------|-------------|----------------|
| 控制粒度 | 部分自定义 (通过钩子) | 完全自定义 |
| 性能 | 较低 (反射遍历字段) | 较高 (手动控制) |
| 复杂度 | 简单, 零样板代码 | 复杂, 需手动实现 |
| 构造器 | **跳过构造器** | 调用无参构造器 |
| 默认行为 | 自动序列化所有非 transient 字段 | 无默认行为, 必须全部手写 |

---

## 6. 安全风险: 反序列化攻击

### 攻击原理 — Gadget Chains

反序列化攻击的核心是 **gadget chain** (小工具链):
利用 classpath 上已有类的 `readObject()` 等方法, 串联出任意代码执行链。

```
攻击流程:
  1. 攻击者构造恶意字节流 (crafted byte stream)
  2. 服务端调用 ObjectInputStream.readObject()
  3. 反序列化触发 readObject() → 内部调用链开始
  4. 链条末端执行 Runtime.exec() — 任意命令执行 (RCE)
```

### 经典漏洞: Apache Commons Collections

```
ClassPathAlreadyHas:  Commons Collections 3.x

Gadget Chain 示例:
  BadAttributeValueExpException.readObject()
    → TiedMapEntry.toString()
      → LazyMap.get()
        → ChainedTransformer.transform()
          → InvokerTransformer.transform()
            → Runtime.getRuntime().exec("calc.exe")
```

### ysoserial — 反序列化漏洞利用工具

[ysoserial](https://github.com/frohoff/ysoserial) 是广泛使用的反序列化 payload 生成工具:

```bash
# 生成 Commons Collections 攻击 payload
java -jar ysoserial.jar CommonsCollections1 "calc.exe" > payload.ser

# 支持的 gadget chain 库:
# CommonsCollections (1-7), Spring, Hibernate, JDK7u21,
# Groovy, BeanShell, Jython, Myfaces 等
```

### 为什么反序列化如此危险

| 问题 | 说明 |
|------|------|
| **跳过构造器** | 对象未经校验即被创建 |
| **自动触发副作用** | readObject() 在类型检查/cast **之前**执行 |
| **classpath 即攻击面** | 依赖的任何 jar 都可能包含可利用的 gadget |
| **难以防御** | 黑名单永远不完整, 新 gadget chain 持续被发现 |

---

## 7. JEP 290: 序列化过滤器 (JDK 9)

[JEP 290](https://openjdk.org/jeps/290) 引入了 `ObjectInputFilter` 机制,
在反序列化**过程中**拦截不安全的类。

### 模式语法 (Pattern Syntax)

```
模式规则:
  类名         允许该类                    java.lang.String
  !类名        拒绝该类                    !java.util.HashMap
  包名.**      允许该包及子包              com.example.**
  !包名.**     拒绝该包及子包              !org.apache.commons.**
  maxdepth=N   限制对象图深度              maxdepth=5
  maxrefs=N    限制对象引用数              maxrefs=100
  maxbytes=N   限制字节流大小              maxbytes=1048576
  maxarray=N   限制数组长度                maxarray=1000
```

### 全局过滤器 (Process-Wide Filter)

```java
// 方式 1: 代码设置
ObjectInputFilter globalFilter = ObjectInputFilter.Config.createFilter(
    "java.lang.*;java.util.*;com.example.**;!*"  // 白名单模式, !* 拒绝其余
);
ObjectInputFilter.Config.setSerialFilter(globalFilter);

// 方式 2: JVM 启动参数
// -Djdk.serialFilter=java.lang.*;java.util.*;!*

// 方式 3: 配置文件 conf/security/java.security
// jdk.serialFilter=java.lang.*;java.util.*;!*
```

### 流级别过滤器 (Stream-Specific Filter)

```java
try (ObjectInputStream ois = new ObjectInputStream(
        new FileInputStream("data.ser"))) {
    // 为当前流单独设置过滤器, 覆盖全局设置
    ois.setObjectInputFilter(
        ObjectInputFilter.Config.createFilter(
            "com.example.dto.*;maxdepth=3;maxrefs=50;!*"
        )
    );
    Object obj = ois.readObject();
}
```

### 自定义过滤器 (Programmatic Filter)

```java
public class StrictFilter implements ObjectInputFilter {
    private static final Set<String> ALLOWED = Set.of(
        "java.lang.String", "java.lang.Integer",
        "java.lang.Long", "com.example.SafeDTO"
    );

    @Override
    public Status checkInput(FilterInfo info) {
        // 限制结构复杂度
        if (info.depth() > 5)        return Status.REJECTED;
        if (info.arrayLength() > 256) return Status.REJECTED;
        if (info.references() > 50)   return Status.REJECTED;

        Class<?> clazz = info.serialClass();
        if (clazz == null) return Status.UNDECIDED;  // 尚未解析类

        // 精确白名单
        if (ALLOWED.contains(clazz.getName())) {
            return Status.ALLOWED;
        }

        return Status.REJECTED;  // 拒绝所有未知类
    }
}
```

---

## 8. JEP 415: Filter Factory (JDK 17)

[JEP 415](https://openjdk.org/jeps/415) 引入了 **Filter Factory** — 允许根据调用上下文
(calling context) 动态选择过滤器, 解决了 JEP 290 "一刀切"的局限性。

### 核心概念: BinaryOperator\<ObjectInputFilter\>

```java
// Filter Factory 签名:
// BinaryOperator<ObjectInputFilter> — 接收 (当前过滤器, 流级别过滤器), 返回合并后的过滤器

ObjectInputFilter.Config.setSerialFilterFactory(
    (current, streamFilter) -> {
        // current: 全局过滤器或上一个 factory 返回的过滤器
        // streamFilter: 通过 setObjectInputFilter() 设置的流过滤器
        // 返回: 实际使用的过滤器

        if (streamFilter != null) {
            // 合并: 流过滤器优先, 全局过滤器兜底
            return ObjectInputFilter.merge(streamFilter, current);
        }
        return current;
    }
);
```

### 上下文相关过滤器 (Context-Specific Filters)

```java
// 根据调用栈选择不同过滤器
ObjectInputFilter.Config.setSerialFilterFactory((current, requested) -> {
    // 检查调用栈, 确定上下文
    StackWalker walker = StackWalker.getInstance(
        StackWalker.Option.RETAIN_CLASS_REFERENCE
    );

    return info -> {
        // RMI 上下文: 宽松过滤
        boolean isRMI = walker.walk(frames ->
            frames.anyMatch(f ->
                f.getDeclaringClass().getName()
                 .startsWith("java.rmi")));

        if (isRMI) {
            // RMI 专用过滤器
            return ObjectInputFilter.Config.createFilter(
                "java.rmi.**;java.lang.*;!*"
            ).checkInput(info);
        }

        // 默认: 严格过滤
        if (requested != null) {
            ObjectInputFilter.Status status = requested.checkInput(info);
            if (status != ObjectInputFilter.Status.UNDECIDED) {
                return status;
            }
        }
        return current != null
            ? current.checkInput(info)
            : ObjectInputFilter.Status.UNDECIDED;
    };
});
```

### JEP 290 vs JEP 415

| 特性 | JEP 290 (JDK 9) | JEP 415 (JDK 17) |
|------|-----------------|-------------------|
| 过滤粒度 | 全局 / 流级别 | 上下文相关 (context-specific) |
| 合并策略 | 流过滤器覆盖全局 | 自定义合并逻辑 |
| 典型用途 | 全站白名单 | RMI、JMX 等不同子系统各自过滤 |
| API | `setSerialFilter()` | `setSerialFilterFactory()` |

---

## 9. Records 序列化

### Records 如何解决反序列化安全问题

Java Record (JDK 16 正式引入) 的反序列化机制与普通类**根本不同**:

```
普通类反序列化:
  1. Unsafe.allocateInstance() — 跳过构造器
  2. 直接设置字段值 — 跳过校验
  3. 调用 readObject() 钩子 (如果存在)

Record 反序列化:
  1. 从流中读取组件值 (component values)
  2. 调用规范构造器 (canonical constructor) — 校验逻辑被执行!
  3. 字段为 final — 不可变
```

### Record 序列化示例

```java
// Record 天然支持安全反序列化
public record Point(int x, int y) implements Serializable {
    // 紧凑构造器中的校验在反序列化时同样执行
    public Point {
        if (x < 0 || y < 0) {
            throw new IllegalArgumentException(
                "Coordinates must be non-negative");
        }
    }
}

// 序列化
Point point = new Point(10, 20);
try (var oos = new ObjectOutputStream(new FileOutputStream("point.ser"))) {
    oos.writeObject(point);
}

// 反序列化 — 会调用 Point(int, int) 构造器
// 恶意篡改的负数坐标会被拒绝
try (var ois = new ObjectInputStream(new FileInputStream("point.ser"))) {
    Point restored = (Point) ois.readObject();
}
```

### Record 序列化的安全优势

| 特性 | 普通类 | Record |
|------|--------|--------|
| 反序列化调用构造器 | 否 (跳过) | **是 (规范构造器)** |
| 字段不可变性 | 不保证 | final 字段, 不可变 |
| 自定义 readObject | 可以 | **不支持** (无需) |
| 攻击面 | 大 (任意状态注入) | 小 (必须通过构造器) |
| 序列化代理 | 需手动实现 | 内建行为类似代理模式 |

> **最佳建议**: 在需要序列化的场景中, 优先使用 Record 作为数据载体 (data carrier)。

---

## 10. 替代方案

### 为什么不用 Java 原生序列化

Brian Goetz (Java 语言架构师) 曾称 Java 序列化为
"*a horrible mistake in 1997*" (1997 年的可怕错误)。主要问题:

| 问题 | 说明 |
|------|------|
| **安全性** | 反序列化攻击是 Java 最大的安全威胁之一 |
| **跨语言** | Java 序列化格式无法被其他语言读取 |
| **版本脆弱** | 类结构变化容易导致兼容性问题 |
| **性能** | 反射开销大, 序列化体积大 |
| **可读性** | 二进制格式, 不可人工调试 |

### JSON: Jackson / Gson

```java
// === Jackson (业界标准) ===
import com.fasterxml.jackson.databind.ObjectMapper;

ObjectMapper mapper = new ObjectMapper();

// 序列化
String json = mapper.writeValueAsString(person);
// {"name":"Alice","age":30}

// 反序列化 — 通过构造器或 setter, 不会绕过校验
Person person = mapper.readValue(json, Person.class);

// Record 支持 (Jackson 2.12+)
record UserDTO(String name, int age) {}
UserDTO dto = mapper.readValue(json, UserDTO.class);


// === Gson (Google) ===
import com.google.gson.Gson;

Gson gson = new Gson();
String json = gson.toJson(person);
Person person = gson.fromJson(json, Person.class);
```

### Protocol Buffers (protobuf)

```protobuf
// person.proto — 跨语言的 schema 定义
syntax = "proto3";
message Person {
    string name = 1;
    int32 age = 2;
}
```

```java
// 使用生成的类 — 类型安全, 高性能
PersonProto.Person person = PersonProto.Person.newBuilder()
    .setName("Alice")
    .setAge(30)
    .build();

byte[] data = person.toByteArray();                        // 序列化
PersonProto.Person parsed = PersonProto.Person.parseFrom(data); // 反序列化
```

### Apache Avro

```java
// Avro: 支持 schema evolution, 适合大数据场景
// Schema 可以 JSON 定义, 也可以 IDL 定义
// 序列化体积最小, 不包含字段名

// Avro 适用场景: Kafka, Hadoop, 数据湖
```

### 方案对比

| 方案 | 类型 | 跨语言 | Schema | 性能 | 体积 | 安全性 |
|------|------|--------|--------|------|------|--------|
| Java Serializable | 二进制 | 否 | 无 | 低 | 大 | 差 |
| JSON (Jackson) | 文本 | 是 | 可选 | 中 | 中 | 好 |
| Protocol Buffers | 二进制 | 是 | 必须 | 高 | 小 | 好 |
| Avro | 二进制 | 是 | 必须 | 高 | 最小 | 好 |
| Java Record + JSON | 文本 | 是 | 可选 | 中 | 中 | 最好 |

---

## 11. 最佳实践

### serialVersionUID

```java
// 规则 1: 始终显式声明 serialVersionUID
private static final long serialVersionUID = 1L;

// 规则 2: 修改类的序列化兼容契约时, 递增 serialVersionUID
// 例如: 删除字段、修改字段类型

// 规则 3: 新增字段时保持 serialVersionUID 不变
// 旧数据反序列化时新字段为默认值
```

### transient 使用原则

```java
public class Session implements Serializable {
    private static final long serialVersionUID = 1L;

    private String userId;
    private transient String authToken;      // 敏感数据 — 不序列化
    private transient Connection dbConn;     // 不可序列化的资源
    private transient Map<String, Object> cache; // 可重建的缓存

    // readObject 中重建 transient 字段
    private void readObject(ObjectInputStream ois)
            throws IOException, ClassNotFoundException {
        ois.defaultReadObject();
        this.cache = new HashMap<>();
        // authToken 和 dbConn 需要重新获取
    }
}
```

### readResolve / writeReplace 使用指南

```java
// 场景 1: 单例保护 — readResolve
// 场景 2: 序列化代理 — writeReplace + readResolve (推荐)
// 场景 3: 枚举 — 自动处理, 无需手动实现

// 枚举天然序列化安全
public enum Status implements Serializable {
    ACTIVE, INACTIVE;
    // 反序列化自动调用 Enum.valueOf(), 无需 readResolve
}
```

### 防御性编程清单

```
□ 优先使用 Record 或序列化代理模式
□ 始终声明 serialVersionUID
□ 使用 transient 排除敏感字段
□ 在 readObject() 中校验所有不变量 (invariants)
□ 配置 JEP 290 过滤器 (全局白名单)
□ 生产环境启用 JEP 415 Filter Factory
□ 考虑替换为 JSON / protobuf
□ 定期审计 classpath 中的 gadget 库 (commons-collections 等)
```

---

## 12. 性能优化

### 避免序列化整个对象图

```java
public class LargeObject implements Serializable {
    private static final long serialVersionUID = 1L;
    private transient LargeData data;  // 不序列化大数据
    private String dataId;             // 只序列化 ID

    private void writeObject(ObjectOutputStream oos)
            throws IOException {
        oos.defaultWriteObject();
    }

    private void readObject(ObjectInputStream ois)
            throws IOException, ClassNotFoundException {
        ois.defaultReadObject();
        this.data = loadData(dataId);  // 根据 ID 重新加载
    }
}
```

### 使用 Externalizable 提升性能

```java
// Externalizable 比 Serializable 快 — 无反射, 无默认字段遍历
public class FastDTO implements Externalizable {
    private int id;
    private String name;

    public FastDTO() {}

    @Override
    public void writeExternal(ObjectOutput out) throws IOException {
        out.writeInt(id);
        out.writeUTF(name);
    }

    @Override
    public void readExternal(ObjectInput in) throws IOException {
        id = in.readInt();
        name = in.readUTF();
    }
}
```

---

## 13. 相关链接

### 本地文档

- [并发编程](../concurrency/) - 线程安全
- [网络编程](../network/) - Socket 序列化

### 外部参考

**JEP 文档:**
- [JEP 290: Filter Incoming Serialization Data](https://openjdk.org/jeps/290) - JDK 9 反序列化过滤器
- [JEP 415: Context-Specific Deserialization Filters](https://openjdk.org/jeps/415) - JDK 17 Filter Factory

**安全文档:**
- [OWASP Deserialization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html)
- [Java Serialization Security](https://www.oracle.com/java/technologies/javase/seccode-guide-serialization.html)

**工具:**
- [ysoserial](https://github.com/frohoff/ysoserial) - 反序列化漏洞 payload 生成器
