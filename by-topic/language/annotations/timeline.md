# 注解与元编程时间线

Java 注解从 JDK 5 到 JDK 26 的演进，包括注解处理器、编译期元编程。

---

## 时间线概览

```
JDK 5 ──── JDK 6 ──── JDK 7 ──── JDK 8 ──── JDK 16 ──── JDK 17 ──── JDK 21 ──── JDK 26
 │           │           │           │           │           │           │           │
 注解引入    APT        类型注解    重复注解    @Sniffer   模式匹配    可重复    注解增强
 JSR 175    JSR 269    JSR 308    @Repeatable  API        Sealed     注解      可见性
```

---

## 时间线详情

### JDK 5 (2004) - 注解引入 (JSR 175)

**JSR 175** - **Joshua Bloch** (Specification Lead, Sun Microsystems)

#### 基础注解

```java
// 定义注解
public @interface MyAnnotation {
    String value();
    String[] authors() default "unknown";
    int version() default 1;
}

// 使用注解
@MyAnnotation(
    value = "Example",
    authors = {"Alice", "Bob"},
    version = 2
)
public class MyClass {
    // ...
}
```

#### 内置注解

```java
// @Override - 重写父类方法
@Override
public String toString() {
    return "Example";
}

// @Deprecated - 标记过时
@Deprecated
public void oldMethod() {
    // ...
}

// @SuppressWarnings - 抑制警告
@SuppressWarnings("unchecked")
List<String> list = (List<String>) object;
```

#### 元注解

```java
// @Target - 注解目标
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
    ElementType.TYPE_USE        // 类型使用 (JDK 8+)
})

// @Retention - 注解保留策略
@Retention(RetentionPolicy.SOURCE)    // 源码级，编译后丢弃
@Retention(RetentionPolicy.CLASS)     // 编译级，JVM 加载后丢弃 (默认)
@Retention(RetentionPolicy.RUNTIME)   // 运行时，可通过反射获取

// @Documented - 生成 Javadoc 时包含
@Documented

// @Inherited - 允许子类继承
@Inherited
```

### JDK 6 (2006) - 注解处理器 (JSR 269)

**JSR 269** - **Joseph D. Darcy** (Specification Lead, Sun Microsystems)

#### Pluggable Annotation Processing API

```java
// 定义注解处理器
@SupportedAnnotationTypes("com.example.*")
@SupportedSourceVersion(SourceVersion.RELEASE_6)
public class MyProcessor extends AbstractProcessor {

    @Override
    public boolean process(Set<? extends TypeElement> annotations,
                          RoundEnvironment roundEnv) {
        for (TypeElement annotation : annotations) {
            for (Element element : roundEnv.getElementsAnnotatedWith(annotation)) {
                // 处理注解元素
                processElement(element);
            }
        }
        return true;
    }

    private void processElement(Element element) {
        // 生成代码
        generateCode(element);
    }
}
```

#### 使用注解处理器

```bash
# 编译时指定处理器
javac -processor com.example.MyProcessor MyClass.java

# 或通过服务发现机制
# META-INF/services/javax.annotation.processing.Processor
# com.example.MyProcessor
# com.example.AnotherProcessor
```

#### apt 工具

```bash
# apt 工具 (JDK 6-8，JDK 8 后废弃，使用 javac)
apt -factory com.example.MyFactory MyClass.java

# apt 在 JDK 8 后被 javac 取代
javac -processor com.example.MyProcessor MyClass.java
```

### JDK 7 (2011) - 类型注解 (JSR 308)

#### 类型注解

```java
// JDK 8 开始支持
// 类型注解可以用于任何类型使用

// 泛型参数
List<@NonNull String> strings;

// 类型转换
String s = (@NonNull String) object;

// 类型实例创建
new @NonNull ArrayList<>();

// 异常
void method() throws @NonNull Exception {};

// 继承
class MyClass extends @NonNull BaseClass {}

// 类型边界
class MyClass<T extends @NonNull Object> {}

// 数组
String @NonNull [] array;

// 接收器
class MyClass {
    void method(@NonNull MyClass this) { }
}
```

### JDK 8 (2014) - 重复注解与类型注解

**JSR 308** - **Michael Ernst**, **Alex Buckley** (Specification Leads), **Werner Dietl** (Implementation Lead)

