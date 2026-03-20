# JDK 21 破坏性变更

> **影响评估**: 中高 | **主要风险**: Virtual Threads 兼容性, 安全策略变更, 平台支持调整

---

## Virtual Threads 相关变更

### 1. 线程模型根本性变化

**变更**: 引入 Virtual Threads (JEP 444) 作为正式特性，改变 Java 并发编程基础模型。

**影响代码**:
- 假设线程是操作系统线程的代码
- 依赖 `Thread` 特定行为的代码
- 使用 `ThreadLocal` 的高性能场景

**具体问题**:

1. **线程 ID 重用加速**:
```java
// Virtual Threads 的线程 ID 可能快速重用
Thread virtualThread = Thread.ofVirtual().start(() -> {
    System.out.println(Thread.currentThread().getId());  // ID 可能很小且重用
});

// 传统假设: 线程 ID 唯一且稳定
// Virtual Threads: ID 可能快速回收和重用
```

2. **线程优先级行为变化**:
```java
// Virtual Threads 忽略线程优先级
Thread virtualThread = Thread.ofVirtual()
    .priority(Thread.MAX_PRIORITY)  // 被忽略
    .start(task);

// 传统线程: 优先级影响调度
// Virtual Threads: 优先级被忽略，所有虚拟线程平等
```

3. **ThreadGroup 变化**:
```java
// Virtual Threads 属于特殊线程组
Thread virtualThread = Thread.ofVirtual().start(task);
System.out.println(virtualThread.getThreadGroup());  // "VirtualThreads"

// 影响: 基于 ThreadGroup 的管理工具可能需要调整
```

**解决方案**:
```java
// 检测是否在虚拟线程中运行
if (Thread.currentThread().isVirtual()) {
    // 虚拟线程特定逻辑
    // 避免依赖传统线程特性
}

// 关键操作迁移到平台线程
if (Thread.currentThread().isVirtual()) {
    Future<?> future = platformThreadExecutor.submit(() -> {
        // 在平台线程执行关键操作
        performCriticalOperation();
    });
    future.get();
}
```

### 2. ThreadLocal 性能影响

**变更**: `ThreadLocal` 在 Virtual Threads 上性能较差，可能引起线程固定。

**症状**:
- Virtual Threads 被固定到平台线程
- 并发性能下降
- 内存使用增加

**诊断**:
```bash
# 启用诊断日志
-Djdk.traceVirtualThreadLocals=true

# 查看线程固定警告
# 日志显示: "Pinned carrier thread due to ThreadLocal"
```

**解决方案**:
1. **减少 ThreadLocal 使用**:
```java
// 使用局部变量替代
public void process() {
    Context context = createContext();  // 局部变量
    // 而不是 ThreadLocal.set(context)
}

// 使用参数传递
void helper(Context context) { ... }
```

2. **使用 ScopedValue (预览) 替代**:
```java
private static final ScopedValue<Context> CURRENT_CONTEXT = ScopedValue.newInstance();

ScopedValue.where(CURRENT_CONTEXT, context).run(() -> {
    // 在此作用域内可访问
    processRequest();
});
```

3. **批量处理避免频繁 ThreadLocal 访问**:
```java
// 差: 每次操作都访问 ThreadLocal
for (Item item : items) {
    Context context = threadLocal.get();
    process(item, context);
}

// 好: 一次获取，多次使用
Context context = threadLocal.get();
for (Item item : items) {
    process(item, context);
}
```

### 3. synchronized 阻塞载体线程

**变更**: `synchronized` 在 Virtual Threads 上会阻塞载体线程。

**影响**: 降低 Virtual Threads 的并发优势。

**示例**:
```java
// 问题代码
public class Counter {
    private int count;
    
    public synchronized void increment() {
        count++;
        Thread.sleep(10);  // I/O 操作，阻塞载体线程!
    }
}

// 使用 Virtual Threads 时
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 1000; i++) {
        executor.submit(() -> {
            counter.increment();  // 会固定虚拟线程!
        });
    }
}
```

**解决方案**:
1. **使用 ReentrantLock**:
```java
public class Counter {
    private int count;
    private final Lock lock = new ReentrantLock();
    
    public void increment() {
        lock.lock();
        try {
            count++;
            Thread.sleep(10);  // 不会阻塞载体线程
        } finally {
            lock.unlock();
        }
    }
}
```

2. **避免在 synchronized 块内进行 I/O**:
```java
public void process() {
    Data data;
    synchronized (this) {
        data = getData();  // 快速操作
    }
    // I/O 操作放在同步块外
    processData(data);  // 可能包含 I/O
}
```

