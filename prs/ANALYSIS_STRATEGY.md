# JDK 26 PR 分析策略

> 如何高效分析 2000+ PR 并生成有价值的报告

---

## 1. 数据获取

### 使用 GitHub API

```bash
# 获取所有 JDK 26 PR
gh pr list --repo openjdk/jdk --state merged \
  --limit 3000 --json number,title,author,labels,additions,deletions,changedFiles \
  --search "merged:>=2024-09-01 base:master" > jdk26-prs.json
```

### 或使用 Git 日志

```bash
# 从 JDK 源码获取 commit 信息
git log --since="2024-09-01" --until="2025-03-01" \
  --pretty=format:"%H|%s|%an|%ae" > jdk26-commits.csv
```

---

## 2. 分类维度

### 按组件分类

| 组件 | 关键词 | 预估 PR 数 | 优先级 |
|------|--------|-----------|--------|
| GC | G1, ZGC, Shenandoah, Parallel | ~150 | ⭐⭐⭐ |
| 编译器 | C2, C1, JIT, Graal | ~200 | ⭐⭐⭐ |
| 网络 | HttpClient, HTTP/2, HTTP/3, QUIC | ~100 | ⭐⭐⭐ |
| 安全 | crypto, TLS, SSL, signature | ~80 | ⭐⭐⭐ |
| 核心 | java.lang, java.util, reflect | ~200 | ⭐⭐ |
| 并发 | Thread, VirtualThread, lock | ~100 | ⭐⭐⭐ |
| 启动 | CDS, AOT, class loading | ~50 | ⭐⭐ |
| JFR | JFR, event, monitoring | ~40 | ⭐⭐ |
| 构建 | build, make, configure | ~100 | ⭐ |
| 测试 | test, jtreg | ~500 | ⭐ |

### 按影响分类

| 级别 | 定义 | PR 数 | 处理方式 |
|------|------|-------|----------|
| P1 | 严重 bug、安全漏洞 | ~20 | 深度分析 |
| P2 | 重要功能、性能优化 | ~100 | 详细分析 |
| P3 | 一般改进 | ~300 | 简要分析 |
| P4 | 小修复、清理 | ~1600 | 统计摘要 |

---

## 3. 自动化脚本

### PR 分类脚本

```python
#!/usr/bin/env python3
# pr_classifier.py - JDK PR 分类器

import json
import re
from collections import defaultdict

# 组件关键词映射
COMPONENT_KEYWORDS = {
    'gc': ['G1', 'ZGC', 'Shenandoah', 'ParallelGC', 'SerialGC', 'garbage'],
    'compiler': ['C2', 'C1', 'JIT', 'compiler', 'intrinsic', 'optimize'],
    'network': ['HttpClient', 'HTTP/2', 'HTTP/3', 'QUIC', 'WebSocket'],
    'security': ['crypto', 'TLS', 'SSL', 'signature', 'key', 'cipher'],
    'core': ['java.lang', 'java.util', 'reflect', 'String', 'Object'],
    'concurrency': ['Thread', 'VirtualThread', 'lock', 'concurrent', 'atomic'],
    'jfr': ['JFR', 'Flight Recorder', 'event', 'monitoring'],
}

def classify_pr(title, body=''):
    """根据标题和内容分类 PR"""
    text = f"{title} {body}".lower()
    
    for component, keywords in COMPONENT_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in text:
                return component
    
    return 'other'

def analyze_prs(prs_file):
    """分析 PR 列表"""
    with open(prs_file) as f:
        prs = json.load(f)
    
    # 按组件分组
    by_component = defaultdict(list)
    for pr in prs:
        component = classify_pr(pr['title'])
        by_component[component].append(pr)
    
    # 按作者分组
    by_author = defaultdict(list)
    for pr in prs:
        by_author[pr['author']['login']].append(pr)
    
    # 生成报告
    print(f"总 PR 数: {len(prs)}")
    print("\n按组件分布:")
    for component, pr_list in sorted(by_component.items(), key=lambda x: -len(x[1])):
        print(f"  {component}: {len(pr_list)}")
    
    print("\nTop 20 贡献者:")
    for author, pr_list in sorted(by_author.items(), key=lambda x: -len(x[1]))[:20]:
        print(f"  {author}: {len(pr_list)} PRs")

if __name__ == '__main__':
    analyze_prs('jdk26-prs.json')
```

### 报告生成脚本

