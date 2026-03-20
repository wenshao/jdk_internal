# JIT 友好代码模式

> 编写能充分利用 JIT 编译器优化能力的代码模式

[← 返回 JIT 编译](../)

---

## 结论先行

| 模式 | 优化效果 | 难度 |
|------|----------|------|
| **方法内联友好** | +10-30% | 低 |
| **循环优化友好** | +20-50% | 低 |
| **避免逃逸** | 减少 GC | 中 |
| **常量折叠友好** | +5-15% | 低 |
| **多态优化** | +10-40% | 中 |

---

## 一眼看懂

### JIT 编译器优化的代码特征

```
JIT 喜欢的代码:
├── 小而热的方法 (易于内联)
├── 简单循环 (便于展开/向量化)
├── 类型稳定 (去虚拟化)
├── 无逃逸对象 (标量替换)
└── 可预测分支 (分支预测)

JIT 不喜欢的代码:
├── 巨大方法 (无法内联)
├── 复杂控制流 (难以优化)
├── 频繁类型切换 (去优化风险)
├── 对象逃逸 (无法标量替换)
└── 反射调用 (难以内联)
```

---

## 1. 方法内联友好设计

### 内联限制

```
C2 内联限制 (JDK 26):
├── MaxInlineSize: 35 字节码 (默认)
├── FreqInlineSize: 325 字节码 (热方法)
├── MaxInlineLevel: 9 层深度
└── 递归内联: 受限
```

### 推荐模式

#### ✅ 小方法

```java
// 推荐: 小方法易于内联
public int calculate(int x) {
    return x * 2 + 1;
}

// 优化后: 直接内联
result = x * 2 + 1;
```

#### ❌ 大方法

```java
// 不推荐: 大方法无法内联
public int complexCalculation(int x) {
    // 100+ 行代码...
    // C2 会放弃内联
}
```

### 实践建议

```java
// 将大方法拆解为小方法
public void processOrder(Order order) {
    validateOrder(order);      // 小方法，可内联
    calculatePrice(order);     // 小方法，可内联
    saveOrder(order);          // 小方法，可内联
}

// 而不是
public void processOrder(Order order) {
    // 50 行代码混合所有逻辑
}
```

---

## 2. 循环优化友好设计

### 推荐模式

#### ✅ 简单可计数循环

```java
// 推荐: 简单循环易于向量化
for (int i = 0; i < array.length; i++) {
    array[i] = array[i] * 2;
}

// C2 可能优化为 SIMD 向量操作
```

#### ❌ 复杂循环

```java
// 不推荐: 复杂循环难以优化
for (Iterator<Integer> it = list.iterator(); it.hasNext(); ) {
    if (someCondition) {
        break;
    }
    Integer value = it.next();
    // ...
}
```

### 循环边界优化

```java
// 推荐: 边界明确
for (int i = 0; i < 1000; i++) {
    // C2 可以完全展开
}

// 避免: 边界不明确
for (int i = 0; i < calculateLimit(); i++) {
    // C2 难以优化
}
```

### 循环不变代码外提

```java
// 推荐: 循环不变量移出
int limit = data.length;
for (int i = 0; i < limit; i++) {
    process(data[i], constant);
}

// 虽然 C2 会尝试外提，但显式写法更可靠
```

---

## 3. 避免对象逃逸

### 标量替换条件

```
C2 标量替换条件:
├── 对象不逃逸方法
├── 对象不存储到堆
├── 对象不传递给其他方法
└── 对象是可分析的 (简单结构)
```

### 推荐模式

#### ✅ 栈上分配

```java
// 推荐: 临时对象不逃逸
public int calculate(Point p1, Point p2) {
    int dx = p1.x - p2.x;
    int dy = p1.y - p2.y;
    return dx * dx + dy * dy;
}

// C2 可能完全消除 Point 对象分配
```

#### ❌ 对象逃逸

```java
// 不推荐: 对象逃逸
public List<Point> calculate() {
    List<Point> result = new ArrayList<>();
    for (int i = 0; i < 1000; i++) {
        result.add(new Point(i, i * 2));  // 必须分配
    }
    return result;
}
```

### StringBuilder 优化

```java
// 推荐: 连接操作保持在方法内
public String process(String[] inputs) {
    StringBuilder sb = new StringBuilder();
    for (String s : inputs) {
        sb.append(s);
    }
    return sb.toString();
}

// C2 JDK 21+ 可以优化为栈上分配
```

---