---

## 安全策略变更

### 4. 准备禁止动态加载代理 (JEP 451)

**变更**: 默认禁止运行时动态加载 Java 代理。

**影响**:
- 使用 `VirtualMachine.loadAgent` 的代码失效
- 某些监控/APM 工具受影响
- 动态字节码增强框架受影响

**错误信息**:
```bash
java.lang.UnsupportedOperationException: Dynamic loading of agents is disabled
    at jdk.internal.loader.ClassLoaders.checkAgentLoading(ClassLoaders.java:300)
```

**解决方案**:

1. **使用命令行参数加载代理**:
```bash
# 之前: 运行时动态加载
# 之后: 启动时加载
java -javaagent:agent.jar -jar app.jar
```

2. **启用动态加载 (不推荐生产)**:
```bash
# 临时启用
-Djdk.instrument.allowDynamicLoading=true

# 或记录使用情况
-Djdk.instrument.traceUsage=true
```

3. **修改应用代码**:
```java
// 之前: 运行时加载
VirtualMachine vm = VirtualMachine.attach(pid);
vm.loadAgent(agentPath, options);

// 之后: 修改为启动时加载或使用替代方案
// 考虑使用 Java Flight Recorder (JFR) 替代部分监控功能
```

**受影响工具**:
- **监控工具**: 部分 APM 代理
- **性能分析工具**: 动态插桩工具
- **开发工具**: 热部署、调试工具

### 5. 更强的模块封装

**变更**: 模块系统封装进一步加强。

**影响**: 反射访问内部 API 更困难。

**错误示例**:
```java
// 尝试访问内部 API
Class<?> clazz = Class.forName("jdk.internal.misc.Unsafe");
Field field = clazz.getDeclaredField("theUnsafe");
field.setAccessible(true);  // 可能失败或需要更多权限
```

**解决方案**:
```bash
# 添加必要的 --add-opens 参数
java --add-opens java.base/jdk.internal.misc=ALL-UNNAMED \
     --add-opens java.base/sun.nio.ch=ALL-UNNAMED \
     --add-opens java.base/java.lang=ALL-UNNAMED \
     --add-opens java.base/java.lang.reflect=ALL-UNNAMED \
     --add-opens java.base/java.lang.invoke=ALL-UNNAMED \
     --add-opens java.base/java.util=ALL-UNNAMED \
     --add-opens java.management/sun.management=ALL-UNNAMED \
     -jar app.jar
```

**常见需要开放的包** (Virtual Threads 相关):
```bash
# Virtual Threads 需要
--add-opens java.base/jdk.internal.vm=ALL-UNNAMED
--add-opens java.base/java.lang=ALL-UNNAMED
--add-opens java.base/java.util.concurrent=ALL-UNNAMED
```

---

## API 废弃和移除

### 6. 废弃 Windows 32位 x86 端口 (JEP 449)

**变更**: Windows 32位版本标记为废弃。

**影响**:
- 32位 Windows 应用无法运行 JDK 21
- 需要 32位 JNI 库的应用受影响

**错误信息**:
```bash
# 尝试在 32位 Windows 运行 JDK 21
Error: This Java instance does not support a 32-bit JVM.
Please install the desired version.
```

**迁移路径**:

1. **应用迁移到 64位**:
```bash
# 重新编译为 64位
javac -target 1.8 -source 1.8 -d "bin64" src/*.java

# 更新构建脚本
# 从 32位目标改为 64位
```

2. **JNI 库迁移**:
```bash
# 重新编译本地库
# Visual Studio: 目标平台从 Win32 改为 x64
# GCC/MinGW: -m32 改为 -m64

# 验证库架构
dumpbin /headers library.dll | findstr "machine"
# 应该显示: 8664 machine (x64)
```

3. **第三方依赖检查**:
- 确保所有本地库提供 64位版本
- 更新安装程序支持 64位
- 测试 64位环境兼容性

### 7. 移除已废弃的 GC 组合

**变更**: 某些 GC 组合不再支持。

**不再支持的组合**:
```bash
# 已移除
-XX:+UseConcMarkSweepGC -XX:+UseParNewGC

# 替代方案
-XX:+UseG1GC  # 推荐
# 或
-XX:+UseZGC   # 低延迟需求
# 或  
-XX:+UseShenandoahGC
```

**错误信息**:
```bash
Error: Could not create the Java Virtual Machine.
Error: A fatal exception has occurred. Program will exit.
Unrecognized VM option 'UseConcMarkSweepGC'
```

