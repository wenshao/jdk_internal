# JDK 8/11/17 Top Contributors

> **Note**: These are historical LTS versions before GitHub PR integration (2021). Data is based on [OpenJDK Census](https://openjdk.org/census) commit counts.

---

## Historical Context

| Version | GA Date | End of Active Support | Primary Development Period |
|---------|---------|----------------------|---------------------------|
| **JDK 8** | 2014-03 | 2019-01 (Public) | 2011-2014 |
| **JDK 11** | 2018-09 | 2023-09 (Public) | 2017-2018 |
| **JDK 17** | 2021-09 | 2029-09 (Estimated) | 2020-2021 |

**Important**: GitHub Integrated PRs started in 2021. For JDK 8/11/17, we use OpenJDK Census commit data as reference.

---

## JDK 17 Top Contributors (2020-2021)

> Based on OpenJDK Census commits during JDK 17 development

| Rank | Contributor | Organization | Focus Area |
|------|-------------|--------------|------------|
| 1 | Thomas Schatzl | Oracle | G1 GC |
| 2 | Albert Mingkun Yang | Oracle | GC |
| 3 | Phil Race | Oracle | Graphics, Printing |
| 4 | Coleen Phillimore | Oracle | HotSpot VM |
| 5 | Magnus Ihse Bursie | Oracle | Build System |
| 6 | Kim Barrett | Oracle | GC |
| 7 | David Holmes | Oracle | Threading |
| 8 | Brian Burkhalter | Oracle | NIO |
| 9 | Erik Gahlin | Oracle | JFR |
| 10 | Claes Redestad | Oracle | Core Libs |

**Key Features**: Sealed Classes, Records, Pattern Matching, Strong Encapsulation

---

## JDK 11 Top Contributors (2017-2018)

> Based on OpenJDK Census commits during JDK 11 development

| Rank | Contributor | Organization | Focus Area |
|------|-------------|--------------|------------|
| 1 | David Katleman | Oracle | Build/Release |
| 2 | Jonathan Gibbons | Oracle | javac |
| 3 | Phil Race | Oracle | Graphics |
| 4 | Coleen Phillimore | Oracle | HotSpot |
| 5 | Thomas Schatzl | Oracle | G1 GC |
| 6 | Magnus Ihse Bursie | Oracle | Build System |
| 7 | Kim Barrett | Oracle | GC |
| 8 | Alan Bateman | Oracle | Core Libs |
| 9 | Chris Hegarty | Oracle | Core Libs |
| 10 | Mandy Chung | Oracle | Module System |

**Key Features**: HTTP Client, ZGC (Experimental), Epsilon GC, Flight Recorder

---

## JDK 8 Top Contributors (2011-2014)

> Based on OpenJDK Census commits during JDK 8 development

| Rank | Contributor | Organization | Focus Area |
|------|-------------|--------------|------------|
| 1 | Brian Goetz | Oracle | Lambda, Streams |
| 2 | Paul Sandoz | Oracle | Streams, Lambda |
| 3 | David Holmes | Oracle | Concurrency |
| 4 | Coleen Phillimore | Oracle | HotSpot |
| 5 | Phil Race | Oracle | Graphics |
| 6 | Joe Darcy | Oracle | Core Libs |
| 7 | Stuart Marks | Oracle | Streams |
| 8 | Maurizio Cimadamore | Oracle | Lambda |
| 9 | John Rose | Oracle | Lambda, InvokeDynamic |
| 10 | Aleksey Shipilev | Red Hat (当时；现 Amazon) | GC, Performance |

**Key Features**: Lambda Expressions, Stream API, Date/Time API, Nashorn

---

## Data Sources

**For JDK 8/11/17**:
- [OpenJDK Census](https://openjdk.org/census) - Official commit statistics
- Git history from Mercurial repositories (pre-2021)

**For JDK 21+**:
- [GitHub Integrated PRs](https://github.com/openjdk/jdk/pulls?q=is%3Apr+label%3Aintegrated+is%3Aclosed)

**Why the difference?**
- OpenJDK used Mercurial before 2021
- GitHub migration happened in 2021
- Committer email (`@openjdk.org`) doesn't reflect organization

---

## Related Pages

- [JDK 26 Top Contributors](jdk26-top-contributors.md) - Latest version
- [JDK 25 Top Contributors](jdk25-top-contributors.md)
- [JDK 21 Top Contributors](jdk21-top-contributors.md)
- [By Organization](../../contributors/stats/by-org.md)
- [OpenJDK Census](https://openjdk.org/census)

**Last Updated**: 2026-03-21
