# 日期时间 API 贡献者

> java.time API 的主要贡献者

---
## 目录

1. [核心贡献者](#1-核心贡献者)
2. [性能优化贡献者 (JDK 22-24)](#2-性能优化贡献者-jdk-22-24)
3. [其他贡献者](#3-其他贡献者)
4. [按公司分类](#4-按公司分类)
5. [贡献统计](#5-贡献统计)
6. [相关资源](#6-相关资源)
7. [联系方式](#7-联系方式)
8. [相关文档](#8-相关文档)

---


## 1. 核心贡献者

### Stephen Colebourne

**角色**: JSR 310 规范负责人

**主要贡献**:
- Joda-Time 创始人
- JSR 310 规范负责人
- ThreeTen-Extra 维护者
- java.time 设计主导

**背景**:

> I created Joda-Time in 2002 as a replacement for the poorly designed `Date` and `Calendar` classes.
>
> The experience from Joda-Time directly influenced the design of JSR 310.

**博客**: [blog.joda.org](https://blog.joda.org/)

**关键文章**:
- ["What about JSR-310?"](https://blog.joda.org/2010/12/what-about-jsr-310_153.html) - 讨论是否放弃 JSR 310
- ["JSR-310 and Java 7 language changes"](https://blog.joda.org/2007/09/jsr-310-and-java-7-language-changes.html) - 设计困难

**LinkedIn**: [Stephen Colebourne](https://www.linkedin.com/in/stephencolebourne/)

---

### Michael Nascimento Santos

**角色**: JSR 310 实现专家

**主要贡献**:
- java.time 核心实现
- ThreeTen Backport 维护者

**背景**:
- 巴西软件工程师
- Java Champion
- JSR 310 早期参与者

---

### Roger Riggs

**角色**: Oracle 工程师

**主要贡献**:
- java.time Oracle 实现
- 测试覆盖

**公司**: Oracle

---

## 2. 性能优化贡献者 (JDK 22-24)

### Shaojin Wen (@wenshao)

**角色**: 阿里云数据库技术团队

**主要贡献** (JDK 22-24):
- JDK-8366224: DecimalDigits.appendPair 优化 (+12% 性能)
- JDK-8365186: DateTimePrintContext.adjust 方法拆分 (+3-12% 性能)
- JDK-8368172: DateTimePrintContext 不可变优化
- JDK-8368825: DateTimeFormatterBuilder switch 优化
- JDK-8337168: LocalDateTime.toString 优化
- JDK-8337832: datetime toString 优化
- JDK-8337279: Share StringBuilder to format instant
- JDK-8336706: LocalDate.toString 优化
- JDK-8336741: LocalTime.toString 优化
- JDK-8336792: DateTimeFormatterBuilder 补零优化
- JDK-8337167: StringSize 去重化
- JDK-8317742: ISO 日期格式一致性修复
- JDK-8355177: StringBuilder::append(char[]) 优化

**GitHub**: [@wenshao](https://github.com/wenshao)

**公司**: Alibaba (阿里云数据库团队 / PolarDB)

---

## 3. 其他贡献者

### 实现团队

| 贡献者 | 角色 | 说明 |
|--------|------|------|
| **Stephen Flores** | 测试 | 测试覆盖 |
| **Brian Goetz** | Review | 平台集成审查 |
| **Mark Reinhold** | Review | JDK 集成审查 |

### 社区贡献者

| 贡献者 | 贡献 |
|--------|------|
| **Joda-Time 社区** | 反馈和测试 |
| **ThreeTen-Extra 社区** | 扩展功能 |

---

## 4. 按公司分类

### Oracle

| 贡献者 | 角色 |
|--------|------|
| Roger Riggs | 实现 |
| Brian Goetz | 审查 |
| Mark Reinhold | 审查 |

### Alibaba / 阿里云

| 贡献者 | 角色 |
|--------|------|
| Shaojin Wen | 性能优化 (JDK 22-24) |

### 独立/社区

| 贡献者 | 角色 |
|--------|------|
| Stephen Colebourne | 规范负责人 |
| Michael Nascimento Santos | 实现 |

---

## 5. 贡献统计

### JSR 310 提交 (OpenJDK)

```bash
# 查看提交统计
git log --all --since="2010-01-01" --until="2014-12-31" \
    -- src/java.base/share/classes/java/time/ \
    --format="%an" | sort | uniq -c | sort -rn
```

**估计** (JSR 310 时期):
- Stephen Colebourne: ~40%
- Michael Nascimento Santos: ~30%
- Roger Riggs: ~15%
- 其他: ~15%

### 性能优化 (JDK 22-24)

```bash
# 查看性能优化相关提交
git log --all --since="2023-01-01" --until="2025-12-31" \
    -- src/java.base/share/classes/java/time/ \
    -- src/java.base/share/classes/jdk/internal/util/DateTimeHelper.java \
    -- src/java.base/share/classes/jdk/internal/util/DecimalDigits.java \
    --format="%an" | sort | uniq -c | sort -rn
```

**主要贡献者**:
- Shaojin Wen: ~70% (性能优化 PR)

---

## 6. 相关资源

### 官方资源
- [JSR 310 Expert Group](https://jcp.org/en/jsr/detail?id=310)
- [OpenJDK java.time](https://github.com/openjdk/jdk/tree/master/src/java.base/share/classes/java/time)

### 社区资源
- [Joda-Time](https://www.joda.org/joda-time/)
- [ThreeTen-Extra](https://www.threeten.org/threeten-extra/)
- [Stephen Colebourne's Blog](https://blog.joda.org/)

---

## 7. 联系方式

| 贡献者 | Twitter | GitHub | Blog |
|--------|---------|--------|------|
| Stephen Colebourne | @jodastephen | jodastephen | blog.joda.org |
| Shaojin Wen | - | @wenshao | - |

---

## 8. 相关文档

- [完整时间线](timeline.md)
- [基础 API](basics.md)
- [JSR 310 PR 分析](jsr310/pr-analysis.md)
- [主索引](README.md)
- [性能优化 PR](prs/)

---

> **更新时间**: 2026-03-20
