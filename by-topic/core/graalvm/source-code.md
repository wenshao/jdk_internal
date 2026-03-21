# GraalVM 源码解读

> 深入 GraalVM 核心源码，理解实现细节

[← 返回 GraalVM 首页](./) | [← 返回架构详解](architecture.md)

---
## 目录

1. [源码结构](#1-源码结构)
2. [核心类解读](#2-核心类解读)
3. [Native Image 源码解读](#3-native-image-源码解读)
4. [Truffle 源码解读](#4-truffle-源码解读)
5. [调试工具使用](#5-调试工具使用)
6. [关键算法](#6-关键算法)
7. [相关链接](#7-相关链接)

---


## 1. 源码结构

### Graal 编译器源码

```
graal/
├── compiler/
│   ├── src/
│   │   ├── org.graalvm.compiler.core/
│   │   │   ├── src/
│   │   │   │   ├── BytecodeParser.java      # 字节码解析
│   │   │   │   ├── GraalCompiler.java       # 编译器入口
│   │   │   │   └── GenContext.java          # 代码生成上下文
│   │   │   ├── org.graalvm.compiler.nodes/  # IR 节点
│   │   │   │   ├── FixedNode.java           # 固定节点
│   │   │   │   ├── FloatingNode.java        # 浮动节点
│   │   │   │   ├── StructuredGraph.java     # 图结构
│   │   │   │   └── IfNode.java              # 条件分支
│   │   │   ├── org.graalvm.compiler.phases/ # 优化阶段
│   │   │   │   ├── Phase.java               # 优化阶段基类
│   │   │   │   ├── InliningPhase.java       # 内联阶段
│   │   │   │   └── EscapeAnalysisPhase.java # 逃逸分析
│   │   │   └── org.graalvm.compiler.lir/    # 低级 IR
│   │   │       ├── LIR.java                 # LIR 表示
│   │   │       ├── AllocationStage.java     # 寄存器分配
│   │   │       └── CodeGeneration.java      # 代码生成
│   │   └── org.graalvm.compiler.hotspot/    # HotSpot 集成
│   │       └── HotSpotGraalCompiler.java    # HotSpot 编译器
│   └── test/                                # 测试
└── docs/                                    # 文档
```

### JVMCI 源码

```
jdk.vm.ci/
├── src/
│   ├── jdk.vm.ci.code/
│   │   ├── src/
│   │   │   ├── CompilationRequest.java      # 编译请求
│   │   │   ├── CompiledMethod.java          # 编译结果
│   │   │   └── CodeCache.java               # 代码缓存
│   │   └── jdk.vm.ci.code.site/
│   │       └── Site.java                    # 代码位置
│   ├── jdk.vm.ci.meta/
│   │   ├── src/
│   │   │   ├── ResolvedJavaType.java        # 解析的类型
│   │   │   ├── ResolvedJavaMethod.java      # 解析的方法
│   │   │   └── ResolvedJavaField.java       # 解析的字段
│   │   └── jdk.vm.ci.meta.site/
│   │       └── Site.java                    # 元数据位置
│   └── jdk.vm.ci.runtime/
│       └── src/
│           └── JVMCICompiler.java           # JVMCI 运行时
└── test/
```

---

## 2. 核心类解读

### 1. GraalCompiler - 编译器入口

```java
// 简化版 GraalCompiler 核心代码
public class GraalCompiler implements Compiler {
    
    private final CompilationPhase[] phases;
    
    public GraalCompiler() {
        // 初始化编译阶段
        this.phases = createCompilationPhases();
    }
    
    /**
     * 编译方法
     * @param method 要编译的 Java 方法
     * @param entryBci 入口字节码索引 (用于 OSR)
     * @param profilingInfo 性能分析信息
     * @return 编译后的机器码
     */
    @Override
    public CompiledMethod compileMethod(
        HotSpotResolvedJavaMethod method,
        int entryBci,
        ProfilingInfo profilingInfo,
        boolean installAsNonVmCompiler,
        JVMCIRuntime runtime
    ) {
        // 1. 创建图结构
        StructuredGraph graph = createGraph(method, entryBci);
        
        // 2. 执行优化阶段
        for (CompilationPhase phase : phases) {
            phase.apply(graph);
        }
        
        // 3. 生成 LIR
        LIR lir = generateLIR(graph);
        
        // 4. 寄存器分配
        allocateRegisters(lir);
        
        // 5. 生成机器码
        byte[] machineCode = generateMachineCode(lir);
        
        // 6. 安装到代码缓存
        return installCode(machineCode, method);
    }
    
    private StructuredGraph createGraph(HotSpotResolvedJavaMethod method, int entryBci) {
        // 字节码解析为图
        GraphBuilder graphBuilder = new GraphBuilder(method, entryBci);
        return graphBuilder.build();
    }
}
```

**关键点**:
- 编译流程分为 5 个阶段
- 使用 StructuredGraph 作为 IR
- 支持 OSR (On-Stack Replacement)

### 2. StructuredGraph - Sea of Nodes 实现

```java
// 简化版 StructuredGraph 核心代码
public class StructuredGraph extends Graph {
    
    // 图节点列表
    private final NodeMap<Node> nodes;
    
    // 起始节点
    private StartNode startNode;
    
    // 返回节点
    private ReturnNode returnNode;
    
    /**
     * 添加节点到图中
     */
    public <T extends Node> T add(T node) {
        nodes.add(node);
        
        // 自动连接到前驱节点
        if (node instanceof FixedNode) {
            connectToPredecessor((FixedNode) node);
        }
        
        return node;
    }
    
    /**
     * 应用优化阶段
     */
    public void optimize(Phase phase) {
        phase.apply(this);
    }
    
    /**
     * 验证图的完整性
     */
    public void verify() {
        // 检查所有节点的类型
        // 检查控制流依赖
        // 检查数据流依赖
        for (Node node : nodes) {
            node.verify(this);
        }
    }
}

// 节点基类
public abstract class Node {
    // 前驱节点
    private Node predecessor;
    
    // 后继节点
    private Node successor;
    
    // 数据流输入
    private Node[] inputs;
    
    // 数据流输出
    private Node[] usages;
    
    /**
     * 节点类型 (用于模式匹配)
     */
    public abstract NodeClass<? extends Node> getNodeClass();
}

// 固定节点 (有控制流依赖)
public abstract class FixedNode extends Node implements FixedNodeInterface {
    // 控制流前驱
    private FixedNode controlPredecessor;
}

// 浮动节点 (仅数据流依赖)
public abstract class FloatingNode extends Node {
    // 无控制流依赖
}
```

**Sea of Nodes 特点**:
- 固定节点和浮动节点分离
- 数据流和控制流统一表示
- 支持增量优化

### 3. EscapeAnalysisPhase - 逃逸分析实现

```java
// 简化版逃逸分析代码
public class EscapeAnalysisPhase extends Phase {
    
    @Override
    protected void run(StructuredGraph graph) {
        // 1. 收集所有对象分配
        List<NewInstanceNode> allocations = collectAllocations(graph);
        
        // 2. 分析每个对象的逃逸状态
        for (NewInstanceNode alloc : allocations) {
            EscapeState escape = analyzeEscape(alloc);
            
            // 3. 根据逃逸状态应用优化
            if (escape == EscapeState.NoEscape) {
                // 标量替换
                scalarReplace(alloc);
            } else if (escape == EscapeState.ArgEscape) {
                // 部分优化
                partialOptimize(alloc);
            }
        }
    }
    
    /**
     * 分析对象的逃逸状态
     */
    private EscapeState analyzeEscape(NewInstanceNode alloc) {
        // 使用固定点迭代算法
        EscapeState state = EscapeState.NoEscape;
        
        boolean changed = true;
        while (changed) {
            changed = false;
            
            // 遍历所有使用点
            for (Node use : alloc.usages()) {
                EscapeState useEscape = analyzeUse(use);
                
                if (useEscape.ordinal() > state.ordinal()) {
                    state = useEscape;
                    changed = true;
                }
            }
        }
        
        return state;
    }
    
    /**
     * 标量替换
     * 将对象替换为其字段
     */
    private void scalarReplace(NewInstanceNode alloc) {
        // 获取对象的类
        ResolvedJavaType type = alloc.stamp().javaType();
        
        // 获取所有字段
        ResolvedJavaField[] fields = type.getInstanceFields();
        
        // 为每个字段创建独立的变量
        for (ResolvedJavaField field : fields) {
            ValueNode initialValue = alloc.initialValue(field);
            
            // 替换所有字段访问
            replaceFieldAccess(alloc, field, initialValue);
        }
        
        // 删除对象分配节点
        alloc.safeDelete();
    }
}

enum EscapeState {
    NoEscape,      // 未逃逸
    ArgEscape,     // 作为参数逃逸
    GlobalEscape   // 全局逃逸
}
```

**逃逸分析算法**:
- 使用固定点迭代
- 保守分析 (高估逃逸)
- 标量替换消除堆分配

---

## 3. Native Image 源码解读

### 静态分析流程

```java
// 简化版 Native Image 静态分析
public class NativeImageGenerator {
    
    public void generateImage(List<String> mainClasses) {
        // 1. 构建调用图
        CallGraph callGraph = buildCallGraph(mainClasses);
        
        // 2. 收集所有可达类
        Set<ResolvedJavaType> reachableTypes = collectReachableTypes(callGraph);
        
        // 3. 分析反射使用
        ReflectionData reflectionData = analyzeReflection(reachableTypes);
        
        // 4. 构建时初始化
        HeapSnapshot heapSnapshot = buildHeapSnapshot(reachableTypes);
        
        // 5. 编译所有方法
        List<CompiledMethod> compiledMethods = compileAll(reachableTypes);
        
        // 6. 生成镜像
        NativeImage image = generateImage(
            compiledMethods, 
            heapSnapshot,
            reflectionData
        );
        
        // 7. 链接
        linkImage(image);
    }
    
    private CallGraph buildCallGraph(List<String> mainClasses) {
        CallGraphBuilder builder = new CallGraphBuilder();
        
        for (String mainClass : mainClasses) {
            // 从 main 方法开始
            ResolvedJavaMethod mainMethod = resolveMainMethod(mainClass);
            builder.buildFrom(mainMethod);
        }
        
        return builder.build();
    }
}
```

### 堆快照序列化

```java
// 简化版堆快照序列化
public class HeapSnapshotSerializer {
    
    public byte[] serialize(HeapSnapshot snapshot) {
        ByteBuffer buffer = ByteBuffer.allocate(snapshot.size());
        
        // 1. 写入对象数量
        buffer.putInt(snapshot.getObjectCount());
        
        // 2. 序列化每个对象
        for (HeapObject obj : snapshot.getObjects()) {
            serializeObject(buffer, obj);
        }
        
        // 3. 写入引用关系
        for (Reference ref : snapshot.getReferences()) {
            serializeReference(buffer, ref);
        }
        
        return buffer.array();
    }
    
    private void serializeObject(ByteBuffer buffer, HeapObject obj) {
        // 对象头
        buffer.putLong(obj.getHeader());
        
        // 类指针
        buffer.putLong(obj.getClassPointer());
        
        // 字段数据
        for (Object field : obj.getFields()) {
            buffer.putLong(encodeField(field));
        }
    }
}
```

---

## 4. Truffle 源码解读

### AST 节点特化

```java
// 简化版 Truffle AST 节点
public abstract class ExpressionNode extends Node {
    
    public abstract Object execute(VirtualFrame frame);
}

// 加法节点 - 多态特化
public class AddNode extends ExpressionNode {
    
    @Child private ExpressionNode left;
    @Child private ExpressionNode right;
    
    // 特化：整数加法
    @Specialization
    protected int addInt(int a, int b) {
        return a + b;
    }
    
    // 特化：长整数加法
    @Specialization
    protected long addLong(long a, long b) {
        return a + b;
    }
    
    // 特化：浮点数加法
    @Specialization
    protected double addDouble(double a, double b) {
        return a + b;
    }
    
    // 特化：字符串连接
    @Specialization
    protected String addString(String a, String b) {
        return a + b;
    }
    
    // 重写执行方法
    @Override
    public Object execute(VirtualFrame frame) {
        Object leftValue = left.execute(frame);
        Object rightValue = right.execute(frame);
        
        // 根据类型分发到特化方法
        return dispatch(leftValue, rightValue);
    }
}
```

### 部分求值实现

```java
// 简化版部分求值
public class PartialEvaluator {
    
    /**
     * 对 AST 进行部分求值
     * @param root 根节点
     * @param graphBuilder 图构建器
     * @return 优化后的图
     */
    public StructuredGraph evaluate(Node root, GraphBuilder graphBuilder) {
        // 创建解释器框架
        VirtualFrame frame = createFrame();
        
        // 递归求值
        evaluateNode(root, frame, graphBuilder);
        
        return graphBuilder.build();
    }
    
    private void evaluateNode(Node node, VirtualFrame frame, 
                              GraphBuilder graphBuilder) {
        if (node instanceof ExpressionNode) {
            ExpressionNode expr = (ExpressionNode) node;
            
            // 获取节点的特化版本
            Specialization spec = expr.getSpecialization(frame);
            
            if (spec != null) {
                // 内联特化代码
                inlineSpecialization(spec, graphBuilder);
            } else {
                // 保留解释器调用
                graphBuilder.addInterpreterCall(expr);
            }
        }
    }
    
    private void inlineSpecialization(Specialization spec, 
                                      GraphBuilder graphBuilder) {
        // 获取特化方法的字节码
        byte[] bytecode = spec.getBytecode();
        
        // 解析字节码为图节点
        BytecodeParser parser = new BytecodeParser(bytecode);
        parser.parse(graphBuilder);
    }
}
```

---

## 5. 调试工具使用

### IGV (Ideal Graph Visualizer)

```bash
# 启用 Graal 图转储
java -Dgraal.Dump=:2 \
     -Dgraal.PrintGraph=Network \
     -jar app.jar

# 查看特定阶段的图
java -Dgraal.Dump=Inlining:2 \
     -jar app.jar

# 输出到文件
java -Dgraal.Dump=:2 \
     -Dgraal.DumpPath=/tmp/graal-dumps \
     -jar app.jar
```

### 编译日志分析

```bash
# 启用编译日志
java -Dgraal.LogFile=graal.log \
     -Dgraal.LogLevel=INFO \
     -Dgraal.TraceInlining=true \
     -jar app.jar

# 查看编译统计
java -Dgraal.PrintCompilation=true \
     -jar app.jar

# 查看性能分析
java -Dgraal.TuneInlinerExploration=1 \
     -Dgraal.UseProfiledBranches=true \
     -jar app.jar
```

---

## 6. 关键算法

### 1. 图模式匹配

```java
// 简化版图模式匹配
public class GraphPatternMatcher {
    
    // 定义模式：x * 2 = x << 1
    private static final Pattern MUL2_PATTERN = Pattern.create(
        "MultiplyNode(value: #x, constant: 2)"
    );
    
    // 定义替换：x << 1
    private static final Replacement SHIFT1_REPLACEMENT = 
        Replacement.create("LeftShiftNode(value: #x, constant: 1)");
    
    public void optimize(StructuredGraph graph) {
        // 查找所有匹配的模式
        for (Match match : MUL2_PATTERN.findAll(graph)) {
            // 应用替换
            match.replace(SHIFT1_REPLACEMENT);
        }
    }
}
```

### 2. 线性扫描寄存器分配

```java
// 简化版线性扫描算法
public class LinearScanAllocator {
    
    public void allocate(LIR lir) {
        // 1. 计算活跃区间
        List<Interval> intervals = computeLiveIntervals(lir);
        
        // 2. 按起点排序
        intervals.sort(Comparator.comparingInt(i -> i.start));
        
        // 3. 线性扫描
        for (Interval interval : intervals) {
            // 释放过期的区间
            expireOldIntervals(interval);
            
            if (availableRegisters.isEmpty()) {
                // 溢出
                spill(interval);
            } else {
                // 分配寄存器
                Register reg = availableRegisters.poll();
                allocate(interval, reg);
            }
        }
    }
}
```

---

## 7. 相关链接

### 源码仓库
- [Graal GitHub](https://github.com/oracle/graal)
- [JVMCI Source](https://github.com/openjdk/jdk/tree/master/src/jdk.vm.ci)
- [Truffle Source](https://github.com/oracle/graal/tree/master/truffle)

### 文档
- [GraalVM 开发者文档](https://www.graalvm.org/latest/docs/developers-guide/)
- [IGV 使用指南](https://github.com/graalvm/graalvm.github.io/blob/master/igv.md)

---

**最后更新**: 2026-03-21
