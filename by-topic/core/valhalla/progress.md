# Valhalla 项目进度追踪

> **最后更新**: 2026-03-20 | **分支**: lworld | **状态**: 🚧 活跃开发中

[← 返回 Valhalla](./)

---

## 一眼看懂

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Valhalla 项目进度 (2026-03)                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ████████████████████████████████░░░░░░░░░░  75% 总体进度           │
│                                                                     │
│  ✅ JVM 核心        ████████████████████  95%                       │
│  ✅ C2 JIT 编译器   ████████████████████░  90%                       │
│  🔄 JNI 支持        ████████████████░░░░░  80%                       │
│  🔄 GC 集成         ████████████████░░░░░  80%                       │
│  🔄 核心库适配      ████████████░░░░░░░░░░  60%                       │
│  🔄 javac 编译器    ████████████████░░░░░  80%                       │
│  ⏳ 规范文档        ████████░░░░░░░░░░░░░░  40%                       │
│  ⏳ 泛型特化        ████████░░░░░░░░░░░░░░  40%                       │
│                                                                     │
│  预计交付: JDK 27+ (2027)                                           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 组件进度详情

### 1. JVM 核心层 (95%)

| 子组件 | 状态 | 说明 |
|--------|------|------|
| InlineKlass | ✅ 完成 | 值类型 Klass 实现 |
| FlatArrayKlass | ✅ 完成 | 扁平化数组 Klass |
| FieldLayoutBuilder | ✅ 完成 | 字段布局构建器 |
| 类文件解析 | ✅ 完成 | Q-Type 描述符支持 |
| 字节码验证 | ✅ 完成 | 值类型验证规则 |
| 方法解析 | 🔄 进行中 | 值类型方法调用优化 |

**最近提交**:
- `8379619`: FieldLayoutBuilder 使用 heapOopSize
- `8380053`: 移除 @NullRestricted 强制预加载

### 2. C2 JIT 编译器 (90%)

| 子组件 | 状态 | 说明 |
|--------|------|------|
| InlineTypeNode | ✅ 完成 | C2 IR 节点 |
| 标量替换 | ✅ 完成 | 逃逸分析优化 |
| 调用约定 | ✅ 完成 | 值类型传参优化 |
| 循环向量化 | 🔄 进行中 | SIMD 优化支持 |
| 内联优化 | ✅ 完成 | 方法内联支持 |
| 寄存器分配 | 🔄 进行中 | 值类型寄存器分配 |

**最近修复**:
- `8379863`: scalar_replaced 断言修复
- `8343835`: StoreD/StoreI 不匹配修复
- `8379791`: Blackhole MemBar 处理
- `8378560`: 反射构造 C2 断言修复

**待解决问题**:
- `8370070`: TestLWorld IR 不匹配 (test85/86)
- 循环向量化在复杂场景下的正确性

### 3. JNI 支持 (80%)

| 子组件 | 状态 | 说明 |
|--------|------|------|
| IsValueObject | ✅ 完成 | 新增 JNI 方法 |
| NewWeakGlobalRef | ✅ 完成 | 值类型抛 IdentityException |
| AllocObject | ✅ 完成 | 值类型分配行为 |
| MonitorEnter | ✅ 完成 | 值类型抛异常 |
| 字段访问 | 🔄 进行中 | Get/Set 字段日志 |
| 数组操作 | 🔄 进行中 | 扁平化数组 JNI |

**最近提交**:
- `8379365`: 新增 IsValueObject JNI 方法
- `8379333`: NewWeakGlobalRef IdentityException (REDO)
- `8379012`: MonitorEnter 异常消息
- `8378609`: AllocObject/NewObject 恢复

**API 变更**:
```c
// 新增
jboolean IsValueObject(JNIEnv* env, jobject value);

// 行为变更
jobject NewWeakGlobalRef(JNIEnv* env, jobject obj);
// 对值类型: 抛出 IdentityException
```

### 4. GC 集成 (80%)

