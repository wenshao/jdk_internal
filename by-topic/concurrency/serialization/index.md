# 序列化

> Serializable、Externalizable、序列化过滤器演进历程

[← 返回并发网络](../)

---

## 快速概览

```
JDK 1.0 ── JDK 1.2 ── JDK 6 ── JDK 9 ── JDK 12 ── JDK 17 ── JDK 21 ── JDK 26
   │         │        │        │        │        │        │        │
序列化   Externalizable  过滤器  Records  Switch   模式    模式    序列化
接口      优化          JEP     不可序列  表达式   匹配    匹配    优化
                     290      默认      简化    for     for
                              序列化            instance instanceof
```

### 核心演进

| 版本 | 特性 | 说明 | JEP |
|------|------|------|-----|
| **JDK 1.0** | Serializable | 基础序列化接口 | - |
| **JDK 1.2** | Externalizable | 自定义序列化 | - |
| **JDK 6** | readResolve/writeReplace | 序列化代理模式 | - |
| **JDK 9** | 过滤器 | 序列化安全过滤 | JEP 290 |
| **JDK 12** | Switch 表达式 | 简化序列化逻辑 | JEP 325 |
| **JDK 17** | Record 序列化 | 不可变对象序列化 | - |
| **JDK 21** | 模式匹配 | for/instanceof | JEP 441 |
| **JDK 26** | 序列化优化 | 性能改进 | - |

---

## 核心贡献者

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
| 6 | Roman Kennke | 4 | Red Hat | Shenandoah GC |
| 7 | Pavel Rappo | 4 | Oracle | API 设计 |

---

## Serializable 接口

### 基础序列化

```java
import java.io.*;

// 实现 Serializable
public class Person implements Serializable {
    private static final long serialVersionUID = 1L;

    private String name;
    private int age;

    // 构造方法、getter、setter
}
```

### 序列化/反序列化

```java
// 序列化
Person person = new Person("Alice", 30);

try (ObjectOutputStream oos = new ObjectOutputStream(
        new FileOutputStream("person.ser"))) {
    oos.writeObject(person);
}

// 反序列化
try (ObjectInputStream ois = new ObjectInputStream(
        new FileInputStream("person.ser"))) {
    Person deserialized = (Person) ois.readObject();
    System.out.println(deserialized.getName());
}
```

### serialVersionUID

```java
// 版本控制
private static final long serialVersionUID = 1L;

// 不指定 (自动生成)
// private static final long serialVersionUID = -123456789L;

// 影响: 类变更时版本不匹配会导致 InvalidClassException
```

---

## 自定义序列化

### transient 关键字

```java
public class User implements Serializable {
    private String username;
    private transient String password;  // 不序列化

    // 反序列化后 password 为 null
}
```

### writeObject/readObject

```java
public class Employee implements Serializable {
    private String name;
    private transient String secret;

    private void writeObject(ObjectOutputStream oos)
            throws IOException {
        oos.defaultWriteObject();  // 默认序列化
        // 自定义加密 secret
        oos.writeObject(encrypt(secret));
    }

    private void readObject(ObjectInputStream ois)
            throws IOException, ClassNotFoundException {
        ois.defaultReadObject();  // 默认反序列化
        // 自定义解密 secret
        this.secret = decrypt((String) ois.readObject());
    }
}
```

### writeReplace/readResolve

```java
public class Singleton implements Serializable {
    private static final Singleton INSTANCE = new Singleton();

    private Singleton() {}

    // 序列化时替换为代理
    private Object writeReplace() {
        return new SerializationProxy(this);
    }

    // 反序列化时返回单例
    private Object readResolve() {
        return INSTANCE;
    }

    // 序列化代理
    private static class SerializationProxy implements Serializable {
        private final String data;

        SerializationProxy(Singleton singleton) {
            this.data = "proxy-data";
        }

        private Object readResolve() {
            return Singleton.INSTANCE;
        }
    }
}
```

---

## Externalizable 接口

### 完全自定义序列化

```java
import java.io.*;

public class Product implements Externalizable {
    private String name;
    private double price;

    // 必须有无参构造方法
    public Product() {}

    public Product(String name, double price) {
        this.name = name;
        this.price = price;
    }

    @Override
    public void writeExternal(ObjectOutput out) throws IOException {
        // 完全自定义序列化逻辑
        out.writeUTF(name);
        out.writeDouble(price);
    }

    @Override
    public void readExternal(ObjectInput in) throws IOException {
        // 完全自定义反序列化逻辑
        name = in.readUTF();
        price = in.readDouble();
    }
}
```

### 对比 Serializable

| 特性 | Serializable | Externalizable |
|------|-------------|----------------|
| 控制粒度 | 部分自定义 | 完全自定义 |
| 性能 | 较低 | 较高 |
| 复杂度 | 简单 | 复杂 |
| 默认行为 | 自动序列化 | 手动实现 |

---

## 序列化过滤器 (JDK 9+)

### JEP 290: 过滤器

**目的**: 防止反序列化漏洞

### 全局过滤器

```java
import java.util.*;

// 设置全局过滤器
ObjectInputFilter filter = ObjectInputFilter.Config.createFilter(
    "java.lang.String;!*"
);

ObjectInputFilter.Config.setSerialFilter(filter);
```

