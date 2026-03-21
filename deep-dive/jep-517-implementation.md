# JEP 517 深入分析: HTTP/3 for the HTTP Client API

> 本文档深入分析 JEP 517 的源码实现，适合希望理解 HTTP/3 内部机制的读者。

---

## 1. 架构概览

### 1.1 协议栈对比

```
HTTP/1.1:
┌─────────────────┐
│    HTTP/1.1     │
├─────────────────┤
│      TCP        │
├─────────────────┤
│      IP         │
└─────────────────┘

HTTP/2:
┌─────────────────┐
│     HTTP/2      │
├─────────────────┤
│      TCP        │  ← 队头阻塞
├─────────────────┤
│     TLS 1.2+    │
├─────────────────┤
│      IP         │
└─────────────────┘

HTTP/3:
┌─────────────────┐
│     HTTP/3      │
├─────────────────┤
│     QUIC        │  ← 无队头阻塞
├─────────────────┤
│    TLS 1.3      │  ← 内置于 QUIC
├─────────────────┤
│      UDP        │
├─────────────────┤
│      IP         │
└─────────────────┘
```

### 1.2 JDK 实现架构

```
java.net.http API
    │
    ▼
┌─────────────────────────────────────────────────────┐
│                  HttpClient                         │
├─────────────────────────────────────────────────────┤
│  Http3ClientImpl                                    │
│  ├── Http3Connection                                │
│  │   ├── Http3Exchange                              │
│  │   └── Http3FrameOrderVerifier                    │
│  └── AltSvcProcessor                                │
├─────────────────────────────────────────────────────┤
│                   QUIC Layer                        │
├─────────────────────────────────────────────────────┤
│  jdk.internal.net.quic                              │
│  ├── QuicTLSEngine                                  │
│  ├── QuicOneRttContext                              │
│  ├── QuicVersion                                    │
│  └── QuicTransportParametersConsumer                │
├─────────────────────────────────────────────────────┤
│                   TLS Layer                         │
├─────────────────────────────────────────────────────┤
│  sun.security.ssl                                   │
│  ├── QuicCipher                                     │
│  ├── QuicKeyManager                                 │
│  ├── QuicTLSEngineImpl                              │
│  └── QuicTransportParametersExtension               │
└─────────────────────────────────────────────────────┘
    │
    ▼
  UDP Socket
```

---

## 2. 核心类分析

### 2.1 QuicTLSEngine

**文件**: `src/java.base/share/classes/jdk/internal/net/quic/QuicTLSEngine.java`

**职责**: 管理 QUIC 连接的 TLS 握手

```java
public class QuicTLSEngine {
    
    // 加密级别
    public enum EncryptionLevel {
        INITIAL,      // 初始密钥
        HANDSHAKE,    // 握手密钥
        APPLICATION   // 应用数据密钥
    }
    
    // 初始化 TLS 上下文
    public void init(QuicTLSContext context) {
        // 设置 TLS 1.3 参数
        // 配置加密套件
        // 初始化密钥材料
    }
    
    // 处理握手数据
    public void handshake(byte[] data, EncryptionLevel level) {
        // 处理 TLS 记录
        // 更新加密级别
        // 生成响应
    }
    
    // 获取当前加密级别
    public EncryptionLevel getEncryptionLevel();
    
    // 获取 1-RTT 密钥
    public QuicOneRttContext getOneRttContext();
}
```

### 2.2 QuicCipher

**文件**: `src/java.base/share/classes/sun/security/ssl/QuicCipher.java`

**职责**: QUIC 数据包加密/解密

```java
class QuicCipher {
    
    // 支持的加密套件
    private static final String[] SUPPORTED_CIPHERS = {
        "TLS_AES_128_GCM_SHA256",
        "TLS_AES_256_GCM_SHA384",
        "TLS_CHACHA20_POLY1305_SHA256"
    };
    
    // 加密 QUIC 包
    public byte[] encrypt(byte[] plaintext, 
                          byte[] key, 
                          byte[] nonce, 
                          byte[] aad) {
        // AEAD 加密
        // 返回密文 + 认证标签
    }
    
    // 解密 QUIC 包
    public byte[] decrypt(byte[] ciphertext,
                          byte[] key,
                          byte[] nonce,
                          byte[] aad) {
        // AEAD 解密
        // 验证认证标签
    }
}
```

