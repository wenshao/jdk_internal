# Erik Duveblad

> Skara project creator, GitHub tooling architect for OpenJDK, build infrastructure and CI contributor

---

## Table of Contents

1. [Basic Information](#1-basic-information)
2. [Career Timeline](#2-career-timeline)
3. [Contribution Overview](#3-contribution-overview)
4. [Key Contributions](#4-key-contributions)
5. [Technical Expertise](#5-technical-expertise)
6. [Contribution Timeline](#6-contribution-timeline)
7. [Development Style](#7-development-style)
8. [Collaboration Network](#8-collaboration-network)
9. [Historical Contributions](#9-historical-contributions)
10. [External Resources](#10-external-resources)

---

## 1. Basic Information

| Field | Value |
|-------|-------|
| **Name** | Erik Duveblad |
| **Current Organization** | Oracle |
| **GitHub** | [@edvbld](https://github.com/edvbld) |
| **OpenJDK** | [edvbld](https://openjdk.org/census#edvbld) |
| **Role** | Skara Project Lead, Code Tools Committer |
| **Contributions** | 241 contributions to openjdk/jdk; 583 commits to openjdk/skara |
| **Primary Areas** | Skara (GitHub bot/tooling), build infrastructure, CI tooling, GC/Metaspace (early career) |
| **Active Period** | 2012 -- 2023 |

> **Data sources**: [GitHub](https://github.com/edvbld), [OpenJDK Census](https://openjdk.org/census), [Skara Project](https://openjdk.org/projects/skara)

---

## 2. Career Timeline

| Year | Event | Details |
|------|-------|---------|
| **2012** | Joined Oracle / OpenJDK | First commits to HotSpot (GC, Metaspace) |
| **2013** | Metaspace contributor | Key work on NPG (Native Permanent Generation) removal, jstat/jmap updates |
| **2017-2018** | GC refactoring | G1 policy cleanup, reproducible builds |
| **2018-2019** | Skara project launch | Created GitHub integration tooling for OpenJDK's migration from Mercurial |
| **2020** | Repository modernization | Added CONTRIBUTING.md, converted README to Markdown |
| **2023** | JFR enhancements | Periodic heap usage JFR events |

---

## 3. Contribution Overview

Erik Duveblad is best known as the primary architect of the **Skara project**, the tooling suite that enabled OpenJDK's historic migration from Mercurial to GitHub. While his commit count in openjdk/jdk (241) reflects his direct codebase contributions, his broader impact through Skara (583 commits in openjdk/skara, 209 stars) fundamentally changed the OpenJDK development workflow for hundreds of contributors.

### Contribution Categories

| Category | Scope | Description |
|----------|-------|-------------|
| Skara / GitHub Tooling | openjdk/skara | Bots, CLI tools, GitHub/Mercurial bridge |
| GC / Metaspace | openjdk/jdk | Early career HotSpot contributions |
| Build Infrastructure | openjdk/jdk | Build system, test configuration |
| Repository Maintenance | openjdk/jdk | README, CONTRIBUTING, test fixes |
| JFR | openjdk/jdk | Periodic heap usage events |

---

## 4. Key Contributions

### 1. Skara Project (2018-present)

The **Skara project** (openjdk/skara) is Erik's defining contribution to OpenJDK. It provides:

- **GitHub bots** -- automated integration, labeling, reviewer assignment, and merge conflict detection for all OpenJDK repositories
- **CLI tools** -- `git-jcheck`, `git-webrev`, `git-skara` commands that integrate with OpenJDK workflows
- **Code review bridge** -- connecting GitHub pull requests with the OpenJDK review process
- **Mailing list integration** -- mirroring PR discussions to mailing lists and vice versa

With 583 commits and the majority of the codebase authored by Erik, Skara is the infrastructure that makes GitHub-based OpenJDK development possible.

### 2. Metaspace / NPG Migration (2012-2013)

Early in his OpenJDK career, Erik contributed to the removal of PermGen and introduction of Metaspace:

- **JDK-8004924**: jmap -heap output for ClassMetaspaceSize
- **JDK-8004172**: Updated jstat counter names for metaspace
- **JDK-8005116**: Renamed -permstat to -clstats in jmap
- **JDK-8000754**: Implemented MemoryPool MXBean for Metaspace

### 3. G1 GC Refactoring (2018)

- **JDK-8197852**: Moved G1DefaultPolicy into G1Policy
- **JDK-8199024**: Removed unnecessary protected/virtual modifiers from G1CollectedHeap
- **JDK-8199027**: Made protected members private in G1Policy
- **JDK-8200626**: Restored history for g1ConcurrentMarkThread files

### 4. Build and Test Infrastructure (2020)

- **JDK-8193686**: Allow --with-jtreg to accept zip compressed jtreg images
- **JDK-8237566**: FindTests.gmk to only include existing TEST.ROOT files
- **JDK-8251551**: Converted README to .md format
- **JDK-8251552**: Added minimal CONTRIBUTING.md file

### 5. JFR Enhancement (2023)

- **JDK-8307458**: Added periodic heap usage JFR events

---

## 5. Technical Expertise

`Skara` `GitHub Bots` `CI/CD Tooling` `Mercurial-to-Git Migration` `HotSpot GC` `Metaspace` `G1 Collector` `Build System` `JFR` `Java` `Rust` `Haskell`

---

## 6. Contribution Timeline

```
2012: ████████████          First HotSpot commits (GC, Metaspace)
2013: ████████████████████  NPG/Metaspace migration work
2014-17: ████████            Internal tooling work
2018: ████████████████████  G1 refactoring, Skara project launch
2019: ██████████████████████████████  Skara development (peak)
2020: ████████████████████  Build infra, repo modernization
2021-22: ████████            Skara maintenance
2023: ██████                JFR enhancements
```

---

## 7. Development Style

- **Tooling-first approach**: Erik's primary impact is through developer tooling rather than runtime code, building the infrastructure that enables other contributors
- **Clean refactoring**: His G1 and Metaspace work shows disciplined cleanup -- removing unnecessary modifiers, consolidating classes, improving code organization
- **Polyglot developer**: Personal projects in Rust (git implementation, Scheme interpreter) and Haskell (MiniJava compiler) demonstrate broad language interests
- **Infrastructure mindset**: From Metaspace monitoring to build system improvements to GitHub bots, his work consistently focuses on making the platform more observable and maintainable

---

## 8. Collaboration Network

### Key Collaborators

| Collaborator | Area |
|--------------|------|
| Erik Joelsson | Build infrastructure |
| Magnus Ihse Bursie | Build system |
| Robin Westberg | Skara project |
| Thomas Schatzl | G1 GC |
| Stefan Karlsson | HotSpot runtime |

---

## 9. Historical Contributions

### JDK Version Contributions

| JDK Version | Primary Contributions |
|-------------|----------------------|
| JDK 8 | Metaspace/NPG migration, jstat/jmap updates |
| JDK 10-11 | G1 GC refactoring, reproducible builds |
| JDK 14-16 | Skara project, GitHub migration tooling |
| JDK 17+ | Build infrastructure, repository modernization |
| JDK 21 | JFR periodic heap usage events |

### Long-term Impact

- **Workflow transformation**: Skara enabled OpenJDK's migration from Mercurial to GitHub, fundamentally changing how 500+ contributors interact with the project
- **Automation**: The bot infrastructure handles thousands of PRs per year across dozens of OpenJDK repositories
- **Metaspace monitoring**: Early contributions to Metaspace tooling remain in the JDK diagnostic stack

---

## 10. External Resources

| Type | Link |
|------|------|
| **GitHub** | [@edvbld](https://github.com/edvbld) |
| **Skara Project** | [openjdk.org/projects/skara](https://openjdk.org/projects/skara) |
| **Skara Repository** | [openjdk/skara](https://github.com/openjdk/skara) (209 stars, 583 commits by edvbld) |
| **Code Review Repository** | [openjdk/cr](https://github.com/openjdk/cr) |
| **GitHub Commits (jdk)** | [openjdk/jdk commits by edvbld](https://github.com/openjdk/jdk/commits?author=edvbld) |
| **JBS Issues** | [bugs.openjdk.org](https://bugs.openjdk.org/issues/?jql=assignee%20%3D%20edvbld) |

---

> **Note**: Erik Duveblad's contribution count in openjdk/jdk (241) understates his overall impact on OpenJDK. His 583 commits to openjdk/skara represent the tooling layer that powers the entire GitHub-based development workflow for the project. This profile is based on publicly available information and may need further verification.
