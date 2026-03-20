# 语言规范 (Language) 索引

> Java 语言规范相关 JSR

---

## 概览

| JSR | 标题 | JDK | 状态 | 说明 |
|-----|------|-----|------|------|
| [JSR 335](jsr-335.md) | Lambda Expressions | 8 | ✅ Final | 函数式接口、 Lambda |
| [JSR 394](jsr-394.md) | Pattern Matching for instanceof | 16 | ✅ Final | 类型模式匹配 |
| [JSR 395](jsr-395.md) | Records | 16 | ✅ Final | 记录类 |
| [JSR 397](jsr-397.md) | Sealed Classes | 17 | ✅ Final | 密封类/接口 |
| [JSR 398](jsr-398.md) | Pattern Matching for switch | 21 | ✅ Final | switch 模式匹配 |
| [JSR 409](jsr-409.md) | Sealed Classes (二次) | 17 | ✅ Final | 正式发布 |
| [JSR 411](jsr-411.md) | Pattern Matching for switch (二次) | 21 | ✅ Final | 正式发布 |
| [JSR 427](jsr-427.md) | Pattern Matching | 23 | ✅ Final | switch 模式匹配 (正式) |
| [Valhalla](valhalla-value-types.md) | Value Types | TBD | 🚧 开发中 | 值类型 (非正式 JSR) |

---

## 孵化项目

### Project Valhalla (值类型)

> **状态**: 🚧 开发中 | **分支**: lworld

值类型是 Java 语言自泛型以来最大的变革，目标是消除装箱开销。

```java
value record Point(int x, int y) { }
```

**详见**: [Valhalla: Value Types](valhalla-value-types.md)

---

## 详解

- [JSR 335: Lambda Expressions](jsr-335.md)
- [JSR 394: Pattern Matching for instanceof](jsr-394.md)
- [JSR 395: Records](jsr-395.md)
- [JSR 397: Sealed Classes](jsr-397.md)
- [JSR 398: Pattern Matching for switch](jsr-398.md)
- [JSR 409: Sealed Classes (Second)](jsr-409.md)
- [JSR 411: Pattern Matching for switch (Second)](jsr-411.md)
- [JSR 427: Pattern Matching (Final)](jsr-427.md)
- [Valhalla: Value Types](valhalla-value-types.md)

---

## 相关链接

- [JCP JSR 列表](https://jcp.org/en/jsr/all)
- [OpenJDK JEPs](https://openjdk.org/jeps/)
- [JEP 索引](/jeps/)
- [Project Valhalla](https://openjdk.org/projects/valhalla/)
