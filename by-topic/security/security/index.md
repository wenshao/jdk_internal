# 安全

> 加密、签名、SSL/TLS、安全策略演进历程

[← 返回安全](../)

---

## 快速概览

```
JDK 1.0 ── JDK 1.2 ── JDK 1.4 ── JDK 6 ── JDK 7 ── JDK 11 ── JDK 17 ── JDK 21 ── JDK 24
   │         │         │        │        │        │        │        │        │
安全    JAAS     JCE     TLS 1.2  TLS 1.3  ChaCha20  密钥    后量子  签名
策略    认证     加密    AES/GCM  ALPN    Poly1305 封装    准备    增强
沙箱    授权     扩展             减少     密码    JEP     密码    SM4
                           RTT     套件    461    算法    支持
```

### 核心演进

| 版本 | 特性 | 说明 | JEP |
|------|------|------|-----|
| **JDK 1.0** | 安全策略 | Sandbox 模型 | - |
| **JDK 1.2** | JAAS | 认证授权 | JSR 196 |
| **JDK 1.4** | JCE | 加密扩展 | JSR 141 |
| **JDK 6** | TLS 1.2 | AES/GCM 模式 | - |
| **JDK 7** | AES-GCM | 认证加密 | - |
| **JDK 11** | TLS 1.3 | 性能优化 | - |
| **JDK 11** | ChaCha20-Poly1305 | 现代密码学 | - |
| **JDK 15** | 禁用弱签名 | SHA-1 | - |
| **JDK 17** | 密钥封装 | JEP 461 | - |
| **JDK 21** | 后量子密码学 | 准备 | - |
| **JDK 24** | SM4 算法 | 中国国密 | - |

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 安全团队 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Weijun Wang | 174 | Oracle | 密码学, 签名 |
| 2 | Xue-Lei Andrew Fan | 116 | Oracle | SSL/TLS |
| 3 | Sean Mullan | 71 | Oracle | 安全策略 |
| 4 | Valerie Peng | 54 | Oracle | 加密算法 |
| 5 | Jamil Nimeh | 39 | Oracle | SSL/TLS |
| 6 | Hai-May Chao | 36 | Oracle | 密码学 |
| 7 | Anthony Scarpino | 32 | Oracle | 安全核心 |

---

## 加密算法

### 对称加密

```java
import javax.crypto.*;
import javax.crypto.spec.*;
import java.security.*;

// AES 加密
Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");

// 生成密钥
KeyGenerator keyGen = KeyGenerator.getInstance("AES");
keyGen.init(256);
SecretKey key = keyGen.generateKey();

// 初始化
cipher.init(Cipher.ENCRYPT_MODE, key);

// 加密
byte[] plaintext = "Hello AES".getBytes();
byte[] ciphertext = cipher.doFinal(plaintext);

// 解密
cipher.init(Cipher.DECRYPT_MODE, key);
byte[] decrypted = cipher.doFinal(ciphertext);
```

### 非对称加密

```java
import java.security.*;
import java.security.interfaces.*;
import javax.crypto.*;

// RSA 密钥对
KeyPairGenerator keyGen = KeyPairGenerator.getInstance("RSA");
keyGen.initialize(2048);
KeyPair keyPair = keyGen.generateKeyPair();

// 公钥加密
Cipher cipher = Cipher.getInstance("RSA/ECB/PKCS1Padding");
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

// SHA-3 (JDK 16+)
MessageDigest sha3 = MessageDigest.getInstance("SHA3-256");
byte[] hash3 = sha3.digest("Hello".getBytes());
```

### HMAC

```java
import javax.crypto.*;
import javax.crypto.spec.*;
import java.security.*;

// HMAC-SHA256
SecretKeySpec keySpec = new SecretKeySpec(
    "secret".getBytes(), "HmacSHA256");
Mac mac = Mac.getInstance("HmacSHA256");
mac.init(keySpec);
byte[] hmac = mac.doFinal("Hello".getBytes());
```

---

## 数字签名

### 签名与验证

```java
import java.security.*;
import java.security.interfaces.*;

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

### EdDSA (JDK 15+)

```java
// Ed25519 (现代签名算法)
KeyPairGenerator keyGen = KeyPairGenerator.getInstance("Ed25519");
KeyPair keyPair = keyGen.generateKeyPair();

Signature sig = Signature.getInstance("Ed25519");
sig.initSign(keyPair.getPrivate());
sig.update("Hello".getBytes());
byte[] signed = sig.sign();
```

---

## SSL/TLS

### TLS 1.3

```java
import javax.net.ssl.*;
import java.net.*;

