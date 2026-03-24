# OpenJDK Mailing List Activity Statistics

**Data source:** [mail.openjdk.org/pipermail](https://mail.openjdk.org/pipermail/)
**Period:** March 2025 -- February 2026 (12 months)
**Scraped:** 2026-03-24

---

## All Tracked Lists by Activity Level

| Rank | Mailing List | 12-Month Messages | Avg/Month | Activity Level |
|------|-------------|------------------:|----------:|----------------|
| 1 | [core-libs-dev](https://mail.openjdk.org/pipermail/core-libs-dev/) | 18,884 | 1,574 | Very High |
| 2 | [hotspot-dev](https://mail.openjdk.org/pipermail/hotspot-dev/) | 17,337 | 1,445 | Very High |
| 3 | [security-dev](https://mail.openjdk.org/pipermail/security-dev/) | 6,443 | 537 | High |
| 4 | [valhalla-dev](https://mail.openjdk.org/pipermail/valhalla-dev/) | 5,806 | 484 | High |
| 5 | [shenandoah-dev](https://mail.openjdk.org/pipermail/shenandoah-dev/) | 3,745 | 312 | Medium-High |
| 6 | [compiler-dev](https://mail.openjdk.org/pipermail/compiler-dev/) | 3,336 | 278 | Medium-High |
| 7 | [leyden-dev](https://mail.openjdk.org/pipermail/leyden-dev/) | 1,376 | 115 | Medium |
| 8 | [jdk-dev](https://mail.openjdk.org/pipermail/jdk-dev/) | 1,127 | 94 | Medium |
| 9 | [loom-dev](https://mail.openjdk.org/pipermail/loom-dev/) | 891 | 74 | Low-Medium |
| 10 | [amber-dev](https://mail.openjdk.org/pipermail/amber-dev/) | 432 | 36 | Low |
| 11 | [panama-dev](https://mail.openjdk.org/pipermail/panama-dev/) | 340 | 28 | Low |
| 12 | [lilliput-dev](https://mail.openjdk.org/pipermail/lilliput-dev/) | 84 | 7 | Very Low |

**Total across all 12 lists:** ~59,800 messages over 12 months (~4,983/month).

---

## Monthly Trends for Top 5 Lists

Message counts by month for the five most active lists:

| Month | core-libs-dev | hotspot-dev | security-dev | valhalla-dev | shenandoah-dev |
|-------|-------------:|------------:|-------------:|-------------:|---------------:|
| 2025-03 | 1,174 | 1,122 | 562 | 181 | 409 |
| 2025-04 | 2,393 | 1,446 | 650 | 217 | 327 |
| 2025-05 | 2,717 | 1,738 | 742 | 202 | 144 |
| 2025-06 | 1,194 | 1,583 | 445 | 140 | 674 |
| 2025-07 | 1,351 | 1,321 | 320 | 230 | 341 |
| 2025-08 | 1,309 | 1,469 | 626 | 164 | 74 |
| 2025-09 | 1,727 | 1,916 | 656 | 575 | 345 |
| 2025-10 | 1,683 | 1,787 | 754 | 513 | 358 |
| 2025-11 | 1,523 | 1,302 | 573 | 437 | 337 |
| 2025-12 | 1,067 | 1,089 | 564 | 749 | 371 |
| 2026-01 | 1,529 | 1,170 | 551 | 1,170 | 365 |
| 2026-02 | 1,218 | 1,394 | 311 | 1,228 | 372 |

### Key Observations

**core-libs-dev** is the single most active list, peaking at 2,717 messages in May 2025. This reflects the breadth of core library work -- java.lang, java.util, java.io, and the many APIs that touch every Java developer. Activity dipped in Dec 2025 (holiday effect) but stays consistently above 1,000 msgs/month.

**hotspot-dev** runs a close second with very consistent volume (1,100--1,900/month). The JVM runtime, GC, and compiler teams generate a steady stream of review-driven discussion here.

**valhalla-dev** shows a dramatic ramp-up: from ~140--230 msgs/month in mid-2025 to 1,170--1,228 in Jan--Feb 2026. This strongly correlates with the push toward value types integration for JDK 25/26 and the Valhalla JEPs progressing through the pipeline.

**security-dev** maintains steady high volume (300--750/month), reflecting ongoing TLS/crypto work, vulnerability response, and certificate management changes.

**shenandoah-dev** has an unusual spike in June 2025 (674 messages, vs its normal ~340) and a quiet August 2025 (74). The GC's development rhythm is bursty, tied to specific development milestones.

---

## Correlation with PR Activity

The mailing list activity correlates with, but is not identical to, PR volume in the [openjdk/jdk](https://github.com/openjdk/jdk) repository:

| Area | Mailing List | Relationship to PRs |
|------|-------------|-------------------|
| Core libraries | core-libs-dev | **Strongest correlation.** Most PRs touching `src/java.base` generate review discussion on-list. The May 2025 spike (2,717 msgs) aligns with heavy PR activity for JDK 25 feature development. |
| HotSpot JVM | hotspot-dev | **Strong correlation.** HotSpot PRs (compiler, GC, runtime) are heavily discussed. The list also carries design discussion that precedes PRs. |
| Security | security-dev | **Moderate correlation.** Some security PRs are routine backports with minimal list discussion; major crypto changes generate significant thread volume. |
| Valhalla | valhalla-dev | **Leading indicator.** List activity surges before PRs land -- heavy spec/design discussion in Dec 2025--Feb 2026 foreshadows upcoming integration PRs. |
| Compiler | compiler-dev | **Moderate correlation.** javac PRs get less on-list review than HotSpot, but language-level changes (patterns, generics) drive extended discussion. |
| Shenandoah | shenandoah-dev | **Tightly coupled.** Most messages are automated PR notifications plus code review discussion, making the list a near-mirror of PR activity. |
| Leyden | leyden-dev | **Leading indicator.** Heavy design discussion (peak: 195 in Apr 2025) precedes integration work for CDS/AOT features. Activity declining in late 2025 suggests features are stabilizing. |
| Loom | loom-dev | **Declining.** Virtual threads shipped in JDK 21; list has shifted from design to maintenance-level discussion (~70--100 msgs/month). |
| Amber | amber-dev | **Low but significant.** Language feature design happens in bursts; a month with 89 messages (Jan 2026) may represent a single pivotal spec debate. |
| Panama | panama-dev | **Low, stabilizing.** FFM API shipped in JDK 22; remaining activity focuses on refinements and edge cases. |
| Lilliput | lilliput-dev | **Near dormant.** Compact headers integrated; only a handful of follow-up messages per month. |

### Summary

The two dominant lists -- **core-libs-dev** and **hotspot-dev** -- together account for 60% of all tracked mailing list traffic. They are the primary venues where code review discussion happens for the main JDK repository.

The most notable trend is **valhalla-dev's 6x growth** from mid-2025 to early 2026, signaling that value types are the most actively developed feature in current OpenJDK. Meanwhile, **loom-dev** and **panama-dev** have wound down as their features have shipped, and **leyden-dev** shows signs of transitioning from design to stabilization.

---

*Raw data: [`scripts/.mailing-list-stats.json`](../../scripts/.mailing-list-stats.json)*
