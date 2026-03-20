# Windows 平台

Windows 是企业环境中 Java 应用部署的重要平台。

---

## 概述

### 支持的架构

| 架构 | 状态 | 说明 |
|------|------|------|
| **x64 (AMD64)** | ✅ 主要平台 | 推荐 |
| **x86 (32位)** | ⚠️ 废弃中 | JDK 21 废弃，JDK 26 移除 |
| **ARM64** | 🔬 实验性 | Windows on ARM |

### 支持的版本

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
JDK 14 ──── jpackage 正式版
          │
JDK 17 ──── 改进安装程序
          │
JDK 21 ──── 废弃 x86 (32位) 端口 (JEP 449)
          │
JDK 26 ──── 移除 x86 (32位) 支持
```

---

## 安装与部署

### 安装方式

| 方式 | 说明 | 适用场景 |
|------|------|----------|
| **MSI 安装包** | 系统级安装 | 企业部署 |
| **EXE 安装包** | 用户级安装 | 开发环境 |
| **ZIP 压缩包** | 免安装 | 便携部署 |
| **jpackage** | 应用打包 | 应用分发 |

### MSI 安装

**静默安装**:
```powershell
# 静默安装
msiexec /i jdk-21_windows-x64_bin.msi /quiet /norestart

# 指定安装目录
msiexec /i jdk-21_windows-x64_bin.msi INSTALLDIR="C:\Java\jdk-21" /quiet

# 添加到 PATH
msiexec /i jdk-21_windows-x64_bin.msi ADDLOCAL="FeatureMain,FeatureEnvironment" /quiet
```

**企业部署**:
```powershell
# 使用 Group Policy 部署
# 1. 创建 GPO
# 2. 计算机配置 → 管理模板 → 软件 → 软件安装
# 3. 添加 MSI 包

# 或使用 SCCM
# 1. 创建应用程序
# 2. 添加部署类型
# 3. 分发到目标集合
```

### ZIP 部署

**解压部署**:
```powershell
# 下载并解压
Expand-Archive -Path openjdk-21_windows-x64_bin.zip -DestinationPath C:\Java

# 设置环境变量
[System.Environment]::SetEnvironmentVariable("JAVA_HOME", "C:\Java\jdk-21", "Machine")
[System.Environment]::SetEnvironmentVariable("PATH", "$env:PATH;C:\Java\jdk-21\bin", "Machine")
```

### jpackage 打包

**创建安装包**:
```bash
# 基本 MSI 包
jpackage --name MyApp \
         --input input \
         --main-jar app.jar \
         --main-class com.example.Main \
         --type msi

# 完整配置
jpackage --name MyApp \
         --input input \
         --main-jar app.jar \
         --main-class com.example.Main \
         --type msi \
         --win-dir-chooser \
         --win-menu \
         --win-shortcut \
         --win-per-user-install \
         --app-version 1.0.0 \
         --vendor "My Company" \
         --description "My Application" \
         --icon icon.ico
```

**支持的包类型**:
- `msi`: Windows Installer 包
- `exe`: 可执行安装程序

---

## 服务集成

### Windows 服务配置

**使用 sc 命令**:
```powershell
# 创建服务
sc create MyJavaApp binPath= "C:\Java\jdk-21\bin\java.exe -jar C:\app\app.jar" start= auto

# 配置服务
sc config MyJavaApp DisplayName= "My Java Application"
sc description MyJavaApp "Java application service"

# 启动服务
sc start MyJavaApp

# 停止服务
sc stop MyJavaApp

# 删除服务
sc delete MyJavaApp
```

**使用 NSSM (推荐)**:
```powershell
# 下载 NSSM
# https://nssm.cc/download

# 安装服务
nssm install MyJavaApp "C:\Java\jdk-21\bin\java.exe" "-jar C:\app\app.jar"

