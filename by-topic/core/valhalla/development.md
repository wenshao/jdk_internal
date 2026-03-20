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
| **lworld PRs** | 85+ |
| **活跃贡献者** | 23 |
| **组织** | Oracle (主导), Red Hat, 个人贡献者 |
| **Stars** | 683 |
| **Forks** | 151 |
| **代码大小** | 915 KB |
| **语言分布** | Java 73.7%, C++ 14.3%, C 8.0%, Assembly 2.7% |

> **数据来源**: https://github.com/openjdk/valhalla
> **PR 查询**: `is:pr is:closed label:integrated` (lworld 标签)

---

## PR 统计分析 (lworld 标签 PR)

### 按贡献者排名 (最新)

| 排名 | 贡献者 | PRs | GitHub | 组织 | 主要领域 |
|------|--------|-----|--------|------|----------|
| 1 | **[Chen Liang](../../by-contributor/profiles/chen-liang.md)** | 11 | @liach | Oracle | javac, 语言特性 |
| 2 | **[Tobias Hartmann](../../by-contributor/profiles/tobias-hartmann.md)** | 9 | @TobiHartmann | Oracle | C2 JIT 编译器 |
| 3 | **[David Holmes](../../by-contributor/profiles/david-holmes.md)** | 6 | @dholmes-ora | Oracle | JNI, 运行时 |
| 4 | **Axel Boldt-Christmas** | 6 | @xmas92 | Oracle | GC, 内存屏障 |
| 5 | **[Daniel D. Daugherty](../../by-contributor/profiles/daniel-daugherty.md)** | 5 | @dcubed-ojdk | Oracle | 测试基础设施 |
| 6 | **[Roger Riggs](../../by-contributor/profiles/roger-riggs.md)** | 4 | @RogerRiggs | Oracle | 核心库, 序列化 |
| 7 | **Benoît Maillard** | 4 | @benoitmaillard | Oracle | C2 JIT 编译器 |
| 8 | **[Frederic Parain](../../by-contributor/profiles/frederic-parain.md)** | 4 | @fparain | Oracle | 字段, JNI |
| 9 | **Quan Anh Mai** | 4 | @merykitty | Oracle | C2 JIT 编译器 |
| 10 | **[Stefan Karlsson](../../by-contributor/profiles/stefan-karlsson.md)** | 4 | @stefank | Oracle | GC, 数组 |
| 11 | **[Christian Hagedorn](../../by-contributor/profiles/christian-hagedorn.md)** | 5 | @chhagedorn | Oracle | C2 JIT 编译器 |
| 12 | **David Beaumont** | 3 | @david-beaumont | Oracle | javac, 构建系统 |
| 13 | **[Alex Menkov]** | 3 | @alexmenkov | Oracle | JDWP, JVMTI |
| 14 | **[Markus Grönlund]** | 3 | @mgronlun | Oracle | JFR |
| 15 | **Ivan Walulya** | 3 | @walulyai | Oracle | 字段布局 |
| 16 | **[Coleen Phillimore](../../by-contributor/profiles/coleen-phillimore.md)** | 2 | @coleenp | Oracle | 类加载, SA |
| 17 | **[Vicente Romero](../../by-contributor/profiles/vicente-romero.md)** | 2 | @vicente-romero-oracle | Oracle | javac |
| 18 | **Casper Norrbin** | 2 | @caspernorrbin | Oracle | 类加载 |
| 19 | **Arraying** | 2 | - | Oracle | 调试方法 |
| 20 | **其他** | 7 | - | - | - |

### 按组件分类

| 组件 | PR 数量 | 占比 | 关键贡献者 |
|------|--------|------|-----------|
| **C2 JIT 编译器** | 15 | 18% | TobiHartmann, chhagedorn, benoitmaillard, merykitty |
| **测试基础设施** | 12 | 14% | dcubed-ojdk, coleenp, alexmenkov |
| **JNI** | 8 | 9% | dholmes-ora, fparain |
| **GC/内存** | 10 | 12% | stefank, xmas92, walulya |
| **字段布局** | 7 | 8% | walulyai, fparain, xmas92 |
| **javac/语言** | 15 | 18% | liach, david-beaumont, vicente-romero-oracle |
| **核心库** | 6 | 7% | RogerRiggs, liach |
| **JFR** | 4 | 5% | mgronlun |
| **类加载** | 3 | 4% | coleenp, caspernorrbin |
| **数组** | 5 | 6% | stefank, fparain, walulya |

