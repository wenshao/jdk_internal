# Aggelos Biboudis

> Java 语言特性设计者，JEP 530 (Primitive Types in Patterns) 实现者，javac 编译器工程师

---

## 1. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Aggelos Biboudis (Angelos Bimpoudis) |
| **当前组织** | [Oracle](../../contributors/orgs/oracle.md) |
| **职位** | Principal Member of Technical Staff, Java Platform Group - 语言和工具 |
| **位置** | 苏黎世, 瑞士 |
| **学历** | PhD, University of Athens (导师: Yannis Smaragdakis) |
| **个人主页** | [biboudis.github.io](http://biboudis.github.io/) |
| **GitHub** | [@biboudis](https://github.com/biboudis) |
| **OpenJDK** | [@biboudis](https://openjdk.org/census#biboudis) |
| **角色** | JDK Reviewer, Committer |
| **主要领域** | Java 语言特性, 模式匹配, javac 编译器, JEP 实现 |
| **PRs (integrated)** | 64 |
| **活跃时间** | 2024 - 至今 |

> **数据来源**: [GitHub](https://github.com/biboudis), [OpenJDK Census](https://openjdk.org/census#biboudis)

---

## 2. 技术影响力

### 影响的主要目录

| 目录 | 说明 |
|------|------|
| `src/jdk.compiler/share/classes/com/sun/tools/javac/` | javac 编译器源码 |
| `src/java.base/share/classes/java/lang/runtime/` | SwitchBootstraps 运行时支持 |
| `test/langtools/tools/javac/` | javac 编译器测试 |

### 贡献时间线

```
2024:      ████████████████████████████ (约25) JEP 488, 模式匹配, Lambda, 泛型修复
2025:      ██████████████████████████████████ (约35) JEP 530, instanceof 翻译, 类型签名修复
2026:      ████ (约4) javadoc, ExactConversionsSupport (截至3月)
```

---

## 3. 技术特长

`模式匹配` `原始类型模式` `instanceof` `switch 表达式` `javac` `类型系统` `SwitchBootstraps` `Lambda` `泛型` `JEP 实现`

---

## 4. 代表性工作

### 1. JEP 530: Primitive Types in Patterns (第四预览)
**PR**: [#27637](https://github.com/openjdk/jdk/pull/27637) | **Bug**: JDK-8359145

实现 JEP 530，将原始类型扩展到模式匹配、instanceof 和 switch 中，使 Java 的模式匹配支持 int、long 等原始类型的精确转换检查。

### 2. JEP 488: Primitive Types in Patterns (第二预览)
**PR**: [#21539](https://github.com/openjdk/jdk/pull/21539) | **Bug**: JDK-8341408

实现 JEP 488，原始类型模式匹配的第二次预览迭代，奠定了语言特性的基础框架。

### 3. SwitchBootstraps 安全防护
**PR**: [#25090](https://github.com/openjdk/jdk/pull/25090) | **Bug**: JDK-8354323

为 SwitchBootstraps.typeSwitch 添加安全防护，确保在编译器外部错误使用时能给出有意义的错误信息。

### 4. 泛型模式匹配类型修复
**PR**: [#21606](https://github.com/openjdk/jdk/pull/21606) | **Bug**: JDK-8340145

修复泛型模式匹配中的内部编译器错误，解决泛型类内部类在模式匹配中的类型推断问题。

---

## 5. 职业时间线

| 年份 | 事件 | 详情 |
|------|------|------|
| **~2017** | PhD 毕业 | University of Athens, 导师 Yannis Smaragdakis, 论文主题: "Expressive and efficient streaming libraries" |
| **2017-2019** | 博士后研究员 @ EPFL | Scala 3 编译器团队 (LAMP 实验室), 导师 Martin Odersky |
| **~2019** | 软件工程师 @ Swisscom AG | 瑞士电信公司 |
| **~2020+** | 加入 Oracle | Java Platform Group, 苏黎世, 专注 Java 语言演进和 javac 编译器 |

---

## 6. 学术成就与发表

### 代表性论文

| 会议 | 论文 |
|------|------|
| **POPL 2017** | "Stream Fusion, to Completeness" (与 Oleg Kiselyov, Nick Palladinos, Yannis Smaragdakis 合著) |
| **ECOOP 2015** | "Streams à la carte: Extensible Pipelines with Object Algebras" |
| **GPCE 2016** | "Recaf: Java Dialects as Libraries" |
| **2018** | "Functional Stream Libraries and Fusion: What's Next" (与 Oleg Kiselyov, Martin Odersky 合著) |

### 学术服务

- 曾任 ICFP、SPLASH、OOPSLA 等顶级会议程序委员会成员
- 共同组织 Shonan Meeting (函数式流处理库)
- 在 EPFL 和 University of Athens 教授软件工程、编程和编译器课程

---

## 7. 技术深度

Aggelos Biboudis 是 Oracle Java Platform Group 的核心成员，专注于 Java 语言新特性的设计和 javac 编译器实现。他的学术背景 (流处理融合、多阶段编程、类型系统) 为其语言设计工作提供了扎实的理论基础。

**关键技术领域**:
- 模式匹配：原始类型模式、instanceof 扩展、switch 表达式集成
- javac 编译器：类型检查、代码生成、Lambda 翻译、签名生成
- JEP 实现：从规范到编译器到运行时的完整特性交付
- 类型系统：泛型、内部类、类型注解、精确转换
- 流处理融合：PhD 研究成果，multi-stage programming 优化技术

---

## 8. 协作网络

| 审查者 | 领域 |
|--------|------|
| Jan Lahoda | javac 编译器 |
| Vicente Romero | javac 编译器 |
| Maurizio Cimadamore | 类型系统, 语言特性 |

---

## 9. 历史贡献

| JDK 版本 | 主要贡献 |
|----------|----------|
| JDK 24 | JEP 488 (模式匹配第二预览), Lambda 修复, 密封类 |
| JDK 25 | JEP 530 (模式匹配第四预览), instanceof 翻译, 类型签名 |
| JDK 26 | ExactConversionsSupport javadoc 修复 |

**长期影响**: 模式匹配的原始类型扩展是 Java 类型系统现代化的关键步骤；修复泛型与模式匹配交互中的多个编译器错误；通过多轮预览迭代持续完善语言特性设计。

---

## 10. 外部资源

| 类型 | 链接 |
|------|------|
| **GitHub** | [@biboudis](https://github.com/biboudis) |
| **个人主页** | [biboudis.github.io](http://biboudis.github.io/) |
| **Google Scholar** | [Aggelos Biboudis](https://scholar.google.com/citations?user=hIq9bFUAAAAJ&hl=en) |
| **DBLP** | [Aggelos Biboudis](https://dblp.uni-trier.de/pid/136/1016.html) |
| **LinkedIn** | [biboudis](https://www.linkedin.com/in/biboudis/) |
| **OpenJDK Census** | [biboudis](https://openjdk.org/census#biboudis) |
| **公司** | [Oracle](https://www.oracle.com/) |
| **Commits** | [openjdk/jdk commits](https://github.com/openjdk/jdk/commits?author=biboudis) |
| **PRs** | [openjdk/jdk PRs](https://github.com/openjdk/jdk/pulls?q=author%3Abiboudis+is%3Amerged) |

---

> **文档版本**: 1.0 | **最后更新**: 2026-03-22
> 基于 GitHub API 数据: 64 integrated PRs. JEP 530 (Primitive Types in Patterns) 为最具影响力的工作.

## 角色晋升 (CFV)

| 日期 | 角色 | 提名者 | 投票数 | 链接 |
|------|------|--------|--------|------|
| 2023-10-23 | Committer | Jan Lahoda | 20 | [CFV](https://mail.openjdk.org/pipermail/jdk-dev/2023-October/008397.html) |
| 2024-05-17 | Reviewer | Jan Lahoda | 17 | [CFV](https://mail.openjdk.org/pipermail/jdk-dev/2024-May/008993.html) |


## 审查统计

| 指标 | 值 |
|------|-----|
| **总审查次数** | 55 |
| **活跃仓库数** | 2 |
