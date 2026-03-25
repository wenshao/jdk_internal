# 回归 Bug 分析

> 863 个标记为 regression 的 PR

---

## 1. 按引入版本

| 版本 | 回归数 | 占该版本 PR % |
|------|--------|-------------|
| JDK 25 | 146 | 4.4% |
| JDK 19 | 128 | 4.6% |
| JDK 23 | 125 | 4.4% |
| JDK 21 | 124 | 4.2% |
| JDK 17 | 68 | 2.3% |
| JDK 26 | 66 | 2.6% |
| JDK 18 | 65 | 4.7% |
| JDK 24 | 56 | 3.3% |
| JDK 20 | 39 | 2.9% |
| JDK 16 | 25 | 1.5% |
| JDK 22 | 21 | 1.5% |

## 2. 按模块 (Top 15)

| 模块 | 回归数 |
|------|--------|
| compiler/c2 | 121 |
| test | 83 |
| client | 74 |
| hotspot | 64 |
| arch/x86 | 57 |
| tools | 44 |
| core-libs/java.io | 43 |
| core-libs | 40 |
| core-libs/java.net | 37 |
| compiler | 35 |
| build | 31 |
| runtime/threading | 30 |
| security | 19 |
| compiler/jvmci | 17 |
| arch/aarch64 | 17 |

## 3. 按组织 (引入回归)

| 组织 | 回归数 | 该组织总 PR | 回归率 |
|------|--------|-----------|--------|
| Oracle | 597 | 17088 | 3.5% |
| Amazon | 43 | 1172 | 3.7% |
| SAP | 11 | 999 | 1.1% |
| Red Hat | 41 | 584 | 7.0% |
| Alibaba | 8 | 388 | 2.1% |
| IBM | 8 | 222 | 3.6% |
| Tencent | 5 | 223 | 2.2% |
| Intel | 26 | 190 | 13.7% |

## 4. 回归严重程度

| 优先级 | 数量 |
|--------|------|
| P1 | 31 |
| P2 | 237 |
| P3 | 418 |
| P4 | 172 |
| P5 | 5 |

## 5. 回归修复速度

| 指标 | 值 |
|------|-----|
| 平均修复天数 | 8.9 |
| 中位数 | 2 |
| 1天内修复 | 347 (40%) |

## 6. 最近回归 (2025-2026)

| Bug ID | 标题 | Author | 组织 | 优先级 | 版本 |
|--------|------|--------|------|--------|------|
| [8352728](../../by-pr/8352/8352728.md) | InternalError loading java.security due t | franferrax |  | P3 | JDK 26 |
| [8352728](../../by-pr/8352/8352728.md) | InternalError loading java.security due t | franferrax |  | P3 | JDK 25 |
| [8369150](../../by-pr/8369/8369150.md) | NMethodRelocationTest fails when JVMTI ev | chadrako | Amazon | P3 | JDK 26 |
| [8371603](../../by-pr/8371/8371603.md) | C2: Missing Ideal optimizations for load  | XiaohongGong | ARM | P3 | JDK 26 |
| [8371603](../../by-pr/8371/8371603.md) | C2: Missing Ideal optimizations for load  | XiaohongGong | ARM | P3 | JDK 26 |
| [8371046](../../by-pr/8371/8371046.md) | Segfault in compiler/whitebox/StressNMeth | chadrako | Amazon | P4 | JDK 26 |
| [8372757](../../by-pr/8372/8372757.md) | MacOS; Accessibility: Crash in [MenuAcces | azuev-java | Oracle | P3 | JDK 26 |
| [8372756](../../by-pr/8372/8372756.md) | Mouse additional buttons and horizontal s | azvegint | Oracle | P3 | JDK 26 |
| [8373046](../../by-pr/8373/8373046.md) | Method::get_c2i_unverified_entry() and ge | ashu-mehra | IBM | P4 | JDK 26 |
| [8371306](../../by-pr/8371/8371306.md) | JDK-8367002 behavior might not match exis | dean-long | Oracle | P3 | JDK 26 |
| [8372703](../../by-pr/8372/8372703.md) | Test compiler/arguments/TestCodeEntryAlig | vpaprotsk | Intel | P3 | JDK 26 |
| [8372862](../../by-pr/8372/8372862.md) | AArch64: Fix GetAndSet-acquire costs afte | shipilev | Amazon | P4 | JDK 26 |
| [8371964](../../by-pr/8371/8371964.md) | C2 compilation asserts with "Unexpected l | merykitty | Oracle | P2 | JDK 26 |
| [8370766](../../by-pr/8370/8370766.md) | JVM crashes when running compiler/excepti | dean-long | Oracle | P3 | JDK 26 |
| [8372451](../../by-pr/8372/8372451.md) | C2 SuperWord: "endless loop" assert. Need | eme64 | Oracle | P3 | JDK 26 |
| [8371464](../../by-pr/8371/8371464.md) | C2: assert(no_dead_loop) failed: dead loo | rwestrel | Red Hat | P3 | JDK 26 |
| [8372708](../../by-pr/8372/8372708.md) | Javadoc ignores "-locale" and uses defaul | hns | Oracle | P3 | JDK 26 |
| [8372461](../../by-pr/8372/8372461.md) | [IR Framework] Multiple test failures aft | chhagedorn | Oracle | P3 | JDK 26 |
| [8371740](../../by-pr/8371/8371740.md) | LinkedTransferQueue.poll() returns null  | viktorklang-ora | Oracle | P3 | JDK 26 |
| [8366888](../../by-pr/8366/8366888.md) | C2: incorrect assertion predicate with sh | rwestrel | Red Hat | P3 | JDK 26 |

---

> **统计时间**: 2026-03-25
