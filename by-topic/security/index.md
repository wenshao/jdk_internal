# 安全与国际化

加密、TLS、后量子密码、安全架构、本地化等。

[← 返回主题索引](../)

---
## 快速导航

| 子主题 | 说明 | 链接 |
|--------|------|------|
| 安全特性 | 加密算法、TLS/SSL、后量子密码学、数字签名 | [安全特性](security/) |
| 安全时间线 | JDK 1.0 至 JDK 26 安全特性完整演进 | [时间线](security/timeline.md) |
| 国际化 | Locale、ResourceBundle、Unicode、CLDR | [国际化](i18n/) |
| 国际化时间线 | JDK 1.0 至 JDK 24 国际化完整演进 | [时间线](i18n/timeline.md) |

---
## 目录

1. [演进概览](#1-演进概览)
2. [版本里程碑详解](#2-版本里程碑详解)
3. [关键 JEP 一览表](#3-关键-jep-一览表)
4. [后量子密码学路线图](#4-后量子密码学路线图)
5. [主题列表](#5-主题列表)
6. [核心贡献者](#6-核心贡献者)
7. [内部开发者资源](#7-内部开发者资源)
8. [统计数据](#8-统计数据)
9. [学习路径](#9-学习路径)

---


## 1. 演进概览

Java 安全体系从 JDK 1.0 的沙箱模型起步，经历了加密扩展、TLS 现代化、Security Manager 退役、
后量子密码学引入等重大变革，至 JDK 26 已形成面向量子安全时代的完整密码学栈。

```
JDK 1.0 ── JDK 1.2 ── JDK 1.4 ── JDK 5 ── JDK 7 ── JDK 8 ── JDK 9 ── JDK 11 ── JDK 13
   │          │          │         │        │        │        │        │          │
 沙箱      JAAS      JCE 集成   JCE无     TLS      TLS 1.2  JPMS    TLS 1.3    TLS默认
 安全策略  认证授权   JSSE合并   限制      1.2支持  默认启用  模块化  JEP 332    TLS 1.3
                     X.509增强  策略      AES-GCM  AES-PBE  安全边界 ChaCha20   JEP 332
                                                            JEP 261  JEP 329

JDK 14 ── JDK 15 ── JDK 16 ── JDK 17 ── JDK 21 ── JDK 24 ── JDK 25 ── JDK 26 ── JDK 27
   │          │          │         │          │          │          │          │         │
 DTLS      EdDSA     禁用旧    SM弃用    KEM API    ML-KEM     KDF API   HPKE      混合TLS
 1.2       JEP 339   TLS算法   JEP 411   JEP 452    JEP 496    JEP 510   PEM v2    JEP 527
 JEP 373             SHA-1    KMAC       HSS/LMS   ML-DSA     PEM v1    ML-DSA    PQ混合
                     禁止     SHA-3                 JEP 497    JEP 470   JEP 518   密钥交换
                                                    KDF预览              JEP 524
                                                    JEP 478              JEP 517
```

---

## 2. 版本里程碑详解

### 基础阶段 (JDK 1.0 - JDK 7)

| 版本 | 主题 | 关键特性 | 说明 |
|------|------|----------|------|
| **JDK 1.0** | 安全沙箱 | Sandbox 模型、SecurityManager | Java 安全体系的起点，通过沙箱隔离不可信代码 |
| **JDK 1.1** | 签名支持 | JAR 签名、DSA 签名 | 引入代码签名验证机制 |
| **JDK 1.2** | JAAS | 认证与授权框架、Policy | 细粒度权限控制，替代全有全无的沙箱模型 |
| **JDK 1.4** | JCE/JSSE 集成 | JCE、JSSE 合入标准库、PKCS#11 | 密码学扩展不再需要单独下载 |
| **JDK 5** | 策略增强 | JCE 无限制策略、XML 签名 | 解除出口管制限制 |
| **JDK 7** | TLS 1.2 | TLS 1.2 支持、AES-GCM、SNI 扩展 | 首次支持 TLS 1.2 (但未默认启用) |

### 现代化阶段 (JDK 8 - JDK 13)

| 版本 | 主题 | 关键特性 | 说明 |
|------|------|----------|------|
| **JDK 8** | TLS 1.2 默认 | TLS 1.2 默认启用、AES-PBE、GCM 优先 | 密码套件优先级调整，GCM 模式优先 |
| **JDK 9** | JPMS 安全边界 | 模块化安全 (JEP 261)、DTLS 1.0、SHA-3 | 模块系统提供强封装，替代部分安全策略功能 |
| **JDK 10** | 根证书 | 开源根证书 (JEP 319) | OpenJDK 内置 CA 证书 |
| **JDK 11** | TLS 1.3 | TLS 1.3 (JEP 332)、ChaCha20-Poly1305 (JEP 329) | 0-RTT 握手、更强的隐私保护 |
| **JDK 12** | 密钥协商 | 默认禁用 TLS 1.0/1.1、增强密钥协商 | 逐步淘汰旧版协议 |
| **JDK 13** | TLS 默认值 | TLS 1.3 默认启用、证书压缩 | TLS 1.3 成为默认协议 |

### 变革阶段 (JDK 14 - JDK 21)

| 版本 | 主题 | 关键特性 | 说明 |
|------|------|----------|------|
| **JDK 14** | DTLS 1.2 | DTLS 1.2 支持 (JEP 373) | UDP 上的安全传输 |
| **JDK 15** | 现代签名 | EdDSA (JEP 339)、禁用弱 TLS 算法 | 引入 Ed25519/Ed448 曲线签名 |
| **JDK 16** | 安全收紧 | 默认禁止 SHA-1 签名、强封装 JDK 内部 API | 清理遗留弱算法 |
| **JDK 17** | SM 弃用 | Security Manager 弃用 (JEP 411)、KMAC、SHA-3 | 标志性转折：沙箱安全模型退出历史舞台 |
| **JDK 21** | KEM 框架 | KEM API (JEP 452)、HSS/LMS 签名 | 为后量子算法奠定 API 基础 |

### 后量子阶段 (JDK 24 - JDK 27+)

| 版本 | 主题 | 关键特性 | 说明 |
|------|------|----------|------|
| **JDK 24** | 后量子基础 | ML-KEM (JEP 496, FIPS 203)、ML-DSA (JEP 497, FIPS 204)、KDF 预览 (JEP 478)、SM 永久禁用 (JEP 486) | NIST 标准化后量子算法正式进入 JDK |
| **JDK 25** | KDF 正式化 | KDF API 正式版 (JEP 510)、PEM 编码预览 (JEP 470)、安全提供者增强 | 密钥派生函数标准化 |
| **JDK 26** | 后量子应用 | ML-DSA JAR 签名 (JEP 518)、HPKE 混合加密、PEM v2 (JEP 524)、HTTP/3 预览 (JEP 517) | 后量子签名进入实际应用场景 |
| **JDK 27** | 混合 TLS (计划) | 后量子混合密钥交换 (JEP 527): X25519MLKEM768、SecP256r1MLKEM768、SecP384r1MLKEM1024 | TLS 1.3 混合模式，经典 + PQ 双重保护 |

---

## 3. 关键 JEP 一览表

### 加密与密码学

| JEP | 名称 | 版本 | 状态 | 说明 |
|-----|------|------|------|------|
| JEP 329 | ChaCha20 and Poly1305 Cryptographic Algorithms | JDK 11 | 已发布 | 替代不安全的 RC4 流密码 (RFC 7539) |
| JEP 339 | Edwards-Curve Digital Signature Algorithm (EdDSA) | JDK 15 | 已发布 | Ed25519/Ed448 现代椭圆曲线签名 (RFC 8032) |
| JEP 370 | SHA-3 Hash Functions | JDK 17 | 已发布 | SHA3-256/384/512、SHAKE128/256 |
| JEP 452 | Key Encapsulation Mechanism API | JDK 21 | 已发布 | KEM 框架 API，为后量子算法铺路 |
| JEP 478 | Key Derivation Function API (Preview) | JDK 24 | 预览 | 密钥派生函数 API (HKDF 等) |
| JEP 496 | Quantum-Resistant ML-KEM | JDK 24 | 已发布 | 后量子密钥封装 (NIST FIPS 203) |
| JEP 497 | Quantum-Resistant ML-DSA | JDK 24 | 已发布 | 后量子数字签名 (NIST FIPS 204) |
| JEP 510 | Key Derivation Function API | JDK 25 | 已发布 | KDF API 正式版 |
| JEP 518 | ML-DSA JAR Signatures | JDK 26 | 已发布 | 使用 ML-DSA 签名 JAR，供应链安全 |
| JEP 524 | PEM Encodings of Cryptographic Objects (Preview 2) | JDK 26 | 预览 | PEM 编解码 API 第二次预览 |

### TLS/SSL 与网络安全

| JEP | 名称 | 版本 | 状态 | 说明 |
|-----|------|------|------|------|
| JEP 332 | Transport Layer Security (TLS) 1.3 | JDK 11 | 已发布 | TLS 1.3 实现 (RFC 8446) |
| JEP 373 | DTLS 1.2 | JDK 14 | 已发布 | UDP 上的安全传输层 |
| JEP 517 | HTTP/3 for the HTTP Client API (Preview) | JDK 26 | 预览 | 基于 QUIC 的 HTTP/3 支持 |
| JEP 527 | Post-Quantum Hybrid Key Exchange for TLS 1.3 | JDK 27 | 计划 | 经典 + ML-KEM 混合密钥交换 |

### 安全架构

| JEP | 名称 | 版本 | 状态 | 说明 |
|-----|------|------|------|------|
| JEP 261 | Module System | JDK 9 | 已发布 | JPMS 模块化安全边界 |
| JEP 319 | Root Certificates | JDK 10 | 已发布 | OpenJDK 内置 CA 根证书 |
| JEP 411 | Deprecate the Security Manager for Removal | JDK 17 | 已发布 | 弃用 Security Manager |
| JEP 486 | Permanently Disable the Security Manager | JDK 24 | 已发布 | 永久禁用 Security Manager |

---

## 4. 后量子密码学路线图

JDK 的后量子密码学 (PQC) 采用分阶段方式推进，与 NIST 标准化进程同步。量子计算机的发展
将威胁当前基于 RSA/ECC 的加密体系，Java 平台正通过以下路线图实现量子安全迁移：

### 实施阶段

| 阶段 | 版本 | 内容 | NIST 标准 | 状态 |
|------|------|------|-----------|------|
| API 基础 | JDK 21 | KEM API 框架 (JEP 452)，定义 `javax.crypto.KEM` 接口 | - | 已完成 |
| 算法引入 | JDK 24 | ML-KEM 密钥封装、ML-DSA 数字签名 | FIPS 203, FIPS 204 | 已完成 |
| 密钥派生 | JDK 25 | KDF API 正式化，支撑 ML-KEM 密钥派生 (HKDF, SSKDF) | - | 已完成 |
| 签名应用 | JDK 26 | ML-DSA 用于 JAR 签名、HPKE 混合加密 (RFC 9180) | FIPS 204 | 已完成 |
| 混合 TLS | JDK 27 (计划) | 后量子混合密钥交换 (JEP 527) | - | 开发中 |
| 全面迁移 | JDK 28+ (展望) | 默认启用 PQ 混合模式、SLH-DSA 无状态签名 | FIPS 205 | 规划中 |

### 算法参数集

**ML-KEM (密钥封装机制, FIPS 203)**:

| 参数集 | 安全级别 | 公钥大小 | 密文大小 | 共享密钥 | 适用场景 |
|--------|----------|----------|----------|----------|----------|
| ML-KEM-512 | NIST 1 (128-bit) | 800 B | 768 B | 32 B | 一般应用 |
| ML-KEM-768 | NIST 3 (192-bit) | 1,184 B | 1,088 B | 32 B | 推荐默认 |
| ML-KEM-1024 | NIST 5 (256-bit) | 1,568 B | 1,568 B | 32 B | 高安全场景 |

**ML-DSA (数字签名, FIPS 204)**:

| 参数集 | 安全级别 | 公钥大小 | 签名大小 | 适用场景 |
|--------|----------|----------|----------|----------|
| ML-DSA-44 | NIST 2 (128-bit) | 1,312 B | 2,420 B | 一般签名 |
| ML-DSA-65 | NIST 3 (192-bit) | 1,952 B | 3,309 B | 推荐默认 |
| ML-DSA-87 | NIST 5 (256-bit) | 2,592 B | 4,627 B | 高安全签名 |

### TLS 1.3 混合密钥交换 (JEP 527, JDK 27)

JEP 527 将在 TLS 1.3 中实现混合密钥交换，结合经典 ECDHE 与后量子 ML-KEM 算法，
提供对经典和量子攻击的双重防护：

| 命名组 | 经典算法 | PQ 算法 | 安全级别 |
|--------|----------|---------|----------|
| X25519MLKEM768 | X25519 | ML-KEM-768 | NIST 3 |
| SecP256r1MLKEM768 | ECDHE P-256 | ML-KEM-768 | NIST 3 |
| SecP384r1MLKEM1024 | ECDHE P-384 | ML-KEM-1024 | NIST 5 |

---

## 5. 主题列表

### [安全特性](security/)

加密、TLS、后量子密码。覆盖对称/非对称加密、数字签名、SSL/TLS 配置、密钥管理等完整安全栈。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 8 | TLS 1.2 (默认)、AES-PBE | - |
| JDK 9 | DTLS 1.0、SHA-3、模块化安全 | JEP 261 |
| JDK 10 | OpenJDK 根证书 | JEP 319 |
| JDK 11 | **TLS 1.3**、ChaCha20-Poly1305 | JEP 332, JEP 329 |
| JDK 14 | DTLS 1.2 | JEP 373 |
| JDK 15 | **EdDSA** (Ed25519)、禁用弱签名算法 | JEP 339 |
| JDK 17 | KMAC、SHA-3 家族、**Security Manager 弃用** | JEP 411 |
| JDK 21 | **KEM API**、HSS/LMS 签名 | JEP 452 |
| JDK 24 | **ML-KEM** 量子抗性密钥封装 (FIPS 203)、**ML-DSA** 量子抗性签名 (FIPS 204)、KDF API 预览、**SM 永久禁用** | JEP 496, JEP 497, JEP 478, JEP 486 |
| JDK 25 | **KDF API** (正式)、PEM 编码预览、安全提供者增强 | JEP 510, JEP 470 |
| JDK 26 | **ML-DSA JAR 签名**、**HPKE 混合公钥加密**、PEM v2、**HTTP/3** (预览) | JEP 518, JEP 524, JEP 517 |

> [安全特性时间线](security/timeline.md)

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

> [国际化时间线](i18n/timeline.md)

---

## 6. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 安全/密码学 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献领域 |
|------|--------|--------|------|--------------|
| 1 | Sean Mullan | 71 | Oracle | Java 安全组技术负责人，安全架构、JEP 411 (SM 弃用)、XML 签名 |
| 2 | Valerie Peng | 54 | Oracle | 密码学算法实现、JCE 提供者、PKCS#11 |
| 3 | Xue-Lei Andrew Fan | 116 | Oracle | SSL/TLS 引擎 (JSSE)、TLS 1.3 实现 (JEP 332)、协议协商 |
| 4 | Weijun Wang | 174 | Oracle | 密钥管理、KDF API (JEP 510)、Kerberos/GSS-API、ML-KEM/ML-DSA |
| 5 | Anthony Scarpino | 32 | Oracle | 安全核心基础设施、加密算法、安全提供者架构 |
| 6 | Jamil Nimeh | 39 | Oracle | SSL/TLS 实现、ChaCha20-Poly1305 (JEP 329)、密码套件 |
| 7 | Bradford Wetmore | 11 | Oracle | TLS 实现、DTLS |
| 8 | Sean Coffey | 12 | Oracle | JSSE (TLS/SSL)、证书验证 |

### 国际化 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | [Naoto Sato](/by-contributor/profiles/naoto-sato.md) | 87 | Oracle | Unicode 支持、CLDR 集成 |
| 2 | [Justin Lu](/by-contributor/profiles/justin-lu.md) | 81 | Oracle | Locale, ResourceBundle |
| 3 | [Shaojin Wen (温绍锦)](../../by-contributor/profiles/shaojin-wen.md) | 12 | Alibaba | java.time 优化 |
| 4 | Roger Riggs | 12 | Oracle | 日期时间 |
| 5 | [Claes Redestad](/by-contributor/profiles/claes-redestad.md) | 8 | Oracle | 启动优化 |
| 6 | Andrey Turbanov | 7 | Independent | 格式化 |
| 7 | Pavel Rappo | 6 | Oracle | 文档, 工具 |

---

## 7. 内部开发者资源

### 源码结构

```
src/java.base/share/classes/java/security/
├── MessageDigest.java           # 消息摘要
├── Signature.java               # 数字签名
├── KeyStore.java                # 密钥存储
├── KeyFactory.java              # 密钥工厂
├── SecureRandom.java            # 安全随机数
├── cert/                        # 证书处理
│   ├── X509Certificate.java
│   └── CertificateFactory.java
└── spec/                        # 密钥规范

src/java.base/share/classes/javax/crypto/
├── Cipher.java                  # 密码学引擎 (加密/解密)
├── KEM.java                     # 密钥封装机制 (JDK 21+, JEP 452)
├── KDF.java                     # 密钥派生函数 (JDK 25+, JEP 510)
├── SecretKeyFactory.java        # 密钥工厂
└── interfaces/                  # 密码学接口

src/java.base/share/classes/com/sun/crypto/  # 内部实现
src/java.base/share/classes/sun/security/    # 安全提供者
├── provider/
│   ├── SunProvider.java         # 默认安全提供者
│   └── NativeP11.java           # PKCS#11 实现
├── ssl/                         # TLS/SSL 实现
│   ├── SSLContextImpl.java      # TLS 上下文
│   ├── ServerContext.java
│   └── ClientContext.java
├── x509/                        # X.509 证书
└── util/                        # 安全工具类

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
| `javax.crypto.KEM` | 密钥封装机制 API (JDK 21+) | 公开 |
| `javax.crypto.KDF` | 密钥派生函数 API (JDK 25+) | 公开 |
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
-Djava.security.properties=/path/to/props   # 安全属性文件

# 密码学
-Djdk.crypto.KeyAgreement.legacyKDF=true     # 兼容旧版 KDF
-Dkeystore.type=PKCS12                       # 默认密钥库类型 (JDK 9+)

# 国际化
-Duser.language=en                          # 语言
-Duser.country=US                            # 国家
-Duser.timezone=America/New_York            # 时区
-Djava.locale.providers=CLDR,SPI            # 本地化提供者
```

### 诊断工具

```bash
# 列出所有安全提供者和密码算法
java -XshowSettings:security -version

# 列出所有 SSL/TLS 协议并调试握手过程
java -Djavax.net.debug=ssl:handshake -version

# 查看密钥库内容
keytool -list -v -keystore $JAVA_HOME/lib/security/cacerts

# 检查 JKS/JCEKS 迁移状态 (JDK 26+ 会发出弃用警告)
keytool -list -keystore legacy.jks -storetype JKS

# 生成 ML-DSA 密钥对 (JDK 24+)
keytool -genkeypair -alias mykey -keyalg ML-DSA -keysize ML-DSA-65

# 检查默认 Locale
java -Duser.language=zh -Duser.country=CN -XshowSettings:locale
```

---

## 8. 统计数据

| 指标 | 数值 | 说明 |
|------|------|------|
| 安全相关 JEP (JDK 8-27) | 25+ | 含加密、TLS、安全架构 |
| TLS 协议支持 | TLS 1.2, 1.3 | TLS 1.0/1.1 已默认禁用 |
| 后量子算法 | ML-KEM (FIPS 203), ML-DSA (FIPS 204) | JDK 24 引入 |
| 密码算法 | 100+ | 对称/非对称/签名/摘要/MAC |
| 安全提供者 | 10+ | SUN, SunJSSE, SunJCE, SunPKCS11 等 |
| Locale 数量 | 150+ | 基于 CLDR 数据 |
| Security Manager 状态 | 已永久禁用 | JEP 411 (JDK 17) → JEP 486 (JDK 24) |

---

## 9. 学习路径

### 入门路径

1. **基础安全概念**: [安全特性](security/) - 对称加密 (AES)、消息摘要 (SHA-256)
2. **TLS/SSL 配置**: [安全特性](security/) - TLS 1.3 握手、证书管理
3. **国际化**: [国际化](i18n/) - Locale、ResourceBundle、字符编码

### 进阶路径

4. **密码学深入**: [安全特性](security/) - 非对称加密、数字签名、KEM API
5. **安全架构**: 模块化安全 (JPMS) → Security Manager 退役历程
6. **密钥管理**: KeyStore、PKCS#12、PEM 编码

### 前沿路径

7. **后量子密码学**: ML-KEM (FIPS 203) → ML-DSA (FIPS 204) → HPKE (RFC 9180)
8. **混合 TLS**: JEP 527 后量子混合密钥交换
9. **供应链安全**: ML-DSA JAR 签名 (JEP 518)
