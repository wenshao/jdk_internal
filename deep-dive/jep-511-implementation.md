# JEP 511 深入分析: Module Import Declarations (模块导入声明)

> 本文档基于 OpenJDK 源码，深入分析 JEP 511 在 javac 编译器中的完整实现。
> 所有代码引用均来自 `src/jdk.compiler` 实际源文件，非伪代码。

---

## 1. 概述与设计目标 (Overview and Design Goals)

### 1.1 问题陈述 (Problem Statement)

传统 Java 导入机制 (traditional import mechanism) 要求逐个包或逐个类声明：

```java
// 典型的 java.base 相关导入 —— 冗长且重复
import java.util.List;
import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;
import java.util.Set;
import java.util.HashSet;
import java.util.stream.Collectors;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Files;
// ... 可能几十行
```

对于初学者 (beginners) 和原型开发 (prototyping)，这些样板代码 (boilerplate) 增加了不必要的阻力。

### 1.2 JEP 511 的解决方案

JEP 511 引入了 **模块导入声明 (module import declaration)** 语法：

```java
import module java.base;
```

一行代码即可导入模块所有**无限定导出包 (unqualified exports)** 中的所有公共顶层类型 (public top-level types)。

### 1.3 关键设计决策 (Key Design Decisions)

| 决策 | 选择 | 理由 |
|------|------|------|
| 语法形式 | `import module <name>;` | 复用 `import` 关键字，`module` 作为上下文关键字 (contextual keyword) |
| 导入范围 | 仅无限定导出包 | 不暴露模块内部 API (internal API)，不包含 qualified exports |
| 传递依赖 | 自动包含 `requires transitive` 的模块 | 与模块系统语义一致 |
| 冲突处理 | 编译器报 `ref.ambiguous` 错误 | 开发者须用显式导入 (explicit import) 消歧 |
| 优先级 | 低于 `import` 和 `import ... *` | 新增独立作用域 `moduleImportScope`，查找顺序最低 |
| 编译产物 | 与传统 import 相同的 class 文件 | 无运行时差异 (no runtime difference) |
| 最低版本 | JDK 25 (`Source.Feature.MODULE_IMPORTS`) | JEP 476 (JDK 23 preview) 的正式版 |

---

## 2. 语法与解析 (Syntax and Parsing)

### 2.1 词法/语法分析 (Lexing and Parsing)

**源文件**: `src/jdk.compiler/share/classes/com/sun/tools/javac/parser/JavacParser.java`

`importDeclaration()` 方法处理所有 import 语句。对于模块导入，关键识别逻辑如下（摘自实际源码）：

```java
// JavacParser.java — importDeclaration() 方法
protected JCTree importDeclaration() {
    int pos = token.pos;
    nextToken();                              // 消费 IMPORT token
    boolean importStatic = false;
    if (token.kind == STATIC) {
        importStatic = true;
        nextToken();
    } else if (token.kind == IDENTIFIER && token.name() == names.module &&
               peekToken(TokenKind.IDENTIFIER)) {
        // ---- 模块导入分支 ----
        checkSourceLevel(Feature.MODULE_IMPORTS);   // 检查源码级别 >= JDK 25
        nextToken();                                // 消费 "module" 标识符
        JCExpression moduleName = qualident(false);  // 解析模块名 (如 java.base)
        accept(SEMI);                               // 消费分号
        return toP(F.at(pos).ModuleImport(moduleName));
    }
    // ... 常规 import / import static 处理 ...
}
```

**要点**:
- `module` 不是 Java 保留字，而是**上下文关键字** (context-sensitive keyword)。解析器通过 `token.name() == names.module` 配合 `peekToken(TokenKind.IDENTIFIER)` 双重检查来识别。
- `checkSourceLevel(Feature.MODULE_IMPORTS)` 确保源码版本 >= JDK 25。对 `--release 24` 编译时会报错：`compiler.err.feature.not.supported.in.source.plural: (compiler.misc.feature.module.imports), 24, 25`。

### 2.2 Feature 注册

