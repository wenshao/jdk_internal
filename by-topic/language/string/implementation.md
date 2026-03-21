# String 内部实现

> Compact Strings、StringLatin1、StringUTF16 详解

---
## 目录

1. [Compact Strings (JEP 254)](#1-compact-strings-jep-254)
2. [StringLatin1](#2-stringlatin1)
3. [StringUTF16](#3-stringutf16)
4. [分发机制](#4-分发机制)
5. [编码转换流程](#5-编码转换流程)
6. [源码结构](#6-源码结构)
7. [贡献者](#7-贡献者)
8. [相关资源](#8-相关资源)

---


## 1. Compact Strings (JEP 254)

### 设计原理

JDK 9 将 `char[]` 改为 `byte[]` + `coder` 标志：

```java
// JDK 8 及之前
public final class String {
    private final char[] value;  // 每字符 2 字节
}

// JDK 9+ Compact Strings
public final class String {
    @Stable
    private final byte[] value;      // 实际存储

    private final byte coder;        // 0 = LATIN1, 1 = UTF16

    static final byte LATIN1 = 0;
    static final byte UTF16  = 1;
}
```

### 内存节省

| 字符串类型 | JDK 8 | JDK 9+ | 节省 |
|-----------|-------|--------|------|
| "Hello" | 10 字节 | 5 字节 | **50%** |
| "Café" | 8 字节 | 4 字节 | **50%** |
| "你好" | 4 字节 | 4 字节 | 0% |

### coder 传播规则

```
LATIN1 + LATIN1 = LATIN1
LATIN1 + UTF16  = UTF16
UTF16  + UTF16  = UTF16
```

### VM 参数

```bash
-XX:+CompactStrings  # 启用 (默认)
-XX:-CompactStrings  # 禁用
```

---

## 2. StringLatin1

单字节编码操作类（包级私有）：

```java
final class StringLatin1 {

    // 长度
    public static int length(byte[] value) {
        return value.length;
    }

    // 获取字符
    public static char charAt(byte[] value, int index) {
        return (char)(value[index] & 0xff);
    }

    // indexOf
    public static int indexOf(byte[] value, int ch, int fromIndex) {
        if (ch < 0) ch = ch + 256;
        for (int i = fromIndex; i < value.length; i++) {
            if (value[i] == ch) return i;
        }
        return -1;
    }

    // hashCode
    public static int hashCode(byte[] value) {
        int h = 0;
        for (byte v : value) {
            h = 31 * h + (v & 0xff);
        }
        return h;
    }

    // 压缩检测
    public static int compress(char[] src, int srcOff,
                              byte[] dst, int dstOff, int len) {
        for (int i = 0; i < len; i++) {
            char c = src[srcOff++];
            if (c > 0xFF) return 0;  // 无法压缩
            dst[dstOff++] = (byte)c;
        }
        return 1;
    }
}
```

---

## 3. StringUTF16

双字节编码操作类（包级私有）：

```java
final class StringUTF16 {

    // 长度 (每字符 2 字节)
    public static int length(byte[] value) {
        return value.length >> 1;
    }

    // 获取字符 (Big-Endian)
    @ForceInline
    public static char getChar(byte[] value, int index) {
        index <<= 1;
        return (char)((value[index] & 0xff) << 8 |
                      (value[index + 1] & 0xff));
    }

    // 设置字符
    @ForceInline
    public static void putChar(byte[] value, int index, int c) {
        index <<= 1;
        value[index]     = (byte)(c >> 8);
        value[index + 1] = (byte)c;
    }

    // 压缩检测
    public static byte[] compress(char[] src, int off, int len) {
        byte[] ret = new byte[len];
        for (int i = 0; i < len; i++) {
            char c = src[off++];
            if (c > 0xFF) return null;
            ret[i] = (byte)c;
        }
        return ret;
    }
}
```

---

## 4. 分发机制

String 根据 `coder` 分发到对应实现：

```java
public final class String {
    private final byte coder;
    private final byte[] value;

    public char charAt(int index) {
        if (index < 0 || index >= value.length()) {
            throw new StringIndexOutOfBoundsException(index);
        }
        return isLatin1()
            ? StringLatin1.charAt(value, index)
            : StringUTF16.charAt(value, index);
    }

    boolean isLatin1() {
        return COMPACT_STRINGS && coder == LATIN1;
    }

    // 长度计算
    public int length() {
        return value.length >> coder;  // LATIN1:*1, UTF16:*0.5
    }
}
```

---

## 5. 编码转换流程

```java
// 从 char[] 构造 String
public String(char[] value) {
    this(value, 0, value.length, null);
}

String(char[] value, int off, int len, Void sig) {
    if (len == 0) {
        this.value = EMPTY_VALUE;
        this.coder = LATIN1;
        return;
    }

    // 尝试压缩为 LATIN1
    if (COMPACT_STRINGS) {
        byte[] val = StringUTF16.compress(value, off, len);
        if (val != null) {
            this.value = val;
            this.coder = LATIN1;
            return;
        }
    }

    // 使用 UTF16
    this.coder = UTF16;
    this.value = StringUTF16.toBytes(value, off, len);
}
```

---

## 6. 源码结构

```
src/java.base/share/classes/java/lang/
├── String.java              # 核心 (~3500 行)
├── StringLatin1.java        # LATIN1 操作 (~500 行)
├── StringUTF16.java         # UTF16 操作 (~800 行)
├── StringConcatHelper.java  # 拼接辅助
├── StringBuilder.java       # 可变字符串
└── StringBuffer.java        # 同步版本

src/java.base/share/classes/java/lang/invoke/
└── StringConcatFactory.java # invokedynamic 拼接工厂
```

---

## 7. 贡献者

### JEP 254: Compact Strings

| 贡献者 | 角色 | 说明 |
|--------|------|------|
| **Aleksey Shipilev** | JEP Author | Red Hat，设计并主导 Compact Strings |
| **Vladimir Kozlov** | 实现 | Oracle，负责 aarch64 架构支持 (JDK-8156943) |
| **Stuart Marks** | Review | Oracle，API 设计审查 |

### 邮件列表讨论节选

> "The key idea is to store String data in byte[] instead of char[], with a coder field indicating the encoding."
> — Aleksey Shipilev, jdk9-dev@openjdk.org, 2015-11-03

> "For aarch64, we need intrinsics for StringLatin1/StringUTF16 operations to maintain performance parity."
> — Vladimir Kozlov, hotspot-dev@openjdk.org, 2016-05-12

---

## 8. 相关资源

- [JEP 254: Compact Strings](https://openjdk.org/jeps/254)
- [OpenJDK String 源码](https://github.com/openjdk/jdk/blob/master/src/java.base/share/classes/java/lang/String.java)
- [Compact Strings in JDK 9](https://openjdk.org/projects/jdk9/)
