# JDK 17 破坏性变更

> **影响评估**: 中 - 主要影响废弃API的使用者，安全管理和内部API访问

---

## 已移除的 API 和功能

### 1. RMI Activation 移除 (JEP 407)

**变更详情**: 完全移除 `java.rmi.activation` 包及相关功能。

**影响代码**:
```java
// 使用 RMI Activation 的代码不再编译
import java.rmi.activation.Activatable;
import java.rmi.activation.ActivationID;
import java.rmi.activation.ActivationGroup;
import java.rmi.activation.ActivationGroupDesc;

// RMI 激活相关 API 调用将失败
Activatable.exportObject(...);
ActivationGroup.createGroup(...);
```

**错误信息**:
```bash
error: package java.rmi.activation does not exist
error: cannot find symbol: class Activatable
```

**替代方案**:
- **现代 RPC 框架**: gRPC, Apache Thrift
- **消息队列**: Apache Kafka, RabbitMQ
- **RESTful 服务**: Spring Boot, Micronaut, Quarkus
- **传统 RMI**: 使用非激活的 RMI (仍然可用)

**迁移步骤**:
1. 识别所有 `java.rmi.activation` 导入
2. 评估使用场景: 动态对象激活 vs 静态服务
3. 选择替代技术栈
4. 逐步迁移，保持向后兼容性

### 2. 实验性 AOT 和 JIT 编译器移除 (JEP 410)

**变更详情**: 移除实验性的提前编译 (AOT) 和 Graal JIT 编译器。

**影响功能**:
- `jaotc` 命令行工具
- `jdk.aot` 模块
- `-XX:AOTLibrary` JVM 参数
- Graal JIT 的实验性集成

**错误信息**:
```bash
# jaotc 命令不再存在
jaotc: command not found

# AOT 相关参数无效
Error: VM option 'AOTLibrary' is experimental and must be enabled via -XX:+UnlockExperimentalVMOptions.
```

**替代方案**:
- **JIT 编译**: 使用标准的 C2 编译器 (HotSpot)
- **未来方案**: 等待 Project Leyden (静态镜像)
- **GraalVM**: 使用独立的 GraalVM 发行版

**临时解决方案**: 无，功能已完全移除。

### 3. Applet API 废弃 (JEP 398)

**变更详情**: `java.applet` 包标记为废弃，计划在未来版本中移除。

**警告信息**:
```
warning: [removal] Applet in java.applet has been deprecated and marked for removal
warning: [removal] AppletContext in java.applet has been deprecated and marked for removal
warning: [removal] AppletStub in java.applet has been deprecated and marked for removal
```

**影响应用**:
- 基于 Applet 的 Web 应用
- Java Web Start 应用
- 教育工具和小游戏

**迁移路径**:
```html
<!-- 从 Applet 迁移到现代 Web 技术 -->

<!-- 之前: Java Applet -->
<applet code="MyApplet.class" width="300" height="200">
    <param name="data" value="example">
</applet>

<!-- 之后: HTML5 + JavaScript -->
<canvas id="myCanvas" width="300" height="200"></canvas>
<script src="myapp.js"></script>

<!-- 或使用 WebAssembly -->
<script type="module">
    import init, { run_app } from './myapp.wasm';
    init().then(() => run_app());
</script>
```

**替代技术**:
- **Web 应用**: HTML5, CSS3, JavaScript/TypeScript
- **桌面应用**: JavaFX, Swing (仍然可用)
- **混合应用**: Electron, NW.js
- **教育工具**: Processing (p5.js), Blockly

### 4. Security Manager 废弃 (JEP 411)

**变更详情**: Security Manager 和相关 API 标记为废弃。

**警告信息**:
```
warning: [removal] SecurityManager in java.lang has been deprecated and marked for removal
warning: [removal] checkPermission in java.lang.SecurityManager has been deprecated and marked for removal
```

