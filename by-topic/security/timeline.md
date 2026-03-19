# 安全特性演进时间线

加密、TLS、后量子密码的发展历程。

---

## 时间线概览

```
JDK 8 ───── JDK 11 ───── JDK 15 ───── JDK 17 ───── JDK 21 ───── JDK 26
 │              │              │              │              │              │
TLS 1.2        TLS 1.3       禁用弱算法     KMAC          ML-DSA        KDF API
(默认)         (默认)        DSA 1024      SHA-3         (后量子)      (正式)
               JEP 332                      JEP 370       JEP 518       JEP 510
               ChaCha20
               JEP 329
```

---

## TLS/SSL 演进

### JDK 8 - TLS 1.2 (默认)

```java
// 默认使用 TLS 1.2
SSLContext ctx = SSLContext.getInstance("TLSv1.2");
ctx.init(null, null, null);

SSLSocketFactory factory = ctx.getSocketFactory();
SSLSocket socket = (SSLSocket) factory.createSocket(host, 443);
```

### JDK 11 - TLS 1.3 (JEP 332)

**优势**：
- 更快的握手 (1-RTT vs 2-RTT)
- 更强的密码套件
- 0-RTT 连接恢复
- 移除不安全的算法

```java
// TLS 1.3 成为默认
SSLContext ctx = SSLContext.getInstance("TLS");
// 自动使用 TLS 1.3

// 启用 0-RTT
SSLParameters params = new SSLParameters();
params.setApplicationProtocols(new String[]{"h2", "http/1.1"});
```

### TLS 1.2 vs TLS 1.3

| 特性 | TLS 1.2 | TLS 1.3 |
|------|---------|---------|
| 握手 RTT | 2-RTT | 1-RTT |
| 恢复 RTT | 1-RTT | 0-RTT |
| 密码套件 | 37+ | 5 |
| 前向安全 | 可选 | 强制 |
| RSA 密钥交换 | 支持 | 不支持 |

### 配置建议

```bash
# java.security 配置
# 启用 TLS 1.3
jdk.tls.client.protocols=TLSv1.3
jdk.tls.server.protocols=TLSv1.3

# 禁用弱密码套件
jdk.tls.disabledAlgorithms=RC4, DES, MD5, SSLv3
```

---

## 加密算法演进

### JDK 8 - 基础加密

```java
// AES 加密
Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
SecretKey key = new SecretKeySpec(bytes, "AES");
cipher.init(Cipher.ENCRYPT_MODE, key, iv);
byte[] encrypted = cipher.doFinal(plaintext);

// RSA
Cipher cipher = Cipher.getInstance("RSA/ECB/PKCS1Padding");
cipher.init(Cipher.ENCRYPT_MODE, publicKey);
byte[] encrypted = cipher.doFinal(data);
```

### JDK 11 - ChaCha20-Poly1305 (JEP 329)

**优势**：
- 软件实现高效
- 适合无 AES 硬件加速的场景
- 认证加密 (AEAD)

```java
// ChaCha20-Poly1305
KeyGenerator keyGen = KeyGenerator.getInstance("ChaCha20");
SecretKey key = keyGen.generateKey();

Cipher cipher = Cipher.getInstance("ChaCha20-Poly1305/None/NoPadding");
cipher.init(Cipher.ENCRYPT_MODE, key);

byte[] nonce = new byte[12];  // 96-bit nonce
SecureRandom random = new SecureRandom();
random.nextBytes(nonce);

cipher.init(Cipher.ENCRYPT_MODE, key, new IvParameterSpec(nonce));
byte[] encrypted = cipher.doFinal(plaintext);
```

### ChaCha20-Poly1305 vs AES-GCM

| 特性 | AES-GCM | ChaCha20-Poly1305 |
|------|---------|-------------------|
| 硬件加速 | x86 AES-NI | 软件实现 |
| 性能 (x86) | 高 | 中等 |
| 性能 (ARM/移动) | 中等 | 高 |
| 密钥大小 | 128/256 位 | 256 位 |
| Nonce 大小 | 96 位 | 96 位 |