---

## 最新开发活动 (2026年3月)

### 3月19日 (2 PRs)
- `8343835`: C2 assert fails with "no mismatched stores" ([chhagedorn](../../by-contributor/profiles/christian-hagedorn.md))
- `8379333`: [REDO] JNI NewWeakGlobalRef IdentityException ([dholmes-ora](../../by-contributor/profiles/david-holmes.md))

### 3月18日 (3 PRs)
- `8380395`: TestCallingConvention ProblemList ([dcubed-ojdk](../../by-contributor/profiles/daniel-daugherty.md))
- `8377324`: Remove MethodData SA tests ([coleenp](../../by-contributor/profiles/coleen-phillimore.md))
- `8379863`: C2 assert scalar_reallocated ([benoitmaillard](../../by-contributor/profiles/))

### 3月16日 (2 PRs)
- `8380191`: [BACKOUT] OptimizePtrCompare ([TobiHartmann](../../by-contributor/profiles/tobias-hartmann.md))
- `8379833`: javac 构造函数代码 ([vicente-romero-oracle](../../by-contributor/profiles/vicente-romero.md))

### 3月13日 (6 PRs)
- `8379258`: JVMTI HeapMonitor 测试 ([alexmenkov](https://openjdk.org/census#alexmenkov))
- `8379369`: JDWP weak references ([alexmenkov](https://openjdk.org/census#alexmenkov))
- `8380053`: @NullRestricted 预加载 ([fparain](../../by-contributor/profiles/frederic-parain.md))
- `8374950`: JFR oldobject 测试 ([mgronlun](../../by-contributor/profiles/markus-gronlund.md))
- `8380026`: 数组 oops 协变 klass() ([stefank](../../by-contributor/profiles/stefan-karlsson.md))
- `8380006`: Deoptimization OOM Mark ([stefank](../../by-contributor/profiles/stefan-karlsson.md))

### 3月12日 (5 PRs)
- `8379906`: Suppressed warnings annotation processing ([david-beaumont](../../by-contributor/profiles/david-beaumont.md))
- `8379791`: C2 Blackhole MemBar ([chhagedorn](../../by-contributor/profiles/christian-hagedorn.md))
- `8370070`: TestLWorld IR 不匹配 ([benoitmaillard](../../by-contributor/profiles/))
- `8379847`: GC 数组元素 klass ([stefank](../../by-contributor/profiles/stefan-karlsson.md))
- `8377351`: ClassInitBarrier crash ([dafedafe](../../by-contributor/profiles/))

### 3月11日 (2 PRs)
- `8379820`: javac launcher release version ([liach](../../by-contributor/profiles/chen-liang.md))
- `8379803`: langtool 测试清理 ([liach](../../by-contributor/profiles/chen-liang.md))

### 3月10日 (3 PRs)
- `8379619`: FieldLayoutBuilder heapOopSize ([walulyai](../../by-contributor/profiles/))
- `8377882`: OptimizePtrCompare 保守 ([rwestrel](../../by-contributor/profiles/))
- `8379592`: EA3 version flick ([MrSimms](../../by-contributor/profiles/))

### 3月9日 (3 PRs)
- `8379559`: ClassFileFormatVersion preview ([liach](../../by-contributor/profiles/chen-liang.md))
- `8375051`: 调试方法 Valhalla 信息 ([Arraying](../../by-contributor/profiles/))
- `8379514`: 数组 klass 清理 ([stefank](../../by-contributor/profiles/stefan-karlsson.md))

### 3月6日 (6 PRs)
- `8378662`: UBSAN 构建失败 ([xmas92](../../by-contributor/profiles/))
- `8379406`: allocateInstance 行为 ([merykitty](../../by-contributor/profiles/))
- `8378560`: 反射构造 C2 assert ([merykitty](../../by-contributor/profiles/))
- `8379365`: JNI IsValueObject ([dholmes-ora](../../by-contributor/profiles/david-holmes.md))
- `8379355`: 字段布局测试 ([fparain](../../by-contributor/profiles/frederic-parain.md))
- `8379328`: [BACKOUT] JNI NewWeakGlobalRef ([dcubed-ojdk](../../by-contributor/profiles/daniel-daugherty.md))

### 3月5日 (5 PRs)
- `8378521`: CardTableBarrierSet 预屏障 ([xmas92](../../by-contributor/profiles/))
- `8378523`: CardTableBarrierSet post-barriers ([xmas92](../../by-contributor/profiles/))
- `8379263`: JVMTI HeapMonitoring ProblemList ([dholmes-ora](../../by-contributor/profiles/david-holmes.md))
- `8375357`: TestLWorld compilable ([marc-chevalier](../../by-contributor/profiles/))
- `8378862`: flatArrayKlass 内存屏障 ([fparain](../../by-contributor/profiles/frederic-parain.md))

### 3月4日 (4 PRs)
- `8379184`: fieldLayoutBuilder 清理 ([walulyai](../../by-contributor/profiles/))
- `8379007`: JNI NewWeakGlobalRef ([dholmes-ora](../../by-contributor/profiles/david-holmes.md))
- `8379163`: Port 8378792 to lworld ([liach](../../by-contributor/profiles/chen-liang.md))
- `8379164`: jdk.jdeps 反射 API ([liach](../../by-contributor/profiles/chen-liang.md))

### 3月3日 (2 PRs)
- `8379012`: JNI MonitorEnter 异常消息 ([dholmes-ora](../../by-contributor/profiles/david-holmes.md))
- `8378609`: JNI AllocObject/NewObject 恢复 ([dholmes-ora](../../by-contributor/profiles/david-holmes.md))

### 3月2日 (2 PRs)
- `8335187`: Object::finalize 注释 ([vicente-romero-oracle](../../by-contributor/profiles/vicente-romero.md))
- `8379006`: 值类序列化 JUnit ([RogerRiggs](../../by-contributor/profiles/roger-riggs.md))

---

## 关键技术领域

### 1. C2 JIT 编译器优化

**活跃贡献者**: Tobias Hartmann (9 PRs), Christian Hagedorn (5 PRs), Quan Anh Mai (4 PRs), Benoît Maillard (4 PRs)

**关键修复**:
- `8343835`: StoreD/StoreI 不匹配断言失败
- `8379791`: Blackhole MemBar 处理
- `8370070`: IR 不匹配问题 (TestLWorld test85/86)
- `8378780`: CastI2N 断言问题
- `8376778`: Ideal 验证哈希边问题
- `8378292`: LoadKlass 断言失败
- `8376708`: CmpL 优化遗漏
- `8379863`: scalar_replaced 断言

**C2 特性**:
- 标量替换优化
- 循环向量化支持
- 内联类型调用约定
- 扁平化数组访问优化

### 2. JNI (Java Native Interface)

**活跃贡献者**: David Holmes (6 PRs), Frederic Parain (4 PRs)

**关键变更**:
- `8379333`: NewWeakGlobalRef 对值类型抛出 IdentityException (REDO)
- `8379365`: 新增 IsValueObject JNI 方法
- `8379328`: [BACKOUT] JNI NewWeakGlobalRef
- `8379012`: MonitorEnter 异常消息修复
- `8378609`: AllocObject/NewObject 行为恢复
- `8375339`: GetObjectField/SetObjectField 日志记录
- `8379263`: JVMTI HeapMonitoring ProblemList
- `8378862`: flatArrayKlass 内存屏障

**JNI 值类型支持**:
```c
// 新增 JNI 方法
jboolean IsValueObject(JNIEnv* env, jobject value);

// 现有方法行为变更
jobject NewWeakGlobalRef(JNIEnv* env, jobject obj);
// 对值类型抛出 IdentityException 而非返回 weak ref
```

### 3. GC 和内存管理

**活跃贡献者**: Stefan Karlsson (4 PRs), Axel Boldt-Christmas (6 PRs), Ivan Walulya (3 PRs)

**关键修复**:
- `8380006`: Deoptimization 缺少 InternalOOMEMark
- `8380026`: 数组 oops 协变 klass()
- `8379847`: GC 访问者清理
- `8378862`: flatArrayKlass copy_array 内存屏障
- `8378521`: 移除 CardTableBarrierSet 预屏障
- `8378523`: 移除 CardTableBarrierSet post-barriers
- `8378650`: 静态字段扁平化决策
- `8378531`: 移除 obj_at(int) 方法
- `8378519`: FlatFieldPayload 构造优化
- `8364464`: GC 分块处理扁平数组

**GC 支持**:
- G1 GC 完整支持
- ZGC 完整支持
- Shenandoah 支持
- Serial GC 支持
- Parallel GC 支持

### 4. 字段布局

**活跃贡献者**: Ivan Walulya (3 PRs), Frederic Parain (4 PRs), Axel Boldt-Christmas (6 PRs)

**关键修复**:
- `8379619`: FieldLayoutBuilder 使用 heapOopSize
- `8379184`: 清理 get_size_and_alignment
- `8378650`: 静态字段扁平化显式决策
- `8378519`: FlatFieldPayload 检查折叠
- `8379355`: 字段布局测试覆盖
- `8379406`: allocateInstance 行为规范

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

### 5. javac 编译器与语言特性

**活跃贡献者**: Chen Liang (11 PRs), David Beaumont (3 PRs), Vicente Romero (2 PRs)

**关键修复**:
- `8379820`: javac launcher release version 21
- `8379803`: langtool 测试清理
- `8379559`: ClassFileFormatVersion preview flags
- `8379163`: Port 8378792 to lworld
- `8379164`: jdk.jdeps 反射 API 处理
- `8378721`: LambdaMetafactory LoadableDescriptors
- `8378184`: 清理与 master 的差异
- `83788697`: ClassFileParser verify_legal_class_name
- `8378767`: Makefile preview mode 重命名
- `8378365`: jrtfs ExplodedImage regex
- `8378272`: StrictProcessor 处理
- `8335187`: Object::finalize 注释

### 6. 数组支持

**活跃贡献者**: Stefan Karlsson (4 PRs), Frederic Parain (4 PRs), Ivan Walulya (3 PRs)

**关键修复**:
- `8380026`: 数组 oops 协变 klass()
- `8379847`: 移除数组元素 klass 访问
- `8378862`: flatArrayKlass copy_array 内存屏障
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

### 7. 测试基础设施

**活跃贡献者**: Daniel D. Daugherty (5 PRs), Coleen Phillimore (2 PRs), Alex Menkov (3 PRs)

**关键修复**:
- `8380395`: TestCallingConvention ProblemList
- `8377324`: MethodData SA 测试移除
- `8379263`: JVMTI HeapMonitoring 测试
- `8378799`: Skynet 测试 ProblemList
- `8378706`: ArchivedFlatArrayTest ProblemList
- `8377710`: JhsdbJstackMixed 测试
- `8377351`: ClassInitBarrier crash
- `8317172`: vmTestbase hiddenloader stress

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

## 核心库贡献

**活跃贡献者**: Roger Riggs (4 PRs)

**关键修复**:
- `8379006`: 值类序列化 JUnit 转换
- `8378375`: System.identityHashCode 值类
- `8378728`: ObjectInputStream 移除 TRACE
- `8378476`: Character cache 禁用 (preview)

---

## JFR 支持

**活跃贡献者**: Markus Grönlund (3 PRs)

**关键修复**:
- `8378840`: JFR 测试 --enable-preview 标志
- `8378771`: JFR Cooperative Sampling
- `8374950`: JFR oldobject 测试

---

## 开发活动时间线

### 2026年2-3月活动 (85 PRs)

```
2月1-5日  ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 4 PRs
2月6-10日 ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 6 PRs
2月11-15日 ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 8 PRs
2月16-20日 ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 12 PRs (高峰)
2月21-25日 ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 11 PRs
2月26-28日 ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 6 PRs
3月1-5日  ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 11 PRs
3月6-10日 ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 11 PRs
3月11-15日 ██████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 7 PRs
3月16-19日 ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 5 PRs
```

**总计**: 85 PRs (2026年2-3月)

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
2025 Q4 ─── EA3 版本
   │
2026 Q1 ─── 持续优化
   │
2026+ ─── 正式交付准备中
```

---

## 贡献者组织分布

### Oracle (主导)

**核心团队**:
- [David Holmes](../../by-contributor/profiles/david-holmes.md) - 运行时架构 (6 PRs)
- [Tobias Hartmann](../../by-contributor/profiles/tobias-hartmann.md) - C2 JIT 编译器 (9 PRs)
- [Christian Hagedorn](../../by-contributor/profiles/christian-hagedorn.md) - C2 JIT 编译器 (5 PRs)
- [Stefan Karlsson](../../by-contributor/profiles/stefan-karlsson.md) - GC (4 PRs)
- [Coleen Phillimore](../../by-contributor/profiles/coleen-phillimore.md) - 类加载 (2 PRs)
- [Roger Riggs](../../by-contributor/profiles/roger-riggs.md) - 核心库 (4 PRs)
- [Frederic Parain](../../by-contributor/profiles/frederic-parain.md) - 字段, JNI (4 PRs)
- [Chen Liang](../../by-contributor/profiles/chen-liang.md) - javac (11 PRs)
- [Markus Grönlund](../../by-contributor/profiles/markus-gronlund.md) - JFR (3 PRs)
- [Vicente Romero](../../by-contributor/profiles/vicente-romero.md) - javac (2 PRs)
- [David Beaumont](../../by-contributor/profiles/david-beaumont.md) - javac, 构建 (3 PRs)
- [Daniel D. Daugherty](../../by-contributor/profiles/daniel-daugherty.md) - 测试 (5 PRs)
- [Alex Menkov](../../by-contributor/profiles/) - JDWP, JVMTI (3 PRs)

### 社区贡献者

| 贡献者 | PRs | 主要领域 |
|--------|-----|----------|
| Axel Boldt-Christmas (xmas92) | 6 | GC, 内存屏障 |
| Ivan Walulya (walulyai) | 3 | 字段布局 |
| Quan Anh Mai (merykitty) | 4 | C2 JIT 编译器 |
| Benoît Maillard (benoitmaillard) | 4 | C2 JIT 编译器 |
| Casper Norrbin (caspernorrbin) | 2 | 类加载 |
| Arraying | 2 | 调试方法 |
| Marc Chevalier (marc-chevalier) | 1 | 测试 |
| Damon Fedafe (dafedafe) | 1 | 运行时 |
| Roland Westrelin (rwestrel) | 1 | C2 优化 |

---

## 技术挑战与解决方案

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

### 官方资源

- [Valhalla GitHub](https://github.com/openjdk/valhalla)
- [Valhalla PR 列表](https://github.com/openjdk/valhalla/pulls)
- [JEP 401: Primitive Classes](https://openjdk.org/jeps/401)
- [JEP 402: Unified Generics](https://openjdk.org/jeps/402)
- [Valhalla 邮件列表](https://mail.openjdk.org/pipermail/valhalla-spec-observers/)

### 本地文档

- [Valhalla 主页](./)
- [值类型详解](./value-types.md)
- [泛型特化详解](./generics.md)
- [时间线](./timeline.md)

### 贡献者档案

- [完整贡献者列表](../../by-contributor/)
- [Chen Liang](../../by-contributor/profiles/chen-liang.md)
- [Tobias Hartmann](../../by-contributor/profiles/tobias-hartmann.md)
- [David Holmes](../../by-contributor/profiles/david-holmes.md)

---

**最后更新**: 2026-03-20

**数据来源**: https://github.com/openjdk/valhalla/pulls (查询: `is:pr is:closed label:integrated`)