**影响代码**:
```java
// 自定义 SecurityManager
public class CustomSecurityManager extends SecurityManager {
    @Override
    public void checkPermission(Permission perm) {
        // 安全检查逻辑
    }
}

// 设置 SecurityManager
System.setSecurityManager(new CustomSecurityManager());

// 检查权限
SecurityManager sm = System.getSecurityManager();
if (sm != null) {
    sm.checkPermission(new FilePermission("/tmp/file", "read"));
}
```

**迁移策略**:

**选项 A: 使用模块系统** (推荐)
```bash
# 使用模块访问控制替代权限检查
--add-reads module1=module2
--add-exports module/package=target.module
--add-opens module/package=target.module
--add-modules module.name
```

**选项 B: 使用容器技术**
```dockerfile
# Dockerfile 示例
FROM eclipse-temurin:17-jre

# 容器权限控制
USER nobody
RUN chown nobody:nobody /app
WORKDIR /app

# 只读文件系统
VOLUME /tmp
COPY --chown=nobody:nobody app.jar /app/

# 最小权限原则
CMD ["java", "-jar", "app.jar"]
```

**选项 C: 使用现代安全框架**
- **认证/授权**: Spring Security, Apache Shiro
- **代码沙箱**: 使用单独的 JVM 进程
- **资源控制**: 使用操作系统级别的控制

**临时解决方案**:
```bash
# 禁用废弃警告
-Xlint:-removal

# 但长期必须迁移
```

---

## 行为变更和兼容性问题

### 5. 严格的模块封装

**变更**: 模块系统封装更严格，影响反射访问。

**错误示例**:
```java
// 尝试访问非导出包
Class<?> clazz = Class.forName("jdk.internal.misc.Unsafe");
Field field = clazz.getDeclaredField("theUnsafe");
field.setAccessible(true);  // JDK 17: InaccessibleObjectException
```

**解决方案**:
```bash
# 添加必要的 --add-opens 参数
java --add-opens java.base/jdk.internal.misc=ALL-UNNAMED \
     --add-opens java.base/sun.nio.ch=ALL-UNNAMED \
     --add-opens java.base/java.lang=ALL-UNNAMED \
     -jar app.jar

# 或使用模块声明
module my.app {
    opens my.reflective.package to java.base;
}
```

**常见需要开放的包**:
- `java.base/jdk.internal.misc` (Unsafe 访问)
- `java.base/sun.nio.ch` (NIO 内部)
- `java.base/java.lang` (反射工具)
- `java.desktop/sun.awt` (AWT 内部)

### 6. 类加载器层次变化

**变更**: 模块系统改变了类加载器层次结构。

**JDK 11 之前的层次**:
```
Bootstrap ClassLoader
    ↓
Extension ClassLoader  
    ↓
Application ClassLoader
```

**JDK 17 模块化层次**:
```
Bootstrap ClassLoader (Java SE 模块)
    ↓
Platform ClassLoader (平台模块)
    ↓
Application ClassLoader (应用模块)
```

**影响**:
- 自定义类加载器代码可能受影响
- 资源查找逻辑可能变化
- 类加载委托模式调整

**检查点**:
```java
// 检查类加载器行为
ClassLoader cl = MyClass.class.getClassLoader();
System.out.println(cl);  // jdk.internal.loader.ClassLoaders$AppClassLoader

// 资源查找
URL resource = cl.getResource("META-INF/services/my.service");
```

### 7. 序列化行为变更

**变更**: 默认的序列化过滤器更严格。

**错误示例**:
```java
// 反序列化可能被拒绝
ObjectInputStream ois = new ObjectInputStream(input);
Object obj = ois.readObject();  // 可能抛出 InvalidClassException

// 错误信息
java.io.InvalidClassException: filter status: REJECTED
```

