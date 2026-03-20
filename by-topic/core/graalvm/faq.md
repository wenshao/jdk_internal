# GraalVM 常见问题 (FAQ)

> 关于 GraalVM 的常见问题和解答

[← 返回 GraalVM 首页](./)

---

## 目录

1. [基础问题](#基础问题)
2. [性能相关](#性能相关)
3. [Native Image](#native-image)
4. [多语言支持](#多语言支持)
5. [故障排查](#故障排查)
6. [最佳实践](#最佳实践)

---

## 基础问题

### Q1: GraalVM 是什么？

**A**: GraalVM 是 Oracle Labs 开发的高性能 JDK 发行版，基于 OpenJDK，主要特性包括：

- **Graal JIT**: 用 Java 编写的高性能编译器
- **Native Image**: AOT 编译为原生可执行文件
- **Truffle**: 多语言运行时框架

### Q2: GraalVM 和 OpenJDK 有什么区别？

| 特性 | OpenJDK | GraalVM |
|------|---------|---------|
| JIT 编译器 | C1 + C2 | C1 + Graal |
| AOT 编译 | 有限 (CDS) | Native Image |
| 多语言 | 不支持 | Truffle 支持 |
| 启动时间 | 秒级 | 毫秒级 (NI) |
| 许可证 | GPLv2+CE | GPLv2+CE / GFTC |

### Q3: GraalVM 是免费的吗？

**A**: 是的，GraalVM Community Edition (CE) 是免费的，基于 GPLv2+CE 许可证。

Enterprise Edition (EE) 需要付费，包含额外功能和支持。

### Q4: 如何安装 GraalVM？

```bash
# 使用 SDKMAN (推荐)
sdk install java 21-graal
sdk use java 21-graal

# 验证安装
java -version
```

### Q5: GraalVM 支持哪些 JDK 版本？

| GraalVM 版本 | JDK 基线 | 支持周期 |
|--------------|----------|----------|
| GraalVM 22 | JDK 17 | 至 2029 |
| GraalVM 24 | JDK 21 | 至 2031 |
| GraalVM 25 | JDK 24 | 至 2027 |

---

## 性能相关

### Q6: GraalVM 比 HotSpot 快多少？

**A**: 取决于工作负载：

| 场景 | 性能差异 |
|------|----------|
| **启动时间 (Native Image)** | 快 90-95% |
| **峰值性能 (Graal JIT)** | 快 5-10% |
| **内存占用 (Native Image)** | 少 70-80% |

详细数据见 [性能基准测试](benchmarks.md)。

### Q7: 为什么 Graal JIT 启动更慢？

**A**: Graal 编译器本身更复杂，需要更多初始化时间。但 Native Image 可以解决这个问题。

```
启动时间对比:
├─ HotSpot C2:  100ms
├─ Graal JIT:   110ms (+10%)
└─ Native Image: 5ms (-95%)
```

### Q8: 什么时候应该使用 Native Image？

**A**: 以下场景推荐 Native Image：

✅ **推荐**:
- 微服务/云原生应用
- Serverless 函数
- CLI 工具
- 启动时间敏感场景

❌ **不推荐**:
- 需要动态类加载
- 大量使用反射
- 短测试脚本

### Q9: GraalVM 内存占用更高吗？

**A**: Graal JIT 模式内存占用高约 20%，但 Native Image 内存占用低 70-80%。

```
内存对比 (微服务):
├─ HotSpot:    200MB
├─ Graal JIT:  230MB (+15%)
└─ Native Image: 50MB (-75%)
```

---

## Native Image

### Q10: Native Image 的原理是什么？

**A**: Native Image 使用**静态分析**在构建时将 Java 字节码编译为原生机器码。

```
传统 JVM:                    Native Image:
Java 源码 → .class → JVM     Java 源码 → .class → 原生可执行文件
                              (构建时编译)
```

### Q11: 如何构建 Native Image？

```bash
# 1. 安装组件
gu install native-image

# 2. 编译
native-image -jar myapp.jar

# 3. 运行
./myapp
```

### Q12: 为什么我的应用无法构建 Native Image？

**A**: 常见原因：

1. **反射未配置**
   ```bash
   # 使用 agent 自动生成配置
   java -agentlib:native-image-agent=config-output-dir=config/ \
        -jar app.jar
   ```

2. **动态类加载**
   - Native Image 不支持运行时类加载
   - 需要使用构建时初始化

3. **JNI 调用**
   - 需要 JNI 配置文件

详细配置见 [Native Image 指南](native-image-guide.md)。

### Q13: Native Image 支持动态代理吗？

**A**: 支持，但需要配置。

```json
// proxy-config.json
[
  {
    "interfaces": [
      "com.example.Service",
      "java.lang.reflect.InvocationHandler"
    ]
  }
]
```

```bash
native-image -H:DynamicProxyConfigurationFiles=proxy-config.json
```

### Q14: 如何优化 Native Image 启动时间？

**A**: 

```bash
# 1. 构建时初始化
native-image --initialize-at-build-time -jar app.jar

# 2. 使用 PGO 优化
native-image --pgo-instrument -jar app.jar
./app  # 运行工作负载
native-image --pgo -jar app.jar

# 3. 减少反射使用
# 4. 优化依赖
```

### Q15: Native Image 支持 GC 吗？

**A**: 支持，可选 GC 包括：

| GC | 参数 | 适用场景 |
|----|------|----------|
| **Serial** | `--gc=Serial` | 内存受限 |
| **G1** | `--gc=G1` | 生产环境 |
| **Epsilon** | `--gc=epsilon` | 无 GC 场景 |

---

## 多语言支持

### Q16: GraalVM 支持哪些语言？

| 语言 | Community | Enterprise | 状态 |
|------|-----------|------------|------|
| **Java** | ✅ | ✅ | 生产就绪 |
| **JavaScript** | ✅ | ✅ | 生产就绪 |
| **Python** | ❌ | ✅ | 实验性 |
| **Ruby** | ❌ | ✅ | 实验性 |
| **R** | ❌ | ✅ | 实验性 |
| **LLVM** | ❌ | ✅ | 实验性 |
| **WebAssembly** | ✅ | ✅ | 实验性 |

### Q17: 如何在 Java 中运行 Python 代码？

```java
import org.graalvm.polyglot.*;

try (Context context = Context.create()) {
    // 执行 Python 代码
    Value result = context.eval("python", "1 + 2");
    System.out.println(result.asInt());  // 3
    
    // 调用 Python 函数
    context.eval("python", """
        def greet(name):
            return f"Hello, {name}!"
    """);
    Value greet = context.getBindings("python").getMember("greet");
    String greeting = greet.execute("World").asString();
}
```

### Q18: GraalVM 的多语言性能如何？

**A**: 

| 语言 | 相对 CPython/V8 | 说明 |
|------|-----------------|------|
| **JavaScript** | 60-80% of V8 | 接近 Node.js |
| **Python** | 50-150% of CPython | 数值计算更快 |
| **Ruby** | 5-10x of MRI | 显著快于 Ruby |

---

## 故障排查

### Q19: 如何启用 Graal JIT 日志？

```bash
java -XX:+UnlockExperimentalVMOptions \
     -XX:+EnableJVMCI \
     -XX:+UseJVMCICompiler \
     -Dgraal.LogFile=graal.log \
     -Dgraal.LogLevel=INFO \
     -jar app.jar
```

### Q20: Native Image 构建失败，如何调试？

```bash
# 1. 启用详细日志
native-image --verbose -jar app.jar

# 2. 报告详细错误
native-image -H:+ReportExceptionStackTraces -jar app.jar

# 3. 输出分析树
native-image -H:PrintAnalysisCallTree=calltree.txt -jar app.jar

# 4. 查看包含的类
native-image -H:PrintClassInitialization=classes.txt -jar app.jar
```

### Q21: 遇到 "Class not found" 错误怎么办？

**A**: 这是反射问题，需要添加反射配置。

```bash
# 方法 1: 使用 agent 自动生成
java -agentlib:native-image-agent=config-output-dir=config/ \
     -jar app.jar

# 方法 2: 手动配置
native-image -H:ReflectionConfigurationFiles=reflection-config.json \
     -jar app.jar
```

### Q22: 如何查看 Native Image 包含哪些类？

```bash
# 生成类列表
native-image -H:PrintClassInitialization=classes.txt -jar app.jar

# 查看 call tree
native-image -H:PrintAnalysisCallTree=calltree.txt -jar app.jar
```

### Q23: 应用运行时崩溃，如何排查？

```bash
# 1. 启用核心转储
ulimit -c unlimited

# 2. 使用 GDB 调试
gdb ./app
(gdb) run
(gdb) bt  # 崩溃时查看堆栈

# 3. 使用 Native Image 调试工具
native-image --debug-attach -jar app.jar
```

---

## 最佳实践

### Q24: 生产环境应该使用哪个版本？

**A**: 

| 场景 | 推荐 |
|------|------|
| **微服务** | GraalVM Native Image |
| **长运行服务** | GraalVM JIT 或 OpenJDK |
| **云原生** | GraalVM Native Image |
| **大数据** | OpenJDK (更成熟) |

### Q25: 如何选择 GraalVM 版本？

**A**: 选择与你的 JDK 版本匹配的 GraalVM：

| JDK 版本 | 推荐 GraalVM |
|----------|--------------|
| JDK 17 | GraalVM 22.x |
| JDK 21 | GraalVM 24.x |
| JDK 24 | GraalVM 25.x |

### Q26: 如何在 Docker 中使用 GraalVM？

```dockerfile
# 构建阶段
FROM ghcr.io/graalvm/native-image-community:21 AS build
COPY . /app
WORKDIR /app
RUN native-image -jar app.jar

# 运行阶段
FROM gcr.io/distroless/base-debian12
COPY --from=build /app/app /app
ENTRYPOINT ["/app"]
```

### Q27: 如何在 CI/CD 中构建 Native Image？

```yaml
# GitHub Actions 示例
name: Build Native Image

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup GraalVM
        uses: graalvm/setup-graalvm@v1
        with:
          java-version: '21'
          distribution: 'graalvm'
          native-image-job: true
      
      - name: Build
        run: |
          mvn package
          native-image -jar target/app.jar
      
      - name: Test
        run: ./app &
```

### Q28: GraalVM 适合我的项目吗？

```
决策流程:

你的应用是...?
    │
    ├─ 微服务/云原生？
    │   └─ → GraalVM Native Image ✅
    │
    ├─ 长运行服务？
    │   ├─ 需要峰值性能 → GraalVM JIT ✅
    │   └─ 稳定性优先 → OpenJDK ✅
    │
    ├─ 多语言应用？
    │   └─ → GraalVM + Truffle ✅
    │
    ├─ CLI 工具？
    │   └─ → GraalVM Native Image ✅
    │
    └─ 大数据处理？
        └─ → OpenJDK (更成熟) ✅
```

---

## 相关资源

### 官方文档
- [GraalVM 官网](https://www.graalvm.org/)
- [官方文档](https://www.graalvm.org/latest/docs/)
- [GitHub](https://github.com/oracle/graal)

### 社区支持
- [Stack Overflow](https://stackoverflow.com/questions/tagged/graalvm)
- [GraalVM Slack](https://graalvm.slack.com/)
- [Mailing List](mailto:graalvm-dev@openjdk.org)

### 学习资源
- [GraalVM 参考手册](https://www.graalvm.org/latest/reference-manual/)
- [Native Image 指南](native-image-guide.md)
- [性能优化](performance.md)

---

**最后更新**: 2026-03-21

**还有问题？** 欢迎在 GitHub 提 Issue 或邮件列表提问。
