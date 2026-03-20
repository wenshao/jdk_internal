# macOS 平台

macOS 是 Apple 设备开发的重要平台，支持 Intel 和 Apple Silicon 架构。

---

## 概述

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
JDK 17 ──── Apple Silicon 正式支持 (JEP 358)
          │   Metal 渲染管道正式版 (JEP 382)
          │
JDK 21 ──── Metal 渲染优化
          │
JDK 26 ──── Apple Silicon 性能优化
```

---

## Apple Silicon 支持

### 架构对比

| 特性 | Intel Mac | Apple Silicon |
|------|-----------|---------------|
| **架构** | x86_64 | aarch64 |
| **JDK 支持** | JDK 8+ | JDK 17+ |
| **性能** | 基准 | +20-40% |
| **能效** | 基准 | +50-100% |
| **Rosetta 2** | 不适用 | 可用 (兼容模式) |

### 原生 vs Rosetta

**原生运行 (推荐)**:
```bash
# 检查架构
uname -m
# arm64 = Apple Silicon 原生
# x86_64 = Intel 或 Rosetta

# 检查 JDK 架构
java -version
# 应显示 "AArch64" 或 "aarch64"
```

**Rosetta 兼容模式**:
```bash
# 使用 Rosetta 运行 Intel JDK
arch -x86_64 java -jar app.jar

# 不推荐：性能损失 20-40%
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

# 或创建通用二进制
lipo -create -output libuniversal.dylib \
     libx86_64.dylib libarm64.dylib
```

**常见问题**:
- 本地库需要重新编译为 arm64
- 某些依赖可能需要更新
- 测试所有 JNI 调用

---

## Metal 渲染管道

### 概述

Metal 是 Apple 的低开销图形 API，替代 OpenGL。

**演进时间线**:
```
JDK 14 ──── Metal 渲染管道孵化
          │
JDK 17 ──── Metal 正式版 (JEP 382)
          │   替代 OpenGL
          │
JDK 21 ──── Metal 性能优化
          │   内存泄漏修复
          │
JDK 26 ──── Metal 增强
```

### 配置选项

**启用 Metal (默认)**:
```bash
# 默认启用
-Dsun.java2d.metal=true

# 回退到 OpenGL (不推荐)
-Dsun.java2d.metal=false
-Dsun.java2d.opengl=true
```

**调试选项**:
```bash
# Metal 调试
-Dsun.java2d.metal.trace=true

# 渲染调试
-Dsun.java2d.trace=log
```

### 性能对比

| 场景 | OpenGL | Metal | 改进 |
|------|--------|-------|------|
| **2D 渲染** | 基准 | +15% | 明显 |
| **图像处理** | 基准 | +25% | 显著 |
| **动画** | 基准 | +20% | 明显 |
| **内存使用** | 基准 | -10% | 改善 |

### 常见问题

**问题 1: Metal 内存泄漏**
```bash
# 症状: 原生内存持续增长
# 影响版本: JDK 17.0.0 - 17.0.10

# 解决方案
# 1. 升级到 JDK 17.0.11+
# 2. 或临时使用 OpenGL
-Dsun.java2d.metal=false
```

**问题 2: 渲染异常**
```bash
# 症状: 图形显示不正确

# 解决方案
# 1. 更新 macOS
# 2. 更新 JDK
# 3. 检查 Metal 支持
system_profiler SPDisplaysDataType
```

---

## 公证要求

### 概述

macOS 10.15+ 要求应用经过公证 (Notarization) 才能运行。

**公证流程**:
```
1. 开发者证书签名
   ↓
2. 提交 Apple 公证
   ↓
3. 公证通过
   ↓
4. 应用可正常运行
```

### jpackage 签名

**代码签名**:
```bash
# 签名应用
codesign --force --deep --sign "Developer ID Application: Your Name (TEAMID)" MyApp.app

# 验证签名
codesign --verify --deep --strict --verbose=2 MyApp.app

# 检查签名信息
codesign --display --verbose=4 MyApp.app
```

**公证提交**:
```bash
# 创建 ZIP
ditto -c -k --keepParent MyApp.app MyApp.zip