### 2.3 Http3Connection

**文件**: `src/java.net.http/share/classes/jdk/internal/net/http/Http3Connection.java`

**职责**: 管理 HTTP/3 连接

```java
class Http3Connection {
    
    private final QuicConnection quicConn;
    private final Http3FrameOrderVerifier frameVerifier;
    
    // 发送 HTTP/3 请求
    public CompletableFuture<HttpResponse> send(HttpRequest request) {
        // 1. 创建 QUIC 流
        // 2. 发送 HTTP/3 帧
        // 3. 接收响应
    }
    
    // 发送 HEADERS 帧
    private void sendHeadersFrame(int streamId, HttpHeaders headers) {
        // QPACK 编码
        // 发送 HEADERS 帧
    }
    
    // 发送 DATA 帧
    private void sendDataFrame(int streamId, byte[] data) {
        // 分片发送
    }
}
```

### 2.4 AltSvcProcessor

**文件**: `src/java.net.http/share/classes/jdk/internal/net/http/AltSvcProcessor.java`

**职责**: 处理 Alt-Svc 头，发现 HTTP/3 端点

```java
class AltSvcProcessor {
    
    // 解析 Alt-Svc 头
    // 格式: h3=":443"; ma=2592000
    public void processAltSvc(HttpResponse response) {
        String altSvc = response.headers().firstValue("Alt-Svc").orElse(null);
        if (altSvc != null) {
            // 解析并缓存 HTTP/3 端点
            parseAndCache(altSvc, response.uri());
        }
    }
    
    // 检查是否有 HTTP/3 端点
    public Optional<URI> getHttp3Endpoint(URI uri) {
        // 返回缓存的 HTTP/3 端点
    }
}
```

---

## 3. 连接建立流程

### 3.1 QUIC 握手

```
客户端                                    服务端
   │                                         │
   │  ──────── Initial (CRYPTO) ──────────►  │
   │         包含 ClientHello                │
   │                                         │
   │  ◄─────── Initial (CRYPTO) ──────────   │
   │         包含 ServerHello                │
   │                                         │
   │  ◄─────── Handshake (CRYPTO) ────────   │
   │         包含 EncryptedExtensions        │
   │         包含 Certificate                │
   │         包含 CertificateVerify          │
   │         包含 Finished                   │
   │                                         │
   │  ──────── Handshake (CRYPTO) ────────►  │
   │         包含 Finished                   │
   │                                         │
   │  ════════ 1-RTT (应用数据) ═════════►   │
   │         可以发送 HTTP/3 请求            │
   │                                         │
```

### 3.2 代码实现

```java
// 简化的连接建立流程
public class QuicConnection {
    
    public CompletableFuture<Void> connect() {
        // 1. 创建 UDP socket
        DatagramSocket socket = new DatagramSocket();
        
        // 2. 生成初始密钥
        QuicKeys initialKeys = QuicKeys.generateInitial(destinationId);
        
        // 3. 发送 Initial 包
        byte[] clientHello = tlsEngine.getClientHello();
        byte[] initialPacket = createInitialPacket(clientHello, initialKeys);
        socket.send(initialPacket);
        
        // 4. 接收服务端响应
        byte[] response = socket.receive();
        
        // 5. 处理握手
        tlsEngine.handshake(response, EncryptionLevel.INITIAL);
        
        // 6. 完成 1-RTT 握手
        return tlsEngine.getHandshakeFuture();
    }
}
```

---

## 4. HTTP/3 帧处理

### 4.1 帧类型

```java
enum Http3FrameType {
    DATA(0x00),           // 数据帧
    HEADERS(0x01),        // 头部帧
    CANCEL_PUSH(0x03),    // 取消推送
    SETTINGS(0x04),       // 设置帧
    PUSH_PROMISE(0x05),   // 推送承诺
    GOAWAY(0x07),         // 关闭连接
    MAX_PUSH_ID(0x0D);    // 最大推送 ID
    
    private final int type;
}
```

### 4.2 帧顺序验证

**文件**: `src/java.net.http/share/classes/jdk/internal/net/http/H3FrameOrderVerifier.java`