**迁移指南**:
```bash
# CMS 用户迁移到 G1
# 之前
-XX:+UseConcMarkSweepGC -XX:+UseParNewGC -XX:CMSInitiatingOccupancyFraction=75

# 之后
-XX:+UseG1GC -XX:MaxGCPauseMillis=200 -XX:InitiatingHeapOccupancyPercent=45

# 低延迟需求迁移到 ZGC
-XX:+UseZGC -XX:MaxGCPauseMillis=10
```

---

## 行为变更

### 8. 默认 TLS 配置增强

**变更**: 更强的默认 TLS 配置。

**影响**:
- 连接旧服务器可能失败
- 弱密码套件被拒绝

**连接失败场景**:
```bash
# 连接只支持 TLS 1.0/弱密码的服务器
javax.net.ssl.SSLHandshakeException: No appropriate protocol

# 或
javax.net.ssl.SSLHandshakeException: Received fatal alert: handshake_failure
```

**解决方案**:

1. **服务器端升级** (推荐):
```bash
# 升级服务器支持 TLS 1.2+
# 使用现代密码套件
```

2. **客户端临时降级** (仅测试):
```bash
# 启用旧协议
-Djdk.tls.client.protocols=TLSv1,TLSv1.1,TLSv1.2,TLSv1.3

# 启用弱算法 (不推荐生产)
-Djdk.tls.disabledAlgorithms="SSLv3, RC4, DES, MD5withRSA, \
    DH keySize < 1024, EC keySize < 224"
# 注意: 移除不想禁用的算法
```

3. **代码中配置**:
```java
// 创建自定义 SSLContext
SSLContext sslContext = SSLContext.getInstance("TLS");
sslContext.init(null, trustManagers, null);

// 配置 SSLParameters
SSLParameters params = sslContext.getDefaultSSLParameters();
params.setProtocols(new String[] {"TLSv1.2", "TLSv1.3"});
params.setCipherSuites(new String[] {
    "TLS_AES_256_GCM_SHA384",
    "TLS_CHACHA20_POLY1305_SHA256",
    "TLS_AES_128_GCM_SHA256"
});

// 应用到连接
SSLSocketFactory factory = sslContext.getSocketFactory();
SSLSocket socket = (SSLSocket) factory.createSocket(host, port);
socket.setSSLParameters(params);
```

### 9. 序列化过滤器默认更严格

**变更**: 默认的反序列化过滤器更严格。

**影响**: 反序列化可能失败。

**错误信息**:
```java
java.io.InvalidClassException: filter status: REJECTED
    at java.base/java.io.ObjectInputStream.filterCheck(ObjectInputStream.java:1412)
```

**解决方案**:
```java
// 配置合适的过滤器
ObjectInputFilter filter = ObjectInputFilter.allowFilter(
    cl -> {
        if (cl == null) return ObjectInputFilter.Status.UNDECIDED;
        
        String name = cl.getName();
        // 允许应用类
        if (name.startsWith("com.example.")) {
            return ObjectInputFilter.Status.ALLOWED;
        }
        // 拒绝危险类
        if (name.startsWith("java.") || name.startsWith("sun.")) {
            return ObjectInputFilter.Status.REJECTED;
        }
        return ObjectInputFilter.Status.UNDECIDED;
    },
    ObjectInputFilter.Status.REJECTED
);

// 设置过滤器
ObjectInputStream ois = new ObjectInputStream(input);
ois.setObjectInputFilter(filter);
```

### 10. 时区数据更新

**变更**: 时区数据更新到最新版本。

**影响**: 历史日期时间处理可能变化。

**示例**:
```java
// 某些历史时区偏移可能变化
ZonedDateTime dateTime = ZonedDateTime.of(2010, 3, 28, 2, 30, 0, 0, 
    ZoneId.of("Europe/Paris"));

// 时区规则变化可能影响结果
```

**验证**:
```bash
# 检查时区数据版本
java -jar tzupdater.jar -v

# 更新时区数据 (如果需要)
java -jar tzupdater.jar -l https://www.iana.org/time-zones
```

---

## 第三方库兼容性问题

### 11. 常见库的 Virtual Threads 兼容性

