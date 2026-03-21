# Vector API 使用指南

> 详细使用示例和最佳实践

[← 返回 Vector API](./)

---

## 目录

1. [基础使用](#基础使用)
2. [常用操作](#常用操作)
3. [高级特性](#高级特性)
4. [性能优化](#性能优化)
5. [常见问题](#常见问题)

---

## 基础使用

### 环境配置

**Maven 依赖** (不需要额外依赖，JDK 内置):

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <version>3.11.0</version>
    <configuration>
        <release>21</release>
        <compilerArgs>
            <arg>--add-modules</arg>
            <arg>jdk.incubator.vector</arg>
        </compilerArgs>
    </configuration>
</plugin>
```

**命令行编译运行**:

```bash
# 编译
javac --add-modules jdk.incubator.vector --release 21 VectorDemo.java

# 运行
java --add-modules jdk.incubator.vector VectorDemo
```

### 第一个向量程序

```java
import jdk.incubator.vector.*;

public class VectorAdd {
    static final VectorSpecies<Float> SPECIES = FloatVector.SPECIES_PREFERRED;
    
    public static void main(String[] args) {
        float[] a = {1.0f, 2.0f, 3.0f, 4.0f, 5.0f, 6.0f, 7.0f, 8.0f};
        float[] b = {10.0f, 20.0f, 30.0f, 40.0f, 50.0f, 60.0f, 70.0f, 80.0f};
        float[] c = new float[8];
        
        // 向量加法
        for (int i = 0; i < a.length; i += SPECIES.length()) {
            FloatVector va = FloatVector.fromArray(SPECIES, a, i);
            FloatVector vb = FloatVector.fromArray(SPECIES, b, i);
            FloatVector vc = va.add(vb);
            vc.intoArray(c, i);
        }
        
        // 输出: [11.0, 22.0, 33.0, 44.0, 55.0, 66.0, 77.0, 88.0]
        System.out.println(java.util.Arrays.toString(c));
    }
}
```

### 向量种类 (Species)

```java
// 获取最优种类 (取决于 CPU)
VectorSpecies<Float> preferred = FloatVector.SPECIES_PREFERRED;

// 指定位宽
VectorSpecies<Float> s64 = FloatVector.SPECIES_64;    // 2 floats
VectorSpecies<Float> s128 = FloatVector.SPECIES_128;  // 4 floats
VectorSpecies<Float> s256 = FloatVector.SPECIES_256;  // 8 floats
VectorSpecies<Float> s512 = FloatVector.SPECIES_512;  // 16 floats

// 查询信息
System.out.println("向量长度: " + preferred.length());  // 例如: 8
System.out.println("位宽: " + preferred.vectorBitSize());  // 例如: 256
System.out.println("字节: " + preferred.vectorByteSize());  // 例如: 32
```

---

## 常用操作

### 数组处理模式

```java
static final VectorSpecies<Float> SPECIES = FloatVector.SPECIES_PREFERRED;

void processArray(float[] data) {
    int i = 0;
    int bound = SPECIES.loopBound(data.length);  // 对齐边界
    
    // 向量化处理主体
    for (; i < bound; i += SPECIES.length()) {
        FloatVector v = FloatVector.fromArray(SPECIES, data, i);
        // ... 处理 v ...
        v.intoArray(data, i);
    }
    
    // 标量处理尾部
    for (; i < data.length; i++) {
        // ... 处理 data[i] ...
    }
}
```

### SAXPY (Scalar A * X Plus Y)

```java
void saxpy(float[] a, float[] x, float[] y, float alpha) {
    int i = 0;
    int bound = SPECIES.loopBound(a.length);
    
    for (; i < bound; i += SPECIES.length()) {
        FloatVector vx = FloatVector.fromArray(SPECIES, x, i);
        FloatVector vy = FloatVector.fromArray(SPECIES, y, i);
        vx.mul(alpha).add(vy).intoArray(a, i);
    }
    
    for (; i < a.length; i++) {
        a[i] = alpha * x[i] + y[i];
    }
}
```

### 点积 (Dot Product)

```java
float dotProduct(float[] a, float[] b) {
    int i = 0;
    int bound = SPECIES.loopBound(a.length);
    FloatVector sum = FloatVector.zero(SPECIES);
    
    for (; i < bound; i += SPECIES.length()) {
        FloatVector va = FloatVector.fromArray(SPECIES, a, i);
        FloatVector vb = FloatVector.fromArray(SPECIES, b, i);
        sum = sum.add(va.mul(vb));
    }
    
    float result = sum.reduceLanes(VectorOperators.ADD);
    
    for (; i < a.length; i++) {
        result += a[i] * b[i];
    }
    
    return result;
}
```

### 向量归一化

```java
void normalize(float[] vectors, int stride) {
    VectorSpecies<Float> species = FloatVector.SPECIES_PREFERRED;
    
    for (int i = 0; i < vectors.length; i += stride) {
        float sum = 0;
        for (int j = 0; j < stride; j++) {
            sum += vectors[i + j] * vectors[i + j];
        }
        float invLen = 1.0f / (float) Math.sqrt(sum);
        
        int j = 0;
        int bound = species.loopBound(stride);
        for (; j < bound; j += species.length()) {
            FloatVector v = FloatVector.fromArray(species, vectors, i + j);
            v.mul(invLen).intoArray(vectors, i + j);
        }
        for (; j < stride; j++) {
            vectors[i + j] *= invLen;
        }
    }
}
```

### 条件处理

```java
void conditionalAdd(float[] a, float[] b, float[] c, float threshold) {
    int i = 0;
    int bound = SPECIES.loopBound(a.length);
    
    for (; i < bound; i += SPECIES.length()) {
        FloatVector va = FloatVector.fromArray(SPECIES, a, i);
        FloatVector vb = FloatVector.fromArray(SPECIES, b, i);
        
        // 创建掩码: a[i] > threshold
        VectorMask<Float> mask = va.compare(VectorOperators.GT, threshold);
        
        // 只在 mask=true 的位置相加
        FloatVector vc = va.add(vb, mask);
        vc.intoArray(c, i);
    }
    
    for (; i < a.length; i++) {
        c[i] = a[i] > threshold ? a[i] + b[i] : a[i];
    }
}
```

---

## 高级特性

### 向量重排 (Shuffle)

```java
void reverseArray(float[] data) {
    VectorSpecies<Float> species = FloatVector.SPECIES_PREFERRED;
    
    // 创建反转 shuffle
    VectorShuffle<Float> reverse = species.laneReversingShuffle();
    
    int i = 0;
    int bound = species.loopBound(data.length);
    
    for (; i < bound; i += species.length()) {
        FloatVector v = FloatVector.fromArray(species, data, i);
        v.rearrange(reverse).intoArray(data, i);
    }
}
```

### 跨向量操作

```java
void slideWindow(float[] data, float[] output) {
    VectorSpecies<Float> species = FloatVector.SPECIES_PREFERRED;
    
    for (int i = 0; i < data.length - species.length(); i += 1) {
        FloatVector v1 = FloatVector.fromArray(species, data, i);
        FloatVector v2 = FloatVector.fromArray(species, data, i + 1);
        
        // 从两个向量中切片组合
        FloatVector result = v1.slice(1, v2);
        result.intoArray(output, i);
    }
}
```

### 类型转换

```java
void convertTypes(int[] ints, float[] floats) {
    VectorSpecies<Integer> iSpecies = IntVector.SPECIES_PREFERRED;
    VectorSpecies<Float> fSpecies = FloatVector.SPECIES_PREFERRED;
    
    int i = 0;
    int bound = iSpecies.loopBound(ints.length);
    
    for (; i < bound; i += iSpecies.length()) {
        IntVector iv = IntVector.fromArray(iSpecies, ints, i);
        // 整数转浮点
        FloatVector fv = iv.convert(VectorOperators.I2F, fSpecies);
        fv.intoArray(floats, i);
    }
}
```

### 与 ByteBuffer 交互

```java
import java.nio.ByteBuffer;
import java.nio.ByteOrder;

void processByteBuffer(ByteBuffer buffer) {
    VectorSpecies<Float> species = FloatVector.SPECIES_PREFERRED;
    int floatCount = buffer.remaining() / 4;
    
    int i = 0;
    int bound = species.loopBound(floatCount);
    
    for (; i < bound; i += species.length()) {
        FloatVector v = FloatVector.fromByteBuffer(
            species, buffer, i * 4, ByteOrder.LITTLE_ENDIAN);
        // ... 处理 v ...
        v.intoByteBuffer(buffer, i * 4, ByteOrder.LITTLE_ENDIAN);
    }
}
```

### 使用 MemorySegment (JDK 19+)

```java
import java.lang.foreign.*;

void processMemorySegment(MemorySegment segment) {
    VectorSpecies<Float> species = FloatVector.SPECIES_PREFERRED;
    long floatCount = segment.byteSize() / 4;

    long i = 0;
    long bound = species.loopBound(floatCount);

    for (; i < bound; i += species.length()) {
        FloatVector v = FloatVector.fromMemorySegment(
            species, segment, i * 4, ByteOrder.nativeOrder());
        // ... 处理 v ...
        v.intoMemorySegment(segment, i * 4, ByteOrder.nativeOrder());
    }
}
```

### VectorShuffle 与 MemorySegment (JDK 26+)

```java
import java.lang.foreign.*;
import jdk.incubator.vector.*;

// JDK 26+: VectorShuffle 可以直接与 MemorySegment 交互
void shuffleWithMemorySegment(MemorySegment segment) {
    VectorSpecies<Integer> species = IntVector.SPECIES_256;
    
    // 从 MemorySegment 创建 Shuffle
    VectorShuffle<Integer> shuffle = VectorShuffle.fromArray(species, segment, 0);
    
    // 应用 Shuffle
    IntVector v = IntVector.fromArray(species, array, 0);
    IntVector shuffled = v.rearrange(shuffle);
    
    // 将 Shuffle 存储到 MemorySegment
    shuffle.intoMemorySegment(segment, 0, ByteOrder.nativeOrder());
}
```

---

## 性能优化

### 1. 选择合适的 Species

```java
// ❌ 硬编码可能不是最优
VectorSpecies<Float> s256 = FloatVector.SPECIES_256;

// ✅ 让 JVM 选择最优
VectorSpecies<Float> preferred = FloatVector.SPECIES_PREFERRED;

// ✅ 根据数据量动态选择
VectorSpecies<Float> species = data.length < 16 
    ? FloatVector.SPECIES_128 
    : FloatVector.SPECIES_PREFERRED;
```

### 2. 数据对齐

```java
// ✅ 64 字节对齐 (AVX-512 友好)
float[] aligned = new float[1024];  // 确保大小是 16 的倍数

// ❌ 未对齐数据可能影响性能
float[] unaligned = new float[1003];
```

### 3. 避免频繁创建 Species

```java
// ❌ 每次循环都查询
for (int i = 0; i < n; i += FloatVector.SPECIES_PREFERRED.length()) { ... }

// ✅ 缓存 Species
static final VectorSpecies<Float> SPECIES = FloatVector.SPECIES_PREFERRED;
for (int i = 0; i < n; i += SPECIES.length()) { ... }
```

### 4. 循环展开

```java
void optimizedLoop(float[] a, float[] b, float[] c) {
    int i = 0;
    int bound = SPECIES.loopBound(a.length);
    
    // 4x 展开减少循环开销
    for (; i < bound - SPECIES.length() * 3; i += SPECIES.length() * 4) {
        FloatVector va0 = FloatVector.fromArray(SPECIES, a, i);
        FloatVector vb0 = FloatVector.fromArray(SPECIES, b, i);
        FloatVector va1 = FloatVector.fromArray(SPECIES, a, i + SPECIES.length());
        FloatVector vb1 = FloatVector.fromArray(SPECIES, b, i + SPECIES.length());
        FloatVector va2 = FloatVector.fromArray(SPECIES, a, i + SPECIES.length() * 2);
        FloatVector vb2 = FloatVector.fromArray(SPECIES, b, i + SPECIES.length() * 2);
        FloatVector va3 = FloatVector.fromArray(SPECIES, a, i + SPECIES.length() * 3);
        FloatVector vb3 = FloatVector.fromArray(SPECIES, b, i + SPECIES.length() * 3);
        
        va0.add(vb0).intoArray(c, i);
        va1.add(vb1).intoArray(c, i + SPECIES.length());
        va2.add(vb2).intoArray(c, i + SPECIES.length() * 2);
        va3.add(vb3).intoArray(c, i + SPECIES.length() * 3);
    }
    
    // 处理剩余
    for (; i < bound; i += SPECIES.length()) {
        FloatVector va = FloatVector.fromArray(SPECIES, a, i);
        FloatVector vb = FloatVector.fromArray(SPECIES, b, i);
        va.add(vb).intoArray(c, i);
    }
    
    // 尾部
    for (; i < a.length; i++) {
        c[i] = a[i] + b[i];
    }
}
```

### 5. 性能测试

```java
import java.util.concurrent.TimeUnit;

void benchmark(float[] a, float[] b) {
    // 预热
    for (int i = 0; i < 10000; i++) {
        vectorAdd(a, b);
    }
    
    // 测试
    long start = System.nanoTime();
    int iterations = 100000;
    for (int i = 0; i < iterations; i++) {
        vectorAdd(a, b);
    }
    long elapsed = System.nanoTime() - start;
    
    double ms = TimeUnit.NANOSECONDS.toMillis(elapsed);
    System.out.printf("平均耗时: %.3f ms%n", ms / iterations);
}
```

---

## 常见问题

### Q: 为什么向量版本有时更慢?

**可能原因**:
1. 数据量太小 - 向量化开销超过收益
2. 未对齐访问 - 内存不对齐导致性能下降
3. 频繁装箱/拆箱 - 使用原始类型数组
4. 缓存未命中 - 确保数据局部性

**解决方案**:
```java
// 检查向量宽度
if (SPECIES.length() < 4) {
    // 使用标量版本
    scalarMethod(data);
} else {
    vectorMethod(data);
}
```

### Q: 如何调试向量代码?

```java
// 打印向量内容
FloatVector v = ...;
float[] temp = v.toArray();
System.out.println(Arrays.toString(temp));

// 检查 mask
VectorMask<Float> mask = ...;
System.out.println(mask.toString());

// 打印向量指令
// JVM 参数: -XX:+UnlockDiagnosticVMOptions -XX:+PrintAssembly
```

### Q: Incubator API 会变怎么办?

**策略**:
1. 封装 API 变更
2. 使用多版本 JAR
3. 关注 JEP 更新

```java
// 封装示例
public interface VectorOps {
    float[] add(float[] a, float[] b);
}

// JDK 16-18 实现
public class VectorOps16 implements VectorOps {
    // JDK 16 API
}

// JDK 19+ 实现
public class VectorOps19 implements VectorOps {
    // JDK 19 API (如有变更)
}
```

### Q: 如何处理可变长度向量 (SVE)?

```java
// ARM SVE 支持可变长度
VectorSpecies<Float> species = FloatVector.SPECIES_PREFERRED;

// 运行时确定长度
int length = species.length();  // 可能是 4, 8, 16, 32...

// 代码无需修改，自动适应
for (int i = 0; i < bound; i += species.length()) {
    // ...
}
```

### Q: 与 Stream API 如何结合?

```java
// 目前不直接支持，需要手动并行化
IntStream.range(0, chunks).parallel().forEach(chunk -> {
    int start = chunk * chunkSize;
    int end = Math.min(start + chunkSize, data.length);
    vectorProcess(data, start, end);
});
```

---

## 完整示例: 矩阵乘法

```java
import jdk.incubator.vector.*;

public class MatrixMultiply {
    static final VectorSpecies<Float> SPECIES = FloatVector.SPECIES_PREFERRED;
    
    public static void multiply(float[][] A, float[][] B, float[][] C) {
        int n = A.length;
        int m = B[0].length;
        int k = A[0].length;
        
        // 转置 B 以便向量化
        float[][] BT = transpose(B);
        
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                C[i][j] = dotProduct(A[i], BT[j]);
            }
        }
    }
    
    private static float dotProduct(float[] a, float[] b) {
        int i = 0;
        int bound = SPECIES.loopBound(a.length);
        FloatVector sum = FloatVector.zero(SPECIES);
        
        for (; i < bound; i += SPECIES.length()) {
            FloatVector va = FloatVector.fromArray(SPECIES, a, i);
            FloatVector vb = FloatVector.fromArray(SPECIES, b, i);
            sum = sum.add(va.mul(vb));
        }
        
        float result = sum.reduceLanes(VectorOperators.ADD);
        
        for (; i < a.length; i++) {
            result += a[i] * b[i];
        }
        
        return result;
    }
    
    private static float[][] transpose(float[][] m) {
        int rows = m.length;
        int cols = m[0].length;
        float[][] t = new float[cols][rows];
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                t[j][i] = m[i][j];
            }
        }
        return t;
    }
}
```

---

## 更多示例

### 图像处理: 亮度调整

```java
void adjustBrightness(byte[] pixels, float factor) {
    VectorSpecies<Byte> species = ByteVector.SPECIES_PREFERRED;
    int i = 0;
    int bound = species.loopBound(pixels.length);
    
    for (; i < bound; i += species.length()) {
        ByteVector v = ByteVector.fromArray(species, pixels, i);
        // 转换为 short 避免溢出
        ShortVector vs = v.convert(VectorOperators.B2S, ShortVector.SPECIES_PREFERRED);
        vs = vs.mul(factor);
        vs = vs.min(255).max(0);
        v = vs.convert(VectorOperators.S2B, species);
        v.intoArray(pixels, i);
    }
    
    for (; i < pixels.length; i++) {
        int val = (int)(pixels[i] & 0xFF) * factor;
        pixels[i] = (byte)Math.min(255, Math.max(0, val));
    }
}
```

### 字符串处理: 大小写转换

```java
void toUpperCase(byte[] ascii) {
    VectorSpecies<Byte> species = ByteVector.SPECIES_PREFERRED;
    byte diff = (byte)('a' - 'A');
    
    int i = 0;
    int bound = species.loopBound(ascii.length);
    
    for (; i < bound; i += species.length()) {
        ByteVector v = ByteVector.fromArray(species, ascii, i);
        
        // mask: 'a' <= c <= 'z'
        VectorMask<Byte> isLower = v.compare(VectorOperators.GE, (byte)'a')
                                  .and(v.compare(VectorOperators.LE, (byte)'z'));
        
        v = v.sub(diff, isLower);
        v.intoArray(ascii, i);
    }
    
    for (; i < ascii.length; i++) {
        if (ascii[i] >= 'a' && ascii[i] <= 'z') {
            ascii[i] -= diff;
        }
    }
}
```

---

> **最后更新**: 2026-03-21
