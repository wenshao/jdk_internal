# macOS 平台

macOS 是 Apple 设备开发的重要平台，支持 Intel 和 Apple Silicon 架构。

---
## 目录

1. [概述](#1-概述)
2. [Apple Silicon 支持](#2-apple-silicon-支持)
3. [Metal 渲染管道](#3-metal-渲染管道)
4. [Aqua 外观](#4-aqua-外观)
5. [代码签名与公证](#5-代码签名与公证)
6. [安装与部署](#6-安装与部署)
7. [文件系统注意事项](#7-文件系统注意事项)
8. [内存与 GC](#8-内存与-gc)
9. [性能调优](#9-性能调优)
10. [常见问题](#10-常见问题)
11. [监控和诊断](#11-监控和诊断)
12. [最佳实践](#12-最佳实践)
13. [相关链接](#13-相关链接)

---


## 1. 概述

### 支持的架构

| 架构 | 状态 | 说明 |
|------|------|------|
| **x64 (Intel)** | ✅ 支持 | 传统 Mac |
| **aarch64 (Apple Silicon)** | ✅ 主要平台 | M1/M2/M3/M4 |

### 支持的版本

| macOS 版本 | 最低支持 | 推荐 |
|------------|----------|------|
| **macOS 12 (Monterey)** | ✅ | - |
| **macOS 13 (Ventura)** | ✅ | ✅ |
| **macOS 14 (Sonoma)** | ✅ | ✅ |
| **macOS 15 (Sequoia)** | ✅ | ✅ |

### 架构演进时间线

```
JDK 8  ──── 仅支持 Intel x64
          │
JDK 16 ──── Apple Silicon (M1) 预览支持
          │
JDK 17 ──── Apple Silicon 正式支持 (JEP 391)
          │   Metal 渲染管道引入 (JEP 382, 非默认)
          │
JDK 19 ──── Metal 成为默认渲染管道
          │
JDK 21 ──── Metal 渲染优化
          │
JDK 25 ──── JEP 519 Compact Object Headers (实验性)
```

---

## 2. Apple Silicon 支持

### JEP 391: macOS/AArch64 Port

JEP 391 将 JDK 移植到 Apple Silicon（AArch64 架构），从 JDK 17 起正式支持。该移植涉及 HotSpot JIT 编译器、解释器和所有平台相关的本地代码。

### 架构对比

| 特性 | Intel Mac | Apple Silicon |
|------|-----------|---------------|
| **架构** | x86_64 | aarch64 |
| **JDK 支持** | JDK 8+ | JDK 17+ |
| **性能** | 基准 | +20-40% |
| **能效** | 基准 | +50-100% |
| **Rosetta 2** | 不适用 | 可用 (兼容模式) |
| **统一内存 (Unified Memory)** | 不适用 | CPU/GPU 共享内存 |

### 原生 vs Rosetta 2 性能

**原生运行 (推荐)**:
```bash
# 检查架构
uname -m
# arm64 = Apple Silicon 原生
# x86_64 = Intel 或 Rosetta

# 检查 JDK 架构
java -version
# 应显示 "AArch64" 或 "aarch64"

# 验证进程是否原生运行
sysctl sysctl.proc_translated
# 0 = 原生, 1 = Rosetta 转译
```

**Rosetta 2 兼容模式**:
```bash
# 使用 Rosetta 运行 Intel JDK
arch -x86_64 java -jar app.jar

# 不推荐：性能损失 20-40%
```

**Rosetta 2 vs 原生性能对比**:

| 场景 | Rosetta 2 | 原生 AArch64 | 差距 |
|------|-----------|-------------|------|
| **JIT 编译吞吐** | 基准 | +30-40% | 显著 |
| **启动时间 (Startup Time)** | 基准 | +15-25% | 明显 |
| **内存占用 (Memory Footprint)** | 较高 | -10-15% | 改善 |
| **GC 暂停 (GC Pause)** | 基准 | +10-20% | 改善 |
| **JNI 调用** | 需要 x86 库 | 需要 arm64 库 | 不兼容 |

> **注意**: Rosetta 2 不支持混合架构 (mixed-architecture)——x86_64 进程只能加载 x86_64 动态库，不能加载 arm64 库，反之亦然。

### W^X 内存策略

Apple Silicon 强制执行 W^X（Write XOR Execute）内存保护策略——同一内存页不能同时拥有写权限和执行权限。这直接影响 JIT 编译器的代码生成。

**HotSpot 的适配**:
```
传统 (Intel):
    mmap(RWX) → 写入机器码 → 直接执行
    同一页同时可写可执行

Apple Silicon (W^X):
    mmap(RW) → 写入机器码 → mprotect(RX) → 执行
    或使用 pthread_jit_write_protect_np() 切换
    同一时刻只有写或执行权限
```

```bash
# JIT 在 Apple Silicon 上使用双映射 (dual mapping) 或 W^X 切换
# HotSpot 通过 pthread_jit_write_protect_np() 实现
# 对应用透明，但影响 JIT 编译性能 (~5% 开销)

# 验证 JIT 正常工作
-XX:+PrintCompilation
-XX:+TraceNMethodInstalls
```

### 本地库兼容性

**JNI 库迁移**:
```bash
# 检查库架构
file libnative.dylib
# 应显示: Mach-O 64-bit dynamically linked shared library arm64

# 重新编译本地库
./configure --host=aarch64-apple-darwin
make clean
make

# 或创建通用二进制 (Universal Binary)
lipo -create -output libuniversal.dylib \
     libx86_64.dylib libarm64.dylib

# 检查通用二进制包含的架构
lipo -info libuniversal.dylib
# Architectures in the fat file: libuniversal.dylib are: x86_64 arm64
```

**常见问题**:
- 本地库需要重新编译为 arm64
- 某些依赖可能需要更新
- 测试所有 JNI 调用
- 通用二进制 (Universal Binary) 可以同时包含 x86_64 和 arm64

---

## 3. Metal 渲染管道

### JEP 382: Metal Rendering Pipeline

Metal 是 Apple 的低开销图形 API，JEP 382 用 Metal 替代了已废弃的 OpenGL 作为 Java2D 渲染管道。Apple 从 macOS 10.14 开始废弃 OpenGL，因此这是长期方向。

**演进时间线**:
```
macOS 10.14 ──── Apple 废弃 OpenGL
             │
JDK 17 ──── Metal 渲染管道引入 (JEP 382, 非默认)
          │
JDK 19 ──── Metal 成为默认渲染管道，替代 OpenGL
          │
JDK 21 ──── Metal 性能优化
          │   内存泄漏修复
          │
JDK 25 ──── Metal 增强
```

### 配置选项

**启用 Metal (默认)**:
```bash
# 默认启用
-Dsun.java2d.metal=true

# 回退到 OpenGL (不推荐，仅用于兼容排查)
-Dsun.java2d.metal=false
-Dsun.java2d.opengl=true
```

**调试选项**: `-Dsun.java2d.metal.trace=true` 启用 Metal 追踪, `-Dsun.java2d.trace=log` 启用渲染追踪日志。

### 性能对比

Metal 相比 OpenGL: 2D 渲染 +15%, 图像处理 +25%, 动画 +20%, 内存使用 -10%, GPU 命令提交延迟 -30%。

### 常见问题

**问题 1: Metal 内存泄漏 (Native Memory Leak)**
```bash
# 症状: 原生内存持续增长
# 影响版本: JDK 17.0.0 - 17.0.10

# 解决方案
# 1. 升级到 JDK 17.0.11+
# 2. 或临时使用 OpenGL
-Dsun.java2d.metal=false
```

**问题 2: 渲染异常 (Rendering Artifacts)**
```bash
# 症状: 图形显示不正确

# 解决方案
# 1. 更新 macOS
# 2. 更新 JDK
# 3. 检查 Metal 支持
system_profiler SPDisplaysDataType
# 确认 "Metal Support" 显示 "Metal 3" 或 "Metal"
```

---

## 4. Aqua 外观

### macOS 原生外观 (Aqua Look and Feel)

macOS 上的 Swing 应用默认使用 Aqua L&F，提供原生 macOS 风格的控件和行为。

**自动启用**:
```java
// macOS 上默认使用 Aqua L&F
UIManager.getSystemLookAndFeelClassName();
// 返回 "com.apple.laf.AquaLookAndFeel"

// 显式设置 (通常不需要)
UIManager.setLookAndFeel("com.apple.laf.AquaLookAndFeel");
```

### macOS 特定属性

```java
// 使用 macOS 原生菜单栏 (屏幕顶部)
System.setProperty("apple.laf.useScreenMenuBar", "true");

// 应用名称 (显示在菜单栏和 Dock)
System.setProperty("apple.awt.application.name", "My App");

// Dock 图标
// 使用 java.awt.Taskbar API (JDK 9+)
Taskbar taskbar = Taskbar.getTaskbar();
taskbar.setIconImage(myIcon);

// 暗色模式 (Dark Mode) 支持
// JDK 17+ 自动跟随系统深色模式
// 检查当前主题
defaults read -g AppleInterfaceStyle
// 返回 "Dark" 或命令失败 (表示浅色模式)
```

### 已知限制

- Aqua L&F 是 macOS 专有的，不可在其他平台使用
- 部分 Swing 组件的外观与原生 AppKit 控件略有差异
- 暗色模式下某些自定义颜色可能需要手动适配
- JavaFX 有独立的 macOS 样式系统，不使用 Aqua L&F

---

## 5. 代码签名与公证

### 概述

macOS 10.15+ 要求应用经过代码签名 (Code Signing) 和公证 (Notarization) 才能通过 Gatekeeper 正常运行。

**安全链条**:
```
开发者证书 (Developer ID Certificate)
   ↓
代码签名 (Code Signing) ← codesign 工具
   ↓
公证提交 (Notarization) ← xcrun notarytool
   ↓
Staple 公证票据 (Staple Ticket)
   ↓
Gatekeeper 验证 → 允许运行
```

### Gatekeeper 行为

| 场景 | Gatekeeper 行为 |
|------|-----------------|
| **已签名 + 已公证** | 直接运行 |
| **已签名 + 未公证** | 警告弹窗 (可手动允许) |
| **未签名** | 阻止运行 (需手动绕过) |
| **签名已损坏** | 阻止运行 (无法绕过) |

### Apple Developer ID 证书

**证书类型**:

| 证书类型 | 用途 | 需要 |
|----------|------|------|
| **Developer ID Application** | 签名 .app 包 | 分发 macOS 应用 |
| **Developer ID Installer** | 签名 .pkg 安装包 | 分发安装程序 |
| **Apple Development** | 开发阶段签名 | 开发测试 |

```bash
# 查看可用签名身份
security find-identity -v -p codesigning

# 典型输出:
# 1) ABC123... "Developer ID Application: Your Company (TEAMID)"
# 2) DEF456... "Developer ID Installer: Your Company (TEAMID)"
```

### 代码签名

```bash
# 签名应用 (.app)
codesign --force --deep --sign "Developer ID Application: Your Name (TEAMID)" \
    --options runtime \
    --entitlements entitlements.plist \
    MyApp.app

# --options runtime: 启用 Hardened Runtime (公证必需)
# --entitlements: 指定权限声明

# 验证签名
codesign --verify --deep --strict --verbose=2 MyApp.app

# 检查签名信息
codesign --display --verbose=4 MyApp.app
```

**Hardened Runtime 权限 (Entitlements)**:

JVM 应用需要以下 entitlements (在 `.plist` 文件中声明):
- `com.apple.security.cs.allow-jit` — 允许 JIT 编译
- `com.apple.security.cs.allow-unsigned-executable-memory` — 允许未签名可执行内存
- `com.apple.security.cs.allow-dyld-environment-variables` — 允许 DYLD 环境变量

### 公证提交

```bash
# 创建 ZIP (用于 .app)
ditto -c -k --keepParent MyApp.app MyApp.zip

# 提交公证
xcrun notarytool submit MyApp.zip \
    --apple-id "your@email.com" \
    --team-id "TEAMID" \
    --password "@keychain:AC_PASSWORD" \
    --wait

# 检查公证日志 (排查失败原因)
xcrun notarytool log <submission-id> \
    --apple-id "your@email.com" \
    --team-id "TEAMID" \
    --password "@keychain:AC_PASSWORD"

# Staple 公证结果 (离线验证)
xcrun stapler staple MyApp.app
# 对于 .dmg 和 .pkg 同样适用
xcrun stapler staple MyApp.dmg
```

### 运行未签名应用

**临时绕过 (仅开发环境)**:
```bash
# 移除隔离属性 (quarantine flag)
xattr -cr MyApp.app

# 或在系统偏好设置中允许
# 系统偏好设置 → 安全性与隐私 → 通用 → 仍要打开

# 完全禁用 Gatekeeper (不推荐)
sudo spctl --master-disable
```

---

## 6. 安装与部署

### 安装方式

| 方式 | 说明 | 适用场景 |
|------|------|----------|
| **PKG 安装包** | 系统级安装 | 企业部署 |
| **DMG 镜像** | 用户级安装 | 开发环境 |
| **TAR.GZ 压缩包** | 免安装 | 便携部署 |
| **Homebrew** | 包管理器 | 开发环境 |

### Homebrew 安装

```bash
# 安装 OpenJDK
brew install openjdk@21

# 创建符号链接
sudo ln -sfn /opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk \
     /Library/Java/JavaVirtualMachines/openjdk-21.jdk

# 验证安装
java -version

# 管理多版本
brew install openjdk@17 openjdk@21 openjdk@25
# 使用 jenv 或手动切换 JAVA_HOME
```

### PKG 安装

```bash
# 下载 PKG
curl -O https://download.java.net/java/GA/jdk21/.../openjdk-21_macos-x64_bin.tar.gz

# 安装
sudo installer -pkg openjdk-21.pkg -target /

# JDK 安装位置
ls /Library/Java/JavaVirtualMachines/

# 使用 java_home 工具查找 JDK
/usr/libexec/java_home -V          # 列出所有版本
/usr/libexec/java_home -v 21       # 查找 JDK 21

# 验证
java -version
```

### jpackage 打包

**创建 DMG**:
```bash
jpackage --name MyApp \
         --input input \
         --main-jar app.jar \
         --main-class com.example.Main \
         --type dmg \
         --app-version 1.0.0 \
         --vendor "My Company" \
         --mac-package-name "My Application" \
         --mac-package-identifier "com.example.myapp" \
         --mac-sign \
         --mac-signing-key-user-name "Developer ID Application: Your Name (TEAMID)" \
         --mac-app-category "public.app-category.developer-tools" \
         --mac-entitlements entitlements.plist
```

**jpackage + jlink 瘦身运行时**:
```bash
# 先用 jlink 创建自定义 JRE (Custom Runtime Image)
jlink --module-path $JAVA_HOME/jmods \
      --add-modules java.base,java.sql,java.logging \
      --output custom-jre \
      --strip-debug \
      --compress zip-6 \
      --no-header-files \
      --no-man-pages

# 再用 jpackage 打包 (使用自定义 JRE)
jpackage --name MyApp \
         --input input \
         --main-jar app.jar \
         --main-class com.example.Main \
         --type dmg \
         --runtime-image custom-jre
# 最终 DMG 可从 ~200MB 缩减到 ~50MB
```

---

## 7. 文件系统注意事项

### APFS 与大小写

macOS 默认使用 APFS (Apple File System)，有一个常见陷阱：**大小写不敏感但保留大小写** (Case-Insensitive, Case-Preserving)。

```bash
# 检查文件系统类型
diskutil info / | grep "File System"
# APFS (Case-insensitive)  ← 默认
# APFS (Case-sensitive)    ← 可选

# 陷阱示例
touch MyClass.java
touch myclass.java    # 在默认 APFS 上，这会覆盖 MyClass.java!
```

**对 Java 项目的影响**:

| 场景 | 问题 | 说明 |
|------|------|------|
| **类名冲突** | `MyClass.java` 和 `myclass.java` | macOS 上视为同一文件，Linux 上为不同文件 |
| **Git 仓库** | 大小写重命名不被检测 | 需要 `git mv` 而非直接重命名 |
| **资源文件** | `Config.properties` vs `config.properties` | macOS 能找到，Linux 部署失败 |
| **JAR 中的类** | 大小写冲突的类文件 | 在 CI/CD (Linux) 中构建失败 |

**最佳实践**:
```bash
# Git 配置: 感知大小写变化
git config core.ignorecase false

# 在 macOS 上创建大小写敏感的 APFS 卷 (用于开发)
diskutil apfs addVolume disk1 "Case-sensitive APFS" DevVolume

# 检查项目中的大小写冲突
find . -type f | sort -f | uniq -di
```

### 路径长度与特殊字符

```java
// macOS 路径限制: 1024 字符 (PATH_MAX)
// 比 Linux (4096) 短

// macOS 文件名中的特殊字符
// 冒号 (:) 在 Finder 中显示为斜杠 (/)，应避免使用
Path safe = Path.of(home, ".myapp", "config.properties");  // 好
Path risky = Path.of(home, "My:App", "config.properties"); // 避免
```

### 扩展属性 (Extended Attributes)

从网络下载的 JAR/dylib 文件会带有 `com.apple.quarantine` 属性，可能导致运行时警告或阻止执行。使用 `xattr -d com.apple.quarantine <file>` 清除，或 `xattr -cr <dir>` 批量清除。

---

## 8. 内存与 GC

### macOS 内存模型

macOS 使用 Mach 虚拟内存子系统，与 Linux 的 `mmap`/`madvise` 有一些关键差异。

**物理内存查询**: `sysctl hw.memsize` 获取物理内存字节数, `vm_stat` 查看内存使用概况 (free/active/inactive/wired 页面)。

### ZGC 与 mach_vm_remap

ZGC 在 macOS 上使用 `mach_vm_remap` 实现多重映射 (Multi-Mapping)，而非 Linux 上的 `mmap` + `MAP_FIXED`。

```
Linux ZGC:
    mmap(MAP_FIXED) → 将多个虚拟地址映射到同一物理页

macOS ZGC:
    mach_vm_remap() → Mach VM API 实现相同效果
    无需 MAP_FIXED，更安全
```

**macOS 上的 ZGC 配置**:
```bash
# 启用 ZGC
-XX:+UseZGC

# macOS 不支持大页 (Large Pages / Huge Pages)
# -XX:+UseLargePages 在 macOS 上无效

# ZGC 堆大小 (macOS 开发环境)
-Xmx4g -Xms4g -XX:+UseZGC

# macOS 上 ZGC 的 SoftMaxHeapSize
-XX:SoftMaxHeapSize=2g    # 尽量控制在 2GB
```

### macOS 内存压缩 (Memory Compression)

macOS 会对不活跃内存进行透明压缩 (`sysctl vm.compressor_mode`)。大堆的不活跃区域可能被压缩，GC 遍历时触发解压缩会增加暂停时间。建议保持堆大小在物理内存的 50-70% 以内。

---

## 9. 性能调优

### Apple Silicon 优化

**CPU 核心调度**:
```bash
# Apple Silicon: Performance (P) 核心 + Efficiency (E) 核心
# macOS 自动调度，JVM 线程默认由系统分配

# 查看 CPU 拓扑
sysctl -a | grep cpu
# hw.perflevel0.logicalcpu: 8  (P 核心)
# hw.perflevel1.logicalcpu: 4  (E 核心)

# JVM 报告的处理器数 = P + E 总数
# Runtime.getRuntime().availableProcessors() → 12 (M2 Pro 示例)
```

**内存优化**:
```bash
# Apple Silicon 统一内存架构 (Unified Memory Architecture)
# CPU 和 GPU 共享同一内存池
# 无需特别配置，自动优化

# 注意: macOS 不支持 Linux 大页 (Huge Pages)
# -XX:+UseLargePages 在 macOS 上无效
# Apple Silicon 使用 16KB 页面 (vs Intel/Linux 4KB)
```

### 通用优化

**内存配置**:
```bash
# 基本配置
-Xms2g -Xmx2g

# GC 选择
-XX:+UseZGC -XX:MaxGCPauseMillis=10  # 低延迟
-XX:+UseG1GC                          # 通用
```

**启动优化**:
```bash
# CDS (Class Data Sharing)
java -Xshare:dump -XX:SharedArchiveFile=app.jsa -jar app.jar
java -Xshare:on -XX:SharedArchiveFile=app.jsa -jar app.jar

# AOT 缓存 (JDK 25+, JEP 514)
java -XX:AOTCacheOutput=app.aot -jar app.jar    # 训练运行
java -XX:AOTCache=app.aot -jar app.jar           # 使用缓存
```

---

## 10. 常见问题

### 问题 1: 沙箱文件访问

**症状**:
- 沙箱应用无法访问某些文件
- `AccessDeniedException`

**解决方案**:
```bash
# 请求沙箱权限
# 或使用安全书签访问

# 禁用沙箱 (开发环境)
# 在 entitlements 文件中设置

# 系统偏好设置 → 安全性与隐私 → 隐私 → 全磁盘访问权限
# 添加 java 或终端应用
```

### 问题 2: 路径问题 (Path Issues)

**症状**:
- 文件路径包含空格或特殊字符
- 路径解析错误
- macOS 与 Linux 大小写行为不一致

**解决方案**:
```java
// 使用 Path API
Path path = Path.of("/Users/user/My Documents/file.txt");

// 避免硬编码路径
String home = System.getProperty("user.home");
Path configPath = Path.of(home, ".myapp", "config.properties");

// 跨平台路径: 始终使用一致的大小写
// macOS 上能找到的文件, Linux 上可能找不到
```

### 问题 3: JDK 版本切换

**症状**:
- 多个 JDK 版本共存时 `JAVA_HOME` 混乱
- IDE 使用了错误的 JDK

**解决方案**:
```bash
# 使用 /usr/libexec/java_home
export JAVA_HOME=$(/usr/libexec/java_home -v 21)

# 添加到 shell 配置
echo 'export JAVA_HOME=$(/usr/libexec/java_home -v 21)' >> ~/.zshrc

# 列出所有已安装的 JDK
/usr/libexec/java_home -V

# Homebrew 安装的 JDK 位置
ls /opt/homebrew/opt/openjdk*/
```

### 问题 4: macOS Sequoia 安全限制

macOS 15 (Sequoia) 加强安全策略，未签名的 JNI 库可能无法加载。使用 `codesign --force --sign - libnative.dylib` 添加 ad-hoc 签名，或 `xattr -d com.apple.quarantine libnative.dylib` 移除隔离属性。

---

## 11. 监控和诊断

### 系统监控

**活动监视器 (Activity Monitor)**:
```
应用程序 → 实用工具 → 活动监视器
```

**终端监控**:
```bash
# CPU 使用
top -pid <pid>

# 内存使用 (包括压缩内存)
ps -p <pid> -o rss,vsz
footprint <pid>    # macOS 专有工具，显示详细内存分类

# 线程状态
ps -M -p <pid>

# 系统级内存统计
vm_stat

# I/O 统计
iostat -d 1
```

### JVM 监控

**JFR 配置**:
```bash
# 启动 JFR
-XX:StartFlightRecording=duration=60s,filename=recording.jfr

# 使用 jcmd
jcmd <pid> JFR.start duration=60s filename=recording.jfr

# macOS 专有事件
# JFR 会自动收集 macOS 特定的系统信息
```

---

## 12. 最佳实践

### 开发环境

```bash
# 推荐配置
-Xms1g -Xmx2g
-XX:+UseZGC
-Dsun.java2d.metal=true

# Shell 配置 (~/.zshrc)
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
export PATH="$JAVA_HOME/bin:$PATH"
```

### 生产部署

```bash
# 推荐配置
-Xms2g -Xmx2g
-XX:+UseZGC -XX:MaxGCPauseMillis=10
-XX:MetaspaceSize=256m
-XX:MaxMetaspaceSize=512m
-Dsun.java2d.metal=true
-Xlog:gc*,safepoint:file=gc.log:time,level,tags:filecount=5,filesize=10m
```

### 应用打包清单

- [ ] 使用 jpackage 创建安装包 (.dmg 或 .pkg)
- [ ] 使用 jlink 创建自定义运行时减小体积
- [ ] 配置 Hardened Runtime entitlements
- [ ] 使用 Developer ID 证书签名
- [ ] 提交 Apple 公证 (Notarization)
- [ ] Staple 公证票据
- [ ] 测试 Gatekeeper 验证通过
- [ ] 测试安装和运行
- [ ] 测试卸载
- [ ] 验证 macOS 和 Linux 大小写一致性

---

## 13. 相关链接

- [Apple Silicon 迁移指南](https://developer.apple.com/documentation/apple_silicon)
- [Metal 文档](https://developer.apple.com/metal/)
- [公证指南](https://developer.apple.com/documentation/security/notarizing_macos_software_before_distribution)
- [JDK 版本文档](/by-version/)