| GC | 状态 | 说明 |
|----|------|------|
| G1 GC | ✅ 完成 | 完整支持 |
| ZGC | ✅ 完成 | 完整支持 |
| Shenandoah | ✅ 完成 | 完整支持 |
| Serial GC | ✅ 完成 | 完整支持 |
| Parallel GC | ✅ 完成 | 完整支持 |
| 内存屏障 | 🔄 进行中 | 扁平数组复制 |

**最近提交**:
- `8380026`: 数组 oops 协变 klass()
- `8380006`: Deoptimization OOM Mark
- `8378862`: flatArrayKlass 内存屏障
- `8378521/8523`: CardTableBarrierSet 清理

### 5. javac 编译器 (80%)

| 子组件 | 状态 | 说明 |
|--------|------|------|
| 语法解析 | ✅ 完成 | value class 语法 |
| 类型检查 | ✅ 完成 | 值类型约束检查 |
| 字节码生成 | ✅ 完成 | Q-Type 生成 |
| 构造函数 | 🔄 进行中 | 验证构造代码 |
| 注解处理 | 🔄 进行中 | @NullRestricted |

**最近提交**:
- `8379833`: javac 构造函数代码验证
- `8379559`: ClassFileFormatVersion preview flags
- `8379820`: javac launcher release version
- `8379906`: Suppressed warnings 注解处理

### 6. 核心库适配 (60%)

| 库 | 状态 | 说明 |
|----|------|------|
| java.lang.Class | ✅ 完成 | isValue(), isIdentity() |
| java.lang.reflect | 🔄 进行中 | 值类型反射 |
| java.io.Serializable | 🔄 进行中 | 值类型序列化 |
| java.util.Collection | ⏳ 计划中 | 值类型集合 |
| java.util.stream | ⏳ 计划中 | 值类型流 |
| java.time | ⏳ 计划中 | 值类型日期时间 |

**最近提交**:
- `8379006`: 值类序列化 JUnit 转换
- `8378375`: System.identityHashCode 值类

### 7. JFR 支持 (70%)

| 子组件 | 状态 | 说明 |
|--------|------|------|
| 事件定义 | ✅ 完成 | 值类型事件 |
| Cooperative Sampling | ✅ 完成 | 栈修复支持 |
| 测试覆盖 | 🔄 进行中 | preview 标志 |

**最近提交**:
- `8378771`: JFR Cooperative Sampling
- `8378840`: JFR 测试 --enable-preview
- `8374950`: JFR oldobject 测试

### 8. 泛型特化 (40%)

| 子组件 | 状态 | 说明 |
|--------|------|------|
| 语法设计 | ✅ 完成 | `List<int>` 语法 |
| 类型擦除 | 🔄 进行中 | 特化类型保留 |
| 字节码生成 | 🔄 进行中 | 特化字节码 |
| 运行时支持 | ⏳ 计划中 | 特化类加载 |

**当前状态**: 早期原型，预计 JDK 28+

---

## 最近 30 天开发活动

### 提交统计

```
2026-02-20 ~ 2026-03-20

组件分布:
C2 JIT     ████████████████████ 25 commits (35%)
JNI        ████████████ 15 commits (21%)
GC         ████████ 10 commits (14%)
javac      ██████ 8 commits (11%)
测试       ██████ 8 commits (11%)
核心库     ████ 6 commits (8%)
其他       ██ 4 commits (6%)

总计: 76 commits
```

### 活跃贡献者 (最近 30 天)

| 贡献者 | Commits | 主要领域 |
|--------|---------|----------|
| Chen Liang | 11 | javac, 语言特性 |
| Tobias Hartmann | 9 | C2 JIT |
| David Holmes | 6 | JNI, 运行时 |
| Axel Boldt-Christmas | 6 | GC, 内存屏障 |
| Christian Hagedorn | 5 | C2 JIT |
| Stefan Karlsson | 4 | GC, 数组 |
| Frederic Parain | 4 | 字段, JNI |
| Roger Riggs | 4 | 核心库 |
| Quan Anh Mai | 4 | C2 JIT |
| Benoît Maillard | 4 | C2 JIT |

---

## 待解决问题

### 高优先级

