# JDK 25 破坏性变更

> **版本**: JDK 25 (LTS) | **发布日期**: 2025-09-16

---
## 目录

1. [变更总览](#1-变更总览)
2. [32-bit x86 端口移除](#2-32-bit-x86-端口移除)
3. [String Templates 撤销](#3-string-templates-撤销)
4. [Security Manager 进一步限制](#4-security-manager-进一步限制)
5. [其他行为变更](#5-其他行为变更)
6. [检测与迁移工具](#6-检测与迁移工具)
7. [相关链接](#7-相关链接)

---


## 1. 变更总览

| 变更 | JEP | 影响范围 | 严重程度 | 迁移难度 |
|------|-----|----------|----------|----------|
| 移除 32-bit x86 端口 | JEP 503 | 32 位 x86 用户 | 🔴 高 | 中 |
| String Templates 撤销 | - | 使用了预览版的代码 | 🟡 中 | 低 |
| Security Manager 限制 | - | 依赖 SM 的应用 | 🟡 中 | 高 |
| 偏向锁完全移除 | - | 依赖偏向锁的性能调优 | 🟢 低 | 低 |

---

## 2. 32-bit x86 端口移除

### JEP 503: Remove the 32-bit x86 Port

**影响**: 无法在 32 位 x86 平台上构建或运行 JDK 25。

**受影响的用户**:
- 仍在使用 32 位操作系统的嵌入式设备
- 遗留的 32 位 Windows 应用

**检测**:
```bash
# 检查当前 JDK 架构
java -XshowSettings:vm 2>&1 | grep "VM"

# 检查操作系统位数
uname -m  # x86_64 = 64位, i686 = 32位
```

**迁移建议**:
1. 升级到 64 位操作系统和 JDK
2. 如果必须使用 32 位，停留在 JDK 24 或更早版本
3. 考虑使用交叉编译方案

---

## 3. String Templates 撤销

### 背景

String Templates (JEP 430) 在 JDK 21 和 JDK 22 中作为预览特性引入，但在社区反馈后被撤销，正在重新设计。

**影响**: 使用了 `STR."..."` 或 `FMT."..."` 语法的代码无法编译。

**检测**:
```bash
# 搜索 String Templates 用法
grep -rn 'STR\."' src/
grep -rn 'FMT\."' src/
grep -rn 'RAW\."' src/
```

**迁移方案**:

```java
// ❌ JDK 21-22 预览版写法（不再可用）
// String msg = STR."Hello \{name}, you are \{age} years old";

// ✅ 替代方案 1: String.format
String msg = String.format("Hello %s, you are %d years old", name, age);

// ✅ 替代方案 2: 字符串拼接
String msg = "Hello " + name + ", you are " + age + " years old";

// ✅ 替代方案 3: MessageFormat
String msg = MessageFormat.format("Hello {0}, you are {1} years old", name, age);
```

---

## 4. Security Manager 进一步限制

### 背景

Security Manager 自 JDK 17 (JEP 411) 起被标记为废弃，JDK 25 进一步限制了其功能。

**影响**:
- `System.setSecurityManager()` 在默认配置下抛出 `UnsupportedOperationException`
- 需要显式 JVM 参数才能启用

**检测**:
```bash
# 搜索 Security Manager 用法
grep -rn 'SecurityManager' src/
grep -rn 'setSecurityManager' src/
grep -rn 'getSecurityManager' src/
grep -rn 'java.security.policy' src/
```

**迁移建议**:

| 原有用途 | 替代方案 |
|----------|----------|
| 限制文件访问 | 操作系统级别权限、容器隔离 |
| 限制网络访问 | 防火墙规则、网络策略 |
| 限制类加载 | 模块系统 (JPMS) 强封装 |
| 沙箱执行 | ProcessBuilder 进程隔离、容器 |

```java
// ❌ 旧方式
System.setSecurityManager(new SecurityManager());

// ✅ 替代：使用 JPMS 模块封装
// module-info.java
module myapp {
    requires java.base;
    // 不导出内部包，实现封装
}
```

---

## 5. 其他行为变更

### 偏向锁完全移除

JDK 15 (JEP 374) 废弃偏向锁，JDK 25 完全移除相关代码。

**影响**: `-XX:+UseBiasedLocking` 参数被忽略。

```bash
# 检查 JVM 参数
grep -rn 'UseBiasedLocking' scripts/ config/
```

**迁移**: 删除 `UseBiasedLocking` 相关参数即可。现代 JDK 的轻量级锁性能已足够。

### ZGC 默认分代模式

JDK 25 中 ZGC 默认启用分代模式（`-XX:+ZGenerational`），非分代模式已废弃。

```bash
# 检查是否显式禁用分代
grep -rn 'ZGenerational' scripts/ config/

# JDK 25 推荐配置
java -XX:+UseZGC MyApp  # 自动使用分代模式
```

---

## 6. 检测与迁移工具

### 快速兼容性检查脚本

```bash
#!/bin/bash
echo "=== JDK 25 兼容性检查 ==="

echo "1. 检查 String Templates 用法..."
COUNT=$(grep -rn 'STR\.\"\|FMT\.\"\|RAW\."' src/ 2>/dev/null | wc -l)
echo "   发现 $COUNT 处 String Templates 用法"

echo "2. 检查 Security Manager 用法..."
COUNT=$(grep -rn 'SecurityManager\|setSecurityManager' src/ 2>/dev/null | wc -l)
echo "   发现 $COUNT 处 Security Manager 用法"

echo "3. 检查废弃 JVM 参数..."
grep -rn 'UseBiasedLocking\|ZUncommit' scripts/ config/ 2>/dev/null

echo "4. 检查 32-bit 依赖..."
file $(which java) | grep -q "32-bit" && echo "   ⚠️ 当前运行在 32 位环境" || echo "   ✅ 64 位环境"

echo "=== 检查完成 ==="
```

### jdeprscan 工具

```bash
# 扫描废弃 API 用法
jdeprscan --release 25 myapp.jar
```

---

## 7. 相关链接

- [JDK 25 主页](../README.md)
- [JDK 25 迁移指南](./migration/from-21.md)
- [JDK 25 JEP 汇总](../jeps.md)
- [JEP 503: Remove 32-bit x86 Port](https://openjdk.org/jeps/503)
- [JEP 411: Deprecate the Security Manager](https://openjdk.org/jeps/411)

---

[← 返回 JDK 25](../README.md)