#### 重复注解

```java
// 定义可重复注解
@Repeatable(Schedules.class)
public @interface Schedule {
    String day();
    String time();
}

// 容器注解
public @interface Schedules {
    Schedule[] value();
}

// 使用重复注解
@Schedule(day = "Monday", time = "10:00")
@Schedule(day = "Wednesday", time = "14:00")
@Schedule(day = "Friday", time = "16:00")
public void meeting() {
    // ...
}

// 反射获取重复注解
Schedule[] schedules = method.getAnnotationsByType(Schedule.class);
```

#### 类型注解示例

```java
// 定义类型注解
@Target({ElementType.TYPE_USE})
@Retention(RetentionPolicy.RUNTIME)
public @interface NonNull {
}

// 使用类型注解
public class Example {
    // 参数类型
    public void process(@NonNull String input) {
        // 变量类型
        @NonNull String result = input.toUpperCase();
    }

    // 返回类型
    public @NonNull String getValue() {
        return "value";
    }

    // 泛型
    List<@NonNull String> getList() {
        return new ArrayList<>();
    }
}
```

### JDK 16 - Sniffer API

```java
// @Sniffer API - 用于检测平台特定特性
// 预览功能，后续 JDK 移除

@Target(ElementType.METHOD)
@Retention(RetentionPolicy.SOURCE)
public @interface Sniffer {
    String value();
}
```

### JDK 17 - Sealed Classes 与注解

```java
// Sealed Classes 配合注解
@Sealed({
    Circle.class,
    Rectangle.class
})
public abstract sealed class Shape {
    // ...
}

// 注解处理器支持 Sealed Classes
@SupportedAnnotationTypes("com.example.*")
public class ShapeProcessor extends AbstractProcessor {
    @Override
    public boolean process(Set<? extends TypeElement> annotations,
                          RoundEnvironment roundEnv) {
        // 处理 Sealed 类型
        for (Element element : roundEnv.getRootElements()) {
            if (element.getKind() == ElementKind.RECORD) {
                processRecord((TypeElement) element);
            }
        }
        return true;
    }
}
```

### JDK 21 - 模式匹配与注解

```java
// Record Patterns 配合注解
public record Point(@Positive int x, @Positive int y) {
    public Point {
        if (x < 0 || y < 0) {
            throw new IllegalArgumentException();
        }
    }
}

@Target(ElementType.TYPE_USE)
@Retention(RetentionPolicy.RUNTIME)
public @interface Positive {
}

// 模式匹配
if (obj instanceof Point(int x, int y)) {
    // x, y 都有 @Positive 注解约束
}
```

### JDK 26 - 注解增强

#### 可重复注解改进

```java
// 更灵活的可重复注解
@Repeatable(value = Tags.class, since = "26")
public @interface Tag {
    String value();
    String category() default "general";
}

// 注解可见性增强
public @interface Visibility {
    boolean publicAccess() default true;
    boolean moduleAccess() default true;
}
```

---

## 注解处理器实战

### Lombok 风格注解

```java
// @Getter 注解
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.SOURCE)
public @interface Getter {
}

// 注解处理器
@SupportedAnnotationTypes("com.example.Getter")
public class GetterProcessor extends AbstractProcessor {

    @Override
    public boolean process(Set<? extends TypeElement> annotations,
                          RoundEnvironment roundEnv) {
        for (Element element : roundEnv.getElementsAnnotatedWith(Getter.class)) {
            if (element.getKind() == ElementKind.CLASS) {
                generateGetters((TypeElement) element);
            }
        }
        return true;
    }

    private void generateGetters(TypeElement classElement) {
        // 获取包名
        String packageName = processingEnv.getElementUtils()
            .getPackageOf(classElement).getQualifiedName().toString();

        // 获取类名
        String className = classElement.getSimpleName().toString();

        // 获取字段
        List<VariableElement> fields = classElement.getEnclosedElements().stream()
            .filter(e -> e.getKind() == ElementKind.FIELD)
            .map(e -> (VariableElement) e)
            .collect(Collectors.toList());

        // 生成 getter 方法
        try (Writer writer = processingEnv.getFiler()
                .createSourceFile(packageName + "." + className + "Getters")
                .openWriter()) {

            writer.write("package " + packageName + ";\n\n");
            writer.write("public class " + className + "Getters {\n");

            for (VariableElement field : fields) {
                String fieldName = field.getSimpleName().toString();
                String fieldType = field.asType().toString();
                String methodName = "get" +
                    Character.toUpperCase(fieldName.charAt(0)) +
                    fieldName.substring(1);

                writer.write("    public " + fieldType + " " +
                    methodName + "() {\n");
                writer.write("        return this." + fieldName + ";\n");
                writer.write("    }\n\n");
            }

            writer.write("}\n");
        } catch (IOException e) {
            processingEnv.getMessager().printMessage(
                Diagnostic.Kind.ERROR, e.getMessage());
        }
    }
}
```

