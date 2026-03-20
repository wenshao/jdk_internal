# 国际化

> Locale、ResourceBundle、Unicode 支持演进历程

---

## 快速概览

```
JDK 1.0 ── JDK 1.1 ── JDK 5 ── JDK 8 ── JDK 17
   │         │        │        │        │
Locale   ResourceBundle Unicode ICU4J 增强
          Properties   4.0    兼容层
```

### 核心演进

| 版本 | 特性 | 说明 |
|------|------|------|
| **JDK 1.0** | Locale | 地区设置 |
| **JDK 1.1** | ResourceBundle | 资源绑定 |
| **JDK 5** | Unicode 4.0 | 完整 Unicode |
| **JDK 8** | ICU4J | 国际化组件 |
| **JDK 17** | 增强 | 更多语言支持 |

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 国际化 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Naoto Sato | 87 | Oracle | 日期, 国际化 |
| 2 | Justin Lu | 81 | Oracle | Locale, ResourceBundle |
| 3 | Andrey Turbanov | 12 | Independent | 格式化 |
| 4 | Pavel Rappo | 8 | Oracle | API 设计 |
| 5 | Rachna Goel | 7 | Oracle | 国际化 |
| 6 | Nishit Jain | 7 | Oracle | Locale |

---

## 相关链接

- [国际化时间线](timeline.md)
- [安全](../security/)
