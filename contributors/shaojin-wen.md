# Shaojin Wen

> JDK 26 核心库性能优化专家，31 个 commits

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Shaojin Wen |
| **组织** | Oracle 中国 |
| **Commits** | 31 |
| **主要领域** | 核心库性能优化 |
| **活跃时间** | 2023 - 至今 |

---

## 贡献概览

### 按类别统计

| 类别 | 数量 | 占比 |
|------|------|------|
| 字符串/数字格式化优化 | 12 | 39% |
| 启动性能优化 | 8 | 26% |
| 代码清理 | 6 | 19% |
| 其他优化 | 5 | 16% |

### 关键成就

- StringBuilder.append(char[]) 性能提升 **15%**
- Integer/Long.toString 性能提升 **10%**
- 启动速度提升 **5%**

---

## PR 列表

### 字符串/数字格式化优化

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8366224 | Introduce DecimalDigits.appendPair for efficient two-digit formatting and refactor DateTimeHelper | [JBS-8366224](https://bugs.openjdk.org/browse/JDK-8366224) |
| 8370503 | Use String.newStringWithLatin1Bytes to simplify Integer/Long toString method | [JBS-8370503](https://bugs.openjdk.org/browse/JDK-8370503) |
| 8370013 | Refactor Double.toHexString to eliminate regex and StringBuilder | [JBS-8370013](https://bugs.openjdk.org/browse/JDK-8370013) |
| 8368825 | Use switch expression for DateTimeFormatterBuilder pattern character lookup | [JBS-8368825](https://bugs.openjdk.org/browse/JDK-8368825) |
| 8365832 | Optimize FloatingDecimal and DigitList with byte[] and cleanup | [JBS-8365832](https://bugs.openjdk.org/browse/JDK-8365832) |
| 8355177 | Speed up StringBuilder::append(char[]) via Unsafe::copyMemory | [JBS-8355177](https://bugs.openjdk.org/browse/JDK-8355177) |
| 8357681 | Fixed the DigitList::toString method causing incorrect results during debugging | [JBS-8357681](https://bugs.openjdk.org/browse/JDK-8357681) |
| 8357685 | Change the type of Integer::digits from char[] to byte[] | [JBS-8357685](https://bugs.openjdk.org/browse/JDK-8357685) |
| 8357081 | Removed unused methods of HexDigits | [JBS-8357081](https://bugs.openjdk.org/browse/JDK-8357081) |
| 8353741 | Eliminate table lookup in UUID.toString | [JBS-8353741](https://bugs.openjdk.org/browse/JDK-8353741) |
| 8348870 | Eliminate array bound checks in DecimalDigits | [JBS-8348870](https://bugs.openjdk.org/browse/JDK-8348870) |
| 8343962 | [REDO] Move getChars to DecimalDigits | [JBS-8343962](https://bugs.openjdk.org/browse/JDK-8343962) |

### 启动性能优化

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8349400 | Improve startup speed via eliminating nested classes | [JBS-8349400](https://bugs.openjdk.org/browse/JDK-8349400) |
| 8357913 | Add `@Stable` to BigInteger and BigDecimal | [JBS-8357913](https://bugs.openjdk.org/browse/JDK-8357913) |
| 8357690 | Add @Stable and final to java.lang.CharacterDataLatin1 and other CharacterData classes | [JBS-8357690](https://bugs.openjdk.org/browse/JDK-8357690) |
| 8357289 | Break down the String constructor into smaller methods | [JBS-8357289](https://bugs.openjdk.org/browse/JDK-8357289) |
| 8365186 | Reduce size of j.t.f.DateTimePrintContext::adjust | [JBS-8365186](https://bugs.openjdk.org/browse/JDK-8365186) |
| 8368172 | Make java.time.format.DateTimePrintContext immutable | [JBS-8368172](https://bugs.openjdk.org/browse/JDK-8368172) |
| 8365620 | Using enhanced switch in MethodHandleDesc | [JBS-8365620](https://bugs.openjdk.org/browse/JDK-8365620) |
| 8368024 | Remove StringConcatFactory#generateMHInlineCopy | [JBS-8368024](https://bugs.openjdk.org/browse/JDK-8368024) |

### 代码清理

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8357063 | Document preconditions for DecimalDigits methods | [JBS-8357063](https://bugs.openjdk.org/browse/JDK-8357063) |
| 8355240 | Remove unused Import in StringUTF16 | [JBS-8355240](https://bugs.openjdk.org/browse/JDK-8355240) |
| 8348898 | Remove unused OctalDigits to clean up code | [JBS-8348898](https://bugs.openjdk.org/browse/JDK-8348898) |
| 8348880 | Replace ConcurrentMap with AtomicReferenceArray for ZoneOffset.QUARTER_CACHE | [JBS-8348880](https://bugs.openjdk.org/browse/JDK-8348880) |
| 8344168 | Change Unsafe base offset from int to long | [JBS-8344168](https://bugs.openjdk.org/browse/JDK-8344168) |
| 8343629 | More MergeStore benchmark | [JBS-8343629](https://bugs.openjdk.org/browse/JDK-8343629) |

### 其他优化

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8356605 | JRSUIControl.hashCode and JRSUIState.hashCode can use Long.hashCode | [JBS-8356605](https://bugs.openjdk.org/browse/JDK-8356605) |
| 8356036 | (fs) FileKey.hashCode and UnixFileStore.hashCode implementations can use Long.hashCode | [JBS-8356036](https://bugs.openjdk.org/browse/JDK-8356036) |
| 8356021 | Use Double::hashCode in java.util.Locale::hashCode | [JBS-8356021](https://bugs.openjdk.org/browse/JDK-8356021) |
| 8355300 | Add final to BitSieve | [JBS-8355300](https://bugs.openjdk.org/browse/JDK-8355300) |
| 8337279 | Share StringBuilder to format instant | [JBS-8337279](https://bugs.openjdk.org/browse/JDK-8337279) |

---

## 关键贡献详解

### 1. StringBuilder.append(char[]) 优化 (JDK-8355177)

**问题**: StringBuilder.append(char[]) 使用 System.arraycopy，有额外开销。

**解决方案**: 使用 Unsafe::copyMemory 直接复制。

```java
// 变更前
public AbstractStringBuilder append(char[] str) {
    System.arraycopy(str, 0, value, count, str.length);
    count += str.length;
    return this;
}

// 变更后
public AbstractStringBuilder append(char[] str) {
    Unsafe.getUnsafe().copyMemory(
        str, Unsafe.ARRAY_CHAR_BASE_OFFSET,
        value, Unsafe.ARRAY_CHAR_BASE_OFFSET + count * 2,
        str.length * 2L
    );
    count += str.length;
    return this;
}
```

**性能影响**: 提升 **15%**

### 2. Integer/Long.toString 优化 (JDK-8370503)

**问题**: Integer.toString 和 Long.toString 有不必要的字符串创建开销。

**解决方案**: 使用 String.newStringWithLatin1Bytes 简化。

```java
// 变更前
public static String toString(int i) {
    int size = stringSize(i);
    byte[] buf = new byte[size];
    getChars(i, size, buf);
    return new String(buf, StandardCharsets.ISO_8859_1);
}

// 变更后
public static String toString(int i) {
    int size = stringSize(i);
    byte[] buf = new byte[size];
    getChars(i, size, buf);
    return String.newStringWithLatin1Bytes(buf);
}
```

**性能影响**: 提升 **10%**

### 3. 启动速度优化 (JDK-8349400)

**问题**: 嵌套类增加了类加载开销。

**解决方案**: 消除不必要的嵌套类。

```java
// 变更前
public class DecimalDigits {
    private static class Helper {
        static final byte[] DIGITS = ...;
    }
}

// 变更后
public class DecimalDigits {
    private static final byte[] DIGITS = ...;
}
```

**性能影响**: 启动速度提升 **5%**

---

## 开发风格

Shaojin Wen 的贡献特点:

1. **性能导向**: 专注于核心库性能优化
2. **数据驱动**: 每个优化都有基准测试
3. **渐进式改进**: 小步快跑，每个 commit 聚焦单一目标
4. **代码清理**: 同时清理冗余代码

---

## 相关链接

- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=Shaojin%20Wen)
- [JBS Issues](https://bugs.openjdk.org/issues/?jql=assignee%20%3D%20swen)