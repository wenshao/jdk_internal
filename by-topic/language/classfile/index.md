# Class File API

> java.lang.classfile - 标准 class 文件读写 API

---

## 快速概览

```
JDK 21 ───── JDK 22 ───── JDK 23 ───── JDK 24 ───── JDK 26
   │             │             │             │             │
 内部工具      预览版        第二次预览      正式版        增强
 jdk.internal  JEP 459       JEP 466       JEP 484       持续优化
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

Class File API 从内部工具到正式 API 的完整演进。

→ [查看时间线](timeline.md)

### [内部实现](implementation.md)

API 设计、源码结构、性能优化。

→ [查看实现](implementation.md)

---

## 贡献者

### JEP 负责人

| JEP | 标题 | Author | Owner |
|-----|------|--------|-------|
| JEP 459 | Class-File API (First Preview) | Brian Goetz | Adam Sotona |
| JEP 466 | Class-File API (Second Preview) | - | Adam Sotona |
| JEP 484 | Class-File API (Final) | Brian Goetz | Adam Sotona |

### Adam Sotona

- **职位**: Principal Java Engineer, Oracle
- **地点**: Prague, Czech Republic
- **经验**: 25+ 年 Java 技术开发经验
- **专长**: Java, RDF, SPARQL, Semantic Technologies, Linked Data, Big Data
- **主要贡献**:
  - Class File API 实现负责人 (JDK-8294982)
  - 56+ 版本迭代 (v6 → v56)
  - 从 `jdk.internal.classfile` 到标准 API 的迁移主导者

> "The Class-File API provides a standard way to parse, generate, and transform Java class files, eventually replacing ASM within the JDK."
> — Adam Sotona, RFR: 8294982

### Brian Goetz

- **职位**: Java Language Architect, Oracle
- **角色**: JEP Author, API 设计指导
- **主要贡献**:
  - Class File API 整体架构设计
  - 与 Lambda、Stream API 的一致性设计

---

## 关键 Bug 与 PR

| Bug ID | 描述 | 状态 |
|--------|------|------|
| JDK-8294982 | Implementation of Classfile API | 已集成 |
| JDK-8308753 | Class-File API transition to Preview | 已集成 |
| JDK-8308754 | Class-File API (Preview) | 已集成 |
| JDK-8334714 | Implement JEP 484: Class-File API | 已集成 |
| JDK-8338981 | Access to private classes during transformation | 已集成 |

### PR #10982

- **标题**: Implementation of Classfile API
- **链接**: https://git.openjdk.org/jdk/pull/10982
- **范围**: API、测试、基准测试
- **版本迭代**: 56+ 个版本

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
    System.out.println(method.methodType().stringValue());
});

// 遍历字段
classModel.fields().forEach(field -> {
    System.out.println(field.fieldName());
    System.out.println(field.fieldType().stringValue());
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
            MethodTypeDesc.of("([Ljava/lang/String;)V"),
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

// 写入文件
Files.write(Path.of("HelloWorld.class"), bytecode);
```

### 转换 Class 文件

```java
// 添加方法调用追踪
byte[] transformed = ClassFile.of().transformClass(
    ClassFile.of().parse(originalBytes),
    ClassTransform.transformingMethods(
        (classBuilder, method, methodBuilder) -> {
            // 在每个方法开始添加日志
            methodBuilder.withCode(
                codeBuilder -> {
                    // 创建日志代码
                    Label start = codeBuilder.newLabel();
                    codeBuilder.labelBinding(start);

                    codeBuilder.getstatic(ClassDesc.of("java/lang/System"), "out",
                                          ClassDesc.of("java/io/PrintStream"))
                               .ldc("Method: " + method.methodName().stringValue())
                               .invokevirtual(
                                   ClassDesc.of("java/io/PrintStream"),
                                   "println",
                                   MethodTypeDesc.of("(Ljava/lang/String;)V"));

                    // 原方法体
                    codeBuilder.with(method.code().orElseThrow());
                }
            );
        }
    )
);
```

---

## 与 ASM 对比

| 特性 | Class File API | ASM |
|------|----------------|-----|
| **来源** | JDK 标准库 | 外部依赖 |
| **许可证** | GPL + Classpath Exception | BSD |
| **API 风格** | 流式函数式 | 访问者模式 |
| **类型安全** | 编译时检查 | 运行时检查 |
| **不可变性** | Model 不可变 | 可变 |
| **维护** | Oracle/JDK 社区 | ObjectWeb |

### 迁移示例

