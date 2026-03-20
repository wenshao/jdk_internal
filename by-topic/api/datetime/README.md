# 日期时间 API 文档索引

> 本目录包含 Java 日期时间 API 从 JDK 1.0 到 JDK 26 的完整演进文档

---

## 文档结构

```
by-topic/datetime/
├── index.md              # 主索引 (包含源码结构、VM 参数、设计决策)
├── timeline.md           # 完整时间线 (包含 Git 提交历史)
├── basics.md             # 基础 API 指南
├── contributors.md       # 贡献者列表
├── prs/                  # PR 分析文档
│   ├── jdk-8317742.md   # ISO 日期格式修复
│   ├── jdk-8336706.md   # LocalDate.toString 优化
│   ├── jdk-8336741.md   # LocalTime.toString 优化
│   ├── jdk-8336792.md   # DateTimeFormatterBuilder 优化
│   ├── jdk-8337167.md   # StringSize 去重化
│   ├── jdk-8337168.md   # LocalDateTime.toString 优化
│   ├── jdk-8337279.md   # StringBuilder 复用
│   ├── jdk-8337832.md   # datetime toString 优化
│   ├── jdk-8334742.md   # 字段类型优化
│   ├── jdk-8345668.md   # ZoneOffset 性能回归修复
│   ├── jdk-8348880.md   # ZoneOffset 缓存优化
│   ├── jdk-8365186.md   # DateTimePrintContext 拆分
│   ├── jdk-8366224.md   # DecimalDigits.appendPair
│   ├── jdk-8368172.md   # DateTimePrintContext 不可变
│   └── jdk-8368825.md   # Switch 表达式优化
├── jsr310/               # JSR 310 相关
│   └── pr-analysis.md   # JSR 310 PR 分析
├── localdate/            # LocalDate 专题
├── localtime/            # LocalTime 专题
├── localdatetime/        # LocalDateTime 专题
├── instant/              # Instant 专题
├── zoneddatetime/        # ZonedDateTime 专题
├── offsetdatetime/       # OffsetDateTime 专题
├── duration/             # Duration 专题
├── period/               # Period 专题
├── formatter/            # DateTimeFormatter 专题
├── zone/                 # 时区相关
│   ├── zoneid.md
│   ├── zoneoffset.md
│   └── zonerules.md
└── issues/               # Bug 分析
    └── jdk-8046707.md
```

---

## 核心内容

### 源码位置

| 功能 | 源码路径 | 实现分析 |
|------|----------|----------|
| LocalDate | `java.base/java/time/LocalDate.java` | [详情](localdate/index.md) |
| LocalTime | `java.base/java/time/LocalTime.java` | [详情](localtime/index.md) |
| LocalDateTime | `java.base/java/time/LocalDateTime.java` | [详情](localdatetime/index.md) |
| Instant | `java.base/java/time/Instant.java` | [详情](instant/index.md) |
| ZonedDateTime | `java.base/java/time/ZonedDateTime.java` | [详情](zoneddatetime/index.md) |
| OffsetDateTime | `java.base/java/time/OffsetDateTime.java` | [详情](offsetdatetime/index.md) |
| ZoneId | `java.base/java/time/ZoneId.java` | [详情](zone/zoneid.md) |
| ZoneOffset | `java.base/java/time/ZoneOffset.java` | [详情](zone/zoneoffset.md) |
| ZoneRules | `java.base/java/time/zone/ZoneRules.java` | [详情](zone/zonerules.md) |
| Duration | `java.base/java/time/Duration.java` | [详情](duration/index.md) |
| Period | `java.base/java/time/Period.java` | [详情](period/index.md) |
| DateTimeFormatter | `java.base/java/time/format/DateTimeFormatter.java` | [详情](formatter/index.md) |

### 内部工具类

| 类 | 路径 | 说明 |
|----|------|------|
| DateTimeHelper | `jdk/internal/util/DateTimeHelper.java` | 日期时间格式化内部工具 (JDK 23+) |
| DecimalDigits | `jdk/internal/util/DecimalDigits.java` | 数字格式化工具 (查找表优化) |

---

## VM 诊断参数

### JIT 编译诊断

```bash
# 监控 C2 内联决策
-XX:+PrintInlining

# 查看编译任务
-XX:+PrintCompilation

# 方法内联阈值（影响 DateTimePrintContext）
-XX:MaxFreqInlineSize=325             # 热方法内联阈值
-XX:MaxInlineSize=35                  # 常规方法内联阈值

# 逃逸分析（影响 StringBuilder 优化）
-XX:+DoEscapeAnalysis                 # 启用逃逸分析
-XX:+EliminateAllocations             # 消除分配
-XX:+PrintEliminateAllocations        # 打印分配消除信息
```

---

## 性能优化时间线

| 版本 | 优化 | 性能提升 |
|------|------|----------|
| JDK 22 | ISO 日期格式修复 (JDK-8317742) | Bug 修复 |
| JDK 23 | LocalDate.toString 优化 (JDK-8336706) | +10% |
| JDK 23 | LocalTime.toString 优化 (JDK-8336741) | +8% |
| JDK 23 | DateTimeFormatterBuilder 优化 (JDK-8336792) | +5% |
| JDK 23 | StringSize 去重化 (JDK-8337167) | 代码清理 |
| JDK 23 | LocalDateTime.toString 优化 (JDK-8337168) | +8% |
| JDK 23 | StringBuilder 复用 (JDK-8337279) | 减少分配 |
| JDK 23 | datetime toString 优化 (JDK-8337832) | +5-12% |
| JDK 24 | DateTimePrintContext 拆分 (JDK-8365186) | +3-12% |
| JDK 24 | DecimalDigits.appendPair (JDK-8366224) | +12% |
| JDK 24 | DateTimePrintContext 不可变 (JDK-8368172) | 分配优化 |
| JDK 24 | Switch 表达式优化 (JDK-8368825) | 代码简化 |

---

## 贡献者

### 核心贡献者

| 贡献者 | 主要贡献 |
|--------|----------|
| **Stephen Colebourne** | JSR 310 规范负责人, Joda-Time 作者 |
| **Michael Nascimento** | JSR 310 实现 |
| **Roger Riggs** | java.time Oracle 实现 |

### 性能优化贡献者 (JDK 22-24)

| 贡献者 | 主要贡献 |
|--------|----------|
| **Shaojin Wen (@wenshao)** | 12+ 性能优化 PR，累计 +50%+ 性能提升 |

---

## 相关资源

### 官方资源
- [JSR 310: Date and Time API](https://jcp.org/en/jsr/detail?id=310)
- [OpenJDK java.time](https://github.com/openjdk/jdk/tree/master/src/java.base/share/classes/java/time)

### 社区资源
- [Joda-Time](https://www.joda.org/joda-time/)
- [ThreeTen-Extra](https://www.threeten.org/threeten-extra/)
- [Stephen Colebourne's Blog](https://blog.joda.org/)

---

> **最后更新**: 2026-03-20
> **文档版本**: 2.0
