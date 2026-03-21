# 加密与安全

> Cipher, Signature, MessageDigest, Key, SSL/TLS 演进历程

[← 返回主题索引](../)

---

## 1. 快速概览

```
JDK 1.0 ── JDK 1.4 ── JDK 7 ── JDK 11 ── JDK 21 ── JDK 24 ── JDK 25 ── JDK 26
   │         │        │        │        │        │        │        │
JCE      JCE    TLS1.2  TLS1.3  KEM     ML-KEM  KDF     HPKE
框架    可选   (完整   ChaCha  API     ML-DSA  API     PEM
              支持)   Poly    JEP452  JEP496  JEP510  JEP524
                      1305            JEP497
```

### 核心演进

| 版本 | 特性 | JEP | 说明 |
|------|------|-----|------|
| **JDK 1.0** | JCE 框架 | - | 基础加密 API |
| **JDK 1.4** | JCE 集成 | - | JCE 成为标准部分 |
| **JDK 7** | TLS 1.2 | - | 完整 TLS 1.2 支持 |
| **JDK 11** | TLS 1.3 | JEP 332 | 新密码套件, ChaCha20-Poly1305 (JEP 329) |
| **JDK 21** | KEM API | JEP 452 | 密钥封装机制框架 |
| **JDK 24** | ML-KEM | JEP 496 | 后量子密钥封装 (FIPS 203) |
| **JDK 24** | ML-DSA | JEP 497 | 后量子签名 (FIPS 204) |
| **JDK 25** | KDF API | JEP 510 | 密钥派生函数 (HKDF) |
| **JDK 25** | PEM 编码 (预览) | JEP 470 | 密钥/证书 PEM 格式 |
| **JDK 26** | HPKE | - | 混合公钥加密 (RFC 9180) |
| **JDK 26** | PEM 编码 (预览 2) | JEP 524 | PEMRecord 重命名为 PEM |

---

## 目录

