# JDK 26 原始类型模式匹配深度分析

> **JEP**: 530 | **状态**: 第四次预览 | **Commit**: 99135d2e05b
> **作者**: Aggelos Biboudis | **Reviewer**: Jan Lahoda

---

## 目录

1. [特性概述](#特性概述)
2. [语言设计](#语言设计)
3. [编译器实现](#编译器实现)
4. [运行时支持](#运行时支持)
5. [字节码生成](#字节码生成)
6. [预览历史](#预览历史)

---

## 1. 特性概述

### 问题

JDK 26 之前，Java 模式匹配只支持引用类型：

```java
// 之前：需要包装类
Object obj = 42;
if (obj instanceof Integer i) {
    int value = i.intValue();  // 需要拆箱
}

// switch 不支持原始类型
switch (obj) {
    case Integer i -> process(i.intValue());
    case Double d -> process(d.doubleValue());
    // ...
}
```

### 解决方案

JEP 530 允许在模式匹配中直接使用原始类型：

```java
// 现在：直接使用原始类型
Object obj = 42;
if (obj instanceof int i) {
    process(i);  // 无需拆箱
}

// switch 支持
String result = switch (obj) {
    case int i -> "int: " + i;
    case long l -> "long: " + l;
    case float f -> "float: " + f;
    case double d -> "double: " + d;
    default -> "unknown";
};
```

---

## 2. 语言设计

### instanceof 模式匹配

```java
// 基本用法
if (obj instanceof int i) {
    System.out.println("int: " + i);
} else if (obj instanceof long l) {
    System.out.println("long: " + l);
} else if (obj instanceof double d) {
    System.out.println("double: " + d);
}
```

### switch 模式匹配

```java
// 完整 switch
Object value = getValue();
String result = switch (value) {
    case int i -> "int: " + i;
    case long l -> "long: " + l;
    case float f -> "float: " + f;
    case double d -> "double: " + d;
    case boolean b -> "boolean: " + b;
    case char c -> "char: " + c;
    case String s -> "String: " + s;
    default -> "unknown";
};
```

### 精确匹配与守卫

```java
// 精确类型匹配
switch (value) {
    case int i when i > 0 -> "positive int";
    case int i when i < 0 -> "negative int";
    case int i -> "zero";
    // ...
}
```

---

## 3. 编译器实现

### 核心文件列表

```
src/jdk.compiler/share/classes/com/sun/tools/javac/
├── code/
│   └── Types.java                    # 类型系统
├── comp/
│   ├── Attr.java                     # 属性检查
│   ├── Check.java                    # 类型检查
│   ├── Lower.java                    # 降级转换
│   ├── TransPatterns.java            # 模式转换
│   └── TypeHarness.java              # 类型工具
└── tree/
    ├── JCTree.java                   # 语法树
    └── TreeMaker.java                # 语法树构造
```

### 类型检查

```java
// Check.java - 类型检查实现
void checkPrimitivePattern(JCInstanceOf tree) {
    // 检查模式类型
    Type patternType = tree.pattern.type;

    // 验证是原始类型
    if (!patternType.isPrimitive()) {
        return;
    }

    // 获取包装类
    Type wrapper = types.boxedClass(patternType).type;

    // 检查可转换性
    if (!types.isConvertible(exprType, patternType)) {
        log.error(tree.pos(), "incompatible.types",
                  exprType, patternType);
    }
}
```

### 模式转换

```java
// TransPatterns.java - 模式降级
JCStatement translatePrimitivePattern(JCIf tree) {
    JCExpression expr = tree.expr;
    JCPrimitiveTypePattern pattern = (JCPrimitiveTypePattern) tree.pattern;

    // 生成等价代码
    // if (expr instanceof Integer && ((Integer)expr).intValue() == ((Integer)expr).intValue()) {
    //     int i = ((Integer)expr).intValue();
    //     // body
    // }

    // 1. 类型检查
    JCExpression typeCheck = make.TypeCheck(expr, boxedType);

    // 2. 值提取
    JCExpression cast = make.TypeCast(boxedType, expr);
    JCExpression unbox = make.Unbox(boxedType, cast);

    // 3. 模式变量声明
    JCVariableDecl varDecl = make.VarDef(pattern.var, unbox);

    // 组合
    return make.If(typeCheck, make.Block(0, List.of(varDecl, tree.thenpart)), null);
}
```

---

## 4. 运行时支持

### SwitchBootstraps

```java
// java.lang.runtime.SwitchBootstraps.java

/**
 * 为 switch 语句生成 invokedynamic 调用点的引导方法
 */
public final class SwitchBootstraps {

    /**
     * 类型 switch 的引导方法
     * 支持原始类型模式匹配
     */
    public static CallSite typeSwitch(
            MethodHandles.Lookup lookup,
            String invocationName,
            MethodType invocationType,
            Object... labels) throws Throwable {

        // labels 包含原始类型的 Class 对象
        // 例如: int.class, long.class, double.class

        // 生成类型检查和分发的 MethodHandle
        MethodHandle mh = generateTypeSwitch(labels);
        return new ConstantCallSite(mh);
    }

    private static MethodHandle generateTypeSwitch(Object[] labels) {
        // 为每个标签生成类型检查
        // 1. null 检查
        // 2. instanceof 检查
        // 3. 原始类型匹配

        return MethodHandles.guardWithTest(
            // 测试：是否为 null 或匹配类型
            typeTest,
            // 匹配：返回索引
            constant(index),
            // 不匹配：继续检查下一个
            nextCase
        );
    }
}
```

### 类型转换规则

```java
// Types.java - 类型转换实现

/**
 * 检查原始类型模式匹配的转换规则
 */
public boolean isConvertible(PrimitiveType from, Type to) {
    // 允许的转换：
    // 1. 相同类型
    // 2. 宽化原始转换 (byte -> short, int -> long, etc.)
    // 3. 拆箱转换 (Integer -> int)

    // 禁止的转换：
    // 1. 窄化原始转换 (需要显式转换)
    // 2. 不兼容的原始类型

    if (from.getTag() == to.getTag()) {
        return true;  // 相同类型
    }

    // 检查宽化转换
    return isWideningPrimitiveConversion(from.getTag(), to.getTag());
}

/**
 * 检查精确可转换性
 */
public boolean isExactConvertible(Type from, Type to) {
    // 精确转换要求：
    // 1. 运行时类型完全匹配
    // 2. 不需要额外检查

    if (from.isPrimitive() && to.isPrimitive()) {
        return from.getTag() == to.getTag();
    }

    return false;
}
```

---

## 5. 字节码生成

### instanceof 字节码

```java
// 源码
if (obj instanceof int i) {
    process(i);
}

// 等价字节码
ALOAD 1                  // 加载 obj
DUP                      // 复制
INSTANCEOF java/lang/Integer  // 类型检查
IFEQ L_not_match         // 如果不是 Integer，跳转
CHECKCAST java/lang/Integer  // 强制转换
INVOKEVIRTUAL java/lang/Integer.intValue ()I  // 拆箱
ISTORE 2                 // 存储到 i
// ... process(i) 的代码
GOTO L_end
L_not_match:
// ... else 分支
L_end:
```

### switch 字节码

```java
// 源码
switch (obj) {
    case int i -> processInt(i);
    case long l -> processLong(l);
    default -> processDefault();
}

// 等价字节码 (使用 invokedynamic)
ALOAD 1                  // 加载 obj
ICONST_0                 // restart index = 0
INVOKEDYNAMIC typeSwitch()I  // 引导方法
// 返回匹配的 case 索引
TABLESWITCH              // 分发到对应 case
// case 0: int
// case 1: long
// default: ...
```

### invokedynamic 优势

1. **延迟绑定**：运行时生成最优化的代码
2. **类型安全**：编译时验证类型
3. **性能优化**：可以缓存类型检查结果
4. **灵活性**：支持动态添加新的 case 类型

---

## 6. 预览历史

```
JEP 455  (JDK 23) - Primitive Types in Patterns (Preview)
JEP 456  (JDK 22) - Primitive Types in Patterns (Second Preview)
JEP 4xx  (JDK 25) - Primitive Types in Patterns (Third Preview)
JEP 530  (JDK 26) - Primitive Types in Patterns (Fourth Preview)
```

### JDK 26 变化

1. **类型推断改进**：更好的类型推断
2. **错误提示优化**：更清晰的错误信息
3. **性能优化**：字节码生成优化
4. **API 完善**：SwitchBootstraps API 完善

---

## 7. 类型匹配规则

### 允许的转换

```java
// 相同类型
if (obj instanceof int i) { }  // ✅

// 宽化原始转换
if (obj instanceof int i) { }  // Integer 可以匹配 int
if (obj instanceof long l) { } // Integer/int 可以匹配 long

// 包装类到原始类型
if (obj instanceof int i) { }  // Integer -> int ✅
```

### 禁止的转换

```java
// 窄化转换（需要显式）
if (obj instanceof byte b) { } // ❌ int 不能匹配 byte

// 不兼容类型
if (obj instanceof boolean b) { } // ❌ Integer 不能匹配 boolean
```

### Switch 顺序注意事项

```java
// ⚠️ 注意：更宽的类型在前会隐藏更窄的类型
switch (value) {
    case long l -> ...   // 匹配 int 和 long
    case int i -> ...    // 永远不会执行！
}

// ✅ 正确：更窄的类型在前
switch (value) {
    case int i -> ...
    case long l -> ...
}
```

---

## 8. 性能考虑

### 编译时优化

```java
// 常量折叠
if (obj instanceof int i) {
    // 编译器可以优化类型检查
}
```

### 运行时优化

```java
// 类型缓存
// invokedynamic 可以缓存类型检查结果
// 后续调用无需重复检查

// 内联优化
// 小型 switch 可以内联展开
```

---

## 9. 最佳实践

### 1. 使用原始类型模式

```java
// ✅ 推荐
if (obj instanceof int i) {
    process(i);
}

// ❌ 避免
if (obj instanceof Integer i) {
    process(i.intValue());
}
```

### 2. Switch 顺序

```java
// ✅ 推荐：从窄到宽
switch (value) {
    case byte b -> ...
    case short s -> ...
    case int i -> ...
    case long l -> ...
}

// ❌ 避免：从宽到窄
switch (value) {
    case long l -> ...  // 会吞掉所有 int
    case int i -> ...   // 永远不会执行
}
```

### 3. 使用守卫

```java
// ✅ 推荐：结合守卫条件
switch (value) {
    case int i when i > 0 -> "positive";
    case int i when i < 0 -> "negative";
    case int i -> "zero";
}
```

---

## 10. 总结

JEP 530 (第四次预览) 带来的原始类型模式匹配：

1. **语法简洁**：无需手动拆箱
2. **类型安全**：编译时类型检查
3. **性能优化**：减少装箱/拆箱开销
4. **完整支持**：instanceof 和 switch

---

## 11. 相关链接

- [JEP 530 官方文档](https://openjdk.org/jeps/530)
- [Commit: 99135d2e05b](https://github.com/openjdk/jdk/commit/99135d2e05b)
- [SwitchBootstraps Javadoc](https://docs.oracle.com/en/java/javase/26/docs/api/java.base/java/lang/runtime/SwitchBootstraps.html)
