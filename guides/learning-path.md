# JDK 26 学习路径

本文档帮助你根据角色和需求找到最适合的学习路径。

---

## 按角色分类

### 🎓 初学者 / 学生

**目标**: 了解 Java 最新特性，简化入门体验

**推荐路径** (约 2 小时):

```
1. [JEP 512: Compact Source Files](../jeps/jep-512.md)
   └── 学习如何用最少的代码写 Java 程序
   
2. [JEP 511: Module Import Declarations](../jeps/jep-511.md)
   └── 学习如何简化 import 语句
   
3. [JEP 530: Primitive Types in Patterns](../jeps/jep-530.md)
   └── 学习模式匹配的新用法
   
4. [JEP 526: Lazy Constants](../jeps/jep-526.md)
   └── 了解延迟初始化的概念
```

**快速入门代码**:

```java
// Hello.java - JDK 26 最简程序
import module java.base;

void main() {
    println("Hello, JDK 26!");
    
    var name = readln("What's your name? ");
    println("Hello, " + name + "!");
}
```

---

### 👨‍💻 应用开发者

**目标**: 在项目中使用新特性，提升代码质量

**推荐路径** (约 4 小时):

```
核心特性
├── [JEP 511: Module Import Declarations](../jeps/jep-511.md)
├── [JEP 502: Stable Values](../jeps/jep-502.md)
├── [JEP 506: Scoped Values](../jeps/jep-506.md)
└── [JEP 525: Structured Concurrency](../jeps/jep-525.md)

网络编程
└── [JEP 517: HTTP/3](../jeps/jep-517.md)

安全编程
├── [JEP 510: KDF API](../jeps/jep-510.md)
└── [JEP 470: PEM Encodings](../jeps/jep-470.md)
```

**实用代码示例**:

```java
// 使用 StableValue 实现单例
public class DatabaseConnection {
    private static final StableValue<Connection> CONN = StableValue.of();
    
    public static Connection getConnection() {
        return CONN.orElseSet(() -> DriverManager.getConnection(url));
    }
}

// 使用 Scoped Value 传递上下文
public class RequestContext {
    private static final ScopedValue<User> CURRENT_USER = ScopedValue.create();
    
    public void handleRequest(User user, Runnable handler) {
        ScopedValue.where(CURRENT_USER, user).run(handler);
    }
}

// 使用 HTTP/3 客户端
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_3_AUTO)
    .build();
```

---

### 🏗️ 架构师 / 技术负责人

**目标**: 评估升级影响，规划技术路线

**推荐路径** (约 6 小时):

```
架构影响评估
├── [JEP 500: Make Final Mean Final](../jeps/jep-500.md) - 安全影响
├── [JEP 503: Remove 32-bit x86](../jeps/jep-503.md) - 平台支持
├── [JEP 504: Remove Applet API](../jeps/jep-504.md) - 遗留系统
└── [迁移指南](migration-guide.md) - 升级策略

性能优化
├── [JEP 522: G1 GC Throughput](../jeps/jep-522.md)
├── [JEP 521: Generational Shenandoah](../jeps/jep-521.md)
├── [JEP 519: Compact Object Headers](../jeps/jep-519.md)
├── [JEP 514: AOT Ergonomics](../jeps/jep-514.md)
└── [JEP 515: AOT Method Profiling](../jeps/jep-515.md)

监控与诊断
├── [JEP 509: JFR CPU-Time Profiling](../jeps/jep-509.md)
├── [JEP 518: JFR Cooperative Sampling](../jeps/jep-518.md)
└── [JEP 520: JFR Method Timing](../jeps/jep-520.md)
```

**决策矩阵**:

| 场景 | 推荐 JEP | 收益 |
|------|----------|------|
| 高并发服务 | 522, 521, 525 | 吞吐量 +15-20% |
| 微服务启动优化 | 514, 515 | 启动时间 -50% |
| 内存敏感应用 | 519 | 内存占用 -20% |
| 安全敏感应用 | 500, 510 | 安全性提升 |

---

### 🔧 运维工程师

**目标**: 优化 JVM 配置，提升监控能力

**推荐路径** (约 3 小时):

```
性能调优
├── [JEP 522: G1 GC Throughput](../jeps/jep-522.md)
├── [JEP 521: Generational Shenandoah](../jeps/jep-521.md)
├── [JEP 519: Compact Object Headers](../jeps/jep-519.md)
└── [速查表](cheat-sheet.md) - JVM 参数

监控诊断
├── [JEP 509: JFR CPU-Time Profiling](../jeps/jep-509.md)
├── [JEP 518: JFR Cooperative Sampling](../jeps/jep-518.md)
└── [JEP 520: JFR Method Timing](../jeps/jep-520.md)
```

**关键配置**:

```bash
# G1 GC 优化配置
-XX:+UseG1GC
-XX:+G1UseClaimTable
-XX:G1HeapRegionSize=32m

# Shenandoah 分代模式
-XX:+UseShenandoahGC
-XX:ShenandoahGCMode=generational

# JFR 配置
-XX:StartFlightRecording=settings=profile,filename=app.jfr
```

---

### 🧪 测试工程师

**目标**: 了解新特性对测试的影响

**推荐路径** (约 2 小时):

```
测试相关
├── [JEP 500: Make Final Mean Final](../jeps/jep-500.md) - 反射测试影响
├── [JEP 506: Scoped Values](../jeps/jep-506.md) - 测试上下文传递
└── [JEP 525: Structured Concurrency](../jeps/jep-525.md) - 并发测试
```

---

## 按主题分类

### 🚀 性能优化

```
启动性能
├── JEP 514: AOT Command Line Ergonomics
└── JEP 515: AOT Method Profiling

运行时性能
├── JEP 522: G1 GC Throughput Improvement
├── JEP 521: Generational Shenandoah
└── JEP 519: Compact Object Headers

监控诊断
├── JEP 509: JFR CPU-Time Profiling
├── JEP 518: JFR Cooperative Sampling
└── JEP 520: JFR Method Timing and Tracing
```

### 🔄 并发编程

```
├── JEP 525: Structured Concurrency (Preview)
├── JEP 506: Scoped Values
└── JEP 502: Stable Values (Preview)
```

### 🌐 网络编程

```
└── JEP 517: HTTP/3 for the HTTP Client API
```

### 🔐 安全编程

```
├── JEP 500: Prepare to Make Final Mean Final
├── JEP 510: Key Derivation Function API
└── JEP 470: PEM Encodings (Preview)
```

### 📝 语言特性

```
├── JEP 511: Module Import Declarations
├── JEP 512: Compact Source Files
├── JEP 530: Primitive Types in Patterns (Preview)
└── JEP 526: Lazy Constants (Preview)
```

### 🗑️ 移除与清理

```
├── JEP 503: Remove the 32-bit x86 Port
└── JEP 504: Remove the Applet API
```

---

## 学习时间估算

| 角色 | 必读 JEP | 选读 JEP | 预计时间 |
|------|----------|----------|----------|
| 初学者 | 4 | 2 | 2 小时 |
| 应用开发者 | 8 | 6 | 4 小时 |
| 架构师 | 15 | 6 | 6 小时 |
| 运维工程师 | 6 | 4 | 3 小时 |
| 测试工程师 | 3 | 4 | 2 小时 |

---

## 下一步

- 📋 [速查表](cheat-sheet.md) - 快速参考
- 📖 [迁移指南](migration-guide.md) - 项目升级
- ❓ [FAQ](faq.md) - 常见问题