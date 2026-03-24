# 模块所有权分析 (详细版)

> 基于主线 24,868 PRs 的 author×module 交叉分析

---

## 模块 Top 贡献者

### test (2433 PRs)

| 贡献者 | PRs | 占比 |
|--------|-----|------|
| prsadhuk | 139 | 6% |
| shipilev | 85 | 3% |
| prrace | 83 | 3% |
| alexeysemenyukoracle | 81 | 3% |
| azvegint | 70 | 3% |

### hotspot (2203 PRs)

| 贡献者 | PRs | 占比 |
|--------|-----|------|
| albertnetymk | 311 | 14% |
| kimbarrett | 145 | 7% |
| coleenp | 138 | 6% |
| iklam | 104 | 5% |
| shipilev | 101 | 5% |

### arch/x86 (1387 PRs)

| 贡献者 | PRs | 占比 |
|--------|-----|------|
| shipilev | 73 | 5% |
| iklam | 59 | 4% |
| coleenp | 45 | 3% |
| jatin-bhateja | 39 | 3% |
| prrace | 34 | 2% |

### core-libs/java.io (1319 PRs)

| 贡献者 | PRs | 占比 |
|--------|-----|------|
| bplb | 215 | 16% |
| jaikiran | 54 | 4% |
| asotona | 47 | 4% |
| mrserb | 41 | 3% |
| magicus | 37 | 3% |

### client (1160 PRs)

| 贡献者 | PRs | 占比 |
|--------|-----|------|
| prsadhuk | 201 | 17% |
| prrace | 148 | 13% |
| mrserb | 119 | 10% |
| turbanoff | 55 | 5% |
| aivanov-jdk | 52 | 4% |

### core-libs (1065 PRs)

| 贡献者 | PRs | 占比 |
|--------|-----|------|
| liach | 87 | 8% |
| naotoj | 77 | 7% |
| jddarcy | 70 | 7% |
| minborg | 63 | 6% |
| justin-curtis-lu | 58 | 5% |

### compiler/c2 (1040 PRs)

| 贡献者 | PRs | 占比 |
|--------|-----|------|
| rwestrel | 153 | 15% |
| eme64 | 143 | 14% |
| chhagedorn | 83 | 8% |
| robcasloz | 70 | 7% |
| tobiasholenstein | 52 | 5% |

### build (1021 PRs)

| 贡献者 | PRs | 占比 |
|--------|-----|------|
| magicus | 173 | 17% |
| shipilev | 82 | 8% |
| MBaesken | 62 | 6% |
| vidmik | 37 | 4% |
| jddarcy | 36 | 4% |

### core-libs/java.net (941 PRs)

| 贡献者 | PRs | 占比 |
|--------|-----|------|
| dfuch | 111 | 12% |
| jaikiran | 77 | 8% |
| djelinski | 45 | 5% |
| vy | 41 | 4% |
| wangweij | 32 | 3% |

### tools (919 PRs)

| 贡献者 | PRs | 占比 |
|--------|-----|------|
| lahodaj | 171 | 19% |
| hns | 81 | 9% |
| alexeysemenyukoracle | 77 | 8% |
| archiecobbs | 54 | 6% |
| vicente-romero-oracle | 48 | 5% |

### runtime/threading (909 PRs)

| 贡献者 | PRs | 占比 |
|--------|-----|------|
| AlanBateman | 70 | 8% |
| plummercj | 64 | 7% |
| dholmes-ora | 53 | 6% |
| coleenp | 48 | 5% |
| dcubed-ojdk | 42 | 5% |

### gc (683 PRs)

| 贡献者 | PRs | 占比 |
|--------|-----|------|
| albertnetymk | 99 | 14% |
| tschatzl | 69 | 10% |
| earthling-amzn | 46 | 7% |
| shipilev | 34 | 5% |
| kimbarrett | 29 | 4% |

### compiler (631 PRs)

| 贡献者 | PRs | 占比 |
|--------|-----|------|
| shipilev | 38 | 6% |
| lahodaj | 23 | 4% |
| iignatev | 21 | 3% |
| DamonFool | 20 | 3% |
| magicus | 20 | 3% |

### gc/g1 (624 PRs)

