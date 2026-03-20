# Valhalla 开发活动分析

基于 GitHub PR 和 git 历史的详细分析。

[← 返回 Valhalla](./)

---

## 概述

### 仓库统计

| 指标 | 数值 |
|------|------|
| **总提交数** | 85,810+ |
| **分支** | lworld (主开发分支) |
| **2024-2025 Valhalla 相关提交** | 821+ |
| **活跃贡献者** | 25+ |
| **组织** | Oracle, Red Hat, 个人贡献者 |

### 语言分布

```
Java     ████████████████████████████████████████ 73.7%
C++      █████████████████ 14.3%
C        ███████ 8.0%
Assembly ███ 2.7%
```

---

## PR 统计分析 (最近 100 个已关闭 PR)

### 按组件分类

| 组件 | PR 数量 | 占比 |
|------|--------|------|
| **Test** | 12 | 24% |
| **JNI** | 8 | 16% |
| **Field** | 8 | 16% |
| **C2 (JIT 编译器)** | 7 | 14% |
| **Class** | 5 | 10% |
| **Array** | 4 | 8% |
| **JFR** | 2 | 4% |
| **GC** | 2 | 4% |

### 按贡献者排名

| 贡献者 | PR 数量 | 组织 | 主要领域 |
|--------|--------|------|----------|
| **[Chen Liang](/by-contributor/profiles/chen-liang.md)** (liach) | 11 | Oracle | javac, 语言特性 |
| **[Tobias Hartmann](/by-contributor/profiles/tobias-hartmann.md)** (TobiHartmann) | 9 | Oracle | C2 JIT 编译器 |
| **[Daniel D. Daugherty](/by-contributor/profiles/daniel-daugherty.md)** (dcubed-ojdk) | 6 | Oracle | 测试基础设施 |
| **[David Holmes](/by-contributor/profiles/david-holmes.md)** (dholmes-ora) | 6 | Oracle | JNI, 运行时 |
| **Axel Boldt-Christmas** (xmas92) | 6 | Oracle | GC, 内存屏障 |
| **[Christian Hagedorn](/by-contributor/profiles/christian-hagedorn.md)** (chhagedorn) | 5 | Oracle | C2 JIT 编译器 |
| **[Roger Riggs](/by-contributor/profiles/roger-riggs.md)** (RogerRiggs) | 4 | Oracle | 核心库, 序列化 |
| **David Beaumont** (david-beaumont) | 4 | Oracle | javac, 构建系统 |
| **[Frederic Parain](/by-contributor/profiles/frederic-parain.md)** (fparain) | 4 | Oracle | 字段, JNI |
| **Quan Anh Mai** (merykitty) | 4 | Oracle | C2 JIT 编译器 |
| **[Stefan Karlsson](/by-contributor/profiles/stefan-karlsson.md)** (stefank) | 4 | Oracle | GC, 数组 |
| **Alex Menkov** (alexmenkov) | 3 | Oracle | JDWP, JVMTI |
| **Benoît Maillard** (benoitmaillard) | 3 | Oracle | C2 JIT 编译器 |
| **Markus Grönlund** (mgronlun) | 3 | Oracle | JFR |
| **Ivan Walulya** (walulyai) | 3 | Oracle | 字段布局 |
| **Casper Norrbin** (caspernorrbin) | 2 | Oracle | 类加载 |
| **[Coleen Phillimore](/by-contributor/profiles/coleen-phillimore.md)** (coleenp) | 2 | Oracle | 类加载, SA |
| **Vicente Romero** (vicente-romero-oracle) | 2 | Oracle | javac |
| 其他 | 10 | - | - |

---

## 最新开发活动 (2026年3月)

### 3月19日
- `8343835`: C2 编译器断言失败修复 (chhagedorn)
- `8379333`: JNI NewWeakGlobalRef 对值类型抛出 IdentityException (dholmes-ora)

### 3月18日
- `8380395`: TestCallingConvention 测试问题修复 (dcubed-ojdk)
- `8377324`: 移除 MethodData SA 测试 (coleenp)

### 3月16日
- `8380191`: 回滚 OptimizePtrCompare 优化 (TobiHartmann)
- `8379833`: javac 构造函数代码修复 (vicente-romero-oracle)

### 3月13日
- `8379258`: JVMTI HeapMonitor 测试修复 (alexmenkov)
- `8379369`: JDWP 代理弱引用修复 (alexmenkov)
- `8380053`: 移除 @NullRestricted 字段强制预加载 (fparain)
- `8374950`: JFR oldobject 测试修复 (mgronlun)
- `8380026`: 数组 oops 协变 klass() (stefank)
- `8380006`: Deoptimization 缺少 InternalOOMEMark (stefank)

---

## 关键技术领域

### 1. C2 JIT 编译器优化

**活跃贡献者**: Tobias Hartmann, Christian Hagedorn, Quan Anh Mai, Benoît Maillard

