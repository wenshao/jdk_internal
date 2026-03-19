# JDK 9

> **发布日期**: 2017-09-21 | **类型**: Feature Release

---

## 核心特性

JDK 9 是 Java 历史上最重要的版本之一，引入了模块系统（Project Jigsaw）。

| 特性 | 影响 | 详情 |
|------|------|------|
| **模块系统 (JPMS)** | ⭐⭐⭐⭐⭐ | JEP 261/262/283，彻底改变 Java 架构 |
| **接口私有方法** | ⭐⭐⭐ | JEP 213 |
| **HTTP/2 Client** | ⭐⭐⭐⭐ | JEP 110 (incubator) |
| **G1 作为默认 GC** | ⭐⭐⭐ | JEP 229 |
| **集合工厂方法** | ⭐⭐⭐ | JEP 269 |
| **Process API** | ⭐⭐ | JEP 102 |

---

## 关键 JEP

| JEP | 标题 | 说明 |
|-----|------|------|
| [JEP 261](https://openjdk.org/jeps/261) | Module System | 模块系统 |
| [JEP 213](https://openjdk.org/jeps/213) | Interface Private Methods | 接口私有方法 |
| [JEP 110](https://openjdk.org/jeps/110) | HTTP/2 Client | HTTP/2 客户端 (孵化器) |
| [JEP 229](https://openjdk.org/jeps/229) | G1 as Default GC | G1 成为默认 GC |
| [JEP 269](https://openjdk.org/jeps/269) | Collection Factory Methods | 集合工厂方法 |
| [JEP 102](https://openjdk.org/jeps/102) | Process API Update | 进程 API 更新 |
| [JEP 280](https://openjdk.org/jeps/280) | Indify String Concatenation | 字符串连接优化 |
| [JEP 295](https://openjdk.org/jeps/295) | Ahead-of-Time Compilation | AOT 编译 |

---

## 代码示例

### 模块系统

```java
// module-info.java
module com.example.myapp {
    requires java.base;
    requires java.logging;
    exports com.example.api;
}
```

### 接口私有方法

```java
public interface MyInterface {
    default void doSomething() {
        helperMethod();
    }

    private void helperMethod() {
        System.out.println("Helper");
    }
}
```

### 集合工厂方法

```java
// 不可变集合
List<String> list = List.of("a", "b", "c");
Set<Integer> set = Set.of(1, 2, 3);
Map<String, Integer> map = Map.of("a", 1, "b", 2);
```

---

## 破坏性变更

| 变更 | 影响 |
|------|------|
| 类加载器变更 | 需要适配 |
| `--illegal-access` | 默认警告 |
| GC 日志格式改变 | 需要更新 |

---

## 相关链接

- [发布说明](https://openjdk.org/projects/jdk/9/)
