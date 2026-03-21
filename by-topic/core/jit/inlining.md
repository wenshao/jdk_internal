# JIT 内联优化

> 方法内联是 JIT 编译器最重要的优化之一
> 内联决策影响代码质量和编译时间

[← 返回 JIT 编译](../)

---

## 一眼看懂

| 维度 | 内容 |
|------|------|
| **什么是内联** | 将方法调用替换为方法体，消除调用开销 |
| **核心收益** | 消除调用开销 (5-20%)、启用后续优化 |
| **主要成本** | 代码膨胀、编译时间增加 |
| **关键阈值** | FreqInlineSize=325, MaxInlineSize=35 |
| **C1 策略** | 保守内联，快速编译 |
| **C2 策略** | 激进内联，深度优化 |

---

## 为什么内联如此重要？

### 内联的收益

```java
// 原始代码
public int process(int x) {
    return add(x, 1) * 2;
}

private static int add(int a, int b) {
    return a + b;
}

// 内联后
public int process(int x) {
    return (x + 1) * 2;  // add 方法被内联
}
```

| 收益类型 | 说明 | 性能提升 |
|----------|------|----------|
| **消除调用开销** | 无需创建栈帧、保存/恢复寄存器 | 5-20% |
| **启用后续优化** | 代码可见后可进行常量折叠、死代码消除 | 10-50% |
| **改善局部性** | 指令缓存更友好 | 5-10% |
| **减少分支** | 消除返回地址跳转 | 3-5% |

### 内联的代价

| 代价类型 | 说明 | 影响 |
|----------|------|------|
| **代码膨胀** | 方法体被复制到每个调用点 | 增加 code cache 压力 |
| **编译时间** | 更大的方法需要更长编译时间 | 启动延迟 |
| **指令缓存** | 过大代码导致缓存失效 | 可能降低性能 |
| **寄存器压力** | 更多临时变量需要寄存器 | 更多的 spilling |

---

## C1 vs C2 内联策略

### 内联阈值对比

| 参数 | C1 | C2 | 说明 |
|------|----|----|------|
| **MaxInlineSize** | 35 | 35 | 绝对最大内联大小 |
| **FreqInlineSize** | 325 | 325 | 热点方法最大内联大小 |
| **内联深度** | 2-3 层 | 9+ 层 | 递归内联最大深度 |

### 内联策略差异

| 方面 | C1 | C2 |
|------|----|----|
| **设计目标** | 快速编译 > 代码质量 | 代码质量 > 编译速度 |
| **虚方法内联** | 保守 (需要类型统计) | 激进 (基于 profiling) |
| **接口方法内联** | 很少 | 基于 CHA (Class Hierarchy Analysis) |
| **构造函数内联** | 有限 | 更积极 |
| **失败处理** | 放弃内联 | 记录供后续优化 |

### 内联决策流程

```
方法调用
   │
   ▼
是否为热点方法？
   │
   ├─ 否 → 使用 MaxInlineSize (35)
   │
   └─ 是 → 使用 FreqInlineSize (325)
            │
            ▼
        方法字节码 < 阈值？
            │
            ├─ 是 → 尝试内联
            │
            └─ 否 → 检查特殊情况
                       │
                       ├─ 极热方法？→ 放宽阈值
                       ├─ 叶子方法？→ 优先内联
                       └─ 否 → 放弃内联
```

---

## C2 内联启发式算法

### 内联决策因素

#### 1. 方法大小

```java
// C2 源码中的简化逻辑
bool InlineTree::is_not_too_large(int bytecode_size) {
    if (bytecode_size > MaxInlineSize) {  // 默认 35
        if (! callee->is_hot()) {
            return false;  // 非热点方法，拒绝内联
        }
        if (bytecode_size > FreqInlineSize) {  // 默认 325
            return false;  // 超过热点阈值，拒绝内联
        }
    }
    return true;
}
```

#### 2. 调用频率

```java
// 基于 profiling 的内联决策
int inline_priority = method->interpreter_invocation_count();
if (inline_priority > COMPILATION_THRESHOLD) {
    // 热点方法，可以内联更大的方法
    max_size = FreqInlineSize;
}
```