**解决方案**:
```java
// 配置合适的过滤器
ObjectInputFilter filter = ObjectInputFilter.allowFilter(
    cl -> cl != null && cl.getName().startsWith("com.example."),
    ObjectInputFilter.Status.REJECTED
);

ObjectInputStream ois = new ObjectInputStream(input);
ois.setObjectInputFilter(filter);
```

### 8. 默认 TLS 配置变更

**变更**: 更严格的安全默认配置。

**影响**:
- TLS 1.0 和 1.1 默认禁用
- 弱密码套件默认禁用
- 证书验证更严格

**连接失败场景**:
```bash
# 连接只支持 TLS 1.0/1.1 的旧服务器失败
javax.net.ssl.SSLHandshakeException: No appropriate protocol

# 使用弱密码套件失败
javax.net.ssl.SSLHandshakeException: Received fatal alert: handshake_failure
```

**临时解决方案** (不推荐生产):
```bash
# 启用旧协议 (仅测试)
-Djdk.tls.client.protocols=TLSv1,TLSv1.1,TLSv1.2,TLSv1.3

# 启用弱算法 (仅测试)
-Djdk.tls.disabledAlgorithms=""
```

**长期解决方案**:
- 升级服务器支持 TLS 1.2+
- 更新证书使用强算法
- 使用现代密码套件

---

## 工具和命令行变更

### 9. 命令行工具变更

**已移除/变更的工具**:
- `jaotc`: 完全移除
- `jjs` (Nashorn): 已移除 (从 JDK 15 开始)
- `pack200`/`unpack200`: 已移除 (从 JDK 14 开始)

**新工具**:
- `jpackage`: 应用打包工具 (正式版)
- `jfr`: Flight Recorder 工具增强

**工具行为变更**:
```bash
# jmap 参数变更
jmap -permstat <pid>  # JDK 8: 可用
jmap -clstats <pid>   # JDK 17: 替代方案

# jstat 变更
jstat -gcpermcapacity <pid>  # JDK 8: 监控 PermGen
jstat -gcmetacapacity <pid>  # JDK 17: 监控 Metaspace
```

### 10. 启动参数变更

**已废弃的参数**:
```bash
# GC 相关
-XX:+UseConcMarkSweepGC    # 使用 G1 或 ZGC
-XX:+UseParNewGC          # 使用 G1 或 ZGC
-XX:+CMSParallelRemarkEnabled  # G1 自动处理

# 性能相关  
-XX:+AggressiveOpts       # 已默认启用优化
-XX:+UseBiasedLocking     # 默认已优化

# 内存相关
-XX:PermSize=128m         # 使用 -XX:MetaspaceSize
-XX:MaxPermSize=256m      # 使用 -XX:MaxMetaspaceSize
```

**新增参数**:
```bash
# ZGC 增强 (不再需要实验标志)
-XX:+UseZGC
-XX:ZAllocationSpikeTolerance=2.0

# 容器支持增强
-XX:+UseContainerSupport  # 默认启用
-XX:MaxRAMPercentage=75.0
-XX:InitialRAMPercentage=50.0

# 统一日志系统
-Xlog:gc*,safepoint:file=gc.log:time,level,tags
```

### 11. 监控和诊断变更

**JVM 统计变更**:
- PermGen 统计 → Metaspace 统计
- CMS GC 统计 → G1/ZGC 统计
- 线程状态统计更详细

**监控工具更新**:
```bash
# 使用新版 jcmd
jcmd <pid> GC.heap_info       # 替代部分 jmap 功能
jcmd <pid> VM.native_memory   # 详细原生内存信息
jcmd <pid> Compiler.codecache # 代码缓存信息

# JFR 增强
jcmd <pid> JFR.start duration=60s settings=profile
jcmd <pid> JFR.dump filename=recording.jfr
```

---

## 平台特定变更

### 12. macOS 渲染管道变更 (JEP 382)

**变更**: 从 OpenGL 迁移到 Metal 渲染管道。