**关键修复**:
- `8343835`: StoreD/StoreI 不匹配断言失败
- `8379791`: Blackhole MemBar 处理
- `8370070`: IR 不匹配问题
- `8378780`: CastI2N 断言问题
- `8376778`: Ideal 验证哈希边问题

**C2 特性**:
- 标量替换优化
- 循环向量化支持
- 内联类型调用约定
- 扁平化数组访问优化

### 2. JNI (Java Native Interface)

**活跃贡献者**: David Holmes, Frederic Parain

**关键变更**:
- `8379333`: NewWeakGlobalRef 对值类型抛出 IdentityException
- `8379365`: 新增 IsValueObject JNI 方法
- `8379012`: MonitorEnter 异常消息修复
- `8378609`: AllocObject/NewObject 行为恢复
- `8375339`: GetObjectField/SetObjectField 日志记录

**JNI 值类型支持**:
```c
// 新增 JNI 方法
jboolean IsValueObject(JNIEnv* env, jobject value);

// 现有方法行为变更
jobject NewWeakGlobalRef(JNIEnv* env, jobject obj);
// 对值类型抛出 IdentityException 而非返回 weak ref
```

### 3. GC 和内存管理

**活跃贡献者**: Stefan Karlsson, Axel Boldt-Christmas, Ivan Walulya

**关键修复**:
- `8380006`: Deoptimization 缺少 OOM Mark
- `8380026`: 数组元素 klass 访问
- `8379847`: GC 访问者清理
- `8378862`: flatArrayKlass::copy_array 内存屏障
- `8378521`: 移除 CardTableBarrierSet 预屏障
- `8378523`: 移除 post-barriers
- `8378650`: 静态字段扁平化决策
- `8378531`: 移除 obj_at() 方法
- `8378519`: FlatFieldPayload 构造优化

**GC 支持**:
- G1 GC 完整支持
- ZGC 完整支持
- Shenandoah 支持
- Serial GC 支持
- Parallel GC 支持

### 4. 字段布局

**活跃贡献者**: Ivan Walulya, Frederic Parain, Axel Boldt-Christmas

**关键修复**:
- `8379619`: FieldLayoutBuilder 使用 heapOopSize
- `8379184`: 清理 get_size_and_alignment
- `8378650`: 静态字段扁平化显式决策
- `8378519`: FlatFieldPayload 检查折叠
- `8379355`: 字段布局测试覆盖

**字段布局策略**:
```
┌─────────────────────────────────────┐
│  Inline Class 字段布局               │
├─────────────────────────────────────┤
│  1. 原始类型字段 (按大小排序)        │
│  2. 嵌套值类型字段 (扁平化)          │
│  3. 引用类型字段 (对齐)              │
│  4. Null marker (如需要)             │
└─────────────────────────────────────┘
```

### 5. 数组支持

**活跃贡献者**: Stefan Karlsson, Frederic Parain

**关键修复**:
- `8380026`: 数组 oops 协变 klass()
- `8379847`: 移除数组元素 klass 访问
- `8378862`: flatArrayKlass 内存屏障
- `8364464`: GC 分块处理扁平数组
- `8376235`: Valhalla ProblemList 分析

**数组类型**:
```java
// 扁平化数组 (flat array)
Point[] flat = new Point[100];  // 连续内存

// 可空扁平数组 (nullable flat array)
Point?[] nullable = new Point?[100];  // 带_null_marker

// 引用数组 (传统)
Point[] ref = new Point[100];  // 引用数组
```

### 6. 测试基础设施

**活跃贡献者**: Daniel D. Daugherty, Coleen Phillimore

**关键修复**:
- `8380395`: TestCallingConvention ProblemList
- `8377324`: MethodData SA 测试移除
- `8379263`: JVMTI HeapMonitoring 测试
- `8378799`: Skynet 测试 ProblemList
- `8378706`: ArchivedFlatArrayTest
- `8377710`: JhsdbJstackMixed 测试

**测试目录**:
```
test/hotspot/jtreg/
├── compiler/valhalla/inlinetypes/    # C2 编译器测试
├── runtime/valhalla/                 # 运行时测试
└── serviceability/jvmti/valhalla/   # JVMTI 测试

test/jdk/
├── java/lang/reflect/valhalla/      # 反射测试
├── com/sun/jdi/valhalla/            # JDI 测试
└── valhalla/valuetypes/             # 值类型测试
```

---

## 开发活动时间线

### 2024年活动

```
1月  ████████████ 活跃开始 (18 commits/day 峰值)
2月  ████████████ 持续开发
3月  ███████████████ JIT 优化高峰
4月  ████████████ GC 改进
5月  ████████████ 测试扩展
6月  ████████████ 字段布局
7月  ██████████ JNI 支持
8月  ██████████ 数组优化
9月  ████████████ 编译器修复
10月 ████████████ 性能优化
11月 ███████████████ 代码重构高峰
12月 ███████████████ 年度冲刺 (46 commits/day 峰值)
```

