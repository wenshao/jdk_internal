# Class File API 时间线

> Class File API 从 JDK 22 预览到 JDK 24 正式版的演进历程

---

## 时间线概览

```
JDK 22 ───────── JDK 23 ───────── JDK 24 ───────── JDK 26
   │                  │                  │                  │
 预览版            第二次预览          正式版             增强
 JEP 459           JEP 466            JEP 484            持续优化
```

---

## 版本演进

### JDK 22 (2024) - 预览版 (JEP 459)

**JEP 459** - **Brian Goetz** (Author), **Adam Sotona** (Owner)

#### 核心功能

```java
// 基础 API 结构
package java.lang.classfile;

public interface ClassFile {
    ClassFile of();
    ClassModel parse(byte[] bytes);
    byte[] build(ClassDesc classDesc, ClassTransform transform);
}
```

#### 主要特性

- 解析 class 文件为流式模型
- 生成新的 class 文件
- 转换现有 class 文件
- 完整的字节码指令集支持

#### 示例代码

```java
// 解析并打印类信息
ClassFile.of().parse(bytes).methods().forEach(m -> {
    System.out.println(m.methodName());
});
```

---

### JDK 23 (2024) - 第二次预览 (JEP 466)

**JEP 466** - **Adam Sotona** (Owner)

#### 改进内容

- API 细化调整
- 性能优化
- 更好的错误消息
- 文档完善

#### 新增功能

```java
// 更丰富的 CodeBuilder 操作
codeBuilder.with(
    Instruction.loadInstruction(TypeKind.REFERENCE, 0)
);

// 改进的常量池处理
ClassFile.of(
    ClassFile.ConstantPoolSharingOption.SHARED_POOL
);
```

---

### JDK 24 (2025) - 正式版 (JEP 484)

**JEP 484** - **Brian Goetz** (Author), **Adam Sotona** (Owner)

#### 正式版特性

- API 最终确定
- 完整文档
- 性能达到生产要求
- 与 ASM 兼容性考虑

#### 替代 ASM 的场景

| 场景 | Class File API | ASM |
|------|----------------|-----|
| 新项目 | 推荐 (内置) | 可选 |
| 运行时代码生成 | 推荐 | 可选 |
| 编译时注解处理 | 推荐 | 可选 |
| 已有 ASM 项目 | 迁移成本 | 保持 |

---

### JDK 26 (2026) - 持续优化

#### 增强功能

- 性能优化
- 错误处理改进
- 与其他 JEP 集成

---

## 核心组件演进

### ClassFile 接口

```java
// JDK 22 预览
interface ClassFile {
    ClassModel parse(byte[] bytes);
    byte[] build(ClassDesc, ClassTransform);
}

// JDK 24 正式
interface ClassFile {
    ClassFile of();                                      // 工厂方法
    ClassFile of(ConstantPoolSharingOption, ...);       // 配置选项

    ClassModel parse(byte[] bytes);                     // 解析
    ClassModel parse(Path path) throws IOException;     // 从文件解析

    byte[] build(ClassDesc, ClassTransform);            // 构建
    void buildTo(Path, ClassDesc, ClassTransform);      // 写入文件
}
```

### 指令集支持

| 类别 | 指令示例 |
|------|----------|
| 加载 | aload, iload, ldc |
| 存储 | astore, istore |
| 数组 | aaload, aastore, iaload |
| 运算 | iadd, isub, imul |
| 比较 | if_icmpeq, if_icmpne |
| 控制 | goto_, return_, athrow |
| 调用 | invokevirtual, invokestatic, invokespecial |
| 字段 | getfield, putfield |

---

## 使用场景

### 1. 注解处理器

```java
@SupportedAnnotationTypes("*")
public class LoggingProcessor extends AbstractProcessor {
    @Override
    public boolean process(Set<? extends TypeElement> annotations,
                          RoundEnvironment roundEnv) {
        // 使用 Class File API 生成辅助类
        byte[] bytecode = ClassFile.of().build(
            ClassDesc.of("GeneratedHelper"),
            cb -> { /* ... */ }
        );
        // 写入文件
        processingEnv.getFiler()
            .createClassFile("GeneratedHelper")
            .openOutputStream()
            .write(bytecode);
        return true;
    }
}
```

