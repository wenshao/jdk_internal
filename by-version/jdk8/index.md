# JDK 8

> **状态**: LTS (长期支持) | **GA 发布**: 2014-03-18 | **类型**: Long Term Support

[![OpenJDK](https://img.shields.io/badge/OpenJDK-8-blue)](https://openjdk.org/projects/jdk8/)
[![LTS](https://img.shields.io/badge/LTS-Extended--purple.svg)](https://www.oracle.com/java/technologies/java-se-support.html)

---
## 目录

1. [版本概览](#1-版本概览)
2. [关键 JEP](#2-关键-jep)
3. [代码示例](#3-代码示例)
4. [GC 状态](#4-gc-状态)
5. [迁移指南](#5-迁移指南)
6. [相关链接](#6-相关链接)

---


## 1. 版本概览

JDK 8 是一个具有里程碑意义的版本，引入了 Lambda 表达式、Stream API 等重大特性：

| 特性 | 说明 |
|------|------|
| **Lambda 表达式** | 函数式编程基础 |
| **Stream API** | 集合操作新方式 |
| **日期时间 API** | 全新的 java.time 包 |
| **默认方法** | 接口默认实现 |
| **类型注解** | 更强的类型检查 |
| **重复注解** | 同一注解多次使用 |
| **方法引用** | Lambda 简化语法 |
| **Optional** | 空值处理 |
| **CompletableFuture** | 异步编程 |
| **Base64 编码** | 内置 Base64 支持 |
| **PermGen 移除** | 替换为 Metaspace |

---

## 2. 关键 JEP

| JEP | 标题 | 说明 |
|-----|------|------|
| [JEP 101](https://openjdk.org/jeps/101) | Generalized Target-Type Inference | 泛型目标类型推断 |
| [JEP 103](https://openjdk.org/jeps/103) | Parallel Array Sorting | 并行数组排序 |
| [JEP 104](https://openjdk.org/jeps/104) | Annotations on Java Types | 类型注解 |
| [JEP 105](https://openjdk.org/jeps/105) | DocTree API | 文档树 API |
| [JEP 106](https://openjdk.org/jeps/106) | Add Javadoc to javax.tools | Javadoc 工具 API |
| [JEP 107](https://openjdk.org/jeps/107) | Bulk Data Operations for Collections | 集合批量操作 |
| [JEP 108](https://openjdk.org/jeps/108) | (Unlisted) | (未列出) |
| [JEP 109](https://openjdk.org/jeps/109) | Enhance Core Libraries with Lambda | 核心库 Lambda 增强 |
| [JEP 112](https://openjdk.org/jeps/112) | Charset Implementation Improvements | 字符集实现改进 |
| [JEP 113](https://openjdk.org/jeps/113) | MS-SFU Kerberos 5 Extensions | MS-SFU Kerberos 扩展 |
| [JEP 114](https://openjdk.org/jeps/114) | TLS Server Name Indication (SNI) Extension | TLS SNI 扩展 |
| [JEP 115](https://openjdk.org/jeps/115) | AEAD CipherSuites | AEAD 密码套件 |
| [JEP 117](https://openjdk.org/jeps/117) | Remove the Annotation-Processing Tool (apt) | 移除 apt 工具 |
| [JEP 118](https://openjdk.org/jeps/118) | Access to Parameter Names at Runtime | 运行时参数名访问 |
| [JEP 119](https://openjdk.org/jeps/119) | javax.lang.model Implementation Backed by Core Reflection | 反射支持的 javax.lang.model |
| [JEP 120](https://openjdk.org/jeps/120) | Repeating Annotations | 重复注解 |
| [JEP 121](https://openjdk.org/jeps/121) | Stronger Algorithms for Password-Based Encryption | 更强的 PBE 算法 |
| [JEP 122](https://openjdk.org/jeps/122) | Remove the Permanent Generation | 移除永久代 |
| [JEP 123](https://openjdk.org/jeps/123) | Configurable Secure Random-Number Generation | 可配置安全随机数 |
| [JEP 124](https://openjdk.org/jeps/124) | Enhance the Certificate Revocation-Checking API | 证书撤销检查 API 增强 |
| [JEP 126](https://openjdk.org/jeps/126) | Lambda Expressions & Virtual Extension Methods | Lambda 表达式 |
| [JEP 127](https://openjdk.org/jeps/127) | Improve Locale Data Packaging and Adopt Unicode CLDR Data | CLDR 区域数据 |
| [JEP 128](https://openjdk.org/jeps/128) | BCP 47 Locale Matching | BCP 47 区域匹配 |
| [JEP 129](https://openjdk.org/jeps/129) | NSA Suite B Cryptographic Algorithms | NSA Suite B 算法 |
| [JEP 130](https://openjdk.org/jeps/130) | SHA-224 Message Digests | SHA-224 摘要 |
| [JEP 131](https://openjdk.org/jeps/131) | PKCS#11 Crypto Provider for 64-bit Windows | 64位 Windows PKCS#11 |
| [JEP 133](https://openjdk.org/jeps/133) | Unicode 6.2 | Unicode 6.2 |
| [JEP 135](https://openjdk.org/jeps/135) | Base64 Encoding & Decoding | Base64 编解码 |
| [JEP 136](https://openjdk.org/jeps/136) | Enhanced Verification Errors | 增强验证错误 |
| [JEP 138](https://openjdk.org/jeps/138) | Autoconf-Based Build System | 自动配置构建系统 |
| [JEP 139](https://openjdk.org/jeps/139) | Enhance javac to Improve Build Speed | javac 构建速度优化 |
| [JEP 140](https://openjdk.org/jeps/140) | Limited doPrivileged | 有限的 doPrivileged |
| [JEP 142](https://openjdk.org/jeps/142) | Reduce Cache Contention on Specified Fields | 减少缓存竞争 |
| [JEP 147](https://openjdk.org/jeps/147) | Reduce Class Metadata Footprint | 减少类元数据占用 |
| [JEP 149](https://openjdk.org/jeps/149) | Reduce Core-Library Memory Usage | 减少核心库内存占用 |
| [JEP 150](https://openjdk.org/jeps/150) | Date & Time API | 日期时间 API（已撤销，由 JSR 310 / JEP 126 交付） |
| [JEP 151](https://openjdk.org/jeps/151) | (Small VM) | 小型 VM |
| [JEP 153](https://openjdk.org/jeps/153) | Launch JavaFX Applications | 启动 JavaFX 应用 |
| [JEP 155](https://openjdk.org/jeps/155) | Concurrency Updates | 并发更新 |
| [JEP 157](https://openjdk.org/jeps/157) | G1 GC: NUMA-Aware Allocation | G1 GC NUMA 感知分配 |
| [JEP 158](https://openjdk.org/jeps/158) | Unified JVM Logging | 统一 JVM 日志（JDK 9 交付） |
| [JEP 159](https://openjdk.org/jeps/159) | Enhanced Class Redefinition | 增强类重定义 |
| [JEP 160](https://openjdk.org/jeps/160) | Lambda-Form Representation for Method Handles | Lambda 形式方法句柄 |
| [JEP 161](https://openjdk.org/jeps/161) | Compact Profiles | 紧凑配置 |
| [JEP 162](https://openjdk.org/jeps/162) | Prepare for Modularization | 模块化准备 |
| [JEP 163](https://openjdk.org/jeps/163) | Prepare JavaFX UI Controls & CSS APIs for Modularization | JavaFX 模块化准备 |
| [JEP 164](https://openjdk.org/jeps/164) | Leverage CPU Instructions for AES Cryptography | AES 硬件指令 |
| [JEP 166](https://openjdk.org/jeps/166) | Overhaul JKS-JCEKS-PKCS12 Keystores | 密钥库改进 |
| [JEP 171](https://openjdk.org/jeps/171) | Fence Intrinsics | 栅栏内联函数 |
| [JEP 173](https://openjdk.org/jeps/173) | Retire Some Rarely-Used GC Combinations | 移除罕见 GC 组合 |
| [JEP 174](https://openjdk.org/jeps/174) | Nashorn JavaScript Engine | Nashorn 引擎 |
| [JEP 176](https://openjdk.org/jeps/176) | Mechanical Checking of Caller-Sensitive Methods | 调用敏感方法检查 |
| [JEP 177](https://openjdk.org/jeps/177) | Optimize java.text.DecimalFormat.format | DecimalFormat 优化 |
| [JEP 178](https://openjdk.org/jeps/178) | Statically-Linked JNI Libraries | 静态链接 JNI 库 |
| [JEP 179](https://openjdk.org/jeps/179) | Document JDK API Support and Stability | JDK API 稳定性文档 |
| [JEP 180](https://openjdk.org/jeps/180) | Handle Frequent HashMap Collisions with Balanced Trees | HashMap 树优化 |
| [JEP 184](https://openjdk.org/jeps/184) | HTTP URL Permissions | HTTP URL 权限 |
| [JEP 185](https://openjdk.org/jeps/185) | Restrict Fetching of External XML Resources | 限制 XML 外部资源 |

---

## 3. 代码示例

### Lambda 表达式

```java
// 之前
button.addActionListener(new ActionListener() {
    @Override
    public void actionPerformed(ActionEvent e) {
        System.out.println("Clicked");
    }
});

// JDK 8
button.addActionListener(e -> System.out.println("Clicked"));

// 方法引用
list.forEach(System.out::println);
```

### Stream API

```java
// 过滤和转换
List<String> names = people.stream()
    .filter(p -> p.getAge() > 18)
    .map(Person::getName)
    .sorted()
    .collect(Collectors.toList());

// 并行流
long count = list.parallelStream()
    .filter(s -> s.startsWith("A"))
    .count();
```

### 日期时间 API

```java
// 之前
Date now = new Date();
SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");

// JDK 8
LocalDate today = LocalDate.now();
LocalDateTime now = LocalDateTime.now();
ZonedDateTime utc = ZonedDateTime.now(ZoneId.of("UTC"));

Period period = Period.between(date1, date2);
Duration duration = Duration.between(instant1, instant2);
```

### Optional

```java
// 避免 NullPointerException
Optional<String> optional = Optional.of("value");

optional.ifPresent(System.out::println);
String result = optional.orElse("default");
String mapped = optional.map(String::toUpperCase).orElse("EMPTY");
```

### 重复注解

```java
@Repeatable(Schedules.class)
@interface Schedule {
    String day();
    String time();
}

@interface Schedules {
    Schedule[] value();
}

@Schedule(day = "Monday", time = "09:00")
@Schedule(day = "Friday", time = "17:00")
void meeting() { }
```

---

## 4. GC 状态

| GC | 状态 | 说明 |
|----|------|------|
| **ParallelGC** | 默认 | 高吞吐量 |
| **G1 GC** | 可选 | 低延迟，JDK 9 成为默认 |
| **CMS** | 可选 | JDK 9 标记废弃，JDK 14 移除 |

---

## 5. 迁移指南

### 从 JDK 7 升级

**破坏性变更**:
- `PermGen` 移除，替换为 `Metaspace`
- `URLClassLoader` 不再搜索 `sun.*` 包

**推荐配置**:
```bash
-XX:+UseG1GC           # 使用 G1 GC
-XX:MaxMetaspaceSize=256m  # 元空间大小
```

---

## 6. 相关链接

- [JDK 8 发布说明](https://openjdk.org/projects/jdk8/)
- [JDK 8 文档](https://docs.oracle.com/javase/8/)
- [Lambda 指南](https://docs.oracle.com/javase/tutorial/java/javaOO/lambdaexpressions.html)
