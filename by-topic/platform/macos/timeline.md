# macOS 平台时间线

JDK 在 macOS 平台上的演进历史。

[← 返回 macOS 平台](./)

---

## JDK 1.0 - 1.4: 早期支持

### JDK 1.0-1.2 (1996-1998)
- Mac OS Classic 有限支持
- 第三方移植

### JDK 1.3-1.4
- Mac OS X 引入后改进
- 基于 BSD 内核

---

## JDK 5-8: Mac OS X 时代

### JDK 5 (2004)
- Mac OS X 10.4 (Tiger) 支持

### JDK 6 (2006)
- Mac OS X 10.5 (Leopard) 支持
- Apple 提供 JDK

### JDK 7 (2011)
- Mac OS X 10.7 (Lion) 支持
- Oracle 接管 Mac JDK

---

## JDK 8: 最后的 Apple 版本

### JDK 8 (2014)

**重要里程碑**: Apple 停止分发 JDK

| 日期 | 事件 |
|------|------|
| 2010-10 | Oracle 宣布接管 Mac JDK |
| 2011 | JDK 7 首个 Oracle Mac 版本 |
| 2014 | JDK 8 发布 |

---

## JDK 16: Apple Silicon 预览

### M1 芯片发布 (2020)

```
2020-11 ─── Apple M1 芯片发布
   │
2021-03 ─── JDK 16 (AArch64 预览)
   │
2021-09 ─── JDK 17 (AArch64 正式版)
```

### JEP 358: Apple Silicon Support

| 版本 | 日期 | 状态 |
|------|------|------|
| JDK 16 | 2021-03 | AArch64 预览 |
| JDK 17 | 2021-09 | AArch64 正式版 |

---

## JDK 17: Metal 渲染管道

### JEP 382: Metal Rendering Pipeline

```
JDK 14 ─── Metal 渲染管道孵化
   │
JDK 16 ─── Metal 第二孵化器
   │
JDK 17 ─── Metal 正式版 (JEP 382)
   │
JDK 21 ─── Metal 性能优化
   │
JDK 26 ─── Metal 增强
```

### Metal vs OpenGL

| 特性 | OpenGL | Metal |
|------|--------|-------|
| **状态** | 废弃 | 活跃 |
| **性能** | 基准 | +20% |
| **支持** | macOS 10.14- | macOS 10.15+ |

---

## JDK 21: Metal 优化

### 性能改进

| 版本 | 日期 | 改进 |
|------|------|------|
| JDK 17.0.11 | 2023-05 | 修复 Metal 内存泄漏 |
| JDK 21 | 2023-09 | Metal 性能优化 |
| JDK 26 | 2025 | Metal 增强 |

---

## macOS 版本支持

### 支持矩阵

| macOS 版本 | 代码名 | 最低 JDK | 推荐 JDK | EOL |
|------------|--------|----------|----------|-----|
| macOS 10.15 | Catalina | JDK 8 | JDK 17 | 2022-11 |
| macOS 11 | Big Sur | JDK 8 | JDK 21 | - |
| macOS 12 | Monterey | JDK 8 | JDK 21 | - |
| macOS 13 | Ventura | JDK 8 | JDK 21 | - |
| macOS 14 | Sonoma | JDK 8 | JDK 21 | - |
| macOS 15 | Sequoia | JDK 21 | JDK 21+ | - |

---

## Apple Silicon 演进

```
M1 (2020) ─── AArch64 支持 (JDK 17)
   │
M1 Pro/Max (2021)
   │
M2 (2022) ─── 性能优化
   │
M2 Pro/Max/Ultra (2022)
   │
M3 (2023) ─── 性能提升
   │
M3 Pro/Max (2023)
   │
M4 (2024) ─── 最新优化
```

### 性能对比

| 芯片 | CPU | GPU | 统一内存 |
|------|-----|-----|----------|
| M1 | 8核 | 7/8核 | 8-16GB |
| M2 | 8/10核 | 10核 | 8-24GB |
| M3 | 8/10/12核 | 10/18核 | 8-36GB |
| M4 | 10核 | 10核 | 16GB+ |

---

## 架构支持

```
JDK 1.0 ─── PowerPC (早期)
   │
JDK 5  ─── Intel x86 (32位)
   │
JDK 6  ─── Intel x64 (64位)
   │
JDK 16 ─── Apple Silicon 预览
   │
JDK 17 ─── Apple Silicon 正式版
   │        └── Intel x64 (持续支持)
```

---

## 公证要求

### 公证时间线

```
2019 ─── macOS 10.15: 公证要求引入
   │
2020 ─── macOS 11: 公证强制
   │
2021 ─── JDK 17: jpackage 签名支持
   │
2023 ─── JDK 21: 签名工具改进
```

### 公证流程

```bash
# 1. 代码签名
codesign --force --deep --sign "Developer ID Application" MyApp.app

# 2. 提交公证
xcrun notarytool submit MyApp.zip --wait

# 3. Staple 公证
xcrun stapler staple MyApp.app
```

---

## 核心贡献者

| 贡献者 | 组织 | 主要贡献 |
|--------|------|----------|
| [Kevin Walls](/by-contributor/profiles/kevin-walls.md) | Oracle | macOS 构建 |
| [Goetz Lindenmaier](/by-contributor/profiles/goetz-lindenmaier.md) | Oracle | 跨平台支持 |

---

## 参考资料

- [JEP 358: Apple Silicon Support](https://openjdk.org/jeps/358)
- [JEP 382: Metal Rendering Pipeline](https://openjdk.org/jeps/382)
- [Apple 开发者文档](https://developer.apple.com/macos/)

→ [返回 macOS 平台](./)
