# 从 JDK 21 迁移到 JDK 25

> JDK 25 是 LTS 版本，本指南帮助您从 JDK 21 平滑升级

---

## 概述

JDK 25 是继 JDK 21 之后的下一个 LTS 版本，提供了多项重要的语言特性和性能改进。

| 类别 | 变更数 | 破坏性 | 兼容性 |
|------|--------|--------|--------|
| 语言特性 | 6 | 低 | ✓ 完全兼容 |
| 性能 | 3 | 低 | ✓ 完全兼容 |
| 并发 | 3 | 低 | ✓ 完全兼容 |
| 安全 | 2 | 中 | ⚠️ 需要注意 |

---

## 快速升级检查

### 1. 兼容性测试

```bash
# 使用 JDK 25 编译现有代码
javac --release 25 YourApp.java

# 运行测试
java -jar yourapp.jar
```

### 2. 依赖检查

```bash
# 检查依赖库兼容性
# 常见库的 JDK 25 兼容性:
# - Spring Boot 3.x ✓
# - Quarkus 3.x ✓
# - Micronaut 4.x ✓
# - Netty 4.1.x ✓
```

---

## 新特性采用

### String Templates (推荐)

**之前**:
```java
String name = "Alice";
int age = 30;
String message = "Name: " + name + ", Age: " + age;
```

**JDK 25**:
```java
String message = STR."Name: \{name}, Age: \{age}";
```

### 虚拟线程 (推荐用于 I/O 密集型)

**之前**:
```java
ExecutorService executor = Executors.newFixedThreadPool(100);
```

**JDK 25**:
```java
ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();
```

### 分代 ZGC (推荐用于大内存)

**之前**:
```bash
java -XX:+UseZGC MyApp
```

**JDK 25**:
```bash
java -XX:+UseZGC -XX:+ZGenerational MyApp
```

---

## 破坏性变更

### Security Manager 限制

**影响**: 如果您的应用使用自定义 Security Manager，需要注意相关变更。

**检查**:
```bash
# 检查是否使用 Security Manager
java -Djava.security.manager MyApp
```

---

## 性能调优建议

### 根据场景选择 GC

| 场景 | JDK 21 | JDK 25 |
|------|--------|--------|
| 大内存 (>8GB) | ZGC | 分代 ZGC (推荐) |
| 低延迟 | ZGC | 分代 ZGC |
| 高吞吐 | G1 | G1 |
| 微服务 | G1 | G1 + 虚拟线程 |

### JVM 参数更新

```bash
# JDK 21 推荐配置
java -XX:+UseZGC -Xmx4g MyApp

# JDK 25 推荐配置
java -XX:+UseZGC -XX:+ZGenerational -Xmx4g MyApp
```

---

## 迁移步骤

### 1. 准备阶段

```bash
# 安装 JDK 25
sdk install java 25

# 设置环境变量
export JAVA_HOME=$HOME/.sdkman/candidates/java/25
export PATH=$JAVA_HOME/bin:$PATH
```

### 2. 测试阶段

```bash
# 编译测试
mvn clean compile

# 运行测试
mvn test

# 集成测试
mvn verify
```

### 3. 生产部署

```bash
# Docker 示例
FROM eclipse-temurin:25-jdk
COPY app.jar /app/app.jar
ENTRYPOINT ["java", "-XX:+UseZGC", "-XX:+ZGenerational", "-jar", "/app/app.jar"]
```

---

## 常见问题

### Q: String Templates 性能如何？

A: String Templates 在编译时优化，性能优于字符串拼接。

### Q: 虚拟线程一定更快吗？

A: 虚拟线程适用于 I/O 密集型场景，CPU 密集型场景收益有限。

### Q: 分代 ZGC 有什么限制？

A: 需要足够的堆内存（建议 >4GB），小内存场景收益不明显。

---

## 更多资源

- [JDK 25 发布说明](https://openjdk.org/projects/jdk/25/)
- [JDK 25 JEP 列表](./jeps.md)
- [虚拟线程指南](https://openjdk.org/jeps/444)
- [分代 ZGC 文档](https://openjdk.org/jeps/468)
