# JDK 26 破坏性变更

> **版本**: JDK 26 (Feature Release) | **发布日期**: 2026-03-17

---
## 目录

1. [变更总览](#1-变更总览)
2. [Applet API 移除](#2-applet-api-移除)
3. [Final 语义更严格](#3-final-语义更严格)
4. [其他行为变更](#4-其他行为变更)
5. [检测与迁移](#5-检测与迁移)
6. [相关链接](#6-相关链接)

---


## 1. 变更总览

| 变更 | JEP | 影响范围 | 严重程度 | 迁移难度 |
|------|-----|----------|----------|----------|
| 移除 Applet API | JEP 504 | Applet 应用 | 🔴 高 | 中 |
| Final 语义更严格 | JEP 500 | 反射修改 final 字段 | 🟡 中 | 低-高 |
| Security Manager 进一步限制 | - | 依赖 SM 的应用 | 🟡 中 | 高 |

---

## 2. Applet API 移除

### JEP 504: Remove the Applet API

**背景**: Applet API 自 JDK 9 (JEP 289) 废弃，JDK 17 (JEP 398) 标记为 forRemoval，JDK 26 正式移除。

**移除的类和包**:
- `java.applet.*` (整个包)
- `javax.swing.JApplet`
- `java.beans.AppletInitializer`

**检测**:
```bash
# 搜索 Applet 用法
grep -rn 'import java.applet\|import javax.swing.JApplet\|extends Applet\|extends JApplet' src/

# 使用 jdeprscan
jdeprscan --release 26 myapp.jar | grep -i applet
```

**迁移方案**:

| 原有功能 | 替代技术 |
|----------|----------|
| 浏览器嵌入 Java | Web 应用 (Spring Boot, Quarkus) |
| GUI 应用分发 | jpackage 打包本地应用 |
| 沙箱执行 | 容器化部署 |

---

## 3. Final 语义更严格

### JEP 500: Prepare to Make Final Mean Final

**影响**: 禁止通过深度反射修改 `final` 字段。此前可以通过 `Field.setAccessible(true)` 修改 final 字段的值。

**受影响代码模式**:

```java
// ❌ JDK 26 中将产生警告，未来版本将抛异常
Field field = MyClass.class.getDeclaredField("CONSTANT");
field.setAccessible(true);
field.set(null, newValue);  // 修改 final 字段
```

**检测**:
```bash
# 运行时检测
java -Djdk.reflect.warnOnIllegalFinalFieldAccess=true MyApp

# 源码搜索
grep -rn 'setAccessible.*true' src/ | grep -v test/
```

**常见受影响场景**:

| 场景 | 影响程度 | 迁移方案 |
|------|----------|----------|
| 测试框架注入 mock | 低 | 使用构造器注入或 Mockito Agent |
| 序列化框架 | 中 | 升级框架版本 |
| 配置注入框架 | 中 | 使用非 final 字段或 setter |
| 遗留单例修改 | 高 | 重构设计模式 |

**迁移建议**:
```java
// ✅ 使用 VarHandle（JDK 9+，受控访问）
VarHandle handle = MethodHandles.lookup()
    .findVarHandle(MyClass.class, "field", String.class);

// ✅ 使用不可变设计
record Config(String value) {}  // 天然不可变
```

---

## 4. 其他行为变更

### Security Manager 进一步限制

延续 JDK 25 的趋势，Security Manager 的限制进一步加强。

### HTTP/3 协议协商

`HttpClient` 在支持 HTTP/3 的服务器上会自动协商升级到 HTTP/3。如果应用依赖特定的 HTTP 版本行为，需要注意：

```java
// 强制使用 HTTP/2（不升级到 HTTP/3）
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_2)
    .build();
```

### ZGC 非分代模式弃用

ZGC 非分代模式 (`-XX:-ZGenerational`) 在 JDK 26 中被标记为弃用，将在未来版本中移除。

---

## 5. 检测与迁移

### 快速兼容性检查

```bash
#!/bin/bash
echo "=== JDK 26 兼容性检查 ==="

echo "1. 检查 Applet API 用法..."
grep -rn 'java.applet\|JApplet\|extends Applet' src/ 2>/dev/null | head -5

echo "2. 检查 final 字段反射修改..."
grep -rn 'setAccessible.*true' src/ 2>/dev/null | head -5

echo "3. 检查 HTTP 版本硬编码..."
grep -rn 'HTTP_1_1\|HTTP_2' src/ 2>/dev/null | head -5

echo "=== 检查完成 ==="
```

---

## 6. 相关链接

- [JDK 26 主页](../index.md)
- [JDK 26 迁移指南](../migration/from-21.md)
- [JEP 504: Remove the Applet API](https://openjdk.org/jeps/504)
- [JEP 500: Prepare to Make Final Mean Final](https://openjdk.org/jeps/500)

---

[← 返回 JDK 26](../index.md)
