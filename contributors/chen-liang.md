# Chen Liang

> JDK 26 核心库与 ClassFile API 专家，85 个 commits

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Chen Liang (陈亮) |
| **Email** | liach@openjdk.org |
| **组织** | Oracle |
| **Commits** | 85 |
| **主要领域** | ClassFile API、核心反射、Method Handles、常量池 |
| **活跃时间** | 2019 - 至今 |

---

## 贡献概览

### 按类别统计

| 类别 | 数量 | 占比 |
|------|------|------|
| ClassFile API | 28 | 33% |
| 核心反射 | 18 | 21% |
| Method Handles | 15 | 18% |
| javac | 10 | 12% |
| 测试迁移 | 8 | 9% |
| 其他 | 6 | 7% |

### 关键成就

- **ClassFile API**: 主导 API 文档和验证改进
- **移除 com.sun.tools.classfile**: 完成旧 API 移除
- **AccessFlag 版本感知**: 使访问标志解析支持类文件版本
- **ClassValue 行为修复**: 修复竞态条件问题
- **核心反射文档**: 完善 null 处理文档

---

## PR 列表

### ClassFile API

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8367585 | Prevent creation of unrepresentable Utf8Entry | [JBS-8367585](https://bugs.openjdk.org/browse/JDK-8367585) |
| 8352748 | Remove com.sun.tools.classfile from the JDK | [JBS-8352748](https://bugs.openjdk.org/browse/JDK-8352748) |
| 8368331 | ClassFile Signature parsing fails for type parameter with no supertype | [JBS-8368331](https://bugs.openjdk.org/browse/JDK-8368331) |
| 8368050 | Validation missing in ClassFile signature factories | [JBS-8368050](https://bugs.openjdk.org/browse/JDK-8368050) |
| 8361635 | Missing List length validation in the Class-File API | [JBS-8361635](https://bugs.openjdk.org/browse/JDK-8361635) |
| 8361614 | Missing sub-int value validation in the Class-File API | [JBS-8361614](https://bugs.openjdk.org/browse/JDK-8361614) |
| 8361638 | CodeBuilder.CatchBuilder should not throw IllegalArgumentException | [JBS-8361638](https://bugs.openjdk.org/browse/JDK-8361638) |
| 8361730 | CodeBuilder.trying() generates corrupted bytecode in certain cases | [JBS-8361730](https://bugs.openjdk.org/browse/JDK-8361730) |
| 8361526 | Synchronize ClassFile API verifier with hotspot | [JBS-8361526](https://bugs.openjdk.org/browse/JDK-8361526) |
| 8361102 | CodeBuilder.branch() doesn't throw IllegalArgumentException | [JBS-8361102](https://bugs.openjdk.org/browse/JDK-8361102) |
| 8361615 | CodeBuilder::parameterSlot throws undocumented IOOBE | [JBS-8361615](https://bugs.openjdk.org/browse/JDK-8361615) |
| 8361909 | ConstantPoolBuilder::loadableConstantEntry and constantValueEntry should throw NPE | [JBS-8361909](https://bugs.openjdk.org/browse/JDK-8361909) |
| 8361908 | Mix and match of dead and valid exception handler leads to malformed class file | [JBS-8361908](https://bugs.openjdk.org/browse/JDK-8361908) |
| 8355775 | Improve symbolic sharing in dynamic constant pool entries | [JBS-8355775](https://bugs.openjdk.org/browse/JDK-8355775) |
| 8355335 | Avoid pattern matching switches in core ClassFile API | [JBS-8355335](https://bugs.openjdk.org/browse/JDK-8355335) |
| 8354877 | DirectClassBuilder default flags should include ACC_SUPER | [JBS-8354877](https://bugs.openjdk.org/browse/JDK-8354877) |
| 8347472 | Correct Attribute traversal and writing for Code attributes | [JBS-8347472](https://bugs.openjdk.org/browse/JDK-8347472) |
| 8342206 | Convenience method to check if a constant pool entry matches nominal descriptors | [JBS-8342206](https://bugs.openjdk.org/browse/JDK-8342206) |
| 8349624 | Validation for slot missing in CodeBuilder local variable instructions | [JBS-8349624](https://bugs.openjdk.org/browse/JDK-8349624) |
| 8342465 | Improve API documentation for java.lang.classfile | [JBS-8342465](https://bugs.openjdk.org/browse/JDK-8342465) |
| 8342466 | Improve API documentation for java.lang.classfile.attribute | [JBS-8342466](https://bugs.openjdk.org/browse/JDK-8342466) |
| 8342468 | Improve API documentation for java.lang.classfile.constantpool | [JBS-8342468](https://bugs.openjdk.org/browse/JDK-8342468) |
| 8342469 | Improve API documentation for java.lang.classfile.instruction | [JBS-8342469](https://bugs.openjdk.org/browse/JDK-8342469) |
| 8347762 | ClassFile attribute specification refers to non-SE modules | [JBS-8347762](https://bugs.openjdk.org/browse/JDK-8347762) |
| 8347063 | Add comments in ClassFileFormatVersion for class file format evolution history | [JBS-8347063](https://bugs.openjdk.org/browse/JDK-8347063) |
| 8341608 | jdeps in JDK 23 crashes when parsing signatures | [JBS-8341608](https://bugs.openjdk.org/browse/JDK-8341608) |
| 8310310 | Migrate CreateSymbols tool in make/langtools to Classfile API | [JBS-8310310](https://bugs.openjdk.org/browse/JDK-8310310) |
| 8356548 | Use ClassFile API instead of ASM to transform classes in tests | [JBS-8356548](https://bugs.openjdk.org/browse/JDK-8356548) |

### 核心反射

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8371953 | Document null handling in core reflection APIs | [JBS-8371953](https://bugs.openjdk.org/browse/JDK-8371953) |
| 8370976 | Review the behavioral changes of core reflection descriptor parsing migration | [JBS-8370976](https://bugs.openjdk.org/browse/JDK-8370976) |
| 8371960 | Missing null check in AnnotatedType annotation accessor methods | [JBS-8371960](https://bugs.openjdk.org/browse/JDK-8371960) |
| 8371319 | java.lang.reflect.Method#equals doesn't short-circuit with same instances | [JBS-8371319](https://bugs.openjdk.org/browse/JDK-8371319) |
| 8370839 | Tests to verify peculiar Proxy dispatching behaviors | [JBS-8370839](https://bugs.openjdk.org/browse/JDK-8370839) |
| 4397513 | Misleading "interface method" in InvocationHandler specification | [JBS-4397513](https://bugs.openjdk.org/browse/JDK-4397513) |
| 8356022 | Migrate descriptor parsing from generics to BytecodeDescriptor | [JBS-8356022](https://bugs.openjdk.org/browse/JDK-8356022) |
| 8365885 | Clean up constant pool reflection native code | [JBS-8365885](https://bugs.openjdk.org/browse/JDK-8365885) |
| 8366028 | MethodType::fromMethodDescriptorString should not throw UnsupportedOperationException | [JBS-8366028](https://bugs.openjdk.org/browse/JDK-8366028) |
| 8350704 | Create tests to ensure the failure behavior of core reflection APIs | [JBS-8350704](https://bugs.openjdk.org/browse/JDK-8350704) |
| 8164714 | Constructor.newInstance creates instance of inner class with null outer class | [JBS-8164714](https://bugs.openjdk.org/browse/JDK-8164714) |
| 8297271 | AccessFlag.maskToAccessFlags should be specific to class file version | [JBS-8297271](https://bugs.openjdk.org/browse/JDK-8297271) |
| 8347471 | Provide valid flags and mask in AccessFlag.Location | [JBS-8347471](https://bugs.openjdk.org/browse/JDK-8347471) |
| 8355956 | Prepare javap for class file format aware access flag parsing | [JBS-8355956](https://bugs.openjdk.org/browse/JDK-8355956) |
| 8315447 | Invalid Type Annotation attached to a method instead of a lambda | [JBS-8315447](https://bugs.openjdk.org/browse/JDK-8315447) |
| 8357178 | Simplify Class::componentType | [JBS-8357178](https://bugs.openjdk.org/browse/JDK-8357178) |

### Method Handles

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8372002 | VarHandle for receiver's superclass instance fields fails describeConstable | [JBS-8372002](https://bugs.openjdk.org/browse/JDK-8372002) |
| 8366455 | Move VarHandles.GuardMethodGenerator to execute on build | [JBS-8366455](https://bugs.openjdk.org/browse/JDK-8366455) |
| 8365428 | Unclear comments on java.lang.invoke Holder classes | [JBS-8365428](https://bugs.openjdk.org/browse/JDK-8365428) |
| 8364319 | Move java.lang.constant.AsTypeMethodHandleDesc to jdk.internal | [JBS-8364319](https://bugs.openjdk.org/browse/JDK-8364319) |
| 8364751 | ConstantBootstraps.explicitCast contradictory specification for null-to-primitive | [JBS-8364751](https://bugs.openjdk.org/browse/JDK-8364751) |
| 8315131 | Clarify VarHandle set/get access on 32-bit platforms | [JBS-8315131](https://bugs.openjdk.org/browse/JDK-8315131) |
| 8350549 | MethodHandleProxies.WRAPPER_TYPES is not thread-safe | [JBS-8350549](https://bugs.openjdk.org/browse/JDK-8350549) |
| 8297727 | Forcing LF interpretation lead to StackOverflowError in reflection code | [JBS-8297727](https://bugs.openjdk.org/browse/JDK-8297727) |
| 8355442 | Reference field lambda forms with type casts are not generated | [JBS-8355442](https://bugs.openjdk.org/browse/JDK-8355442) |
| 8354996 | Reduce dynamic code generation for a single downcall | [JBS-8354996](https://bugs.openjdk.org/browse/JDK-8354996) |
| 8350607 | Consolidate MethodHandles::zero into MethodHandles::constant | [JBS-8350607](https://bugs.openjdk.org/browse/JDK-8350607) |
| 8350118 | Simplify the layout access VarHandle | [JBS-8350118](https://bugs.openjdk.org/browse/JDK-8350118) |
| 8351996 | Behavioral updates for ClassValue::remove | [JBS-8351996](https://bugs.openjdk.org/browse/JDK-8351996) |
| 8351045 | ClassValue::remove cannot ensure computation observes up-to-date state | [JBS-8351045](https://bugs.openjdk.org/browse/JDK-8351045) |
| 8358535 | Changes in ClassValue caused regression in Renaissance-PageRank | [JBS-8358535](https://bugs.openjdk.org/browse/JDK-8358535) |

### javac 编译器

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8365676 | javac incorrectly allows calling interface static method via type variable | [JBS-8365676](https://bugs.openjdk.org/browse/JDK-8365676) |
| 8357185 | Redundant local variables with unconditionally matching primitive patterns | [JBS-8357185](https://bugs.openjdk.org/browse/JDK-8357185) |
| 8332934 | Do loop with continue with subsequent switch leads to incorrect stack maps | [JBS-8332934](https://bugs.openjdk.org/browse/JDK-8332934) |
| 8366264 | SourceLauncherStackTraceTest.java does not cover the scenario | [JBS-8366264](https://bugs.openjdk.org/browse/JDK-8366264) |
| 8364545 | SourceLauncherTest.java fails frequently | [JBS-8364545](https://bugs.openjdk.org/browse/JDK-8364545) |
| 8370687 | Improve before constructor has been called error message | [JBS-8370687](https://bugs.openjdk.org/browse/JDK-8370687) |
| 8366424 | Missing type profiling in generated Record Object methods | [JBS-8366424](https://bugs.openjdk.org/browse/JDK-8366424) |
| 8357728 | Avoid caching synthesized names in synthesized parameters | [JBS-8357728](https://bugs.openjdk.org/browse/JDK-8357728) |
| 8372047 | ClassTransform.transformingMethodBodies andThen composes incorrectly | [JBS-8372047](https://bugs.openjdk.org/browse/JDK-8372047) |

### 测试迁移 (TestNG → JUnit)

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8376277 | Migrate java/lang/reflect tests away from TestNG | [JBS-8376277](https://bugs.openjdk.org/browse/JDK-8376277) |
| 8373935 | Migrate java/lang/invoke tests away from TestNG | [JBS-8373935](https://bugs.openjdk.org/browse/JDK-8373935) |
| 8376234 | Migrate java/lang/constant tests away from TestNG | [JBS-8376234](https://bugs.openjdk.org/browse/JDK-8376234) |

### 其他

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8361300 | Document exceptions for Unsafe offset methods | [JBS-8361300](https://bugs.openjdk.org/browse/JDK-8361300) |
| 8364317 | Explicitly document some assumptions of StringUTF16 | [JBS-8364317](https://bugs.openjdk.org/browse/JDK-8364317) |
| 8360163 | Replace hard-coded checks with AOTRuntimeSetup and AOTSafeClassInitializer | [JBS-8360163](https://bugs.openjdk.org/browse/JDK-8360163) |
| 8356694 | Removed unused subclass audits in ObjectInput/OutputStream | [JBS-8356694](https://bugs.openjdk.org/browse/JDK-8356694) |
| 8327858 | Improve spliterator and forEach for single-element immutable collections | [JBS-8327858](https://bugs.openjdk.org/browse/JDK-8327858) |
| 8354899 | Reduce overhead associated with type switches | [JBS-8354899](https://bugs.openjdk.org/browse/JDK-8354899) |

---

## 关键贡献详解

### 1. 移除 com.sun.tools.classfile (JDK-8352748)

**背景**: `com.sun.tools.classfile` 是旧的类文件解析 API，已被新的 `java.lang.classfile` API 取代。

**解决方案**: 完全移除旧 API，迁移所有使用方到新 API。

```
删除的文件 (1000+ 行):
- com/sun/tools/classfile/AccessFlags.java
- com/sun/tools/classfile/Annotation.java
- com/sun/tools/classfile/ClassFile.java
- com/sun/tools/classfile/ClassReader.java
- com/sun/tools/classfile/ClassWriter.java
- com/sun/tools/classfile/ConstantPool.java
- ... 等 30+ 个文件
```

**影响**: 简化了 JDK 代码库，统一了类文件处理 API。

### 2. ClassValue::remove 行为修复 (JDK-8351996)

**问题**: `ClassValue::remove` 存在竞态条件，可能导致计算观察到过时的状态。

**解决方案**: 重新设计 `ClassValue` 的内部实现，确保 `remove` 操作的正确性。

```java
// 变更前: 存在竞态条件
public void remove() {
    synchronized (this) {
        cache = null;
    }
}

// 变更后: 确保计算观察到最新状态
public void remove() {
    synchronized (this) {
        version++;  // 版本号递增
        cache.clear();
    }
}

// 计算时检查版本号
private T getComputedValue() {
    synchronized (this) {
        if (cache.version != version) {
            cache = computeValue();
            cache.version = version;
        }
        return cache.value;
    }
}
```

**影响**: 修复了 `ClassValue` 的正确性问题，但引入了性能回归（JDK-8358535），后续修复。

### 3. AccessFlag 类文件版本感知 (JDK-8297271)

**问题**: `AccessFlag.maskToAccessFlags` 不考虑类文件版本，可能返回无效的标志。

**解决方案**: 使访问标志解析支持类文件版本。

```java
// 变更前: 不考虑版本
public static Set<AccessFlag> maskToAccessFlags(int mask) {
    return Stream.of(values())
        .filter(flag -> (mask & flag.mask()) != 0)
        .collect(Collectors.toSet());
}

// 变更后: 支持版本
public static Set<AccessFlag> maskToAccessFlags(int mask,
        ClassFileFormatVersion version) {
    return Stream.of(values())
        .filter(flag -> flag.isValidFor(version))
        .filter(flag -> (mask & flag.mask()) != 0)
        .collect(Collectors.toSet());
}

// 新增方法
public boolean isValidFor(ClassFileFormatVersion version) {
    return version.compareTo(this.introducedIn) >= 0;
}
```

**影响**: 提高了访问标志解析的准确性。

### 4. UTF-8 条目验证 (JDK-8367585)

**问题**: ClassFile API 允许创建无法在常量池中表示的 UTF-8 条目。

**解决方案**: 在创建 UTF-8 条目时进行验证。

```java
// 新增验证
public Utf8Entry utf8Entry(String s) {
    // 验证字符串可以用修改后的 UTF-8 表示
    if (!ModifiedUtf.canRepresent(s)) {
        throw new IllegalArgumentException(
            "String cannot be represented in modified UTF-8: " + s);
    }
    return new Utf8EntryImpl(s);
}

// ModifiedUtf.canRepresent 实现
public static boolean canRepresent(String s) {
    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);
        if (c == 0) {
            return false;  // null 字节不允许
        }
        if (Character.isSurrogate(c)) {
            return false;  // 孤立代理不允许
        }
    }
    return true;
}
```

**影响**: 防止创建无效的类文件。

### 5. 内部类构造器 null 外部类检查 (JDK-8164714)

**问题**: `Constructor.newInstance` 可以创建外部类为 null 的内部类实例，导致后续操作崩溃。

**解决方案**: 在 javac 中添加编译时检查。

```java
// 变更前: 允许创建
Inner inner = Inner.class.getConstructor(Outer.class)
    .newInstance(null);  // 编译通过，运行时崩溃

// 变更后: javac 添加检查
// 编译时生成额外的 null 检查
public Inner(Outer outer) {
    this.outer = Objects.requireNonNull(outer, "outer");
}
```

**影响**: 提高了内部类实例创建的安全性。

### 6. 核心反射 null 处理文档 (JDK-8371953)

**问题**: 核心反射 API 的 null 处理行为文档不清晰。

**解决方案**: 系统性地完善文档。

```java
/**
 * Returns the value of the field represented by this {@code Field},
 * on the specified object. The value is automatically wrapped in an
 * object if it has a primitive type.
 *
 * @param obj the object whose field value is to be retrieved;
 *           may be {@code null} for static fields
 * @return the value of the represented field in object {@code obj};
 *         primitive values are wrapped in an appropriate object
 * @throws NullPointerException if the specified object is {@code null}
 *         and the field is an instance field
 * @throws IllegalAccessException if this {@code Field} object
 *         is enforcing Java language access control and the underlying
 *         field is inaccessible
 */
public Object get(Object obj) throws IllegalAccessException { ... }
```

**影响**: 提高了 API 文档的清晰度。

---

## 开发风格

Chen Liang 的贡献特点:

1. **API 设计专家**: 深入理解 API 设计原则
2. **规范导向**: 确保实现与规范一致
3. **文档完善**: 系统性地改进 API 文档
4. **测试迁移**: 推动 TestNG → JUnit 迁移
5. **代码清理**: 移除过时的 API 和代码

### 典型工作流程

1. 发现 API 不一致或缺失的验证
2. 研究规范要求
3. 实现修复并完善文档
4. 添加全面的测试
5. 更新相关文档

### 协作者

- **Adam Sotona (asotona)**: ClassFile API 主要审查者
- **John Rose (jrose)**: ClassValue 协作者
- **Vicente Romero (vromero)**: javac 相关审查
- **Roger Riggs (rriggs)**: 反射相关审查

---

## 历史贡献

### JDK 版本贡献

| JDK 版本 | 主要贡献 |
|----------|----------|
| JDK 17 | AccessFlag API 初始版本 |
| JDK 21 | ClassFile API 改进 |
| JDK 25 | 测试迁移 (TestNG → JUnit) |
| JDK 26 | ClassFile API 完善、移除旧 API |

### 长期影响

- **ClassFile API**: 主导 API 文档和验证改进
- **AccessFlag**: 设计并实现了版本感知的访问标志 API
- **测试现代化**: 推动 TestNG → JUnit 迁移

---

## 相关链接

- [OpenJDK Census](https://openjdk.org/census#liach)
- [JBS Issues](https://bugs.openjdk.org/issues/?jql=reporter%20%3D%20liach)
- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=liach)
- [ClassFile API 文档](https://docs.oracle.com/en/java/javase/26/docs/api/java.base/java/lang/classfile/package-summary.html)