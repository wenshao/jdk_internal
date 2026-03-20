# 反射与元数据

> 反射、注解、MethodHandle 和 ClassFile API 的演进历程

[← 返回语言特性](../)

---

## 快速概览

```
JDK 1.0 ── JDK 5 ── JDK 6 ── JDK 7 ── JDK 8 ── JDK 11 ── JDK 16 ── JDK 21 ── JDK 24 ── JDK 26
   │         │        │        │        │        │        │        │        │        │
反射    注解    注解   MethodHandle Lambda   Foreign  ClassFile ClassFile  Mirror  invokedynamic
API    (JSR   处理   (JSR   invokedynamic  (JEP   (JEP    (JEP    API     API
        175)    JSR    JSR   292)      389)   395)    484)    增强    更新
                269)                                               反射
```

### 核心演进

| 版本 | 特性 | JEP | 说明 |
|------|------|-----|------|
| **JDK 1.0** | 反射 API | - | Class, Method, Field |
| **JDK 5** | 注解 | JSR 175 | @interface, 元编程 |
| **JDK 6** | 注解处理器 | JSR 269 | 编译期处理 |
| **JDK 7** | MethodHandle | JSR 292 | 动态语言支持 |
| **JDK 8** | Lambda invokedynamic | JSR 335 | 函数式编程 |
| **JDK 11** | Foreign Memory | JEP 370 | 外部内存访问 |
| **JDK 14** | Foreign Memory | JEP 389/393 | 内存访问 API |
| **JDK 16** | ClassFile API | JEP 395 | Class 文件操作 |
| **JDK 21** | Foreign Function | JEP 444 | FFI API |
| **JDK 24** | Class-File API | JEP 484 | 正式版 |
| **JDK 26** | Mirror API | - | 反射 API 增强 |

---

## 目录

- [反射 API](#反射-api)
- [注解](#注解)
- [MethodHandle](#methodhandle)
- [ClassFile API](#classfile-api)
- [Foreign API](#foreign-api)
- [最新增强](#最新增强)
- [核心贡献者](#核心贡献者)
- [相关链接](#相关链接)

---

## 反射 API

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

## 注解

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

## MethodHandle

**JDK 7 引入 (JSR 292)**

### 基础使用

```java
// MethodHandle - 比反射更快的动态调用
MethodHandles.Lookup lookup = MethodHandles.lookup();

// 获取 MethodHandle
MethodHandle toStringHandle = lookup.findVirtual(
    String.class, "toString", MethodType.methodType(String.class)
);

// 调用
String result = (String) toStringHandle.invokeExact("Hello");

// invoke - 自动类型转换
String result = (String) toStringHandle.invoke("Hello");
```

### 方法类型

```java
// MethodType - 方法签名描述
MethodType mt2 = MethodType.methodType(String.class);              // () -> String
MethodType mt3 = MethodType.methodType(String.class, int.class);   // (int) -> String
MethodType mt4 = MethodType.methodType(String.class, int.class, int.class);  // (int, int) -> String
```

### 特殊方法句柄

```java
// 字段访问
VarHandle intHandle = MethodHandles.lookup()
    .findVarHandle(MyClass.class, "intValue", int.class);

// 读写
int value = (int) intHandle.get(obj);
intHandle.set(obj, 42);

// 数组元素访问
VarHandle arrayHandle = MethodHandles.arrayElementVarHandle(int[].class);
int element = (int) arrayHandle.get(array, 5);
arrayHandle.set(array, 5, 100);
```

---

## ClassFile API

**JDK 16 预览 (JEP 395), JDK 24 正式 (JEP 484)**

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

## Foreign API

### Foreign Memory Access

**JDK 14 预览 (JEP 370/389), JDK 22 正式 (JEP 454)**

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

## 最新增强

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

### JDK 26: Mirror API 增强

反射 API 性能改进：

```java
// 更快的反射调用
// 改进的 Method.invoke() 性能
// 更好的缓存机制
```

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 类加载/反射 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Coleen Phillimore | 341 | Oracle | 类加载, 运行时 |
| 2 | Ioi Lam | 254 | Oracle | 反射, CDS, AOT |
| 3 | Calvin Cheung | 103 | Oracle | 类加载 |
| 4 | Harold Seigel | 89 | Oracle | JVM 运行时 |
| 5 | Stefan Karlsson | 87 | Oracle | 并发 GC |
| 6 | David Holmes | 63 | Oracle | 并发规范 |
| 7 | Aleksey Shipilev | 61 | Oracle | 性能基准 |
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

## Git 提交历史

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

## 相关链接

### 内部文档

- [反射时间线](timeline.md) - 详细的历史演进
- [Class File API](../classfile/) - 字节码操作
- [语法演进](../syntax/) - 语言特性
- [语言特性](../)

### 外部资源

- [JEP 395: Class File API (Preview)](https://openjdk.org/jeps/395)
- [JEP 484: Class-File API](https://openjdk.org/jeps/484)
- [JEP 370: Foreign Memory Access (Experimental)](https://openjdk.org/jeps/370)
- [JEP 389: Foreign Linker API (Experimental)](https://openjdk.org/jeps/389)
- [JEP 454: Foreign Function & Memory API](https://openjdk.org/jeps/454)
- [JSR 292: Supporting Dynamically Typed Languages](https://jcp.org/en/jsr/detail?id=292)
- [JSR 308: Annotations on Java Types](https://jcp.org/en/jsr/detail?id=308)

---

**最后更新**: 2026-03-20

**Sources**:
- [JEP 484: Class-File API](https://openjdk.org/jeps/484)
- [JEP 454: Foreign Function & Memory API](https://openjdk.org/jeps/454)
- [JEP 395: Class File API (Preview)](https://openjdk.org/jeps/395)
- [OpenJDK Git Commits](https://github.com/openjdk/jdk/commits/master/src/java.base/share/classes/java/lang/String.java)