**源文件**: `src/jdk.compiler/share/classes/com/sun/tools/javac/code/Source.java`

```java
MODULE_IMPORTS(JDK25, Fragments.FeatureModuleImports, DiagKind.PLURAL),
```

该枚举将模块导入功能绑定到 JDK 25 源码级别 (source level)。

---

## 3. AST 节点结构 (AST Node Structure)

### 3.1 类继承体系

**源文件**: `src/jdk.compiler/share/classes/com/sun/tools/javac/tree/JCTree.java`

JEP 511 引入了独立的 AST 节点类 `JCModuleImport`，与传统 `JCImport` 共享抽象基类 `JCImportBase`：

```
JCTree
  └── JCImportBase (abstract, implements ImportTree)
        ├── JCImport          — 传统 import 和 import static
        └── JCModuleImport    — import module 声明
```

### 3.2 JCImportBase 基类

```java
public static abstract class JCImportBase extends JCTree implements ImportTree {
    @DefinedBy(Api.COMPILER_TREE)
    public Kind getKind() { return Kind.IMPORT; }

    @Override @DefinedBy(Api.COMPILER_TREE)
    public <R,D> R accept(TreeVisitor<R,D> v, D d) {
        return v.visitImport(this, d);
    }

    public abstract JCTree getQualifiedIdentifier();
}
```

注意 `JCImportBase` 和 `JCModuleImport` 的 `getKind()` 都返回 `Kind.IMPORT`，对 Tree API 的使用者而言，模块导入仍然是 "IMPORT" 类别。通过 `isModule()` 方法区分。

### 3.3 JCModuleImport 节点

```java
public static class JCModuleImport extends JCImportBase {
    /** The module name. 模块名表达式 */
    public JCExpression module;

    protected JCModuleImport(JCExpression module) {
        this.module = module;
    }

    @Override
    public void accept(Visitor v) { v.visitModuleImport(this); }

    @DefinedBy(Api.COMPILER_TREE)
    public boolean isStatic() { return false; }     // 模块导入不是 static import
    @DefinedBy(Api.COMPILER_TREE)
    public boolean isModule() { return true; }      // 标记为模块导入
    @DefinedBy(Api.COMPILER_TREE)
    public JCExpression getQualifiedIdentifier() { return module; }

    @Override
    public Tag getTag() { return MODULEIMPORT; }    // 独立的 Tag 枚举值
}
```

`Tag.MODULEIMPORT` 是 JCTree.Tag 枚举中新增的值（行 110），使编译器各阶段可以通过 `hasTag(MODULEIMPORT)` 识别模块导入节点。

### 3.4 ImportTree 公共 API

**源文件**: `src/jdk.compiler/share/classes/com/sun/source/tree/ImportTree.java`

```java
public interface ImportTree extends Tree {
    boolean isStatic();

    /**
     * {@return true if this is an module import declaration.}
     * @since 25
     */
    boolean isModule();

    Tree getQualifiedIdentifier();
}
```

`isModule()` 方法从 JDK 25 起添加，是区分模块导入和传统导入的公共 API。

### 3.5 JCCompilationUnit 中的作用域

每个编译单元 (compilation unit) 维护三个独立的导入作用域：

```java
// JCTree.java — JCCompilationUnit 类
/** A scope for all named imports. 单类型导入作用域 */
public NamedImportScope namedImportScope;
/** A scope for all import-on-demands. 通配符导入作用域 */
public StarImportScope starImportScope;
/** A scope for all single module imports. 模块导入作用域 */
public StarImportScope moduleImportScope;
```

`moduleImportScope` 是 JEP 511 新增的。类型为 `StarImportScope`（与 `starImportScope` 相同），因为模块导入在语义上等价于一组按需导入 (on-demand imports)。

---

## 4. 树工具类的适配 (Tree Utility Adaptations)

### 4.1 TreeMaker — 节点工厂

**源文件**: `src/jdk.compiler/share/classes/com/sun/tools/javac/tree/TreeMaker.java`

