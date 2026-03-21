# java.crypto 模块分析

> Java 加密服务提供者，实现密码学算法和安全协议

---

## 1. 模块概述

`java.crypto` 是 Java 安全架构的核心模块，提供加密、解密、密钥生成、消息认证码 (MAC) 等密码学功能。

### 模块定义

**文件**: `src/java.base/share/classes/module-info.java`

```java
module java.base {
    exports java.security;
    exports java.security.cert;
    exports java.security.spec;
    exports javax.crypto;
    exports javax.crypto.spec;
}
```

### 架构

```
┌─────────────────────────────────────────────────────────┐
│                   应用层 API                             │
│  Cipher, KeyGenerator, MessageDigest, Signature, ...    │
├─────────────────────────────────────────────────────────┤
│                  Provider 架构                           │
│  (SPI 接口 - 允许第三方提供者实现)                        │
├─────────────────────────────────────────────────────────┤
│              SunPKCS11 / SunMSCAPI / SunJCE             │
│              (默认安全提供者)                            │
├─────────────────────────────────────────────────────────┤
│          底层实现 (Native / Software)                   │
│    PKCS#11 / Microsoft CAPI / 纯 Java 实现              │
└─────────────────────────────────────────────────────────┘
```

---

## 2. 核心类分析

### 2.1 Cipher (对称加密)

**源码**: `java.base/share/classes/javax/crypto/Cipher.java`

```java
public class Cipher {
    // 获取 Cipher 实例
    public static Cipher getInstance(String transformation)

    // 初始化
    public final void init(int opmode, Key key)

    // 加密/解密
    public final byte[] doFinal(byte[] input)
}
```

**支持的算法**:

| 算法 | 密钥长度 | 模式 | 填充 | JDK 26 状态 |
|------|---------|------|------|-------------|
| AES | 128/192/256 | CBC/GCM/CTR | PKCS5/NoPadding | ✓ |
| ChaCha20 | 256 | - | Poly1305 | ✓ (JDK 11+) |
| DES | 56 | CBC/ECB | PKCS5 | ⚠️ 遗留算法 |
| 3DES | 168 | CBC/ECB | PKCS5 | ⚠️ 遗留算法 |

**JDK 26 推荐**: 使用 AES-GCM (认证加密)

```java
// 推荐: AES-GCM (认证加密)
Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
SecretKey key = KeyGenerator.getInstance("AES").generateKey();
GCMParameterSpec spec = new GCMParameterSpec(128, iv);
cipher.init(Cipher.ENCRYPT_MODE, key, spec);
```

### 2.2 MessageDigest (哈希)

**源码**: `java.base/share/classes/java/security/MessageDigest.java`

```java
public abstract class MessageDigest {
    public static MessageDigest getInstance(String algorithm)
    public byte[] digest(byte[] input)
    public void update(byte[] input)
}
```

**支持的算法**:

| 算法 | 输出长度 | JDK 26 状态 |
|------|---------|-------------|
| SHA-256 | 256 | ✓ 推荐 |
| SHA-384 | 384 | ✓ |
| SHA-512 | 512 | ✓ |
| SHA-3 | 224/256/384/512 | ✓ (JDK 9+) |
| MD5 | 128 | ⚠️ 不安全 |

### 2.3 Signature (数字签名)

**源码**: `java.base/share/classes/java/security/Signature.java`

```java
public abstract class Signature {
    public static Signature getInstance(String algorithm)
    public final void initSign(PrivateKey privateKey)
    public final void initVerify(PublicKey publicKey)
    public final byte[] sign()
    public final boolean verify(byte[] signature)
}
```

**支持的算法**:

| 算法 | 密钥类型 | JDK 26 状态 |
|------|---------|-------------|
| Ed25519 | EdDSA | ✓ 推荐 (JDK 15+) |
| Ed448 | EdDSA | ✓ (JDK 15+) |
| RSA | RSA | ✓ |
| ECDSA | EC | ✓ |
| DSA | DSA | ⚠️ 遗留 |

### 2.4 KeyPairGenerator (密钥生成)

**源码**: `java.base/share/classes/java/security/KeyPairGenerator.java`

```java
public abstract class KeyPairGenerator {
    public static KeyPairGenerator getInstance(String algorithm)
    public KeyPair generateKeyPair()
}
```

**JDK 26 新增**: 密钥生成时间优化

```java
// Ed25519 (快速签名)
KeyPairGenerator kpg = KeyPairGenerator.getInstance("Ed25519");
KeyPair kp = kpg.generateKeyPair();

// RSA 3072 (传统场景)
kpg = KeyPairGenerator.getInstance("RSA");
kpg.initialize(3072);
KeyPair rsaKey = kpg.generateKeyPair();
```

### 2.5 KeyGenerator (对称密钥)

**源码**: `java.base/share/classes/javax/crypto/KeyGenerator.java`

```java
public class KeyGenerator {
    public static KeyGenerator getInstance(String algorithm)
    public SecretKey generateKey()
}
```

