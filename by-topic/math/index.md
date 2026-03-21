# 数学计算

> BigDecimal, Math, Random, StrictMath 演进历程

[← 返回主题索引](../)

---

## 1. 快速概览

```
JDK 1.0 ── JDK 5 ── JDK 8 ── JDK 17 ── JDK 21
   │        │        │        │        │
Math     StrictMath  Random  增强   随机数
类       精确数学  (API)   分割器  生成器
```

### 核心演进

| 版本 | 特性 | 说明 |
|------|------|------|
| **JDK 1.0** | Math, Random | 基础数学函数 |
| **JDK 1.0** | BigDecimal | 精确小数 |
| **JDK 5** | StrictMath | 精确数学函数 |
| **JDK 8** | SplittableRandom | 可分割随机数 |
| **JDK 17** | RandomGenerator | 随机数增强 (JEP 356) |
| **JDK 21** | Math 增强 | 性能优化 |

---

## 目录

- [Math 类](#math-类)
- [StrictMath 类](#strictmath-类)
- [BigDecimal](#bigdecimal)
- [BigInteger](#biginteger)
- [Random 随机数](#random-随机数)
- [RandomGenerator (JDK 17+)](#randomgenerator-jdk-17)
- [最佳实践](#最佳实践)
- [核心贡献者](#核心贡献者)
- [相关链接](#相关链接)

---

## 2. Math 类

### 基础函数

```java
import java.lang.Math;

// 三角函数
double sin = Math.sin(Math.PI / 2);      // 1.0
double cos = Math.cos(0);                   // 1.0
double tan = Math.tan(Math.PI / 4);       // 1.0

// 反三角函数
double asin = Math.asin(1.0);              // π/2
double acos = Math.acos(0.0);              // π/2
double atan = Math.atan(1.0);              // π/4

// 双曲函数
double sinh = Math.sinh(1.0);
double cosh = Math.cosh(1.0);
double tanh = Math.tanh(1.0);

// 指数和对数
double exp = Math.exp(1.0);                // e^1
double log = Math.log(10.0);               // ln(10)
double log10 = Math.log10(100);            // 2.0
double pow = Math.pow(2, 10);              // 1024.0

// 取整
double ceil = Math.ceil(3.5);               // 4.0 (向上)
double floor = Math.floor(3.5);             // 3.0 (向下)
double round = Math.round(3.5);             // 4.0 (四舍五入)
double rint = Math.rint(3.5);               // 4.0 (最近偶数)

// 其他
double abs = Math.abs(-5.0);                // 5.0
double max = Math.max(1, 2);                // 2
double min = Math.min(1, 2);                // 1
double sign = Math.signum(-5.0);            // -1.0
double hypot = Math.hypot(3, 4);            // 5.0 (勾股定理)
```

### 常量

```java
System.out.println(Math.E);    // 2.718281828459045
System.out.println(Math.PI);   // 3.141592653589793
```

### 角度转换

```java
// 弧度 → 角度
double degrees = Math.toDegrees(Math.PI);  // 180.0

// 角度 → 弧度
double radians = Math.toRadians(180.0);    // 3.14159...
```

### 幂运算

```java
// Math.pow vs 运算符
double pow = Math.pow(2, 10);    // 1024.0
double square = 2 * 2;             // 4

// sqrt 比 pow(x, 0.5) 快
double sqrt = Math.sqrt(16);       // 4.0
double cbrt = Math.cbrt(27);       // 3.0 (立方根，JDK 8+)
```

---

## 3. StrictMath 类

**JDK 5 引入**

### 与 Math 的区别

| 特性 | Math | StrictMath |
|------|------|------------|
| 性能 | 快 | 慢 (精确) |
| 精度 | 平台相关 | 跨平台一致 |
| 用途 | 通用 | 需要精确结果 |

### 使用场景

```java
import java.lang.StrictMath;

// 需要跨平台一致的结果
double sin = StrictMath.sin(Math.PI / 2);
double log = StrictMath.log(10.0);

// 与 Math 相同的 API
StrictMath.cos(x);
StrictMath.tan(x);
StrictMath.exp(x);
StrictMath.pow(x, y);
```

---

## 4. BigDecimal

### 基础使用

```java
import java.math.*;

// 创建 BigDecimal
BigDecimal a = new BigDecimal("123.456");
BigDecimal b = BigDecimal.valueOf(123.456);
BigDecimal c = new BigDecimal(123.456789, MathContext.DECIMAL64);

// 避免使用 double 构造函数!
// ❌ 错误: new BigDecimal(0.1)  // 实际是 0.100000000000000005551...
// ✅ 正确: new BigDecimal("0.1")
```

### 基本运算

```java
BigDecimal a = new BigDecimal("123.456");
BigDecimal b = new BigDecimal("789.012");

// 加减乘除
BigDecimal sum = a.add(b);           // 912.468
BigDecimal diff = a.subtract(b);     // -665.556
BigDecimal product = a.multiply(b);  // 97408.232...
BigDecimal quotient = a.divide(b, 2, RoundingMode.HALF_UP);  // 0.16

// 幂运算
BigDecimal power = a.pow(3);         // a^3

// 符号
BigDecimal neg = a.negate();          // -123.456
BigDecimal abs = a.abs();              // 123.456
```

### 舍入模式

```java
import java.math.RoundingMode;

// 舍入模式
BigDecimal value = new BigDecimal("123.456");

value.setScale(2, RoundingMode.UP);       // 123.46 (远离零)
value.setScale(2, RoundingMode.DOWN);     // 123.45 (趋向零)
value.setScale(2, RoundingMode.CEILING);  // 123.46 (向上)
value.setScale(2, RoundingMode.FLOOR);    // 123.45 (向下)
value.setScale(2, RoundingMode.HALF_UP);  // 123.46 (四舍五入)
value.setScale(2, RoundingMode.HALF_DOWN); // 123.46 (五舍六入)
value.setScale(2, RoundingMode.HALF_EVEN); // 123.46 (向偶数)
```

### 除法注意事项

```java
// ⚠️ 注意: 非整除法必须指定 scale 和 RoundingMode
BigDecimal a = new BigDecimal("1");
BigDecimal b = new BigDecimal("3");

// ❌ 错误: 会抛出 ArithmeticException
// BigDecimal result = a.divide(b);

// ✅ 正确
BigDecimal result = a.divide(b, 10, RoundingMode.HALF_UP);  // 0.3333333333
```

### 比较大小

```java
BigDecimal a = new BigDecimal("123.456");
BigDecimal b = new BigDecimal("123.456");

int cmp = a.compareTo(b);  // 0 (相等), <0 (a<b), >0 (a>b)

if (cmp == 0) {
    System.out.println("Equal");
} else if (cmp < 0) {
    System.out.println("a < b");
} else {
    System.out.println("a > b");
}

// ❌ 不要使用 equals!
// a.equals(b) 会比较 scale，0.1 != 0.10
```

### 精度控制

```java
import java.math.MathContext;

// 指定精度
BigDecimal a = new BigDecimal("1.0", MathContext.DECIMAL32);   // 7 位精度
BigDecimal b = new BigDecimal("1.0", MathContext.DECIMAL64);   // 16 位精度
BigDecimal c = new BigDecimal("1.0", MathContext.UNLIMITED);  // 无限制

// 运算受精度影响
BigDecimal result = a.multiply(b);  // 使用 a 的精度
```

### 金融计算

```java
// 金融计算示例
public class FinancialCalculation {

    // 利息计算
    public static BigDecimal calculateInterest(
            BigDecimal principal,
            BigDecimal rate,
            int periods) {

        // 本金 × 利率 × 期数
        return principal
            .multiply(rate)
            .multiply(BigDecimal.valueOf(periods))
            .setScale(2, RoundingMode.HALF_UP);
    }

    // 复利
    public static BigDecimal compoundInterest(
            BigDecimal principal,
            BigDecimal rate,
            int periods) {

        // 本金 × (1 + 利率)^期数
        BigDecimal onePlusRate = BigDecimal.ONE.add(rate);
        BigDecimal factor = onePlusRate.pow(periods);
        return principal
            .multiply(factor)
            .setScale(2, RoundingMode.HALF_UP);
    }

    // 税金转换
    public static BigDecimal exchange(
            BigDecimal amount,
            BigDecimal rate,
            int scale) {

        return amount
            .multiply(rate)
            .setScale(scale, RoundingMode.HALF_UP);
    }
}

// 使用
BigDecimal principal = new BigDecimal("10000.00");
BigDecimal rate = new BigDecimal("0.05");  // 5%
BigDecimal interest = FinancialCalculation.calculateInterest(principal, rate, 12);
```

---

## 5. BigInteger

### 基础使用

```java
import java.math.BigInteger;

// 创建 BigInteger
BigInteger a = new BigInteger("12345678901234567890");
BigInteger b = BigInteger.valueOf(1234567890L);

// 常量
BigInteger ONE = BigInteger.ONE;
BigInteger TEN = BigInteger.TEN;
BigInteger ZERO = BigInteger.ZERO;

// 运算
BigInteger sum = a.add(b);
BigInteger diff = a.subtract(b);
BigInteger product = a.multiply(b);
BigInteger quotient = a.divide(b);
BigInteger remainder = a.remainder(b);

// 幂运算
BigInteger power = a.pow(10);  // a^10

// 取模
BigInteger mod = a.mod(b);

// 取模幂运算 (更快)
BigInteger modPow = a.modPow(b, m);
```

### 位运算

```java
// 位运算
BigInteger and = a.and(b);
BigInteger or = a.or(b);
BigInteger xor = a.xor(b);
BigInteger not = a.not();
BigInteger shiftLeft = a.shiftLeft(10);   // a << 10
BigInteger shiftRight = a.shiftRight(10);  // a >> 10
```

### GCD 和 LCM

```java
// 最大公约数
BigInteger gcd = a.gcd(b);  // 54

// 最小公倍数
BigInteger lcm = a.multiply(b).divide(a.gcd(b));
```

### 素数运算

```java
// 是否为素数
boolean isPrime = a.isProbablePrime(100);

// 下一个素数
BigInteger nextPrime = a.nextProbablePrime();
```

---

## 6. Random 随机数

### Random 类

```java
import java.util.Random;

// 创建 Random
Random random = new Random();

// 生成随机数
int r1 = random.nextInt();                  // 任意 int
int r2 = random.nextInt(100);               // 0-99
long r3 = random.nextLong();                 // 任意 long
float r4 = random.nextFloat();                // 0.0-1.0
double r5 = random.nextDouble();              // 0.0-1.0
boolean r6 = random.nextBoolean();             // true/false

// 字节数组
byte[] bytes = new byte[16];
random.nextBytes(bytes);

// Gaussian 分布
double gaussian = random.nextGaussian();    // 均值 0，标准差 1
```

### ThreadLocalRandom (JDK 7+)

```java
import java.util.concurrent.ThreadLocalRandom;

// 线程局部随机数生成器 (性能更好)
ThreadLocalRandom random = ThreadLocalRandom.current();

int r1 = random.nextInt(100);
int r2 = random.nextInt(10, 20);  // 10-19 (包含 10，不包含 20)
long r3 = random.nextLong();
double r4 = random.nextDouble();
```

### SplittableRandom (JDK 8+)

```java
import java.util.SplittableRandom;

// 可分割随机数生成器
SplittableRandom random = new SplittableRandom();

int r1 = random.nextInt(100);
long r2 = random.nextLong(100, 200);

// 分割 (多线程)
SplittableRandom split = random.split();

// 生成随机流
random.ints(0, 100).limit(10).forEach(System.out::println);
```

---

## 7. RandomGenerator (JDK 17+)

**JEP 356: Enhanced Random Number Generator**

### 基础使用

```java
import java.util.random.*;

// 创建 RandomGenerator
RandomGenerator random = RandomGenerator.getDefault();

// 基本方法 (与 Random 相同)
int r1 = random.nextInt(100);
long r2 = random.nextLong();
double r3 = random.nextDouble();
```

### 随机数算法

```java
// 指定算法
RandomGenerator lxm = RandomGenerator.of("L32X64MixRandom");
RandomGenerator xoroshiro = RandomGenerator.of("Xoroshiro128PlusPlus");

// 创建可跳转的随机数生成器
JumpableGenerator jumpable = RandomGenerator.of("L32X64MixRandom");
jumpable.jump();  // 跳转到下一个状态
```

### 随机数流

```java
// 随机数流
RandomGenerator random = RandomGenerator.getDefault();

// ints() - 随机 int 流
random.ints(0, 100)
    .limit(10)
    .forEach(System.out::println);

// nextLong()
long r = random.nextLong(0, 1000000);
```

---

## 8. 最佳实践

### BigDecimal 使用

```java
// ✅ 推荐
// 1. 使用字符串构造函数
new BigDecimal("0.1");

// 2. 使用 valueOf
BigDecimal.valueOf(123.456);

// 3. 指定 scale
a.divide(b, 10, RoundingMode.HALF_UP);

// 4. 使用 compareTo 比较
a.compareTo(b) == 0;

// ❌ 避免
// 1. 使用 double 构造函数
new BigDecimal(0.1);  // 精度丢失

// 2. 使用 equals 比较
a.equals(b);  // scale 不同会返回 false

// 3. 除法不指定 scale
a.divide(b);  // 可能抛出异常
```

### 金融计算

```java
// 金融计算最佳实践
public class MoneyUtils {

    // 总是指定 scale
    private static final int MONEY_SCALE = 2;

    // 加法
    public static BigDecimal add(BigDecimal a, BigDecimal b) {
        return a.add(b).setScale(MONEY_SCALE, RoundingMode.HALF_UP);
    }

    // 乘法
    public static BigDecimal multiply(BigDecimal a, BigDecimal b) {
        return a.multiply(b).setScale(MONEY_SCALE, RoundingMode.HALF_UP);
    }

    // 除法
    public static BigDecimal divide(BigDecimal a, BigDecimal b) {
        return a.divide(b, MONEY_SCALE, RoundingMode.HALF_UP);
    }

    // 格式化
    public static String format(BigDecimal amount) {
        return String.format("$%,.2f", amount);
    }
}
```

### 随机数生成

```java
// ✅ 推荐
// 1. 使用 ThreadLocalRandom (并发)
ThreadLocalRandom.current().nextInt(100);

// 2. 使用 SplittableRandom (并行流)
SplittableRandom random = new SplittableRandom();
random.ints(0, 100).parallel().forEach(...);

// 3. 使用 RandomGenerator (JDK 17+)
RandomGenerator.getDefault().nextInt(100);

// ❌ 避免
// 1. 多线程共享 Random (性能问题)
Random random = new Random();  // 有竞争
```

### 性能优化

```java
// Math vs StrictMath
Math.sqrt(x);   // 快，适合大多数场景
StrictMath.sqrt(x);  // 慢，需要跨平台一致

// Random vs ThreadLocalRandom
// 单线程: Random
Random random = new Random();

// 多线程: ThreadLocalRandom
ThreadLocalRandom.current().nextInt();

// 并行流: SplittableRandom
SplittableRandom random = new SplittableRandom();
random.ints(0, 100).parallel().forEach(...);
```

---

## 9. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 数学 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Joseph D. Darcy | 10+ | Oracle | Math API |
| 2 | Brian Burkhalter | 8+ | Oracle | 字符串/数学 |
| 3 | Jim Gish | 5+ | Oracle | 数学函数 |
| 4 | Roger Riggs | 3+ | Oracle | 核心库 |

### 历史贡献者

| 贡献者 | 公司/机构 | 主要贡献 |
|--------|----------|----------|
| **Joseph Darcy** | Oracle | BigDecimal, Math 增强 |
| **Mike Cowlishaw** | | BigDecimal 规范 |
| **Joshua Bloch** | Sun/Google | Math 设计 |

---

## 10. 相关链接

### 内部文档

- [API 框架](../api/) - 集合框架
- [核心库](../core/) - 核心平台

### 外部资源

- [BigDecimal 规范](https://docs.oracle.com/javase/8/docs/api/java/math/BigDecimal.html)
- [BigInteger 规范](https://docs.oracle.com/javase/8/docs/api/java/math/BigInteger.html)
- [JEP 356](/jeps/math/jep-356.md)
- [StrictMath 文档](https://docs.oracle.com/javase/8/docs/api/java/lang/StrictMath.html)

---

**最后更新**: 2026-03-20
