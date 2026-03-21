# 安全特性演进时间线

加密、TLS、后量子密码的发展历程。

---
## 目录

1. [时间线概览](#1-时间线概览)
2. [密码学基础](#2-密码学基础)
3. [TLS/SSL 演进](#3-tlsssl-演进)
4. [加密算法演进](#4-加密算法演进)
5. [后量子密码](#5-后量子密码)
6. [KDF API (JEP 510)](#6-kdf-api-jep-510)
7. [PEM 格式支持 (JEP 470 / JEP 524)](#7-pem-格式支持-jep-470--jep-524)
8. [安全配置建议](#8-安全配置建议)
9. [完整示例](#9-完整示例)
10. [时间线总结](#10-时间线总结)
11. [相关链接](#11-相关链接)

---


## 1. 时间线概览

```
JDK 8 ── JDK 11 ── JDK 15 ── JDK 17 ── JDK 21 ── JDK 24 ── JDK 25 ── JDK 26
 │          │          │          │          │          │          │          │
TLS 1.2   TLS 1.3   禁用弱    KMAC       KEM API   ML-KEM    KDF API   PEM
(默认)    (默认)    算法     SHA-3      JEP 452   JEP 496   JEP 510   JEP 524
          JEP 332             JEP 370              ML-DSA    PEM       HPKE
          ChaCha20                                 JEP 497   JEP 470   JAR签名
          JEP 329                                                      ML-DSA
```

---

## 2. 密码学基础

### 对称加密 vs 非对称加密

```
┌─────────────────────────────────────────────────────────┐
│                 加密算法分类                             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  对称加密                    非对称加密                   │
│  ┌─────────────┐             ┌─────────────┐            │
│  │ AES, ChaCha │             │ RSA, ECDSA  │            │
│  │ DES, 3DES   │             │ ML-DSA      │            │
│  └─────────────┘             └─────────────┘            │
│         │                           │                   │
│         ▼                           ▼                   │
│  ┌─────────────────┐       ┌─────────────────┐          │
│  │  加解密同密钥    │       │  公钥加密       │          │
│  │  速度快         │       │  私钥解密       │          │
│  │  适合大量数据   │       │  速度慢         │          │
│  │  密钥分发困难   │       │  密钥分发方便   │          │
│  └─────────────────┘       └─────────────────┘          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 哈希算法

| 算法 | 输出长度 | 状态 | 说明 |
|------|----------|------|------|
| MD5 | 128 位 | 已破解 | 禁用 |
| SHA-1 | 160 位 | 已破解 | 禁用 |
| SHA-256 | 256 位 | 安全 | 推荐 |
| SHA-3 | 可变 | 安全 | JDK 17+ |
| SHAKE | 可变 | 安全 | JDK 17+ |

---

## 3. TLS/SSL 演进

### TLS 协议版本

```
┌─────────────────────────────────────────────────────────┐
│                   TLS 协议演进                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  SSL 1.0 (1994)  - 未公开发布                            │
│       ↓                                                 │
│  SSL 2.0 (1995)  - 已废弃，存在严重安全漏洞              │
│       ↓                                                 │
│  SSL 3.0 (1996)  - 已废弃 (POODLE 攻击)                 │
│       ↓                                                 │
│  TLS 1.0 (1999)  - 已废弃 (BEAST 攻击)                  │
│       ↓                                                 │
│  TLS 1.1 (2006)  - 已废弃                               │
│       ↓                                                 │
│  TLS 1.2 (2008)  - JDK 8 默认                           │
│       ↓                                                 │
│  TLS 1.3 (2018)  - JDK 11 默认                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### TLS 1.3 改进 (JEP 332)

#### 握手对比

```
┌─────────────────────────────────────────────────────────┐
│              TLS 1.2 vs TLS 1.3 握手                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  TLS 1.2                    TLS 1.3                     │
│  ─────────                 ─────────                    │
│  Client ──ClientHello──> Server                          │
│          <──ServerHello──                               │
│          <──Certificate──                               │
│          <──ServerHelloDone──                           │
│  Client ──ClientKeyExchange──> Server                    │
│          <──ServerHelloDone──                           │
│  Client ──ChangeCipherSpec──> Server                    │
│          <──ChangeCipherSpec──                          │
│  Client ──Finished────> Server                           │
│          <──Finished────                                │
│                                                         │
│  2-RTT (最少)                1-RTT                       │
│  不支持 0-RTT                支持 0-RTT 恢复             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

#### 密码套件简化

| TLS 1.2 | TLS 1.3 |
|---------|---------|
| 37+ 套件 | 5 套件 |
| RSA 密钥交换 | 仅 (EC)DHE |
| 可选前向安全 | 强制前向安全 |
| CBC/GCM 模式 | 仅 AEAD |

### TLS 配置

```java
// 创建 TLS 1.3 SSLContext
SSLContext sslContext = SSLContext.getInstance("TLSv1.3");
sslContext.init(null, null, null);

// 或者使用默认 (JDK 11+ 自动使用 TLS 1.3)
SSLContext sslContext = SSLContext.getDefault();

// 创建 SSLSocketFactory
SSLSocketFactory factory = sslContext.getSocketFactory();

// 创建 HttpsURLConnection
HttpsURLConnection.setDefaultSSLSocketFactory(factory);

// 配置 HTTPS Client
HttpClient client = HttpClient.newBuilder()
    .sslContext(sslContext)
    .sslParameters(sslContext.getDefaultSSLParameters())
    .build();
```

### TLS 配置文件

```bash
# $JAVA_HOME/conf/security/java.security

# 启用 TLS 1.3
jdk.tls.client.protocols=TLSv1.3,TLSv1.2
jdk.tls.server.protocols=TLSv1.3,TLSv1.2

# 禁用弱密码套件
jdk.tls.disabledAlgorithms=\
    SSLv3, TLSv1, TLSv1.1, \
    RC4, DES, MD5, \
    CBC, \
    TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384, \
    TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384

# 密钥大小限制
jdk.tls.keySize=2048

# 签名算法限制
jdk.tls.disabledAlgorithms=\
    SHA1, RSA keySize < 2048, DSA keySize < 2048
```

---

## 4. 加密算法演进

### JDK 8 - 基础加密

```java
import javax.crypto.*;
import javax.crypto.spec.*;
import java.security.*;

// AES 加密
public class AESExample {
    private static final String ALGO = "AES/CBC/PKCS5Padding";

    public static byte[] encrypt(byte[] plaintext, SecretKey key, IvParameterSpec iv)
        throws Exception {

        Cipher cipher = Cipher.getInstance(ALGO);
        cipher.init(Cipher.ENCRYPT_MODE, key, iv);
        return cipher.doFinal(plaintext);
    }

    public static byte[] decrypt(byte[] ciphertext, SecretKey key, IvParameterSpec iv)
        throws Exception {

        Cipher cipher = Cipher.getInstance(ALGO);
        cipher.init(Cipher.DECRYPT_MODE, key, iv);
        return cipher.doFinal(ciphertext);
    }

    // 生成密钥和 IV
    public static void main(String[] args) throws Exception {
        KeyGenerator keyGen = KeyGenerator.getInstance("AES");
        keyGen.init(256);
        SecretKey key = keyGen.generateKey();

        byte[] iv = new byte[16];
        SecureRandom random = new SecureRandom();
        random.nextBytes(iv);
        IvParameterSpec ivSpec = new IvParameterSpec(iv);

        byte[] encrypted = encrypt("Hello".getBytes(), key, ivSpec);
        byte[] decrypted = decrypt(encrypted, key, ivSpec);
    }
}
```

### JDK 11 - ChaCha20-Poly1305 (JEP 329)

#### 算法原理

```
┌─────────────────────────────────────────────────────────┐
│            ChaCha20-Poly1305 架构                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Plaintext                                              │
│      │                                                  │
│      ▼                                                  │
│  ┌─────────────────┐                                   │
│  │   ChaCha20      │  流密码 (加密)                     │
│  │  (256-bit key)  │                                   │
│  │  (96-bit nonce) │                                   │
│  └────────┬────────┘                                   │
│           │                                             │
│           ▼                                             │
│  ┌─────────────────┐                                   │
│  │   Poly1305      │  MAC (认证)                        │
│  │   (AEAD)        │                                   │
│  └────────┬────────┘                                   │
│           │                                             │
│           ▼                                             │
│     Ciphertext + Tag                                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

#### 使用示例

```java
import javax.crypto.*;
import javax.crypto.spec.*;
import java.security.*;

// ChaCha20-Poly1305
public class ChaCha20Example {

    // 生成密钥和 nonce
    public static KeyPair generateChaCha20Key() throws Exception {
        KeyGenerator keyGen = KeyGenerator.getInstance("ChaCha20");
        return keyGen.generateKeyPair();
    }

    // 加密
    public static byte[] encrypt(byte[] plaintext, SecretKey key, byte[] nonce)
        throws Exception {

        Cipher cipher = Cipher.getInstance("ChaCha20-Poly1305/None/NoPadding");
        cipher.init(Cipher.ENCRYPT_MODE, key, new IvParameterSpec(nonce));
        return cipher.doFinal(plaintext);
    }

    // 解密
    public static byte[] decrypt(byte[] ciphertext, SecretKey key, byte[] nonce)
        throws Exception {

        Cipher cipher = Cipher.getInstance("ChaCha20-Poly1305/None/NoPadding");
        cipher.init(Cipher.DECRYPT_MODE, key, new IvParameterSpec(nonce));
        return cipher.doFinal(ciphertext);
    }

    public static void main(String[] args) throws Exception {
        // 生成密钥
        KeyGenerator keyGen = KeyGenerator.getInstance("ChaCha20");
        keyGen.init(256);
        SecretKey key = keyGen.generateKey();

        // 生成 nonce (96-bit = 12 bytes)
        byte[] nonce = new byte[12];
        SecureRandom random = new SecureRandom();
        random.nextBytes(nonce);

        // 加密
        byte[] plaintext = "Hello, ChaCha20!".getBytes();
        byte[] encrypted = encrypt(plaintext, key, nonce);

        // 解密
        byte[] decrypted = decrypt(encrypted, key, nonce);
        System.out.println(new String(decrypted));
    }
}
```

#### ChaCha20 vs AES-GCM

| 特性 | AES-GCM | ChaCha20-Poly1305 |
|------|---------|-------------------|
| 硬件加速 | x86 AES-NI | 软件实现 |
| 性能 (x86) | 高 (~10GB/s) | 中等 (~2GB/s) |
| 性能 (ARM/移动) | 中等 | 高 |
| 密钥大小 | 128/256 位 | 256 位 |
| Nonce 大小 | 96 位 | 96 位 |
| 认证加密 | 是 (AEAD) | 是 (AEAD) |

### JDK 17 - KMAC & SHA-3 (JEP 370)

#### SHA-3 家族

```java
import java.security.*;

// SHA3-256
MessageDigest md3 = MessageDigest.getInstance("SHA3-256");
byte[] hash3 = md3.digest("Hello".getBytes());

// SHAKE128 (可变输出)
MessageDigest shake = MessageDigest.getInstance("SHAKE128");
shake.update("Hello".getBytes());
byte[] hash128 = shake.digest(32);  // 32 字节输出

// SHAKE256
MessageDigest shake256 = MessageDigest.getInstance("SHAKE256");
shake256.update("Hello".getBytes());
byte[] hash256 = shake256.digest(64);  // 64 字节输出
```

#### KMAC (Keccak Message Authentication Code)

```java
import javax.crypto.*;
import javax.crypto.spec.*;
import java.security.*;

// KMAC256
public class KMACExample {

    public static byte[] computeMac(byte[] data, byte[] key, byte[] custom)
        throws Exception {

        KMACParameterSpec params = new KMACParameterSpec(
            256,                    // 输出长度 (bit)
            custom                  // 自定义字符串
        );

        Mac mac = Mac.getInstance("KMAC256");
        SecretKeySpec keySpec = new SecretKeySpec(key, "KMAC256");
        mac.init(keySpec, params);

        return mac.doFinal(data);
    }

    public static void main(String[] args) throws Exception {
        byte[] key = "my-secret-key".getBytes();
        byte[] custom = "my-application".getBytes();
        byte[] data = "Hello, KMAC!".getBytes();

        byte[] mac = computeMac(data, key, custom);
        System.out.println("KMAC: " + bytesToHex(mac));
    }

    private static String bytesToHex(byte[] bytes) {
        StringBuilder sb = new StringBuilder();
        for (byte b : bytes) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }
}
```

---

## 5. 后量子密码

### 背景

```
传统公钥密码算法的脆弱性:
┌─────────────────────────────────────────────────────────┐
│  算法        │  密钥大小    │  量子计算机破解时间        │
├─────────────────────────────────────────────────────────┤
│  RSA-2048   │  256 字节   │  数小时 (Shor 算法)        │
│  RSA-4096   │  512 字节   │  数小时                     │
│  ECDSA-P256 │  64 字节    │  数小时                     │
│  Ed25519    │  32 字节    │  数小时                     │
├─────────────────────────────────────────────────────────┤
│  ML-DSA-87  │  ~2.5 KB     │  仍然安全 (无已知量子算法)  │
│  ML-KEM-1024│  ~1.5 KB     │  仍然安全                  │
└─────────────────────────────────────────────────────────┘
```

### JDK 24 - ML-DSA (JEP 497)

基于 FIPS 204 的后量子签名算法，JDK 24 交付。

```java
import java.security.*;

// ML-DSA 签名
public class MLDSAExample {

    // 生成密钥对
    public static KeyPair generateKeyPair(String algorithm) throws Exception {
        KeyPairGenerator kpg = KeyPairGenerator.getInstance(algorithm);
        return kpg.generateKeyPair();
    }

    // 签名
    public static byte[] sign(byte[] data, PrivateKey privateKey) throws Exception {
        String algorithm = privateKey.getAlgorithm();
        Signature sig = Signature.getInstance(algorithm);
        sig.initSign(privateKey);
        sig.update(data);
        return sig.sign();
    }

    // 验证
    public static boolean verify(byte[] data, byte[] signature, PublicKey publicKey)
        throws Exception {

        String algorithm = publicKey.getAlgorithm();
        Signature sig = Signature.getInstance(algorithm);
        sig.initVerify(publicKey);
        sig.update(data);
        return sig.verify(signature);
    }

    public static void main(String[] args) throws Exception {
        // ML-DSA 有三个安全级别
        String[] algorithms = {"ML-DSA-44", "ML-DSA-65", "ML-DSA-87"};

        for (String algo : algorithms) {
            System.out.println("Testing " + algo);

            // 生成密钥
            KeyPair kp = generateKeyPair(algo);

            // 签名
            byte[] data = "Hello, Post-Quantum!".getBytes();
            byte[] signature = sign(data, kp.getPrivate());
            System.out.println("  Signature size: " + signature.length + " bytes");

            // 验证
            boolean valid = verify(data, signature, kp.getPublic());
            System.out.println("  Valid: " + valid);
        }
    }
}
```

#### ML-DSA 安全级别

| 算法 | NIST 类别 | 密钥大小 | 签名大小 | 安全强度 |
|------|-----------|----------|----------|----------|
| ML-DSA-44 | 2 | ~1.3 KB | ~2.4 KB | ~128-bit |
| ML-DSA-65 | 3 | ~1.6 KB | ~3.3 KB | ~192-bit |
| ML-DSA-87 | 5 | ~2.0 KB | ~4.6 KB | ~256-bit |

### JDK 24 - ML-KEM (JEP 496, 密钥封装)

```java
import javax.crypto.*;
import java.security.*;

// ML-KEM 密钥封装
public class MLKEMExample {

    // 生成密钥对
    public static KeyPair generateKeyPair() throws Exception {
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("ML-KEM");
        return kpg.generateKeyPair();
    }

    // 封装 (发送方)
    public static Encapsulated encapsulate(PublicKey publicKey, SecretKey sharedSecret)
        throws Exception {

        Cipher cipher = Cipher.getInstance("ML-KEM");
        cipher.init(Cipher.WRAP_MODE, publicKey);

        // 封装共享密钥
        byte[] encapsulated = cipher.wrap(sharedSecret);
        return new Encapsulated(encapsulated, sharedSecret);
    }

    // 解封装 (接收方)
    public static SecretKey decapsulate(byte[] encapsulated, KeyPair keyPair)
        throws Exception {

        Cipher cipher = Cipher.getInstance("ML-KEM");
        cipher.init(Cipher.UNWRAP_MODE, keyPair.getPrivate());

        return (SecretKey) cipher.unwrap(encapsulated, "AES", Cipher.SECRET_KEY);
    }

    record Encapsulated(byte[] data, SecretKey sharedSecret) {}
}
```

---

## 6. KDF API (JEP 510)

### 演进历程

| 版本 | 状态 | JEP |
|------|------|-----|
| JDK 24 | 预览 | JEP 478 |
| JDK 25 | **正式** | JEP 510 |

### KDF 基础

```
┌─────────────────────────────────────────────────────────┐
│                 KDF 工作原理                             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  主密钥 (Master Key)                                    │
│      │                                                  │
│      ▼                                                  │
│  ┌─────────────────┐                                   │
│  │      KDF        │                                   │
│  │  ┌───────────┐  │                                   │
│  │  │ Salt      │  │                                   │
│  │  │ Info      │  │                                   │
│  │  │ Length    │  │                                   │
│  │  └───────────┘  │                                   │
│  └────────┬────────┘                                   │
│           │                                             │
│           ▼                                             │
│  ┌─────────────────────────────────┐                    │
│  │  子密钥 1 │ 子密钥 2 │ 子密钥 3 │                    │
│  └─────────────────────────────────┘                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### HKDF 使用

```java
import javax.crypto.KDF;
import javax.crypto.spec.*;
import java.security.*;

// HKDF (HMAC-based KDF)
public class KDFExample {

    public static void hkdfExample() throws Exception {
        // 输入密钥材料 (IKM)
        byte[] ikm = "my-input-key-material".getBytes();

        // Salt
        byte[] salt = new byte[32];
        SecureRandom random = new SecureRandom();
        random.nextBytes(salt);

        // Info (可选上下文信息)
        byte[] info = "my-application-context".getBytes();

        // 创建 KDF
        KDF kdf = KDF.getInstance("HKDF-SHA256");

        // 派生密钥参数
        SecretKeySpec saltKey = new SecretKeySpec(salt, "HKDF-SHA256");
        KDFParameters params = new KDFParameters(
            saltKey,    // 盐值
            info,       // 上下文信息
            256        // 输出密钥长度 (bit)
        );

        // 派生密钥
        SecretKey derivedKey = kdf.deriveKey("derived-key", ikm, params);

        System.out.println("Derived key: " +
            bytesToHex(derivedKey.getEncoded()));
    }

    // 从主密钥派生多个子密钥
    public static void deriveMultipleKeys() throws Exception {
        byte[] masterKey = new byte[32];
        new SecureRandom().nextBytes(masterKey);

        KDF kdf = KDF.getInstance("HKDF-SHA256");
        SecretKeySpec saltKey = new SecretKeySpec(new byte[32], "HKDF-SHA256");

        // 加密密钥
        KDFParameters encParams = new KDFParameters(
            saltKey,
            "encryption".getBytes(),
            256
        );
        SecretKey encKey = kdf.deriveKey("enc", masterKey, encParams);

        // 认证密钥
        KDFParameters authParams = new KDFParameters(
            saltKey,
            "authentication".getBytes(),
            256
        );
        SecretKey authKey = kdf.deriveKey("auth", masterKey, authParams);

        System.out.println("Encryption key: " + bytesToHex(encKey.getEncoded()));
        System.out.println("Auth key: " + bytesToHex(authKey.getEncoded()));
    }

    private static String bytesToHex(byte[] bytes) {
        StringBuilder sb = new StringBuilder();
        for (byte b : bytes) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }
}
```

### 支持的 KDF 算法

| 算法 | 说明 | 用途 |
|------|------|------|
| HKDF-SHA256 | HMAC-based KDF (SHA-256) | 通用密钥派生 |
| HKDF-SHA384 | HMAC-based KDF (SHA-384) | 更高安全需求 |
| HKDF-SHA512 | HMAC-based KDF (SHA-512) | 最高安全需求 |
| PBKDF2-HMAC-SHA256 | Password-based KDF | 从密码派生密钥 |
| PBKDF2-HMAC-SHA512 | Password-based KDF | 从密码派生密钥 |

---

## 7. PEM 格式支持 (JEP 470 / JEP 524)

### PEM 格式示例

```
-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC...
-----END PRIVATE KEY-----

-----BEGIN CERTIFICATE-----
MIIDXTCCAkWgAwIBAgIJAKL0UG+mRKqzMA0GCSqGSIb3DQEBCwUAMEU...
-----END CERTIFICATE-----

-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEAE9s5vBT8zGQ2Y2g3c2Y2g...
-----END PUBLIC KEY-----
```

### PEM 读写

```java
import java.security.*;
import java.security.spec.*;
import java.security.pem.*;
import java.nio.file.*;

// PEM 格式支持 (JDK 25 预览 JEP 470, JDK 26 第二次预览 JEP 524)
public class PEMExample {

    // 读取 PEM 格式的私钥
    public static PrivateKey readPrivateKey(String pemFile) throws Exception {
        String pem = Files.readString(Paths.get(pemFile));

        // 解析 PEM
        byte[] der = PemParser.parse(pem);

        // 生成私钥
        KeyFactory kf = KeyFactory.getInstance("RSA");
        return kf.generatePrivate(new PKCS8EncodedKeySpec(der));
    }

    // 读取 PEM 格式的证书
    public static Certificate readCertificate(String pemFile) throws Exception {
        String pem = Files.readString(Paths.get(pemFile));

        CertificateFactory cf = CertificateFactory.getInstance("X.509");
        return cf.generateCertificate(
            new ByteArrayInputStream(pem.getBytes())
        );
    }

    // 写入 PEM 格式
    public static void writePrivateKey(PrivateKey key, String pemFile) throws Exception {
        String pem = PemWriter.encode(key);
        Files.writeString(Paths.get(pemFile), pem);
    }

    public static void main(String[] args) throws Exception {
        // 生成密钥对
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("RSA");
        kpg.initialize(2048);
        KeyPair kp = kpg.generateKeyPair();

        // 保存为 PEM
        writePrivateKey(kp.getPrivate(), "private.pem");

        // 读取 PEM
        PrivateKey readKey = readPrivateKey("private.pem");
        System.out.println("Key restored: " + readKey.getAlgorithm());
    }
}
```

---

## 8. 安全配置建议

### java.security 配置

```bash
# $JAVA_HOME/conf/security/java.security

# ===== TLS 配置 =====
# 启用 TLS 1.3
jdk.tls.client.protocols=TLSv1.3,TLSv1.2
jdk.tls.server.protocols=TLSv1.3,TLSv1.2

# 禁用弱密码套件
jdk.tls.disabledAlgorithms=\
    SSLv3, TLSv1, TLSv1.1, \
    RC4, DES, MD5, \
    CBC, \
    TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384

# ===== 签名算法限制 =====
jdk.jar.disabledAlgorithms=\
    MD2, MD5, RSA keySize < 1024, \
    DSA keySize < 1024, \
    include jdk.disabled.namedCurves

# ===== 密钥大小限制 =====
jdk.tls.keySize=2048

# ===== 证书验证 =====
# 启用 OCSP
jdk.security.caDnSuffix=cn=CA
ocsp.enable=true
```

### 代码安全实践

```java
// ✅ 推荐: 使用强加密算法
Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
MessageDigest md = MessageDigest.getInstance("SHA-256");
Mac mac = Mac.getInstance("HmacSHA256");

// ❌ 避免: 使用弱算法
Cipher cipher = Cipher.getInstance("DES/ECB/PKCS5Padding");
MessageDigest md = MessageDigest.getInstance("MD5");
Mac mac = Mac.getInstance("HmacMD5");

// ✅ 推荐: 使用安全随机数
SecureRandom random = SecureRandom.getInstanceStrong();
byte[] salt = new byte[16];
random.nextBytes(salt);

// ❌ 避免: 使用伪随机数
Random random = new Random();  // 不适合安全用途
```

---

## 9. 完整示例

### 安全 HTTP 客户端

```java
import javax.net.ssl.*;
import java.net.http.*;
import java.security.cert.*;
import java.security.*;

public class SecureHttpClient {
    private final HttpClient client;

    public SecureHttpClient() throws Exception {
        // 创建 TLS 1.3 SSLContext
        SSLContext sslContext = SSLContext.getInstance("TLSv1.3");
        sslContext.init(null, null, new SecureRandom());

        // 配置 SSLParameters
        SSLParameters sslParams = sslContext.getDefaultSSLParameters();
        sslParams.setEndpointIdentificationAlgorithm("HTTPS");

        this.client = HttpClient.newBuilder()
            .version(HttpClient.Version.HTTP_3)
            .sslContext(sslContext)
            .sslParameters(sslParams)
            .connectTimeout(Duration.ofSeconds(10))
            .build();
    }

    public String get(String url) throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(url))
            .GET()
            .build();

        HttpResponse<String> response = client.send(request,
            HttpResponse.BodyHandlers.ofString());

        if (response.statusCode() >= 400) {
            throw new RuntimeException("HTTP error: " + response.statusCode());
        }

        return response.body();
    }
}
```

### 后量子加密示例

```java
import java.security.*;

public class PostQuantumCrypto {

    // 混合加密 (传统 + 后量子)
    public static byte[] hybridSign(byte[] data,
                                      KeyPair traditionalKey,
                                      KeyPair pqKey) throws Exception {

        // 传统签名
        Signature tradSig = Signature.getInstance("Ed25519");
        tradSig.initSign(traditionalKey.getPrivate());
        tradSig.update(data);
        byte[] tradSignature = tradSig.sign();

        // 后量子签名
        Signature pqSig = Signature.getInstance("ML-DSA");
        pqSig.initSign(pqKey.getPrivate());
        pqSig.update(data);
        byte[] pqSignature = pqSig.sign();

        // 组合签名
        byte[] combined = new byte[tradSignature.length + pqSignature.length];
        System.arraycopy(tradSignature, 0, combined, 0, tradSignature.length);
        System.arraycopy(pqSignature, 0, combined, tradSignature.length, pqSignature.length);

        return combined;
    }

    // 混合验证
    public static boolean hybridVerify(byte[] data, byte[] combined,
                                        PublicKey traditionalKey,
                                        PublicKey pqKey) throws Exception {

        int tradLen = combined.length / 2;

        // 传统验证
        byte[] tradSignature = new byte[tradLen];
        System.arraycopy(combined, 0, tradSignature, 0, tradLen);
        Signature tradSig = Signature.getInstance("Ed25519");
        tradSig.initVerify(traditionalKey);
        tradSig.update(data);
        boolean tradValid = tradSig.verify(tradSignature);

        // 后量子验证
        byte[] pqSignature = new byte[combined.length - tradLen];
        System.arraycopy(combined, tradLen, pqSignature, 0, pqSignature.length);
        Signature pqSig = Signature.getInstance("ML-DSA");
        pqSig.initVerify(pqKey);
        pqSig.update(data);
        boolean pqValid = pqSig.verify(pqSignature);

        return tradValid && pqValid;
    }
}
```

---

## 10. 时间线总结

| 版本 | 特性 | JEP | 说明 |
|------|------|-----|------|
| JDK 8 | TLS 1.2 | - | 默认 TLS 版本 |
| JDK 8 | AES-GCM | - | 认证加密 |
| JDK 11 | **TLS 1.3** | JEP 332 | 更快更强的握手 |
| JDK 11 | **ChaCha20-Poly1305** | JEP 329 | 现代加密算法 |
| JDK 15 | 禁用弱签名 | - | 移除 DSA 1024 位 |
| JDK 17 | **KMAC** | JEP 370 | SHA-3 家族 MAC |
| JDK 17 | **SHA-3** | JEP 370 | Keccak 哈希 |
| JDK 21 | **KEM API** | JEP 452 | 密钥封装机制 API |
| JDK 21 | HSS/LMS | - | 后量子状态哈希签名 |
| JDK 24 | **ML-KEM** | JEP 496 | 后量子密钥封装 (FIPS 203) |
| JDK 24 | **ML-DSA** | JEP 497 | 后量子签名 (FIPS 204) |
| JDK 24 | KDF API (预览) | JEP 478 | 密钥派生函数预览 |
| JDK 25 | **KDF API** | JEP 510 | 密钥派生标准化 (HKDF) |
| JDK 25 | PEM 格式 (预览) | JEP 470 | 密钥格式支持预览 |
| JDK 25 | TLS 安全增强 | - | SHA-1 禁用于 TLS 1.2 握手签名 |
| JDK 26 | PEM 格式 (预览 2) | JEP 524 | PEMRecord 重命名为 PEM |
| JDK 26 | **HPKE** | - | 混合公钥加密 (RFC 9180) |
| JDK 26 | ML-DSA JAR 签名 | - | 后量子 JAR 签名支持 |
| JDK 27 | PQ TLS 1.3 | JEP 527 | 后量子混合密钥交换 |

---

## 11. 相关链接

- [JEP 332](/jeps/security/jep-332.md)
- [JEP 329](/jeps/security/jep-329.md)
- [JEP 370](/jeps/ffi/jep-370.md)
- [JEP 496](/jeps/security/jep-496.md)
- [JEP 497](/jeps/security/jep-497.md)
- [JEP 510](/jeps/security/jep-510.md)
- [JEP 470](/jeps/security/jep-470.md)
- [JEP 524](/jeps/security/jep-524.md)
- [JEP 527](/jeps/security/jep-527.md)
- [NIST Post-Quantum Cryptography](https://csrc.nist.gov/projects/post-quantum-cryptography)
