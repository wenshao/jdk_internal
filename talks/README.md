# 技术演讲 Technical Talks

> JVM Language Summit (JVMLS) 及其他重要 Java 技术会议的演讲索引
>
> 本页仅收录可验证的演讲（有视频链接或会议存档），不收录未经确认的内容。

---

## 目录

1. [概述](#1-概述)
2. [JVMLS 按年份](#2-jvmls-按年份)
3. [其他重要会议](#3-其他重要会议)
4. [推荐观看](#4-推荐观看)
5. [贡献者演讲主页](#5-贡献者演讲主页)

---

## 1. 概述

### JVM Language Summit (JVMLS) 是什么

**JVM Language Summit** 是 OpenJDK 社区主办的年度技术峰会，每年 8 月在 Oracle 总部
(Santa Clara, CA) 举行。会议采用单轨道 (single-track) 形式，由 JVM 工程师和语言设计者
做 30-60 分钟深度技术报告，穿插 workshop 和 lightning talk。

JVMLS 的特点：

- **面向实现者 (implementors)**：不是营销/产品发布，而是编译器、GC、运行时的核心设计讨论
- **小规模高密度**：2.5 天，约 20-30 场 talk，观众约 100 人
- **覆盖所有 OpenJDK 大项目**：Amber, Loom, Panama, Valhalla, Leyden, Babylon, Lilliput 等
- **全程录像**：所有 talk 发布到 YouTube / [Inside.java](https://inside.java/)
- **workshop 和 lightning talk**：传统 30-60 分钟 talk 穿插开放式 workshop 和即兴 lightning talk，
  鼓励与会者进行深入的技术讨论

### 为什么重要

JVMLS talk 是了解 JDK 内部技术方向的**最佳一手资料**。JEP 文档描述 "what"，而 JVMLS talk
解释 "why" 和 "how"——设计权衡 (design trade-offs)、实现难点 (implementation challenges)、
未来路线图 (roadmap)。

**对本知识库的价值**：

- 理解 JEP 背后的动机：比如 [JEP 439 Generational ZGC](../jeps/gc/jep-439.md)，
  通过 Per Liden 的 JVMLS talk 可以理解为什么选择分代设计
- 跟踪项目进展：Valhalla 每年都有 "State of Valhalla" talk，展示最新进展和设计变更
- 了解实现细节：Ron Pressler 的 Continuations talk 深入讲解了虚拟线程的底层实现

### 官方资源

| 资源 | 链接 | 说明 |
|------|------|------|
| JVMLS 官方页面 | [openjdk.org](https://openjdk.org/projects/mlvm/jvmlangsummit/) | 日程、注册、历届信息 |
| OpenJDK YouTube | [youtube.com/@OpenJDK](https://www.youtube.com/@OpenJDK) | 所有 JVMLS 录像 |
| Inside.java | [inside.java](https://inside.java/) | Oracle 官方 Java 技术博客，含 JVMLS 视频和文字总结 |
| Inside.java 作者索引 | [inside.java/u](https://inside.java/u) | 按演讲者浏览 Inside.java 文章 |
| InfoQ JVMLS | [infoq.com/jvmlanguagesummit](https://www.infoq.com/jvmlanguagesummit/) | 第三方报道和总结 |

### JVMLS 与 JEP 的关系

许多 JEP 在正式提交前都会在 JVMLS 上做过演讲。以下是本知识库中重要 JEP 与对应 JVMLS talk 的映射：

| JEP | 标题 | 对应 JVMLS Talk | 演讲者 | 本地文档 |
|-----|------|-----------------|--------|----------|
| [JEP 439](../jeps/gc/jep-439.md) | Generational ZGC | JVMLS 2023: Generational ZGC and Beyond | Per Liden, Stefan Karlsson | [ZGC](../by-topic/core/gc/zgc.md) |
| [JEP 444](../jeps/concurrency/jep-444.md) | Virtual Threads | JVMLS 2023: Continuations Under the Covers | Ron Pressler | [Loom](../by-topic/core/loom/) |
| JEP 401 | Value Classes and Objects | JVMLS 2025: Value Classes Heap Flattening | Frederic Parain | [Valhalla](../by-topic/core/valhalla/) |
| JEP 521 | Generational Shenandoah | (尚未在 JVMLS 演讲) | William Kemper | [Shenandoah](../by-topic/core/gc/shenandoah.md) |

> 提示：JVMLS talk 通常比 JEP 文档提供更多的设计背景。如果你想理解某个 JEP 的 "why"，
> 搜索对应的 JVMLS talk 是最好的方式。

### 主要 OpenJDK 项目与 JVMLS 覆盖

| 项目 | 描述 | JVMLS 覆盖 | 本地文档 |
|------|------|-----------|----------|
| **Amber** | 语言特性演进 (records, sealed classes, pattern matching) | 每年 Brian Goetz 演讲 | [语法](../by-topic/language/syntax/) |
| **Loom** | Virtual threads, structured concurrency | 2023-2024 Ron Pressler & Alan Bateman | [Loom](../by-topic/core/loom/) |
| **Panama** | Foreign Function & Memory API, Vector API | 2024-2025 Paul Sandoz | [Panama](../by-topic/core/panama/) |
| **Valhalla** | Value types, primitive classes | 每年 Brian Goetz / Dan Smith | [Valhalla](../by-topic/core/valhalla/) |
| **Leyden** | AOT 优化, 启动性能, CDS | 2024-2025 Ioi Lam | [JIT](../by-topic/core/jit/) |
| **Babylon** | Code reflection, GPU acceleration | 2024-2025 Paul Sandoz | [Panama](../by-topic/core/panama/) |
| **Lilliput** | 减少对象头大小 | Roman Kennke (FOSDEM) | [GC](../by-topic/core/gc/) |
| **ZGC** | Scalable low-latency GC | 每年 Per Liden / Erik Österlund | [ZGC](../by-topic/core/gc/zgc.md) |

### 如何使用本页

本页消除了旧版按年份、按主题、按贡献者三重重复列表的问题，改为互补结构：

1. **第 2 节 "JVMLS 按年份"**：每年的完整 talk 列表（带视频链接），最权威的记录
2. **第 3 节 "其他重要会议"**：非 JVMLS 的重要演讲
3. **第 4 节 "推荐观看"**：按主题精选的 "must watch" 列表，从第 2、3 节中挑选
4. **第 5 节 "贡献者演讲主页"**：每个演讲者的主页链接，不重复列出每场 talk

**查找某个 talk**：使用浏览器 Ctrl+F 搜索演讲者名字或关键词。

### JVMLS 常见主题演进 Topic Evolution

以下主题在 JVMLS 反复出现，可通过对比历年 talk 看到项目演进：

| 主题 | 2023 | 2024 | 2025 | 本地文档 |
|------|------|------|------|----------|
| **Valhalla / Value Types** | Dan Smith: Value Objects in Valhalla | Brian Goetz: Where Are We? | Frederic Parain: JEP 401 Heap Flattening | [Valhalla](../by-topic/core/valhalla/) |
| **Loom / Virtual Threads** | Ron Pressler: Continuations; Alan Bateman: Challenges | Ron Pressler: Where Are We? | - | [Loom](../by-topic/core/loom/) |
| **ZGC** | Per Liden: Generational ZGC | Joel Sikström: Auto Heap Sizing | Erik Österlund: Colored Pointers | [ZGC](../by-topic/core/gc/zgc.md) |
| **Project Leyden** | - | Ioi Lam: Project Leyden | Ioi Lam: Assembling Leyden | [JIT](../by-topic/core/jit/) |
| **Project Babylon** | - | Paul Sandoz: Code Reflection | Paul Sandoz: Symbolic Modeling | [Panama](../by-topic/core/panama/) |
| **Keynote** | Saab & Reinhold | Saab & Reinhold: Java in 2024 | Brian Goetz: Growing Java | - |

---

## 2. JVMLS 按年份

> 以下按最近到最早排列。每年列出有视频链接或 Inside.java 文章的演讲。

### JVMLS 2025 (8月4-6日)

- **播放列表**: [YouTube Playlist](https://www.youtube.com/playlist?list=PLX8CzqL3ArzUOgZpIX6GsoRhPbnij-sco)
- **官方页面**: [openjdk.org/projects/mlvm/jvmlangsummit](https://openjdk.org/projects/mlvm/jvmlangsummit/)
- **预告**: [Inside.java 公告](https://inside.java/2025/07/01/jvmls2025/)

JVMLS 2025 的核心主题：Project Leyden 交付了 JDK 24/25 中的 JEP，Valhalla 的 JEP 401 Value Classes
进入实现阶段，ZGC 继续演进 colored pointer 设计，Babylon 项目的 symbolic modeling 逐渐成熟。

| 演讲者 | 主题 | 视频链接 | 本地文档 |
|--------|------|----------|----------|
| Brian Goetz (Oracle) | Growing the Java Language | [Inside.java](https://inside.java/2025/08/21/jvmls-growing-java-language/) | [语法](../by-topic/language/syntax/) |
| John Rose (Oracle) | The Static Dynamic JVM — A Many Layered Dive | [Inside.java](https://inside.java/2026/01/11/jvmls-static-dynamic-jvm/) | [JVM](../by-topic/core/jvm/) |
| Erik Österlund (Oracle) | Evolving ZGC's Pointer Color Palette | [Inside.java](https://inside.java/2025/10/06/jvmls-zgc-colored-pointers/) | [ZGC](../by-topic/core/gc/zgc.md) |
| Ioi Lam 等 (Oracle) | Assembling Project Leyden | [Inside.java](https://inside.java/2025/10/21/jvmls-assembling-project-leyden/) | [JIT](../by-topic/core/jit/) |
| Frederic Parain (Oracle) | Value Classes Heap Flattening — What to Expect from JEP 401 | [Inside.java](https://inside.java/2025/10/31/jvmls-jep-401/) | [Valhalla](../by-topic/core/valhalla/) |
| Paul Sandoz (Oracle) | Beyond the Vector API — A Quest for a Lower Level API | [Inside.java](https://inside.java/2025/11/16/jvmls-vector-api/) | [Performance](../by-topic/core/performance/) |
| Paul Sandoz 等 (Oracle) | Symbolic Modeling and Transformation of Java Code | [Inside.java](https://inside.java/2025/11/22/jvmls-symbolic-modelling-java-transformation/) | [JIT](../by-topic/core/jit/) |

**关键看点**：

- Brian Goetz 的 "Growing the Java Language" 获得了 30k+ 观看量，讨论了 Java 语言演进的哲学
  和未来方向，包括 pattern matching 的下一步和 value types 如何影响语言设计
- John Rose 深入探讨了 JVM 如何在静态分析和动态执行之间取得平衡
- Erik Österlund 讲解了 ZGC 的 colored pointer 从非分代到分代 ZGC 的演进，
  以及为 thread-local GC 做的准备
- Project Leyden 已经在 JDK 24 和 JDK 25 中交付了具体的 JEP

### JVMLS 2024 (8月5-7日)

- **播放列表**: [YouTube Playlist](https://www.youtube.com/playlist?list=PLX8CzqL3ArzUEYnTa6KYORRbP3nhsK0L1)
- **官方页面**: [openjdk.org/projects/mlvm/summit2024](https://openjdk.org/projects/mlvm/summit2024/)
- **Inside Java Newscast #75**: [Best of Java Performance](https://inside.java/2024/08/29/newscast-75/)

JVMLS 2024 三天议程涵盖 Project Babylon (code reflection)、Leyden (AOT 优化)、
Valhalla (value types)、Loom (virtual threads) 等核心项目的最新进展。

| 演讲者 | 主题 | 视频链接 | 本地文档 |
|--------|------|----------|----------|
| Georges Saab, Mark Reinhold (Oracle) | Keynote: Java in 2024 | [Inside.java](https://inside.java/2024/08/12/jvmls-keynote/) | [JDK 21](../by-version/jdk21/) |
| Brian Goetz (Oracle) | Valhalla — Where Are We? | [Inside.java](https://inside.java/2024/08/23/jvmls-valhalla/) | [Valhalla](../by-topic/core/valhalla/) |
| Paul Sandoz (Oracle) | Project Babylon — Code Reflection | [Inside.java](https://inside.java/2024/08/14/jvmls-code-reflection/) | [JIT](../by-topic/core/jit/) |
| Ioi Lam, Dan Heidinga (Oracle) | Project Leyden | [Inside.java](https://inside.java/2024/08/25/jvmls-leyden/) | [JIT](../by-topic/core/jit/) |
| Ron Pressler 等 (Oracle) | Loom — Where Are We? | [Inside.java](https://inside.java/2024/10/06/jvmls-loom/) | [Loom](../by-topic/core/loom/) |
| Paul Sandoz, Gary Frost (Oracle) | HAT (Heterogeneous Accelerator Toolkit) Update | [Inside.java](https://inside.java/2024/09/30/jvmls-hat/) | [Performance](../by-topic/core/performance/) |
| Joel Sikström (Oracle) | ZGC Automatic Heap Sizing | [Inside.java](https://inside.java/2024/11/09/jvmls-zgc/) | [ZGC](../by-topic/core/gc/zgc.md) |

**关键看点**：

- Georges Saab 和 Mark Reinhold 的 keynote 回顾了 Java 在 2024 年的整体状态
- Brian Goetz 展示了 Valhalla 从概念到实现的进展，介绍了 value classes 的设计决策
- Project Babylon 首次在 JVMLS 亮相，Paul Sandoz 展示了 code reflection API
  和 code model 的设计思路
- HAT 项目展示了如何通过 Babylon 让 Java 访问 GPU 加速
- Joel Sikström 讲解了 ZGC 的自动堆大小调整目标——最小化用户配置，只需设置堆大小

### JVMLS 2023 (8月7-9日)

- **播放列表**: [YouTube Playlist](https://www.youtube.com/playlist?list=PLX8CzqL3ArzW90jKUCf4H6xCKpStxsOzp)
- **官方页面**: [openjdk.org/projects/mlvm/summit2023](https://openjdk.org/projects/mlvm/summit2023/)

JVMLS 2023 正值 JDK 21 LTS 发布前夕，virtual threads (JEP 444) 和 generational ZGC (JEP 439)
成为焦点话题。

| 演讲者 | 主题 | 视频链接 | 本地文档 |
|--------|------|----------|----------|
| Georges Saab, Mark Reinhold (Oracle) | Keynote | [Inside.java](https://inside.java/2023/09/14/jvmls-keynote/) | [JDK 21](../by-version/jdk21/) |
| Dan Smith (Oracle) | Value Objects in Valhalla | [Inside.java](https://inside.java/2023/09/05/value-objects-in-valhalla/) | [Valhalla](../by-topic/core/valhalla/) |
| Ron Pressler (Oracle) | Continuations Under the Covers | [Inside.java](https://inside.java/2023/08/26/continuations-under-the-covers/) | [Loom](../by-topic/core/loom/) |
| Per Liden, Stefan Karlsson (Oracle) | Generational ZGC and Beyond | [Inside.java](https://inside.java/2023/08/31/generational-zgc-and-beyond/) | [ZGC](../by-topic/core/gc/zgc.md) |
| Alan Bateman (Oracle) | The Challenges of Introducing Virtual Threads | [视频](https://www.youtube.com/watch?v=Ma0NtbG0mHY) | [Loom](../by-topic/core/loom/) |

**关键看点**：

- Ron Pressler 深入讲解了 continuations 的底层实现，这是理解 virtual threads 工作原理的核心
- Per Liden 和 Stefan Karlsson 展示了 Generational ZGC 的设计动机和实现方案，
  即将在 JDK 21 中通过 [JEP 439](../jeps/gc/jep-439.md) 交付
- Alan Bateman 讨论了将 virtual threads 引入 Java 平台面临的挑战，包括与现有 API 的兼容性问题
- Dan Smith 展示了 Valhalla 中 value objects 的语义和 JVM 支持

### JVMLS 2019 (7月29-31日)

- **播放列表**: [YouTube Playlist](https://www.youtube.com/playlist?list=PLX8CzqL3ArzXFRVYmbvZfZQ0CQMfIIFCH)

JVMLS 2019 是 COVID-19 之前的最后一次线下 JVMLS。Loom 项目的 virtual threads 还处于
早期原型阶段，Shenandoah 刚进入 JDK 12 (JEP 189)，ZGC 在 JDK 11 中以实验状态加入。

> 注意：2019 年的 talk 列表已较久远，本页不逐一列出。请直接查看 YouTube 播放列表。

### 往届 JVMLS (2013-2018)

| 年份 | 日期 | 官方页面 | 说明 |
|------|------|----------|------|
| 2018 | 7月30-31日 | [openjdk.org](https://openjdk.org/projects/mlvm/summit2018/) | Graal 和 Truffle 是热点话题 |
| 2017 | 7月31日-8月1日 | [openjdk.org](https://openjdk.org/projects/mlvm/summit2017/) | Value types 早期探索 |
| 2016 | 8月1-3日 | [openjdk.org](https://openjdk.org/projects/mlvm/summit2016/) | Project Panama 早期讨论 |
| 2013 | 7月 | [openjdk.org](https://openjdk.org/projects/mlvm/summit2013/) | Lambda (JDK 8) 实现讨论 |

> **2020-2022 年**：因 COVID-19 疫情停办或转为线上形式。2023 年恢复线下举办。

---

## 3. 其他重要会议

### FOSDEM (Free and Open Source Developers' European Meeting)

每年 2 月在布鲁塞尔举行的大型开源开发者会议，设有专门的 **Free Java devroom**。
GC 相关的演讲质量很高，尤其是 Shenandoah 和 G1 的深度报告。

| 年份 | 演讲者 | 主题 | 链接 | 本地文档 |
|------|--------|------|------|----------|
| 2024 | Roman Kennke (Amazon) | Shenandoah GC Update | [FOSDEM Archive](https://archive.fosdem.org/2024/schedule/speaker/KQYDEV/) | [Shenandoah](../by-topic/core/gc/shenandoah.md) |
| 2018 | Thomas Schatzl (Oracle) | G1 — Never Done! | [FOSDEM 2018 Archive](https://archive.fosdem.org/2018/) | [G1 GC](../by-topic/core/gc/g1-gc.md) |

### Devoxx

欧洲最大的 Java 开发者会议系列，每年在比利时 (Devoxx BE)、法国 (Devoxx FR) 等地举行。
演讲录像通常发布到 YouTube 的 Devoxx 频道。

| 年份 | 演讲者 | 主题 | 链接 | 本地文档 |
|------|--------|------|------|----------|
| 2024 | Alan Bateman (Oracle) | Loom's Next Phases (Live Q&A) | [Inside.java](https://inside.java/2024/10/09/loom-next/) | [Loom](../by-topic/core/loom/) |
| 2017 | Aleksey Shipilev (Red Hat→Amazon) | Shenandoah: The GC That Could | [YouTube](https://www.youtube.com/watch?v=VCeHkcwfF9Q) | [Shenandoah](../by-topic/core/gc/shenandoah.md) |

### JavaOne

Oracle 主办的旗舰 Java 会议。2018 年停办后于 **2025 年回归**。

| 年份 | 演讲者 | 主题 | 链接 | 本地文档 |
|------|--------|------|------|----------|
| 2025 | Brian Goetz 等 (Oracle) | Ask the Java Architects | [Inside.java](https://inside.java/2025/12/15/javaone-ask-java-architects/) | [Valhalla](../by-topic/core/valhalla/) |
| 2025 | Erik Österlund 等 (Oracle) | ZGC — Paving the GC On-Ramp | [Inside.java](https://inside.java/2025/07/10/javaone-zgc/) | [ZGC](../by-topic/core/gc/zgc.md) |

### QCon / InfoQ

InfoQ 平台上有大量 Java 和 JVM 相关的技术演讲和采访。

| 演讲者 | 主题 | 链接 | 本地文档 |
|--------|------|------|----------|
| Ron Pressler (Oracle) | Java's Project Loom, Virtual Threads and Structured Concurrency | [InfoQ Podcast](https://www.infoq.com/podcasts/java-project-loom/) | [Loom](../by-topic/core/loom/) |

### Inside Java Podcast

Oracle 官方 Java 播客，由 Java Developer Relations 团队制作。

| 期数 | 嘉宾 | 主题 | 链接 | 本地文档 |
|------|------|------|------|----------|
| #38 | Ron Pressler | Integrity by Default | [Inside.java](https://inside.java/2025/06/24/podcast-038/) | [Loom](../by-topic/core/loom/) |

### Inside Java Newscast

Inside Java Newscast 是 Oracle 定期发布的视频新闻节目，经常包含对 JVMLS 内容的总结和分析。

| 期数 | 主题 | 链接 |
|------|------|------|
| #75 | Best of Java Performance (含 JVMLS 2024 内容) | [Inside.java](https://inside.java/2024/08/29/newscast-75/) |
| #83 | Java's Plans for 2025 | [Inside.java](https://inside.java/2025/01/16/newscast-83/) |
| #103 | Java's 2025 in Review | [Inside.java](https://inside.java/2025/12/18/newscast-103/) |

### Aleksey Shipilev 的独立演讲

Aleksey Shipilev 在多个 JUG (Java User Group) 和技术会议上发表过 Shenandoah 相关演讲。
他的个人网站 [shipilev.net](https://shipilev.net/) 收录了所有演讲的幻灯片。

| 年份 | 会议 | 主题 | 链接 |
|------|------|------|------|
| 2019 | JUG Berlin-Brandenburg | Shenandoah GC 2.0: The Great Revolution | [幻灯片 (PDF)](https://shipilev.net/talks/jugbb-Sep2019-shenandoah.pdf) |
| 2017 | Devoxx | Shenandoah: The GC That Could | [YouTube](https://www.youtube.com/watch?v=VCeHkcwfF9Q) |

### Thomas Schatzl 的博客

Thomas Schatzl 在他的个人博客上定期发布 G1 GC 的变更记录，
是了解 G1 逐版本变化的最佳资料。

- **博客地址**: [tschatzl.github.io](https://tschatzl.github.io/)
- **内容**: 每个 JDK 版本的 G1/Parallel GC 变更汇总
- **本地文档**: [G1 GC](../by-topic/core/gc/g1-gc.md)

### Emanuel Peter 的博客

Emanuel Peter 在博客上发布了 C2 JIT 编译器的深度技术文章，
是目前公开可获得的最好的 C2 入门资料。

- **博客地址**: [eme64.github.io/blog](https://eme64.github.io/blog/)
- **内容**: Introduction to C2 系列文章, auto-vectorization, SuperWord 优化
- **本地文档**: [JIT 编译](../by-topic/core/jit/), [C2 优化阶段](../by-topic/core/jit/c2-phases.md)

---

## 4. 推荐观看

按主题精选最值得观看的演讲，涵盖 GC、并发 (Loom)、语言设计 (Amber/Valhalla)、
性能 (JIT/Leyden)、FFI (Panama) 五大领域。

> **阅读建议**：第 2 节 "JVMLS 按年份" 列出了所有已确认的 talk。
> 本节从中精选 "must watch" 级别的演讲，按主题组织，方便快速定位。
> 已在第 2 节出现的 talk 在这里以简短形式列出，不重复完整描述。

### GC (Garbage Collection)

理解 Java GC 演进的核心演讲。ZGC、Shenandoah、G1 三大 collector 的设计者亲自讲解。

| 演讲 | 演讲者 | 会议 | 视频 | 本地文档 |
|------|--------|------|------|----------|
| Evolving ZGC's Pointer Color Palette | Erik Österlund (Oracle) | JVMLS 2025 | [Inside.java](https://inside.java/2025/10/06/jvmls-zgc-colored-pointers/) | [ZGC](../by-topic/core/gc/zgc.md) |
| ZGC Automatic Heap Sizing | Joel Sikström (Oracle) | JVMLS 2024 | [Inside.java](https://inside.java/2024/11/09/jvmls-zgc/) | [ZGC](../by-topic/core/gc/zgc.md) |
| Generational ZGC and Beyond | Per Liden, Stefan Karlsson (Oracle) | JVMLS 2023 | [Inside.java](https://inside.java/2023/08/31/generational-zgc-and-beyond/) | [JEP 439](../jeps/gc/jep-439.md) |
| ZGC — Paving the GC On-Ramp | Erik Österlund 等 (Oracle) | JavaOne 2025 | [Inside.java](https://inside.java/2025/07/10/javaone-zgc/) | [ZGC](../by-topic/core/gc/zgc.md) |
| Shenandoah: The GC That Could | Aleksey Shipilev (Red Hat→Amazon) | Devoxx 2017 | [YouTube](https://www.youtube.com/watch?v=VCeHkcwfF9Q) | [Shenandoah](../by-topic/core/gc/shenandoah.md) |

**为什么推荐**：
- ZGC 三部曲 (2023 Generational → 2024 Auto Heap Sizing → 2025 Colored Pointers) 展示了
  ZGC 从分代设计到自动化配置再到下一代 thread-local GC 的完整演进路线
- Aleksey Shipilev 的 Shenandoah talk 是经典中的经典，讲解了 concurrent compaction 的核心算法

**相关本地文档**: [GC 演进](../by-topic/core/gc/), [G1 GC](../by-topic/core/gc/g1-gc.md),
[Shenandoah](../by-topic/core/gc/shenandoah.md), [JEP 439](../jeps/gc/jep-439.md)

### Loom / 并发 Concurrency

Virtual threads 从设计到实现的核心演讲。

| 演讲 | 演讲者 | 会议 | 视频 | 本地文档 |
|------|--------|------|------|----------|
| Loom — Where Are We? | Ron Pressler 等 (Oracle) | JVMLS 2024 | [Inside.java](https://inside.java/2024/10/06/jvmls-loom/) | [Loom](../by-topic/core/loom/) |
| Continuations Under the Covers | Ron Pressler (Oracle) | JVMLS 2023 | [Inside.java](https://inside.java/2023/08/26/continuations-under-the-covers/) | [JEP 444](../jeps/concurrency/jep-444.md) |
| The Challenges of Introducing Virtual Threads | Alan Bateman (Oracle) | JVMLS 2023 | [视频](https://www.youtube.com/watch?v=Ma0NtbG0mHY) | [Loom](../by-topic/core/loom/) |
| Loom's Next Phases (Live Q&A) | Alan Bateman (Oracle) | Devoxx BE 2024 | [Inside.java](https://inside.java/2024/10/09/loom-next/) | [Loom](../by-topic/core/loom/) |

**为什么推荐**：
- Ron Pressler 的 "Continuations Under the Covers" 是理解 virtual threads 底层实现的最佳资料，
  深入讲解了 continuation 如何 freeze/thaw stack frames
- Alan Bateman 的 talk 从 API 设计角度讨论了兼容性挑战——
  如何让 `java.net.Socket` 等旧 API 透明地支持 virtual threads

**相关本地文档**: [Loom](../by-topic/core/loom/), [并发](../by-topic/concurrency/),
[JEP 444](../jeps/concurrency/jep-444.md)

### Amber / Valhalla / 语言设计 Language Design

Java 语言演进的设计哲学和实现进展。

| 演讲 | 演讲者 | 会议 | 视频 | 本地文档 |
|------|--------|------|------|----------|
| Growing the Java Language | Brian Goetz (Oracle) | JVMLS 2025 | [Inside.java](https://inside.java/2025/08/21/jvmls-growing-java-language/) | [语法](../by-topic/language/syntax/) |
| Valhalla — Where Are We? | Brian Goetz (Oracle) | JVMLS 2024 | [Inside.java](https://inside.java/2024/08/23/jvmls-valhalla/) | [Valhalla](../by-topic/core/valhalla/) |
| Value Objects in Valhalla | Dan Smith (Oracle) | JVMLS 2023 | [Inside.java](https://inside.java/2023/09/05/value-objects-in-valhalla/) | [Valhalla](../by-topic/core/valhalla/) |
| Value Classes Heap Flattening (JEP 401) | Frederic Parain (Oracle) | JVMLS 2025 | [Inside.java](https://inside.java/2025/10/31/jvmls-jep-401/) | [Valhalla](../by-topic/core/valhalla/) |

**为什么推荐**：
- Brian Goetz 的演讲是理解 Java 语言设计哲学的必看内容——
  Java 不追求 "最新特性"，而是追求 "正确的特性"
- Valhalla 从概念到 JEP 401 实现经历了近 10 年，这些 talk 展示了设计如何随时间演变

**相关本地文档**: [Valhalla](../by-topic/core/valhalla/), [模式匹配](../by-topic/core/patterns/),
[Records](../by-topic/core/records/), [泛型](../by-topic/core/generics/)

### Panama / Babylon / FFI

Foreign Function & Memory API 以及 Project Babylon 的 code reflection。

| 演讲 | 演讲者 | 会议 | 视频 | 本地文档 |
|------|--------|------|------|----------|
| Project Babylon — Code Reflection | Paul Sandoz (Oracle) | JVMLS 2024 | [Inside.java](https://inside.java/2024/08/14/jvmls-code-reflection/) | [Panama](../by-topic/core/panama/) |
| Beyond the Vector API | Paul Sandoz (Oracle) | JVMLS 2025 | [Inside.java](https://inside.java/2025/11/16/jvmls-vector-api/) | [Performance](../by-topic/core/performance/) |
| HAT (Heterogeneous Accelerator Toolkit) | Paul Sandoz, Gary Frost (Oracle) | JVMLS 2024 | [Inside.java](https://inside.java/2024/09/30/jvmls-hat/) | [Performance](../by-topic/core/performance/) |
| Symbolic Modeling and Transformation of Java Code | Paul Sandoz 等 (Oracle) | JVMLS 2025 | [Inside.java](https://inside.java/2025/11/22/jvmls-symbolic-modelling-java-transformation/) | [JIT](../by-topic/core/jit/) |

**为什么推荐**：
- Project Babylon 是 Java 访问 GPU 和异构加速器的关键项目，
  HAT 展示了如何通过 code reflection 让 Java 代码在 GPU 上运行
- Paul Sandoz 的 Vector API talk 展示了超越当前 API 的下一步——
  提供更底层的机器指令访问

**相关本地文档**: [Panama](../by-topic/core/panama/)

### Performance / JIT / Leyden

JIT 编译、AOT 优化、Project Leyden 的演进。

| 演讲 | 演讲者 | 会议 | 视频 | 本地文档 |
|------|--------|------|------|----------|
| The Static Dynamic JVM — A Many Layered Dive | John Rose (Oracle) | JVMLS 2025 | [Inside.java](https://inside.java/2026/01/11/jvmls-static-dynamic-jvm/) | [JIT](../by-topic/core/jit/) |
| Assembling Project Leyden | Ioi Lam 等 (Oracle) | JVMLS 2025 | [Inside.java](https://inside.java/2025/10/21/jvmls-assembling-project-leyden/) | [JIT](../by-topic/core/jit/) |
| Project Leyden | Ioi Lam, Dan Heidinga (Oracle) | JVMLS 2024 | [Inside.java](https://inside.java/2024/08/25/jvmls-leyden/) | [JIT](../by-topic/core/jit/) |
| Keynote: Java in 2024 | Georges Saab, Mark Reinhold (Oracle) | JVMLS 2024 | [Inside.java](https://inside.java/2024/08/12/jvmls-keynote/) | [JDK 21](../by-version/jdk21/) |

**为什么推荐**：
- John Rose 是 JVM 架构的核心设计者 (invokedynamic, method handles 等)，
  他的 "Static Dynamic JVM" 探讨了 JVM 在静态/动态之间的平衡
- Project Leyden 对比 2024 和 2025 两年的 talk 可以看到实质性进展——
  从概念走向在 JDK 24/25 中交付的具体 JEP

**相关本地文档**: [JIT 编译](../by-topic/core/jit/), [C2 编译器](../by-topic/core/jit/c2-phases.md),
[性能优化](../by-topic/core/performance/)

---

## 5. 贡献者演讲主页

核心 JVMLS 演讲者的 Inside.java 主页、个人博客、OpenJDK 档案。

> 本节仅列出在 JVMLS 或其他主要会议有演讲记录的贡献者。
> 完整贡献者列表见 [贡献者索引](../by-contributor/) 和 [组织统计](../contributors/orgs/)。

### 语言设计 / 编译器 Language Design / Compilers

| 贡献者 | 组织 | 领域 | 主页 | 本地档案 |
|--------|------|------|------|----------|
| Brian Goetz | Oracle | Java 语言架构师 (Chief Architect), Valhalla, Amber | [Inside.java](https://inside.java/u/BrianGoetz/) | [Valhalla](../by-topic/core/valhalla/) |
| Dan Smith | Oracle | Valhalla 规范 Lead, value types 语义设计 | [Inside.java](https://inside.java/u/) | [Valhalla](../by-topic/core/valhalla/) |
| Gavin Bierman | Oracle | Pattern Matching JEP 作者 (JEP 305/394/440) | [Inside.java](https://inside.java/u/GavinBierman/) | [模式匹配](../by-topic/core/patterns/) |
| John Rose | Oracle | JVM 架构, invokedynamic, method handles | [Inside.java](https://inside.java/u/) | [JIT](../by-topic/core/jit/) |
| Joe Darcy | Oracle | 语言特性, Records, annotation processing | [Speaking Archive](https://github.com/jddarcy/SpeakingArchive) | [Records](../by-topic/core/records/) |
| Maurizio Cimadamore | Oracle | Panama Foreign Function API | [Inside.java](https://inside.java/u/) | [Panama](../by-topic/core/panama/) |
| Viktor Klang | Oracle | Structured Concurrency, reactive streams | [Inside.java](https://inside.java/u/) | [Loom](../by-topic/core/loom/) |

### GC (Garbage Collection)

| 贡献者 | 组织 | 领域 | 主页 | 本地档案 |
|--------|------|------|------|----------|
| Per Liden | Oracle | ZGC 创建者和技术 Lead | [OpenJDK Wiki](https://wiki.openjdk.org/spaces/zgc/pages/34668579/Main) | [ZGC](../by-topic/core/gc/zgc.md) |
| Stefan Karlsson | Oracle | ZGC co-lead, [JEP 439](../jeps/gc/jep-439.md) Owner | [OpenJDK](https://openjdk.org/jeps/439) | [ZGC](../by-topic/core/gc/zgc.md) |
| Erik Österlund | Oracle | ZGC colored pointers, barrier 设计 | [Inside.java](https://inside.java/u/ErikOsterlund/) | [ZGC](../by-topic/core/gc/zgc.md) |
| Thomas Schatzl | Oracle | G1 GC 核心开发者 | [Blog](https://tschatzl.github.io/) | [G1 GC](../by-topic/core/gc/g1-gc.md) |
| Aleksey Shipilev | **Amazon** | Shenandoah, JVM 性能 (2023 年从 Red Hat 转至 Amazon) | [shipilev.net](https://shipilev.net/) | [Shenandoah](../by-topic/core/gc/shenandoah.md) |
| Roman Kennke | **Amazon** | Shenandoah 项目 Lead, Lilliput (2022 年从 Red Hat 转至 Amazon) | [FOSDEM Profile](https://archive.fosdem.org/2024/schedule/speaker/KQYDEV/) | [Shenandoah](../by-topic/core/gc/shenandoah.md) |
| William Kemper | **Amazon** | Generational Shenandoah (JEP 521) | [GitHub](https://github.com/earthling-amzn) | [Shenandoah](../by-topic/core/gc/shenandoah.md) |

> **组织归属说明**：Aleksey Shipilev 和 Roman Kennke 早期在 Red Hat 开发 Shenandoah，
> 目前均在 Amazon (AWS)。William Kemper 一直在 Amazon。

### Loom / 并发 Concurrency

| 贡献者 | 组织 | 领域 | 主页 | 本地档案 |
|--------|------|------|------|----------|
| Ron Pressler | Oracle | Virtual Threads 架构师, Continuations 实现 | [Inside.java](https://inside.java/u/RonPressler/) | [Loom](../by-topic/core/loom/) |
| Alan Bateman | Oracle | Virtual Threads 平台集成, NIO | [Inside.java](https://inside.java/u/AlanBateman/) | [Loom](../by-topic/core/loom/) |

### JIT / 性能 / Leyden Performance

| 贡献者 | 组织 | 领域 | 主页 | 本地档案 |
|--------|------|------|------|----------|
| Ioi Lam | Oracle | AOT/CDS, Project Leyden Lead | - | [JIT](../by-topic/core/jit/) |
| Emanuel Peter | Oracle | C2 编译器, auto-vectorization, SuperWord | [Blog](https://eme64.github.io/blog/) | [JIT](../by-topic/core/jit/) |
| Paul Sandoz | Oracle | Panama, Babylon, Vector API, HAT | [Inside.java](https://inside.java/u/PaulSandoz/) | [Panama](../by-topic/core/panama/) |
| Tobias Hartmann | Oracle | C2 JIT 编译器 | - | [C2](../by-topic/core/jit/c2-phases.md) |
| Vladimir Kozlov | Oracle | JIT 编译器架构 | [OpenJDK Wiki](https://wiki.openjdk.org/display/Main/VladimirKozlov) | [JIT](../by-topic/core/jit/) |
| Claes Redestad | Oracle | 启动性能优化, 字符串处理 | - | [性能](../by-topic/core/performance/) |

### Valhalla / Panama 项目 Project Leads

| 贡献者 | 组织 | 领域 | 主页 | 本地档案 |
|--------|------|------|------|----------|
| Frederic Parain | Oracle | Valhalla JVM 实现, value class heap flattening | - | [Valhalla](../by-topic/core/valhalla/) |
| Dan Heidinga | Oracle | Project Leyden, JVM 运行时, formerly IBM J9 | - | [JIT](../by-topic/core/jit/) |
| Gary Frost | Oracle | HAT (Heterogeneous Accelerator Toolkit), GPU 加速 | - | [Performance](../by-topic/core/performance/) |

### 其他核心贡献者 Other Key Contributors

| 贡献者 | 组织 | 领域 | 主页 | 本地档案 |
|--------|------|------|------|----------|
| Mandy Chung | Oracle | 类加载, 模块系统, JLink | [Inside.java](https://inside.java/u/mchung/) | [类加载](../by-topic/core/classloading/) |
| Georges Saab | Oracle | SVP Java Platform Group, JVMLS Keynote 主持人 | - | - |
| Mark Reinhold | Oracle | Chief Architect Java Platform, JVMLS Keynote 主持人 | - | - |
| Joel Sikström | Oracle | ZGC 自动堆大小, 内存管理 | - | [ZGC](../by-topic/core/gc/zgc.md) |

### 组织分布 Organization Distribution

JVMLS 演讲者的组织分布反映了 OpenJDK 贡献的格局：

| 组织 | 代表性演讲者 | 重点领域 | 本地文档 |
|------|-------------|----------|----------|
| **Oracle** | Brian Goetz, Ron Pressler, Per Liden, Paul Sandoz, John Rose | 几乎所有 OpenJDK 项目 | [Oracle](../contributors/orgs/oracle.md) |
| **Amazon (AWS)** | Aleksey Shipilev, Roman Kennke, William Kemper | Shenandoah GC, JVM 性能, Corretto | [Amazon](../contributors/orgs/amazon.md) |
| **Red Hat** | Andrew Dinn, Andrew Haley | JVM 代码生成, AArch64 | [Red Hat](../contributors/orgs/redhat.md) |
| **SAP** | Tomas Stuefe, Goetz Lindenmaier | JVM 诊断工具, HotSpot 运行时 | [SAP](../contributors/orgs/sap.md) |

> **说明**：Oracle 在 JVMLS 演讲者中占绝大多数，因为 JVMLS 由 Oracle 主办，
> 且大部分 OpenJDK 核心项目由 Oracle 员工主导。
> Amazon/Red Hat 的贡献集中在 GC (Shenandoah) 领域。
>
> 关于贡献者组织归属的详细信息，参见 [组织统计](../contributors/orgs/)。

---

## 观看建议 Viewing Tips

### 推荐学习路径 Learning Paths

如果你是 JDK 内部实现的新手，建议按以下顺序观看：

**路径 A：GC 深入理解**

1. Aleksey Shipilev - Shenandoah: The GC That Could (Devoxx 2017)
   — 最好的 GC 入门演讲，清楚地解释了 concurrent GC 的核心挑战
2. Per Liden & Stefan Karlsson - Generational ZGC and Beyond (JVMLS 2023)
   — 理解分代 GC 的设计动机和 ZGC 的独特实现
3. Erik Österlund - Evolving ZGC's Pointer Color Palette (JVMLS 2025)
   — ZGC 下一步的技术方向
4. 阅读本地文档：[GC 演进](../by-topic/core/gc/) → [ZGC](../by-topic/core/gc/zgc.md) → [JEP 439](../jeps/gc/jep-439.md)

**路径 B：Virtual Threads 理解**

1. Ron Pressler - Continuations Under the Covers (JVMLS 2023)
   — 底层实现的最佳讲解
2. Alan Bateman - The Challenges of Introducing Virtual Threads (JVMLS 2023)
   — 平台集成的挑战
3. Ron Pressler - Loom: Where Are We? (JVMLS 2024)
   — 最新进展和未来计划
4. 阅读本地文档：[Loom](../by-topic/core/loom/) → [JEP 444](../jeps/concurrency/jep-444.md)

**路径 C：Java 语言演进**

1. Brian Goetz - Growing the Java Language (JVMLS 2025)
   — Java 语言设计的哲学
2. Brian Goetz - Valhalla: Where Are We? (JVMLS 2024)
   — Value types 的设计决策
3. Dan Smith - Value Objects in Valhalla (JVMLS 2023)
   — 规范层面的设计
4. 阅读本地文档：[Valhalla](../by-topic/core/valhalla/) → [语法演进](../by-topic/language/syntax/)

**路径 D：JIT 和性能优化**

1. John Rose - The Static Dynamic JVM (JVMLS 2025)
   — JVM 架构的高层视角
2. Emanuel Peter 的 C2 博客系列
   — C2 编译器的入门级讲解
3. Ioi Lam - Assembling Project Leyden (JVMLS 2025)
   — AOT 优化的实践
4. 阅读本地文档：[JIT](../by-topic/core/jit/) → [C2 编译器](../by-topic/core/jit/c2-phases.md)

### 观看技巧

- **速度调节**：JVMLS talk 通常很技术密集，建议 0.75x-1.0x 速度观看
- **配合阅读**：先阅读本知识库对应的本地文档 (如 [ZGC](../by-topic/core/gc/zgc.md))，
  再看 talk 效果更好
- **对比历年**：同一个项目的历年 talk 对比可以看到设计的演变过程
  (如 Valhalla 2023→2024→2025)
- **幻灯片**：部分 talk 的幻灯片发布在 [cr.openjdk.org](https://cr.openjdk.org/) 上，
  可以配合视频使用

---

## 相关本地文档

| 文档 | 说明 |
|------|------|
| [按主题浏览](../by-topic/) | 跨版本技术演进 (GC, JIT, Loom, Valhalla 等) |
| [按版本浏览](../by-version/) | JDK 版本指南 (JDK 17, 21, 23, 24, 25 等) |
| [GC 索引](../by-topic/core/gc/) | ZGC, G1, Shenandoah 的完整分析 |
| [Loom 索引](../by-topic/core/loom/) | Virtual Threads, Continuations |
| [Valhalla 索引](../by-topic/core/valhalla/) | Value Types, JEP 401 |
| [Panama 索引](../by-topic/core/panama/) | Foreign Function & Memory API |
| [JIT 索引](../by-topic/core/jit/) | C2 编译器, JIT 优化, Graal |
| [性能优化](../by-topic/core/performance/) | 性能分析和优化 |
| [JEP 分析](../jeps/) | JDK Enhancement Proposals |
| [PR 分析](../by-pr/) | 深度 Issue/PR 分析 |
| [贡献者索引](../by-contributor/) | 按贡献者浏览 |

### 其他有用的 Inside.java 技术文章

除了演讲录像，Inside.java 还发布了一些独立的深度技术文章，与 JVMLS talk 互补：

| 主题 | 链接 | 说明 | 本地文档 |
|------|------|------|----------|
| Introducing Generational ZGC | [Inside.java](https://inside.java/2023/11/28/gen-zgc-explainer/) | 配合 JVMLS 2023 ZGC talk 的详细技术说明 | [JEP 439](../jeps/gc/jep-439.md) |
| Performance Improvements in JDK 25 | [Inside.java](https://inside.java/2025/10/20/jdk-25-performance-improvements/) | JDK 25 性能改进总结 | [Performance](../by-topic/core/performance/) |
| Java Next — From Amber to Loom, from Panama to Valhalla | [Inside.java](https://inside.java/2023/04/02/java-next/) | 四大项目的综合介绍 | [Loom](../by-topic/core/loom/) |

### 外部研究资源

| 资源 | 链接 | 说明 |
|------|------|------|
| Ted Neward's JVMLS Archive | [research.tedneward.com](https://research.tedneward.com/conferences/jvmls/index.html) | 历年 JVMLS 视频链接整理 |
| Class Central JVMLS Collection | [classcentral.com](https://www.classcentral.com/subject/jvm-language-summit) | 20+ JVMLS 演讲的分类索引 |
| Tech Talks Weekly Top 100 Java Talks | [techtalksweekly.io](https://www.techtalksweekly.io/p/100-most-watched-java-conference) | 2025 年最受欢迎的 Java 演讲排名 |

---

**最后更新**: 2026-03-22

**Sources**:
- [JVMLS Official](https://openjdk.org/projects/mlvm/jvmlangsummit/)
- [Inside.java](https://inside.java/)
- [JVMLS 2025 Playlist](https://www.youtube.com/playlist?list=PLX8CzqL3ArzUOgZpIX6GsoRhPbnij-sco)
- [JVMLS 2024 Playlist](https://www.youtube.com/playlist?list=PLX8CzqL3ArzUEYnTa6KYORRbP3nhsK0L1)
- [JVMLS 2023 Playlist](https://www.youtube.com/playlist?list=PLX8CzqL3ArzW90jKUCf4H6xCKpStxsOzp)
- [Aleksey Shipilev](https://shipilev.net/)
- [Thomas Schatzl Blog](https://tschatzl.github.io/)
- [Emanuel Peter Blog](https://eme64.github.io/blog/)
- [William Kemper GitHub](https://github.com/earthling-amzn)
