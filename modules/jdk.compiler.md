# jdk.compiler 模块分析

> Java 编译器 (javac) 实现，提供编译器 API 和抽象语法树 (AST) 访问

---

## 1. 模块概述 (Module Overview)

`jdk.compiler` 包含 Java 编译器 `javac` 的完整实现，提供通过 `javax.tools.JavaCompiler` API
进行程序化编译的能力，以及通过 `com.sun.source.*` 包访问编译器内部的抽象语法树 (Compiler Tree API)。

**源码统计**: 347 个 Java 文件

### 模块定义 (Module Declaration)

**文件**: `src/jdk.compiler/share/classes/module-info.java`

```java
module jdk.compiler {
    requires transitive java.compiler;
    requires jdk.internal.opt;
    requires jdk.zipfs;

    // 公开导出 (Public exports)
    exports com.sun.source.doctree;
    exports com.sun.source.tree;
    exports com.sun.source.util;
    exports com.sun.tools.javac;

    // 限定导出 (Qualified exports) - 主要供 jdk.javadoc、jdk.jshell 使用
    exports com.sun.tools.javac.api to jdk.javadoc, jdk.jshell, jdk.internal.md;
    exports com.sun.tools.javac.code to jdk.javadoc, jdk.jshell;
    exports com.sun.tools.javac.comp to jdk.javadoc, jdk.jshell;
    exports com.sun.tools.javac.file to jdk.jdeps, jdk.javadoc;
    exports com.sun.tools.javac.jvm to jdk.javadoc;
    exports com.sun.tools.javac.main to jdk.javadoc, jdk.jshell;
    exports com.sun.tools.javac.model to jdk.javadoc;
    exports com.sun.tools.javac.parser to jdk.jshell, jdk.internal.md;
    exports com.sun.tools.javac.tree to jdk.javadoc, jdk.jshell, jdk.internal.md;
    exports com.sun.tools.javac.util to jdk.jdeps, jdk.javadoc, jdk.jshell, jdk.internal.md;

    // SPI
    uses javax.annotation.processing.Processor;
    uses com.sun.source.util.Plugin;
    uses com.sun.tools.javac.platform.PlatformProvider;

    provides javax.tools.JavaCompiler with com.sun.tools.javac.api.JavacTool;
    provides javax.tools.Tool with com.sun.tools.javac.api.JavacTool;
    provides java.util.spi.ToolProvider with com.sun.tools.javac.main.JavacToolProvider;
}
```

### 架构 (Architecture)

```
┌─────────────────────────────────────────────────────────┐
│                     应用代码                              │
│  ToolProvider / JavaCompiler / JavacTask                 │
├─────────────────────────────────────────────────────────┤
│              javax.tools API (java.compiler 模块)        │
│  JavaCompiler / JavaFileManager / JavaFileObject         │
├─────────────────────────────────────────────────────────┤
│            com.sun.source.* (Compiler Tree API)          │
│  Tree / TreeScanner / TreeVisitor / JavacTask            │
├─────────────────────────────────────────────────────────┤
│              com.sun.tools.javac.* (javac 实现)          │
│  main / parser / comp / tree / code / jvm               │
├─────────────────────────────────────────────────────────┤
│              JavaFileManager / StandardJavaFileManager   │
│  文件系统 / ZipFS / 模块路径                               │
└─────────────────────────────────────────────────────────┘
```

---

## 2. 包结构 (Package Structure)

### com.sun.tools.javac 核心包

| 包 | 说明 | 关键类 |
|---|------|--------|
| `main` | 编译器入口和主流程 | `JavaCompiler`, `Main`, `Arguments` |
| `parser` | 词法分析和语法分析 | `JavacParser`, `JavaTokenizer`, `Scanner`, `Tokens` |
| `tree` | 抽象语法树 (AST) 定义 | `JCTree`, `TreeMaker`, `TreeInfo`, `Pretty` |
| `comp` | 语义分析和代码转换 | `Attr`, `Check`, `Flow`, `Resolve`, `Enter`, `Lower` |
| `code` | 符号和类型系统 | `Symbol`, `Type`, `Types`, `Symtab`, `Scope`, `Flags` |
| `jvm` | 字节码生成 | `Gen`, `Code`, `ClassWriter`, `ClassReader`, `Items` |
| `api` | 公开 API 实现 | `JavacTool`, `JavacTaskImpl`, `JavacTrees` |
| `model` | javax.lang.model 实现 | `JavacElements`, `JavacTypes` |
| `processing` | 注解处理 | `JavacProcessingEnvironment`, `JavacFiler`, `JavacRoundEnvironment` |
| `file` | 文件管理 | `JavacFileManager`, `Locations`, `PathFileObject` |
| `util` | 工具类 | `Context`, `Log`, `Names`, `List`, `ListBuffer` |
| `resources` | 资源文件 | 编译器消息和提示文本 |
| `platform` | 平台支持 | `JDKPlatformProvider`, `PlatformDescription` |
| `launcher` | 源码直接启动 | `SourceLauncher`, `MemoryClassLoader` |