| 贡献者 | PRs | 占比 |
|--------|-----|------|
| tschatzl | 266 | 43% |
| albertnetymk | 153 | 25% |
| walulyai | 58 | 9% |
| Hamlin-Li | 43 | 7% |
| kstefanj | 13 | 2% |

### security (539 PRs)

| 贡献者 | PRs | 占比 |
|--------|-----|------|
| wangweij | 108 | 20% |
| XueleiFan | 44 | 8% |
| valeriepeng | 41 | 8% |
| seanjmullan | 35 | 6% |
| rhalade | 32 | 6% |

### runtime/serviceability (493 PRs)

| 贡献者 | PRs | 占比 |
|--------|-----|------|
| plummercj | 78 | 16% |
| sspitsyn | 67 | 14% |
| alexmenkov | 48 | 10% |
| lmesnik | 47 | 10% |
| kevinjwalls | 38 | 8% |

### runtime/jfr (482 PRs)

| 贡献者 | PRs | 占比 |
|--------|-----|------|
| egahlin | 251 | 52% |
| mgronlun | 62 | 13% |
| aivanov-jdk | 18 | 4% |
| shipilev | 13 | 3% |
| MBaesken | 12 | 2% |

### arch/riscv (384 PRs)

| 贡献者 | PRs | 占比 |
|--------|-----|------|
| Hamlin-Li | 85 | 22% |
| RealFYang | 59 | 15% |
| DingliZhang | 45 | 12% |
| robehn | 44 | 11% |
| zifeihan | 43 | 11% |

### gc/shenandoah (363 PRs)

| 贡献者 | PRs | 占比 |
|--------|-----|------|
| zhengyu123 | 91 | 25% |
| shipilev | 77 | 21% |
| earthling-amzn | 68 | 19% |
| rkennke | 36 | 10% |
| pengxiaolong | 20 | 6% |

### arch/aarch64 (349 PRs)

| 贡献者 | PRs | 占比 |
|--------|-----|------|
| theRealAph | 29 | 8% |
| shqking | 17 | 5% |
| nick-arm | 16 | 5% |
| eastig | 16 | 5% |
| e1iu | 15 | 4% |

## 贡献者专业化

Top 30 贡献者的模块集中度：

| 贡献者 | 总 PRs | 主要模块 | 集中度 |
|--------|--------|---------|--------|
| shipilev | 772 | hotspot (101) | 13% |
| albertnetymk | 706 | hotspot (311) | 44% |
| tschatzl | 522 | gc/g1 (266) | 51% |
| iklam | 409 | runtime/cds (127) | 31% |
| MBaesken | 406 | build (62) | 15% |
| prsadhuk | 394 | client (201) | 51% |
| coleenp | 386 | hotspot (138) | 36% |
| bplb | 341 | core-libs/java.io (215) | 63% |
| magicus | 335 | build (173) | 52% |
| kimbarrett | 323 | hotspot (145) | 45% |
| prrace | 303 | client (148) | 49% |
| egahlin | 302 | runtime/jfr (251) | 83% |
| lahodaj | 297 | tools (171) | 58% |
| jaikiran | 293 | core-libs/java.net (77) | 26% |
| dholmes-ora | 281 | hotspot (76) | 27% |
| dcubed-ojdk | 278 | test (65) | 23% |
| turbanoff | 272 | client (55) | 20% |
| tstuefe | 272 | runtime/nmt (43) | 16% |
| plummercj | 267 | runtime/serviceability (78) | 29% |
| mrserb | 261 | client (119) | 46% |
| naotoj | 257 | core-libs (77) | 30% |
| jddarcy | 238 | core-libs (70) | 29% |
| lmesnik | 230 | test (58) | 25% |
| cl4es | 221 | core-libs (57) | 26% |
| liach | 220 | core-libs (87) | 40% |
| alexeysemenyukoracle | 218 | test (81) | 37% |
| rwestrel | 216 | compiler/c2 (153) | 71% |
| eme64 | 215 | compiler/c2 (143) | 67% |
| justin-curtis-lu | 209 | core-libs (58) | 28% |
| stefank | 196 | gc/zgc (52) | 27% |

---

> **统计时间**: 2026-03-24
