# JDK 26 迁移指南

本文档提供从旧版本 JDK 升级到 JDK 26 的完整指南。

---
## 目录

1. [升级前评估](#1-升级前评估)
2. [迁移场景](#2-迁移场景)
3. [升级步骤](#3-升级步骤)
4. [性能优化建议](#4-性能优化建议)
5. [常见问题](#5-常见问题)
6. [回滚计划](#6-回滚计划)
7. [检查清单](#7-检查清单)

---


## 1. 升级前评估

### 兼容性检查

```bash
# 1. 检查 Java 版本
java -version

# 2. 检查依赖的 JDK 内部 API
jdeps --jdk-internals myapp.jar

# 3. 检查已废弃 API
jdeprscan myapp.jar
```

### 风险评估矩阵

| 风险级别 | 场景 | 建议 |
|----------|------|------|
| 🟢 低 | 标准库使用，无内部 API | 直接升级 |
| 🟡 中 | 使用已废弃 API | 先迁移废弃 API |
| 🔴 高 | 依赖 32位 x86 或 Applet | 需要重构 |

---

## 2. 迁移场景

### 场景 1: 移除 32位 x86 支持 (JEP 503)

**影响**: 如果你的应用运行在 32位 x86 平台

**检查方法**:

```bash
# 检查当前架构
uname -m
# i686, i386 = 32位 (受影响)
# x86_64, aarch64 = 64位 (不受影响)

# 检查 JVM 架构
java -XshowSettings:properties -version 2>&1 | grep os.arch
```

**迁移方案**:

```bash
# 方案 1: 升级到 64位系统
# 推荐方案，获得更好性能

# 方案 2: 使用 JDK 25 或更早版本
# 临时方案，不推荐长期使用

# 方案 3: 迁移到 ARM 等其他架构
# 适用于嵌入式场景
```

---

### 场景 2: 移除 Applet API (JEP 504)

**影响**: 如果代码使用了 `java.applet` 包

**检查方法**:

```bash
# 搜索 Applet 相关代码
grep -r "import java.applet" src/
grep -r "extends Applet" src/
grep -r "extends JApplet" src/
grep -r "AppletContext" src/
```

**迁移方案**:

```java
// 旧代码
import java.applet.Applet;

public class MyApplet extends Applet {
    public void init() {
        add(new Label("Hello"));
    }
}

// 新代码: 独立应用
import javax.swing.*;

public class MyApplication extends JFrame {
    public MyApplication() {
        add(new JLabel("Hello"));
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        pack();
        setVisible(true);
    }
    
    public static void main(String[] args) {
        SwingUtilities.invokeLater(MyApplication::new);
    }
}
```

**Web 替代方案**:

| 原方案 | 替代方案 |
|--------|----------|
| Applet | JavaScript + WebAssembly |
| Applet | Java Web Start (已移除，不推荐) |
| Applet | 独立桌面应用 (JavaFX/Swing) |

---

### 场景 3: Final 字段修改限制 (JEP 500)

**影响**: 如果代码通过反射或 JNI 修改 final 字段

**检查方法**:

```bash
# 搜索反射修改 final 字段的代码
grep -r "setAccessible" src/ | grep -i field
grep -r "Field.set" src/
grep -rn "final.*Field" src/
```

**迁移方案**:

```java
// 旧代码: 通过反射修改 final
public class Config {
    private final int timeout = 30;
    
    public void setTimeout(int newTimeout) throws Exception {
        Field f = getClass().getDeclaredField("timeout");
        f.setAccessible(true);
        f.set(this, newTimeout);  // JDK 26 默认失败
    }
}

// 方案 1: 移除 final
public class Config {
    private int timeout = 30;  // 移除 final
    
    public void setTimeout(int newTimeout) {
        this.timeout = newTimeout;
    }
}

// 方案 2: 使用 AtomicReference
public class Config {
    private final AtomicReference<Integer> timeout = 
        new AtomicReference<>(30);
    
    public void setTimeout(int newTimeout) {
        timeout.set(newTimeout);
    }
}

// 方案 3: 使用可变容器
public class Config {
    private final int[] timeout = {30};  // 数组内容可变
    
    public void setTimeout(int newTimeout) {
        timeout[0] = newTimeout;
    }
}

// 方案 4: 参考 JEP 500 文档了解迁移选项
```

---

### 场景 4: 迁移到新并发 API

**从 ThreadLocal 迁移到 Scoped Values**:

```java
// 旧代码: ThreadLocal
public class RequestContext {
    private static final ThreadLocal<User> currentUser = new ThreadLocal<>();
    
    public void handleRequest(User user) {
        currentUser.set(user);
        try {
            processRequest();
        } finally {
            currentUser.remove();  // 必须清理
        }
    }
    
    public User getCurrentUser() {
        return currentUser.get();
    }
}

// 新代码: Scoped Values
public class RequestContext {
    private static final ScopedValue<User> CURRENT_USER = ScopedValue.create();
    
    public void handleRequest(User user) {
        ScopedValue.where(CURRENT_USER, user).run(() -> {
            processRequest();  // 自动清理
        });
    }
    
    public User getCurrentUser() {
        return CURRENT_USER.get();
    }
}
```

**从 ExecutorService 迁移到 StructuredTaskScope**:

```java
// 旧代码: ExecutorService
ExecutorService executor = Executors.newCachedThreadPool();
try {
    Future<String> userFuture = executor.submit(() -> fetchUser());
    Future<List<Order>> ordersFuture = executor.submit(() -> fetchOrders());
    
    String user = userFuture.get();
    List<Order> orders = ordersFuture.get();
    
    return new Response(user, orders);
} catch (Exception e) {
    userFuture.cancel(true);
    ordersFuture.cancel(true);
    throw e;
} finally {
    executor.shutdown();
}

// 新代码: StructuredTaskScope
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Subtask<String> user = scope.fork(() -> fetchUser());
    Subtask<List<Order>> orders = scope.fork(() -> fetchOrders());
    
    scope.join();
    scope.throwIfFailed();
    
    return new Response(user.resultNow(), orders.resultNow());
}  // 自动关闭和取消
```

---

### 场景 5: 启用 HTTP/3

```java
// 旧代码: HTTP/1.1 或 HTTP/2
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_2)
    .build();

// 新代码: HTTP/3 自动协商
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_3_AUTO)  // 自动选择最佳版本
    .connectTimeout(Duration.ofSeconds(10))
    .build();

// 检查实际使用的版本
HttpResponse<String> response = client.send(request, handler);
System.out.println("Protocol: " + response.version());
```

---

## 3. 升级步骤

### 1. 准备阶段

```bash
# 1.1 备份当前环境
cp -r /path/to/app /path/to/app.backup

# 1.2 创建测试分支
git checkout -b upgrade-jdk26

# 1.3 下载 JDK 26
# 从 https://jdk.java.net/26/ 下载
```

### 2. 编译阶段

```bash
# 2.1 更新构建工具
# Maven
mvn versions:display-property-updates
mvn versions:update-properties

# Gradle
./gradlew dependencyUpdates

# 2.2 更新编译器版本
# Maven pom.xml
<properties>
    <maven.compiler.source>26</maven.compiler.source>
    <maven.compiler.target>26</maven.compiler.target>
</properties>

# 2.3 编译
mvn clean compile

# 2.4 处理编译错误
# 根据错误信息逐个修复
```

### 3. 测试阶段

```bash
# 3.1 运行单元测试
mvn test

# 3.2 运行集成测试
mvn verify

# 3.3 启用预览特性测试
mvn test -DargLine="--enable-preview"

# 3.4 性能测试
# 对比升级前后性能指标
```

### 4. 部署阶段

```bash
# 4.1 更新 Docker 基础镜像
FROM eclipse-temurin:26-jdk

# 4.2 更新启动脚本
java --enable-preview -jar myapp.jar

# 4.3 更新 JVM 参数
# 参考 cheat-sheet.md 中的 JVM 参数
```

---

## 4. 性能优化建议

### 启动优化

```bash
# 创建 CDS 归档
java -XX:ArchiveClassesAtExit=app.aot -cp myapp.jar MyApp

# 使用 CDS 归档启动
java -XX:SharedArchiveFile=app.aot -cp myapp.jar MyApp
```

### GC 优化

```bash
# G1 GC (通用场景)
-XX:+UseG1GC
# JEP 522 Claim Table 优化默认启用，无需额外参数
-XX:MaxGCPauseMillis=100

# Shenandoah (低延迟场景)
-XX:+UseShenandoahGC
-XX:ShenandoahGCMode=generational
```

### 内存优化

```bash
# 启用紧凑对象头
-XX:+UseCompactObjectHeaders  # 默认启用

# 压缩指针
-XX:+UseCompressedOops
-XX:+UseCompressedClassPointers
```

---

## 5. 常见问题

### Q: 编译时报 "source level 26 not supported"

```bash
# 更新 Maven 编译插件
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <version>3.13.0</version>
</plugin>
```

### Q: 运行时报 "Preview features not enabled"

```bash
# 添加 --enable-preview 参数
java --enable-preview -jar myapp.jar

# Maven 测试
mvn test -DargLine="--enable-preview"
```

### Q: 反射修改 final 字段失败

```bash
# 方案 1: 重构代码 (推荐)
# 方案 2: 临时启用
# 注意: --finalization=enabled 用于重新启用 Object.finalize()，
# 与 final 字段修改无关。请参考 JEP 500 文档了解迁移选项。
```

### Q: HTTP/3 连接失败

```java
// 检查服务器是否支持 HTTP/3
// 使用自动协商模式
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_3_AUTO)  // 自动降级
    .build();
```

---

## 6. 回滚计划

如果升级后出现问题：

```bash
# 1. 回滚代码
git checkout main
git branch -D upgrade-jdk26

# 2. 回滚部署
# 使用之前的 Docker 镜像或部署包

# 3. 分析问题
# 收集日志、堆栈信息
# 在测试环境复现
```

---

## 7. 检查清单

升级完成后，确认以下项目：

- [ ] 所有单元测试通过
- [ ] 集成测试通过
- [ ] 性能基准测试符合预期
- [ ] 无编译警告
- [ ] 无运行时警告
- [ ] 日志输出正常
- [ ] 监控指标正常
- [ ] 文档已更新