### com.sun.source.* (Compiler Tree API)

| 包 | 说明 |
|---|------|
| `com.sun.source.tree` | AST 节点接口 (Tree, CompilationUnitTree, ClassTree, MethodTree 等) |
| `com.sun.source.util` | 工具类 (JavacTask, TreeScanner, TreePathScanner, Trees, Plugin) |
| `com.sun.source.doctree` | 文档注释 AST (DocTree, DocCommentTree 等) |

---

## 3. 编译阶段 (Compilation Phases)

### CompileStates 枚举

**文件**: `src/jdk.compiler/share/classes/com/sun/tools/javac/comp/CompileStates.java`

```java
public enum CompileState {
    INIT(0),           // 初始化
    PARSE(1),          // 词法分析 + 语法分析 → JCTree
    ENTER(2),          // 符号注册 → 建立符号表
    PROCESS(3),        // 注解处理
    ATTR(4),           // 属性分析 → 类型检查、名称解析
    FLOW(5),           // 数据流分析 → 可达性、异常、赋值检查
    WARN(6),           // 警告分析
    TRANSTYPES(7),     // 类型转换 → 泛型擦除
    TRANSPATTERNS(8),  // 模式转换 → 模式匹配脱糖
    LOWER(9),          // 代码降低 → 语法糖脱糖
    UNLAMBDA(10),      // Lambda 转换 → Lambda 脱糖为方法
    GENERATE(11);      // 字节码生成 → .class 文件
}
```

### 编译流水线详解 (Pipeline Details)

```
源代码 (.java)
    │
    ▼ ① PARSE (解析)
    │  JavacParser.parseCompilationUnit()
    │  JavaTokenizer → Token 流 → JCTree AST
    │
    ▼ ② ENTER (录入)
    │  Enter.complete() + MemberEnter
    │  TypeEnter → 将类/接口/方法注册到符号表 (Symtab)
    │  处理 import 语句，建立作用域 (Scope)
    │
    ▼ ③ PROCESS (注解处理)
    │  JavacProcessingEnvironment
    │  如果生成了新源文件 → 回到 PARSE 重新开始
    │
    ▼ ④ ATTR (属性化)
    │  Attr.attribClass()
    │  名称解析 (Resolve)、类型推断 (Infer)
    │  重载解析 (Resolve.resolveMethod)
    │  类型检查 (Check)
    │
    ▼ ⑤ FLOW (流分析)
    │  Flow.analyzeTree()
    │  活跃性分析 (Liveness): 可达性检查
    │  赋值分析 (Assignation): final 变量赋值检查
    │  异常分析: 受检异常必须捕获或声明
    │
    ▼ ⑥ WARN (警告分析)
    │  WarningAnalyzer
    │  分析并报告编译器警告
    │
    ▼ ⑦ TRANSTYPES (类型擦除)
    │  TransTypes.translateTopLevelClass()
    │  泛型类型擦除 → 原始类型
    │  插入类型转换 (casts)
    │
    ▼ ⑧ TRANSPATTERNS (模式转换)
    │  TransPatterns
    │  switch 模式匹配 → 传统 switch 脱糖
    │  instanceof 模式 → 传统 instanceof + cast
    │
    ▼ ⑨ LOWER (代码降低)
    │  LambdaToMethod.translateTopLevelClass()
    │  Lambda 表达式 → 私有静态/实例方法
    │  方法引用 → invokedynamic 调用点
    │
    │  Lower.translateTopLevelClass()
    │  内部类 → 独立类 (合成访问方法)
    │  增强 for → 迭代器/索引 for
    │  try-with-resources → try-finally
    │  String switch → hashCode/equals
    │  assert → if + AssertionError
    │  enum → 普通类 + values()/valueOf()
    │  record → 普通类 + 访问器/equals/hashCode/toString
    │
    ▼ ⑩ UNLAMBDA (Lambda 脱糖)
    │  LambdaToMethod.translateTopLevelClass()
    │  Lambda 表达式 → 私有静态/实例方法
    │  方法引用 → invokedynamic 调用点
    │
    ▼ ⑪ GENERATE (字节码生成)
    │  Gen.genClass()
    │  JCTree → Code (字节码指令)
    │  ClassWriter.writeClass() → .class 文件
    │
    ▼
字节码 (.class)
```

