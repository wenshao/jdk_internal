# jdk.compiler 模块分析

> Java 编译器 API，提供程序化编译和语言模型访问

---

## 1. 模块概述

`jdk.compiler` 包含 Java 编译器 (`javac`) 的 API，允许应用程序在运行时动态编译 Java 源代码。

### 模块定义

**文件**: `src/jdk.compiler/share/classes/module-info.java`

```java
module jdk.compiler {
    requires transitive java.xml;

    exports javax.tools;
    exports javax.tools.java6c.compiler;  // javac 内部 API (谨慎使用)

    exports com.sun.source.doctree;
    exports com.sun.source.javadoc;
    exports com.sun.source.tree;
    exports com.sun.source.util;
    exports com.sun.tools.javac;
    // ... 更多内部包
}
```

### 架构

```
┌─────────────────────────────────────────────────────────┐
│                     应用代码                              │
│  JavaCompiler / JavaFileObject / DiagnosticListener     │
├─────────────────────────────────────────────────────────┤
│                 javax.tools API                         │
│  (标准编译器 API)                                         │
├─────────────────────────────────────────────────────────┤
│                 com.sun.tools.javac                      │
│  (javac 实现)                                            │
├─────────────────────────────────────────────────────────┤
│              JavaFileManager / StandardJavaFileManager  │
├─────────────────────────────────────────────────────────┤
│                  文件系统                                │
└─────────────────────────────────────────────────────────┘
```

---

## 2. 核心 API

### 2.1 JavaCompiler

**源码**: `src/jdk.compiler/share/classes/javax/tools/JavaCompiler.java`

```java
public interface JavaCompiler extends OptionChecker, JavaFileManager {
    // 获取编译器实例
    static JavaCompiler getSystemJavaCompiler()

    // 编译任务
    CompilationTask getTask(
        Writer out,                           // 输出
        JavaFileManager fileManager,          // 文件管理器
        DiagnosticListener<? super JavaFileObject> diagnosticListener,  // 诊断监听
        Iterable<String> options,             // 编译选项
        Iterable<String> classes,             // 要编译的类
        Iterable<? extends JavaFileObject> compilationUnits  // 编译单元
    )

    // 标准文件管理器
    StandardJavaFileManager getStandardFileManager(
        DiagnosticListener<? super JavaFileObject> diagnosticListener,
        Locale locale,
        Charset charset
    )
}
```

### 2.2 JavaFileObject

**源码**: `src/jdk.compiler/share/classes/javax/tools/JavaFileObject.java`

```java
public interface JavaFileObject extends FileObject {
    enum Kind {
        SOURCE(".java"),    // 源文件
        CLASS(".class"),    // 类文件
        HTML(".html"),      // HTML 文档
        OTHER("");          // 其他
    }

    Kind getKind()
    NestingKind getNestingKind()
    boolean isNameCompatible(String simpleName, Kind kind)
}
```

### 2.3 CompilationTask

```java
public interface JavaCompiler.CompilationTask extends Callable<Boolean> {
    // 添加编译单元
    void addUnits(Iterable<? extends JavaFileObject> units)

    // 设置选项
    void setOptions(List<String> options)

    // 设置处理器
    void setProcessors(Iterable<? extends Processor> processors)

    // 设置监听器
    void setLocale(Locale locale)

    // 执行编译
    Boolean call()
}
```

---

## 3. 使用示例

### 3.1 基本编译

```java
JavaCompiler compiler = ToolProvider.getSystemJavaCompiler();

StandardJavaFileManager fm = compiler.getStandardFileManager(null, null, null);

Iterable<? extends JavaFileObject> files =
    fm.getJavaFileObjectsFromStrings(Arrays.asList("MyClass.java"));

CompilationTask task = compiler.getTask(
    null,      // 输出
    fm,        // 文件管理器
    null,      // 诊断监听
    null,      // 编译选项
    null,      // 要处理的类
    files      // 编译单元
);

boolean success = task.call();
```

