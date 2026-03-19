# 反射与元数据演进时间线

Java 反射和元数据从 JDK 1.0 到 JDK 26 的完整演进历程。

---

## 时间线概览

```
JDK 1.0 ──── JDK 5 ──── JDK 6 ──── JDK 7 ──── JDK 8 ──── JDK 11 ──── JDK 16 ──── JDK 26
 │             │           │           │           │           │           │           │
Reflection    Annotations  Pluggable   MethodHandle Lambda     Constable   ClassFile  Mirror
API           (JSR 175)   Annotation  (JSR 292)  (Invoke-    Constant   API       API
                                       Dynamic)              Desc
```

---

## 反射体系结构

```
┌─────────────────────────────────────────────────────────┐
│                  Java 反射体系                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Class 对象                                            │
│      │                                                  │
│      ├── Field (字段)                                   │
│      ├── Method (方法)                                  │
│      ├── Constructor (构造器)                           │
│      ├── Annotation (注解)                              │
│      └── Parameter (参数)                               │
│                                                         │
│  反射操作:                                              │
│  ├── 获取元数据                                         │
│  ├── 动态调用方法                                       │
│  ├── 动态访问字段                                       │
│  ├── 创建实例                                           │
│  └── 修改访问控制                                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## JDK 1.0 - 反射 API

### 获取 Class 对象

```java
// 获取 Class 对象的三种方式

// 1. 通过类字面量
Class<String> clazz1 = String.class;

// 2. 通过对象的 getClass() 方法
String str = "Hello";
Class<?> clazz2 = str.getClass();

// 3. 通过 Class.forName()
Class<?> clazz3 = Class.forName("java.lang.String");
```

### 获取类信息

```java
Class<?> clazz = String.class;

// 类名
String simpleName = clazz.getSimpleName();  // String
String canonicalName = clazz.getCanonicalName();  // java.lang.String
String name = clazz.getName();  // java.lang.String

// 修饰符
int modifiers = clazz.getModifiers();
boolean isPublic = Modifier.isPublic(modifiers);
boolean isFinal = Modifier.isFinal(modifiers);
boolean isAbstract = Modifier.isAbstract(modifiers);
boolean isInterface = Modifier.isInterface(modifiers);

// 继承关系
Class<?> superclass = clazz.getSuperclass();
Class<?>[] interfaces = clazz.getInterfaces();

// 包
Package pkg = clazz.getPackage();
String packageName = pkg.getName();
```

### Constructor

```java
import java.lang.reflect.Constructor;

// 获取所有构造器
Constructor<?>[] constructors = String.class.getConstructors();

// 获取指定构造器
try {
    Constructor<String> constructor = String.class.getConstructor(byte[].class);
} catch (NoSuchMethodException e) {
    e.printStackTrace();
}

// 创建实例
try {
    Constructor<String> constructor = String.class.getConstructor(byte[].class);
    String str = constructor.newInstance("Hello".getBytes());
} catch (Exception e) {
    e.printStackTrace();
}
```

### Field

```java
import java.lang.reflect.Field;

class Person {
    private String name;
    public int age;
}

// 获取字段
Field[] fields = Person.class.getDeclaredFields();

// 获取公共字段
Field[] publicFields = Person.class.getFields();

// 获取指定字段
try {
    Field nameField = Person.class.getDeclaredField("name");
    Field ageField = Person.class.getField("age");

    // 访问控制
    nameField.setAccessible(true);  // 暴力反射

    // 获取/设置值
    Person person = new Person();
    nameField.set(person, "Alice");
    ageField.set(person, 25);

    // 获取值
    String name = (String) nameField.get(person);
    int age = (int) ageField.get(person);
} catch (Exception e) {
    e.printStackTrace();
}
```

### Method

```java
import java.lang.reflect.Method;

// 获取方法
Method[] methods = String.class.getDeclaredMethods();

