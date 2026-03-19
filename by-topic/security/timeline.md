# 安全特性演进时间线

加密、TLS、后量子密码的发展历程。

---

## 时间线概览

```
JDK 8 ───── JDK 11 ───── JDK 17 ───── JDK 21 ───── JDK 26
│              │              │              │              │
TLS 1.2        TLS 1.3       ChaCha20      ML-DSA        KDF API
(默认)         (默认)        Poly1305      (后量子)     (标准化)
                              增强密码
```

---

## TLS/SSL 演进

### JDK 8 - TLS 1.2

```java
// 默认使用 TLS 1.2
SSLContext ctx = SSLContext.getInstance("TLSv1.2");
```

### JDK 11 - TLS 1.3

```java
// TLS 1.3 成为默认
// 优势:
// - 更快的握手
// - 更强的密码套件
// - 1-RTT 握手恢复
```

### JDK 17+ - 更新密码套件

```bash
# 禁用弱密码套件
jdk.tls.client.cipherSuites=TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
```

---

## 加密算法

### JDK 8 - 基础加密

```java
// AES 加密
Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
cipher.init(Cipher.ENCRYPT_MODE, key, iv);
byte[] encrypted = cipher.doFinal(plaintext);
```

### JDK 11 - ChaCha20-Poly1305

```java
// 新增 ChaCha20-Poly1305 算法
Cipher cipher = Cipher.getInstance("ChaCha20-Poly1305/NoPadding");
```

### JDK 21 - 更强算法支持

- KMAC (Keccak Message Authentication Code)
- SHA-3 家族
- 更强的密钥派生

---

## 后量子密码

### JDK 26 - ML-DSA (后量子数字签名)

基于 FIPS 204 的后量子签名算法：

```java
// ML-DSA (也称为 CRYSTALS-Dilithium)
KeyPairGenerator kpg = KeyPairGenerator.getInstance("ML-DSA");
KeyPair kp = kpg.generateKeyPair();

Signature sig = Signature.getInstance("ML-DSA");
sig.initSign(kp.getPrivate());
sig.update(data);
byte[] signature = sig.sign();
```

### 为什么需要后量子密码？

```
传统算法 (RSA, ECDSA)
    ↓
量子计算机 (Shor 算法)
    ↓
可在数小时内破解
```

### ML-DSA 特性

| 特性 | 值 |
|------|-----|
| 密钥大小 | ~2KB |
| 签名大小 | ~2.5KB |
| 安全强度 | AES-256 等级 |

---

## KDF API (JDK 26)

### 密钥派生函数 API

```java
import javax.crypto.KDF;

// 从密码派生密钥
KDF kdf = KDF.getInstance("HKDF-SHA256");
SecretKey derivedKey = kdf.deriveKey("my-key", password, salt, info);
```

### 应用场景

- 从用户密码生成加密密钥
- 从主密钥派生多个子密钥
- 密钥轮换

---

## 安全配置建议

### 启用强 TLS

```bash
# 启用 TLS 1.3
jdk.tls.client.protocols=TLSv1.3
jdk.tls.server.protocols=TLSv1.3
```

### 禁用弱算法

```bash
# 禁用 RC4
jdk.tls.disabledAlgorithms=RC4

# 禁用短密钥
jdk.tls.keySize=2048
```

---

## 时间线总结

| 版本 | 特性 | 说明 |
|------|------|------|
| JDK 8 | TLS 1.2 | 默认 TLS 版本 |
| JDK 11 | TLS 1.3 | 更快更强的握手 |
| JDK 11 | ChaCha20-Poly1305 | 现代加密算法 |
| JDK 15 | 禁用弱签名 | 移除 DSA 1024 位 |
| JDK 17 | KMAC | SHA-3 家族 |
| JDK 21 | 增强密码 | 更多现代算法 |
| JDK 26 | **ML-DSA** | 后量子签名 |
| JDK 26 | **KDF API** | 密钥派生标准化 |
| JDK 26 | **PEM 格式** | 密钥格式支持 |

---

## 相关链接

- [JEP 510: KDF API](https://openjdk.org/jeps/510)
- [JEP 470: PEM Encodings](https://openjdk.org/jeps/470)
- [Java 安全文档](https://docs.oracle.com/en/java/javase/11/security/java-security-overview.html)
