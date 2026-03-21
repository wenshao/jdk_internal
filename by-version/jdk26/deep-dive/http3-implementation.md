# JDK 26 HTTP/3 实现深度分析

> **JEP**: 517 | **状态**: 正式发布 | **Commit**: e8db14f584f
> **代码量**: +104,307 / -2,639 行
> **作者**: Daniel Fuchs 等 (11位贡献者)

---

## 目录

1. [架构概览](#架构概览)
2. [QUIC 协议实现](#quic-协议实现)
3. [HTTP/3 层实现](#http-3-层实现)
4. [TLS 1.3 集成](#tls-13-集成)
5. [拥塞控制](#拥塞控制)
6. [源码文件结构](#源码文件结构)
7. [关键类分析](#关键类分析)
8. [性能优化](#性能优化)
9. [与 RFC 对应关系](#与-rfc-对应关系)

---

## 1. 架构概览

### 分层架构

```
┌─────────────────────────────────────────────────────────┐
│                   java.net.http API                     │
│              (HttpClient, HttpRequest, HttpResponse)     │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                   Http3ClientImpl                        │
│  - HTTP/3 连接池管理                                      │
│  - 版本协商 (HTTP/3_AUTO)                                 │
│  - Alt-Svc 处理                                          │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                   HTTP/3 Layer                           │
│  - HTTP/3 帧处理 (DATA, HEADERS, SETTINGS, etc.)          │
│  - QPACK 头压缩                                          │
│  - 流管理 (Http3Stream)                                  │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                   QUIC Layer                             │
│  - QUIC 连接 (QuicConnectionImpl)                        │
│  - QUIC 流 (QuicStream)                                  │
│  - 可靠性保证 (ACK, 丢包重传)                              │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                   TLS 1.3 Layer                          │
│  - QuicTLSEngineImpl                                     │
│  - 加密级别 (Initial, Handshake, 1-RTT)                   │
│  - 传输参数协商                                          │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                   UDP Socket                             │
└─────────────────────────────────────────────────────────┘
```

### 模块关系图

```
java.net.http                          java.base
     │                                       │
     ├─ Http3ClientImpl                     ├─ jdk.internal.net.quic
     │   ├─ Http3Connection                │   ├─ QuicTLSEngine (接口)
     │   ├─ Http3Exchange                  │   ├─ QuicOneRttContext
     │   └─ Http3ConnectionPool            │   └─ QuicTransportException
     │                                       │
     ├─ http3/                              ├─ sun.security.ssl
     │   ├─ frames/                         │   ├─ QuicTLSEngineImpl
     │   │   └─ Http3FrameType              │   ├─ QuicCipher
     │   └─ streams/                        │   └─ QuicKeyManager
     │                                       │
     └─ quic/                               └─ jdk.internal.net.http.quic
         ├─ QuicClient                      (HTTP Client 内部实现)
         ├─ QuicConnectionImpl              ├─ QuicConnectionImpl
         ├─ QuicStream                      ├─ Http3ClientImpl
         └─ frames/                         ├─ QuicCubicCongestionController
             ├─ QuicFrame                   └─ QuicRenoCongestionController
             └─ ...
```

---

## 2. QUIC 协议实现

### QUIC 版本支持

```java
// Http3ClientImpl.java
private static final List<QuicVersion> availableQuicVersions;
static {
    // 默认支持 QUIC v1 和 v2，v1 优先
    final List<QuicVersion> defaultPref =
        List.of(QuicVersion.QUIC_V1, QuicVersion.QUIC_V2);

    // 可通过系统属性自定义
    final String sysPropVal =
        Utils.getProperty("jdk.httpclient.quic.available.versions");
    // ...
}
```

### QUIC 连接状态机

```java
// QuicConnectionImpl.java - 核心连接类
public class QuicConnectionImpl extends QuicConnection implements QuicPacketReceiver {

    // 连接配置参数
    public static final int SMALLEST_MAXIMUM_DATAGRAM_SIZE = 1200;
    public static final int DEFAULT_MAX_INITIAL_TIMEOUT = 30; // 秒
    public static final long DEFAULT_INITIAL_MAX_DATA = 15 << 20; // 15 MB
    public static final long DEFAULT_INITIAL_STREAM_MAX_DATA = 6 << 20; // 6 MB
    public static final int DEFAULT_MAX_BIDI_STREAMS = 100;

    // 连接核心组件
    private final QuicEndpoint endpoint;           // UDP 端点
    private final QuicTLSEngine tlsEngine;          // TLS 引擎
    private final QuicCongestionController cc;      // 拥塞控制
    private final QuicRttEstimator rttEstimator;    // RTT 估算
    private final QuicConnectionStreams streams;    // 流管理器
    private final QuicPacketEncoder encoder;        // 数据包编码器
    private final QuicPacketDecoder decoder;        // 数据包解码器
}
```

### QUIC 数据包类型

```java
// QuicPacket.java - 数据包接口
public interface QuicPacket {

    enum PacketType {
        INITIAL,      // 初始化数据包 (携带 TLS ClientHello)
        HANDSHAKE,    // 握手数据包
        ZERORTT,      // 0-RTT 数据包 (早期数据)
        ONERTT,       // 1-RTT 数据包 (应用数据)
        RETRY,        // 重试数据包 (服务器拒绝)
        VERSIONS,     // 版本协商数据包
        NONE          // 无包号数据包 (如 Stateless Reset)
    }

    enum PacketNumberSpace {
        INITIAL,      // Initial 数据包的包号空间
        HANDSHAKE,    // Handshake 数据包的包号空间
        APPLICATION,  // 1-RTT/0-RTT 数据包的包号空间
        NONE          // 无包号空间
    }
}
```

### QUIC 帧类型

```java
// QUIC 支持的帧类型 (frames/QuicFrame.java 子类)
├── PADDING           // 填充帧
├── PING              // 保活帧
├── ACK               // 确认帧
├── RESET_STREAM      // 重置流帧
├── STOP_SENDING      // 停止发送帧
├── CRYPTO            // 加密握手数据帧
├── NEW_TOKEN         // 新令牌帧
├── MAX_DATA          // 最大数据量帧
├── MAX_STREAM_DATA   // 最大流数据帧
├── MAX_STREAMS       // 最大流数帧
├── DATA_BLOCKED      // 数据阻塞帧
├── STREAM_DATA_BLOCKED // 流数据阻塞帧
├── STREAMS_BLOCKED   // 流阻塞帧
├── NEW_CONNECTION_ID // 新连接 ID 帧
├── RETIRE_CONNECTION_ID // 废弃连接 ID 帧
├── PATH_CHALLENGE    // 路径挑战帧
├── PATH_RESPONSE     // 路径响应帧
├── CONNECTION_CLOSE  // 连接关闭帧
└── HANDSHAKE_DONE    // 握手完成帧
```

---

## 3. HTTP/3 层实现

### HTTP/3 帧类型

```java
// Http3FrameType.java - HTTP/3 帧类型枚举
public enum Http3FrameType {
    DATA(0x00),           // 数据帧
    HEADERS(0x01),        // 头部帧
    CANCEL_PUSH(0x03),    // 取消推送帧
    SETTINGS(0x04),       // 设置帧
    PUSH_PROMISE(0x05),   // 推送承诺帧
    GOAWAY(0x07),         // 关闭帧
    MAX_PUSH_ID(0x0d);    // 最大推送 ID 帧

    // 非法帧类型 (HTTP/2 遗留，无 HTTP/3 对应)
    // 0x02, 0x06, 0x08, 0x09
}
```

### HTTP/3 连接管理

```java
// Http3ClientImpl.java - HTTP/3 客户端核心类
final class Http3ClientImpl implements AutoCloseable {

    // 连接池
    private final Http3ConnectionPool connections;

    // 待恢复连接管理器
    private final Http3PendingConnections reconnections;

    // QUIC 客户端
    private final QuicClient quicClient;

    // 连接恢复机制
    sealed interface ConnectionRecovery permits PendingConnection, StreamLimitReached {}

    // 流限制处理
    public void streamLimitReached(Http3Connection connection, HttpRequestImpl request) {
        lock.lock();
        try {
            reconnections.streamLimitReached(connectionKey(request), connection);
        } finally {
            lock.unlock();
        }
    }
}
```

### HTTP/3 流处理

```java
// Http3Stream.java - HTTP/3 流实现
abstract class Http3Stream {

    // 流状态
    enum StreamState {
        IDLE,           // 空闲
        RESERVED,       // 已保留
        OPEN,           // 打开
        HALF_CLOSED,    // 半关闭
        CLOSED          // 关闭
    }

    // QPACK 解码器
    private final QPackDecoder qpackDecoder;

    // HTTP/3 帧处理器
    protected void handleFrame(Http3Frame frame) {
        switch (frame.type()) {
            case Http3FrameType.TYPE.DATA_FRAME -> handleDataFrame((DataFrame) frame);
            case Http3FrameType.TYPE.HEADERS_FRAME -> handleHeadersFrame((HeadersFrame) frame);
            case Http3FrameType.TYPE.SETTINGS_FRAME -> handleSettingsFrame((SettingsFrame) frame);
            // ...
        }
    }
}
```

---

## 4. TLS 1.3 集成

### 加密级别

```java
// QuicTLSEngine.java - TLS 引擎接口
public interface QuicTLSEngine {

    enum HandshakeState {
        NEED_SEND_CRYPTO,     // 需要发送加密数据
        NEED_RECV_CRYPTO,     // 需要接收加密数据
        HANDSHAKE_COMPLETE,   // 握手完成
        HANDSHAKE_FAILED      // 握手失败
    }

    enum KeySpace {
        INITIAL,      // Initial 加密 (从 ClientHello 派生)
        HANDSHAKE,    // Handshake 加密 (从 ServerHello 派生)
        ONE_RTT,      // 1-RTT 加密 (握手完成后派生)
        ZERO_RTT,     // 0-RTT 加密 (从会话票证派生)
        RETRY         // Retry 加密
    }
}
```

### QUIC TLS 实现

```java
// QuicTLSEngineImpl.java - TLS 引擎实现
public final class QuicTLSEngineImpl implements QuicTLSEngine, SSLTransport {

    // 消息类型到加密级别的映射
    private static final Map<Byte, KeySpace> messageTypeMap =
        Map.of(
            SSLHandshake.CLIENT_HELLO.id, INITIAL,
            SSLHandshake.SERVER_HELLO.id, INITIAL,
            SSLHandshake.ENCRYPTED_EXTENSIONS.id, HANDSHAKE,
            SSLHandshake.FINISHED.id, HANDSHAKE,
            SSLHandshake.NEW_SESSION_TICKET.id, ONE_RTT
        );

    // 密钥管理器
    private final InitialKeyManager initialKeyManager;      // Initial 密钥
    private final HandshakeKeyManager handshakeKeyManager;  // Handshake 密钥
    private final OneRttKeyManager oneRttKeyManager;        // 1-RTT 密钥

    // 仅支持 TLS 1.3
    public QuicTLSEngineImpl(SSLContextImpl sslContextImpl, String peerHost, int peerPort) {
        conContext.sslConfig.enabledProtocols = List.of(ProtocolVersion.TLS13);
        // ...
    }
}
```

### QUIC 传输参数

```java
// QuicTransportParameters.java - 传输参数
public class QuicTransportParameters {

    // 传输参数 ID
    enum ParameterId {
        active_connection_id_limit(0x0e),
        initial_max_data(0x00),
        initial_max_stream_data_bidi_local(0x04),
        initial_max_stream_data_bidi_remote(0x05),
        initial_max_stream_data_uni(0x06),
        initial_max_streams_bidi(0x02),
        initial_max_streams_uni(0x03),
        max_idle_timeout(0x01),
        max_udp_payload_size(0x03),
        version_information(0x0b)
    }

    // HTTP/3 特定配置
    // HTTP/3 不允许服务器发起双向流
    transportParameters.setIntParameter(initial_max_streams_bidi, 0);
    transportParameters.setIntParameter(initial_max_stream_data_bidi_remote, 0);
}
```

---

## 5. 拥塞控制

### CUBIC 拥塞控制器

```java
// QuicCubicCongestionController.java - CUBIC 实现 (RFC 9438)
public final class QuicCubicCongestionController extends QuicBaseCongestionController {

    // CUBIC 参数
    public static final double BETA = 0.7;       // 乘性减小的因子
    public static final double ALPHA = 3 * (1 - BETA) / (1 + BETA);  // 加性增长因子
    private static final double C = 0.4;         // CUBIC 常数

    // CUBIC 状态变量
    private long wMaxBytes;          // 拥塞窗口最大值
    private long cwndPriorBytes;     // 拥塞事件前的窗口
    private long timeNanos;          // 时间 t
    private long kNanos;             // 时间 K (wMax 减少到当前窗口的时间)
    private long wEstBytes;          // Reno 友好窗口估计

    // CUBIC 窗口计算公式
    // Wcubic(t) = C * (t-K)^3 + Wmax
    private double wCubicBytes(long timeNanos) {
        return (C * maxDatagramSize * Math.pow((timeNanos - kNanos) / 1e9, 3)) + wMaxBytes;
    }

    // 拥塞避免时确认包处理
    boolean congestionAvoidanceAcked(int packetBytes, Deadline sentTime) {
        // 更新 Reno 友好窗口
        if (wEstBytes < cwndPriorBytes) {
            wEstBytes += Math.max((long) (ALPHA * maxDatagramSize * packetBytes / congestionWindow), 1);
        } else {
            wEstBytes += Math.max((long)maxDatagramSize * packetBytes / congestionWindow, 1);
        }

        // 计算 CUBIC 目标窗口
        long rttNanos = TimeUnit.MICROSECONDS.toNanos(rttEstimator.state().smoothedRttMicros());
        double dblTargetBytes = wCubicBytes(timeNanos + rttNanos);
        long targetBytes = (long) Math.min(dblTargetBytes, 1.5 * congestionWindow);

        // 增加拥塞窗口
        if (targetBytes > congestionWindow) {
            congestionWindow += Math.max((targetBytes - congestionWindow) * packetBytes / congestionWindow, 1L);
        }

        // 确保 Reno 友好性
        if (wEstBytes > congestionWindow) {
            congestionWindow = wEstBytes;
        }
    }
}
```

### Reno 拥塞控制器

```java
// QuicRenoCongestionController.java - Reno 实现
public final class QuicRenoCongestionController extends QuicBaseCongestionController {

    // Reno 参数
    private static final int NUM_SEGMENTS = 10;

    // 拥塞避免阶段
    boolean congestionAvoidanceAcked(int packetBytes, Deadline sentTime) {
        // 每个窗口增加一个数据段大小
        long add = maxDatagramSize * packetBytes / congestionWindow;
        if (add == 0) {
            // 确保至少增加一点
            add = (packetBytes * NUM_SEGMENTS) / congestionWindow;
        }
        congestionWindow += Math.max(add, 1L);
    }
}
```

### RTT 估算

```java
// QuicRttEstimator.java - RTT 估算器
public class QuicRttEstimator {

    // RTT 状态
    public static final record State(
        long latestRttMicros,      // 最新 RTT
        long smoothedRttMicros,    // 平滑 RTT (SRTT)
        long rttVarMicros,         // RTT 变化量
        long minRttMicros          // 最小 RTT
    ) {}

    // RTT 更新算法 (RFC 9002)
    public void update(long ackDelayMicros, long rttSampleMicros) {
        // 调整后的 RTT 样本
        long adjustedRttSample = rttSampleMicros;
        if (rttSampleMicros >= ackDelayMicros) {
            adjustedRttSample = rttSampleMicros - ackDelayMicros;
        }

        // 更新最小 RTT
        if (minRttMicros == 0 || rttSampleMicros < minRttMicros) {
            minRttMicros = rttSampleMicros;
        }

        // 初始化或更新平滑 RTT
        if (smoothedRttMicros == 0) {
            smoothedRttMicros = adjustedRttSample;
            rttVarMicros = adjustedRttSample / 2;
        } else {
            rttVarMicros = (3 * rttVarMicros + Math.abs(smoothedRttMicros - adjustedRttSample)) / 4;
            smoothedRttMicros = (7 * smoothedRttMicros + adjustedRttSample) / 8;
        }
    }
}
```

---

## 6. 源码文件结构

### 完整文件列表

```
src/java.base/share/classes/jdk/internal/net/quic/
├── QuicKeyUnavailableException.java       # 密钥不可用异常
├── QuicOneRttContext.java                 # 1-RTT 加密上下文
├── QuicTLSEngine.java                     # TLS 引擎接口
├── QuicTLSContext.java                    # TLS 上下文
├── QuicTransportErrors.java               # 传输错误码
├── QuicTransportException.java            # 传输异常
├── QuicTransportParametersConsumer.java   # 传输参数消费者接口

src/java.base/share/classes/sun/security/ssl/
├── QuicCipher.java                        # QUIC 加密套件
├── QuicEngineOutputRecord.java            # QUIC 输出记录
├── QuicKeyManager.java                    # QUIC 密钥管理器
├── QuicTLSEngineImpl.java                 # TLS 引擎实现
└── QuicTransportParametersExtension.java  # TLS 传输参数扩展

src/java.net.http/share/classes/jdk/internal/net/http/
├── Http3ClientImpl.java                   # HTTP/3 客户端实现
├── Http3ClientProperties.java             # HTTP/3 客户端属性
├── Http3Connection.java                   # HTTP/3 连接接口
├── Http3ConnectionPool.java               # HTTP/3 连接池
├── Http3ExchangeImpl.java                 # HTTP/3 交换实现
├── Http3PendingConnections.java           # HTTP/3 待处理连接
├── Http3PushManager.java                  # HTTP/3 推送管理器
├── Http3PushPromiseStream.java            # HTTP/3 推送流
├── Http3Stream.java                       # HTTP/3 流抽象
└── HttpQuicConnection.java                # HTTP/QUIC 连接适配器

src/java.net.http/share/classes/jdk/internal/net/http/http3/
├── frames/
│   ├── AbstractHttp3Frame.java            # HTTP/3 帧基类
│   ├── Http3Error.java                    # HTTP/3 错误
│   └── Http3FrameType.java                # HTTP/3 帧类型枚举
└── streams/
    ├── Http3Streams.java                  # HTTP/3 流工具
    └── QuicStreamIntReader.java           # QUIC 流整数读取器

src/java.net.http/share/classes/jdk/internal/net/http/quic/
├── QuicClient.java                        # QUIC 客户端
├── QuicConnection.java                    # QUIC 连接接口
├── QuicConnectionId.java                  # QUIC 连接 ID
├── QuicConnectionIdFactory.java           # 连接 ID 工厂
├── QuicConnectionImpl.java                # QUIC 连接实现
├── QuicCongestionController.java          # 拥塞控制接口
├── QuicCubicCongestionController.java     # CUBIC 拥塞控制
├── QuicRenoCongestionController.java      # Reno 拥塞控制
├── QuicEndpoint.java                      # QUIC UDP 端点
├── QuicInstance.java                      # QUIC 实例
├── QuicPacer.java                         # QUIC 发送节奏控制
├── QuicPacketReceiver.java                # 数据包接收器接口
├── QuicRttEstimator.java                  # RTT 估算器
├── QuicSelector.java                      # QUIC 选择器
├── QuicStream.java                        # QUIC 流接口
├── QuicStreamLimitException.java          # 流限制异常
├── QuicTimerQueue.java                    # 定时器队列
├── QuicTransportParameters.java           # 传输参数
├── frames/
│   ├── AckFrame.java                      # ACK 帧
│   ├── ConnectionCloseFrame.java          # 连接关闭帧
│   ├── CryptoFrame.java                   # CRYPTO 帧
│   ├── MaxDataFrame.java                  # MAX DATA 帧
│   ├── MaxStreamDataFrame.java            # MAX STREAM DATA 帧
│   ├── MaxStreamsFrame.java               # MAX STREAMS 帧
│   ├── NewConnectionIDFrame.java          # 新连接 ID 帧
│   ├── PaddingFrame.java                  # 填充帧
│   ├── PingFrame.java                     # PING 帧
│   ├── QuicFrame.java                     # QUIC 帧基类
│   ├── ResetStreamFrame.java              # RESET STREAM 帧
│   └── ...
├── packets/
│   ├── HandshakePacket.java               # 握手数据包
│   ├── InitialPacket.java                 # 初始数据包
│   ├── LongHeader.java                    # 长头数据包基类
│   ├── OneRttPacket.java                  # 1-RTT 数据包
│   ├── PacketSpace.java                   # 数据包空间
│   ├── QuicPacket.java                    # 数据包接口
│   ├── QuicPacketDecoder.java             # 数据包解码器
│   ├── QuicPacketEncoder.java             # 数据包编码器
│   ├── QuicPacketNumbers.java             # 数据包编号工具
│   ├── RetryPacket.java                   # 重试数据包
│   └── VersionNegotiationPacket.java      # 版本协商数据包
└── streams/
    ├── AbstractQuicStream.java            # QUIC 流基类
    ├── QuicBidiStream.java                # 双向流接口
    ├── QuicBidiStreamImpl.java            # 双向流实现
    ├── QuicConnectionStreams.java         # 连接流管理器
    ├── QuicReceiverStream.java            # 接收流接口
    ├── QuicReceiverStreamImpl.java        # 接收流实现
    ├── QuicSenderStream.java              # 发送流接口
    ├── QuicSenderStreamImpl.java          # 发送流实现
    ├── QuicStream.java                    # 流接口
    ├── QuicStreamReader.java              # 流读取器
    ├── QuicStreamWriter.java              # 流写入器
    └── QuicStreams.java                   # 流工具类
```

---

## 7. 关键类分析

### QuicConnectionImpl - QUIC 连接核心

**职责**：
- 管理 QUIC 连接的完整生命周期
- 处理数据包的发送和接收
- 协调 TLS 握手
- 管理流创建和销毁
- 实现拥塞控制和丢包恢复

**关键方法**：
```java
public class QuicConnectionImpl extends QuicConnection {

    // 连接建立
    public CompletableFuture<QuicConnection> connect(SocketAddress peer) { ... }

    // 数据包处理
    @Override
    public void receive(QuicDatagram datagram) { ... }

    // 流创建
    public QuicBidiStream createBidiStream(long streamId) { ... }

    // 连接关闭
    public void close(int errorCode, ByteBuffer reason) { ... }
}
```

**状态管理**：
- `INITIAL` → `HANDSHAKE` → `1-RTT` 加密级别转换
- 连接 ID 轮换机制
- 路径验证和迁移

### Http3ClientImpl - HTTP/3 客户端

**职责**：
- 管理 HTTP/3 连接池
- 处理 Alt-Svc 发现
- 版本协商 (HTTP/3_AUTO)
- 连接恢复和重建

**连接池策略**：
```java
final class Http3ClientImpl {
    private final Http3ConnectionPool connections;

    // 获取或创建连接
    Http3Connection getConnection(Exchange<?> exchange) {
        // 1. 检查现有连接池
        // 2. 检查 Alt-Svc 缓存
        // 3. 创建新 QUIC 连接
        // 4. 执行 HTTP/3 握手
    }

    // 流限制处理
    public void streamLimitReached(Http3Connection conn, HttpRequestImpl req) {
        // 启动新连接，等待队列中的请求
    }
}
```

### QuicTLSEngineImpl - TLS 1.3 集成

**职责**：
- 实现 QUIC 特定的 TLS 1.3
- 管理多个加密级别
- 处理传输参数扩展
- 派生数据包保护密钥

**密钥派生**：
```java
// 基于 TLS 1.3 导出密钥
Initial Keys = HKDF-Extract(salt, ClientHello)
Handshake Keys = TLS-13 Handshake
1-RTT Keys = TLS-13 Application Data
0-RTT Keys = (from resumption)
```

---

## 8. 性能优化

### 1. 零拷贝设计

```java
// 使用 ByteBuffer 直接操作，减少数据拷贝
public void receive(ByteBuffer data) {
    // 直接解析 ByteBuffer，无需额外拷贝
    QuicPacket packet = decoder.decode(data);
}
```

### 2. 异步 I/O

```java
// 使用 NIO Selector 实现非阻塞 I/O
public class QuicSelector {
    private final Selector selector;

    public void register(DatagramChannel channel) {
        channel.register(selector, SelectionKey.OP_READ, this);
    }
}
```

### 3. 流水线处理

```java
// 数据包处理流水线
receive() → decode() → validate() → process() → respond()
```

### 4. 内存池化

```java
// 重用数据包缓冲区
private final ThreadLocal<ByteBuffer> packetBuffer =
    ThreadLocal.withInitial(() -> ByteBuffer.allocateDirect(MAX_PACKET_SIZE));
```

---

## 9. 与 RFC 对应关系

### RFC 9000 - QUIC 核心协议

| RFC 章节 | Java 类/方法 | 说明 |
|----------|-------------|------|
| 2. 连接 | QuicConnectionImpl | 连接生命周期管理 |
| 3. 流 | QuicStream | 流创建和管理 |
| 4. 数据包 | QuicPacket | 数据包类型定义 |
| 5. 帧 | frames.QuicFrame* | 各类帧实现 |
| 6. 版本协商 | QuicVersion | 版本号处理 |
| 7. 流量控制 | QuicCongestionController | 流量控制 |
| 8. 拥塞控制 | QuicCubicCongestionController | CUBIC 算法 |
| 9. 丢失检测 | QuicRttEstimator | RTT 估算和丢包检测 |

### RFC 9001 - QUIC TLS 集成

| RFC 章节 | Java 类/方法 | 说明 |
|----------|-------------|------|
| 4. 加密级别 | QuicTLSEngine.KeySpace | Initial/Handshake/1-RTT |
| 5. 传输参数 | QuicTransportParameters | 参数编码/解码 |
| 6. 密钥更新 | QuicKeyManager | 密钥派生和更新 |

### RFC 9114 - HTTP/3

| RFC 章节 | Java 类/方法 | 说明 |
|----------|-------------|------|
| 4. 连接建立 | Http3ClientImpl | HTTP/3 握手 |
| 5. 传输层 | QUIC 层 | 使用 QUIC 流 |
| 6. 帧类型 | http3.frames.Http3Frame* | HTTP/3 帧实现 |
| 7. QPACK | QPackEncoder/Decoder | 头压缩 |

---

## 10. 总结

JDK 26 的 HTTP/3 实现是一个完整的、生产就绪的 HTTP/3 和 QUIC 协议栈：

1. **完整的 QUIC 协议实现**：支持 RFC 9000/9001/9002
2. **完整的 HTTP/3 实现**：支持 RFC 9114
3. **TLS 1.3 深度集成**：多级别加密，0-RTT 支持
4. **两种拥塞控制算法**：CUBIC 和 Reno
5. **高性能设计**：零拷贝、异步 I/O、连接池
6. **良好的扩展性**：清晰的接口定义，易于扩展

---

## 11. 相关链接

- [JEP 517 官方文档](https://openjdk.org/jeps/517)
- [RFC 9000: QUIC](https://www.rfc-editor.org/rfc/rfc9000)
- [RFC 9001: QUIC TLS](https://www.rfc-editor.org/rfc/rfc9001)
- [RFC 9114: HTTP/3](https://www.rfc-editor.org/rfc/rfc9114)
- [Commit: e8db14f584f](https://github.com/openjdk/jdk/commit/e8db14f584f)