### JDK 17 - KMAC (JEP 370)

**Keccak Message Authentication Code**

```java
// KMAC256
KMACParameterSpec params = new KMACParameterSpec(256, "my-key".getBytes(), "custom".getBytes());

Mac mac = Mac.getInstance("KMAC256");
mac.init(key, params);
byte[] macResult = mac.doFinal(data);
```

### JDK 17 - SHA-3 家族

```java
// SHA3-256
MessageDigest md = MessageDigest.getInstance("SHA3-256");
byte[] hash = md.digest(data);

// SHAKE128
MessageDigest shake = MessageDigest.getInstance("SHAKE128");
shake.update(data);
byte[] hash128 = shake.digest(32);  // 32 字节输出
```

---

## 后量子密码

### 背景

```
传统算法 (RSA, ECDSA)
    ↓
量子计算机 (Shor 算法)
    ↓
可在数小时内破解 2048 位 RSA
```

### JDK 26 - ML-DSA (JEP 518)

基于 FIPS 204 (CRYSTALS-Dilithium) 的后量子签名算法。

```java
import java.security.*;

// 生成密钥对
KeyPairGenerator kpg = KeyPairGenerator.getInstance("ML-DSA");
KeyPair kp = kpg.generateKeyPair();

// 签名
Signature sig = Signature.getInstance("ML-DSA");
sig.initSign(kp.getPrivate());
sig.update(data);
byte[] signature = sig.sign();

// 验证
sig.initVerify(kp.getPublic());
sig.update(data);
boolean valid = sig.verify(signature);
```

### ML-DSA 特性

| 特性 | ML-DSA | RSA-2048 | ECDSA-P256 |
|------|--------|----------|------------|
| 密钥大小 | ~2KB | 256B | 64B |
| 签名大小 | ~2.5KB | 256B | 64B |
| 安全强度 | AES-256 | 112-bit | 128-bit |
| 量子安全 | ✅ | ❌ | ❌ |

### ML-DSA 安全级别

```java
// ML-DSA-44 (安全级别 1)
KeyPairGenerator kpg44 = KeyPairGenerator.getInstance("ML-DSA44");

// ML-DSA-65 (安全级别 3)
KeyPairGenerator kpg65 = KeyPairGenerator.getInstance("ML-DSA65");

// ML-DSA-87 (安全级别 5)
KeyPairGenerator kpg87 = KeyPairGenerator.getInstance("ML-DSA87");
```

### JDK 26 - ML-KEM (密钥封装机制)

```java
// 密钥封装
KeyPairGenerator kpg = KeyPairGenerator.getInstance("ML-KEM");
KeyPair kp = kpg.generateKeyPair();

// 封装
Cipher cipher = Cipher.getInstance("ML-KEM");
cipher.init(Cipher.WRAP_MODE, kp.getPublic());
byte[] encapsulatedKey = cipher.wrap(secretKey);

// 解封装
cipher.init(Cipher.UNWRAP_MODE, kp.getPrivate());
SecretKey secretKey = (SecretKey) cipher.unwrap(encapsulatedKey, "AES", Cipher.SECRET_KEY);
```

---

## KDF API (JEP 510)

### 演进历程

| 版本 | 状态 | JEP |
|------|------|-----|
| JDK 22 | 预览 | JEP 495 |
| JDK 23 | 第二次预览 | JEP 508 |
| JDK 26 | **正式** | JEP 510 |

### 密钥派生函数 API

```java
import javax.crypto.KDF;
import javax.crypto.spec.*;

// HKDF-SHA256
KDF kdf = KDF.getInstance("HKDF-SHA256");

SecretKey salt = new SecretKeySpec(
    new byte[32], "HKDF-SHA256");

SecretKey derivedKey = kdf.deriveKey(
    "my-key",
    new KDFParameters(
        salt,
        "info-context".getBytes(),
        256  // 密钥长度
    )
);
```

