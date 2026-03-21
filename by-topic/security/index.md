# 安全国际化

加密、TLS、本地化等。

[← 返回主题索引](../)

---
## 目录

1. [演进概览](#1-演进概览)
2. [主题列表](#2-主题列表)
3. [核心贡献者](#3-核心贡献者)
4. [内部开发者资源](#4-内部开发者资源)
5. [统计数据](#5-统计数据)
6. [学习路径](#6-学习路径)

---


## 1. 演进概览

```
JDK 1.0 ─── JDK 8 ─── JDK 11 ─── JDK 17 ─── JDK 21 ─── JDK 26
   │           │            │            │            │           │
 JSSE       TLS 1.2      TLS 1.3      KMAC        后量子签名   ML-DSA
 HTTPS                   ChaCha20     SHA-3       KDF API     (正式)
                        (JEP 329,332)             (JEP 495)   (JEP 518)
```

### 版本里程碑

| 版本 | 主题 | 关键特性 |
|------|------|----------|
| **JDK 8** | TLS 1.2 | TLS 1.2 默认启用 |
| **JDK 11** | TLS 1.3 | TLS 1.3 (JEP 332)、ChaCha20-Poly1305 (JEP 329) |
| **JDK 17** | 新密码学 | KMAC、SHA-3 家族 |
| **JDK 21** | 签名增强 | HSS/LMS 签名 |
| **JDK 26** | 后量子密码 | ML-DSA (JEP 518)、KDF API 正式 (JEP 510) |

---

## 2. 主题列表

### [安全特性](security/)

加密、TLS、后量子密码。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 8 | TLS 1.2 (默认) | - |
| JDK 11 | **TLS 1.3**、ChaCha20-Poly1305 | JEP 332, JEP 329 |
| JDK 15 | 禁用弱签名算法 | - |
| JDK 17 | KMAC、SHA-3 家族 | - |
| JDK 21 | 增强密码套件、HSS/LMS 签名 | - |
| JDK 22-23 | KDF API (预览) | JEP 495, JEP 508 |
| JDK 26 | **ML-DSA** 后量子签名、**KDF API** (正式)、**PEM 格式** | JEP 518, JEP 510, JEP 470 |

→ [安全特性时间线](security/timeline.md)

### [国际化](i18n/)

Java 国际化 (i18n) 从 JDK 1.0 到 JDK 26 的完整演进。

| 版本 | 主要变化 | 说明 |
|------|----------|------|
| JDK 1.0 | Locale, ResourceBundle | 基础 i18n |
| JDK 1.1 | DecimalFormat, SimpleDateFormat | 格式化 |
| JDK 5 | Formatter, MessageFormat | 增强格式化 |
| JDK 6 | Unicode 4.0 | 规范化 |
| JDK 8 | CLDR 数据 | 更准确本地化 |
| JDK 13 | Unicode 13 | 新字符支持 |
| JDK 18 | Unicode 扩展 | EAI 支持 |

→ [国际化时间线](i18n/timeline.md)

---

## 3. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 安全/密码学 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Valerie Peng | 38 | Oracle | 密码学算法 |
| 2 | Weijun Wang | 36 | Oracle | 密钥管理, KDF |
| 3 | Sean Mullan | 31 | Oracle | 安全架构、JEP 332 (TLS 1.3) |
| 4 | Andrey Turbanov | 16 | Oracle | 密码学优化 |
| 5 | Sean Coffey | 12 | Oracle | JSSE (TLS/SSL) |
| 6 | Bradford Wetmore | 11 | Oracle | TLS 实现 |
| 7 | Joe Darcy | 10 | Oracle | 安全 API |

### 国际化 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | [Naoto Sato](/by-contributor/profiles/naoto-sato.md) | 64 | Oracle | Unicode 支持、CLDR 集成 |
| 2 | [Shaojin Wen (温绍锦)](../../by-contributor/profiles/shaojin-wen.md) | 12 | Alibaba | java.time 优化 |
| 3 | Roger Riggs | 12 | Oracle | 日期时间 |
| 4 | [Claes Redestad](/by-contributor/profiles/claes-redestad.md) | 8 | Oracle | 启动优化 |
| 5 | Andrey Turbanov | 7 | Oracle | 格式化 |
| 6 | Pavel Rappo | 6 | Oracle | 文档, 工具 |

---

## 4. 内部开发者资源

### 源码结构

```
src/java.base/share/classes/java/security/
├── MessageDigest.java           # 消息摘要
├── Signature.java               # 数字签名
├── Cipher.java                  # 加密/解密
├── KeyStore.java                # 密钥存储
└── cert/                        # 证书处理

src/java.base/share/classes/javax/crypto/
├── Cipher.java                  # 密码学引擎
├── SecretKeyFactory.java        # 密钥工厂
└── interfaces/                  # 密码学接口

src/java.base/share/classes/com/sun/crypto/  # 内部实现
src/java.base/share/classes/sun/security/    # 安全提供者
├── provider/
│   ├── SunProvider.java        # 默认安全提供者
│   └── NativeP11.java           # PKCS#11 实现
├── ssl/                         # TLS/SSL 实现
│   ├── ServerContext.java
│   └── ClientContext.java
└── x509/                        # X.509 证书

src/java.base/share/classes/java/util/
├── Locale.java                  # 地区设置
├── ResourceBundle.java          # 资源包
├── Currency.java                # 货币
└── calendar/                    # 日历

src/java.base/share/classes/sun/util/locale/  # 内部国际化
├── LocaleProviderAdapter.java
└── cldr/                        # CLDR 数据
```

### 关键内部类

| 类 | 作用 | 访问级别 |
|---|------|----------|
| `sun.security.ssl.SSLContextImpl` | TLS 上下文实现 | 内部 |
| `sun.security.provider.Sun` | 默认安全提供者 | 内部 |
| `sun.security.util.SecurityProviderConstants` | 安全常量 | 内部 |
| `jdk.internal.misc.Cleaner` | 用于密钥清理 | `@Restricted` |

### VM 参数速查

```bash
# TLS/SSL
-Djdk.tls.client.protocols=TLSv1.3,TLSv1.2  # 启用的协议
-Djdk.tls.server.cipherSuites=TLS_AES_256_GCM_SHA384  # 密码套件
-Djavax.net.ssl.trustStore=/path/to/cacerts  # 信任库
-Djavax.net.ssl.keyStore=/path/to/keystore  # 密钥库
-Djavax.net.debug=ssl,handshake             # SSL 调试

# 安全提供者
-Djava.security.policy=/path/to/policy      # 安全策略
-Djava.security.debug=access,failure        # 安全调试

# 密码学
-Djdk.crypto.KeyAgreement.legacyKDF=true     # 兼容旧版 KDF

# 国际化
-Duser.language=en                          # 语言
-Duser.country=US                            # 国家
-Duser.timezone=America/New_York            # 时区
-Djava.locale.providers=CLDR,SPI            # 本地化提供者
```

### 诊断工具

```bash
# 列出所有密码算法
java -XshowSettings:properties -version 2>&1 | grep security

# 列出所有 SSL/TLS 协议
java -Djdk.tls.server.protocols=TLSv1.3,TLSv1.2 -Djavax.net.debug=ssl -version

# 测试密钥库
keytool -list -v -keystore $JAVA_HOME/lib/security/cacerts

# 检查默认 Locale
java -Duser.language=zh -Duser.country=CN -XshowSettings:locale
```

---

## 5. 统计数据

| 指标 | 数值 |
|------|------|
| 安全 JEP (JDK 8-26) | 15+ |
| TLS 协议支持 | TLS 1.2, 1.3 |
| 密码算法 | 100+ |
| Locale 数量 | 150+ |

---

## 6. 学习路径

1. **入门**: [国际化](i18n/) → 多语言支持
2. **进阶**: [安全特性](security/) → 加密与 TLS
3. **深入**: [安全特性](security/) → 后量子密码 → 前沿安全
