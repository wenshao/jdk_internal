# Naoto Sato

> **GitHub**: [@naotoj](https://github.com/naotoj)
> **Inside.java**: [NaotoSato](https://inside.java/u/NaotoSato/)
> **Organization**: Oracle (Java Platform Group)
> **Location**: San Jose, California

---

## 概述

Naoto Sato 是 Oracle Java Platform Group 的**首席技术工程师 (Principal Member of Technical Staff)**，专注于 JDK 核心库的**国际化 (i18n)** 和**本地化** 功能。他是 Java UTF-8 标准化的重要推动者，作为 **6 个 JEP 的负责人**，彻底改变了 Java 的字符编码和本地化处理方式。

**教育背景**: 东京工业大学精密机械系统工程硕士 (M. Engineering)

**主要成就**:
- JEP 127/128: JDK 8 国际化基础架构
- JEP 226/252: JDK 9 CLDR 集成
- JEP 400: JDK 18 UTF-8 默认编码
- JEP draft 8344154: JSON 便捷方法 (当前进行中)

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Naoto Sato |
| **当前组织** | Oracle America, Inc. |
| **团队** | Java Platform Group |
| **职位** | Engineer / Principal Member of Technical Staff |
| **GitHub** | [@naotoj](https://github.com/naotoj) |
| **Twitter** | [@naotoj](https://twitter.com/naotoj) |
| **Bluesky** | [@naotoj.bsky.social](https://bsky.app/profile/naotoj.bsky.social) |
| **OpenJDK** | [@naoto](https://openjdk.org/census#naoto) |
| **角色** | OpenJDK Member, JDK Reviewer, i18n Lead |
| **邮件** | naoto@openjdk.org, naoto.sato@oracle.com |
| **专长** | Unicode, Internationalization, Charset, Console, TimeZone |

---

## 职业经历

### Sun Microsystems (2000-2010)

- **职位**: Software Engineer
- **部门**: Java & Developer Platforms Group
- **工作**: Java 国际化 (i18n) 库开发
- **地点**: 加利福尼亚州

### Oracle (2010-至今)

- **职位**: Principal Member of Technical Staff
- **部门**: Java Platform Group
- **专注**: JDK 核心库，国际化与本地化
- **地点**: 加利福尼亚州圣何塞 / 德克萨斯州奥斯汀

### IBM Japan

- **职位**: Globalization Team
- **工作**: Java 国际化与本地化

### 教育背景

- **学位**: Master of Science (M.S.) in Precision Machinery Systems
- **学校**: 东京工业大学 (Tokyo Institute of Technology), 日本
- **说明**: 从精密机械工程转向软件国际化领域

---

## 主要 JEP 贡献

### JEP draft 8344154: Convenience Methods for JSON Documents (进行中)

| 属性 | 值 |
|------|-----|
| **角色** | Author, Owner |
| **合作者** | Paul Sandoz, Justin Lu, Stuart Marks |
| **状态** | Draft → Submitted |
| **说明** | 为 Java 提供 JSON 文档读写便捷方法，无需外部库 |

**影响**: 终结 Java 对 JSON 库的依赖，提供内置 JSON 支持。

```java
// 计划中的 API
String json = """
    {
        "name": "Alice",
        "age": 30
    }
    """;
JSON.parse(json); // 无需外部库
```

### JEP 400: UTF-8 by Default (JDK 18)

| 属性 | 值 |
|------|-----|
| **角色** | Author, Owner |
| **合作者** | Alan Bateman |
| **状态** | Closed / Delivered |
| **发布版本** | JDK 18 |

**影响**: 使 UTF-8 成为所有平台的默认字符集，解决了 Java 多年来的跨平台编码不一致问题。

```java
// JDK 18 之前 - 平台依赖的默认编码
FileReader reader = new FileReader("test.txt");
// Windows: 使用 Cp1252
// macOS: 使用 UTF-8

// JDK 18+ - 统一使用 UTF-8
FileReader reader = new FileReader("test.txt");
// 所有平台: UTF-8
```

### JEP 252: Use CLDR Locale Data by Default (JDK 9)

| 属性 | 值 |
|------|-----|
| **角色** | Author, Owner |
| **合作者** | Alex Buckley |
| **状态** | Closed / Delivered |
| **发布版本** | JDK 9 |

**影响**: 使用 Unicode CLDR 作为默认本地化数据源，提供更准确的本地化支持。

### JEP 226: UTF-8 Property Resource Bundles (JDK 9)

| 属性 | 值 |
|------|-----|
| **角色** | Owner |
| **状态** | Closed / Delivered |
| **发布版本** | JDK 9 |

**影响**: 允许 ResourceBundle 使用 UTF-8 编码的属性文件，简化国际化资源管理。

```properties
# 之前需要 native2ascii 转换
message=\u4f60\u597d\u4e16\u754c

# 现在可以直接使用 UTF-8
message=你好世界
```

### JEP 128: Unicode BCP 47 Locale Matching (JDK 8)

| 属性 | 值 |
|------|-----|
| **角色** | Author |
| **Owner** | Yuka Kamiya |
| **状态** | Closed / Delivered |
| **发布版本** | JDK 8 |

**影响**: 实现 Unicode LDML 规范的 BCP 47 语言标签匹配。

```java
// BCP 47 语言范围匹配
List<Locale> locales = List.of(
    Locale.forLanguageTag("ja-JP"),
    Locale.forLanguageTag("en-US")
);

LanguageRange range = new LanguageRange("ja-JP");
Locale.filter(range, locales); // 匹配 ja-JP
```

### JEP 127: Improve Locale Data Packaging and Adopt Unicode CLDR Data (JDK 8)

| 属性 | 值 |
|------|-----|
| **角色** | Owner |
| **状态** | Closed / Delivered |
| **发布版本** | JDK 8 |

**影响**: 改进本地化数据打包，采用 Unicode CLDR 数据，减少堆内存占用。

---

## 核心技术贡献

### 1. CompactNumberFormat 实现 (JDK 11)

- **JDK-8177552**: Compact Number Formatting support
- **JDK-8222756**: Plural support in CompactNumberFormat
- **JDK-8232633**: 复数规则增强

实现紧凑数字格式化，支持 locale 相关的缩写形式：

```java
NumberFormat fmt = NumberFormat.getCompactNumberInstance(Locale.US, NumberFormat.Style.SHORT);
fmt.format(1000)   // "1K"
fmt.format(1000000) // "1M"
fmt.format(1000000000) // "1B"
```

### 2. Console API 改进

- **JDK-8308591**: JLine 作为默认 Console 提供者
- **JDK-8298322**: Console 实现分离 (ProxyingConsole)
- **JDK-8361613**: System.console() 仅对交互式终端可用
- **JDK-8295803**: Console 在 jshell 等环境中可用

```java
// 交互式终端检查
Console console = System.console();
if (console != null) {
    // 仅在真实终端环境中可用
    String line = console.readLine("Enter input: ");
}
```

### 3. Unicode 和 CLDR 更新

持续负责 Unicode 和 CLDR (Common Locale Data Repository) 版本更新：

| 版本 | JDK | 说明 |
|------|-----|------|
| Unicode 17.0 | JDK 26 | 最新 Unicode 标准 |
| CLDR 48.0 | JDK 26 | 本地化数据更新 |
| CLDR 47.0 | JDK 25 | 本地化数据更新 |
| ICU4J 78.1 | JDK 26 | ICU 库更新 |

### 4. TimeZone 数据维护

- **JDK-8352716**: 更新时区数据到 2025b
- **JDK-8342550**: 对 JDK1.1 兼容时区 ID 发出弃用警告
- **JDK-8166983**: 移除旧版/遗留 tzdata 文件

```java
// 弃用的时区 ID
TimeZone.getTimeZone("EST"); // 警告: 已弃用
TimeZone.getTimeZone("America/New_York"); // 推荐使用
```

### 5. Locale 和 Charset 改进

- **JDK-8353118**: 弃用 java.locale.useOldISOCodes 系统属性
- **JDK-8358626**: 生成 UTF-8 编码的 CLDR 资源
- **JDK-8357886**: 移除 COMPAT locale data provider 的 TimeZoneNames_*
- **JDK-8301971**: 使 JDK 源代码使用 UTF-8

### 6. System.out/err 编码改进

- **JDK-8352906**: 修复 Windows 上 stdout/err.encoding 设置
- **JDK-8359732**: 将标准 I/O 编码相关系统属性设为 StaticProperty
- **JDK-8356985**: Console 的 read*() 方法使用 stdin.encoding

### 7. DateTime API 增强

- **JDK-8364752**: java.time.Instant 支持 ISO 8601 的 HH:mm:ss 偏移格式
- **JDK-8351017**: 修复 ChronoUnit.MONTHS.between() 在二月的计算问题
- **JDK-8175709**: DateTimeFormatterBuilder.appendZoneId() JavaDoc 修复

### 8. ListFormat 实现

- **JDK-8041488**: Locale-Dependent List Patterns (ListFormat 实现)
- **JDK-8317265**: ListFormat::format 规范澄清
- **JDK-8318487**: ListFormat.equals() 方法规范
- **JDK-8318569**: 为 ListFormat 添加 Locale 和 Patterns 的 getter 方法

```java
// ListFormat 示例
ListFormat formatter = ListFormat.getInstance(Locale.US);
String result = formatter.format(List.of("Alice", "Bob", "Charlie"));
// "Alice, Bob, and Charlie"
```

### 9. Locale Provider 现代化

- **JDK-8174269**: 移除 COMPAT locale data provider (JDK 23)
  - 减少 JDK footprint 和启动时间
  - 迁移到 CLDR 数据
- **JDK-8138613**: 从默认提供者列表中移除 SPI locale provider adapter
  - 改善运行时启动性能
- **JDK-8305402**: 为 COMPAT provider 移除发出警告
- **JDK-8263202**: 更新 Hebrew/Indonesian/Yiddish ISO 639 语言代码
  - 使用当前 ISO 639 标准
  - 引入 java.locale.useOldISOCodes 系统属性以保持向后兼容
- **JDK-8269513**: 澄清 useOldISOCodes 系统属性规范
- **JDK-8267552**: ISO 639 语言代码发布说明
- **JDK-8353118**: 弃用 java.locale.useOldISOCodes 系统属性 (2025年4月)
- **JDK-8355522**: 移除 java.locale.useOldISOCodes 系统属性 (2025年12月)

> **说明**: Naoto Sato 主导了从旧版 ISO 639 代码到当前标准的迁移，提供了完整的迁移路径。

### 10. Collation 增强

- **JDK-8308108**: 支持 Unicode 扩展的排序设置
  - BCP 47 U 扩展支持
  - `ks` (colStrength) 和 `kk` (colNormalization) 参数

```java
// BCP 47 collation extensions
Locale locale = Locale.forLanguageTag("en-US-u-ks-level4-kk-true");
Collator collator = Collator.getInstance(locale);
// 使用四级排序强度和规范化
```

---

## 近期动态 (2024-2025)

### 2025 年工作

- **JEP draft 8344154**: JSON 便捷方法 - Owner，提交状态
- **JDK-8358626**: 生成 UTF-8 编码的 CLDR 资源 (6月)
- **JDK-8175709**: DateTimeFormatterBuilder.appendZoneId() JavaDoc 修复 (1月)
- **2025-12**: 撤回 Locale Enhancement Project 赞助

### 2024 年工作

- **JDK-8174269**: 移除 COMPAT locale data provider (v3, v5, v6 review)
- **JDK-8308108**: 支持 Unicode 扩展的排序设置 (BCP 47 U extension)
- **JDK-8318761**: MessageFormat 模式支持增强
- **JDK-8317265**: ListFormat::format 规范改进
- **JDK-8318487**: ListFormat.equals() 方法规范
- **JDK-8301991**: 将 l10n 属性资源包转换为 UTF-8 原生格式

### 2023 年工作

- **JDK-8041488**: Locale-Dependent List Patterns 实现
- 多个 Unicode 和 CLDR 更新

### 邮件列表活跃度

在 i18n-dev 邮件列表中持续活跃：
- 2025-06: RFR: 8358626 UTF-8 CLDR resources
- 2025-01: RFR: 8175709 DateTimeFormatterBuilder JavaDoc
- 2024: 多个 Collation 和 MessageFormat 相关 RFC

---

## 社区贡献与演讲

### Unicode Conference 演讲

Naoto Sato 是 International Unicode Conference (IUC) 的常驻演讲者：

| 会议 | 主题 | 合作者 |
|------|------|--------|
| IUC 31 | New Internationalization Features of the Java Platform | Craig Cummings |
| IUC 30 | Java Internationalization Updates | - |
| IUC 29 | XML Data Handling and Internationalization | - |
| IUC 28 | Java i18n Best Practices | - |
| IUC 26 | New Internationalization Features of the Java(TM) Platform | Craig Cummings |
| IUC 22 | Thai and Hindi Support in Sun's Java 2 Runtime Environment | - |

### Inside.java Podcast

- **Episode 23** (2022-03-22): "Java 18 is Here!"
  - 讨论 JEP 400: UTF-8 by Default
  - [收听链接](https://inside.java/2022/03/22/podcast-023/)

### 博客文章

- **"JEP 400 and the Default Charset"** (2021-10-04)
  - 详细解释 UTF-8 成为默认字符集的背景和影响
  - [文章链接](https://inside.java/2021/10/04/the-default-charset-jep400/)

---

## 贡献统计

### OpenJDK PR 统计

| 指标 | 数值 |
|------|------|
| **GitHub PRs** | 273+ 已合并 |
| **主要领域** | i18n, Unicode, CLDR, Console, TimeZone |
| **活跃时间** | 2000 - 至今 |

### 按类别贡献

| 类别 | 数量 | 描述 |
|------|------|------|
| Unicode/CLDR 更新 | 8+ | Unicode 17.0, CLDR 47/48, ICU4J 更新 |
| Console 改进 | 10+ | System.console() 增强, 编码处理 |
| TimeZone | 8+ | 时区数据更新, 弃用警告 |
| Locale/Charset | 12+ | Locale 处理, 字符集处理 |
| Date/Time | 5+ | Instant 解析, Calendar 修复 |
| Character/Emoji | 5+ | Unicode 块, emoji 方法 |

---

## 开发风格

### 代码质量关注点

1. **标准合规性**: 严格遵循 Unicode、CLDR、ISO 8601 等标准
2. **弃用管理**: 仔细规划弃用策略，提供迁移路径
3. **文档完善**: 清晰的 Javadoc 和 @spec 标签
4. **性能优化**: Static property 优化等性能改进

### 提交模式

- 将 Unicode/CLDR 更新分组处理
- 平台特定修复 (Windows, macOS, Linux)
- 测试基础设施改进
- 文档增强

### 测试方法

- Locale 数据验证
- 时区转换测试
- 字符编码验证
- Console 行为测试

---

## 主要 Bug 修复精选

| Issue | 标题 | 影响 |
|-------|------|------|
| 8372117 | Character.UnicodeBlock 注释修正 | 文档准确性 |
| 8346944 | 更新 Unicode 数据文件到 17.0.0 | Unicode 支持 |
| 8346947 | 更新 ICU4J 到 78.1 | 国际化 |
| 8354548 | 更新 CLDR 到 48.0 | 本地化数据 |
| 8369184 | SimpleTimeZone equals() 修复 | 正确性 |
| 8368328 | CompactNumberFormat.clone() 修复 | 线程安全 |
| 8364752 | Instant 支持 HH:mm:ss 偏移 | API 兼容性 |
| 8361972 | 明确 System.console() 条件 | 行为澄清 |
| 8361613 | System.console() 交互式终端检查 | 用户体验 |
| 8352906 | Windows stdout/err.encoding 修复 | 平台兼容性 |
| 8352716 | 时区数据更新到 2025b | 时区准确性 |
| 8342550 | JDK1.1 兼容时区 ID 弃用警告 | 迁移提示 |
| 8301971 | 使 JDK 源代码 UTF-8 | 代码现代化 |

---

## 相关链接

### 官方资料
- [OpenJDK Profile](https://openjdk.org/people/naoto)
- [Inside.java Profile](https://inside.java/u/NaotoSato/)
- [GitHub Profile](https://github.com/naotoj)

### JEP 文档
- [JEP draft 8344154: Convenience Methods for JSON Documents](https://openjdk.org/jeps/8344154)
- [JEP 400: UTF-8 by Default](https://openjdk.org/jeps/400)
- [JEP 252: Use CLDR Locale Data by Default](https://openjdk.org/jeps/252)
- [JEP 226: UTF-8 Property Resource Bundles](https://openjdk.org/jeps/226)
- [JEP 128: Unicode BCP 47 Locale Matching](https://openjdk.org/jeps/128)
- [JEP 127: Improve Locale Data Packaging](https://openjdk.org/jeps/127)

### 文章和演讲
- [JEP 400 and the Default Charset](https://inside.java/2021/10/04/the-default-charset-jep400/)
- [Inside Java Podcast Episode 23](https://inside.java/2022/03/22/podcast-023/)
- [Unicode Conference Presentations](https://www.unicodeconference.org/)

### 开发资源
- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=naotoj)
- [JBS Issues](https://bugs.openjdk.org/issues/?jql=reporter%20%3D%20naoto)
- [i18n-dev Mailing List](https://mail.openjdk.org/mailman/listinfo/i18n-dev)

---

**Sources**:
- [Inside.java - NaotoSato](https://inside.java/u/NaotoSato/)
- [OpenJDK JEP draft 8344154: JSON Convenience Methods](https://openjdk.org/jeps/8344154)
- [OpenJDK JEP 400: UTF-8 by Default](https://openjdk.org/jeps/400)
- [OpenJDK JEP 252: Use CLDR Locale Data by Default](https://openjdk.org/jeps/252)
- [OpenJDK JEP 226: UTF-8 Property Resource Bundles](https://openjdk.org/jeps/226)
- [OpenJDK JEP 128: Unicode BCP 47 Locale Matching](https://openjdk.org/jeps/128)
- [OpenJDK JEP 127: Improve Locale Data Packaging](https://openjdk.org/jeps/127)
- [JEP 400 and the Default Charset - Inside.java](https://inside.java/2021/10/04/the-default-charset-jep400/)
- [Inside Java Podcast Episode 23](https://inside.java/2022/03/22/podcast-023/)
- [Unicode Conference Biographies](http://www.unicode.org/iuc/iuc28/biosabstracts/b030.html)
- [OpenJDK i18n Group](https://openjdk.org/groups/i18n/)
- [i18n-dev Mailing List - 2025-06](https://mail.openjdk.org/archives/list/i18n-dev@openjdk.org/2025/6/)
- [i18n-dev Mailing List - JDK-8301991](https://mail.openjdk.org/pipermail/i18n-dev/2023-September/003977.html)
- [i18n-dev Mailing List - Locale Enhancement Withdrawal](https://mail.openjdk.org/pipermail/i18n-dev/2025-December/012223.html)
- [Build-dev Mailing List - JDK-8263202](https://mail.openjdk.org/archives/list/build-dev@openjdk.org/thread/XQ7SFQZNRTMEKY5M2SJCGEMJTVRRC5CI/)
- [JDK-8174269 Webrev - COMPAT Removal](https://cr.openjdk.org/~naoto/JDK-8174269-COMPAT-Removal/)
- [JDK-8041488 Webrev - List Patterns](https://cr.openjdk.org/~naoto/JDK-8041488-ListPatterns/webrev.04/)
- [JDK-8318487 Webrev - ListFormat.equals](https://cr.openjdk.org/~naoto/JDK-8318487-ListFormat.equals/webrev.00/)
- [ZoomInfo - Naoto Sato Profile](https://www.zoominfo.com/p/Naoto-Sato/186129467)
