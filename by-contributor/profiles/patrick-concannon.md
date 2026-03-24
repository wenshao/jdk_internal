# Patrick Concannon

> **GitHub**: [@pconcannon](https://github.com/pconcannon)
> **Organization**: Oracle
> **OpenJDK Contributions**: 76 to openjdk/jdk (31 integrated PRs on GitHub)

---
## 目录

1. [概述](#1-概述)
2. [Basic Information](#2-basic-information)
3. [Contribution Overview](#3-contribution-overview)
4. [Key Contributions](#4-key-contributions)
5. [Recent Activity](#5-recent-activity)
6. [Development Style](#6-development-style)
7. [Related Links](#7-related-links)

---

## 1. 概述

Patrick Concannon is an Oracle engineer who contributed to the JDK primarily in the areas of networking (java.net), HTTP server/client APIs, and core library modernization. With 76 contributions to openjdk/jdk, he was active during the JDK 16-18 era, driving two major efforts: (1) cleaning up and modernizing the HTTP server and networking javadoc, and (2) systematically updating core library packages to use modern Java language features like `instanceof` pattern variables and switch expressions. He also contributed to socket implementation cleanup, helping remove legacy `PlainSocketImpl` and `PlainDatagramSocketImpl` code.

---

## 2. Basic Information

| Attribute | Value |
|-----------|-------|
| **Name** | Patrick Concannon |
| **Current Organization** | Oracle |
| **GitHub** | [@pconcannon](https://github.com/pconcannon) |
| **PRs** | [31 integrated](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Apconcannon+is%3Aclosed+label%3Aintegrated) |
| **Total Contributions** | 76 (including pre-GitHub commits) |
| **主要领域** | Networking, HTTP Server/Client, Language Modernization, java.net |

---

## 3. Contribution Overview

### By Category

| Category | Approx. Count | Description |
|----------|---------------|-------------|
| HTTP Server Javadoc | 8 | Comprehensive javadoc cleanup across com.sun.net.httpserver |
| Socket Implementation | 5 | Removing legacy socket impls, deprecating factory mechanisms |
| Pattern Variable Migration | 7 | Updating core packages to use `instanceof` pattern variables |
| Switch Expression Migration | 6 | Updating core packages to use switch expressions |
| Networking APIs | 5+ | HttpRequest.Builder, UnixDomainPrincipal, NAPI tests |

### Key Areas of Expertise

- **HTTP Server API (com.sun.net.httpserver)**: Javadoc quality across HttpExchange, HttpServer, HttpHandler, HttpPrincipal, HttpsExchange, Authenticator, Filter, and Headers classes.
- **Socket Implementation Cleanup**: Removal of legacy `PlainSocketImpl`/`PlainDatagramSocketImpl`, deprecation of the socket impl factory mechanism, dropping pre-JDK 1.4 DatagramSocketImpl support.
- **Language Modernization**: Systematic migration of core library code to use `instanceof` pattern variables (JEP 375/394) and switch expressions (JEP 361) across java.lang, java.net, java.nio, java.time, java.util, java.io, java.math, java.text, and java.security.
- **HTTP Client API**: Enhancing `HttpRequest.Builder` with the ability to seed from an existing `HttpRequest` (JDK-8252304).

---

## 4. Key Contributions

### 4.1 Legacy Socket Implementation Removal (JDK-8253119)

Removed the legacy `PlainSocketImpl` and `PlainDatagramSocketImpl` implementations ([PR #4574](https://github.com/openjdk/jdk/pull/4574)). This was a significant cleanup that eliminated dual socket implementation paths, simplifying the networking stack after the NIO-based socket reimplementation in JDK 15-16.

### 4.2 Socket Impl Factory Deprecation (JDK-8235139)

Deprecated the socket implementation factory mechanism ([PR #2375](https://github.com/openjdk/jdk/pull/2375)), marking it for eventual removal. This legacy API allowed replacing the default socket implementation, which conflicted with the modern NIO-based approach.

### 4.3 HttpRequest.Builder Seeding (JDK-8252304)

Added the ability to seed an `HttpRequest.Builder` from an existing `HttpRequest` ([PR #1059](https://github.com/openjdk/jdk/pull/1059)), making it easier to create modified copies of HTTP requests in the java.net.http API.

### 4.4 HTTP Server Javadoc Overhaul

Conducted a comprehensive javadoc cleanup across the entire `com.sun.net.httpserver` package in a series of PRs (#81, #301, #429, #506, #610, #810, #958, #1014). This included fixing `HttpPrincipal.getName()` returning incorrect names (JDK-8255584) and adding missing `@throws IOException` declarations.

### 4.5 Core Library Language Modernization

Led a systematic effort to update core library code to modern Java idioms across 14 PRs. This covered `instanceof` pattern variables in java.lang, java.net, java.nio, java.time, java.io, java.math, java.text, java.util, and java.security, followed by switch expression conversions in the same packages.

### 4.6 UnixDomainPrincipal Record Class (JDK-8254996)

Converted `jdk.net.UnixDomainPrincipal` to a record class ([PR #1668](https://github.com/openjdk/jdk/pull/1668)), an early adoption of the records feature in the JDK codebase.

---

## 5. Recent Activity

| Date | PR | Title |
|------|-----|-------|
| 2021-11 | [#6252](https://github.com/openjdk/jdk/pull/6252) | Remove usePlainDatagramSocketImpl option from test |
| 2021-11 | [#5887](https://github.com/openjdk/jdk/pull/5887) | Drop support for pre JDK 1.4 DatagramSocketImpl implementations |
| 2021-07 | [#4690](https://github.com/openjdk/jdk/pull/4690) | Insert missing commas in copyrights in java.net |
| 2021-07 | [#4574](https://github.com/openjdk/jdk/pull/4574) | Remove the legacy PlainSocketImpl and PlainDatagramSocketImpl |
| 2021-07 | [#4553](https://github.com/openjdk/jdk/pull/4553) | Update java.security to use switch expressions |
| 2021-07 | [#4552](https://github.com/openjdk/jdk/pull/4552) | Update java.time to use switch expressions (part II) |
| 2021-06 | [#4433](https://github.com/openjdk/jdk/pull/4433) | Update java.time to use switch expressions |
| 2021-06 | [#4312](https://github.com/openjdk/jdk/pull/4312) | Update java.lang to use switch expressions |

---

## 6. Development Style

### Patterns

- **Systematic module-by-module sweeps**: Tackling an entire category of changes across all core library packages in order, ensuring consistent modernization.
- **Documentation-first**: Many contributions focused on javadoc correctness, sometimes finding actual bugs during review (e.g., HttpPrincipal.getName).
- **Legacy cleanup**: Several contributions removed deprecated or obsolete code paths, simplifying the codebase.
- **Concentrated activity period**: Most GitHub contributions occurred during 2020-2021 (JDK 16-18 era), with the remaining 45 contributions in the pre-GitHub period.

### Commit Style

Commits follow the standard OpenJDK format: `JDK-NNNNNNN: <description>`. Messages are concise and directly match the JBS bug title.

---

## 7. Related Links

- [GitHub Profile](https://github.com/pconcannon)
- [GitHub Commits to openjdk/jdk](https://github.com/openjdk/jdk/commits?author=pconcannon)
- [Integrated PRs](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Apconcannon+is%3Aclosed+label%3Aintegrated)


## 审查统计

| 指标 | 值 |
|------|-----|
| **总审查次数** | 28 |
| **活跃仓库数** | 1 |