### 3.2 内存编译

```java
// 从字符串编译
class StringSource extends SimpleJavaFileObject {
    private final String code;

    StringSource(String name, String code) {
        super(URI.create("string:///" + name.replace('.', '/') + ".java"), Kind.SOURCE);
        this.code = code;
    }

    @Override
    public CharSequence getCharContent(boolean ignoreEncodingErrors) {
        return code;
    }
}

JavaCompiler compiler = ToolProvider.getSystemJavaCompiler();
JavaFileObject file = new StringSource("com.example.Generated", """
    package com.example;
    public class Generated {
        public static void main(String[] args) {
            System.out.println("Hello from compiled code!");
        }
    }
    """);

CompilationTask task = compiler.getTask(null, null, null, null, null, List.of(file));
boolean success = task.call();
```

### 3.3 诊断监听

```java
DiagnosticCollector<JavaFileObject> diagnostics = new DiagnosticCollector<>();

CompilationTask task = compiler.getTask(
    null,
    fm,
    diagnostics,  // 收集诊断信息
    null,
    null,
    files
);

task.call();

// 处理诊断信息
for (Diagnostic<? extends JavaFileObject> d : diagnostics.getDiagnostics()) {
    System.out.printf("[%s] %s:%d:%d - %s%n",
        d.getKind(),
        d.getSource().getName(),
        d.getLineNumber(),
        d.getColumnNumber(),
        d.getMessage(null)
    );
}
```

### 3.4 编译选项

```java
List<String> options = List.of(
    "-d", "output",                    // 输出目录
    "-source", "26",                   // 源代码版本
    "-target", "26",                   // 目标版本
    "-classpath", "/path/to/libs",     // 类路径
    "-g",                              // 生成调试信息
    "-parameters",                     // 保留参数名
    "-Xlint:unchecked",                // 警告选项
    "-Werror"                          // 警告视为错误
);

CompilationTask task = compiler.getTask(null, fm, null, options, null, files);
```

---

## 4. Java 语言模型 API

### 4.1 抽象语法树 (AST)

**源码**: `src/jdk.compiler/share/classes/com/sun/source/tree/`

```java
import com.sun.source.tree.*;
import com.sun.source.util.*;

// 解析源代码为 AST
JavacTask task = (JavacTask) compiler.getTask(null, fm, null, null, null, files);

Iterable<? extends CompilationUnitTree> units = task.parse();

// 遍历 AST
new TreeScanner<Void, Void>() {
    @Override
    public Void visitMethodInvocation(MethodInvocationTree node, Void p) {
        System.out.println("Method call: " + node.getMethodSelect());
        return super.visitMethodInvocation(node, p);
    }

    @Override
    public Void visitClass(ClassTree node, Void p) {
        System.out.println("Class: " + node.getSimpleName());
        return super.visitClass(node, p);
    }
}.scan(units.iterator().next(), null);
```

### 4.2 符号 API

**源码**: `src/jdk.compiler/share/classes/com/sun/source/util/JavacTask.java`

```java
// 分析符号
JavacTask task = (JavacTask) compiler.getTask(...);

task.analyze();

// 获取类型信息
TypeElement type = task.getElements().getTypeElement("java.util.List");
```

---

## 5. 注解处理器

### 5.1 Processor 接口

**源码**: `src/jdk.compiler/share/classes/javax/annotation/processing/Processor.java`

```java
public interface Processor {
    Set<String> getSupportedAnnotationTypes()
    SourceVersion getSupportedSourceVersion()
    void init(ProcessingEnvironment processingEnv)
    boolean process(Set<? extends TypeElement> annotations, RoundEnvironment roundEnv)
}
```

### 5.2 自定义处理器示例

