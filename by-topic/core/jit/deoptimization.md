# 去优化 (Deoptimization) 详解

> 为什么 JIT 编译的代码会回退到解释执行？

[← 返回 JIT 编译](../)

---

## 结论先行

| 问题 | 答案 |
|------|------|
| **什么是去优化？** | JIT 编译的代码因假设失效，回退到解释执行 |
| **为什么需要？** | 允许编译器做激进优化，假设失败时可以回退 |
| **性能影响？** | 首次去优化有开销，后续重新编译可能更快 |
| **如何避免？** | 保持类型稳定、避免假设失效、预热充分 |

---

## 一眼看懂

### 去优化的本质

```
JIT 编译器做优化时基于假设:
├── 类型假设: 这个变量永远是 String
├── 假设单态: 这个方法永远只调用一个实现
├── 假设常量: 这个值永远不会变
└── 假设边界: 循环次数总是 1000

如果假设正确 → 优化生效 → 极致性能
如果假设失效 → 去优化触发 → 回退解释 → 重新分析
```

### 去优化流程

```
优化代码执行
    │
    ↓
检查假设 (Safepoint/分支)
    │
    ├─ 假设有效 → 继续执行
    │
    └─ 假设失效 → 去优化
            │
            ↓
    保存当前状态到解释帧
            │
            ↓
    跳转到解释器
            │
            ↓
    记录去优化原因
            │
            ↓
    可能重新编译 (基于新信息)
```

---

## 去优化的类型

### 1. 类型不精确 (Type Speculation Failed)

```java
// 编译器假设 obj 是 ArrayList
List<String> list = (List<String>) obj;
list.add("item");

// 运行时 obj 变成了 LinkedList
// → 去优化触发
```

### 2. 类层级变化 (Hierarchy Change)

```java
// 编译时只有一个子类
interface Animal { void speak(); }
class Dog implements Animal { void speak() { woof(); } }

// 运行时添加了新的子类
class Cat implements Animal { void speak() { meow(); } }

// → 去优化触发 (去虚拟化失效)
```

### 3. 分支预测失败 (Branch Prediction Failed)

```java
// 编译器优化: 假设 condition 总是 false
if (condition) {
    // 这个分支被优化掉
}

// 运行时 condition 变成 true
// → 去优化触发
```

### 4. 方法重定义 (Method Redefined)

```java
// 使用 JVMTI 重新定义方法
// → 所有依赖此方法的编译代码失效
// → 去优化触发
```

### 5. 优化假设失效 (Optimization Assumption Failed)

```java
// 基于循环计数优化
for (int i = 0; i < 1000; i++) {  // 编译时确定
    // 展开为 1000 次直接操作
}

// 运行时边界变了
// → 去优化触发
```

### 6. 延迟优化失效 (Lazy Optimization Failed)

```java
// 编译器延迟某个操作
// 运行时发现无法延迟
// → 去优化触发
```

### 7. 断言失败 (Assertion Failed)

```java
// 编译器插入的断言检查失败
// → 去优化触发
```

### 8. 约束失效 (Constraint Failed)

```java
// 编译器基于的约束条件不再满足
// → 去优化触发
```

### 9. 转换失败 (Conversion Failed)

```java
// 类型转换优化假设失效
// → 去优化触发
```

### 10. 其他原因

- 字段访问假设失效
- 数组长度假设失效
- 空检查优化失效

---

## 查看去优化

### 启用去优化日志

```bash
# 查看去优化事件
-XX:+PrintDeoptimizationDetails

# 查看编译和去优化统计
-XX:+PrintCompilation
-XX:+LogCompilation

# 完整日志
-XX:+UnlockDiagnosticVMOptions
-XX:+PrintDeoptimizationDetails
-XX:LogCompilation=file.xml
-XX:CompileCommand=print,*Class.method
```

### 去优化日志解读

```
# 示例输出
<deoptimization thread='main' id='1' reason='null_check' action='reinterpret'>
  <bytecodes>
    invokevirtual java/lang/String.charAt (I)C
    invokestatic java/lang/String.checkBoundsBeginEnd (II)V
  </bytecodes>
  <action reason='null_check'>
    <jvms bci='4' method='java/lang/String.charAt (I)C'/>
  </action>
  <pc>0x00007f1234567890</pc>
</deoptimization>
```

**字段说明**:
- `reason`: 去优化原因
- `action`: 处理方式
- `bytecodes`: 触发的字节码
- `pc`: 发生位置

### JFR 监控

```bash
# 使用 JFR 记录去优化
jfr record --name=deopt \
    --jdk.DeoptimizationReplay=true \
    --settings=profile \
    duration=60s \
    filename=deopt.jfr

# 分析
jfr print --events jdk.Deoptimization* deopt.jfr
```

---

## 去优化级别

### 动作类型 (Action)

| Action | 说明 | 影响 |
|--------|------|------|
| **reinterpret** | 重新解释 | 轻微，继续执行 |
| **make_not_entrant** | 禁止进入 | 中等，不再进入此代码 |
| **make_not_compilable** | 禁止编译 | 严重，不再编译此方法 |

### Action 详解

#### 1. Reinterpret (重新解释)

```java
// 最轻量的去优化
// 仅调整执行状态，不丢弃编译代码
// 下次进入可能继续使用
```

#### 2. Make Not Entrant (禁止进入)

```java
// 标记代码为"不可进入"
// 当前执行完此代码后，不再使用
// 解释器接管
// 可能触发重新编译
```

#### 3. Make Not Compilable (禁止编译)

```java
// 放弃优化此方法
// 解释器永久执行
// 极少发生，除非方法有问题
```

---

## 避免频繁去优化

### 1. 保持类型稳定