# 提交公证
xcrun notarytool submit MyApp.zip \
    --apple-id "your@email.com" \
    --team-id "TEAMID" \
    --password "@keychain:AC_PASSWORD" \
    --wait

# 检查状态
xcrun notarytool history \
    --apple-id "your@email.com" \
    --team-id "TEAMID" \
    --password "@keychain:AC_PASSWORD"

# Staple 公证结果
xcrun stapler staple MyApp.app
```

### 运行未签名应用

**临时绕过**:
```bash
# 移除隔离属性
xattr -cr MyApp.app

# 或在系统偏好设置中允许
# 系统偏好设置 → 安全性与隐私 → 通用 → 仍要打开
```

---

## 安装与部署

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
```

### PKG 安装

```bash
# 下载 PKG
curl -O https://download.java.net/java/GA/jdk21/.../openjdk-21_macos-x64_bin.tar.gz

# 安装
sudo installer -pkg openjdk-21.pkg -target /

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
         --mac-signing-key-user-name "Developer ID Application: Your Name (TEAMID)"
```

**创建 PKG**:
```bash
jpackage --name MyApp \
         --input input \
         --main-jar app.jar \
         --main-class com.example.Main \
         --type pkg \
         --app-version 1.0.0 \
         --vendor "My Company" \
         --mac-package-name "My Application" \
         --mac-package-identifier "com.example.myapp" \
         --mac-sign \
         --mac-signing-key-user-name "Developer ID Application: Your Name (TEAMID)"
```

---

## 性能调优

### Apple Silicon 优化

**内存优化**:
```bash
# Apple Silicon 统一内存架构
# 无需特别配置，自动优化

# 大页内存
-XX:+UseLargePages
```

**CPU 优化**:
```bash
# 性能核心 vs 能效核心
# macOS 自动调度，无需配置

# 线程数建议
# 使用默认值，macOS 会自动优化
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
# CDS
java -Xshare:dump -XX:SharedArchiveFile=app.jsa -jar app.jar
java -Xshare:on -XX:SharedArchiveFile=app.jsa -jar app.jar
```

---

## 常见问题

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
```

### 问题 2: 路径问题

**症状**:
- 文件路径包含空格或特殊字符
- 路径解析错误

**解决方案**:
```java
// 使用 Path API
Path path = Path.of("/Users/user/My Documents/file.txt");

// 避免硬编码路径
String home = System.getProperty("user.home");
Path configPath = Path.of(home, ".myapp", "config.properties");
```

### 问题 3: 权限问题

**症状**:
- 全磁盘访问权限缺失
- 文件操作被拒绝

**解决方案**:
```bash
# 系统偏好设置 → 安全性与隐私 → 隐私 → 全磁盘访问权限
# 添加 java 或终端应用
```

---

## 监控和诊断

### 系统监控

**活动监视器**:
```
应用程序 → 实用工具 → 活动监视器
```

**终端监控**:
```bash
# CPU 使用
top -pid <pid>

# 内存使用
ps -p <pid> -o rss,vsz

# 线程状态
ps -M -p <pid>
```

### JVM 监控

**JFR 配置**:
```bash
# 启动 JFR
-XX:StartFlightRecording=duration=60s,filename=recording.jfr

# 使用 jcmd
jcmd <pid> JFR.start duration=60s filename=recording.jfr
```

---

## 最佳实践

### 开发环境

```bash
# 推荐配置
-Xms1g -Xmx2g
-XX:+UseZGC
-Dsun.java2d.metal=true
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

### 应用打包

- [ ] 使用 jpackage 创建安装包
- [ ] 签名应用
- [ ] 提交公证
- [ ] 测试安装和运行
- [ ] 测试卸载

---

## 相关链接

- [Apple Silicon 迁移指南](https://developer.apple.com/documentation/apple_silicon)
- [Metal 文档](https://developer.apple.com/metal/)
- [公证指南](https://developer.apple.com/documentation/security/notarizing_macos_software_before_distribution)
- [JDK 版本文档](/by-version/)