## 4. 类型稳定与去虚拟化

### 推荐模式

#### ✅ 单态调用

```java
// 推荐: 类型稳定
List<String> list = new ArrayList<>();
for (int i = 0; i < 1000; i++) {
    list.add("item");
}

// C2 可以去虚拟化 List.add 调用
```

#### ❌ 多态切换

```java
// 不推荐: 类型频繁切换
List<String> list;
if (condition) {
    list = new ArrayList<>();
} else {
    list = new LinkedList<>();
}
// C2 无法去虚拟化
```

### Final 类型

```java
// 推荐: 使用 final 类 (Java 17+ sealed 也可)
public final class Point {
    public final int x;
    public final int y;
}

// C2 可以更好地优化 final 类
```

---

## 5. 常量折叠友好

### 推荐模式

#### ✅ 编译时常量

```java
// 推荐: 使用 final
private static final int MULTIPLIER = 10;

public int calculate(int x) {
    return x * MULTIPLIER;  // 可折叠为 x * 10
}
```

#### ❌ 运行时常量

```java
// 不推荐
private int multiplier = 10;

public int calculate(int x) {
    return x * multiplier;  // 无法折叠
}
```

### 条件消除

```java
// 推荐: 使用 final boolean
private static final boolean DEBUG = false;

public void log(String message) {
    if (DEBUG) {  // C2 会完全消除这段代码
        System.out.println(message);
    }
}
```

---

## 6. 避免 Deoptimization

### Deoptimization 触发条件

```
常见触发原因:
├── 类型假设失效
├── 类层次结构变化
├── 分支预测失败
└── 优化假设不成立
```

### 推荐模式

#### ✅ 类型一致

```java
// 推荐: 保持类型一致
List<String> list = new ArrayList<>();
// 始终使用 ArrayList，不切换类型
```

#### ❌ 类型切换

```java
// 不推荐: 运行时切换类型
List<?> list = new ArrayList<>();
if (condition) {
    list = new LinkedList<>();
}
// 触发 deoptimization
```

---

## 7. 反射优化

### 推荐模式

#### ✅ MethodHandle (Java 7+)

```java
// 推荐: MethodHandle 更易内联
MethodHandle mh = lookup.findVirtual(MyClass.class, "method",
    MethodType.methodType(void.class));
mh.invokeExact(obj);
```

#### ❌ 反射调用

```java
// 不推荐: 反射难以内联
Method m = obj.getClass().getMethod("method");
m.invoke(obj);
```

### 变长参数优化

```java
// 推荐: 避免反射变长参数
// 反射变长参数会创建数组，影响性能
```

---

## 8. 异常处理优化

### 推荐模式

#### ✅ 避免热路径异常

```java
// 推荐: 预先检查
public void process(String input) {
    if (input == null) {
        throw new IllegalArgumentException();
    }
    // 正常处理
}
```

#### ❌ 热路径异常

```java
// 不推荐: 依赖异常处理
try {
    process(input);
} catch (NullPointerException e) {
    // 恢复逻辑
}
// NPE 会影响 JIT 优化
```

---

## 9. 数组与集合优化

### 数组边界检查消除

```java
// 推荐: 简单循环
for (int i = 0; i < array.length; i++) {
    array[i] *= 2;
}

// C2 可以证明 i 始终在范围内
// 消除所有边界检查
```

### 集合大小初始化

```java
// 推荐: 预设大小
List<String> list = new ArrayList<>(1000);

// 避免: 频繁扩容
List<String> list = new ArrayList<>();
// 扩容会触发数组复制和对象分配
```

---

## 10. 并行流优化

### 推荐模式

#### ✅ 大数据集

```java
// 推荐: 大数据集使用并行流
largeList.parallelStream()
    .map(x -> process(x))
    .collect(toList());
```

#### ❌ 小数据集

```java
// 不推荐: 小数据集
smallList.parallelStream()
    .map(x -> process(x))
    .collect(toList());
// 并行开销 > 收益
```

### 无状态操作

```java
// 推荐: 无状态 lambda
list.parallelStream()
    .map(x -> x * 2)  // 无状态，可并行
    .collect(toList());

// 避免: 有状态操作
list.parallelStream()
    .map(x -> {
        sharedState.update(x);  // 有状态，需要同步
        return x * 2;
    });
```

---

## 实战案例

### 案例 1: 字符串处理优化

#### 优化前