```java
@SupportedAnnotationTypes("com.example.Generate")
@SupportedSourceVersion(SourceVersion.RELEASE_26)
public class CodeGeneratorProcessor extends AbstractProcessor {

    @Override
    public boolean process(Set<? extends TypeElement> annotations, RoundEnvironment roundEnv) {
        for (TypeElement annotation : annotations) {
            for (Element element : roundEnv.getElementsAnnotatedWith(annotation)) {
                // 生成代码
                generateClass(element);
            }
        }
        return true;
    }

    private void generateClass(Element element) {
        String className = element.getSimpleName() + "Generated";

        JavaFileObject file = processingEnv.getFiler()
            .createSourceFile(className);

        try (Writer writer = file.openWriter()) {
            writer.write("""
                package %s;
                public class %s {
                    public static void main(String[] args) {
                        System.out.println("Generated!");
                    }
                }
                """.formatted(
                    processingEnv.getElementUtils().getPackageOf(element).toString(),
                    className
                ));
        } catch (IOException e) {
            processingEnv.getMessager().printMessage(
                Diagnostic.Kind.ERROR,
                "Failed to generate: " + e.getMessage()
            );
        }
    }
}
```

---

## 6. JDK 26 变更

### 6.1 语言特性支持

| 特性 | JDK | javac 支持 |
|------|-----|------------|
| 模式匹配 for switch | 21+ | ✓ |
| Record 类 | 16+ | ✓ |
| Sealed 类 | 17+ | ✓ |
| 虚拟线程 | 21+ | ✓ |
| 字符串模板 | 21+ (Preview) | ✓ |
| 隐式类和实例 Main 方法 | 21+ (Preview) | ✓ |

### 6.2 编译器改进

- **增量编译**: 改进的依赖跟踪
- **错误恢复**: 更好的语法错误恢复
- **性能**: 编译速度提升

### 6.3 新增选项

```bash
# JDK 26 新增
--enable-preview              # 启用预览特性
--release 26                 # 针对 JDK 26 编译
-source 26 -target 26        # 等价于 --release 26
```

---

## 7. 高级用法

### 7.1 自定义文件管理器

```java
class MemoryFileManager extends ForwardingJavaFileManager<StandardJavaFileManager> {
    private final Map<String, ByteArrayClass> classes = new HashMap<>();

    protected MemoryFileManager(StandardJavaFileManager fileManager) {
        super(fileManager);
    }

    @Override
    public JavaFileObject getJavaFileForOutput(Location location, String className,
                                               JavaFileObject.Kind kind, FileObject sibling) {
        if (kind == JavaFileObject.Kind.CLASS) {
            ByteArrayClass clazz = new ByteArrayClass(className);
            classes.put(className, clazz);
            return clazz;
        }
        return super.getJavaFileForOutput(location, className, kind, sibling);
    }

    public byte[] getClassBytes(String className) {
        return classes.get(className).getBytes();
    }
}
```

### 7.2 动态类加载

```java
// 编译并加载
MemoryFileManager fm = new MemoryFileManager(
    compiler.getStandardFileManager(null, null, null)
);

CompilationTask task = compiler.getTask(null, fm, null, null, null, List.of(file));
task.call();

// 获取编译后的字节码
byte[] bytes = fm.getClassBytes("com.example.Generated");

// 加载类
ClassLoader loader = new ClassLoader() {
    protected Class<?> findClass(String name) throws ClassNotFoundException {
        if (name.equals("com.example.Generated")) {
            return defineClass(name, bytes, 0, bytes.length);
        }
        return super.findClass(name);
    }
};

Class<?> clazz = loader.loadClass("com.example.Generated");
```

---

## 8. 相关链接

- [javax.tools 文档](https://docs.oracle.com/en/java/javase/26/docs/api/java.compiler/javax/tools/package-summary.html)
- [注解处理器教程](https://docs.oracle.com/en/java/javase/26/docs/api/java.compiler/javax/annotation/processing/package-summary.html)
- [javac 源码](https://github.com/openjdk/jdk/tree/master/src/jdk.compiler/share/classes)
