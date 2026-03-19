# JDK 26 Security Component Summary

> Commits: 234 (5.9% of total)
> Key Contributors: Weijun Wang, Alexey Semenyuk, Artur Barashev, Sean Coffey

---

## Overview

JDK 26 brings significant security enhancements, including post-quantum cryptography improvements, new encryption standards support, and certificate validation enhancements.

---

## Post-Quantum Cryptography

### ML-KEM and ML-DSA Improvements

JDK 26 continues the post-quantum cryptography journey started in earlier releases:

| Issue | Description | Impact |
|-------|-------------|--------|
| 8371259 | ML-DSA AVX2/AVX512 intrinsics | ⭐⭐⭐⭐⭐ |
| 8347938 | ML-KEM/ML-DSA private key encoding | ⭐⭐⭐⭐ |
| 8349732 | JAR signing with ML-DSA | ⭐⭐⭐⭐ |

**JDK-8371259**: ML-DSA intrinsics for x86

| Metric | Value |
|--------|-------|
| Additions | 1,572 |
| Deletions | 703 |
| Author | Volodymyr Paprotski |

This adds AVX2 and AVX512 intrinsics for ML-DSA, significantly improving performance on modern CPUs.

### Hybrid Public Key Encryption (HPKE)

**JDK-8325448**: Hybrid Public Key Encryption

| Metric | Value |
|--------|-------|
| Additions | 2,120 |
| Deletions | 230 |
| Author | Weijun Wang |

Implements RFC 9180 Hybrid Public Key Encryption standard.

---

## JAR Signing

### ML-DSA Support

**JDK-8349732**: Support for JARs signed with ML-DSA

Allows JAR files to be signed with post-quantum signatures:
- ML-DSA-44
- ML-DSA-65
- ML-DSA-87

### Keytool Improvements

| Issue | Description |
|-------|-------------|
| 8354469 | Don't expose password in plain text when command is piped |
| 8374808 | New KeyStore methods to return certificate chain |

---

## Certificate Validation

### Algorithm Constraints

| Issue | Description | Author |
|-------|-------------|--------|
| 8367104 | RSASSA-PSS parameter validation | Artur Barashev |
| 8365820 | Certificate scope constraints | Artur Barashev |
| 8365953 | Handshake session certificate fix | Artur Barashev |
| 8368032 | Enhanced certificate checking | Jamil Nimeh |

### Trust Store Updates

| Issue | Description | Author |
|-------|-------------|--------|
| 8361212 | Remove AffirmTrust root CAs | Rajan Halade |
| 8359170 | Add 2 TLS and 2 CS Sectigo roots | Rajan Halade |
| 8369282 | Distrust Chunghwa ePKI Root | Mark Powers |

---

## Cryptographic Providers

### SunPKCS11

| Issue | Description |
|-------|-------------|
| 8343232 | PKCS#12 KeyStore support for RFC 9879 |

### SunJCE

| Issue | Description | Author |
|-------|-------------|--------|
| 8244336 | Restrict algorithms at JCE layer | Valerie Peng |
| 8368984 | Cipher transformation validation | Valerie Peng |

---

## Kerberos

| Issue | Description | Author |
|-------|-------------|--------|
| 8356997 | /etc/krb5.conf parser should allow include/includedir | Weijun Wang |

---

## JAAS

### FFM-based Rewrite

**JDK-8277489**: Rewrite JAAS UnixLoginModule with FFM (Foreign Function & Memory)

| Metric | Value |
|--------|-------|
| Additions | 220 |
| Deletions | 165 |
| Author | Weijun Wang |

Migrates native code to use the FFM API instead of JNI.

---

## Secure Random

No major changes, but general improvements to entropy sources.

---

## Key Commits by Impact

| Issue | Description | +/- | Author |
|-------|-------------|-----|--------|
| 8374219 | jpackage Executor fixes | 10,795 | Alexey Semenyuk |
| 8336695 | Commons BCEL 6.10.0 | 3,589 | Joe Wang |
| 8325448 | HPKE implementation | 2,350 | Weijun Wang |
| 8376038 | java/sql JUnit migration | 4,648 | Justin Lu |
| 8371259 | ML-DSA intrinsics | 2,275 | Volodymyr Paprotski |
| 8347938 | ML-KEM/ML-DSA key encoding | 1,774 | Weijun Wang |

---

## jpackage Security

Alexey Semenyuk contributed significant improvements to jpackage security:

| Issue | Description |
|-------|-------------|
| 8374219 | Fix issues in Executor class |
| 8373631 | Improve functional classes |
| 8371438 | Handle --mac-sign edge cases |
| 8379426 | Runtime bundle version suffix |
| 8370126 | Signing testing improvements |

---

## Top Contributors

| Rank | Contributor | Focus Area |
|------|-------------|------------|
| 1 | Alexey Semenyuk | jpackage |
| 2 | Weijun Wang | Crypto, Kerberos |
| 3 | Artur Barashev | Certificates |
| 4 | Valerie Peng | JCE |
| 5 | Sean Coffey | TLS debugging |
| 6 | Jamil Nimeh | Certificate validation |
| 7 | Rajan Halade | Root CAs |
| 8 | Mark Powers | PKCS#12 |

---

## Test Migration

Security tests migrated from TestNG to JUnit:

| Issue | Description |
|-------|-------------|
| 8376038 | java/sql tests |
| 8379798 | javax/xml/jaxp functional tests |
| 8378111 | java/util/jar tests |

---

## Security Best Practices

### What's New

1. **Post-Quantum Ready**: ML-DSA and ML-KEM fully supported
2. **Modern Key Storage**: HPKE for modern encryption
3. **Better Validation**: Enhanced certificate chain checking
4. **Clean Debugging**: Improved TLS logging

### What's Deprecated/Removed

1. **AffirmTrust Roots**: Removed due to distrust
2. **Legacy Kerb5 Parser**: More permissive now

---

## Migration Notes

### For Application Developers

1. **Test with ML-DSA**: Consider testing JAR signing with post-quantum algorithms
2. **Certificate Chains**: Verify chains don't depend on removed root CAs
3. **HPKE**: New API available for hybrid encryption

### For Security Auditors

1. **New Intrinsics**: ML-DSA now has hardware acceleration
2. **Debug Output**: SSLLogger uses System.Logger now
3. **Algorithm Restrictions**: JCE layer has new restrictions

### For DevOps

1. **jpackage**: Signing improvements may affect build scripts
2. **Kerberos**: Parser changes may affect configuration parsing

---

## Compliance Notes

- **FIPS 203**: ML-KEM implementation
- **FIPS 204**: ML-DSA implementation  
- **RFC 9180**: HPKE implementation
- **RFC 9879**: PKCS#12 updates

---

*Last updated: 2026-03-19*
