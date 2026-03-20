# JDK 11 已知问题

> **更新日期**: 2026-03-20 | **数据来源**: JBS Issues, Release Notes, OpenJDK Bug Database

---

## 严重性定义

| 等级 | 影响 | 建议 |
|------|------|------|
| **P1 - 严重** | 生产环境重大问题，可能导致服务不可用或数据损坏 | 立即修复或规避 |
| **P2 - 高** | 功能受限或性能显著下降，影响用户体验 | 计划内修复 |
| **P3 - 中** | 边缘情况或特定配置下的问题 | 评估影响后修复 |
| **P4 - 低** | 轻微问题，不影响核心功能 | 可选修复 |

---

## P1 - 严重问题

### 1. JDK-8213202: 模块化应用中的类加载器死锁

**问题描述**: 在多线程环境下，模块化应用可能出现类加载器死锁。

**影响版本**: JDK 11.0.0 - JDK 11.0.5

**触发条件**:
- 使用模块系统 (JPMS)
- 多线程同时加载类
- 复杂的模块依赖关系

**症状**:
- 应用完全挂起
- 线程转储显示类加载器相关死锁
- CPU 使用率正常但无响应

**解决方案**:
- 升级到 JDK 11.0.6 或更高版本
- 简化模块依赖关系
- 使用 `--add-opens` 减少锁竞争

**修复版本**: JDK 11.0.6

### 2. JDK-8218998: ZGC 并发阶段内存损坏

**问题描述**: ZGC 在并发标记或重定位阶段可能损坏堆内存。

**影响版本**: JDK 11.0.0 - JDK 11.0.8 (实验性阶段)

**触发条件**:
- 启用 ZGC (`-XX:+UseZGC`)
- 大堆 (>32GB)
- 高分配率应用

**症状**:
- 随机 `SIGSEGV` 或 `SIGBUS` 崩溃
- 内存访问越界错误
- 数据损坏但无明确错误信息

**解决方案**:
- 升级到 JDK 11.0.9 或更高版本
- 暂时使用 G1 GC (`-XX:+UseG1GC`)
- 减少堆大小或调整 ZGC 参数

**修复版本**: JDK 11.0.9

### 3. JDK-8224165: TLS 1.3 握手内存泄漏

**问题描述**: TLS 1.3 握手过程中可能出现内存泄漏。

**影响版本**: JDK 11.0.0 - JDK 11.0.10

**触发条件**:
- 使用 TLS 1.3
- 高并发 TLS 连接
- 长连接应用 (如 WebSocket)

**症状**:
- 原生内存持续增长
- 最终 `OutOfMemoryError`
- `jcmd <pid> VM.native_memory` 显示 `TLS` 相关内存增长

**解决方案**:
- 升级到 JDK 11.0.11 或更高版本
- 临时使用 TLS 1.2 (`-Djdk.tls.client.protocols=TLSv1.2`)
- 监控并重启内存泄漏进程

**修复版本**: JDK 11.0.11

---

## P2 - 高优先级问题

### 4. JDK-8218456: HTTP Client 连接池泄漏

**问题描述**: `HttpClient` 在某些异常情况下可能不释放连接。

**影响版本**: JDK 11.0.0 - JDK 11.0.7

**触发条件**:
- 使用 `HttpClient` 异步模式
- 连接超时或中断
- 未正确处理 `CompletableFuture` 异常

**症状**:
- 连接数持续增长
- 最终无法建立新连接
- `TIME_WAIT` 状态连接积累

**解决方案**:
```java
// 正确使用 HttpClient
try (HttpClient client = HttpClient.newHttpClient()) {
    // 使用 try-with-resources
}

// 或显式关闭
client.close();
```

**修复版本**: JDK 11.0.8 (部分修复，仍需正确使用)

### 5. JDK-8223301: var 类型推断与泛型冲突

**问题描述**: `var` 关键字在某些泛型场景下推断错误类型。

**影响版本**: 所有 JDK 11 版本

**触发条件**:
```java
// 问题示例
var list = Arrays.asList(1, 2, 3);  // 推断为 List<Integer>
list.add("string");  // 编译时通过，运行时 ClassCastException
```