### 自动生成代码

```java
// Builder 模式注解
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.SOURCE)
public @interface Builder {
}

// 处理器生成 Builder 类
@SupportedAnnotationTypes("com.example.Builder")
public class BuilderProcessor extends AbstractProcessor {
    // 生成 Builder 代码
}

// 使用
@Builder
public class Person {
    private String name;
    private int age;
    private String email;
}

// 自动生成
public class PersonBuilder {
    private String name;
    private int age;
    private String email;

    public PersonBuilder name(String name) {
        this.name = name;
        return this;
    }

    public PersonBuilder age(int age) {
        this.age = age;
        return this;
    }

    public PersonBuilder email(String email) {
        this.email = email;
        return this;
    }

    public Person build() {
        return new Person(name, age, email);
    }
}
```

---

## 编译期元编程

### 符号 API

```java
// Element 表示程序元素
public interface Element {
    // 获取元素类型
    ElementKind getKind();

    // 获取注解
    <A extends Annotation> A getAnnotation(Class<A> annotationType);

    // 获取 enclosed elements
    List<? extends Element> getEnclosedElements();

    // 获取父元素
    Element getEnclosingElement();
}

// TypeElement 表示类型元素
public interface TypeElement extends Element {
    // 获取全限定名
    Name getQualifiedName();

    // 获取简单名称
    Name getSimpleName();

    // 获取类型参数
    List<? extends TypeParameterElement> getTypeParameters();
}

// VariableElement 表示字段、参数等
public interface VariableElement extends Element {
    // 获取常量值
    Object getConstantValue();
}
```

### 生成文件

```java
// 使用 Filer API 生成文件
Filer filer = processingEnv.getFiler();

// 生成 Java 源文件
JavaFileObject sourceFile = filer.createSourceFile(
    "com.example.GeneratedClass");

try (Writer writer = sourceFile.openWriter()) {
    writer.write("package com.example;\n\n");
    writer.write("public class GeneratedClass {\n");
    writer.write("    public static void hello() {\n");
    writer.write("        System.out.println(\"Hello!\");\n");
    writer.write("    }\n");
    writer.write("}\n");
}

// 生成资源文件
FileObject resourceFile = filer.createResource(
    StandardLocation.CLASS_OUTPUT,
    "",
    "META-INF/services/com.example.Service");

try (Writer writer = resourceFile.openWriter()) {
    writer.write("com.example.ServiceImpl\n");
}
```

---

## 常用注解处理器框架

### AutoValue

```java
// Google AutoValue - 自动生成值对象
@AutoValue
public abstract class Person {
    public abstract String name();
    public abstract int age();
    public abstract String email();

    public static Builder builder() {
        return new AutoValue_Person.Builder();
    }

    @AutoValue.Builder
    public abstract static class Builder {
        public abstract Builder name(String value);
        public abstract Builder age(int value);
        public abstract Builder email(String value);
        public abstract Person build();
    }
}
```

### AutoService

```java
// Google AutoService - 自动生成服务配置
@AutoService(Service.class)
public class ServiceImpl implements Service {
    // 自动生成 META-INF/services/com.example.Service
}
```

### Dagger 依赖注入

```java
// Dagger 使用注解处理器生成代码
@Module
public class AppModule {
    @Provides
    @Singleton
    public DataService provideDataService() {
        return new DataService();
    }
}

@Component(modules = AppModule.class)
@Singleton
public interface AppComponent {
    DataService dataService();
}

// 自动生成 DaggerAppComponent
```

