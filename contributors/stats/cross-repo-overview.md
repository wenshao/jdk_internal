# OpenJDK 跨仓库贡献全景分析

> 基于 25 个仓库, 43,394 个 Integrated PRs 的完整数据

---

## 1. 数据规模

| 类别 | 仓库数 | PRs | 占比 |
|------|--------|-----|------|
| **主线开发** (openjdk/jdk) | 1 | 24,868 | 57.3% |
| **LTS 维护** (jdk17u/21u/11u/8u-dev) | 4 | 9,858 | 22.7% |
| **实验性项目** (valhalla, panama 等) | 10 | 4,976 | 11.5% |
| **工具** (jfx, jmc) | 2 | 2,408 | 5.5% |
| **非 LTS 更新** (jdk22u/23u/24u/25u) | 4 | 943 | 2.2% |
| **专用分支** (riscv-port, shenandoah) | 4 | 341 | 0.8% |
| **总计** | **25** | **43,394** | 100% |

---

## 2. 实验性项目组织主导关系

OpenJDK 的实验性项目呈现出明确的**组织分工**模式：

| 项目 | 主导组织 | 占比 | 核心贡献者 | PRs | 目标 |
|------|---------|------|-----------|-----|------|
| **[Valhalla](../../valhalla/contributors.md)** | [Oracle](../orgs/oracle.md) | 90% | TobiHartmann (331), MrSimms (322) | 2,082 | Value Types |
| **Panama-Foreign** | [Oracle](../orgs/oracle.md) | 97% | [mcimadamore](../../by-contributor/profiles/maurizio-cimadamore.md) (312) | 817 | FFM API |
| **Babylon** | [Oracle](../orgs/oracle.md) | 100% | grfrost (428) | 910 | GPU/Code Reflection |
| **Loom** | [Oracle](../orgs/oracle.md) | 69% | [coleenp](../../by-contributor/profiles/coleen-phillimore.md) (33) | 146 | Virtual Threads |
| **Shenandoah** | [Amazon](../orgs/amazon.md) | 99% | earthling-amzn (337) | 482 | Low-pause GC |
| **Lilliput** | [Red Hat](../orgs/redhat.md) | 72% | rkennke (92, 现 [Datadog](../orgs/datadog.md)) | 147 | Compact Headers |
| **Leyden** | [Amazon](../orgs/amazon.md) | 52% | [shipilev](../../by-contributor/profiles/aleksey-shipilev.md) (41) | 83 | 启动优化/AOT |
| **CRaC** | [Azul](../orgs/azul.md) | 81% | TimPushkin (75) | 251 | 检查点恢复 |
| **JFX** | [Oracle](../orgs/oracle.md) | 97% | kevinrushforth (297) | 1,782 | JavaFX GUI |
| **JMC** | [Datadog](../orgs/datadog.md) | 55% | thegreystone (165, Datadog) | 626 | Mission Control |

### 组织 → 项目领导力映射

```
Oracle      → Valhalla, Panama, Babylon, Loom, JFX (创新主导)
Amazon      → Shenandoah, Leyden (GC + 启动优化)
Red Hat     → Lilliput (内存优化)
Azul        → CRaC (检查点恢复)
SAP         → LTS 维护
Datadog     → JMC (监控工具) + Lilliput
```

---

## 3. 跨仓库贡献者

### Top 20 跨仓库贡献者 (活跃 5+ 仓库)

