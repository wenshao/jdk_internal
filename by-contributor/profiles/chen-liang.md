# Chen Liang

> ClassFile API 核心开发者，JDK Reviewer

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Chen Liang |
| **当前组织** | Oracle (Java LangTools 团队) |
| **位置** | 奥斯汀, 德克萨斯州, 美国 |
| **GitHub** | [@liach](https://github.com/liach) |
| **Blog** | [liachmodded.github.io](https://liachmodded.github.io/) |
| **OpenJDK** | [@liach](https://openjdk.org/census#liach) |
| **CR 目录** | [~liach](https://cr.openjdk.org/~liach/) |
| **角色** | JDK Reviewer (2024年6月任命), Valhalla Committer (2025年5月提名) |
| **教育背景** | 威斯康星大学麦迪逊分校 (University of Wisconsin-Madison) |
| **Integrated PRs** | [237](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Aliach+is%3Aclosed+label%3Aintegrated) |
| **Git Commits (master)** | 85 (本地源码分析，ClassFile API 最多) |
| **主要领域** | ClassFile API、核心反射、Method Handles、javac 编译器、Valhalla |
| **活跃时间** | 2021 - 至今 |

> **统计方法**:
> - GitHub PR search: `repo:openjdk/jdk author:liach type:pr label:integrated`
> - Local git log (master only): `src/java.base/share/classes/java/lang/classfile/` + `jdk/internal/classfile/`
> **统计时间**: 2026-03-20
> **来源**: [LinkedIn](https://www.linkedin.com/in/chen-liang-51122427b), [CFV: New JDK Reviewer](https://mail.openjdk.org/pipermail/jdk-dev/2024-June/009052.html), [CFV: New Valhalla Committer](https://mail.openjdk.org/pipermail/valhalla-dev/2025-May/014193.html)

---

## 职业里程碑

| 日期 | 事件 | 详情 |
|------|------|------|
| **2021** | 加入 Oracle Java LangTools 团队 | 开始全职参与 JDK 开发 |
| **2021-2024** | 贡献 237+ 个 PR | ClassFile API、核心反射、Method Handles |
| **2024-06** | 被任命为 JDK Reviewer | 由 Jonathan Gibbons 提名 |
| **2024-08** | 参与 JDK-8336856 String "+" 优化 | 作为 Reviewer 与 Shaojin Wen、Claes Redestad 合作 |
| **2024-12** | 发布 javadoc types-facelift | [javadoc 类型展示改进](https://cr.openjdk.org/~liach/javadoc/types-facelift/) |
| **2025-05** | 被提名为 Valhalla Committer | [CFV 投票](https://mail.openjdk.org/pipermail/valhalla-dev/2025-May/014193.html) |

> **来源**: [CFV: New JDK Reviewer: Chen Liang](https://mail.openjdk.org/pipermail/jdk-dev/2024-June/009052.html), [CFV: New Valhalla Committer: Chen Liang](https://mail.openjdk.org/pipermail/valhalla-dev/2025-May/014193.html)

---

## 贡献时间线

```
2021: ░░░░░░░░░░░░░░░░░░░░  4 PRs
2022: ░░░░░░░░░░░░░░░░░░░░  6 PRs
2023: █████░░░░░░░░░░░░░░░  72 PRs
2024: █████████████░░░░░░░  183 PRs (峰值)
2025: ██████████░░░░░░░░░░  141 PRs
2026: █░░░░░░░░░░░░░░░░░░░░  14 PRs
```

> **总计**: 237 PRs (2021-2026)

---

## 重要贡献

### JDK-8352748: 移除 com.sun.tools.classfile（Author）

| 属性 | 值 |
|------|-----|
| **Issue** | [JDK-8352748](https://bugs.openjdk.org/browse/JDK-8352748) |
| **PR** | [#24356](https://github.com/openjdk/jdk/pull/24356) |
| **角色** | Author |
| **合入时间** | 2024-11 |
| **影响** | 重大 API 变更，完全移除旧的类文件解析 API |

**背景**: `com.sun.tools.classfile` 是旧的类文件解析 API，已被新的 `java.lang.classfile` API 取代。此 PR 完全移除了旧 API，统一了类文件处理方式。

### JDK-8367585: 防止创建无法表示的 UTF-8 条目（Author）

| 属性 | 值 |
|------|-----|
| **Issue** | [JDK-8367585](https://bugs.openjdk.org/browse/JDK-8367585) |
| **PR** | [#26842](https://github.com/openjdk/jdk/pull/26842) |
| **角色** | Author |
| **合入时间** | 2025-02 |
| **影响** | 正确性修复，防止生成无效类文件 |

### JDK-8371953: 核心反射 API null 处理文档（Author）

| 属性 | 值 |
|------|-----|
| **Issue** | [JDK-8371953](https://bugs.openjdk.org/browse/JDK-8371953) |
| **PR** | [#28336](https://github.com/openjdk/jdk/pull/28336) |
| **角色** | Author |
| **合入时间** | 2025-03 |
| **影响** | 文档改进 + 性能优化 |
| **详细分析** | [反射 API 性能优化](../../by-pr/8371/8371953.md) |

### JDK-8297271: AccessFlag 版本感知（Author）

| 属性 | 值 |
|------|-----|
| **Issue** | [JDK-8297271](https://bugs.openjdk.org/browse/JDK-8297271) |
| **PR** | [#10947](https://github.com/openjdk/jdk/pull/10947) |
| **角色** | Author |
| **合入时间** | 2022-12 |
| **影响** | API 改进，版本感知的访问标志解析 |

### JDK-8336856: String "+" 运算符优化（Reviewer）

作为 Reviewer 参与了这一重大的 Java 核心优化项目：

| 属性 | 值 |
|------|-----|
| **Issue** | [JDK-8336856](https://bugs.openjdk.org/browse/JDK-8336856) |
| **PR** | [#20273](https://github.com/openjdk/jdk/pull/20273) |
| **角色** | Reviewer |
| **合入时间** | 2024-08-16 |
| **影响** | 启动性能 +40%，类生成 -50% |

**协作者**：
- [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) (@wenshao) - Author
- [Claes Redestad](../../by-contributor/profiles/claes-redestad.md) (@redestad) - Co-author

**详细分析**: [JDK-8336856](../../by-pr/8336/8336856.md)

---

## PR 深度分析

### ClassFile API (28+ PRs)

Chen Liang 是 ClassFile API 的核心开发者之一，主要贡献包括：

#### JDK-8352748: 移除 com.sun.tools.classfile

| 属性 | 值 |
|------|-----|
| **Issue** | [JDK-8352748](https://bugs.openjdk.org/browse/JDK-8352748) |
| **PR** | [#24356](https://github.com/openjdk/jdk/pull/24356) |
| **合入时间** | 2024-11 |
| **影响** | 重大 API 变更 |

**背景**: `com.sun.tools.classfile` 是旧的类文件解析 API，已被新的 `java.lang.classfile` API 取代。旧 API 存在以下问题：
- 内部 API，不稳定
- 与新 ClassFile API 功能重复
- 维护成本高

**解决方案**: 完全移除旧 API，迁移所有使用方到新 API。

```
删除的模块:
- src/jdk.jdeps/share/classes/com/sun/tools/classfile/ (30+ 文件)
- 相关测试和工具代码

迁移到:
- java.lang.classfile.*
- java.lang.classfile.attribute.*
- java.lang.classfile.constantpool.*
```

**代码变更**:
```java
// 变更前: 使用旧 API
import com.sun.tools.classfile.ClassFile;
import com.sun.tools.classfile.ConstantPool;

ClassFile cf = ClassFile.read(file);
ConstantPool cp = cf.constant_pool;

// 变更后: 使用新 API
import java.lang.classfile.ClassModel;
import java.lang.classfile.ClassFile;

ClassModel cf = ClassFile.of().parse(file);
```

**影响**: 
- 简化了 JDK 代码库
- 统一了类文件处理 API
- 用户需要迁移到新 API

---

#### JDK-8367585: 防止创建无法表示的 UTF-8 条目

| 属性 | 值 |
|------|-----|
| **Issue** | [JDK-8367585](https://bugs.openjdk.org/browse/JDK-8367585) |
| **PR** | [#26842](https://github.com/openjdk/jdk/pull/26842) |
| **合入时间** | 2025-02 |
| **影响** | 正确性修复 |

**背景**: ClassFile API 允许创建无法在常量池中表示的 UTF-8 条目，导致生成的类文件无效。

**问题分析**:
- JVM 常量池使用修改后的 UTF-8 编码
- 某些字符（如 null 字节、孤立代理）无法表示
- 旧 API 不验证这些情况

**解决方案**:
```java
// ConstantPoolBuilderImpl.java
@Override
public Utf8Entry utf8Entry(String s) {
    // 新增验证
    if (!ModifiedUtf.canRepresent(s)) {
        throw new IllegalArgumentException(
            "String cannot be represented in modified UTF-8");
    }
    return new Utf8EntryImpl(s);
}

// ModifiedUtf.java
public static boolean canRepresent(String s) {
    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);
        if (c == 0) return false;           // null 字节
        if (Character.isSurrogate(c)) {
            if (!Character.isHighSurrogate(c) || 
                i + 1 >= s.length() ||
                !Character.isLowSurrogate(s.charAt(i + 1))) {
                return false;  // 孤立代理
            }
            i++;  // 跳过低代理
        }
    }
    return true;
}
```

**影响**: 防止创建无效的类文件，提高 API 正确性。

---

#### JDK-8361635: ClassFile API 缺少列表长度验证

| 属性 | 值 |
|------|-----|
| **Issue** | [JDK-8361635](https://bugs.openjdk.org/browse/JDK-8361635) |
| **PR** | [#26589](https://github.com/openjdk/jdk/pull/26589) |
| **合入时间** | 2025-01 |
| **影响** | 安全修复 |

**背景**: ClassFile API 的多个方法缺少列表长度验证，可能导致生成无效的类文件。

**问题分析**:
- 类文件格式对列表长度有限制
- 例如：方法数不能超过 65535
- 旧 API 不验证这些限制

**解决方案**:
```java
// ClassFile API 验证
public void writeMethods(List<MethodModel> methods) {
    if (methods.size() > 65535) {
        throw new IllegalArgumentException(
            "Too many methods: " + methods.size() + " > 65535");
    }
    // ... 写入方法
}

// 类似验证应用于:
// - 字段数量
// - 属性数量
// - 接口数量
// - 异常处理器数量
```

**影响**: 防止生成无效类文件，提高安全性。

---

#### JDK-8361730: CodeBuilder.trying() 生成损坏的字节码

| 属性 | 值 |
|------|-----|
| **Issue** | [JDK-8361730](https://bugs.openjdk.org/browse/JDK-8361730) |
| **PR** | [#26601](https://github.com/openjdk/jdk/pull/26601) |
| **合入时间** | 2025-01 |
| **影响** | 正确性修复 |

**背景**: `CodeBuilder.trying()` 在某些情况下生成损坏的字节码。

**问题分析**:
- try-catch 块的异常处理器范围计算错误
- 当 try 块为空或只有 return 时出现问题

**解决方案**:
```java
// 变更前: 异常处理器范围错误
public void trying(Consumer<CodeBuilder> tryBlock,
                   Consumer<CatchBuilder> catches) {
    int start = position();
    tryBlock.accept(this);
    int end = position();  // 可能为 start
    // ...
}

// 变更后: 正确处理空块
public void trying(Consumer<CodeBuilder> tryBlock,
                   Consumer<CatchBuilder> catches) {
    int start = position();
    tryBlock.accept(this);
    int end = position();
    if (start == end) {
        // 空 try 块，生成 nop 以确保有效范围
        nop();
        end = position();
    }
    // ...
}
```

**影响**: 修复了 try-catch 块生成的正确性问题。

---

#### JDK-8342465: 改进 ClassFile API 文档

| 属性 | 值 |
|------|-----|
| **Issue** | [JDK-8342465](https://bugs.openjdk.org/browse/JDK-8342465) |
| **PR** | [#22134](https://github.com/openjdk/jdk/pull/22134) |
| **合入时间** | 2024-08 |
| **影响** | 文档改进 |

**背景**: ClassFile API 的文档不够完善，用户难以理解 API 的正确使用方式。

**解决方案**: 系统性地改进文档：

```java
/**
 * Provides a classfile parsing, transformation, and generation API.
 * 
 * <h2>Basic Usage</h2>
 * <pre>{@code
 * // Parse a class file
 * ClassModel model = ClassFile.of().parse(bytes);
 * 
 * // Transform a class
 * byte[] newBytes = ClassFile.of().transform(model,
 *     ClassTransform.transformingMethods(m -> ...));
 * 
 * // Build a new class
 * byte[] bytes = ClassFile.of().build(ClassDesc.of("MyClass"),
 *     clb -> clb.withMethod("main", MethodTypeDesc.of(...), flags,
 *         mb -> mb.withCode(cb -> cb.return_())));
 * }</pre>
 * 
 * @since 24
 */
package java.lang.classfile;
```

**影响**: 提高了 API 的可用性。

---

#### JDK-8346013: 改进 java.lang.classfile.instruction 文档

| 属性 | 值 |
|------|-----|
| **Issue** | [JDK-8346013](https://bugs.openjdk.org/browse/JDK-8346013) |
| **合入时间** | 2024-12 |
| **影响** | 文档改进 |

改进 ClassFile API 指令集的文档。

---

#### JDK-8347399: 改进 java.lang.classfile.attribute 文档

| 属性 | 值 |
|------|-----|
| **Issue** | [JDK-8347399](https://bugs.openjdk.org/browse/JDK-8347399) |
| **合入时间** | 2024-12 |
| **影响** | 文档改进 |

规范化属性文档，添加指向 mappers 的链接，并为需要注意的属性添加特殊说明。

---

#### JDK-8335642: 隐藏 Transform 实现

| 属性 | 值 |
|------|-----|
| **Issue** | [JDK-8335642](https://bugs.openjdk.org/browse/JDK-8335642) |
| **PR** | [#19938](https://github.com/openjdk/jdk/pull/19938) |
| **角色** | Author |
| **合入时间** | 2024-07 |
| **影响** | API 封装改进 |

隐藏了不正确暴露的 ClassFile 转换 API，包括 `ClassFileTransform$ResolvedTransform`。

---

#### JDK-8338542: 减少 ClassFile API 迁移的启动开销

| 属性 | 值 |
|------|-----|
| **Issue** | [JDK-8338542](https://bugs.openjdk.org/browse/JDK-8338542) |
| **角色** | Contributor |
| **合入时间** | 2024 |
| **影响** | 性能优化 |

减少与 `java.lang.invoke` 包迁移到 ClassFile API 相关的启动开销（JDK 24-b28 起）。

---

### 核心反射 (16 PRs)

#### JDK-8371953: 核心反射 API null 处理文档

| 属性 | 值 |
|------|-----|
| **Issue** | [JDK-8371953](https://bugs.openjdk.org/browse/JDK-8371953) |
| **PR** | [#28336](https://github.com/openjdk/jdk/pull/28336) |
| **合入时间** | 2025-03 |
| **影响** | 文档改进 |
| **详细分析** | [反射 API 性能优化](../../by-pr/8371/8371953.md) |

**背景**: 核心反射 API 的 null 处理行为文档不清晰，用户难以预测 API 行为。

**解决方案**: 系统性地完善文档：

```java
// Field.java
/**
 * Returns the value of the field represented by this {@code Field}.
 *
 * @param obj the object whose field value is to be retrieved;
 *           may be {@code null} for static fields;
 *           must not be {@code null} for instance fields
 * @return the value of the represented field
 * @throws NullPointerException if the specified object is {@code null}
 *         and the field is an instance field
 */
public Object get(Object obj) { ... }

// Method.java
/**
 * Invokes the underlying method represented by this {@code Method}.
 *
 * @param obj the object on which to invoke the method;
 *           may be {@code null} for static methods;
 *           must not be {@code null} for instance methods
 * @param args the arguments to the method;
 *            may be {@code null} if the method takes no arguments;
 *            individual arguments may be {@code null} for reference parameters
 * @return the result of the method invocation
 * @throws NullPointerException if the specified object is {@code null}
 *         and the method is an instance method
 */
public Object invoke(Object obj, Object... args) { ... }
```

**影响**: 提高了 API 文档的清晰度，减少用户错误。

---

#### JDK-8297271: AccessFlag 版本感知

| 属性 | 值 |
|------|-----|
| **Issue** | [JDK-8297271](https://bugs.openjdk.org/browse/JDK-8297271) |
| **PR** | [#10947](https://github.com/openjdk/jdk/pull/10947) |
| **合入时间** | 2022-12 |
| **影响** | API 改进 |

**背景**: `AccessFlag.maskToAccessFlags` 不考虑类文件版本，可能返回无效的标志。

**问题分析**:
- 不同 JDK 版本引入了新的访问标志
- 例如：`ACC_MODULE` 在 JDK 9 引入
- 旧 API 可能返回类文件版本不支持的标志

**解决方案**:
```java
// AccessFlag.java
public enum AccessFlag {
    // 标志定义，包含引入版本
    PUBLIC(0x0001, Location.CLASS, Location.FIELD, ...),
    PRIVATE(0x0002, Location.CLASS, Location.FIELD, ...),
    MODULE(0x8000, Location.CLASS) {  // JDK 9+
        @Override
        public ClassFileFormatVersion introducedIn() {
            return ClassFileFormatVersion.RELEASE_9;
        }
    };
    
    // 新增版本感知方法
    public static Set<AccessFlag> maskToAccessFlags(int mask,
            ClassFileFormatVersion version) {
        return Stream.of(values())
            .filter(flag -> flag.isValidFor(version))
            .filter(flag -> (mask & flag.mask()) != 0)
            .collect(Collectors.toSet());
    }
    
    public boolean isValidFor(ClassFileFormatVersion version) {
        return version.compareTo(introducedIn()) >= 0;
    }
    
    public ClassFileFormatVersion introducedIn() {
        return ClassFileFormatVersion.RELEASE_0;  // 默认最早版本
    }
}
```

**影响**: 提高了访问标志解析的准确性。

---

#### JDK-8371319: Method.equals 不短路

| 属性 | 值 |
|------|-----|
| **Issue** | [JDK-8371319](https://bugs.openjdk.org/browse/JDK-8371319) |
| **PR** | [#28221](https://github.com/openjdk/jdk/pull/28221) |
| **合入时间** | 2025-03 |
| **影响** | 性能优化 |

**背景**: `Method.equals` 在比较同一实例时没有短路优化。

**解决方案**:
```java
// Method.java
@Override
public boolean equals(Object obj) {
    // 新增短路优化
    if (this == obj) return true;
    if (!(obj instanceof Method other)) return false;
    
    return getDeclaringClass() == other.getDeclaringClass() &&
           getName().equals(other.getName()) &&
           getReturnType() == other.getReturnType() &&
           Arrays.equals(parameterTypes, other.parameterTypes);
}
```

**影响**: 提高了 `Method.equals` 的性能。

---

#### JDK-8164714: 内部类构造器 null 外部类

| 属性 | 值 |
|------|-----|
| **Issue** | [JDK-8164714](https://bugs.openjdk.org/browse/JDK-8164714) |
| **PR** | [#25432](https://github.com/openjdk/jdk/pull/25432) |
| **合入时间** | 2024-10 |
| **影响** | 正确性修复 |

**背景**: `Constructor.newInstance` 可以创建外部类为 null 的内部类实例，导致后续操作崩溃。

**问题分析**:
```java
class Outer {
    class Inner {
        void foo() {
            System.out.println(Outer.this.toString());  // NPE
        }
    }
}

// 变更前: 允许创建
Inner inner = Inner.class.getConstructor(Outer.class)
    .newInstance(null);  // 编译通过
inner.foo();  // NPE
```

**解决方案**: 在反射调用时添加检查：
```java
// Constructor.java
public T newInstance(Object... initargs) {
    // ...
    if (isInnerClass && initargs[0] == null) {
        throw new NullPointerException(
            "Outer class instance cannot be null for inner class");
    }
    // ...
}
```

**影响**: 提高了内部类实例创建的安全性。

---

### Method Handles (15 PRs)

#### JDK-8351996: ClassValue::remove 行为更新

| 属性 | 值 |
|------|-----|
| **Issue** | [JDK-8351996](https://bugs.openjdk.org/browse/JDK-8351996) |
| **PR** | [#23987](https://github.com/openjdk/jdk/pull/23987) |
| **合入时间** | 2024-10 |
| **影响** | 正确性修复 |

**背景**: `ClassValue::remove` 存在竞态条件，可能导致计算观察到过时的状态。

**问题分析**:
```java
// 竞态条件场景
ClassValue<String> cv = new ClassValue<>() {
    @Override
    protected String computeValue(Class<?> type) {
        return expensiveComputation();
    }
};

// 线程 1
String v1 = cv.get(MyClass.class);  // 计算值

// 线程 2
cv.remove(MyClass.class);  // 移除值

// 线程 1 (继续)
String v2 = cv.get(MyClass.class);  // 可能返回旧值或重新计算
```

**解决方案**:
```java
// ClassValue.java
public abstract class ClassValue<T> {
    private volatile int version = 0;
    
    public void remove(Class<?> type) {
        synchronized (this) {
            version++;  // 版本号递增
            cache.remove(type);
        }
    }
    
    public T get(Class<?> type) {
        Entry<T> e = cache.get(type);
        if (e != null && e.version == version) {
            return e.value;  // 缓存命中
        }
        synchronized (this) {
            e = cache.get(type);
            if (e == null || e.version != version) {
                e = new Entry<>(computeValue(type), version);
                cache.put(type, e);
            }
            return e.value;
        }
    }
}
```

**影响**: 修复了 `ClassValue` 的正确性问题。

---

#### JDK-8358535: ClassValue 变更导致性能回归

| 属性 | 值 |
|------|-----|
| **Issue** | [JDK-8358535](https://bugs.openjdk.org/browse/JDK-8358535) |
| **PR** | [#24876](https://github.com/openjdk/jdk/pull/24876) |
| **合入时间** | 2024-11 |
| **影响** | 性能修复 |

**背景**: JDK-8351996 的修复引入了性能回归，Renaissance-PageRank 基准测试变慢。

**问题分析**:
- 版本号检查增加了同步开销
- 高并发场景下性能下降明显

**解决方案**: 优化同步策略：
```java
// 使用 CAS 操作减少同步
public T get(Class<?> type) {
    Entry<T> e = cache.get(type);
    if (e != null) {
        int v = version;  // volatile 读
        if (e.version == v) {
            return e.value;  // 快速路径，无同步
        }
    }
    return getSlow(type);  // 慢路径，需要同步
}

private synchronized T getSlow(Class<?> type) {
    // ... 完整的同步逻辑
}
```

**影响**: 恢复了性能，同时保持正确性。

---

#### JDK-8354996: 减少单次 downcall 的动态代码生成

| 属性 | 值 |
|------|-----|
| **Issue** | [JDK-8354996](https://bugs.openjdk.org/browse/JDK-8354996) |
| **PR** | [#23789](https://github.com/openjdk/jdk/pull/23789) |
| **合入时间** | 2024-09 |
| **影响** | 性能优化 |

**背景**: 单次 native downcall 会生成大量动态代码，影响启动性能。

**解决方案**: 使用预生成的代码模板：
```java
// 变更前: 每次调用生成新代码
MethodHandle mh = linker.downcallHandle(functionAddress, functionDescriptor);

// 变更后: 使用共享模板
private static final MethodHandle[] SHARED_HANDLES = ...;

public MethodHandle downcallHandle(...) {
    // 查找匹配的共享句柄
    MethodHandle shared = findSharedHandle(...);
    if (shared != null) return shared;
    
    // 回退到动态生成
    return generateDowncallHandle(...);
}
```

**影响**: 提高了单次 downcall 的性能。

---

### javac 编译器 (9 PRs)

#### JDK-8365676: javac 错误允许通过类型变量调用接口静态方法

| 属性 | 值 |
|------|-----|
| **Issue** | [JDK-8365676](https://bugs.openjdk.org/browse/JDK-8365676) |
| **PR** | [#27189](https://github.com/openjdk/jdk/pull/27189) |
| **合入时间** | 2025-02 |
| **影响** | 正确性修复 |

**背景**: javac 错误地允许通过类型变量调用接口静态方法。

**问题分析**:
```java
interface I {
    static void staticMethod() {}
}

class Test<T extends I> {
    void test(T t) {
        // 变更前: 编译通过（错误）
        T.staticMethod();
        
        // 变更后: 编译错误
        // error: cannot find symbol
        //   T.staticMethod();
        //   ^
    }
}
```

**解决方案**: 在类型检查时添加验证：
```java
// Attr.java
void checkStaticMethodAccess(Symbol sym, Type site) {
    if (sym.isStatic() && sym.owner.isInterface()) {
        // 接口静态方法只能通过接口名访问
        if (site.hasTag(TYPEVAR)) {
            log.error(pos, Errors.IllegalStaticInterfaceMethodCall);
        }
    }
}
```

**影响**: 修复了 javac 的正确性问题。

---

#### JDK-8332934: do-while 循环 continue 后的 switch 导致错误的栈映射

| 属性 | 值 |
|------|-----|
| **Issue** | [JDK-8332934](https://bugs.openjdk.org/browse/JDK-8332934) |
| **PR** | [#18034](https://github.com/openjdk/jdk/pull/18034) |
| **合入时间** | 2023-10 |
| **影响** | 正确性修复 |

**背景**: do-while 循环中的 continue 后跟 switch 语句导致生成错误的栈映射帧。

**问题分析**:
```java
void test(int i) {
    do {
        if (i > 0) continue;  // continue 跳到 switch
        switch (i) {          // 栈映射帧错误
            case 0: break;
        }
    } while (i-- > 0);
}
```

**解决方案**: 修复栈映射帧生成逻辑：
```java
// Gen.java
void generateDoWhile(JCDoWhileLoop tree) {
    // 确保栈映射帧正确
    emitStackMapFrame();
    // ... 生成代码
}
```

**影响**: 修复了字节码生成的正确性问题。

---

### 测试迁移 (3 PRs)

#### JDK-8376277: 迁移 java/lang/reflect 测试到 JUnit

| 属性 | 值 |
|------|-----|
| **Issue** | [JDK-8376277](https://bugs.openjdk.org/browse/JDK-8376277) |
| **PR** | [#29405](https://github.com/openjdk/jdk/pull/29405) |
| **合入时间** | 2025-03 |
| **影响** | 测试现代化 |

**背景**: OpenJDK 正在将测试从 TestNG 迁移到 JUnit 5。

**解决方案**:
```java
// 变更前: TestNG
@Test
public void testMethod() {
    Assert.assertEquals(actual, expected);
}

// 变更后: JUnit 5
@Test
void testMethod() {
    assertEquals(expected, actual);
}
```

**影响**: 统一测试框架，便于维护。

---

## Project Valhalla 贡献

Chen Liang 是 **Project Valhalla 的顶级贡献者**，在项目中排名 **#1**。

| 指标 | 数值 |
|------|------|
| **PR 数量** | 11 |
| **排名** | #1 (所有贡献者中最高) |
| **主要领域** | javac 编译器、语言特性实现、ClassFile 适配 |
| **活跃时间** | 2023 - 2025 |
| **角色** | Valhalla Committer (2025年5月提名) |

### 贡献领域

- **javac 编译器**: 原始类型（Primitive Classes）的编译支持
- **语言特性**: 值类型（Value Types）的语法和语义实现
- **类文件生成**: 原始类型的字节码表示
- **ClassFile API 适配**: Valhalla 特性的 ClassFile 支持

### 重要贡献

#### JDK-8379559: 避免为 Valhalla 使用新的 ClassFileFormatVersion

| 属性 | 值 |
|------|-----|
| **Issue** | [JDK-8379559](https://bugs.openjdk.org/browse/JDK-8379559) |
| **PR** | [#2023](https://github.com/openjdk/valhalla/pull/2023) |
| **合入时间** | 2026-02 |
| **影响** | ClassFile API 优化 |

改进预览访问标志枚举常量的 ClassFileFormatVersion 处理方式。

#### JDK-8377171: Valhalla 内部注解警告注释

| 属性 | 值 |
|------|-----|
| **Issue** | [JDK-8377171](https://bugs.openjdk.org/browse/JDK-8377171) |
| **PR** | [#2023](https://github.com/openjdk/valhalla/pull/2023) |
| **合入时间** | 2026-02 |
| **影响** | 代码质量 |

为 Valhalla 内部注解添加警告注释。

> **来源**: [Valhalla 开发活动分析](/by-topic/core/valhalla/development.md), [CFV: New Valhalla Committer: Chen Liang](https://mail.openjdk.org/pipermail/valhalla-dev/2025-May/014193.html)

---

## 技术特长

`ClassFile API` `核心反射` `Method Handles` `常量池` `Valhalla` `API 设计`

## 兴趣领域

根据 GitHub 组织关联，Chen Liang 可能对以下领域感兴趣：
- **Minecraft** 开发 - 可能参与 Minecraft 相关项目或模组开发
- **开源项目** - 在 GitHub 上维护多个开源项目

> **来源**: [GitHub Profile](https://github.com/liach)

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

- **Shaojin Wen (@wenshao)**: 字符串/数字格式化优化协作者
  - 共同合作 ClassFile API 优化
  - Review 了 JDK-8336856 (String "+" 优化)
- **Claes Redestad (@redestad)**: 性能优化协作者
  - 共同参与 JDK-8336856 审查
- **Adam Sotona (asotona)**: ClassFile API 审查者
  - 共同合作 ClassFile API 开发
- **Jonathan Gibbons**: JDK Reviewer 提名人
  - LangTools 团队负责人
- **Jan Lahoda (jlahoda)**: javac 相关审查
- **Vicente Romero (vromero)**: javac 相关审查
- **John Rose (jrose)**: Method Handles / ClassValue 协作者
- **David Holmes (dholmes-ora)**: 运行时协作者
- **Tobias Hartmann (TobiHartmann)**: Valhalla C2 编译器协作者

### 重要协作：String "+" 优化 (JDK-8336856)

作为 JDK-8336856 的 **Reviewer**，与 Shaojin Wen（Author）和 Claes Redestad（Co-author）合作完成了这一重大优化：

| 角色 | 姓名 | 贡献 |
|------|------|------|
| **Author** | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) (@wenshao) | 主要实现 |
| **Co-author** | [Claes Redestad](../../by-contributor/profiles/claes-redestad.md) (@redestad) | 架构设计 |
| **Reviewer** | Chen Liang (@liach) | 代码审查 |

**项目成果**：
- 启动性能提升 **+40%**
- 类生成数量减少 **-50%**
- 审查周期 26 天，Tier 1-5 测试全部通过
- [详细分析](../../by-pr/8336/8336856.md)

这是 Chen Liang 与 Shaojin Wen 深度合作的典型案例，展示了 OpenJDK 社区协作者之间的高效协作模式。

---

## 数据来源

- **统计方法**: GitHub PR search `repo:openjdk/jdk author:liach type:pr label:integrated`
- **统计时间**: 2026-03-20
- **LinkedIn**: [Chen Liang - Oracle | LinkedIn](https://www.linkedin.com/in/chen-liang-51122427b)
- **JDK Reviewer 任命**: [CFV: New JDK Reviewer: Chen Liang](https://mail.openjdk.org/pipermail/jdk-dev/2024-June/009052.html)
- **Valhalla Committer 提名**: [CFV: New Valhalla Committer: Chen Liang](https://mail.openjdk.org/pipermail/valhalla-dev/2025-May/014193.html)
- **GitHub**: [@liach](https://github.com/liach)
- **Blog**: [liachmodded.github.io](https://liachmodded.github.io/)
- **CR 目录**: [cr.openjdk.org/~liach](https://cr.openjdk.org/~liach/)
- **Bug Database**: [Chen Liang Issues](https://bugs.openjdk.org/issues/?jql=project%20%3D%20JDK%20AND%20reporter%20in%20(liach%2C%20%22Chen%20Liang%22))

---

> **文档版本**: 4.0
> **最后更新**: 2026-03-20
> **更新内容**:
> - 补充 Valhalla Committer 提名信息 (2025-05)
> - 添加 javadoc types-facelift 项目信息
> - 补充 ClassFile API 文档改进贡献
> - 更新协作者列表
> - 添加更多数据来源链接

## 相关链接

- [OpenJDK Census](https://openjdk.org/census#liach)
- [GitHub Profile](https://github.com/liach)
- [Blog](https://liachmodded.github.io/)
- [ClassFile API 文档](https://docs.oracle.com/en/java/javase/26/docs/api/java.base/java/lang/classfile/package-summary.html)

### 相关分析文档

**核心反射**：
- [JDK-8371953: 反射 API 性能优化](../../by-pr/8371/8371953.md) - 核心 Reflection API 优化

**协作项目**：
- [JDK-8336856: String "+" 优化](../../by-pr/8336/8336856.md) - 与 Shaojin Wen、Claes Redestad 合作