**影响**:
- AWT/Swing 应用渲染后端变化
- 3D 渲染性能特征变化
- 图形 Bug 可能不同

**症状**:
- 渲染性能变化
- 图形瑕疵可能不同
- 高 DPI 渲染可能受影响

**解决方案**:
```bash
# 强制使用 OpenGL (如果需要)
-Dsun.java2d.metal=false
-Dsun.java2d.opengl=true

# 或使用 Metal 优化
-Dsun.java2d.metal=true  # 默认
```

### 13. Apple Silicon (AArch64) 支持

**变更**: 原生 Apple Silicon 支持。

**兼容性问题**:
- 本地库 (JNI) 需要重新编译
- 性能特征不同
- Rosetta 2 翻译层可能引入问题

**检查清单**:
```bash
# 验证架构
uname -m  # 应为 arm64
java -version  # 应包含 AArch64

# 检查本地库
file /path/to/libnative.dylib
# 应为: Mach-O 64-bit dynamically linked shared library arm64
```

**本地库迁移**:
```bash
# 重新编译本地库
./configure --host=aarch64-apple-darwin
make clean
make

# 或使用通用二进制
lipo -create -output libuniversal.dylib \
     libx86_64.dylib libarm64.dylib
```

### 14. Windows 安装程序变更

**变更**: 安装程序和注册表项变更。

**影响**:
- 自动 JRE 检测可能受影响
- 浏览器插件完全移除
- 注册表路径可能变化

**验证安装**:
```powershell
# 检查注册表
Get-ItemProperty -Path "HKLM:\SOFTWARE\JavaSoft\JDK\17"

# 检查环境变量
$env:JAVA_HOME
java -version
```

---

## 第三方库兼容性

### 15. 常见库的 JDK 17 兼容性

| 库/框架 | 最小兼容版本 | 关键问题 | 解决方案 |
|---------|--------------|----------|----------|
| **Spring Framework** | 5.3+ | Security Manager 依赖 | 升级到 Spring 6.x |
| **Hibernate** | 5.6+ | 反射访问内部 API | 使用 `--add-opens` |
| **Jackson** | 2.13+ | 模块化兼容性 | 升级版本 |
| **Log4j 2** | 2.17+ | 安全修复 | 必须升级 |
| **Apache HttpClient** | 5.1+ | 模块化 | 升级或使用 JDK HttpClient |
| **JUnit 5** | 5.8+ | 模块测试支持 | 升级 |
| **Mockito** | 4.0+ | 反射 API 变化 | 使用 inline mock maker |

### 16. 反射库兼容性

**影响库**:
- **ASM**: 需要 9.0+ 版本
- **ByteBuddy**: 需要 1.12+ 版本
- **Javassist**: 需要 3.28+ 版本
- **CGLIB**: 需要 3.3+ 版本

**兼容性检查**:
```xml
<!-- 更新依赖版本 -->
<dependency>
    <groupId>org.ow2.asm</groupId>
    <artifactId>asm</artifactId>
    <version>9.3</version>
</dependency>
<dependency>
    <groupId>net.bytebuddy</groupId>
    <artifactId>byte-buddy</artifactId>
    <version>1.12.8</version>
</dependency>
```

### 17. 序列化库兼容性

**变更影响**:
- 自定义序列化框架
- 对象关系映射 (ORM)
- 分布式缓存

**测试建议**:
1. 序列化/反序列化往返测试
2. 版本兼容性测试
3. 安全性测试 (反序列化攻击防护)

---

## 迁移检查和验证

### 兼容性测试清单

**必须测试的项目**:
- [ ] RMI Activation 使用检查
- [ ] Security Manager 依赖检查
- [ ] 内部 API 反射访问检查
- [ ] 序列化兼容性测试
- [ ] TLS 连接测试
- [ ] 本地库 (JNI) 兼容性

