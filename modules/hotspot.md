# hotspot 模块分析

> HotSpot VM，Oracle JDK 的默认 Java 虚拟机实现

---

## 1. 模块概述

HotSpot 是 Oracle JDK 的默认 JVM 实现，名称来源于其"热点检测"技术——通过运行时分析找出频繁执行的代码（热点）并进行即时编译优化。

### 架构

```
┌─────────────────────────────────────────────────────────┐
│                    Java 应用                             │
│  (字节码)                                                │
├─────────────────────────────────────────────────────────┤
│                 类加载器子系统                           │
│  Bootstrap / Extension / Application                     │
├─────────────────────────────────────────────────────────┤
│                   运行时数据区                           │
│  堆 / 方法区 / 程序计数器 / 虚拟机栈 / 本地方法栈         │
├─────────────────────────────────────────────────────────┤
│                   执行引擎                               │
│  解释器 ──→ C1 编译器 ──→ C2 编译器                      │
│  (热点检测)     (客户端)        (服务器端)               │
├─────────────────────────────────────────────────────────┤
│                   本地接口                               │
│  JNI                                                   │
├─────────────────────────────────────────────────────────┤
│                   操作系统                               │
└─────────────────────────────────────────────────────────┘
```

---

## 2. 源码结构

**目录**: `src/hotspot/share/`

```
hotspot/
├── classfile/       # 类文件处理
│   ├── classLoader.cpp
│   └── classFileParser.cpp
├── code/            # 代码缓存
│   ├── codeCache.cpp
│   └── nmethod.cpp
├── compiler/        # 编译器接口
│   ├── compileBroker.cpp
│   └── compilationPolicy.cpp
├── gc/              # 垃圾回收
│   ├── g1/
│   ├── shenandoah/
│   ├── z/
│   └── parallel/
├── interpreter/     # 解释器
│   ├── interpreter.cpp
│   └── templateTable.cpp
├── memory/          # 内存管理
│   ├── metaspace.cpp
│   └── virtualspace.cpp
├── oops/            # 对象模型
│   ├── oop.cpp
│   └── instanceOop.cpp
├── prims/           # JNI、JVMTI 等原语
│   ├── jni.cpp
│   └── jvmti.cpp
├── runtime/         # 运行时
│   ├── arguments.cpp
│   ├── thread.cpp
│   ├── vm.cpp
│   └── init.cpp
├── services/        # JVM 服务
│   └── management.cpp
└── utilities/       # 工具类
    └── globalDefinitions.cpp
```

---

## 3. 核心组件

### 3.1 类加载器子系统

**源码**: `src/hotspot/share/classloader/`

```cpp
// 类加载流程
ClassFileParser::parseClassFile()
    → ClassLoader::load_class()
        → SystemDictionary::resolve_instance_class_or_null()
            → ClassLinker::link_class()
                → Klass::verify()
                → Interpreter::enter()
```

**双亲委派模型**:
```
Bootstrap ClassLoader (JAVA_HOME/lib)
    ↑
Extension ClassLoader (JAVA_HOME/lib/ext)
    ↑
Application ClassLoader (Classpath)
```

### 3.2 运行时数据区

**源码**: `src/hotspot/share/memory/`

| 区域 | 用途 | 实现 |
|------|------|------|
| 堆 | 对象实例 | `CollectedHeap` |
| 方法区 | 类信息 | `Metaspace` |
| 程序计数器 | 当前指令 | `Thread::_pc` |
| 虚拟机栈 | 局部变量、操作数栈 | `JavaThread::_stack` |
| 本地方法栈 | Native 方法 | `JavaThread::_stack` |

### 3.3 执行引擎

**分层编译** (JDK 7+):

```
解释执行
    ↓ (热点检测, 调用次数 > C1 阈值)
C1 编译 (Client 编译器)
    ↓ (进一步热点, 调用次数 > C2 阈值)
C2 编译 (Server 编译器)
```

**源码**: `src/hotspot/share/compiler/`

```cpp
// 编译策略
SimpleThresholdPolicy::compile()
    → CompilationPolicy::select_method()
        → CompileBroker::compile_method()
            → Compiler::compile()
```

### 3.4 垃圾回收器

**源码**: `src/hotspot/share/gc/`

