# JDK 11 破坏性变更

> **影响评估**: 高 - 由于模块系统和API移除，需要代码修改和依赖调整

---

## 模块系统相关破坏性变更

### 1. Java EE 和 CORBA 模块移除 (JEP 320)

**变更详情**: JDK 11 移除了以下 Java EE 和 CORBA 模块：
- `java.activation` (JAF)
- `java.corba` (CORBA)
- `java.transaction` (JTA)
- `java.xml.bind` (JAXB)
- `java.xml.ws` (JAX-WS)
- `java.xml.ws.annotation` (Common Annotations)

**错误信息**:
```bash
Error: module not found: java.xml.bind
Error: package javax.activation does not exist
```

**解决方案**:
```xml
<!-- Maven 依赖 -->
<dependency>
    <groupId>javax.xml.bind</groupId>
    <artifactId>jaxb-api</artifactId>
    <version>2.3.1</version>
</dependency>
<dependency>
    <groupId>com.sun.xml.bind</groupId>
    <artifactId>jaxb-impl</artifactId>
    <version>2.3.1</version>
</dependency>
<dependency>
    <groupId>javax.activation</groupId>
    <artifactId>javax.activation-api</artifactId>
    <version>1.2.0</version>
</dependency>
```

### 2. 模块封装强化

**变更**: 非导出包无法通过反射访问。

**错误示例**:
```java
// 尝试访问内部 API
Field field = sun.misc.Unsafe.class.getDeclaredField("theUnsafe");
// JDK 11: InaccessibleObjectException
```

**解决方案**:
```bash
# 添加 --add-opens 参数
java --add-opens java.base/sun.misc=ALL-UNNAMED -jar app.jar

# 或者使用模块声明
module my.app {
    opens my.package to java.base;
}
```

### 3. 扩展机制移除

**变更**: `java.ext.dirs` 系统属性不再有效。

**影响**: 通过扩展目录加载的库无法工作。

**解决方案**: 使用类路径或模块路径。

---

## API 移除和废弃

### 4. Nashorn JavaScript 引擎废弃 (JEP 335)

**变更**: Nashorn 引擎标记为废弃，计划在未来版本中移除。

**影响代码**:
```java
// 使用 Nashorn
ScriptEngine engine = new ScriptEngineManager().getEngineByName("nashorn");
engine.eval("print('Hello Nashorn')");
```

**替代方案**:
- **GraalVM JavaScript**: 性能更好，支持 ES6+
- **迁移到其他语言**: 考虑使用 Kotlin Script 或 Groovy
- **使用 javax.script 的其他引擎**: Rhino (较老)

### 5. Pack200 工具和 API 废弃 (JEP 336)

**变更**: Pack200 压缩工具标记为废弃。

**影响**: 
- `java.util.jar.Pack200` API
- `pack200` 和 `unpack200` 命令行工具

**替代方案**: 使用标准压缩算法 (如 gzip)。

### 6. 已移除的内部 API

**已移除的 `sun.misc` 类**:
- `sun.misc.BASE64Encoder` / `sun.misc.BASE64Decoder`
- `sun.misc.Unsafe` 的部分方法受限访问

**替代方案**:
```java
// 替代 BASE64Encoder
import java.util.Base64;
Base64.Encoder encoder = Base64.getEncoder();
String encoded = encoder.encodeToString(data);

// 替代 Unsafe，使用标准 API
VarHandle handles = MethodHandles.arrayElementVarHandle(byte[].class);
```

### 7. 已移除的 `java.awt.peer` 包

**变更**: `java.awt.peer` 包完全移除。

**影响**: 依赖于 AWT 对等接口的 GUI 应用。

**解决方案**: 使用跨平台 GUI 框架或迁移到 JavaFX。

---

## 工具和命令行变更

### 8. JavaFX 分离

**变更**: JavaFX 从 JDK 中分离，需要单独下载。

**影响**: 使用 JavaFX 的应用无法直接运行。

