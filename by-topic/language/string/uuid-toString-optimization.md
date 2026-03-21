# UUID.toString() 优化深度分析

> 从 Compact Strings 适配到 SIMD 风格向量运算的十年进化之路

---

## 1. TL;DR 快速概览

> 💡 **1 分钟了解核心要点**

### 优化成果

| 指标 | 原始 | 最终 | 提升 |
|------|------|------|------|
| 吞吐量 | ~2000 ops/ms | ~4000+ ops/ms | **+100%+** |
| 函数调用 | 8 次 | 4 次 | -50% |
| 内存访问 | 24+ 次 | 4 次 | -83% |
| 分支预测 | 16+ 次 | 0 次 | 消除 |

### 核心技术

```
查表法 ──────────────────────→ hex8 向量化 ─────────────────→ 内联优化
   ↓                            ↓                              ↓
HexDigits.put4()          Long.expand()            ByteArrayLittleEndian
256 元素查找表              SIMD 风格并行              无查找表
```

### 时间线

```
2016 ──── 2020 ─────────── 2024 ─────────────────────── 2025
 │         │                  │                              │
适配       fromString        hex8 SIMD                  消除查表
Compact   优化              向量运算                    (JDK-8353741)
Strings
```

### 主要贡献者

- **[Shaojin Wen (温绍锦)](../../by-contributor/profiles/shaojin-wen.md)** - hex8 算法、消除查找表
- **Kieran Farrell** - UUIDv7、循环展开
- **Aleksey Shipilev** - Compact Strings 适配
- **Claes Redestad** - fromString 优化

### 关键代码

```java
// 核心：8 个数字并行转 ASCII
private static long hex8(long i) {
    i = Long.expand(i, 0x0F0F_0F0F_0F0F_0F0FL);
    long m = (i + 0x0606_0606_0606_0606L) & 0x1010_1010_1010_1010L;
    return Long.reverseBytes(((m << 1) + (m >> 1) - (m >> 4))
            + 0x3030_3030_3030_3030L + i);
}
```

---

## 目录

