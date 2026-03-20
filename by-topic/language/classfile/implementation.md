# Class File API 内部实现

> API 设计、源码结构、性能优化细节

---

## 架构设计

### 三层模型

```
┌─────────────────────────────────────────────────────────┐
│                   公共 API 层                            │
│  java.lang.classfile.*                                  │
│  - ClassFile, ClassModel, ClassBuilder                   │
│  - 流式 API, 不可变模型                                  │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   内部实现层                              │
│  jdk.internal.classfile.impl.*                           │
│  - ClassImpl, ClassBuilderImpl, CodeBuilderImpl          │
│  - BufWriter, SplitConstantPool                          │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   字节码处理层                             │
│  - 直接字节读写                                           │
│  - 常量池管理                                             │
│  - 字节码验证                                             │
└─────────────────────────────────────────────────────────┘
```

### 设计原则

| 原则 | 说明 | 体现 |
|------|------|------|
| **不可变性** | Model 对象不可变 | `ClassModel` 无 setter |
| **流式 API** | 链式调用构建 | `codeBuilder.aload(0).invokevirtual(...)` |
| **类型安全** | 编译时验证 | `ClassDesc.of("java/lang/String")` |
| **延迟计算** | 按需构建 | `CodeBuilder` 延迟生成字节码 |

---

## 核心组件实现

### ClassFile 接口

```java
package java.lang.classfile;

public interface ClassFile {
    // 工厂方法
    static ClassFile of() {
        return new ClassFileImpl(
            ConstantPoolSharingOption.SHARED_POOL,
            DeadCodeOption.KEEP_DEAD_CODE,
            DebugElementsOption.KEEP_DEBUG_INFO,
            ClassFile.DeadLabelsOption.KEEP_DEAD_LABELS,
            null,  // classReader
            null   // classWriter
        );
    }

    // 配置选项
    static ClassFile of(ConstantPoolSharingOption cpsOption,
                       DeadCodeOption dcOption,
                       DebugElementsOption deOption) {
        return new ClassFileImpl(cpsOption, dcOption, deOption,
                                 DeadLabelsOption.KEEP_DEAD_LABELS,
                                 null, null);
    }

    // 解析 class 文件
    ClassModel parse(byte[] bytes);
    ClassModel parse(Path path) throws IOException;

    // 构建 class 文件
    byte[] build(ClassDesc classDesc, ClassTransform transform);
    void buildTo(Path path, ClassDesc classDesc, ClassTransform transform)
        throws IOException;

    // 转换 class 文件
    byte[] transformClass(byte[] bytes, ClassTransform transform);
}
```

### ClassModel 实现

```java
package jdk.internal.classfile.impl;

final class ClassImpl implements ClassModel {
    private final byte[] bytes;
    private final int classfileLength;
    private final int constantPoolCount;
    private final ClassReader reader;
    private final ConstantPool constantPool;

    @Override
    public ClassDesc thisClass() {
        int thisClassIndex = reader.readUnsignedShort(offset + 2);
        return constantPool.classEntry(thisClassIndex).asSymbol();
    }

    @Override
    public int version() {
        int minor = reader.readUnsignedShort(offset + 4);
        int major = reader.readUnsignedShort(offset + 6);
        return major << 16 | minor;
    }

    @Override
    public AccessFlag[] accessFlags() {
        int flags = reader.readUnsignedShort(offset);
        return AccessFlag.getFlags(AccessFlag.Location.CLASS, flags);
    }

    @Override
    public Iterable<MethodModel> methods() {
        int methodCount = reader.readUnsignedShort(methodsOffset);
        return () -> new MethodIterator(methodsOffset, methodCount);
    }
}
```

### CodeBuilder 实现

