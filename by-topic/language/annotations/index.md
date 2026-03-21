# 注解

> 注解声明、注解处理器、类型注解演进历程

[← 返回语言特性](../)

---
## 目录

1. [快速概览](#1-快速概览)
2. [核心贡献者](#2-核心贡献者)
3. [内置注解](#3-内置注解)
4. [自定义注解](#4-自定义注解)
5. [注解处理器 (JSR 269)](#5-注解处理器-jsr-269)
6. [可重复注解 (JDK 8+)](#6-可重复注解-jdk-8)
7. [类型注解 (JSR 308)](#7-类型注解-jsr-308)
8. [注解模式匹配 (JDK 21+)](#8-注解模式匹配-jdk-21)
9. [常用注解](#9-常用注解)
10. [注解反射](#10-注解反射)
11. [重要 PR 分析](#11-重要-pr-分析)
12. [注解性能最佳实践](#12-注解性能最佳实践)
13. [相关链接](#13-相关链接)

---


## 1. 快速概览

```
JDK 1.0 ── JDK 5 ── JDK 6 ── JDK 8 ── JDK 16 ── JDK 21 ── JDK 23
   │         │        │        │        │        │        │
Javadoc   注解    注解    类型注解  Record   注解    注解
标签    JSR 175  处理器  可重复注解  支持    模式    增强
         @Override  JSR   JSR 308   @Target  匹配
         @Deprecated  269  @Repeatable       for
         @SuppressWarnings                 instanceof
```

### 核心演进

| 版本 | 特性 | 说明 | JSR/JEP |
|------|------|------|---------|
| **JDK 1.0** | Javadoc | 文档注释 | - |
| **JDK 5** | 注解 | @Override, @Deprecated | JSR 175 |
| **JDK 6** | 注解处理器 | Pluggable Annotation Processing | JSR 269 |
| **JDK 8** | 类型注解 | Type Use | JSR 308 |
| **JDK 8** | 可重复注解 | @Repeatable | - |
| **JDK 16** | Record 支持 | @Target(RECORD_COMPONENT) | - |
| **JDK 21** | 注解模式匹配 | for instanceof, switch | JEP 441 |

---

## 2. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 注解/处理器团队 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Joe Darcy | 30 | Oracle | 注解, 类型系统 |
| 2 | [Jan Lahoda](/by-contributor/profiles/jan-lahoda.md) | 18 | Oracle | 注解处理器 |
| 3 | Pavel Rappo | 10 | Oracle | API 设计 |
| 4 | Jonathan Gibbons | 10 | Oracle | Javadoc, 注解 |
| 5 | Vicente Romero | 6 | Oracle | javac 编译器 |
| 6 | Jim Laskey | 4 | Oracle | 字符串模板 |
| 7 | Aggelos Biboudis | 3 | Oracle | 模式匹配 |

---

## 3. 内置注解

### java.lang 注解

```java
@Override          // 重写父类方法
public String toString() {
    return "Example";
}

@Deprecated        // 已弃用
public void oldMethod() {}

@SuppressWarnings("unchecked")  // 抑制警告
public void genericMethod() {}

@FunctionalInterface  // 函数式接口 (JDK 8+)
public interface Runnable {
    void run();
}
```

### 类型注解 (JDK 8+)

```java
import java.lang.annotation.ElementType;
import java.lang.annotation.Target;

@Target({ElementType.TYPE_USE})
@interface NonNull {}

// 类型注解
List<@NonNull String> list = new ArrayList<>();
myMethod((@NonNull String) str);
```

---

## 4. 自定义注解

### 声明注解

```java
import java.lang.annotation.*;

@Retention(RetentionPolicy.RUNTIME)  // 运行时保留
@Target(ElementType.TYPE)             // 用于类、接口
public @interface MyAnnotation {
    String value() default "";
    int count() default 0;
    String[] tags() default {};
}
```

### Retention 策略

| 策略 | 说明 | 用途 |
|------|------|------|
| **SOURCE** | 源码保留，编译丢弃 | @Override |
| **CLASS** | 编译保留，JVM 丢弃 | 字节码生成 |
| **RUNTIME** | 运行时保留 | 反射读取 |

### Target 类型

```java
@Target({
    ElementType.TYPE,           // 类、接口、枚举
    ElementType.FIELD,          // 字段
    ElementType.METHOD,         // 方法
    ElementType.PARAMETER,      // 参数
    ElementType.CONSTRUCTOR,    // 构造器
    ElementType.LOCAL_VARIABLE, // 局部变量
    ElementType.ANNOTATION_TYPE,// 注解类型
    ElementType.PACKAGE,        // 包
    ElementType.TYPE_PARAMETER, // 类型参数 (JDK 8+)
    ElementType.TYPE_USE,       // 类型使用 (JDK 8+)
    ElementType.RECORD_COMPONENT, // Record 组件 (JDK 16+)
    ElementType.MODULE          // 模块 (JDK 9+)
})
```

---

## 5. 注解处理器 (JSR 269)

### 创建处理器

```java
import javax.annotation.processing.*;
import javax.lang.model.SourceVersion;
import javax.lang.model.element.*;
import java.util.Set;

@SupportedAnnotationTypes("com.example.MyAnnotation")
@SupportedSourceVersion(SourceVersion.RELEASE_21)
public class MyProcessor extends AbstractProcessor {

    @Override
    public boolean process(Set<? extends TypeElement> annotations,
                          RoundEnvironment roundEnv) {
        for (TypeElement annotation : annotations) {
            for (Element element : roundEnv.getElementsAnnotatedWith(annotation)) {
                // 处理注解
                processingEnv.getMessager().printMessage(
                    Diagnostic.Kind.NOTE,
                    "Processing: " + element);
            }
        }
        return true;
    }
}
```

### 注册处理器

```bash
# META-INF/services/javax.annotation.processing.Processor
com.example.MyProcessor
```

### 编译时处理

```bash
# 编译并运行处理器
javac -processor com.example.MyProcessor \
    -cp processor.jar \
    source/Main.java
```

---

## 6. 可重复注解 (JDK 8+)

### @Repeatable

```java
import java.lang.annotation.*;

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface Roles {
    Role[] value();
}

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
@Repeatable(Roles.class)
public @interface Role {
    String value();
}

// 使用
@Role("admin")
@Role("user")
public class User {}
```

### 运行时读取

```java
Roles roles = User.class.getAnnotation(Roles.class);
for (Role role : roles.value()) {
    System.out.println(role.value());
}

// 或直接获取多个
Role[] rolesArray = User.class.getAnnotationsByType(Role.class);
```

---

## 7. 类型注解 (JSR 308)

### 类型注解用途

```java
import java.lang.annotation.*;

@Target(ElementType.TYPE_USE)
@interface NonNull {}
@Target(ElementType.TYPE_USE)
@interface Nullable {}

// 泛型类型
Map<@NonNull String, @Nullable Object> map;

// 类型转换
String str = (@NonNull String) obj;

// 继承
class MyClass extends @NonNull ArrayList<@NonNull String> {}

// 异常
void method() throws @NonNull Exception {}

// 创建
new @NonNull ArrayList<@NonNull String>();

// 类型参数
<@NonNull T> void genericMethod(T t) {}

// 数组
String @NonNull [] array;
```

### Checker Framework

```bash
# 类型检查
javac -processor org.checkerframework.checker.nullness.NullnessChecker \
    MyFile.java
```

---

## 8. 注解模式匹配 (JDK 21+)

### JEP 441: Pattern Matching

```java
// 注解模式匹配
sealed interface Shape permits Circle, Rectangle {}

@record class Circle(double radius) {}
@record class Rectangle(double width, double height) {}

// switch 中匹配注解
String format(Shape shape) {
    return switch (shape) {
        case Circle(var radius) -> "Circle: " + radius;
        case Rectangle(var w, var h) -> "Rect: " + w + "x" + h;
    };
}

// instanceof 模式匹配
if (obj instanceof Circle(double radius)) {
    System.out.println("Radius: " + radius);
}
```

---

## 9. 常用注解

### Lombok 风格注解

```java
@Data                    // Getter, Setter, equals, hashCode, toString
@AllArgsConstructor       // 全参构造器
@NoArgsConstructor        // 无参构造器
@Builder                 // 建造者模式
@Value                   // 不可变类
@Slf4j                   // 日志
```

### Spring 注解

```java
@Component              // 组件
@Service                // 服务
@Repository             // 仓库
@Controller             // 控制器
@Autowired              // 自动装配
@RequestMapping         // 请求映射
@GetMapping             // GET 映射
@PostMapping            // POST 映射
```

### JPA 注解

```java
@Entity                  // 实体
@Table                   // 表映射
@Id                     // 主键
@GeneratedValue         // 生成策略
@Column                 // 列映射
@OneToMany              // 一对多
@ManyToOne              // 多对一
```

---

## 10. 注解反射

### 读取注解

```java
import java.lang.annotation.*;
import java.lang.reflect.*;

// 类注解
MyAnnotation annotation = MyClass.class.getAnnotation(MyAnnotation.class);

// 所有注解
Annotation[] annotations = MyClass.class.getAnnotations();

// 方法注解
Method method = MyClass.class.getMethod("myMethod");
MyAnnotation methodAnnotation = method.getAnnotation(MyAnnotation.class);

// 参数注解
Parameter[] parameters = method.getParameters();
for (Parameter param : parameters) {
    MyAnnotation paramAnnotation = param.getAnnotation(MyAnnotation.class);
}

// 字段注解
Field field = MyClass.class.getDeclaredField("myField");
MyAnnotation fieldAnnotation = field.getAnnotation(MyAnnotation.class);
```

### 运行时处理注解

```java
public class AnnotationProcessor {
    public static void process(Class<?> clazz) {
        // 检查类注解
        if (clazz.isAnnotationPresent(MyAnnotation.class)) {
            MyAnnotation annotation = clazz.getAnnotation(MyAnnotation.class);
            System.out.println("Value: " + annotation.value());
            System.out.println("Count: " + annotation.count());
        }

        // 处理方法
        for (Method method : clazz.getDeclaredMethods()) {
            if (method.isAnnotationPresent(MyAnnotation.class)) {
                // 处理方法注解
            }
        }
    }
}
```

---

## 11. 重要 PR 分析

### 注解处理器性能优化

#### JDK-8341859: ClassFile Benchmark 优化

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐⭐ 测试稳定性提升 63%

通过缓存方法名减少基准测试中的噪声：

**优化点**:
- 静态初始化时预生成所有方法名
- 避免基准测试期间的字符串拼接
- 减少内存分配

**效果**:
- 标准差：2.34% → 0.87%（-62.8%）
- 95% CI 半宽：±4.6% → ±1.7%（-63%）

→ [详细分析](/by-pr/8341/8341859.md)

### 字节码生成优化

#### JDK-8341906: BufWriter 写入合并

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐ +28% 字节码写入性能

优化注解处理器生成的字节码写入性能：

**优化策略**: 将多次小写入合并为一次大写入

```java
// 优化前：3 次方法调用
buf.writeU1(u1Value);
buf.writeU2(u2Value);
buf.writeU4(u4Value);

// 优化后：1 次方法调用
buf.writeU1U2U4(u1Value, u2Value, u4Value);
```

→ [详细分析](/by-pr/8341/8341906.md)

---

## 12. 注解性能最佳实践

### Retention 策略选择

| 策略 | 性能影响 | 推荐场景 |
|------|----------|----------|
| **SOURCE** | 无运行时开销 | 编译期检查（@Override） |
| **CLASS** | 轻微字节码开销 | 字节码工具 |
| **RUNTIME** | 反射开销 | 运行时处理 |

```java
// ✅ 推荐：使用最弱的 Retention 策略
@Retention(RetentionPolicy.SOURCE)  // 编译后丢弃
@interface CompileTimeCheck {}

// ❌ 避免：不必要的 RUNTIME 策略
@Retention(RetentionPolicy.RUNTIME)  // 增加类文件大小
@interface SimpleMarker {}
```

### 注解处理器优化

```java
// ✅ 推荐：缓存 Elements
private static final Map<String, Element> CACHE = new HashMap<>();

@Override
public boolean process(Set<? extends TypeElement> annotations,
                      RoundEnvironment roundEnv) {
    for (Element element : roundEnv.getRootElements()) {
        String key = element.getSimpleName().toString();
        CACHE.putIfAbsent(key, element);
    }
    return false;
}
```

---

## 13. 相关链接

### 本地文档

- [反射](../reflection/) - 注解反射
- [语法演进](../syntax/) - 注解语法
- [Record](../record/) - 注解支持

### 外部参考

**JSR 文档:**
- [JSR 175: A Metadata Facility for Java](https://jcp.org/en/jsr/detail?id=175)
- [JSR 269: Pluggable Annotation Processing API](https://jcp.org/en/jsr/detail?id=269)
- [JSR 308: Annotations on Java Types](https://jcp.org/en/jsr/detail?id=308)

**JEP 文档:**
- [JEP 441](/jeps/language/jep-441.md)
- [JEP 466](/jeps/tools/jep-466.md)
