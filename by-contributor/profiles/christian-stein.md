# Christian Stein

> **GitHub**: [@sormuras](https://github.com/sormuras)
> **Organization**: Oracle
> **OpenJDK Contributions**: 77 to openjdk/jdk (77 integrated PRs on GitHub)

---
## Table of Contents

1. [Overview](#1-overview)
2. [Basic Information](#2-basic-information)
3. [Contribution Overview](#3-contribution-overview)
4. [Key Contributions](#4-key-contributions)
5. [Recent Activity](#5-recent-activity)
6. [Development Style](#6-development-style)
7. [Related Links](#7-related-links)

---

## 1. Overview

Christian Stein is an Oracle engineer based in Germany, widely known in the Java ecosystem as the creator and lead of the JUnit Platform's module-aware test infrastructure. Within OpenJDK, his 77 contributions focus on the Java source launcher, jtreg test infrastructure, jar tool validation, and module system tooling. He is the primary driver behind JEP 458 (Launch Multi-File Source-Code Programs) and has systematically modernized JDK test suites to use JUnit, while maintaining the jtreg test harness integration across releases.

---

## 2. Basic Information

| Attribute | Value |
|-----------|-------|
| **Name** | Christian Stein |
| **Current Organization** | Oracle (Java Platform Group, Language Tools) |
| **GitHub** | [@sormuras](https://github.com/sormuras) |
| **Personal Website** | [sormuras.github.io](https://sormuras.github.io/) |
| **Bio** | @openjdk / @junit-team |
| **Location** | Germany |
| **Java Experience** | Programming with Java since 1998 |
| **PRs** | [77 integrated](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Asormuras+is%3Aclosed+label%3Aintegrated) |
| **Total Contributions** | 77 |
| **Primary Areas** | Source launcher, jtreg, jar tool, module system, JUnit migration |

---

## 3. Contribution Overview

### By Category

| Category | Approx. Count | Description |
|----------|---------------|-------------|
| Source Launcher | 15+ | Multi-file launch, service loader SPI, edge cases |
| jtreg Updates | 12+ | Version bumps, GitHub Actions integration, configuration |
| JUnit Migration | 10+ | Refactoring JDK tests from testng/custom to JUnit |
| jar Tool | 8+ | Validation, multi-release JARs, parent directory creation |
| Java Launcher | 6+ | Help text, argument files, native access |
| Module System | 5+ | Automatic module names, module-path documentation |
| Test Infrastructure | 10+ | Problem listing, ToolBox API, TEST.ROOT configuration |

---

## 4. Key Contributions

### 4.1 JEP 458: Launch Multi-File Source-Code Programs (JDK-8306914)

Stein's most significant contribution to OpenJDK: implementing the ability for the `java` launcher to compile and run programs composed of multiple source files without requiring explicit compilation. This dramatically lowers the barrier for scripting and prototyping in Java, extending the single-file source launcher introduced in JDK 11.

### 4.2 Source Launcher Service Loader Support (JDK-8333131, JDK-8336470)

Extended the source launcher to work with the ServiceLoader SPI in unnamed modules, enabling source-launched programs to discover and use service providers. This makes the source launcher viable for more realistic application patterns.

### 4.3 jar --validate Enhancements (JDK-8268611, JDK-8268613)

Improved the `jar --validate` command to check targeted classes in multi-release JAR files and verify initial entries. These additions make `jar --validate` a more comprehensive tool for detecting malformed JARs before deployment.

### 4.4 Automatic Module Name Validation (JDK-8375433)

Added validation of automatic module names in the `jar` tool, catching invalid module names at packaging time rather than at runtime. This helps developers catch module system issues earlier in their build process.

### 4.5 JUnit Test Migration

Leading an ongoing effort to migrate JDK test suites from ad-hoc test frameworks and TestNG to JUnit. Recent work includes refactoring tests in `jdk/com/sun`, `langtools/shellsupport/doc`, and `lib-test/jdk` directories, improving test consistency and maintainability.

### 4.6 CommandLine Reusable Module (JDK-8236919)

Refactored `com.sun.tools.javac.main.CommandLine` into a reusable module shared across JDK tools, eliminating duplication of argument file parsing logic between javac, jar, and other tools.

---

## 5. Recent Activity

| Date | PR | Title |
|------|-----|-------|
| 2026-03 | [#30203](https://github.com/openjdk/jdk/pull/30203) | Refactor jdk/com/sun tests to use JUnit |
| 2026-03 | [#30166](https://github.com/openjdk/jdk/pull/30166) | Refactor langtools/shellsupport/doc tests to use JUnit |
| 2026-03 | [#30089](https://github.com/openjdk/jdk/pull/30089) | Remove modular transition support settings from TEST.ROOT |
| 2026-03 | [#30087](https://github.com/openjdk/jdk/pull/30087) | Use JUnit in lib-test/jdk tests |
| 2026-02 | [#29452](https://github.com/openjdk/jdk/pull/29452) | Update to use jtreg 8.2.1 |

---

## 6. Career History & Community Roles

| Year | Event | Details |
|------|-------|---------|
| **1998** | Started Java development | Programming with Java since 1998 |
| **2017** | Joined JUnit Team | Core member of JUnit 5 development team |
| **2019** | OpenJDK Author | Granted OpenJDK Author status |
| **~2020** | Joined Oracle | Java Platform Group, Language Tools team |
| **2020** | OpenJDK Committers' Workshop | Talk: "Bach.java + Testing In The Modular World" |

### OpenJDK Roles

- **JDK Committer/Reviewer**: Mainline contributor
- **JEP Owner**: JEP 458 (Launch Multi-File Source-Code Programs) — primary implementer
- **jtreg Steward**: Responsible for jtreg version updates across JDK releases

### Open Source Projects

| Project | Role |
|---------|------|
| **JUnit 5** | Core Team Member (since 2017) |
| **Apache Maven** | Developer |
| **Bach** | Creator — module-only build tool leveraging jshell/java |
| **junit-platform-maven-plugin** | Author — Maven integration for JUnit Platform |

### Conference Talks

| Year | Event | Topic |
|------|-------|-------|
| **2021** | FOSDEM | [Free Java Devroom talk](https://archive.fosdem.org/2021/schedule/speaker/christian_stein/) |
| **2023** | JavaLand | "JDK Tools and where to find them" |
| **2020** | JUG Hessel | "Bach.java + Testing In The Modular World" |
| **2019** | Accento.dev Karlsruhe | ["Testing In The Modular World"](https://2019.accento.dev/speakers/christian-stein/) |
| **Various** | JavaZone Oslo, German JUGs | "JUnit 5 - Platform & Jupiter API" |

### Writing

- Contributor at [Inside.java](https://inside.java/u/ChristianStein/)
- Author at [foojay.io](https://foojay.io/today/author/sormuras/)
- Technical blog at [sormuras.github.io](https://sormuras.github.io/)

---

## 7. Development Style

### Patterns

- **Tooling-first mindset**: Focuses on improving the developer experience through better launcher behavior, tool validation, and test infrastructure rather than core runtime changes.
- **Systematic modernization**: Methodically migrating test suites to JUnit across multiple JDK modules, one directory at a time, with careful attention to test semantics.
- **jtreg stewardship**: Responsible for jtreg version updates across JDK releases, coordinating GitHub Actions CI integration and resolving compatibility issues.
- **Edge case hunter**: Many source launcher contributions fix obscure but real edge cases (classes with `$` in names, trailing comments in argument files, missing stack traces in exceptions).
- **Cross-project perspective**: Brings experience from JUnit Platform and build tool ecosystems to improve JDK's own testing and tooling practices.

### Commit Style

Commits follow the standard OpenJDK format: `JDK-NNNNNNN: <description>`. Messages are descriptive and action-oriented, often explaining the user-visible behavior being fixed.

---

## 8. Related Links

- [GitHub Profile](https://github.com/sormuras)
- [Personal Website](https://sormuras.github.io/)
- [Inside.java Author Page](https://inside.java/u/ChristianStein/)
- [foojay.io Author Page](https://foojay.io/today/author/sormuras/)
- [FOSDEM 2021 Speaker Page](https://archive.fosdem.org/2021/schedule/speaker/christian_stein/)
- [Accento 2019 Speaker Page](https://2019.accento.dev/speakers/christian-stein/)
- [GitHub Commits to openjdk/jdk](https://github.com/openjdk/jdk/commits?author=sormuras)
- [Integrated PRs](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Asormuras+is%3Aclosed+label%3Aintegrated)
