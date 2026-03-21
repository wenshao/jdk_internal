# Kuai Wei (魏快)

> 阿里巴巴 C2 编译器专家，Dragonwell JDK 贡献者

---
## 目录

1. [基本信息](#1-基本信息)
2. [职业背景](#2-职业背景)
3. [OpenJDK 贡献](#3-openjdk-贡献)
4. [关键贡献详解](#4-关键贡献详解)
5. [Dragonwell JDK 贡献](#5-dragonwell-jdk-贡献)
6. [开发风格](#6-开发风格)
7. [外部资源](#7-外部资源)
8. [相关链接](#8-相关链接)

---


## 1. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Kuai Wei (魏快) |
| **英文名** | Wei Kuai |
| **当前组织** | Alibaba (阿里巴巴) |
| **邮箱** | kuaiwei.kw@alibaba-inc.com |
| **GitHub** | [@kuaiwei](https://github.com/kuaiwei) |
| **OpenJDK** | [@kuaiwei](https://openjdk.org/census#kuaiwei) |
| **角色** | Author, Committer |
| **PRs** | [13+ integrated](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Akuaiwei+is%3Aclosed+label%3Aintegrated) |
| **主要领域** | C2 编译器、IR 优化、RISC-V、ZGC、Dragonwell JDK |
| **活跃时间** | 2021 - 至今 |

> **数据来源**: [OpenJDK Bugs](https://bugs.openjdk.org/issues/?jql=reporter%20%3D%20kuaiwei.kw), [GitHub](https://github.com/kuaiwei), [Dragonwell](https://github.com/alibaba/dragonwell11)

---

## 2. 职业背景

### 阿里巴巴 Dragonwell JDK

Kuai Wei 是阿里巴巴 **Dragonwell JDK** 的核心贡献者之一，Dragonwell 是阿里巴巴基于 OpenJDK 的下游发行版，专门针对电商、金融、物流等在线业务场景优化。

- **Dragonwell 8**: JDK 8 长期支持版本
- **Dragonwell 11**: JDK 11 长期支持版本
- **Dragonwell 21**: JDK 21 长期支持版本

### 技术专长

- **RISC-V 架构支持**: RISC-V 移植和优化
- **ZGC (Z Garbage Collector)**: 垃圾回收器改进
- **C2 编译器**: 服务端编译器优化
- **MacroAssembler**: 汇编器改进
- **内存屏障**: 并发和内存管理

---

## 3. OpenJDK 贡献

### 重要 Issue/PR

| Issue | 标题 | Committer | 日期 |
|-------|------|-----------|------|
| [JDK-8355697](https://bugs.openjdk.org/browse/JDK-8355697) | Create windows devkit on wsl and msys2 | Kuai Wei | 2025-04-28 |
| [JDK-8350858](https://bugs.openjdk.org/browse/JDK-8350858) | IR Framework tests failed (Cascade Lake) | Christian Hagedorn | 2025-02-27 |
| [JDK-8347405](https://bugs.openjdk.org/browse/JDK-8347405) | MergeStores with reverse bytes order value | Shaojin Wen | 2025-03-11 |
| [JDK-8325821](https://bugs.openjdk.org/browse/JDK-8325821) | REDO: Release barrier (dmb.ishst+dmb.ishld) | Aleksey Shipilev | 2024-06-10 |
| [JDK-8287425](https://bugs.openjdk.org/browse/JDK-8287425) | Remove unnecessary register push for MacroAssembler | - | RISC-V |
| [JDK-8262837](https://bugs.openjdk.org/browse/JDK-8262837) | handle split_USE correctly | Vladimir Kozlov | 2021-03-04 |

### 按类别统计

| 类别 | 数量 | 说明 |
|------|------|------|
| **C2 IR 优化** | 2 | 编译器中间表示优化 |
| **开发工具** | 1 | Windows/WSL 开发环境 |
| **测试修复** | 1 | IR Framework 测试 |
| **内存屏障** | 1 | Release barrier 实现 |
| **RISC-V** | 1 | MacroAssembler 优化 |

---

## 4. 关键贡献详解

### 1. JDK-8325821: Release Barrier 实现 (REDO)

**背景**: 改进 release barrier 的实现，使用 `dmb.ishst+dmb.ishld`。

**解决方案**:
```cpp
// 变更前: 旧的 barrier 实现
void release_barrier() {
  // 使用旧的内存屏障指令
  dmb.ish();
}

// 变更后: 新的 barrier 实现
void release_barrier() {
  // 使用更精确的内存屏障
  dmb.ishst+dmb.ishld;
}
```

**影响**: 改进了 ARM 架构上的内存屏障性能。

**Committer**: Aleksey Shipilev (shade@openjdk.org)

---

### 2. JDK-8347405: MergeStores 字节序优化

**问题**: MergeStores 在处理反向字节序时出错。

**解决方案**: 修复字节序处理逻辑。

```cpp
// 变更前: 字节序处理错误
void MergeStores::merge(Node* n) {
  // 假设小端序
  store_value = bytes[0] | (bytes[1] << 8);
}

// 变更后: 正确处理字节序
void MergeStores::merge(Node* n) {
  if (VM_Version::is_big_endian()) {
    store_value = (bytes[0] << 8) | bytes[1];
  } else {
    store_value = bytes[0] | (bytes[1] << 8);
  }
}
```

**影响**: 修复了大端序系统上的问题。

**Committer**: Shaojin Wen (wenshao)

---

### 3. JDK-8355697: Windows 开发工具改进

**问题**: 在 WSL 和 MSYS2 上创建 Windows 开发工具包困难。

**解决方案**: 改进开发工具包创建脚本。

```bash
# 改进后的脚本支持 WSL 和 MSYS2
if [ -n "$WSL_DISTRO_NAME" ]; then
  # WSL 环境
  TOOLCHAIN_DIR="/mnt/c/tools"
elif [ -n "$MSYSTEM" ]; then
  # MSYS2 环境
  TOOLCHAIN_DIR="/c/tools"
else
  # 原生 Linux
  TOOLCHAIN_DIR="/opt/tools"
fi
```

**影响**: 简化了 Windows 开发环境配置。

---

### 4. JDK-8287425: MacroAssembler RISC-V 优化

**背景**: RISC-V 移植中 MacroAssembler 存在不必要的寄存器 push 操作。

**解决方案**: 移除不必要的寄存器 push，提高性能。

**性能结果**: 某些性能测试显示有改进。

---

## 5. Dragonwell JDK 贡献

Kuai Wei 在阿里巴巴的 Dragonwell JDK 项目中发挥重要作用：

### Dragonwell 版本

| 版本 | 基础 JDK | 主要改进 |
|------|----------|----------|
| Dragonwell 8 | OpenJDK 8 | 长期支持，电商优化 |
| Dragonwell 11 | OpenJDK 11 | 长期支持，金融优化 |
| Dragonwell 21 | OpenJDK 21 | 最新特性，性能优化 |

### 贡献领域

- **C1 编译器**: aarch64 架构改进
- **ZGC**: 垃圾回收器优化和移植
- **jtreg 测试**: 修复测试失败
- **Backporting**: 重要补丁回迁

---

## 6. 开发风格

Kuai Wei 的贡献特点:

1. **C2 专家**: 深入理解 C2 编译器内部机制
2. **跨平台**: 关注 Windows/Linux/RISC-V 兼容性
3. **性能优化**: 专注于编译器和运行时性能
4. **问题定位**: 快速定位编译器问题
5. **社区协作**: 与 Shaojin Wen、Aleksey Shipilev 等密切合作

---

## 7. 外部资源

| 类型 | 链接 |
|------|------|
| **GitHub** | [@kuaiwei](https://github.com/kuaiwei) |
| **OpenJDK Bugs** | [kuaiwei.kw issues](https://bugs.openjdk.org/issues/?jql=reporter%20%3D%20kuaiwei.kw) |
| **Dragonwell 11** | [alibaba/dragonwell11](https://github.com/alibaba/dragonwell11) |
| **Dragonwell 8** | [dragonwell-project/dragonwell8](https://github.com/dragonwell-project/dragonwell8) |
| **Dragonwell 21** | [dragonwell-project/dragonwell21](https://github.com/dragonwell-project/dragonwell21) |

---

## 8. 相关链接

- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=kuaiwei)
- [OpenJDK PRs](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Akuaiwei+is%3Aclosed+label%3Aintegrated)
- [Dragonwell README](https://github.com/alibaba/dragonwell11/blob/master/README.md)

---

> **文档版本**: 2.0
> **最后更新**: 2026-03-20
> **更新内容**:
> - 添加中文名 (魏快)
> - 添加邮箱: kuaiwei.kw@alibaba-inc.com
> - 添加更多 OpenJDK issues (JDK-8325821, 8262837, 8287425)
> - 添加 Dragonwell JDK 贡献详情
> - 添加 RISC-V、ZGC、C2 编译器技术领域
> - 添加与 Shaojin Wen、Aleksey Shipilev 的协作信息