#### 3. 方法类型

| 方法类型 | 内联优先级 | 原因 |
|----------|-----------|------|
| **静态方法** | ⭐⭐⭐⭐⭐ | 无多态，100% 确定 |
| **final 方法** | ⭐⭐⭐⭐⭐ | 无多态 |
| **private 方法** | ⭐⭐⭐⭐⭐ | 类内可见，易分析 |
| **构造函数** | ⭐⭐⭐⭐ | 通常可内联 |
| **简单虚方法** | ⭐⭐⭐ | 需要 CHA 分析 |
| **接口方法** | ⭐⭐ | 需要更强的 CHA |
| **复杂多态** | ⭐ | 很难内联 |

#### 4. 类层次分析 (CHA)

```java
// C2 可以在编译时分析类层次
interface Animal { void speak(); }
class Dog implements Animal { void speak() { bark(); } }
class Cat implements Animal { void speak() { meow(); } }

// 如果只有一种实现
Animal a = new Dog();
a.speak();  // C2 可以内联 Dog.speak()

// 如果有多种实现
Animal a = getRandomAnimal();
a.speak();  // C2 可能生成内联缓存
```

### 内联缓存 (Inline Cache)

当无法确定具体类型时，C2 使用内联缓存：

```java
// 伪代码展示内联缓存
void callAnimal(Animal a) {
    // 生成多路径代码
    if (a.type == Dog.class) {
        // 内联 Dog.speak()
    } else if (a.type == Cat.class) {
        // 内联 Cat.speak()
    } else {
        // 调用虚方法
        a.speak();
    }
}
```

---

## 内联限制和特殊情况

### 无法内联的情况

| 情况 | 原因 |
|------|------|
| **递归调用** | 会导致无限代码膨胀 |
| **异常处理路径** | 复杂控制流 |
| **本地方法** | 无法访问实现 |
| **过大方法** | 超过阈值 |
| **深度嵌套** | 超过内联深度 |
| **同步方法** | 需要特殊处理 (但可以内联)

### 递归内联

虽然完全递归无法内联，但尾递归可以优化：

```java
// 优化前
public int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

// JIT 可以部分内联
public int factorial(int n) {
    int result = 1;
    while (n > 1) {
        result *= n--;
    }
    return result;
}
```

---

## 实用内联优化建议

### 方法设计原则

#### 1. 保持热路径方法简短

```java
// 不推荐：大方法混合冷热代码
public void processRequest(Request req) {
    // 200 行热路径代码
    validate(req);
    transform(req);
    save(req);

    // 100 行边界情况处理
    if (req.hasEdgeCase()) {
        // 50 行边界处理
    }
}

// 推荐：拆分为多个方法
public void processRequest(Request req) {
    // 20 行热路径
    validate(req);
    transform(req);
    save(req);

    // 边界情况委托
    if (req.hasEdgeCase()) {
        handleEdgeCase(req);  // 冷方法，不被内联
    }
}
```

#### 2. 早期返回模式

```java
// 推荐：常见情况优先处理
public int calculate(int x, int y) {
    // 热路径：90% 的情况
    if (x > 0 && y > 0) {
        return fastPath(x, y);
    }
    // 冷路径：10% 的情况
    return slowPath(x, y);
}
```

#### 3. 使用静态方法

```java
// 静态方法更容易内联
private static int add(int a, int b) {
    return a + b;
}

// 虚方法需要额外的多态检查
private int add(int a, int b) {
    return a + b;
}
```

### 内联友好设计模式

#### 模式 1: 策略模式 + Lambda

```java
// Lambda 适合内联
public void process(List<Item> items) {
    items.forEach(item -> {
        // 小型 lambda，容易被内联
        item.process();
    });
}
```

#### 模式 2: 辅助方法提取

