# I/O 优化：DataInput/Output UTF 处理

> **JDK-8339699 + JDK-8340232**: Optimize readUTF/writeUTF
> **PRs**: [#20886](https://github.com/openjdk/jdk/pull/20886), [#20903](https://github.com/openjdk/jdk/pull/20903)
> **Author**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) (Alibaba)
> **性能提升**: +15-30% (Java 序列化、RMI 场景)

[← 返回 JDK 25](../)

---
## 目录

1. [一眼看懂](#1-一眼看懂)
2. [问题背景](#2-问题背景)
3. [优化方案](#3-优化方案)
4. [性能提升](#4-性能提升)
5. [实际应用场景](#5-实际应用场景)
6. [技术细节](#6-技术细节)
7. [相关 PR](#7-相关-pr)
8. [更多信息](#8-更多信息)

---


## 1. 一眼看懂

| 维度 | 内容 |
|------|------|
| **问题** | Modified UTF-8 编码处理使用逐字节/逐字符循环 |
| **解决** | 使用 `JLA.countPositives` 等内部方法批量处理 |
| **受益场景** | Java 序列化、RMI、自定义协议通信 |
| **风险等级** | 🟢 低 - 内部实现优化，API 不变 |

---

## 2. 问题背景

### Modified UTF-8

Java 特有的 UTF-8 变体，用于：
- **Java 序列化** - `ObjectOutputStream/ObjectInputStream`
- **RMI** - 远程方法调用
- **自定义协议** - 许多 Java 框架

### 原始实现问题

```java
// 问题1：逐字节检查 ASCII 前缀
while (count < utflen) {
    c = (int) bytearr[count] & 0xff;
    if (c > 127) break;
    count++;
    chararr[chararr_count++]=(char)c;
}

// 问题2：逐字符解码多字节序列
while (count < utflen) {
    c = (int) bytearr[count] & 0xff;
    switch (c >> 4) {
        // ... 每个字符单独处理
    }
}
```

---

## 3. 优化方案

### readUTF 优化 (JDK-8340232)

```java
// 优化后：使用批量处理
public static final String readUTF(DataInput in) throws IOException {
    // 使用 JLA.countPositives 批量扫描 ASCII
    int count = JLA.countPositives(bytearr, 0, utflen);

    // 使用 JLA.inflateBytesToChars 批量解码
    JLA.inflateBytesToChars(bytearr, 0, utflen, chararr, 0);
}
```

### writeUTF 优化 (JDK-8339699)

```java
// 新增：ModifiedUtf 工具类
class ModifiedUtf {
    static int encode(char[] str, int off, int len, byte[] dst) {
        // 使用优化的批量编码逻辑
        return JLA.countPositives(str, off, len, dst);
    }
}
```

---

## 4. 性能提升

| 操作 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| `readUTF()` (ASCII) | 180 ns | 125 ns | **+30%** |
| `readUTF()` (中文) | 320 ns | 265 ns | **+17%** |
| `writeUTF()` | 150 ns | 115 ns | **+23%** |
| 序列化/反序列化 | 高开销 | 低开销 | **+15-25%** |

---

## 5. 实际应用场景

### Java 序列化

```java
// ObjectOutputStream 使用 writeUTF
try (ObjectOutputStream oos = new ObjectOutputStream(fout)) {
    oos.writeObject(user);
}
```

### RMI 调用

```java
// RMI 使用 Modified UTF-8 传输字符串
RemoteInterface stub = (RemoteInterface) Naming.lookup("rmi://host/service");
```

---

## 6. 技术细节

### JLA (JavaLangAccess)

`JLA` 是 `java.lang` 包的内部工具类，提供高性能的数组操作：

| 方法 | 用途 |
|------|------|
| `countPositives` | 批量统计 ASCII 字符 |
| `inflateBytesToChars` | 批量字节转字符 |
| `compress` | 字符串压缩 |

---

## 7. 相关 PR

| PR | Issue | 标题 | 提升 |
|----|-------|------|------|
| #20886 | JDK-8339699 | DataOutputStream writeUTF | +15-25% |
| #20903 | JDK-8340232 | DataInputStream readUTF | +15-30% |

---

## 8. 更多信息

- [writeUTF PR 分析](../../../by-pr/8339/8339699.md)
- [readUTF PR 分析](../../../by-pr/8340/8340232.md)
- [贡献者档案](/by-contributor/profiles/shaojin-wen.md)
- [Topic: I/O API](/by-topic/api/io/index.md)
- [JDK 25](/by-version/jdk25/index.md)

---

**最后更新**: 2026-03-20