// 启用 TLS 1.3
SSLContext sslContext = SSLContext.getInstance("TLSv1.3");
sslContext.init(null, null, null);

// 创建 HTTPS 连接
HttpsURLConnection.setDefaultSSLSocketFactory(
    sslContext.getSocketFactory());

URL url = new URL("https://example.com");
HttpsURLConnection conn = (HttpsURLConnection) url.openConnection();
conn.setSSLSocketFactory(sslContext.getSocketFactory());
```

### SSLContext 配置

```java
// TrustManager (信任所有证书 - 仅测试)
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

SSLContext sslContext = SSLContext.getInstance("TLS");
sslContext.init(null, trustAllCerts, new java.security.SecureRandom());
```

### 密码套件配置

```java
// 启用 ChaCha20-Poly1305
SSLContext sslContext = SSLContext.getInstance("TLS");
sslContext.init(null, null, null);

SSLSocketFactory factory = sslContext.getSocketFactory();
SSLSocket socket = (SSLSocket) factory.createSocket("example.com", 443);

// 设置密码套件
String[] enabledCipherSuites = {
    "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256",
    "TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256",
    "TLS_AES_256_GCM_SHA384"  // TLS 1.3
};
socket.setEnabledCipherSuites(enabledCipherSuites);
```

---

## 密钥管理

### KeyStore

```java
import java.security.*;
import java.security.cert.Certificate;
import java.io.*;

// 创建 KeyStore
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
try (FileInputStream fis = new FileInputStream("keystore.p12")) {
    keyStore.load(fis, "password".toCharArray());
}

// 获取密钥
Key storedKey = keyStore.getKey("mykey", "password".toCharArray());
```

### 证书

```java
import java.security.cert.*;
import java.io.*;

// 加载证书
CertificateFactory cf = CertificateFactory.getInstance("X.509");
try (FileInputStream fis = new FileInputStream("cert.pem")) {
    X509Certificate cert = (X509Certificate) cf.generateCertificate(fis);

    // 验证证书
    cert.checkValidity();

    // 获取信息
    Principal subject = cert.getSubjectDN();
    Principal issuer = cert.getIssuerDN();
    Date notBefore = cert.getNotBefore();
    Date notAfter = cert.getNotAfter();
}
```

---

## JCE (Java Cryptography Extension)

### 无限强度策略

**JDK 8 之前**: 需要安装 JCE Unlimited Strength

**JDK 8+**: 默认启用

```java
// 检查密钥限制
int maxKeySize = javax.crypto.Cipher.getMaxAllowedKeyLength("AES");
System.out.println("Max AES key size: " + maxKeySize);
```

---

## 安全策略

### Policy 文件

```java
// grant 权限
grant {
    permission java.io.FilePermission "/tmp/*", "read,write";
    permission java.net.SocketPermission "example.com:80", "connect";
    permission java.security.AllPermission;  // 所有权限 (不推荐)
};
```

### AccessController

```java
import java.security.*;

// 特权操作
AccessController.doPrivileged((PrivilegedAction<Void>) () -> {
    System.setProperty("java.io.tmpdir", "/tmp");
    return null;
});
```

---

## 最佳实践

### 密码选择

| 用途 | 推荐算法 |
|------|----------|
| 对称加密 | AES-256-GCM |
| 非对称加密 | RSA-2048+ / ECDSA / Ed25519 |
| 消息摘要 | SHA-256 / SHA-3 |
| HMAC | HMAC-SHA256 |
| 密钥协商 | ECDHE |
| TLS | TLS 1.3 |

### 常见错误

```java
// ❌ 不要使用
Cipher.getInstance("DES");              // 弱加密
Cipher.getInstance("MD5");              // 弱哈希
MessageDigest.getInstance("SHA-1");     // 已弃用

// ✅ 推荐
Cipher.getInstance("AES/GCM/NoPadding");
MessageDigest.getInstance("SHA-256");
```

---

## 相关链接

### 本地文档

- [国际化](../i18n/) - 字符编码
- [网络](../../concurrency/network/) - SSL/TLS

### 外部参考

**JSR 文档:**
- [JSR 141: JCE 1.2.1](https://jcp.org/en/jsr/detail?id=141)
- [JSR 196: JAAS](https://jcp.org/en/jsr/detail?id=196)

**技术文档:**
- [Oracle Java Security](https://www.oracle.com/java/technologies/javase/seccodeguide.html)
- [TLS 1.3 in Java](https://openjdk.org/groups/security/)
- [Cipher Suites](https://docs.oracle.com/en/java/javase/21/security/oracle-providers.html)
