# Xiaowei Lu (陆晓伟)

> ZGC 优化贡献者，Jade GC 论文作者，阿里巴巴

---
## 目录

1. [基本信息](#1-基本信息)
2. [学术贡献](#2-学术贡献)
3. [PR 列表](#3-pr-列表)
4. [关键贡献](#4-关键贡献)
5. [Dragonwell JDK 贡献](#5-dragonwell-jdk-贡献)
6. [职业时间线](#6-职业时间线)
7. [技术专长](#7-技术专长)
8. [数据来源](#8-数据来源)
9. [相关链接](#9-相关链接)

---


## 1. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Xiaowei Lu (陆晓伟) |
| **当前组织** | 阿里巴巴云 (Alibaba Cloud) |
| **位置** | 杭州，中国 |
| **邮箱** | lxw263044@alibaba-inc.com |
| **GitHub** | [@weixlu](https://github.com/weixlu) |
| **ORCID** | [0009-0001-6990-5081](https://orcid.org/0009-0001-6990-5081) |
| **OpenJDK** | Committer (xwlu) |
| **Integrated PRs** | [3](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Aweixlu+is%3Aclosed+label%3Aintegrated) |
| **主要领域** | ZGC, Jade GC, 垃圾回收器, 内存模型 |
| **活跃时间** | 2021 - 至今 |

> **数据来源**: [GitHub](https://github.com/weixlu), [ORCID](https://orcid.org/0009-0001-6990-5081), [OpenJDK JBS](https://bugs.openjdk.org/browse/JDK-8270347)

---

## 2. 学术贡献

### Jade GC 论文 (EuroSys 2024)

| 属性 | 值 |
|------|-----|
| **标题** | Jade: A High-throughput Concurrent Copying Garbage Collector |
| **会议** | EuroSys 2024 (ACM European Conference on Computer Systems) |
| **发表日期** | 2024-04-22 |
| **作者** | Mingyu Wu, Liang Mao, **Xiaowei Lu**, Yude Lin, Yifeng Jin, Zhe Li, Hongtao, Hao Tang, Denghui Dong, Haibo Chen, Binyu Zang |
| **机构** | Shanghai Jiao Tong University (IPADS), Alibaba Group |
| **链接** | [ACM DL](https://dl.acm.org/doi/10.1145/3627703.3650087), [PDF](https://dl.acm.org/doi/pdf/10.1145/3627703.3650087) |

**论文摘要**:
Jade 是一个高吞吐量的并发复制垃圾收集器，针对现代多核服务器环境设计。通过创新的并发复制算法和内存管理策略，Jade 在保持低延迟的同时显著提高了 GC 吞吐量。

---

## 3. PR 列表

| Issue | 标题 | 合入时间 |
|-------|------|----------|
| 8273112 | -Xloggc:<filename> should override -verbose:gc | 2021-04 |
| 8272138 | ZGC: Adopt relaxed ordering for self-healing | 2021-03 |
| 8270347 | ZGC: Adopt release-acquire ordering for forwarding table | 2021-02 |

---

## 4. 关键贡献

### ZGC 自愈宽松顺序优化 (JDK-8272138)

**问题**: ZGC 自愈操作使用过于严格的内存顺序，影响性能。

**解决方案**: 使用宽松的内存顺序：

```cpp
// 变更前: 使用强顺序
oop result = Atomic::cmpxchg(addr, expected, new_value);

// 变更后: 使用宽松顺序
oop result = Atomic::cmpxchg_relaxed(addr, expected, new_value);
```

**影响**: 提升 ZGC 自愈操作性能。

### ZGC 转发表访问顺序修复 (JDK-8270347)

**问题**: ZGC 转发表访问需要正确的内存顺序保证。

**解决方案**: 使用 release-acquire 顺序：

```cpp
// 变更后: 使用 release-acquire 顺序
ZForwardingEntry* entry = forwarding->find(addr);
if (entry != nullptr) {
  return Atomic::load_acquire(&entry->to());
}
```

**影响**: 确保 ZGC 在弱内存模型平台上的正确性。

### GC 日志覆盖修复 (JDK-8273112)

**问题**: `-Xloggc:<filename>` 不能正确覆盖 `-verbose:gc`。

**解决方案**: 修复日志选项优先级：

```cpp
// 变更后: -Xloggc 优先级高于 -verbose:gc
if (Arguments::has_xloggc()) {
  // 使用 -Xloggc 指定的文件
  gclog_file = new fileStream(Arguments::xloggc_file());
}
```

**影响**: 用户可以正确使用 `-Xloggc` 覆盖默认日志设置。

---

## 5. Dragonwell JDK 贡献

Xiaowei Lu 在阿里巴巴 Dragonwell JDK 项目中也有重要贡献：

### 活跃领域

| 领域 | 说明 |
|------|------|
| **ZGC MXBean** | 修复 ZGC 监控 bean 在类卸载时的暂停时间和计数收集问题 |
| **数组对齐** | 参与讨论紧凑对象头 (compact object headers) 的数组元素对齐放宽 |
| **RISC-V 架构** | 参与 RISC-V (riscv64) 架构的字段布局相关工作 |
| **ARM64 (aarch64)** | 参与 ARM64 平台的编译器相关问题 |

---

## 6. 职业时间线

| 年份 | 事件 | 详情 |
|------|------|------|
| **2021** | OpenJDK 首次贡献 | ZGC 内存顺序优化 (JDK-8270347, JDK-8272138) |
| **2021** | GC 日志修复 | JDK-8273112: -Xloggc 覆盖 -verbose:gc |
| **2024** | EuroSys 2024 论文 | 发表 Jade GC 论文 |
| **2024** | Dragonwell 贡献 | 继续为 Dragonwell JDK 做出贡献 |

---

## 7. 技术专长

- **ZGC (Z Garbage Collector)**: 内存顺序优化、自愈机制
- **Jade GC**: 高吞吐量并发复制垃圾收集器
- **内存模型**: release-acquire 语义、内存屏障
- **跨平台**: RISC-V、ARM64 (aarch64) 架构支持
- **Dragonwell JDK**: 阿里巴巴 OpenJDK 发行版

---

## 8. 数据来源

- **统计方法**: GitHub PR search `repo:openjdk/jdk author:weixlu type:pr label:integrated`
- **统计时间**: 2026-03-20
- **论文**: EuroSys 2024 Proceedings
- **ORCID**: Open Researcher and Contributor ID

---

## 9. 相关链接

| 类型 | 链接 |
|------|------|
| **GitHub** | [@weixlu](https://github.com/weixlu) |
| **ORCID** | [0009-0001-6990-5081](https://orcid.org/0009-0001-6990-5081) |
| **OpenJDK PRs** | [GitHub Search](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Aweixlu) |
| **Jade GC Paper** | [ACM DL](https://dl.acm.org/doi/10.1145/3627703.3650087) |
| **Jade GC PDF** | [PDF](https://dl.acm.org/doi/pdf/10.1145/3627703.3650087) |

---

> **文档版本**: 2.0
> **最后更新**: 2026-03-20
> **更新内容**:
> - 添加中文名 (陆晓伟)
> - 添加邮箱: lxw263044@alibaba-inc.com
> - 添加位置: 杭州，阿里巴巴云
> - 添加 ORCID: 0009-0001-6990-5081
> - 添加 EuroSys 2024 Jade GC 论文信息
> - 添加 Dragonwell JDK 贡献详情
> - 添加职业时间线
> - 添加技术专长列表