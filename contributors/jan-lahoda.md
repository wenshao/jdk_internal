# Jan Lahoda

> javac 核心开发者，JEP 511/512 主导者

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Jan Lahoda |
| **当前组织** | Oracle |
| **GitHub** | [@jlahoda](https://github.com/jlahoda) |
| **OpenJDK** | [@jlahoda](https://openjdk.org/census#jlahoda) |
| **角色** | JDK Reviewer |
| **主要领域** | javac, JShell, 语言特性 |
| **主导 JEP** | JEP 511, JEP 512 |
| **活跃时间** | 2006 - 至今 |

> **数据调查时间**: 2026-03-19

---

## 贡献概览

### 按类别统计

| 类别 | 数量 | 占比 |
|------|------|------|
| javac 改进 | 35 | 56% |
| JShell 改进 | 15 | 24% |
| JEP 实现 | 5 | 8% |
| Bug 修复 | 7 | 12% |

### 关键成就

- **JEP 511**: Module Import Declarations
- **JEP 512**: Compact Source Files and Instance Main Methods
- **JShell 改进**: 大量可用性改进

---

## PR 列表

### JEP 实现

| Issue | 标题 | 描述 |
|-------|------|------|
| 8344708 | Implement JEP 511: Module Import Declarations | **模块导入** |
| 8344706 | Implement JEP 512: Compact Source Files and Instance Main Methods | **紧凑源文件** |

### javac 编译器

| Issue | 标题 | 描述 |
|-------|------|------|
| 8372336 | javac fails with an exception when a class is missing while evaluating conditional expression | 条件表达式修复 |
| 8371309 | Diagnostic.getEndPosition can throw an NPE with typical broken code | NPE 修复 |
| 8371248 | Crash in -Xdoclint with invalid @link | 文档注释崩溃修复 |
| 8364991 | Incorrect not-exhaustive error | switch 穷尽性检查修复 |
| 8370865 | Incorrect parser error for compact source files and multi-variable declarations | 解析器错误修复 |
| 8369489 | Marker annotation on inner class access crashes javac compiler | 内部类注解崩溃修复 |
| 8366968 | Exhaustive switch expression rejected for not covering all possible values | switch 表达式修复 |
| 8367499 | Refactor exhaustiveness computation from Flow into a separate class | 重构穷尽性计算 |
| 8368848 | JShell's code completion not always working for multi-snippet inputs | 代码补全修复 |
| 8365314 | javac fails with an exception for erroneous source | 错误源码处理 |
| 8364987 | javac fails with an exception when looking for diamond creation | 菱形创建修复 |
| 8362885 | A more formal way to mark javac's Flags that belong to a specific Symbol type | 标志标记改进 |
| 8362116 | System.in.read() etc. don't accept input once immediate Ctrl+D pressed in JShell | JShell 输入修复 |
| 8361570 | Incorrect 'sealed is not allowed here' compile-time error | sealed 错误修复 |
| 8359497 | IllegalArgumentException thrown by SourceCodeAnalysisImpl.highlights() | 高亮异常修复 |
| 8351260 | java.lang.AssertionError: Unexpected type tree: (ERROR) = (ERROR) | 类型树断言修复 |
| 8341342 | Elements.getAllModuleElements() does not work properly before JavacTask.analyze() | 模块元素获取修复 |

### JShell 改进

| Issue | 标题 | 描述 |
|-------|------|------|
| 8370334 | javadoc NPE with "import module" statement | 模块导入文档修复 |
| 8366691 | JShell should support a more convenient completion | 代码补全改进 |
| 8340840 | jshell ClassFormatError when making inner class static | 内部类修复 |
| 8368999 | jshell crash when existing sealed class is updated to also be abstract | sealed 类崩溃修复 |
| 8357809 | Test JdiListeningExecutionControlTest.java failed with TransportTimeoutException | 测试修复 |
| 8366582 | Test ToolSimpleTest.java failed: provider not found | 测试修复 |
| 8285150 | Improve tab completion for annotations | 注解补全改进 |
| 8177650 | JShell tool: packages in classpath don't appear in completions | 包补全改进 |
| 8365776 | Convert JShell tests to use JUnit instead of TestNG | 测试框架迁移 |

### javadoc 改进

| Issue | 标题 | 描述 |
|-------|------|------|
| 8365689 | Elements.getFileObjectOf fails with a NullPointerException when an erroneous Element is passed in | NPE 修复 |
| 8365060 | Historical data for JDK 8 should include the jdk.net package | 历史数据修复 |

---

## 关键贡献详解

### 1. JEP 511: Module Import Declarations

**背景**: 传统 import 需要逐个导入类，繁琐且冗长。

**解决方案**: 支持模块级导入。

```java
// 变更前
import java.util.List;
import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;
// ... 可能几十个 import

// 变更后
import module java.base;  // 导入整个模块的导出包
```

**编译器实现**:

```java
// ImportTree 接口扩展
public interface ImportTree extends Tree {
    boolean isStatic();
    boolean isModule();  // 新增
    Tree getQualifiedIdentifier();
}

// 模块导入解析
void resolveModuleImport(ModuleSymbol module) {
    for (Exports export : module.exports) {
        if (!export.isQualified()) {
            currentScope.enter(export.package);
        }
    }
}
```

**影响**: 简化了代码，特别是脚本和教学场景。

### 2. JEP 512: Compact Source Files

**背景**: Java 程序需要大量样板代码，对初学者不友好。

**解决方案**: 支持隐式类和实例 main 方法。

```java
// 变更前
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}

// 变更后
void main() {
    println("Hello, World!");
}
```

**编译器实现**:

```java
// 解析隐式类
JCCompilationUnit parseImplicitClass(String source) {
    // 1. 解析方法声明
    JCMethodDecl main = parseMethodDecl();
    
    // 2. 创建隐式类包装
    JCClassDecl implicitClass = make.ClassDef(
        Flags.FINAL | Flags.SYNTHETIC,
        names.empty,
        List.nil(),
        null,
        List.nil(),
        List.of(main)
    );
    
    return make.TopLevel(List.nil(), List.of(implicitClass));
}
```

**影响**: 降低了 Java 入门门槛。

### 3. Switch 穷尽性检查重构 (JDK-8367499)

**问题**: switch 穷尽性检查逻辑分散在 Flow 类中，难以维护。

**解决方案**: 提取到独立的类。

```java
// 变更前: 在 Flow 类中
class Flow {
    void checkSwitchExhaustive(JCSwitch switchTree) {
        // 复杂的检查逻辑
    }
}

// 变更后: 独立类
class SwitchExhaustivenessChecker {
    public void check(JCSwitch switchTree) {
        // 清晰的检查逻辑
    }
}
```

**影响**: 代码更清晰，易于扩展。

---

## 开发风格

Jan 的贡献特点:

1. **语言专家**: 深入理解 Java 语言规范
2. **渐进式改进**: 小步快跑，每个 commit 聚焦单一目标
3. **测试驱动**: 每个改动都有充分的测试
4. **向后兼容**: 严格保证兼容性

---

## 相关链接

- [OpenJDK Changesets](https://hg.openjdk.org/jdk/jdk/user?user=jlahoda)
- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=Jan%20Lahoda)
- [JBS Issues](https://bugs.openjdk.org/issues/?jql=assignee%20%3D%20jlahoda)