- [背景](#背景)
- [优化历史时间线](#优化历史时间线)
- [早期优化 (2016-2020)](#早期优化-2016-2020)
- [核心优化 (2024-2025)](#核心优化-2024-2025)
- [算法原理](#算法原理)
- [性能对比](#性能对比)
- [贡献者](#贡献者)
- [参考资料](#参考资料)

---

## 2. 背景

`java.util.UUID#toString()` 是一个高频调用的方法，用于将 128 位的 UUID 转换为标准字符串表示格式：

```
123e4567-e89b-12d3-a456-426614174000
```

格式说明：`8-4-4-4-12` 格式，共 36 个字符（包含 4 个连字符）

---

## 3. 优化历史时间线

```
┌─────────────────────────────────────────────────────────────────┐
│                    UUID.toString() 优化历史                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  2016 ────────────────────────────────────────────────────     │
│    Aleksey Shipilev                                          │
│    适配 Compact Strings (JDK-8148936)                         │
│                                                                 │
│  2020 ────────────────────────────────────────────────────     │
│    Claes Redestad                                            │
│    优化 fromString (JDK-8196334)                             │
│                                                                 │
│  2024 ────────────────────────────────────────────────────     │
│    Shaojin Wen                                                │
│    hex8 SIMD 风格向量运算                                     │
│                                                                 │
│  2024 ────────────────────────────────────────────────────     │
│    Kieran Farrell                                            │
│    循环展开 (unroll loop)                                    │
│                                                                 │
│  2025 ────────────────────────────────────────────────────     │
│    Shaojin Wen                                                │
│    消除查找表 (JDK-8353741)                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. 早期优化 (2016-2020)

### 2016: Compact Strings 适配

**提交**: [JDK-8148936](https://bugs.openjdk.org/browse/JDK-8148936)
**作者**: [Aleksey Shipilev](https://github.com/Shipo)
**审查**: Igor Veresov, Claes Redestad

JDK 9 引入 **Compact Strings** (JEP 254) 后，`UUID.toString()` 需要适配新的字符串表示方式。

```java
// 之前: 使用 char[] (UTF-16)
new String(char[])  // 每个 char 2 字节

// 之后: 使用 byte[] (Latin1)
new String(byte[], StandardCharsets.ISO_8859_1)  // ASCII 只需 1 字节
```

**关键改动**:
- 移除对 `JavaLangAccess.fastUUID()` 的依赖
- 使用 `StandardCharsets.ISO_8859_1` 替代 `new String(byte[])`
- 减少字符串构造时的内存拷贝

### 2020: fromString() 优化

**提交**: [JDK-8196334](https://bugs.openjdk.org/browse/JDK-8196334)
**作者**: [Claes Redestad](https://github.com/redestad)
**协作者**: Andriy Plokhotnyuk, Jon Chambers

虽然主要针对 `fromString()`，但也为后续 `toString()` 优化奠定了基础：

```java
// 快速路径: 36 字符标准格式
if (name.length() == 36) {
    // 快速验证 4 个连字符位置
    if (name.charAt(8) == '-' && name.charAt(13) == '-' &&
        name.charAt(18) == '-' && name.charAt(23) == '-') {
        // 直接解析 16 进制...
    }
}
```

---

## 5. 核心优化 (2024-2025)

### 原始实现：查表法

```java
// 使用 HexDigits.put4() 的原始实现
@Override
public String toString() {
    byte[] buf = new byte[36];
    HexDigits.put4(buf, 0, i0 >> 16);
    HexDigits.put4(buf, 4, i0);
    buf[8] = '-';
    HexDigits.put4(buf, 9, i1 >> 16);
    // ... 8 次 put4 调用
    return jla.newStringNoRepl(buf, StandardCharsets.ISO_8859_1);
}
```

**查找表结构**:
- `DIGITS[256]` - 存储 0x00-0xFF 的十六进制字符串
- 每次 `put4` 需要 4 次数组访问
- 缓存未命中风险

### 第一次优化：hex8 向量化

**提交**: [4f54ac68](https://github.com/openjdk/jdk/commit/4f54ac68a9f)
**作者**: [Shaojin Wen (温绍锦)](../../by-contributor/profiles/shaojin-wen.md)
**时间**: 2025-01-15

核心思想：使用 `long` 类型模拟 SIMD 向量运算，一次处理 8 个十六进制数字。

```java
private static long hex8(long i) {
    // 1. 扩展位: 0xAABBCCDD -> 0xA0A0B0B0C0C0D0D
    i = Long.expand(i, 0x0F0F_0F0F_0F0F_0F0FL);

    // 2. 检测 a-f 字符 (使用进位标志)
    long m = (i + 0x0606_0606_0606_0606L) & 0x1010_1010_1010_1010L;

    // 3. 计算 ASCII 偏移并反转字节序
    return Long.reverseBytes(
        ((m << 1) + (m >> 1) - (m >> 4))
        + 0x3030_3030_3030_3030L
        + i
    );
}
```

**优化效果**:
- 函数调用: 8 次 → 4 次
- 内存访问: 24+ 次 → 4 次
- 分支预测: 多次分支 → 无分支

### 循环展开优化

**提交**: [adb50724](https://github.com/openjdk/jdk/commit/adb50724a65)
**作者**: Kieran Farrell
**时间**: 2025-06-27

小优化，减少循环开销：

```java
// 展开 put4 调用
HexDigits.put4(buf, 0, i0 >> 16);
HexDigits.put4(buf, 4, i0);
// 而非循环调用
```

### 最终优化：消除查找表

**Issue**: [JDK-8353741](https://bugs.openjdk.org/browse/JDK-8353741)
**提交**: [796ec5e7cfc](https://github.com/openjdk/jdk/commit/796ec5e7cfc)
**作者**: [Shaojin Wen (温绍锦)](../../by-contributor/profiles/shaojin-wen.md)
**审查**: Ron Pressler
**时间**: 2025-05-22

完全移除 `HexDigits` 依赖，内联 `hex8` 到 `UUID` 类：

```java
@Override
public String toString() {
    byte[] buf = new byte[36];
    buf[8] = '-';
    buf[13] = '-';
    buf[18] = '-';
    buf[23] = '-';

    // 使用 ByteArrayLittleEndian 优化写入
    ByteArrayLittleEndian.setLong(buf, 0, hex8(mostSigBits >>> 32));
    long x0 = hex8(mostSigBits);
    ByteArrayLittleEndian.setInt(buf, 9, (int) x0);
    ByteArrayLittleEndian.setInt(buf, 14, (int) (x0 >>> 32));
    // ...

    return jla.uncheckedNewStringWithLatin1Bytes(buf);
}
```

**关键改进**:
1. 内联 `hex8` 消除方法调用开销
2. 使用 `ByteArrayLittleEndian` 优化 x86/ARM 等常见架构
3. 使用 `uncheckedNewStringWithLatin1Bytes` 跳过异常检查

---

## 6. 算法原理

### ASCII 十六进制字符规律

```
十进制  十六进制  ASCII   二进制
0       0        0x30    0011_0000
1       1        0x31    0011_0001
...
9       9        0x39    0011_1001
10      a        0x61    0110_0001  ← 差距 39
11      b        0x62    0110_0010
...
15      f        0x66    0110_0110
```

**关键观察**:
- `0-9`: 直接加 `0x30`
- `a-f`: 需要额外加 `39`

### 向量化转换算法

```
输入: 0xAB (10, 11)

步骤 1: 扩展位 (Long.expand)
  0xAB -> 0x0A0B

步骤 2: 加 6 检测 a-f
  0x0A0B + 0x0606 = 0x1011

步骤 3: 提取进位标志
  0x1011 & 0x1010 = 0x1010
  └─ 第 8 位和 12 位为 1 → 对应 a 和 b

步骤 4: 计算偏移
  m = 0x1010
  (m << 1) + (m >> 1) - (m >> 4)
  = 0x2020 + 0x0808 - 0x0101
  = 0x2727  (每字节 = 39)

步骤 5: 组合最终结果
  0x2727 + 0x3030 + 0x0A0B = 0x6162
  = 'a' | ('b' << 8)
```

### Long.expand() 原理

```java
// JDK 21+ 新增方法
public static long expand(long i, long mask) {
    // 将每个 4 位组扩展为 8 位
    // mask 指定哪些位需要扩展
    // 例如: expand(0xABCD, 0x0F0F) = 0x0A0B0C0D
}
```

这实际上是在硬件层面使用 SIMD 指令（如 x86 的 BMI2 指令集）。

---

## 7. 性能对比

### 基准测试结果 (JMH)

| 实现 | 吞吐量 (ops/ms) | 相对提升 | 分支数 | 内存访问 |
|------|-----------------|----------|--------|----------|
| 原始查表法 | ~2000 | 基准 | 16+ | 24+ |
| hex8 初版 | ~3500 | +75% | 0 | 4 |
| 最终版本 | ~4000+ | +100%+ | 0 | 4 |

### CPU 指令效率

| 操作 | 原始 | 优化后 |
|------|------|--------|
| 数组加载 | 24+ | 0 |
| 分支预测 | 16+ | 0 |
| 位运算 | 16 | ~20 |
| 内存写入 | 36 | 36 |
| 总指令数 | ~150 | ~80 |

### 不同场景表现

| 场景 | 原始 | 优化后 | 提升 |
|------|------|--------|------|
| 批量 UUID 转字符串 | 基准 | +100% | 吞吐量翻倍 |
| 日志输出 | 基准 | +30% | GC 压力降低 |
| 分布式追踪 | 基准 | +50% | 序列化加速 |

---

## 8. 贡献者

### 主要贡献者

| 贡献者 | 贡献 | Issue/PR |
|--------|------|----------|
| **Shaojin Wen (温绍锦)** | hex8 SIMD 算法、消除查找表 | [JDK-8353741](https://bugs.openjdk.org/browse/JDK-8353741) |
| **Kieran Farrell** | UUIDv7 支持、循环展开 | [JDK-8334015](https://bugs.openjdk.org/browse/JDK-8334015) |
| **Aleksey Shipilev** | Compact Strings 适配 | [JDK-8148936](https://bugs.openjdk.org/browse/JDK-8148936) |
| **Claes Redestad** | fromString() 优化 | [JDK-8196334](https://bugs.openjdk.org/browse/JDK-8196334) |
| **Roger Riggs** | 清理、术语规范 | [JDK-8370910](https://bugs.openjdk.org/browse/JDK-8370910) |
| **Volkan Yazıcı** | JavaLangAccess API 重构 | [JDK-8353197](https://bugs.openjdk.org/browse/JDK-8353197) |
| **liach** | HexDigits 优化建议 | - |

### 审查者

- Ron Pressler - JDK-8353741 审查
- [Roger Riggs](../../by-contributor/profiles/roger-riggs.md) - 多次 PR 审查

---

## 9. 参考资料

### 相关 Issue 和 PR

- [JDK-8353741: Eliminate table lookup in UUID.toString](https://bugs.openjdk.org/browse/JDK-8353741)
- [JDK-8334015: Add Support for UUID Version 7](https://bugs.openjdk.org/browse/JDK-8334015)
- [JDK-8148936: Adapt UUID.toString() to Compact Strings](https://bugs.openjdk.org/browse/JDK-8148936)
- [JDK-8196334: Optimize UUID#fromString](https://bugs.openjdk.org/browse/JDK-8196334)

### OpenJDK 提交

```bash
# 核心优化
4f54ac68a9f - optimization for uuid toString
796ec5e7cfc - 8353741: Eliminate table lookup in UUID.toString
adb50724a65 - unroll loop

# 早期工作
24816037ab2 - 8148936: Adapt UUID.toString() to Compact Strings
ebadfaeb2e1 - 8196334: Optimize UUID#fromString
```

### 技术文档

- [Long.expand() JavaDoc](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Long.html#expand(long,int))
- [ByteArrayLittleEndian](https://github.com/openjdk/jdk/blob/master/src/java.base/share/classes/jdk/internal/util/ByteArrayLittleEndian.java)
- [UUID.java 源码](https://github.com/openjdk/jdk/blob/master/src/java.base/share/classes/java/util/UUID.java)

### 相关文章

- [String 拼接优化](../../string/optimization.md)
- [Compact Strings (JEP 254)](/jeps/language/jep-254.md)
- [性能优化时间线](../../core/performance/timeline.md)

---

**最后更新**: 2026-03-20

**贡献者档案**:
- [Shaojin Wen (温绍锦)](../../by-contributor/profiles/shaojin-wen.md)
- [Claes Redestad](../../by-contributor/profiles/claes-redestad.md)
- Kieran Farrell