| GC | 版本 | 特点 |
|-----|------|------|
| Serial | JDK 1.3+ | 单线程, 小内存 |
| Parallel | JDK 5+ | 多线程, 吞吐量优先 |
| CMS | JDK 6-14 | 低延迟 (已移除) |
| G1 | JDK 7+ | 平衡延迟和吞吐量 |
| ZGC | JDK 11+ | 低延迟 (< 10ms) |
| Shenandoah | JDK 12+ | 低延迟 |

---

## 4. JDK 26 变更

### 4.1 虚拟线程 (Virtual Threads)

**JEP**: JEP 444

**源码**: `src/hotspot/share/runtime/continuation.cpp`

```cpp
// Continuation 实现
Continuation::freeze()
    → 保存栈帧
Continuation::thaw()
    → 恢复栈帧
```

### 4.2 分层编译改进

- C1/C2 编译阈值优化
- 编译队列改进

### 4.3 性能改进

- 压缩指针 (Compressed Oops) 优化
- 锁优化 (偏向锁、轻量级锁)

---

## 5. 关键源码分析

### 5.1 对象模型

**源码**: `src/hotspot/share/oops/oop.hpp`

```cpp
class oopDesc {
 private:
  volatile markWord _mark;     // Mark Word (锁、GC、哈希)
  union _metadata {
    Klass*      _klass;        // 类元数据指针
    narrowKlass _compressed_klass;  // 压缩类指针
  } _metadata;

 public:
  // 对象头布局 (64 位 JVM)
  // |unused:25|hash:31|unused:1|age:4|biased_lock:1|lock:2| (normal)
  // |thread:54|epoch:2|unused:1|age:4|biased_lock:1|lock:2| (biased)
  // |ptr:62|lock:2| (lightweight/weight)
};
```

### 5.2 线程模型

**源码**: `src/hotspot/share/runtime/thread.cpp`

```cpp
class JavaThread: public Thread {
 private:
  // Java 栈
  JavaFrameAnchor _anchor;
  // 本地栈
  OSThread* _osthread;
  // 线程状态
  JavaThreadState _thread_state;
};
```

### 5.3 JIT 编译入口

**源码**: `src/hotspot/share/compiler/compileBroker.cpp`

```cpp
void CompileBroker::compile_method() {
  // 创建编译任务
  CompileTask* task = new CompileTask(...);

  // 提交到编译队列
  _compile_queue->add(task);

  // 通知编译线程
  _compile_queue->notify_all();
}
```

---

## 6. JVM 选项

### 6.1 内存相关

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `-Xms` | 物理内存 1/64 | 初始堆大小 |
| `-Xmx` | 物理内存 1/4 | 最大堆大小 |
| `-XX:MetaspaceSize` | 取决于平台 | 元空间初始大小 |
| `-XX:MaxMetaspaceSize` | 无限制 | 元空间最大大小 |

### 6.2 GC 相关

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `-XX:+UseG1GC` | ✓ | 使用 G1 GC |
| `-XX:+UseZGC` | - | 使用 ZGC |
| `-XX:+UseParallelGC` | - | 使用 Parallel GC |
| `-XX:MaxGCPauseMillis` | 200 | 最大 GC 暂停时间 (G1) |

### 6.3 编译相关

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `-XX:+TieredCompilation` | ✓ | 分层编译 |
| `-XX:CompileThreshold` | 10000 | C2 编译阈值 |
| `-XX:InitialCodeCacheSize` | 160KB | 代码缓存初始大小 |

---

## 7. 性能调优

### 7.1 内存调优

```bash
# 推荐: 设置初始堆和最大堆相同
java -Xms2g -Xmx2g -jar app.jar

# 推荐: 设置元空间大小
java -XX:MetaspaceSize=256m -XX:MaxMetaspaceSize=512m -jar app.jar
```

### 7.2 GC 调优

```bash
# G1 GC (推荐)
java -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -jar app.jar

# ZGC (低延迟)
java -XX:+UseZGC -jar app.jar

# GC 日志
java -Xlog:gc*:file=gc.log -jar app.jar
```

### 7.3 JIT 调优

```bash
# 预热优化
java -XX:CompileThreshold=8000 -jar app.jar

# 代码缓存
java -XX:InitialCodeCacheSize=32m -XX:ReservedCodeCacheSize=256m -jar app.jar
```

---

## 8. 相关链接

- [HotSpot 官方文档](https://openjdk.org/groups/hotspot/)
- [JVM 工具接口 (JVMTI)](https://docs.oracle.com/en/java/javase/26/docs/specs/jvmti.html)
- [源码](https://github.com/openjdk/jdk/tree/master/src/hotspot)
