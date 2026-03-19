# JEP 511 深入分析: Module Import Declarations

> 本文档深入分析 JEP 511 的源码实现，适合希望理解内部机制的读者。

---

## 1. 设计目标

### 问题陈述

传统 import 机制的问题：
```java
// 需要逐个导入
import java.util.List;
import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;
import java.util.Set;
import java.util.HashSet;
// ... 可能几十个 import
```

### 设计决策

| 决策 | 选择 | 原因 |
|------|------|------|
| 语法 | `import module <name>` | 与现有 import 语法一致 |
| 作用域 | 仅导入导出包 | 不暴露内部 API |
| 冲突处理 | 需要显式 disambiguate | 避免意外行为 |
| 兼容性 | 编译后与传统 import 相同 | 无运行时差异 |

---

## 2. 编译器实现

### 2.1 词法分析

**文件**: `src/jdk.compiler/share/classes/com/sun/tools/javac/parser/JavacParser.java`

```java
// 伪代码 - import 语句解析
private JCTree importDeclaration() {
    // 解析 import 关键字
    accept(IMPORT);
    
    // 检查是否是静态导入
    boolean isStatic = (token.kind == STATIC);
    if (isStatic) nextToken();
    
    // 检查是否是模块导入
    boolean isModule = false;
    if (token.kind == MODULE) {
        isModule = true;
        nextToken();
    }
    
    // 解析导入路径
    JCExpression pid = qualident();
    
    // 创建 AST 节点
    return toP(F.at(pos).Import(pid, isStatic, isModule));
}
```

### 2.2 AST 节点

**文件**: `src/jdk.compiler/share/classes/com/sun/source/tree/ImportTree.java`

```java
public interface ImportTree extends Tree {
    /**
     * 是否是静态导入
     */
    boolean isStatic();
    
    /**
     * 是否是模块导入 (JDK 25+)
     */
    boolean isModule();
    
    /**
     * 获取导入的标识符
     */
    Tree getQualifiedIdentifier();
}
```

### 2.3 符号解析

**核心流程**:

```
源码: import module java.base;
         ↓
    词法分析
         ↓
    语法分析 → ImportTree(isModule=true)
         ↓
    符号解析
         ↓
    ┌─────────────────────────────────┐
    │ 1. 获取模块 java.base            │
    │ 2. 读取模块描述符 (module-info)   │
    │ 3. 获取所有 exports 包           │
    │ 4. 将包加入导入作用域             │
    └─────────────────────────────────┘
         ↓
    后续类型解析时搜索这些包
```

**关键代码** (简化):

```java
// 模块导入解析
void resolveModuleImport(ModuleSymbol module) {
    // 1. 获取模块的所有导出包
    for (Exports export : module.exports) {
        PackageSymbol pkg = export.package;
        
        // 2. 检查是否有目标限制
        if (export.isQualified()) {
            // 仅对特定模块导出，跳过
            continue;
        }
        
        // 3. 将包加入当前作用域
        currentScope.enter(pkg);
    }
}
```

---

## 3. 模块系统变更

### 3.1 ModuleInfo 变更

**文件**: `src/java.base/share/classes/jdk/internal/module/ModuleInfo.java`

**变更内容**: 简化了 `requires transitive java.base` 的验证逻辑

```java
// 变更前: 复杂的条件判断
if (major >= 54
    && ((mods.contains(Requires.Modifier.TRANSITIVE)
         && !isPreview
         && !"java.se".equals(mn))
        || mods.contains(Requires.Modifier.STATIC))) {
    // 报错
}

// 变更后: 简化
if (major >= 54 && mods.contains(Requires.Modifier.STATIC)) {
    // 仅检查 STATIC 修饰符
}
```

**原因**: 模块导入需要更灵活的 `requires transitive` 处理。

### 3.2 类读取器变更

**文件**: `src/jdk.compiler/share/classes/com/sun/tools/javac/jvm/ClassReader.java`

移除了部分模块相关的限制检查，因为模块导入需要更宽松的语义。

---

## 4. JShell 集成

### 4.1 默认启动脚本

**文件**: `src/jdk.jshell/share/classes/jdk/jshell/tool/resources/DEFAULT.jsh`

```java
// 变更前: 多个 import 语句
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

// 变更后: 单行模块导入
import module java.base;
```

### 4.2 SnippetMaps 扩展

**文件**: `src/jdk.jshell/share/classes/jdk/jshell/SnippetMaps.java`

新增模块导入的映射处理：

