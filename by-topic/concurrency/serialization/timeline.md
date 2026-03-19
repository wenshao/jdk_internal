# 序列化演进时间线

Java 序列化从 JDK 1.0 到 JDK 26 的完整演进历程。

---

## 时间线概览

```
JDK 1.0 ──── JDK 5 ──── JDK 6 ──── JDK 7 ──── JDK 8 ──── JDK 17 ──── JDK 26
 │             │           │           │           │           │           │
Java          枚举         XStream     Externalizable   Record     封存     自定义序列化
Serializable  序列化       库         配置         序列化     序列化
```

---

## JDK 1.0 - Java Serializable

### 基础序列化

```java
import java.io.*;

// 实现 Serializable
public class Person implements Serializable {
    private static final long serialVersionUID = 1L;

    private String name;
    private int age;
    private transient String password;  // 不序列化

    public Person(String name, int age, String password) {
        this.name = name;
        this.age = age;
        this.password = password;
    }

    // getters and setters...
}
```

### 序列化操作

```java
// 序列化
Person person = new Person("Alice", 25, "secret");

try (ObjectOutputStream oos = new ObjectOutputStream(
        new FileOutputStream("person.ser"))) {
    oos.writeObject(person);
}

// 反序列化
try (ObjectInputStream ois = new ObjectInputStream(
        new FileInputStream("person.ser"))) {
    Person deserialized = (Person) ois.readObject();
}
```

### serialVersionUID

```java
// serialVersionUID 作用
// - 版本控制
// - 兼容性检查

// 生成
private static final long serialVersionUID = 123456789L;

// 自动生成 (不推荐)
// serialver -classpath . com.example.Person
```

---

## JDK 5 - 枚举序列化

### Enum 序列化

```java
// 枚举序列化
public enum Status {
    PENDING, APPROVED, REJECTED;

    // 枚举默认可序列化
}

// 序列化
ObjectOutputStream oos = new ObjectOutputStream(...);
oos.writeObject(Status.PENDING);

// 反序列化
Status status = (Status) ois.readObject();
```

---

## JDK 7 - Externalizable

### Externalizable

```java
import java.io.*;

// Externalizable - 自定义序列化
public class Person implements Externalizable {
    private String name;
    private int age;

    public Person() {}  // 必须有无参构造器

    @Override
    public void writeExternal(ObjectOutput out) throws IOException {
        out.writeObject(name);
        out.writeInt(age);
    }

    @Override
    public void readExternal(ObjectInput in) throws IOException, ClassNotFoundException {
        name = (String) in.readObject();
        age = in.readInt();
    }
}
```

### 序列化代理

```java
// 序列化代理
public class Person implements Serializable {
    private static final long serialVersionUID = 1L;

    private String name;

    private Object writeReplace() {
        // 替换序列化对象
        return new PersonProxy(this);
    }

    private static class PersonProxy implements Serializable {
        private Person person;

        public PersonProxy(Person person) {
            this.person = person;
        }

        private Object readResolve() {
            // 恢复原始对象
            return person;
        }
    }
}
```

---

## JDK 8 - Record 序列化

### Record 序列化

```java
// Record 自动实现 Serializable
public record Person(String name, int age)
    implements Serializable {
    // 所有字段自动序列化
}

// 序列化
Person person = new Person("Alice", 25);

try (ObjectOutputStream oos = new ObjectOutputStream(
        new FileOutputStream("person.ser"))) {
    oos.writeObject(person);
}

// 反序列化
Person deserialized = (Person) ois.readObject();
```

---

## 第三方库

### JSON 序列化

```java
// Jackson
ObjectMapper mapper = new ObjectMapper();

// 序列化
String json = mapper.writeValueAsString(person);

// 反序列化
Person person = mapper.readValue(json, Person.class);
```

### XML 序列化

```java
// JAXB
// 定义
@XmlRootElement
@XmlType(propOrder = {"name", "age"})
public class Person {
    private String name;
    private int age;
    // getters and setters
}

// 序列化
JAXBContext jaxbContext = JAXBContext.newInstance(Person.class);
Marshaller marshaller = jaxbContext.createMarshaller();
marshaller.marshal(person, new File("person.xml"));

// 反序列化
Unmarshaller unmarshaller = jaxbContext.createUnmarshaller();
Person person = unmarshaller.unmarshal(new File("person.xml"));
```

---

## 安全性

### 反序列化漏洞

```java
// 危险代码
try (ObjectInputStream ois = new ObjectInputStream(
        new FileInputStream("untrusted.ser"))) {
    Object obj = ois.readObject();  // 可能执行任意代码
}

// 防御
// 1. 使用白名单
ObjectInputFilter filter = ObjectInputFilter.Config.createFilter(
    "com.example.Person;!*",
    ObjectInputFilter.Status.REJECTED);
ois.setObjectInputFilter(filter);

// 2. 使用安全的序列化框架
// - Jackson @JsonTypeInfo
// - Gson
```

---

## 最佳实践

### serialVersionUID

```java
// ✅ 推荐: 始终声明
private static final long serialVersionUID = 1L;

// ❌ 避免: 不声明 (编译器自动生成)
// 可能导致版本不一致
```

### transient

```java
// ✅ 推荐: 敏感信息使用 transient
private transient String password;
private transient Connection connection;

// ❌ 避免: 序列化不必要的字段
// - 大集合
// - 上下文对象
// - 线程
```

---

## 时间线总结

| 版本 | 特性 | 说明 |
|------|------|------|
| JDK 1.0 | Serializable | 基础序列化 |
| JDK 5 | Enum 序列化 | 枚举支持 |
| JDK 6 | SerialVersionUID 工具 | 生成 UID |
| JDK 7 | Externalizable 增强 | 自定义序列化 |
| JDK 17 | 密封序列化 | 序列化检查 |
| JDK 21+ | Record 序列化 | 简化序列化 |

---

## 相关链接

- [Serializable](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/io/Serializable.html)
- [ObjectInputFilter](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/io/ObjectInputFilter.html)
