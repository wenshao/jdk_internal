# Doug Lea

> **OpenJDK**: [@dl](https://openjdk.org/census#dl)
> **Personal Site**: [Concurrency JSR-166 Interest](https://gee.cs.oswego.edu/dl/concurrency-interest/)
> **Organization**: SUNY Oswego (State University of New York)
> **Role**: Professor of Computer Science, JSR-166 Specification Lead

---

## 概述

Doug Lea 是 **SUNY Oswego (纽约州立大学奥斯威戈分校) 计算机科学教授**，Java 并发编程的奠基人。他是 **JSR-166 (java.util.concurrent)** 的规范负责人，创建了现代 Java 并发编程的基础设施。他的工作对 Java 平台产生了深远影响，被公认为 Java 并发领域的传奇人物。

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Doug Lea |
| **当前组织** | SUNY Oswego (State University of New York) |
| **职位** | Professor of Computer Science |
| **OpenJDK** | [@dl](https://openjdk.org/census#dl) |
| **角色** | JDK Committer, JDK Reviewer, JSR-166 Spec Lead |
| **邮件** | dl@openjdk.org |
| **专长** | Java Concurrency, Memory Model, Fork/Join, Parallel Computing |
| **学术引用** | 6,000+ (Google Scholar) |

---

## OpenJDK 角色

### Committer & Reviewer

- **JDK 9 Committer**: 2014年1月当选
- **JDK 9 Reviewer**: 2016年4月当选
- **OpenJDK Interim Governance Board**: 前成员
- **Username**: `dl` (OpenJDK Census)

---

## 主要 JEP 贡献

### JEP 266: More Concurrency Updates

| 属性 | 值 |
|------|-----|
| **角色** | Author |
| **状态** | Closed / Delivered |
| **发布版本** | JDK 9 |
| **Bug** | JDK-8132960 |

**影响**: java.util.concurrent 包的进一步更新和改进。

### JSR-166: Concurrency Utilities

| 属性 | 值 |
|------|-----|
| **角色** | Specification Lead |
| **状态** | Final |
| **发布版本** | Java 5.0 (Tiger) |

**影响**: 引入 java.util.concurrent 包，提供标准化的并发编程工具类。

### JSR-166y: Fork/Join Framework

| 属性 | 值 |
|------|-----|
| **角色** | Primary Author |
| **状态** | Final |
| **发布版本** | Java 7 |

**影响**: 引入 Fork/Join 框架，支持并行任务执行。

---

## 核心技术贡献

### 1. java.util.concurrent 框架

Doug Lea 创建了 Java 并发编程的基础设施：

```java
// 线程池
ExecutorService executor = Executors.newFixedThreadPool(4);

// 并发集合
ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();

// 同步器
CountDownLatch latch = new CountDownLatch(3);
Semaphore semaphore = new Semaphore(5);

// 原子变量
AtomicInteger counter = new AtomicInteger(0);

// Future 和 Callable
Future<String> future = executor.submit(() -> "result");
```

### 2. Fork/Join 框架

```java
// Fork/Join 示例
class RecursiveTask extends RecursiveTask<Integer> {
    @Override
    protected Integer compute() {
        if (smallEnough()) {
            return computeDirectly();
        }
        RecursiveTask left = new RecursiveTask(data, 0, mid);
        RecursiveTask right = new RecursiveTask(data, mid, end);
        left.fork();
        int rightResult = right.compute();
        int leftResult = left.join();
        return leftResult + rightResult;
    }
}
```

### 3. Java Memory Model (JMM)

- **JMM9 Project**: JDK 9 内存模型修订项目负责人
- 与 JVM 团队合作改进内存模型规范

### 4. Synchronizer 框架

- **The java.util.concurrent Synchronizer framework**
- PODC CSJP workshop 2004
- 发表在 Science of Computer Programming 期刊

---

## 学术背景

### 教育职位

- **Professor of Computer Science**: SUNY Oswego
- **Co-director**: Software Engineering Lab, New York Center for Advanced Technology in Computer Applications

### 出版著作

1. **"Concurrent Programming in Java"**
   - Java 内部机制的经典读物
   - 与 JVM 规范并列为必读书目

2. **"Java Concurrency in Practice"** (合著)
   - 与 Brian Goetz 等合著
   - Java 并发编程的权威指南

3. **"Object-Oriented Software Development"**

### 学术发表

- **53+ 篇论文**
- **6,000+ 引用** (Google Scholar)
- 研究领域: 并发编程、面向对象设计、软件工程

---

## 开源贡献

### CVS Repository

Doug Lea 维护着 JSR-166 相关代码的 CVS 仓库：
- JSR-166 类
- 相关类、测试、基准测试
- 演示程序

### 近期工作

- **core-libs-dev 邮件列表**: 活跃参与
- **文档改进**: java.util.concurrent 类的文档完善
- **Project Loom**: ForkJoin 方法需要适应虚拟线程

---

## 技术专长

### 并发编程

- **线程池**: ExecutorService 框架
- **并发集合**: ConcurrentHashMap, ConcurrentLinkedQueue 等
- **同步器**: CountDownLatch, Semaphore, CyclicBarrier 等
- **原子变量**: AtomicInteger, AtomicReference 等
- **Fork/Join**: 分治并行计算框架

### 内存模型

- **Java Memory Model**: JMM 规范
- **happens-before**: 内存可见性保证
- **volatile**: volatile 语义

---

## 影响力与认可

### 社区评价

- 被广泛认为是 **Java 并发编程的传奇人物**
- 他的工作对现代 Java 并发编程产生了 **深远影响**
- java.util.concurrent 包被广泛使用于整个 Java 生态系统

### 技术影响

- **Java 5.0**: 引入 java.util.concurrent (JSR-166)
- **Java 7**: 引入 Fork/Join 框架 (JSR-166y)
- **Java 9**: JEP 266 更多并发更新
- **后续版本**: 持续改进和维护

---

## 相关链接

### 官方资料
- [OpenJDK Census - dl](https://openjdk.org/census#dl)
- [SUNY Oswego Vita](https://gee.cs.oswego.edu/dl/html/vita.html)
- [OpenJDK User Profile](https://mail.openjdk.org/archives/users/0c582be84f03408a9e79f604168ccd86/)

### JSR-166 资源
- [Concurrency JSR-166 Interest Site](https://gee.cs.oswego.edu/dl/concurrency-interest/)
- [JSR-166 Specification](https://jcp.org/ja/jsr/detail?id=166)

### 邮件列表
- [CFV: New JDK9 Committer: Doug Lea](https://mail.openjdk.org/pipermail/jdk9-dev/2014-January/000252.html)
- [JDK9 Reviewer Announcement](https://mail.openjdk.org/pipermail/jdk9-dev/2016-April/004101.html)

### JEP 文档
- [JEP 266: More Concurrency Updates](https://openjdk.org/jeps/266)

---

**Sources**:
- [OpenJDK Census - dl](https://openjdk.org/census#dl)
- [SUNY Oswego Vita](https://gee.cs.oswego.edu/dl/html/vita.html)
- [Concurrency JSR-166 Interest Site](https://gee.cs.oswego.edu/dl/concurrency-interest/)
- [CFV: JDK9 Committer](https://mail.openjdk.org/pipermail/jdk9-dev/2014-January/000252.html)
- [JDK9 Reviewer Announcement](https://mail.openjdk.org/pipermail/jdk9-dev/2016-April/004101.html)
- [JEP 266: More Concurrency Updates](https://openjdk.org/jeps/266)
- [OpenJDK Governance Board Minutes](https://openjdk.org/groups/gb/minutes/2011-05-19)
