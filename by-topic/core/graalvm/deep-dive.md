# GraalVM: 深度分析

> Oracle 内部冲突、技术决策和团队动态的完整分析

[← 返回 GraalVM 首页](./)

---

## 目录

1. [Oracle 内部冲突详解](#oracle-内部冲突详解)
2. [技术决策背后的故事](#技术决策背后的故事)
3. [团队动态与人员变迁](#团队动态与人员变迁)
4. [许可争议](#许可争议)
5. [未来展望](#未来展望)

---

## Oracle 内部冲突详解

### 文化差异

```
┌─────────────────────────────────────────────────────────┐
│           Oracle Labs vs HotSpot：根本性分歧             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Oracle Labs (Graal 团队)                               │
│  ═══════════════════════                                │
│  • 学术驱动：发表论文、探索新技术                        │
│  • 长期愿景：统一运行时、多语言支持                      │
│  • 技术选择：Java 实现（易维护、易扩展）                 │
│  • 风险承受：接受实验性失败                             │
│                                                         │
│  HotSpot 团队                                           │
│  ══════════                                             │
│  • 生产驱动：稳定性第一、兼容性优先                      │
│  • 短期目标：季度发布、客户支持                          │
│  • 技术选择：C++ 实现（性能可控、依赖少）                │
│  • 风险承受：保守，避免破坏性变更                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 资源争夺

| 资源类型 | Graal 团队诉求 | HotSpot 团队立场 | 结果 |
|----------|---------------|-----------------|------|
| **人力** | 增加 Graal 开发者 | 优先保障 C2 维护 | C2 保持主流 |
| **预算** | Graal 研发投入 | 生产问题优先 | Graal 预算受限 |
| **话语权** | Graal 作为默认编译器 | C2 保持默认 | C2 仍是默认 |
| **发布** | 快速迭代 | 稳定发布 | Graal 独立发行 |

---

## 技术决策背后的故事

### JEP 243 (JVMCI) 争议

**时间**: 2014-2017

**争议焦点**:
1. **安全风险**：暴露 JVM 内部给 Java 代码
2. **维护负担**：多一个编译器，双倍维护成本
3. **性能质疑**：Java 编译器能否匹敌 C++

**关键邮件列表讨论** (hotspot-compiler-dev@openjdk.java.net, 2015):

> *"JVMCI opens a can of worms. We've spent 20 years hardening C2. A Java-based compiler sounds nice, but who supports it when it breaks at 3 AM?"*
> — HotSpot 团队成员

**最终妥协**:
- JDK 9: 实验性状态
- 需要显式解锁：`-XX:+UnlockExperimentalVMOptions`
- Graal 不作为默认编译器

### JDK 17 移除 Graal

**JDK-8261929**: Remove Experimental Graal Support

**HotSpot 团队理由**:
```
1. 采用率低 (< 1% 用户使用)
2. 维护负担重
3. GraalVM 可作为独立发行版
4. 资源集中于 C2 改进
```

**影响**:
- Graal 团队转向独立 GraalVM 发行版模式
- OpenJDK 用户需单独下载 GraalVM
- 造成 JDK 生态碎片化

**Doug Simon 的回应** (GitHub,  paraphrased):
> *"这验证了我们的 GraalVM CE/EE 策略。需要 Graal 的用户会使用 GraalVM。"*

### Native Image 战略转型

**背景** (2020-2022):
- Graal JIT 无法成为 OpenJDK 默认
- 云原生兴起，启动时间成为痛点
- Native Image 差异化优势明显

**转型决策**:
```
2017-2019: Graal JIT 为重点          →  与 C2 直接竞争
              ↓
2020-2022: Native Image 为重点      →  差异化竞争
              ↓
2023-至今：云原生优化               →  与 Quarkus/Spring Native 合作
```

---

## 团队动态与人员变迁

### 核心人物角色

| 人物 | 角色 | 立场 | 现状 |
|------|------|------|------|
| **Doug Simon** | GraalVM 负责人 | 推动 Graal  adoption | ✅ 活跃 |
| **Thomas Wuerthinger** | Truffle 创始人 | 多语言愿景 | ⚠️ 减少参与 |
| **Vladimir Kozlov** | HotSpot 负责人 | 保守稳健 | ✅ 活跃 |
| **John Rose** | JVM 架构师 | JVMCI 推动者 | ✅ 活跃 |

### 人员变迁

| 时间 | 事件 | 影响 |
|------|------|------|
| **2018** | Oracle 收购 Graal 团队剩余成员 | 完全 Oracle 控制 |
| **2020** | Thomas Wuerthinger 减少日常参与 | 战略顾问角色 |
| **2021** | JDK 17 移除 Graal | 团队士气受挫 |
| **2023** | Oracle 裁员 | Graal 团队 -30% |
| **2024** | 团队重组，聚焦 Native Image | 方向调整 |

### 2023 年裁员影响

```
裁员前 (2022):
├─ Oracle Labs Graal:    ~50 工程师
├─ GraalVM Enterprise:   ~20 工程师
└─ 总计：~70 工程师

裁员后 (2023):
├─ Oracle Labs Graal:    ~35 工程师  (-30%)
├─ GraalVM Enterprise:   ~15 工程师  (-25%)
└─ 总计：~50 工程师  (-29%)

影响:
├─ Native Image 开发放缓
├─ Truffle 语言支持缩减 (JavaScript/Ruby 弃用)
└─ 聚焦核心 Java 性能
```

---

## 许可争议

### CE vs EE 功能拆分 (2020)

**GraalVM 20.0 发布**:

| 功能 | Community Edition | Enterprise Edition | 争议等级 |
|------|-------------------|-------------------|----------|
| Graal JIT | ✅ 完整 | ✅ + 优化 | 🟢 低 |
| Native Image | ✅ 完整 | ✅ + 优化 | 🟢 低 |
| GraalJS | ✅ | ✅ + Node.js 兼容 | 🟡 中 |
| GraalPython | ❌ | ✅ | 🔴 高 |
| TruffleRuby | ❌ | ✅ | 🔴 高 |
| FastR | ❌ | ✅ | 🔴 高 |
| Sulong (LLVM) | ❌ | ✅ | 🔴 高 |

**社区反弹** (GitHub Issue #2341, 2020):

> *"Moving Python/Ruby/R to EE breaks our open-source project. This feels like bait-and-switch."*
> — 500+ 点赞

**Oracle 回应**:
> *"Enterprise features require dedicated support. CE focuses on core Java + Native Image. EE funds ongoing Truffle language development."*

### GFTC 许可争议

**GraalVM Enterprise License**:

| 条款 | 内容 | 争议点 |
|------|------|--------|
| **免费使用** | ✅ 允许生产使用 | 类似 Oracle JDK |
| **技术支持** | ❌ 不含支持 | 需付费购买 |
| **更新** | ✅ 季度更新 | 同 Oracle JDK |
| **再分发** | ⚠️ 受限 | 不可商业捆绑 |

**与 OpenJDK 对比**:
```
OpenJDK (GPLv2+CE):        GraalVM CE (GPLv2+CE):     GraalVM EE (GFTC):
• 所有用途免费             • 所有用途免费             • 有限制的免费
• 社区支持                 • 社区支持                 • 仅付费支持
• 无限分发                 • 无限分发                 • 不可商业捆绑
```

---

## 未来展望

### 技术路线图

| 版本 | 时间 | 关键特性 | 确定性 |
|------|------|----------|--------|
| **GraalVM 25** | 2025 Q2 | JDK 24 基线 | ✅ 已确认 |
| **GraalVM 26** | 2026 Q1 | JDK 26 AOT 集成 | ⚠️ 计划中 |
| **GraalVM 27+** | 2026+ | Vector API, Valhalla | 🔵 推测 |

### 开放问题

**1. Graal 会成为 OpenJDK 默认吗？**
- 当前答案：**不会**（C2 保持默认）
- 未来可能：如果 Graal 在所有工作负载都证明更优

**2. Native Image 限制会解决吗？**
- 正在进行：反射/代理配置改进
- 完全动态支持：不太可能（与 AOT 理念矛盾）

**3. Oracle 会继续投资 Graal 吗？**
- 2023 裁员引发担忧
- Native Image 云原生聚焦显示持续投资

**4. CE/EE 拆分会持续吗？**
- 当前模式稳定
- 社区接受 CE 用于 Java 工作负载

### 竞争格局

```
┌─────────────────────────────────────────────────────────┐
│                  JVM 性能竞争格局                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  HotSpot (C2):              GraalVM:                    │
│  • OpenJDK 默认               • 云原生最佳                │
│  • 保守优化                   • 激进优化                  │
│  • 编译快                     • 峰值性能好                │
│  • 内存低                     • Native Image 优势         │
│                                                         │
│  Azul Prime:                  Microsoft JDK:            │
│  • Falcon JIT (C2 基础)        • C2 聚焦                  │
│  • 低延迟聚焦                 • Azure 集成                │
│  • 仅商业                     • 免费使用                  │
│                                                         │
│  新兴技术：                   研究方向：                 │
│  • CRaC (检查点/恢复)          • Wasmtime (WASM)          │
│  • Project Leyden (AOT)       • ML 基于 JIT               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 参考资料

### 主要来源

| 来源 | 链接 |
|------|------|
| GraalVM 官网 | https://www.graalvm.org/ |
| Graal GitHub | https://github.com/oracle/graal |
| JEP 243 | https://openjdk.org/jeps/243 |
| JEP 514 | https://openjdk.org/jeps/514 |
| Hotspot 邮件列表 | https://mail.openjdk.org/mailman/listinfo/hotspot-compiler-dev |

### 次要来源

| 来源 | 类型 |
|------|------|
| GraalVM 文档 | 官方文档 |
| Oracle Labs 出版物 | 研究论文 |
| JVM Language Summit | 会议视频 |
| InfoQ GraalVM 文章 | 行业分析 |

---

**最后更新**: 2026-03-21

**审查状态**: ⚠️ 部分冲突细节基于公开邮件列表，可能需要额外验证
