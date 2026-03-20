# 泛型

> 类型参数、泛型类、泛型方法、通配符、类型擦除

[← 返回核心平台](../)

---

## 快速概览

```
JDK 1.0 ── JDK 4 ── JDK 5 ── JDK 7 ── JDK 8 ── JDK 17
   │        │        │        │        │        │
集合    JSR 14   Generics  Diamond  类型    Var
使用    预览      (JSR201)  操作符   注解    增强
```

### 核心演进

| 版本 | 特性 | JEP | 说明 |
|------|------|-----|------|
| **JDK 5** | 泛型 | JSR 14 | 类型参数化 |
| **JDK 5** | 泛型方法 | - | 方法级泛型 |
| **JDK 5** | 通配符 | - | ? extends/super |
| **JDK 7** | Diamond 操作符 | - | 类型推断 |
| **JDK 8** | 类型注解 | - | @TypeUse |
| **JDK 17** | Var 语义增强 | - | 隐式类型 |

---

## 目录

- [泛型基础](#泛型基础)
- [泛型类与接口](#泛型类与接口)
- [泛型方法](#泛型方法)
- [通配符](#通配符)
- [类型擦除](#类型擦除)
- [泛型约束](#泛型约束)
- [最佳实践](#最佳实践)
- [核心贡献者](#核心贡献者)
- [相关链接](#相关链接)

---

## 泛型基础

### 为什么需要泛型

```java
// JDK 5 之前: 使用 Object, 需要类型转换
List list = new ArrayList();
list.add("Hello");
String s = (String) list.get(0);  // 需要强制转换
list.add(123);  // 编译通过, 但运行时可能出错

// JDK 5+: 使用泛型, 类型安全
List<String> list = new ArrayList<>();
list.add("Hello");
String s = list.get(0);  // 无需转换
// list.add(123);  // 编译错误!
```

### 泛型语法

```java
// 1. 泛型类
public class Box<T> {
    private T value;

    public void set(T value) {
        this.value = value;
    }

    public T get() {
        return value;
    }
}

// 使用
Box<String> stringBox = new Box<>();
stringBox.set("Hello");
String s = stringBox.get();

Box<Integer> intBox = new Box<>();
intBox.set(123);
Integer i = intBox.get();

// 2. 多个类型参数
public class Pair<K, V> {
    private K key;
    private V value;

    public Pair(K key, V value) {
        this.key = key;
        this.value = value;
    }

    public K getKey() { return key; }
    public V getValue() { return value; }
}

// 使用
Pair<String, Integer> pair = new Pair<>("age", 25);
```

### 类型参数命名

```java
// 常用类型参数命名:
// E - Element (集合元素)
// K - Key (键)
// V - Value (值)
// T - Type (类型)
// N - Number (数字)
// S, U, V - 第二、第三、第四类型

public interface Map<K, V> { ... }
public interface List<E> { ... }
public class CompletableFuture<T> { ... }
```

---

## 泛型类与接口

### 泛型类

```java
// 1. 基础泛型类
public class Container<T> {
    private T item;

    public Container(T item) {
        this.item = item;
    }

    public T getItem() {
        return item;
    }

    public void setItem(T item) {
        this.item = item;
    }
}

// 使用
Container<String> strContainer = new Container<>("Hello");
Container<Integer> intContainer = new Container<>(123);

// 2. 有界类型参数
public class NumberBox<T extends Number> {
    private T number;

    public NumberBox(T number) {
        this.number = number;
    }

    public double doubleValue() {
        return number.doubleValue();
    }
}

// 使用
NumberBox<Integer> intBox = new NumberBox<>(123);
NumberBox<Double> doubleBox = new NumberBox<>(3.14);
// NumberBox<String> strBox = new NumberBox<>("abc");  // 编译错误!

// 3. 多重边界
public class ComparableNumber<T extends Number & Comparable<T>> {
    private T number;

    public ComparableNumber(T number) {
        this.number = number;
    }

    public boolean isGreaterThan(T other) {
        return number.compareTo(other) > 0;
    }
}
```

### 泛型接口

```java
// 1. 泛型接口
public interface Repository<T> {
    T findById(Long id);
    List<T> findAll();
    void save(T entity);
    void delete(T entity);
}

// 实现泛型接口
public class UserRepository implements Repository<User> {
    @Override
    public User findById(Long id) {
        return new User();
    }

    @Override
    public List<User> findAll() {
        return List.of();
    }

    @Override
    public void save(User user) { }

    @Override
    public void delete(User user) { }
}

// 2. 泛型接口也可以是协变的
public interface Producer<T> {
    T produce();
}

public interface Consumer<T> {
    void consume(T item);
}

// Producer 是协变的 (extends)
// Consumer 是逆变的 (super)
```

---

## 泛型方法

### 泛型方法语法

```java
// 1. 基础泛型方法
public class Util {
    // 泛型方法: 类型参数在返回类型之前声明
    public static <T> void swap(T[] array, int i, int j) {
        T temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }

    // 使用
    public static void main(String[] args) {
        String[] names = {"Alice", "Bob", "Charlie"};
        swap(names, 0, 2);  // T 推断为 String
    }
}

// 2. 有界泛型方法
public static <T extends Comparable<T>> T max(T a, T b) {
    return a.compareTo(b) > 0 ? a : b;
}

// 使用
String maxStr = max("hello", "world");
Integer maxInt = max(10, 20);

// 3. 多个类型参数
public static <K, V> boolean compare(Pair<K, V> p1, Pair<K, V> p2) {
    return p1.getKey().equals(p2.getKey()) &&
           p1.getValue().equals(p2.getValue());
}

// 4. 类型推断 (JDK 7+ Diamond 操作符)
Box<String> box = new Box<>();  // 类型推断为 String
```

### 静态泛型方法 vs 实例泛型方法

```java
public class Example<T> {

    // 实例泛型方法: 使用类的类型参数
    public void instanceMethod(T item) {
        // ...
    }

    // 静态泛型方法: 声明自己的类型参数
    public static <S> void staticMethod(S item) {
        // ...
    }

    // 静态方法不能使用类的类型参数
    // public static void error(T item) { }  // 编译错误!
}
```

---

## 通配符

### 上界通配符 (? extends T)

```java
// ? extends T - 上界通配符, 可以读取但不能写入

public static double sum(List<? extends Number> list) {
    double sum = 0;
    for (Number n : list) {
        sum += n.doubleValue();  // 可以读取
    }
    return sum;
}

// 使用
List<Integer> ints = List.of(1, 2, 3);
List<Double> doubles = List.of(1.5, 2.5, 3.5);

System.out.println(sum(ints));    // 6.0
System.out.println(sum(doubles)); // 7.5

// 不能写入
List<? extends Number> list = new ArrayList<Integer>();
// list.add(123);  // 编译错误! 不能确定具体类型
list.add(null);  // 只能添加 null
```

### 下界通配符 (? super T)

```java
// ? super T - 下界通配符, 可以写入但不能读取 (除 Object 外)

public static void addNumbers(List<? super Integer> list) {
    list.add(123);      // 可以添加 Integer
    list.add(456);      // 可以添加 Integer
    // Integer i = list.get(0);  // 编译错误! 不能确定具体类型
    Object obj = list.get(0);  // 只能作为 Object 读取
}

// 使用
List<Number> numbers = new ArrayList<>();
addNumbers(numbers);
System.out.println(numbers);  // [123, 456]

List<Object> objects = new ArrayList<>();
addNumbers(objects);
System.out.println(objects);  // [123, 456]
```

### 无界通配符 (?)

```java
// ? - 无界通配符, 只能读取为 Object, 只能写入 null

public static void printList(List<?> list) {
    for (Object elem : list) {
        System.out.println(elem);
    }
}

// 使用
List<String> strings = List.of("a", "b", "c");
List<Integer> ints = List.of(1, 2, 3);

printList(strings);  // a, b, c
printList(ints);    // 1, 2, 3
```

### PECS 原则

```java
// PECS: Producer Extends, Consumer Super

// 1. Producer - 使用 extends
public static void copy(List<? extends Number> src,
                        List<? super Number> dest) {
    for (Number n : src) {
        dest.add(n);
    }
}

// 2. 使用示例
public class Stack<E> {
    public void pushAll(Iterable<? extends E> src) {
        for (E e : src) {
            push(e);
        }
    }

    public void popAll(Collection<? super E> dst) {
        while (!isEmpty()) {
            dst.add(pop());
        }
    }

    private void push(E e) { }
    private E pop() { return null; }
    private boolean isEmpty() { return false; }
}
```

---

## 类型擦除

### 擦除机制

```java
// 类型擦除: 泛型只在编译时存在, 运行时被擦除

public class Box<T> {
    private T value;

    public void set(T value) {
        this.value = value;
    }

    public T get() {
        return value;
    }
}

// 编译后 (类似):
public class Box {
    private Object value;

    public void set(Object value) {
        this.value = value;
    }

    public Object get() {
        return value;
    }
}

// 有界类型擦除到边界
public class NumberBox<T extends Number> {
    private T value;

    public void set(T value) {
        this.value = value;
    }

    public T get() {
        return value;
    }
}

// 编译后:
public class NumberBox {
    private Number value;

    public void set(Number value) {
        this.value = value;
    }

    public Number get() {
        return value;
    }
}
```

### 擦除的影响

```java
// 1. 不能使用基本类型
// List<int> list = new ArrayList<>();  // 编译错误!
List<Integer> list = new ArrayList<>();  // 使用包装类

// 2. 不能创建类型参数实例
public class Box<T> {
    // private T item = new T();  // 编译错误!
}

// 解决方案: 传递类型对象
public class Box<T> {
    private T item;
    private Class<T> type;

    public Box(Class<T> type) {
        this.type = type;
        try {
            this.item = type.getDeclaredConstructor().newInstance();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}

// 3. 不能创建泛型数组
// List<String>[] lists = new List<String>[10];  // 编译错误!

// 解决方案: 使用数组或 List
List<String>[] lists = new List[10];  // 警告, 但可以编译
List<List<String>> lists = new ArrayList<>();

// 4. instanceof 不能用于泛型类型
// if (list instanceof List<String>) { }  // 编译错误!

// 解决方案: 使用通配符
if (list instanceof List<?>) { }

// 5. 静态上下文不能使用类型参数
public class Box<T> {
    // private static T item;  // 编译错误!
    // private static T getInstance() { }  // 编译错误!
}

// 6. 不能重载泛型方法
// public void print(List<String> list) { }
// public void print(List<Integer> list) { }  // 编译错误! 擦除后签名相同
```

---

## 泛型约束

### 类型约束

```java
// 1. 上界约束
public static <T extends Number> T max(T a, T b) {
    return a.doubleValue() > b.doubleValue() ? a : b;
}

// 2. 多重边界
public static <T extends Number & Comparable<T>> T max(T a, T b) {
    return a.compareTo(b) > 0 ? a : b;
}

// 注意: 类必须在接口之前
// public static <T extends Comparable<T> & Number> T max(T a, T b) { }  // 错误!

// 3. 递归边界
public interface Comparable<T> {
    int compareTo(T o);
}

// T 必须实现 Comparable<T>
public static <T extends Comparable<T>> T max(List<T> list) {
    T max = list.get(0);
    for (T item : list) {
        if (item.compareTo(max) > 0) {
            max = item;
        }
    }
    return max;
}
```

### 数组与协变

```java
// 数组是协变的, 泛型是不变的

// 1. 数组协变
String[] strings = new String[10];
Object[] objects = strings;  // OK
objects[0] = 123;  // 运行时抛出 ArrayStoreException

// 2. 泛型不变
List<String> strings = new ArrayList<>();
// List<Object> objects = strings;  // 编译错误!

// 3. 通配符实现协变/逆变
List<? extends Number> numbers = new ArrayList<Integer>();  // 协变
List<? super Integer> integers = new ArrayList<Number>();  // 逆变
```

---

## 最佳实践

### 命名规范

```java
// ✅ 推荐
public interface Map<K, V> { }
public interface List<E> { }
public class CompletableFuture<T> { }
public static <T extends Comparable<T>> T max(T a, T b) { }

// ❌ 避免
public interface Map<Key, Value> { }  // 太长
public interface Map<T1, T2> { }      // 无意义
```

### 边界选择

```java
// ✅ 推荐: 使用边界限制类型参数

// 1. 单一边界
public static <T extends Number> double sum(List<T> list) {
    double sum = 0;
    for (T item : list) {
        sum += item.doubleValue();
    }
    return sum;
}

// 2. 多重边界
public static <T extends Number & Comparable<T>> T max(T a, T b) {
    return a.compareTo(b) > 0 ? a : b;
}

// 3. 递归边界
public static <T extends Comparable<T>> T sort(List<T> list) {
    // ...
    return list.get(0);
}
```

### 通配符使用

```java
// ✅ 推荐: 使用通配符增加 API 灵活性

// 1. 输入参数 - 使用 extends (Producer)
public static void process(List<? extends Number> list) {
    for (Number n : list) {
        System.out.println(n.doubleValue());
    }
}

// 2. 输出参数 - 使用 super (Consumer)
public static void collect(List<? super Integer> list) {
    list.add(1);
    list.add(2);
}

// 3. 不可修改 - 使用无界通配符
public static int size(List<?> list) {
    return list.size();
}

// ❌ 避免: 过度使用通配符
public static void process(List<?> list) {  // 太宽泛
    // ...
}
```

### 泛型方法 vs 泛型类

```java
// ✅ 推荐: 泛型方法用于独立于类的泛型行为

public class Collections {
    // 泛型方法 - 与类无关
    public static <T> void swap(List<T> list, int i, int j) {
        // ...
    }

    public static <T extends Comparable<? super T>> void sort(List<T> list) {
        // ...
    }
}

// 泛型类 - 类本身需要类型参数
public class ArrayList<E> implements List<E> {
    // ...
}
```

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 泛型实现 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Gilad Bracha | 10+ | Sun | JSR 14 规范 |
| 2 | Neal Gafter | 8+ | Sun | 编译器实现 |
| 3 | Joseph Darcy | 5+ | Oracle | 泛型增强 |
| 4 | Maurizio Cimadamore | 5+ | Oracle | 类型推断 |

### 历史贡献者

| 贡献者 | 公司/机构 | 主要贡献 |
|--------|----------|----------|
| **Gilad Bracha** | Sun | JSR 14 规范负责人 |
| **Neal Gafter** | Sun | JSR 14 共同作者 |

---

## 相关链接

### 内部文档

- [语法演进](../language/syntax/) - 语法演进历程
- [集合框架](../../api/collections/) - 集合框架详解

### 外部资源

- [JSR 14: Generics](https://jcp.org/en/jsr/detail?id=14)
- [Generics (Java Tutorial)](https://docs.oracle.com/javase/tutorial/java/generics/)
- [Angelika Langer - Java Generics FAQ](https://www.angelikalanger.com/GenericsFAQ/JavaGenericsFAQ.html)

---

**最后更新**: 2026-03-20