```java
public JCModuleImport ModuleImport(JCExpression moduleName) {
    JCModuleImport tree = new JCModuleImport(moduleName);
    tree.pos = pos;
    return tree;
}
```

### 4.2 Pretty — 源码打印

**源文件**: `src/jdk.compiler/share/classes/com/sun/tools/javac/tree/Pretty.java`

```java
public void visitModuleImport(JCModuleImport tree) {
    try {
        print("import module ");
        printExpr(tree.module);
        print(';');
        println();
    } catch (IOException e) {
        throw new UncheckedIOException(e);
    }
}
```

### 4.3 TreeScanner — 树遍历

**源文件**: `src/jdk.compiler/share/classes/com/sun/tools/javac/tree/TreeScanner.java`

```java
@Override
public void visitModuleImport(JCModuleImport tree) {
    scan(tree.module);
}
```

### 4.4 TreeTranslator — 树变换

**源文件**: `src/jdk.compiler/share/classes/com/sun/tools/javac/tree/TreeTranslator.java`

为 `JCModuleImport` 新增了 `visitModuleImport` 方法。

### 4.5 TreeCopier — 树复制

**源文件**: `src/jdk.compiler/share/classes/com/sun/tools/javac/tree/TreeCopier.java`

```java
@DefinedBy(Api.COMPILER_TREE)
public JCTree visitImport(ImportTree node, P p) {
    if (node instanceof JCModuleImport mimp) {
        JCExpression module = copy(mimp.module, p);
        return M.at(mimp.pos).ModuleImport(module);
    } else {
        JCImport t = (JCImport) node;
        JCFieldAccess qualid = copy(t.qualid, p);
        return M.at(t.pos).Import(qualid, t.staticImport);
    }
}
```

### 4.6 TreeDiffer — 树比较

**源文件**: `src/jdk.compiler/share/classes/com/sun/tools/javac/comp/TreeDiffer.java`

```java
public void visitModuleImport(JCModuleImport tree) {
    JCModuleImport that = (JCModuleImport) parameter;
    // 比较两个模块导入是否等价
}
```

---

## 5. 符号解析：doModuleImport 核心实现 (Symbol Resolution)

### 5.1 编译阶段定位

模块导入的解析发生在 **TypeEnter** 阶段 (类型进入 / type entering)，具体在 `ImportsPhase` 内部类的 `resolveImports` 方法中。

**源文件**: `src/jdk.compiler/share/classes/com/sun/tools/javac/comp/TypeEnter.java`

编译流水线 (compilation pipeline) 中的位置：

```
源码解析 (Parse)
    ↓
符号进入 (Enter) — 建立顶层符号表
    ↓
类型进入 (TypeEnter) — ImportsPhase
    ├── implicitImports()        ← java.lang.* 隐式导入 + 隐式类的 java.base 导入
    ├── handleImports()          ← 处理所有用户声明的 import (包括 module import)
    │     ├── doModuleImport()   ← 处理 import module 声明
    │     └── doImport()         ← 处理传统 import 声明
    ↓
成员进入 (MemberEnter)
    ↓
属性标注 (Attr) — 类型检查和解析
    ↓
代码生成 (Gen)
```

### 5.2 handleImports — 分发入口

```java
private void handleImports(List<JCImportBase> imports) {
    for (JCImportBase imp : imports) {
        if (imp instanceof JCModuleImport mimp) {
            doModuleImport(mimp);      // 模块导入走专用路径
        } else {
            doImport((JCImport) imp, false);
        }
    }
}
```

用 `instanceof` 模式匹配 (pattern matching) 区分 `JCModuleImport` 和 `JCImport`。

### 5.3 doModuleImport — 完整源码分析

这是 JEP 511 的**核心方法**，完整逻辑如下：

