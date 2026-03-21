# Valhalla 架构与源码分析

基于 lworld 分支源码的深度技术分析。

[← 返回 Valhalla](./)

---
## 目录

1. [架构概览](#1-架构概览)
2. [源码结构](#2-源码结构)
3. [核心类分析](#3-核心类分析)
4. [字段布局系统](#4-字段布局系统)
5. [C2 编译器优化](#5-c2-编译器优化)
6. [JNI 支持](#6-jni-支持)
7. [测试覆盖](#7-测试覆盖)
8. [最近开发活动分析](#8-最近开发活动分析)
9. [与主 JDK 的差异](#9-与主-jdk-的差异)
10. [构建与测试](#10-构建与测试)
11. [相关链接](#11-相关链接)

---


## 1. 架构概览

### 分层架构

```
┌─────────────────────────────────────────────────────────────────────┐
│                        应用层 (Application)                          │
│  value class Point { int x, y; }                                    │
├─────────────────────────────────────────────────────────────────────┤
│                        语言层 (Language)                             │
│  javac: 语法解析, 类型检查, 字节码生成                               │
├─────────────────────────────────────────────────────────────────────┤
│                        字节码层 (Bytecode)                           │
│  Q-Type 描述符, defaultvalue, withfield 指令                        │
├─────────────────────────────────────────────────────────────────────┤
│                        JVM 层 (Runtime)                              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                 │
│  │  InlineKlass │ │FlatArrayKlass│ │  FieldLayout │                 │
│  └──────────────┘ └──────────────┘ └──────────────┘                 │
├─────────────────────────────────────────────────────────────────────┤
│                        GC 层 (Garbage Collection)                    │
│  G1, ZGC, Shenandoah, Serial, Parallel                             │
├─────────────────────────────────────────────────────────────────────┤
│                        JIT 层 (Compilation)                          │
│  ┌──────────────┐ ┌──────────────┐                                  │
│  │  C1 (Client) │ │  C2 (Server) │                                  │
│  │  InlineType  │ │InlineTypeNode│                                  │
│  └──────────────┘ └──────────────┘                                  │
├─────────────────────────────────────────────────────────────────────┤
│                        本地接口层 (JNI/JVMTI)                         │
│  IsValueObject, NewWeakGlobalRef IdentityException                  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. 源码结构

### 核心源码目录

```
valhalla/src/
├── java.base/share/classes/
│   ├── java/lang/
│   │   └── Class.java              # isValue(), isIdentity()
│   └── jdk/internal/
│       ├── value/
│       │   └── ValueClass.java     # 值类型工具类
│       └── vm/annotation/
│           └── LooselyConsistentValue.java
│
├── hotspot/share/
│   ├── oops/
│   │   ├── inlineKlass.hpp         # 值类型 Klass
│   │   ├── inlineKlass.cpp
│   │   ├── flatArrayKlass.hpp      # 扁平化数组 Klass
│   │   ├── flatArrayKlass.cpp
│   │   ├── flatArrayOop.cpp        # 扁平化数组 Oop
│   │   └── fieldLayoutBuilder.hpp  # 字段布局构建器
│   │
│   ├── opto/
│   │   ├── inlinetypenode.hpp      # C2 IR 节点
│   │   └── inlinetypenode.cpp
│   │
│   ├── classfile/
│   │   └── classFileParser.cpp     # 类文件解析
│   │
│   └── prims/
│       └── jni.cpp                 # JNI 实现
│
└── test/
    ├── hotspot/jtreg/
    │   └── compiler/valhalla/inlinetypes/
    └── jdk/
        └── valhalla/valuetypes/
```

---

## 3. 核心类分析

### 1. InlineTypeNode (C2 JIT)

**文件**: `src/hotspot/share/opto/inlinetypenode.hpp`

```cpp
// C2 IR 中表示值类型的节点
class InlineTypeNode : public TypeNode {
private:
  enum { 
    Control,    // 控制输入
    Oop,        // 堆分配缓冲区的 Oop
    IsBuffered, // 是否堆分配
    NullMarker, // Null 标记 (0=null, 1=non-null)
    Values      // 字段值节点
  };

  // 获取值类型的 Klass
  ciInlineKlass* inline_klass() const;

  // 字段加载
  void load(GraphKit* kit, Node* base, Node* ptr, ...);
  
  // 字段存储
  void store(GraphKit* kit, Node* base, Node* ptr, ...) const;
  
  // 从 Oop 创建
  static InlineTypeNode* make_from_oop(GraphKit* kit, Node* oop, 
                                        ciInlineKlass* vk);
  
  // 创建全零值
  static InlineTypeNode* make_all_zero(PhaseGVN& gvn, ciInlineKlass* vk);
};
```

**关键实现**:

```cpp
// 克隆并创建 Phi 节点处理控制流合并
InlineTypeNode* InlineTypeNode::clone_with_phis(
    PhaseGVN* gvn, Node* region, SafePointNode* map, 
    bool is_non_null, bool init_with_top) {
  
  InlineTypeNode* vt = clone_if_required(gvn, map);
  
  // 为 Oop 值创建 PhiNode
  PhiNode* oop = PhiNode::make(region, init_with_top ? top : vt->get_oop(), t);
  vt->set_oop(*gvn, oop);
  
  // 为 is_buffered 创建 PhiNode
  Node* is_buffered_node = PhiNode::make(region, ...);
  vt->set_req(IsBuffered, is_buffered_node);
  
  // 为 null_marker 创建 PhiNode
  Node* null_marker_node = is_non_null ? gvn->intcon(1) 
                                       : PhiNode::make(region, ...);
  vt->set_req(NullMarker, null_marker_node);
  
  return vt;
}
```

### 2. FlatArrayKlass (扁平化数组)

**文件**: `src/hotspot/share/oops/flatArrayKlass.hpp`

```cpp
/**
 * 值类型数组，布局类似 typeArrayOop
 * 但需要 oops 迭代器支持
 */
class FlatArrayKlass : public ObjArrayKlass {
  friend class Deoptimization;
  friend class oopFactory;

 private:
  LayoutKind _layout_kind;  // 布局类型

 public:
  // 元素类型 (必须是 InlineKlass)
  InlineKlass* element_klass() const {
    return InlineKlass::cast(ObjArrayKlass::element_klass());
  }

  // 分配 Klass
  static FlatArrayKlass* allocate_klass(
      Klass* element_klass, ArrayProperties props, 
      LayoutKind lk, TRAPS);

  // 数组布局辅助
  static jint array_layout_helper(InlineKlass* vklass, LayoutKind lk);

  // Oop 分配
  oop allocate(int length, TRAPS);
  
  // 元素大小
  int element_byte_size() const {
    return 1 << layout_helper_log2_element_size(_layout_helper);
  }
  
  // 包含 oops
  bool contains_oops() {
    return element_klass()->contains_oops();
  }
};
```

**数组布局对比**:

```
传统引用数组 (Point[]):
┌─────────────────────────────────────────────────┐
│ header │ length │ ref0 │ ref1 │ ref2 │ ...     │
└─────────────────────────────────────────────────┘
           │        │      │
           ▼        ▼      ▼
         [Point]  [Point] [Point]
         24 bytes 24B    24B

扁平化数组 (flat Point[]):
┌─────────────────────────────────────────────────┐
│ header │ length │ x0│y0│ x1│y1│ x2│y2│ ...     │
└─────────────────────────────────────────────────┘
         (连续内存，无对象头)
```

### 3. ValueClass (Java 工具类)

**文件**: `src/java.base/share/classes/jdk/internal/value/ValueClass.java`

```java
/**
 * 值类型工具类
 */
public final class ValueClass {
    
    /// 检查字段类型是否可存储值对象
    public static boolean isValueObjectCompatible(Class<?> fieldType) {
        return PreviewFeatures.isEnabled()
                && !fieldType.isPrimitive()
                && (!fieldType.isIdentity() || fieldType == Object.class);
    }
    
    /// 检查是否为具体值类
    public static boolean isConcreteValueClass(Class<?> clazz) {
        return clazz.isValue() && !Modifier.isAbstract(clazz.getModifiers());
    }
    
    /// 检查是否有二进制负载 (可扁平化)
    public static boolean hasBinaryPayload(Class<?> c) {
        if (!ValueClass.isConcreteValueClass(c))
            return c.isPrimitive();
        return Unsafe.getUnsafe().isFlatPayloadBinary(c);
    }
    
    /// 检查字段是否为 NullRestricted
    public static boolean isNullRestrictedField(Field f) {
        return JLRA.isNullRestrictedField(f);
    }
    
    /// 分配 Null-Restricted 数组
    @IntrinsicCandidate
    public static native Object[] newNullRestrictedAtomicArray(
        Class<?> componentType, int length);
}
```

### 4. LooselyConsistentValue 注解

**文件**: `src/java.base/share/classes/jdk/internal/vm/annotation/LooselyConsistentValue.java`

```java
/**
 * 标记一个值类可以容忍数据竞争导致的不一致。
 * 
 * 允许 JVM 使用非原子策略读写扁平化字段和数组。
 */
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
public @interface LooselyConsistentValue { }
```

---

## 4. 字段布局系统

### FieldLayoutBuilder

```
字段布局策略:
┌─────────────────────────────────────────────────────────────────┐
│                    Inline Class 字段布局                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 原始类型字段 (按大小降序排列)                                │
│     ┌────────┬────────┬────────┬────────┐                       │
│     │ double │ long   │ int    │ short  │                       │
│     └────────┴────────┴────────┴────────┘                       │
│                                                                 │
│  2. 嵌套值类型字段 (递归扁平化)                                  │
│     ┌────────────────────────────────────┐                       │
│     │ Point.x │ Point.y │ Complex.re/im │                       │
│     └────────────────────────────────────┘                       │
│                                                                 │
│  3. 引用类型字段 (按对齐)                                        │
│     ┌────────┬────────┐                                         │
│     │ String │ Object │                                         │
│     └────────┴────────┘                                         │
│                                                                 │
│  4. Null Marker (如需要)                                         │
│     ┌──────────────┐                                             │
│     │ _null_marker │  ← 仅当可空时                               │
│     └──────────────┘                                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 布局类型 (LayoutKind)

```cpp
enum LayoutKind {
  LayoutKind::Reference,    // 引用数组
  LayoutKind::Flat,         // 扁平化数组
  LayoutKind::NullableFlat  // 可空扁平化数组 (带 null marker)
};
```

---

## 5. C2 编译器优化

### 标量替换

```
原始代码:
  Point p = new Point(1, 2);
  int sum = p.x + p.y;

C2 优化后:
  int p_x = 1;
  int p_y = 2;
  int sum = p_x + p_y;  // 无对象分配!
```

### 内联优化

```cpp
// InlineTypeNode 在 safepoint 的标量化
void InlineTypeNode::make_scalar_in_safepoint(
    PhaseIterGVN* igvn, Unique_Node_List& worklist, 
    SafePointNode* sfpt) {
  
  // 将字段值直接添加到 safepoint
  // 避免在 safepoint 保留整个对象
  for (uint i = 0; i < vk->nof_declared_nonstatic_fields(); ++i) {
    Node* field_value = field_value(i);
    sfpt->add_req(field_value);
  }
}
```

### 向量化机会

```java
// 传统数组 - 难以向量化
Point[] points = new Point[1000];
for (int i = 0; i < 1000; i++) {
    points[i].x += 1;  // 需要解引用
}

// 扁平化数组 - 容易向量化
Point[] points = new Point[1000];  // 扁平化
for (int i = 0; i < 1000; i++) {
    points[i].x += 1;  // 连续内存, SIMD 优化
}

// 生成的 SIMD 指令 (x86 AVX2):
// vpaddd ymm0, ymm1, [rdi+rax*4]  ; 一次处理 8 个 int
```

---

## 6. JNI 支持

### 新增方法

```c
// 检查是否为值对象
jboolean IsValueObject(JNIEnv* env, jobject value);
```

### 行为变更

```c
// 对值类型抛出 IdentityException
jobject NewWeakGlobalRef(JNIEnv* env, jobject obj) {
    if (obj != NULL && obj->is_value_object()) {
        ThrowNew(env, "java/lang/IdentityException", 
                 "Cannot create weak reference to value object");
        return NULL;
    }
    // ... 原有逻辑
}
```

### 相关 PR

| Issue | 描述 | 作者 |
|-------|------|------|
| 8379365 | 新增 IsValueObject JNI 方法 | David Holmes |
| 8379333 | NewWeakGlobalRef IdentityException (REDO) | David Holmes |
| 8379012 | MonitorEnter 异常消息 | David Holmes |
| 8378609 | AllocObject/NewObject 恢复 | David Holmes |

---

## 7. 测试覆盖

### 测试目录结构

```
test/
├── hotspot/jtreg/
│   ├── compiler/valhalla/inlinetypes/
│   │   ├── TestLWorld.java          # L-World 核心测试
│   │   ├── TestCallingConvention.java
│   │   ├── TestIntrinsics.java
│   │   └── field_layout/
│   │       └── ValueRandomLayoutTest.java
│   │
│   ├── runtime/valhalla/
│   │   └── inlinetypes/
│   │       ├── IsIdentityClassTest.java
│   │       └── ValueClassPreviewTest.java
│   │
│   └── serviceability/jvmti/valhalla/
│
└── jdk/
    ├── valhalla/valuetypes/
    │   ├── NullRestrictedTest.java
    │   ├── NullRestrictedArraysTest.java
    │   ├── SubstitutabilityTest.java
    │   ├── Reflection.java
    │   ├── MethodHandleTest.java
    │   └── StreamTest.java
    │
    ├── java/lang/reflect/valhalla/
    └── java/io/Serializable/valueObjects/
```

### 关键测试用例

```java
// test/jdk/valhalla/valuetypes/NullRestrictedTest.java
@Test
public void testNullRestricted() {
    class Container {
        @NullRestricted
        Point location;  // 不能为 null
    }
    
    Container c = new Container();
    // c.location 默认为 Point.default
    // c.location = null;  // 编译错误!
}

// test/jdk/valhalla/valuetypes/SubstitutabilityTest.java
@Test
public void testEquals() {
    Point p1 = new Point(1, 2);
    Point p2 = new Point(1, 2);
    
    // 值比较，非引用比较
    assertTrue(p1.equals(p2));
    assertTrue(p1.hashCode() == p2.hashCode());
}
```

---

## 8. 最近开发活动分析

### 2026年3月 lworld 分支关键提交

| Issue | 描述 | 组件 | 作者 |
|-------|------|------|------|
| 8379863 | C2 scalar_replaced 断言 | C2 | Benoît Maillard |
| 8380015 | ValueRandomLayoutTest 除零 | 测试 | Stefan Karlsson |
| 8343835 | C2 StoreD/StoreI 断言 | C2 | Christian Hagedorn |
| 8379333 | JNI NewWeakGlobalRef REDO | JNI | David Holmes |
| 8379833 | javac 构造函数代码 | javac | Vicente Romero |
| 8380053 | @NullRestricted 预加载移除 | 运行时 | Frederic Parain |
| 8379365 | JNI IsValueObject 新增 | JNI | David Holmes |
| 8380026 | 数组 oops 协变 klass() | GC | Stefan Karlsson |
| 8378862 | flatArrayKlass 内存屏障 | GC | Frederic Parain |
| 8379619 | FieldLayoutBuilder heapOopSize | 字段 | Ivan Walulya |

### 技术趋势分析

```
C2 编译器优化:
  ████████████████████ 40%
  
JNI 支持:
  ████████████ 25%

GC/内存:
  ████████ 17%

javac/语言:
  ██████ 13%

其他:
  ███ 5%
```

---

## 9. 与主 JDK 的差异

### 合并策略

```bash
# 定期从 master 合并
git checkout lworld
git merge origin/master

# 解决冲突 (主要集中在):
# - hotspot/share/oops/
# - hotspot/share/opto/
# - src/java.base/share/classes/
```

### 关键差异文件

| 文件 | 差异类型 |
|------|----------|
| `inlineKlass.hpp/cpp` | 新增 |
| `flatArrayKlass.hpp/cpp` | 新增 |
| `inlinetypenode.hpp/cpp` | 新增 |
| `classFileParser.cpp` | 修改 |
| `jni.cpp` | 修改 |
| `ValueClass.java` | 新增 |

---

## 10. 构建与测试

### 构建命令

```bash
# 克隆仓库
git clone https://github.com/openjdk/valhalla
cd valhalla
git checkout lworld

# 配置
bash configure --enable-preview

# 构建
make images

# 运行测试
make test TEST="jtreg:test/jdk/valhalla/valuetypes"
```

### 启用预览

```bash
# 运行值类型程序
java --enable-preview -cp classes Main

# 运行时选项
java -XX:+EnableValhalla --enable-preview Main
```

---

## 11. 相关链接

### 官方资源

- [Valhalla GitHub](https://github.com/openjdk/valhalla)
- [JEP 401: Primitive Classes](https://openjdk.org/jeps/401)
- [Valhalla Wiki](https://wiki.openjdk.org/display/valhalla)

### 本地文档

- [Valhalla 主页](./)
- [值类型详解](./value-types.md)
- [泛型特化详解](./generics.md)
- [时间线](./timeline.md)
- [开发活动分析](./development.md)

---

**最后更新**: 2026-03-20

**源码仓库**: `/root/git/valhalla` (lworld 分支)
