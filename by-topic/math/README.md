# 数学计算

> BigDecimal, Math, Random, StrictMath, HexFormat, Vector API 数学运算演进历程

[← 返回主题索引](../)

---

## 1. 快速概览

```
JDK 1.0 ── JDK 1.2 ── JDK 8 ── JDK 9 ── JDK 17 ── JDK 21 ── JDK 22+
   │        │          │        │        │         │        │
Math     StrictMath  Splittable SecureRandom HexFormat  Math    Vector API
类       精确数学    Random    DRBG增强   RandomGen  .clamp  数学加速
BigDecimal           (JEP 193) (JEP 273)  (JEP 356)    -
```

### 核心演进

| 版本 | 特性 | JEP | 说明 |
|------|------|-----|------|
| **JDK 1.0** | Math, Random, BigDecimal, BigInteger | - | 基础数学函数与大数运算 |
| **JDK 1.2** | StrictMath, strictfp | - | 跨平台浮点一致性 |
| **JDK 7** | ThreadLocalRandom | - | 线程局部随机数 |
| **JDK 8** | SplittableRandom | JEP 193 | 可分割随机数 |
| **JDK 9** | SecureRandom DRBG | JEP 273 | 密码学安全随机数增强 |
| **JDK 17** | JEP 306: strictfp 恢复 | JEP 306 | 默认 strict 浮点语义 |
| **JDK 17** | RandomGenerator, HexFormat | JEP 356 | 随机数统一接口 + 十六进制 |
| **JDK 21** | Math.clamp | - | 范围限制函数 (standalone API addition) |
| **JDK 22+** | fdlibm Java 移植 | - | Anton Artemov 的纯 Java 数学库 |

---

## 目录

