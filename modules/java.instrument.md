---

# java.instrument 模块分析

> Java Agent / Instrumentation API — 字节码增强框架，支持类加载时和运行时修改

---

## 1. 模块定义

**源文件**: `src/java.instrument/share/classes/module-info.java`

```
module java.instrument {
    exports java.lang.instrument;
}
```

### 核心类

| 类 | 用途 |
|---|---|
| `Instrumentation` | 核心 API：类转换、重定义、再转换 |
| `ClassFileTransformer` | 字节码转换器接口 |
| `ClassDefinition` | 类重定义描述 |
| `UnmodifiableClassException` | 不可修改类异常 |

---

## 2. 核心架构

### 2.1 Java Agent 工作原理

```
┌─────────────────────────────────────────────────────────────┐
│                   Java Agent 加载流程                        │
│                                                             │
│  JVM 启动                                                   │
│    │                                                        │
│    ├── -javaagent:myagent.jar                               │
│    │     │                                                  │
│    │     └── premain(String args, Instrumentation inst)     │
│    │           │                                            │
│    │           ├── 注册 ClassFileTransformer                │
│    │           └── inst.addTransformer(transformer)         │
│    │                                                        │
│    ├── 类加载时触发 Transformer                              │
│    │     │                                                  │
│    │     └── byte[] transform(...) → 修改后的字节码          │
│    │                                                        │
│    └── Agent.attach(pid) (运行时附加)                       │
│          │                                                  │
│          └── agentmain(String args, Instrumentation inst)   │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Agent 打包结构

```
my-agent.jar
├── META-INF/
│   └── MANIFEST.MF
│       ├── Premain-Class: com.example.MyAgent
│       ├── Agent-Class: com.example.MyAgent      (运行时附加)
│       ├── Can-Redefine-Classes: true             (类重定义)
│       ├── Can-Retransform-Classes: true          (类再转换)
│       └── Can-Set-Native-Method-Prefix: true     (原生方法前缀)
│
└── com/example/MyAgent.class
```

---

## 3. 核心 API

### 3.1 premain (启动时加载)

```java
public class MyAgent {
    public static void premain(String args, Instrumentation inst) {
        System.out.println("Agent loaded at startup: " + args);

        // 注册字节码转换器
        inst.addTransformer(new ClassFileTransformer() {
            @Override
            public byte[] transform(ClassLoader loader, String className,
                    Class<?> classBeingRedefined, ProtectionDomain domain,
                    byte[] classfileBuffer) {
                if (className.startsWith("com/example/")) {
                    // 使用 ASM/Javassist 修改字节码
                    return modifyClass(classfileBuffer);
                }
                return null; // null 表示不修改
            }
        });
    }
}
```

### 3.2 agentmain (运行时附加)

```java
public class MyAgent {
    public static void agentmain(String args, Instrumentation inst) {
        // 运行时附加（如 Arthas 的工作原理）
        inst.addTransformer(new ClassFileTransformer() {
            @Override
            public byte[] transform(...) {
                // 修改已加载的类
                return modifyClass(classfileBuffer);
            }
        }, true); // true = canRetransform

        // 触发已加载类的再转换
        for (Class<?> clazz : inst.getAllLoadedClasses()) {
            if (inst.isModifiableClass(clazz)
                    && clazz.getName().startsWith("com.example")) {
                inst.retransformClasses(clazz);
            }
        }
    }
}
```

### 3.3 Instrumentation API 关键方法

| 方法 | 说明 |
|------|------|
| `addTransformer(transformer, canRetransform)` | 注册转换器 |
| `removeTransformer(transformer)` | 移除转换器 |
| `retransformClasses(Class<?>...)` | 再转换已加载的类 |
| `redefineClasses(ClassDefinition...)` | 完全重定义类 |
| `getAllLoadedClasses()` | 获取所有已加载类 |
| `getInitiatedClasses(loader)` | 获取类加载器加载的类 |
| `getObjectSize(obj)` | 获取对象大小 |
| `isModifiableClass(clazz)` | 检查类是否可修改 |
| `setNativeMethodPrefix(prefix)` | 设置原生方法前缀 |

---

## 4. 主要使用场景

### 4.1 APM (应用性能监控)

```
SkyWalking, Pinpoint, Elastic APM 等工具的核心原理:

1. Agent 在类加载时注入监控代码
2. 拦截方法入口/出口，记录调用链
3. 收集指标上报到 APM Server

拦截示例 (概念):
  原始: void hello() { ... }
  修改: void hello() {
          long start = System.nanoTime();
          try { ... } finally {
              tracer.record("hello", System.nanoTime() - start);
          }
        }
```

### 4.2 热部署 / 热加载

```
Spring DevTools, JRebel, Arthas 等工具:

1. 监控 class 文件变化
2. 使用 retransformClasses() 热更新已加载的类
3. 无需重启 JVM
```

### 4.3 Mock / 测试

```
Mockito, PowerMock, JMockit 等框架:

1. 在测试运行前修改类的字节码
2. 注入 mock 行为
3. 修改 final 类、static 方法等
```

---

## 5. 限制与注意事项

| 限制 | 说明 |
|------|------|
| **不可改变类结构** | retransform 不能增减字段/方法/父类/接口 |
| **不可修改 JDK 核心类** | `java.lang.String` 等核心类默认不可修改 |
| **启动顺序** | premain 期间不能使用未加载的类 |
| **性能影响** | 大量 transformer 会影响类加载性能 |
| **线程安全** | transformer 的 transform 方法可能被并发调用 |
| **JDK 21+ 安全限制** | JEP 451 限制动态加载 Agent，需 `-XX:+EnableDynamicAgentLoading` |

### JDK 21+ Agent 限制 (JEP 451)

```bash
# JDK 21: 动态附加 Agent 会发出警告
# JDK 22+: 可能默认禁止动态附加

# 显式允许动态附加
-XX:+EnableDynamicAgentLoading

# 或者使用 -javaagent 方式启动时加载（不受限制）
-javaagent:/path/to/agent.jar
```

---

## 6. 与其他技术对比

| 特性 | Java Agent | AOP (AspectJ) | ByteBuddy | ASM |
|------|-----------|---------------|-----------|-----|
| 加载时机 | 类加载前 | 编译期/加载期 | 类加载前 | 类加载前 |
| 运行时修改 | ✅ | ❌ | ✅ | ✅ |
| 复杂度 | 高 | 中 | 低 | 高 |
| 无侵入 | ✅ | ⚠️ (LTW) | ✅ | ✅ |
| 生产使用 | ✅ | ⚠️ | ✅ | ✅ |

---

## 7. 相关链接

- [JEP 451: 准备禁止动态加载 Agent](/jeps/security/jep-451.md)
- [类加载器主题](/by-topic/core/classloading/)
- [反射与元数据](/by-topic/language/reflection/)
- [模块系统](/by-topic/core/modules/)
