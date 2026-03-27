---

# Metaspace OOM：动态类加载导致的元空间溢出

> **声明**：本文中所有监控数据、性能指标均为 **示意数据（illustrative data）**，实际结果取决于工作负载、硬件环境和 JVM 版本。

---

## 目录

1. [背景与问题描述](#1-背景与问题描述)
2. [环境信息](#2-环境信息)
3. [第一阶段：OOM 发现](#3-第一阶段oom-发现)
4. [第二阶段：Metaspace 分析](#4-第二阶段metaspace-分析)
5. [第三阶段：根因定位](#5-第三阶段根因定位)
6. [第四阶段：修复方案](#6-第四阶段修复方案)
7. [最终效果对比](#7-最终效果对比)
8. [经验总结与 Checklist](#8-经验总结与-checklist)

---

## 1. 背景与问题描述

### 1.1 业务场景

**规则引擎平台**，允许业务人员通过 DSL 配置业务规则。规则被编译为 Java 类并动态加载到 JVM 中运行。

### 1.2 问题现象

- **定期 OOM**: 运行 3-5 天后出现 `java.lang.OutOfMemoryError: Metaspace`
- **Metaspace 持续增长**: 从初始 80MB 增长到 1GB+
- **Full GC 无法回收**: Full GC 后 Metaspace 使用量不下降
- **重启后恢复**: 重启后恢复正常，3-5 天后再次 OOM

---

## 2. 环境信息

```
JDK 版本:    JDK 17.0.12
GC:          G1 (默认)
JVM 内存:    -Xms4g -Xmx4g -XX:MaxMetaspaceSize=512m
框架:        Spring Boot 3.1 + Drools 8.x (规则引擎)
规则数量:    约 20,000 条，每天新增/更新约 500 条
```

---

## 3. 第一阶段：OOM 发现

### 3.1 OOM 日志

```
java.lang.OutOfMemoryError: Metaspace
    at java.lang.ClassLoader.defineClass1(Native Method)
    at java.lang.ClassLoader.defineClass(ClassLoader.java:756)
    at com.example.rules.RuleCompiler.compile(RuleCompiler.java:89)
```

### 3.2 NMT (Native Memory Tracking)

```bash
# 启用 NMT
-XX:NativeMemoryTracking=detail

# 查看 Metaspace 使用
jcmd <pid> VM.native_memory summary
```

```
Total: reserved=5678MB, committed=4612MB
- Java Heap:    reserved=4096MB, committed=4096MB
- Class (metaspace): reserved=1142MB, committed=512MB  ← 接近限制
  - Internal: reserved=0MB, committed=0MB
```

---

## 4. 第二阶段：Metaspace 分析

### 4.1 类加载统计

```bash
jcmd <pid> GC.class_stats | head -20
```

发现：已加载类数量约 120,000+，其中 95,000+ 是动态生成的规则类。

### 4.2 类加载器分析

```bash
jcmd <pid> GC.class_histogram | grep Rule
```

```
 num     #instances         #bytes  class name (module)
   1:       95000       15200000  com.example.rules.GeneratedRule$$Lambda
   2:       95000       11400000  com.example.rules.GeneratedRule
   ...
```

### 4.3 JFR Metaspace 事件

```bash
jcmd <pid> JFR.start settings=profile
# 等待 1 小时后 dump
jcmd <pid> JFR.dump filename=metaspace-analysis.jfr
```

JFR 显示 `jdk.MetaSpaceAllocationFailure` 事件频繁发生。

---

## 5. 第三阶段：根因定位

### 5.1 类加载器泄漏

```java
// 问题代码: 每次规则更新都创建新的 ClassLoader
public class RuleEngine {
    // ❌ 每次更新创建新的 ClassLoader，旧的不会被 GC
    public void reloadRules(List<Rule> rules) {
        // 创建新的 ClassLoader
        ClassLoader ruleClassLoader = new URLClassLoader(
            new URL[]{compileDir.toURI().toURL()},
            getClass().getClassLoader()
        );

        for (Rule rule : rules) {
            Class<?> clazz = ruleClassLoader.loadClass(rule.getClassName());
            // 加载类并缓存
            ruleInstances.put(rule.getId(), clazz.getDeclaredConstructor().newInstance());
        }
        // 旧的 ClassLoader 及其加载的类无法被 GC！
    }
}
```

### 5.2 根因链条

```
1. 规则更新 → 创建新 ClassLoader → 加载新类
2. 旧 ClassLoader 未被释放 → 旧类留在 Metaspace
3. 每天更新 500 次 → 每天泄漏约 500 * ~50KB = 25MB Metaspace
4. 512MB Metaspace 在 ~20 天后耗尽
```

### 5.3 GC Root 追踪

```
旧 ClassLoader 的 GC Root:
  RuleEngine.ruleInstances (ConcurrentHashMap)
    → 持有旧 Class 实例的引用
      → 持有 ClassLoader 引用
        → ClassLoader 持有所有已加载类
          → Metaspace 无法释放
```

---

## 6. 第四阶段：修复方案

### 6.1 方案一：清除旧 ClassLoader 引用

```java
// ✅ 修复: 更新规则前清理旧引用
public class RuleEngine {
    private volatile ClassLoader currentClassLoader;

    public void reloadRules(List<Rule> rules) {
        ClassLoader newClassLoader = new URLClassLoader(
            new URL[]{compileDir.toURI().toURL()},
            getClass().getClassLoader()
        );

        Map<String, Object> newInstances = new HashMap<>();
        for (Rule rule : rules) {
            Class<?> clazz = newClassLoader.loadClass(rule.getClassName());
            newInstances.put(rule.getId(), clazz.getDeclaredConstructor().newInstance());
        }

        // 原子替换: 旧引用被清除，可被 GC
        ruleInstances.clear();
        ruleInstances.putAll(newInstances);
        currentClassLoader = newClassLoader;

        // 触发 GC 释放 Metaspace
        System.gc();
    }
}
```

### 6.2 方案二：使用 ClassLoader 生命周期管理

```java
// ✅ 更优: 使用 Closeable URLClassLoader
public void reloadRules(List<Rule> rules) {
    // 关闭旧的 ClassLoader (释放资源)
    if (currentClassLoader instanceof URLClassLoader ucl) {
        try {
            ucl.close();  // JDK 7+ 支持
        } catch (IOException e) {
            log.warn("Failed to close old ClassLoader", e);
        }
    }

    // 创建新 ClassLoader
    currentClassLoader = new CloseableClassLoader(compileDir);
    // ...
}
```

### 6.3 方案三：增大 Metaspace + 监控

```bash
# 增大 Metaspace 上限
-XX:MaxMetaspaceSize=1g

# 启用 Metaspace GC 日志
-Xlog:gc+metaspace*=info:file=/logs/gc.log

# NMT 持续监控
-XX:NativeMemoryTracking=summary
```

---

## 7. 最终效果对比

| 指标 | 修复前 | 修复后 |
|------|--------|--------|
| Metaspace 增长速度 | ~25MB/天 | ~2MB/天 (稳定) |
| 已加载类数 | 120,000+ (持续增长) | ~28,000 (稳定) |
| OOM 频率 | 每 3-5 天 | 0 |
| Full GC 后 Metaspace 回收 | 几乎不回收 | 正常回收 |

---

## 8. 经验总结与 Checklist

### Metaspace OOM 排查 Checklist

- [ ] 检查 OOM 错误信息是否为 `Metaspace`（而非 Java heap）
- [ ] 使用 `jcmd GC.class_stats` 统计已加载类数量
- [ ] 使用 `jcmd VM.native_memory summary` 查看 Class 内存使用
- [ ] 使用 JFR 监控 `jdk.MetaSpaceAllocationFailure` 事件
- [ ] 检查是否有自定义 ClassLoader 未正确释放
- [ ] 检查是否有动态代理（`java.lang.reflect.Proxy`）大量创建
- [ ] 检查是否有 `CGLIB` / `ByteBuddy` / `ASM` 动态生成类
- [ ] 检查 Groovy / JSP / Drools 等动态语言/规则引擎的类加载行为
- [ ] 使用 `jcmd GC.class_histogram` 找出占用最大的类

### 关键经验

1. **ClassLoader 泄漏是 Metaspace OOM 的最常见原因**——比单纯类数量过多更常见
2. **`MaxMetaspaceSize` 应始终设置**——不设置则无上限，可能耗尽系统内存
3. **`Closeable.close()` 是 JDK 7+ 的关键 API**——主动释放 ClassLoader 资源
4. **NMT (Native Memory Tracking) 是排查利器**——`-XX:NativeMemoryTracking=detail`
5. **动态类生成框架应配置类池大小上限**——如 Drools 的 `MaxRulesInCache`

### 相关资源

- [内存泄漏诊断案例](memory-leak-diagnosis.md)
- [类加载器主题](/by-topic/core/classloading/)
- [模块系统](/by-topic/core/modules/)
- [JFR 指南](/guides/jfr.md)