- [Math 类](#2-math-类)
- [strictfp 与 JEP 306](#3-strictfp-与-jep-306)
- [StrictMath 与 fdlibm](#4-strictmath-与-fdlibm)
- [BigDecimal](#5-bigdecimal)
- [BigInteger](#6-biginteger)
- [Random 随机数演进](#7-random-随机数演进)
- [SecureRandom 与 DRBG](#8-securerandom-与-drbg)
- [HexFormat (JDK 17)](#9-hexformat-jdk-17)
- [Math.clamp (JDK 21)](#10-mathclamp-jdk-21)
- [向量化数学: Vector API](#11-向量化数学-vector-api)
- [最佳实践](#12-最佳实践)
- [核心贡献者](#13-核心贡献者)
- [相关链接](#14-相关链接)

---

## 2. Math 类

### 基本数学函数 (Basic Math Functions)

`java.lang.Math` 提供常用的数学运算，内部实现委托给平台原生代码或 StrictMath。

```java
import java.lang.Math;

// 三角函数 (trigonometric functions)
double sin = Math.sin(Math.PI / 2);      // 1.0
double cos = Math.cos(0);                 // 1.0
double tan = Math.tan(Math.PI / 4);      // ≈1.0
double asin = Math.asin(1.0);            // π/2
double acos = Math.acos(0.0);            // π/2
double atan = Math.atan(1.0);            // π/4
double atan2 = Math.atan2(1.0, 1.0);    // π/4 (两参数版本)

// 双曲函数 (hyperbolic functions)
double sinh = Math.sinh(1.0);
double cosh = Math.cosh(1.0);
double tanh = Math.tanh(1.0);

// 指数和对数 (exponential & logarithmic)
double exp = Math.exp(1.0);              // e^1 ≈ 2.718
double expm1 = Math.expm1(0.001);       // e^x - 1，小值时精度更高
double log = Math.log(10.0);             // ln(10)
double log10 = Math.log10(100);          // 2.0
double log1p = Math.log1p(0.001);       // ln(1+x)，小值时精度更高
double pow = Math.pow(2, 10);            // 1024.0

// 取整 (rounding)
double ceil = Math.ceil(3.2);            // 4.0 (向正无穷)
double floor = Math.floor(3.8);          // 3.0 (向负无穷)
long round = Math.round(3.5);           // 4 (四舍五入)
double rint = Math.rint(2.5);           // 2.0 (banker's rounding，最近偶数)

// 其他常用 (miscellaneous)
double abs = Math.abs(-5.0);             // 5.0
int max = Math.max(1, 2);               // 2
int min = Math.min(1, 2);               // 1
double sign = Math.signum(-5.0);         // -1.0
double hypot = Math.hypot(3, 4);         // 5.0 (勾股定理，避免溢出)
double sqrt = Math.sqrt(16);             // 4.0
double cbrt = Math.cbrt(27);             // 3.0 (立方根)
```

### 常量 (Constants)

```java
System.out.println(Math.E);    // 2.718281828459045 (自然对数底数)
System.out.println(Math.PI);   // 3.141592653589793 (圆周率)
// JDK 19+: Math.TAU = 2 * Math.PI = 6.283185307179586
```

### 角度转换 (Angle Conversion)

```java
double degrees = Math.toDegrees(Math.PI);  // 180.0 (弧度 → 角度)
double radians = Math.toRadians(180.0);    // π (角度 → 弧度)
```

### 精确整数运算 (Exact Arithmetic, JDK 8+)

```java
// 溢出时抛出 ArithmeticException 而非静默回绕 (silent wraparound)
int sum = Math.addExact(Integer.MAX_VALUE, 1);       // ArithmeticException!
int diff = Math.subtractExact(Integer.MIN_VALUE, 1);  // ArithmeticException!
int prod = Math.multiplyExact(Integer.MAX_VALUE, 2);  // ArithmeticException!
int neg = Math.negateExact(Integer.MIN_VALUE);         // ArithmeticException!
long incr = Math.incrementExact(Long.MAX_VALUE);       // ArithmeticException!
long decr = Math.decrementExact(Long.MIN_VALUE);       // ArithmeticException!
int narrow = Math.toIntExact(Long.MAX_VALUE);          // ArithmeticException!

// JDK 9+: floorDiv / floorMod 支持 long
long fd = Math.floorDiv(-7L, 2L);    // -4 (向负无穷取整除法)
long fm = Math.floorMod(-7L, 2L);    // 1  (结果与除数同号)
```

### FMA (Fused Multiply-Add, JDK 9+)

```java
// a * b + c，一次舍入，精度更高
double result = Math.fma(a, b, c);   // IEEE 754 fused multiply-add
// 用于科学计算和矩阵运算，避免中间舍入
```

---

## 3. strictfp 与 JEP 306

### 背景

JDK 1.2 引入 `strictfp` 关键字，要求浮点运算严格遵循 IEEE 754。不标 `strictfp` 的代码允许使用扩展精度 (extended precision)，结果可能因平台而异。

### JEP 306: Restore Always-Strict Floating-Point Semantics (JDK 17)

现代硬件 (SSE2+) 已默认支持严格 IEEE 754 语义，不再有性能差异。JEP 306 将所有浮点运算恢复为 always-strict，`strictfp` 关键字实质上变为 no-op。

```java
// JDK 17 之前: strictfp 有实际意义
strictfp class StrictCalculation {
    double compute(double a, double b) {
        return a * b + a / b;  // 严格 IEEE 754
    }
}

// JDK 17+: strictfp 不再需要，所有运算默认严格
class Calculation {
    double compute(double a, double b) {
        return a * b + a / b;  // 已经是严格模式
    }
}
```

| 时期 | 默认行为 | strictfp 效果 |
|------|---------|--------------|
| JDK 1.0–1.1 | 严格 (strict) | 不存在 |
| JDK 1.2–16 | 宽松 (default) | 切换为严格 |
| JDK 17+ | 严格 (strict) | 无操作 (no-op) |

---

## 4. StrictMath 与 fdlibm

### StrictMath vs Math

| 特性 | Math | StrictMath |
|------|------|-----------|
| 实现 | 可委托给平台原生代码 | 必须使用 fdlibm 或等价算法 |
| 精度 | 同样 IEEE 754 (JDK 17+) | 跨平台 bit-for-bit 一致 |
| 性能 | 可使用硬件指令优化 | 通常较慢 |
| 用途 | 通用计算 | 跨平台可重现结果 |

**关键区别**: JDK 17+ 之后 `Math` 和 `StrictMath` 在浮点严格性上相同，但 `StrictMath` 保证 **算法层面** 跨平台一致 (bit-for-bit reproducible)，而 `Math` 可能因不同 JVM 实现使用不同的底层算法。

### fdlibm: C 数学库基础

StrictMath 的超越函数 (transcendental functions) 基于 **fdlibm** (Freely Distributable Math Library)，最初由 Sun 的 K.C. Ng 编写。

```java
// StrictMath.sin/cos/exp/log 等均使用 fdlibm 算法
// 保证结果在所有平台上 bit-for-bit 一致

StrictMath.sin(0.5);   // 所有平台返回完全相同的 double 值
StrictMath.exp(1.0);   // 所有平台返回完全相同的 double 值
```

### fdlibm 的 Java 移植 (Anton Artemov)

自 JDK 22 起，Anton Artemov (Oracle) 逐步将 fdlibm 的 C 实现移植为纯 Java 代码，消除 JNI 调用开销。

```
移植进度 (截至 JDK 24):
- Math.sin/cos/tan → 纯 Java (JDK 24)
- Math.exp/log     → 纯 Java
- Math.pow         → 纯 Java
- 其他函数         → 持续进行中
```

优势:
- 消除 JNI 调用开销 (JNI call overhead)
- 允许 JIT 进一步内联优化 (inlining)
- 便于 GraalVM 等 AOT 编译器处理
- 代码维护更容易

---

## 5. BigDecimal

### 基础使用

```java
import java.math.*;

// 创建 BigDecimal — 字符串构造是首选
BigDecimal a = new BigDecimal("123.456");
BigDecimal b = BigDecimal.valueOf(123.456);    // 内部先转为字符串
BigDecimal c = new BigDecimal(123.456789, MathContext.DECIMAL64);

// 避免 double 构造函数!
// new BigDecimal(0.1)  → 0.1000000000000000055511151231257827021181583404541015625
// new BigDecimal("0.1") → 0.1 (精确)
```

### 精度控制 (Precision Control)

```java
import java.math.MathContext;

// MathContext = precision (有效数字) + RoundingMode
MathContext mc32 = MathContext.DECIMAL32;    // 7 位有效数字, HALF_EVEN
MathContext mc64 = MathContext.DECIMAL64;    // 16 位有效数字, HALF_EVEN
MathContext mc128 = MathContext.DECIMAL128;  // 34 位有效数字, HALF_EVEN

// 自定义精度
MathContext custom = new MathContext(20, RoundingMode.HALF_UP);

// 精度贯穿运算
BigDecimal x = new BigDecimal("1.0").divide(
    new BigDecimal("3.0"), mc64
);  // 0.3333333333333333 (16 位)

// scale vs precision
// scale: 小数点后位数
// precision: 总有效数字位数
BigDecimal v = new BigDecimal("123.456");
v.scale();      // 3
v.precision();  // 6
```

### RoundingMode 详解

```java
import java.math.RoundingMode;

BigDecimal value = new BigDecimal("2.5");

// 8 种舍入模式
value.setScale(0, RoundingMode.UP);         // 3  — 远离零 (away from zero)
value.setScale(0, RoundingMode.DOWN);       // 2  — 趋向零 (toward zero, truncate)
value.setScale(0, RoundingMode.CEILING);    // 3  — 向正无穷 (toward +∞)
value.setScale(0, RoundingMode.FLOOR);      // 2  — 向负无穷 (toward -∞)
value.setScale(0, RoundingMode.HALF_UP);    // 3  — 四舍五入 (round half up)
value.setScale(0, RoundingMode.HALF_DOWN);  // 2  — 五舍六入 (round half down)
value.setScale(0, RoundingMode.HALF_EVEN);  // 2  — 银行家舍入 (banker's rounding)
value.setScale(0, RoundingMode.UNNECESSARY);// ArithmeticException 若需舍入

// 负数时的差异
BigDecimal neg = new BigDecimal("-2.5");
neg.setScale(0, RoundingMode.UP);           // -3 (远离零)
neg.setScale(0, RoundingMode.CEILING);      // -2 (向正无穷)
```

### 金融计算最佳实践 (Financial Calculation Best Practices)

```java
public class MoneyUtils {
    // 金额用 BigDecimal 表示，绝不用 double/float
    private static final int MONEY_SCALE = 2;
    private static final RoundingMode ROUNDING = RoundingMode.HALF_EVEN; // 银行家舍入

    // 加法 — 分别 setScale 后再加
    public static BigDecimal add(BigDecimal a, BigDecimal b) {
        return a.add(b).setScale(MONEY_SCALE, ROUNDING);
    }

    // 乘法 (如税率、折扣)
    public static BigDecimal multiply(BigDecimal amount, BigDecimal rate) {
        return amount.multiply(rate).setScale(MONEY_SCALE, ROUNDING);
    }

    // 除法 — 必须指定 scale 和 RoundingMode
    public static BigDecimal divide(BigDecimal a, BigDecimal b) {
        return a.divide(b, MONEY_SCALE, ROUNDING);
    }

    // 利息计算 (interest calculation)
    public static BigDecimal simpleInterest(
            BigDecimal principal, BigDecimal annualRate, int days) {
        return principal
            .multiply(annualRate)
            .multiply(BigDecimal.valueOf(days))
            .divide(BigDecimal.valueOf(365), MONEY_SCALE + 4, ROUNDING)
            .setScale(MONEY_SCALE, ROUNDING);
    }

    // 复利 (compound interest): P × (1 + r)^n
    public static BigDecimal compoundInterest(
            BigDecimal principal, BigDecimal rate, int periods) {
        BigDecimal onePlusRate = BigDecimal.ONE.add(rate);
        BigDecimal factor = onePlusRate.pow(periods, MathContext.DECIMAL128);
        return principal.multiply(factor).setScale(MONEY_SCALE, ROUNDING);
    }
}
```

**金融计算规则汇总**:
1. 永远用 `String` 构造函数创建 BigDecimal
2. 除法必须指定 `scale` + `RoundingMode`
3. 比较用 `compareTo()`，不用 `equals()` (0.10 ≠ 0.1 in equals)
4. 中间计算保留更多小数位，最终再舍入
5. 金额分摊时注意 "分摊余额" (remainder allocation) 问题

### 除法注意事项

```java
BigDecimal a = new BigDecimal("1");
BigDecimal b = new BigDecimal("3");

// ArithmeticException: Non-terminating decimal expansion
// BigDecimal result = a.divide(b);

// 正确做法: 指定 scale 和 RoundingMode
BigDecimal result = a.divide(b, 10, RoundingMode.HALF_UP);  // 0.3333333333
```

### 比较大小

```java
BigDecimal x = new BigDecimal("1.0");
BigDecimal y = new BigDecimal("1.00");

x.equals(y);       // false — scale 不同 (1 vs 2)
x.compareTo(y);    // 0     — 数值相等
```

---

## 6. BigInteger

### 基础使用

```java
import java.math.BigInteger;

// 创建
BigInteger a = new BigInteger("12345678901234567890");
BigInteger b = BigInteger.valueOf(1234567890L);

// 常量
BigInteger.ZERO;  BigInteger.ONE;  BigInteger.TWO;  BigInteger.TEN;

// 算术运算 (arithmetic)
BigInteger sum = a.add(b);
BigInteger diff = a.subtract(b);
BigInteger product = a.multiply(b);
BigInteger[] divAndRem = a.divideAndRemainder(b);  // [商, 余数]
BigInteger power = a.pow(10);

// 位运算 (bitwise)
BigInteger and = a.and(b);
BigInteger or = a.or(b);
BigInteger xor = a.xor(b);
BigInteger not = a.not();
BigInteger shifted = a.shiftLeft(10);    // a << 10
int bitLen = a.bitLength();              // 二进制位数
int bitCount = a.bitCount();             // 1 的个数
```

### GCD / LCM

```java
BigInteger gcd = a.gcd(b);                          // 最大公约数
BigInteger lcm = a.multiply(b).divide(a.gcd(b));    // 最小公倍数
```

### 素数运算 (Primality)

```java
// Miller-Rabin 概率素性测试
boolean isPrime = a.isProbablePrime(100);  // certainty=100, 误判概率 < 2^(-100)

// 下一个可能的素数
BigInteger nextPrime = a.nextProbablePrime();

// 生成随机素数 (密码学常用)
BigInteger prime = BigInteger.probablePrime(2048, new SecureRandom());
```

### 密码学应用 (Cryptographic Applications)

```java
// 模幂运算 (modular exponentiation): a^b mod m
// RSA 加密/解密的核心操作
BigInteger modPow = a.modPow(b, m);

// 模逆 (modular inverse): a^(-1) mod m
// RSA 密钥生成中计算 d = e^(-1) mod φ(n)
BigInteger modInverse = a.modInverse(m);

// RSA 简化示例
BigInteger p = BigInteger.probablePrime(1024, new SecureRandom());
BigInteger q = BigInteger.probablePrime(1024, new SecureRandom());
BigInteger n = p.multiply(q);                // 模数
BigInteger phi = p.subtract(BigInteger.ONE)
                  .multiply(q.subtract(BigInteger.ONE));  // 欧拉函数
BigInteger e = BigInteger.valueOf(65537);     // 公钥指数
BigInteger d = e.modInverse(phi);             // 私钥指数

// 加密: c = m^e mod n
BigInteger ciphertext = message.modPow(e, n);
// 解密: m = c^d mod n
BigInteger plaintext = ciphertext.modPow(d, n);
```

### 进制转换 (Radix Conversion)

```java
BigInteger val = new BigInteger("255");
val.toString(2);    // "11111111" (二进制)
val.toString(16);   // "ff" (十六进制)

// 从其他进制创建
BigInteger fromHex = new BigInteger("ff", 16);   // 255
BigInteger fromBin = new BigInteger("11111111", 2);  // 255

// 字节数组互转
byte[] bytes = val.toByteArray();
BigInteger fromBytes = new BigInteger(1, bytes);  // signum=1 (正数)
```

---

## 7. Random 随机数演进

### 演进路线

```
JDK 1.0   Random           — 基础，线程安全但有竞争 (contention)
JDK 7     ThreadLocalRandom — 线程局部，无竞争
JDK 8     SplittableRandom — 可分割，并行流友好
JDK 17    RandomGenerator  — 统一接口 (JEP 356)
```

### Random (JDK 1.0)

```java
import java.util.Random;

Random random = new Random();          // 基于当前时间种子
Random seeded = new Random(42L);       // 固定种子，可复现

int r1 = random.nextInt();             // 任意 int
int r2 = random.nextInt(100);          // [0, 100)
long r3 = random.nextLong();
double r4 = random.nextDouble();       // [0.0, 1.0)
double gaussian = random.nextGaussian(); // 均值 0，标准差 1

byte[] bytes = new byte[16];
random.nextBytes(bytes);

// 局限: 内部使用 CAS (AtomicLong)，多线程下有竞争
```

### ThreadLocalRandom (JDK 7+)

```java
import java.util.concurrent.ThreadLocalRandom;

// 每个线程独立实例，消除竞争
ThreadLocalRandom tlr = ThreadLocalRandom.current();

int r1 = tlr.nextInt(10, 20);         // [10, 20)
long r2 = tlr.nextLong(100);          // [0, 100)
double r3 = tlr.nextDouble(1.0, 2.0); // [1.0, 2.0)

// 注意: 不可序列化，不可跨线程传递
// 不可 new ThreadLocalRandom()，只能 ThreadLocalRandom.current()
```

### SplittableRandom (JDK 8+)

```java
import java.util.SplittableRandom;

SplittableRandom sr = new SplittableRandom();

// 分割 (split): 为子任务创建独立生成器，统计独立
SplittableRandom child = sr.split();

// 适合 Fork/Join 和并行流
sr.ints(0, 100).limit(10).forEach(System.out::println);
sr.longs(1000).parallel().forEach(v -> { /* ... */ });
```

### RandomGenerator 统一接口 (JDK 17, JEP 356)

```java
import java.util.random.*;

// 统一接口
RandomGenerator rg = RandomGenerator.getDefault();

// 指定算法
RandomGenerator lxm = RandomGenerator.of("L64X128MixRandom");
RandomGenerator xoro = RandomGenerator.of("Xoroshiro128PlusPlus");
RandomGenerator xoshiro = RandomGenerator.of("Xoshiro256PlusPlus");

// 算法族接口层次
// RandomGenerator
//   ├── StreamableGenerator     — 可产生 RandomGenerator 流
//   ├── JumpableGenerator       — 可跳跃状态
//   │     └── LeapableGenerator — 可大步跳跃
//   └── SplittableGenerator     — 可分割
//   └── ArbitrarilyJumpableGenerator — 任意距离跳跃

// 列出所有可用算法
RandomGeneratorFactory.all()
    .map(f -> f.name() + " (period=" + f.stateBits() + " bits)")
    .forEach(System.out::println);
```

### 选择指南

| 场景 | 推荐 | 原因 |
|------|------|------|
| 单线程通用 | `Random` 或 `RandomGenerator.getDefault()` | 简单 |
| 多线程 | `ThreadLocalRandom` | 无竞争 |
| 并行流 / Fork-Join | `SplittableRandom` | 可分割 |
| 需要特定算法 | `RandomGenerator.of("算法名")` | JDK 17+ |
| 密码学安全 | `SecureRandom` | 见下节 |

---

## 8. SecureRandom 与 DRBG

### SecureRandom 基础

```java
import java.security.SecureRandom;

// 平台默认实现
SecureRandom sr = new SecureRandom();

// 指定算法
SecureRandom sha1 = SecureRandom.getInstance("SHA1PRNG");
SecureRandom native_ = SecureRandom.getInstance("NativePRNG");

// 生成安全随机数
byte[] token = new byte[32];
sr.nextBytes(token);

int r = sr.nextInt(1000000);  // 安全的 OTP
```

### DRBG (Deterministic Random Bit Generator, JDK 9+, JEP 273)

JDK 9 引入 DRBG 机制，遵循 NIST SP 800-90Ar1 标准。

```java
import java.security.DrbgParameters;
import java.security.SecureRandom;

// 使用 DRBG
SecureRandom drbg = SecureRandom.getInstance("DRBG",
    DrbgParameters.instantiation(
        256,                              // 安全强度 (security strength) 位
        DrbgParameters.Capability.PR_AND_RESEED,  // 支持预测阻力 + 重播种
        "personalization string".getBytes()        // 个性化字符串
    )
);

// 带额外输入的生成
byte[] output = new byte[32];
drbg.nextBytes(output,
    DrbgParameters.nextBytes(
        256,                             // 请求的安全强度
        false,                           // 是否要求预测阻力
        "additional input".getBytes()    // 附加输入
    )
);

// 重播种 (reseed)
drbg.reseed(DrbgParameters.reseed(
    false,                              // 是否要求预测阻力
    "additional input".getBytes()       // 附加输入
));
```

### SecureRandom vs Random

| 特性 | Random | SecureRandom |
|------|--------|-------------|
| 算法 | 线性同余 (LCG) | SHA1PRNG / NativePRNG / DRBG |
| 可预测性 | 已知种子可推导后续值 | 密码学不可预测 |
| 性能 | 快 | 慢 (需要熵源) |
| 用途 | 模拟、游戏、测试 | 密钥生成、令牌、盐值 |

---

## 9. HexFormat (JDK 17)

`java.util.HexFormat` 提供十六进制编解码 (hex encoding/decoding) 的标准 API，替代第三方工具。

```java
import java.util.HexFormat;

// 默认实例: 小写，无分隔符
HexFormat hex = HexFormat.of();

// 编码 (encoding)
byte[] data = {0x0A, 0x1B, 0x2C};
String encoded = hex.formatHex(data);           // "0a1b2c"

// 解码 (decoding)
byte[] decoded = hex.parseHex("0a1b2c");        // {0x0A, 0x1B, 0x2C}

// 单值转换
String s = hex.toHexDigits((byte) 0xFF);         // "ff"
int val = hex.fromHexDigits("ff");                // 255

// 自定义格式
HexFormat custom = HexFormat.ofDelimiter(":")
    .withPrefix("0x")
    .withUpperCase();

String mac = custom.formatHex(new byte[]{
    (byte)0xAA, (byte)0xBB, (byte)0xCC,
    (byte)0xDD, (byte)0xEE, (byte)0xFF
});
// "0xAA:0xBB:0xCC:0xDD:0xEE:0xFF"

// 解析带分隔符的十六进制
byte[] parsed = custom.parseHex("0xAA:0xBB:0xCC:0xDD:0xEE:0xFF");

// 替代旧方案
// 旧: Integer.toHexString(), String.format("%02x"), 第三方 Hex.encodeHex()
// 新: HexFormat.of().formatHex(bytes) — 标准、可配置、不可变、线程安全
```

---

## 10. Math.clamp (JDK 21)

`Math.clamp()` 将值限制在 `[min, max]` 范围内 (range clamping)。

```java
// Math.clamp(value, min, max)
int clamped = Math.clamp(150, 0, 100);       // 100 (超上界)
int clamped2 = Math.clamp(-10, 0, 100);      // 0   (低于下界)
int clamped3 = Math.clamp(50, 0, 100);       // 50  (范围内不变)

long clampedL = Math.clamp(1000L, 0L, 500L); // 500L
float clampedF = Math.clamp(1.5f, 0.0f, 1.0f); // 1.0f
double clampedD = Math.clamp(3.14, 0.0, 1.0);   // 1.0

// 典型用途
// 1. 颜色值限制 (0-255)
int red = Math.clamp(computedRed, 0, 255);

// 2. 音量控制
double volume = Math.clamp(userInput, 0.0, 1.0);

// 3. 分页参数
int page = Math.clamp(requestedPage, 1, totalPages);

// JDK 21 之前的等价写法
int oldClamp = Math.max(min, Math.min(max, value));
```

---

## 11. 向量化数学: Vector API

Vector API (孵化中, JEP 338/417/438/469/489) 利用 SIMD 指令加速数学运算。

```java
import jdk.incubator.vector.*;

// 使用 SIMD 加速数组运算
static final VectorSpecies<Float> SPECIES = FloatVector.SPECIES_PREFERRED;

void vectorAdd(float[] a, float[] b, float[] result) {
    int i = 0;
    int bound = SPECIES.loopBound(a.length);

    // 向量化循环 (vectorized loop)
    for (; i < bound; i += SPECIES.length()) {
        FloatVector va = FloatVector.fromArray(SPECIES, a, i);
        FloatVector vb = FloatVector.fromArray(SPECIES, b, i);
        FloatVector vr = va.add(vb);
        vr.intoArray(result, i);
    }

    // 尾部标量处理 (scalar tail)
    for (; i < a.length; i++) {
        result[i] = a[i] + b[i];
    }
}

// 向量化数学函数
void vectorMath(float[] input, float[] output) {
    int i = 0;
    int bound = SPECIES.loopBound(input.length);

    for (; i < bound; i += SPECIES.length()) {
        FloatVector v = FloatVector.fromArray(SPECIES, input, i);
        // 向量化运算: 一次处理多个元素
        FloatVector result = v.mul(v)        // x^2
                              .add(v)        // x^2 + x
                              .neg();        // -(x^2 + x)
        result.intoArray(output, i);
    }
    for (; i < input.length; i++) {
        output[i] = -(input[i] * input[i] + input[i]);
    }
}
```

Vector API 对数学运算的加速场景:
- 数组批量算术运算 (element-wise arithmetic)
- 矩阵乘法 (matrix multiplication)
- 图像处理滤波 (image filtering)
- 科学计算 (scientific computing)
- 机器学习推理 (ML inference)

---

## 12. 最佳实践

### BigDecimal 使用

```java
// 推荐
new BigDecimal("0.1");                          // 字符串构造
BigDecimal.valueOf(123.456);                    // valueOf
a.divide(b, 10, RoundingMode.HALF_UP);         // 指定 scale
a.compareTo(b) == 0;                           // 用 compareTo

// 避免
new BigDecimal(0.1);                            // double 构造，精度丢失
a.equals(b);                                   // scale 不同返回 false
a.divide(b);                                   // 非整除抛异常
```

### 随机数选择

```java
// 通用单线程
Random random = new Random();

// 多线程并发
ThreadLocalRandom.current().nextInt(100);

// 并行流
new SplittableRandom().ints(0, 100).parallel().forEach(...);

// JDK 17+ 推荐
RandomGenerator.of("L64X128MixRandom").nextInt(100);

// 密码学场景 (令牌、密钥、盐值)
SecureRandom sr = new SecureRandom();
```

### 性能提示

```java
// Math.sqrt(x) 优于 Math.pow(x, 0.5)
// Math.abs(x) 优于 (x >= 0 ? x : -x) — JIT 可内联为单条指令
// Math.fma(a, b, c) 优于 a * b + c — 更高精度，可能映射到硬件 FMA
// Math.clamp(v, lo, hi) 优于 Math.max(lo, Math.min(hi, v)) — 更清晰

// BigDecimal: 避免 toString() 做格式化，用 toPlainString()
BigDecimal bd = new BigDecimal("1E+10");
bd.toString();       // "1E+10"
bd.toPlainString();  // "10000000000"
```

---

## 13. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 数学 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Joseph D. Darcy | 10+ | Oracle | Math/StrictMath API, BigDecimal |
| 2 | Brian Burkhalter | 8+ | Oracle | BigDecimal, 数学优化 |
| 3 | Jim Gish | 5+ | Oracle | 数学函数 |
| 4 | Roger Riggs | 3+ | Oracle | 核心库 |

### 历史贡献者

| 贡献者 | 公司/机构 | 主要贡献 |
|--------|----------|----------|
| **Joseph Darcy** | Oracle | BigDecimal, Math 增强, strictfp |
| **Mike Cowlishaw** | IBM | BigDecimal 规范 (General Decimal Arithmetic) |
| **Joshua Bloch** | Sun/Google | Math 设计 |
| **K.C. Ng** | Sun | fdlibm 原始 C 实现 |
| **Anton Artemov** | Oracle | fdlibm Java 移植 |
| **Guy Steele** | Sun | SplittableRandom 设计 |

---

## 14. 相关链接

### 内部文档

- [API 框架](../api/) - 集合框架
- [核心库](../core/) - 核心平台

### 外部资源

- [BigDecimal Javadoc](https://docs.oracle.com/javase/8/docs/api/java/math/BigDecimal.html)
- [BigInteger Javadoc](https://docs.oracle.com/javase/8/docs/api/java/math/BigInteger.html)
- [JEP 273: DRBG-Based SecureRandom](https://openjdk.org/jeps/273)
- [JEP 306: Restore Always-Strict Floating-Point Semantics](https://openjdk.org/jeps/306)
- [JEP 356: Enhanced Pseudo-Random Number Generators](https://openjdk.org/jeps/356)
- [JEP 489: Vector API (Ninth Incubator)](https://openjdk.org/jeps/489)
- [StrictMath Javadoc](https://docs.oracle.com/javase/8/docs/api/java/lang/StrictMath.html)
- [fdlibm (Wikipedia)](https://en.wikipedia.org/wiki/Fdlibm)

---

**最后更新**: 2026-03-22
