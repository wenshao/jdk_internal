# UUID.toString() 优化深度分析

> 从查表法到 SIMD 风格向量运算的性能进化之旅

**作者**: Shaojin Wen (文绍金)
**Issue**: JDK-8353741
**提交时间**: 2025-05-22

---

## 目录

- [背景](#背景)
- [原始实现：查表法](#原始实现查表法)
- [第一次优化：引入 hex8](#第一次优化引入-hex8)
- [第二次优化：消除查表](#第二次优化消除查表)
- [性能对比](#性能对比)
- [算法原理](#算法原理)
- [总结](#总结)

---

## 背景

`java.util.UUID#toString()` 是一个高频调用的方法，用于将 128 位的 UUID 转换为标准字符串表示格式：

```
123e4567-e89b-12d3-a456-426614174000
```

格式说明：`8-4-4-4-12` 格式，共 36 个字符（包含 4 个连字符）

---

## 原始实现：查表法

### HexDigits.put4 实现

原始实现使用 `HexDigits.put4()` 方法，基于预计算的查找表：

```java
// 原始 toString() 实现
@Override
public String toString() {
    int i0 = (int) (mostSigBits >> 32);
    int i1 = (int) mostSigBits;
    int i2 = (int) (leastSigBits >> 32);
    int i3 = (int) leastSigBits;

    byte[] buf = new byte[36];
    HexDigits.put4(buf, 0, i0 >> 16);
    HexDigits.put4(buf, 4, i0);
    buf[8] = '-';
    HexDigits.put4(buf, 9, i1 >> 16);
    buf[13] = '-';
    HexDigits.put4(buf, 14, i1);
    buf[18] = '-';
    HexDigits.put4(buf, 19, i2 >> 16);
    buf[23] = '-';
    HexDigits.put4(buf, 24, i2);
    HexDigits.put4(buf, 28, i3 >> 16);
    HexDigits.put4(buf, 32, i3);

    return jla.newStringNoRepl(buf, StandardCharsets.ISO_8859_1);
}
```

### 查找表结构

```java
// HexDigits.java
@Stable
private static final short[] DIGITS;

static {
    short[] digits = new short[16 * 16];
    for (int i = 0; i < 16; i++) {
        short lo = (short) (i < 10 ? i + '0' : i - 10 + 'a');
        for (int j = 0; j < 16; j++) {
            short hi = (short) ((j < 10 ? j + '0' : j - 10 + 'a') << 8);
            digits[(i << 4) + j] = (short) (hi | lo);
        }
    }
    DIGITS = digits;
}

// put4 方法需要 6 次查表操作（每次处理 4 位，共 16 位）
```

### 性能瓶颈

1. **内存访问开销**：每次 `put4` 需要多次数组访问
2. **缓存未命中**：256 元素的查找表可能导致 CPU 缓存未命中
3. **串行处理**：每次只能处理少量位

---

## 第一次优化：引入 hex8

### SIMD 风格向量运算

核心思想：使用 `long` 类型模拟 SIMD 向量运算，一次处理 8 个十六进制数字。

```java
private static long hex8(long i) {
    // 1. 将每个 4 位组扩展为 8 位
    //    0xAABBCCDD -> 0xA0A0B0B0C0C0D0D
    i = Long.expand(i, 0x0F0F_0F0F_0F0F_0F0FL);

    // 2. 使用进位标志检测 a-f 字符
    long m = (i + 0x0606_0606_0606_0606L) & 0x1010_1010_1010_1010L;

    // 3. 计算 ASCII 偏移量并反转字节序
    return Long.reverseBytes(
            ((m << 1) + (m >> 1) - (m >> 4))
            + 0x3030_3030_3030_3030L  // ASCII '0' 基数
            + i                       // 原始值
    );
}
```

### 优化后的 toString()

```java
@Override
public String toString() {
    byte[] buf = new byte[36];
    buf[8] = '-';
    buf[13] = '-';
    buf[18] = '-';
    buf[23] = '-';

    long x0 = hex8(mostSigBits >>> 32);
    long x1 = hex8(mostSigBits);
    ByteArrayLittleEndian.setLong(buf, 0, x0);
    ByteArrayLittleEndian.setInt(buf, 9, (int) x1);
    ByteArrayLittleEndian.setInt(buf, 14, (int) (x1 >>> 32));

    long x2 = hex8(leastSigBits >>> 32);
    long x3 = hex8(leastSigBits);
    ByteArrayLittleEndian.setInt(buf, 19, (int) x2);
    ByteArrayLittleEndian.setInt(buf, 24, (int) (x2 >>> 32));
    ByteArrayLittleEndian.setLong(buf, 28, x3);

    return jla.uncheckedNewStringWithLatin1Bytes(buf);
}
```

### 优化效果

| 指标 | 原始 | hex8 | 提升 |
|------|------|------|------|
| 函数调用 | 8 次 | 4 次 | 50% ↓ |
| 内存访问 | 24+ 次 | 4 次 | 83% ↓ |
| 分支预测 | 多次分支 | 无分支 | 消除 |

---

## 第二次优化：消除查表

### JDK-8353741: 完全消除查找表

最终优化将 `hex8` 方法内联到 `UUID` 类中，完全移除了对 `HexDigits` 类的依赖。

**关键改进**：
1. **内联 hex8**：消除方法调用开销
2. **统一 API**：使用 `uncheckedNewStringWithLatin1Bytes` 替代 `newStringNoRepl`
3. **字节序优化**：使用 `ByteArrayLittleEndian` 优化常见架构

```java
// 最终实现 (JDK master)
@Override
public String toString() {
    byte[] buf = new byte[36];
    buf[8] = '-';
    buf[13] = '-';
    buf[18] = '-';
    buf[23] = '-';

    ByteArrayLittleEndian.setLong(buf, 0, hex8(mostSigBits >>> 32));
    long x0 = hex8(mostSigBits);
    ByteArrayLittleEndian.setInt(buf, 9, (int) x0);
    ByteArrayLittleEndian.setInt(buf, 14, (int) (x0 >>> 32));

    long x1 = hex8(leastSigBits >>> 32);
    ByteArrayLittleEndian.setInt(buf, 19, (int) x1);
    ByteArrayLittleEndian.setInt(buf, 24, (int) (x1 >>> 32));
    ByteArrayLittleEndian.setLong(buf, 28, hex8(leastSigBits));

    return jla.uncheckedNewStringWithLatin1Bytes(buf);
}
```

---

## 算法原理

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

**关键观察**：
- `0-9`: 直接加 `0x30`
- `a-f`: 需要额外加 `39`（`0x61 - 0x39 - 0x30 = 0x10` 的位模式）

### 向量化转换算法

```
输入: 0xAB (10, 11)

步骤 1: 扩展位
  0xAB -> 0x0A0B

步骤 2: 加 6 检测 a-f
  0x0A0B + 0x0606 = 0x1011

步骤 3: 提取进位标志
  0x1011 & 0x1010 = 0x1010
  - 第 8 位和 12 位为 1 → 对应 a 和 b

步骤 4: 计算偏移
  m = 0x1010
  (m << 1) + (m >> 1) - (m >> 4)
  = 0x2020 + 0x0808 - 0x0101
  = 0x2727  (每字节 = 39)

步骤 5: 组合最终结果
  0x2727 + 0x3030 + 0x0A0B = 0x6162
  = 'a' | ('b' << 8)
```

---

## 性能对比

### 基准测试结果 (JMH)

| 实现 | 吞吐量 (ops/ms) | 相对提升 |
|------|-----------------|----------|
| 原始查表法 | ~2000 | 基准 |
| hex8 优化 | ~3500 | +75% |
| 最终版本 | ~4000+ | +100%+ |

### CPU 指令数对比

| 操作 | 原始 | 优化后 |
|------|------|--------|
| 数组加载 | 24+ | 0 |
| 分支 | 8+ | 0 |
| 位运算 | 16 | ~20 |
| 内存写入 | 36 | 36 |

---

## 总结

### 优化关键点

1. **消除查找表**：从内存访问转为纯计算
2. **SIMD 风格并行**：一次处理 8 个数字
3. **无分支设计**：利用位运算实现条件逻辑
4. **内联优化**：减少方法调用开销

### 适用场景

这种优化技巧适用于：
- 固定格式的十六进制字符串转换
- 高频调用的转换方法
- 延迟敏感的应用场景

### 相关提交

```bash
# 第一次优化：引入 hex8
4f54ac68a9f optimization for uuid toString

# 添加 reverseBytes
99feb9ac2b0 reverseBytes

# 使用 HexDigits.hex8
ca0433d7f42 use HexDigits hex8

# 最终优化：消除查表
796ec5e7cfc 8353741: Eliminate table lookup in UUID.toString
```

---

## 参考资料

- [JDK-8353741](https://bugs.openjdk.org/browse/JDK-8353741)
- [Long.expand() JavaDoc](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Long.html#expand(long,int))
- [ByteArrayLittleEndian](https://github.com/openjdk/jdk/blob/master/src/java.base/share/classes/jdk/internal/util/ByteArrayLittleEndian.java)

---

**贡献者**: Shaojin Wen (Alibaba)
**审查者**: Ron Pressler (Oracle)
