# Native Image 配置最佳实践

> 从零开始配置 Native Image 的完整指南，包含常见问题解决方案

[← 返回 GraalVM 首页](./) | [← 返回性能优化](performance.md)

---
## 目录

1. [快速开始](#1-快速开始)
2. [核心配置参数](#2-核心配置参数)
3. [初始化配置](#3-初始化配置)
4. [反射配置](#4-反射配置)
5. [JNI 配置](#5-jni-配置)
6. [代理配置](#6-代理配置)
7. [资源文件配置](#7-资源文件配置)
8. [PGO (Profile-Guided Optimization)](#8-pgo-profile-guided-optimization)
9. [调试和故障排查](#9-调试和故障排查)
10. [性能调优](#10-性能调优)
11. [框架特定指南](#11-框架特定指南)
12. [完整配置示例](#12-完整配置示例)
13. [相关链接](#13-相关链接)

---


## 1. 快速开始

### 基础配置

```bash
# 1. 安装 GraalVM
sdk install java 21-graal
sdk use java 21-graal

# 2. 安装 native-image 组件
gu install native-image

# 3. 验证安装
native-image --version

# 4. 编译 Hello World
javac Hello.java
native-image Hello
./hello
```

### Maven 配置

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.graalvm.buildtools</groupId>
            <artifactId>native-maven-plugin</artifactId>
            <version>0.10.0</version>
            <extensions>true</extensions>
            <executions>
                <execution>
                    <id>build-native</id>
                    <goals>
                        <goal>compile-no-fork</goal>
                    </goals>
                    <phase>package</phase>
                </execution>
            </executions>
            <configuration>
                <buildArgs>
                    <arg>--no-fallback</arg>
                    <arg>--gc=G1</arg>
                </buildArgs>
            </configuration>
        </plugin>
    </plugins>
</build>
```

### Gradle 配置

```kotlin
plugins {
    id("org.graalvm.buildtools.native") version "0.10.0"
}

graalvmNative {
    binaries {
        named("main") {
            imageName.set("myapp")
            mainClass.set("com.example.Main")
            buildArgs.add("--no-fallback")
            buildArgs.add("--gc=G1")
        }
    }
}
```

---

## 2. 核心配置参数

### 性能优化参数

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| `--gc=G1` | 使用 G1 GC | 生产环境 |
| `--gc=Serial` | 使用 Serial GC | 内存受限 |
| `-O3` | 最高优化级别 | 生产环境 |
| `--no-fallback` | 不生成 fallback 镜像 | 生产环境 |
| `--pgo` | 使用 PGO 优化 | 性能敏感 |

### 启动时间优化

```bash
native-image \
  --initialize-at-build-time \
  --no-fallback \
  -O3 \
  -jar app.jar
```

### 内存优化

```bash
native-image \
  --gc=Serial \
  -H:MaximumHeapSizePercent=20 \
  -jar app.jar
```

---

## 3. 初始化配置

### 构建时初始化 vs 运行时初始化

```
┌─────────────────────────────────────────────────────────────────┐
│              初始化时机对比                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  构建时初始化 (Build-time)                                       │
│  ═══════════════════                                            │
│  • 在 native-image 构建过程中执行                                │
│  • 结果序列化到镜像中                                            │
│  • 启动时直接使用，无需重新初始化                                │
│  • 启动快，内存少                                                │
│  • 无法访问运行时信息                                            │
│                                                                 │
│  运行时初始化 (Run-time)                                         │
│  ═══════════════════                                            │
│  • 在原生可执行文件运行时执行                                    │
│  • 与传统 Java 应用行为一致                                      │
│  • 可以访问系统属性、环境变量等                                  │
│  • 启动慢，但更兼容                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 配置示例

```bash
# 默认：所有类在运行时初始化
native-image -jar app.jar

# 构建时初始化所有类 (最快启动)
native-image \
  --initialize-at-build-time \
  -jar app.jar

# 构建时初始化特定包
native-image \
  --initialize-at-build-time=com.example,com.library \
  -jar app.jar

# 运行时初始化特定类 (解决兼容性问题)
native-image \
  --initialize-at-build-time \
  --initialize-at-run-time=com.example problematic.Class \
  -jar app.jar
```

### 常见问题类

需要运行时初始化的常见类：

```bash
# 安全相关
--initialize-at-run-time=sun.security.util

# 网络相关
--initialize-at-run-time=sun.net

# 第三方库常见需要运行时初始化的类
--initialize-at-run-time=org.apache.commons.logging
--initialize-at-run-time=ch.qos.logback
```

---

## 4. 反射配置

### 为什么需要反射配置？

Native Image 使用**静态分析**，无法检测运行时反射调用。

```java
// 这段代码在 Native Image 中会失败:
Class<?> clazz = Class.forName("com.example.MyClass");
Object obj = clazz.getDeclaredConstructor().newInstance();

// 错误：MyClass 未在镜像中包含
```

### 配置方法

#### 方法 1: 注解配置 (推荐)

```java
import org.graalvm.nativeimage.hosted.Reflection;

@AutomaticFeature
public class ReflectionRegistration implements Feature {
    @Override
    public void beforeAnalysis(BeforeAnalysisAccess access) {
        Reflection.registerClass(com.example.MyClass.class,
            Executable.class,
            Field.class,
            Method.class
        );
    }
}
```

#### 方法 2: JSON 配置

**reflection-config.json**:
```json
[
  {
    "name": "com.example.MyClass",
    "allDeclaredConstructors": true,
    "allPublicConstructors": true,
    "allDeclaredMethods": true,
    "allPublicMethods": true,
    "allDeclaredFields": true,
    "allPublicFields": true
  },
  {
    "name": "com.example.AnotherClass",
    "queryAllDeclaredConstructors": true,
    "queryAllPublicMethods": true
  }
]
```

**编译时使用**:
```bash
native-image \
  -H:ReflectionConfigurationFiles=reflection-config.json \
  -jar app.jar
```

#### 方法 3: 自动生成配置 (推荐用于大型项目)

```bash
# 1. 使用 agent 运行应用
java -agentlib:native-image-agent=config-output-dir=config/ \
     -jar app.jar

# 执行所有功能，触发反射调用
# 访问所有 API 端点
# 运行所有测试

# 2. 使用生成的配置编译
native-image \
  -H:ConfigurationFileDirectories=config/ \
  -jar app.jar
```

### 框架特定配置

#### Spring Boot

```bash
# Spring Boot 3.x 原生支持
native-image \
  -H:+ReportExceptionStackTraces \
  --initialize-at-build-time=org.springframework \
  --initialize-at-run-time=org.springframework.boot \
  -jar app.jar
```

#### Hibernate/JPA

```json
// hibernate-reflection.json
[
  {
    "name": "org.hibernate.bytecode.enhance.spi.interceptor.EnhancementAsProxyLazinessInterceptor",
    "queryAllDeclaredMethods": true
  },
  {
    "name": "com.example.MyEntity",
    "allDeclaredFields": true,
    "allDeclaredMethods": true,
    "allDeclaredConstructors": true
  }
]
```

---

## 5. JNI 配置

### JNI 访问配置

**jni-config.json**:
```json
[
  {
    "name": "com.example.NativeLib",
    "methods": [
      {
        "name": "nativeMethod",
        "parameterTypes": ["int", "java.lang.String"]
      }
    ]
  }
]
```

### 使用配置

```bash
native-image \
  -H:JNIConfigurationFiles=jni-config.json \
  -jar app.jar
```

---

## 6. 代理配置

### JDK 动态代理

**proxy-config.json**:
```json
[
  {
    "interfaces": [
      "com.example.Service",
      "org.springframework.beans.factory.InitializingBean"
    ]
  }
]
```

---

## 7. 资源文件配置

### 包含资源文件

**resource-config.json**:
```json
{
  "resources": [
    {
      "pattern": "META-INF/services/.*"
    },
    {
      "pattern": "application\\.properties$"
    },
    {
      "pattern": "templates/.*\\.html$"
    }
  ],
  "bundles": [
    {
      "name": "messages"
    }
  ]
}
```

**使用方式**:
```bash
native-image \
  -H:ResourceConfigurationFiles=resource-config.json \
  -jar app.jar
```

---

## 8. PGO (Profile-Guided Optimization)

### 什么是 PGO?

PGO 通过收集运行时 profile 信息来优化编译。

```
┌─────────────────────────────────────────────────────────────────┐
│                    PGO 流程                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 插桩编译                                                     │
│     native-image --pgo-instrument -jar app.jar                 │
│                          ↓                                      │
│  2. 运行应用 (收集 profile)                                      │
│     ./app                                                       │
│     # 执行典型工作负载                                           │
│                          ↓                                      │
│  3. 使用 profile 重新编译                                         │
│     native-image --pgo -jar app.jar                            │
│                          ↓                                      │
│  4. 性能提升 10-15%                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### PGO 配置示例

```bash
# Step 1: 插桩编译
native-image \
  --pgo-instrument \
  -O3 \
  -jar app.jar

# Step 2: 运行工作负载
./app
# 运行典型场景，收集 branch probabilities

# Step 3: PGO 编译
native-image \
  --pgo \
  -O3 \
  --no-fallback \
  -jar app.jar

# 生成的 default.iprof 文件包含 profile 数据
```

---

## 9. 调试和故障排查

### 常见错误及解决方案

#### 错误 1: 类未找到

```
Error: Class not found: com.example.MyClass
```

**原因**: 该类通过反射访问，但未配置。

**解决**:
```bash
# 添加反射配置
-H:ReflectionConfigurationFiles=reflection-config.json
```

#### 错误 2: 方法未找到

```
Error: Method not found: com.example.MyClass.<init>()
```

**原因**: 构造函数需要反射访问。

**解决**:
```json
{
  "name": "com.example.MyClass",
  "allDeclaredConstructors": true
}
```

#### 错误 3: 资源文件未找到

```
Error: Resource not found: /config.properties
```

**原因**: 资源文件未包含在镜像中。

**解决**:
```json
{
  "resources": [
    {
      "pattern": "config\\.properties$"
    }
  ]
}
```

### 诊断选项

```bash
# 报告详细错误
native-image \
  -H:+ReportExceptionStackTraces \
  -jar app.jar

# 输出生成报告
native-image \
  -H:GenerateDebugInfo=1 \
  -H:Dump=:2 \
  -jar app.jar

# 分析构建过程
native-image \
  -H:PrintAnalysisCallTree=calltree.txt \
  -jar app.jar

# 查看包含的类
native-image \
  -H:PrintClassInitialization=classes.txt \
  -jar app.jar
```

---

## 10. 性能调优

### 启动时间优化清单

```
□ 使用 --initialize-at-build-time
□ 减少运行时初始化的类
□ 使用 --gc=Serial (内存受限时)
□ 启用 -O3 优化
□ 使用 PGO 优化
□ 减少反射使用
□ 预生成代理配置
```

### 内存优化清单

```
□ 使用 --gc=Serial
□ 设置 -H:MaximumHeapSizePercent
□ 移除未使用的依赖
□ 优化资源文件包含
□ 使用最小化配置
```

### 编译时间优化

```bash
# 使用构建缓存
native-image \
  -H:UseAnalysisCache=true \
  -H:AnalysisCachePath=/tmp/graal-cache \
  -jar app.jar

# 并行编译
native-image \
  -J-Djava.util.concurrent.ForkJoinPool.common.parallelism=4 \
  -jar app.jar
```

---

## 11. 框架特定指南

### Spring Boot 3.x

```yaml
# application.yml
spring:
  aot:
    enabled: true
```

```bash
# 使用 Spring Boot Maven Plugin
mvn -Pnative native:compile
```

### Quarkus

```properties
# application.properties
quarkus.native.enabled=true
quarkus.native.container-build=true
```

```bash
# 构建原生镜像
mvn package -Pnative
```

### Micronaut

```yaml
# application.yml
micronaut:
  application:
    name: myapp
  native:
    enabled: true
```

```bash
# 构建
mn native-image
```

---

## 12. 完整配置示例

### Spring Boot 3 应用

```bash
#!/bin/bash

# Spring Boot 3 Native Image 完整配置

native-image \
  --no-fallback \
  --gc=G1 \
  -O3 \
  --pgo \
  \
  # 初始化配置
  --initialize-at-build-time=org.springframework,com.example \
  --initialize-at-run-time=org.springframework.boot \
  \
  # 反射配置
  -H:ReflectionConfigurationFiles=reflection-config.json \
  \
  # 资源文件配置
  -H:ResourceConfigurationFiles=resource-config.json \
  \
  # 代理配置
  -H:DynamicProxyConfigurationFiles=proxy-config.json \
  \
  # JNI 配置
  -H:JNIConfigurationFiles=jni-config.json \
  \
  # 诊断输出
  -H:+ReportExceptionStackTraces \
  -H:GenerateDebugInfo=1 \
  \
  # 输出
  -H:Name=myapp \
  -jar target/myapp.jar
```

---

## 13. 相关链接

### 官方文档
- [Native Image Documentation](https://www.graalvm.org/latest/reference-manual/native-image/)
- [Configuration Guide](https://www.graalvm.org/latest/reference-manual/native-image/metadata/)

### 工具
- [Native Image Agent](https://www.graalvm.org/latest/reference-manual/native-image/metadata/AutomaticMetadataCollection/)
- [GraalVM Build Tools](https://github.com/graalvm/graalvm-buildtools)

### 框架指南
- [Spring Boot Native](https://docs.spring.io/spring-boot/docs/current/reference/html/native-image.html)
- [Quarkus Native](https://quarkus.io/guides/building-native-image)
- [Micronaut Native](https://micronaut-projects.github.io/micronaut-spring/latest/guide/index.html#native)

---

**最后更新**: 2026-03-21