// 获取指定方法
try {
    Method method = String.class.getMethod("substring", int.class, int.class);

    // 调用方法
    String str = "Hello, World!";
    String result = (String) method.invoke(str, 0, 5);  // "Hello"

    // 获取返回类型
    Class<?> returnType = method.getReturnType();

    // 获取参数类型
    Class<?>[] parameterTypes = method.getParameterTypes();
} catch (Exception e) {
    e.printStackTrace();
}
```

### Array 反射

```java
import java.lang.reflect.Array;

// 创建数组
String[] array = (String[]) Array.newInstance(String.class, 10);

// 获取/设置元素
Array.set(array, 0, "Hello");
String element = (String) Array.get(array, 0);

// 获取数组长度
int length = Array.getLength(array);

// 多维数组
int[][] matrix = (int[][]) Array.newInstance(int.class, 3, 4);
```

---

## JDK 5 - Annotations (JSR 175)

### 定义注解

```java
// 标记注解
public @interface MyAnnotation {
}

// 单值注解
public @interface Author {
    String value();
}

// 完整注解
public @interface UserInfo {
    String name();
    int age() default 18;
    String[] roles();
}

// 元注解
@Retention(RetentionPolicy.RUNTIME)
@Target({ElementType.TYPE, ElementType.METHOD})
@Documented
@Inherited
public @interface MyAnnotation {
}
```

### 元注解

| 元注解 | 说明 |
|--------|------|
| @Retention | 注解保留策略 (SOURCE/CLASS/RUNTIME) |
| @Target | 注解目标 (TYPE/FIELD/METHOD 等) |
| @Documented | 包含在 Javadoc 中 |
| @Inherited | 自动继承 |

### 读取注解

```java
@Author("Alice")
@UserInfo(name = "Bob", age = 25, roles = {"admin", "user"})
public class MyClass {

    @Author("Charlie")
    public void myMethod() {}
}

// 读取类注解
Class<?> clazz = MyClass.class;

Author author = clazz.getAnnotation(Author.class);
if (author != null) {
    System.out.println(author.value());  // Alice
}

UserInfo userInfo = clazz.getAnnotation(UserInfo.class);
if (userInfo != null) {
    System.out.println(userInfo.name());    // Bob
    System.out.println(userInfo.age());     // 25
    System.out.println(Arrays.toString(userInfo.roles()));
}

// 读取方法注解
Method method = clazz.getMethod("myMethod");
Author methodAuthor = method.getAnnotation(Author.class);

// 获取所有注解
Annotation[] annotations = clazz.getAnnotations();
```

---

## JDK 6 - Pluggable Annotation Processing

### 注解处理器

```java
import javax.annotation.processing.*;
import javax.lang.model.SourceVersion;
import javax.lang.model.element.*;
import javax.tools.Diagnostic;

@SupportedAnnotationTypes("com.example.*")
@SupportedSourceVersion(SourceVersion.RELEASE_6)
public class MyProcessor extends AbstractProcessor {

    @Override
    public boolean process(Set<? extends TypeElement> annotations,
                          RoundEnvironment roundEnv) {

        for (TypeElement annotation : annotations) {
            for (Element element : roundEnv.getElementsAnnotatedWith(annotation)) {
                processingEnv.getMessager().printMessage(
                    Diagnostic.Kind.NOTE,
                    "Found annotation: " + element);
            }
        }

        return true;
    }
}
```

---

## JDK 7 - MethodHandle (JSR 292)

### MethodHandle 基础

```java
import java.lang.invoke.*;

// MethodHandle - 方法句柄 (比反射更快)
public class MethodHandleExample {

    public void hello() {
        System.out.println("Hello!");
    }

    public static void main(String[] args) throws Throwable {
        MethodHandleExample obj = new MethodHandleExample();

        // 创建 Lookup
        MethodHandles.Lookup lookup = MethodHandles.lookup();

        // 获取方法句柄
        MethodHandle handle = lookup.findVirtual(
            MethodHandleExample.class,
            "hello",
            MethodType.methodType(void.class)
        );

        // 调用方法
        handle.invoke(obj);

        // 静态方法
        MethodHandle staticHandle = lookup.findStatic(
            MethodHandleExample.class,
            "staticMethod",
            MethodType.methodType(void.class)
        );

        // 构造器
        MethodHandle constructor = lookup.findConstructor(
            MethodHandleExample.class,
            MethodType.methodType(void.class)
        );
        MethodHandleExample instance = (MethodHandleExample) constructor.invoke();
    }
}
```

### CallSite

```java
// CallSite - 调用站点
import java.lang.invoke.*;