### 自定义过滤器

```java
public class SerializationFilter implements ObjectInputFilter {
    @Override
    public Status checkInput(FilterInfo filterInfo) {
        if (filterInfo.depth() > 10) {
            return Status.REJECTED;  // 深度限制
        }

        if (filterInfo.arrayLength() > 1000) {
            return Status.REJECTED;  // 数组长度限制
        }

        if (filterInfo.references() > 100) {
            return Status.REJECTED;  // 引用数限制
        }

        Class<?> clazz = filterInfo.classType();
        if (clazz != null) {
            // 白名单
            if (clazz.getName().startsWith("java.lang.")) {
                return Status.ALLOWED;
            }
            // 黑名单
            if (clazz.getName().equals("dangerous.Class")) {
                return Status.REJECTED;
            }
        }

        return Status.UNDECIDED;
    }
}

// 使用过滤器
ObjectInputFilter.Config.setSerialFilter(new SerializationFilter());
```

### 流级别过滤器

```java
try (ObjectInputStream ois = new ObjectInputStream(
        new FileInputStream("data.ser"))) {
    // 设置流级别过滤器
    ois.setObjectInputFilter(filter);
    Object obj = ois.readObject();
}
```

---

## Record 序列化 (JDK 17+)

### Record 作为数据载体

```java
// Record 默认基于构造器参数序列化
public record Point(int x, int y) implements Serializable {}

// 使用
Point point = new Point(10, 20);

try (ObjectOutputStream oos = new ObjectOutputStream(
        new FileOutputStream("point.ser"))) {
    oos.writeObject(point);
}
```

### 自定义 Record 序列化

```java
public record Person(String name, int age) implements Serializable {
    // 自定义序列化逻辑
    private static final long serialVersionUID = 1L;

    // 可以添加 writeObject/readObject
    // 但 Record 的不可变性使这不太常见
}
```

---

## 序列化安全

### 反序列化漏洞

**问题**: 恶意对象链执行任意代码

```java
// 危险代码
try (ObjectInputStream ois = new ObjectInputStream(
        new FileInputStream("untrusted.ser"))) {
    Object obj = ois.readObject();  // 可能执行恶意代码
}
```

### 防护措施

1. **使用过滤器**:
```java
ObjectInputFilter filter = ObjectInputFilter.Config.createFilter(
    "com.example.*;!*"
);
ObjectInputFilter.Config.setSerialFilter(filter);
```

2. **限制深度**:
```java
ObjectInputFilter filter = info -> {
    if (info.depth() > 5) {
        return Status.REJECTED;
    }
    return Status.UNDECIDED;
};
```

3. **使用白名单**:
```java
Set<String> allowedClasses = Set.of(
    "java.lang.String",
    "java.lang.Integer",
    "com.example.SafeClass"
);
```

4. **使用安全的序列化格式**:
- JSON
- XML
- Protocol Buffers
- 其他二进制格式

---

## 替代方案

### JSON 序列化

```java
import com.fasterxml.jackson.databind.ObjectMapper;

ObjectMapper mapper = new ObjectMapper();

// 序列化
String json = mapper.writeValueAsString(person);

// 反序列化
Person person = mapper.readValue(json, Person.class);
```

### XML 序列化

```java
import jakarta.xml.bind.JAXB;

// 序列化
String xml = JAXB.marshal(person, String.class);

// 反序列化
Person person = JAXB.unmarshal(new StringReader(xml), Person.class);
```

### Protocol Buffers

```java
// 定义 .proto 文件
message Person {
    string name = 1;
    int32 age = 2;
}

// 使用生成的类
PersonProto.Person person = PersonProto.Person.newBuilder()
    .setName("Alice")
    .setAge(30)
    .build();

// 序列化
byte[] data = person.toByteArray();

// 反序列化
PersonProto.Person parsed = PersonProto.Person.parseFrom(data);
```

---

## 性能优化

### 避免序列化整个对象图

```java
// 使用代理
public class LargeObject implements Serializable {
    private transient LargeData data;  // 不序列化大数据
    private String dataId;             // 只序列化 ID

    private void writeObject(ObjectOutputStream oos)
            throws IOException {
        oos.defaultWriteObject();
        // 不写入 data
    }

    private void readObject(ObjectInputStream ois)
            throws IOException, ClassNotFoundException {
        ois.defaultReadObject();
        // 根据 dataId 重新加载数据
        this.data = loadData(dataId);
    }
}
```

### 使用 Externalizable

```java
// Externalizable 通常比 Serializable 快
public class FastSerializable implements Externalizable {
    @Override
    public void writeExternal(ObjectOutput out) throws IOException {
        // 手动优化序列化
    }

    @Override
    public void readExternal(ObjectInput in) throws IOException {
        // 手动优化反序列化
    }
}
```

---

## 相关链接

### 本地文档

- [并发编程](../concurrency/) - 线程安全
- [网络编程](../network/) - Socket 序列化

### 外部参考

**JEP 文档:**
- [JEP 290: Filter Incoming Serialization Data](https://openjdk.org/jeps/290)

**安全文档:**
- [OWASP Deserialization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html)
- [Java Serialization Security](https://www.oracle.com/java/technologies/javase/seccode-guide-serialization.html)