- [JCE 框架](#jce-框架)
- [消息摘要](#消息摘要)
- [对称加密](#对称加密)
- [非对称加密](#非对称加密)
- [数字签名](#数字签名)
- [密钥管理](#密钥管理)
- [SSL/TLS](#ssltls)
- [最佳实践](#最佳实践)
- [核心贡献者](#核心贡献者)
- [相关链接](#相关链接)

---

## 2. JCE 框架

**Java Cryptography Extension**

### 基础概念

```java
import javax.crypto.*;

// Cipher 对象
// transformation: 算法/模式/填充
Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");

// 初始化
// 加密模式: ENCRYPT_MODE
// 解密模式: DECRYPT_MODE
// 包装模式: WRAP_MODE / UNWRAP_MODE
cipher.init(Cipher.ENCRYPT_MODE, key);
```

### JCE 提供者

```java
// 查看可用提供者
Provider[] providers = Security.getProviders();
for (Provider provider : providers) {
    System.out.println(provider.getName());
}

// 指定提供者
Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding", "SunJCE");
```

---

## 3. 消息摘要

### MessageDigest

```java
import java.security.*;

// 常用算法
String[] algorithms = {"MD5", "SHA-1", "SHA-256", "SHA-384", "SHA-512", "SHA3-256"};

// SHA-256 (推荐)
MessageDigest digest = MessageDigest.getInstance("SHA-256");
byte[] hash = digest.digest("Hello, World!".getBytes());

// 十六进制输出
String hex = bytesToHex(hash);
System.out.println(hex);  // SHA-256 hash

// 工具方法
private static String bytesToHex(byte[] bytes) {
    StringBuilder hex = new StringBuilder();
    for (byte b : bytes) {
        hex.append(String.format("%02x", b));
    }
    return hex.toString();
}
```

### 算法对比

| 算法 | 输出长度 | 安全性 | 用途 |
|------|----------|--------|------|
| MD5 | 128位 | ❌ 不安全 | 文件校验 (遗留) |
| SHA-1 | 160位 | ⚠️ 弱安全 | 遗留系统 |
| SHA-256 | 256位 | ✅ 安全 | 通用 |
| SHA-384 | 384位 | ✅ 安全 | 高安全需求 |
| SHA-512 | 512位 | ✅ 安全 | 高安全需求 |
| SHA-3-256 | 256位 | ✅ 安全 | 替代 SHA-2 选择 |

---

## 4. 对称加密

### Cipher (AES)

```java
import javax.crypto.*;
import javax.crypto.spec.*;
import java.security.*;

// 生成密钥
KeyGenerator keyGen = KeyGenerator.getInstance("AES");
keyGen.init(256);  // 128, 192, 256
SecretKey key = keyGen.generateKey();

// 或使用指定密钥
byte[] keyBytes = "1234567890123456".getBytes();
SecretKey key = new SecretKeySpec(keyBytes, "AES");

// 加密
Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
cipher.init(Cipher.ENCRYPT_MODE, key, new IvParameterSpec(iv));

byte[] plaintext = "Hello, AES!".getBytes();
byte[] ciphertext = cipher.doFinal(plaintext);

// 解密
cipher.init(Cipher.DECRYPT_MODE, key, new IvParameterSpec(iv));
byte[] decrypted = cipher.doFinal(ciphertext);
```

### 加密模式

| 模式 | 特点 | 安全性 |
|------|------|--------|
| **ECB** | 简单，并行 | ❌ 不安全 |
| **CBC** | 链式，需要 IV | ✅ 安全 |
| **CTR** | 流式，并行 | ✅ 安全 |
| **GCM** | 认证加密 (AEAD) | ✅ 推荐 |
| **CFB** | 流式 | ⚠️ 需注意 |

### GCM 模式 (推荐)

```java
// AES-GCM (认证加密)
Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
SecretKey key = new SecretKeySpec(keyBytes, "AES");
GCMParameterSpec gcmSpec = new GCMParameterSpec(128, iv);
cipher.init(Cipher.ENCRYPT_MODE, key, gcmSpec);

byte[] ciphertext = cipher.doFinal(plaintext);

// GCM 包含认证标签
byte[] tag = cipher.getIV();  // 初始化向量
```

### 填充模式

| 模式 | 说明 |
|------|------|
| **NoPadding** | 无填充，数据需对齐 |
| **PKCS5Padding** | PKCS#5 填充 (最常用) |
| **ISO10126Padding** | ISO 10126 填充 |

---

## 5. 非对称加密

### KeyPair 生成

```java
import java.security.*;

// RSA 密钥对生成
KeyPairGenerator keyGen = KeyPairGenerator.getInstance("RSA");
keyGen.initialize(2048);  // 1024, 2048, 4096
KeyPair keyPair = keyGen.generateKeyPair();

PublicKey publicKey = keyPair.getPublic();
PrivateKey privateKey = keyPair.getPrivate();

// 保存密钥
byte[] publicKeyBytes = publicKey.getEncoded();
byte[] privateKeyBytes = privateKey.getEncoded();
```

### RSA 加密/解密

```java
import javax.crypto.*;

// RSA 加密
Cipher cipher = Cipher.getInstance("RSA/ECB/PKCS1Padding");
cipher.init(Cipher.ENCRYPT_MODE, publicKey);

byte[] plaintext = "Hello, RSA!".getBytes();
byte[] ciphertext = cipher.doFinal(plaintext);

// RSA 解密
cipher.init(Cipher.DECRYPT_MODE, privateKey);
byte[] decrypted = cipher.doFinal(ciphertext);
```

### RSA 限制

| 密钥大小 | 最大加密数据 |
|----------|-------------|
| 1024 | 117 字节 |
| 2048 | 245 字节 |
| 4096 | 501 字节 |

> **注意**: RSA 只适合加密少量数据，实际应使用混合加密

### 混合加密

```java
// 1. 生成会话密钥
SecretKey sessionKey = KeyGenerator.getInstance("AES").generateKey();

// 2. 用会话密钥加密数据
Cipher aesCipher = Cipher.getInstance("AES/GCM/NoPadding");
aesCipher.init(Cipher.ENCRYPT_MODE, sessionKey);
byte[] encryptedData = aesCipher.doFinal(plaintext);

// 3. 用 RSA 加密会话密钥
Cipher rsaCipher = Cipher.getInstance("RSA/ECB/PKCS1Padding");
rsaCipher.init(Cipher.ENCRYPT_MODE, publicKey);
byte[] encryptedKey = rsaCipher.doFinal(sessionKey.getEncoded());

// 发送: encryptedKey + encryptedData
```

---

## 6. 数字签名

### 签名

```java
import java.security.*;

// 生成密钥对
KeyPairGenerator keyGen = KeyPairGenerator.getInstance("RSA");
keyGen.initialize(2048);
KeyPair keyPair = keyGen.generateKeyPair();

// 签名
PrivateKey privateKey = keyPair.getPrivate();
Signature signature = Signature.getInstance("SHA256withRSA");
signature.initSign(privateKey);
signature.update("Hello, Signature!".getBytes());
byte[] signatureBytes = signature.sign();
```

### 验证

```java
// 验证签名
PublicKey publicKey = keyPair.getPublic();
Signature signature = Signature.getInstance("SHA256withRSA");
signature.initVerify(publicKey);
signature.update("Hello, Signature!".getBytes());
boolean valid = signature.verify(signatureBytes);

System.out.println("Signature valid: " + valid);
```

### 签名算法

| 算法 | 说明 |
|------|------|
| **SHA256withRSA** | 推荐 |
| **SHA384withRSA** | 高安全 |
| **SHA512withRSA** | 最高安全 |
| **SHA256withECDSA** | ECDSA |
| **Ed25519** | 现代算法 |

---

## 7. 密钥管理

### KeyStore

```java
import java.io.*;
import java.security.*;

// 创建 KeyStore
KeyStore keyStore = KeyStore.getInstance("PKCS12");
keyStore.load(null, null);  // 创建空 KeyStore

// 存储密钥
keyStore.setKeyEntry("mykey",
    privateKey,
    new char[]{'p', 'a', 's', 's', 'w', 'o', 'r', 'd'},
    new Certificate[]{cert});

// 保存 KeyStore
try (FileOutputStream fos = new FileOutputStream("keystore.p12")) {
    keyStore.store(fos, "password".toCharArray());
}

// 加载 KeyStore
try (FileInputStream fis = new FileInputStream("keystore.p12")) {
    keyStore.load(fis, "password".toCharArray());
}

// 读取密钥
PrivateKey privateKey = (PrivateKey) keyStore.getKey("mykey",
    "password".toCharArray());
```

### KeyGenerator

```java
// AES 密钥生成
KeyGenerator aesKeyGen = KeyGenerator.getInstance("AES");
aesKeyGen.init(256);
SecretKey aesKey = aesKeyGen.generateKey();

// HMAC 密钥生成
SecretKey hmacKey = new SecretKeySpec(bytes, "HmacSHA256");

// DES 密钥生成 (不推荐)
KeyGenerator desKeyGen = KeyGenerator.getInstance("DES");
SecretKey desKey = desKeyGen.generateKey();
```

---

## 8. SSL/TLS

### SSLContext

```java
import javax.net.ssl.*;

// 创建 SSLContext
SSLContext sslContext = SSLContext.getInstance("TLSv1.3");
sslContext.init(null, null, null);  // 使用默认信任

// 或自定义
KeyManagerFactory kmf = KeyManagerFactory.getInstance(
    KeyManagerFactory.getDefaultAlgorithm());
TrustManagerFactory tmf = TrustManagerFactory.getInstance(
    TrustManagerFactory.getDefaultAlgorithm());

sslContext.init(kmf.getKeyManagers(), tmf.getTrustManagers(),
    new SecureRandom());
```

### HTTPS 客户端

```java
import javax.net.ssl.*;
import java.net.*;

// 创建自定义 SSLContext
SSLContext sslContext = SSLContext.getInstance("TLS");

// 禁用证书验证 (仅测试!)
TrustManager[] trustAllCerts = new TrustManager[]{
    new X509TrustManager() {
        public java.security.cert.X509Certificate[] getAcceptedIssuers() {
            return null;
        }
        public void checkClientTrusted(
                java.security.cert.X509Certificate[] certs, String authType) {}
        public void checkServerTrusted(
                java.security.cert.X509Certificate[] certs, String authType) {}
    }
};

sslContext.init(null, trustAllCerts, new SecureRandom());

// 配置 HttpsURLConnection
HttpsURLConnection.setDefaultSSLSocketFactory(
    sslContext.getSocketFactory());

// 使用 HttpClient
HttpClient client = HttpClient.newBuilder()
    .sslContext(sslContext)
    .build();
```

### HTTPS 服务端

```java
import javax.net.ssl.*;
import com.sun.net.httpserver.*;

// 配置 SSL
HttpsServer server = HttpsServer.create(new InetSocketAddress(8443));
HttpsConfigurator config = server.getHttpsConfigurator();

config.setSSLParameters(sslContext.getDefaultSSLParameters());
config.setNeedClientAuth(false);  // 不需要客户端证书
```

### TLS 版本

| 版本 | JDK 支持 | 状态 |
|------|----------|------|
| TLS 1.0 | JDK 5+ | ❌ 不安全 |
| TLS 1.1 | JDK 5+ | ❌ 不安全 |
| TLS 1.2 | JDK 7+ | ⚠️ 可接受 |
| TLS 1.3 | JDK 11+ | ✅ 推荐 |

---

## 9. 最佳实践

### 算法选择

```java
// ✅ 推荐
MessageDigest.getInstance("SHA-256");           // 摘要
KeyGenerator.getInstance("AES").init(256);      // 对称
Signature.getInstance("SHA256withRSA");        // 签名
Cipher.getInstance("AES/GCM/NoPadding");      // 加密

// ❌ 避免
MessageDigest.getInstance("MD5");               // 不安全
MessageDigest.getInstance("SHA-1");             // 弱安全
Cipher.getInstance("AES/ECB/PKCS5Padding");    // ECB 不安全
```

### 密钥管理

```java
// ✅ 推荐
// 使用 KeyStore 存储密钥
// 使用强随机数生成密钥
SecureRandom random = SecureRandom.getInstanceStrong();
KeyGenerator.getInstance("AES").init(256, random);

// ❌ 避免
// 硬编码密钥
// 使用弱随机数
Random random = new Random();  // 不安全
```

### 安全随机数

```java
import java.security.SecureRandom;

// 强随机数
SecureRandom strong = SecureRandom.getInstanceStrong();
byte[] bytes = new byte[32];
strong.nextBytes(bytes);

// 生成随机 IV
byte[] iv = new byte[16];
strong.nextBytes(iv);
```

---

## 10. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 加密 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Xuelei Fan | 20+ | Oracle | 加密框架 |
| 2 | Sean Mullan | 15+ | Oracle | JCE, 安全框架 |
| 3 | Valerie Peng | 10+ | Oracle | JSSE |
| 4 | Bradford Wetmore | 8+ | Oracle | TLS |
| 5 | Weijun Wang | 5+ | Oracle | JSSE |

---

## 11. 相关链接

### 内部文档

- [安全框架](../security/security/) - 安全框架详解
- [SSL/TLS](../security/ssl/) - SSL/TLS 详解

### 外部资源

- [JCE 规范](https://docs.oracle.com/javase/8/docs/technotes/guides/security/crypto/CryptoSpec.html)
- [Java Cryptography Architecture](https://docs.oracle.com/javase/8/docs/technotes/guides/security/crypto/CryptoSpec.html)
- [AES-GCM Spec](https://csrc.nist.gov/publications/detail/fips/197/2015/final)

---

**最后更新**: 2026-03-20