public class CallSiteExample {
    public static void main(String[] args) throws Throwable {
        MethodHandles.Lookup lookup = MethodHandles.lookup();
        MethodType methodType = MethodType.methodType(void.class);

        // 创建 CallSite
        ConstantCallSite callSite = new ConstantCallSite(
            lookup.findStatic(CallSiteExample.class, "target", methodType)
        );

        MethodHandle handle = callSite.dynamicInvoker();
        handle.invoke();
    }

    private static void target() {
        System.out.println("Target method");
    }
}
```

---

## JDK 8 - Lambda 和 invokedynamic

### Lambda 实现

```java
// Lambda 使用 invokedynamic 实现
// 编译时:
// 1. 生成 lambda 表达式的静态方法
// 2. 生成 invokedynamic 指令
// 3. 运行时调用 LambdaMetafactory.metafactory()

Function<String, String> f = s -> s.toUpperCase();

// 等价于:
// invokedynamic invokestatic "apply" ()Ljava/lang/Object;
```

### LambdaMetafactory

```java
import java.lang.invoke.*;
import java.util.function.*;

public class LambdaMetafactoryExample {

    public static void main(String[] args) throws Throwable {
        MethodHandles.Lookup lookup = MethodHandles.lookup();

        MethodType methodType = MethodType.methodType(
            Object.class,
            Object.class
        );

        CallSite callSite = LambdaMetafactory.metafactory(
            lookup,
            "apply",
            MethodType.methodType(Function.class),
            methodType,
            lookup.findStatic(
                LambdaMetafactoryExample.class,
                "toUpperCase",
                methodType
            ),
            methodType
        );

        Function<String, String> function =
            (Function<String, String>) callSite.getTarget().invoke();
        System.out.println(function.apply("hello"));  // HELLO
    }

    private static String toUpperCase(Object obj) {
        return ((String) obj).toUpperCase();
    }
}
```

---

## JDK 8 - 反射增强

### Parameter 反射

```java
import java.lang.reflect.Parameter;

// 获取方法参数名 (需要编译时 -parameters 参数)
public class ParameterExample {
    public void method(String name, int age) {}

    public static void main(String[] args) throws Exception {
        Method method = ParameterExample.class
            .getDeclaredMethod("method", String.class, int.class);

        Parameter[] parameters = method.getParameters();

        for (Parameter parameter : parameters) {
            System.out.println("Name: " + parameter.getName());
            System.out.println("Type: " + parameter.getType());
            System.out.println("Modifiers: " + parameter.getModifiers());
        }
    }
}
```

---

## JDK 11 - Constable 和 ConstantDesc

### Constable 接口

```java
// Constable - 可转换为常量描述
public interface Constable {
    Optional<? extends ConstantDesc> describeConstable();
}

// 实现 Constable 的类型
// - String
// - Integer, Long, Double 等包装类
// - Enum
// - Class

// 使用
String str = "Hello";
Optional<ConstantDesc> desc = str.describeConstable();
```

### ConstantDesc

```java
// ConstantDesc - 常量描述
public interface ConstantDesc {
    ConstantDesc resolveConstantDesc(MethodHandles.Lookup lookup)
        throws ReflectiveOperationException;
}

// 实现 ConstantDesc 的类型
// - String (通过 ConstantDescs)
// - Integer, Long 等
// - ClassDesc
// - MethodTypeDesc
// - DynamicConstantDesc
```

---

## JDK 16 - ClassFile API

### ClassFile API (预览)

```java
import java.lang.classfile.*;
import java.lang.classfile.instruction.*;

// 读取类文件
ClassModel classModel = ClassFile.of().parse(
    Paths.get("MyClass.class").toByteArray()
);

