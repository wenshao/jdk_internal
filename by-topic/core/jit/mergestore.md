# MergeStore 优化

> C2 JIT 编译器的内存写入合并优化技术

[← 返回 JIT 编译](./)

---

## 快速概览

**MergeStore** 是 HotSpot C2 JIT 编译器的一项优化技术，能够将**多次连续的内存写入**合并为**单次宽写入**。

```java
// 原始代码
buf[0] = 'a';
buf[1] = 'b';
buf[2] = 'c';
buf[3] = 'd';

// JIT 优化后 (MergeStore)
Unsafe.putInt(buf, 0, 0x64636261);  // 单次 32 位写入
```

| 优势 | 说明 |
|------|------|
| **减少内存访问** | 4 次字节写入 → 1 次整型写入 |
| **提高缓存利用率** | 更少的内存总线占用 |
| **利用 CPU 宽写入** | 64 位 CPU 可一次写入 8 字节 |

---

## 目录

- [核心原理](#核心原理)
- [演进历史](#演进历史)
- [相关 PR](#相关-pr)
- [最佳实践](#最佳实践)
- [性能对比](#性能对比)

---

## 核心原理

### C2 优化过程

```
原始字节码:
├── aload_2 (加载数组引用)
├── iconst_0
├── bipush 'a'
├── bastore (存储 'a')
├── iconst_1
├── bipush 'b'
├── bastore (存储 'b')
├── iconst_2
├── bipush 'c'
├── bastore (存储 'c')
├── iconst_3
├── bipush 'd'
└── bastore (存储 'd')

        ↓ C2 优化 (MergeStore)

优化后机器码:
├── mov eax, 0x64636261  ("abcd")
└── mov [buf], eax       (单次 32 位写入)
```

### 触发条件

| 条件 | 说明 |
|------|------|
| **连续存储** | 多次存储到连续地址 |
| **相同类型** | 字节/字符/整数 |
| **常量或可预测值** | JIT 可分析 |
| **安全边界** | 数组边界可验证 |

### 不触发的情况

```java
// ❌ 不连续的存储
buf[0] = 'a';
buf[5] = 'b';

// ❌ 不同类型的存储
buf[0] = (byte) x;
buf[1] = (char) y;

// ❌ 边界无法验证
for (int i = 0; i < unknown; i++) {
    buf[i] = value;  // unknown 可能导致越界
}
```

---

## 演进历史

### JDK 21 (2023)

- **JDK-8318446**: 初始 MergeStore 优化
  - 支持基本类型数组
  - Big-Endian 和 Little-Endian
  - Unsafe 和 VarHandle 写入

### JDK 22-23 (2024)

- **JDK-8334342**: 添加 JMH 基准测试
- **JDK-8333893**: StringBuilder append(boolean/null) 优化
- **JDK-8347405**: 支持反向字节序
- **JDK-8343629**: 扩展基准测试覆盖

### JDK 24 (2025)

- **PR #28228**: 合并两个 append(char) 调用
- **PR #29688**: 优化连续 Latin1 字符追加

### JDK 25 (2025)

- **PR #29699**: StringBuilder char append 优化
- **JDK-8370405**: 修复标量替换错误

---

## 相关 PR

### 核心 JIT 优化

#### JDK-8318446: MergeStore 初始实现

> **状态**: 已集成 (JDK 21)
> **影响**: ⭐⭐⭐⭐⭐ 基础优化

**改进内容**:
- 基本类型数组存储合并
- Big-Endian/Little-Endian 支持
- Unsafe 和 VarHandle 优化路径

```java
// 优化前 (4 次字节存储)
array[offset] = (byte) (value >> 24);
array[offset + 1] = (byte) (value >> 16);
array[offset + 2] = (byte) (value >> 8);
array[offset + 3] = (byte) value;

// 优化后 (1 次整型存储)
UNSAFE.putInt(array, offset, value);
```

→ [详细分析](/by-pr/8334/8334342.md) (基准测试)

#### JDK-8347405: Reverse Bytes Order

> **状态**: 已集成 (JDK 23)
> **影响**: ⭐⭐⭐ 字节序优化

**改进内容**:
- 支持反向字节序的存储合并
- `Unsafe.putInt(array, offset, Integer.reverseBytes(value))`

### StringBuilder 优化

#### JDK-8333893: append(boolean) & append(null)

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐⭐ +5-15% 性能提升

**问题**: 原始实现无法触发 MergeStore

**解决方案**:
```java
// 优化前 - 无法触发 MergeStore
public AbstractStringBuilder append(boolean b) {
    writeInt(b ? 1 : 0);  // 间接调用
    return this;
}

// 优化后 - 可触发 MergeStore
public AbstractStringBuilder append(boolean b) {
    if (b) {
        putStringAt("true");   // 4 个连续字符
    } else {
        putStringAt("false");  // 5 个连续字符
    }
    return this;
}
```

**效果**:
- append(boolean): **+14.7%**
- append(null): **+9.2%**

→ [详细分析](/by-pr/8333/8333893.md)

#### PR #28228: 合并两个 append(char)

> **作者**: Shaojin Wen
> **影响**: ⭐⭐⭐⭐ char append 优化

**改进**: 将两个连续的 `append(char)` 合并为 `append(char, char)`

```java
// 优化前
sb.append('a');
sb.append('b');

// 优化后 (新增方法)
sb.append('a', 'b');  // 可触发 MergeStore
```

#### PR #29688: 连续 Latin1 字符优化

> **作者**: Shaojin Wen
> **影响**: ⭐⭐⭐⭐ Latin1 字符串优化

**改进**: 优化 `StringLatin1.putCharsAt` 以触发 MergeStore

```java
// 优化后 - 连续的 putByte 可被合并
static void putCharsAt(byte[] val, int index, int c1, int c2, int c3, int c4) {
    UNSAFE.putByte(val, address, (byte)(c1));
    UNSAFE.putByte(val, address + 1, (byte)(c2));
    UNSAFE.putByte(val, address + 2, (byte)(c3));
    UNSAFE.putByte(val, address + 3, (byte)(c4));
}
// JIT 优化为: UNSAFE.putInt(val, address, packedValue)
```

### Bug 修复

#### JDK-8370405: 标量替换错误

> **状态**: 已修复
> **影响**: ⭐⭐⭐⭐ 重要修复

**问题**: MergeStores 在分配消除中被错误标量替换

**修复**: 改进逃逸分析和标量替换的交互

#### JDK-8371385: TestRematerializeObjects 失败

> **状态**: 已修复
> **平台**: s390x, 非 x86

**问题**: `-XX:-UseUnalignedAccesses` 下测试失败

**修复**: 改进非对齐访问的处理

---

## 最佳实践

### 触发 MergeStore 的代码模式

#### ✅ 推荐模式

```java
// 1. 连续常量字符
static void putNull(byte[] buf, int offset) {
    buf[offset] = 'n';
    buf[offset + 1] = 'u';
    buf[offset + 2] = 'l';
    buf[offset + 3] = 'l';
}

// 2. 使用 Unsafe.putByte
static void putChars(byte[] buf, int offset) {
    UNSAFE.putByte(buf, base + offset, 'a');
    UNSAFE.putByte(buf, base + offset + 1, 'b');
    UNSAFE.putByte(buf, base + offset + 2, 'c');
    UNSAFE.putByte(buf, base + offset + 3, 'd');
}

// 3. Big-Endian 手动写入
static void putIntBE(byte[] buf, int offset, int value) {
    buf[offset] = (byte) (value >> 24);
    buf[offset + 1] = (byte) (value >> 16);
    buf[offset + 2] = (byte) (value >> 8);
    buf[offset + 3] = (byte) value;
}
```

#### ❌ 避免的模式

```java
// 1. 不连续的存储
buf[0] = 'a';
buf[5] = 'b';  // 跳过了索引 1-4

// 2. 动态索引
for (int i = 0; i < count; i++) {
    buf[getIndex(i)] = value;  // 索引不可预测
}

// 3. 条件存储
if (condition) {
    buf[0] = 'a';
}
buf[1] = 'b';  // 可能不连续
```

### StringBuilder 使用建议

```java
// ✅ 推荐: 直接 append 常量
sb.append("null");  // 可触发 MergeStore

// ✅ 推荐: 使用专门的 append 方法
sb.append(true);    // JDK-8333893 优化后

// ⚠️ 避免条件拼接
sb.append(x ? "yes" : "no");  // 三元运算符可能阻碍优化
```

---

## 性能对比

### JMH 基准测试结果

| 方法 | 平均时间 (ns) | 相对性能 | MergeStore |
|------|---------------|----------|------------|
| **setIntB (手动)** | ~12000 | 基准 | ❌ |
| **setIntBU (Unsafe)** | ~8000 | +50% | N/A |
| **setIntBV (VarHandle)** | ~8500 | +41% | N/A |
| **setIntB (JIT 优化)** | ~8200 | +46% | ✅ |

### StringBuilder 优化效果

| 操作 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| append(boolean) | 45.2 ns | 38.5 ns | **+14.7%** |
| append(null) | 38.6 ns | 35.1 ns | **+9.2%** |
| append(char, char) | 28.4 ns | 24.2 ns | **+17.4%** |

### 真实场景影响

| 场景 | 预期提升 |
|------|----------|
| JSON 序列化 | +3-8% |
| 日志格式化 | +2-5% |
| 字符串拼接 | +5-15% |

---

## 诊断和验证

### 查看 JIT 编译输出

```bash
# 启用 JIT 编译日志
java -XX:+PrintCompilation -XX:+PrintInlining \
     -XX:+UnlockDiagnosticVMOptions \
     -XX:+PrintAssembly \
     YourClass

# 查看汇编输出
# 查找 "mov" 指令，确认是否使用宽写入
```

### JMH 基准测试

```bash
# 运行 MergeStore 基准测试
cd jdk
make test TEST="micro:java.lang.invoke.MergeStoreBench"

# 或直接运行
java -jar build/benchmarks/jars/micro-benchmarks.jar \
     MergeStoreBench
```

### 确认 MergeStore 生效

```java
// 测试代码
@Benchmark
public void putChars4(byte[] buf) {
    buf[0] = 't';
    buf[1] = 'e';
    buf[2] = 's';
    buf[3] = 't';
}

// 使用 -XX:+PrintAssembly 查看
// 优化后应该看到单次 mov 指令
```

---

## 相关链接

### 内部文档

- [JIT 编译索引](./index.md)
- [C2 编译阶段](./c2-phases.md)
- [JIT 诊断工具](./diagnostics.md)
- [性能优化](../performance/)

### PR 分析

- [JDK-8334342: MergeStore JMH 基准测试](/by-pr/8334/8334342.md)
- [JDK-8333893: StringBuilder boolean/null 优化](/by-pr/8333/8333893.md)
- [JDK-8343629: 更多 MergeStore 基准测试](/by-pr/8343/8343629.md)

### 外部资源

- [JDK-8318446: MergeStore 初始实现](https://bugs.openjdk.org/browse/JDK-8318446)
- [JDK-8347405: Reverse Bytes Order](https://bugs.openjdk.org/browse/JDK-8347405)
- [JMH 文档](https://openjdk.org/projects/code-tools/jmh/)

### 邮件列表讨论

- [hotspot-compiler-dev](https://mail.openjdk.org/pipermail/hotspot-compiler-dev/)
- MergeStore 优化设计讨论

---

**最后更新**: 2026-03-20

**Sources**:
- [OpenJDK MergeStore PRs](https://github.com/openjdk/jdk/pulls?q=is%3Apr+MergeStore+is%3Aclosed)
- [JDK-8318446 Bug Report](https://bugs.openjdk.org/browse/JDK-8318446)