```java
private void doModuleImport(JCModuleImport tree) {
    Name moduleName = TreeInfo.fullName(tree.module);
    ModuleSymbol module = syms.getModule(moduleName);

    if (module != null) {
        // ---- 第一步: 检查模块可读性 (readability check) ----
        if (!env.toplevel.modle.readModules.contains(module)) {
            if (env.toplevel.modle.isUnnamed()) {
                // 无名模块 (unnamed module): 报 "unnamed module does not read: X"
                log.error(tree.pos, Errors.ImportModuleDoesNotReadUnnamed(module));
            } else {
                // 命名模块 (named module): 报 "module A does not read: X"
                log.error(tree.pos, Errors.ImportModuleDoesNotRead(
                    env.toplevel.modle, module));
            }
            // 错误恢复：确保模块的指令 (directives) 被加载
            module.getDirectives();
        }

        // ---- 第二步: BFS 遍历模块及其 transitive 依赖 ----
        List<ModuleSymbol> todo = List.of(module);
        Set<ModuleSymbol> seenModules = new HashSet<>();

        while (!todo.isEmpty()) {
            ModuleSymbol currentModule = todo.head;
            todo = todo.tail;

            if (!seenModules.add(currentModule)) {
                continue;    // 已处理过，跳过 (防止循环)
            }

            // ---- 第三步: 处理当前模块的每个 exports 指令 ----
            for (ExportsDirective export : currentModule.exports) {
                // 跳过限定导出 (qualified exports)
                if (export.modules != null &&
                    !export.modules.contains(env.toplevel.modle)) {
                    continue;
                }

                // 将导出包转换为 import pkg.* 形式的合成导入
                PackageSymbol pkg = export.getPackage();
                JCImport nestedImport = make.at(tree.pos)
                    .Import(make.Select(make.QualIdent(pkg), names.asterisk), false);

                // 调用 doImport，标记 fromModuleImport=true
                doImport(nestedImport, true);
            }

            // ---- 第四步: 追踪 requires transitive 依赖 ----
            for (RequiresDirective requires : currentModule.requires) {
                if (requires.isTransitive()) {
                    todo = todo.prepend(requires.module);
                }
            }
        }
    } else {
        // 模块未找到: 报 "imported module not found: X"
        log.error(tree.pos, Errors.ImportModuleNotFound(moduleName));
    }
}
```

### 5.4 关键设计细节

**BFS 遍历传递依赖 (Transitive Dependencies)**:
- 算法使用广度优先搜索 (BFS) 遍历 `requires transitive` 链。
- `seenModules` 集合防止重复处理和循环引用。
- 仅追踪 `requires transitive` 的模块，不追踪普通 `requires`。

**限定导出过滤 (Qualified Export Filtering)**:
- `export.modules != null` 表示这是一个限定导出 (如 `exports impl to use`)。
- 仅当当前编译单元所属模块在 `export.modules` 列表中时才导入。
- 对于无名模块 (unnamed module) 中的代码，限定导出永远被跳过。

**合成导入 (Synthetic Import)**:
- 每个导出包被转换为等价的 `import pkg.*;` 合成 `JCImport` 节点。
- 调用 `doImport(nestedImport, true)` 时第二个参数 `fromModuleImport=true` 控制目标作用域。

### 5.5 importAll 中的作用域分流

```java
private void importAll(JCImport imp, final TypeSymbol tsym,
                       Env<AttrContext> env, boolean fromModuleImport) {
    StarImportScope targetScope =
            fromModuleImport ? env.toplevel.moduleImportScope   // 模块导入 → moduleImportScope
                             : env.toplevel.starImportScope;    // 普通 import * → starImportScope

    targetScope.importAll(types, tsym.members(), typeImportFilter, imp, cfHandler);
}
```

`fromModuleImport` 标志确保模块导入的符号进入 `moduleImportScope` 而非 `starImportScope`，从而实现不同的查找优先级。

---

## 6. 类型查找优先级 (Type Lookup Precedence)

### 6.1 Resolve.java 中的查找顺序

**源文件**: `src/jdk.compiler/share/classes/com/sun/tools/javac/comp/Resolve.java`

当编译器需要解析一个简单类型名 (如 `List`) 时，按以下顺序在各作用域中查找：