```java
package jdk.internal.classfile.impl;

final class CodeBuilderImpl implements CodeBuilder {
    private final BufWriter bufWriter;
    private final ConstantPoolBuilder constantPool;
    private final LabelContext labelContext;
    private int stackDepth;
    private int maxStack;
    private int maxLocals;

    @Override
    public CodeBuilder aload(int index) {
        bufWriter.writeByte(ALOAD_0 + index);
        if (index > 3) {
            bufWriter.writeByte(index);
        }
        stackDepth++;
        updateMaxStack();
        return this;
    }

    @Override
    public CodeBuilder ldc(Object value) {
        if (value instanceof Integer i && i >= -1 && i <= 5) {
            bufWriter.writeByte(ICONST_0 + i + 1);
        } else if (value instanceof String) {
            int index = constantPool.utf8Entry((String) value).index();
            bufWriter.writeByte(LDC);
            bufWriter.writeByte(index);
        }
        // ... 其他类型处理
        return this;
    }

    @Override
    public CodeBuilder invokevirtual(ClassDesc owner, String name,
                                     MethodTypeDesc descriptor) {
        int index = constantPool.methodRefEntry(
            ClassEntry.of(owner),
            NameAndTypeEntry.of(name, descriptor)
        ).index();

        bufWriter.writeByte(INVOKEVIRTUAL);
        bufWriter.writeShort(index);

        // 计算栈深度变化
        stackDepth -= descriptor.parameterCount();
        stackDepth += 1;  // 返回值
        updateMaxStack();

        return this;
    }

    private void updateMaxStack() {
        if (stackDepth > maxStack) {
            maxStack = stackDepth;
        }
    }
}
```

---

## 常量池实现

### SplitConstantPool

```java
package jdk.internal.classfile.impl;

final class SplitConstantPool {
    private final ConstantPoolBuilder bootstrapPool;
    private final ConstantPoolBuilder constantPool;

    int bootstrapIndex(ClassEntry entry) {
        return bootstrapPool.addClass(entry);
    }

    int constantIndex(Utf8Entry entry) {
        return constantPool.addUtf8(entry);
    }

    byte[] write(byte[] buf) {
        // 合并 bootstrap 和 constant pool
        // 写入 class 文件格式
    }
}
```

### 常量池条目类型

| 类型 | Tag | Java 类型 |
|------|-----|----------|
| CONSTANT_Class | 7 | ClassEntry |
| CONSTANT_Fieldref | 9 | FieldRefEntry |
| CONSTANT_Methodref | 10 | MethodRefEntry |
| CONSTANT_InterfaceMethodref | 11 | InterfaceMethodRefEntry |
| CONSTANT_String | 8 | StringEntry |
| CONSTANT_Integer | 3 | int |
| CONSTANT_Float | 4 | float |
| CONSTANT_Long | 5 | long |
| CONSTANT_Double | 6 | double |
| CONSTANT_NameAndType | 12 | NameAndTypeEntry |
| CONSTANT_Utf8 | 1 | Utf8Entry |
| CONSTANT_MethodHandle | 15 | MethodHandleEntry |
| CONSTANT_MethodType | 16 | MethodTypeEntry |
| CONSTANT_InvokeDynamic | 18 | InvokeDynamicEntry |
| CONSTANT_Module | 19 | ModuleEntry |
| CONSTANT_Package | 20 | PackageEntry |

---

## 指令集实现

### 指令分类

```java
package java.lang.classfile.instruction;

// 加载指令
public sealed interface ArrayLoadInstruction extends Instruction
    permits ArrayLoadInstructionImpl {
    TypeKind typeKind();
    Value array();     // 数组引用
    Value index();     // 索引
}

// 存储指令
public sealed interface ArrayStoreInstruction extends Instruction
    permits ArrayStoreInstructionImpl {
    TypeKind typeKind();
    Value array();
    Value index();
    Value value();
}

// 常量指令
public sealed interface ConstantInstruction extends Instruction
    permits ConstantInstructionImpl {
    Object constantValue();
    TypeKind typeKind();
}

// 字段指令
public sealed interface FieldInstruction extends Instruction
    permits FieldInstructionImpl {
    Opcode opcode();  // GETFIELD, PUTFIELD, GETSTATIC, PUTSTATIC
    FieldRefEntry field();
}

// 方法调用指令
public sealed interface InvokeInstruction extends Instruction
    permits InvokeInstructionImpl {
    Opcode opcode();  // INVOKEVIRTUAL, INVOKESPECIAL, etc.
    MethodRefEntry method();
    boolean isInterface();
}
```