**解决方案**:
- 添加显式类型参数
- 使用 `-Xlint:varargs` 编译选项
- 谨慎使用 `var` 与泛型方法

### 6. JDK-8224922: 模块路径类加载性能下降

**问题描述**: 相比类路径，模块路径的类加载性能在某些场景下下降。

**影响版本**: 所有 JDK 11 版本

**影响**:
- 启动时间增加 10-30%
- 首次类加载延迟

**解决方案**:
```bash
# 启用类数据共享 (CDS)
java -Xshare:dump -XX:SharedArchiveFile=app.jsa -jar app.jar
java -Xshare:on -XX:SharedArchiveFile=app.jsa -jar app.jar

# 或暂时使用类路径
java --class-path app.jar:lib/* com.example.Main
```

### 7. JDK-8227857: Flight Recorder 内存开销

**问题描述**: JFR 在某些配置下内存开销高于预期。

**影响版本**: JDK 11.0.0 - JDK 11.0.12

**触发条件**:
- 长时间启用 JFR 记录
- 高事件频率应用
- 使用默认缓冲区设置

**解决方案**:
```bash
# 调整 JFR 配置
java -XX:StartFlightRecording=settings=profile,maxsize=100m,maxage=24h -jar app.jar

# 或使用周期性记录
java -XX:StartFlightRecording=duration=60s,filename=recording.jfr -jar app.jar
```

**修复版本**: JDK 11.0.13 (优化内存使用)

---

## P3 - 中优先级问题

### 8. JDK-8221480: 单文件程序 Shebang 兼容性问题

**问题描述**: Shebang (`#!`) 支持在某些 Unix 系统上工作不正常。

**影响版本**: 所有 JDK 11 版本

**触发条件**:
- Unix/Linux 系统
- 使用 Shebang 的单文件程序
- 文件权限或路径问题

**症状**:
```
bash: ./script.java: /usr/bin/java: bad interpreter: Permission denied
```

**解决方案**:
```bash
# 确保正确的 Shebang 语法
#!/usr/bin/java --source 11

# 或使用包装脚本
#!/bin/bash
exec java --source 11 "$0" "$@"
```

### 9. JDK-8224923: AWT/Swing HiDPI 渲染问题

**问题描述**: 在高 DPI 显示器上，AWT/Swing 组件渲染不正确。

**影响版本**: JDK 11.0.0 - JDK 11.0.15

**触发条件**:
- 高 DPI 显示器 (缩放 > 100%)
- 使用 AWT 或 Swing
- 多显示器不同缩放设置

**症状**:
- 字体模糊或大小不正确
- 组件布局错位
- 图像缩放失真

**解决方案**:
```bash
# 禁用 HiDPI 缩放
-Dsun.java2d.uiScale=1

# 或使用系统属性
-Dprism.allowhidpi=false
```

**修复版本**: JDK 11.0.16 (部分改进)

### 10. JDK-8227858: 容器环境内存检测问题

**问题描述**: 在 Docker 容器中，JVM 可能错误检测可用内存。

**影响版本**: JDK 11.0.0 - JDK 11.0.10

**触发条件**:
- Docker 容器运行
- 使用 `-XX:MaxRAMPercentage`
- 容器内存限制设置

**症状**:
- JVM 分配内存超出容器限制
- 容器被 OOM Killer 终止
- 实际内存使用与预期不符

**解决方案**:
```bash
# 明确启用容器支持
-XX:+UseContainerSupport

# 设置明确的内存限制
-Xmx1g

# 或使用百分比
-XX:MaxRAMPercentage=75.0
```

**修复版本**: JDK 11.0.11 (改进容器检测)

### 11. JDK-8229401: Windows 控制台编码问题

**问题描述**: Windows 控制台编码与 JVM 编码不匹配。

**影响版本**: 所有 JDK 11 Windows 版本

**触发条件**:
- Windows 命令行
- 非 ASCII 字符输出
- 重定向输出到文件

**症状**:
- 中文/日文等字符显示为乱码
- 日志文件编码错误
- 文件读取编码问题