```java
// Resolve.java — findType 方法中的查找链
// 1. 局部作用域 (local scopes) — 循环遍历封闭的类和方法

// 2. 单类型导入 (named imports)
sym = findGlobalType(env, env.toplevel.namedImportScope, name, ...);
if (sym.exists()) return sym;

// 3. 同文件顶层类 (top-level classes in same file)
sym = findGlobalType(env, env.toplevel.toplevelScope, name, ...);
if (sym.exists()) return sym;

// 4. 同包类 (classes in same package)
sym = findGlobalType(env, env.toplevel.packge.members(), name, ...);
if (sym.exists()) return sym;

// 5. 通配符导入 (star imports, import ... *)
sym = findGlobalType(env, env.toplevel.starImportScope, name, ...);
if (sym.exists()) return sym;

// 6. 模块导入 (module imports) — 优先级最低
sym = findGlobalType(env, env.toplevel.moduleImportScope, name, ...);
if (sym.exists()) return sym;
```

### 6.2 优先级总结

| 优先级 | 作用域 | 来源 |
|--------|--------|------|
| 1 (最高) | 局部作用域 (local scope) | 封闭类、方法中的声明 |
| 2 | `namedImportScope` | `import java.util.List;` |
| 3 | `toplevelScope` | 同文件中的其他顶层类 |
| 4 | `packge.members()` | 同包中的其他类 |
| 5 | `starImportScope` | `import java.util.*;` |
| 6 (最低) | `moduleImportScope` | `import module java.base;` |

这意味着：
- 显式的 `import java.util.Date;` (优先级 2) 总是优先于模块导入 (优先级 6)。
- `import java.util.*;` (优先级 5) 也优先于 `import module java.sql;` (优先级 6)。
- 两个模块导入之间若导出相同简单类名的类，则报歧义错误。

### 6.3 错误恢复 (Recovery)

```java
// Resolve.java
private final RecoveryLoadClass moduleImportScopeRecovery =
        onDemandImportScopeRecovery(true);

private RecoveryLoadClass onDemandImportScopeRecovery(boolean moduleImportScope) {
    return (env, name) -> {
        Scope importScope = moduleImportScope ? env.toplevel.moduleImportScope
                                              : env.toplevel.starImportScope;
        Symbol existing = importScope.findFirst(Convert.shortName(name),
                sym -> sym.kind == TYP && sym.flatName() == name);
        // ... 尝试通过 ClassFinder 加载类 ...
    };
}
```

`moduleImportScopeRecovery` 和 `starImportScopeRecovery` 使用相同的恢复策略工厂方法，仅目标作用域不同。

---

## 7. 冲突处理 (Conflict Resolution)

### 7.1 歧义场景 (Ambiguity Scenario)

当两个模块导出包含相同简单名称的类时：

```java
import module java.base;    // 导出 java.util.Date
import module java.sql;     // 导出 java.sql.Date

public class Example {
    Date d;  // 编译错误: ref.ambiguous
}
```

编译器报错信息（来自测试用例验证）：
```
compiler.err.ref.ambiguous: Date, kindname.class, java.sql.Date, java.sql,
                            kindname.class, java.util.Date, java.util
```

### 7.2 消歧方法 (Disambiguation)

**方法一**: 添加显式单类型导入 (explicit single-type import)
```java
import module java.base;
import module java.sql;
import java.util.Date;      // 优先级 2，高于模块导入的优先级 6

public class Example {
    Date d;                  // 解析为 java.util.Date
}
```

**方法二**: 使用完全限定名 (fully qualified name)
```java
import module java.base;
import module java.sql;

public class Example {
    java.util.Date  utilDate;
    java.sql.Date   sqlDate;
}
```

**方法三**: 使用通配符导入 (star import) 消歧
```java
import module java.base;
import module java.sql;
import java.util.*;          // 优先级 5，高于模块导入的优先级 6

public class Example {
    Date d;                  // 解析为 java.util.Date
}
```

### 7.3 模块导入与星号导入的交互

来自测试用例 `testConflicts`：

```java
import module java.logging;       // 导出 java.util.logging.Logger
import java.lang.System.*;        // 导出 System.Logger (内部类)

public class Test {
    Logger l;                      // 不冲突! star import (优先级 5) 胜出
}
```

