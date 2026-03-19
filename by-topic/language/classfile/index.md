# Class File API

> java.lang.classfile - 标准 class 文件读写 API

---

## 快速概览

```
JDK 22 ───── JDK 23 ───── JDK 24 ───── JDK 26
   │             │             │             │
 预览版        第二次预览      正式版        增强
 JEP 459       JEP 466       JEP 484       优化
```

### 核心特性

| 特性 | 说明 |
|------|------|
| **解析 class 文件** | `ClassFile.of().parse(bytes)` |
| **生成 class 文件** | `ClassFile.of().build(classDesc)` |
| **转换 class 文件** | `ClassFile.of().transformClass(bytecode)` |
| **流式 API** | 函数式风格构建字节码 |
| **类型安全** | 编译时验证字节码操作 |
| **替代 ASM** | 标准库内置，无需外部依赖 |

---

## 文档导航

### [时间线](timeline.md)

Class File API 从预览到正式的完整演进。

→ [查看时间线](timeline.md)

---

## 基础用法

### 解析 Class 文件

```java
import java.lang.classfile.*;

// 解析 class 文件
ClassModel classModel = ClassFile.of().parse(bytes);

// 读取类信息
classModel.thisClass().asSymbol();     // 类名
classModel.version();                   // 版本
classModel.accessFlags();               // 访问标志
classModel.flags();                     // 状态

// 遍历方法
classModel.methods().forEach(method -> {
    System.out.println(method.methodName());
});

// 遍历字段
classModel.fields().forEach(field -> {
    System.out.println(field.fieldName());
});
```

### 生成 Class 文件

```java
import java.lang.classfile.*;
import java.lang.classfile.constantpool.*;

// 生成简单的 Hello World 类
byte[] bytecode = ClassFile.of().build(
    ClassDesc.of("HelloWorld"),
    classBuilder -> {
        classBuilder.withFlags(AccessFlag.PUBLIC);
        classBuilder.withMethod(
            "main",
            MethodTypeDesc.of("(Ljava/lang/String;)V"),
            AccessFlag.PUBLIC | AccessFlag.STATIC,
            methodBuilder -> {
                methodBuilder.withCode(
                    codeBuilder -> codeBuilder
                        .getstatic(ClassDesc.of("java/lang/System"), "out",
                                 ClassDesc.of("java/io/PrintStream"))
                        .ldc("Hello, World!")
                        .invokevirtual(
                            ClassDesc.of("java/io/PrintStream"),
                            "println",
                            MethodTypeDesc.of("(Ljava/lang/String;)V"))
                        .return_()
                );
            }
        );
    }
);
```

### 转换 Class 文件

```java
// 添加日志到每个方法
byte[] transformed = ClassFile.of().transformClass(
    ClassFile.of().parse(originalBytes),
    ClassTransform.transformingMethods(
        (classBuilder, method, methodBuilder) -> {
            // 在每个方法开始添加日志
            methodBuilder.withCode(
                codeBuilder -> codeBuilder
                    .getstatic(ClassDesc.of("java/lang/System"), "out",
                             ClassDesc.of("java/io/PrintStream"))
                    .ldc("Method: " + method.methodName().stringValue())
                    .invokevirtual(
                        ClassDesc.of("java/io/PrintStream"),
                        "println",
                        MethodTypeDesc.of("(Ljava/lang/String;)V"))
                    .with(method.code().orElseThrow())
            );
        }
    )
);
```

### 注解处理

```java
// 查找所有带 @Deprecated 注解的方法
ClassFile.of().parse(bytes)
    .methods()
    .forEach(method -> {
        boolean hasDeprecated = method.findAttribute(Attributes.deprecated())
                                     .isPresent();
        if (hasDeprecated) {
            System.out.println("Deprecated: " + method.methodName());
        }
    });
```

---

## 核心组件

### ClassFile

```java
ClassFile cf = ClassFile.of();

// 解析选项
ClassFile cf = ClassFile.of(
    ClassFile.ConstantPoolSharingOption.SHARED_POOL,
    ClassFile.DeadCodeOption.KEEP_DEAD_CODE,
    ClassFile.DebugElementsOption.KEEP_DEBUG_INFO
);
```

### ClassModel

```java
ClassModel cm = cf.parse(bytes);

cm.thisClass();              // 类名
cm.superclass();             // 父类
cm.interfaces();             // 接口列表
cm.fields();                 // 字段
cm.methods();                // 方法
cm.attributes();             // 类属性
cm.majorVersion();           // 主版本
cm.minorVersion();           // 次版本
```

### CodeBuilder

```java
methodBuilder.withCode(codeBuilder -> {
    // 加载指令
    codeBuilder.aload(0);           // 加载 this
    codeBuilder.iload(1);           // 加载 int 参数
    codeBuilder.ldc("constant");    // 加载常量

    // 存储指令
    codeBuilder.astore(0);          // 存储引用
    codeBuilder.istore(1);          // 存储 int

    // 数组指令
    codeBuilder.aaload();           // 加载引用数组元素
    codeBuilder.aastore();          // 存储引用数组元素

    // 控制流
    codeBuilder.ifnull(label);      // 条件跳转
    codeBuilder.goto_(label);       // 无条件跳转
    codeBuilder.return_();          // 返回 void
});
```

---

## 与 ASM 对比

| 特性 | Class File API | ASM |
|------|----------------|-----|
| 来源 | JDK 标准库 | 外部依赖 |
| API 风格 | 流式函数式 | 访问者模式 |
| 类型安全 | 编译时检查 | 运行时检查 |
| 维护成本 | JDK 维护 | 社区维护 |
| JDK 版本兼容 | 需要重新编译 | 单一 jar 支持多版本 |

---

## 内部实现

### 源码结构

```
src/java.base/share/classes/java/lang/classfile/
├── ClassFile.java                # 主入口
├── ClassModel.java               # 类模型
├── ClassBuilder.java             # 类构建器
├── MethodModel.java              # 方法模型
├── FieldModel.java               # 字段模型
├── CodeBuilder.java              # 字节码构建器
├── Instruction.java              # 指令接口
├── attribute/                    # 属性
│   ├── Attributes.java
│   └── ...
├── constantpool/                 # 常量池
│   ├── ConstantPoolBuilder.java
│   └── ...
└── enums/                        # 枚举和标志
    ├── AccessFlag.java
    └── Opcode.java

src/java.base/share/classes/jdk/internal/classfile/
└── impl/                         # 内部实现
    ├── ClassImpl.java
    ├── ClassBuilderImpl.java
    ├── Util.java
    └── ...
```

### 关键内部类

| 类 | 作用 | 访问级别 |
|---|------|----------|
| `jdk.internal.classfile.impl.ClassImpl` | ClassModel 实现 | 内部 |
| `jdk.internal.classfile.impl.BufWriter` | 字节码写入器 | 内部 |
| `jdk.internal.classfile.impl.Util` | 工具方法 | 内部 |

---

## VM 参数

```bash
# Class File API 无需特殊 VM 参数
# 但可以启用验证
-XX:+VerifyAppCDS                 # 验证 AOT 编译的类
-Xlog:class+load=info             # 记录类加载
```

---

## 相关链接

- [JEP 484: Class-File API](https://openjdk.org/jeps/484)
- [JEP 466: Class-File API (Second Preview)](https://openjdk.org/jeps/466)
- [JEP 459: Class-File API (First Preview)](https://openjdk.org/jeps/459)
- [java.lang.classfile 包文档](https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/lang/classfile/package-summary.html)
