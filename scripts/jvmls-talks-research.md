# JVMLS 演讲资料收集

> 收集整理中，待后续添加到贡献者页面

---

## JVMLS 简介

**JVM Language Summit** 是 OpenJDK 社区主办的年度技术峰会，通常在每年 8 月举行。会议聚焦 JVM 内部实现、语言设计、性能优化等核心话题。

### 历届会议

| 年份 | 日期 | 地点/形式 | YouTube 播放列表 |
|------|------|----------|----------------|
| 2025 | 8月4-6日 | Oracle HQ, Santa Clara | [播放列表](https://www.youtube.com/playlist?list=PLX8CzqL3ArzUOgZpIX6GsoRhPbnij-sco) |
| 2024 | 8月5-7日 | Oracle HQ, Santa Clara | [播放列表](https://www.youtube.com/playlist?list=PLX8CzqL3ArzUEYnTa6KYORRbP3nhsK0L1) |
| 2023 | 8月 | Oracle HQ, Santa Clara | [播放列表](https://www.youtube.com/playlist?list=PLX8CzqL3ArzW90jKUCf4H6xCKpStxsOzp) |
| 2019 | 7月29-31日 | Oracle HQ, Santa Clara | [播放列表](https://www.youtube.com/playlist?list=PLX8CzqL3ArzXFRVYmbvZfZQ0CQMfIIFCH) |
| 2018 | 8月 | Oracle HQ, Santa Clara | - |
| 2017 | 8月 | Oracle HQ, Santa Clara | - |
| 2016 | 8月 | Oracle HQ, Santa Clara | - |
| 2015 | 8月 | Oracle HQ, Santa Clara | - |
| 2014 | 8月 | Oracle HQ, Santa Clara | - |
| 2013 | 8月 | Oracle HQ, Santa Clara | - |
| 2012 | 8月 | Oracle HQ, Santa Clara | - |

---

## JVMLS 2024 演讲 (8月5-7日)

> 官方页面: [OpenJDK JVMLS 2024](https://openjdk.org/projects/mlvm/summit2024/)
> 议程: [Agenda](https://openjdk.org/projects/mlvm/summit2024/agenda.html)

### Keynote
- **Java in 2024** - [视频](https://www.youtube.com/watch?v=NV4v7KXKQ-c)

### 已知演讲
| 演讲者 | 主题 | 链接 |
|--------|------|------|
| Georges Saab, Mark Reinhold | Keynote | [视频](https://www.youtube.com/watch?v=NV4v7KXKQ-c) |
| Brian Goetz | Project Valhalla | [报道](https://realjenius.com/2024/12/15/valhalla-simplicity/) |
| Per Liden | Generational ZGC | 待确认 |
| Thomas Schatzl | G1 GC Improvements | 待确认 |

---

## JVMLS 2023 演讲

> 官方播放列表: [YouTube](https://www.youtube.com/playlist?list=PLX8CzqL3ArzW90jKUCf4H6xCKpStxsOzp)

### Keynote
- **JVM Language Summit 2023 Keynote** - [视频](https://www.youtube.com/watch?v=Ma0NtbG0mHY)
  - Georges Saab (Senior VP, Java Platform Group, Oracle)
  - Mark Reinhold (Chief Architect, Java Platform Group, Oracle)

---

## JVMLS 2019 演讲

> 官方播放列表: [YouTube](https://www.youtube.com/playlist?list=PLX8CzqL3ArzXFRVYmbvZfZQ0CQMfIIFCH)
> 官方页面: [OpenJDK](https://openjdk.org/projects/mlvm/summit2019/)

---

## 按贡献者整理的演讲

### Aleksey Shipilev (性能优化/Shenandoah)

> **博客**: [shipilev.net](https://shipilev.net/)
> **GitHub**: [@shipilev](https://github.com/shipilev)

#### JVMLS 演讲
| 年份 | 主题 | 资料 |
|------|------|------|
| 2013 | False Sharing, and @Contended | 幻灯片 |
| 2013 | Java Concurrency Stress Tests (lightning talk) | 幻灯片 |

#### 其他重要演讲
| 会议 | 年份 | 主题 | 资料 |
|------|------|------|------|
| JUG Berlin-Brandenburg | 2019 | Shenandoah GC | [幻灯片](https://shipilev.net/talks/jugbb-Sep2019-shenandoah.pdf) |
| JavaZone | 2018 | Shenandoah GC Part I | [幻灯片](https://shipilev.net/talks/javazone-Sep2018-shenandoah.pdf) |
| Devoxx | 2017 | Shenandoah GC | [幻灯片](https://shipilev.net/talks/devoxx-Nov2017-shenandoah.pdf) |
| Joker | 2017 | Shenandoah GC | [幻灯片](https://shipilev.net/talks/joker-Nov2017-shenandoah-II.pdf) |
| - | - | Shenandoah: The Garbage Collector That Could | [视频](https://www.youtube.com/watch?v=VCeHkcwfF9Q) |

**主要主题:**
- Shenandoah GC (低延迟垃圾回收)
- Java Object Layout (JOL)
- Java Concurrency Stress Tests (JCStress)
- Performance Benchmarking
- @Contended (False Sharing 优化)

---

### Brian Goetz (语言设计/Project Valhalla)

> **身份**: Java Language Architect, Oracle
> **Inside.Java**: [@BrianGoetz](https://inside.java/u/BrianGoetz/)

#### JVMLS 演讲
| 年份 | 主题 | 资料 |
|------|------|------|
| 2024 | Project Valhalla: The Epic Refactor to Elegance | [报道](https://realjenius.com/2024/12/15/valhalla-simplicity/) |
| 2023 | Pattern Matching | 待确认 |

#### Project Valhalla 资源
| 资源 | 链接 |
|------|------|
| State of Valhalla (官方) | [文档](https://cr.openjdk.org/~briangoetz/valhalla/sov/01-background.html) |
| The State of Valhalla (采访) | [nipafx.dev](https://nipafx.dev/brian-goetz-valhalla-26h/) |
| Project Valhalla Update | [视频](https://www.youtube.com/watch?v=EzXZLPqQmmQ) |

#### Pattern Matching 资源
| 资源 | 链接 |
|------|------|
| State of Pattern Matching | [视频](https://www.youtube.com/watch?v=a8OdwUiSnXw) |
| Pattern Matching for Java | [视频](https://www.youtube.com/watch?v=n3_8YcYKScw) |
| Pattern Matching Introduction (InfoQ) | [文章](https://www.infoq.com/news/2017/09/pattern-matching-for-java/) |

**主要主题:**
- Project Valhalla (Value Objects, Flattened Data Types)
- Pattern Matching (模式匹配)
- Project Amber (语言特性简化)
- Lambda Expressions (JSR-335)
- Collections API

---

### Per Liden (ZGC)

> **身份**: ZGC Lead, Oracle

#### JVMLS 演讲
| 年份 | 主题 | 资料 |
|------|------|------|
| 2024 | Generational ZGC Status | 待确认 |
| 2023 | ZGC Evolution | 待确认 |
| 2019 | ZGC Deep Dive | 待确认 |

#### ZGC 资源
| 资源 | 链接 |
|------|------|
| ZGC Wiki (OpenJDK) | [文档](https://wiki.openjdk.org/spaces/zgc/pages/34668579/Main) |
| JEP 439: Generational ZGC | [JEP](https://openjdk.org/jeps/439) |

**主要主题:**
- Z Garbage Collector (ZGC)
- Generational ZGC (JEP 439)
- Low Latency GC

---

### Thomas Schatzl (G1 GC)

> **博客**: [tschatzl.github.io](https://tschatzl.github.io/)
> **GitHub**: [@tschatzl](https://github.com/tschatzl)

#### JVMLS 演讲
| 年份 | 主题 | 资料 |
|------|------|------|
| 2024 | G1 Throughput Improvements | 待确认 |

#### 其他演讲
| 会议 | 年份 | 主题 | 资料 |
|------|------|------|------|
| FOSDEM | 2018 | G1 - Not^H^H^HNever Done! | [页面](https://archive.fosdem.org/2018/schedule/event/g1/) |
| - | 2021 | JDK 17 G1/Parallel GC changes | [博客](https://tschatzl.github.io/2021/09/16/jdk17-g1-parallel-gc-changes.html) |

**主要主题:**
- G1 Garbage Collector
- GC Performance Improvements
- JDK 17 GC Changes

---

### Emanuel Peter (C2 编译器/SuperWord)

> **博客**: [eme64.github.io/blog](https://eme64.github.io/blog/)
> **GitHub**: [@eme64](https://github.com/eme64)

#### JVMLS 演讲
| 年份 | 主题 | 资料 |
|------|------|------|
| 2025 | C2 SuperWord NormalMapping Demo | JVMLS 2025 (待确认) |

#### C2 编译器博客系列
| 部分 | 标题 | 链接 |
|------|------|------|
| Part 1 | Introduction to HotSpot JVM C2 JIT Compiler | [文章](https://eme64.github.io/blog/2024/12/24/Intro-to-C2-Part01.html) |
| Part 2 | Introduction to C2 Part 2 | [文章](https://eme64.github.io/blog/) |
| Part 3 | Introduction to C2 Part 3 | [文章](https://eme64.github.io/blog/2025/01/23/Intro-to-C2-Part03.html) |

**主要主题:**
- C2 JIT Compiler (服务端编译器)
- SuperWord (自动向量化优化)
- Vector API
- SIMD Optimization

---

### David Holmes (并发/Threading)

> **身份**: Consulting Member of Technical Staff, Oracle

#### JVMLS 演讲
| 年份 | 主题 | 资料 |
|------|------|------|
| - | Signal Handling | 待收集 |
| - | Project Loom | 待收集 |

**主要主题:**
- Virtual Threads (Project Loom)
- Thread Scheduling
- Signal Handling

---

### Claes Redestad (性能优化)

> **GitHub**: [@cl4es](https://github.com/cl4es)

#### JVMLS 演讲
| 年份 | 主题 | 资料 |
|------|------|------|
| - | - | 待收集 |

**主要主题:**
- String Compaction
- Startup Performance
- Memory Footprint Optimization

---

### Stuart Marks (核心库)

> **GitHub**: [@stuart-marks](https://github.com/stuart-marks)

#### JVMLS 演讲
| 年份 | 主题 | 资料 |
|------|------|------|
| - | Collections API | 待收集 |

**主要主题:**
- Collections Framework
- Stream API
- API Design

---

## 其他重要会议

### FOSDEM (Brussels)

| 年份 | 演讲者 | 主题 |
|------|--------|------|
| 2024 | Per Liden | ZGC |
| 2018 | Thomas Schatzl | G1 - Not^H^H^HNever Done! |

### Devoxx

| 年份 | 演讲者 | 主题 |
|------|--------|------|
| 2017 | Aleksey Shipilev | Shenandoah GC |
| - | Brian Goetz | Pattern Matching |

### JavaOne / Oracle Code One

| 年份 | 演讲者 | 主题 |
|------|--------|------|
| ... | ... | ... |

---

## 信息来源

### 官方渠道

| 来源 | URL | 说明 |
|------|-----|------|
| OpenJDK Wiki | https://wiki.openjdk.org | JVMLS 信息 |
| OpenJDK YouTube | https://www.youtube.com/@OpenJDK | 演讲视频 |
| JVMLS 2024 | https://openjdk.org/projects/mlvm/summit2024/ | 2024 官方页面 |
| JVMLS 2025 | https://openjdk.org/projects/mlvm/jvmlangsummit/ | 2025 官方页面 |
| Inside.Java | https://inside.java | Java 官方博客 |

### 个人博客

| 贡献者 | 博客 | 说明 |
|--------|------|------|
| Aleksey Shipilev | https://shipilev.net/ | 演讲幻灯片、性能优化 |
| Emanuel Peter | https://eme64.github.io/blog/ | C2 编译器技术 |
| Thomas Schatzl | https://tschatzl.github.io/ | G1 GC |

---

## 收集方法

1. **YouTube**: 搜索 "JVMLS [year] OpenJDK"
2. **OpenJDK Wiki**: 查找 jvmls 页面
3. **个人博客**: 贡献者博客通常有演讲幻灯片
4. **Inside.Java**: 官方博客和新闻报道

---

## 后续行动

- [x] 收集 JVMLS 2024 播放列表
- [x] 收集 JVMLS 2023 播放列表
- [x] 收集 JVMLS 2019 播放列表
- [ ] 收集 JVMLS 2021/2022 播放列表
- [ ] 收集 JVMLS 2018 及之前年份的资料
- [ ] 整理每位贡献者的演讲历史
- [ ] 添加到贡献者页面的 "Talks & Presentations" 部分
- [ ] 创建正式的 JVMLS 文档页面

---

**最后更新**: 2026-03-20

**Sources**:
- [JVMLS 2024 - OpenJDK](https://openjdk.org/projects/mlvm/summit2024/)
- [JVMLS 2024 - YouTube Playlist](https://www.youtube.com/playlist?list=PLX8CzqL3ArzUEYnTa6KYORRbP3nhsK0L1)
- [JVMLS 2023 - YouTube Playlist](https://www.youtube.com/playlist?list=PLX8CzqL3ArzW90jKUCf4H6xCKpStxsOzp)
- [JVMLS 2019 - YouTube Playlist](https://www.youtube.com/playlist?list=PLX8CzqL3ArzXFRVYmbvZfZQ0CQMfIIFCH)
- [JVMLS 2025 - OpenJDK](https://openjdk.org/projects/mlvm/jvmlangsummit/)
- [Aleksey Shipilev - Shenandoah Presentation](https://www.youtube.com/watch?v=VCeHkcwfF9Q)
- [Brian Goetz - Valhalla State](https://nipafx.dev/brian-goetz-valhalla-26h/)
- [Emanuel Peter - C2 Blog](https://eme64.github.io/blog/)