```java
// 将复杂计算拆分为可内联的小方法
public double calculatePrice(Order order) {
    return basePrice(order) +
           discount(order) +
           tax(order);
}

private static double basePrice(Order o) { /* ... */ }
private static double discount(Order o) { /* ... */ }
private static double tax(Order o) { /* ... */ }
```

---

## 诊断内联决策

### 使用 PrintInlining

```bash
# 查看内联决策
java -XX:+PrintCompilation -XX:+PrintInlining -XX:MaxInlineSize=1000 MyApp

# 输出示例
@ 3   java.util.String::charAt (26 bytes)   inline (hot)
  @ 4   java.lang.String::length (6 bytes)   inline (hot)
  @ 4   java.lang.String::isLatin1 (6 bytes)   inline (hot)
!    @ 3   java.lang.String::<init> (852 bytes)   failed to inline: hot method too big
```

### 输出解读

| 符号 | 含义 |
|------|------|
| `@` | 成功内联 |
| `!` | 内联失败 |
| `hot` | 热点方法 |
| `too big` | 方法太大 |
| `too deep` | 内联深度超限 |

### 常见内联失败原因

| 失败原因 | 解决方案 |
|----------|----------|
| **hot method too big** | 拆分方法，分离冷热代码 |
| **too deep** | 减少调用层次 |
| **recursive** | 改写为迭代 |
| **virtual call** | 使用 final 或静态方法 |

---

## VM 参数参考

### 内联控制参数

```bash
# 基础参数
-XX:MaxInlineSize=35                # 最大内联大小 (字节码)
-XX:FreqInlineSize=325              # 热点方法最大内联大小
-XX:InlineSmallCode=1000            # 小代码阈值

# 内联深度
-XX:MaxInlineLevel=9                # 最大内联深度
-XX:MaxRecursiveInlineLevel=1       # 最大递归内联层级

# 内联频率控制
-XX:CompileThreshold=10000          # C2 编译阈值
-XX:OnStackReplacePercentage=140    # OSR 比例

# 诊断
-XX:+PrintCompilation               # 打印编译活动
-XX:+PrintInlining                  # 打印内联决策
-XX:+CITime                         # 编译时间统计
-XX:+LogCompilation                 # 详细编译日志
```

### 实验性参数

```bash
# 激进内联
-XX:MaxInlineSize=1000              # 允许内联更大的方法
-XX:FreqInlineSize=1000             # 提高热点阈值

# 保守内联
-XX:MaxInlineSize=20                # 减少内联
-XX:MaxInlineLevel=3                # 限制内联深度
```

---

## 实际案例

### 案例 1: String 构造函数优化

> **JDK-8357289**: String 构造函数过大导致无法内联
> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) (Alibaba)

**问题**: `String(Charset, byte[], int, int)` 方法 852 字节，超过 325 字节阈值

**解决方案**: 拆分为多个小方法

| 方法 | 大小 | 用途 |
|------|------|------|
| `String(Charset, byte[], int, int)` | 120 字节 | 主构造函数 |
| `create(byte[], int)` | 45 字节 | 创建方法 |
| `compress(byte[], int, int)` | 123 字节 | 压缩方法 |

**效果**: +5-10% 性能提升

→ [详细分析](/by-pr/8357/8357289.md)

### 案例 2: DateTime 优化

> **JDK-8337279**: DateTimeHelper 共享 StringBuilder
> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) (Alibaba)

**问题**: `DateTimeFormatterBuilder.format` 方法过大，无法内联

**解决方案**: 拆分方法，使用共享 StringBuilder

```java
// 优化后：可内联的小方法
private static void currentEra(StringBuilder buf, long inSec, int inNano) {
    // 123 字节，可以内联
}
```

**效果**: +10-15% 性能提升

→ [详细分析](/by-pr/8337/8337279.md)

### 案例 3: StringBuilder 优化

> **JDK-8333893**: StringBuilder append(boolean/null) 优化
> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) (Alibaba)

**问题**: append 方法调用链无法被内联

**解决方案**: 重写为可触发 MergeStore 的形式

