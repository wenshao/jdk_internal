# Java 加密与安全 (Cryptography & Security)

> JCA/JCE 架构，位于 java.base 模块内，java.security 包 81 个文件 + javax.crypto 包 63 个文件

---

## 1. 模块概述 (Overview)

Java 加密功能不是独立模块，而是 `java.base` 模块导出的多个安全相关包。

**源码**: `src/java.base/share/classes/module-info.java`

```java
module java.base {
    // JCA - Java Cryptography Architecture
    exports java.security;
    exports java.security.cert;         // 证书 (51 个文件)
    exports java.security.interfaces;   // 密钥接口
    exports java.security.spec;         // 密钥/参数规范 (36 个文件)

    // JCE - Java Cryptography Extension
    exports javax.crypto;               // 加密引擎
    exports javax.crypto.interfaces;    // DH 密钥接口 (5 个文件)
    exports javax.crypto.spec;          // 算法参数规范 (20 个文件)

    // JAAS
    exports javax.security.auth;
    exports javax.security.auth.callback;
    exports javax.security.auth.login;
    exports javax.security.auth.spi;
    exports javax.security.auth.x500;
    exports javax.security.cert;
}
```

### 包文件统计 (Source File Counts)

| 包 | 文件数 | 说明 |
|---|---|---|
| `java.security` | 81 | JCA 核心：Provider, MessageDigest, Signature, KeyStore, PEM |
| `java.security.cert` | 51 | 证书 (Certificate)：X.509, CRL, CertPath |
| `java.security.spec` | 36 | 密钥规范 (Key Spec)：RSA, EC, EdDSA 参数 |
| `javax.crypto` | 42 | JCE 核心：Cipher, Mac, KeyGenerator, KDF, KEM |
| `javax.crypto.spec` | 20 | 算法参数：GCMParameterSpec, HKDFParameterSpec |
| `javax.crypto.interfaces` | 5 | DH/PBE 密钥接口 |
| **安全相关合计** | **约 235** | 不含 sun.security 内部实现 |

### JCA/JCE 架构 (Architecture)

```
┌──────────────────────────────────────────────────────────┐
│                    应用层 API (Application API)            │
│  Cipher, MessageDigest, Signature, KeyGenerator,          │
│  Mac, KeyAgreement, KDF, KEM, SecureRandom               │
├──────────────────────────────────────────────────────────┤
│              Engine / SPI 机制 (Engine/SPI Pattern)        │
│  CipherSpi, MessageDigestSpi, SignatureSpi,               │
│  KeyGeneratorSpi, MacSpi, KDFSpi, KEMSpi                 │
├──────────────────────────────────────────────────────────┤
│            Provider 注册与选择 (Provider Framework)         │
│  Security.getProviders(), Provider.getService()           │
├───────────┬──────────┬───────────┬────────────────────────┤
│  SUN      │ SunJCE   │ SunEC     │ SunPKCS11 / SunMSCAPI  │
│ (签名/摘要) │ (对称加密) │ (椭圆曲线) │ (PKCS#11 / Windows)   │
├───────────┴──────────┴───────────┴────────────────────────┤
│          底层实现 (Native / Software Implementation)       │
│  纯 Java 实现 / PKCS#11 硬件 / Microsoft CAPI             │
└──────────────────────────────────────────────────────────┘
```

**Provider SPI 设计模式**:

每个加密引擎类 (如 `Cipher`) 都对应一个 SPI 接口 (如 `CipherSpi`)。应用通过 `getInstance()` 工厂方法获取实例，框架根据 Provider 注册查找对应的 SPI 实现。

---

## 2. java.security 包核心类 (JCA Core, 81 files)

### 2.1 引擎类 (Engine Classes)

| 类 | SPI | 说明 |
|---|---|---|
| `MessageDigest` | `MessageDigestSpi` | 消息摘要 (Hash)：SHA-256, SHA-3 |
| `Signature` | `SignatureSpi` | 数字签名：Ed25519, RSA, ECDSA |
| `KeyPairGenerator` | `KeyPairGeneratorSpi` | 非对称密钥对生成 |
| `KeyFactory` | `KeyFactorySpi` | 密钥规范转换 |
| `KeyStore` | `KeyStoreSpi` | 密钥和证书存储 (PKCS12, JKS) |
| `SecureRandom` | `SecureRandomSpi` | 安全随机数生成器 (DRBG) |
| `AlgorithmParameters` | `AlgorithmParametersSpi` | 算法参数编解码 |
| `AlgorithmParameterGenerator` | `AlgorithmParameterGeneratorSpi` | 算法参数生成 |