| 库/框架 | 兼容性 | 最小版本 | 问题 |
|---------|--------|----------|------|
| **Netty** | ✅ 良好 | 4.1.90+ | 早期版本可能阻塞载体线程 |
| **gRPC** | ✅ 良好 | 1.49.0+ | 需要配置 |
| **Reactor** | ✅ 良好 | 3.5.0+ | 自动检测虚拟线程 |
| **Spring Framework** | ✅ 良好 | 6.1.0+ | 需要配置 |
| **HikariCP** | ⚠️ 需要配置 | 5.0.0+ | 连接池大小需要调整 |
| **Log4j 2** | ✅ 良好 | 2.20.0+ | 支持虚拟线程上下文 |
| **JUnit 5** | ✅ 良好 | 5.10.0+ | 测试在虚拟线程中运行 |

**不兼容库的症状**:
- Virtual Threads 被固定
- 性能没有提升
- 奇怪的并发问题

**诊断命令**:
```bash
# 检查线程固定
-Djdk.traceVirtualThreads=true
-Djdk.traceVirtualThreadLocals=true

# 查看日志中的 "pinned" 警告
```

### 12. 本地库 (JNI) 兼容性

**问题**: 本地库假设线程是操作系统线程。

**检查点**:
```c
// 有问题的 JNI 代码
JNIEXPORT void JNICALL Java_MyClass_doWork(JNIEnv *env, jobject obj) {
    // 假设当前线程是平台线程
    pthread_t thread = pthread_self();  // 可能不是期望的线程
    
    // 使用线程局部存储 (TLS)
    __thread int counter;  // 可能有问题
    
    // 调用阻塞系统调用
    sleep(1);  // 阻塞载体线程!
}
```

**解决方案**:
1. **避免在 JNI 中阻塞**:
```c
// 使用非阻塞 I/O
// 或快速返回，让虚拟线程挂起
```

2. **重新设计交互**:
```java
// 将耗时操作移到 Java 端
public void process() {
    // 快速 JNI 调用
    nativePreprocess();
    
    // I/O 在 Java 端进行
    data = readData();
    
    // 再次快速 JNI 调用
    nativePostprocess(data);
}
```

3. **使用平台线程执行本地代码**:
```java
if (Thread.currentThread().isVirtual()) {
    // 切换到平台线程执行 JNI 调用
    Future<?> future = platformThreadExecutor.submit(() -> {
        nativeMethod();
    });
    future.get();
} else {
    nativeMethod();
}
```

---

## 工具和命令行变更

### 13. 已移除的命令行工具

**已移除**:
- `javaws` (Java Web Start) - 从 JDK 9 开始逐步移除
- `pack200`/`unpack200` - 从 JDK 14 移除
- `java-rmi.cgi` - RMI 相关工具

**替代方案**:
```bash
# 应用分发使用 jpackage
jpackage --name MyApp --input lib --main-jar app.jar

# 或使用现代安装技术
```

### 14. 已废弃的 JVM 参数

**已废弃参数** (使用会警告):
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

**警告信息**:
```bash
OpenJDK 64-Bit Server VM warning: Option UseConcMarkSweepGC was deprecated in version 9.0 and will likely be removed in a future release.
```

### 15. 监控工具变更

**jmap 变更**:
```bash
# 某些选项已移除
jmap -permstat <pid>  # 已移除

# 使用替代命令
jcmd <pid> GC.heap_info
jcmd <pid> VM.native_memory summary

# 或使用更新的选项
jmap -clstats <pid>    # 类加载器统计
```

**jstat 变更**:
```bash
# PermGen 统计 → Metaspace 统计
jstat -gcpermcapacity <pid>  # 已废弃
jstat -gcmetacapacity <pid>  # 使用这个

# 新增 Virtual Threads 统计
jstat -gcutil <pid>  # 包含虚拟线程相关信息
```

---

## 平台特定变更

### 16. macOS 渲染管道

**变更**: Metal 渲染管道改进，OpenGL 支持减弱。

**影响**: AWT/Swing 应用渲染可能变化。

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

# 调试渲染问题
-Dsun.java2d.trace=log
```

### 17. Linux 容器支持增强

**变更**: 更好的容器资源检测。

**影响**: 自动资源检测可能变化。

**问题**: 在旧版本容器运行时中，资源检测可能不准确。

**解决方案**:
```bash
# 明确设置资源限制
-XX:ActiveProcessorCount=4
-XX:MaxRAMPercentage=75.0
-XX:InitialRAMPercentage=50.0

# 或禁用自动检测
-XX:-UseContainerSupport  # 不推荐，仅诊断用
```

### 18. Windows 安装程序变更

**变更**: 安装程序和注册表项变更。

**影响**:
- 自动 JRE 检测可能受影响
- 某些注册表路径变化

**验证**:
```powershell
# 检查注册表
Get-ItemProperty -Path "HKLM:\SOFTWARE\JavaSoft\JDK\21"