| 排名 | 贡献者 | 组织 | 活跃仓库数 | 总 PRs | 主要领域 |
|------|--------|------|-----------|--------|----------|
| 1 | [shipilev](../../by-contributor/profiles/aleksey-shipilev.md) | [Amazon](../orgs/amazon.md) | **14** | 1,335+ | Shenandoah, Leyden, LTS 维护 |
| 2 | [RealFYang](../../by-contributor/profiles/fei-yang.md) | [Huawei](../orgs/huawei.md) | **12** | 200+ | RISC-V, AArch64, LTS 维护 |
| 3 | earthling-amzn | [Amazon](../orgs/amazon.md) | **10** | 400+ | Shenandoah, LTS 维护 |
| 4 | [sendaoYan](../../by-contributor/profiles/sendaoyan.md) | [Alibaba](../orgs/alibaba.md) | **10** | 450+ | 全版本维护 |
| 5 | [RealCLanger](../../by-contributor/profiles/christoph-langer.md) | [SAP](../orgs/sap.md) | **9** | 355 | JMC, LTS 维护 |
| 6 | [jerboaa](https://github.com/jerboaa) | [Red Hat](../orgs/redhat.md) | **9** | 120+ | LTS 维护 |
| 7 | [TheRealMDoerr](../../by-contributor/profiles/martin-doerr.md) | [SAP](../orgs/sap.md) | **9** | 570 | PPC64, LTS 维护 |
| 8 | [tstuefe](../../by-contributor/profiles/thomas-stuefe.md) | [Red Hat](../orgs/redhat.md) | **9** | 280+ | Lilliput, Runtime |
| 9 | [MBaesken](../../by-contributor/profiles/matthias-baesken.md) | [SAP](../orgs/sap.md) | **8** | 991 | 构建, AIX, LTS 维护 |
| 10 | [reinrich](../../by-contributor/profiles/richard-reingruber.md) | [SAP](../orgs/sap.md) | **8** | 102+ | C2, LTS 维护 |
| 11 | [rwestrel](../../by-contributor/profiles/roland-westrelin.md) | [Red Hat](../orgs/redhat.md) | **8** | 230+ | C2, Valhalla |
| 12 | rkennke | [Red Hat](../orgs/redhat.md) | **8** | 150+ | Lilliput, Shenandoah, Loom |
| 13 | [gnu-andrew](https://github.com/gnu-andrew) | [Red Hat](../orgs/redhat.md) | **8** | 151+ | JDK 8/11 维护 |
| 14 | mrserb | [Oracle](../orgs/oracle.md) | **8** | 290+ | GUI, LTS 维护 |
| 15 | zifeihan | [Alibaba](../orgs/alibaba.md) | **8** | 100+ | RISC-V, LTS 维护 |

> **92 人** 活跃于 5 个以上仓库。shipilev (Amazon) 以 14 个仓库的覆盖度位居第一。

---

## 4. 组织全景对比

### 主线 + LTS + 实验性项目综合

| 组织 | 主线 | LTS 维护 | 实验性 | 工具 | 总计 | 特征 |
|------|------|---------|--------|------|------|------|
| [Oracle](../orgs/oracle.md) | 17,088 | — | ~3,100 | ~440 | 20,600+ | 全领域主导 |
| [SAP](../orgs/sap.md) | 999 | 5,264 | — | 34 | 6,297+ | LTS 维护 |
| [Amazon](../orgs/amazon.md) | 1,172 | 566 | 830+ | — | 2,568+ | Shenandoah + Leyden |
| [Red Hat](../orgs/redhat.md) | 584 | 770 | 140+ | — | 1,494+ | Lilliput + LTS |
| [Alibaba](../orgs/alibaba.md) | 448 | 559 | — | — | 1,007 | 主线 + LTS 均衡 |
| [IBM](../orgs/ibm.md) | 222 | — | 17+ | — | 239+ | s390x, Leyden |
| [Huawei](../orgs/huawei.md) | 156 | — | 10+ | — | 166+ | RISC-V 全版本 |
| [Azul](../orgs/azul.md) | 18 | — | 200+ | — | 218+ | CRaC 主导 |

---

## 5. Top 审查者 (主线)

| 排名 | 审查者 | 审查次数 | 组织 | 主要领域 |
|------|--------|---------|------|----------|
| 1 | dholmes-ora | 2,527 | [Oracle](../orgs/oracle.md) | HotSpot Runtime |
| 2 | [AlanBateman](../../by-contributor/profiles/alan-bateman.md) | 1,862 | [Oracle](../orgs/oracle.md) | 核心库, NIO |
| 3 | vnkozlov | 1,845 | [Oracle](../orgs/oracle.md) | C2 编译器 |
| 4 | [shipilev](../../by-contributor/profiles/aleksey-shipilev.md) | 1,606 | [Amazon](../orgs/amazon.md) | 性能, GC |
| 5 | tschatzl | 1,391 | [Oracle](../orgs/oracle.md) | G1 GC |
| 6 | [TobiHartmann](../../by-contributor/profiles/tobias-hartmann.md) | 1,314 | [Oracle](../orgs/oracle.md) | C2, Valhalla |
| 7 | prrace | 1,177 | [Oracle](../orgs/oracle.md) | 2D 图形 |
| 8 | [coleenp](../../by-contributor/profiles/coleen-phillimore.md) | 1,097 | [Oracle](../orgs/oracle.md) | 运行时, Loom |
| 9 | mrserb | 1,014 | [Oracle](../orgs/oracle.md) | GUI |
| 10 | erikj79 | 968 | [Oracle](../orgs/oracle.md) | 构建系统 |

---

## 6. 数据来源

- **25 个仓库 CSV**: `{repo}/all-integrated-prs.csv`
- **OpenJDK Census**: `scripts/.census-data.csv` (672 人)
- **Author→Org 映射**: `scripts/.author-org-mapping.json` (237 人)
- **采集时间**: 2026-03-24
- **采集工具**: `scripts/fetch-repo-prs.py`

---

> **文档版本**: 1.0
> **最后更新**: 2026-03-24
