# 安全

> 加密、签名、SSL/TLS、安全策略演进历程

---

## 快速概览

```
JDK 1.0 ── JDK 1.2 ── JDK 6 ── JDK 7 ── JDK 11 ── JDK 21
   │         │        │        │        │        │
安全    JAAS    TLS 1.2  TLS 1.3  ChaCha20  后量子
策略    JCE     AES/GCM  ALPN    密码套件   密码学
```

### 核心演进

| 版本 | 特性 | 说明 |
|------|------|------|
| **JDK 1.0** | 安全策略 | sandbox |
| **JDK 1.2** | JAAS | 认证授权 |
| **JDK 1.4** | JCE | 加密扩展 |
| **JDK 6** | TLS 1.2 | 安全传输 |
| **JDK 7** | AES-GCM | 认证加密 |
| **JDK 11** | TLS 1.3 | 性能优化 |
| **JDK 11** | ChaCha20-Poly1305 | 现代密码学 |
| **JDK 21** | 后量子密码学 | 准备 |

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 安全 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Weijun Wang | 174 | Oracle | 密码学, 签名 |
| 2 | Xue-Lei Andrew Fan | 116 | Oracle | SSL/TLS |
| 3 | Sean Mullan | 71 | Oracle | 安全策略 |
| 4 | Valerie Peng | 54 | Oracle | 加密算法 |
| 5 | Jamil Nimeh | 39 | Oracle | SSL/TLS |
| 6 | Hai-May Chao | 36 | Oracle | 密码学 |
| 7 | Anthony Scarpino | 32 | Oracle | 安全核心 |

---

## 相关链接

- [安全时间线](timeline.md)
- [国际化](../i18n/)
