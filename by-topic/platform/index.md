# 平台特定主题

跨平台追踪 JDK 在不同操作系统上的演进、问题和优化。本页面提供各平台支持状态的全面概览，涵盖 Linux、Windows、macOS 以及容器环境，并记录构建系统演进和关键 JEP 变更。

---
## 目录

1. [平台概览](#1-平台概览)
2. [各 JDK 版本平台支持矩阵](#2-各-jdk-版本平台支持矩阵)
3. [Linux 平台深度分析](#3-linux-平台深度分析)
4. [macOS 平台深度分析](#4-macos-平台深度分析)
5. [Windows 平台深度分析](#5-windows-平台深度分析)
6. [容器环境最佳实践](#6-容器环境最佳实践)
7. [平台相关 JEP 汇总](#7-平台相关-jep-汇总)
8. [构建系统演进](#8-构建系统演进)
9. [子主题索引](#9-子主题索引)
10. [平台对比](#10-平台对比)
11. [常见问题](#11-常见问题)
12. [最佳实践](#12-最佳实践)
13. [相关链接](#13-相关链接)

---


## 1. 平台概览

| 平台 | 支持状态 | 主要架构 | 特有特性 |
|------|----------|----------|----------|
| **Linux** | 主要平台 | x64, aarch64, ppc64le, s390x, riscv64 | 容器优化、cgroup v1/v2 支持、大页内存 |
| **Windows** | 主要平台 | x64 (32 位已移除, JDK 24+) | 注册表集成、服务支持、IOCP 异步 I/O |
| **macOS** | 主要平台 | x64, aarch64 (Apple Silicon) | Metal 渲染管道、公证要求、W^X 内存保护 |
| **RISC-V** | Linux 平台 | riscv64 (RV64GV) | JDK 19 起主线集成，实验性 RVV/Zba/Zbb |
| **容器** | 跨平台 | 所有架构 | 资源限制感知、cgroup 集成、紧凑对象头优化 |

---

## 2. 各 JDK 版本平台支持矩阵

### 架构支持状态

| 平台 / 架构 | JDK 8 | JDK 11 | JDK 17 | JDK 21 | JDK 24 | JDK 25 (LTS) | JDK 26 |
|-------------|--------|--------|--------|--------|--------|---------------|--------|
| **Linux x64** | LTS | LTS | LTS | LTS | GA | LTS | GA |
| **Linux aarch64** | -- | GA | LTS | LTS | GA | LTS | GA |
| **Linux ppc64le** | GA | GA | LTS | LTS | GA | LTS | GA |
| **Linux s390x** | GA | GA | LTS | LTS | GA | LTS | GA |
| **Linux riscv64** | -- | -- | -- | GA | GA | GA | GA |
| **Linux x86 (32位)** | GA | GA | GA | GA | 废弃 | 移除 | 移除 |
| **Windows x64** | LTS | LTS | LTS | LTS | GA | LTS | GA |
| **Windows x86 (32位)** | LTS | LTS | LTS | 废弃 | 移除 | -- | -- |
| **Windows aarch64** | -- | -- | -- | 实验性 | 实验性 | 实验性 | 实验性 |
| **macOS x64** | LTS | LTS | LTS | LTS | GA | LTS | GA |
| **macOS aarch64** | -- | -- | LTS | LTS | GA | LTS | GA |

> **说明**: LTS = 长期支持版本, GA = 正式发布, 废弃 = 标记为废弃, 移除 = 代码已移除, -- = 不支持

### 功能支持矩阵

| 功能 | Linux | Windows | macOS | 容器 |
|------|-------|---------|-------|------|
| **ZGC** | x64/aarch64 | x64 | x64/aarch64 | 所有 |
| **Shenandoah** | x64/aarch64 | x64 | x64/aarch64 | 所有 |
| **Virtual Threads** | 全架构 | x64 | 全架构 | 所有 |
| **jpackage** | deb/rpm | msi/exe | dmg/pkg | N/A |
| **容器感知** | 原生 | 有限 | 有限 | 原生 |
| **紧凑对象头 (JDK 25+)** | x64/aarch64 | x64 | x64/aarch64 | 所有 |
| **RISC-V 端口** | riscv64 | -- | -- | Linux |
| **大页内存** | THP + 显式 | 显式 | 有限 | 继承宿主 |

---

## 3. Linux 平台深度分析

### [Linux 平台](linux/) -- 详细文档

Linux 是 JDK 开发和部署的首要平台，拥有最完善的支持和最佳性能。

| 主题 | 说明 |
|------|------|
| [容器支持](linux/containers.md) | Docker/Kubernetes 资源感知 |
| [cgroup 支持](linux/cgroup.md) | cgroup v1/v2 内存和 CPU 检测 |
| [性能调优](linux/performance.md) | Linux 特定性能优化 |
| [系统调用](linux/syscalls.md) | Linux 系统调用优化 |

### 容器感知演进

JDK 的 Linux 容器感知能力经历了多个版本的逐步完善：

```
JDK 8  ──── 无容器感知: 直接读取宿主机 /proc，导致资源检测错误
          │
JDK 10 ──── 容器感知引入 (JEP 307)
          │   - 自动检测 CPU/内存限制
          │   - 引入 -XX:+UseContainerSupport 标志
          │   - 读取 cgroup v1 信息
          │
JDK 11 ──── 改进容器检测
          │   - 更准确的 CPU 配额计算
          │   - 修复多个边界条件检测问题
          │
JDK 14 ──── cgroup v2 初步支持
          │   - 识别 cgroup v2 文件系统
          │
JDK 17 ──── cgroup v2 改进
          │   - 更好的内存检测 (memory.max / memory.current)
          │   - CPU 配额检测优化 (cpu.max)
          │
JDK 21 ──── cgroup v2 完整支持
          │   - 完整的 cgroup v2 统一层级支持
          │   - 混合 cgroup v1/v2 环境兼容
          │
JDK 24 ──── 紧凑对象头实验性支持 (JEP 450)
          │   废弃 Linux 32 位 x86 端口 (JEP 501)
          │
JDK 25 ──── 紧凑对象头正式版 (JEP 519)，内存减少 10-20%
          │   移除 Linux 32 位 x86 端口 (JEP 503)
          │   JFR CPU 时间分析 (JEP 509)
          │
JDK 26 ──── AOT 类加载与链接 (JEP 483)，容器启动优化
              G1 GC 减少同步 (JEP 522)
```

### cgroup v2 支持详解

随着 Ubuntu 21.10+、Fedora 31+、Debian 11+ 等主流发行版默认启用 cgroup v2，JDK 的完整 cgroup v2 支持变得至关重要。

| 特性 | cgroup v1 | cgroup v2 | JDK 最低版本 |
|------|-----------|-----------|-------------|
| **内存限制检测** | memory.limit_in_bytes | memory.max | JDK 10 / JDK 14 |
| **内存使用检测** | memory.usage_in_bytes | memory.current | JDK 10 / JDK 14 |
| **CPU 配额检测** | cpu.cfs_quota_us + cpu.cfs_period_us | cpu.max | JDK 10 / JDK 17 |
| **CPU 使用统计** | cpuacct.usage | cpu.stat | JDK 11 / JDK 21 |
| **完整支持** | JDK 8+ | JDK 21+ | -- |

### io_uring 状态

io_uring 是 Linux 5.1+ 引入的高性能异步 I/O 接口，目前 JDK 尚未提供官方内置支持。现状如下：

| 方面 | 状态 |
|------|------|
| **JDK 官方支持** | 无，尚无正式 JEP 提案 |
| **当前异步 I/O** | NIO2 基于 epoll (LinuxAsynchronousChannelProvider) |
| **第三方方案** | JUring 库 -- 基于 Panama FFM API 提供 io_uring 绑定 |
| **性能收益 (JUring)** | 本地文件 +33%，远程文件 +78% (相比 NIO FileChannel) |
| **内核要求** | Linux 5.1+ (推荐 5.11+ 以获得完整特性) |
| **潜在集成路径** | Panama FFM API (JDK 22 正式版) 降低了集成门槛 |

---

## 4. macOS 平台深度分析

### [macOS 平台](macos/) -- 详细文档

Apple 设备开发平台，近年经历了从 Intel 到 Apple Silicon 的重大架构转型。

| 主题 | 说明 |
|------|------|
| [Apple Silicon](macos/apple-silicon.md) | M1/M2/M3/M4 原生支持 |
| [Metal 渲染](macos/metal.md) | Metal 渲染管道 |
| [公证要求](macos/notarization.md) | macOS 应用签名 |
| [性能调优](macos/performance.md) | macOS 特定优化 |

### Apple Silicon 支持 (JEP 391)

JEP 391 于 JDK 17 正式引入 macOS/AArch64 端口，使 JDK 原生运行在 Apple M 系列芯片上。

**技术要点**:
- 基于已有的 linux/aarch64 和 macos/x64 端口，通过条件编译适配 macOS ABI 差异
- 实现 W^X (Write-XOR-Execute) 内存保护 -- macOS/AArch64 禁止内存同时可写可执行
- 使用 `pthread_jit_write_protect_np` API 在代码生成和执行间切换
- 支持 Apple 统一内存架构 (UMA)，CPU/GPU 共享内存池

| 芯片系列 | 发布年份 | 核心配置 | JDK 支持状态 |
|----------|----------|----------|-------------|
| **M1 / M1 Pro/Max/Ultra** | 2020-2022 | 8-20 核 | JDK 17+ 完全支持 |
| **M2 / M2 Pro/Max/Ultra** | 2022-2023 | 8-24 核 | JDK 17+ 完全支持 |
| **M3 / M3 Pro/Max** | 2023-2024 | 8-16 核 | JDK 17+ 完全支持 |
| **M4 / M4 Pro/Max** | 2024-2025 | 10-16 核 | JDK 21+ 推荐 |

**性能对比 (Apple Silicon 原生 vs Intel Rosetta 2)**:

| 指标 | Apple Silicon 原生 | Intel via Rosetta 2 |
|------|-------------------|---------------------|
| **启动速度** | 基准 | -20~40% |
| **稳态吞吐量** | 基准 | -20~30% |
| **能效比** | 基准 | -50~60% |
| **内存效率** | 基准 (UMA) | 额外翻译开销 |

### Metal 渲染管道 (JEP 382)

JEP 382 实现了基于 Apple Metal API 的 Java 2D 内部渲染管道，替代已被 Apple 废弃的 OpenGL。

**背景**: Apple 于 macOS 10.14 (2018 年 9 月) 废弃 OpenGL，Java 2D 完全依赖 OpenGL 进行内部渲染，因此必须迁移到 Metal。

**演进时间线**:
```
JDK 17 ──── Metal 渲染管道引入 (JEP 382)
          │   - 作为可选管道，默认仍使用 OpenGL
          │   - 启用: -Dsun.java2d.metal=true
          │
JDK 19 ──── Metal 成为默认渲染管道 (build 18 起)
          │   - 替代 OpenGL 作为默认选项
          │   - 回退: -Dsun.java2d.metal=false
          │
JDK 21 ──── Metal 性能优化
          │   - 修复内存泄漏 (影响 JDK 17.0.0-17.0.10)
          │   - 渲染性能提升约 15-25%
          │
JDK 26 ──── Metal 增强与稳定性改进
```

**性能对比 (Metal vs OpenGL)**:

| 渲染场景 | OpenGL | Metal | 改进幅度 |
|----------|--------|-------|----------|
| 2D 基本渲染 | 基准 | +15% | 明显 |
| 图像处理/变换 | 基准 | +25% | 显著 |
| Swing 动画 | 基准 | +20% | 明显 |
| GPU 内存占用 | 基准 | -10% | 改善 |

### 公证 (Notarization) 要求

macOS 10.15+ 要求分发的应用必须经过 Apple 公证。对于使用 jpackage 打包的 Java 应用，需要：

1. **开发者证书签名** -- Developer ID Application 证书
2. **提交 Apple 公证服务** -- 使用 `xcrun notarytool submit`
3. **Staple 公证结果** -- 使用 `xcrun stapler staple`
4. **分发签名后的应用** -- dmg/pkg 格式

---

## 5. Windows 平台深度分析

### [Windows 平台](windows/) -- 详细文档

Windows 是企业 Java 部署的重要平台。

| 主题 | 说明 |
|------|------|
| [安装与部署](windows/installation.md) | MSI/EXE 安装程序 |
| [服务集成](windows/service.md) | Windows 服务支持 |
| [注册表集成](windows/registry.md) | Java Preferences API |
| [性能调优](windows/performance.md) | Windows 特定优化 |

### 32 位端口移除历程

32 位 x86 端口的移除分为 Windows 和 Linux 两条线路，最终全部完成：

**Windows 32 位 x86**:

| 版本 | JEP | 操作 | 说明 |
|------|-----|------|------|
| JDK 21 | JEP 449 | 废弃 | Virtual Threads 在 Win32 上退化为内核线程，无法获得 Loom 收益 |
| JDK 24 | JEP 479 | 移除 | 移除全部 Windows 32 位 x86 源码和构建支持 |

**Linux 32 位 x86** (最后残余的 32 位端口):

| 版本 | JEP | 操作 | 说明 |
|------|-----|------|------|
| JDK 24 | JEP 501 | 废弃 | 无新 32 位 x86 硬件生产，不再有行业需求 |
| JDK 25 | JEP 503 | 移除 | 移除后 Zero 端口成为唯一在 32 位 x86 上运行 Java 的方式 |

> **影响**: 32 位端口的移除使新特性不再需要实现 32 位回退，降低了维护成本并解锁了更多优化空间。

### jpackage 演进 (JEP 343 / JEP 392)

jpackage 工具将 Java 应用打包为平台原生安装包：

```
JDK 14 ──── jpackage 孵化版 (JEP 343)
          │   - 基于 JavaFX javapackager 重写
          │   - 移除 Java Web Start 和 JavaFX 相关特性
          │   - 模块名: jdk.incubator.jpackage
          │
JDK 15 ──── jpackage 继续孵化
          │   - 收集反馈，完善功能
          │
JDK 16 ──── jpackage 正式版 (JEP 392)
          │   - 模块名改为 jdk.jpackage
          │   - --bind-services 替换为 --jlink-options
          │
JDK 17+ ──── 持续改进
              - 安装程序定制选项增加
              - 跨平台一致性增强
```

**各平台支持的包格式**:

| 平台 | 包格式 | 说明 |
|------|--------|------|
| **Windows** | msi, exe | MSI 支持企业组策略分发 |
| **macOS** | dmg, pkg | 支持代码签名和公证集成 |
| **Linux** | deb, rpm | 符合各发行版包管理规范 |

---

## 6. 容器环境最佳实践

### [容器环境](containers/) -- 详细文档

| 主题 | 说明 |
|------|------|
| [资源感知](containers/resource-awareness.md) | CPU/内存限制检测 |
| [Docker 优化](containers/docker.md) | Docker 最佳实践 |
| [Kubernetes](containers/kubernetes.md) | K8s 部署优化 |
| [镜像优化](containers/images.md) | 容器镜像最佳实践 |

### 内存检测与配置

容器环境中 JVM 内存配置是最关键的调优点。推荐使用百分比方式配置，而非固定值：

```bash
# 推荐: 基于容器限制的百分比配置
-XX:+UseContainerSupport          # 默认启用 (JDK 10+)
-XX:MaxRAMPercentage=75.0         # 堆内存占容器内存的 75%
-XX:InitialRAMPercentage=50.0     # 初始堆占 50%
-XX:MinRAMPercentage=25.0         # 最小堆占 25%

# 原生内存预留 (避免 OOM Killer)
# 容器 1GB → 堆 ~750MB，留 ~250MB 给线程栈/Metaspace/直接内存/JIT 代码缓存
-XX:MaxDirectMemorySize=128m      # 限制直接内存
-XX:MaxMetaspaceSize=256m         # 限制 Metaspace
```

**内存分配拆解 (1GB 容器示例)**:

| 内存区域 | 推荐占比 | 大小 (1GB 容器) |
|----------|----------|----------------|
| Java 堆 | 70-75% | 700-750 MB |
| Metaspace | 5-10% | 50-100 MB |
| 线程栈 | 5-8% | 50-80 MB |
| 直接内存 | 3-5% | 30-50 MB |
| JIT 代码缓存 | 3-5% | 30-50 MB |
| 其他 (JVM 内部) | 5-10% | 50-100 MB |

### CPU 检测与配置

```bash
# CPU 检测 (JDK 10+)
-XX:+UseContainerSupport          # 自动读取 cgroup CPU 配额
-XX:ActiveProcessorCount=4        # 手动覆盖 (整数值，无小数 CPU 支持)

# 影响的关键参数:
# - ParallelGCThreads (GC 并行线程数)
# - ConcGCThreads (并发 GC 线程数)
# - CICompilerCount (JIT 编译线程数)
# - ForkJoinPool.commonPool 并行度
```

### 容器环境 GC 选择指南

| GC 类型 | 适用场景 | 容器最低内存 | 启动标志 |
|---------|---------|-------------|---------|
| **Serial GC** | 微服务、极小容器 | 64-256 MB | `-XX:+UseSerialGC` |
| **G1 GC** | 通用、中大型服务 | 512 MB+ | `-XX:+UseG1GC` (默认) |
| **ZGC** | 低延迟要求 | 1 GB+ | `-XX:+UseZGC` |
| **Shenandoah** | 低延迟、Red Hat 生态 | 1 GB+ | `-XX:+UseShenandoahGC` |

### 容器启动优化

```bash
# CDS (Class Data Sharing) -- 减少启动时间 20-40%
-XX:SharedArchiveFile=app.jsa

# AOT 类加载 (JDK 26+, JEP 483) -- 容器冷启动显著改善
# 训练阶段:
java -XX:AOTCacheOutput=app.aot -jar app.jar
# 生产运行:
java -XX:AOTCache=app.aot -jar app.jar

# 紧凑对象头 (JDK 25+, JEP 519) -- 堆使用减少约 10-20%
-XX:+UseCompactObjectHeaders
```

---

## 7. 平台相关 JEP 汇总

### 平台端口与架构

| JEP | 版本 | 标题 | 说明 |
|-----|------|------|------|
| JEP 237 | JDK 9 | Linux/AArch64 Port | Linux ARM 64 位端口 |
| JEP 388 | JDK 16 | Windows/AArch64 Port | Windows ARM 64 位端口 |
| JEP 391 | JDK 17 | macOS/AArch64 Port | Apple Silicon 原生支持，W^X 内存保护 |
| JEP 422 | JDK 19 | Linux/RISC-V Port | RISC-V 64 位端口主线集成 |
| JEP 449 | JDK 21 | Deprecate Windows 32-bit x86 | 废弃 Windows 32 位端口 |
| JEP 479 | JDK 24 | Remove Windows 32-bit x86 | 移除 Windows 32 位端口 |
| JEP 501 | JDK 24 | Deprecate 32-bit x86 Port | 废弃 Linux 32 位端口 (最后残余) |
| JEP 503 | JDK 25 | Remove 32-bit x86 Port | 移除全部 32 位 x86 端口 |

### 图形与渲染

| JEP | 版本 | 标题 | 说明 |
|-----|------|------|------|
| JEP 382 | JDK 17 | New macOS Rendering Pipeline | Metal 渲染管道替代 OpenGL |

### 容器与运行时

| JEP | 版本 | 标题 | 说明 |
|-----|------|------|------|
| JEP 307 | JDK 10 | Parallel Full GC for G1 | G1 Full GC 并行化 |
| JDK-8146115 | JDK 10 | Container Awareness | 容器资源感知 (UseContainerSupport) |
| JEP 450 | JDK 24 | Compact Object Headers (Experimental) | 紧凑对象头实验版 |
| JEP 519 | JDK 25 | Compact Object Headers | 紧凑对象头正式版 |
| JEP 483 | JDK 26 | AOT Class Loading & Linking | AOT 类加载，容器启动优化 |
| JEP 522 | JDK 26 | G1 GC: Reduce Synchronization | G1 减少同步提高吞吐 |

### 打包与分发

| JEP | 版本 | 标题 | 说明 |
|-----|------|------|------|
| JEP 138 | JDK 9 | Autoconf-Based Build System | 构建系统迁移到 autoconf |
| JEP 343 | JDK 14 | Packaging Tool (Incubator) | jpackage 孵化版 |
| JEP 392 | JDK 16 | Packaging Tool | jpackage 正式版 |

---

## 8. 构建系统演进

OpenJDK 构建系统经历了从传统 Makefile 到现代 autoconf 体系的重大转型。

### 演进时间线

```
JDK 6/7 ──── 传统 Makefile 体系
            │ - 依赖环境变量控制构建选项
            │ - 递归 Makefile 结构
            │ - 跨平台构建配置困难
            │
JDK 8   ──── 过渡期
            │ - 开始引入 autoconf
            │ - 新旧构建系统并存
            │
JDK 9   ──── autoconf 构建系统正式化 (JEP 138)
            │ - ./configure 脚本自动检测系统配置
            │ - 移除递归 Makefile，改用扁平结构
            │ - M4 宏定义 (configure.ac) 生成 configure 脚本
            │ - autoconf 2.69 用于重新生成 configure
            │
JDK 11+ ──── 持续完善
            │ - 交叉编译支持增强
            │ - 构建性能优化
            │
JDK 17+ ──── 现代化构建
            │ - Apple Silicon 交叉编译支持
            │ - 更好的工具链检测
            │
JDK 24+ ──── 构建简化
              - 移除 32 位端口后构建矩阵简化
              - 减少平台特定代码路径
```

### 构建流程

```bash
# 标准构建流程 (JDK 9+)
bash configure --with-debug-level=release    # 配置
make images                                  # 构建
make test                                    # 测试

# 交叉编译示例 (在 x64 上为 aarch64 构建)
bash configure \
    --openjdk-target=aarch64-linux-gnu \
    --with-sysroot=/usr/aarch64-linux-gnu
make images
```

---

## 9. 子主题索引

### [Linux 平台](linux/)

| 主题 | 说明 |
|------|------|
| [容器支持](linux/containers.md) | Docker/Kubernetes 资源感知 |
| [cgroup 支持](linux/cgroup.md) | cgroup v1/v2 内存和 CPU 检测 |
| [性能调优](linux/performance.md) | Linux 特定性能优化 |
| [系统调用](linux/syscalls.md) | Linux 系统调用优化 |

### [Windows 平台](windows/)

| 主题 | 说明 |
|------|------|
| [安装与部署](windows/installation.md) | MSI/EXE 安装程序 |
| [服务集成](windows/service.md) | Windows 服务支持 |
| [注册表集成](windows/registry.md) | Java Preferences API |
| [性能调优](windows/performance.md) | Windows 特定优化 |

### [macOS 平台](macos/)

| 主题 | 说明 |
|------|------|
| [Apple Silicon](macos/apple-silicon.md) | M1/M2/M3/M4 原生支持 |
| [Metal 渲染](macos/metal.md) | Metal 渲染管道 |
| [公证要求](macos/notarization.md) | macOS 应用签名 |
| [性能调优](macos/performance.md) | macOS 特定优化 |

### [容器环境](containers/)

| 主题 | 说明 |
|------|------|
| [资源感知](containers/resource-awareness.md) | CPU/内存限制检测 |
| [Docker 优化](containers/docker.md) | Docker 最佳实践 |
| [Kubernetes](containers/kubernetes.md) | K8s 部署优化 |
| [镜像优化](containers/images.md) | 容器镜像最佳实践 |

---

## 10. 平台对比

### 性能特征

| 平台 | 启动性能 | 稳态吞吐量 | 内存效率 | 备注 |
|------|----------|-----------|----------|------|
| **Linux x64** | 基准 | 基准 | 基准 | 最佳整体性能，最完善的优化 |
| **Linux aarch64** | +5% | +5~10% | +5% | Graviton/Ampere 云实例优势 |
| **Windows x64** | +5% | -3% | +2% | 文件系统和进程创建开销 |
| **macOS Intel** | +3% | -2% | +1% | Metal 渲染管道开销 |
| **macOS Apple Silicon** | +10% | +5~15% | +15% | 统一内存架构 + 高能效比 |
| **容器 (Linux)** | +2% | 基准 | -5% | cgroup 隔离开销，可通过 AOT 优化 |

### I/O 子系统对比

| 平台 | 事件通知机制 | 异步文件 I/O | 网络 I/O |
|------|-------------|-------------|---------|
| **Linux** | epoll | io_uring (第三方) / AIO | epoll |
| **Windows** | IOCP | IOCP | IOCP |
| **macOS** | kqueue | kqueue | kqueue |

---

## 11. 常见问题

### Linux

| 问题 | 影响版本 | 解决方案 |
|------|---------|----------|
| cgroup v2 内存检测错误 | JDK 11-17 | 升级到 JDK 21+，或手动指定 -Xmx |
| 容器 CPU 检测不准确 | JDK 10-17 | 使用 `-XX:ActiveProcessorCount=N` 手动覆盖 |
| 大页内存配置复杂 | 所有版本 | 使用 `-XX:+UseTransparentHugePages` |
| 32 位应用无法运行 | JDK 25+ | 使用 Zero 端口或升级到 64 位 |

### Windows

| 问题 | 影响版本 | 解决方案 |
|------|---------|----------|
| 控制台编码乱码 | 所有版本 | `-Dfile.encoding=UTF-8 -Dconsole.encoding=UTF-8` |
| 路径长度超过 260 字符 | 所有版本 | 启用长路径支持 (LongPathsEnabled 注册表项) |
| 32 位支持移除 | JDK 24+ | 迁移到 64 位 JDK，重新编译 JNI 库 |
| 服务集成复杂 | 所有版本 | 使用 WinSW 或 NSSM 服务包装器 |

### macOS

| 问题 | 影响版本 | 解决方案 |
|------|---------|----------|
| Metal 渲染内存泄漏 | JDK 17.0.0-17.0.10 | 升级到 JDK 17.0.11+ |
| 公证失败 | JDK 14+ | 使用 notarytool 重新提交，检查签名证书 |
| Apple Silicon 本地库不兼容 | JDK 17+ | 重新编译 JNI 库为 arm64 或创建通用二进制 |
| Rosetta 2 性能损失 | JDK 17+ | 使用 AArch64 原生 JDK 构建 |

### 容器

| 问题 | 影响版本 | 解决方案 |
|------|---------|----------|
| OOM Killer 终止容器 | 所有版本 | `-XX:MaxRAMPercentage=70.0`，预留原生内存 |
| CPU 配额导致线程过多 | JDK 10-17 | `-XX:ActiveProcessorCount=N` |
| cgroup v2 环境不识别 | JDK 10-17 | 升级到 JDK 21+ |
| 容器启动慢 | 所有版本 | CDS/AppCDS (JDK 17+)，AOT 缓存 (JDK 26+) |

---

## 12. 最佳实践

### Linux 生产部署

```bash
# JVM 参数推荐
-XX:+UseContainerSupport
-XX:MaxRAMPercentage=75.0
-XX:InitialRAMPercentage=50.0
-XX:ActiveProcessorCount=4

# GC 选择
-XX:+UseZGC                      # 低延迟场景
-XX:+UseG1GC                     # 通用场景 (默认)
-XX:+UseShenandoahGC              # Red Hat 生态

# 大页内存
-XX:+UseLargePages
-XX:+UseTransparentHugePages
```

### Windows 生产部署

```bash
# 内存配置
-Xms2g -Xmx2g
-XX:+UseLargePages                # 需要"锁定内存中的页"权限
-XX:MaxMetaspaceSize=512m

# 编码配置
-Dfile.encoding=UTF-8
-Dconsole.encoding=UTF-8

# GC 选择
-XX:+UseZGC -XX:MaxGCPauseMillis=10
```

### macOS 开发环境

```bash
# Apple Silicon 优化
-XX:+UseZGC
-Dsun.java2d.metal=true           # JDK 19+ 已默认启用
-Xms1g -Xmx2g
```

### 容器部署

```yaml
# Kubernetes 配置示例
resources:
  requests:
    memory: "512Mi"
    cpu: "250m"
  limits:
    memory: "1Gi"
    cpu: "500m"

env:
- name: JAVA_TOOL_OPTIONS
  value: >
    -XX:+UseContainerSupport
    -XX:MaxRAMPercentage=75.0
    -XX:ActiveProcessorCount=2
    -XX:+UseZGC
    -XX:+UseCompactObjectHeaders
```

---

## 13. 相关链接

- [按版本浏览](/by-version/)
- [核心主题](/by-topic/core/)
- [性能优化](/by-topic/core/performance/)
- [GC 调优](/by-topic/core/gc/)
- [容器部署指南](containers/)
- [JEP 391: macOS/AArch64 Port](https://openjdk.org/jeps/391)
- [JEP 382: New macOS Rendering Pipeline](https://openjdk.org/jeps/382)
- [JEP 307: Container Awareness](https://openjdk.org/jeps/307)
- [JEP 392: Packaging Tool](https://openjdk.org/jeps/392)
- [JEP 503: Remove the 32-bit x86 Port](https://openjdk.org/jeps/503)
- [OpenJDK Supported Build Platforms](https://wiki.openjdk.org/display/Build/Supported+Build+Platforms)
