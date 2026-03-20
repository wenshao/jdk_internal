# DateTime toString 优化

> **JDK-8337832**: Optimize datetime toString
> **PR**: [#20368](https://github.com/openjdk/jdk/pull/20368)
> **Author**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) (Alibaba)
> **性能提升**: +20-40% (日期时间格式化场景)

[← 返回 JDK 25](../)

---

## 一眼看懂

| 维度 | 内容 |
|------|------|
| **问题** | `LocalDateTime.toString()` 等方法创建多个临时字符串 |
| **解决** | 添加 `formatTo(StringBuilder)` 私有方法，直接写入缓冲区 |
| **受益场景** | 日志记录、序列化、调试输出 |
| **风险等级** | 🟢 低 - 添加私有方法，API 不变 |

---

## 问题背景

### 原始实现

```java
// LocalDateTime.toString() 原始实现
public String toString() {
    return date.toString() + 'T' + time.toString();
}
```

**问题**：每次调用会创建：
1. `date.toString()` 的临时 String
2. `time.toString()` 的临时 String
3. 拼接结果的 String

### 影响的类

- `LocalDateTime`
- `ZonedDateTime`
- `OffsetDateTime`
- `OffsetTime`

---

## 优化方案

### 新增私有方法

```java
// 新增：直接写入 StringBuilder
private void formatTo(StringBuilder sb) {
    // 直接将日期时间格式化到 StringBuilder
    date.formatTo(sb);
    sb.append('T');
    time.formatTo(sb);
}

// 优化后的 toString
public String toString() {
    StringBuilder sb = new StringBuilder(32); // 预分配
    formatTo(sb);
    return sb.toString();
}
```

---

## 性能提升

| 场景 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| `LocalDateTime.toString()` | ~120 ns | ~85 ns | **+29%** |
| `ZonedDateTime.toString()` | ~180 ns | ~130 ns | **+28%** |
| 日志格式化 | 高开销 | 低开销 | **+30%** |

---

## 实际应用场景

### 日志记录

```java
// 每条日志都会调用 toString()
logger.info("Event at: " + LocalDateTime.now());
```

### JSON 序列化

```java
// Jackson 等框架会调用 toString()
public class Event {
    private LocalDateTime timestamp;
}
```

---

## 相关优化

同一作者 (Shaojin Wen) 的其他优化：

| Issue | 标题 |
|-------|------|
| [JDK-8339699](../../by-pr/8339/8339699.md) | DataOutputStream writeUTF 优化 |
| [JDK-8340232](../../by-pr/8340/8340232.md) | DataInputStream readUTF 优化 |

---

## 更多信息

- [完整 PR 分析](../../by-pr/8337/8337832.md)
- [贡献者档案](/by-contributor/profiles/shaojin-wen.md)
- [GitHub PR](https://github.com/openjdk/jdk/pull/20368)
- [Topic: Date/Time API](/by-topic/api/datetime/index.md)
- [相关 PR: JDK-8337279](../../by-pr/8337/8337279.md) - Share StringBuilder to format instant
- [相关 PR: JDK-8337168](/by-topic/api/datetime/prs/jdk-8337168.md) - Optimize LocalDateTime.toString

---

**最后更新**: 2026-03-20
