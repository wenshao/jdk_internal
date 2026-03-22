# Windows 平台

Windows 是企业环境中 Java 应用部署的重要平台。

---
## 目录

1. [概述](#1-概述)
2. [安装与部署](#2-安装与部署)
3. [服务集成](#3-服务集成)
4. [注册表与 Preferences API](#4-注册表与-preferences-api)
5. [控制台与字符编码](#5-控制台与字符编码)
6. [Windows 特定优化](#6-windows-特定优化)
7. [DLL 加载与本地库](#7-dll-加载与本地库)
8. [jpackage 打包详解](#8-jpackage-打包详解)
9. [Windows ARM64](#9-windows-arm64)
10. [Windows Server 与容器](#10-windows-server-与容器)
11. [性能调优](#11-性能调优)
12. [常见问题](#12-常见问题)
13. [监控和诊断](#13-监控和诊断)
14. [最佳实践](#14-最佳实践)
15. [相关链接](#15-相关链接)

---


## 1. 概述

### 支持的架构 (Supported Architectures)

| 架构 | 状态 | 说明 |
|------|------|------|
| **x64 (AMD64)** | ✅ 主要平台 | 推荐 (recommended) |
| **x86 (32位)** | ❌ 已移除 | JDK 21 废弃，JDK 24 移除 (JEP 479) |
| **ARM64 (AArch64)** | ✅ 正式支持 | JEP 388 (JDK 16 实验，JDK 21 后成熟) |

### 支持的版本 (Supported Versions)

| Windows 版本 | 最低支持 | 推荐 |
|--------------|----------|------|
| **Windows 10** | 1507 | 22H2 |
| **Windows 11** | 21H2 | 最新 |
| **Windows Server 2016** | ✅ | - |
| **Windows Server 2019** | ✅ | ✅ |
| **Windows Server 2022** | ✅ | ✅ |

### 架构支持时间线

```
JDK 8  ──── x86 (32位) 和 x64 (64位) 支持
          │
JDK 16 ──── Windows AArch64 实验性支持 (JEP 388)
          │  jpackage 正式版 (JEP 392)
          │
JDK 17 ──── 改进安装程序, Windows AArch64 继续成熟
          │
JDK 18 ──── UTF-8 默认编码 (JEP 400)
          │
JDK 21 ──── 废弃 x86 (32位) 端口 (JEP 449)
          │  控制台默认 UTF-8
          │
JDK 24 ──── 移除 x86 (32位) 支持 (JEP 479)
```

---

## 2. 安装与部署

### 安装方式 (Installation Methods)

| 方式 | 说明 | 适用场景 |
|------|------|----------|
| **MSI 安装包** | 系统级安装 (system-level install) | 企业部署 |
| **EXE 安装包** | 用户级安装 (user-level install) | 开发环境 |
| **ZIP 压缩包** | 免安装 (portable) | 便携部署 |
| **jpackage** | 应用打包 (application packaging) | 应用分发 |

### MSI 安装 (MSI Installation)

**静默安装 (silent install)**:
```powershell
# 静默安装
msiexec /i jdk-21_windows-x64_bin.msi /quiet /norestart

# 指定安装目录 (specify install directory)
msiexec /i jdk-21_windows-x64_bin.msi INSTALLDIR="C:\Java\jdk-21" /quiet

# 添加到 PATH (add to PATH)
msiexec /i jdk-21_windows-x64_bin.msi ADDLOCAL="FeatureMain,FeatureEnvironment" /quiet
```

**企业部署 (enterprise deployment)**:
```powershell
# 使用 Group Policy 部署 (GPO deployment)
# 1. 创建 GPO
# 2. 计算机配置 → 管理模板 → 软件 → 软件安装
# 3. 添加 MSI 包

# 或使用 SCCM / Intune
# 1. 创建应用程序
# 2. 添加部署类型
# 3. 分发到目标集合
```

### ZIP 部署 (ZIP Deployment)

```powershell
# 下载并解压 (download and extract)
Expand-Archive -Path openjdk-21_windows-x64_bin.zip -DestinationPath C:\Java

# 设置环境变量 (set environment variables)
[System.Environment]::SetEnvironmentVariable("JAVA_HOME", "C:\Java\jdk-21", "Machine")
[System.Environment]::SetEnvironmentVariable("PATH", "$env:PATH;C:\Java\jdk-21\bin", "Machine")
```

---

## 3. 服务集成

### Windows 服务配置 (Windows Service Configuration)

**使用 sc 命令 (using sc command)**:
```powershell
# 创建服务 (create service)
sc create MyJavaApp binPath= "C:\Java\jdk-21\bin\java.exe -jar C:\app\app.jar" start= auto

# 配置服务 (configure service)
sc config MyJavaApp DisplayName= "My Java Application"
sc description MyJavaApp "Java application service"

# 启动/停止/删除 (start/stop/delete)
sc start MyJavaApp
sc stop MyJavaApp
sc delete MyJavaApp
```

**使用 NSSM (推荐, recommended)**:
```powershell
# 安装服务 (install service)
nssm install MyJavaApp "C:\Java\jdk-21\bin\java.exe" "-jar C:\app\app.jar"

# 配置服务 (configure service)
nssm set MyJavaApp AppDirectory "C:\app"
nssm set MyJavaApp DisplayName "My Java Application"
nssm set MyJavaApp Description "Java application service"
nssm set MyJavaApp Start SERVICE_AUTO_START

# 配置日志 (configure logging)
nssm set MyJavaApp AppStdout "C:\logs\app.log"
nssm set MyJavaApp AppStderr "C:\logs\error.log"

# 启动服务 (start service)
nssm start MyJavaApp
```

**使用 WinSW**: 通过 XML 配置文件定义服务 (id, executable, arguments, log 等)，然后用 `myapp.exe install/start/stop/uninstall` 操作。支持自动重启策略和日志轮转。

---

## 4. 注册表与 Preferences API

### Java Preferences API (注册表访问)

Preferences API 是 Java 标准的键值存储接口，在 Windows 平台上底层实现 (backing store) 使用 Windows 注册表 (Windows Registry)。

```java
import java.util.prefs.Preferences;

public class RegistryExample {
    public static void main(String[] args) throws Exception {
        // 用户首选项 → HKEY_CURRENT_USER
        Preferences userPrefs = Preferences.userNodeForPackage(
            RegistryExample.class);
        userPrefs.put("setting1", "value1");
        userPrefs.putInt("setting2", 42);
        userPrefs.putBoolean("featureEnabled", true);
        userPrefs.putByteArray("data", new byte[]{1, 2, 3});

        // 系统首选项 → HKEY_LOCAL_MACHINE (需要管理员权限)
        Preferences systemPrefs = Preferences.systemNodeForPackage(
            RegistryExample.class);
        systemPrefs.put("globalSetting", "globalValue");

        // 读取值 (read values)
        String value = userPrefs.get("setting1", "default");
        int number = userPrefs.getInt("setting2", 0);

        // 子节点导航 (child node navigation)
        Preferences child = userPrefs.node("database");
        child.put("host", "localhost");

        // 导出/导入 XML, 变更监听 (export/import, change listener)
        userPrefs.exportSubtree(System.out);
        userPrefs.addPreferenceChangeListener(evt ->
            System.out.println(evt.getKey() + " = " + evt.getNewValue()));
        userPrefs.flush();
    }
}
```

**注册表存储位置 (registry location)**:
```
用户首选项 (user preferences):
  HKEY_CURRENT_USER\Software\JavaSoft\Prefs\<package-path>

系统首选项 (system preferences):
  HKEY_LOCAL_MACHINE\Software\JavaSoft\Prefs\<package-path>

注意: 包名中的点 (.) 被替换为斜杠 (/)
例如: com.example.app → /com/example/app
```

### 直接注册表访问 (Direct Registry Access)

```java
// 使用 JNA (Java Native Access) 直接操作注册表
import com.sun.jna.platform.win32.Advapi32Util;
import com.sun.jna.platform.win32.WinReg;

public class DirectRegistry {
    public static void main(String[] args) {
        String keyPath = "Software\\MyApp";

        // 创建键 (create key)
        Advapi32Util.registryCreateKey(
            WinReg.HKEY_CURRENT_USER, keyPath);

        // 设置值 (set value)
        Advapi32Util.registrySetStringValue(
            WinReg.HKEY_CURRENT_USER, keyPath,
            "Setting", "Value");
        Advapi32Util.registrySetIntValue(
            WinReg.HKEY_CURRENT_USER, keyPath,
            "Count", 42);

        // 读取值 (read value)
        String value = Advapi32Util.registryGetStringValue(
            WinReg.HKEY_CURRENT_USER, keyPath, "Setting");

        // 检查键是否存在 (check key existence)
        boolean exists = Advapi32Util.registryKeyExists(
            WinReg.HKEY_CURRENT_USER, keyPath);
    }
}
```

也可通过 `ProcessBuilder` 调用 `reg.exe` 查询注册表 (无第三方依赖)。

---

## 5. 控制台与字符编码

### JDK 21+ 控制台 UTF-8 默认化

JDK 18 (JEP 400) 将文件 I/O 的默认编码改为 UTF-8，JDK 21 进一步将 `System.out` / `System.err` 在 Windows 控制台上也默认使用 UTF-8。

```
JDK 17 及之前 (Windows):
  System.out 编码 = 系统代码页 (system code page)
  例如: GBK (代码页 936), MS932 (代码页 932)
  → 中文输出在非中文 Windows 上乱码 (garbled output)

JDK 18+ (JEP 400):
  文件 I/O 默认编码 = UTF-8
  System.out 编码 = 仍可能使用系统代码页

JDK 21+:
  System.out / System.err = UTF-8 (在 Windows 控制台)
  → 跨平台控制台输出一致 (consistent console output)
```

### 控制台编码配置 (Console Encoding Configuration)

```powershell
# 方法 1: 设置控制台代码页 (set console code page)
chcp 65001  # 切换到 UTF-8

# 方法 2: JVM 参数 (JVM arguments)
java -Dstdout.encoding=UTF-8 -Dstderr.encoding=UTF-8 -jar app.jar

# 方法 3: PowerShell 配置 (PowerShell configuration)
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8

# 方法 4: Windows Terminal (推荐, recommended)
# Windows Terminal 原生支持 UTF-8，无需额外配置
```

```java
// 检查当前控制台编码 (check current console encoding, JDK 17+)
Console console = System.console();
if (console != null) {
    System.out.println("Console charset: " + console.charset());
}
// JDK 18+: Charset.defaultCharset() 始终返回 UTF-8
```

---

## 6. Windows 特定优化

### WinAPI 集成 (Windows API Integration)

JDK 在 Windows 上通过 JNI 调用 Windows API 实现特定功能。了解这些底层集成有助于性能调优和问题排查。

```
JDK 内部的 Windows API 使用:
┌──────────────────────┬─────────────────────────────────────┐
│ JDK 功能              │ 底层 Windows API                     │
├──────────────────────┼─────────────────────────────────────┤
│ 文件 I/O             │ CreateFileW, ReadFile, WriteFile     │
│ 异步 I/O (NIO.2)     │ IOCP (I/O Completion Ports)         │
│ 内存映射              │ CreateFileMappingW, MapViewOfFile   │
│ 进程管理              │ CreateProcessW, WaitForSingleObject │
│ 线程                  │ CreateThread, SetThreadPriority     │
│ 网络 Socket           │ WSAStartup, WSASend, WSARecv       │
│ 大页内存              │ VirtualAlloc (MEM_LARGE_PAGES)      │
│ 高精度计时            │ QueryPerformanceCounter/Frequency  │
│ 控制台                │ GetConsoleOutputCP, WriteConsoleW   │
│ 注册表 (Preferences) │ RegOpenKeyExW, RegSetValueExW       │
└──────────────────────┴─────────────────────────────────────┘
```

### IOCP 异步 I/O (I/O Completion Ports)

```java
// Windows 上 NIO.2 的 AsynchronousChannelGroup 使用 IOCP
// 这是 Windows 最高效的异步 I/O 模型

import java.nio.channels.*;
import java.nio.*;
import java.net.*;

// 创建异步服务端 (create async server)
AsynchronousServerSocketChannel server =
    AsynchronousServerSocketChannel.open();
server.bind(new InetSocketAddress(8080));

// IOCP 由 JDK 自动使用 (automatically used on Windows)
// 无需手动配置，NIO.2 异步操作自动受益
```

### 高精度计时 (High-Resolution Timing)

```java
// Windows 上 System.nanoTime() 使用 QueryPerformanceCounter
// 精度通常为 100 纳秒级别

long start = System.nanoTime();
// ... 业务逻辑
long elapsed = System.nanoTime() - start;

// Windows 特殊情况: Thread.sleep 精度
// 默认 Windows 计时器分辨率约 15.6ms (64 Hz)
// JDK 通过 timeBeginPeriod(1) 提升到 1ms 精度
// JDK 9+ 在不需要时会调用 timeEndPeriod(1) 恢复
```

---

## 7. DLL 加载与本地库

### DLL 加载路径 (DLL Loading Path)

JDK 在 Windows 上加载本地库 (native libraries) 时遵循特定的搜索路径。

```
DLL 搜索顺序 (search order):
1. System.loadLibrary("name")
   → 在 java.library.path 中搜索 name.dll

2. System.load("C:\\path\\to\\name.dll")
   → 加载指定绝对路径的 DLL

java.library.path 默认值 (Windows):
  1. 应用程序目录 (application directory)
  2. Windows 系统目录 (C:\Windows\System32)
  3. 16位系统目录 (C:\Windows\System)
  4. Windows 目录 (C:\Windows)
  5. PATH 环境变量中的目录
```

```java
// 加载 DLL (load DLL)
System.loadLibrary("mylib");              // 搜索 mylib.dll
System.load("C:\\libs\\mylib.dll");       // 绝对路径
System.getProperty("java.library.path"); // 查看搜索路径
```

### DLL 常见问题 (Common DLL Issues)

```powershell
# 检查 DLL 依赖 (check dependencies)
dumpbin /dependents C:\path\to\mylib.dll
```

```bash
# UnsatisfiedLinkError → 添加 DLL 目录到 java.library.path
java -Djava.library.path="C:\libs" -jar app.jar

# DLL 位数不匹配 → 64位 JDK 只能加载 64位 DLL (bitness mismatch)
```

### JDK 安全 DLL 加载 (Secure DLL Loading)

JDK 12+ 增强了 DLL 加载安全，使用 `SetDefaultDllDirectories` 防止 DLL 劫持攻击 (DLL hijacking)。推荐使用绝对路径加载。

```java
// 自定义安全加载 (custom secure loading)
Path dllPath = Path.of(System.getProperty("app.native.dir"), "mylib.dll");
System.load(dllPath.toAbsolutePath().toString());
```

---

## 8. jpackage 打包详解

### MSI 包创建 (MSI Package Creation)

```bash
# 基本 MSI 包 (basic MSI package)
jpackage --name MyApp \
         --input input \
         --main-jar app.jar \
         --main-class com.example.Main \
         --type msi

# 完整配置 (full configuration)
jpackage --name MyApp \
         --input input \
         --main-jar app.jar \
         --main-class com.example.Main \
         --type msi \
         --win-dir-chooser \
         --win-menu \
         --win-menu-group "My Company" \
         --win-shortcut \
         --win-shortcut-prompt \
         --win-per-user-install \
         --win-upgrade-uuid "12345678-1234-1234-1234-123456789012" \
         --app-version 1.0.0 \
         --vendor "My Company" \
         --description "My Application" \
         --icon icon.ico \
         --license-file LICENSE.txt \
         --install-dir "My Company\\MyApp"
```

支持的包类型: `msi` (Windows Installer，支持 GPO 部署/静默安装/升级检测) 和 `exe` (可执行安装程序)。企业部署推荐 MSI。

### 包含自定义 JRE (Custom JRE with jlink)

```bash
# 使用 jlink 创建精简 JRE + jpackage 打包
jpackage --name MyApp \
         --input input \
         --main-jar app.jar \
         --main-class com.example.Main \
         --type msi \
         --runtime-image custom-jre \
         --java-options "-Xmx512m" \
         --java-options "-Dfile.encoding=UTF-8" \
         --arguments "--config=default.yml"

# 结果: 自包含应用 (self-contained application)
# 用户无需单独安装 JDK
```

---

## 9. Windows ARM64

### JEP 388: Windows/AArch64 Port

JEP 388 在 JDK 16 引入了 Windows ARM64 (AArch64) 端口的实验性支持。

```
Windows ARM64 时间线:
JDK 16 ──── JEP 388: 实验性支持 (experimental)
           │ 目标: Surface Pro X, Windows Dev Kit 等设备
           │
JDK 17 ──── 继续完善, HotSpot C2 编译器支持
           │
JDK 21 ──── 成熟可用 (production-ready)
           │ Microsoft 提供 ARM64 构建
           │
JDK 24 ──── 稳定运行 (stable)
```

### ARM64 功能状态 (Feature Status)

| 功能 | 状态 | 说明 |
|------|------|------|
| **解释器** (interpreter) | ✅ 完全支持 | - |
| **C1 编译器** (client) | ✅ 完全支持 | 快速编译 |
| **C2 编译器** (server) | ✅ 完全支持 | 优化编译 |
| **ZGC** | ✅ 支持 | 低延迟 GC |
| **Shenandoah GC** | ✅ 支持 | 低暂停 GC |
| **Graal JIT** (GraalVM) | 🔬 实验性 | 部分支持 |
| **JFR** (Flight Recorder) | ✅ 支持 | 诊断工具 |
| **jpackage** | ✅ 支持 | ARM64 安装包 |

### x64 模拟 (x64 Emulation)

Windows 11 on ARM 支持 x64 模拟，但有性能损失。推荐使用原生 ARM64 JDK。

| 模式 | 相对性能 |
|------|---------|
| 原生 ARM64 JDK (native) | 100% |
| x64 模拟 JDK (emulated) | ~60-80% |

```powershell
# 检查 JDK 架构 (check JDK architecture)
java -XshowSettings:all 2>&1 | Select-String "os.arch"
# ARM64: os.arch = aarch64    x64: os.arch = amd64
```

---

## 10. Windows Server 与容器

### Windows Server 容器 (Windows Server Containers)

Windows Server 支持两种容器隔离模式 (container isolation modes)。

```
容器类型:
┌─────────────────────────────────────────────────────┐
│ 进程隔离 (Process Isolation)                         │
│ - 共享宿主内核 (shared host kernel)                   │
│ - 更轻量，启动更快                                    │
│ - 需要 Windows Server 版本匹配                        │
│ - 类似 Linux 容器                                    │
├─────────────────────────────────────────────────────┤
│ Hyper-V 隔离 (Hyper-V Isolation)                     │
│ - 每个容器有独立内核 (dedicated kernel)                │
│ - 更强隔离性                                         │
│ - 支持不同 Windows 版本                               │
│ - 额外开销较大                                       │
└─────────────────────────────────────────────────────┘
```

### Docker 使用 (Docker on Windows Server)

```dockerfile
# Windows Server Core 基础镜像 + JDK
FROM mcr.microsoft.com/windows/servercore:ltsc2022
ADD https://download.java.net/java/GA/jdk21/.../openjdk-21_windows-x64_bin.zip C:\temp\jdk.zip
RUN powershell Expand-Archive C:\temp\jdk.zip C:\Java; Remove-Item C:\temp\jdk.zip
ENV JAVA_HOME=C:\\Java\\jdk-21
ENV PATH="${JAVA_HOME}\\bin;${PATH}"
COPY target/app.jar C:/app/app.jar
CMD ["java", "-jar", "C:\\app\\app.jar"]

# Nano Server (更小的镜像, smaller image)
# 注意: 没有完整 Win32 API, AWT/Swing 不可用
# FROM mcr.microsoft.com/windows/nanoserver:ltsc2022
```

### 容器资源与配置 (Container Resources and Configuration)

```powershell
# Docker 资源限制 (resource limits)
docker run -d --name java-app --memory 2g --cpus 2 -p 8080:8080 my-java-app

# JDK 10+ 自动检测容器资源限制 (container awareness)
docker exec java-app java -XshowSettings:system -version

# Windows Server 优化 (server optimization)
# 禁用 Defender 实时保护 (开发环境, JDK 编译提速 10-30%)
Set-MpPreference -DisableRealtimeMonitoring $true

# 服务器核心模式 (Server Core) + JDK headless
java -Djava.awt.headless=true -jar app.jar
```

---

## 11. 性能调优

### 内存优化 (Memory Optimization)

**大页内存 (Large Pages)**:
```bash
# 启用大页 (需要管理员权限, requires admin)
# 1. 本地安全策略 → 本地策略 → 用户权利指派
# 2. "锁定内存中的页" → 添加用户
# (Local Security Policy → User Rights Assignment → Lock pages in memory)

# JVM 配置
-XX:+UseLargePages
```

**内存配置 (Memory Configuration)**:
```bash
# 基本配置
-Xms2g -Xmx2g

# Metaspace
-XX:MetaspaceSize=256m
-XX:MaxMetaspaceSize=512m

# 直接内存 (direct memory)
-XX:MaxDirectMemorySize=256m
```

### CPU 优化 (CPU Optimization)

```powershell
# 处理器亲和性 (processor affinity)
$process = Get-Process -Name java
$process.ProcessorAffinity = 0x0F  # 使用 CPU 0-3

# 优先级设置 (priority setting)
$process = Get-Process -Name java
$process.PriorityClass = 'High'
```

### I/O 优化 (I/O Optimization)

```powershell
# 禁用 8.3 文件名 (disable 8.3 names)
fsutil 8dot3name set C: 1

# 禁用最后访问时间更新 (disable last access time)
fsutil behavior set disablelastaccess 1
```

```bash
# Windows 使用 IOCP (I/O Completion Ports)
# JDK NIO.2 自动使用，无需手动配置
```

---

## 12. 常见问题

### 问题 1: 控制台编码问题

**症状**: 非 ASCII 字符显示为乱码 (garbled output for non-ASCII)

**解决方案**:
```bash
# JDK 21+ 默认 UTF-8，通常无需配置
# 旧版本使用以下参数:
-Dstdout.encoding=UTF-8
-Dstderr.encoding=UTF-8
```
```powershell
# PowerShell 配置
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001
```

### 问题 2: 路径长度限制

**症状**: 文件路径超过 260 字符时报错 (path exceeds MAX_PATH)

**解决方案**:
```powershell
# 启用长路径支持 (enable long path support, Windows 10 1607+)
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
    -Name "LongPathsEnabled" -Value 1

# 或使用 UNC 路径 (or use UNC path)
\\?\C:\very\long\path\...
```

### 问题 3: 防火墙阻止

**症状**: 网络连接被阻止 (network connection blocked)

**解决方案**:
```powershell
New-NetFirewallRule -DisplayName "Java Application" `
    -Direction Inbound -Program "C:\Java\jdk-21\bin\java.exe" -Action Allow
```

### 问题 4: 32 位支持移除

**症状**: JDK 24+ 无 32 位版本 (JEP 479)

**解决方案**:
- 迁移到 64 位 JDK (migrate to 64-bit JDK)
- 更新本地库 (JNI) 到 64 位 (update native libraries to 64-bit)
- 测试 64 位兼容性 (test 64-bit compatibility)

---

## 13. 监控和诊断

### 系统监控 (System Monitoring)

**任务管理器 (Task Manager)**:
```
Ctrl+Shift+Esc → 详细信息 → java.exe
```

**性能监视器 (Performance Monitor)**:
```powershell
# 打开性能监视器
perfmon

# 添加计数器 (add counters)
# Process → % Processor Time → java
# Process → Private Bytes → java
# Process → Thread Count → java
```

**PowerShell 监控 (PowerShell Monitoring)**:
```powershell
# CPU 使用 (CPU usage)
Get-Counter "\Process(java)\% Processor Time"

# 内存使用 (memory usage)
Get-Counter "\Process(java)\Private Bytes"

# 线程数 (thread count)
Get-Counter "\Process(java)\Thread Count"
```

### JVM 监控 (JVM Monitoring)

**JFR 配置 (JFR Configuration)**:
```bash
# 启动 JFR (start JFR)
-XX:StartFlightRecording=duration=60s,filename=recording.jfr

# 使用 jcmd
jcmd <pid> JFR.start duration=60s filename=recording.jfr
```

**GC 日志 (GC Logging)**:
```bash
# 统一日志格式 (unified logging format)
-Xlog:gc*,safepoint:file=gc.log:time,level,tags:filecount=5,filesize=10m
```

---

## 14. 最佳实践

### 生产部署清单 (Production Deployment Checklist)

- [ ] 使用 64 位 JDK (use 64-bit JDK)
- [ ] 配置适当的内存设置 (configure memory)
- [ ] 设置服务自动启动 (auto-start service)
- [ ] 配置日志轮转 (log rotation)
- [ ] 设置监控和告警 (monitoring and alerting)
- [ ] 配置防火墙规则 (firewall rules)
- [ ] 测试故障恢复 (test failure recovery)
- [ ] Windows Defender 排除 JDK 目录 (exclude JDK from antivirus scan)
- [ ] ARM64 设备使用原生 JDK (use native JDK on ARM64)

### 推荐配置 (Recommended Configuration)

```bash
# 生产环境 JVM 参数 (production JVM arguments)
-Xms2g -Xmx2g
-XX:+UseZGC
-XX:MaxGCPauseMillis=10
-XX:+UseLargePages
-XX:MetaspaceSize=256m
-XX:MaxMetaspaceSize=512m
-Dfile.encoding=UTF-8
-Dstdout.encoding=UTF-8
-Dstderr.encoding=UTF-8
-Xlog:gc*,safepoint:file=gc.log:time,level,tags:filecount=5,filesize=10m
-XX:StartFlightRecording=maxsize=100m,maxage=24h,disk=true
```

---

## 15. 相关链接

- [jpackage 文档](https://docs.oracle.com/en/java/javase/21/jpackage/)
- [Windows 服务最佳实践](https://docs.microsoft.com/en-us/windows/win32/services/services)
- [JEP 388: Windows/AArch64 Port](https://openjdk.org/jeps/388)
- [JEP 400: UTF-8 by Default](https://openjdk.org/jeps/400)
- [JEP 479: Remove Windows 32-bit x86 Port](https://openjdk.org/jeps/479)
- [性能调优指南](/by-topic/core/performance/)
- [JDK 版本文档](/by-version/)