# 检查环境变量
$env:JAVA_HOME
java -version
```

---

## 迁移检查和验证

### 兼容性测试清单

**必须测试的项目**:
- [ ] Virtual Threads 兼容性测试
- [ ] synchronized 块内 I/O 操作检查
- [ ] ThreadLocal 使用审查
- [ ] JNI 代码兼容性验证
- [ ] 动态代理加载检查
- [ ] TLS 连接测试
- [ ] 序列化兼容性测试

**推荐测试的项目**:
- [ ] 性能基准测试 (Virtual Threads vs Platform Threads)
- [ ] 内存使用模式测试
- [ ] 第三方库兼容性验证
- [ ] 监控工具功能测试

### 诊断工具使用

1. **Virtual Threads 诊断**:
```bash
# 启用详细日志
-Djdk.traceVirtualThreads=true
-Djdk.traceVirtualThreadLocals=true
-Djdk.traceVirtualThreads.dump=virtual-threads.txt

# 监控线程状态
jcmd <pid> Thread.dump_to_file -format=json threads.json

# JFR 记录 Virtual Threads 事件
jcmd <pid> JFR.start duration=60s filename=vt-recording.jfr
```

2. **兼容性扫描**:
```bash
# 扫描已废弃 API
jdeprscan --release 21 --for-removal app.jar

# 分析依赖
jdeps --multi-release 21 --ignore-missing-deps app.jar

# 检查模块化问题
jdeps --check app.jar
```

3. **性能分析**:
```bash
# 使用 async-profiler
java -agentlib:asyncProfiler=start,event=cpu,file=profile.html -jar app.jar

# 或使用 JFR
java -XX:StartFlightRecording=duration=60s,filename=perf.jfr -jar app.jar
```

### 逐步迁移策略

**阶段 1: 评估** (1-2 周)
- 环境兼容性验证
- Virtual Threads 适用性分析
- 风险评估

**阶段 2: 代码适配** (2-4 周)
- 处理破坏性变更
- 调整 Virtual Threads 不兼容代码
- 更新第三方库

**阶段 3: 测试** (2-3 周)
- 单元测试适配
- 性能基准测试
- 并发测试强化
- 安全测试

**阶段 4: 部署** (1-2 周)
- 金丝雀部署
- 监控告警配置
- 回滚计划执行

---

## 紧急修复方案

### 遇到 Virtual Threads 问题

```bash
# 临时禁用 Virtual Threads
-Djdk.virtualThreads.enabled=false

# 或减少虚拟线程使用
-Djdk.virtualThreads.scheduler.maxPoolSize=64

# 诊断线程固定
-Djdk.traceVirtualThreads=true
```

### 遇到模块访问错误

```bash
# 开放必要的包
--add-opens java.base/jdk.internal.misc=ALL-UNNAMED \
--add-opens java.base/sun.nio.ch=ALL-UNNAMED \
--add-opens java.base/java.lang=ALL-UNNAMED \
--add-opens java.base/java.util.concurrent=ALL-UNNAMED \
--add-opens java.base/jdk.internal.vm=ALL-UNNAMED
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
     -jar app.jar
```

---

## 资源和文档

### 官方迁移指南
- [JDK 21 迁移指南](https://docs.oracle.com/en/java/javase/21/migrate/)
- [Virtual Threads 迁移指南](https://docs.oracle.com/en/java/javase/21/core/virtual-threads.html)
- [从 JDK 17 迁移到 JDK 21](https://docs.oracle.com/en/java/javase/21/migrate/migrating-from-jdk-17-to-jdk-21.html)

### 兼容性工具
- [Java Compatibility Kit (JCK)](https://openjdk.org/groups/conformance/)
- [JTReg 测试框架](https://openjdk.org/jtreg/)

### 社区资源
- [OpenJDK loom-dev 邮件列表](https://mail.openjdk.org/mailman/listinfo/loom-dev)
- [Stack Overflow: java-21-migration](https://stackoverflow.com/questions/tagged/java-21+migration)
- [Java User Groups](https://community.oracle.com/community/developer/)

### 商业支持选项
- **Oracle Java SE Subscription**: 官方支持
- **Red Hat OpenJDK Support**: 企业支持
- **Azul Prime Support**: Virtual Threads 性能优化支持
- **Amazon Corretto**: 长期免费支持