---

## 4. 关键类详解 (Key Classes)

### 4.1 JavaCompiler (编译器主控)

**文件**: `src/jdk.compiler/share/classes/com/sun/tools/javac/main/JavaCompiler.java`

```java
public class JavaCompiler {
    // 编译器主入口，协调所有编译阶段
    // 方法 compile() 驱动整个编译流程
    // 使用 Todo 队列管理待处理的编译单元
}
```

### 4.2 JCTree (抽象语法树)

**文件**: `src/jdk.compiler/share/classes/com/sun/tools/javac/tree/JCTree.java`

```java
public abstract class JCTree implements Tree, Cloneable, DiagnosticPosition {
    // 所有 AST 节点的基类
    // 内部定义了所有具体的 AST 节点类型:

    // JCCompilationUnit   → 编译单元 (整个源文件)
    // JCClassDecl         → 类/接口/枚举/记录声明
    // JCMethodDecl        → 方法声明
    // JCVariableDecl      → 变量声明
    // JCBlock             → 代码块
    // JCIf                → if 语句
    // JCForLoop           → for 循环
    // JCSwitch            → switch 语句
    // JCReturn            → return 语句
    // JCTry               → try 语句
    // JCMethodInvocation  → 方法调用
    // JCNewClass          → new 表达式
    // JCLambda            → Lambda 表达式
    // JCMemberReference   → 方法引用
    // JCBinary            → 二元运算
    // JCLiteral           → 字面量
    // JCIdent             → 标识符
    // JCFieldAccess       → 字段访问
    // JCTypeCast          → 类型转换
    // JCInstanceOf        → instanceof
    // JCBindingPattern    → 绑定模式
    // JCRecordPattern     → record 模式
    // JCImportBase        → import 声明基类
    // ... (更多节点类型)
}
```

### 4.3 树操作工具 (Tree Utilities)

**目录**: `src/jdk.compiler/share/classes/com/sun/tools/javac/tree/`

| 文件 | 说明 |
|------|------|
| `TreeMaker.java` | AST 节点工厂，创建 JCTree 节点 |
| `TreeInfo.java` | AST 信息查询工具 |
| `TreeScanner.java` | AST 遍历器 (Visitor 模式) |
| `TreeTranslator.java` | AST 转换器 (用于脱糖等转换) |
| `TreeCopier.java` | AST 深拷贝工具 |
| `Pretty.java` | AST 格式化输出 (漂亮打印) |
| `DocPretty.java` | 文档注释格式化 |
| `DCTree.java` | 文档注释 AST 节点 |

### 4.4 符号和类型系统 (Symbol and Type System)

**目录**: `src/jdk.compiler/share/classes/com/sun/tools/javac/code/`

| 文件 | 说明 |
|------|------|
| `Symbol.java` | 符号抽象基类 (ClassSymbol, MethodSymbol, VarSymbol 等) |
| `Type.java` | 类型抽象基类 (ClassType, ArrayType, MethodType, TypeVar 等) |
| `Types.java` | 类型操作工具 (子类型判断、类型擦除、捕获转换等) |
| `Symtab.java` | 预定义符号表 (Object, String, int 等) |
| `Scope.java` | 作用域 (嵌套的符号查找) |
| `Flags.java` | 访问修饰符标志 (PUBLIC, STATIC, FINAL 等) |
| `Kinds.java` | 符号种类 (VAR, MTH, TYP, PCK 等) |
| `TypeTag.java` | 类型标签 (BYTE, CHAR, INT, CLASS, ARRAY 等) |
| `Source.java` | 源码级别 (控制支持的语言特性) |
| `ClassFinder.java` | 类查找器 (从 classpath/modulepath 加载类) |
| `ClassReader.java` | .class 文件读取器 |

### 4.5 语义分析 (Semantic Analysis)