```java
// ✅ 推荐: 单态使用
List<String> list = new ArrayList<>();
// 始终使用 ArrayList

// ❌ 避免: 运行时切换类型
List<?> list = new ArrayList<>();
if (condition) {
    list = new LinkedList();  // 触发去优化
}
```

### 2. 充分预热

```java
// ✅ 推荐: 预热后再测量
for (int i = 0; i < 10000; i++) {
    method();  // 预热
}
// 现在测量性能

// ❌ 避免: 冷启动测量
method();  // 可能在去优化
measure();
```

### 3. 避免动态类型切换

```java
// ❌ 避免
Object obj = getString();
if (obj instanceof String) {
    // 第一次编译时假设是 String
} else if (obj instanceof Integer) {
    // 类型变化，去优化
}

// ✅ 推荐: 重载方法
processString(String s);
processInteger(Integer i);
```

### 4. 稳定的多态

```java
// ✅ 推荐: 有限的多态 (2-4 个实现)
interface Shape { double area(); }
class Circle implements Shape { ... }
class Rectangle implements Shape { ... }
// C2 可以处理这种多态

// ❌ 避免: 过多的实现
// 100+ 个实现 → 无法优化 → 去优化
```

### 5. 避免条件假设失效

```java
// ✅ 推荐: 使用 final
private static final int LIMIT = 1000;
for (int i = 0; i < LIMIT; i++) { ... }

// ❌ 避免: 动态边界
for (int i = 0; i < calculateLimit(); i++) { ... }
```

---

## 去优化与重新编译

### 重新编译触发条件

```
去优化后:
├── 少量去优化 → 继续使用编译代码
├── 中等去优化 → 标记 not_entrant → 重新编译
└── 频繁去优化 → 放弃优化 → 解释执行
```

### 重新编译策略

```java
// 第一次编译 (C2)
// 假设: obj 是 ArrayList
// 去优化: obj 变成 LinkedList
//
// 第二次编译 (C2)
// 假设: obj 可能是 ArrayList 或 LinkedList
// 生成: 检查类型，分派到不同代码
//
// 如果继续去优化:
// 第三次编译 (C2)
// 生成: 更保守的代码 (虚方法调用)
```

### 去优化阈值

```bash
# 去优化相关参数
-XX:CompileThreshold=10000         # 编译阈值
-XX:PerMethodRecompilationCutoff=400  # 每个方法重新编译次数限制
-XX:PerBytecodeRecompilationCutoff=100 # 每个字节码重新编译限制
```

---

## 实战案例分析

### 案例 1: 类型不稳定

```java
public class TypeInstability {
    private Object data;

    public void process() {
        if (data instanceof String) {
            // 第一次编译: 假设 data 是 String
            String s = (String) data;
            s.length();
        } else {
            // data 类型变化 → 去优化
        }
    }

    public void setData(Object data) {
        this.data = data;  // 运行时类型变化
    }
}
```

**去优化日志**:
```
<deoptimization reason='type_check' action='make_not_entrant'>
```

**解决方案**:
```java
// 使用泛型保持类型稳定
public class TypeStability<T> {
    private T data;
    // ...
}
```

### 案例 2: 继承层级变化

```java
interface Animal { void speak(); }
class Dog implements Animal {
    public void speak() { System.out.println("woof"); }
}

public class Main {
    public static void main(String[] args) {
        Animal a = new Dog();
        // 编译: 去虚拟化 Dog.speak

        // 运行时: 动态加载新类
        loadClass("class Cat implements Animal { ... }");
        a.speak();  // 去优化！
    }
}
```

### 案例 3: 分支预测失败

```java
public class BranchPrediction {
    private boolean initialized = false;

    public void init() {
        // 第一次编译: initialized 总是 false
        if (initialized) {
            // 分支被优化掉
        }
        initialized = true;
    }

    public void run() {
        if (initialized) {
            // 优化后的代码中没有这个检查
            // 去优化！
        }
    }
}
```

---

## 去优化统计

### 查看统计

```bash
# 使用 jstat
jstat -compiler <pid>
# 输出包含:
# LastDeoptTime: 上次去优化时间
# DeoptMethod: 去优化的方法
# DeoptRatio: 去优化比率

# 使用 JFR
jfr print --events jdk.DeoptimizationReplay replay.jfr
```

### 去优化率

```
健康的去优化率: < 1%
需要关注: 1-5%
有问题: > 5%
```

---

## 调试去优化

### 1. 定位去优化方法

```bash
# 启用详细日志
-XX:+PrintDeoptimizationDetails
-XX:+UnlockDiagnosticVMOptions

# 查看特定方法
-XX:CompileCommand=print,*Class.method
-XX:+LogCompilation
```

### 2. 分析去优化原因

```bash
# 使用 hsdis 查看汇编
# 查找 "deopt" 指令
# 理解哪些检查触发了去优化
```

### 3. 验证修复

```java
// 修复前: 测试去优化次数
// 修复后: 重新测试，确认去优化减少
```

---

## 相关链接

### 本地文档

- [C2 优化阶段](c2-phases.md) - 去优化在编译流程中的位置
- [诊断工具](diagnostics.md) - 如何查看去优化日志
- [最佳实践](best-practices.md) - 避免去优化的代码模式
- [内联优化](inlining.md) - 内联失败导致的去优化

### 外部资源

- [JVM Deoptimization](https://shipilev.net/blog/2014/04/Deoptimization-And-Deoptimization-In-HotSpot-JVM/)
- [Understanding Deoptimization](https://medium.com/@divyansh.ved/understanding-deoptimization-in-jvm-8b8e3e3c5f7e)

---

**最后更新**: 2026-03-21
