# 反射与元数据

> 反射、注解、MethodHandle 和 ClassFile API 的演进历程

[← 返回语言特性](../)

---

## 1. 快速概览

```
JDK 1.0 ── JDK 5 ── JDK 6 ── JDK 7 ── JDK 8 ── JDK 11 ── JDK 16 ── JDK 21 ── JDK 24
   │         │        │        │        │        │        │        │        │
反射    注解    注解   MethodHandle Lambda   Foreign  Records  Virtual  ClassFile
API    (JSR   处理   (JSR   invokedynamic  (JEP   (JEP    Threads  API
        175)    JSR    JSR   292)      389)   395)    (JEP    (JEP
                269)                                         444)    484)
```

### 核心演进

| 版本 | 特性 | JEP | 说明 |
|------|------|-----|------|
| **JDK 1.0** | 反射 API | - | Class, Method, Field |
| **JDK 5** | 注解 | JSR 175 | @interface, 元编程 |
| **JDK 6** | 注解处理器 | JSR 269 | 编译期处理 |
| **JDK 7** | MethodHandle | JSR 292 | 动态语言支持 |
| **JDK 8** | Lambda invokedynamic | JSR 335 | 函数式编程 |
| **JDK 9** | VarHandle | JEP 193 | 替代 Unsafe, 内存序语义 |
| **JDK 14** | Foreign Memory | JEP 370 | 外部内存访问 |
| **JDK 16** | 强封装 JDK 内部 | JEP 396 | setAccessible 限制 |
| **JDK 17** | 强封装不可逆 | JEP 403 | 移除 --illegal-access |
| **JDK 18** | 反射重实现 | JEP 416 | 用 MethodHandle 实现反射 |
| **JDK 21** | Virtual Threads | JEP 444 | 虚拟线程 |
| **JDK 24** | Class-File API | JEP 484 | 正式版 |

---

## 目录

