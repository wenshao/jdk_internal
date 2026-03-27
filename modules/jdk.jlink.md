---

# jdk.jlink 模块分析

> jlink — Java 链接器，用于创建自定义运行时镜像

---

## 1. 模块定义

**源文件**: `src/jdk.jlink/share/classes/module-info.java`

```
module jdk.jlink {
    requires jdk.internal.opt;
    requires jdk.jdeps;

    uses jdk.tools.jlink.plugin.Plugin;

    exports jdk.tools.jlink.builder;
    exports jdk.tools.jlink.plugin;
}
```

### 核心包

| 包 | 用途 |
|---|---|
| `jdk.tools.jlink.builder` | 运行时镜像构建器 |
| `jdk.tools.jlink.plugin` | jlink 插件 API |

---

## 2. 核心功能

### 2.1 jlink 工作流程

```
┌──────────────────────────────────────────────────────────┐
│                    jlink 工作流程                         │
│                                                          │
│  ┌──────────┐     ┌──────────┐     ┌──────────────┐    │
│  │ 模块路径  │────►│ 模块解析  │────►│ 字节码优化   │    │
│  │ (jmods)  │     │ (依赖图) │     │ (Plugin 链) │    │
│  └──────────┘     └──────────┘     └──────┬───────┘    │
│                                           │             │
│  ┌──────────┐     ┌──────────┐     ┌──────▼───────┐    │
│  │ 原生启动器 │────►│ 运行时镜像 │◄────┤ 资源打包    │    │
│  │ (bin/java)│     │ (jre)    │     │ (resources) │    │
│  └──────────┘     └──────────┘     └──────────────┘    │
└──────────────────────────────────────────────────────────┘
```

### 2.2 基本用法

```bash
# 创建包含 java.base 模块的最小运行时
jlink --module-path $JAVA_HOME/jmods \
      --add-modules java.base \
      --output custom-jre

# 查看镜像大小
du -sh custom-jre/
# 约 40-50MB (vs 完整 JDK ~300MB)
```

### 2.3 常用场景

```bash
# 场景 1: Spring Boot + 特定模块
jlink --module-path app.jar:$JAVA_HOME/jmods \
      --add-modules com.example.app,java.sql,java.naming \
      --output app-runtime

# 场景 2: 压缩镜像
jlink --module-path $JAVA_HOME/jmods \
      --add-modules java.base,java.logging \
      --compress=2 \
      --strip-debug \
      --no-header-files \
      --no-man-pages \
      --output minimal-jre

# 场景 3: 包含服务提供者
jlink --module-path $JAVA_HOME/jmods \
      --add-modules java.base,java.sql \
      --bind-services \
      --output jre-with-drivers
```

---

## 3. 内置插件

jlink 使用插件管道（Plugin Pipeline）对模块进行转换：

| 插件 | 说明 | 选项 |
|------|------|------|
| `compress` | 压缩资源 | `--compress={0,1,2}` |
| `strip-debug` | 移除调试信息 | `--strip-debug` |
| `strip-native-commands` | 移除原生工具 | `--strip-native-commands` |
| `no-man-pages` | 移除 man 页面 | `--no-man-pages` |
| `no-header-files` | 移除头文件 | `--no-header-files` |
| `include-locales` | 包含指定 Locale | `--include-locales=en,zh` |
| `order-resources` | 资源排序优化 | `--order-resources=...` |
| `exclude-files` | 排除文件 | `--exclude-files=*.diz` |
| `exclude-resources` | 排除资源 | `--exclude-resources=**/javax/**` |
| `generate-cds` | 生成 CDS 归档 | `--generate-cds-archive` |
| `vm-options` | 设置默认 VM 选项 | -- |

### 压缩级别

| 级别 | 方法 | 压缩率 | 启动速度 |
|------|------|--------|---------|
| 0 | 不压缩 | 0% | 最快 |
| 1 | 共享字符串常量 | ~10% | 快 |
| 2 | ZIP 压缩 | ~30-40% | 略慢（需解压） |

---

## 4. 模块分辨率

### 4.1 依赖图分析

```bash
# 查看模块依赖
jdeps --module-path $JAVA_HOME/jmods \
      --list-deps app.jar

# 输出示例:
#   java.base
#   java.sql
#   java.logging
#   java.naming

# 生成模块图
jdeps --module-path $JAVA_HOME/jmods \
      --generate-module-info . app.jar
```

### 4.2 可读性图

```bash
# 查看 java.sql 的依赖
jlink --module-path $JAVA_HOME/jmods \
      --add-modules java.sql \
      --suggest-providers java.sql.Driver
```

---

## 5. 与容器镜像集成

### 5.1 Docker 多阶段构建

```dockerfile
# Stage 1: 使用 jlink 创建自定义 JRE
FROM eclipse-temurin:21 AS builder
WORKDIR /app
COPY target/app.jar .
RUN jlink --module-path $JAVA_HOME/jmods \
          --add-modules java.base,java.sql,java.logging,java.naming,java.management \
          --compress=2 \
          --strip-debug \
          --no-header-files \
          --no-man-pages \
          --output /custom-jre

# Stage 2: 使用自定义 JRE 运行
FROM debian:bookworm-slim
COPY --from=builder /custom-jre /opt/jre
COPY --from=builder /app/app.jar /app.jar
ENTRYPOINT ["/opt/jre/bin/java", "-jar", "/app.jar"]
```

### 5.2 镜像大小对比

| 运行时 | 大小 |
|--------|------|
| 完整 JDK 21 | ~480MB |
| 完整 JRE 21 | ~200MB |
| jlink (java.base) | ~45MB |
| jlink (java.base + 常用模块) | ~70MB |
| jlink + compress=2 | ~50MB |
| GraalVM Native Image | ~30-60MB |

---

## 6. 自定义插件

```java
// 自定义 jlink 插件
public class CustomPlugin implements Plugin {
    @Override
    public String getName() {
        return "custom-plugin";
    }

    @Override
    public ResourcePool transform(ResourcePool in, ResourcePoolBuilder out) {
        in.transformAndCopy(resource -> {
            // 自定义转换逻辑
            return resource;
        }, out);
        return out.build();
    }
}

// 注册: META-INF/services/jdk.tools.jlink.plugin.Plugin
```

---

## 7. 常见问题

| 问题 | 解决方案 |
|------|---------|
| `module not found` | 检查 `--module-path` 是否包含 jmods 目录 |
| 镜像缺少类 | 使用 `--bind-services` 或手动添加缺失模块 |
| SPI 服务不工作 | 使用 `--bind-services` 包含服务提供者 |
| 启动报 `ClassNotFoundException` | 用 `jdeps` 分析依赖，添加缺失模块 |
| 镜像过大 | 使用 `--compress=2 --strip-debug` |

---

## 8. 相关链接

- [模块系统主题](/by-topic/core/modules/)
- [启动优化案例](/cases/startup-optimization.md)
- [java.base 模块分析](java.base.md)