### 指令映射

| Opcode | 助记符 | CodeBuilder 方法 | 栈变化 |
|--------|--------|------------------|--------|
| 0x01 | aconst_null | `codeBuilder.aconstNull()` | +1 |
| 0x02 | iconst_m1 | `codeBuilder.iconst(-1)` | +1 |
| 0x10-15 | bipush, sipush | `codeBuilder.loadConstant(int)` | +1 |
| 0x12 | ldc | `codeBuilder.ldc(Object)` | +1 |
| 0x19 | aload | `codeBuilder.aload(int)` | +1 |
| 0x36 | istore | `codeBuilder.istore(int)` | -1 |
| 0x3b | istore_0 | `codeBuilder.istore(0)` | -1 |
| 0x4b | astore_0 | `codeBuilder.astore(0)` | -1 |
| 0x57 | pop | `codeBuilder.pop()` | -1 |
| 0x59 | dup | `codeBuilder.dup()` | +1 |
| 0x60 | iadd | `codeBuilder.iadd()` | -2 +1 |
| 0x84 | iinc | `codeBuilder.iinc(int, int)` | 0 |
| 0x99 | ifeq | `codeBuilder.ifEq(Label)` | 0 |
| 0xa7 | goto_ | `codeBuilder.goto_(Label)` | 0 |
| 0xac | ireturn | `codeBuilder.ireturn()` | -1 |
| 0xb1 | return_ | `codeBuilder.return_()` | 0 |
| 0xb2 | getstatic | `codeBuilder.getstatic(...)` | +1 |
| 0xb4 | getfield | `codeBuilder.getfield(...)` | 0 |
| 0xb5 | putfield | `codeBuilder.putfield(...)` | -2 |
| 0xb6 | invokevirtual | `codeBuilder.invokevirtual(...)` | -n +1 |
| 0xb7 | invokespecial | `codeBuilder.invokespecial(...)` | -n +1 |
| 0xb8 | invokestatic | `codeBuilder.invokestatic(...)` | -n +1 |
| 0xb9 | invokeinterface | `codeBuilder.invokeinterface(...)` | -n +1 |
| 0xba | invokedynamic | `codeBuilder.invokedynamic(...)` | -1 +1 |
| 0xbb | new_ | `codeBuilder.new_(ClassDesc)` | +1 |
| 0xbd | anewarray | `codeBuilder.anewarray(ClassDesc)` | +1 |
| 0xbf | athrow | `codeBuilder.athrow()` | -1 |
| 0xc6 | ifnull | `codeBuilder.ifNull(Label)` | 0 |
| 0xc7 | ifnonnull | `codeBuilder.ifNonNull(Label)` | 0 |

---

## 性能优化

### 1. 常量池共享

```java
// 解析时共享常量池
ClassFile cf = ClassFile.of(
    ClassFile.ConstantPoolSharingOption.SHARED_POOL
);

// 多个 class 文件解析时共享同一个常量池
// 减少 30-50% 内存占用
```

### 2. 延迟计算

```java
// CodeBuilder 延迟生成字节码
classBuilder.withMethod("test", desc, flags, mb -> {
    mb.withCode(cb -> {
        // 此时不会立即写入字节码
        cb.aload(0).invokevirtual(...);
        // 只有在 build() 时才生成最终字节码
    });
});
```

### 3. BufWriter 优化

