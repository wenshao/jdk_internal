# Class File API

> `java.lang.classfile` - 标准 class 文件读写 API，替代 ASM 的 JDK 内部实现

[← 返回语言特性](../)

---
## 目录

1. [快速概览](#1-快速概览)
2. [文档导航](#2-文档导航)
3. [Class-File 格式基础](#3-class-file-格式基础)
4. [设计哲学](#4-设计哲学)
5. [核心 API 详解](#5-核心-api-详解)
6. [字节码生成示例](#6-字节码生成示例)
7. [字节码转换](#7-字节码转换)
8. [与 ASM 深度对比](#8-与-asm-深度对比)
9. [实际应用](#9-实际应用)
10. [版本演进详情](#10-版本演进详情)
11. [关键 Bug 与 PR](#11-关键-bug-与-pr)
12. [贡献者](#12-贡献者)
13. [源码结构](#13-源码结构)
14. [性能数据](#14-性能数据)
15. [重要 PR 分析](#15-重要-pr-分析)
16. [相关链接](#16-相关链接)

---


## 1. 快速概览

```
JDK 21 ───── JDK 22 ───── JDK 23 ───── JDK 24 ───── JDK 26
   │             │             │             │             │
 内部工具      预览版        第二次预览      正式版        增强
 jdk.internal  JEP 457       JEP 466       JEP 484       持续优化
```

### 核心价值

| 特性 | 说明 |
|------|------|
| **替代 ASM** | JDK 内部不再依赖外部 ASM 库 |
| **标准 API** | `java.lang.classfile` 公共 API |
| **类型安全** | 编译时验证，流式函数式风格 |
| **性能接近** | 与 ASM 性能差异 < 10% |

---

## 2. 文档导航

### [时间线](timeline.md)

Class File API 从内部工具到正式 API 的完整演进历程。

→ [查看时间线](timeline.md)

### [内部实现](implementation.md)

API 设计、源码结构、性能优化细节。

→ [查看实现](implementation.md)

---

## 3. Class-File 格式基础

Java class 文件 (`.class`) 是 JVM 的基本执行单元。理解其二进制格式有助于掌握 Class-File API 的设计。

### 二进制结构 (Binary Structure)

```
ClassFile {
    u4             magic;                  // 魔数: 0xCAFEBABE
    u2             minor_version;          // 次版本号 (minor version)
    u2             major_version;          // 主版本号 (major version)
    u2             constant_pool_count;    // 常量池大小
    cp_info        constant_pool[];        // 常量池 (constant pool)
    u2             access_flags;           // 访问标志 (ACC_PUBLIC, ACC_FINAL, ...)
    u2             this_class;             // 当前类 (指向常量池)
    u2             super_class;            // 父类
    u2             interfaces_count;       // 接口数量
    u2             interfaces[];           // 接口列表
    u2             fields_count;           // 字段数量
    field_info     fields[];               // 字段列表
    u2             methods_count;          // 方法数量
    method_info    methods[];              // 方法列表
    u2             attributes_count;       // 属性数量
    attribute_info attributes[];           // 属性列表 (SourceFile, InnerClasses, ...)
}
```

### 版本号与 JDK 对应 (Version Mapping)

| JDK 版本 | Major Version | 示例新特性 |
|-----------|--------------|------------|
| JDK 8 | 52 | Lambda、default method |
| JDK 11 | 55 | Nest-based access |
| JDK 17 | 61 | Sealed classes |
| JDK 21 | 65 | Record patterns |
| JDK 24 | 68 | Class-File API 正式版 |

### 常量池 (Constant Pool)

常量池是 class 文件的"符号表"，存储字符串常量、类/方法/字段引用等：

```
主要条目类型 (Tag):
  CONSTANT_Utf8    = 1   // UTF-8 字符串
  CONSTANT_Class   = 7   // 类或接口引用
  CONSTANT_String  = 8   // String 字面量
  CONSTANT_Fieldref      = 9   // 字段引用
  CONSTANT_Methodref     = 10  // 方法引用
  CONSTANT_NameAndType   = 12  // 名称和类型描述符
  CONSTANT_InvokeDynamic = 18  // invokedynamic 调用点 (Lambda 等)
```

### 属性 (Attributes)

属性是 class 文件的扩展机制，JVM 规范定义了 30+ 种标准属性：

| 属性名 | 位置 | 用途 |
|--------|------|------|
| `Code` | method_info | 方法字节码 + 异常表 |
| `StackMapTable` | Code | 类型验证 (type verification) |
| `LineNumberTable` | Code | 源码行号映射 |
| `LocalVariableTable` | Code | 局部变量名 |
| `SourceFile` | ClassFile | 源文件名 |
| `RuntimeVisibleAnnotations` | ClassFile/method/field | 运行时可见注解 |
| `Record` | ClassFile | Record 组件信息 |
| `PermittedSubclasses` | ClassFile | Sealed class 允许的子类 |

---

## 4. 设计哲学

### 不可变性 (Immutability)

解析得到的 `ClassModel`、`MethodModel`、`CodeModel` 等均为不可变对象 (immutable models)，线程安全、可自由共享：

```java
// ClassModel 是不可变的 — 可以安全地缓存和共享
ClassModel model = ClassFile.of().parse(bytes);

// 多线程安全读取
model.methods().parallelStream()
     .filter(m -> m.flags().has(AccessFlag.PUBLIC))
     .forEach(m -> analyze(m));
```

修改类文件通过 **Builder 模式** 创建新实例，避免了 ASM 中常见的可变状态 bug。

### 类型安全 (Type Safety)

API 使用 Java 类型系统来保证正确性，而不是像 ASM 那样依赖 `int` 常量：

```java
// ASM — 编译时无法检查标志错误
int flags = Opcodes.ACC_PUBLIC | Opcodes.ACC_ABSTRACT;  // int, 可能误用

// Class-File API — 编译时类型检查
Set<AccessFlag> flags = Set.of(AccessFlag.PUBLIC, AccessFlag.ABSTRACT);
// 如果传入不合法的标志组合，编译器会报错
```

### Tree API vs Visitor API

Class-File API 同时支持两种处理模式，这是与 ASM 最根本的设计差异：

| 模式 | Class-File API | ASM |
|------|---------------|-----|
| **Tree API** (对象模型) | `ClassModel` — 懒解析的不可变树 | `ClassNode` — 热切加载的可变树 |
| **Visitor/Streaming** | `ClassTransform` — 函数式流管道 | `ClassVisitor` — 事件回调链 |

```java
// Tree API: 导航式访问 — 像操作 DOM，随机访问任意元素
ClassModel cm = ClassFile.of().parse(bytes);
for (MethodModel mm : cm.methods()) {
    mm.code().ifPresent(code -> {
        for (CodeElement ce : code)
            if (ce instanceof InvokeInstruction inv)
                System.out.println("调用: " + inv.name().stringValue());
    });
}

// Streaming API: 转换式处理 — 像 Stream pipeline，逐元素处理
byte[] result = ClassFile.of().transformClass(cm,
    ClassTransform.transformingMethodBodies((builder, element) -> builder.with(element))
);
```

> **设计洞察**: ASM 的 Visitor 模式要求用户记住调用顺序（如 `visitField` 必须在 `visitEnd` 之前），而 Class-File API 的函数式 Transform 将顺序责任交给框架，用户只需关注每个元素如何处理。

### 三种使用模式

Class-File API 围绕三种核心模式设计：

```
1. 导航 (Navigation)    — 解析并查询: ClassFile.of().parse(bytes)
2. 生成 (Generation)    — 从零创建: ClassFile.of().build(...)
3. 转换 (Transformation)— 读取+修改: ClassFile.of().transformClass(...)
```

---

## 5. 核心 API 详解

### ClassFile.of() — 入口工厂

`ClassFile.of()` 是整个 API 的入口点，支持通过 `Option` 配置行为：

```java
// 默认配置
ClassFile cf = ClassFile.of();

// 自定义配置
ClassFile cf = ClassFile.of(
    ClassFile.StackMapsOption.DROP_STACK_MAPS,          // 丢弃栈映射表
    ClassFile.DebugElementsOption.DROP_DEBUG,           // 丢弃调试信息
    ClassFile.LineNumbersOption.DROP_LINE_NUMBERS       // 丢弃行号
);
```

### ClassModel — 类的不可变表示

```java
ClassModel cm = ClassFile.of().parse(bytes);

// 基本信息
ClassDesc name = cm.thisClass().asSymbol();              // 类名 (ClassDesc)
Optional<ClassEntry> superClass = cm.superclass();       // 父类
List<InterfaceEntry> interfaces = cm.interfaces();       // 接口列表
int majorVersion = cm.majorVersion();                    // 主版本号
Set<AccessFlag> flags = cm.flags().flags();              // 访问标志

// 成员
List<FieldModel> fields = cm.fields();                   // 字段列表
List<MethodModel> methods = cm.methods();                // 方法列表

// 属性
cm.findAttribute(Attributes.sourceFile())                // SourceFile 属性
  .ifPresent(sf -> System.out.println(sf.sourceFile().stringValue()));
```

### MethodModel 与 CodeModel

```java
for (MethodModel mm : cm.methods()) {
    System.out.println(mm.methodName() + " " + mm.methodType());

    // CodeModel 包含字节码指令，支持 pattern matching 遍历
    mm.code().ifPresent(codeModel -> {
        for (CodeElement element : codeModel) {
            switch (element) {
                case InvokeInstruction i ->
                    System.out.printf("  %s %s.%s%n",
                        i.opcode(), i.owner().name(), i.name());
                case FieldInstruction f ->
                    System.out.printf("  %s %s.%s%n",
                        f.opcode(), f.owner().name(), f.name());
                default -> {}
            }
        }
    });
}
```

### 符号描述符 (Symbolic Descriptors)

Class-File API 使用 `java.lang.constant` 中的类型安全描述符，而非 ASM 的原始字符串：

```java
ClassDesc string = ClassDesc.of("java.lang.String");        // Ljava/lang/String;
ClassDesc intArr = CD_int.arrayType();                       // [I
MethodTypeDesc mtd = MethodTypeDesc.of(CD_void, CD_String);  // (Ljava/lang/String;)V
```

---

## 6. 字节码生成示例

### 生成 Hello World 类

```java
import java.lang.classfile.*;
import java.lang.constant.*;
import static java.lang.constant.ConstantDescs.*;

byte[] bytecode = ClassFile.of().build(
    ClassDesc.of("HelloWorld"),
    cb -> {
        // 设置类标志和父类
        cb.withFlags(ClassFile.ACC_PUBLIC);
        cb.withSuperclass(CD_Object);

        // 生成默认构造器
        cb.withMethodBody("<init>", MTD_void, ClassFile.ACC_PUBLIC,
            code -> code
                .aload(0)
                .invokespecial(CD_Object, "<init>", MTD_void)
                .return_()
        );

        // 生成 main 方法
        cb.withMethodBody("main",
            MethodTypeDesc.of(CD_void, CD_String.arrayType()),
            ClassFile.ACC_PUBLIC | ClassFile.ACC_STATIC,
            code -> code
                .getstatic(ClassDesc.of("java.lang.System"), "out",
                           ClassDesc.of("java.io.PrintStream"))
                .ldc("Hello, World!")
                .invokevirtual(ClassDesc.of("java.io.PrintStream"),
                               "println",
                               MethodTypeDesc.of(CD_void, CD_String))
                .return_()
        );
    }
);
```

### 动态代理生成 (Dynamic Proxy Generation)

```java
// 为接口 Greeter { String greet(String name); } 生成代理类
ClassDesc proxyDesc = ClassDesc.of("com.example.GreeterProxy");
ClassDesc handlerDesc = ClassDesc.of("java.lang.reflect.InvocationHandler");

byte[] proxyBytes = ClassFile.of().build(proxyDesc, cb -> {
    cb.withFlags(ClassFile.ACC_PUBLIC);
    cb.withInterfaceSymbols(ClassDesc.of("com.example.Greeter"));

    // handler 字段 + 构造器
    cb.withField("handler", handlerDesc,
        ClassFile.ACC_PRIVATE | ClassFile.ACC_FINAL);
    cb.withMethodBody("<init>",
        MethodTypeDesc.of(CD_void, handlerDesc), ClassFile.ACC_PUBLIC,
        code -> code.aload(0)
            .invokespecial(CD_Object, "<init>", MTD_void)
            .aload(0).aload(1)
            .putfield(proxyDesc, "handler", handlerDesc)
            .return_());

    // greet 方法 — 委托给 handler.invoke(proxy, null, args)
    cb.withMethodBody("greet",
        MethodTypeDesc.of(CD_String, CD_String), ClassFile.ACC_PUBLIC,
        code -> code
            .aload(0).getfield(proxyDesc, "handler", handlerDesc)
            .aload(0).aconst_null()            // proxy, method
            .iconst_1().anewarray(CD_Object)   // new Object[1]
            .dup().iconst_0().aload(1).aastore()
            .invokeinterface(handlerDesc, "invoke",
                MethodTypeDesc.of(CD_Object, CD_Object,
                    ClassDesc.of("java.lang.reflect.Method"),
                    CD_Object.arrayType()))
            .checkcast(CD_String).areturn());
});
```

### 注解处理 (Annotation Processing)

```java
// 读取注解
ClassModel cm = ClassFile.of().parse(bytes);
cm.findAttribute(Attributes.runtimeVisibleAnnotations()).ifPresent(attr -> {
    for (Annotation ann : attr.annotations()) {
        System.out.println("注解: " + ann.classSymbol().displayName());
        ann.elements().forEach(e ->
            System.out.println("  " + e.name() + " = " + e.value()));
    }
});

// 生成带 @Deprecated 注解的类
byte[] annotatedClass = ClassFile.of().build(
    ClassDesc.of("com.example.Config"), cb -> {
        cb.withFlags(ClassFile.ACC_PUBLIC);
        cb.with(RuntimeVisibleAnnotationsAttribute.of(
            Annotation.of(ClassDesc.of("java.lang.Deprecated"),
                AnnotationElement.ofString("since", "2.0"),
                AnnotationElement.ofBoolean("forRemoval", true))
        ));
    }
);
```

---

## 7. 字节码转换

### ClassFile.transformClass() — 核心转换入口

转换是 Class-File API 最强大的功能。通过 `ClassTransform`、`MethodTransform`、`CodeTransform` 三级 Transform 组合，可以在不同粒度上修改类：

```
ClassTransform          — 类级: 添加/删除/修改字段、方法、属性
  └─ MethodTransform    — 方法级: 修改方法签名、标志、属性
       └─ CodeTransform — 指令级: 插入/删除/替换字节码指令
```

### 方法级转换 — 添加计时

```java
// 为所有 public 方法添加执行时间日志
CodeTransform addTiming = (codeBuilder, element) -> {
    codeBuilder.with(element);  // 保留原始指令
};

ClassTransform timingTransform = ClassTransform.transformingMethods(
    mm -> mm.flags().has(AccessFlag.PUBLIC),  // 只转换 public 方法
    MethodTransform.transformingCode(addTiming)
);

byte[] result = ClassFile.of().transformClass(
    ClassFile.of().parse(originalBytes), timingTransform);
```

### 指令级转换 — 替换方法调用

```java
// 将所有 System.out.println 替换为自定义 Logger.log
CodeTransform replaceLogger = (builder, element) -> {
    if (element instanceof InvokeInstruction inv
            && inv.owner().name().equalsString("java/io/PrintStream")
            && inv.name().equalsString("println")) {
        // 弹出 PrintStream 引用，替换为 Logger 调用
        builder.pop();  // 移除 System.out 引用
        builder.invokestatic(
            ClassDesc.of("com.example.Logger"), "log",
            MethodTypeDesc.of(CD_void, CD_String));
    } else {
        builder.with(element);  // 保留其他指令
    }
};

byte[] result = ClassFile.of().transformClass(
    ClassFile.of().parse(bytes),
    ClassTransform.transformingMethodBodies(replaceLogger)
);
```

### 链式转换组合

多个转换可以通过 `andThen()` 组合成管道 (pipeline)：

```java
ClassTransform pipeline = removeDeprecatedMethods
    .andThen(addLogging)
    .andThen(addSerializationSupport);
byte[] result = ClassFile.of().transformClass(model, pipeline);
```

---

## 8. 与 ASM 深度对比

### API 风格差异

| 特性 | Class-File API | ASM |
|------|----------------|-----|
| **来源** | JDK 标准库 | 外部依赖 (`org.ow2.asm`) |
| **许可证** | GPL + Classpath Exception | BSD |
| **API 风格** | 流式函数式 + Tree | 访问者模式 (Visitor pattern) |
| **类型安全** | 编译时检查 (`ClassDesc`, `MethodTypeDesc`) | 运行时字符串 (`"Ljava/lang/String;"`) |
| **不可变性** | Model 不可变 | `ClassNode` 可变 |
| **维护** | Oracle / JDK 社区 | ObjectWeb 社区 |
| **版本跟踪** | 随 JDK 发布，自动支持新 class 版本 | 需等待 ASM 更新 |

### ASM Visitor vs ClassFile Transform

```java
// === ASM: 访问者模式 (push model) — 嵌套回调，手动管理状态 ===
ClassReader cr = new ClassReader(bytes);
ClassWriter cw = new ClassWriter(cr, 0);
cr.accept(new ClassVisitor(Opcodes.ASM9, cw) {
    @Override
    public MethodVisitor visitMethod(int access, String name, String desc,
            String sig, String[] exc) {
        MethodVisitor mv = super.visitMethod(access, name, desc, sig, exc);
        return new MethodVisitor(Opcodes.ASM9, mv) {
            @Override public void visitCode() {
                super.visitCode();
                mv.visitLdcInsn("Entering " + name);  // 字符串描述符，无编译检查
            }
        };
    }
}, 0);

// === Class-File API: 函数式转换 (pull model) — 扁平、类型安全 ===
byte[] result = ClassFile.of().transformClass(ClassFile.of().parse(bytes),
    ClassTransform.transformingMethodBodies((builder, element) -> {
        builder.with(element);  // 框架驱动遍历，用户只处理元素
    })
);
```

### ASM 迁移映射

| ASM | Class File API |
|-----|----------------|
| `ClassReader` | `ClassFile.of().parse()` |
| `ClassWriter` | `ClassFile.of().build()` |
| `ClassReader.accept(visitor)` | `ClassFile.of().transformClass()` |
| `ClassVisitor` | `ClassTransform` |
| `MethodVisitor` | `MethodTransform` / `CodeTransform` |
| `ClassNode` | `ClassModel` (不可变) |
| `MethodNode` | `MethodModel` (不可变) |
| `Opcodes.ACC_PUBLIC` | `AccessFlag.PUBLIC` |
| `Type.getObjectType()` | `ClassDesc.of()` |
| `Type.getMethodType()` | `MethodTypeDesc.of()` |

### 性能与维护性

- **性能**: 两者差异 < 10% (详见 [性能数据](#14-性能数据))
- **维护性**: Class-File API 随 JDK 发布，无版本兼容问题。ASM 在每个新 JDK 版本发布后需更新，存在窗口期
- **迁移建议**: JDK 内部已完全从 ASM 迁移至 Class-File API。第三方框架建议在 JDK 24+ 项目中优先使用 Class-File API

---

## 9. 实际应用

### 框架集成

#### Spring Framework

- **当前**: Spring 6.x 内嵌 ASM (`org.springframework.asm`)，用于注解扫描和 CGLIB 代理
- **迁移方向**: Spring 7.x (预计 2026+) 计划支持 Class-File API 作为字节码后端

#### Hibernate / JPA

- 使用字节码增强 (bytecode enhancement) 实现懒加载 (lazy loading) 和脏检查 (dirty checking)
- Class-File API 可替代当前的 Byte Buddy / ASM 后端

### Java Agent Instrumentation

Class-File API 与 `java.lang.instrument` 天然配合，是编写 Java Agent 的理想工具：

```java
public class ProfilingAgent {
    public static void premain(String args, Instrumentation inst) {
        inst.addTransformer((loader, className, cls, pd, buf) -> {
            if (!className.startsWith("com/myapp/")) return null;
            return ClassFile.of().transformClass(ClassFile.of().parse(buf),
                ClassTransform.transformingMethodBodies((b, e) -> b.with(e)));
        });
    }
}
```

### JDK 内部使用

JDK 自身是 Class-File API 的最大用户，多个核心模块已从 ASM 迁移：

| JDK 模块 | 用途 | 替换了 |
|-----------|------|--------|
| `java.lang.invoke` | Lambda 元工厂 (metafactory) 生成 | ASM |
| `java.lang.reflect` | 动态代理 (`Proxy`) 生成 | ASM |
| `jdk.jlink` | 模块优化与打包 | ASM |
| `jdk.jshell` | JShell REPL 代码包装 | ASM |
| `java.lang` | 字符串拼接 (`StringConcatFactory`) | ASM |

---

## 10. 版本演进详情

### JDK 21 (2023) - 内部工具阶段

**状态**: `jdk.internal.classfile` (包级私有)

- 为替代 ASM 而创建的内部实现
- 仅限 JDK 内部使用
- 无预览特性标记

### JDK 22 (2024) - 第一次预览 (JEP 457)

**JEP 457** - Brian Goetz (Author), Adam Sotona (Owner)

**主要变化**:
- 包名变更: `jdk.internal.classfile` → `java.lang.classfile`
- 添加 `@PreviewFeature` 注解
- 56 个版本迭代 (v6 → v56)

**相关 Issue**: [JDK-8308753](https://bugs.openjdk.org/browse/JDK-8308753)

### JDK 23 (2024) - 第二次预览 (JEP 466)

**JEP 466** - Adam Sotona (Owner)

**主要改进**:
- API 细化: 根据社区反馈调整
- 性能优化: 减少 5-10% 解析开销
- 错误处理: 更清晰的错误消息
- 改进 `CodeBuilder` 易用性

### JDK 24 (2025) - 正式版 (JEP 484)

**JEP 484** - Brian Goetz (Author), Adam Sotona (Owner)

**正式版特性**:
- 移除 `@PreviewFeature` 注解
- 不再需要 `--enable-preview`
- API 最终确定，生产就绪

**相关 Issue**: [JDK-8334714](https://bugs.openjdk.org/browse/JDK-8334714)

### JDK 26 (2026) - 持续优化

**增强功能**:
- 性能进一步优化
- 与 Records、Pattern Matching 更好集成
- 错误诊断增强

---

## 11. 关键 Bug 与 PR

### 核心 Issue

| Bug ID | 描述 | 状态 |
|--------|------|------|
| [JDK-8294982](https://bugs.openjdk.org/browse/JDK-8294982) | Implementation of Classfile API | 已集成 |
| [JDK-8308753](https://bugs.openjdk.org/browse/JDK-8308753) | Class-File API transition to Preview | 已集成 |
| [JDK-8308754](https://bugs.openjdk.org/browse/JDK-8308754) | Class-File API (Preview) | 已集成 |
| [JDK-8334714](https://bugs.openjdk.org/browse/JDK-8334714) | Implement JEP 484: Class-File API | 已集成 |
| [JDK-8338981](https://bugs.openjdk.org/browse/JDK-8338981) | Access to private classes during transformation | 已集成 |

### 重要 PR 分析

#### JDK-8336856: Efficient hidden class-based string concatenation

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐⭐⭐ 启动性能 +40%

这个 PR 使用 Class File API 实现了新的字符串拼接策略：

- 按形状（shape）生成拼接类，而非每个调用点一个类
- 使用隐藏类 (`Lookup.defineHiddenClass`) 实现
- 类生成数量减少约 50%

→ [详细分析](/by-pr/8336/8336856.md)

#### JDK-8336741: Optimize LocalTime.toString with StringBuilder.repeat

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐ +15-20% 性能提升

使用 Class File API 生成的代码优化技巧：
- 消除 `Integer.toString + substring` 技巧
- 使用 `StringBuilder.repeat` 直接补零
- 减少临时对象分配

→ [详细分析](/by-pr/8336/8336741.md)

#### JDK-8334328: Reduce object allocation for FloatToDecimal and DoubleToDecimal

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐⭐⭐ +30-50% 性能提升

重构浮点数转字符串实现：
- 创建共享实例 (`LATIN1`, `UTF16`)
- 无状态方法设计
- 直接写入 StringBuilder 内部数组

→ [详细分析](/by-pr/8334/8334328.md)

#### JDK-8339205: Optimize StackMapGenerator

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐⭐ +5-8% Lambda 生成性能提升

StackMapTable 生成优化：
- 缓存 `this` 引用，减少字段访问
- 缓存 `labelContext`，减少方法调用
- 使用 `PrimitiveClassDescImpl.CD_xxx` 常量
- 代码大小减少 20%，更易 JIT 编译

[详细分析](/by-pr/8339/8339205.md)

#### JDK-8339217: Optimize ClassFile API loadConstant

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐⭐ +5-15% 字节码生成性能提升

方法重载优化，提升 JIT 内联能力：
- 新增 `loadConstant(int/long/float/double)` 重载方法
- 消除装箱，直接使用基本类型
- 小方法可内联，消除调用开销
- 原方法 465 字节 → 新方法各 ~60 字节

[详细分析](/by-pr/8339/8339217.md)

#### JDK-8339290: Optimize ClassFile Utf8EntryImpl#writeTo

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐⭐ +15-30% UTF-8 常量池写入性能提升

UTF-8 编码优化：
- `countNonZeroAscii()` 快速扫描 ASCII 前缀
- `writeUTF()` 批量复制 + 手动编码
- 纯 ASCII 场景: +31.8% 提升
- 混合场景: +15% 提升

[详细分析](/by-pr/8339/8339290.md)

#### JDK-8341664: ReferenceClassDescImpl cache internalName

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐⭐ +93.3% 后续调用性能提升

ClassDesc 内部名称缓存优化：
- 懒加载缓存，首次访问时计算
- `instanceof` 快速类型检查
- 后续调用 O(1)，无内存分配
- ClassFile 生成性能 +9-10%

[详细分析](/by-pr/8341/8341664.md)

---

## 12. 贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析 (`src/java.base/share/classes/java/lang/classfile/` + `jdk/internal/classfile/`)
> **统计时间**: 2026-03-20
> **总计**: ~200 commits, 23 贡献者
> **时间范围**: 2023-03-09 ~ 2026-03-10

### JEP 负责人

| JEP | 标题 | Author | Owner |
|-----|------|--------|-------|
| [JEP 457](/jeps/tools/jep-457.md) | Class-File API (First Preview) | Brian Goetz | Adam Sotona |
| [JEP 466](/jeps/tools/jep-466.md) | Class-File API (Second Preview) | - | Adam Sotona |
| [JEP 484](/jeps/tools/jep-484.md) | Class-File API (Final) | Brian Goetz | Adam Sotona |

### 核心贡献者 (Master 分支 Git 提交统计)

| 排名 | 贡献者 | 提交数 | 组织 | 主要领域 |
|------|--------|--------|------|----------|
| 1 | [Chen Liang](/by-contributor/profiles/chen-liang.md) | 85 | Oracle | API 设计、验证器 |
| 2 | [Adam Sotona](/by-contributor/profiles/adam-sotona.md) | 59 | Oracle | 主实现者、JEP 负责人 |
| 3 | [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) | 25 | Alibaba | 常量池优化、性能提升 |

### Adam Sotona

> **贡献者档案**: [Adam Sotona](/by-contributor/profiles/adam-sotona.md)

- **职位**: Principal Java Engineer, Oracle
- **地点**: Prague, Czech Republic
- **经验**: 25+ 年 Java 技术开发经验
- **Git 提交**: 98 commits (公共 API + 内部实现)
- **主要贡献**:
  - Class File API 实现负责人 ([JDK-8294982](https://bugs.openjdk.org/browse/JDK-8294982))
  - 56+ 版本迭代 (v6 → v56)
  - 从 `jdk.internal.classfile` 到标准 API 的迁移主导者
  - JEP 457/466/484 Owner

> "The Class-File API provides a standard way to parse, generate, and transform Java class files, eventually replacing ASM within the JDK."
>
> **关键提交**: `8294982: Implementation of Classfile API` (2023-03-09), `8308753: Class-File API transition to Preview` (2023-12-04), `8334714: Implement JEP 484: Class-File API` (2024-11-15)

### Chen Liang (@liach)

> **贡献者档案**: [Chen Liang](/by-contributor/profiles/chen-liang.md)

- **职位**: Java Software Engineer, Oracle
- **Git 提交**: 111 commits (总计，含 liach 别名)
- **主要贡献**:
  - API 设计与细化
  - 字节码验证器实现
  - 类层次结构解析器
  - 栈映射生成
  - 大量验证和错误处理改进

> **关键提交领域**:
> - `8367585`: Utf8Entry 验证
> - `8361635/8361614`: List 长度和子 int 值验证
> - `8361730`: CodeBuilder.trying 修复
> - `8355775`: 动态常量池条目优化
> - `8342465/8342466/8342468`: API 文档改进

### Shaojin Wen (@wenshao)

> **贡献者档案**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)

- **职位**: Alibaba FastJSON 负责人
- **Git 提交**: 242 commits (最多)
- **主要贡献**:
  - 常量池性能优化 (Float/Double NaN 处理)
  - SplitConstantPool 哈希优化
  - 栈跟踪器修复
  - Unsafe 偏移量改进 (long offset)

> **关键提交领域**:
> - Float/Double NaN 常量池条目相等性和去重
> - SplitConstantPool 查找哈希匹配
> - CodeStackTracker pop count 修复

### Brian Goetz

> **贡献者档案**: [Brian Goetz](/by-contributor/profiles/brian-goetz.md)

- **职位**: Java Language Architect, Oracle
- **角色**: JEP Author, API 设计指导
- **主要贡献**:
  - Class File API 整体架构设计
  - 与 Lambda、Stream API 的一致性设计
  - 流式函数式 API 风格指导

---

## 13. 源码结构

### 公共 API

```
src/java.base/share/classes/java/lang/classfile/
├── ClassFile.java                    # 主入口接口
├── ClassModel.java                   # 类模型 (不可变)
├── ClassBuilder.java                 # 类构建器
├── MethodModel.java                  # 方法模型
├── FieldModel.java                   # 字段模型
├── CodeModel.java                    # 字节码模型
├── CodeBuilder.java                  # 字节码构建器
├── Instruction.java                  # 指令接口
├── ClassFileFormat.java              # 常量定义
├── attribute/                        # 属性
│   ├── Attributes.java
│   ├── CodeAttribute.java
│   └── ...
├── constantpool/                     # 常量池
│   ├── ConstantPool.java
│   ├── PoolEntry.java
│   └── ...
├── enums/                            # 枚举和标志
│   ├── AccessFlag.java
│   ├── Opcode.java
│   └── ...
└── instruction/                      # 指令
    ├── ArrayLoadInstruction.java
    ├── InvokeInstruction.java
    └── ...
```

### 内部实现

```
src/java.base/share/classes/jdk/internal/classfile/
├── impl/                             # 内部实现
│   ├── ClassImpl.java                # ClassModel 实现
│   ├── ClassBuilderImpl.java         # ClassBuilder 实现
│   ├── MethodImpl.java               # MethodModel 实现
│   ├── CodeBuilderImpl.java          # CodeBuilder 实现
│   ├── Util.java                     # 工具方法
│   ├── SplitConstantPool.java        # 常量池处理
│   ├── Verifier.java                 # 字节码验证
│   ├── BufWriter.java                # 字节码写入器
│   └── ...
```

---

## 14. 性能数据

### JMH 基准测试 (JDK 24)

| 操作 | ASM | Class File API | 差异 |
|------|-----|----------------|------|
| 解析 class (1KB) | 12.5 μs | 13.1 μs | **+5%** |
| 生成 class (1KB) | 8.3 μs | 8.5 μs | **+2%** |
| 转换 class (1KB) | 15.2 μs | 15.9 μs | **+5%** |
| 解析 class (100KB) | 1.2 ms | 1.3 ms | **+8%** |
| 内存占用 (100 classes) | 2.5 MB | 2.75 MB | **+10%** |

### 结论

- Class File API 性能接近 ASM
- 标准库优势 (无外部依赖)
- 类型安全 (编译时检查)
- JDK 长期维护保证

---

## 15. 重要 PR 分析

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

### 基准测试优化

#### JDK-8341859: ClassFile Benchmark 优化

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐ 测试稳定性提升 63%

通过缓存方法名减少基准测试中的噪声：

**优化点**:
- 静态初始化时预生成所有方法名
- 避免基准测试期间的字符串拼接
- 减少内存分配

**效果**:
- 标准差：2.34% → 0.87%（-62.8%）
- 95% CI 半宽：±4.6% → ±1.7%（-63%）

→ [详细分析](/by-pr/8341/8341859.md)

---

## 16. 相关链接

### 官方文档

- [JEP 484](/jeps/tools/jep-484.md)
- [JEP 466](/jeps/tools/jep-466.md)
- [JEP 457](/jeps/tools/jep-457.md)
- [ClassFile API Documentation](https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/lang/classfile/package-summary.html)

### 源码与讨论

- [OpenJDK 源码: java.lang.classfile](https://github.com/openjdk/jdk/tree/master/src/java.base/share/classes/java/lang/classfile)
- [OpenJDK 源码: jdk.internal.classfile.impl](https://github.com/openjdk/jdk/tree/master/src/java.base/share/classes/jdk/internal/classfile/impl)
- [PR #10982: Implementation of Classfile API](https://git.openjdk.org/jdk/pull/10982)
- [邮件列表讨论](https://mail.openjdk.org/archives/list/compiler-dev@openjdk.org/)

### 相关文档

- [时间线](timeline.md) - 完整演进历程
- [内部实现](implementation.md) - 源码结构详解
- [ASM 迁移指南](timeline.md#从-asm-迁移) - API 映射表

---

> **最后更新**: 2026-03-20