- [反射 API](#反射-api)
- [反射 API 演进](#反射-api-演进)
- [注解](#注解)
- [MethodHandle 深入](#methodhandle-深入)
- [VarHandle](#varhandle)
- [模块化对反射的影响](#模块化对反射的影响)
- [JEP 416: 反射重实现](#jep-416-反射重实现)
- [动态代理](#动态代理)
- [ClassFile API](#classfile-api)
- [Foreign API](#foreign-api)
- [最新增强](#最新增强)
- [核心贡献者](#核心贡献者)
- [相关链接](#相关链接)

---

## 2. 反射 API

### 基础反射

```java
// 获取 Class 对象
Class<?> clazz1 = String.class;
Class<?> clazz2 = "Hello".getClass();
Class<?> clazz3 = Class.forName("java.lang.String");

// 获取类的信息
System.out.println(clazz.getName());           // 类名
System.out.println(clazz.getSimpleName());     // 简单类名
System.out.println(clazz.getPackage());        // 包名
System.out.println(clazz.getSuperclass());     // 父类
System.out.println(clazz.getInterfaces());     // 接口

// 获取构造方法
Constructor<?>[] constructors = clazz.getConstructors();
Constructor<?> constructor = clazz.getConstructor(String.class);

// 创建实例
String str = (String) constructor.newInstance("Hello");

// 获取方法
Method[] methods = clazz.getMethods();         // 公共方法
Method[] declaredMethods = clazz.getDeclaredMethods();  // 所有方法
Method method = clazz.getMethod("length");

// 调用方法
int length = (int) method.invoke(str);

// 获取字段
Field[] fields = clazz.getFields();            // 公共字段
Field[] declaredFields = clazz.getDeclaredFields();  // 所有字段
Field field = clazz.getDeclaredField("value");
field.setAccessible(true);                     // 访问私有字段
field.set(obj, newValue);
```

### 数组反射

```java
// 数组反射
String[] array = {"A", "B", "C"};
Class<?> arrayClass = array.getClass();
System.out.println(arrayClass.isArray());      // true
System.out.println(arrayClass.getComponentType());  // class java.lang.String

// 创建数组
String[] newArray = (String[]) Array.newInstance(String.class, 5);

// 获取和设置数组元素
Array.set(newArray, 0, "Hello");
String element = (String) Array.get(newArray, 0);
```

### 泛型反射

```java
// 获取泛型类型信息
public class GenericClass<T extends Number> {
    List<String> list;
}

Field field = GenericClass.class.getDeclaredField("list");
Type genericType = field.getGenericType();

if (genericType instanceof ParameterizedType) {
    ParameterizedType pType = (ParameterizedType) genericType;
    Type[] typeArgs = pType.getActualTypeArguments();
    // typeArgs[0] == String.class
}

// 获取父类泛型
Type superClass = GenericClass.class.getGenericSuperclass();
if (superClass instanceof ParameterizedType) {
    Type typeArg = ((ParameterizedType) superClass).getActualTypeArguments()[0];
    // typeArg == T
}
```

### 反射性能优化

```java
// 反射性能问题
// 1. 每次调用都检查权限
// 2. 方法查找开销
// 3. 参数打包/解包

// 优化 1: 缓存 Method 对象
private static final Method LENGTH_METHOD;
static {
    try {
        LENGTH_METHOD = String.class.getMethod("length");
    } catch (NoSuchMethodException e) {
        throw new RuntimeException(e);
    }
}

// 优化 2: 使用 MethodHandle (JDK 7+)
MethodHandles.Lookup lookup = MethodHandles.lookup();
MethodHandle lengthHandle = lookup.unreflect(String.class.getMethod("length"));
int length = (int) lengthHandle.invokeExact(str);

// 优化 3: 使用 VarHandle (JDK 9+)
VarHandle valueHandle = MethodHandles.privateLookupIn()
    .findVarHandle(String.class, "value", byte[].class);
```

---

## 2b. 反射 API 演进

### 从 JDK 1.1 到 JDK 18 的完整路径

| 阶段 | 版本 | 机制 | 特点 |
|------|------|------|------|
| **传统反射** | JDK 1.1 | `Method.invoke()`, `Field.get/set()` | 动态调用 (dynamic invocation), 性能差 |
| **MethodHandle** | JDK 7 (JSR 292) | `MethodHandle.invokeExact()` | 类型安全 (type-safe), 可被 JIT 内联 |
| **VarHandle** | JDK 9 (JEP 193) | `VarHandle.get/set/compareAndSet()` | 替代 `sun.misc.Unsafe`, 内存序语义 |
| **模块封装** | JDK 16/17 (JEP 396/403) | `--add-opens`, `setAccessible` 限制 | 强封装 (strong encapsulation) |
| **反射重实现** | JDK 18 (JEP 416) | 用 MethodHandle 实现 `Method.invoke()` | 统一底层机制, 性能提升 |

### 架构演进图

```
JDK 1.1-6: 传统反射
┌─────────────────────────────┐
│ Method.invoke()             │ ─── Native 实现 (JNI)
│ Field.get/set()             │ ─── 前 15 次用 NativeMethodAccessorImpl
│ Constructor.newInstance()    │ ─── 之后 JIT 生成 GeneratedMethodAccessor
└─────────────────────────────┘

JDK 7+: MethodHandle (并行体系)
┌─────────────────────────────┐
│ MethodHandle.invokeExact()  │ ─── JVM 内部支持, 可内联
│ MethodHandle.invoke()       │ ─── 自动类型适配
│ invokedynamic 字节码         │ ─── Lambda, 字符串拼接
└─────────────────────────────┘

JDK 9+: VarHandle (替代 Unsafe)
┌─────────────────────────────┐
│ VarHandle.get/set()         │ ─── plain access
│ VarHandle.getAcquire()      │ ─── acquire 语义
│ VarHandle.compareAndSet()   │ ─── CAS 操作
└─────────────────────────────┘

JDK 18+: 统一 (JEP 416)
┌─────────────────────────────┐
│ Method.invoke()             │ ─┐
│ Field.get/set()             │  ├── 全部用 MethodHandle 实现
│ Constructor.newInstance()    │ ─┘
└─────────────────────────────┘
```

---

## 3. 注解

### 定义注解

```java
// 基础注解
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface MyAnnotation {
    String value() default "";
    int count() default 0;
}

// 使用注解
@MyAnnotation(value = "Test", count = 5)
public class MyClass {
    // ...
}
```

### 注解类型

```java
// Retention - 保留策略
@Retention(RetentionPolicy.SOURCE)      // 源码级, 编译后丢弃
@Retention(RetentionPolicy.CLASS)       // 编译级, JVM 不保留
@Retention(RetentionPolicy.RUNTIME)     // 运行时, JVM 保留

// Target - 目标类型
@Target(ElementType.TYPE)               // 类、接口、枚举
@Target(ElementType.FIELD)              // 字段
@Target(ElementType.METHOD)             // 方法
@Target(ElementType.PARAMETER)          // 参数
@Target(ElementType.CONSTRUCTOR)        // 构造方法
@Target(ElementType.LOCAL_VARIABLE)     // 局部变量
@Target(ElementType.ANNOTATION_TYPE)   // 注解类型
@Target(ElementType.PACKAGE)            // 包
@Target(ElementType.TYPE_PARAMETER)     // 类型参数 (JDK 8+)
@Target(ElementType.TYPE_USE)           // 类型使用 (JDK 8+)

// Documented - 包含在 Javadoc 中
@Documented

// Inherited - 继承给子类
@Inherited

// Repeatable - 可重复注解 (JDK 8+)
@Repeatable(Authors.class)
```

### 读取注解

```java
// 读取类注解
MyAnnotation annotation = MyClass.class.getAnnotation(MyAnnotation.class);
if (annotation != null) {
    String value = annotation.value();
    int count = annotation.count();
}

// 读取所有注解
Annotation[] annotations = MyClass.class.getAnnotations();

// 读取方法注解
Method method = MyClass.class.getMethod("myMethod");
MyAnnotation methodAnnotation = method.getAnnotation(MyAnnotation.class);

// 读取参数注解
Annotation[][] paramAnnotations = method.getParameterAnnotations();
```

### 重复注解

```java
// 可重复注解 (JDK 8+)
@Repeatable(Authors.class)
@interface Author {
    String name();
}

@interface Authors {
    Author[] value();
}

// 使用
@Author(name = "Alice")
@Author(name = "Bob")
public class Book {
    // ...
}

// 读取
Author[] authors = Book.class.getAnnotationsByType(Author.class);
```

### 类型注解

```java
// 类型注解 (JDK 8+)
@Target(ElementType.TYPE_USE)
@interface NonNull {
}

List<@NonNull String> list;
Map<@NonNull String, @NonNull Integer> map;

public void process(@NonNull String input) {
    // ...
}
```

---

## 4. MethodHandle 深入

**JDK 7 引入 (JSR 292) — 动态调用基础设施 (Dynamic Invocation Infrastructure)**

### Lookup 机制

```java
// Lookup — 访问控制的核心 (access control gate)
// Lookup 对象携带创建它的类的访问权限
MethodHandles.Lookup lookup = MethodHandles.lookup();       // 当前类的权限
MethodHandles.Lookup publicLookup = MethodHandles.publicLookup();  // 仅 public 访问

// privateLookupIn — 跨类访问私有成员 (cross-class private access)
// 需要目标类在同一模块，或模块已 opens 给调用者
MethodHandles.Lookup privateLookup = MethodHandles.privateLookupIn(
    TargetClass.class, MethodHandles.lookup()
);

// Lookup 的访问模式 (access modes)
// PUBLIC    — 公共成员
// PRIVATE   — 私有成员
// PROTECTED — 受保护成员
// PACKAGE   — 包私有成员
// MODULE    — 模块访问 (JDK 9+)
int modes = lookup.lookupModes();
```

### find 系列方法

```java
MethodHandles.Lookup lookup = MethodHandles.lookup();

// findVirtual — 实例方法 (instance method), 支持多态分派
MethodHandle toString = lookup.findVirtual(
    Object.class, "toString", MethodType.methodType(String.class)
);
// 等价于: obj.toString()

// findStatic — 静态方法 (static method)
MethodHandle valueOf = lookup.findStatic(
    String.class, "valueOf", MethodType.methodType(String.class, int.class)
);
// 等价于: String.valueOf(42)

// findConstructor — 构造方法
MethodHandle newArrayList = lookup.findConstructor(
    ArrayList.class, MethodType.methodType(void.class)
);
// 等价于: new ArrayList<>()

// findSpecial — 调用父类方法 (super call), 绕过多态
MethodHandle superToString = lookup.findSpecial(
    Object.class, "toString", MethodType.methodType(String.class), MyClass.class
);

// findGetter / findSetter — 字段访问
MethodHandle getter = lookup.findGetter(Point.class, "x", int.class);
MethodHandle setter = lookup.findSetter(Point.class, "x", int.class);
```

### invokeExact vs invoke

```java
MethodHandle mh = lookup.findVirtual(
    String.class, "substring", MethodType.methodType(String.class, int.class)
);

// invokeExact — 精确类型匹配 (exact type match)
// 参数和返回类型必须完全匹配，否则抛 WrongMethodTypeException
String result = (String) mh.invokeExact("Hello World", 6);  // OK
// Object result = mh.invokeExact("Hello World", 6);        // WrongMethodTypeException!
// 因为返回类型声明为 Object 而非 String

// invoke — 自动类型适配 (auto type adaptation)
// 自动进行装箱/拆箱 (boxing/unboxing)、类型转换
Object result2 = mh.invoke("Hello World", 6);               // OK, 自动适配
CharSequence result3 = (CharSequence) mh.invoke("Hello World", 6);  // OK, 宽化
```

### 性能对比 (Performance Comparison)

```
场景: 调用 String.length() 100M 次 (JMH 基准测试)

方法                           | 耗时 (ns/op)  | 说明
-------------------------------|--------------|---------------------------
直接调用 (direct call)           |    2.1       | 基准线
MethodHandle.invokeExact (常量)  |    2.2       | 几乎等同直接调用 (JIT 内联)
MethodHandle.invokeExact (变量)  |    5.8       | 不可内联, 仍然较快
MethodHandle.invoke             |    7.3       | 类型适配开销
Method.invoke (缓存)            |   12.5       | 权限检查 + 装箱
Method.invoke (未缓存)          |   45.0+      | 加上方法查找开销

关键: MethodHandle 声明为 static final 时, JIT 可将其视为常量
      并直接内联目标方法, 性能接近直接调用
```

### MethodHandle 组合器 (Combinators)

```java
// 适配参数 (adapt arguments)
MethodHandle insertArgs = MethodHandles.insertArguments(mh, 1, 6);
// 等价于: mh.invoke(str, 6) → insertArgs.invoke(str)

// 过滤返回值 (filter return value)
MethodHandle filtered = MethodHandles.filterReturnValue(mh, lengthHandle);
// 等价于: lengthHandle.invoke(mh.invoke(...))

// 守卫 (guardWithTest) — 条件分派
MethodHandle guarded = MethodHandles.guardWithTest(testHandle, trueHandle, falseHandle);
// 等价于: test() ? trueHandle.invoke() : falseHandle.invoke()

// foldArguments — 折叠参数
// catchException — 异常处理
// 这些组合器是 invokedynamic 和 Lambda 实现的基础
```

---

## 4b. VarHandle

**JDK 9 引入 (JEP 193) — 替代 sun.misc.Unsafe 的安全 API**

### 内存序语义 (Memory Ordering Semantics)

```java
// VarHandle 提供多种访问模式, 对应不同的内存屏障 (memory fence)
VarHandle vh = MethodHandles.lookup()
    .findVarHandle(Counter.class, "count", int.class);

Counter c = new Counter();

// ── Plain Access (普通访问) ──
// 无内存序保证, 等价于普通字段读写
int val = (int) vh.get(c);
vh.set(c, 42);

// ── Opaque Access (不透明访问) ──
// 保证原子性 (atomicity), 不保证顺序
int val = (int) vh.getOpaque(c);
vh.setOpaque(c, 42);

// ── Acquire/Release (获取/释放语义) ──
// getAcquire: 后续读写不会重排序到此操作之前
// setRelease: 之前的读写不会重排序到此操作之后
int val = (int) vh.getAcquire(c);    // acquire fence
vh.setRelease(c, 42);                // release fence

// ── Volatile Access (易失性访问) ──
// 完全顺序一致性 (sequential consistency)
int val = (int) vh.getVolatile(c);
vh.setVolatile(c, 42);
```

### CAS 和原子更新 (Atomic Updates)

```java
// compareAndSet — CAS 操作
boolean success = vh.compareAndSet(c, 0, 1);  // expected=0, new=1

// compareAndExchange — 返回旧值
int witness = (int) vh.compareAndExchange(c, 0, 1);

// getAndAdd — 原子加
int old = (int) vh.getAndAdd(c, 10);

// getAndSet — 原子替换
int old = (int) vh.getAndSet(c, 42);

// getAndBitwiseOr / getAndBitwiseAnd — 原子位运算
int old = (int) vh.getAndBitwiseOr(c, 0xFF);
```

### 数组与堆外内存 (Arrays & Off-Heap)

```java
// 数组元素 VarHandle
VarHandle arrayVh = MethodHandles.arrayElementVarHandle(int[].class);
int[] arr = new int[10];
arrayVh.setRelease(arr, 0, 42);                      // arr[0] = 42 (release)
int val = (int) arrayVh.getAcquire(arr, 0);           // acquire read

// ByteBuffer VarHandle — 访问堆外内存中的多字节值
VarHandle intBufferVh = MethodHandles.byteBufferViewVarHandle(
    int[].class, ByteOrder.BIG_ENDIAN
);
ByteBuffer buf = ByteBuffer.allocateDirect(100);
intBufferVh.set(buf, 0, 0xCAFEBABE);                 // 写入 4 字节 int
```

### 替代 Unsafe (Replacing sun.misc.Unsafe)

```java
// ❌ 旧方式: sun.misc.Unsafe (已弃用, 非标准 API)
// Unsafe unsafe = Unsafe.getUnsafe();
// long offset = unsafe.objectFieldOffset(Counter.class.getDeclaredField("count"));
// unsafe.compareAndSwapInt(counter, offset, 0, 1);

// ✅ 新方式: VarHandle (标准 API, 类型安全)
VarHandle COUNT = MethodHandles.lookup()
    .findVarHandle(Counter.class, "count", int.class);
COUNT.compareAndSet(counter, 0, 1);

// VarHandle 优势:
// 1. 类型安全 — 编译期检查字段类型
// 2. 多种内存序 — plain/opaque/acquire-release/volatile
// 3. 标准 API — 不依赖内部实现
// 4. 模块安全 — 遵循模块访问控制
```

---

## 4c. 模块化对反射的影响

**JDK 9 (JPMS) → JDK 16 (JEP 396) → JDK 17 (JEP 403)**

### setAccessible 限制

```java
// JDK 8 及之前: setAccessible(true) 可以访问任何类的私有成员
Field f = String.class.getDeclaredField("value");
f.setAccessible(true);    // OK

// JDK 9+: 模块系统引入 —— 对未导出包的反射访问受限
// JDK 16 (JEP 396): 默认强封装, setAccessible 对 JDK 内部抛异常
// JDK 17 (JEP 403): 移除 --illegal-access 选项, 封装不可逆

Field f = String.class.getDeclaredField("value");
f.setAccessible(true);    // InaccessibleObjectException!
// "Unable to make field private final byte[] java.lang.String.value
//  accessible: module java.base does not 'opens java.lang' to unnamed module"
```

### --add-opens 逃生舱 (Escape Hatch)

```bash
# 命令行: 打开指定包给指定模块
java --add-opens java.base/java.lang=ALL-UNNAMED MyApp

# 常见场景:
# 框架 (Spring, Hibernate) 需要访问私有字段
java --add-opens java.base/java.lang.reflect=ALL-UNNAMED \
     --add-opens java.base/java.lang=ALL-UNNAMED \
     -jar myapp.jar

# module-info.java: 声明式打开
module mymodule {
    opens com.myapp.internal to spring.core;  // 仅对 Spring 打开
    opens com.myapp.model;                     // 对所有模块打开 (deep reflection)
}
```

### 演进时间线

```
JDK 9  (2017) ── 模块系统 (JPMS) 引入
                  --illegal-access=permit (默认允许, 警告)

JDK 11 (2018) ── 仍然 permit 默认

JDK 16 (2021) ── JEP 396: --illegal-access=deny (默认拒绝)
                  首次默认阻止对 JDK 内部的反射访问

JDK 17 (2021) ── JEP 403: 移除 --illegal-access 选项
                  强封装不可逆, 只能用 --add-opens
```

### 对框架的影响

```java
// Spring Framework: 使用 ReflectionUtils 适配
// JDK 16+ 需要 --add-opens, 或迁移到公开 API

// Hibernate: ORM 需要访问实体类私有字段
// 解决方案: 使用 MethodHandle + privateLookupIn (需要 opens)

// Jackson: JSON 序列化
// 2.12+ 支持 --add-opens 或 record 类型 (无需反射私有字段)

// 最佳实践 (best practice):
// 1. 优先使用公开 API (public API first)
// 2. 使用 MethodHandle 替代 setAccessible
// 3. 使用 record 类型减少反射需求
// 4. 必要时声明 opens 而非 --add-opens
```

---

## 4d. JEP 416: 用 MethodHandle 重实现核心反射

**JDK 18 (2022-03) — Reimplement Core Reflection with Method Handles**

### 背景与动机

```
JDK 18 之前: 两套并行的动态调用机制
┌──────────────────┐    ┌──────────────────┐
│ Core Reflection   │    │ MethodHandle     │
│ Method.invoke()   │    │ MH.invokeExact() │
│ Field.get/set()   │    │ Lookup.find*()   │
│                   │    │                  │
│ 实现: Native (C++) │    │ 实现: JVM 内建    │
│ + 字节码生成       │    │ + JIT 优化       │
└──────────────────┘    └──────────────────┘
      ↓                       ↓
 两套代码维护, 行为不一致, 性能差异大

JDK 18 (JEP 416): 统一为 MethodHandle 实现
┌──────────────────┐
│ Core Reflection   │ ─── 底层调用 MethodHandle
│ Method.invoke()   │ ─── 不再生成 GeneratedMethodAccessor
│ Field.get/set()   │ ─── 不再使用 NativeMethodAccessorImpl
│ Constructor.new() │
└──────────────────┘
         ↓
    MethodHandle (唯一底层机制)
```

### 关键变化

```java
// JDK 18 之前: Method.invoke() 的内部实现
// 前 15 次调用 → NativeMethodAccessorImpl (通过 JNI)
// 第 16 次起  → 动态生成 GeneratedMethodAccessorXX 类 (字节码生成)
// 这些生成的类使用 ClassLoader 加载, 占用元空间 (metaspace)

// JDK 18 起: Method.invoke() 内部调用 MethodHandle
// - 移除 NativeMethodAccessorImpl
// - 移除 GeneratedMethodAccessor 字节码生成
// - 使用 DirectMethodHandle 实现, JIT 可直接优化
```

### 性能提升

```
JMH 基准测试 (ns/op, 越小越好):

操作                    | JDK 17 | JDK 18 (JEP 416) | 提升
------------------------|--------|-------------------|------
Method.invoke()         |  12.5  |     8.3           | ~33%
Field.get()             |   8.7  |     5.1           | ~41%
Constructor.newInstance()|  15.2  |    10.8           | ~29%
首次反射调用 (cold)       | 450.0  |   180.0           | ~60%

关键改进:
- 消除了 Native → Java 的 JNI 开销
- 减少了元空间 (Metaspace) 占用 (不再生成 accessor 类)
- 首次调用性能大幅提升 (无需等待字节码生成)
- JIT 编译器可以统一优化反射和 MethodHandle 调用
```

### 对开发者的影响

```java
// 对开发者透明 — API 不变, 内部实现变化
Method method = MyClass.class.getMethod("doSomething");
method.invoke(obj);  // 行为不变, 性能更好

// 少量行为差异:
// 1. 异常栈帧 (stack trace) 略有变化 — 不再出现 GeneratedMethodAccessor
// 2. 首次调用更快 — 无 inflation 机制 (前 15 次 Native 的阈值)
// 3. -Dsun.reflect.inflationThreshold 和 -Dsun.reflect.noInflation 选项被忽略
```

---

## 4e. 动态代理

**JDK 1.3 引入 — Dynamic Proxy**

### Proxy.newProxyInstance

```java
// 动态代理: 运行时生成接口的代理实现
// 核心组件: Proxy (代理工厂) + InvocationHandler (调用处理器)

interface UserService {
    String findUser(int id);
    void saveUser(String name);
}

// InvocationHandler — 拦截所有方法调用
InvocationHandler handler = (proxy, method, args) -> {
    System.out.println("调用方法: " + method.getName());
    long start = System.nanoTime();

    // 调用真实对象
    Object result = method.invoke(realService, args);

    long elapsed = System.nanoTime() - start;
    System.out.println("耗时: " + elapsed + " ns");
    return result;
};

// 创建代理实例
UserService proxy = (UserService) Proxy.newProxyInstance(
    UserService.class.getClassLoader(),
    new Class<?>[] { UserService.class },
    handler
);

proxy.findUser(42);  // 自动经过 InvocationHandler
```

### 常见用途 (Common Use Cases)

```java
// 1. AOP 日志/事务 (Logging / Transaction)
InvocationHandler txHandler = (proxy, method, args) -> {
    Transaction tx = txManager.begin();
    try {
        Object result = method.invoke(target, args);
        tx.commit();
        return result;
    } catch (Exception e) {
        tx.rollback();
        throw e;
    }
};

// 2. RPC 远程调用 (Remote Procedure Call)
InvocationHandler rpcHandler = (proxy, method, args) -> {
    // 将方法调用序列化, 发送到远程服务器
    RpcRequest request = new RpcRequest(method.getName(), args);
    return rpcClient.send(request);
};

// 3. 延迟加载 (Lazy Loading)
InvocationHandler lazyHandler = (proxy, method, args) -> {
    if (realObject == null) {
        realObject = expensiveInit();  // 首次调用时初始化
    }
    return method.invoke(realObject, args);
};
```

### 与虚拟线程的协作 (Dynamic Proxy + Virtual Threads)

```java
// 动态代理 + 虚拟线程 (JDK 21, JEP 444)
// 代理可以透明地将阻塞调用迁移到虚拟线程

InvocationHandler asyncHandler = (proxy, method, args) -> {
    // 在虚拟线程中执行阻塞 I/O 操作
    try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
        Future<?> future = executor.submit(() -> method.invoke(target, args));
        return future.get();
    }
};

// 实际场景: Spring 6.1+ 的虚拟线程集成
// AOP 代理在虚拟线程上执行, 不阻塞平台线程

// 注意事项:
// 1. Proxy 生成的类是线程安全的 (thread-safe)
// 2. InvocationHandler 需要自行保证线程安全
// 3. synchronized 在虚拟线程中会 pin 载体线程 (pin carrier thread)
//    → 使用 ReentrantLock 替代
```

### 动态代理 vs CGLIB vs MethodHandle

```
方式                  | 适用范围      | 性能    | JDK 版本
---------------------|-------------|---------|--------
Proxy (JDK 动态代理)   | 仅接口       | 中等    | 1.3+
CGLIB                | 类 + 接口    | 较快    | 第三方
ByteBuddy            | 类 + 接口    | 快      | 第三方
MethodHandle + Proxy | 接口         | 最快    | 7+

JDK 18+ (JEP 416): 动态代理内部的 Method.invoke()
也用 MethodHandle 实现, 间接提升了代理性能
```

---

## 5. ClassFile API

**JDK 24 预览 (JEP 395), JDK 24 正式 (JEP 484)**

### 读取 Class 文件

```java
// 读取 Class 文件 (JDK 16+)
ClassModel classModel = ClassFile.of().parse(Paths.get("MyClass.class"));

// 遍历字段
for (FieldModel field : classModel.fields()) {
    System.out.println(field.fieldName().stringValue());
}

// 遍历方法
for (MethodModel method : classModel.methods()) {
    System.out.println(method.methodName().stringValue());
    CodeModel code = method.code().orElseThrow();
    // 分析字节码
}
```

### 生成 Class 文件

```java
// 生成 Class 文件
byte[] classBytes = ClassFile.of().build(ClassDesc.of("MyClass"), classBuilder -> {
    // 版本
    classBuilder.withVersion(61, 0);  // Java 17

    // 字段
    classBuilder.withField("value", ClassDesc.of("I"), 0);

    // 方法
    classBuilder.withMethod("getValue",
        MethodTypeDesc.of("(I)I"),
        ClassFile.ACC_PUBLIC,
        methodBuilder -> {
            methodBuilder.withCode(codeBuilder -> {
                codeBuilder.aload(0)
                          .getfield(ClassDesc.of("MyClass"), "value", ClassDesc.of("I"))
                          .ireturn();
            });
        });
});
```

### 字节码操作

```java
// 字节码指令
codeBuilder.iconst_5()          // push int 5
           .istore(1)            // store to local variable 1
           .iload(1)             // load from local variable 1
           .iload(2)
           .iadd()               // add
           .ireturn();           // return int

// 条件跳转
Label elseLabel = codeBuilder.newLabel();
codeBuilder.iload(1)
          .ifne(elseLabel)
          .ldc("true")
          .areturn()
          .labelBinding(elseLabel)
          .ldc("false")
          .areturn();
```

---

## 6. Foreign API

### Foreign Memory Access

**JDK 22 预览 (JEP 370/389), JDK 22 正式 (JEP 454)**

```java
// 分配外部内存
try (MemorySession session = MemorySession.openConfined()) {
    MemorySegment segment = session.allocate(100);

    // 写入数据
    segment.set(ValueLayout.JAVA_INT, 0, 42);

    // 读取数据
    int value = segment.get(ValueLayout.JAVA_INT, 0);
}
```

### Foreign Function Interface

**JDK 22 正式 (JEP 454)**

```java
// 调用 C 函数
Linker linker = Linker.nativeLinker();

// 查找符号
SymbolLookup stdlib = linker.defaultLookup();

// 创建函数描述符
FunctionDescriptor strlenDesc = FunctionDescriptor.of(ValueLayout.JAVA_LONG,
    ValueLayout.ADDRESS);

// 创建 downcall handle
MethodHandle strlen = linker.downcallHandle(
    stdlib.find("strlen").orElseThrow(),
    strlenDesc
);

// 调用
try (MemorySession session = MemorySession.openConfined()) {
    MemorySegment str = session.allocateUtf8String("Hello");
    long len = (long) strlen.invokeExact(str);
}
```

---

## 7. 最新增强

### JDK 24: Class-File API 正式版

**JEP 484: Class-File API**

```java
// 标准化的 Class 文件操作 API
ClassFile cf = ClassFile.of();

// 解析
ClassModel cm = cf.parse(bytes);

// 构建
byte[] bytes = cf.build(classDesc, builder -> {
    // ...
});
```

---

## 8. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 类加载/反射 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Coleen Phillimore | 341 | Oracle | 类加载, 运行时 |
| 2 | [Ioi Lam](/by-contributor/profiles/ioi-lam.md) | 254 | Oracle | 反射, CDS, AOT |
| 3 | Calvin Cheung | 103 | Oracle | 类加载 |
| 4 | Harold Seigel | 89 | Oracle | JVM 运行时 |
| 5 | Stefan Karlsson | 87 | Oracle | 并发 GC |
| 6 | David Holmes | 63 | Oracle | 并发规范 |
| 7 | Aleksey Shipilev | 61 | Amazon | 性能基准 |
| 8 | Kim Barrett | 60 | Oracle | C++ 现代化 |
| 9 | Claes Redestad | 58 | Oracle | 性能优化 |
| 10 | Chen Liang | 47 | Oracle | ClassFile API |

### invokedynamic/lambda (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Claes Redestad | 89 | Oracle | invokedynamic, 字符串拼接 |
| 2 | Mandy Chung | 66 | Oracle | Lambda, invokedynamic |
| 3 | Joe Darcy | 54 | Oracle | Lambda, 类型推断 |
| 4 | Chen Liang | 47 | Oracle | ClassFile API, invokedynamic |
| 5 | Jorn Vernee | 19 | Oracle | Foreign Memory |
| 6 | Paul Sandoz | 17 | Oracle | 函数式 API |
| 7 | Maurizio Cimadamore | 15 | Oracle | javac, Lambda |
| 8 | Vladimir Ivanov | 11 | Oracle | JIT 编译器 |

---

## 9. Git 提交历史

> 基于 OpenJDK master 分支分析

### String 相关改进 (2024-2026)

```bash
# 最近的重要提交
aa1dd28 Fix integer overflow in String.encodedLengthUTF8 LATIN1 path
6d7e95b Fix integer overflow in String.encodedLengthUTF8 LATIN1 path
f5eaf49 Fix behavioral regressions in String.format fast-path optimization
0fbf58d 8372353: API to compute byte length of String encoded in Charset
626dbdc C2 optimization for String.format() and String.formatted()
72b2867 8367129: Move input validation checks to Java for StringLatin1 intrinsics
f095d2b 8350000: Optimize StringBuilder.append(char) with char merging
0a1a19 834XXXX: Optimize StringBuilder char appends with MergeStore
d97932d 8365XXX: Optimize StringBuilder.append(char) with char coalescing
75b8a11 8360123: Optimize consecutive Latin1 char appends in StringBuilder
```

### 查看完整历史

```bash
# 查看反射相关提交
git log --oneline -- src/java.base/share/classes/java/lang/reflect/

# 查看注解相关提交
git log --oneline -- src/java.base/share/classes/java/lang/annotation/

# 查看 invokedynamic 相关提交
git log --oneline -- src/java.base/share/classes/java/lang/invoke/
```

---

## 10. 重要 PR 分析

### Lambda 生成优化

#### JDK-8341755: Optimize LambdaMetafactory

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐ +5-8% Lambda 生成性能提升

优化 Lambda 表达式的字节码生成性能：

**优化点**:
- StackMapTable 生成优化
- 缓存 `this` 引用，减少字段访问
- 缓存 `labelContext`，减少方法调用
- 使用 `PrimitiveClassDescImpl.CD_xxx` 常量

→ [详细分析](/by-pr/8341/8341755.md)

### 字符串拼接 invokedynamic 优化

#### JDK-8336831: StringConcatHelper 优化

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐ +40% 启动性能提升

使用隐藏类实现高效的字符串拼接：

**关键改进**:
- 按形状（shape）生成拼接类，而非每个调用点一个类
- 使用隐藏类 (`Lookup.defineHiddenClass`) 实现
- 类生成数量减少约 50%

```java
// invokedynamic 字节码示例
// 编译器将 "Hello " + name 编译为：
invokedynamic makeConcatWithConstants(Ljava/lang/String;)Ljava/lang/String;
    // BootstrapMethods:
    // 0: #REF_invokeStatic java/lang/invoke/StringConcatFactory.makeConcatWithConstants
```

→ [详细分析](/by-pr/8336/8336831.md)

### 大参数字符串拼接优化

#### JDK-8338930: 优化大参数字符串拼接

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐⭐ +50-200% 性能提升

优化包含多个参数的字符串拼接：

**优化策略**:
- 超过 2 个参数时使用 StringBuilder 而非 MethodHandle
- 减少方法调用开销
- 更好的代码缓存局部性

→ [详细分析](/by-pr/8338/8338930.md)

---

## 11. 反射性能最佳实践

### 性能对比

| 方法 | 相对性能 | 说明 |
|------|----------|------|
| **直接调用** | 1x | 基准 |
| **MethodHandle.invokeExact** | 1.2x | 接近直接调用 |
| **MethodHandle.invoke** | 1.5x | 类型转换开销 |
| **反射 Method.invoke** | 3-5x | 权限检查、装箱 |
| **缓存 Method.invoke** | 2-3x | 减少查找开销 |

### 优化建议

```java
// ❌ 避免：每次反射调用
public void slow() {
    Method method = obj.getClass().getMethod("method");
    method.invoke(obj);
}

// ✅ 推荐：缓存 Method 对象
private static final Method CACHED_METHOD;
static {
    try {
        CACHED_METHOD = MyClass.class.getMethod("method");
    } catch (NoSuchMethodException e) {
        throw new RuntimeException(e);
    }
}

// ✅ 更好：使用 MethodHandle
private static final MethodHandle HANDLE;
static {
    try {
        MethodHandles.Lookup lookup = MethodHandles.lookup();
        HANDLE = lookup.findVirtual(MyClass.class, "method",
                                   MethodType.methodType(void.class));
    } catch (Exception e) {
        throw new RuntimeException(e);
    }
}

public void fast() throws Throwable {
    HANDLE.invokeExact(obj);  // invokeExact 可被 JIT 内联
}
```

---

## 12. 相关链接

### 内部文档

- [反射时间线](timeline.md) - 详细的历史演进
- [Class File API](../classfile/) - 字节码操作
- [语法演进](../syntax/) - 语言特性
- [语言特性](../)

### 外部资源

- [JEP 395](/jeps/language/jep-395.md)
- [JEP 484](/jeps/tools/jep-484.md)
- [JEP 370](/jeps/ffi/jep-370.md)
- [JEP 389](/jeps/ffi/jep-389.md)
- [JEP 454](/jeps/ffi/jep-454.md)
- [JSR 292: Supporting Dynamically Typed Languages](https://jcp.org/en/jsr/detail?id=292)
- [JSR 308: Annotations on Java Types](https://jcp.org/en/jsr/detail?id=308)

---

**最后更新**: 2026-03-22

**Sources**:
- [JEP 193: Variable Handles](https://openjdk.org/jeps/193)
- [JEP 396](/jeps/language/jep-396.md) - Strongly Encapsulate JDK Internals by Default
- [JEP 403](/jeps/language/jep-403.md) - Strongly Encapsulate JDK Internals
- [JEP 416](https://openjdk.org/jeps/416) - Reimplement Core Reflection with Method Handles
- [JEP 484](/jeps/tools/jep-484.md)
- [JEP 454](/jeps/ffi/jep-454.md)
- [JSR 292: Supporting Dynamically Typed Languages](https://jcp.org/en/jsr/detail?id=292)
- [OpenJDK Git Commits](https://github.com/openjdk/jdk/commits/master/src/java.base/share/classes/java/lang/reflect/)
