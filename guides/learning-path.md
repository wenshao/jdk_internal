# Java / JDK 学习路径

> 按角色定制的学习路线：后端工程师、性能工程师、安全工程师、框架开发者、JDK 贡献者。

---
## 目录

1. [后端工程师 (Backend Engineer)](#1-后端工程师-backend-engineer)
2. [性能工程师 (Performance Engineer)](#2-性能工程师-performance-engineer)
3. [安全工程师 (Security Engineer)](#3-安全工程师-security-engineer)
4. [框架开发者 (Framework Developer)](#4-框架开发者-framework-developer)
5. [JDK 贡献者 (JDK Contributor)](#5-jdk-贡献者-jdk-contributor)
6. [学习时间估算](#6-学习时间估算)
7. [通用资源](#7-通用资源)

---


## 1. 后端工程师 (Backend Engineer)

> 目标: 用好 JDK 21-26 的新特性，写出更简洁、高效、可维护的代码。

### 阶段 1: 虚拟线程 (Virtual Threads) — 2 小时

**为什么先学这个**: 这是 Java 并发编程近 20 年来最大的变革，直接影响你的日常编码方式。

```
核心知识
├── 虚拟线程 vs 平台线程的区别
├── Executors.newVirtualThreadPerTaskExecutor()
├── Thread.ofVirtual().start()
└── 什么时候不该用虚拟线程 (CPU 密集型、synchronized 代码块)
```

关键代码：
```java
// JDK 21+ — 每个请求一个虚拟线程
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (var task : tasks) {
        executor.submit(() -> handleRequest(task));  // 百万级并发
    }
}

// Spring Boot 3.2+ 一行配置
// application.properties:
// spring.threads.virtual.enabled=true
```

**实践**: 将一个现有的线程池改为虚拟线程，观察吞吐量和线程数变化。

### 阶段 2: 结构化并发 (Structured Concurrency) — 2 小时

**前置**: 虚拟线程

```
核心知识
├── StructuredTaskScope 基本用法
├── ShutdownOnFailure (任一失败全部取消)
├── ShutdownOnSuccess (任一成功全部取消)
├── 自定义 Joiner 策略
└── 与 CompletableFuture 的对比
```

关键代码：
```java
// JDK 26 Preview — 聚合多个 API 调用
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Subtask<User> user = scope.fork(() -> fetchUser(id));
    Subtask<List<Order>> orders = scope.fork(() -> fetchOrders(id));

    scope.join();           // 等待所有子任务
    scope.throwIfFailed();  // 如果有失败则抛出异常

    return new UserProfile(user.get(), orders.get());
}
// 优势: 任何子任务失败 → 自动取消其他子任务 → 无泄漏
```

### 阶段 3: 模式匹配 (Pattern Matching) — 2 小时

```
演进路线
├── instanceof 模式匹配 (JDK 16, final)
├── switch 模式匹配 (JDK 21, final)
├── Record Patterns (JDK 21, final)
├── 解构 (Deconstruction) — sealed class + record
└── 原始类型模式 (JDK 26, preview)
```

关键代码：
```java
// JDK 21 — switch 模式匹配 + Record Patterns
sealed interface Shape permits Circle, Rectangle {}
record Circle(double radius) implements Shape {}
record Rectangle(double width, double height) implements Shape {}

double area(Shape shape) {
    return switch (shape) {
        case Circle(var r) -> Math.PI * r * r;
        case Rectangle(var w, var h) -> w * h;
    };
    // 编译器确保穷尽性 (exhaustiveness) — sealed 保证
}

// JDK 21 — 守卫模式 (guarded pattern)
String classify(Object obj) {
    return switch (obj) {
        case Integer i when i > 0 -> "positive int";
        case Integer i -> "non-positive int";
        case String s when s.isEmpty() -> "empty string";
        case String s -> "string: " + s;
        case null -> "null";
        default -> "other";
    };
}
```

### 阶段 4: Records 与数据建模 — 1 小时

```
核心知识
├── Record 基本语法
├── 紧凑构造器 (Compact Constructor)
├── Record 与 sealed interface 结合
├── Record 作为 DTO / 值对象
└── Record 的限制 (不可继承、字段不可变)
```

关键代码：
```java
// 紧凑构造器 — 参数校验
record Email(String address) {
    Email {
        if (!address.contains("@"))
            throw new IllegalArgumentException("Invalid email: " + address);
        address = address.toLowerCase().strip();  // 规范化
    }
}

// 作为不可变 DTO
record ApiResponse<T>(int code, String message, T data) {
    static <T> ApiResponse<T> ok(T data) {
        return new ApiResponse<>(200, "OK", data);
    }
    static <T> ApiResponse<T> error(int code, String msg) {
        return new ApiResponse<>(code, msg, null);
    }
}
```

### 阶段 5: Scoped Values 与上下文传递 — 1 小时

```
核心知识
├── ScopedValue vs ThreadLocal
├── ScopedValue.where().run() / .call()
├── 虚拟线程中的自动继承
└── 与 Structured Concurrency 结合
```

关键代码：
```java
// JDK 25+ — 替代 ThreadLocal 的上下文传递
private static final ScopedValue<RequestContext> CTX = ScopedValue.newInstance();

void handleRequest(HttpRequest request) {
    var ctx = new RequestContext(request.headers(), Instant.now());
    ScopedValue.where(CTX, ctx).run(() -> {
        processBusinessLogic();  // 整个调用链都能读取 CTX
    });
    // 离开 run() 后 CTX 自动清除 — 无内存泄漏
}
```

### 阶段 6: 进阶 — 各 1 小时

- **HTTP/3 客户端** (JEP 517): `HttpClient.Version.HTTP_3_AUTO`
- **StableValue** (JEP 502): 替代 double-checked locking 的延迟初始化
- **Module Import** (JEP 511): `import module java.base;`
- **Text Blocks** (JDK 15) / **String Templates** 趋势

---

## 2. 性能工程师 (Performance Engineer)

> 目标: 深入理解 JVM 运行时行为，能调优 GC、JIT、启动时间。

### 阶段 1: GC 选择与调优 — 3 小时

```
GC 选择决策
├── G1 GC (默认) — 通用 Web 服务
│   ├── 关键参数: -XX:MaxGCPauseMillis, -XX:G1HeapRegionSize
│   └── JDK 26: Claim Table 优化 (JEP 522, 吞吐量 +10-15%)
│
├── ZGC — 低延迟在线服务 (< 1ms 暂停)
│   ├── -XX:+UseZGC -XX:+ZGenerational (JDK 21+)
│   └── 支持 8MB-16TB 堆
│
├── Shenandoah — 低延迟 + 吞吐兼顾
│   ├── -XX:+UseShenandoahGC
│   └── JDK 26: 分代模式 (JEP 521, -XX:ShenandoahGCMode=generational)
│
├── Parallel GC — 批处理高吞吐
│   └── -XX:+UseParallelGC
│
└── Serial / Epsilon — 小堆或特殊场景
```

实操：
```bash
# 对比不同 GC 的效果
java -XX:+UseG1GC -Xlog:gc*:file=g1.log -jar app.jar
java -XX:+UseZGC -XX:+ZGenerational -Xlog:gc*:file=zgc.log -jar app.jar

# 分析 GC 日志
# 工具: GCViewer, GCEasy.io, JDK Mission Control
```

### 阶段 2: JIT 编译器 — 2 小时

```
核心知识
├── C1 (Client) vs C2 (Server) 编译器
├── 分层编译 (Tiered Compilation): 解释 → C1 → C2
├── 热点检测 (Hot Spot Detection): -XX:CompileThreshold
├── 内联 (Inlining): -XX:MaxInlineSize, -XX:FreqInlineSize
├── 逃逸分析 (Escape Analysis): 标量替换、栈上分配
└── Graal JIT (实验性): -XX:+UseJVMCICompiler
```

实操：
```bash
# 查看 JIT 编译日志
java -XX:+PrintCompilation -jar app.jar

# 详细 JIT 信息
java -XX:+UnlockDiagnosticVMOptions -XX:+LogCompilation \
     -XX:LogFile=jit.log -jar app.jar

# 工具: JITWatch (可视化 JIT 日志)
```

### 阶段 3: AOT 与启动优化 — 2 小时

```
优化手段 (由易到难)
├── CDS (Class Data Sharing) — 默认开启
│   └── 自定义 CDS: java -XX:SharedArchiveFile=app.jsa
│
├── AOT 缓存 (JDK 26, JEP 514/515)
│   ├── 训练: java -XX:AOTCacheOutput=app.aot -jar app.jar
│   ├── 使用: java -XX:AOTCache=app.aot -jar app.jar
│   └── 效果: 启动快 30-50%，含方法级 profiling 数据
│
├── GraalVM Native Image
│   ├── native-image -jar app.jar
│   └── 启动快 50-100x，但峰值吞吐可能下降 10-30%
│
└── CRaC (Coordinated Restore at Checkpoint)
    └── 毫秒级启动，需要 Azul Zulu / Liberica JDK
```

### 阶段 4: JFR (Java Flight Recorder) — 2 小时

```
核心知识
├── JFR 基本用法
│   ├── 启动时: -XX:StartFlightRecording=settings=profile,filename=app.jfr
│   └── 运行中: jcmd <pid> JFR.start
│
├── JDK 26 新事件
│   ├── JEP 509: CPU-Time Profiling (精准 CPU 时间)
│   ├── JEP 518: Cooperative Sampling (低开销采样)
│   └── JEP 520: Method Timing (方法耗时追踪)
│
└── 分析工具
    ├── JDK Mission Control (JMC) — 官方 GUI
    ├── async-profiler — 结合 JFR 输出
    └── IntelliJ Profiler — IDE 集成
```

### 阶段 5: 火焰图 (Flame Graphs) — 1 小时

```bash
# 使用 async-profiler
./asprof -d 30 -f flamegraph.html <pid>

# 使用 JFR + JMC
jcmd <pid> JFR.start duration=30s filename=profile.jfr
# 在 JMC 中打开 → Method Profiling → 自动生成火焰图

# CPU 火焰图 vs 分配火焰图 vs 锁火焰图
./asprof -e cpu -d 30 -f cpu.html <pid>      # CPU
./asprof -e alloc -d 30 -f alloc.html <pid>  # 内存分配
./asprof -e lock -d 30 -f lock.html <pid>    # 锁竞争
```

### 阶段 6: 内存分析 — 1 小时

```
工具链
├── jmap -histo <pid>              # 快速查看对象统计
├── jmap -dump:format=b,file=heap.hprof <pid>  # 堆转储
├── Eclipse MAT                     # 堆分析 (支持 OQL)
├── VisualVM                        # 轻量 GUI
└── JFR 内存事件                    # 持续监控分配热点
```

JDK 26 紧凑对象头 (JEP 519) 对内存分析的影响：
- 对象头从 12-16 bytes 压缩到 8 bytes
- 小对象密集的应用堆占用减少 10-20%
- `jmap -histo` 输出的 shallow size 会更小

---

## 3. 安全工程师 (Security Engineer)

> 目标: 掌握 Java 平台安全机制的演进，应用现代安全实践。

### 阶段 1: TLS 1.3 与 HTTPS — 2 小时

```
核心知识
├── TLS 1.3 vs 1.2 (握手、加密套件、前向保密)
├── JDK 11+ 默认支持 TLS 1.3
├── 证书管理 (keytool, PKCS#12)
├── 配置最佳实践
│   ├── 禁用 TLS 1.0/1.1
│   ├── 使用强加密套件
│   └── OCSP Stapling
└── HttpClient (JDK 11+) 的 TLS 配置
```

```java
// TLS 1.3 + HttpClient
SSLContext sslContext = SSLContext.getInstance("TLSv1.3");
sslContext.init(null, null, null);

HttpClient client = HttpClient.newBuilder()
    .sslContext(sslContext)
    .build();
```

```properties
# java.security — 推荐配置
jdk.tls.disabledAlgorithms=SSLv3, TLSv1, TLSv1.1, RC4, DES, MD5withRSA, \
    DH keySize < 2048, EC keySize < 224
```

### 阶段 2: 后量子密码 (Post-Quantum Cryptography) — 2 小时

```
核心知识
├── 为什么需要 PQC (量子计算威胁)
├── NIST PQC 标准: ML-KEM, ML-DSA, SLH-DSA
├── JDK 实现时间线
│   ├── JDK 24: ML-KEM (密钥封装)
│   ├── JDK 25: ML-DSA (数字签名)
│   └── JDK 26+: TLS 混合模式
├── "先收集后解密" (harvest-now-decrypt-later) 风险
└── 迁移策略: 经典 + PQC 混合模式
```

```java
// JDK 24+ ML-KEM
KeyPairGenerator kpg = KeyPairGenerator.getInstance("ML-KEM");
kpg.initialize(NamedParameterSpec.ML_KEM_768);
KeyPair kp = kpg.generateKeyPair();

// KEM 封装
KEM kem = KEM.getInstance("ML-KEM");
KEM.Encapsulator enc = kem.newEncapsulator(kp.getPublic());
KEM.Encapsulated encapsulated = enc.encapsulate();
SecretKey sharedSecret = encapsulated.key();
byte[] ciphertext = encapsulated.encapsulation();
```

### 阶段 3: 序列化安全 — 1.5 小时

```
核心知识
├── Java 反序列化漏洞历史 (RCE 攻击链)
├── 序列化过滤器 (JDK 9+)
│   ├── 全局过滤器: jdk.serialFilter
│   ├── 流级别过滤器: ObjectInputFilter
│   └── 过滤器工厂 (JDK 17+)
├── 替代方案: JSON, Protocol Buffers, Record Serialization
└── 序列化移除路线图 (长期目标)
```

```java
// 全局序列化过滤器
ObjectInputFilter.Config.setSerialFilter(
    ObjectInputFilter.Config.createFilter(
        "com.myapp.**;java.util.**;!*"  // 白名单模式
    )
);

// 自定义过滤器工厂 (JDK 17+)
ObjectInputFilter.Config.setSerialFilterFactory((current, next) -> {
    // 合并过滤器逻辑
    return ObjectInputFilter.merge(next, current);
});
```

### 阶段 4: Security Manager 迁移 — 1.5 小时

```
迁移路径
├── 识别 Security Manager 使用点
│   └── grep -r "SecurityManager\|System.setSecurityManager\|checkPermission" src/
│
├── 替代方案映射
│   ├── 文件/网络限制 → OS/容器级沙箱
│   ├── 代码权限 → JPMS exports/opens
│   ├── 类加载控制 → 自定义 ClassLoader
│   └── 审计日志 → JFR 安全事件
│
└── 迁移验证
    └── JDK 24+ 启动时 SecurityManager 相关代码直接抛异常
```

### 阶段 5: KDF 与密码学 API — 1 小时

```
JDK 26 新 API
├── KDF API (JEP 510): 标准化密钥派生
├── PEM Encodings (JEP 470): PEM 格式编解码
└── 最佳实践
    ├── 密钥存储: KeyStore (PKCS#12)
    ├── 密码哈希: Argon2 (第三方) 或 PBKDF2
    └── 随机数: SecureRandom (默认即可)
```

---

## 4. 框架开发者 (Framework Developer)

> 目标: 理解 JDK 底层机制变化，为框架 (Spring, Quarkus, Micronaut 等) 适配新 JDK。

### 阶段 1: MethodHandle 与反射机制 — 3 小时

```
核心知识
├── java.lang.reflect → java.lang.invoke 迁移
│   ├── MethodHandle: 比反射更快的方法调用
│   ├── VarHandle: 替代 sun.misc.Unsafe 的字段操作
│   └── MethodHandles.Lookup: 访问控制
│
├── 反射访问限制演进
│   ├── JDK 16: --illegal-access=deny 默认
│   ├── JDK 17: 移除 --illegal-access
│   └── JDK 26: final 字段反射修改受限 (JEP 500)
│
└── 性能对比
    ├── 反射调用: ~100ns (有缓存)
    ├── MethodHandle: ~10ns (内联后接近直接调用)
    └── 直接调用: ~1ns
```

```java
// MethodHandle 示例
MethodHandles.Lookup lookup = MethodHandles.lookup();
MethodHandle mh = lookup.findVirtual(String.class, "length",
    MethodType.methodType(int.class));
int len = (int) mh.invoke("hello");  // 5

// VarHandle 示例 (替代 Unsafe)
VarHandle vh = MethodHandles.lookup().findVarHandle(
    MyClass.class, "counter", int.class);
vh.compareAndSet(obj, 0, 1);  // CAS 操作
```

### 阶段 2: JPMS 对框架的影响 — 2 小时

```
关键问题
├── 框架如何处理模块封装
│   ├── opens 指令 — 最佳方案
│   ├── --add-opens — 过渡方案
│   └── MethodHandles.privateLookupIn() — 合法的深度反射
│
├── ServiceLoader 与模块
│   └── provides/uses 声明
│
├── 动态代理与模块
│   ├── JDK Proxy: 接口必须可访问
│   └── CGLIB/ByteBuddy: 需要 opens
│
└── 注解处理 (Annotation Processing)
    └── 在模块系统中的变化
```

### 阶段 3: Class-File API (JDK 24+ Preview) — 2 小时

```
核心知识
├── 替代 ASM/BCEL/Javassist 的标准 API
├── ClassFile.of() 读取/生成/转换字节码
├── 与 JDK 版本同步演进 (不再有 ASM 版本滞后问题)
└── MethodHandle + ClassFile API = 完整的运行时代码生成
```

```java
// 使用 Class-File API 生成类 (JDK 24+)
byte[] bytes = ClassFile.of().build(
    ClassDesc.of("com.example", "Generated"),
    cb -> cb.withMethod("hello",
        MethodTypeDesc.of(CD_String),
        ClassFile.ACC_PUBLIC | ClassFile.ACC_STATIC,
        mb -> mb.withCode(code -> code
            .ldc("Hello from generated code!")
            .areturn()
        )
    )
);
```

### 阶段 4: Hidden Classes — 1 小时

```
核心知识
├── 替代 Unsafe.defineAnonymousClass (已移除)
├── MethodHandles.Lookup.defineHiddenClass()
├── 不可被名称发现，GC 可独立回收
├── 典型用途: Lambda 实现, 动态代理, 模板引擎
└── JDK 26: ClassFile API + Hidden Classes = 标准化动态代码生成
```

### 阶段 5: Foreign Function & Memory API (Panama) — 2 小时

```
核心知识 (JDK 22 Final)
├── 替代 JNI 的标准化本地交互
├── MemorySegment: 安全的堆外内存
├── FunctionDescriptor + Linker: 调用 C 函数
├── jextract: 自动从 .h 文件生成 Java 绑定
└── Arena: 内存生命周期管理
```

```java
// 调用 C strlen 函数
Linker linker = Linker.nativeLinker();
SymbolLookup stdlib = linker.defaultLookup();

MethodHandle strlen = linker.downcallHandle(
    stdlib.find("strlen").orElseThrow(),
    FunctionDescriptor.of(JAVA_LONG, ADDRESS)
);

try (Arena arena = Arena.ofConfined()) {
    MemorySegment str = arena.allocateFrom("Hello");
    long len = (long) strlen.invoke(str);  // 5
}
```

---

## 5. JDK 贡献者 (JDK Contributor)

> 目标: 理解 OpenJDK 源码结构，能构建、测试、提交补丁。

### 阶段 1: 源码结构 — 1 小时

```
OpenJDK 仓库布局 (https://github.com/openjdk/jdk)
├── src/
│   ├── java.base/              # 基础模块
│   │   ├── share/classes/      # 平台无关 Java 代码
│   │   ├── share/native/       # 平台无关 C/C++ 代码
│   │   ├── linux/              # Linux 特定
│   │   ├── macosx/             # macOS 特定
│   │   └── windows/            # Windows 特定
│   ├── java.sql/               # JDBC 模块
│   ├── jdk.compiler/           # javac
│   ├── jdk.internal.vm.ci/     # JIT 编译器接口
│   └── hotspot/                # HotSpot VM
│       ├── share/              # 平台无关 C++ 代码
│       │   ├── gc/             # GC 实现 (g1, zgc, shenandoah...)
│       │   ├── oops/           # 对象系统
│       │   ├── runtime/        # 运行时
│       │   └── compiler/       # JIT
│       ├── cpu/                # CPU 特定 (x86, aarch64, riscv)
│       └── os/                 # OS 特定
├── test/                       # 测试
│   ├── jdk/                    # API 测试
│   ├── hotspot/                # VM 测试
│   └── langtools/              # 编译器测试
├── make/                       # 构建系统
└── doc/                        # 文档
```

### 阶段 2: 构建 OpenJDK — 2 小时

```bash
# 1. 获取源码
git clone https://github.com/openjdk/jdk.git
cd jdk

# 2. 安装 Boot JDK (需要 N-1 版本)
# 构建 JDK 26 需要 JDK 25 作为 Boot JDK
sdk install java 25-open

# 3. 安装构建依赖
# Ubuntu/Debian:
sudo apt install build-essential autoconf zip unzip \
  libx11-dev libxext-dev libxrender-dev libxrandr-dev \
  libxtst-dev libxt-dev libcups2-dev libfontconfig1-dev \
  libasound2-dev

# macOS:
xcode-select --install
brew install autoconf

# 4. 配置
bash configure --with-boot-jdk=$JAVA_HOME

# 5. 构建
make images    # 完整构建 (~10-30 分钟)
make hotspot   # 仅构建 HotSpot (更快)

# 6. 验证
./build/*/images/jdk/bin/java -version
```

### 阶段 3: 测试 — 1 小时

```bash
# 运行特定测试
make test TEST="jdk/java/lang/String"

# 运行 tier1 测试 (快速验证)
make test-tier1

# 运行 JTReg 测试
make test TEST="test/jdk/java/util/concurrent"

# 运行 GTest (C++ 单元测试)
make test TEST="gtest:all"
```

### 阶段 4: 提交流程 — 1 小时

```
OpenJDK 贡献流程
├── 1. 签署 OCA (Oracle Contributor Agreement)
│      https://oca.opensource.oracle.com/
│
├── 2. 创建 JBS Issue (bugs.openjdk.org)
│      描述 bug 或增强请求
│
├── 3. Fork + 开发
│      ├── fork openjdk/jdk 到你的 GitHub
│      ├── 创建分支: git checkout -b JDK-XXXXXXX
│      ├── 编码 + 测试
│      └── 每个 commit message 以 JBS ID 开头
│
├── 4. 创建 Pull Request
│      ├── PR 标题: "JDK-XXXXXXX: 简短描述"
│      ├── Skara bot 自动分配 reviewer
│      └── 需要至少 1 个 Reviewer 批准
│
├── 5. Review 与合并
│      ├── 回应 review 意见
│      ├── 通过所有 CI 测试
│      └── Reviewer 输入 /integrate 合并
│
└── 工具: Skara CLI (git-pr, git-jcheck, git-webrev)
```

### 阶段 5: 深入特定领域 — 持续学习

```
选择一个方向深入
├── 语言 / 编译器 → src/jdk.compiler (javac)
│   └── 推荐: 关注 Project Amber mailing list
│
├── GC → src/hotspot/share/gc/
│   └── 推荐: 阅读 GC 相关 JEP 的实现代码
│
├── 并发 → src/java.base/share/classes/java/util/concurrent/
│   └── 推荐: 阅读 Doug Lea 的代码和论文
│
├── 安全 → src/java.base/share/classes/java/security/
│   └── 推荐: 关注 security-dev mailing list
│
└── 性能 → src/hotspot/share/compiler/ + share/opto/
    └── 推荐: 阅读 C2 IR 和优化 pass
```

---

## 6. 学习时间估算

| 角色 | 阶段数 | 预计总时间 | 建议节奏 |
|------|--------|-----------|---------|
| 后端工程师 | 6 | 9-12 小时 | 每天 1-2 小时，1 周完成 |
| 性能工程师 | 6 | 11-14 小时 | 每天 2 小时，1 周完成 |
| 安全工程师 | 5 | 8-10 小时 | 每天 2 小时，5 天完成 |
| 框架开发者 | 5 | 10-12 小时 | 每天 2 小时，1 周完成 |
| JDK 贡献者 | 5 | 6+ 小时 (入门) | 构建环境搭好后持续学习 |

---

## 7. 通用资源

### 官方资源

- [OpenJDK 官网](https://openjdk.org/) — JEP、项目、邮件列表
- [Inside.java](https://inside.java/) — Oracle Java 团队博客
- [Java YouTube 频道](https://www.youtube.com/@java) — 官方视频
- [Dev.java](https://dev.java/) — 官方开发者门户

### 社区资源

- [Baeldung](https://www.baeldung.com/) — Java 教程 (英文)
- [InfoQ Java](https://www.infoq.com/java/) — 技术新闻
- [r/java](https://www.reddit.com/r/java/) — Reddit Java 社区
- [CNCF TAG-Runtime](https://github.com/cncf/tag-runtime) — 云原生 Java

### 书籍推荐

- **Effective Java** (Joshua Bloch) — Java 最佳实践圣经
- **Java Concurrency in Practice** (Brian Goetz) — 并发编程经典
- **Optimizing Java** (Ben Evans) — JVM 性能调优
- **The Well-Grounded Java Developer** — 现代 Java 全景

### 本项目其他指南

- [FAQ](faq.md) — 常见问题
- [速查表](cheat-sheet.md) — JVM 参数与 API 快速参考
- [迁移指南](migration-guide.md) — JDK 版本升级详细步骤
- [模块系统指南](modules.md) — JPMS 实用指南
- [发行版对比](jdk-distributions.md) — 主流发行版详细对比