### 支持的 KDF 算法

| 算法 | 说明 |
|------|------|
| HKDF-SHA256 | HMAC-based KDF (SHA-256) |
| HKDF-SHA384 | HMAC-based KDF (SHA-384) |
| HKDF-SHA512 | HMAC-based KDF (SHA-512) |
| PBKDF2-HMAC-SHA256 | Password-based KDF |
| PBKDF2-HMAC-SHA512 | Password-based KDF |

### 应用场景

```java
// 1. 从密码派生加密密钥
KDF kdf = KDF.getInstance("PBKDF2-HMAC-SHA256");
KDFParameters params = new KDFParameters(
    salt,
    iterations,
    keyLength
);
SecretKey key = kdf.deriveKey("derived", password, params);

// 2. 从主密钥派生多个子密钥
SecretKey masterKey = ...;

// 加密密钥
SecretKey encKey = kdf.deriveKey(
    "encryption",
    masterKey,
    new KDFParameters(salt, "enc".getBytes(), 256)
);

// 认证密钥
SecretKey authKey = kdf.deriveKey(
    "auth",
    masterKey,
    new KDFParameters(salt, "auth".getBytes(), 256)
);
```

---

## PEM 格式支持 (JEP 470)

### JDK 26 - PEM Encodings

**Privacy-Enhanced Mail (PEM)** 格式是密钥和证书的标准文本格式。

```java
// 读取 PEM 格式的私钥
String pem = """
    -----BEGIN PRIVATE KEY-----
    MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC...
    -----END PRIVATE KEY-----
    """;

PrivateKey privateKey = KeyFactory.getInstance("RSA")
    .generatePrivate(new PKCS8EncodedKeySpec(
        PemParser.parse(pem)
    ));

// 读取 PEM 格式的证书
Certificate cert = CertificateFactory.getInstance("X.509")
    .generateCertificate(
        new ByteArrayInputStream(pem.getBytes())
    );
```

### PEM 工具类

```java
// JDK 26 新增
import java.security.pem.*;

// 解析 PEM
PemObject pem = PemParser.parse(pemString);

// 生成 PEM
String pem = PemWriter.encode(privateKey);
```

---

## 密钥库演进

### JKS → PKCS12

```bash
# JDK 8 之前: JKS (默认)
keytool -importcert -keystore keystore.jks

# JDK 9+: PKCS12 (默认)
keytool -importcert -keystore keystore.p12

# 迁移
keytool -importkeystore \
  -srckeystore keystore.jks -destkeystore keystore.p12 \
  -srcstoretype JKS -deststoretype PKCS12
```

### 配置

```bash
# java.security
# 默认密钥库类型
keystore.type=pkcs12

# 禁用 JKS (可选)
jdk.tls.disabledAlgorithms=JKS
```

---

## 安全配置建议

### TLS 配置

```bash
# java.security
# 启用 TLS 1.3
jdk.tls.client.protocols=TLSv1.3
jdk.tls.server.protocols=TLSv1.3

# 禁用弱密码套件
jdk.tls.disabledAlgorithms=\
    RC4, DES, MD5, SSLv3, \
    TLSv1, TLSv1.1, \
    TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384, \
    TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384

# 密钥大小限制
jdk.tls.keySize=2048
```

### 证书验证

```java
// 启用证书吊销检查
System.setProperty("com.sun.security.enableCRLDP", "true");
System.setProperty("com.sun.security.ocsp.enable", "true");

// 自定义信任存储
System.setProperty("javax.net.ssl.trustStore", "/path/to/truststore.jks");
System.setProperty("javax.net.ssl.trustStorePassword", "changeit");
```

### 禁用弱算法

```bash
# java.security
jdk.jar.disabledAlgorithms=\
    MD2, MD5, RSA keySize < 1024, \
    DSA keySize < 1024

# 签名算法
jdk.security.legacyAlgorithms=\
    SHA1, RSA keySize < 2048
```