```java
class H3FrameOrderVerifier {
    
    // 验证帧顺序
    // HTTP/3 要求帧按特定顺序发送
    public void verify(int streamId, Http3FrameType type) {
        StreamState state = streamStates.get(streamId);
        
        switch (state) {
            case IDLE:
                // 第一个帧必须是 HEADERS
                if (type != HEADERS) {
                    throw new ProtocolException("Expected HEADERS");
                }
                break;
            case HEADERS_RECEIVED:
                // 可以接收 DATA 或 trailers HEADERS
                if (type != DATA && type != HEADERS) {
                    throw new ProtocolException("Unexpected frame");
                }
                break;
            // ...
        }
    }
}
```

---

## 5. QPACK 头部压缩

### 5.1 概述

QPACK 是 HTTP/3 的头部压缩算法，类似 HTTP/2 的 HPACK，但针对 QUIC 优化。

```
HPACK (HTTP/2):
- 单一字节流
- 队头阻塞问题

QPACK (HTTP/3):
- 双向流
- 无队头阻塞
- 需要确认机制
```

### 5.2 实现

```java
class QPackEncoder {
    
    private final QPackDynamicTable dynamicTable;
    
    // 编码头部
    public byte[] encode(HttpHeaders headers) {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        
        for (Map.Entry<String, String> header : headers.map()) {
            // 1. 检查静态表
            int staticIndex = staticTable.indexOf(header);
            if (staticIndex >= 0) {
                // 使用静态表索引
                out.write(0x80 | staticIndex);
                continue;
            }
            
            // 2. 检查动态表
            int dynamicIndex = dynamicTable.indexOf(header);
            if (dynamicIndex >= 0) {
                // 使用动态表索引
                out.write(0x80 | (dynamicIndex + staticTable.size()));
                continue;
            }
            
            // 3. 字面量编码
            encodeLiteral(out, header);
            
            // 4. 添加到动态表
            dynamicTable.add(header);
        }
        
        return out.toByteArray();
    }
}
```

---

## 6. 流量控制

### 6.1 QUIC 流量控制

```java
class QuicFlowController {
    
    private long maxData;           // 最大接收数据
    private long receivedData;      // 已接收数据
    private long maxStreamData;     // 单流最大数据
    
    // 检查是否需要发送 MAX_DATA 帧
    public boolean shouldSendMaxData() {
        return receivedData >= maxData * 0.75;
    }
    
    // 更新窗口
    public void updateWindow(long increment) {
        maxData += increment;
        sendMaxDataFrame(increment);
    }
}
```

### 6.2 HTTP/3 流限制

```java
class StreamLimitException extends Exception {
    // 当达到最大并发流数时抛出
}

class Http3Connection {
    
    private final int maxConcurrentStreams = 100;
    private int activeStreams = 0;
    
    public synchronized int acquireStream() throws StreamLimitException {
        if (activeStreams >= maxConcurrentStreams) {
            throw new StreamLimitException("Max concurrent streams reached");
        }
        return ++activeStreams;
    }
}
```

---

## 7. 错误处理

### 7.1 QUIC 传输错误

**文件**: `src/java.base/share/classes/jdk/internal/net/quic/QuicTransportErrors.java`

```java
public class QuicTransportErrors {
    
    // QUIC 错误码
    public static final int NO_ERROR = 0x00;
    public static final int INTERNAL_ERROR = 0x01;
    public static final int CONNECTION_REFUSED = 0x02;
    public static final int FLOW_CONTROL_ERROR = 0x03;
    public static final int STREAM_LIMIT_ERROR = 0x04;
    public static final int STREAM_STATE_ERROR = 0x05;
    public static final int FINAL_SIZE_ERROR = 0x06;
    public static final int FRAME_ENCODING_ERROR = 0x07;
    public static final int TRANSPORT_PARAMETER_ERROR = 0x08;
    // ...
}
```

### 7.2 HTTP/3 错误

