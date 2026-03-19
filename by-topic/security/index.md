# 安全国际化

加密、TLS、本地化等。

---

## 主题列表

### [安全特性](security/)

加密、TLS、后量子密码。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 8 | TLS 1.2 (默认) | - |
| JDK 11 | **TLS 1.3** (默认)、ChaCha20-Poly1305 | JEP 332, JEP 329 |
| JDK 15 | 禁用弱签名算法 | - |
| JDK 17 | KMAC、SHA-3 家族 | JEP 370 |
| JDK 21 | 增强密码套件、HSS/LMS 签名 | - |
| JDK 22-23 | KDF API (预览) | JEP 495, JEP 508 |
| JDK 26 | **ML-DSA** 后量子签名、**KDF API** (正式)、**PEM 格式** | JEP 518, JEP 510, JEP 470 |

→ [安全特性时间线](security/timeline.md)

### [国际化](i18n/)

Java 国际化 (i18n) 从 JDK 1.0 到 JDK 26 的完整演进。

| 版本 | 主要变化 | 说明 |
|------|----------|------|
| JDK 1.0 | Locale, ResourceBundle | 基础 i18n |
| JDK 1.1 | DecimalFormat, SimpleDateFormat | 格式化 |
| JDK 5 | Formatter, MessageFormat | 增强格式化 |
| JDK 6 | Unicode 4.0 | 规范化 |
| JDK 8 | CLDR 数据 | 更准确本地化 |
| JDK 13 | Unicode 13 | 新字符支持 |
| JDK 18 | Unicode 扩展 | EAI 支持 |

→ [国际化时间线](i18n/timeline.md)

---

## 学习路径

1. **入门**: [国际化](i18n/) → 多语言支持
2. **进阶**: [安全特性](security/) → 加密与 TLS
3. **深入**: [安全特性](security/) → 后量子密码 → 前沿安全