### 2025年活动

```
1月  ████████████ 持续开发
2月  ████████████ 测试修复
3月  ████████████ JIT 优化
4月  ███████████████ 交付冲刺 (40 commits/day)
5月  ████████████ 持续开发
6月  ████████████ GC 改进
7月  ██████████ 夏季放缓
8月  ██████████ 稳定版本
9月  ████████████ 秋季冲刺
10月 ████████████ 持续开发
11月 ████████████ 年度冲刺
12月 ███████████████ 年终冲刺 (48 commits/day 峰值)
```

### 2026年活动 (截至3月)

```
1月  ████████████ 新年继续
2月  ████████████ 持续开发
3月  ████████████ 当前活跃
```

---

## JEP 401 (Primitive Classes) 状态

### 实现阶段

| 阶段 | 描述 | 状态 |
|------|------|------|
| **JVM 层** | inlineKlass, flatArrayKlass | ✅ 完成 |
| **javac 层** | 值类语法, 类型检查 | ✅ 完成 |
| **类库** | 核心库适配 | 🔄 进行中 |
| **JNI** | 值类型 JNI 支持 | 🔄 进行中 |
| **JFR** | 飞行记录支持 | 🔄 进行中 |
| **文档** | 规范文档 | 🔄 进行中 |

### 关键里程碑

```
2023 Q4 ─── Bootstrap VM 转换到 JEP 401 模型
   │
2024 Q1 ─── C2 编译器更新
   │
2024 Q2 ─── C1 编译器更新
   │
2024 Q3 ─── 核心库迁移
   │
2024 Q4 ─── 测试扩展
   │
2025 Q1 ─── JNI 支持
   │
2025 Q2 ─── 持续优化
   │
2025+ ─── 正式交付准备中
```

---

## 贡献者组织分布

### Oracle

**核心团队**:
- [David Holmes](/by-contributor/profiles/david-holmes.md) - 运行时架构
- [Tobias Hartmann](/by-contributor/profiles/tobias-hartmann.md) - C2 JIT 编译器
- [Christian Hagedorn](/by-contributor/profiles/christian-hagedorn.md) - C2 JIT 编译器
- [Stefan Karlsson](/by-contributor/profiles/stefan-karlsson.md) - GC
- [Coleen Phillimore](/by-contributor/profiles/coleen-phillimore.md) - 类加载
- [Roger Riggs](/by-contributor/profiles/roger-riggs.md) - 核心库
- [Frederic Parain](/by-contributor/profiles/frederic-parain.md) - 字段, JNI

### Red Hat

- [Roman Kennke](/by-contributor/profiles/roman-kennke.md) - Shenandoah GC

### 社区贡献者

- Axel Boldt-Christmas (xmas92) - GC, 内存屏障
- Ivan Walulya (walulyai) - 字段布局
- Quan Anh Mai (merykitty) - C2 JIT 编译器
- Benoît Maillard (benoitmaillard) - C2 JIT 编译器

---

## 技术挑战

### 1. JIT 编译器适配

**挑战**:
- 值类型标量替换
- 调用约定优化
- 寄存器分配
- 循环向量化

**解决方案**:
- C2: 扩展中间表示 (IR)
- C1: 添加值类型特定优化
- 新增 `inlineKlass` 专用节点

### 2. GC 支持

**挑战**:
- 扁平化数组遍历
- 值类型字段引用
- Null marker 处理
- 并发收集

**解决方案**:
- 分块遍历扁平数组
- 值类型内部引用处理
- 特殊 GC barriers

### 3. JNI 兼容性

**挑战**:
- 值类型不能有弱引用
- MonitorEnter 不支持值类型
- 字段访问日志

**解决方案**:
- 新增 `IsValueObject` 方法
- 抛出 `IdentityException`
- 更新 JNI 规范

---

## 参与贡献

### 如何贡献

1. **Fork 仓库**: https://github.com/openjdk/valhalla
2. **创建分支**: 基于 `lworld` 分支
3. **编写测试**: 所有变更需要测试
4. **提交 PR**: 包含问题 ID (如 `8379333`)

### 代码审查流程

```
PR 创建
   │
   ├── 检查清单
   │   ├── CI 测试通过
   │   ├── 测试覆盖充分
   │   ├── 文档更新
   │   └── 向后兼容
   │
   ├── 审查者批准
   │   └── 至少一名 Reviewer
   │
   ├── 标记 integrated
   │
   └── 合并到 lworld
```

---

## 参考资料

- [Valhalla GitHub](https://github.com/openjdk/valhalla)
- [Valhalla PR 列表](https://github.com/openjdk/valhalla/pulls)
- [JEP 401: Primitive Classes](https://openjdk.org/jeps/401)
- [JEP 402: Unified Generics](https://openjdk.org/jeps/402)
- [Valhalla 邮件列表](https://mail.openjdk.org/pipermail/valhalla-spec-observers/)

---

→ [返回 Valhalla](./)
