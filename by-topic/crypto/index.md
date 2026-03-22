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
| **JDK 9** | DRBG SecureRandom | - | 确定性随机位生成器 |
| **JDK 11** | TLS 1.3 | JEP 332 | 新密码套件, ChaCha20-Poly1305 (JEP 329) |
| **JDK 15** | EdDSA | JEP 339 | Edwards-Curve 数字签名 |
| **JDK 21** | KEM API | JEP 452 | 密钥封装机制框架 |
| **JDK 24** | ML-KEM | JEP 496 | 后量子密钥封装 (FIPS 203) |
| **JDK 24** | ML-DSA | JEP 497 | 后量子签名 (FIPS 204) |
| **JDK 25** | KDF API | JEP 510 | 密钥派生函数 (HKDF) |
| **JDK 25** | PEM 编码 (预览) | JEP 470 | 密钥/证书 PEM 格式 |
| **JDK 26** | HPKE | - | 混合公钥加密 (RFC 9180) |
| **JDK 26** | PEM 编码 (预览 2) | JEP 524 | PEMRecord 重命名为 PEM |

---

## 目录

- [JCA/JCE 架构](#2-jcajce-架构)
- [消息摘要](#3-消息摘要-message-digest)
- [对称加密](#4-对称加密-symmetric-encryption)
- [非对称加密](#5-非对称加密-asymmetric-encryption)
- [数字签名](#6-数字签名-digital-signature)
- [后量子密码 PQC](#7-后量子密码-pqc)
- [密钥管理](#8-密钥管理-key-management)
- [SecureRandom](#9-securerandom)
- [SSL/TLS](#10-ssltls)
- [常见安全陷阱](#11-常见安全陷阱)
- [最佳实践](#12-最佳实践)
- [核心贡献者](#13-核心贡献者)
- [相关链接](#14-相关链接)

---

## 2. JCA/JCE 架构

**JCA** (Java Cryptography Architecture) 定义框架和接口;
**JCE** (Java Cryptography Extension) 提供加密实现。两者在 JDK 1.4 之后统一集成。

### Provider 模型 (提供者模型)

JCA 使用 **Provider-based architecture**——算法实现与 API 完全解耦:

```
┌──────────────────────────────────────────────────┐
│              应用代码 (Application Code)            │
├──────────────────────────────────────────────────┤
│           Engine Classes (引擎类)                  │
│  Cipher · MessageDigest · Signature · KeyGenerator │
│  KeyPairGenerator · Mac · SecureRandom · KEM       │
├──────────────────────────────────────────────────┤
│         SPI (Service Provider Interface)           │
│  CipherSpi · MessageDigestSpi · SignatureSpi ...   │
├─────────┬─────────┬──────────┬───────────────────┤
│ SunJCE  │ SunEC   │ SunRsaSign│ BouncyCastle ... │
│(AES,DES)│(EC曲线) │  (RSA)    │   (第三方)        │
└─────────┴─────────┴──────────┴───────────────────┘
```

```java
// 列出所有已注册的 Provider
for (Provider p : Security.getProviders()) {
    System.out.printf("%-20s version %.1f%n", p.getName(), p.getVersion());
}

// 按优先级查找——不指定 Provider，JCA 按注册顺序搜索
Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");

// 指定 Provider——跳过搜索，直接使用指定实现
Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding", "SunJCE");

// 动态插入自定义 Provider（优先级 1 = 最高）
Security.insertProviderAt(new BouncyCastleProvider(), 1);
```

### Engine Classes (引擎类) 一览

| 引擎类 | 用途 | 典型算法 |
|--------|------|----------|
| `Cipher` | 对称/非对称加密解密 | AES, RSA, ChaCha20 |
| `MessageDigest` | 消息摘要 (Hash) | SHA-256, SHA-3 |
| `Signature` | 数字签名与验证 | SHA256withRSA, Ed25519, ML-DSA |
| `KeyGenerator` | 对称密钥生成 | AES, HmacSHA256, ChaCha20 |
| `KeyPairGenerator` | 非对称密钥对生成 | RSA, EC, Ed25519, ML-KEM |
| `Mac` | 消息认证码 (HMAC) | HmacSHA256, HmacSHA3-256 |
| `SecureRandom` | 安全随机数 | DRBG, NativePRNG |
| `KeyStore` | 密钥/证书存储 | PKCS12, JKS |
| `KeyFactory` | 密钥格式转换 | RSA, EC |
| `KEM` (JDK 21+) | 密钥封装机制 | ML-KEM |
| `KDF` (JDK 25+) | 密钥派生函数 | HKDF |

### Engine Class 通用模式

所有引擎类遵循相同的使用模式——`getInstance()` 工厂方法:

```java
// 1. 获取实例 (Factory Method Pattern)
MessageDigest md   = MessageDigest.getInstance("SHA-256");
Cipher cipher      = Cipher.getInstance("AES/GCM/NoPadding");
Signature sig      = Signature.getInstance("Ed25519");
Mac mac            = Mac.getInstance("HmacSHA256");
KeyGenerator kg    = KeyGenerator.getInstance("AES");
KeyPairGenerator kpg = KeyPairGenerator.getInstance("EC");
SecureRandom sr    = SecureRandom.getInstance("DRBG");

// 2. 初始化 (init / initialize)
// 3. 执行操作 (update + doFinal / sign / verify / generateKey)
```

---

## 3. 消息摘要 (Message Digest)

### MessageDigest 基础

```java
// SHA-256 (通用推荐)
MessageDigest digest = MessageDigest.getInstance("SHA-256");
byte[] hash = digest.digest("Hello, World!".getBytes(StandardCharsets.UTF_8));

// 增量更新——处理大文件时避免内存溢出
MessageDigest md = MessageDigest.getInstance("SHA-256");
try (InputStream is = Files.newInputStream(Path.of("largefile.bin"))) {
    byte[] buf = new byte[8192];
    int n;
    while ((n = is.read(buf)) != -1) {
        md.update(buf, 0, n);
    }
}
byte[] fileHash = md.digest();

// 十六进制输出
String hex = HexFormat.of().formatHex(fileHash);  // JDK 17+
```

### SHA-3 家族 (JDK 9+)

```java
// SHA-3 提供不同于 SHA-2 的内部结构 (Keccak 海绵函数)
// 即使 SHA-2 被攻破，SHA-3 仍然安全——defense in depth
MessageDigest sha3 = MessageDigest.getInstance("SHA3-256");
byte[] hash = sha3.digest(data);
```

### 算法对比

| 算法 | 输出长度 | 安全性 | 使用场景 |
|------|----------|--------|----------|
| MD5 | 128 位 | 不安全 | 仅用于非安全校验 (遗留) |
| SHA-1 | 160 位 | 弱，已有碰撞攻击 | 遗留系统兼容 |
| **SHA-256** | 256 位 | 安全 | **通用推荐**: 数据完整性、数字签名 |
| SHA-384 | 384 位 | 安全 | TLS 证书、高安全场景 |
| SHA-512 | 512 位 | 安全 | 64 位平台上性能更优 |
| **SHA3-256** | 256 位 | 安全 | 替代 SHA-2，后量子安全分析更乐观 |
| SHA3-512 | 512 位 | 安全 | 最高安全需求 |

> **选择建议**: 新项目用 SHA-256；如需对抗未来量子威胁，考虑 SHA3-256。

---

## 4. 对称加密 (Symmetric Encryption)

### AES 密钥生成与基本加密

```java
// 密钥生成——始终用 KeyGenerator，不要手动构造
KeyGenerator keyGen = KeyGenerator.getInstance("AES");
keyGen.init(256, SecureRandom.getInstanceStrong());  // 128/192/256 位
SecretKey key = keyGen.generateKey();
```

### AES 模式详解

| 模式 | 全称 | 特点 | 安全性 |
|------|------|------|--------|
| **ECB** | Electronic Codebook | 相同明文块产生相同密文——泄露模式信息 | 不安全，禁止使用 |
| **CBC** | Cipher Block Chaining | 链式加密，需要 IV，不可并行加密 | 安全 (需正确 IV) |
| **CTR** | Counter | 流式，可并行，需唯一 nonce | 安全 |
| **GCM** | Galois/Counter Mode | AEAD 认证加密，同时保证机密性与完整性 | **推荐** |

### AES-GCM (推荐的 AEAD 模式)

```java
// AES-GCM: 认证加密 (Authenticated Encryption with Associated Data)
// 同时提供: 机密性 (Confidentiality) + 完整性 (Integrity) + 认证 (Authentication)

// --- 加密 ---
byte[] nonce = new byte[12]; // GCM 推荐 12 字节 nonce
SecureRandom.getInstanceStrong().nextBytes(nonce);

Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
GCMParameterSpec gcmSpec = new GCMParameterSpec(128, nonce); // 128 位认证标签
cipher.init(Cipher.ENCRYPT_MODE, key, gcmSpec);

// AAD: 附加认证数据 (不加密，但参与认证)
cipher.updateAAD("metadata".getBytes(StandardCharsets.UTF_8));

byte[] ciphertext = cipher.doFinal(plaintext);
// ciphertext 末尾包含 16 字节认证标签 (authentication tag)

// --- 解密 ---
cipher.init(Cipher.DECRYPT_MODE, key, gcmSpec);
cipher.updateAAD("metadata".getBytes(StandardCharsets.UTF_8));
byte[] decrypted = cipher.doFinal(ciphertext); // 认证失败抛 AEADBadTagException
```

> **GCM nonce 注意**: 同一密钥下 nonce 绝不能重复，否则安全性完全丧失。

### AES-CBC (传统模式)

```java
// CBC 仍在广泛使用，但不提供认证——需额外 HMAC
byte[] iv = new byte[16]; // CBC 需要 16 字节 IV
SecureRandom.getInstanceStrong().nextBytes(iv);

Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
cipher.init(Cipher.ENCRYPT_MODE, key, new IvParameterSpec(iv));
byte[] ciphertext = cipher.doFinal(plaintext);
// 必须将 IV 与密文一起传输 (IV 不需保密)
```

### ChaCha20-Poly1305 (JEP 329, JDK 11+)

```java
// ChaCha20-Poly1305: 流密码 + AEAD
// 优势: 不依赖 AES 硬件指令，在无 AES-NI 的设备上更快
// 广泛用于 TLS 1.3、WireGuard

KeyGenerator keyGen = KeyGenerator.getInstance("ChaCha20");
keyGen.init(256);
SecretKey key = keyGen.generateKey();

byte[] nonce = new byte[12];
SecureRandom.getInstanceStrong().nextBytes(nonce);

Cipher cipher = Cipher.getInstance("ChaCha20-Poly1305");
cipher.init(Cipher.ENCRYPT_MODE, key,
    new IvParameterSpec(nonce));  // ChaCha20 使用 IvParameterSpec
cipher.updateAAD(aad);
byte[] ciphertext = cipher.doFinal(plaintext);
```

### 对称算法选择指南

| 场景 | 推荐算法 | 说明 |
|------|----------|------|
| 通用加密 | **AES-256-GCM** | AEAD 认证加密，有 AES-NI 加速 |
| 无 AES 硬件 | **ChaCha20-Poly1305** | 移动设备、嵌入式 |
| 遗留兼容 | AES-CBC + HMAC | 需要额外完整性保护 |
| 磁盘加密 | AES-XTS | JDK 未内置，需第三方 Provider |

---

## 5. 非对称加密 (Asymmetric Encryption)

### RSA

```java
// RSA 密钥对生成
KeyPairGenerator keyGen = KeyPairGenerator.getInstance("RSA");
keyGen.initialize(2048);  // 最低 2048，推荐 3072+
KeyPair keyPair = keyGen.generateKeyPair();

// RSA-OAEP (推荐填充方式，比 PKCS1Padding 更安全)
Cipher cipher = Cipher.getInstance("RSA/ECB/OAEPWithSHA-256AndMGF1Padding");
cipher.init(Cipher.ENCRYPT_MODE, keyPair.getPublic());
byte[] ciphertext = cipher.doFinal(plaintext);

cipher.init(Cipher.DECRYPT_MODE, keyPair.getPrivate());
byte[] decrypted = cipher.doFinal(ciphertext);
```

| RSA 密钥大小 | 安全级别 (等价对称密钥) | 推荐程度 |
|-------------|----------------------|----------|
| 1024 位 | ~80 位 | 不安全，禁止使用 |
| 2048 位 | ~112 位 | 最低要求 |
| 3072 位 | ~128 位 | 推荐 |
| 4096 位 | ~140 位 | 高安全需求 |

### EC 椭圆曲线 (Elliptic Curve)

```java
// EC 密钥对——相比 RSA，更短密钥实现同等安全
KeyPairGenerator ecGen = KeyPairGenerator.getInstance("EC");
ecGen.initialize(new ECGenParameterSpec("secp256r1")); // NIST P-256
KeyPair ecKeyPair = ecGen.generateKeyPair();

// ECDH 密钥协商 (Key Agreement)
KeyAgreement ka = KeyAgreement.getInstance("ECDH");
ka.init(myPrivateKey);
ka.doPhase(peerPublicKey, true);
byte[] sharedSecret = ka.generateSecret();
// 用 sharedSecret 派生对称密钥 (通过 HKDF)

// ECDSA 签名
Signature sig = Signature.getInstance("SHA256withECDSA");
sig.initSign(ecKeyPair.getPrivate());
sig.update(data);
byte[] signature = sig.sign();
```

| EC 曲线 | 密钥大小 | 等价 RSA | 标准 |
|---------|---------|----------|------|
| secp256r1 (P-256) | 256 位 | ~3072 位 RSA | NIST, TLS 默认 |
| secp384r1 (P-384) | 384 位 | ~7680 位 RSA | 高安全 |
| secp521r1 (P-521) | 521 位 | ~15360 位 RSA | 极高安全 |

### EdDSA (JEP 339, JDK 15+)

```java
// EdDSA: Edwards-Curve Digital Signature Algorithm
// 优势: 常数时间实现 (抗侧信道)、确定性签名、性能优于 ECDSA

// Ed25519——128 位安全等级
KeyPairGenerator edGen = KeyPairGenerator.getInstance("Ed25519");
KeyPair edKeyPair = edGen.generateKeyPair();

Signature edSig = Signature.getInstance("Ed25519");
edSig.initSign(edKeyPair.getPrivate());
edSig.update(data);
byte[] signature = edSig.sign();

// Ed448——224 位安全等级
KeyPairGenerator ed448Gen = KeyPairGenerator.getInstance("Ed448");
```

### 混合加密 (Hybrid Encryption)

RSA/EC 只能加密少量数据——实际使用时总是混合加密:

```java
// 1. 生成对称会话密钥
SecretKey sessionKey = KeyGenerator.getInstance("AES").generateKey();

// 2. 对称加密实际数据
Cipher aesCipher = Cipher.getInstance("AES/GCM/NoPadding");
byte[] nonce = new byte[12];
SecureRandom.getInstanceStrong().nextBytes(nonce);
aesCipher.init(Cipher.ENCRYPT_MODE, sessionKey, new GCMParameterSpec(128, nonce));
byte[] encryptedData = aesCipher.doFinal(plaintext);

// 3. RSA-OAEP 加密会话密钥
Cipher rsaCipher = Cipher.getInstance("RSA/ECB/OAEPWithSHA-256AndMGF1Padding");
rsaCipher.init(Cipher.ENCRYPT_MODE, recipientPublicKey);
byte[] encryptedKey = rsaCipher.doFinal(sessionKey.getEncoded());

// 传输: nonce + encryptedKey + encryptedData
```

### 非对称算法选择指南

| 用途 | 推荐 | 说明 |
|------|------|------|
| 数字签名 | **Ed25519** | 现代首选，性能和安全性最优 |
| 密钥协商 | **ECDH (P-256)** | TLS 默认选择 |
| 加密密钥传输 | **RSA-OAEP 3072+** | 兼容性最好 |
| 后量子安全 | **ML-KEM + ML-DSA** | JDK 24+，见第 7 节 |

---

## 6. 数字签名 (Digital Signature)

### 签名与验证

```java
// --- 签名 ---
KeyPairGenerator keyGen = KeyPairGenerator.getInstance("RSA");
keyGen.initialize(3072);
KeyPair keyPair = keyGen.generateKeyPair();

Signature signer = Signature.getInstance("SHA256withRSA");
signer.initSign(keyPair.getPrivate());
signer.update("Hello, Signature!".getBytes(StandardCharsets.UTF_8));
byte[] signatureBytes = signer.sign();

// --- 验证 ---
Signature verifier = Signature.getInstance("SHA256withRSA");
verifier.initVerify(keyPair.getPublic());
verifier.update("Hello, Signature!".getBytes(StandardCharsets.UTF_8));
boolean valid = verifier.verify(signatureBytes);
```

### 签名算法一览

| 算法 | JDK 版本 | 推荐程度 | 说明 |
|------|----------|----------|------|
| SHA256withRSA | 1.4+ | 安全 | 传统广泛使用 |
| SHA384withRSA | 1.4+ | 安全 | 高安全需求 |
| SHA256withECDSA | 7+ | 安全 | 短签名，性能好 |
| **Ed25519** | 15+ | **推荐** | 现代首选，确定性签名 |
| Ed448 | 15+ | 推荐 | 224 位安全等级 |
| **ML-DSA** | 24+ | **后量子推荐** | FIPS 204 标准 |

---

## 7. 后量子密码 (PQC)

量子计算机可破解 RSA/EC/DH——NIST 已发布后量子标准。JDK 24 率先支持。

### ML-KEM: 密钥封装 (JEP 496, JDK 24)

```java
// ML-KEM (Module-Lattice-Based Key Encapsulation Mechanism)
// 基于 FIPS 203 标准，替代 RSA/ECDH 进行密钥交换

// 生成密钥对 (使用 KEM API, JEP 452)
KeyPairGenerator kpg = KeyPairGenerator.getInstance("ML-KEM");
kpg.initialize(NamedParameterSpec.ML_KEM_768); // ML-KEM-512/768/1024
KeyPair keyPair = kpg.generateKeyPair();

// --- 发送方: 封装 (Encapsulate) ---
KEM kem = KEM.getInstance("ML-KEM");
KEM.Encapsulator enc = kem.newEncapsulator(keyPair.getPublic());
KEM.Encapsulated encapsulated = enc.encapsulate();
SecretKey sharedSecret = encapsulated.key();        // 共享密钥
byte[] encapsulation = encapsulated.encapsulation(); // 发给接收方

// --- 接收方: 解封装 (Decapsulate) ---
KEM.Decapsulator dec = kem.newDecapsulator(keyPair.getPrivate());
SecretKey receivedSecret = dec.decapsulate(encapsulation); // 得到相同密钥
```

### ML-DSA: 数字签名 (JEP 497, JDK 24)

```java
// ML-DSA (Module-Lattice-Based Digital Signature Algorithm)
// 基于 FIPS 204 标准，替代 RSA/ECDSA 签名

KeyPairGenerator kpg = KeyPairGenerator.getInstance("ML-DSA");
kpg.initialize(NamedParameterSpec.ML_DSA_65); // ML-DSA-44/65/87
KeyPair keyPair = kpg.generateKeyPair();

Signature signer = Signature.getInstance("ML-DSA");
signer.initSign(keyPair.getPrivate());
signer.update(data);
byte[] signature = signer.sign();

Signature verifier = Signature.getInstance("ML-DSA");
verifier.initVerify(keyPair.getPublic());
verifier.update(data);
boolean valid = verifier.verify(signature);
```

### ML-KEM/ML-DSA 参数集

| 参数集 | 安全等级 (NIST) | 公钥大小 | 适用场景 |
|--------|----------------|----------|----------|
| ML-KEM-512 | Level 1 (~128 位) | 800 B | 轻量场景 |
| **ML-KEM-768** | Level 3 (~192 位) | 1184 B | **通用推荐** |
| ML-KEM-1024 | Level 5 (~256 位) | 1568 B | 极高安全 |
| ML-DSA-44 | Level 2 | 1312 B | 轻量签名 |
| **ML-DSA-65** | Level 3 | 1952 B | **通用推荐** |
| ML-DSA-87 | Level 5 | 2592 B | 极高安全 |

### PQC 迁移策略

1. **盘点现有算法** — 排查所有 RSA/EC/DH 使用点
2. **混合模式过渡** — 经典算法 + PQC 并行 (如 TLS 混合密钥交换)
3. **优先迁移长期密钥** — 加密归档数据面临 "harvest now, decrypt later" 威胁
4. **签名迁移可稍后** — 签名通常不面临 "先存后破" 风险
5. **测试密钥/签名大小影响** — PQC 密钥和签名显著大于经典算法

---

## 8. 密钥管理 (Key Management)

### KeyStore: JKS vs PKCS12

```java
// PKCS12 (推荐，JDK 9+ 默认格式)
KeyStore ks = KeyStore.getInstance("PKCS12");
ks.load(null, null); // 创建空 KeyStore

// 存储私钥 + 证书链
ks.setKeyEntry("server-key", privateKey,
    "keypass".toCharArray(), certificateChain);

// 存储信任的证书
ks.setCertificateEntry("ca-cert", caCertificate);

// 持久化到文件
try (var fos = new FileOutputStream("keystore.p12")) {
    ks.store(fos, "storepass".toCharArray());
}

// 从文件加载
try (var fis = new FileInputStream("keystore.p12")) {
    ks.load(fis, "storepass".toCharArray());
}
PrivateKey pk = (PrivateKey) ks.getKey("server-key", "keypass".toCharArray());
```

| 格式 | 说明 | JDK 默认 |
|------|------|----------|
| JKS | Java 专有，仅支持私钥和证书 | JDK 8 及之前 |
| **PKCS12** | 行业标准，支持更多密钥类型 | **JDK 9+** |
| JCEKS | JCE 扩展，支持 SecretKey | 不推荐 |

### KDF API: 密钥派生 (JEP 510, JDK 25)

```java
// KDF (Key Derivation Function) — 从共享密钥 / 密码派生加密密钥
// HKDF: 基于 HMAC 的提取-扩展 KDF (RFC 5869)

KDF kdf = KDF.getInstance("HKDF-SHA256");

// Extract + Expand 两阶段
SecretKey inputKey = ...; // 来自密钥协商的共享密钥
byte[] salt = SecureRandom.getInstanceStrong().generateSeed(32);
byte[] info = "application-context".getBytes(StandardCharsets.UTF_8);

// 派生 256 位 AES 密钥
SecretKey derivedKey = kdf.deriveKey("AES",
    HKDFParameterSpec.ofExtract()
        .addIKM(inputKey)
        .addSalt(salt)
        .thenExpand(info, 32));  // 32 字节 = 256 位
```

### PEM API (JEP 470/524, JDK 25/26 预览)

```java
// PEM (Privacy-Enhanced Mail) 格式: -----BEGIN XXX----- 文本格式
// JEP 470 (JDK 25 预览), JEP 524 (JDK 26 预览 2) 引入标准 API

// 编码为 PEM 字符串
String pem = PEM.encode(publicKey);
// 输出:
// -----BEGIN PUBLIC KEY-----
// MIIBIjANBgkqhk...
// -----END PUBLIC KEY-----

// 从 PEM 字符串解码
PublicKey restored = PEM.decode(pem, PublicKey.class);

// 支持类型: PublicKey, PrivateKey, X509Certificate, X509CRL, etc.
```

---

## 9. SecureRandom

### DRBG (JDK 9+)

```java
// DRBG: Deterministic Random Bit Generator (NIST SP 800-90Ar1)
// JDK 9 引入 DRBG 算法，提供可配置的安全随机数

// 默认实例 (NativePRNG 或 DRBG，取决于平台)
SecureRandom sr = new SecureRandom();

// 强随机数——可能阻塞等待足够的熵
SecureRandom strong = SecureRandom.getInstanceStrong();

// 指定 DRBG 参数
SecureRandom drbg = SecureRandom.getInstance("DRBG",
    DrbgParameters.instantiation(
        256,                                    // 安全强度 (Security Strength)
        DrbgParameters.Capability.PR_AND_RESEED, // 预测抵抗 + 重新播种
        null                                    // personalization string
    ));
```

### 熵源 (Entropy Source)

| 平台 | 默认熵源 | 说明 |
|------|----------|------|
| Linux | `/dev/urandom` | 非阻塞，启动后安全 |
| Linux | `/dev/random` | 可能阻塞 (旧内核) |
| Windows | `CryptGenRandom` | 系统级 CSPRNG |
| macOS | `SecRandomCopyBytes` | 系统级 CSPRNG |

```java
// JVM 系统属性控制熵源
// -Djava.security.egd=file:/dev/urandom
// 或在 $JAVA_HOME/conf/security/java.security 中配置:
// securerandom.source=file:/dev/urandom
```

### 性能注意事项

```java
// getInstanceStrong() 在 Linux 上默认使用 /dev/random，高并发时可能阻塞
// 推荐: 密钥生成用 getInstanceStrong()，其他场景用普通实例

// 不推荐: 每次调用都创建新实例
byte[] nonce = new byte[12];
new SecureRandom().nextBytes(nonce);  // 反复创建开销大

// 推荐: 复用实例 (SecureRandom 是线程安全的)
private static final SecureRandom RANDOM = new SecureRandom();
RANDOM.nextBytes(nonce);

// 定期重新播种 (可选的额外安全措施)
RANDOM.reseed();  // JDK 9+
```

---

## 10. SSL/TLS

### SSLContext

```java
// TLS 1.3 (推荐)
SSLContext sslContext = SSLContext.getInstance("TLSv1.3");
sslContext.init(null, null, null);  // 使用默认信任

// 自定义 KeyManager + TrustManager
KeyManagerFactory kmf = KeyManagerFactory.getInstance(
    KeyManagerFactory.getDefaultAlgorithm());
kmf.init(keyStore, "password".toCharArray());

TrustManagerFactory tmf = TrustManagerFactory.getInstance(
    TrustManagerFactory.getDefaultAlgorithm());
tmf.init(trustStore);

sslContext.init(kmf.getKeyManagers(), tmf.getTrustManagers(),
    new SecureRandom());

// 使用 HttpClient (JDK 11+)
HttpClient client = HttpClient.newBuilder()
    .sslContext(sslContext)
    .build();
```

### TLS 版本

| 版本 | JDK 支持 | 状态 |
|------|----------|------|
| TLS 1.0 | JDK 5+ | 不安全，已禁用 |
| TLS 1.1 | JDK 5+ | 不安全，已禁用 |
| TLS 1.2 | JDK 7+ | 可接受 |
| **TLS 1.3** | JDK 11+ | **推荐** |

---

## 11. 常见安全陷阱

### 陷阱 1: ECB 模式泄露数据模式

```java
// 错误: ECB 模式——相同明文块产生相同密文，暴露数据模式
Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding"); // 不安全!
// ECB 加密位图图像时，可从密文看出轮廓——著名的 "ECB 企鹅" 问题

// 正确: 使用 GCM 或 CBC
Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
```

### 陷阱 2: 硬编码密钥

```java
// 错误: 密钥直接写在代码中——反编译即可获取
SecretKey key = new SecretKeySpec("MySecretKey12345".getBytes(), "AES");

// 正确: 从 KeyStore 或环境变量加载
SecretKey key = (SecretKey) keyStore.getKey("aes-key", password);
// 或通过 KDF 从密码派生
```

### 陷阱 3: 使用 java.util.Random 生成安全材料

```java
// 错误: java.util.Random 是可预测的线性同余生成器
Random insecure = new Random();
byte[] iv = new byte[16];
insecure.nextBytes(iv); // IV 可预测 → 加密可破解

// 正确: 必须使用 SecureRandom
SecureRandom secure = new SecureRandom();
secure.nextBytes(iv);
```

### 陷阱 4: GCM nonce 复用

```java
// 错误: 固定或计数器式 nonce + 同一密钥
byte[] nonce = new byte[]{0,0,0,0,0,0,0,0,0,0,0,1}; // 固定 nonce!

// 正确: 每次加密使用随机 nonce
byte[] nonce = new byte[12];
SecureRandom.getInstanceStrong().nextBytes(nonce);
// nonce 与密文一起存储/传输
```

### 陷阱 5: 忽略认证 (Cipher without MAC)

```java
// 错误: 使用 CBC 但无完整性校验——容易受 padding oracle 攻击
Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
// 攻击者篡改密文 → 解密成功但数据被修改

// 正确: 使用 AEAD 模式 (GCM/ChaCha20-Poly1305) 或加 HMAC
Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding"); // 内置认证
```

### 陷阱 6: 禁用证书验证

```java
// 错误: 测试代码泄露到生产环境——中间人攻击
TrustManager[] trustAll = { new X509TrustManager() {
    public void checkServerTrusted(...) {} // 信任一切!
}};

// 正确: 使用系统默认信任 + 必要时添加自定义 CA
TrustManagerFactory tmf = TrustManagerFactory.getInstance("PKIX");
tmf.init(trustStore); // trustStore 包含可信 CA
```

### 安全陷阱自查清单

| 检查项 | 正确做法 |
|--------|----------|
| 加密模式 | GCM 或 ChaCha20-Poly1305 (AEAD) |
| 密钥存储 | KeyStore / HSM / 密钥管理服务 |
| 随机数 | SecureRandom，非 java.util.Random |
| GCM nonce | 每次加密随机生成 12 字节 |
| RSA 填充 | OAEP，非 PKCS1Padding |
| RSA 密钥 | 至少 2048 位，推荐 3072+ |
| 证书验证 | 生产环境必须启用 |
| 消息摘要 | SHA-256+，禁止 MD5/SHA-1 |

---

## 12. 最佳实践

### 算法选择速查

```java
// 对称加密
Cipher.getInstance("AES/GCM/NoPadding");          // 通用推荐
Cipher.getInstance("ChaCha20-Poly1305");           // 无 AES-NI 时

// 摘要
MessageDigest.getInstance("SHA-256");              // 通用
MessageDigest.getInstance("SHA3-256");             // 后量子考量

// 签名
Signature.getInstance("Ed25519");                  // 现代推荐
Signature.getInstance("ML-DSA");                   // 后量子 (JDK 24+)

// 密钥封装
KEM.getInstance("ML-KEM");                         // 后量子 (JDK 24+)

// 密钥派生
KDF.getInstance("HKDF-SHA256");                    // JDK 25+

// 随机数
SecureRandom.getInstanceStrong();                  // 密钥生成
new SecureRandom();                                // 普通用途
```

---

## 13. 核心贡献者

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

## 14. 相关链接

### 内部文档

- [安全框架](../security/security/) - 安全框架详解
- [SSL/TLS](../security/ssl/) - SSL/TLS 详解

### JEP 参考

- [JEP 329: ChaCha20 and Poly1305 Cryptographic Algorithms](https://openjdk.org/jeps/329)
- [JEP 332: Transport Layer Security (TLS) 1.3](https://openjdk.org/jeps/332)
- [JEP 339: Edwards-Curve Digital Signature Algorithm (EdDSA)](https://openjdk.org/jeps/339)
- [JEP 452: Key Encapsulation Mechanism API](https://openjdk.org/jeps/452)
- [JEP 496: Quantum-Resistant Module-Lattice-Based Key Encapsulation Mechanism](https://openjdk.org/jeps/496)
- [JEP 497: Quantum-Resistant Module-Lattice-Based Digital Signature Algorithm](https://openjdk.org/jeps/497)
- [JEP 510: Key Derivation Function API (Preview)](https://openjdk.org/jeps/510)
- [JEP 470: PEM Encodings of Cryptographic Objects (Preview)](https://openjdk.org/jeps/470)
- [JEP 524: PEM Encodings of Cryptographic Objects (Second Preview)](https://openjdk.org/jeps/524)

### 外部资源

- [JCA Reference Guide](https://docs.oracle.com/en/java/javase/21/security/java-cryptography-architecture-jca-reference-guide.html)
- [NIST Post-Quantum Cryptography](https://csrc.nist.gov/projects/post-quantum-cryptography)
- [AES-GCM (NIST SP 800-38D)](https://csrc.nist.gov/publications/detail/sp/800-38d/final)

---

**最后更新**: 2026-03-22