---

## 3. SSL/TLS 支持

### 3.1 SSLEngine

**源码**: `java.base/share/classes/javax/net/ssl/SSLEngine.java`

```java
public class SSLEngine {
    public void beginHandshake()
    public SSLEngineResult wrap(ByteBuffer src, ByteBuffer dst)
    public SSLEngineResult unwrap(ByteBuffer src, ByteBuffer dst)
}
```

### 3.2 SSLContext

**支持的协议** (JDK 26):

| 协议 | 状态 | 说明 |
|------|------|------|
| TLS 1.3 | ✓ 默认 | 推荐 |
| TLS 1.2 | ✓ | 兼容 |
| TLS 1.1/1.0 | ✗ | 禁用 |
| SSLv3 | ✗ | 禁用 |

```java
// 推荐: TLS 1.3
SSLContext ctx = SSLContext.getInstance("TLSv1.3");
ctx.init(null, null, null);  // 使用默认信任

// HTTP/3 (QUIC) 需要 TLS 1.3
```

---

## 4. JDK 26 变更

### 4.1 算法更新

| 变更 | 说明 |
|------|------|
| SHA-3 | 优化性能 |
| EdDSA | 改进密钥生成速度 |
| AES-GCM | 硬件加速支持 |

### 4.2 安全增强

- 禁用弱加密算法 (RC4, DES, MD5)
- TLS 1.3 作为默认协议
- 改进 X.509 证书验证

### 4.3 性能改进

- ChaCha20-Poly1305 硬件加速
- 密钥派生函数 (KDF) 优化

---

## 5. 使用示例

### 5.1 对称加密

```java
// AES-GCM (认证加密)
SecretKey key = KeyGenerator.getInstance("AES").generateKey();
byte[] iv = new byte[12];  // GCM 推荐 12 字节
new SecureRandom().nextBytes(iv);

Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
GCMParameterSpec spec = new GCMParameterSpec(128, iv);
cipher.init(Cipher.ENCRYPT_MODE, key, spec);

byte[] ciphertext = cipher.doFinal(plaintext);
```

### 5.2 非对称加密

```java
// Ed25519 签名 (JDK 15+)
KeyPairGenerator kpg = KeyPairGenerator.getInstance("Ed25519");
KeyPair kp = kpg.generateKeyPair();

Signature sig = Signature.getInstance("Ed25519");
sig.initSign(kp.getPrivate());
sig.update(data);
byte[] signature = sig.sign();

// 验证
sig.initVerify(kp.getPublic());
sig.update(data);
boolean valid = sig.verify(signature);
```

### 5.3 哈希

```java
MessageDigest md = MessageDigest.getInstance("SHA-256");
byte[] hash = md.digest(data);
```

### 5.4 TLS 连接

```java
SSLContext ctx = SSLContext.getInstance("TLSv1.3");
ctx.init(null, new TrustManager[]{new X509TrustManager() {
    public void checkClientTrusted(X509Certificate[] chain, String authType) {}
    public void checkServerTrusted(X509Certificate[] chain, String authType) {}
    public X509Certificate[] getAcceptedIssuers() { return new X509Certificate[0]; }
}}, null);

SSLSocketFactory factory = ctx.getSocketFactory();
SSLSocket socket = (SSLSocket) factory.createSocket(host, 443);
socket.startHandshake();
```

---

## 6. 安全最佳实践

### 6.1 算法选择

| 用途 | 推荐算法 |
|------|---------|
| 对称加密 | AES-256-GCM |
| 哈希 | SHA-256 / SHA-3-256 |
| 签名 | Ed25519 |
| 密钥交换 | X25519 |
| KDF | HKDF-SHA256 |

### 6.2 避免的算法

- MD5, SHA-1 (哈希碰撞)
- DES, 3DES (密钥长度不足)
| RC4 (流密码弱点)
- ECB 模式 (不安全)

### 6.3 密钥管理

```java
// 推荐: 使用 KeyStore
KeyStore ks = KeyStore.getInstance("PKCS12");
try (InputStream is = Files.newInputStream(keystorePath)) {
    ks.load(is, password);
}

// 推荐: 使用密码加密存储 PBEKeySpec
SecretKeyFactory factory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");
KeySpec spec = new PBEKeySpec(password, salt, 100000, 256);
SecretKey tmp = factory.generateSecret(spec);
SecretKey key = new SecretKeySpec(tmp.getEncoded(), "AES");
```

---

## 7. 相关链接

- [JDK 26 安全文档](https://openjdk.org/groups/security/)
- [Java 加密架构 (JCA)](https://docs.oracle.com/en/java/javase/26/security/java-cryptography-architecture-jca-reference-guide.html)
- [PKCS#11 参考](https://docs.oracle.com/en/java/javase/26/security/pkcs11-reference-guide.html)
- [源码](https://github.com/openjdk/jdk/tree/master/src/java.base/share/classes/javax/crypto)