# 配置服务
nssm set MyJavaApp AppDirectory "C:\app"
nssm set MyJavaApp DisplayName "My Java Application"
nssm set MyJavaApp Description "Java application service"
nssm set MyJavaApp Start SERVICE_AUTO_START

# 配置日志
nssm set MyJavaApp AppStdout "C:\logs\app.log"
nssm set MyJavaApp AppStderr "C:\logs\error.log"

# 启动服务
nssm start MyJavaApp
```

**使用 WinSW**:
```xml
<!-- myapp.xml -->
<service>
  <id>MyJavaApp</id>
  <name>My Java Application</name>
  <description>Java application service</description>
  <executable>java</executable>
  <arguments>-jar C:\app\app.jar</arguments>
  <workingdirectory>C:\app</workingdirectory>
  <logpath>C:\logs</logpath>
  <log mode="roll-by-size">
    <sizeThreshold>10240</sizeThreshold>
    <keepFiles>8</keepFiles>
  </log>
  <onfailure action="restart" delay="10 sec"/>
  <onfailure action="restart" delay="20 sec"/>
  <onfailure action="none"/>
  <resetfailure>1 hour</resetfailure>
</service>
```

```powershell
# 安装服务
myapp.exe install

# 启动服务
myapp.exe start

# 停止服务
myapp.exe stop

# 卸载服务
myapp.exe uninstall
```

---

## 注册表集成

### Java Preferences API

**使用 Preferences API**:
```java
import java.util.prefs.Preferences;

public class RegistryExample {
    public static void main(String[] args) {
        // 用户首选项 (HKEY_CURRENT_USER)
        Preferences userPrefs = Preferences.userNodeForPackage(RegistryExample.class);
        userPrefs.put("setting1", "value1");
        userPrefs.putInt("setting2", 42);
        
        // 系统首选项 (HKEY_LOCAL_MACHINE)
        Preferences systemPrefs = Preferences.systemNodeForPackage(RegistryExample.class);
        systemPrefs.put("globalSetting", "globalValue");
        
        // 读取值
        String value = userPrefs.get("setting1", "default");
        System.out.println("Setting1: " + value);
    }
}
```

**注册表位置**:
```
HKEY_CURRENT_USER\Software\JavaSoft\Prefs\...
HKEY_LOCAL_MACHINE\Software\JavaSoft\Prefs\...
```

### 直接注册表访问

**使用 JNA**:
```java
import com.sun.jna.platform.win32.Advapi32Util;
import com.sun.jna.platform.win32.WinReg;

public class DirectRegistry {
    public static void main(String[] args) {
        String keyPath = "Software\\MyApp";
        
        // 创建键
        Advapi32Util.registryCreateKey(WinReg.HKEY_CURRENT_USER, keyPath);
        
        // 设置值
        Advapi32Util.registrySetStringValue(
            WinReg.HKEY_CURRENT_USER, keyPath, "Setting", "Value");
        
        // 读取值
        String value = Advapi32Util.registryGetStringValue(
            WinReg.HKEY_CURRENT_USER, keyPath, "Setting");
        
        System.out.println("Value: " + value);
    }
}
```

---

## 性能调优

### 内存优化

**大页内存**:
```bash
# 启用大页 (需要管理员权限)
# 1. 本地安全策略 → 本地策略 → 用户权利指派
# 2. "锁定内存中的页" → 添加用户

# JVM 配置
-XX:+UseLargePages
```

**内存配置**:
```bash
# 基本配置
-Xms2g -Xmx2g

# Metaspace
-XX:MetaspaceSize=256m
-XX:MaxMetaspaceSize=512m

# 直接内存
-XX:MaxDirectMemorySize=256m
```

### CPU 优化

**处理器亲和性**:
```powershell
# 使用 PowerShell 设置亲和性
$process = Get-Process -Name java
$process.ProcessorAffinity = 0x0F  # 使用 CPU 0-3
```

**优先级设置**:
```powershell
# 设置进程优先级
$process = Get-Process -Name java
$process.PriorityClass = 'High'
```

### I/O 优化

**文件系统优化**:
```powershell
# 禁用 8.3 文件名
fsutil 8dot3name set C: 1