**解决方案**:
```xml
<!-- Maven 依赖 -->
<dependency>
    <groupId>org.openjfx</groupId>
    <artifactId>javafx-controls</artifactId>
    <version>11.0.2</version>
</dependency>
```

```bash
# 运行时需要模块路径
java --module-path /path/to/javafx-sdk-11/lib \
     --add-modules javafx.controls \
     -jar myapp.jar
```

### 9. `java -version` 输出格式变更

**变更**: 版本字符串格式更新，可能影响版本检测脚本。

**JDK 8 格式**:
```
java version "1.8.0_301"
Java(TM) SE Runtime Environment (build 1.8.0_301-b09)
Java HotSpot(TM) 64-Bit Server VM (build 25.301-b09, mixed mode)
```

**JDK 11 格式**:
```
openjdk version "11.0.13" 2021-10-19
OpenJDK Runtime Environment (build 11.0.13+8)
OpenJDK 64-Bit Server VM (build 11.0.13+8, mixed mode)
```

### 10. JVM TI 和 JVMTI 变更

**变更**: 某些 JVM Tool Interface 函数签名变更。

**影响**: 本地代理和监控工具。

**解决方案**: 重新编译本地库，更新 JVM TI 版本。

---

## 安全相关破坏性变更

### 11. TLS 1.0 和 1.1 默认禁用

**变更**: TLS 1.0 和 1.1 默认禁用，只启用 TLS 1.2+。

**影响**: 连接旧服务器可能失败。

**解决方案**:
```bash
# 临时启用旧协议 (不推荐)
-Djdk.tls.client.protocols=TLSv1,TLSv1.1,TLSv1.2,TLSv1.3

# 长期方案: 升级服务器支持 TLS 1.2+
```

### 12. 弱加密算法禁用

**已禁用的算法**:
- RC4 流密码
- DES 加密 (部分模式)
- MD5 和 SHA-1 签名 (部分用途)

**错误信息**:
```
javax.net.ssl.SSLHandshakeException: No appropriate protocol
```

### 13. 安全性管理器策略变更

**变更**: 默认策略更严格，某些操作需要显式权限。

**影响**: 使用 `SecurityManager` 的应用。

**解决方案**: 更新策略文件或授予必要权限。

---

## 构建和部署破坏性变更

### 14. 类文件版本变更

**变更**: 类文件版本从 52 (JDK 8) 升级到 55 (JDK 11)。

**影响**: JDK 11 编译的类不能在 JDK 8 上运行。

**解决方案**:
```xml
<!-- Maven 编译目标 -->
<properties>
    <maven.compiler.source>8</maven.compiler.source>
    <maven.compiler.target>8</maven.compiler.target>
    <!-- 使用 release 选项 -->
    <maven.compiler.release>8</maven.compiler.release>
</properties>
```

### 15. 启动脚本变更

**废弃的 JVM 参数**:
- `-XX:+AggressiveOpts`: 使用默认优化
- `-XX:+UseConcMarkSweepGC`: 使用 G1 或 ZGC
- `-Xincgc`: 使用 G1 GC

**新参数**:
```bash
# 容器支持
-XX:+UseContainerSupport
-XX:MaxRAMPercentage=75.0

# 统一日志
-Xlog:gc*,safepoint:file=gc.log:time,level,tags
```

### 16. 监控工具变更

**变更**:
- `jmap -permstat` 已移除 (Metaspace 替代 PermGen)
- `jstat -gcpermcapacity` 已移除

**替代方案**:
```bash
# 监控 Metaspace
jstat -gcmetacapacity <pid>

# 使用 jcmd
jcmd <pid> GC.metaspace
```

---

## 第三方库兼容性问题

### 17. 常见库的 JDK 11 兼容性

| 库/框架 | 最小兼容版本 | 说明 |
|---------|--------------|------|
| Spring Framework | 5.1+ | 需要 Spring 5.x |
| Hibernate | 5.4+ | 需要更新版本 |
| Log4j | 2.11+ | Log4j 1.x 不兼容 |
| Jackson | 2.10+ | 需要较新版本 |
| JUnit | 5.4+ | JUnit 4 可能有问题 |