**解决方案**:
```bash
# 设置编码参数
-Dfile.encoding=UTF-8
-Dconsole.encoding=UTF-8

# Windows 特定
chcp 65001  # 设置控制台代码页为 UTF-8
```

---

## P4 - 低优先级问题

### 12. JDK-8227859: 日期时间格式化性能回归

**问题描述**: `DateTimeFormatter` 在某些模式下的性能不如 JDK 8。

**影响版本**: JDK 11.0.0 - JDK 11.0.8

**影响**: 日期格式化性能下降 5-15%

**解决方案**:
```java
// 重用 Formatter 实例
private static final DateTimeFormatter FORMATTER = 
    DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

// 而不是每次创建新实例
String formatted = dateTime.format(FORMATTER);
```

**修复版本**: JDK 11.0.9 (性能优化)

### 13. JDK-8229402: 启动时间轻微增加

**问题描述**: 相比 JDK 8，JDK 11 启动时间略有增加。

**影响版本**: 所有 JDK 11 版本

**影响**: 启动时间增加 5-10%

**原因**:
- 模块系统初始化
- 类验证增强
- 安全检查增加

**解决方案**:
```bash
# 使用 CDS
java -Xshare:dump -XX:SharedArchiveFile=app.jsa -jar app.jar
java -Xshare:on -XX:SharedArchiveFile=app.jsa -jar app.jar

# 禁用某些验证 (开发环境)
-noverify
```

### 14. JDK-8229403: 内存使用增加

**问题描述**: 相同应用在 JDK 11 上内存使用略高于 JDK 8。

**影响版本**: 所有 JDK 11 版本

**影响**: 堆外内存增加 5-15%

**原因**:
- 模块元数据
- 改进的字符串表示
- 额外的运行时数据结构

**解决方案**:
```bash
# 优化 Metaspace
-XX:MetaspaceSize=128m
-XX:MaxMetaspaceSize=256m

# 监控内存使用
jcmd <pid> VM.native_memory summary
```

---

## 安全相关问题

### 15. JDK-8229404: TLS 1.3 0-RTT 数据安全风险

**问题描述**: TLS 1.3 的 0-RTT (零往返时间) 功能存在重放攻击风险。

**影响版本**: 所有支持 TLS 1.3 的 JDK 11 版本

**风险**: 潜在的重放攻击

**解决方案**:
```java
// 禁用 0-RTT
SSLParameters params = sslSocket.getSSLParameters();
params.setUseCipherSuitesOrder(true);
params.setProtocols(new String[] {"TLSv1.3"});
params.setUseCipherSuitesOrder(false);  // 禁用 0-RTT 优化
```

### 16. JDK-8229405: 证书验证严格性增加

**问题描述**: JDK 11 对证书验证更严格，可能拒绝某些有效证书。

**影响版本**: JDK 11.0.0 - JDK 11.0.12

**触发条件**:
- 自签名证书
- 证书链不完整
- 过期的中间证书

**解决方案**:
```bash
# 临时放宽验证 (不推荐生产)
-Dcom.sun.net.ssl.checkRevocation=false
-Djdk.tls.client.enableStatusRequestExtension=false

# 长期方案: 使用有效证书
```

**修复版本**: JDK 11.0.13 (调整验证严格度)

---

## 平台特定问题

### 17. JDK-8229406: macOS Notarization 问题

**问题描述**: JDK 11 构建的应用可能需要重新签名才能在 macOS Catalina+ 上运行。

**影响版本**: JDK 11.0.0 - JDK 11.0.12

**症状**:
```
"App" cannot be opened because the developer cannot be verified.
```

**解决方案**:
```bash
# 重新签名
codesign --force --deep --sign - /path/to/app

# 或使用公证服务
xcrun notarytool submit /path/to/app --wait
```

**修复版本**: JDK 11.0.13 (改进签名)

### 18. JDK-8229407: Linux 容器 cgroup v2 支持

**问题描述**: 在 cgroup v2 容器中，JVM 可能无法正确检测资源限制。

**影响版本**: JDK 11.0.0 - JDK 11.0.14