因为 `starImportScope` 的优先级高于 `moduleImportScope`，所以 `System.Logger` 被选中。

---

## 8. 隐式类的自动导入 (Implicit Class Auto-Import)

### 8.1 implicitImports 中的自动 java.base 导入

**源文件**: `src/jdk.compiler/share/classes/com/sun/tools/javac/comp/TypeEnter.java`

对于隐式类 (implicit class，JEP 477/512)，编译器自动注入 `import module java.base;`：

```java
private void implicitImports(JCCompilationUnit tree, Env<AttrContext> env) {
    // 始终导入 java.lang.*
    importAll(make.at(tree.pos()).Import(
        make.Select(make.QualIdent(javaLang.owner), javaLang), false),
        javaLang, env, false);

    List<JCTree> defs = tree.getTypeDecls();
    boolean isImplicitClass = !defs.isEmpty() &&
            defs.head instanceof JCClassDecl cls &&
            (cls.mods.flags & IMPLICIT_CLASS) != 0;

    if (isImplicitClass) {
        // 隐式类自动获得 import module java.base
        doModuleImport(make.ModuleImport(make.QualIdent(syms.java_base)));
    }
}
```

这使得隐式类 (如 JEP 512 紧凑源文件) 可以直接使用 `List`、`Map`、`Path` 等类型而无需任何 import 声明：

```java
// 隐式类 + 自动模块导入
void main() {
    var list = new ArrayList<String>();
    var path = Path.of("/tmp");
    println("Hello");
}
```

---

## 9. 错误诊断消息 (Error Diagnostic Messages)

**源文件**: `src/jdk.compiler/share/classes/com/sun/tools/javac/resources/compiler.properties`

JEP 511 定义了三个专用错误消息：

```properties
# 模块未找到
compiler.err.import.module.not.found=\
    imported module not found: {0}

# 无名模块不可读
compiler.err.import.module.does.not.read.unnamed=\
    unnamed module does not read: {0}

# 命名模块不可读
compiler.err.import.module.does.not.read=\
    module {0} does not read: {1}
```

### 9.1 错误触发场景

**模块未找到 (Module Not Found)**:
```java
import module nonexistent.module;  // 编译器报: imported module not found: nonexistent.module
```

**模块不可读 — 无名模块 (Unnamed Module)**:
```java
// 在无名模块中, 如果模块不在模块路径上:
import module lib;  // 编译器报: unnamed module does not read: lib
```

**模块不可读 — 命名模块 (Named Module)**:
```java
// module-info.java 中没有 requires lib:
module myapp { }

// 在 myapp 的源文件中:
import module lib;  // 编译器报: module myapp does not read: lib
```

---

## 10. 模块系统交互 (Module System Interaction)

### 10.1 仅导入 exports，不导入 opens

模块导入只处理 `ExportsDirective`，不涉及 `OpensDirective`。一个包即使被 `opens` 给所有模块（用于反射 / reflection），也不会被模块导入引入：

```java
module lib {
    exports api;           // import module lib 会导入 api 包
    opens internal;        // import module lib 不会导入 internal 包
    exports impl to use;   // 仅导入给 use 模块，其他模块不可见
}
```

### 10.2 requires transitive 的传递规则

`doModuleImport` 通过 BFS 遍历 `requires transitive` 链：

```java
// 模块声明
module m1 {
    requires transitive m2;    // m2 的导出包也会被 import module m1 导入
    exports api1;
}
module m2 {
    exports api4;
    exports api5 to test;      // 限定导出
}

// 使用方
module test { requires m1; }

// 在 test 模块的源文件中:
import module m1;
// 可见: api1.* (来自 m1) + api4.* (来自 m2, 通过 transitive)
// 可见: api5.* (来自 m2, 限定导出给 test)
// 不可见: m1 和 m2 的非导出包
```