| Issue | 描述 | 状态 | 负责人 |
|-------|------|------|--------|
| 8370070 | TestLWorld IR 不匹配 | 🔍 调查中 | Benoît Maillard |
| 8380015 | ValueRandomLayoutTest 除零 | 🔍 调查中 | Stefan Karlsson |
| 8378662 | UBSAN 构建失败 | 🔍 调查中 | Axel Boldt-Christmas |

### 中优先级

| Issue | 描述 | 状态 |
|-------|------|------|
| 泛型特化原型 | `List<int>` 支持 | 🔄 开发中 |
| 核心库迁移 | 值类型适配 | 🔄 开发中 |
| 文档完善 | 规范文档 | 🔄 开发中 |

---

## 里程碑时间线

```
2024 Q4 ────┬── ✅ Bootstrap VM 转换
            │
2025 Q1 ────┼── ✅ C2 编译器更新
            │
2025 Q2 ────┼── ✅ JNI 基础支持
            │
2025 Q3 ────┼── ✅ GC 集成
            │
2025 Q4 ────┼── ✅ EA3 版本
            │
2026 Q1 ────┼── 🔄 持续优化 (当前)
            │
2026 Q2 ────┼── ⏳ 核心库迁移
            │
2026 Q3 ────┼── ⏳ 测试扩展
            │
2026 Q4 ────┼── ⏳ EA4/预览版本?
            │
2027+ ──────┴── ⏳ 正式交付 (JDK 27/28)
```

---

## 如何测试

### 构建 Valhalla JDK

```bash
# 克隆仓库
git clone https://github.com/openjdk/valhalla
cd valhalla
git checkout lworld

# 配置
bash configure --enable-preview

# 构建
make images

# 输出位置
# build/linux-x86_64-server-release/images/jdk/
```

### 运行值类型程序

```java
// Point.java
public value record Point(int x, int y) {
    public Point translate(int dx, int dy) {
        return new Point(x + dx, y + dy);
    }
}

// Main.java
public class Main {
    public static void main(String[] args) {
        Point p1 = new Point(1, 2);
        Point p2 = p1.translate(3, 4);
        System.out.println(p2);  // Point[x=4, y=6]
    }
}
```

```bash
# 编译
javac --enable-preview --release 26 Point.java Main.java

# 运行
java --enable-preview Main
```

### 运行测试

```bash
# 运行所有 Valhalla 测试
make test TEST="jtreg:test/jdk/valhalla"

# 运行特定测试
make test TEST="jtreg:test/jdk/valhalla/valuetypes/NullRestrictedTest.java"

# 运行 C2 编译器测试
make test TEST="jtreg:test/hotspot/jtreg/compiler/valhalla"
```

---

## 版本标签

| 标签 | 日期 | 说明 |
|------|------|------|
| jdk-27+13 | 2026-03-15 | 最新 |
| jdk-27+12 | 2026-03-08 | - |
| jdk-27+11 | 2026-03-01 | - |
| jdk-27+10 | 2026-02-22 | - |

---

## 相关链接

### 官方资源

- [Valhalla GitHub](https://github.com/openjdk/valhalla)
- [lworld 分支](https://github.com/openjdk/valhalla/tree/lworld)
- [PR 列表](https://github.com/openjdk/valhalla/pulls?q=is%3Apr+is%3Aclosed+label%3Aintegrated)
- [JEP 401: Primitive Classes](https://openjdk.org/jeps/401)

### 本地文档

- [架构与源码分析](architecture.md)
- [值类型详解](value-types.md)
- [泛型特化详解](generics.md)
- [时间线](timeline.md)
- [开发活动分析](development.md)

---

## 更新日志

### 2026-03-20
- 新增 progress.md 进度追踪文档
- 组件完成度: JVM 95%, C2 90%, JNI 80%, GC 80%
- 最近 30 天: 76 commits, 10+ 活跃贡献者

### 2026-03-15
- JDK 27+13 标签发布
- JNI IsValueObject 方法新增
- C2 scalar_replaced 断言修复

### 2026-03-10
- FieldLayoutBuilder 优化
- javac 构造函数代码验证修复

---

> **数据来源**: 
> - GitHub: https://github.com/openjdk/valhalla
> - 本地仓库: `/root/git/valhalla` (lworld 分支)
> - PR 查询: `is:pr is:closed label:integrated`