### 18. 反射库兼容性

**影响库**:
- **ASM**: 需要 7.0+ 版本
- **Javassist**: 需要 3.25+ 版本  
- **CGLIB**: 需要 3.2.10+ 版本

**解决方案**: 更新依赖版本。

### 19. 序列化兼容性

**变更**: `java.io.ObjectInputStream` 对反序列化进行额外检查。

**影响**: 自定义序列化代码。

**错误示例**:
```
java.io.InvalidClassException: filter status: REJECTED
```

**解决方案**: 实现 `ObjectInputFilter` 或使用安全反序列化库。

---

## 迁移检查清单

### 必须检查的项目

1. **模块化兼容性**:
   - [ ] 检查 Java EE 模块使用
   - [ ] 更新依赖添加缺失模块
   - [ ] 测试反射访问内部 API

2. **API 兼容性**:
   - [ ] 扫描 Nashorn 使用
   - [ ] 替换已移除的 `sun.misc` API
   - [ ] 更新 JavaFX 应用

3. **安全配置**:
   - [ ] 测试 TLS 连接
   - [ ] 更新加密算法
   - [ ] 验证安全性管理器策略

4. **构建配置**:
   - [ ] 更新编译目标版本
   - [ ] 检查第三方库兼容性
   - [ ] 更新构建工具版本

### 建议检查的项目

1. **性能测试**:
   - [ ] 基准测试性能变化
   - [ ] 监控内存使用模式
   - [ ] 测试 GC 行为

2. **监控工具**:
   - [ ] 更新监控配置
   - [ ] 测试诊断工具
   - [ ] 验证日志格式

---

## 紧急修复选项

### 如果遇到模块问题

```bash
# 临时解决方案: 使用类路径模式
java --class-path app.jar:lib/* com.example.Main

# 添加缺失模块
java --add-modules java.xml.bind,java.activation -jar app.jar

# 开放内部 API 访问
java --add-opens java.base/sun.misc=ALL-UNNAMED \
     --add-opens java.base/java.lang=ALL-UNNAMED \
     -jar app.jar
```

### 如果遇到安全连接问题

```bash
# 临时启用旧协议
java -Djdk.tls.client.protocols=TLSv1,TLSv1.1,TLSv1.2,TLSv1.3 \
     -jar app.jar

# 启用弱算法 (不推荐)
java -Djdk.tls.disabledAlgorithms= \
     -jar app.jar
```

### 如果遇到启动问题

```bash
# 忽略无法识别的参数
java -XX:+IgnoreUnrecognizedVMOptions \
     -jar app.jar

# 使用兼容性模式
java -XX:+UseG1GC \
     -XX:MaxGCPauseMillis=200 \
     -jar app.jar
```

---

## 资源

### 诊断工具

1. **jdeps**: 依赖分析
```bash
# 分析模块依赖
jdeps --multi-release 11 --ignore-missing-deps app.jar

# 检查内部 API 使用
jdeps -jdkinternals app.jar
```

2. **jdeprscan**: 废弃 API 扫描
```bash
# 扫描已移除的 API
jdeprscan --release 11 --for-removal app.jar
```

3. **jlink**: 创建自定义运行时
```bash
# 创建包含所需模块的运行时
jlink --module-path $JAVA_HOME/jmods:mods \
      --add-modules java.base,java.xml.bind,java.activation \
      --output custom-jre
```

### 文档资源

- [JDK 11 迁移指南](https://docs.oracle.com/en/java/javase/11/migrate/)
- [模块系统快速入门](https://openjdk.org/projects/jigsaw/quick-start)
- [Java Platform Module System](https://openjdk.org/projects/jigsaw/)

### 社区支持

- [OpenJDK 迁移讨论](https://mail.openjdk.org/mailman/listinfo/migration-dev)
- [Stack Overflow: java-11-migration](https://stackoverflow.com/questions/tagged/java-11+migration)
- [Java Champions 博客](https://inside.java/)