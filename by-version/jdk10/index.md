# JDK 10

> **发布日期**: 2018-03-20 | **类型**: Feature Release

---

## 核心特性

JDK 10 是一个短期版本，主要包含局部变量类型推断（var）和线程局部握手。

| 特性 | 影响 | 详情 |
|------|------|------|
| **局部变量类型推断** | ⭐⭐⭐⭐⭐ | JEP 286，`var` 关键字 |
| **线程局部握手** | ⭐⭐⭐ | JEP 312 |
| **G1 并行 Full GC** | ⭐⭐⭐ | JEP 307 |
| **应用类数据共享** | ⭐⭐⭐ | JEP 310 |
| **基于 Java 的 JIT 编译器** | ⭐⭐⭐ | JEP 317 |

---

## 关键 JEP

| JEP | 标题 | 说明 |
|-----|------|------|
| [JEP 286](https://openjdk.org/jeps/286) | Local-Variable Type Inference | 局部变量类型推断 |
| [JEP 312](https://openjdk.org/jeps/312) | Thread-Local Handshakes | 线程局部握手 |
| [JEP 307](https://openjdk.org/jeps/307) | Parallel Full GC for G1 | G1 并行 Full GC |
| [JEP 310](https://openjdk.org/jeps/310) | Application Class-Data Sharing | 应用类数据共享 |
| [JEP 317](https://openjdk.org/jeps/317) | Java-Based JIT Compiler | Graal JIT |
| [JEP 304](https://openjdk.org/jeps/304) | Garbage Collector Interface | GC 接口统一 |
| [JEP 313](https://openjdk.org/jeps/313) | Remove the Native-Header Generation Tool | 移除 javah |
| [JEP 314](https://openjdk.org/jeps/314) | Additional Unicode Language-Tag Extensions | Unicode 扩展 |
| [JEP 316](https://openjdk.org/jeps/316) | Heap Allocation on Alternative Memory Devices | 堆外内存分配 |
| [JEP 319](https://openjdk.org/jeps/319) | Root Certificates | 根证书 |
| [JEP 322](https://openjdk.org/jeps/322) | Time-Based Release Versioning | 基于时间的版本号 |

---

## 代码示例

### 局部变量类型推断

```java
// 之前
List<String> list = new ArrayList<String>();
Map<String, List<String>> map = new HashMap<String, List<String>>();

// JDK 10
var list = new ArrayList<String>();
var map = new HashMap<String, List<String>>();

// 在 for 循环中
for (var entry : map.entrySet()) {
    System.out.println(entry.getKey());
}
```

### 应用类数据共享

```bash
# 生成共享存档
java -Xshare:dump -XX:SharedArchiveFile=myapp.jsa \
     -XX:SharedClassListFile=classlist

# 使用共享存档
java -Xshare:on -XX:SharedArchiveFile=myapp.jsa MyApp
```

---

## 性能改进

| 领域 | 改进 |
|------|------|
| 启动时间 | AppCDS 提升 10-30% |
| G1 GC | Full GC 并行化 |
| 内存 | 堆外内存支持 |

---

## 相关链接

- [发布说明](https://openjdk.org/projects/jdk/10/)