---

## 时间线总结

| 版本 | 特性 | JEP | 说明 |
|------|------|-----|------|
| JDK 8 | TLS 1.2 | - | 默认 TLS 版本 |
| JDK 8 | AES-GCM | - | 认证加密 |
| JDK 11 | **TLS 1.3** | JEP 332 | 更快更强的握手 |
| JDK 11 | **ChaCha20-Poly1305** | JEP 329 | 现代加密算法 |
| JDK 15 | 禁用弱签名 | - | 移除 DSA 1024 位 |
| JDK 17 | **KMAC** | JEP 370 | SHA-3 家族 MAC |
| JDK 17 | **SHA-3** | JEP 370 | Keccak 哈希 |
| JDK 21 | 增强密码 | - | 更多现代算法 |
| JDK 21 | HSS/LMS | - | 后量子状态哈希签名 |
| JDK 22 | KDF API (预览) | JEP 495 | 密钥派生函数 |
| JDK 23 | KDF API (预览) | JEP 508 | 第二次预览 |
| JDK 24 | 12 KDF 算法 | - | 更多 KDF 支持 |
| JDK 26 | **ML-DSA** | JEP 518 | 后量子签名 |
| JDK 26 | **ML-KEM** | - | 后量子密钥封装 |
| JDK 26 | **KDF API** | JEP 510 | 密钥派生标准化 |
| JDK 26 | **PEM 格式** | JEP 470 | 密钥格式支持 |

---

## 完整示例

### 安全 HTTP 客户端

```java
import javax.net.ssl.*;
import java.net.http.*;
import java.security.cert.*;

public class SecureHttpClient {
    private final HttpClient client;

    public SecureHttpClient() throws Exception {
        // 创建 TLS 1.3 SSLContext
        SSLContext sslContext = SSLContext.getInstance("TLSv1.3");

        // 自定义信任管理器 (生产环境应使用标准信任)
        TrustManager[] trustManagers = {
            new X509TrustManager() {
                public X509Certificate[] getAcceptedIssuers() { return null; }
                public void checkClientTrusted(X509Certificate[] certs, String type) { }
                public void checkServerTrusted(X509Certificate[] certs, String type) { }
            }
        };

        sslContext.init(null, trustManagers, new SecureRandom());

        this.client = HttpClient.newBuilder()
            .version(HttpClient.Version.HTTP_3)
            .sslContext(sslContext)
            .sslParameters(sslContext.getDefaultSSLParameters())
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

        return response.body();
    }
}
```

### 后量子签名示例

```java
import java.security.*;

public class PostQuantumSignature {
    public static void main(String[] args) throws Exception {
        // 生成 ML-DSA 密钥对
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("ML-DSA");
        KeyPair kp = kpg.generateKeyPair();

        // 要签名的数据
        byte[] data = "Hello, Post-Quantum!".getBytes();

        // 签名
        Signature sig = Signature.getInstance("ML-DSA");
        sig.initSign(kp.getPrivate());
        sig.update(data);
        byte[] signature = sig.sign();

        System.out.println("Signature size: " + signature.length + " bytes");

        // 验证
        sig.initVerify(kp.getPublic());
        sig.update(data);
        boolean valid = sig.verify(signature);

        System.out.println("Signature valid: " + valid);
    }
}
```

---

## 相关链接

- [JEP 332: TLS 1.3](https://openjdk.org/jeps/332)
- [JEP 329: ChaCha20-Poly1305](https://openjdk.org/jeps/329)
- [JEP 370: KMAC & SHA-3](https://openjdk.org/jeps/370)
- [JEP 518: ML-DSA](https://openjdk.org/jeps/518)
- [JEP 510: KDF API](https://openjdk.org/jeps/510)
- [JEP 470: PEM Encodings](https://openjdk.org/jeps/470)
