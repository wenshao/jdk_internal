# 技术演讲

> JVMLS (JVM Language Summit) 和其他重要技术会议演讲资料

---

## 目录

- [JVMLS (JVM Language Summit)](#jvmls-jvm-language-summit)
- [按主题索引](#按主题索引)
- [按贡献者索引](#按贡献者索引)
- [相关链接](#相关链接)

---

## JVMLS (JVM Language Summit)

**JVM Language Summit** 是 OpenJDK 社区主办的年度技术峰会，聚焦 JVM 内部实现、语言设计、性能优化等核心话题。

### 历届会议

| 年份 | 日期 | 地点 | 播放列表 | 本地资料 |
|------|------|------|----------|----------|
| 2025 | 8月4-6日 | Oracle HQ, Santa Clara | [YouTube](https://www.youtube.com/playlist?list=PLX8CzqL3ArzUOgZpIX6GsoRhPbnij-sco) | [分析](../jeps/tools/) |
| 2024 | 8月5-7日 | Oracle HQ, Santa Clara | [YouTube](https://www.youtube.com/playlist?list=PLX8CzqL3ArzUEYnTa6KYORRbP3nhsK0L1) | [分析](../jeps/tools/) |
| 2023 | 8月 | Oracle HQ, Santa Clara | [YouTube](https://www.youtube.com/playlist?list=PLX8CzqL3ArzW90jKUCf4H6xCKpStxsOzp) | [分析](../jeps/tools/) |
| 2019 | 7月29-31日 | Oracle HQ, Santa Clara | [YouTube](https://www.youtube.com/playlist?list=PLX8CzqL3ArzXFRVYmbvZfZQ0CQMfIIFCH) | - |

### JVMLS 2024 精选

| 演讲者 | 主题 | 类型 | 相关本地文档 |
|--------|------|------|-------------|
| Georges Saab, Mark Reinhold | Keynote: Java in 2024 | [视频](https://www.youtube.com/watch?v=NV4v7KXKQ-c) | [JDK 21](../by-version/jdk21/) |
| Brian Goetz | Project Valhalla | [报道](https://realjenius.com/2024/12/15/valhalla-simplicity/) | [Valhalla](../by-topic/core/valhalla/) |
| Per Liden | Generational ZGC | - | [ZGC](../by-topic/core/gc/zgc.md) |
| Thomas Schatzl | G1 GC Improvements | - | [G1 GC](../by-topic/core/gc/g1-gc.md) |
| Stefan Karlsson | 分代 ZGC 实现 | - | [ZGC](../by-topic/core/gc/zgc.md) |
| Roman Kennke | Shenandoah 分代 | - | [Shenandoah](../by-topic/core/gc/shenandoah.md) |
| William Kemper | 分代 Shenandoah | - | [Shenandoah](../by-topic/core/gc/shenandoah.md) |
| Tobias Hartmann | C2 JIT 编译器 | - | [JIT](../by-topic/core/jit/) |
| Christian Hagedorn | JIT 优化 | - | [JIT](../by-topic/core/jit/) |
| Roland Westrelin | Graal JIT | - | [GraalVM](../by-topic/core/graalvm/) |

### JVMLS 2023 精选

| 演讲者 | 主题 | 类型 | 相关本地文档 |
|--------|------|------|-------------|
| Georges Saab, Mark Reinhold | Keynote | [视频](https://www.youtube.com/watch?v=Ma0NtbG0mHY) | [JDK 21](../by-version/jdk21/) |
| Roman Kennke | 分代 Shenandoah | - | [Shenandoah](../by-topic/core/gc/shenandoah.md) |
| Gavin Bierman | Record Patterns | - | [模式匹配](../by-topic/core/patterns/) |
| Jan Lahoda | 模式匹配编译器 | - | [语法](../by-topic/language/syntax/) |
| Claes Redestad | String Deduplication | - | [字符串](../by-topic/language/string/) |
| David Holmes | 并发编程 | - | [并发](../by-topic/concurrency/) |

### JVMLS 2022 精选

| 演讲者 | 主题 | 类型 | 相关本地文档 |
|--------|------|------|-------------|
| Ron Pressler | Virtual Threads | - | [虚拟线程](../by-topic/core/loom/) |
| Nathan Reynolds | Structured Concurrency | - | [结构化并发](../by-topic/core/loom/) |

### JVMLS 常见主题

| 主题 | 相关本地文档 | 相关 JEP |
|------|-------------|---------|
| **ZGC** | [GC 演进](../by-topic/core/gc/) | [JEP 439](../jeps/core/jep-439.md) |
| **Shenandoah** | [GC 演进](../by-topic/core/gc/) | [JEP 429](../jeps/core/jep-429.md) |
| **G1 GC** | [GC 演进](../by-topic/core/gc/) | [JEP 522](../jeps/core/jep-522.md) |
| **Project Valhalla** | [JEPs](../jeps/) | - |
| **Project Loom** | [Virtual Threads](../by-topic/concurrency/concurrency/) | [JEP 444](../jeps/concurrency/jep-444.md) |
| **Panama** | [FFM API](../by-topic/) | - |
| **Vector API** | [性能优化](../by-topic/core/performance/) | - |

---

## 其他会议

### FOSDEM

| 年份 | 演讲者 | 主题 | 本地文档 |
|------|--------|------|----------|
| 2018 | Thomas Schatzl | G1 - Not^H^H^HNever Done! | [G1 GC](../by-topic/core/gc/) |
| 2024 | Per Liden | ZGC | [ZGC](../by-topic/core/gc/) |
| 2024 | Roman Kennke | Shenandoah | [Shenandoah](../by-topic/core/gc/) |

### Devoxx

| 年份 | 演讲者 | 主题 | 本地文档 |
|------|--------|------|----------|
| 2017 | Aleksey Shipilev | Shenandoah GC | [Shenandoah](../by-topic/core/gc/) |
| 2019 | Stuart Marks | Collections | [集合](../by-topic/api/collections/) |
| 2022 | Jos de Jong | Java 17 Updates | [JDK 17](../by-version/jdk17/) |

### JavaOne / Oracle Code One

| 年份 | 演讲者 | 主题 | 本地文档 |
|------|--------|------|----------|
| 2018 | Per Liden | ZGC: Low Latency Garbage Collector | [ZGC](../by-topic/core/gc/) |
| 2019 | Kim Barrett | G1 GC | [G1 GC](../by-topic/core/gc/) |

---

## 按主题索引

### GC (Garbage Collection)

| 演讲者 | 会议 | 年份 | 主题 | 本地文档 |
|--------|------|------|------|----------|
| Per Liden | JVMLS | 2024 | Generational ZGC | [ZGC](../by-topic/core/gc/) |
| Stefan Karlsson | JVMLS | 2024 | 分代 ZGC 实现 | [ZGC](../by-topic/core/gc/) |
| Thomas Schatzl | JVMLS | 2024 | G1 GC Improvements | [G1 GC](../by-topic/core/gc/) |
| Roman Kennke | JVMLS | 2023 | 分代 Shenandoah | [Shenandoah](../by-topic/core/gc/) |
| Aleksey Shipilev | Devoxx | 2017 | Shenandoah GC | [Shenandoah](../by-topic/core/gc/) |
| William Kemper | JVMLS | 2024 | 分代 Shenandoah | [Shenandoah](../by-topic/core/gc/) |

### 语言设计

| 演讲者 | 会议 | 年份 | 主题 | 本地文档 |
|--------|------|------|------|----------|
| Brian Goetz | JVMLS | 2024 | Project Valhalla | [语法](../by-topic/language/syntax/) |
| Brian Goetz | - | 2022 | State of Pattern Matching | [模式匹配](../by-topic/core/patterns/) |
| Gavin Bierman | JVMLS | 2023 | Record Patterns | [模式匹配](../by-topic/core/patterns/) |
| Jan Lahoda | JVMLS | 2023 | 模式匹配编译器实现 | [语法](../by-topic/language/syntax/) |

### 并发编程

| 演讲者 | 会议 | 年份 | 主题 | 本地文档 |
|--------|------|------|------|----------|
| Ron Pressler | Devoxx | 2023 | Virtual Threads | [并发](../by-topic/concurrency/concurrency/) |
| Nathan Reynolds | JVMLS | 2023 | Structured Concurrency | [并发](../by-topic/concurrency/concurrency/) |
| David Holmes | JavaOne | 2019 | Java Concurrency | [并发](../by-topic/concurrency/concurrency/) |

### 性能优化

| 演讲者 | 会议 | 年份 | 主题 | 本地文档 |
|--------|------|------|------|----------|
| Emanuel Peter | - | 2024 | Introduction to C2 | [JIT](../by-topic/core/jit/) |
| Vladimir Kozlov | Oracle | 2021 | JIT Compilation | [JIT](../by-topic/core/jit/) |
| Claes Redestad | JVMLS | 2023 | String Deduplication | [字符串](../by-topic/language/string/) |

**Vladimir Kozlov** - JIT 编译专家
- [JIT 编译](../by-topic/core/jit/)
- **OpenJDK Wiki**: [VladimirKozlov](https://wiki.openjdk.org/display/Main/VladimirKozlov)

### 类加载与模块

| 演讲者 | 会议 | 年份 | 主题 | 本地文档 |
|--------|------|------|------|----------|
| Mandy Chung | JavaOne | 2019 | ClassLoader | [类加载](../by-topic/core/classloading/) |
| Paul Sandoz | JVMLS | 2019 | JPMS Modules | [模块](../by-topic/core/modules/) |

---

## 按贡献者索引

### A-D

#### Aleksey Shipilev - Shenandoah GC

| 会议 | 年份 | 主题 | 本地文档 |
|------|------|------|----------|
| JUG Berlin-Brandenburg | 2019 | Shenandoah GC | [档案](../by-contributor/profiles/aleksey-shipilev.md) |
| JavaZone | 2018 | Shenandoah GC | [Shenandoah](../by-topic/core/gc/) |
| Devoxx | 2017 | Shenandoah GC | [Shenandoah](../by-topic/core/gc/) |
| - | - | Shenandoah: The GC That Could | [视频](https://www.youtube.com/watch?v=VCeHkcwfF9Q) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/aleksey-shipilev.md)
- [Shenandoah GC 分析](../by-topic/core/gc/)
- [组织: Red Hat](../contributors/orgs/redhat.md)

---

### Brian Goetz - 语言设计/Project Valhalla

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| State of Valhalla | 官方文档 | [JEPs](../jeps/) |
| The State of Valhalla | 采访 | [语法](../by-topic/language/syntax/) |
| Project Valhalla Update | 视频 | [语法](../by-topic/language/syntax/) |
| State of Pattern Matching | 视频 | [模式匹配](../by-topic/core/patterns/) |

**本地资源**:
- [语法演进](../by-topic/language/syntax/)
- [模式匹配](../by-topic/core/patterns/)
- [泛型系统](../by-topic/core/generics/)
- **Inside.Java**: [@BrianGoetz](https://inside.java/u/BrianGoetz/)

---

### Per Liden - ZGC

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| JVMLS 2024 | 演讲 | [ZGC](../by-topic/core/gc/) |
| ZGC Main | Wiki | [ZGC](../by-topic/core/gc/) |
| JEP 439 | JEP | [JEP 439](../jeps/core/jep-439.md) |
| Generational ZGC | 文档 | [ZGC](../by-topic/core/gc/) |

**本地资源**:
- [ZGC 演进](../by-topic/core/gc/)
- [组织: Oracle](../contributors/orgs/oracle.md)
- **OpenJDK Wiki**: [ZGC Main](https://wiki.openjdk.org/spaces/zgc/pages/34668579/Main)

---

### Thomas Schatzl - G1 GC

| 会议 | 年份 | 主题 | 本地文档 |
|------|------|------|----------|
| FOSDEM | 2018 | G1 - Not^H^H^HNever Done! | [G1 GC](../by-topic/core/gc/) |
| JVMLS | 2024 | G1 GC Improvements | [G1 GC](../by-topic/core/gc/) |
| - | 2021 | JDK 17 G1/Parallel GC changes | [G1 GC](../by-topic/core/gc/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/thomas-schatzl.md)
- [G1 GC 演进](../by-topic/core/gc/)
- [组织: Oracle](../contributors/orgs/oracle.md)
- [个人博客](https://tschatzl.github.io/)

---

### Stefan Karlsson - 分代 ZGC

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| JVMLS 2024 | 演讲 | [ZGC](../by-topic/core/gc/) |
| JEP 439 | JEP Owner | [JEP 439](../jeps/core/jep-439.md) |

**本地资源**:
- [ZGC 演进](../by-topic/core/gc/)
- [组织: Oracle](../contributors/orgs/oracle.md)
- **OpenJDK**: [JEP 439 Owner](https://openjdk.org/jeps/439)

---

### Roman Kennke - Shenandoah GC

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| JVMLS 2023 | 演讲 | [Shenandoah](../by-topic/core/gc/) |
| JEP 429 | JEP Owner | [JEP 429](../jeps/core/jep-429.md) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/roman-kennke.md)
- [Shenandoah GC](../by-topic/core/gc/)
- [组织: Red Hat](../contributors/orgs/redhat.md)

---

### William Kemper - 分代 Shenandoah

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| JVMLS 2024 | 演讲 | [Shenandoah](../by-topic/core/gc/) |
| JDK-8355970 | PR | [分析](../by-pr/8355/8355970.md) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/william-kemper.md)
- [Shenandoah GC](../by-topic/core/gc/)
- [组织: Red Hat](../contributors/orgs/redhat.md)

---

### Emanuel Peter - C2 编译器

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| Introduction to C2 Part 1 | 博客 | [JIT](../by-topic/core/jit/) |
| Introduction to C2 Part 3 | 博客 | [JIT](../by-topic/core/jit/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/emanuel-peter.md)
- [JIT 编译](../by-topic/core/jit/)
- [性能优化](../by-topic/core/performance/)
- [个人博客](https://eme64.github.io/blog/)

---

### Gavin Bierman - 模式匹配

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| JVMLS 2023 | Record Patterns | [模式匹配](../by-topic/core/patterns/) |
| JEP 305/394/440 | JEP Author | [JEPs](../jeps/) |

**本地资源**:
- [模式匹配](../by-topic/core/patterns/)
- [语法演进](../by-topic/language/syntax/)
- [组织: Oracle](../contributors/orgs/oracle.md)
- **Inside.Java**: [@GavinBierman](https://inside.java/u/GavinBierman/)

---

### Jan Lahoda - 编译器实现

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| JVMLS 2023 | 模式匹配编译器 | [语法](../by-topic/language/syntax/) |
| JEP 相关 | JEP Owner | [JEPs](../jeps/) |

**本地资源**:
- [语法演进](../by-topic/language/syntax/)
- [Class File API](../by-topic/language/classfile/)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### David Holmes - 并发编程

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| JavaOne 2019 | Java Concurrency | [并发](../by-topic/concurrency/concurrency/) |
| JSR-166 | Spec Lead | [并发](../by-topic/concurrency/concurrency/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/david-holmes.md)
- [并发编程](../by-topic/concurrency/concurrency/)
- [网络编程](../by-topic/concurrency/network/)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Paul Sandoz - 集合/Stream API

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| Devoxx 2019 | Collections | [集合](../by-topic/api/collections/) |
| JEP 相关 | JEP Author | [JEPs](../jeps/) |

**本地资源**:
- [集合框架](../by-topic/api/collections/)
- [Stream API](../by-topic/language/streams/)
- [组织: Oracle](../contributors/orgs/oracle.md)
- **Inside.Java**: [@PaulSandoz](https://inside.java/u/PaulSandoz/)

---

### Claes Redestad - 性能优化

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| JVMLS 2023 | String Deduplication | [字符串](../by-topic/language/string/) |
| JDK-8341755 | PR 相关 | [分析](../by-pr/8341/8341755.md) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/claes-redestad.md)
- [字符串处理](../by-topic/language/string/)
- [性能优化](../by-topic/core/performance/)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Coleen Phillimore - 类加载器

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| 类加载器 | 实现 | [类加载](../by-topic/core/classloading/) |
| HotSpot 内部 | 架构 | [JVM](../by-topic/core/jit/) |
| Valhalla | 值类型 | [Valhalla](../by-topic/core/valhalla/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/coleen-phillimore.md)
- [类加载器](../by-topic/core/classloading/)
- [JVM 架构](../by-topic/core/jit/)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### David Beaumont - javac 编译器

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| javac | 编译器实现 | [语法](../by-topic/language/syntax/) |
| 构建系统 | 工具 | [构建](../by-topic/core/jit/) |
| ClassFile API | API | [ClassFile](../by-topic/core/classfile/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/david-beaumont.md)
- [javac](../by-topic/language/syntax/)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Shaojin Wen - 性能优化

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| JDK-8341755 | Lambda 优化 +15-20% | [分析](../by-pr/8341/8341755.md) |
| JDK-8349400 | Enum 优化 -82% | [分析](../by-pr/8349/8349400.md) |
| JDK-8339217 | ClassFile 优化 +5-15% | [分析](../by-pr/8339/8339217.md) |
| JDK-8339290 | UTF-8 优化 +15-30% | [分析](../by-pr/8339/8339290.md) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/shaojin-wen.md)
- [语法演进](../by-topic/language/syntax/)
- [Lambda 表达式](../by-topic/language/lambda/)
- [组织: Alibaba](../contributors/orgs/alibaba.md)

---

### Kim Barrett - JVM 运行时

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| JavaOne 2019 | G1 GC | [G1 GC](../by-topic/core/gc/) |
| JDK 相关 | C++ 现代化 | [JVM](../by-topic/core/jit/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/kim-barrett.md)
- [G1 GC](../by-topic/core/gc/)
- [JIT 编译](../by-topic/core/jit/)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Chen Liang - javac 编译器

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| javac 实现 | 编译器 | [语法](../by-topic/language/syntax/) |
| ClassFile API | API 设计 | [ClassFile](../by-topic/core/classfile/) |
| Project Valhalla | 值类型 | [Valhalla](../by-topic/core/valhalla/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/chen-liang.md)
- [javac 编译器](../by-topic/language/syntax/)
- [ClassFile API](../by-topic/core/classfile/)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Claes Redestad - 性能优化

---

### Vicente Romero - 编译器

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| JVMLS | 类型检查 | [语法](../by-topic/language/syntax/) |
| JEP 相关 | JEP Author | [JEPs](../jeps/) |

**本地资源**:
- [语法演进](../by-topic/language/syntax/)
- [模式匹配](../by-topic/core/patterns/)
- [组织: Oracle](../contributors/orgs/oracle.md)
- **Inside.Java**: [@vicente-romero](https://inside.java/u/vicente-romero/)

---

### Albert Mingkun Yang - G1 GC

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| JDK PR | G1 GC | [G1 GC](../by-topic/core/gc/) |
| 性能优化 | 内存管理 | [内存](../by-topic/core/memory/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/albert-mingkun-yang.md)
- [G1 GC](../by-topic/core/gc/)
- [内存管理](../by-topic/core/memory/)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Ron Pressler - Virtual Threads

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| Devoxx 2023 | Virtual Threads | [并发](../by-topic/concurrency/concurrency/) |
| Oracle | Virtual Threads 深度讲解 | [并发](../by-topic/concurrency/concurrency/) |

**本地资源**:
- [并发编程](../by-topic/concurrency/concurrency/)
- [Project Loom](../by-topic/core/loom/)
- [组织: Oracle](../contributors/orgs/oracle.md)
- **Inside.Java**: [@ronpressler](https://inside.java/u/ronpressler/)

---

### Nathan Reynolds - Structured Concurrency

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| JVMLS 2023 | Structured Concurrency | [并发](../by-topic/concurrency/concurrency/) |

**本地资源**:
- [并发编程](../by-topic/concurrency/concurrency/)
- [Project Loom](../by-topic/core/loom/)
- [组织: Oracle](../contributors/orgs/oracle.md)
- **OpenJDK Wiki**: [NathanReynolds](https://wiki.openjdk.org/display/Main/NathanReynolds)

---

### IoI Lam - C2 JIT 编译器

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| JIT 编译 | 实现 | [JIT](../by-topic/core/jit/) |
| 性能优化 | 演讲 | [性能](../by-topic/core/performance/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/ioi-lam.md)
- [JIT 编译](../by-topic/core/jit/)
- [性能优化](../by-topic/core/performance/)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Johannes Graham - JDK 更新

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| JDK Release | 版本管理 | [版本](../by-version/) |
| JEP 流程 | 治理 | [JEP](../jeps/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/johannes-graham.md)
- [JDK 版本](../by-version/)
- [JEP 流程](../jeps/)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Joe Darcy - 语言特性

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| Records | 语言特性 | [Records](../by-topic/core/records/) |
| Pattern Matching | 模式匹配 | [模式](../by-topic/core/patterns/) |
| Sealed Classes | 密封类 | [语法](../by-topic/language/syntax/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/joe-darcy.md)
- [Records](../by-topic/core/records/)
- [模式匹配](../by-topic/core/patterns/)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Roger Riggs - 核心库

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| 核心库 | API 设计 | [核心库](../by-topic/core/) |
| 序列化 | 实现 | [序列化](../by-topic/core/) |
| Process API | 进程管理 | [进程](../by-topic/core/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/roger-riggs.md)
- [核心库](../by-topic/core/)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Tobias Hartmann - C2 JIT 编译器

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| C2 编译器 | 实现 | [JIT](../by-topic/core/jit/) |
| JIT 优化 | 性能 | [性能](../by-topic/core/performance/) |
| Valhalla | 值类型 | [Valhalla](../by-topic/core/valhalla/) |

**本地资源**:
- [C2 编译器](../by-topic/core/jit/c2-phases.md)
- [JIT 参数](../by-topic/core/jit/vm-parameters.md)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Christian Hagedorn - C2 JIT 编译器

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| C2 编译器 | 实现 | [JIT](../by-topic/core/jit/) |
| 优化阶段 | IR | [C2](../by-topic/core/jit/c2-phases.md) |

**本地资源**:
- [C2 编译器](../by-topic/core/jit/c2-phases.md)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Vladimir Kozlov - JIT 编译器架构

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| JIT Compilation | 架构 | [JIT](../by-topic/core/jit/) |
| C2 编译器 | 实现 | [C2](../by-topic/core/jit/c2-phases.md) |

**本地资源**:
- [JIT 编译](../by-topic/core/jit/)
- [C2 优化](../by-topic/core/jit/c2-phases.md)
- [VM 参数](../by-topic/core/jit/vm-parameters.md)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Weijun Wang - 安全/加密

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| 安全 | 实现 | [安全](../by-topic/core/security/) |
| 加密 | API | [加密](../by-topic/core/security/) |
| 密钥管理 | 工具 | [密钥](../by-topic/core/security/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/weijun-wang.md)
- [安全模块](../by-topic/core/security/)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Phil Race - 2D 图形

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| 2D 图形 | 实现 | [图形](../by-topic/desktop/) |
| 渲染 | 性能 | [渲染](../by-topic/desktop/) |
| Font | 字体 | [字体](../by-topic/desktop/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/phil-race.md)
- [2D 图形](../by-topic/desktop/)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Jaikiran Pai - NIO/网络

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| NIO | 实现 | [NIO](../by-topic/io/) |
| 网络 | 编程 | [网络](../by-topic/io/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/jaikiran-pai.md)
- [NIO API](../by-topic/io/)
- [网络编程](../by-topic/io/)
- [组织: Red Hat](../contributors/orgs/redhat.md)

---

### Andrew Dinn - JVM 代码生成

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| 代码生成 | JIT | [JIT](../by-topic/core/jit/) |
| 寄存器 | 架构 | [架构](../by-topic/core/arch/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/andrew-dinn.md)
- [JIT 编译](../by-topic/core/jit/)
- [组织: Red Hat](../contributors/orgs/redhat.md)

---

### Tomas Stuefe - JVM 工具

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| JVM 工具 | 诊断 | [诊断](../by-topic/diagnostics/) |
| hsdis | 反汇编 | [工具](../by-topic/diagnostics/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/thomas-stuefe.md)
- [诊断工具](../by-topic/diagnostics/)
- [组织: SAP](../contributors/orgs/sap.md)

---

### Nick Gasson - AArch64 移植

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| AArch64 | 移植 | [AArch64](../by-topic/core/arch/aarch64.md) |
| ARM | 架构 | [架构](../by-topic/core/arch/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/nick-gasson.md)
- [AArch64](../by-topic/core/arch/aarch64.md)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Erik Joelsson - 版本管理

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| JDK 版本 | 发布 | [版本](../by-version/) |
| Git | 工具 | [工具](../by-topic/core/jit/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/erik-joelsson.md)
- [JDK 版本](../by-version/)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Erik Gahlin - JFR

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| JFR | 实现 | [JFR](../by-topic/diagnostics/) |
| 性能分析 | 工具 | [诊断](../by-topic/diagnostics/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/erik-gahlin.md)
- [JFR](../by-topic/diagnostics/)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Volkan Yazici - ZGC

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| ZGC | 实现 | [ZGC](../by-topic/core/gc/zgc.md) |
| GC | 垃圾收集 | [GC](../by-topic/core/gc/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/volkan-yazici.md)
- [ZGC](../by-topic/core/gc/zgc.md)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Leonid Mesnik - JVM 诊断

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| JVM TI | 实现 | [JVM TI](../by-topic/diagnostics/) |
| 诊断 | 工具 | [诊断](../by-topic/diagnostics/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/leonid-mesnik.md)
- [JVM TI](../by-topic/diagnostics/)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Justin Lu - ZGC

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| ZGC | 实现 | [ZGC](../by-topic/core/gc/zgc.md) |
| GC | 垃圾收集 | [GC](../by-topic/core/gc/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/justin-lu.md)
- [ZGC](../by-topic/core/gc/zgc.md)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Roland Westrelin - Graal JIT

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| Graal | JIT 编译器 | [GraalVM](../by-topic/core/graalvm/) |
| JVMCI | 接口 | [JVMCI](../by-topic/core/graalvm/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/rooland-westrelin.md)
- [GraalVM](../by-topic/core/graalvm/)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Martin Haessig - 性能分析

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| 性能 | 分析 | [性能](../by-topic/core/performance/) |
| JMH | 基准 | [性能](../by-topic/core/performance/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/martin-haessig.md)
- [性能优化](../by-topic/core/performance/)
- [组织: Red Hat](../contributors/orgs/redhat.md)

---

### Per Minborg - Java 集成

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| Java 集成 | 演讲 | [集成](../by-topic/core/) |
| Panama | FFI | [Panama](../by-topic/core/panama/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/per-minborg.md)
- [Project Panama](../by-topic/core/panama/)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Francesco Andreuzzi - GraalVM

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| GraalVM | 演讲 | [GraalVM](../by-topic/core/graalvm/) |
| Truffle | DSL | [GraalVM](../by-topic/core/graalvm/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/francesco-andreuzzi.md)
- [GraalVM](../by-topic/core/graalvm/)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Daniel Fuchs - JMX/监控

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| JMX | 实现 | [监控](../by-topic/diagnostics/) |
| 管理 | API | [管理](../by-topic/diagnostics/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/daniel-fuchs.md)
- [JMX 监控](../by-topic/diagnostics/)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Adam Sotona - 移动/嵌入式

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| 移动 | Java | [移动](../by-topic/platform/) |
| 嵌入式 | IoT | [嵌入式](../by-topic/platform/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/adam-sotona.md)
- [移动平台](../by-topic/platform/)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Jim Laskey - 字符串处理

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| 字符串 | API | [字符串](../by-topic/language/string/) |
| 模板字符串 | 特性 | [语法](../by-topic/language/syntax/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/jim-laskey.md)
- [字符串处理](../by-topic/language/string/)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Ben Perez - 性能优化

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| 性能 | 优化 | [性能](../by-topic/core/performance/) |
| JIT | 编译器 | [JIT](../by-topic/core/jit/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/ben-perez.md)
- [性能优化](../by-topic/core/performance/)
- [JIT 编译](../by-topic/core/jit/)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Matthias Baesken - 支持/诊断

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| 支持 | 工具 | [诊断](../by-topic/diagnostics/) |
| Windows | 平台 | [Windows](../by-topic/platform/windows/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/matthias-baesken.md)
- [诊断工具](../by-topic/diagnostics/)
- [Windows 平台](../by-topic/platform/windows/)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Naoto Sato - 国际化

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| i18n | 国际化 | [国际化](../by-topic/core/i18n/) |
| Locale | 本地化 | [本地化](../by-topic/core/i18n/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/naoto-sato.md)
- [国际化](../by-topic/core/i18n/)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Magnus Ihse Bursie - 构建系统

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| 构建 | 工具 | [构建](../by-topic/core/jit/) |
| make | 实现 | [构建](../by-topic/core/jit/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/magnus-ihse-bursie.md)
- [构建系统](../by-topic/core/jit/)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Brian Burkhalter - 数学库

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| Math | 数学库 | [核心库](../by-topic/core/) |
| BigDecimal | 精度 | [核心库](../by-topic/core/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/brian-burkhalter.md)
- [核心库](../by-topic/core/)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Prasanta Sadhukhan - Web 服务

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| JAX-WS | Web 服务 | [Web](../by-topic/web/) |
| XML | 处理 | [XML](../by-topic/web/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/prasanta-sadhukhan.md)
- [Web 服务](../by-topic/web/)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Jatin Bhateja - ZGC

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| ZGC | 实现 | [ZGC](../by-topic/core/gc/zgc.md) |
| GC | 垃圾收集 | [GC](../by-topic/core/gc/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/jatin-bhateja.md)
- [ZGC](../by-topic/core/gc/zgc.md)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Anatoly Zelenin - JVM 运行时

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| 运行时 | 实现 | [JVM](../by-topic/core/jit/) |
| 内存 | 管理 | [内存](../by-topic/core/memory/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/anatoly-zelenin.md)
- [JVM 运行时](../by-topic/core/jit/)
- [内存管理](../by-topic/core/memory/)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Alexey Semenyuk - JFR

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| JFR | 实现 | [JFR](../by-topic/diagnostics/) |
| 性能 | 分析 | [诊断](../by-topic/diagnostics/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/alexey-semenyuk.md)
- [JFR](../by-topic/diagnostics/)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Amit Kumar - 安全

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| 安全 | 实现 | [安全](../by-topic/core/security/) |
| 加密 | 算法 | [加密](../by-topic/core/security/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/amit-kumar.md)
- [安全模块](../by-topic/core/security/)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### Yasumasa Suenaga - ZGC

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| ZGC | 移植 | [ZGC](../by-topic/core/gc/zgc.md) |
| 文档 | 翻译 | [文档](../by-topic/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/yasumasa-suenaga.md)
- [ZGC](../by-topic/core/gc/zgc.md)
- [组织: Fujitsu](../contributors/orgs/)

---

### Mandy Chung - 类加载

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| JavaOne 2019 | ClassLoader | [类加载](../by-topic/core/classloading/) |
| Oracle | 类加载器详解 | [类加载](../by-topic/core/classloading/) |

**本地资源**:
- [类加载器](../by-topic/core/classloading/)
- [模块系统](../by-topic/core/modules/)
- [组织: Oracle](../contributors/orgs/oracle.md)
- **Inside.Java**: [@mchung](https://inside.java/u/mchung/)

---

### Goetz Lindenmaier - HotSpot Runtime

| 资源 | 类型 | 本地文档 |
|------|------|----------|
| HotSpot 内部 | 文档 | [JVM](../by-topic/core/jit/) |
| 运行时优化 | 演讲 | [性能](../by-topic/core/performance/) |

**本地资源**:
- [贡献者档案](../by-contributor/profiles/goetz-lindenmaier.md)
- [JIT 编译](../by-topic/core/jit/)
- [性能优化](../by-topic/core/performance/)
- [组织: Oracle](../contributors/orgs/oracle.md)

---

### 更多贡献者

查看完整的贡献者列表：
- [贡献者索引](../by-contributor/)
- [组织统计](../contributors/orgs/)

---

## 相关链接

### 本地文档

- [按主题浏览](../by-topic/) - 跨版本技术演进
- [按版本浏览](../by-version/) - JDK 版本指南
- [PR 分析](../by-pr/) - 深度 Issue/PR 分析
- [JEP 分析](../jeps/) - JDK Enhancement Proposals

### 官方资源

- [OpenJDK Wiki](https://wiki.openjdk.org/)
- [OpenJDK YouTube](https://www.youtube.com/@OpenJDK)
- [Inside.Java](https://inside.java/)
- [JVMLS 官方](https://openjdk.org/projects/mlvm/jvmlangsummit/)

### 研究工具

- [JVMLS 演讲资料收集](../scripts/jvmls-talks-research.md) - 详细的收集清单
- [Agent 研究方法](../AGENTS.md) - 文档分析方法论

---

**最后更新**: 2026-03-20

**Sources**:
- [JVMLS 2024 - OpenJDK](https://openjdk.org/projects/mlvm/summit2024/)
- [JVMLS 2024 - YouTube](https://www.youtube.com/playlist?list=PLX8CzqL3ArzUEYnTa6KYORRbP3nhsK0L1)
- [Aleksey Shipilev - Talks](https://shipilev.net/)
- [Brian Goetz - Valhalla](https://cr.openjdk.org/~briangoetz/valhalla/sov/)
- [Thomas Schatzl - Blog](https://tschatzl.github.io/)
- [Emanuel Peter - Blog](https://eme64.github.io/blog/)
