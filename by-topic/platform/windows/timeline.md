# Windows 平台时间线

JDK 在 Windows 平台上的演进历史。

[← 返回 Windows 平台](./)

---
## 目录

1. [JDK 1.0 - 1.4: 基础支持](#1-jdk-10---14-基础支持)
2. [JDK 5-8: 现代支持](#2-jdk-5-8-现代支持)
3. [JDK 14: jpackage 正式版](#3-jdk-14-jpackage-正式版)
4. [JDK 17: 安装程序改进](#4-jdk-17-安装程序改进)
5. [JDK 21: 废弃 32 位](#5-jdk-21-废弃-32-位)
6. [JDK 26: 移除 32 位支持](#6-jdk-26-移除-32-位支持)
7. [Windows 版本支持](#7-windows-版本支持)
8. [架构演进](#8-架构演进)
9. [特性时间线](#9-特性时间线)
10. [核心贡献者](#10-核心贡献者)
11. [参考资料](#11-参考资料)

---


## 1. JDK 1.0 - 1.4: 基础支持

### JDK 1.0 (1996)
- Windows 95/NT 支持
- 绿色线程 (Green Threads)

### JDK 1.2 (1998)
- 原生线程引入
- 性能提升

### JDK 1.3 - 1.4
- HotSpot VM
- NIO 引入

---

## 2. JDK 5-8: 现代支持

### JDK 5 (2004)
- 泛型、注解
- 性能改进

### JDK 6 (2006)
- 脚本引擎
- JMX 改进

### JDK 8 (2014)
- Lambda 表达式
- Stream API

---

## 3. JDK 14: jpackage 正式版

### JEP 343: Packaging Tool

| 版本 | 日期 | 状态 |
|------|------|------|
| JDK 14 | 2020-03 | jpackage 孵化器 |
| JDK 15 | 2020-09 | jpackage 第二孵化器 |
| JDK 16 | 2021-03 | jpackage 正式版 |

**支持的包类型**:
- `msi`: Windows Installer
- `exe`: 可执行安装程序

---

## 4. JDK 17: 安装程序改进

### 安装体验改进

| 版本 | 日期 | 变化 |
|------|------|------|
| JDK 17 | 2021-09 | 改进 MSI 安装程序 |
| JDK 21 | 2023-09 | 优化安装体验 |
| JDK 26 | 2025 | 安装程序增强 |

---

## 5. JDK 21: 废弃 32 位

### JEP 449: Deprecate the Windows 32-bit x86 Port

| 版本 | 日期 | 状态 |
|------|------|------|
| JDK 21 | 2023-09 | 废弃 x86 (32位) |
| JDK 26 | 2025 | 移除 x86 (32位) |

**影响**:
- 不再提供 32 位 JDK
- 需要迁移到 64 位

---

## 6. JDK 26: 移除 32 位支持

### 完全移除

```powershell
# JDK 26+ 无 32 位版本
# 需要迁移到 64 位

# 迁移步骤:
# 1. 更新应用兼容性
# 2. 更新 JNI 库
# 3. 测试 64 位环境
```

---

## 7. Windows 版本支持

### 支持矩阵

| Windows 版本 | 最低 JDK | 推荐 JDK | EOL |
|--------------|----------|----------|-----|
| Windows 7 | JDK 8 | JDK 8 | 2020-01 |
| Windows 8.1 | JDK 8 | JDK 11 | 2023-01 |
| Windows 10 1507+ | JDK 8 | JDK 21 | 2025-10 |
| Windows 11 | JDK 17 | JDK 21 | - |
| Windows Server 2016 | JDK 8 | JDK 21 | 2027-01 |
| Windows Server 2019 | JDK 8 | JDK 21 | 2029-01 |
| Windows Server 2022 | JDK 11 | JDK 21 | 2031-01 |

---

## 8. 架构演进

```
JDK 1.0 ─── x86 (32位)
   │
JDK 5  ─── x64 (64位)
   │
JDK 21 ─── 废弃 x86 (32位)
   │
JDK 26 ─── 移除 x86 (32位)
   │        └── x64 (64位) 唯一支持
```

---

## 9. 特性时间线

### IOCP 支持

```
JDK 1.4 ─── NIO 引入
   │
JDK 7  ─── NIO.2 异步 I/O
   │
JDK 21 ─── IOCP 优化
```

### 服务支持

```
JDK 6  ─── Service Wrapper (第三方)
   │
JDK 14 ─── jpackage 服务支持
   │
JDK 21 ─── 服务集成改进
```

### 注册表集成

```
JDK 1.4 ─── Preferences API
   │
JDK 8  ─── 改进注册表访问
   │
JDK 17 ─── 注册表性能优化
```

---

## 10. 核心贡献者

| 贡献者 | 组织 | 主要贡献 |
|--------|------|----------|
| [Andrew Leonard](/by-contributor/profiles/andrew-leonard.md) | Oracle | Windows 构建 |
| [Thomas Stuefe](/by-contributor/profiles/thomas-stuefe.md) | Oracle | 跨平台支持 |

---

## 11. 参考资料

- [JEP 343: Packaging Tool](https://openjdk.org/jeps/343)
- [JEP 449](/jeps/tools/jep-449.md)
- [Windows 服务最佳实践](https://docs.microsoft.com/en-us/windows/win32/services/)

→ [返回 Windows 平台](./)