```java
// ASM 代码
ClassReader cr = new ClassReader(bytes);
ClassWriter cw = new ClassWriter(cr, 0);
cr.accept(new ClassVisitor(Opcodes.ASM9, cw) {
    @Override
    public MethodVisitor visitMethod(int access, String name, String descriptor,
                                     String signature, String[] exceptions) {
        return new MethodVisitor(api, super.visitMethod(access, name, descriptor, signature, exceptions)) {
            @Override
            public void visitCode() {
                // 插入代码
                super.visitCode();
                mv.visitFieldInsn(GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");
                mv.visitLdcInsn("Method: " + name);
                mv.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream", "println", "(Ljava/lang/String;)V", false);
            }
        };
    }
}, 0);

// Class File API 等价代码
byte[] transformed = ClassFile.of().transformClass(
    ClassFile.of().parse(bytes),
    ClassTransform.transformingMethods((cb, m, mb) -> {
        mb.withCode(code -> {
            code.getstatic(ClassDesc.of("java/lang/System"), "out",
                          ClassDesc.of("java/io/PrintStream"))
               .ldc("Method: " + m.methodName().stringValue())
               .invokevirtual(ClassDesc.of("java/io/PrintStream"), "println",
                            MethodTypeDesc.of("(Ljava/lang/String;)V"))
               .with(m.code().orElseThrow());
        });
    })
);
```

---

## 内部实现

### 源码结构

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
│   ├── Attributes.java               # 属性工厂
│   ├── CodeAttribute.java            # Code 属性
│   ├── DeprecatedAttribute.java      # @Deprecated
│   ├── SignatureAttribute.java       # 泛型签名
│   └── ...
├── constantpool/                     # 常量池
│   ├── ConstantPool.java             # 常量池接口
│   ├── ConstantPoolBuilder.java      # 常量池构建器
│   ├── PoolEntry.java                # 常量池条目
│   └── ...
├── enums/                            # 枚举和标志
│   ├── AccessFlag.java               # 访问标志
│   ├── Opcode.java                   # 操作码
│   ├── TypeKind.java                 # 类型种类
│   └── ...
└── instruction/                      # 指令
    ├── ArrayLoadInstruction.java
    ├── ArrayStoreInstruction.java
    ├── ConstantInstruction.java
    ├── FieldInstruction.java
    ├── InvokeInstruction.java
    └── ...

src/java.base/share/classes/jdk/internal/classfile/
├── impl/                             # 内部实现
│   ├── ClassImpl.java                # ClassModel 实现
│   ├── ClassBuilderImpl.java         # ClassBuilder 实现
│   ├── MethodImpl.java               # MethodModel 实现
│   ├── CodeBuilderImpl.java          # CodeBuilder 实现
│   ├── Util.java                     # 工具方法
│   ├── SplitConstantPool.java        # 常量池处理
│   ├── Verifier.java                 # 字节码验证
│   └── ...
└── instruction/                      # 内部指令实现
    ├── BoundInstruction.java
    ├── SimpleInstruction.java
    └── ...
```

### 关键内部类

| 类 | 作用 | 访问级别 |
|---|------|----------|
| `jdk.internal.classfile.impl.ClassImpl` | ClassModel 实现 | 内部 |
| `jdk.internal.classfile.impl.BufWriter` | 字节码写入器 | 内部 |
| `jdk.internal.classfile.impl.Util` | 工具方法 | 内部 |
| `jdk.internal.classfile.impl.DirectClassBuilder` | 直接类构建器 | 内部 |
| `jdk.internal.classfile.impl.NonterminalCode` | 代码验证 | 内部 |

---

## 邮件列表讨论

### RFR: JDK-8294982 (v56)

**主题**: RFR: 8294982: Implementation of Classfile API [v56]

> "This is the root PR for the Classfile API implementation, including comprehensive tests and benchmarks."
> — Adam Sotona, build-dev@openjdk.org

**讨论要点**:
- 56 个版本迭代
- 完整的测试覆盖
- JMH 基准测试

### RFR: JDK-8308753 (v2)

**主题**: RFR: 8308753: Class-File API transition to Preview [v2]

> "All JDK modules using the Classfile API are newly participating in the preview feature."
> — Adam Sotona, compiler-dev@openjdk.org

**变更内容**:
- 从 `jdk.internal.classfile` 迁移到 `java.lang.classfile`
- 所有使用该 API 的 JDK 模块启用预览
- javac 相关修改

---

## VM 参数

```bash
# 启用预览功能 (JDK 22-23)
--enable-preview

# 类加载日志
-Xlog:class+load=info

# 验证选项
-XX:+VerifyAppCDS                 # 验证 AOT 编译的类
-XX:+VerifyRecursive              # 递归验证
```

---

## 相关链接

- [JEP 484: Class-File API](https://openjdk.org/jeps/484)
- [JEP 466: Class-File API (Second Preview)](https://openjdk.org/jeps/466)
- [JEP 459: Class-File API (First Preview)](https://openjdk.org/jeps/459)
- [PR #10982: Implementation of Classfile API](https://git.openjdk.org/jdk/pull/10982)
- [JDK-8294982: Classfile API Implementation](https://bugs.openjdk.org/browse/JDK-8294982)
- [ClassFile API Documentation](https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/lang/classfile/package-summary.html)
- [mail.openjdk.org: Class-File API Discussions](https://mail.openjdk.org/archives/list/compiler-dev@openjdk.org/)
