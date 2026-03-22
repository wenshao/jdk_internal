# 注解

> 注解声明、注解处理器、类型注解演进历程

[← 返回语言特性](../)

---
## 目录

1. [快速概览](#1-快速概览)
2. [核心贡献者](#2-核心贡献者)
3. [内置注解](#3-内置注解)
4. [自定义注解](#4-自定义注解)
5. [注解处理器 (JSR 269 / APT)](#5-注解处理器-jsr-269--annotation-processing-tool-apt)
6. [可重复注解 (JDK 8+ / JEP 120)](#6-可重复注解-jdk-8--repeatable-annotations-jep-120)
7. [类型注解 (JSR 308 / JEP 104)](#7-类型注解-jsr-308--jep-104--type-annotations)
8. [注解模式匹配 (JDK 21+)](#8-注解模式匹配-jdk-21)
9. [元注解](#9-元注解-meta-annotations)
10. [常用标准注解](#10-常用标准注解-standard-annotations)
11. [运行时注解处理](#11-运行时注解处理-runtime-annotation-processing)
12. [重要 PR 分析](#12-重要-pr-分析)
13. [注解性能最佳实践](#13-注解性能最佳实践)
14. [相关链接](#14-相关链接)

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

## 5. 注解处理器 (JSR 269) / Annotation Processing Tool (APT)

> JSR 269 定义了 Pluggable Annotation Processing API，替代了早期 `com.sun.mirror` API。
> 核心包：`javax.annotation.processing`，核心类：`AbstractProcessor`。

### 处理器生命周期 (Processor Lifecycle)

```
                 ┌─────────────────────────────────────────┐
                 │              javac 编译器                │
                 │                                         │
 源码 ──────────►│  Round 1 ──► Round 2 ──► ... ──► Final  │──► .class
                 │  discover    process      process  done  │
                 │  processors  generated    generated       │
                 │              sources      sources         │
                 └─────────────────────────────────────────┘
```

- **多轮处理 (Multi-round processing)**: 每轮处理新生成的源文件，直到没有新文件产生
- **最终轮 (Final round)**: `RoundEnvironment.processingOver()` 返回 `true`
- **声明/返回语义**: `process()` 返回 `true` 表示"已消费"该注解，其他处理器不再处理

### 创建处理器

```java
import javax.annotation.processing.*;
import javax.lang.model.SourceVersion;
import javax.lang.model.element.*;
import javax.tools.Diagnostic;
import java.util.Set;

@SupportedAnnotationTypes("com.example.MyAnnotation")
@SupportedSourceVersion(SourceVersion.RELEASE_21)
public class MyProcessor extends AbstractProcessor {

    @Override
    public synchronized void init(ProcessingEnvironment processingEnv) {
        super.init(processingEnv);
        // processingEnv 提供四大工具：
        // - getMessager()    编译消息输出 (Compiler messages)
        // - getFiler()       文件创建 (Source/Class/Resource generation)
        // - getElementUtils() 元素工具 (Element utilities)
        // - getTypeUtils()   类型工具 (Type utilities)
    }

    @Override
    public boolean process(Set<? extends TypeElement> annotations,
                          RoundEnvironment roundEnv) {
        for (TypeElement annotation : annotations) {
            for (Element element : roundEnv.getElementsAnnotatedWith(annotation)) {
                processingEnv.getMessager().printMessage(
                    Diagnostic.Kind.NOTE,
                    "Processing: " + element);
            }
        }
        return true; // 声明已消费 (claimed)
    }
}
```

### 编译时代码生成 (Compile-time Code Generation)

```java
// 使用 Filer 生成新的 Java 源文件
@Override
public boolean process(Set<? extends TypeElement> annotations,
                      RoundEnvironment roundEnv) {
    for (Element element : roundEnv.getElementsAnnotatedWith(AutoValue.class)) {
        String className = element.getSimpleName() + "_Impl";
        String packageName = processingEnv.getElementUtils()
            .getPackageOf(element).getQualifiedName().toString();

        try {
            JavaFileObject file = processingEnv.getFiler()
                .createSourceFile(packageName + "." + className);
            try (var writer = file.openWriter()) {
                writer.write("package " + packageName + ";\n");
                writer.write("public class " + className + " { }\n");
            }
        } catch (IOException e) {
            processingEnv.getMessager().printMessage(
                Diagnostic.Kind.ERROR, e.getMessage(), element);
        }
    }
    return true;
}
```

### 注册处理器

```bash
# 方式 1: ServiceLoader — META-INF/services/javax.annotation.processing.Processor
com.example.MyProcessor

# 方式 2: 命令行指定
javac -processor com.example.MyProcessor \
    -cp processor.jar \
    source/Main.java

# 方式 3: 自动发现（默认行为）
# 编译器扫描 classpath 上所有 META-INF/services 注册的处理器
javac -cp processor.jar source/Main.java

# 禁用注解处理
javac -proc:none source/Main.java
```

---

## 6. 可重复注解 (JDK 8+) / Repeatable Annotations (JEP 120)

> JEP 120 引入 `@Repeatable` 元注解，允许同一注解在同一声明位置重复使用。
> 编译器自动将重复注解包装到容器注解 (Container Annotation) 中。

### 容器注解模式 (Container Annotation Pattern)

```java
import java.lang.annotation.*;

// 1. 容器注解 — 必须有 value() 方法返回注解数组
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface Roles {
    Role[] value();  // 必须命名为 value
}

// 2. 可重复注解 — @Repeatable 指向容器注解
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
@Repeatable(Roles.class)
public @interface Role {
    String value();
}

// 3. 使用：同一位置重复标注
@Role("admin")
@Role("user")
public class User {}

// 编译器实际生成等价形式：
// @Roles({@Role("admin"), @Role("user")})
// public class User {}
```

### 容器注解约束 (Container Constraints)

| 约束 | 说明 |
|------|------|
| `value()` 返回类型 | 必须是可重复注解的数组 |
| `@Retention` | 容器的保留策略 >= 可重复注解的保留策略 |
| `@Target` | 容器的目标范围 >= 可重复注解的目标范围 |
| `@Documented` | 若可重复注解有，则容器也必须有 |
| `@Inherited` | 若可重复注解有，则容器也必须有 |

### 运行时读取 — getAnnotation vs getAnnotationsByType

```java
// getAnnotation: 只返回容器注解 (Container)
Roles roles = User.class.getAnnotation(Roles.class);
if (roles != null) {
    for (Role role : roles.value()) {
        System.out.println(role.value());
    }
}

// getAnnotationsByType: 自动展开容器，直接返回可重复注解数组（推荐）
Role[] rolesArray = User.class.getAnnotationsByType(Role.class);
for (Role role : rolesArray) {
    System.out.println(role.value());  // "admin", "user"
}

// 注意：getAnnotation(Role.class) 返回 null（因为实际存储的是 @Roles）
Role single = User.class.getAnnotation(Role.class);  // null!
```

---

## 7. 类型注解 (JSR 308 / JEP 104) / Type Annotations

> JSR 308（对应 JEP 104）扩展了注解可出现的位置：从声明 (declarations) 扩展到类型使用 (type uses)。
> 核心目标：启用可插拔类型系统 (Pluggable Type Systems)，在编译期捕获更多错误。

### TYPE_USE 注解位置

```java
import java.lang.annotation.*;

@Target(ElementType.TYPE_USE)
@interface NonNull {}
@Target(ElementType.TYPE_USE)
@interface Nullable {}

// 泛型类型参数 (Generic type arguments)
Map<@NonNull String, @Nullable Object> map;

// 类型转换 (Type cast)
String str = (@NonNull String) obj;

// 继承/实现 (extends/implements)
class MyClass extends @NonNull ArrayList<@NonNull String> {}

// 异常声明 (throws)
void method() throws @NonNull Exception {}

// 对象创建 (new)
new @NonNull ArrayList<@NonNull String>();

// 类型参数边界 (Type parameter bounds)
<@NonNull T extends @Nullable Comparable<T>> void sort(List<T> list) {}

// 数组 — 注意位置含义不同
String @NonNull []   array1;  // 数组本身非空
@NonNull String []   array2;  // 数组元素非空
@NonNull String @NonNull [] array3;  // 两者都非空
```

### Checker Framework 与 @NonNull/@Nullable 生态

Checker Framework 是 TYPE_USE 注解的主要消费者，提供编译期空安全检查：

```bash
# 使用 Checker Framework 进行空值检查
javac -processor org.checkerframework.checker.nullness.NullnessChecker \
    -Astubs=stubs/ \
    MyFile.java
```

```java
import org.checkerframework.checker.nullness.qual.*;

public class SafeService {
    // 方法参数非空约束 — 编译期强制
    public String process(@NonNull String input) {
        return input.trim();  // 安全：编译器已保证 input != null
    }

    // 返回值可空声明
    public @Nullable String find(String key) {
        return map.get(key);  // 可能返回 null
    }

    // 编译错误示例：
    // String result = find("key").trim();
    //   ↑ error: dereference of possibly-null reference
}
```

**常见 TYPE_USE 注解生态对比**:

| 注解包 | 来源 | 特点 |
|--------|------|------|
| `org.checkerframework.checker.nullness.qual` | Checker Framework | 完整的可插拔类型系统 |
| `org.jetbrains.annotations` | JetBrains | IntelliJ IDEA 静态分析 |
| `jakarta.annotation` | Jakarta EE | 标准化，但仅限声明位置 |
| `org.eclipse.jdt.annotation` | Eclipse | ECJ 编译器支持 |

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

## 9. 元注解 (Meta-Annotations)

> 元注解是"注解的注解"，定义在 `java.lang.annotation` 包中，用于控制自定义注解的行为。

| 元注解 | 作用 | 引入版本 |
|--------|------|----------|
| `@Target` | 限制注解可出现的位置 (Applicable contexts) | JDK 5 |
| `@Retention` | 控制注解保留阶段 (SOURCE/CLASS/RUNTIME) | JDK 5 |
| `@Inherited` | 子类自动继承父类的类级注解 | JDK 5 |
| `@Documented` | 注解出现在 Javadoc 中 | JDK 5 |
| `@Repeatable` | 允许同一位置重复使用 (见第 6 节) | JDK 8 |

```java
// @Inherited 的继承语义
@Inherited
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
@interface Auditable {}

@Auditable
class BaseEntity {}

class UserEntity extends BaseEntity {}
// UserEntity.class.isAnnotationPresent(Auditable.class) → true
// 注意：仅对类继承生效，接口实现不继承
```

---

## 10. 常用标准注解 (Standard Annotations)

### java.lang 内置注解

| 注解 | 用途 | Retention | 说明 |
|------|------|-----------|------|
| `@Override` | 重写检查 | SOURCE | 编译器验证方法确实重写了父类方法 |
| `@Deprecated` | 弃用标记 | RUNTIME | JDK 9+ 增加 `forRemoval` 和 `since` |
| `@SuppressWarnings` | 抑制警告 | SOURCE | 支持 `"unchecked"`, `"deprecation"`, `"preview"` 等 |
| `@FunctionalInterface` | 函数式接口 | RUNTIME | 编译器验证恰好一个抽象方法 |
| `@SafeVarargs` | 可变参数安全 | RUNTIME | 抑制堆污染警告 (heap pollution) |

```java
// @Deprecated 增强 (JDK 9+)
@Deprecated(since = "17", forRemoval = true)
public void legacyMethod() {}
// since: 标注弃用起始版本
// forRemoval: true 表示将在未来版本移除，编译器产生更强警告

// @SuppressWarnings 常用值
@SuppressWarnings("unchecked")     // 未检查的泛型操作
@SuppressWarnings("deprecation")   // 使用已弃用 API
@SuppressWarnings("preview")       // 预览特性 (JDK 14+)
@SuppressWarnings({"unchecked", "rawtypes"})  // 多个值
```

### JDK 内部注解

| 注解 | 包 | 用途 |
|------|-----|------|
| `@CallerSensitive` | `jdk.internal.reflect` | 标记对调用者敏感的方法（如 `Class.forName`） |
| `@Stable` | `jdk.internal.vm.annotation` | 标记字段为稳定值，JIT 可常量折叠 |
| `@Contended` | `jdk.internal.vm.annotation` | 避免伪共享 (False sharing)，填充缓存行 |
| `@ForceInline` | `jdk.internal.vm.annotation` | 强制 JIT 内联 |

### 框架注解设计模式 (Framework Annotation Patterns)

#### Spring — 组件扫描与依赖注入

```java
// 组件层次 — @Component 的派生注解 (Stereotype annotations)
@Component              // 通用组件 (Generic component)
@Service                // 服务层 (Service layer)
@Repository             // 数据访问层 (DAO layer)，自动异常转换
@Controller             // MVC 控制器 (Web controller)

// 依赖注入 (Dependency Injection)
@Autowired              // 按类型注入 (By type)
@Qualifier("myBean")    // 按名称限定 (By qualifier)
@Primary                // 多候选时优先 (Primary candidate)
@Lazy                   // 延迟初始化 (Lazy initialization)

// 条件装配 (Conditional configuration)
@ConditionalOnProperty(name = "feature.enabled", havingValue = "true")
@ConditionalOnClass(DataSource.class)
@ConditionalOnMissingBean(MyService.class)
```

#### JPA / Hibernate — 对象关系映射

```java
@Entity                              // 实体类 → 数据库表
@Table(name = "users")               // 指定表名
@Id                                  // 主键
@GeneratedValue(strategy = IDENTITY) // 主键生成策略
@Column(name = "user_name",          // 列映射
        nullable = false, length = 50)
@OneToMany(mappedBy = "user",        // 一对多
           cascade = CascadeType.ALL,
           fetch = FetchType.LAZY)
@ManyToOne                           // 多对一
@JoinColumn(name = "user_id")       // 外键列
```

#### Bean Validation — 约束验证

```java
@Valid                   // 级联验证 (Cascaded validation)
@NotNull                 // 非空
@NotBlank                // 非空且非空白字符串
@Size(min = 2, max = 50) // 大小约束
@Email                   // 邮箱格式
@Pattern(regexp = "...")  // 正则匹配
@Min(0) @Max(100)        // 数值范围
```

---

## 11. 运行时注解处理 (Runtime Annotation Processing)

### AnnotatedElement API

> `java.lang.reflect.AnnotatedElement` 是所有可携带注解的反射元素的父接口。
> 实现类：`Class`, `Method`, `Field`, `Constructor`, `Parameter`, `Package`, `Module`。

| 方法 | 行为 | @Inherited | @Repeatable |
|------|------|------------|-------------|
| `getAnnotation(Class<A>)` | 返回指定类型的单个注解 | 考虑继承 | 返回 null（实际存的是容器） |
| `getAnnotations()` | 返回所有注解 | 考虑继承 | 返回容器注解 |
| `getDeclaredAnnotation(Class<A>)` | 仅当前元素声明的注解 | 不考虑 | 返回 null |
| `getDeclaredAnnotations()` | 仅当前元素声明的所有注解 | 不考虑 | 返回容器注解 |
| `getAnnotationsByType(Class<A>)` | 展开容器，返回数组 | 考虑继承 | **自动展开** |
| `getDeclaredAnnotationsByType(Class<A>)` | 展开容器，仅当前元素 | 不考虑 | **自动展开** |
| `isAnnotationPresent(Class<A>)` | 是否存在指定注解 | 考虑继承 | 对可重复注解返回 false |

```java
import java.lang.annotation.*;
import java.lang.reflect.*;

// 类注解
MyAnnotation annotation = MyClass.class.getAnnotation(MyAnnotation.class);

// 所有注解（含从父类 @Inherited 继承的）
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

### getAnnotation vs getAnnotationsByType 关键区别

```java
@Role("admin")
@Role("user")
class User {}

// getAnnotation — 查找精确类型，可重复注解存储为容器
User.class.getAnnotation(Role.class);   // null — 实际不存在单个 @Role
User.class.getAnnotation(Roles.class);  // @Roles({@Role("admin"), @Role("user")})

// getAnnotationsByType — 自动展开容器（推荐用于可重复注解）
User.class.getAnnotationsByType(Role.class);  // [@Role("admin"), @Role("user")]
```

### 运行时注解扫描实践

```java
public class AnnotationScanner {
    public static void process(Class<?> clazz) {
        // 检查类注解
        if (clazz.isAnnotationPresent(MyAnnotation.class)) {
            MyAnnotation annotation = clazz.getAnnotation(MyAnnotation.class);
            System.out.println("Value: " + annotation.value());
        }

        // 扫描方法注解
        for (Method method : clazz.getDeclaredMethods()) {
            if (method.isAnnotationPresent(MyAnnotation.class)) {
                MyAnnotation ma = method.getAnnotation(MyAnnotation.class);
                // 基于注解值执行逻辑
            }
        }

        // 扫描字段上的可重复注解
        for (Field field : clazz.getDeclaredFields()) {
            Constraint[] constraints =
                field.getAnnotationsByType(Constraint.class);
            for (Constraint c : constraints) {
                validate(field, c);
            }
        }
    }
}
```

---

## 12. 重要 PR 分析

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

## 13. 注解性能最佳实践

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

## 14. 相关链接

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