来自测试 `testTransitiveDependencies` 的验证：
- `import module m1` → `Api1` 可用 (m1 的无限定导出), `Api4` 可用 (m2 通过 transitive), `Api2` 可用 (限定导出给 test)
- `Api3` 不可用 (限定导出给 m3), `Impl1` 不可用 (未导出)

### 10.3 可读性检查 (Readability Check)

在处理导出包之前，编译器检查当前模块是否可以读取 (read) 目标模块：

```java
if (!env.toplevel.modle.readModules.contains(module)) {
    // 报错但继续 (错误恢复)
}
```

这意味着你必须在 `module-info.java` 中声明 `requires` 对应的模块，然后才能 `import module` 它。对于无名模块 (unnamed module)，模块路径上的所有模块自动可读。

---

## 11. JShell 集成 (JShell Integration)

### 11.1 默认启动脚本

**源文件**: `src/jdk.jshell/share/classes/jdk/jshell/tool/resources/DEFAULT.jsh`

JDK 25 之前的 `DEFAULT.jsh` 包含多个 `import` 语句：

```java
// 旧版 DEFAULT.jsh (JDK 24 及之前)
import java.io.*;
import java.math.*;
import java.net.*;
import java.nio.file.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.function.*;
import java.util.prefs.*;
import java.util.regex.*;
import java.util.stream.*;
```

JDK 25 起简化为一行：

```java
import module java.base;
```

这为 JShell 用户提供了 `java.base` 模块所有导出包中的类型，覆盖范围远超旧版的手动列表。

---

## 12. 测试用例分析 (Test Case Analysis)

**源文件**: `test/langtools/tools/javac/ImportModule.java`

该测试文件覆盖了以下关键场景：

### 12.1 基本模块导入

```java
@Test
public void testImportJavaBase(Path base) throws Exception {
    // 源码: import module java.base;
    // 验证: List 和 ArrayList 可直接使用
    // 验证: 编译产物正确, 运行输出 "java.util.ArrayList"
}
```

### 12.2 源码级别检查

```java
@Test
public void testVerifySourceLevelCheck(Path base) throws Exception {
    // 使用 --release 24 编译 import module 语句
    // 预期错误: feature.not.supported.in.source.plural: module.imports, 24, 25
}
```

### 12.3 冲突检测

```java
@Test
public void testConflicts(Path base) throws Exception {
    // 场景 1: import module java.base + import module java.sql → Date 歧义
    // 场景 2: 添加 import java.util.Date 可消歧
    // 场景 3: import module java.logging + import java.lang.System.* → Logger 不冲突
    //         (star import 优先级高于 module import)
}
```

### 12.4 限定导出排除

```java
@Test
public void testNoQualifiedExports(Path base) throws Exception {
    // module lib { exports api; exports impl to use; }
    // import module lib → Api 可见, Impl 不可见 (限定导出)
}
```

### 12.5 传递依赖

```java
@Test
public void testTransitiveDependencies(Path base) throws Exception {
    // module m1 { requires transitive m2; exports api1; exports api2 to test; }
    // module m2 { exports api4; exports api5 to test; exports api6 to m3; }
    //
    // import module m1:
    //   Api1 ✓ (m1 无限定导出)
    //   Api2 ✓ (m1 限定导出给 test)
    //   Api3 ✗ (m1 限定导出给 m3)
    //   Impl1 ✗ (m1 未导出)
    //   Api4 ✓ (m2 通过 transitive, 无限定导出)
    //   Api5 ✓ (m2 通过 transitive, 限定导出给 test)
    //   Api6 ✗ (m2 通过 transitive, 但限定导出给 m3)
    //   Impl2 ✗ (m2 未导出)
}
```

---

## 13. 修改的源文件清单 (Modified Source Files)

### 13.1 编译器核心 (jdk.compiler)