**推荐测试的项目**:
- [ ] 性能基准测试
- [ ] 内存使用模式测试
- [ ] 启动时间测试
- [ ] 模块化兼容性测试

### 诊断工具使用

1. **使用 jdeps 分析**:
```bash
# 分析模块依赖
jdeps --multi-release 17 --ignore-missing-deps app.jar

# 检查内部 API 使用
jdeps -jdkinternals app.jar

# 生成模块化建议
jdeps --generate-module-info . app.jar
```

2. **使用 jdeprscan 扫描**:
```bash
# 扫描废弃 API
jdeprscan --release 17 --for-removal app.jar

# 扫描所有废弃 API
jdeprscan --release 17 app.jar
```

3. **使用 jlink 创建自定义运行时**:
```bash
# 验证模块化
jlink --module-path $JAVA_HOME/jmods:mods \
      --add-modules java.base,java.sql,java.xml \
      --output custom-jre
```

### 逐步迁移策略

**阶段 1: 评估和准备** (1-2 周)
- 环境兼容性验证
- 依赖库分析
- 风险评估

**阶段 2: 代码迁移** (2-4 周)
- 废弃 API 替换
- 模块化调整
- 测试环境部署

**阶段 3: 测试验证** (2-3 周)
- 全面测试套件执行
- 性能基准测试
- 安全测试

**阶段 4: 生产部署** (1-2 周)
- 金丝雀部署
- 监控和告警配置
- 回滚计划执行

---

## 紧急修复方案

### 遇到模块访问错误

```bash
# 临时解决方案: 开放所有必要包
java --add-opens java.base/jdk.internal.misc=ALL-UNNAMED \
     --add-opens java.base/sun.nio.ch=ALL-UNNAMED \
     --add-opens java.base/java.lang=ALL-UNNAMED \
     --add-opens java.base/java.lang.reflect=ALL-UNNAMED \
     --add-opens java.base/java.lang.invoke=ALL-UNNAMED \
     --add-opens java.base/java.util=ALL-UNNAMED \
     --add-opens java.desktop/sun.awt=ALL-UNNAMED \
     -jar app.jar
```

### 遇到序列化错误

```java
// 配置宽松的反序列化过滤器 (仅测试)
ObjectInputFilter.Config.setSerialFilter(
    ObjectInputFilter.allowFilter(cl -> true, ObjectInputFilter.Status.UNDECIDED)
);
```

### 遇到 TLS 连接失败

```bash
# 临时启用旧协议 (仅测试)
java -Djdk.tls.client.protocols=TLSv1,TLSv1.1,TLSv1.2,TLSv1.3 \
     -Djdk.tls.server.protocols=TLSv1,TLSv1.1,TLSv1.2,TLSv1.3 \
     -jar app.jar
```

### 遇到启动参数错误

```bash
# 忽略无法识别的参数
java -XX:+IgnoreUnrecognizedVMOptions \
     -jar app.jar
```

---

## 资源和文档

### 官方迁移指南
- [JDK 17 迁移指南](https://docs.oracle.com/en/java/javase/17/migrate/)
- [从 JDK 11 迁移到 JDK 17](https://docs.oracle.com/en/java/javase/17/migrate/migrating-from-previous-releases.html)

### 兼容性工具
- [Java Compatibility Kit (JCK)](https://openjdk.org/groups/conformance/)
- [JTReg 测试框架](https://openjdk.org/jtreg/)

### 社区资源
- [OpenJDK 迁移讨论](https://mail.openjdk.org/mailman/listinfo/migration-dev)
- [Stack Overflow: java-17-migration](https://stackoverflow.com/questions/tagged/java-17+migration)
- [Java User Groups](https://community.oracle.com/community/developer/)

### 商业支持选项
- **Oracle Java SE Subscription**: 官方支持
- **Red Hat OpenJDK Support**: 企业支持
- **Azul Prime Support**: 性能优化支持
- **Amazon Corretto**: 长期免费支持