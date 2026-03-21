# JDK 8 新特性（相比 JDK 7）

> **对比基准**: JDK 7u80 (2015-04-14) → JDK 8u401 (2024-01-16)

---
## 目录

1. [语言特性](#1-语言特性)
2. [API 增强](#2-api-增强)
3. [JVM 改进](#3-jvm-改进)
4. [工具增强](#4-工具增强)
5. [安全性改进](#5-安全性改进)
6. [性能提升](#6-性能提升)
7. [废弃和移除](#7-废弃和移除)
8. [迁移建议](#8-迁移建议)
9. [兼容性检查](#9-兼容性检查)
10. [资源链接](#10-资源链接)

---


## 1. 语言特性

### Lambda 表达式 (JSR 335)

**语法示例**:
```java
// JDK 7 之前
Collections.sort(list, new Comparator<String>() {
    public int compare(String s1, String s2) {
        return s1.compareTo(s2);
    }
});

// JDK 8 Lambda
Collections.sort(list, (s1, s2) -> s1.compareTo(s2));
```

**关键改进**:
- 函数式接口 (`@FunctionalInterface`)
- 方法引用 (`String::toUpperCase`)
- 构造函数引用 (`ArrayList::new`)

### Stream API

**核心接口**:
- `Stream<T>`: 元素序列
- `IntStream`, `LongStream`, `DoubleStream`: 基本类型流

**操作类型**:
- 中间操作: `filter`, `map`, `sorted`
- 终端操作: `forEach`, `collect`, `reduce`

### 默认方法 (Default Methods)

**解决接口演进问题**:
```java
interface List<E> extends Collection<E> {
    default void sort(Comparator<? super E> c) {
        Collections.sort(this, c);
    }
}
```

### 类型注解

**注解位置扩展**:
```java
@NonNull String str = "hello";  // 类型注解
List<@NonNull String> list;     // 泛型参数注解
```

---

## 2. API 增强

### 日期时间 API (JSR 310)

**全新设计**:
- `LocalDate`, `LocalTime`, `LocalDateTime`
- `ZonedDateTime`, `OffsetDateTime`
- `Period`, `Duration`
- `DateTimeFormatter`

**替代方案**:
- 替代 `java.util.Date` 和 `java.util.Calendar`
- 不可变、线程安全

### 集合框架增强

**新方法**:
- `Collection.removeIf(Predicate)`
- `List.sort(Comparator)`
- `Map.getOrDefault(Object, V)`
- `Map.forEach(BiConsumer)`
- `Map.computeIfAbsent(K, Function)`

### Concurrency 增强

**新增类**:
- `CompletableFuture`: 异步编程
- `StampedLock`: 乐观读锁
- `LongAdder`, `DoubleAdder`: 高并发计数器

### 其他 API

**NIO.2 增强**:
- `Files.list(Path)`, `Files.walk(Path)`
- `Files.lines(Path)`: 流式读取文件

**Base64 支持**:
- `java.util.Base64` 类
- URL 安全编码

---

## 3. JVM 改进

### Metaspace 替换 PermGen

| 特性 | PermGen (JDK 7) | Metaspace (JDK 8) |
|------|-----------------|--------------------|
| **位置** | 堆内 | 堆外 (native memory) |
| **大小限制** | `-XX:MaxPermSize` | `-XX:MaxMetaspaceSize` |
| **垃圾收集** | Full GC 时回收 | 独立于堆 GC |
| **元数据** | 类元数据 | 类元数据、方法元数据 |

**配置迁移**:
```bash
# JDK 7
-XX:PermSize=128m -XX:MaxPermSize=256m

# JDK 8
-XX:MetaspaceSize=128m -XX:MaxMetaspaceSize=256m
```

### G1 GC 增强

**状态变化**:
- JDK 6u14: 引入 (实验性)
- JDK 7u4: 成为官方特性
- JDK 8: 生产环境就绪

**关键参数**:
- `-XX:+UseG1GC`
- `-XX:MaxGCPauseMillis=200`

### 移除 HotSpot PermGen

**影响**:
- `-XX:PermSize`, `-XX:MaxPermSize` 参数无效
- 监控工具需要更新
- 内存分析工具需要适配

---

## 4. 工具增强

### Nashorn JavaScript 引擎

**替代 Rhino**:
- 基于 JSR 292 (InvokeDynamic)
- 性能大幅提升
- `jjs` 命令行工具

### 注解处理器增强

**重复注解**:
```java
@Repeatable(Schedules.class)
@interface Schedule {
    String time();
}

@Schedule(time="9am")
@Schedule(time="5pm")
public void scheduledMethod() { }
```

### JDK 工具

**jcmd 增强**:
- 统一命令行工具
- 替代 `jstack`, `jmap`, `jinfo` 部分功能

**Java Mission Control (JMC)**:
- 商业特性 (Oracle JDK)
- 开源版本 (OpenJDK)

---

## 5. 安全性改进

### TLS 1.2 默认支持

**协议升级**:
- 启用 TLS 1.2 作为默认安全协议
- 禁用弱密码套件

### 证书撤销检查

**OCSP Stapling**:
- 减少证书验证延迟
- 提高 TLS 握手性能

### 安全性管理器增强

**细化权限控制**:
- 更细粒度的安全策略
- 改进的沙箱机制

---

## 6. 性能提升

### Lambda 性能优化

**InvokeDynamic**:
- 运行时优化
- 自适应编译

### 集合操作优化

**Stream 管道优化**:
- 惰性求值
- 短路操作
- 并行流性能

### 启动时间优化

**类数据共享 (CDS)**:
- 改进的归档格式
- 更快的应用启动

---

## 7. 废弃和移除

### 废弃的 API

| API | 替代方案 | 移除版本 |
|-----|----------|----------|
| `Thread.stop()` | 中断机制 | 未移除 |
| `Thread.suspend()` | 并发工具 | 未移除 |
| `Runtime.runFinalizersOnExit()` | Cleaner API | JDK 18 |
| `SecurityManager` 部分方法 | 模块系统 | JDK 17 |

### 移除的特性

| 特性 | 说明 | 影响 |
|------|------|------|
| **PermGen** | 替换为 Metaspace | 需要调整内存参数 |
| **Java Browser Plugin** | 浏览器不再支持 | Applet 迁移 |

---

## 8. 迁移建议

### 代码迁移

1. **Lambda 重构**:
   - 识别匿名内部类
   - 转换为 Lambda 表达式

2. **日期时间迁移**:
   - 替换 `java.util.Date` 为 `java.time.*`
   - 更新日期格式化代码

3. **集合操作**:
   - 使用 Stream API 替换循环
   - 利用新的集合方法

### 配置迁移

1. **内存配置**:
   - 更新 PermGen 参数为 Metaspace
   - 调整 GC 参数

2. **安全配置**:
   - 更新 TLS 配置
   - 检查证书链

### 工具更新

1. **构建工具**:
   - Maven: 确保编译器版本
   - Gradle: 更新 Java 兼容性

2. **监控工具**:
   - 更新 JVM 监控参数
   - 适配 Metaspace 指标

---

## 9. 兼容性检查

### 向后兼容性

**二进制兼容性**:
- 类文件版本: 52 (JDK 8)
- 目标版本: `-target 1.8`

**源代码兼容性**:
- 大多数 JDK 7 代码无需修改
- 注意废弃 API 的使用

### 已知问题

1. **PermGen 相关工具**:
   - 监控工具可能显示错误的内存区域
   - 需要工具更新

2. **第三方库兼容性**:
   - 检查库的 JDK 8 兼容性
   - 更新依赖版本

---

## 10. 资源链接

### 官方文档
- [JDK 8 特性列表](https://openjdk.org/projects/jdk8/features)
- [迁移指南](https://docs.oracle.com/javase/8/docs/technotes/guides/migration/index.html)

### 工具支持
- [Java Version Almanac](https://javaalmanac.io/jdk/8/)
- [API 差异报告](https://apitools.info/java-api-diff/8/)

### 社区资源
- [Stack Overflow JDK 8 标签](https://stackoverflow.com/questions/tagged/java-8)
- [Baeldung Java 8 教程](https://www.baeldung.com/java-8-tutorial)