```
src/jdk.compiler/share/classes/com/sun/
├── source/tree/
│   └── ImportTree.java                  # 新增 isModule() 方法 (@since 25)
├── tools/javac/
│   ├── code/
│   │   └── Source.java                  # 新增 Feature.MODULE_IMPORTS(JDK25)
│   ├── parser/
│   │   └── JavacParser.java            # importDeclaration() 新增模块导入解析分支
│   ├── tree/
│   │   ├── JCTree.java                 # 新增 JCImportBase 基类、JCModuleImport 节点、
│   │   │                               #   Tag.MODULEIMPORT、moduleImportScope 字段
│   │   ├── TreeMaker.java             # 新增 ModuleImport() 工厂方法
│   │   ├── Pretty.java                # 新增 visitModuleImport() 打印方法
│   │   ├── TreeScanner.java           # 新增 visitModuleImport() 遍历方法
│   │   ├── TreeTranslator.java        # 新增 visitModuleImport() 变换方法
│   │   └── TreeCopier.java            # visitImport() 增加 JCModuleImport 分支
│   ├── comp/
│   │   ├── TypeEnter.java             # 核心: doModuleImport(), handleImports(),
│   │   │                               #   implicitImports() 中的隐式类处理
│   │   ├── Resolve.java               # 新增 moduleImportScope 查找步骤,
│   │   │                               #   moduleImportScopeRecovery
│   │   └── TreeDiffer.java            # 新增 visitModuleImport() 比较方法
│   └── resources/
│       └── compiler.properties         # 新增 3 个错误消息:
│                                        #   import.module.not.found
│                                        #   import.module.does.not.read.unnamed
│                                        #   import.module.does.not.read
```

### 13.2 JShell

```
src/jdk.jshell/share/classes/jdk/jshell/
└── tool/resources/
    └── DEFAULT.jsh                      # 替换为 import module java.base;
```

### 13.3 测试

```
test/langtools/tools/javac/
├── ImportModule.java                    # 主测试: 基本导入、冲突、限定导出、transitive
├── processing/
│   └── ModuleImportProcessingTest.java  # 注解处理器与模块导入的交互
└── diags/examples/
    ├── ImportModule.java                # 诊断示例
    ├── ImportModuleNotFound.java        # 模块未找到诊断示例
    └── ImportModuleDoesNotReadUnnamed.java  # 无名模块不可读诊断示例
```

---

## 14. 与 JEP 476 (Preview) 的关系

JEP 511 是 JEP 476 (Module Import Declarations, Preview in JDK 23) 的正式版本 (final)。主要变更：

- 移除 `@Preview` 限制，不再需要 `--enable-preview` 标志
- 源码级别从预览特性升级为 `JDK25` 标准特性
- Bug 修复: 8328481, 8332236, 8332890, 8344647, 8347646 (参见测试文件头部的 `@bug` 注解)
- 完善了与隐式类 (JEP 477/512) 的集成

---

## 15. 总结 (Summary)

JEP 511 的实现涉及编译器的多个层次：

1. **解析层 (Parser)**: `JavacParser.importDeclaration()` 识别 `import module` 语法，创建 `JCModuleImport` AST 节点。

2. **AST 层 (Tree)**: `JCModuleImport` 继承 `JCImportBase`，使用独立的 `Tag.MODULEIMPORT`。六个树工具类 (TreeMaker, Pretty, TreeScanner, TreeTranslator, TreeCopier, TreeDiffer) 全部适配。

3. **符号解析层 (TypeEnter)**: `doModuleImport()` 通过 BFS 遍历目标模块及其 `requires transitive` 依赖，将每个无限定导出包转换为合成的 `import pkg.*;`，注入 `moduleImportScope`。

4. **类型查找层 (Resolve)**: `moduleImportScope` 作为优先级最低的查找作用域，确保显式导入和通配符导入始终优先。

5. **模块系统交互**: 仅处理 `exports` 指令（不处理 `opens`），跳过限定导出（除非当前模块在目标列表中），自动追踪 `requires transitive` 链。

核心设计原则：
- 模块导入是纯粹的**编译期语法糖** (compile-time syntactic sugar)，不改变 class 文件格式或运行时行为
- 通过独立的 `moduleImportScope` 实现最低优先级，不干扰现有导入语义
- 完全尊重模块系统的封装边界 (encapsulation boundary)