### 2.2 Provider 框架

| 类 | 说明 |
|---|---|
| `Provider` | 安全提供者基类，注册算法实现 |
| `Security` | 全局安全属性和 Provider 管理 |
| `AuthProvider` | 需要登录认证的 Provider |

### 2.3 密钥接口 (Key Interfaces)

| 接口 | 说明 |
|---|---|
| `Key` | 所有密钥的根接口 |
| `PublicKey` | 公钥 |
| `PrivateKey` | 私钥 |
| `AsymmetricKey` | 非对称密钥 (JDK 新增) |
| `KeyPair` | 密钥对容器 |

### 2.4 PEM 编解码 (JDK 新增, Preview)

| 类 | 说明 |
|---|---|
| `PEM` | PEM 格式接口 (标注 `@PreviewFeature`) |
| `PEMEncoder` | 将密钥/证书编码为 PEM 文本 |
| `PEMDecoder` | 从 PEM 文本解码密钥/证书 |
| `DEREncodable` | DER 编码接口 |

### 2.5 权限与策略 (Permission & Policy)

| 类 | 说明 |
|---|---|
| `Permission` | 权限抽象基类 |
| `AllPermission` | 全部权限 |
| `BasicPermission` | 基本权限 |
| `SecurityPermission` | 安全操作权限 |
| `Policy` | 安全策略 (已弃用) |
| `AccessController` | 访问控制 (已弃用) |
| `ProtectionDomain` | 保护域 |

### 2.6 其他

| 类 | 说明 |
|---|---|
| `SecureClassLoader` | 安全类加载器 |
| `CodeSource` | 代码来源 |
| `CodeSigner` | 代码签名者 |
| `Timestamp` | 签名时间戳 |
| `DrbgParameters` | DRBG 随机数参数 (JDK 9+) |
| `CryptoPrimitive` | 密码原语枚举 |
| `AlgorithmConstraints` | 算法约束接口 |

---

## 3. javax.crypto 包核心类 (JCE Core, 42 files)

### 3.1 引擎类 (Engine Classes)

| 类 | SPI | 说明 |
|---|---|---|
| `Cipher` | `CipherSpi` | 对称/非对称加解密 |
| `Mac` | `MacSpi` | 消息认证码 (HMAC) |
| `KeyGenerator` | `KeyGeneratorSpi` | 对称密钥生成 |
| `KeyAgreement` | `KeyAgreementSpi` | 密钥协商 (DH, ECDH) |
| `SecretKeyFactory` | `SecretKeyFactorySpi` | 对称密钥工厂 |
| `ExemptionMechanism` | `ExemptionMechanismSpi` | 豁免机制 |
| `KDF` | `KDFSpi` | 密钥派生函数 (JDK 新增) |
| `KEM` | `KEMSpi` | 密钥封装机制 (JDK 21+，后量子密码学准备) |

### 3.2 密钥与数据

| 类 | 说明 |
|---|---|
| `SecretKey` | 对称密钥接口 |
| `SealedObject` | 加密封装的对象 |
| `EncryptedPrivateKeyInfo` | PKCS#8 加密私钥 |
| `CipherInputStream` | 加密输入流 |
| `CipherOutputStream` | 加密输出流 |
| `NullCipher` | 空密码 (不加密，测试用) |

### 3.3 算法参数规范 (javax.crypto.spec, 20 files)

