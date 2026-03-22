# 从 JDK 21 迁移到 JDK 26

> **目标版本**: JDK 26 (GA 2026-03-17)
> **来源版本**: JDK 21 (LTS)

---
## 目录

1. [快速切换](#1-快速切换)
2. [重要变更](#2-重要变更)
3. [新特性推荐](#3-新特性推荐)
4. [JVM 参数更新](#4-jvm-参数更新)
5. [测试清单](#5-测试清单)
6. [回滚方案](#6-回滚方案)
7. [更多信息](#7-更多信息)

---


## 1. 快速切换

```bash
# SDKMAN
sdk install java 26
sdk default java 26

# 验证版本
java -version  # 应显示 openjdk version "26"
```

---

## 2. 重要变更

### ✅ 兼容性

JDK 26 与 JDK 21 具有良好的二进制兼容性，大部分应用无需修改即可运行。

### ⚠️ 破坏性变更

| 变更 | 影响 | 建议 |
|------|------|------|
| Applet API 移除 | 使用 `javax.swing.JApplet` 的应用 | 迁移到现代 Web 技术 |
| Final 语义更严格 | 依赖 final 字段构造行为的代码 | 检查并修复 |
| 部分预览特性默认值变化 | 使用 `--enable-preview` 的代码 | 明确启用预览特性 |

---

## 3. 新特性推荐

### 网络应用

```java
// HTTP/3 自动协商
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_3)  // 新增
    .build();
```

### 并发编程

```java
// 结构化并发 (第六次预览)
try (var scope = StructuredTaskScope.open()) {
    Subtask<String> user = scope.fork(() -> fetchUser());
    Subtask<List<Order>> orders = scope.fork(() -> fetchOrders());
    scope.join();
    return new Response(user.get(), orders.get());
}
```

### 性能优化

```bash
# G1 GC 自动获得 10-20% 吞吐量提升
java -XX:+UseG1GC MyApp

# 大内存应用启用 ZGC (默认分代模式)
java -XX:+UseZGC MyApp
```

---

## 4. JVM 参数更新

| 参数 (JDK 21) | 参数 (JDK 26) | 说明 |
|--------------|--------------|------|
| `-XX:+UseZGC` | `-XX:+UseZGC` | 分代 ZGC 已为默认模式，无需额外参数 |

---

## 5. 测试清单

- [ ] 编译通过 (`javac --release 26`)
- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 性能基准测试
- [ ] 预览特性测试 (如使用)

---

## 6. 回滚方案

如果遇到问题：

```bash
# SDKMAN
sdk default java 21

# 或直接使用特定版本
sdk use java 21
```

---

## 7. 更多信息

- [JDK 26 发布说明](https://openjdk.org/projects/jdk/26/)
- [JDK 26 完整特性](/by-version/jdk26/README.md)
- [JDK 26 JEP 列表](../jeps.md)