```python
#!/usr/bin/env python3
# report_generator.py - 生成 PR 分析报告

import json
from datetime import datetime

TEMPLATE = '''# {component} PR 分析

> 统计时间: {date}
> PR 数量: {count}

---

## 概览

| 指标 | 值 |
|------|-----|
| 总 PR 数 | {count} |
| 新增代码行 | {additions} |
| 删除代码行 | {deletions} |
| 修改文件数 | {files} |

## 重要 PR 列表

{pr_list}

## 贡献者

{contributors}
'''

def generate_report(component, prs):
    """生成组件报告"""
    # 计算统计
    additions = sum(p.get('additions', 0) for p in prs)
    deletions = sum(p.get('deletions', 0) for p in prs)
    files = sum(p.get('changedFiles', 0) for p in prs)
    
    # 生成 PR 列表
    pr_list = []
    for pr in sorted(prs, key=lambda x: x.get('additions', 0), reverse=True)[:20]:
        pr_list.append(f"- [#{pr['number']}] {pr['title']} (@{pr['author']['login']})")
    
    # 统计贡献者
    contributors = {}
    for pr in prs:
        author = pr['author']['login']
        contributors[author] = contributors.get(author, 0) + 1
    
    contrib_list = [f"- @{a}: {c} PRs" for a, c in 
                    sorted(contributors.items(), key=lambda x: -x[1])[:10]]
    
    return TEMPLATE.format(
        component=component,
        date=datetime.now().strftime('%Y-%m-%d'),
        count=len(prs),
        additions=additions,
        deletions=deletions,
        files=files,
        pr_list='\n'.join(pr_list),
        contributors='\n'.join(contrib_list)
    )
```

---

## 4. AI 辅助分析

### 批量分析流程

```
┌─────────────────────────────────────────────────────────────┐
│                    AI 辅助分析流程                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 获取 PR 列表 (GitHub API)                               │
│     ↓                                                       │
│  2. 自动分类 (关键词 + ML)                                  │
│     ↓                                                       │
│  3. 优先级排序 (影响评估)                                   │
│     ↓                                                       │
│  4. AI 深度分析 (Top 50)                                    │
│     - 使用 Qwen/Claude 分析 PR 描述                         │
│     - 提取关键技术点                                        │
│     - 生成详细文档                                          │
│     ↓                                                       │
│  5. 半自动分析 (Top 200)                                    │
│     - 模板化报告                                            │
│     - 关键信息提取                                          │
│     ↓                                                       │
│  6. 统计摘要 (剩余)                                         │
│     - 按组件聚合                                            │
│     - 生成变更日志                                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### AI Prompt 模板

```
分析以下 JDK PR 并生成技术文档:

PR 标题: {title}
PR 描述: {body}
变更文件: {files}

请生成:
1. 概述 (50字)
2. 技术要点 (3-5点)
3. 影响 (性能/兼容性)
4. 代码示例 (如适用)
```

---

## 5. 输出结构

```
prs/
├── index.md                    # 总索引
├── jdk26-overview.md           # JDK 26 概览
├── jdk26-statistics.md         # 统计报告
│
├── components/                 # 按组件分析
│   ├── gc.md                   # GC 组件总结
│   ├── compiler.md             # 编译器总结
│   ├── network.md              # 网络总结
│   └── ...
│
├── {prefix}/                   # 详细 PR 分析
│   └── {issue}.md
│
└── contributors/               # 贡献者分析
    ├── top-20.md               # Top 20 贡献者
    └── {author}.md             # 个人贡献
```

---

## 6. 执行计划

### 阶段 1: 数据收集 (1天)

```bash
# 1. 获取 PR 数据
./scripts/fetch_prs.sh

# 2. 获取 commit 数据
./scripts/fetch_commits.sh

# 3. 分类
python3 scripts/classify_prs.py
```

### 阶段 2: 核心分析 (2天)

- 手动深度分析 Top 50 PR
- AI 辅助分析 Top 200 PR
- 生成组件总结报告

### 阶段 3: 统计报告 (1天)

- 生成统计数据
- 创建变更日志
- 完善索引

---

## 7. 快速启动

```bash
# 创建分析脚本目录
mkdir -p scripts/

# 下载 PR 数据
gh pr list --repo openjdk/jdk --state merged \
  --limit 3000 --json number,title,author,labels \
  --search "merged:>=2024-09-01" > prs/jdk26-prs.json

# 运行分类
python3 scripts/classify_prs.py prs/jdk26-prs.json
```

---

## 8. 重点关注领域

### JDK 26 核心改动

| 领域 | 重点 PR | 状态 |
|------|---------|------|
| 分代 Shenandoah | JEP 521 | ✅ 已分析 |
| Compact Headers | JEP 519 | ✅ 已分析 |
| HTTP/3 | JEP 517 | 待分析 |
| G1 优化 | 8372162 | ✅ 已分析 |
| 虚拟线程优化 | 8372159 | ✅ 已分析 |
| 后量子密码 | 8371259, 8347606 | ✅ 已分析 |

---

## 9. 资源需求

| 任务 | 时间 | 工具 |
|------|------|------|
| 数据获取 | 1 小时 | gh, curl |
| 分类排序 | 2 小时 | Python |
| 深度分析 | 8 小时 | AI + 手动 |
| 报告生成 | 4 小时 | Python |
| 审核修订 | 4 小时 | 手动 |
| **总计** | **~20 小时** | |

---

## 变更历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0 | 2025-03 | 初始策略文档 |