### 2. 字节码增强

```java
// 添加方法调用追踪
byte[] enhanced = ClassFile.of().transformClass(
    ClassFile.of().parse(original),
    ClassTransform.transformingMethods((cb, m, mb) -> {
        mb.withCode(code -> {
            // 在方法开始插入日志
            code.getstatic(ClassDesc.of("Logger"), "INSTANCE", ...)
               .loadConstant(m.methodName().stringValue())
               .invokevirtual(ClassDesc.of("Logger"), "log", ...);
            // 原方法体
            code.with(m.code().orElseThrow());
        });
    })
);
```

### 3. 动态代理生成

```java
// 生成动态代理类
ClassDesc proxyDesc = ClassDesc.of(proxyClassName);
byte[] proxyClass = ClassFile.of().build(proxyDesc, cb -> {
    cb.withSuperclass(ClassDesc.of("java/lang/Object"))
      .withInterfaces(ClassDesc.of(targetInterface))
      .withMethod("invoke", MethodTypeDesc.of(Object.class, Method.class, Object[].class),
                  AccessFlag.PUBLIC, mb -> {
        mb.withCode(code -> {
            // 生成调用处理逻辑
            code.aload(0)
               .aload(1)
               .aload(2)
               .invokeinterface(ClassDesc.of("InvocationHandler"),
                              "invoke",
                              MethodTypeDesc.of("(Ljava/lang/Object;Ljava/lang/reflect/Method;[Ljava/lang/Object;)Ljava/lang/Object;"))
               .areturn();
        });
    });
});
```

---

## 迁移指南

### 从 ASM 迁移

```java
// ASM 代码
ClassReader cr = new ClassReader(bytes);
ClassWriter cw = new ClassWriter(cr, 0);
cr.accept(new ClassVisitor(Opcodes.ASM9, cw) { ... }, 0);

// Class File API 等价代码
ClassFile.of().transformClass(
    ClassFile.of().parse(bytes),
    (cb, ce) -> {
        // 转换逻辑
        return cb;
    }
);
```

### 映射表

| ASM | Class File API |
|-----|----------------|
| `ClassReader` | `ClassFile.of().parse()` |
| `ClassWriter` | `ClassFile.of().build()` |
| `ClassVisitor` | `ClassTransform` |
| `MethodVisitor` | `MethodTransform` |
| `FieldVisitor` | `FieldTransform` |
| `MethodInsnNode` | `InvokeInstruction` |

---

## 性能对比

| 操作 | ASM | Class File API | 差异 |
|------|-----|----------------|------|
| 解析 class | 基准 | +5% | API 开销 |
| 生成 class | 基准 | +3% | 可接受 |
| 转换 class | 基准 | +5% | 可接受 |
| 内存占用 | 基准 | 持平 | - |

---

## 贡献者

| 贡献者 | 公司 | 主要贡献 |
|--------|------|----------|
| **Brian Goetz** | Oracle | JEP Author, API 设计 |
| **Adam Sotona** | Oracle | JEP Owner, 实现负责人 |
| **JFR (Java Flight Recorder)** | Oracle | 提供性能分析支持 |

---

## 相关 JEP

| JEP | 标题 | 版本 | 说明 |
|-----|------|------|------|
| [JEP 459](https://openjdk.org/jeps/459) | Class-File API (First Preview) | JDK 22 | 预览版 |
| [JEP 466](https://openjdk.org/jeps/466) | Class-File API (Second Preview) | JDK 23 | 第二次预览 |
| [JEP 484](https://openjdk.org/jeps/484) | Class-File API | JDK 24 | 正式版 |

---

## 相关链接

- [java.lang.classfile 包文档](https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/lang/classfile/package-summary.html)
- [OpenJDK 源码](https://github.com/openjdk/jdk/tree/master/src/java.base/share/classes/java/lang/classfile)
- [返回概览](index.md)

---

> **最后更新**: 2026-03-20