**目录**: `src/jdk.compiler/share/classes/com/sun/tools/javac/comp/`

| 文件 | 说明 |
|------|------|
| `Enter.java` | 第一遍扫描: 注册顶层类/接口符号 |
| `TypeEnter.java` | 完成类型信息录入 (超类、接口、成员) |
| `MemberEnter.java` | 录入成员 (字段、方法) |
| `Attr.java` | 属性化: 类型检查、名称解析、常量折叠 |
| `Resolve.java` | 名称解析: 方法重载解析、变量查找 |
| `Check.java` | 类型安全检查: 类型兼容性、废弃检测 |
| `Infer.java` | 泛型类型推断 |
| `DeferredAttr.java` | 延迟属性化 (Lambda/方法引用类型推断) |
| `ArgumentAttr.java` | 参数级属性化 |
| `Flow.java` | 数据流分析: 可达性、异常、赋值 |
| `Annotate.java` | 注解处理和验证 |
| `Modules.java` | 模块系统处理 |
| `ConstFold.java` | 常量折叠优化 |
| `Operators.java` | 运算符类型解析 |
| `Lower.java` | 语法糖脱糖 (内部类、enum、record、增强 for 等) |
| `TransTypes.java` | 泛型擦除 |
| `TransPatterns.java` | 模式匹配脱糖 |
| `LambdaToMethod.java` | Lambda 转方法 |
| `ExhaustivenessComputer.java` | switch 穷尽性检查 |
| `ThisEscapeAnalyzer.java` | this 逃逸分析 |
| `WarningAnalyzer.java` | 警告分析 |

### 4.6 字节码生成 (Bytecode Generation)

**目录**: `src/jdk.compiler/share/classes/com/sun/tools/javac/jvm/`

| 文件 | 说明 |
|------|------|
| `Gen.java` | AST → 字节码指令的翻译器 |
| `Code.java` | 字节码指令缓冲区和栈帧跟踪 |
| `Items.java` | 操作数栈项 (LocalItem, StaticItem, MemberItem 等) |
| `ClassWriter.java` | .class 文件写入器 |
| `ClassReader.java` | .class 文件读取器 |
| `ByteCodes.java` | JVM 字节码常量定义 |
| `PoolWriter.java` | 常量池写入器 |
| `PoolReader.java` | 常量池读取器 |
| `StringConcat.java` | 字符串拼接策略 (invokedynamic) |
| `ClassFile.java` | Class 文件格式常量 |
| `CRTable.java` | 代码/行号映射表 |
| `Target.java` | 目标版本 (控制生成的字节码版本) |

---

## 5. Context 机制 (Dependency Injection)

**文件**: `src/jdk.compiler/share/classes/com/sun/tools/javac/util/Context.java`

```java
// javac 使用 Context 作为轻量级依赖注入容器
// 所有编译器组件通过 Context 获取彼此的引用
// 每次编译创建一个新的 Context 实例

public class Context {
    // 典型用法:
    // protected static final Context.Key<Attr> attrKey = new Context.Key<>();
    // public static Attr instance(Context context) {
    //     Attr instance = context.get(attrKey);
    //     if (instance == null) instance = new Attr(context);
    //     return instance;
    // }
}
```

---

## 6. 使用示例 (Usage Examples)

### 6.1 基本编译 (Basic Compilation)

```java
JavaCompiler compiler = ToolProvider.getSystemJavaCompiler();

StandardJavaFileManager fm = compiler.getStandardFileManager(null, null, null);

Iterable<? extends JavaFileObject> files =
    fm.getJavaFileObjectsFromStrings(List.of("MyClass.java"));

JavaCompiler.CompilationTask task = compiler.getTask(
    null,   // 输出 Writer
    fm,     // 文件管理器
    null,   // 诊断监听器
    null,   // 编译选项
    null,   // 要处理的类名
    files   // 编译单元
);

boolean success = task.call();
```

### 6.2 内存编译 (In-Memory Compilation)

```java
class StringSource extends SimpleJavaFileObject {
    private final String code;

    StringSource(String name, String code) {
        super(URI.create("string:///" + name.replace('.', '/') + ".java"),
              Kind.SOURCE);
        this.code = code;
    }

    @Override
    public CharSequence getCharContent(boolean ignoreEncodingErrors) {
        return code;
    }
}

JavaCompiler compiler = ToolProvider.getSystemJavaCompiler();
JavaFileObject file = new StringSource("com.example.Hello", """
    package com.example;
    public class Hello {
        public static String greet() { return "Hello!"; }
    }
    """);

JavaCompiler.CompilationTask task =
    compiler.getTask(null, null, null, null, null, List.of(file));
task.call();
```