// 遍历方法
for (MethodModel method : classModel.methods()) {
    System.out.println("Method: " + method.methodName());

    // 遍历字节码
    for (CodeModel code : method.code().orElse(List.of())) {
        for (Instruction instruction : code) {
            System.out.println("  " + instruction);
        }
    }
}
```

---

## JDK 26 - Mirror API

### Mirror API (反射现代化)

```java
// Mirror API - 反射 API 的现代化替代
// 提供更好的性能和安全性

// 访问类
ClassDesc desc = ClassDesc.of("java.lang.String");

// 访问方法
MethodTypeDesc mt = MethodTypeDesc.of(
    ClassDesc.of("java.lang.String"),
    ClassDesc.of("int"),
    ClassDesc.of("int")
);

// 动态访问
MethodHandle handle = MethodHandles.lookup()
    .findVirtual(String.class, "substring",
        MethodType.methodType(String.class, int.class, int.class));
```

---

## 反射性能优化

### 缓存反射对象

```java
// ✅ 推荐: 缓存反射对象
public class ReflectionCache {
    private static final Map<Class<?>, Map<String, Field>> FIELD_CACHE =
        new ConcurrentHashMap<>();

    public static Field getField(Class<?> clazz, String fieldName) {
        return FIELD_CACHE
            .computeIfAbsent(clazz, k -> new HashMap<>())
            .computeIfAbsent(fieldName, name -> {
                try {
                    Field field = clazz.getDeclaredField(name);
                    field.setAccessible(true);
                    return field;
                } catch (NoSuchFieldException e) {
                    throw new RuntimeException(e);
                }
            });
    }
}

// ❌ 避免: 每次都查找
public class NoCache {
    public Object getValue(Object obj, String fieldName) throws Exception {
        Field field = obj.getClass().getDeclaredField(fieldName);
        field.setAccessible(true);
        return field.get(obj);
    }
}
```

### 使用 MethodHandle

```java
// MethodHandle 比反射快
public class MethodHandleBenchmark {

    private static final MethodHandle HANDLE;

    static {
        try {
            HANDLE = MethodHandles.lookup().findVirtual(
                String.class,
                "toLowerCase",
                MethodType.methodType(String.class)
            );
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    // 直接调用 (最快)
    public static String direct(String str) {
        return str.toLowerCase();
    }

    // MethodHandle (快)
    public static String methodHandle(String str) throws Throwable {
        return (String) HANDLE.invoke(str);
    }

    // 反射 (慢)
    public static String reflection(String str) throws Exception {
        Method method = String.class.getMethod("toLowerCase");
        return (String) method.invoke(str);
    }
}
```

---

## 反射选择指南

| 场景 | 推荐 | 说明 |
|------|------|------|
| 简单反射 | 反射 API | 简单易用 |
| 高频调用 | MethodHandle | 性能更好 |
| Lambda | invokedynamic | 编译器自动处理 |
| 字节码操作 | ClassFile API | JDK 16+ |
| 注解处理 | Annotation Processor | 编译时处理 |

---

## 时间线总结

| 版本 | 特性 | 说明 |
|------|------|------|
| JDK 1.0 | 反射 API | Class, Field, Method, Constructor |
| JDK 5 | Annotations | 注解支持 (JSR 175) |
| JDK 6 | Pluggable Annotation Processing | 注解处理器 |
| JDK 7 | MethodHandle | 方法句柄 (JSR 292) |
| JDK 8 | Lambda invokedynamic | Lambda 实现机制 |
| JDK 8 | Parameter 反射 | 方法参数名反射 |
| JDK 11 | Constable/ConstantDesc | 常量描述 |
| JDK 16 | ClassFile API | 字节码操作 |
| JDK 26 | Mirror API | 反射现代化 |

---

## 相关链接

- [Reflection Tutorial](https://docs.oracle.com/javase/tutorial/reflect/)
- [MethodHandle (JSR 292)](https://docs.oracle.com/javase/8/docs/api/java/lang/invoke/package-summary.html)
- [Annotations (JSR 175)](https://jcp.org/en/jsr/detail?id=175)