```java
public String process(String[] inputs) {
    String result = "";
    for (String s : inputs) {
        result += s;  // 每次创建新 String
    }
    return result;
}
```

#### 优化后

```java
public String process(String[] inputs) {
    StringBuilder sb = new StringBuilder(inputs.length * 16);
    for (String s : inputs) {
        sb.append(s);
    }
    return sb.toString();
}

// 性能提升: 5-10x
```

### 案例 2: 循环向量化

#### 优化前

```java
public void multiply(int[] a, int[] b, int[] c) {
    for (int i = 0; i < a.length; i++) {
        c[i] = a[i] * b[i];
    }
}
```

#### C2 可能优化为

```java
// SIMD 向量化 (如果硬件支持)
for (int i = 0; i < a.length; i += 4) {
    __m128i va = _mm_loadu_si128(&a[i]);
    __m128i vb = _mm_loadu_si128(&b[i]);
    __m128i vc = _mm_mullo_epi32(va, vb);
    _mm_storeu_si128(&c[i], vc);
}

// 性能提升: 2-4x
```

### 案例 3: 逃逸分析优化

#### 优化前

```java
class Point {
    int x, y;
}

public int distance(int x1, int y1, int x2, int y2) {
    Point p1 = new Point(x1, y1);  // 可能逃逸
    Point p2 = new Point(x2, y2);  // 可能逃逸
    return Math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2);
}
```

#### 优化后

```java
// C2 标量替换
public int distance(int x1, int y1, int x2, int y2) {
    int p1$x = x1;  // 标量
    int p1$y = y1;
    int p2$x = x2;
    int p2$y = y2;
    int dx = p1$x - p2$x;
    int dy = p1$y - p2$y;
    return Math.sqrt(dx * dx + dy * dy);
}

// 无对象分配，无 GC 压力
```

---

## 诊断工具

### 检查内联

```bash
# 查看内联决策
-XX:+PrintInlining

# 检查特定方法
-XX:CompileCommand=print,*Class.method
```

### 检查逃逸分析

```bash
# 查看逃逸分析结果
-XX:+PrintEliminateAllocations
-XX:+PrintEscapeAnalysis
```

### 检查循环优化

```bash
# 查看循环向量化
-XX:+PrintVectorization
-XX:+Verbose
```

---

## 常见陷阱

### 陷阱 1: 过早优化

```java
// 不推荐: 微优化牺牲可读性
int result = ((x << 3) + (x << 1));  // x * 10

// 推荐: 让 JIT 处理
int result = x * 10;  // C2 会自动优化
```

### 陷阱 2: 忽略预热

```java
// 错误: 冷启动测量性能
for (int i = 0; i < 1000; i++) {
    long start = System.nanoTime();
    method();
    long time = System.nanoTime() - start;
}

// 正确: 预热后测量
for (int i = 0; i < 10000; i++) { method(); }  // 预热
for (int i = 0; i < 1000; i++) {
    long start = System.nanoTime();
    method();
    long time = System.nanoTime() - start;
}
```

### 陷阱 3: 忽略编译阈值

```java
// C2 编译阈值 (默认):
// - Tier4CompileThreshold: 10000 次调用
// 确保 JMH 测试运行足够次数
```

---

## 总结

### JIT 友好代码特征

| 特征 | 说明 | 效果 |
|------|------|------|
| **小方法** | 易于内联 | +10-30% |
| **简单循环** | 便于向量化 | +20-50% |
| **类型稳定** | 去虚拟化 | +10-20% |
| **无逃逸** | 标量替换 | 减少 GC |
| **常量友好** | 常量折叠 | +5-15% |

### 最佳实践

```
1. 保持方法小而专注
2. 使用简单循环结构
3. 避免对象逃逸
4. 保持类型稳定
5. 使用 final 常量
6. 避免 deoptimization
7. 减少反射调用
8. 合理使用集合
9. 预热后再测量
10. 让编译器做优化
```

---

## 相关链接

### 本地文档

- [内联优化详解](inlining.md) - 内联策略和阈值
- [循环优化详解](loop-optimizations.md) - 循环优化技术
- [逃逸分析详解](escape-analysis.md) - 标量替换条件
- [诊断工具](diagnostics.md) - 如何诊断 JIT 问题

### 外部资源

- [Java Performance Tuning Guide](https://docs.oracle.com/javase/8/docs/technotes/guides/performance/)
- [JMH Benchmark Patterns](https://openjdk.org/projects/code-tools/jmh/)

---

**最后更新**: 2026-03-21