### 6.3 AST 访问 (Compiler Tree API)

```java
JavaCompiler compiler = ToolProvider.getSystemJavaCompiler();
StandardJavaFileManager fm = compiler.getStandardFileManager(null, null, null);

JavacTask task = (JavacTask) compiler.getTask(
    null, fm, null, null, null,
    fm.getJavaFileObjectsFromStrings(List.of("Example.java"))
);

// 解析为 AST
Iterable<? extends CompilationUnitTree> units = task.parse();

// 遍历 AST
new TreeScanner<Void, Void>() {
    @Override
    public Void visitClass(ClassTree node, Void p) {
        System.out.println("Class: " + node.getSimpleName());
        return super.visitClass(node, p);
    }

    @Override
    public Void visitMethod(MethodTree node, Void p) {
        System.out.println("  Method: " + node.getName());
        return super.visitMethod(node, p);
    }
}.scan(units.iterator().next(), null);
```

### 6.4 诊断信息收集 (Diagnostic Collection)

```java
DiagnosticCollector<JavaFileObject> diagnostics = new DiagnosticCollector<>();

JavaCompiler.CompilationTask task = compiler.getTask(
    null, fm, diagnostics, null, null, files
);

task.call();

for (Diagnostic<? extends JavaFileObject> d : diagnostics.getDiagnostics()) {
    System.out.printf("[%s] %s:%d - %s%n",
        d.getKind(),
        d.getSource() != null ? d.getSource().getName() : "<none>",
        d.getLineNumber(),
        d.getMessage(null)
    );
}
```

### 6.5 注解处理器 (Annotation Processor)

```java
@SupportedAnnotationTypes("com.example.Generate")
@SupportedSourceVersion(SourceVersion.RELEASE_26)
public class CodeGenerator extends AbstractProcessor {

    @Override
    public boolean process(Set<? extends TypeElement> annotations,
                          RoundEnvironment roundEnv) {
        for (Element element : roundEnv.getElementsAnnotatedWith(
                processingEnv.getElementUtils()
                    .getTypeElement("com.example.Generate"))) {
            generateClass(element);
        }
        return true;
    }

    private void generateClass(Element element) {
        String className = element.getSimpleName() + "Impl";
        try {
            JavaFileObject file = processingEnv.getFiler()
                .createSourceFile(className);
            try (Writer writer = file.openWriter()) {
                writer.write("public class " + className + " { }");
            }
        } catch (IOException e) {
            processingEnv.getMessager().printMessage(
                Diagnostic.Kind.ERROR, e.getMessage());
        }
    }
}
```

---

## 7. 编译器插件 (Compiler Plugin)

**接口**: `com.sun.source.util.Plugin`

```java
// 编译器插件可在编译期间访问 AST
// 通过 -Xplugin:name 命令行选项激活
// 通过 ServiceLoader 发现 (META-INF/services/com.sun.source.util.Plugin)

public interface Plugin {
    String getName();
    void init(JavacTask task, String... args);
}
```

---

## 8. 源码直接启动 (Source Launcher)

**文件**: `src/jdk.compiler/share/classes/com/sun/tools/javac/launcher/SourceLauncher.java`

```java
// 支持 `java HelloWorld.java` 直接运行源文件
// MemoryClassLoader 在内存中编译并加载
// MemoryFileManager 管理内存中的编译产物
```

相关文件:
- `MemoryClassLoader.java` - 内存类加载器
- `MemoryFileManager.java` - 内存文件管理器
- `MemoryContext.java` - 内存编译上下文
- `ProgramFileObject.java` - 程序文件对象
- `ProgramDescriptor.java` - 程序描述符

---

## 9. 相关链接 (Related Links)

- [javax.tools API 文档](https://docs.oracle.com/en/java/javase/21/docs/api/java.compiler/javax/tools/package-summary.html)
- [Compiler Tree API (com.sun.source)](https://docs.oracle.com/en/java/javase/21/docs/api/jdk.compiler/com/sun/source/tree/package-summary.html)
- [javac 源码](https://github.com/openjdk/jdk/tree/master/src/jdk.compiler/share/classes)