---

## 最佳实践

### 注解设计

```java
// ✅ 推荐: 明确的 @Target
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface Transactional {
    Propagation value() default Propagation.REQUIRED;
}

// ✅ 推荐: 合理的默认值
public @interface Config {
    String value() default "";
    int timeout() default 30000;
    boolean enabled() default true;
}

// ❌ 避免: 过于复杂的注解
public @interface Complex {
    String[] values();
    Map<String, String> config();  // 不支持
    Class<?>[] classes();
}
```

### 注解处理器

```java
// ✅ 推荐: 增量编译支持
@SupportedAnnotationTypes("com.example.*")
@SupportedOptions({"debug", "verify"})
public class MyProcessor extends AbstractProcessor {
    @Override
    public Set<String> getSupportedOptions() {
        return Set.of("debug", "verify");
    }
}

// ✅ 推荐: 清晰的错误消息
processingEnv.getMessager().printMessage(
    Diagnostic.Kind.ERROR,
    "Invalid annotation on " + element.getSimpleName()
);
```

---

## 贡献者

### JSR 规范负责人

| JSR | 特性 | 规范负责人 | 公司 |
|-----|------|-----------|------|
| JSR 175 | 注解引入 | **Joshua Bloch** | Sun Microsystems |
| JSR 269 | 注解处理器 API | **Joseph D. Darcy** | Sun Microsystems |
| JSR 308 | 类型注解 | **Michael Ernst**, Alex Buckley | UW, Oracle |

### Joshua Bloch

- **职位**: Former Chief Java Architect, Sun Microsystems (2001-2008), later Google
- **代表作**: 《Effective Java》作者
- **主要贡献**:
  - JSR 175 Specification Lead (注解引入)
  - Java Collections Framework 设计
  - 作者多项 JSR 规范

> "Annotations are a metadata facility that allows classes, interfaces, fields, and methods to be marked as having particular attributes."
> — Joshua Bloch, JSR 175 Specification Lead

### Joseph D. Darcy

- **职位**: JDK Developer, Oracle (formerly Sun Microsystems)
- **背景**: Stanford University, Applied Mathematics (M.S., 2009)
- **主要贡献**:
  - JSR 269 Specification Lead (注解处理器 API)
  - Project Coin Lead (JDK 7 小型语言改进)
  - Java 浮点运算专家 ("Java Floating-Point Czar")
  - 20+ 年 JDK 核心库和编译器开发经验

### Michael Ernst

- **职位**: Professor, University of Washington (formerly MIT)
- **主要贡献**:
  - JSR 308 Specification Lead (类型注解)
  - Checker Framework 创始人
  - JavaOne 2009 "Java Rock Star" 获奖者
  - 20,000+ 引用的计算机科学研究员

### Alex Buckley

- **职位**: Java Language Specification Lead, Oracle
- **主要贡献**:
  - JSR 308 Co-Specification Lead
  - JLS (Java Language Specification) 维护者
  - 多个 JEP 规范审查者

### Werner Dietl

- **职位**: Implementation Lead, JSR 308
- **背景**: University of Washington
- **主要贡献**:
  - JSR 308 类型注解实现负责人
  - Checker Framework 核心开发者

---

## 相关 JEP

| JEP | 标题 | 版本 | 说明 |
|-----|------|------|------|
| [JSR 175](https://jcp.org/en/jsr/detail?id=175) | A Metadata Facility for the Java Programming Language | JDK 5 | 注解引入 |
| [JSR 269](https://jcp.org/en/jsr/detail?id=269) | Pluggable Annotation Processing API | JDK 6 | 注解处理器 |
| [JSR 308](https://jcp.org/en/jsr/detail?id=308) | Annotations on Java Types | JDK 8 | 类型注解 |

---

## 相关链接

- [Annotation Processing Tool](https://docs.oracle.com/en/java/javase/21/docs/specs/man/javac.html)
- [Package javax.annotation.processing](https://docs.oracle.com/en/java/javase/21/docs/api/java.compiler/javax/annotation/processing/package-summary.html)
- [Package javax.lang.model](https://docs.oracle.com/en/java/javase/21/docs/api/java.compiler/javax/lang/model/package-summary.html)
