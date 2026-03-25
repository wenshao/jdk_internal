# Backport 追踪分析

> 4,554 个主线 PR 被 backport 到 LTS 维护分支

---

## 1. 概览

| 指标 | 值 |
|------|-----|
| **被 backport 的主线 PR** | 4554 / 22501 (20%) |
| **backport 到 2+ 版本** | 2258 |
| **backport 到 3+ 版本** | 438 |

## 2. 按优先级

| 优先级 | 主线总数 | 被 backport | 比率 |
|--------|---------|------------|------|
| P1 | 155 | 14 | 9% |
| P2 | 985 | 169 | 17% |
| P3 | 4141 | 1074 | 25% |
| P4 | 16187 | 3181 | 19% |
| P5 | 887 | 100 | 11% |

## 3. 按组织

| 组织 | 被 backport | 主线总数 | 比率 |
|------|------------|---------|------|
| Oracle | 2991 | 15577 | 19% |
| Amazon | 268 | 1130 | 23% |
| SAP | 239 | 602 | 39% |
| Red Hat | 119 | 438 | 27% |
| Alibaba | 75 | 376 | 19% |
| IBM | 54 | 220 | 24% |
| Tencent | 41 | 211 | 19% |
| Intel | 13 | 181 | 7% |

## 4. 按模块 (Top 15)

| 模块 | backport 数 |
|------|------------|
| test | 1169 |
| client | 350 |
| core-libs/java.net | 287 |
| core-libs/java.io | 284 |
| hotspot | 258 |
| arch/x86 | 231 |
| security | 191 |
| build | 181 |
| compiler/c2 | 176 |
| runtime/threading | 138 |
| compiler | 128 |
| gc | 114 |
| core-libs | 113 |
| runtime/jfr | 97 |
| arch/aarch64 | 95 |

## 5. 各 LTS 版本 backport 覆盖

| LTS 版本 | 维护 PRs | 可追溯主线 | 追溯率 |
|----------|---------|-----------|--------|
| JDK 17u | 4000 | 3137 | 78% |
| JDK 21u | 2486 | 2061 | 82% |
| JDK 11u | 2771 | 1575 | 56% |
| JDK 25u | 341 | 307 | 90% |
| JDK 8u | 601 | 228 | 37% |

## 6. 被 backport 到最多版本的 PR