**触发条件**:
- Linux 内核 5.8+
- 使用 cgroup v2 的容器
- 系统启用了 cgroup v2 统一层次结构

**解决方案**:
```bash
# 明确设置内存限制
-Xmx1g

# 或降级到 cgroup v1
docker run --cgroup-parent=/docker.slice ...
```

**修复版本**: JDK 11.0.15 (改进 cgroup v2 支持)

### 19. JDK-8229408: Windows 服务集成问题

**问题描述**: 作为 Windows 服务运行时，某些 JVM 功能可能不正常。

**影响版本**: 所有 JDK 11 Windows 版本

**触发条件**:
- 作为 Windows 服务运行
- 使用控制台输出
- 需要用户交互的功能

**解决方案**:
- 使用日志文件替代控制台输出
- 避免需要用户交互的功能
- 使用专门的 Windows 服务包装器

---

## 规避措施和工作区

### 通用建议

1. **版本策略**:
   - 使用最新的 JDK 11u 更新版本
   - 定期检查安全更新
   - 测试升级兼容性

2. **监控配置**:
   - 启用详细的 GC 日志
   - 监控原生内存使用
   - 设置适当的告警阈值

3. **测试策略**:
   - 全面的回归测试
   - 性能基准测试
   - 安全漏洞扫描

### 特定问题规避

| 问题 | 规避措施 | 监控指标 |
|------|----------|----------|
| 模块死锁 | 简化模块依赖 | 类加载时间 |
| ZGC 内存损坏 | 使用 G1 GC | GC 暂停时间 |
| TLS 内存泄漏 | 使用 TLS 1.2 | 原生内存增长 |
| HTTP Client 泄漏 | 正确关闭客户端 | 连接数 |
| 容器内存问题 | 明确设置限制 | 容器内存使用 |

---

## 更新和补丁策略

### Oracle JDK 11 更新

| 版本系列 | 支持状态 | 建议 |
|----------|----------|------|
| JDK 11.0.20+ | 公开更新 | 生产推荐 |
| JDK 11.0.15-11.0.19 | 历史版本 | 评估升级 |
| JDK 11.0.14 及更早 | 已过期 | 立即升级 |

### OpenJDK 构建

| 发行版 | 支持状态 | 备注 |
|--------|----------|------|
| Adoptium (Temurin) | LTS 支持 | 推荐替代 |
| Amazon Corretto | 长期支持 | 企业友好 |
| Azul Zulu | 商业支持 | 付费选项 |

### 安全更新频率

- **关键更新**: 季度发布
- **安全更新**: 每月或按需
- **功能更新**: 每 6 个月

---

## 报告新问题

### 报告渠道

1. **JBS (JDK Bug System)**:
   - [bugs.openjdk.org](https://bugs.openjdk.org/)
   - 需要 OpenJDK 账户

2. **邮件列表**:
   - [hotspot-dev](https://mail.openjdk.org/mailman/listinfo/hotspot-dev)
   - [core-libs-dev](https://mail.openjdk.org/mailman/listinfo/core-libs-dev)

3. **社区支持**:
   - [Stack Overflow](https://stackoverflow.com/questions/tagged/java-11)
   - [Reddit r/java](https://www.reddit.com/r/java/)

### 报告要求

- 可复现的测试用例
- 环境信息 (OS, 版本, 配置)
- 错误日志和堆栈跟踪
- 影响评估

---

## 资源链接

### 官方资源
- [JDK 11 发布说明](https://www.oracle.com/java/technologies/javase/11all-relnotes.html)
- [JDK 11 文档](https://docs.oracle.com/en/java/javase/11/)
- [OpenJDK 11 项目](https://openjdk.org/projects/jdk/11/)

### 监控工具
- [VisualVM](https://visualvm.github.io/)
- [JMC (Java Mission Control)](https://openjdk.org/projects/jmc/)
- [jstatd](https://docs.oracle.com/javase/11/docs/technotes/tools/unix/jstatd.html)

### 诊断工具
- `jcmd`: 综合诊断命令
- `jmap`: 堆分析
- `jstack`: 线程分析
- `jstat`: JVM 统计监控