```java
// 新增方法
public void addModuleImport(String moduleName) {
    // 解析模块并添加其导出包到导入作用域
    ModuleSymbol module = syms.getModule(names.fromString(moduleName));
    if (module == null) {
        // 错误: 模块未找到
        return;
    }
    
    // 添加所有导出包
    for (PackageSymbol pkg : module.exports) {
        addImport(pkg.fullname.toString());
    }
}
```

---

## 5. 冲突处理

### 5.1 命名冲突场景

```java
import module java.base;
import module java.sql;

public class Example {
    Date date;  // 错误: java.util.Date 和 java.sql.Date 冲突
}
```

### 5.2 解决方案

```java
// 方案 1: 显式导入
import module java.base;
import module java.sql;
import java.util.Date;  // 显式指定

public class Example {
    Date date;  // java.util.Date
}

// 方案 2: 完全限定名
public class Example {
    java.util.Date utilDate;
    java.sql.Date sqlDate;
}
```

### 5.3 编译器实现

```java
// 类型解析时的冲突检测
Symbol resolveType(Name name, Scope scope) {
    List<Symbol> candidates = new ArrayList<>();
    
    // 搜索所有导入的包
    for (PackageSymbol pkg : importedPackages) {
        Symbol sym = pkg.members().find(name);
        if (sym != null) {
            candidates.add(sym);
        }
    }
    
    // 检查冲突
    if (candidates.size() > 1) {
        // 报告歧义错误
        log.error(pos, Errors.AmbiguousType(name, candidates));
        return null;
    }
    
    return candidates.isEmpty() ? null : candidates.get(0);
}
```

---

## 6. 性能考虑

### 6.1 编译时开销

| 操作 | 传统 import | 模块 import |
|------|-------------|-------------|
| 解析 import | O(n) | O(1) |
| 类型查找 | O(n) n=import数 | O(m) m=导出包数 |
| 内存占用 | 低 | 中等 |

### 6.2 优化策略

```java
// 编译器缓存模块导出包列表
class ModuleExportsCache {
    private static final Map<ModuleSymbol, List<PackageSymbol>> cache = new ConcurrentHashMap<>();
    
    static List<PackageSymbol> getExports(ModuleSymbol module) {
        return cache.computeIfAbsent(module, m -> 
            m.exports.stream()
                .filter(e -> !e.isQualified())
                .map(e -> e.package)
                .toList()
        );
    }
}
```

---

## 7. 与其他 JEP 的关系

### 7.1 JEP 512: Compact Source Files

```java
// 两者配合使用
import module java.base;

void main() {
    println("Hello");  // 紧凑源文件 + 模块导入
}
```

### 7.2 JEP 476: Module Import Declarations (Preview)

JEP 511 是 JEP 476 的正式版本，主要变更：
- 移除预览标记
- 修复发现的问题
- 优化性能

---

## 8. 测试用例分析

**文件**: `test/langtools/tools/javac/ImportModule.java`

关键测试场景：

```java
// 测试 1: 基本模块导入
@Test
public void testImportJavaBase() {
    // import module java.base;
    // 应该能使用 List, ArrayList 等
}

// 测试 2: 多模块导入冲突
@Test
public void testAmbiguousImport() {
    // import module java.base;
    // import module java.sql;
    // Date 应该报歧义错误
}

// 测试 3: 传递依赖
@Test
public void testTransitiveDependencies() {
    // import module m1; // m1 requires transitive m2
    // 应该能访问 m2 的导出包
}

// 测试 4: 限定导出
@Test
public void testQualifiedExports() {
    // import module lib; // lib exports pkg to X
    // pkg 不应该被导入
}
```

---

## 9. 相关源码文件

```
src/jdk.compiler/share/classes/com/sun/
├── source/tree/ImportTree.java          # AST 接口
├── tools/javac/
│   ├── parser/JavacParser.java          # 语法解析
│   ├── comp/
│   │   ├── Enter.java                   # 符号进入
│   │   ├── MemberEnter.java             # 成员进入
│   │   └── Resolve.java                 # 类型解析
│   └── code/Source.java                 # 源码版本

src/java.base/share/classes/jdk/internal/module/
└── ModuleInfo.java                      # 模块信息解析

src/jdk.jshell/share/classes/jdk/jshell/
├── SnippetMaps.java                     # JShell 导入映射
└── tool/resources/DEFAULT.jsh           # 默认启动脚本
```

---

## 10. 总结

JEP 511 的实现涉及：
1. **编译器前端**: 新增模块导入语法解析
2. **符号解析**: 扩展导入作用域处理
3. **模块系统**: 简化 requires transitive 验证
4. **JShell 集成**: 更新默认启动脚本

核心设计原则：
- 保持与现有 import 语法的一致性
- 不暴露模块内部 API
- 编译后与传统 import 无差异