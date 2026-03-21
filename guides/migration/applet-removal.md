# Applet API 移除迁移指南

> JDK 26 正式移除 Applet API，本文档提供迁移指导

---
## 目录

1. [背景](#1-背景)
2. [移除的 API](#2-移除的-api)
3. [迁移方案](#3-迁移方案)
4. [迁移步骤](#4-迁移步骤)
5. [常见问题](#5-常见问题)
6. [相关资源](#6-相关资源)

---


## 1. 背景

JEP 504 在 JDK 26 中移除了 Applet API。这是 Java 历史上重要的遗留代码清理。

### 移除时间线

| 版本 | 状态 |
|------|------|
| JDK 9 | 标记为废弃 (@Deprecated) |
| JDK 17 | forRemoval = true |
| JDK 26 | 正式移除 |

---

## 2. 移除的 API

### java.applet 包

| 类/接口 | 描述 |
|---------|------|
| `Applet` | Applet 基类 |
| `AppletStub` | Applet 存根接口 |
| `AudioClip` | 音频剪辑接口 |
| `AppletContext` | Applet 上下文 |
| `AppletInitializer` | Applet 初始化器 |

### 相关工具

- `appletviewer` 工具已移除
- HTML `<applet>` 标签支持已移除

---

## 3. 迁移方案

### 1. Web 应用迁移

| 原技术 | 推荐替代 |
|--------|----------|
| Applet | Web 框架 (Spring Boot, Jakarta EE) |
| Swing Applet | JavaFX Web 应用 |
| 企业应用 | 微服务架构 |

### 2. 桌面应用迁移

| 原技术 | 推荐替代 |
|--------|----------|
| Applet GUI | JavaFX 应用 |
| Swing 组件 | JavaFX 或 Swing 独立应用 |
| WebStart | jpackage + 自包含应用 |

### 3. 嵌入式内容迁移

| 原技术 | 推荐替代 |
|--------|----------|
| 网页嵌入 | JavaScript + REST API |
| 交互式内容 | WebAssembly (TeaVM, CheerpJ) |

---

## 4. 迁移步骤

### 1. 评估现有代码

```bash
# 查找 Applet 相关代码
grep -r "java.applet" src/
grep -r "extends Applet" src/
grep -r "JApplet" src/
```

### 2. 选择迁移路径

根据应用类型选择合适的替代技术：

- **简单工具**: 考虑命令行工具
- **GUI 应用**: 迁移到 JavaFX
- **Web 应用**: 迁移到现代 Web 框架

### 3. 重构代码

1. 移除 Applet 生命周期方法 (`init`, `start`, `stop`, `destroy`)
2. 将 GUI 代码迁移到独立窗口
3. 替换 Applet 特有功能 (如 `getCodeBase`, `getDocumentBase`)

### 4. 测试验证

- 功能测试
- 性能测试
- 兼容性测试

---

## 5. 常见问题

### Q: 为什么移除 Applet API？

A: Applet 技术已过时，现代浏览器已不再支持。维护成本高，安全风险大。

### Q: 现有 Applet 应用怎么办？

A: 建议迁移到现代技术栈。对于无法迁移的应用，可考虑：
- 使用旧版 JDK 运行
- 使用第三方解决方案 (CheerpJ)

### Q: Java Web Start 还能用吗？

A: Java Web Start 在 JDK 11 后已被移除。建议使用 jpackage 创建自包含应用。

---

## 6. 相关资源

- [JEP 504: Remove the Applet API](https://openjdk.org/jeps/504)
- [JavaFX 迁移指南](https://openjfx.io/openjfx-docs/)
- [jpackage 用户指南](https://docs.oracle.com/en/java/javase/21/jpackage/)