```java
public class Http3Errors {
    
    // HTTP/3 错误码 (per RFC 9114)
    public static final int H3_NO_ERROR = 0x0100;
    public static final int H3_GENERAL_PROTOCOL_ERROR = 0x0101;
    public static final int H3_INTERNAL_ERROR = 0x0102;
    public static final int H3_STREAM_CREATION_ERROR = 0x0103;
    public static final int H3_CLOSED_CRITICAL_STREAM = 0x0104;
    public static final int H3_FRAME_UNEXPECTED = 0x0105;
    public static final int H3_FRAME_ERROR = 0x0106;
    public static final int H3_EXCESSIVE_LOAD = 0x0107;
    public static final int H3_ID_ERROR = 0x0108;
    public static final int H3_SETTINGS_ERROR = 0x0109;
    public static final int H3_MISSING_SETTINGS = 0x010A;
    public static final int H3_REQUEST_REJECTED = 0x010B;
    public static final int H3_REQUEST_CANCELLED = 0x010C;
    public static final int H3_REQUEST_INCOMPLETE = 0x010D;
    public static final int H3_MESSAGE_ERROR = 0x010E;
    public static final int H3_CONNECT_ERROR = 0x010F;
    public static final int H3_VERSION_FALLBACK = 0x0110;
}
```

---

## 8. 安全配置

### 8.1 java.security 配置

**文件**: `src/java.base/share/conf/security/java.security`

```properties
# HTTP/3 相关配置
jdk.httpclient.http3.enabled=true
jdk.httpclient.http3.maxStreams=100
# Note: maxFrameSize is an HTTP/2 concept (SETTINGS_MAX_FRAME_SIZE), not applicable to HTTP/3
jdk.httpclient.http3.headerTableSize=65536
```

### 8.2 TLS 配置

```java
// QUIC 要求 TLS 1.3
public class QuicTLSContext {
    
    static {
        // 强制使用 TLS 1.3
        Security.setProperty("jdk.tls.client.protocols", "TLSv1.3");
    }
    
    // 支持的加密套件
    private static final String[] CIPHER_SUITES = {
        "TLS_AES_128_GCM_SHA256",
        "TLS_AES_256_GCM_SHA384",
        "TLS_CHACHA20_POLY1305_SHA256"
    };
}
```

---

## 9. 性能优化

### 9.1 连接复用

```java
class Http3ConnectionPool {
    
    private final Map<URI, Http3Connection> connections = new ConcurrentHashMap<>();
    
    public CompletableFuture<Http3Connection> getConnection(URI uri) {
        return connections.computeIfAbsent(uri, this::createConnection);
    }
    
    // 连接复用，避免重复握手
}
```

### 9.2 0-RTT 数据

```java
class QuicZeroRtt {
    
    // 发送 0-RTT 数据（恢复连接时）
    public void sendZeroRttData(byte[] data) {
        if (hasPreviousSession()) {
            // 使用之前的密钥加密
            byte[] encrypted = encryptWithPreviousKeys(data);
            send(encrypted);
        }
    }
}
```

---

## 10. 相关源码文件

```
src/java.base/share/classes/
├── jdk/internal/net/quic/
│   ├── QuicTLSEngine.java              # TLS 引擎
│   ├── QuicOneRttContext.java          # 1-RTT 上下文
│   ├── QuicVersion.java                # QUIC 版本
│   ├── QuicTransportErrors.java        # 传输错误
│   └── QuicTransportException.java     # 传输异常
└── sun/security/ssl/
    ├── QuicCipher.java                 # 加密
    ├── QuicKeyManager.java             # 密钥管理
    └── QuicTLSEngineImpl.java          # TLS 实现

src/java.net.http/share/classes/
├── java/net/http/
│   ├── HttpClient.java                 # 客户端 API
│   ├── HttpOption.java                 # HTTP 选项
│   └── UnsupportedProtocolVersionException.java
└── jdk/internal/net/http/
    ├── Http3ClientImpl.java            # HTTP/3 客户端
    ├── Http3Connection.java            # HTTP/3 连接
    ├── Http3Exchange.java              # HTTP/3 交换
    ├── H3FrameOrderVerifier.java       # 帧顺序验证
    └── AltSvcProcessor.java            # Alt-Svc 处理
```

---

## 11. 总结

JEP 517 的实现涉及：
1. **QUIC 协议栈**: 全新的传输层实现
2. **TLS 1.3 集成**: 内置于 QUIC 的加密
3. **HTTP/3 帧处理**: HEADERS, DATA, SETTINGS 等
4. **QPACK 压缩**: 头部压缩优化
5. **流量控制**: QUIC 和 HTTP/3 双层控制
6. **错误处理**: 完整的错误码体系

关键设计决策：
- 使用 UDP 替代 TCP
- TLS 1.3 内置，无额外握手
- 支持自动降级到 HTTP/2 或 HTTP/1.1