| Bug ID | 标题 | Author | 组织 | 优先级 | backport 到 |
|--------|------|--------|------|--------|-------------|
| [8375063](../../by-pr/8375/8375063.md) | Update Libpng to 1.6.54 | jayathirthrao | Oracle | P3 | JDK 11u, JDK 17u, JDK 21u, JDK 25u, JDK 8u |
| [8369282](../../by-pr/8369/8369282.md) | Distrust TLS server certificates anchored by Chung | mcpowers | Oracle | P3 | JDK 11u, JDK 17u, JDK 21u, JDK 25u, JDK 8u |
| [8373476](../../by-pr/8373/8373476.md) | (tz) Update Timezone Data to 2025c | johnyjose30 |  | P3 | JDK 11u, JDK 17u, JDK 21u, JDK 25u, JDK 8u |
| [8377526](../../by-pr/8377/8377526.md) | Update Libpng to 1.6.55 | jayathirthrao | Oracle | P3 | JDK 11u, JDK 17u, JDK 21u, JDK 25u, JDK 8u |
| [8301310](../../by-pr/8301/8301310.md) | The SendRawSysexMessage test may cause a JVM crash | AlecJY |  | P3 | JDK 11u, JDK 17u, JDK 21u, JDK 8u |
| [8318410](../../by-pr/8318/8318410.md) | jdk/java/lang/instrument/BootClassPath/BootClassPa | yukikimmura |  | P4 | JDK 11u, JDK 17u, JDK 21u, JDK 8u |
| [8322725](../../by-pr/8322/8322725.md) | (tz) Update Timezone Data to 2023d | johnyjose30 |  | P3 | JDK 11u, JDK 17u, JDK 21u, JDK 8u |
| [8323640](../../by-pr/8323/8323640.md) | [TESTBUG]testMemoryFailCount in jdk/internal/platf | sendaoYan | Alibaba | P4 | JDK 11u, JDK 17u, JDK 21u, JDK 8u |
| [8321480](../../by-pr/8321/8321480.md) | ISO 4217 Amendment 176 Update | justin-curtis-lu | Oracle | P3 | JDK 11u, JDK 17u, JDK 21u, JDK 8u |
| [8325096](../../by-pr/8325/8325096.md) | Test java/security/cert/CertPathBuilder/akiExt/AKI | coffeys | Oracle | P4 | JDK 11u, JDK 17u, JDK 21u, JDK 8u |
| [8325150](../../by-pr/8325/8325150.md) | (tz) Update Timezone Data to 2024a | johnyjose30 |  | P3 | JDK 11u, JDK 17u, JDK 21u, JDK 8u |
| [8318039](../../by-pr/8318/8318039.md) | GHA: Bump macOS and Xcode versions | vidmik | Oracle | P4 | JDK 11u, JDK 17u, JDK 21u, JDK 8u |
| [8324723](../../by-pr/8324/8324723.md) | GHA: Upgrade some actions to avoid deprecated Node | shipilev | Amazon | P4 | JDK 11u, JDK 17u, JDK 21u, JDK 8u |
| [8326529](../../by-pr/8326/8326529.md) | JFR: Test for CompilerCompile events fails due to  | roberttoyonaga |  | P4 | JDK 11u, JDK 17u, JDK 21u, JDK 8u |
| [8328825](../../by-pr/8328/8328825.md) | Google CAInterop test failures | rhalade | Oracle | P3 | JDK 11u, JDK 17u, JDK 21u, JDK 8u |
| [8305931](../../by-pr/8305/8305931.md) | jdk/jfr/jcmd/TestJcmdDumpPathToGCRoots.java failed | egahlin | Oracle | P4 | JDK 11u, JDK 17u, JDK 21u, JDK 8u |
| [8326521](../../by-pr/8326/8326521.md) | JFR: CompilerPhase event test fails on windows 32  | roberttoyonaga |  | P4 | JDK 11u, JDK 17u, JDK 21u, JDK 8u |
| [8316138](../../by-pr/8316/8316138.md) | Add GlobalSign 2 TLS root certificates | rhalade | Oracle | P3 | JDK 11u, JDK 17u, JDK 21u, JDK 8u |
| [8316328](../../by-pr/8316/8316328.md) | Test jdk/jfr/event/oldobject/TestSanityDefault.jav | mrserb | Oracle | P3 | JDK 11u, JDK 17u, JDK 21u, JDK 8u |
| [8311666](../../by-pr/8311/8311666.md) | Disabled tests in test/jdk/sun/java2d/marlin | cushon | Google | P3 | JDK 11u, JDK 17u, JDK 21u, JDK 8u |
| [8305072](../../by-pr/8305/8305072.md) | Win32ShellFolder2.compareTo is inconsistent | aivanov-jdk | Oracle | P4 | JDK 11u, JDK 17u, JDK 21u, JDK 8u |
| [8333724](../../by-pr/8333/8333724.md) | Problem list security/infra/java/security/cert/Cer | RealCLanger | SAP | P4 | JDK 11u, JDK 17u, JDK 21u, JDK 8u |
| [8334653](../../by-pr/8334/8334653.md) | ISO 4217 Amendment 177 Update | justin-curtis-lu | Oracle | P3 | JDK 11u, JDK 17u, JDK 21u, JDK 8u |
| [8336928](../../by-pr/8336/8336928.md) | GHA: Bundle artifacts removal broken | zzambers |  | P4 | JDK 11u, JDK 17u, JDK 21u, JDK 8u |
| [8316193](../../by-pr/8316/8316193.md) | jdk/jfr/event/oldobject/TestListenerLeak.java java | egahlin | Oracle | P4 | JDK 11u, JDK 17u, JDK 21u, JDK 8u |
| [8338402](../../by-pr/8338/8338402.md) | GHA: some of bundles may not get removed | zzambers |  | P4 | JDK 11u, JDK 17u, JDK 21u, JDK 8u |
| [8339644](../../by-pr/8339/8339644.md) | Improve parsing of Day/Month in tzdata rules | naotoj | Oracle | P4 | JDK 11u, JDK 17u, JDK 21u, JDK 8u |
| [8340815](../../by-pr/8340/8340815.md) | Add SECURITY.md file | gdams |  | P4 | JDK 11u, JDK 17u, JDK 21u, JDK 8u |
| [8340387](../../by-pr/8340/8340387.md) | Update OS detection code to recognize Windows Serv | MBaesken | SAP | P3 | JDK 11u, JDK 17u, JDK 21u, JDK 8u |
| [8335912](../../by-pr/8335/8335912.md) | Add an operation mode to the jar command when extr | slowhog | Oracle | P5 | JDK 11u, JDK 17u, JDK 21u, JDK 8u |

---

> **统计时间**: 2026-03-25
