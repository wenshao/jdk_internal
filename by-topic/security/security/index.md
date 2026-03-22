# 安全

> 加密、签名、SSL/TLS、安全策略演进历程

[← 返回安全](../)

---
## 目录

1. [快速概览](#1-快速概览)
2. [核心贡献者](#2-核心贡献者)
3. [JDK 加密提供者架构](#3-jdk-加密提供者架构)
4. [加密算法](#4-加密算法)
5. [数字签名](#5-数字签名)
6. [TLS 演进详解](#6-tls-演进详解)
7. [后量子密码 (PQC)](#7-后量子密码-pqc)
8. [Key Derivation Function API](#8-key-derivation-function-api)
9. [PEM API](#9-pem-api)
10. [序列化安全](#10-序列化安全)
11. [Security Manager 消亡史](#11-security-manager-消亡史)
12. [密钥管理](#12-密钥管理)
13. [最佳实践](#13-最佳实践)
14. [相关链接](#14-相关链接)

---


## 1. 快速概览

```
JDK 1.0 ── JDK 1.2 ── JDK 1.4 ── JDK 7 ── JDK 11 ── JDK 21 ── JDK 24 ── JDK 25 ── JDK 26
   │         │         │        │        │        │        │        │        │
安全    JAAS     JCE     TLS    TLS     KEM     ML-KEM  KDF     HPKE
策略    认证     加密    1.2    1.3     API     JEP496  API     PEM
沙箱    授权     扩展    AES    ChaCha  JEP     ML-DSA  JEP     JEP524
                        GCM    Poly    452     JEP497  510     JAR签名
```

### 核心演进

| 版本 | 特性 | 说明 | JEP |
|------|------|------|-----|
| **JDK 1.0** | 安全策略 | Sandbox 模型 | - |
| **JDK 1.2** | JAAS | 认证授权 | - |
| **JDK 1.4** | JCE | 加密扩展 | - |
| **JDK 7** | TLS 1.2 | AES/GCM 模式 | - |
| **JDK 7** | AES-GCM | 认证加密 | - |
| **JDK 9** | JEP 290 | 序列化过滤器 | JEP 290 |
| **JDK 11** | TLS 1.3 | 性能优化 | JEP 332 |
| **JDK 11** | ChaCha20-Poly1305 | 现代密码学 | JEP 329 |
| **JDK 15** | 禁用弱签名 | SHA-1 | - |
| **JDK 17** | JEP 415 | 上下文序列化过滤器 | JEP 415 |
| **JDK 17** | JEP 411 | Security Manager 弃用 | JEP 411 |
| **JDK 21** | 密钥封装 API | KEM 框架 | JEP 452 |
| **JDK 24** | ML-KEM | 后量子密钥封装 (FIPS 203) | JEP 496 |
| **JDK 24** | ML-DSA | 后量子签名 (FIPS 204) | JEP 497 |
| **JDK 24** | JEP 486 | Security Manager 永久禁用 | JEP 486 |
| **JDK 24** | KDF API (预览) | 密钥派生函数 | JEP 478 |
| **JDK 25** | KDF API | 密钥派生函数 (HKDF) | JEP 510 |
| **JDK 25** | PEM 编码 (预览) | 密钥/证书 PEM 格式 | JEP 470 |
| **JDK 26** | HPKE | 混合公钥加密 (RFC 9180) | - |
| **JDK 26** | PEM 编码 (预览 2) | PEMRecord 重命名为 PEM | JEP 524 |
| **JDK 26** | ML-DSA JAR 签名 | 后量子 JAR 签名 | JEP 518 |

---

## 2. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 安全团队 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Weijun Wang | 174 | Oracle | 密码学, 签名, KDF API (JEP 510), ML-KEM/ML-DSA 实现 |
| 2 | Xue-Lei Andrew Fan | 116 | Oracle | SSL/TLS 引擎 (JSSE), TLS 1.3 实现 (JEP 332), 协议协商 |
| 3 | Sean Mullan | 71 | Oracle | Java 安全组技术负责人, 安全架构, JEP 411 (SM 弃用), XML 签名 |
| 4 | Valerie Peng | 54 | Oracle | JCE 提供者实现, PKCS#11, 加密算法底层 |
| 5 | Jamil Nimeh | 39 | Oracle | SSL/TLS, ChaCha20-Poly1305 (JEP 329), 密码套件 |
| 6 | Hai-May Chao | 36 | Oracle | 密码学算法 |
| 7 | Anthony Scarpino | 32 | Oracle | 安全核心基础设施, 安全提供者架构 |
| 8 | Sean Coffey | 12 | Oracle | JSSE (TLS/SSL), 证书验证, 安全更新维护 |

### 关键人物详情

**Xue-Lei Andrew Fan (范学雷)** — JSSE (Java Secure Socket Extension) 的核心维护者。JDK 中 TLS 协议栈的大量代码出自他手，包括 TLS 1.3 实现 (JEP 332)、SSLEngine/SSLSocket 架构重构、协议版本协商机制等。在 `sun.security.ssl` 包中的提交覆盖了握手状态机 (handshake state machine)、密码套件选择、ALPN 协商等关键路径。

**Sean Mullan** — Oracle 安全组的技术负责人 (Tech Lead)。主导了 Security Manager 弃用 (JEP 411) 和 XML 数字签名的长期维护。他的工作更偏架构层面：安全策略框架、证书路径验证 (CertPath)、安全提供者接口设计等。

**Sean Coffey** — 主要活跃在 JDK 安全更新 (CPU/PSU) 中，负责 JSSE 的 bug 修复和安全补丁。在 Oracle 的季度安全更新 (Critical Patch Update) 中经常出现他的提交。

---

## 3. JDK 加密提供者架构

Java 安全体系基于 **Provider Architecture** (提供者架构)，将加密算法的接口定义与具体实现分离。应用代码通过 `java.security` 和 `javax.crypto` 中的引擎类 (engine classes) 调用算法，底层由注册的安全提供者 (Security Provider) 提供实现。

### 提供者层次结构

```
┌─────────────────────────────────────────────────────────┐
│              应用代码                                     │
│   Cipher.getInstance("AES/GCM/NoPadding")               │
│   Signature.getInstance("SHA256withRSA")                 │
│   KEM.getInstance("ML-KEM")                              │
└───────────────────────┬─────────────────────────────────┘
                        │ 查找匹配的 Provider
┌───────────────────────▼─────────────────────────────────┐
│          java.security.Provider 注册表                    │
│   按优先级顺序查找 (priority number, 数字越小优先级越高)    │
└───────────────────────┬─────────────────────────────────┘
                        │
    ┌───────────┬───────┴──────┬──────────────┬───────────┐
    ▼           ▼              ▼              ▼           ▼
┌───────┐ ┌─────────┐  ┌──────────┐  ┌───────────┐ ┌─────────┐
│  SUN  │ │ SunJCE  │  │ SunEC    │  │ SunPKCS11 │ │SunJSSE  │
│       │ │         │  │          │  │           │ │         │
│摘要   │ │对称加密 │  │椭圆曲线  │  │硬件令牌   │ │TLS/SSL  │
│签名   │ │MAC      │  │ECDSA     │  │HSM 集成   │ │协议实现 │
│SecRng │ │密钥协商 │  │EdDSA     │  │PKCS#11    │ │DTLS     │
│证书   │ │KEM      │  │ECDHE     │  │智能卡     │ │握手协商 │
│PBE    │ │KDF      │  │ML-KEM*   │  │           │ │         │
└───────┘ └─────────┘  └──────────┘  └───────────┘ └─────────┘
```

### 内置安全提供者

| 提供者 | 全名 | 主要职责 | 典型算法 |
|--------|------|----------|----------|
| **SUN** | `sun.security.provider.Sun` | 基础安全服务 | SHA-256, SHA-3, DSA, SecureRandom, CertificateFactory |
| **SunJCE** | `com.sun.crypto.provider.SunJCE` | 对称加密, MAC, 密钥协商 | AES, ChaCha20, HmacSHA256, DH, KEM, KDF |
| **SunEC** | `sun.security.ec.SunEC` | 椭圆曲线密码学 | ECDSA, ECDHE, EdDSA (Ed25519/Ed448), XDH |
| **SunPKCS11** | `sun.security.pkcs11.SunPKCS11` | 硬件安全模块 (HSM) 接口 | 通过 PKCS#11 标准对接硬件令牌/智能卡 |
| **SunJSSE** | `sun.security.ssl.SunJSSE` | TLS/SSL/DTLS 协议 | SSLContext, TrustManagerFactory, KeyManagerFactory |
| **SunRsaSign** | `sun.security.rsa.SunRsaSign` | RSA 签名和加密 | SHA256withRSA, SHA384withRSA, RSA/ECB/PKCS1Padding |
| **SunMSCAPI** | (仅 Windows) | Windows 证书库集成 | Windows-ROOT, Windows-MY KeyStore |
| **OracleUcrypto** | (仅 Solaris/旧版) | 硬件加速 | 利用 CPU 加密指令 |

### 提供者优先级与选择

```java
import java.security.*;

// 列出所有已注册提供者及其优先级
for (Provider p : Security.getProviders()) {
    System.out.printf("%-20s version=%.1f  position=%d%n",
        p.getName(), p.getVersion(), p.isConfigured() ? 1 : 0);
}

// 指定提供者
Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding", "SunJCE");

// 动态添加提供者 (在所有已有提供者之后)
Security.addProvider(new BouncyCastleProvider());

// 插入到指定位置 (1 = 最高优先级)
Security.insertProviderAt(new BouncyCastleProvider(), 1);

// 在 java.security 配置文件中设置提供者顺序
// security.provider.1=SUN
// security.provider.2=SunRsaSign
// security.provider.3=SunEC
// security.provider.4=SunJSSE
// security.provider.5=SunJCE
// security.provider.6=SunPKCS11
```

### 引擎类 (Engine Classes) 速查

引擎类是应用代码的入口点，通过 `getInstance()` 工厂方法获取实例：

| 引擎类 | 包 | 用途 | 示例算法 |
|--------|----|------|----------|
| `MessageDigest` | `java.security` | 消息摘要 | SHA-256, SHA3-256 |
| `Signature` | `java.security` | 数字签名 | SHA256withRSA, Ed25519, ML-DSA |
| `Cipher` | `javax.crypto` | 加密/解密 | AES/GCM/NoPadding |
| `Mac` | `javax.crypto` | 消息认证码 | HmacSHA256 |
| `KeyGenerator` | `javax.crypto` | 对称密钥生成 | AES |
| `KeyPairGenerator` | `java.security` | 非对称密钥对生成 | RSA, EC, ML-KEM, ML-DSA |
| `KeyAgreement` | `javax.crypto` | 密钥协商 | ECDH, XDH |
| `KEM` | `javax.crypto` | 密钥封装 (JDK 21+) | ML-KEM |
| `KDF` | `javax.crypto` | 密钥派生 (JDK 25+) | HKDF-SHA256 |
| `KeyFactory` | `java.security` | 密钥格式转换 | RSA, EC |
| `SecureRandom` | `java.security` | 安全随机数 | DRBG, NativePRNG |
| `SSLContext` | `javax.net.ssl` | TLS 上下文 | TLSv1.3 |

---

## 4. 加密算法

### 对称加密

```java
import javax.crypto.*;
import javax.crypto.spec.*;
import java.security.*;

// AES-GCM 加密 (推荐的认证加密模式)
Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");

// 生成 256 位 AES 密钥
KeyGenerator keyGen = KeyGenerator.getInstance("AES");
keyGen.init(256);
SecretKey key = keyGen.generateKey();

// GCM 需要 12 字节的 IV (nonce)
byte[] iv = new byte[12];
SecureRandom.getInstanceStrong().nextBytes(iv);
GCMParameterSpec gcmSpec = new GCMParameterSpec(128, iv); // 128-bit auth tag

// 加密
cipher.init(Cipher.ENCRYPT_MODE, key, gcmSpec);
cipher.updateAAD("metadata".getBytes());  // 附加认证数据 (AAD)
byte[] ciphertext = cipher.doFinal("Hello AES-GCM".getBytes());

// 解密
cipher.init(Cipher.DECRYPT_MODE, key, gcmSpec);
cipher.updateAAD("metadata".getBytes());  // AAD 必须一致
byte[] decrypted = cipher.doFinal(ciphertext);
```

### 非对称加密

```java
import java.security.*;
import javax.crypto.*;

// RSA 密钥对
KeyPairGenerator keyGen = KeyPairGenerator.getInstance("RSA");
keyGen.initialize(2048);
KeyPair keyPair = keyGen.generateKeyPair();

// 公钥加密
Cipher cipher = Cipher.getInstance("RSA/ECB/OAEPWithSHA-256AndMGF1Padding");
cipher.init(Cipher.ENCRYPT_MODE, keyPair.getPublic());
byte[] encrypted = cipher.doFinal("Hello RSA".getBytes());

// 私钥解密
cipher.init(Cipher.DECRYPT_MODE, keyPair.getPrivate());
byte[] decrypted = cipher.doFinal(encrypted);
```

### 消息摘要

```java
import java.security.*;

// SHA-256
MessageDigest digest = MessageDigest.getInstance("SHA-256");
byte[] hash = digest.digest("Hello".getBytes());

// SHA-3 (JDK 9+)
MessageDigest sha3 = MessageDigest.getInstance("SHA3-256");
byte[] hash3 = sha3.digest("Hello".getBytes());
```

### HMAC

```java
import javax.crypto.*;
import javax.crypto.spec.*;

// HMAC-SHA256
SecretKeySpec keySpec = new SecretKeySpec(
    "secret".getBytes(), "HmacSHA256");
Mac mac = Mac.getInstance("HmacSHA256");
mac.init(keySpec);
byte[] hmac = mac.doFinal("Hello".getBytes());
```

---

## 5. 数字签名

### RSA 签名与验证

```java
import java.security.*;

// 生成密钥对
KeyPairGenerator keyGen = KeyPairGenerator.getInstance("RSA");
keyGen.initialize(2048);
KeyPair keyPair = keyGen.generateKeyPair();

// 签名
Signature signature = Signature.getInstance("SHA256withRSA");
signature.initSign(keyPair.getPrivate());
signature.update("Hello".getBytes());
byte[] signed = signature.sign();

// 验证
signature.initVerify(keyPair.getPublic());
signature.update("Hello".getBytes());
boolean valid = signature.verify(signed);
```

### EdDSA (JDK 15+, JEP 339)

```java
// Ed25519 (现代签名算法, 高性能、固定时间实现)
KeyPairGenerator keyGen = KeyPairGenerator.getInstance("Ed25519");
KeyPair keyPair = keyGen.generateKeyPair();

Signature sig = Signature.getInstance("Ed25519");
sig.initSign(keyPair.getPrivate());
sig.update("Hello".getBytes());
byte[] signed = sig.sign();

// Ed448 (更高安全级别, 224-bit security)
KeyPairGenerator keyGen448 = KeyPairGenerator.getInstance("Ed448");
KeyPair keyPair448 = keyGen448.generateKeyPair();
```

### ML-DSA 签名 (JDK 24+, JEP 497)

后量子数字签名，详见 [第 7 节](#7-后量子密码-pqc)。

---

## 6. TLS 演进详解

### TLS 版本在 JDK 中的支持历史

JDK 对 TLS 协议的支持经历了完整的生命周期——从引入、默认启用到最终禁用旧版本：

| 协议版本 | 引入版本 | 默认启用 | 禁用版本 | RFC |
|----------|----------|----------|----------|-----|
| SSL 2.0 | JDK 1.2 | JDK 1.2 | JDK 6u19 (2010) 已移除 | - |
| SSL 3.0 | JDK 1.2 | JDK 1.2 | JDK 8u31 (POODLE 攻击后) | RFC 6101 |
| TLS 1.0 | JDK 1.4 | JDK 1.4 | JDK 12 默认禁用, JDK 20 移除 | RFC 2246 |
| TLS 1.1 | JDK 7 | JDK 7 | JDK 12 默认禁用, JDK 20 移除 | RFC 4346 |
| TLS 1.2 | JDK 7 | JDK 8 | 仍然支持 | RFC 5246 |
| TLS 1.3 | JDK 11 (JEP 332) | JDK 13 | 当前推荐 | RFC 8446 |
| DTLS 1.0 | JDK 9 | JDK 9 | 仍然支持 | RFC 4347 |
| DTLS 1.2 | JDK 15 (JEP 373) | JDK 15 | 当前推荐 | RFC 6347 |

### JSSE 架构 (Java Secure Socket Extension)

JSSE 是 JDK 中 TLS/SSL 协议的实现框架，核心组件包括：

```
┌─────────────────────────────────────────────────┐
│                  应用层                           │
│   HttpsURLConnection / HttpClient / SSLSocket    │
└─────────────────────┬───────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│               SSLContext                          │
│   - 持有 KeyManager[] + TrustManager[]           │
│   - 创建 SSLSocketFactory / SSLEngine            │
│   - 配置协议版本、密码套件                         │
└──────┬──────────────┬───────────────────────────┘
       │              │
┌──────▼──────┐ ┌─────▼──────────────────────────┐
│  SSLSocket  │ │  SSLEngine                      │
│             │ │                                  │
│ 阻塞 I/O   │ │ 非阻塞 I/O (NIO)                │
│ 简单场景   │ │ 高性能服务器 (Netty, gRPC 等)    │
│ 直接读写   │ │ 需要手动管理缓冲区               │
│             │ │ wrap()/unwrap() 模型             │
└─────────────┘ └─────────────────────────────────┘
       │              │
┌──────▼──────────────▼───────────────────────────┐
│          Handshake Protocol (握手协议)            │
│   1. ClientHello → 协议版本、密码套件、扩展       │
│   2. ServerHello → 选定密码套件、证书             │
│   3. 密钥交换 (ECDHE / ML-KEM)                   │
│   4. Finished → 握手完成, 开始加密通信            │
└──────┬──────────────────────────────────────────┘
       │
┌──────▼──────────────────────────────────────────┐
│   KeyManager          │  TrustManager            │
│   管理客户端/服务端    │  验证对端证书             │
│   自身的密钥和证书     │  信任链检查               │
│   (KeyStore)          │  (TrustStore/cacerts)     │
└─────────────────────────────────────────────────┘
```

**SSLContext** — TLS 配置的中心。通过 `SSLContext.getInstance("TLSv1.3")` 获取实例，然后用 `init(KeyManager[], TrustManager[], SecureRandom)` 初始化。

**SSLSocket** — 基于阻塞 I/O 的 TLS 套接字，适合简单的客户端连接。直接继承自 `java.net.Socket`，使用方式与普通 Socket 相同。

**SSLEngine** — 基于非阻塞 I/O 的 TLS 引擎，适合高性能场景。Netty、gRPC、Undertow 等框架均使用 SSLEngine。它不直接进行 I/O，而是通过 `wrap()` (加密出站数据) 和 `unwrap()` (解密入站数据) 操作缓冲区。

### TLS 1.3 的关键改进

TLS 1.3 (RFC 8446, JEP 332) 相比 TLS 1.2 有根本性改进：

| 改进项 | TLS 1.2 | TLS 1.3 |
|--------|---------|---------|
| 握手往返 | 2-RTT | 1-RTT (首次), 0-RTT (重连) |
| 密钥交换 | RSA / ECDHE / DHE (可选) | 仅 (EC)DHE (前向安全强制) |
| 加密模式 | CBC / GCM / CCM | 仅 AEAD (GCM, ChaCha20-Poly1305) |
| 握手加密 | ServerHello 后明文 | ServerHello 后立即加密 |
| 密码套件数量 | 约 300+ (含不安全) | 仅 5 个 (均安全) |
| 0-RTT | 不支持 | 支持 (early data) |
| PSK | 不原生支持 | 原生支持 (会话恢复) |

**TLS 1.3 的 5 个密码套件** (JDK 中全部支持):
- `TLS_AES_256_GCM_SHA384`
- `TLS_AES_128_GCM_SHA256`
- `TLS_CHACHA20_POLY1305_SHA256`
- `TLS_AES_128_CCM_SHA256`
- `TLS_AES_128_CCM_8_SHA256`

### TLS 1.3 配置代码示例

```java
import javax.net.ssl.*;
import java.security.*;

// === 基础 TLS 1.3 客户端配置 ===
SSLContext sslContext = SSLContext.getInstance("TLSv1.3");
sslContext.init(null, null, null);  // 使用默认 TrustStore

SSLSocketFactory factory = sslContext.getSocketFactory();
SSLSocket socket = (SSLSocket) factory.createSocket("example.com", 443);

// 仅启用 TLS 1.3
socket.setEnabledProtocols(new String[]{"TLSv1.3"});

// 指定 TLS 1.3 密码套件
socket.setEnabledCipherSuites(new String[]{
    "TLS_AES_256_GCM_SHA384",
    "TLS_CHACHA20_POLY1305_SHA256"
});

socket.startHandshake();
SSLSession session = socket.getSession();
System.out.println("Protocol: " + session.getProtocol());       // TLSv1.3
System.out.println("Cipher:   " + session.getCipherSuite());
```

```java
// === SSLEngine 配置 (用于 NIO / Netty 等框架) ===
SSLContext ctx = SSLContext.getInstance("TLSv1.3");
ctx.init(null, null, null);

SSLEngine engine = ctx.createSSLEngine("example.com", 443);
engine.setUseClientMode(true);

// 配置 ALPN (Application-Layer Protocol Negotiation)
SSLParameters params = engine.getSSLParameters();
params.setApplicationProtocols(new String[]{"h2", "http/1.1"});
params.setProtocols(new String[]{"TLSv1.3", "TLSv1.2"});
engine.setSSLParameters(params);

// wrap/unwrap 模型
// engine.wrap(appBuffer, netBuffer);    // 加密出站数据
// engine.unwrap(netBuffer, appBuffer);  // 解密入站数据
```

```java
// === 完整的双向 TLS (mTLS) 服务端配置 ===
// 加载服务端 KeyStore (含私钥 + 证书)
KeyStore keyStore = KeyStore.getInstance("PKCS12");
keyStore.load(new FileInputStream("server.p12"), "password".toCharArray());

KeyManagerFactory kmf = KeyManagerFactory.getInstance("SunX509");
kmf.init(keyStore, "password".toCharArray());

// 加载 TrustStore (用于验证客户端证书)
KeyStore trustStore = KeyStore.getInstance("PKCS12");
trustStore.load(new FileInputStream("truststore.p12"), "password".toCharArray());

TrustManagerFactory tmf = TrustManagerFactory.getInstance("SunX509");
tmf.init(trustStore);

SSLContext sslContext = SSLContext.getInstance("TLSv1.3");
sslContext.init(kmf.getKeyManagers(), tmf.getTrustManagers(), null);

SSLServerSocketFactory ssf = sslContext.getServerSocketFactory();
SSLServerSocket serverSocket = (SSLServerSocket) ssf.createServerSocket(8443);
serverSocket.setNeedClientAuth(true);  // 要求客户端证书 (mTLS)
serverSocket.setEnabledProtocols(new String[]{"TLSv1.3"});
```

### TLS 1.3 的 0-RTT 和 PSK 模式

**0-RTT (Early Data)** — TLS 1.3 允许在握手完成前发送应用数据 (early data)，实现零往返延迟。但 0-RTT 数据存在重放攻击风险 (replay attack)，因此仅适用于幂等操作。

JDK 中 0-RTT 的限制：
- JDK 11 的 TLS 1.3 实现 **不支持发送** 0-RTT 数据 (客户端侧)
- 服务端可配置是否接受 0-RTT 数据
- 这是有意为之的安全考量：0-RTT 数据不具备前向安全性且可被重放

**PSK (Pre-Shared Key)** — TLS 1.3 使用 PSK 进行会话恢复 (session resumption)，取代了 TLS 1.2 的 session ID 和 session ticket 机制。JDK 的 JSSE 实现自动管理 PSK 的生命周期：

```java
// PSK 会话恢复是自动的，由 SSLSession 管理
SSLContext ctx = SSLContext.getInstance("TLSv1.3");
ctx.init(null, null, null);

// 第一次连接: 完整握手 (1-RTT)
SSLSocket socket1 = (SSLSocket) ctx.getSocketFactory()
    .createSocket("example.com", 443);
socket1.startHandshake();
SSLSession session = socket1.getSession();
socket1.close();

// 第二次连接: PSK 恢复握手 (更快)
// JSSE 自动使用缓存的 PSK 进行会话恢复
SSLSocket socket2 = (SSLSocket) ctx.getSocketFactory()
    .createSocket("example.com", 443);
socket2.startHandshake();
// session.isValid() 检查会话是否仍可恢复
```

### 调试 TLS 连接

```bash
# 完整的 SSL 调试输出
java -Djavax.net.debug=ssl:handshake:verbose MyApp

# 仅显示握手过程
java -Djavax.net.debug=ssl:handshake MyApp

# 显示密钥材料 (仅调试, 勿在生产环境使用)
java -Djavax.net.debug=ssl:keygen MyApp

# 显示会话缓存活动
java -Djavax.net.debug=ssl:session MyApp

# 系统属性控制
-Djdk.tls.client.protocols=TLSv1.3         # 客户端协议列表
-Djdk.tls.server.protocols=TLSv1.3         # 服务端协议列表
-Djdk.tls.ephemeralDHKeySize=2048           # DH 临时密钥大小
-Djdk.tls.rejectClientInitiatedRenegotiation=true  # 禁止重协商
```

---

## 7. 后量子密码 (PQC)

### 量子威胁与迁移背景

量子计算机一旦达到足够规模 (预计 2030-2040 年)，Shor 算法可以在多项式时间内破解 RSA 和 ECC——当前互联网安全的基石。这意味着：
- RSA-2048 密钥可被量子计算机在数小时内破解
- ECDSA/ECDHE (P-256, P-384) 同样不再安全
- 对称加密 (AES) 和哈希 (SHA) 受 Grover 算法影响较小，密钥长度翻倍即可

更紧迫的是 **"先存后解" (Harvest Now, Decrypt Later)** 攻击：攻击者现在截获加密通信，等量子计算机可用后再解密。因此后量子迁移需要尽早开始。

NIST 在 2024 年 8 月正式发布了首批后量子密码标准：
- **FIPS 203**: ML-KEM (基于 Module-Lattice 的密钥封装机制)
- **FIPS 204**: ML-DSA (基于 Module-Lattice 的数字签名)
- **FIPS 205**: SLH-DSA (基于哈希的无状态签名, JDK 尚未实现)

### ML-KEM — 后量子密钥封装 (JEP 496, JDK 24)

ML-KEM (Module-Lattice-Based Key Encapsulation Mechanism) 用于安全地建立共享密钥，取代传统的 RSA 密钥传输和 ECDH 密钥协商。

```java
import javax.crypto.KEM;
import java.security.*;

// === ML-KEM 密钥封装完整示例 ===

// 1. 生成 ML-KEM 密钥对 (接收方)
KeyPairGenerator kpg = KeyPairGenerator.getInstance("ML-KEM");
kpg.initialize(NamedParameterSpec.ML_KEM_768);  // NIST Level 3, 推荐默认
KeyPair receiverKeyPair = kpg.generateKeyPair();

// 2. 发送方: 使用接收方公钥进行封装 (encapsulate)
//    生成一个共享密钥 + 密文 (发送给接收方)
KEM kemSender = KEM.getInstance("ML-KEM");
KEM.Encapsulator encapsulator = kemSender.newEncapsulator(receiverKeyPair.getPublic());
KEM.Encapsulated encapsulated = encapsulator.encapsulate();

byte[] ciphertext = encapsulated.encapsulation();  // 发送给接收方
SecretKey sharedKeySender = encapsulated.key();     // 发送方的共享密钥

// 3. 接收方: 使用私钥解封装 (decapsulate)
//    从密文中恢复相同的共享密钥
KEM kemReceiver = KEM.getInstance("ML-KEM");
KEM.Decapsulator decapsulator = kemReceiver.newDecapsulator(receiverKeyPair.getPrivate());
SecretKey sharedKeyReceiver = decapsulator.decapsulate(ciphertext);

// sharedKeySender 与 sharedKeyReceiver 相同
// 后续可用此共享密钥进行 AES-GCM 对称加密通信
```

```java
// === 三个参数集的选择 ===

// ML-KEM-512: NIST Level 1 (128-bit 安全), 适合一般应用
kpg.initialize(NamedParameterSpec.ML_KEM_512);
// 公钥 800 字节, 密文 768 字节

// ML-KEM-768: NIST Level 3 (192-bit 安全), 推荐默认
kpg.initialize(NamedParameterSpec.ML_KEM_768);
// 公钥 1184 字节, 密文 1088 字节

// ML-KEM-1024: NIST Level 5 (256-bit 安全), 高安全场景
kpg.initialize(NamedParameterSpec.ML_KEM_1024);
// 公钥 1568 字节, 密文 1568 字节
```

### ML-DSA — 后量子数字签名 (JEP 497, JDK 24)

ML-DSA (Module-Lattice-Based Digital Signature Algorithm) 用于生成和验证数字签名，取代 RSA 和 ECDSA。

```java
import java.security.*;

// === ML-DSA 签名完整示例 ===

// 1. 生成 ML-DSA 密钥对
KeyPairGenerator kpg = KeyPairGenerator.getInstance("ML-DSA");
kpg.initialize(NamedParameterSpec.ML_DSA_65);  // NIST Level 3, 推荐默认
KeyPair keyPair = kpg.generateKeyPair();

// 2. 签名
Signature signer = Signature.getInstance("ML-DSA");
signer.initSign(keyPair.getPrivate());
signer.update("Hello Post-Quantum World".getBytes());
byte[] signature = signer.sign();
// 签名大小约 3309 字节 (ML-DSA-65)

// 3. 验证
Signature verifier = Signature.getInstance("ML-DSA");
verifier.initVerify(keyPair.getPublic());
verifier.update("Hello Post-Quantum World".getBytes());
boolean valid = verifier.verify(signature);
System.out.println("Signature valid: " + valid);
```

```java
// === ML-DSA 参数集选择 ===

// ML-DSA-44: NIST Level 2, 一般签名
kpg.initialize(NamedParameterSpec.ML_DSA_44);
// 公钥 1312 字节, 签名 2420 字节

// ML-DSA-65: NIST Level 3, 推荐默认
kpg.initialize(NamedParameterSpec.ML_DSA_65);
// 公钥 1952 字节, 签名 3309 字节

// ML-DSA-87: NIST Level 5, 高安全场景
kpg.initialize(NamedParameterSpec.ML_DSA_87);
// 公钥 2592 字节, 签名 4627 字节
```

### ML-DSA JAR 签名 (JEP 518, JDK 26)

JDK 26 将 ML-DSA 扩展到 JAR 签名场景，保护 Java 软件供应链免受量子威胁：

```bash
# 使用 keytool 生成 ML-DSA 密钥对
keytool -genkeypair -alias mykey -keyalg ML-DSA \
    -keysize ML-DSA-65 -keystore mystore.p12 \
    -dname "CN=My App, O=My Org"

# 使用 jarsigner 用 ML-DSA 签名 JAR
jarsigner -keystore mystore.p12 myapp.jar mykey

# 验证签名
jarsigner -verify -verbose myapp.jar
```

### 混合密钥交换策略

在后量子迁移过渡期，推荐使用 **混合 (hybrid)** 方案——同时使用经典算法和后量子算法。这样即使其中一种算法被攻破，另一种仍然提供安全保障。

**JEP 527 (JDK 27, 计划)** — TLS 1.3 混合密钥交换：

| 命名组 | 经典算法 | PQ 算法 | 安全级别 | 说明 |
|--------|----------|---------|----------|------|
| X25519MLKEM768 | X25519 | ML-KEM-768 | NIST 3 | Chrome/Firefox 已支持此组合 |
| SecP256r1MLKEM768 | ECDHE P-256 | ML-KEM-768 | NIST 3 | 兼容传统基础设施 |
| SecP384r1MLKEM1024 | ECDHE P-384 | ML-KEM-1024 | NIST 5 | 最高安全级别 |

混合方案的原理：经典 ECDHE 和 ML-KEM 各自独立生成共享密钥，然后将两个共享密钥通过 KDF (如 HKDF) 组合成最终密钥。只要任一算法安全，最终密钥就是安全的。

### PQC 迁移路径建议

```
阶段 1 (现在): 盘点 — 识别所有使用 RSA/ECC 的地方
    │
    ▼
阶段 2 (JDK 24+): 试验 — 在非关键系统测试 ML-KEM/ML-DSA
    │
    ▼
阶段 3 (JDK 27+): 混合模式 — TLS 使用混合密钥交换
    │                        JAR 签名使用 ML-DSA
    ▼
阶段 4 (未来): 纯 PQ — 当经典算法正式被认为不安全时
                       全面切换到后量子算法
```

---

## 8. Key Derivation Function API

### 背景

密钥派生函数 (Key Derivation Function, KDF) 从一个输入密钥材料 (Input Keying Material, IKM) 派生出一个或多个加密密钥。KDF 在以下场景至关重要：
- TLS 1.3 握手后从共享密钥派生会话密钥
- 从密码 (password) 派生加密密钥 (PBKDF2 等)
- 从 ECDH/ML-KEM 协商结果派生对称密钥
- 密钥轮换 (key rotation)

JDK 24 引入 KDF API 预览版 (JEP 478)，JDK 25 正式化 (JEP 510)。之前 JDK 中没有标准的 KDF API，开发者需要手动使用 HMAC 实现 HKDF，或依赖第三方库。

### HKDF (HMAC-based Key Derivation Function)

HKDF (RFC 5869) 是最重要的 KDF，分为两步：
1. **Extract**: 从输入密钥材料中提取固定长度的伪随机密钥 (PRK)
2. **Expand**: 从 PRK 派生出所需长度的输出密钥

```java
import javax.crypto.KDF;
import javax.crypto.SecretKey;
import javax.crypto.spec.HKDFParameterSpec;

// === HKDF 完整示例 (JDK 25+) ===

// 1. 获取 HKDF 实例
KDF hkdf = KDF.getInstance("HKDF-SHA256");

// 2. 输入密钥材料 (例如来自 ML-KEM 或 ECDH 协商的共享密钥)
SecretKey ikm = ...;  // 输入密钥材料
byte[] salt = "my-salt".getBytes();
byte[] info = "tls13-derived-key".getBytes();

// 3. Extract + Expand (一步完成)
HKDFParameterSpec params = HKDFParameterSpec.extractThenExpand(
    ikm,          // 输入密钥材料
    salt,         // 盐值 (可选但推荐)
    info,         // 上下文信息
    32            // 输出密钥长度 (256 bits)
);
SecretKey derivedKey = hkdf.deriveKey("AES", params);

// 4. 也可以分步执行
// Extract 阶段
HKDFParameterSpec extractParams = HKDFParameterSpec.extract(ikm, salt);
SecretKey prk = hkdf.deriveKey("HKDF-PRK", extractParams);

// Expand 阶段
HKDFParameterSpec expandParams = HKDFParameterSpec.expand(prk, info, 32);
SecretKey expandedKey = hkdf.deriveKey("AES", expandParams);
```

### KDF 在 TLS 1.3 中的作用

TLS 1.3 的密钥调度 (Key Schedule) 大量依赖 HKDF。握手完成后，多个密钥通过 HKDF 的 Extract-Expand 链式派生：

```
PSK (或 0) ──Extract──► Early Secret
                           │
                       Derive-Secret──► client_early_traffic_secret (0-RTT)
                           │
(EC)DHE ────Extract──► Handshake Secret
                           │
                       Derive-Secret──► client_handshake_traffic_secret
                       Derive-Secret──► server_handshake_traffic_secret
                           │
             Extract──► Master Secret
                           │
                       Derive-Secret──► client_application_traffic_secret
                       Derive-Secret──► server_application_traffic_secret
```

每个 `Derive-Secret` 操作都是一次 `HKDF-Expand-Label` 调用。JEP 510 的 KDF API 使得 JSSE 内部可以使用标准化的 Java API 进行这些密钥派生操作。

---

## 9. PEM API

### 背景

PEM (Privacy-Enhanced Mail) 是密码学对象 (密钥、证书、CSR 等) 最常见的文本编码格式。在 JEP 470/524 之前，JDK 没有标准的 PEM 编解码 API，开发者需要手动处理 Base64 头尾标记和 DER 编码转换。

### PEM 编码示例 (JEP 470 预览, JDK 25; JEP 524 预览 2, JDK 26)

```java
import java.security.*;
import java.security.spec.*;

// === PEM 编码 (JDK 26, 预览功能) ===

// 生成 EC 密钥对
KeyPairGenerator kpg = KeyPairGenerator.getInstance("EC");
kpg.initialize(new ECGenParameterSpec("secp256r1"));
KeyPair keyPair = kpg.generateKeyPair();

// 将公钥编码为 PEM 格式字符串
// PEM 类在 JDK 26 中从 PEMRecord 重命名为 PEM (JEP 524)
String pemPublicKey = PEM.encode(keyPair.getPublic());
// 输出:
// -----BEGIN PUBLIC KEY-----
// MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE...
// -----END PUBLIC KEY-----

// 将私钥编码为 PEM
String pemPrivateKey = PEM.encode(keyPair.getPrivate());
// -----BEGIN PRIVATE KEY-----
// MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEH...
// -----END PRIVATE KEY-----

// 从 PEM 字符串解码回密钥对象
PublicKey decodedPubKey = PEM.decode(pemPublicKey, PublicKey.class);
PrivateKey decodedPrivKey = PEM.decode(pemPrivateKey, PrivateKey.class);
```

```java
// === PEM 编码证书 ===
import java.security.cert.*;

// 加载 X.509 证书
CertificateFactory cf = CertificateFactory.getInstance("X.509");
X509Certificate cert = (X509Certificate)
    cf.generateCertificate(new FileInputStream("server.crt"));

// 编码为 PEM
String pemCert = PEM.encode(cert);
// -----BEGIN CERTIFICATE-----
// MIIDazCCAlOgAwIBAgIUB...
// -----END CERTIFICATE-----

// 从 PEM 解码回证书
X509Certificate decodedCert = PEM.decode(pemCert, X509Certificate.class);
```

### PEM API 的设计要点

| 方面 | 说明 |
|------|------|
| 类名变化 | JDK 25 (JEP 470) 中叫 `PEMRecord`，JDK 26 (JEP 524) 重命名为 `PEM` |
| 支持类型 | `PublicKey`, `PrivateKey`, `X509Certificate`, `X509CRL`, `PKCS10CertRequest` |
| 加密私钥 | 支持 PKCS#8 加密格式 (encrypted PEM) |
| 线程安全 | `PEM.encode()` 和 `PEM.decode()` 均为线程安全的静态方法 |
| 预览状态 | JDK 26 仍为预览，需要 `--enable-preview` 编译和运行 |

---

## 10. 序列化安全

### 反序列化攻击原理

Java 序列化 (`ObjectInputStream.readObject()`) 是历史上最严重的安全攻击面之一。反序列化攻击利用 **gadget chain** (工具链)——一系列可被串联的类，在反序列化过程中触发任意代码执行。

攻击原理简述：

```
恶意序列化数据
    │
    ▼
ObjectInputStream.readObject()
    │
    ▼ 调用目标类的 readObject()/readResolve()
    │
    ▼ 触发 gadget chain (例如: HashMap → TiedMapEntry → LazyMap
    │   → ChainedTransformer → InvokerTransformer)
    │
    ▼ 最终调用 Runtime.exec("恶意命令")
```

著名的 gadget chain 包括：
- **Commons Collections**: `InvokerTransformer` 链，2015 年 Apache Commons Collections 漏洞
- **Spring Framework**: `MethodInvokeTypeProvider` 链
- **JNDI Injection**: 通过 `InitialContext.lookup()` 加载远程代码 (Log4Shell 变体)

### JEP 290: 序列化过滤器 (JDK 9)

JEP 290 引入了 **ObjectInputFilter**，允许在反序列化之前检查和拒绝危险的类：

```java
import java.io.*;

// === 基于模式的过滤器 (Pattern-based Filter) ===
ObjectInputStream ois = new ObjectInputStream(inputStream);

// 设置过滤器: 允许特定类, 拒绝其他
ObjectInputFilter filter = ObjectInputFilter.Config.createFilter(
    "com.myapp.dto.*;java.util.*;!*"
    // com.myapp.dto 包下的类: 允许
    // java.util 包下的类: 允许
    // 其他所有类: 拒绝 (!*)
);
ois.setObjectInputFilter(filter);

Object obj = ois.readObject();  // 只有通过过滤器的类才能反序列化
```

```java
// === 限制对象图大小 ===
ObjectInputFilter sizeFilter = ObjectInputFilter.Config.createFilter(
    "maxdepth=5;maxrefs=100;maxbytes=1000000;maxarray=1000"
    // maxdepth: 对象图最大深度
    // maxrefs:  最大引用数
    // maxbytes: 最大字节数
    // maxarray: 数组最大长度
);
```

```java
// === 编程式过滤器 ===
ObjectInputFilter customFilter = filterInfo -> {
    Class<?> clazz = filterInfo.serialClass();
    if (clazz != null) {
        // 拒绝所有 java.lang.reflect 包下的类
        if (clazz.getPackageName().startsWith("java.lang.reflect")) {
            return ObjectInputFilter.Status.REJECTED;
        }
        // 拒绝 Runtime 类 (防止命令执行)
        if (clazz == Runtime.class || clazz == ProcessBuilder.class) {
            return ObjectInputFilter.Status.REJECTED;
        }
    }
    return ObjectInputFilter.Status.ALLOWED;
};
ois.setObjectInputFilter(customFilter);
```

### JEP 415: 上下文序列化过滤器 (JDK 17)

JEP 290 的过滤器是 per-stream 的 (每个 ObjectInputStream 单独设置)，容易遗漏。JEP 415 引入了 **filter factory**，可以为整个 JVM 设置全局过滤器工厂：

```java
// === JVM 级别的过滤器工厂 (JDK 17+) ===
ObjectInputFilter.Config.setSerialFilterFactory((current, next) -> {
    // current: 流级别的过滤器 (如果有)
    // next:    JVM 全局默认过滤器
    // 返回的过滤器将被应用

    // 组合策略: 流级别过滤器优先, 全局过滤器兜底
    if (current == null) {
        return next;  // 没有流级别过滤器, 使用全局的
    }
    // 合并: 两个过滤器都必须通过
    return filterInfo -> {
        ObjectInputFilter.Status status = current.checkInput(filterInfo);
        if (status == ObjectInputFilter.Status.REJECTED) {
            return ObjectInputFilter.Status.REJECTED;
        }
        return next.checkInput(filterInfo);
    };
});
```

```bash
# 通过 JVM 属性设置全局过滤器 (无需修改代码)
java -Djdk.serialFilter="!org.apache.commons.collections.**;!java.lang.Runtime" MyApp
```

### 序列化安全演进总结

| 版本 | 特性 | 说明 |
|------|------|------|
| JDK 1.1 | ObjectInputStream | 引入序列化, 无安全机制 |
| JDK 9 | JEP 290: ObjectInputFilter | per-stream 过滤器, 白名单/黑名单 |
| JDK 17 | JEP 415: Filter Factory | JVM 全局过滤器工厂, 上下文感知 |
| JDK 未来 | 逐步限制 | 长期目标是默认禁止反序列化不可信数据 |

---

## 11. Security Manager 消亡史

### 完整时间线

Java 的 Security Manager 是最初 Applet 时代的沙箱安全核心，经历了从核心地位到彻底移除的完整生命周期：

```
JDK 1.0 (1996)  SecurityManager 诞生
    │            ── Applet 沙箱模型: 不可信代码在受限环境运行
    │            ── 概念简洁: 网络代码不能访问本地文件系统
    │
JDK 1.2 (1998)  细粒度权限模型
    │            ── 引入 Policy, Permission, ProtectionDomain
    │            ── AccessController.doPrivileged() 特权操作
    │            ── 从全有全无变为细粒度权限控制
    │
JDK 1.4 (2002)  JAAS 集成
    │            ── 基于 Subject 的授权
    │            ── 与认证框架结合
    │
JDK 6 (2006)    复杂度巅峰
    │            ── Policy 文件语法复杂
    │            ── 实际使用率极低 (大多数应用不启用 SM)
    │            ── 维护成本高, 每个新 API 都要考虑权限检查
    │
JDK 9 (2017)    JPMS 提供替代
    │            ── 模块系统 (JEP 261) 提供强封装
    │            ── 内部 API 不再可直接访问
    │            ── 模块边界成为新的安全屏障
    │
JDK 17 (2021)   JEP 411: 弃用 Security Manager
    │            ── 正式标记为 deprecated for removal
    │            ── 运行时启用 SM 会打印警告
    │            ── 社区反响: 大部分赞成, 少数框架 (如 Elasticsearch) 反对
    │
JDK 18-23       持续推进
    │            ── 逐步减少 JDK 内部对 SM 的依赖
    │            ── 清理 doPrivileged 调用
    │
JDK 24 (2025)   JEP 486: 永久禁用
                 ── Security Manager 相关 API 抛出 UnsupportedOperationException
                 ── System.setSecurityManager() 始终抛异常
                 ── -Djava.security.manager 系统属性被忽略
                 ── 代码仍存在但不可用, 后续版本将彻底移除
```

### 为什么要移除 Security Manager?

1. **使用率极低**: 绝大多数 Java 应用从未启用 Security Manager。据 Oracle 调查，只有不到 1% 的生产应用使用它。

2. **维护负担巨大**: JDK 中每个涉及 I/O、网络、反射的 API 都包含 `SecurityManager.check*()` 调用。这些检查遍布数千个文件，增加了代码复杂度和新特性开发成本。

3. **安全模型已过时**: Security Manager 基于 "代码来源" (code origin) 的信任模型——来自本地的代码可信，来自网络的不可信。这个模型在 Applet 时代有意义，但在现代微服务/容器化部署中不适用。

4. **性能开销**: 每次 I/O、网络、反射操作都要检查权限栈，影响 JIT 优化和应用性能。

5. **绕过容易**: 历史上多次出现 Security Manager 绕过漏洞 (sandbox escape)，证明它并非可靠的安全边界。

### 替代方案

| 替代方案 | 适用场景 | 说明 |
|----------|----------|------|
| **JPMS 模块系统** | API 封装 | 模块的 `exports`/`opens` 控制包的可见性，比 Security Manager 的 AccessController 更简洁可靠 |
| **容器隔离** | 进程级隔离 | Docker/Kubernetes 的 seccomp、AppArmor、namespace 提供操作系统级别的沙箱 |
| **JVM 沙箱 (GraalVM)** | 代码隔离 | GraalVM 的 Truffle 沙箱为嵌入语言提供隔离 |
| **代码审计 + 依赖扫描** | 供应链安全 | 结合 ML-DSA JAR 签名 (JEP 518) 验证依赖完整性 |
| **最小权限容器** | 部署安全 | 以 non-root 用户、只读文件系统、无网络 (除所需端口) 运行 |

---

## 12. 密钥管理

### KeyStore

```java
import java.security.*;
import java.io.*;

// 创建 PKCS12 KeyStore (JDK 9+ 默认格式)
KeyStore keyStore = KeyStore.getInstance("PKCS12");
keyStore.load(null, null);

// 存储密钥
SecretKey key = ...;
keyStore.setKeyEntry("mykey", key, "password".toCharArray(), null);

// 保存到文件
try (FileOutputStream fos = new FileOutputStream("keystore.p12")) {
    keyStore.store(fos, "password".toCharArray());
}

// 加载 KeyStore
KeyStore loaded = KeyStore.getInstance("PKCS12");
try (FileInputStream fis = new FileInputStream("keystore.p12")) {
    loaded.load(fis, "password".toCharArray());
}

// 获取密钥
Key storedKey = loaded.getKey("mykey", "password".toCharArray());
```

### 证书

```java
import java.security.cert.*;
import java.io.*;

// 加载 X.509 证书
CertificateFactory cf = CertificateFactory.getInstance("X.509");
try (FileInputStream fis = new FileInputStream("cert.pem")) {
    X509Certificate cert = (X509Certificate) cf.generateCertificate(fis);

    // 验证证书
    cert.checkValidity();

    // 获取信息
    Principal subject = cert.getSubjectX500Principal();
    Principal issuer = cert.getIssuerX500Principal();
    Date notBefore = cert.getNotBefore();
    Date notAfter = cert.getNotAfter();
}
```

### KeyStore 类型演进

| 类型 | 引入版本 | 状态 | 说明 |
|------|----------|------|------|
| JKS | JDK 1.2 | 弃用 (JDK 26 警告) | Java 专有格式, 仅支持私钥 |
| JCEKS | JDK 1.4 | 弃用 | JKS 增强版, 支持对称密钥 |
| **PKCS12** | JDK 1.4 | **推荐 (JDK 9+ 默认)** | 行业标准, 跨平台兼容 |
| PKCS11 | JDK 5 | 特殊场景 | 硬件安全模块 (HSM) 接口 |

---

## 13. 最佳实践

### 密码选择 (2025 年推荐)

| 用途 | 推荐算法 | 后量子替代 |
|------|----------|------------|
| 对称加密 | AES-256-GCM | (AES 仍安全, 量子影响小) |
| 非对称加密 | RSA-2048+ / ECDSA | ML-KEM (密钥封装) |
| 数字签名 | Ed25519 / SHA256withRSA | ML-DSA |
| 消息摘要 | SHA-256 / SHA-3 | (哈希仍安全) |
| HMAC | HMAC-SHA256 | (HMAC 仍安全) |
| 密钥协商 | ECDHE (X25519) | X25519MLKEM768 (混合) |
| TLS | TLS 1.3 | TLS 1.3 + 混合密钥交换 |
| 密钥派生 | HKDF-SHA256 | (KDF 仍安全) |
| JAR 签名 | SHA256withRSA | ML-DSA (JEP 518) |

### 常见错误

```java
// ❌ 不要使用
Cipher.getInstance("DES");                   // 弱加密, 56-bit 密钥
Cipher.getInstance("AES/ECB/PKCS5Padding");  // ECB 模式不安全
MessageDigest.getInstance("MD5");            // 碰撞已被证明
MessageDigest.getInstance("SHA-1");          // 已弃用于签名
Cipher.getInstance("RSA/ECB/PKCS1Padding");  // 易受 Bleichenbacher 攻击
new ObjectInputStream(untrustedInput).readObject();  // 反序列化攻击

// ✅ 推荐
Cipher.getInstance("AES/GCM/NoPadding");                      // AEAD 认证加密
Cipher.getInstance("RSA/ECB/OAEPWithSHA-256AndMGF1Padding");  // RSA-OAEP
MessageDigest.getInstance("SHA-256");                          // 安全哈希
KEM.getInstance("ML-KEM");                                     // 后量子密钥封装
Signature.getInstance("ML-DSA");                               // 后量子签名
```

### 安全配置检查清单

```
□ TLS 版本 ≥ 1.2 (推荐 1.3)
□ 禁用不安全密码套件 (RC4, DES, 3DES, CBC without MAC-then-Encrypt)
□ 使用 AEAD 加密模式 (GCM, ChaCha20-Poly1305)
□ 密钥长度: RSA ≥ 2048, ECC ≥ 256, AES ≥ 128
□ 序列化过滤器已配置 (JEP 290/415)
□ KeyStore 类型为 PKCS12 (非 JKS)
□ 证书链完整且有效
□ 不信任所有证书 (TrustAllCerts 仅限测试)
□ 评估后量子迁移计划
```

---

## 14. 相关链接

### 本地文档

- [安全时间线](timeline.md) - JDK 1.0 至 JDK 26 安全特性完整演进
- [国际化](../i18n/) - 字符编码
- [网络](../../concurrency/network/) - SSL/TLS

### 外部参考

**JEP 文档:**
- [JEP 290: Filter Incoming Serialization Data](https://openjdk.org/jeps/290)
- [JEP 332: Transport Layer Security (TLS) 1.3](https://openjdk.org/jeps/332)
- [JEP 411: Deprecate the Security Manager for Removal](https://openjdk.org/jeps/411)
- [JEP 415: Context-Specific Deserialization Filters](https://openjdk.org/jeps/415)
- [JEP 452: Key Encapsulation Mechanism API](https://openjdk.org/jeps/452)
- [JEP 478: Key Derivation Function API (Preview)](https://openjdk.org/jeps/478)
- [JEP 486: Permanently Disable the Security Manager](https://openjdk.org/jeps/486)
- [JEP 496: Quantum-Resistant Module-Lattice-Based Key Encapsulation Mechanism](https://openjdk.org/jeps/496)
- [JEP 497: Quantum-Resistant Module-Lattice-Based Digital Signature Algorithm](https://openjdk.org/jeps/497)
- [JEP 510: Key Derivation Function API](https://openjdk.org/jeps/510)
- [JEP 518: ML-DSA JAR Signatures](https://openjdk.org/jeps/518)
- [JEP 524: PEM Encodings of Cryptographic Objects (Second Preview)](https://openjdk.org/jeps/524)
- [JEP 527: Post-Quantum Hybrid Key Exchange for TLS 1.3](https://openjdk.org/jeps/527)

**技术文档:**
- [Oracle Java Security Guide](https://docs.oracle.com/en/java/javase/21/security/)
- [Oracle Security Providers](https://docs.oracle.com/en/java/javase/21/security/oracle-providers.html)
- [OpenJDK Security Group](https://openjdk.org/groups/security/)
- [NIST Post-Quantum Cryptography](https://csrc.nist.gov/projects/post-quantum-cryptography)
- [RFC 8446: TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446)
- [RFC 5869: HKDF](https://www.rfc-editor.org/rfc/rfc5869)