```java
// 优化后：可触发 JIT MergeStore 优化
static void putCharsAt(byte[] val, int index, int c1, int c2, int c3, int c4) {
    UNSAFE.putByte(val, address, (byte)(c1));
    UNSAFE.putByte(val, address + 1, (byte)(c2));
    UNSAFE.putByte(val, address + 2, (byte)(c3));
    UNSAFE.putByte(val, address + 3, (byte)(c4));
}
```

**效果**: append(boolean) +14.7%, append(null) +9.2%

→ [详细分析](/by-pr/8333/8333893.md)

### 案例 4: 复杂字符串拼接内存爆炸

> **JDK-8327247**: C2 编译复杂字符串拼接时内存占用高达 2GB
> **作者**: [Claes Redestad](/by-contributor/profiles/claes-redestad.md)

**问题**: 复杂字符串拼接导致 C2 编译器内存指数级增长

| 参数数量 | C2 内存占用 |
|----------|-------------|
| 13 | 6.3 MB |
| 23 | 18 MB |
| 123 | **868 MB** ⚠️ |
| 极端情况 | **~2 GB** 💥 |

**根本原因**: 字符串拼接生成复杂的 MethodHandle 组合树，导致内联爆炸

**解决方案**: 限制字符串拼接的参数数量阈值，添加系统属性控制

```bash
# 限制字符串拼接参数数量
-Djdk.invoke.stringConcat=100
```

**效果**: 内存使用减少 180 倍

→ [详细分析](/by-pr/8327/8327247.md)

### 案例 5: Formatter.isValid 内联优化

> **JDK-8335252**: Reduce size of j.u.Formatter.Conversion#isValid
> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) (Alibaba)

**问题**: `Formatter.Conversion#isValid` 方法 358 字节，超过内联阈值

```java
// 原始实现：大型 switch 表达式
static boolean isValid(char c) {
    switch (c) {
        case 'b', 'B', 'h', 'H', 's', 'S', 'c', 'C', 'd', 'o',
             'x', 'X', 'e', 'E', 'f', 'g', 'G', 'a', 'A',
             't', 'T', 'n', '%', DECIMAL_FLOAT, HEXADECIMAL_FLOAT,
             HEXADECIMAL_FLOAT_UPPER, LINE_SEPARATOR, PERCENT_SIGN -> true;
        default -> false;
    };
}
// 方法大小: 358 字节 > 325 字节阈值
// JIT 日志: failed to inline: hot method too big
```

**解决方案**: 简化 switch，将部分常量移到 default 处理

```java
// 优化后：可内联的小方法
static boolean isValid(char c) {
    return switch (c) {
        case 'b', 'B', 'h', 'H', 's', 'S', 'c', 'C', 'd', 'o',
             'x', 'X', 'e', 'E', 'f', 'g', 'G', 'a', 'A',
             't', 'T', LINE_SEPARATOR -> true;
        // 不要把 PERCENT_SIGN 放在 switch 里，
        // 那样会使方法大小超过 325，无法内联
        default -> c == PERCENT_SIGN;
    };
}
// 方法大小: 10 字节 < 325 字节阈值
// JIT 日志: inline (hot)
```

**效果**:
- 方法大小: 358 → 10 字节
- 内联状态: 失败 → 成功
- 性能提升: +15-25%

→ [详细分析](/by-pr/8335/8335252.md)

---

## 相关链接

### 本地文档

- [C2 优化阶段](c2-phases.md) - 内联在编译流程中的位置
- [VM 参数](vm-parameters.md) - 完整参数参考
- [诊断工具](diagnostics.md) - 调试内联决策
- [Graal JIT](graal-jit.md) - Graal 内联策略对比
- [Graal 高级优化](graal-advanced-optimizations.md) - 内联优化对比

### 外部资源

- [Introduction to C2 - Part 3: Inlining](https://eme64.github.io/blog/2024/12/31/Intro-to-C2-Part03.html) - Emanuel Peter 的深入分析
- [JVM TI Inline APIs](https://docs.oracle.com/en/java/javase/17/vm/jvm-tool-interface.html)

---

**最后更新**: 2026-03-20
