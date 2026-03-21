# String 构造函数优化

> **JDK-8357289**: Break down the String constructor into smaller methods
> **PR**: [#25290](https://github.com/openjdk/jdk/pull/25290)
> **Author**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) (Alibaba)
> **性能提升**: +5-10% (String 构造相关场景)

[← 返回 JDK 26](../)

---
## 目录

1. [一眼看懂](#1-一眼看懂)
2. [问题背景](#2-问题背景)
3. [优化方案](#3-优化方案)
4. [性能提升](#4-性能提升)
5. [实际应用场景](#5-实际应用场景)
6. [技术细节](#6-技术细节)
7. [相关优化](#7-相关优化)
8. [贡献者](#8-贡献者)
9. [更多信息](#9-更多信息)

---


## 1. 一眼看懂

| 维度 | 内容 |
|------|------|
| **问题** | String 构造函数代码大小 (852 bytes) 超过 JIT 内联阈值 (325 bytes) |
| **解决** | 拆分为多个小方法，使每个方法可被 JIT 内联 |
| **受益场景** | 字符串反序列化、JSON 处理、网络协议解析 |
| **风险等级** | 🟢 低 - 纯重构，行为不变 |

---

## 2. 问题背景

### JIT 内联阈值

HotSpot JIT 编译器有内联大小限制：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| **FreqInlineSize** | 325 bytes | 热点方法最大内联大小 |
| **MaxInlineSize** | 35 bytes | 普通方法最大内联大小 |

### 问题发现

通过 `-XX:+PrintInlining` 发现 String 构造函数无法被内联：

```
!  @ 8   java.lang.String::<init> (852 bytes)   failed to inline: hot method too big
```

**影响链**：
```
Charset.defaultCharset()
  └─ String.<init>(byte[], Charset)  <- 852 bytes，无法内联！
```

---

## 3. 优化方案

### 拆分前 vs 拆分后

```java
// 拆分前：852 bytes 的大方法
String(Charset charset, byte[] bytes, int offset, int length) {
    // 参数检查 + 编码 + 压缩 + 边界处理...全部在这里
}

// 拆分后：每个方法 < 325 bytes
String(Charset charset, byte[] bytes, int offset, int length) {
    // 只做参数检查和委托
    Objects.requireNonNull(charset);
    Result result = StringCoding.decode(charset, bytes, offset, length);
    this.value = result.value;
    this.coder = result.coder;
}

// 新增：可内联的创建方法 (45 bytes)
private static String create(byte[] value, int coder) {
    if (COMPACT_STRINGS && coder == LATIN1) {
        return new String(value, LATIN1);
    }
    return new String(value, UTF16);
}
```

### 优化效果验证

使用 `-XX:+PrintInlining` 验证：

```diff
!     @ 8   java.lang.String::<init> (852 bytes)   failed to inline: hot method too big
+@     @ 8   java.lang.String::create (45 bytes)   inline (hot)
+@     @ 8   java.lang.String::compress (123 bytes)   inline (hot)
```

---

## 4. 性能提升

| 场景 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| `new String(bytes, charset)` | 45.2 ns/op | 41.3 ns/op | **+9.4%** |
| `new String(bytes, off, len, charset)` | 48.6 ns/op | 43.8 ns/op | **+11.0%** |
| 字符串反序列化 | 125 ns/op | 113 ns/op | **+10.6%** |

---

## 5. 实际应用场景

### 1. JSON 反序列化

```java
// Jackson/Gson
ObjectMapper mapper = new ObjectMapper();
User user = mapper.readValue(json, User.class);
// 每个字符串字段都会调用 String 构造函数
```

### 2. HTTP 请求处理

```java
// HTTP 请求体解析
String body = new String(bytes, StandardCharsets.UTF_8);
```

### 3. 文件读取

```java
// 读取文本文件
String content = Files.readString(path, StandardCharsets.UTF_8);
```

---

## 6. 技术细节

### 为什么是 325 bytes？

这是 HotSpot JVM 的硬编码内联阈值：

```cpp
// HotSpot 源码 (src/hotspot/share/compiler/compileBroker.cpp)
product(intx, FreqInlineSize, 325,
         "Maximum bytecode size of a method to be inlined")
```

### 为什么不用静态工厂方法？

1. **构造函数必须保留** - Java 语言规范要求
2. **拆分后仍可内联** - 小方法可以被 JIT 优化器内联
3. **静态辅助方法** - `create()` 方法是静态的，更容易内联

---

## 7. 相关优化

同一作者 (Shaojin Wen) 的其他 String 优化：

| Issue | 标题 | 提升 |
|-------|------|------|
| [JDK-8333893](/by-pr/8333/8333893.md) | StringBuilder boolean/null 优化 | +5-15% |
| [JDK-8353741](/by-pr/8355/8353741.md) | UUID.toString 消除表查找 | +82% |
| [JDK-8336856](/by-pr/8336/8336856.md) | 隐藏类拼接策略 | 启动优化 |

---

## 8. 贡献者

**作者**: [Shaojin Wen (温绍锦)](/by-contributor/profiles/shaojin-wen.md)
- **组织**: [Alibaba](/contributors/orgs/alibaba.md)
- **专长**: JIT 优化、字符串处理、核心库
- **Integrated PRs**: 97+
- **相关贡献**:
  - [JDK-8333893](/by-pr/8333/8333893.md): StringBuilder boolean/null 优化
  - [JDK-8353741](/by-pr/8355/8353741.md): UUID.toString 消除表查找
  - [JDK-8336856](/by-pr/8336/8336856.md): 隐藏类拼接策略

---

## 9. 更多信息

- [完整 PR 分析](/by-pr/8357/8357289.md) - 包含设计决策、代码审查要点
- [贡献者档案](/by-contributor/profiles/shaojin-wen.md) - Shaojin Wen
- [GitHub PR](https://github.com/openjdk/jdk/pull/25290)

---

**最后更新**: 2026-03-20
