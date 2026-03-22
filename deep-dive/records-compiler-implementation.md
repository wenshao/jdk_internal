# Record 编译器实现深度解析

> 基于 JDK 源码 `JavacParser`、`TypeEnter`、`Lower`、`Check`、`ClassWriter`
> 以及运行时 `java.lang.runtime.ObjectMethods` 的实际实现。所有代码引用均来自真实源码。

---

## 目录

1. [编译总览：从源码到字节码](#1-编译总览从源码到字节码)
2. [解析阶段：语法识别](#2-解析阶段语法识别)
3. [类型录入阶段：符号表构建](#3-类型录入阶段符号表构建)
4. [降低阶段：方法体生成](#4-降低阶段方法体生成)
5. [规范构造器与访问器生成](#5-规范构造器与访问器生成)
6. [ObjectMethods.bootstrap 与 invokedynamic](#6-objectmethodsbootstrap-与-invokedynamic)
7. [字节码分析](#7-字节码分析)
8. [Record 序列化安全](#8-record-序列化安全)
9. [与 Sealed Classes 配合](#9-与-sealed-classes-配合)
10. [编译器限制与检查](#10-编译器限制与检查)
11. [设计决策总结](#11-设计决策总结)

---

## 1. 编译总览：从源码到字节码

### 编译流水线 (Compilation Pipeline)

```
源码 record Point(int x, int y) { }
  │
  ├─ Parse         ── JavacParser.recordDeclaration()  → 设置 Flags.RECORD，生成 AST
  ├─ Enter         ── TypeEnter.RecordPhase/MembersPhase → 创建 RecordComponent，注入隐式成员符号
  ├─ Attr/Check    ── 类型检查 + 限制验证（不能 abstract，隐式 final 等）
  ├─ Lower         ── Lower.visitRecordDef() → 生成方法体（invokedynamic + 访问器 + 构造器赋值）
  └─ Gen           ── ClassWriter → 写入 Record 属性，输出 class 文件
```

### 一个 record 展开为什么

```java
// 编译器等价展开 (Compiler-equivalent expansion)
public final class Point extends java.lang.Record {
    private final int x;
    private final int y;

    public Point(int x, int y) {     // 规范构造器 (Canonical Constructor)
        super(); this.x = x; this.y = y;
    }
    public int x() { return this.x; } // 组件访问器 — 非 getX() 风格
    public int y() { return this.y; }

    // 以下三个方法体为 invokedynamic 调用 ObjectMethods.bootstrap
    public final String toString()          { /* indy */ }
    public final int hashCode()             { /* indy */ }
    public final boolean equals(Object o)   { /* indy */ }
}
```

---

## 2. 解析阶段：语法识别

### JavacParser.recordDeclaration() — `JavacParser.java:4396`

```java
protected JCClassDecl recordDeclaration(JCModifiers mods, Comment dc) {
    nextToken();
    mods.flags |= Flags.RECORD;                              // [1] 设置 RECORD 标志
    Name name = typeName();
    List<JCTypeParameter> typarams = typeParametersOpt();     // [2] 泛型参数
    List<JCVariableDecl> headerFields = formalParameters(false, true); // [3] recordComponent=true
    List<JCExpression> implementing = List.nil();
    if (token.kind == IMPLEMENTS) { ... }                     // [4] 只能 implements，不能 extends
    List<JCTree> defs = classInterfaceOrRecordBody(name, false, true);
    // [5] 头部字段 prepend 到 defs（作为隐式字段声明）
    for (int i = fields.size() - 1; i >= 0; i--)
        defs = defs.prepend(fields.get(i));
    return F.at(pos).ClassDef(mods, name, typarams, null/*extending*/, implementing, defs);
}
```

**Compact constructor (紧凑构造器)** 处理：当 Parser 检测到无参数列表的构造器体 +
`COMPACT_RECORD_CONSTRUCTOR` 标志时，自动将头部参数复制到构造器参数列表（`JavacParser.java:4422-4432`）。

---

## 3. 类型录入阶段：符号表构建

### RecordPhase — 字段与组件关联 (`TypeEnter.java:1025-1067`)

```java
if ((sym.flags_field & RECORD) != 0) {
    List<JCVariableDecl> fields = TreeInfo.recordFields(tree);
    // 为每个字段创建对应的 RecordComponent，传播注解
    for (JCVariableDecl field : fields) {
        RecordComponent rc = getRecordComponentAt(sym, fieldPos);
        sym.createRecordComponent(rc, rcDecl, field.sym);
    }
}
```

### MembersPhase — 隐式成员注入 (`TypeEnter.java:1279-1331`)

`addRecordMembersIfNeeded()` 检查用户是否已自定义方法，未定义则注入：

```java
private void addRecordMembersIfNeeded(JCClassDecl tree, Env<AttrContext> env) {
    if (lookupMethod(tree.sym, names.toString, List.nil()) == null) {
        // 标志组合：PUBLIC | RECORD | FINAL | GENERATED_MEMBER
        // RECORD 标志表示编译器生成，Lower 据此判断是否生成 invokedynamic
        JCMethodDecl toString = make.MethodDef(
            make.Modifiers(PUBLIC | RECORD | FINAL | GENERATED_MEMBER),
            names.toString, make.Type(syms.stringType), ...);
        memberEnter.memberEnter(toString, env);
    }
    // hashCode、equals 同理...

    // 添加访问器（仅当用户未自定义时）
    recordFields.stream()
        .filter(vd -> lookupMethod(syms.objectType.tsym, vd.name, List.nil()) == null)
        .forEach(vd -> addAccessor(vd, env));
}
```

### 访问器符号注入 (`TypeEnter.java:1192-1226`)

```java
private void addAccessor(JCVariableDecl tree, Env<AttrContext> env) {
    MethodSymbol implSym = lookupMethod(env.enclClass.sym, tree.sym.name, List.nil());
    if (implSym == null || (implSym.flags_field & GENERATED_MEMBER) != 0) {
        JCMethodDecl getter = make.MethodDef(
            make.Modifiers(PUBLIC | GENERATED_MEMBER, originalAnnos),
            tree.sym.name,       // 方法名 = 字段名 (x, 非 getX)
            tc.copy(recordField.vartype), List.nil()/*无参数*/, ...);
        memberEnter.memberEnter(getter, env);
        rec.accessor = getter.sym;
    } else {
        rec.accessor = implSym;  // 用户自定义了访问器
    }
}
```

---

## 4. 降低阶段：方法体生成

### Lower.visitRecordDef() — `Lower.java:2465-2484`

```java
private void visitRecordDef(JCClassDecl tree) {
    List<VarSymbol> vars = recordVars(tree.type);
    // [1] 为每个组件创建 MethodHandle 引用（invokedynamic 静态参数）
    MethodHandleSymbol[] getterMethHandles = new MethodHandleSymbol[vars.size()];
    for (VarSymbol var : vars)
        getterMethHandles[index++] = var.asMethodHandle(true);

    // [2] 生成访问器方法体：return this.field;
    tree.defs = tree.defs.appendList(generateMandatedAccessors(tree));

    // [3] 生成 toString/hashCode/equals — 全部使用 invokedynamic
    tree.defs = tree.defs.appendList(List.of(
        generateRecordMethod(tree, names.toString, vars, getterMethHandles),
        generateRecordMethod(tree, names.hashCode, vars, getterMethHandles),
        generateRecordMethod(tree, names.equals,   vars, getterMethHandles)
    ));
}
```

访问器方法体生成（`Lower.java:2271`）极其简单——直接 `return this.field`:

```java
List<JCTree> generateMandatedAccessors(JCClassDecl tree) {
    return tree.sym.getRecordComponents().stream()
        .filter(rc -> (rc.accessor.flags() & GENERATED_MEMBER) != 0)
        .map(rc -> make.MethodDef(rc.accessor,
            make.Block(0, List.of(make.Return(make.Ident(field))))))
        .collect(List.collector());
}
```

---

## 5. 规范构造器与访问器生成

### RecordConstructorHelper — `TypeEnter.java:1468-1528`

```java
class RecordConstructorHelper extends BasicConstructorHelper {
    @Override
    public MethodSymbol constructorSymbol() {
        MethodSymbol csym = super.constructorSymbol();
        csym.flags_field |= GENERATEDCONSTR;
        for (JCVariableDecl field : recordFieldDecls) {
            params.add(new VarSymbol(
                GENERATED_MEMBER | PARAMETER | RECORD, field.name, field.sym.type, csym));
        }
        csym.flags_field |= RECORD;
        return csym;
    }
}
```

### 字段赋值注入 — `Lower.java:2748-2768`

编译器在 compact constructor 或生成的规范构造器**末尾**自动插入 final 字段赋值：

```java
if (tree.name == names.init && (
    (tree.sym.flags_field & COMPACT_RECORD_CONSTRUCTOR) != 0 ||
    (tree.sym.flags_field & (GENERATEDCONSTR | RECORD)) == (GENERATEDCONSTR | RECORD))) {

    for (VarSymbol field : fields) {
        if ((field.flags_field & UNINITIALIZED_FIELD) != 0) {
            VarSymbol param = tree.params.stream()
                .filter(p -> p.name == field.name).findFirst().get().sym;
            // 插入: this.field = param;
            tree.body.stats = tree.body.stats.append(
                make.Exec(make.Assign(
                    make.Select(make.This(field.owner.erasure(types)), field),
                    make.Ident(param))));
            field.flags_field &= ~UNINITIALIZED_FIELD;
        }
    }
}
```

这意味着紧凑构造器中用户代码（验证逻辑）在前，编译器赋值在后：

```java
record Range(int lo, int hi) {
    Range {                                          // compact constructor
        if (lo > hi) throw new IllegalArgumentException();
        // 编译器自动插入: this.lo = lo; this.hi = hi;
    }
}
```

---

## 6. ObjectMethods.bootstrap 与 invokedynamic

### 为什么使用 invokedynamic？

| 优势 | 说明 |
|------|------|
| **字节码紧凑** | 每个方法只需一条 `invokedynamic`，而非几十条比较/散列指令 |
| **运行时优化** | bootstrap 在首次调用时链接，JIT 可针对实际类型内联 |
| **实现可演进** | JDK 可升级 ObjectMethods 而无需重新编译 record 类 |
| **多态分析** | 对引用类型字段，生成隐藏类做单态内联 profiling |

### generateRecordMethod() — `Lower.java:2486-2538`

```java
JCTree generateRecordMethod(JCClassDecl tree, Name name, ...) {
    if ((msym.flags() & RECORD) != 0) {  // 仅编译器生成的方法
        // 静态参数: [Record.class, "x;y", MH(x), MH(y)]
        LoadableConstant[] staticArgsValues = new LoadableConstant[2 + getterMethHandles.length];
        staticArgsValues[0] = (ClassType)tree.sym.type;
        staticArgsValues[1] = LoadableConstant.String(
            vars.stream().map(v -> v.name).collect(Collectors.joining(";")));
        // ... 复制 getter MethodHandles

        // 生成 indy: ObjectMethods.bootstrap(lookup, name, type, Point.class, "x;y", MH...)
        JCFieldAccess qualifier = makeIndyQualifier(
            syms.objectMethodsType, tree, msym, ..., bootstrapName, name, false);

        // 方法体: return indy_call(this) 或 return indy_call(this, o)
        return make.MethodDef(msym, make.Block(0, List.of(make.Return(proxyCall))));
    }
}
```

### ObjectMethods.bootstrap() — `ObjectMethods.java:510`

```java
public static Object bootstrap(MethodHandles.Lookup lookup, String methodName,
        TypeDescriptor type, Class<?> recordClass, String names,
        MethodHandle... getters) throws Throwable {
    MethodHandle handle = switch (methodName) {
        case "equals"   -> makeEquals(lookup, recordClass, getterList);
        case "hashCode" -> makeHashCode(lookup, recordClass, getterList);
        case "toString" -> makeToString(lookup, recordClass, getters, nameList);
    };
    return methodType != null ? new ConstantCallSite(handle) : handle;
}
```

### equals 实现 — makeEquals()

使用 MethodHandle 组合器构建等价性检查链：

- **原始类型**：`eq(int, int)` 等静态方法直接 `==` 比较
- **float/double**：`Float.compare`/`Double.compare`（处理 NaN 和 -0.0）
- **引用类型**：调用 `Object.equals()`，但为支持多态内联，
  **动态生成隐藏类 (hidden class)**，每个字段的 `equals` 有独立的 JIT profile

```java
// ObjectMethods.java — 多态优化
if (hasPolymorphism) {
    var bytes = classFileContext.build(
        ClassDesc.of(specializerClassName(lookup.lookupClass(), "Equalator")), clb -> {
            // 为每个非单态字段生成 static boolean equalatorN(T, T) 方法
        });
    var specializerLookup = lookup.defineHiddenClass(bytes, true, ...);
}
```

### hashCode 实现 — `result * 31 + fieldHash`

```java
private static int hashCombiner(int x, int y) { return x * 31 + y; }
```

同样为引用类型字段生成隐藏类做多态优化。

### toString 实现

使用 `StringConcatFactory::makeConcatWithConstants` 拼接，格式 `Point[x=1, y=2]`。
超过 `MAX_STRING_CONCAT_SLOTS = 20` 个 slot 时分片处理。

---

## 7. 字节码分析

对 `record Point(int x, int y) {}` 编译后的 `javap -c -v` 关键输出：

```
public final class Point extends java.lang.Record
  flags: (0x0031) ACC_PUBLIC, ACC_FINAL, ACC_SUPER
```

#### 规范构造器

```
public Point(int, int);
  Code:  aload_0 → invokespecial Record."<init>" → aload_0 → iload_1 →
         putfield x → aload_0 → iload_2 → putfield y → return
```

#### 访问器

```
public int x();
  Code:  aload_0 → getfield x → ireturn
```

#### equals — invokedynamic

```
public final boolean equals(java.lang.Object);
  Code:  aload_0 → aload_1 →
         invokedynamic #0:equals:(LPoint;Ljava/lang/Object;)Z → ireturn
```

#### BootstrapMethods 属性

```
BootstrapMethods:
  0: REF_invokeStatic ObjectMethods.bootstrap:(...)Ljava/lang/Object;
    Method arguments:
      Point                    // recordClass
      x;y                     // component names
      REF_getField Point.x:I  // getter MH
      REF_getField Point.y:I  // getter MH
```

#### Record 属性 — `ClassWriter.java:863`

```java
int writeRecordAttribute(ClassSymbol csym) {
    databuf.appendChar(csym.getRecordComponents().size());
    for (VarSymbol v : csym.getRecordComponents()) {
        databuf.appendChar(poolWriter.putName(v.name));       // 组件名
        databuf.appendChar(poolWriter.putDescriptor(v));      // 类型描述符
        acount += writeMemberAttrs(v, true);                  // 注解等
    }
}
```

Class 文件中的 Record 属性使得 `Class.getRecordComponents()` 能在运行时获取组件信息。

---

## 8. Record 序列化安全

### 传统类 vs Record 的反序列化

| 方面 | 普通类 | Record |
|------|--------|--------|
| 对象创建 | `Unsafe.allocateInstance()` — 绕过构造器 | **始终调用规范构造器** |
| 安全性 | 可能产生非法状态对象 | 构造器验证确保不变量 |
| readObject | 可自定义 | **不允许** — 忽略 readObject/readObjectNoData |

### ObjectStreamClass.RecordSupport — `ObjectStreamClass.java:2212`

```java
static MethodHandle deserializationCtr(ObjectStreamClass desc) {
    RecordComponent[] recordComponents = desc.forClass().getRecordComponents();
    mh = desc.getRecordConstructor();                    // 获取规范构造器 MH
    mh = mh.asType(mh.type().changeReturnType(Object.class));
    mh = MethodHandles.dropArguments(mh, ..., byte[].class, Object[].class);
    for (int i = recordComponents.length - 1; i >= 0; i--) {
        MethodHandle combiner = streamFieldExtractor(name, type, desc);
        mh = MethodHandles.foldArguments(mh, i, combiner);  // 从流数据提取组件值
    }
    // 最终: (byte[], Object[]) -> Object — 始终经过规范构造器
}
```

反序列化时构造器中的验证逻辑照常执行，防止序列化攻击：

```java
record Range(int lo, int hi) {
    Range { if (lo > hi) throw new IllegalArgumentException(); }
}
// 反序列化时 lo > hi 的恶意数据会被拒绝
```

---

## 9. 与 Sealed Classes 配合

Record + sealed interface 实现代数数据类型 (Algebraic Data Types / ADT)：

```java
public sealed interface Shape permits Circle, Rectangle {}
public record Circle(double radius) implements Shape {}
public record Rectangle(double w, double h) implements Shape {}

// 穷举模式匹配 — 编译器验证所有子类型已覆盖，不需要 default
double area = switch (shape) {
    case Circle(var r)        -> Math.PI * r * r;
    case Rectangle(var w, var h) -> w * h;
};
```

编译器对此模式的支持：
- **穷举性检查**：sealed 提供完整子类型列表，switch 不需要 default
- **Record Pattern 解构**：编译器调用访问器方法 (`radius()`, `w()`) 提取组件值
- **嵌套模式**：record 中的 record 可递归解构

```java
sealed interface Expr permits Lit, Add {}
record Lit(int v) implements Expr {}
record Add(Expr l, Expr r) implements Expr {}

int eval(Expr e) {
    return switch (e) {
        case Lit(var v)       -> v;
        case Add(var l, var r) -> eval(l) + eval(r);
    };
}
```

---

## 10. 编译器限制与检查

### Flags 定义 — `Flags.java`

```java
public static final long RECORD = 1L<<61;                    // record 类/字段/构造器/方法
public static final long COMPACT_RECORD_CONSTRUCTOR = 1L<<51; // 紧凑构造器
```

### 编译器强制的限制

| 限制 | 检查位置 | 实现方式 |
|------|----------|----------|
| **隐式 final** | `Check.java:1195` | `implicit \|= FINAL` |
| **不能 abstract** | `Check.java:1194` | `mask &= ~ABSTRACT` |
| **隐式继承 Record** | `TypeEnter.java:621` | `recordBase()` 返回 `java.lang.Record` |
| **不能显式 extends** | `JavacParser.java:4396` | Parser 不解析 extends 子句 |
| **不能有额外实例字段** | `JavacParser.java:4754` | 非 static 字段被拒绝 |
| **字段隐式 private final** | 编译器自动添加 | 头部组件自动 `private final` |
| **内部 record 隐式 static** | `Check.java:1180` | `implicit = STATIC` |

### 注解传播规则 (Annotation Propagation)

Record 组件上的注解按 `@Target` 传播到多个目标（`Check.java:3068-3172`）：

```
@Target(FIELD)             → 字段 (Field)
@Target(METHOD)            → 访问器 (Accessor)
@Target(PARAMETER)         → 构造器参数 (Constructor Parameter)
@Target(RECORD_COMPONENT)  → RecordComponent
@Target(TYPE_USE)          → 所有适用位置
```

---

## 11. 设计决策总结

### 关键架构决策

| 决策 | 理由 |
|------|------|
| **invokedynamic 而非直接字节码** | 实现可演进，字节码紧凑，运行时优化空间大 |
| **ConstantCallSite** | equals/hashCode/toString 行为不变，只需链接一次 |
| **隐藏类 (Hidden Class) 优化** | 为引用类型字段的 equals/hashCode 提供单态内联 profile |
| **组件访问器而非 getter** | `x()` 而非 `getX()`，函数式风格 |
| **规范构造器反序列化** | 确保不变量，消除序列化攻击面 |
| **RECORD 标志复用** | 1L<<61 用于类、字段、构造器、方法，区分用户定义 vs 编译器生成 |

### 编译阶段职责分离

```
JavacParser   ── 语法识别，Flags.RECORD，解析头部组件
TypeEnter     ── 创建 RecordComponent，注入隐式成员符号（仅声明，无方法体）
Check         ── 验证限制（不能 abstract，不能有实例字段等）
Lower         ── 生成方法体（访问器 return field，三方法 invokedynamic，构造器赋值注入）
ClassWriter   ── 写入 Record 属性到 class 文件
ObjectMethods ── 运行时 bootstrap，MethodHandle 链实现 equals/hashCode/toString
```

### 源码文件索引

| 文件 | 关键内容 |
|------|----------|
| `javac/parser/JavacParser.java` | `recordDeclaration()` |
| `javac/comp/TypeEnter.java` | `RecordPhase`, `MembersPhase`, `RecordConstructorHelper`, `addAccessor()` |
| `javac/comp/Lower.java` | `visitRecordDef()`, `generateRecordMethod()`, `generateMandatedAccessors()` |
| `javac/comp/Check.java` | 修饰符检查，注解传播 |
| `javac/code/Flags.java` | `RECORD` (1L<<61), `COMPACT_RECORD_CONSTRUCTOR` (1L<<51) |
| `javac/code/Symbol.java` | `RecordComponent` 内部类 |
| `javac/jvm/ClassWriter.java` | `writeRecordAttribute()` |
| `java/lang/runtime/ObjectMethods.java` | `bootstrap()`, `makeEquals()`, `makeHashCode()`, `makeToString()` |
| `java/io/ObjectStreamClass.java` | `RecordSupport.deserializationCtr()` |