| 类 | 说明 |
|---|---|
| `SecretKeySpec` | 通用对称密钥规范 |
| `GCMParameterSpec` | AES-GCM 参数 (IV + Tag 长度) |
| `IvParameterSpec` | 初始化向量 |
| `ChaCha20ParameterSpec` | ChaCha20 参数 (JDK 11+) |
| `PBEKeySpec` | 基于口令的密钥规范 |
| `PBEParameterSpec` | PBE 参数 (盐 + 迭代次数) |
| `HKDFParameterSpec` | HKDF 密钥派生参数 (JDK 新增) |
| `HPKEParameterSpec` | HPKE 混合公钥加密参数 (JDK 新增) |
| `OAEPParameterSpec` | RSA-OAEP 参数 |
| `DHParameterSpec` | DH 参数 |
| `DHPublicKeySpec` / `DHPrivateKeySpec` | DH 密钥规范 |
| `DESKeySpec` / `DESedeKeySpec` | DES 密钥规范 (遗留) |
| `RC2ParameterSpec` / `RC5ParameterSpec` | RC 参数 (遗留) |

---

## 4. 算法支持 (Algorithm Support)

### 4.1 对称加密 (Symmetric Encryption)

| 算法 | 密钥长度 (bits) | 模式 | 状态 |
|---|---|---|---|
| AES | 128/192/256 | GCM, CBC, CTR, ECB | 推荐 (AES-GCM) |
| ChaCha20 | 256 | Poly1305 | 推荐 (JDK 11+) |
| DES | 56 | CBC, ECB | 已弃用 |
| DESede (3DES) | 168 | CBC, ECB | 遗留 |

### 4.2 消息摘要 (Message Digest / Hash)

| 算法 | 输出 (bits) | 状态 |
|---|---|---|
| SHA-256 | 256 | 推荐 |
| SHA-384 | 384 | 推荐 |
| SHA-512 | 512 | 推荐 |
| SHA-3-256/384/512 | 可变 | 推荐 (JDK 9+) |
| SHA-1 | 160 | 签名已弃用 |
| MD5 | 128 | 不安全 |

### 4.3 数字签名 (Digital Signature)

| 算法 | 密钥类型 | 状态 |
|---|---|---|
| Ed25519 | EdDSA | 推荐 (JDK 15+) |
| Ed448 | EdDSA | 推荐 (JDK 15+) |
| ECDSA | EC | 推荐 |
| SHA256withRSA | RSA | 推荐 (RSA >= 2048) |
| DSA | DSA | 遗留 |

### 4.4 密钥协商 (Key Agreement)

| 算法 | 说明 |
|---|---|
| X25519 | 推荐 (JDK 11+) |
| X448 | 推荐 (JDK 11+) |
| ECDH | EC 密钥协商 |
| DH | 传统 Diffie-Hellman |

### 4.5 密钥派生 (KDF) 与密钥封装 (KEM)

| 类 | 算法 | 说明 |
|---|---|---|
| `KDF` | HKDF-SHA256 等 | 从共享密钥派生子密钥 (JDK 新增) |
| `KEM` | DHKEM 等 | 密钥封装机制，后量子密码学准备 (JDK 21+) |

---

## 5. SSL/TLS 支持 (javax.net.ssl)

SSL/TLS 类位于 `javax.net.ssl` 包（同样在 java.base 中）。

### 5.1 核心类

| 类 | 说明 |
|---|---|
| `SSLContext` | TLS 上下文，管理密钥和信任 |
| `SSLEngine` | 非阻塞 TLS 引擎 |
| `SSLSocket` / `SSLServerSocket` | 阻塞 TLS 套接字 |
| `SSLSocketFactory` | TLS 套接字工厂 |
| `TrustManager` / `KeyManager` | 信任和密钥管理 |
| `X509TrustManager` | X.509 证书验证 |
| `HttpsURLConnection` | HTTPS 连接 |

### 5.2 协议支持

| 协议 | 状态 |
|---|---|
| TLS 1.3 | 默认，推荐 |
| TLS 1.2 | 支持，兼容 |
| TLS 1.1 / 1.0 | 已禁用 |
| SSLv3 | 已禁用 |

---

## 6. 使用示例 (Usage Examples)

### 6.1 AES-GCM 认证加密 (Authenticated Encryption)

