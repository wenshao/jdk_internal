# 安全 (Security) JEPs

> JDK 21-26 安全相关 JEP 汇总

---
## 目录

1. [概览](#1-概览)
2. [Key Encapsulation Mechanism API (JEP 452)](#2-key-encapsulation-mechanism-api-jep-452)
3. [Key Derivation Function API (JEP 510)](#3-key-derivation-function-api-jep-510)
4. [PEM Encodings (JEP 470)](#4-pem-encodings-jep-470)
5. [相关链接](#5-相关链接)

---


## 1. 概览

| JEP | 标题 | JDK | 状态 | 说明 |
|-----|------|-----|------|------|
| [JEP 451](jep-451.md) | Multi-Release JAR Files | 21 | ⚠️ 废弃 | 准备移除 |
| [JEP 452](jep-452.md) | Key Encapsulation Mechanism API | 21 | ✅ 正式 | 密钥封装 |
| [JEP 470](jep-470.md) | PEM Encodings | 25 | 🔍 预览 | PEM 编码 |
| [JEP 510](jep-510.md) | Key Derivation Function API | 25 | ✅ 正式 | 密钥派生 |

---

## 2. Key Encapsulation Mechanism API (JEP 452)

### 核心概念

```java
// 密钥封装
public class KeyStore {
    private static final Encapsulator ENCAPSULATOR = 
        KeyEncapsulator.getInstance("AES");
    
    public static EncapsulatedKey generateKey() {
        return ENCAPSULATOR.generateKey(
            new KeySpec.Builder("AES", 256).build()
        );
    }
    
    public static byte[] unwrap(EncapsulatedKey key, char[] password) {
        return key.unwrap(password);
    }
}
```

**详见**：[JEP 452](jep-452.md)

---

## 3. Key Derivation Function API (JEP 510)

### 核心用法

```java
// 密钥派生
public class KeyDerivation {
    private static final KDF kdf = KDF.getInstance("HKDF");
    
    public static SecretKey deriveKey(byte[] password, byte[] salt) {
        return kdf.generateSecretKey(
            new KDFSpec.Builder("HKDF", 256)
                .withSalt(salt)
                .build(),
            password
        );
    }
}
```

**详见**：[JEP 510](jep-510.md)

---

## 4. PEM Encodings (JEP 470)

PEM 编码支持，简化证书处理。

---

## 5. 相关链接

- Java 安全指南 
- [加密 API 文档](https://docs.oracle.com/en/java/javase/21/security/)