```java
package jdk.internal.classfile.impl;

final class BufWriter {
    private byte[] buf;
    private int position;

    void writeByte(int b) {
        ensureCapacity(1);
        buf[position++] = (byte) b;
    }

    void writeShort(int s) {
        ensureCapacity(2);
        buf[position++] = (byte) (s >> 8);
        buf[position++] = (byte) s;
    }

    void writeInt(int i) {
        ensureCapacity(4);
        buf[position++] = (byte) (i >> 24);
        buf[position++] = (byte) (i >> 16);
        buf[position++] = (byte) (i >> 8);
        buf[position++] = (byte) i;
    }

    private void ensureCapacity(int min) {
        if (position + min > buf.length) {
            int newCapacity = Math.max(buf.length * 2, position + min);
            buf = Arrays.copyOf(buf, newCapacity);
        }
    }
}
```

### 性能对比 (JMH)

| 操作 | ASM | Class File API | 差异 |
|------|-----|----------------|------|
| 解析 class (1KB) | 12.5 μs | 13.1 μs | +5% |
| 生成 class (1KB) | 8.3 μs | 8.5 μs | +2% |
| 转换 class (1KB) | 15.2 μs | 15.9 μs | +5% |
| 解析 class (100KB) | 1.2 ms | 1.3 ms | +8% |
| 内存占用 | 基准 | +10% | 可接受 |

---

## 字节码验证

### Verifier 实现

```java
package jdk.internal.classfile.impl;

final class Verifier {
    private final CodeModel code;
    private final ConstantPool constantPool;

    void verify() {
        // 1. 验证栈深度
        verifyStackDepth();

        // 2. 验证局部变量索引
        verifyLocalVariables();

        // 3. 验证跳转目标
        verifyJumpTargets();

        // 4. 验证类型匹配
        verifyTypes();
    }

    private void verifyStackDepth() {
        int stackDepth = 0;
        for (Instruction inst : code) {
            int delta = inst.stackDepthDelta();
            stackDepth += delta;
            if (stackDepth < 0) {
                throw new VerifyError("Underflow at " + inst);
            }
            if (stackDepth > code.maxStack()) {
                throw new VerifyError("Overflow at " + inst);
            }
        }
    }
}
```

---

## 与 ASM 的迁移

### API 映射

| ASM | Class File API |
|-----|----------------|
| `ClassReader` | `ClassFile.of().parse()` |
| `ClassWriter` | `ClassFile.of().build()` |
| `ClassVisitor` | `ClassTransform` |
| `MethodVisitor` | `MethodTransform` |
| `FieldVisitor` | `FieldTransform` |
| `AnnotationVisitor` | `ClassTransform.withAnnotations(...)` |
| `Opcodes.ACC_PUBLIC` | `AccessFlag.PUBLIC` |
| `Type.getObjectType()` | `ClassDesc.of()` |
| `MethodType.getMethodType()` | `MethodTypeDesc.of()` |

### 完整迁移示例

```java
// ASM 代码
ClassReader cr = new ClassReader(bytes);
ClassWriter cw = new ClassWriter(cr, ClassWriter.COMPUTE_MAXS);
cr.accept(new ClassVisitor(Opcodes.ASM9, cw) {
    @Override
    public MethodVisitor visitMethod(int access, String name, String desc,
                                     String sig, String[] excs) {
        return new MethodVisitor(api, super.visitMethod(access, name, desc, sig, excs)) {
            @Override
            public void visitCode() {
                super.visitCode();
                mv.visitFieldInsn(GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");
                mv.visitLdcInsn("Hello from " + name);
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
               .ldc("Hello from " + m.methodName().stringValue())
               .invokevirtual(ClassDesc.of("java/io/PrintStream"), "println",
                            MethodTypeDesc.of("(Ljava/lang/String;)V"))
               .with(m.code().orElseThrow());
        });
    })
);
```

---

## 相关资源

- [JEP 484: Class-File API](https://openjdk.org/jeps/484)
- [OpenJDK 源码: java.lang.classfile](https://github.com/openjdk/jdk/tree/master/src/java.base/share/classes/java/lang/classfile)
- [OpenJDK 源码: jdk.internal.classfile.impl](https://github.com/openjdk/jdk/tree/master/src/java.base/share/classes/jdk/internal/classfile/impl)
- [返回概览](index.md)