# 禁用最后访问时间更新
fsutil behavior set disablelastaccess 1
```

**异步 I/O**:
```bash
# Windows 使用 IOCP
# JDK 自动使用，无需配置
```

---

## 常见问题

### 问题 1: 控制台编码问题

**症状**:
- 非 ASCII 字符显示为乱码
- 日志文件编码错误

**解决方案**:
```bash
# 设置编码
-Dfile.encoding=UTF-8
-Dconsole.encoding=UTF-8

# 或在 PowerShell 中
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001
```

### 问题 2: 路径长度限制

**症状**:
- 文件路径超过 260 字符时报错

**解决方案**:
```powershell
# 启用长路径支持 (Windows 10 1607+)
# 注册表修改
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
    -Name "LongPathsEnabled" -Value 1

# 或使用 UNC 路径
\\?\C:\very\long\path\...
```

### 问题 3: 防火墙阻止

**症状**:
- 网络连接被阻止
- 应用无法监听端口

**解决方案**:
```powershell
# 添加防火墙规则
New-NetFirewallRule -DisplayName "Java Application" `
    -Direction Inbound -Program "C:\Java\jdk-21\bin\java.exe" -Action Allow
```

### 问题 4: 32 位支持移除

**症状**:
- JDK 26+ 无 32 位版本

**解决方案**:
- 迁移到 64 位 JDK
- 更新本地库 (JNI) 到 64 位
- 测试 64 位兼容性

---

## 监控和诊断

### 系统监控

**任务管理器**:
```
Ctrl+Shift+Esc → 详细信息 → java.exe
```

**性能监视器**:
```powershell
# 打开性能监视器
perfmon

# 添加计数器
# Process → % Processor Time → java
# Process → Private Bytes → java
# Process → Thread Count → java
```

**PowerShell 监控**:
```powershell
# CPU 使用
Get-Counter "\Process(java)\% Processor Time"

# 内存使用
Get-Counter "\Process(java)\Private Bytes"

# 线程数
Get-Counter "\Process(java)\Thread Count"
```

### JVM 监控

**JFR 配置**:
```bash
# 启动 JFR
-XX:StartFlightRecording=duration=60s,filename=recording.jfr

# 使用 jcmd
jcmd <pid> JFR.start duration=60s filename=recording.jfr
```

**GC 日志**:
```bash
# 统一日志格式
-Xlog:gc*,safepoint:file=gc.log:time,level,tags:filecount=5,filesize=10m
```

---

## 最佳实践

### 生产部署清单

- [ ] 使用 64 位 JDK
- [ ] 配置适当的内存设置
- [ ] 设置服务自动启动
- [ ] 配置日志轮转
- [ ] 设置监控和告警
- [ ] 配置防火墙规则
- [ ] 测试故障恢复

### 推荐配置

```bash
# 生产环境 JVM 参数
-Xms2g -Xmx2g
-XX:+UseZGC
-XX:MaxGCPauseMillis=10
-XX:+UseLargePages
-XX:MetaspaceSize=256m
-XX:MaxMetaspaceSize=512m
-Dfile.encoding=UTF-8
-Dconsole.encoding=UTF-8
-Xlog:gc*,safepoint:file=gc.log:time,level,tags:filecount=5,filesize=10m
-XX:StartFlightRecording=maxsize=100m,maxage=24h,disk=true
```

---

## 相关链接

- [jpackage 文档](https://docs.oracle.com/en/java/javase/21/jpackage/)
- [Windows 服务最佳实践](https://docs.microsoft.com/en-us/windows/win32/services/services)
- [性能调优指南](/by-topic/core/performance/)
- [JDK 版本文档](/by-version/)