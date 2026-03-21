# 从 JDK 7 迁移到 JDK 8

> **迁移复杂度**: 中等 | **建议时间**: 2-4 周 | **测试要求**: 全面回归测试

---
## 目录

1. [迁移概览](#1-迁移概览)
2. [准备工作](#2-准备工作)
3. [代码迁移步骤](#3-代码迁移步骤)
4. [配置迁移](#4-配置迁移)
5. [测试策略](#5-测试策略)
6. [部署策略](#6-部署策略)
7. [常见问题解决](#7-常见问题解决)
8. [迁移后优化](#8-迁移后优化)
9. [工具和资源](#9-工具和资源)
10. [总结检查清单](#10-总结检查清单)

---


## 1. 迁移概览

### 迁移路径

```
JDK 7u80 (当前)
    ↓
JDK 8u401 (目标)
    ↓
兼容性测试
    ↓
性能基准测试
    ↓
生产部署
```

### 关键时间点

| 阶段 | 时间估算 | 负责人 |
|------|----------|--------|
| **评估和规划** | 1-2 周 | 架构师 |
| **代码迁移** | 1-2 周 | 开发团队 |
| **测试验证** | 1-2 周 | QA 团队 |
| **部署上线** | 1 周 | 运维团队 |

---

## 2. 准备工作

### 环境评估

1. **系统要求检查**:
```bash
# 检查操作系统兼容性
uname -a
cat /etc/os-release

# 检查架构支持
java -version
```

2. **依赖库兼容性**:
```xml
<!-- Maven 依赖检查 -->
<dependency>
    <groupId>org.example</groupId>
    <artifactId>library</artifactId>
    <version>1.0.0</version>
</dependency>
```

3. **构建工具更新**:
| 工具 | JDK 7 版本 | JDK 8 要求 | 操作 |
|------|------------|------------|------|
| Maven | 3.0+ | 3.3+ | 升级 |
| Gradle | 2.0+ | 2.8+ | 升级 |
| Ant | 1.9+ | 1.10+ | 升级 |

### 风险评估

| 风险类别 | 可能性 | 影响 | 缓解措施 |
|----------|--------|------|----------|
| **API 不兼容** | 中 | 高 | 全面测试 |
| **性能回归** | 低 | 中 | 性能基准测试 |
| **第三方库问题** | 高 | 中 | 提前验证 |
| **工具链问题** | 低 | 低 | 测试环境验证 |

---

## 3. 代码迁移步骤

### 步骤 1: 编译环境更新

1. **更新构建配置**:
```xml
<!-- Maven pom.xml -->
<properties>
    <maven.compiler.source>1.8</maven.compiler.source>
    <maven.compiler.target>1.8</maven.compiler.target>
</properties>
```

```groovy
// Gradle build.gradle
sourceCompatibility = 1.8
targetCompatibility = 1.8
```

2. **更新 IDE 配置**:
- IntelliJ IDEA: Project Structure → SDK → JDK 8
- Eclipse: Window → Preferences → Java → Installed JREs
- VS Code: `java.home` 设置

### 步骤 2: 废弃 API 替换

1. **使用 jdeprscan 扫描**:
```bash
# 扫描废弃 API 使用
jdeprscan --release 8 your-application.jar
```

2. **常见废弃 API 替换**:
| 废弃 API | 替代方案 | 说明 |
|----------|----------|------|
| `Thread.stop()` | 中断机制 | 使用 `thread.interrupt()` |
| `Thread.suspend()` | 并发工具 | 使用 `Lock` 或 `Semaphore` |
| `Runtime.runFinalizersOnExit()` | Cleaner API | 使用 `try-with-resources` |

### 步骤 3: 语言特性迁移

1. **Lambda 表达式引入**:
```java
// 之前: 匿名内部类
Collections.sort(list, new Comparator<String>() {
    public int compare(String s1, String s2) {
        return s1.compareTo(s2);
    }
});

// 之后: Lambda 表达式
Collections.sort(list, (s1, s2) -> s1.compareTo(s2));
```

2. **Stream API 迁移**:
```java
// 之前: 循环
List<String> result = new ArrayList<>();
for (String s : list) {
    if (s.length() > 5) {
        result.add(s.toUpperCase());
    }
}

// 之后: Stream API
List<String> result = list.stream()
    .filter(s -> s.length() > 5)
    .map(String::toUpperCase)
    .collect(Collectors.toList());
```

3. **日期时间 API 迁移**:
```java
// 之前: java.util.Date
Date now = new Date();
SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
String formatted = sdf.format(now);

// 之后: java.time
LocalDateTime now = LocalDateTime.now();
DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
String formatted = now.format(formatter);
```

### 步骤 4: 并发代码优化

1. **CompletableFuture 替换**:
```java
// 之前: Future + ExecutorService
ExecutorService executor = Executors.newFixedThreadPool(10);
Future<String> future = executor.submit(() -> "result");
String result = future.get();

// 之后: CompletableFuture
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> "result");
String result = future.join();
```

2. **原子类更新**:
```java
// 高并发计数器
// 之前: AtomicLong
AtomicLong counter = new AtomicLong();

// 之后: LongAdder (性能更好)
LongAdder counter = new LongAdder();
counter.increment();
```

### 步骤 5: 集合框架优化

1. **新方法使用**:
```java
// 移除满足条件的元素
list.removeIf(s -> s == null);

// 遍历 Map
map.forEach((key, value) -> System.out.println(key + ": " + value));

// 计算或获取默认值
map.computeIfAbsent(key, k -> createValue(k));
```

---

## 4. 配置迁移

### JVM 参数迁移

1. **内存参数更新**:
```bash
# JDK 7
-XX:PermSize=128m
-XX:MaxPermSize=256m

# JDK 8
-XX:MetaspaceSize=128m
-XX:MaxMetaspaceSize=256m
```

2. **GC 参数优化**:
```bash
# 启用 G1 GC (推荐)
-XX:+UseG1GC
-XX:MaxGCPauseMillis=200
-XX:G1HeapRegionSize=4m

# 或者保持 ParallelGC
-XX:+UseParallelGC
-XX:+UseParallelOldGC
```

3. **其他参数**:
```bash
# 时区数据
-Duser.timezone=Asia/Shanghai

# 安全随机数
-Djava.security.egd=file:/dev/./urandom

# 编码设置
-Dfile.encoding=UTF-8
```

### 应用服务器配置

1. **Tomcat 配置**:
```xml
<!-- conf/server.xml -->
<Connector port="8080" protocol="HTTP/1.1"
           connectionTimeout="20000"
           redirectPort="8443"
           URIEncoding="UTF-8" />
```

2. **启动脚本更新**:
```bash
#!/bin/bash
# 之前: JDK 7
JAVA_HOME=/usr/lib/jvm/java-7-openjdk

# 之后: JDK 8
JAVA_HOME=/usr/lib/jvm/java-8-openjdk
```

### 监控配置更新

1. **JMX 配置**:
```bash
# 启用 JMX 监控
-Dcom.sun.management.jmxremote
-Dcom.sun.management.jmxremote.port=9010
-Dcom.sun.management.jmxremote.ssl=false
-Dcom.sun.management.jmxremote.authenticate=false
```

2. **GC 日志配置**:
```bash
# 详细的 GC 日志
-Xloggc:/path/to/gc.log
-XX:+PrintGCDetails
-XX:+PrintGCDateStamps
-XX:+PrintGCTimeStamps
```

---

## 5. 测试策略

### 单元测试

1. **测试框架兼容性**:
| 框架 | JDK 7 版本 | JDK 8 要求 | 操作 |
|------|------------|------------|------|
| JUnit | 4.12 | 4.12+ | 验证 |
| TestNG | 6.14 | 6.14+ | 验证 |
| Mockito | 2.18 | 2.18+ | 验证 |

2. **测试代码更新**:
```java
// 测试 Lambda 表达式
@Test
public void testLambda() {
    List<String> list = Arrays.asList("a", "b", "c");
    long count = list.stream().filter(s -> s.equals("a")).count();
    assertEquals(1, count);
}
```

### 集成测试

1. **API 兼容性测试**:
- 所有 REST API 端点测试
- 数据库操作测试
- 外部服务集成测试

2. **性能基准测试**:
```bash
# 使用 JMH 进行性能测试
mvn clean install
java -jar target/benchmarks.jar
```

### 回归测试

1. **功能测试覆盖**:
- 所有业务功能测试
- 边界条件测试
- 错误处理测试

2. **安全测试**:
- TLS/SSL 连接测试
- 认证授权测试
- 输入验证测试

---

## 6. 部署策略

### 分阶段部署

1. **阶段 1: 开发环境**:
- 部署 JDK 8
- 基础功能测试
- 性能基准测试

2. **阶段 2: 测试环境**:
- 完整回归测试
- 性能压力测试
- 安全扫描

3. **阶段 3: 预生产环境**:
- 真实流量测试
- 监控验证
- 回滚测试

4. **阶段 4: 生产环境**:
- 金丝雀部署
- 逐步扩大范围
- 监控告警验证

### 回滚计划

1. **回滚条件**:
- 关键功能故障
- 性能严重下降
- 安全漏洞

2. **回滚步骤**:
```bash
# 停止应用
systemctl stop application

# 恢复 JDK 7
export JAVA_HOME=/usr/lib/jvm/java-7-openjdk

# 启动应用
systemctl start application
```

3. **回滚验证**:
- 功能验证
- 性能验证
- 数据一致性验证

---

## 7. 常见问题解决

### 编译问题

1. **类型推断错误**:
```java
// 错误: 类型推断失败
List<String> list = Collections.emptyList();

// 修复: 显式类型参数
List<String> list = Collections.<String>emptyList();
```

2. **默认方法冲突**:
```java
interface A {
    default void foo() { System.out.println("A"); }
}

interface B {
    default void foo() { System.out.println("B"); }
}

class C implements A, B {
    // 必须重写 foo() 方法
    @Override
    public void foo() {
        A.super.foo();  // 调用特定接口的默认方法
    }
}
```

### 运行时问题

1. **Metaspace 内存溢出**:
```bash
# 错误信息
java.lang.OutOfMemoryError: Metaspace

# 解决方案
-XX:MaxMetaspaceSize=512m
-XX:+UseMetaspace
```

2. **类加载器问题**:
```bash
# 错误信息
java.lang.NoClassDefFoundError

# 解决方案
- 检查类路径配置
- 更新依赖库版本
- 清理缓存
```

### 性能问题

1. **启动时间变慢**:
```bash
# 启用 CDS
java -Xshare:dump
java -Xshare:on -jar app.jar
```

2. **内存使用增加**:
```bash
# 监控 Metaspace
jstat -gcmetacapacity <pid>
jcmd <pid> GC.metaspace
```

---

## 8. 迁移后优化

### 代码优化机会

1. **Lambda 重构**:
- 识别匿名内部类
- 转换为 Lambda 表达式
- 使用方法引用

2. **Stream API 优化**:
- 替换传统循环
- 使用并行流优化性能
- 减少中间操作

3. **并发代码优化**:
- 使用 CompletableFuture 简化异步编程
- 使用 LongAdder 替代 AtomicLong
- 使用 StampedLock 优化读写锁

### 性能调优

1. **JVM 调优**:
```bash
# G1 GC 调优
-XX:+UseG1GC
-XX:MaxGCPauseMillis=200
-XX:G1HeapRegionSize=4m
-XX:InitiatingHeapOccupancyPercent=45
```

2. **应用调优**:
- 缓存策略优化
- 数据库连接池调优
- 线程池配置优化

### 监控和告警

1. **新增监控指标**:
- Metaspace 使用率
- G1 GC 暂停时间
- Lambda 表达式编译统计

2. **告警配置**:
```yaml
# Prometheus 告警规则
- alert: HighMetaspaceUsage
  expr: jvm_memory_bytes_used{area="nonheap", id="Metaspace"} / jvm_memory_bytes_max{area="nonheap", id="Metaspace"} > 0.8
  for: 5m
```

---

## 9. 工具和资源

### 迁移工具

1. **jdeps**: 依赖分析
```bash
# 分析依赖关系
jdeps -jdkinternals your-application.jar
```

2. **jdeprscan**: 废弃 API 扫描
```bash
# 扫描废弃 API
jdeprscan --release 8 --for-removal your-application.jar
```

3. **Java Version Almanac**: 版本特性查询
- [javaalmanac.io](https://javaalmanac.io/)

### 文档资源

1. **官方文档**:
- [JDK 8 迁移指南](https://docs.oracle.com/javase/8/docs/technotes/guides/migration/index.html)
- [兼容性指南](https://docs.oracle.com/javase/8/docs/technotes/guides/compatibility/index.html)

2. **社区资源**:
- [Stack Overflow: java-8-migration](https://stackoverflow.com/questions/tagged/java-8+migration)
- [OpenJDK 邮件列表](https://mail.openjdk.org/mailman/listinfo)

### 支持渠道

1. **商业支持**:
- Oracle Java SE Support
- Red Hat OpenJDK Support
- IBM Semeru Support

2. **社区支持**:
- OpenJDK 社区
- Java User Groups
- 技术论坛和博客

---

## 10. 总结检查清单

### 迁移前检查
- [ ] 系统兼容性验证
- [ ] 第三方库兼容性验证
- [ ] 构建工具更新
- [ ] 开发环境配置

### 迁移中检查
- [ ] 代码编译通过
- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 性能基准测试通过

### 迁移后检查
- [ ] 生产环境部署验证
- [ ] 监控告警配置
- [ ] 回滚计划验证
- [ ] 文档更新

### 长期优化
- [ ] 代码重构计划
- [ ] 性能优化计划
- [ ] 安全加固计划
- [ ] 技术债务清理