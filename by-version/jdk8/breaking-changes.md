# JDK 8 破坏性变更

> **影响评估**: 高 - 部分变更需要代码修改或配置调整

---
## 目录

1. [语言和 API 破坏性变更](#1-语言和-api-破坏性变更)
2. [JVM 和运行时破坏性变更](#2-jvm-和运行时破坏性变更)
3. [API 破坏性变更](#3-api-破坏性变更)
4. [工具和命令行变更](#4-工具和命令行变更)
5. [第三方兼容性问题](#5-第三方兼容性问题)
6. [配置和部署破坏性变更](#6-配置和部署破坏性变更)
7. [迁移检查清单](#7-迁移检查清单)
8. [回滚策略](#8-回滚策略)
9. [资源](#9-资源)

---


## 1. 语言和 API 破坏性变更

### 1. 类型推断规则变更 (JDK-8029004)

**问题描述**: JDK 8 改进了泛型方法类型推断规则，可能导致编译错误。

**示例**:
```java
// JDK 7 编译通过
List<String> list = Collections.emptyList();

// JDK 8 可能需要显式类型参数
List<String> list = Collections.<String>emptyList();
```

**影响范围**: 使用泛型方法调用的代码。

**解决方案**: 添加显式类型参数或更新编译器设置。

### 2. `javac` 更严格的编译检查

**变更**: JDK 8 的 `javac` 对某些编码模式实施更严格的检查。

**示例**:
```java
// JDK 7 允许
switch (null) { ... }

// JDK 8 编译错误: 不能切换 null
```

**影响范围**: 使用 `switch` 语句、未使用的局部变量等。

**解决方案**: 修复编译警告和错误。

### 3. 重复注解必须使用 `@Repeatable`

**变更**: JDK 8 要求重复注解声明 `@Repeatable` 元注解。

**示例**:
```java
// JDK 7 不支持重复注解
// JDK 8 需要 @Repeatable
@Repeatable(Schedules.class)
@interface Schedule {
    String time();
}

@interface Schedules {
    Schedule[] value();
}
```

**影响范围**: 自定义注解框架。

---

## 2. JVM 和运行时破坏性变更

### 4. PermGen 移除，替换为 Metaspace

**变更详情**:
- `PermGen` 内存区域完全移除
- 替换为堆外的 `Metaspace`
- 相关 JVM 参数变更

**参数映射**:
| JDK 7 参数 | JDK 8 参数 | 说明 |
|------------|------------|------|
| `-XX:PermSize` | `-XX:MetaspaceSize` | 初始大小 |
| `-XX:MaxPermSize` | `-XX:MaxMetaspaceSize` | 最大大小 |
| `-XX:PermSize` (已移除) | 无 | 不再有效 |

**影响**:
- 监控工具需要更新 (无法监控 PermGen)
- 内存溢出错误信息变化
- 性能特征变化

### 5. 默认安全管理器策略变更

**变更**: JDK 8 加强了安全性管理器默认策略。

**影响**:
- 使用 `SecurityManager` 的应用可能需要调整策略文件
- 某些操作需要显式权限

**解决方案**: 更新 `java.policy` 文件或授予必要权限。

### 6. URLClassLoader 不再搜索 `sun.*` 包

**变更**: `URLClassLoader` 默认不再搜索 `sun.*` 内部包。

**影响**: 依赖 `sun.*` 内部 API 的应用。

**解决方案**: 使用标准 API 替代，或使用 `-Xbootclasspath/a`。

---

## 3. API 破坏性变更

### 7. 集合框架默认方法冲突

**问题**: 接口默认方法可能与其他接口或类方法冲突。

**示例**:
```java
interface A {
    default void foo() { System.out.println("A"); }
}

interface B {
    default void foo() { System.out.println("B"); }
}

class C implements A, B {  // 编译错误: 冲突的默认方法
    // 必须重写 foo()
    @Override
    public void foo() { A.super.foo(); }
}
```

**影响范围**: 实现多个接口的类。

### 8. `java.util.Date` 相关 API 行为微调

**变更**: `java.util.Date` 的 `toString()` 格式微调，`parse()` 方法更严格。

**影响**: 日期解析和格式化代码。

### 9. `Locale` 数据更新

**变更**: Unicode CLDR 数据更新，可能导致本地化行为变化。

**影响**: 国际化应用。

---

## 4. 工具和命令行变更

### 10. `javac` 默认源和目标版本

**变更**: `javac` 默认生成 JDK 8 字节码。

**影响**: 需要兼容旧版本的应用。

**解决方案**: 使用 `-source` 和 `-target` 选项。

### 11. `java` 命令行参数解析变更

**变更**: 某些 JVM 参数格式更严格。

**示例**:
```bash
# JDK 7 可能允许
-XX:MaxPermSize=256M

# JDK 8 需要正确单位
-XX:MaxMetaspaceSize=256m
```

**影响**: 启动脚本和配置。

### 12. 监控工具变更

**变更**:
- `jmap -permstat` 移除
- `jstat -gcpermcapacity` 移除

**替代方案**:
- 使用 `jstat -gcmetacapacity` 监控 Metaspace
- 使用 `jcmd` 新命令

---

## 5. 第三方兼容性问题

### 13. 反射访问限制

**变更**: JDK 8 加强了模块边界，反射访问内部 API 可能受限。

**影响**: 使用反射访问 `sun.*` 或 `com.sun.*` 包的应用。

**解决方案**: 使用 `--add-opens` 命令行选项 (JDK 9+)，或重构代码。

### 14. 字节码操作库兼容性

**影响库**:
- ASM: 需要 5.0+ 版本
- Javassist: 需要 3.20+ 版本
- CGLIB: 需要 3.2+ 版本

**解决方案**: 更新依赖版本。

### 15. 序列化兼容性

**变更**: `java.io.ObjectInputStream` 对反序列化进行额外检查。

**影响**: 自定义序列化代码。

---

## 6. 配置和部署破坏性变更

### 16. 安装目录结构变更

**变更**: Oracle JDK 安装目录结构变化。

**影响**: 部署脚本和安装程序。

### 17. 浏览器插件变更

**变更**: Java 浏览器插件架构变更。

**影响**: Applet 应用。

**解决方案**: 考虑迁移到 Web Start 或其他技术。

### 18. 字体渲染变更

**变更**: 字体渲染引擎更新。

**影响**: 图形界面应用的外观。

---

## 7. 迁移检查清单

### 必须检查的项目

1. **内存配置**:
   - [ ] 更新 PermGen 参数为 Metaspace
   - [ ] 调整 GC 参数 (如果使用 G1)

2. **编译检查**:
   - [ ] 使用 JDK 8 编译器重新编译
   - [ ] 修复所有编译警告

3. **第三方依赖**:
   - [ ] 检查库的 JDK 8 兼容性
   - [ ] 更新不兼容的库

4. **监控工具**:
   - [ ] 更新 JVM 监控配置
   - [ ] 测试监控工具

### 建议检查的项目

1. **性能测试**:
   - [ ] 基准测试性能变化
   - [ ] 监控内存使用模式

2. **安全测试**:
   - [ ] 验证安全管理器策略
   - [ ] 测试 TLS/SSL 连接

3. **兼容性测试**:
   - [ ] 回归测试所有功能
   - [ ] 测试边缘情况

---

## 8. 回滚策略

### 如果遇到问题

1. **临时解决方案**:
   - 使用兼容性参数
   - 降级到 JDK 7

2. **长期解决方案**:
   - 分析根本原因
   - 实施永久修复

### 紧急修复选项

1. **JVM 参数调整**:
```bash
# 兼容性参数示例
-XX:+IgnoreUnrecognizedVMOptions  # 忽略无法识别的参数
-Djava.security.manager=allow     # 宽松安全管理器
```

2. **代码热修复**:
   - 使用条件代码 (版本检测)
   - 动态加载替代实现

---

## 9. 资源

### 官方文档
- [JDK 8 兼容性指南](https://docs.oracle.com/javase/8/docs/technotes/guides/compatibility/index.html)
- [已知问题列表](https://bugs.openjdk.org/browse/JDK-8000)

### 诊断工具
- `jdeprscan`: 扫描废弃 API 使用
- `jdeps`: 分析依赖关系

### 社区支持
- [OpenJDK 邮件列表](https://mail.openjdk.org/mailman/listinfo)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/java-8+migration)