```java
// 密钥生成
KeyGenerator kg = KeyGenerator.getInstance("AES");
kg.init(256);
SecretKey key = kg.generateKey();

// 加密
byte[] iv = new byte[12];  // GCM 推荐 12 字节 IV
new SecureRandom().nextBytes(iv);
Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
cipher.init(Cipher.ENCRYPT_MODE, key, new GCMParameterSpec(128, iv));
byte[] ciphertext = cipher.doFinal(plaintext);

// 解密
cipher.init(Cipher.DECRYPT_MODE, key, new GCMParameterSpec(128, iv));
byte[] decrypted = cipher.doFinal(ciphertext);
```

### 6.2 Ed25519 数字签名

```java
// 密钥生成
KeyPairGenerator kpg = KeyPairGenerator.getInstance("Ed25519");
KeyPair kp = kpg.generateKeyPair();

// 签名
Signature sig = Signature.getInstance("Ed25519");
sig.initSign(kp.getPrivate());
sig.update(data);
byte[] signature = sig.sign();

// 验签
sig.initVerify(kp.getPublic());
sig.update(data);
boolean valid = sig.verify(signature);
```

### 6.3 HKDF 密钥派生

```java
KDF hkdf = KDF.getInstance("HKDF-SHA256");
SecretKey derived = hkdf.deriveKey("AES",
    HKDFParameterSpec.ofExtract()
        .addIKM(sharedSecret)
        .addSalt(salt)
        .thenExpand(info, 32)
        .build());
```

### 6.4 KEM 密钥封装

```java
// 接收方生成密钥对
KeyPairGenerator kpg = KeyPairGenerator.getInstance("X25519");
KeyPair kp = kpg.generateKeyPair();

// 发送方封装
KEM kem = KEM.getInstance("DHKEM");
KEM.Encapsulator enc = kem.newEncapsulator(kp.getPublic());
KEM.Encapsulated encapsulated = enc.encapsulate();
SecretKey sharedSecret = encapsulated.key();       // 共享密钥
byte[] encapsulation = encapsulated.encapsulation(); // 发送给接收方

// 接收方解封装
KEM.Decapsulator dec = kem.newDecapsulator(kp.getPrivate());
SecretKey recovered = dec.decapsulate(encapsulation);
```

### 6.5 KeyStore 密钥存储

```java
KeyStore ks = KeyStore.getInstance("PKCS12");
try (InputStream is = Files.newInputStream(keystorePath)) {
    ks.load(is, password);
}
PrivateKey pk = (PrivateKey) ks.getKey("mykey", keyPassword);
Certificate cert = ks.getCertificate("mykey");
```

---

## 7. 安全最佳实践 (Security Best Practices)

### 7.1 算法选择指南

| 用途 | 推荐算法 | 避免 |
|---|---|---|
| 对称加密 | AES-256-GCM | DES, 3DES, ECB 模式 |
| 哈希 | SHA-256 / SHA-3-256 | MD5, SHA-1 |
| 数字签名 | Ed25519, ECDSA | DSA |
| 密钥交换 | X25519, ECDH | 低参数 DH |
| 密钥派生 | HKDF-SHA256 | 简单哈希 |
| 口令哈希 | PBKDF2 (10万+迭代) | 明文存储 |
| TLS | 1.3 | 1.0, 1.1 |

### 7.2 常见错误

| 错误 | 正确做法 |
|---|---|
| ECB 模式加密 | 使用 GCM (认证加密) |
| 固定 IV | 每次加密使用随机 IV |
| 信任所有证书 | 使用默认 TrustManager 或自定义验证 |
| 硬编码密钥 | 使用 KeyStore 或外部密钥管理 |

---

## 8. 相关链接 (References)

- [Java Cryptography Architecture (JCA) Reference Guide](https://docs.oracle.com/en/java/javase/21/security/java-cryptography-architecture-jca-reference-guide.html)
- [JEP 478: Key Derivation Function API](https://openjdk.org/jeps/478)
- [JEP 452: Key Encapsulation Mechanism API](https://openjdk.org/jeps/452)
- [源码 java.security](https://github.com/openjdk/jdk/tree/master/src/java.base/share/classes/java/security)
- [源码 javax.crypto](https://github.com/openjdk/jdk/tree/master/src/java.base/share/classes/javax/crypto)
- 本地源码: `src/java.base/share/classes/java/security/`, `src/java.base/share/classes/javax/crypto/`
