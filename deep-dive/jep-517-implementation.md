# JEP 517 深入分析: HTTP/3 for the HTTP Client API

> 本文档基于 JDK 源码深入分析 JEP 517 的实现，覆盖 QUIC 传输层、HTTP/3 帧处理、QPACK 头部压缩、
> Alt-Svc 发现机制及回退策略。所有类名和包结构均来自实际源码验证。

---

## 1. 架构概览 (Architecture Overview)

### 1.1 协议栈对比 (Protocol Stack Comparison)

```
HTTP/1.1:                HTTP/2:                  HTTP/3:
┌────────────┐          ┌────────────┐           ┌────────────┐
│  HTTP/1.1  │          │  HTTP/2    │           │  HTTP/3    │
├────────────┤          ├────────────┤           ├────────────┤
│    TCP     │          │    TCP     │ ← HOL     │   QUIC     │ ← 无 HOL
├────────────┤          ├────────────┤           ├────────────┤
│            │          │  TLS 1.2+  │           │  TLS 1.3   │ ← 内置
├────────────┤          ├────────────┤           ├────────────┤
│    IP      │          │    IP      │           │   UDP      │
└────────────┘          └────────────┘           ├────────────┤
                                                 │    IP      │
                                                 └────────────┘
```

HTTP/2 基于 TCP 的多路复用存在队头阻塞 (Head-of-Line Blocking) 问题：一个丢包会阻塞
连接上所有流。HTTP/3 基于 QUIC (RFC 9000)，使用 UDP 传输，每个流独立可靠传输，
丢包仅影响单个流。

### 1.2 JDK 实现包结构 (Package Structure)

JDK 的 HTTP/3 实现分为四个清晰的层次，所有代码位于 `java.net.http` 模块中：

```
src/java.net.http/share/classes/
├── java/net/http/                          # 公共 API 层
│   ├── HttpClient.java                     # 客户端 API (支持 HTTP_3 版本)
│   ├── HttpOption.java                     # Http3DiscoveryMode 等选项
│   ├── StreamLimitException.java           # 流限制异常
│   └── UnsupportedProtocolVersionException.java
│
└── jdk/internal/net/http/
    ├── Http3ClientImpl.java                # HTTP/3 客户端实现
    ├── Http3Connection.java                # HTTP/3 连接管理
    ├── Http3ConnectionPool.java            # HTTP/3 连接池
    ├── Http3ExchangeImpl.java              # HTTP/3 请求/响应交换
    ├── Http3Stream.java                    # HTTP/3 流基类 (sealed)
    ├── Http3PushPromiseStream.java          # 服务端推送流
    ├── Http3PushManager.java               # 推送管理
    ├── Http3PendingConnections.java         # 待定连接管理
    ├── Http3ClientProperties.java          # HTTP/3 配置属性
    ├── H3FrameOrderVerifier.java           # 帧顺序验证器
    ├── HttpQuicConnection.java             # HTTP-QUIC 连接桥接
    ├── AltSvcProcessor.java                # Alt-Svc 发现处理
    ├── AltServicesRegistry.java            # Alt-Svc 注册表
    │
    ├── http3/                              # HTTP/3 协议层
    │   ├── Http3Error.java                 # HTTP/3 错误码枚举 (RFC 9114 Section 8)
    │   ├── ConnectionSettings.java         # 连接设置 (record 类型)
    │   ├── frames/                         # HTTP/3 帧定义
    │   │   ├── Http3Frame.java             # 帧接口
    │   │   ├── Http3FrameType.java         # 帧类型枚举
    │   │   ├── AbstractHttp3Frame.java     # 帧基类
    │   │   ├── DataFrame.java             # DATA 帧 (0x00)
    │   │   ├── HeadersFrame.java          # HEADERS 帧 (0x01)
    │   │   ├── CancelPushFrame.java       # CANCEL_PUSH 帧 (0x03)
    │   │   ├── SettingsFrame.java         # SETTINGS 帧 (0x04)
    │   │   ├── PushPromiseFrame.java      # PUSH_PROMISE 帧 (0x05)
    │   │   ├── GoAwayFrame.java           # GOAWAY 帧 (0x07)
    │   │   ├── MaxPushIdFrame.java        # MAX_PUSH_ID 帧 (0x0d)
    │   │   ├── FramesDecoder.java         # 帧解码器
    │   │   ├── MalformedFrame.java        # 格式错误帧
    │   │   ├── PartialFrame.java          # 部分帧 (未完全接收)
    │   │   └── UnknownFrame.java          # 未知类型帧
    │   └── streams/                        # HTTP/3 流管理
    │       ├── Http3Streams.java           # 流类型常量 + StreamType 枚举
    │       ├── UniStreamPair.java          # 单向流对 (读/写端)
    │       ├── QueuingStreamPair.java      # 带队列的流对
    │       ├── PeerUniStreamDispatcher.java # 远端单向流分发器
    │       └── QuicStreamIntReader.java    # QUIC 流整数读取器
    │
    ├── qpack/                              # QPACK 头部压缩 (RFC 9204)
    │   ├── QPACK.java                      # 工具类 + 配置
    │   ├── Encoder.java                    # 编码器
    │   ├── Decoder.java                    # 解码器
    │   ├── DynamicTable.java               # 动态表
    │   ├── StaticTable.java                # 静态表 (99 条固定条目)
    │   ├── HeadersTable.java               # 头部表
    │   ├── TablesIndexer.java              # 表索引器
    │   ├── HeaderField.java                # 头部字段
    │   ├── TableEntry.java                 # 表条目 (含 EntryType)
    │   ├── FieldSectionPrefix.java         # 字段段前缀
    │   ├── InsertionPolicy.java            # 插入策略
    │   ├── DecodingCallback.java           # 解码回调
    │   ├── QPackException.java             # QPACK 异常
    │   ├── readers/                        # 读取器
    │   │   ├── HeaderFrameReader.java      # 头部帧读取器
    │   │   ├── EncoderInstructionsReader.java
    │   │   ├── DecoderInstructionsReader.java
    │   │   ├── FieldLineIndexedReader.java
    │   │   ├── FieldLineNameReferenceReader.java
    │   │   ├── FieldLineLiteralsReader.java
    │   │   ├── FieldLineIndexedPostBaseReader.java
    │   │   ├── FieldLineNameRefPostBaseReader.java
    │   │   ├── FieldLineReader.java
    │   │   ├── IntegerReader.java
    │   │   ├── StringReader.java
    │   │   └── ReaderError.java
    │   └── writers/                        # 写入器
    │       ├── HeaderFrameWriter.java
    │       ├── EncoderInstructionsWriter.java
    │       ├── DecoderInstructionsWriter.java
    │       ├── FieldLineIndexedWriter.java
    │       ├── FieldLineIndexedNameWriter.java
    │       ├── FieldLineLiteralsWriter.java
    │       ├── FieldLineSectionPrefixWriter.java
    │       ├── EncoderDuplicateEntryWriter.java
    │       ├── EncoderDynamicTableCapacityWriter.java
    │       ├── EncoderInsertIndexedNameWriter.java
    │       ├── EncoderInsertLiteralNameWriter.java
    │       ├── BinaryRepresentationWriter.java
    │       ├── IntegerWriter.java
    │       └── StringWriter.java
    │
    └── quic/                               # QUIC 传输层 (RFC 9000)
        ├── QuicClient.java                 # QUIC 客户端 (1:1 对应 Http3ClientImpl)
        ├── QuicConnection.java             # QUIC 连接抽象类
        ├── QuicConnectionImpl.java         # QUIC 连接实现
        ├── QuicEndpoint.java               # QUIC 端点 (管理 UDP 通道)
        ├── QuicInstance.java               # QUIC 实例接口
        ├── QuicSelector.java               # QUIC 选择器 (NIO/虚拟线程)
        ├── QuicConnectionId.java           # 连接 ID
        ├── QuicConnectionIdFactory.java    # 连接 ID 工厂
        ├── LocalConnIdManager.java         # 本地连接 ID 管理器
        ├── PeerConnIdManager.java          # 对端连接 ID 管理器
        ├── PeerConnectionId.java           # 对端连接 ID
        ├── QuicTransportParameters.java    # 传输参数 (RFC 9000 Section 18)
        ├── ConnectionTerminator.java       # 连接终止器接口
        ├── ConnectionTerminatorImpl.java   # 连接终止器实现
        ├── TerminationCause.java           # 终止原因
        ├── QuicBaseCongestionController.java # 拥塞控制基类
        ├── QuicCongestionController.java     # 拥塞控制接口
        ├── QuicRenoCongestionController.java # NewReno 拥塞控制
        ├── QuicCubicCongestionController.java # CUBIC 拥塞控制 (RFC 9438)
        ├── QuicPacer.java                  # 发送速率控制
        ├── QuicRttEstimator.java           # RTT 估计器
        ├── QuicTimerQueue.java             # 定时器队列
        ├── QuicTimedEvent.java             # 定时事件
        ├── IdleTimeoutManager.java         # 空闲超时管理器
        ├── QuicPacketReceiver.java         # 数据包接收器
        ├── PacketEmitter.java              # 数据包发射器
        ├── PacketSpaceManager.java         # 包空间管理器
        ├── CodingContext.java              # 编码上下文
        ├── BuffersReader.java              # 缓冲区读取器
        ├── OrderedFlow.java                # 有序流
        ├── VariableLengthEncoder.java      # 变长整数编码
        ├── QuicStreamLimitException.java   # 流限制异常
        ├── packets/                        # QUIC 数据包
        │   ├── QuicPacket.java             # 数据包接口
        │   ├── QuicPacketDecoder.java      # 数据包解码器
        │   ├── QuicPacketEncoder.java      # 数据包编码器
        │   ├── QuicPacketNumbers.java      # 包号管理
        │   ├── PacketSpace.java            # 包空间 (Initial/Handshake/Application)
        │   ├── LongHeader.java             # 长头格式
        │   ├── LongHeaderPacket.java       # 长头数据包
        │   ├── ShortHeaderPacket.java      # 短头数据包 (1-RTT)
        │   ├── InitialPacket.java          # Initial 包
        │   ├── HandshakePacket.java        # Handshake 包
        │   ├── OneRttPacket.java           # 1-RTT 包
        │   ├── ZeroRttPacket.java          # 0-RTT 包
        │   ├── RetryPacket.java            # Retry 包
        │   └── VersionNegotiationPacket.java # 版本协商包
        ├── frames/                         # QUIC 帧
        │   ├── QuicFrame.java              # 帧接口
        │   ├── AckFrame.java               # ACK 帧
        │   ├── CryptoFrame.java            # CRYPTO 帧 (TLS 数据)
        │   ├── StreamFrame.java            # STREAM 帧
        │   ├── ConnectionCloseFrame.java   # 连接关闭帧
        │   ├── MaxDataFrame.java           # MAX_DATA 帧
        │   ├── MaxStreamDataFrame.java     # MAX_STREAM_DATA 帧
        │   ├── MaxStreamsFrame.java         # MAX_STREAMS 帧
        │   ├── NewConnectionIDFrame.java   # 连接 ID 更新
        │   ├── RetireConnectionIDFrame.java
        │   ├── NewTokenFrame.java          # 令牌帧 (0-RTT)
        │   ├── PingFrame.java              # PING 帧
        │   ├── PaddingFrame.java           # 填充帧
        │   ├── ResetStreamFrame.java       # 流重置帧
        │   ├── StopSendingFrame.java       # 停止发送帧
        │   ├── HandshakeDoneFrame.java     # 握手完成帧
        │   ├── PathChallengeFrame.java     # 路径挑战帧
        │   ├── PathResponseFrame.java      # 路径响应帧
        │   ├── DataBlockedFrame.java       # 数据阻塞帧
        │   ├── StreamDataBlockedFrame.java # 流数据阻塞帧
        │   └── StreamsBlockedFrame.java    # 流阻塞帧
        └── streams/                        # QUIC 流
            ├── QuicStream.java             # 流接口 (sealed)
            ├── AbstractQuicStream.java     # 流抽象基类
            ├── QuicBidiStream.java         # 双向流接口
            ├── QuicBidiStreamImpl.java     # 双向流实现
            ├── QuicSenderStream.java       # 发送流接口
            ├── QuicSenderStreamImpl.java   # 发送流实现
            ├── QuicReceiverStream.java     # 接收流接口
            ├── QuicReceiverStreamImpl.java # 接收流实现
            ├── QuicStreams.java            # 流工具类
            ├── QuicConnectionStreams.java  # 连接流管理
            ├── QuicStreamReader.java       # 流读取器
            ├── QuicStreamWriter.java       # 流写入器
            ├── StreamCreationPermit.java   # 流创建许可
            ├── StreamWriterQueue.java      # 流写入队列
            └── CryptoWriterQueue.java      # CRYPTO 写入队列
```

---

## 2. QUIC 传输层实现 (QUIC Transport Layer)

### 2.1 QuicClient -- QUIC 客户端入口

**文件**: `jdk/internal/net/http/quic/QuicClient.java`

`QuicClient` 是 QUIC 层的核心入口，与 `Http3ClientImpl` 一一对应。它负责创建连接、
管理端点、处理 QUIC 版本协商。

```java
// 源码中的实际声明
public final class QuicClient implements QuicInstance, AutoCloseable {

    // 常量定义 (来自 RFC 9000 Section 14)
    static final int SMALLEST_MAXIMUM_DATAGRAM_SIZE = 1200;
    static final int INITIAL_SERVER_CONNECTION_ID_LENGTH = 17;
    static final int MAX_ENDPOINTS_LIMIT = 16;
    static final int DEFAULT_MAX_ENDPOINTS = Utils.getIntegerNetProperty(
            "jdk.httpclient.quic.maxEndpoints", 1);

    private final QuicTLSContext quicTLSContext;
    private final SSLParameters sslParameters;
    private final List<QuicVersion> availableVersions;  // QUIC 版本偏好列表
    private final QuicTransportParameters transportParams;
    private final QuicEndpoint[] endpoints;              // 端点数组
    private volatile QuicSelector<?> selector;           // NIO/虚拟线程选择器
    private final Map<InitialTokenRecipient, byte[]> initialTokens; // NEW_TOKEN 缓存
}
```

关键设计决策：

1. **多端点支持 (Multi-endpoint)**: 通过 `QuicEndpoint[]` 数组支持多个 UDP 端点，
   `chooseEndpoint()` 方法基于 `connectionCount()` 实现负载均衡。每个端点对应一个
   UDP `DatagramChannel`。端点数量上限为 `MAX_ENDPOINTS_LIMIT=16`，默认由
   `jdk.httpclient.quic.maxEndpoints` 控制（默认 1）。

2. **双通道模式 (Dual Channel Mode)**: 通过 `QuicEndpoint.ChannelType` 枚举支持两种模式：
   - `NON_BLOCKING_WITH_SELECTOR`: 非阻塞 NIO + `QuicSelector.createQuicNioSelector()`
   - `BLOCKING_WITH_VIRTUAL_THREADS`: 阻塞 I/O + 虚拟线程 + `QuicSelector.createQuicVirtualThreadPoller()`

3. **版本协商 (Version Negotiation)**: 默认支持 QUIC v1 (RFC 9000) 和 QUIC v2 (RFC 9369)，
   v1 优先。通过 `jdk.httpclient.quic.available.versions` 系统属性配置，值为十六进制版本号
   的逗号分隔列表。

4. **NEW_TOKEN 管理**: `initialTokenFor()` / `registerInitialToken()` 管理服务端发送的
   初始令牌。令牌按 `(host, port)` 存储于 `ConcurrentHashMap`，使用后即移除（一次性使用，
   见 RFC 9000 Section 8.1.3）。

### 2.2 QuicConnection / QuicConnectionImpl -- QUIC 连接

**文件**: `jdk/internal/net/http/quic/QuicConnection.java` (抽象类),
`jdk/internal/net/http/quic/QuicConnectionImpl.java` (实现)

`QuicConnection` 是抽象基类，定义了 QUIC 连接的公共 API：

```java
// 源码中的实际 API
public abstract class QuicConnection {
    // 启动 QUIC 握手，返回 CompletableFuture<QuicEndpoint>
    public abstract CompletableFuture<QuicEndpoint> startHandshake();

    // 创建本地发起的双向流（受对端 MAX_STREAMS 限制）
    public abstract CompletableFuture<QuicBidiStream> openNewLocalBidiStream(
            Duration limitIncreaseDuration);

    // 创建本地发起的单向流（写入专用）
    public abstract CompletableFuture<QuicSenderStream> openNewLocalUniStream(
            Duration limitIncreaseDuration);

    // 添加远端流监听器，返回 true 表示获取该流
    public abstract void addRemoteStreamListener(
            Predicate<? super QuicReceiverStream> streamConsumer);

    // 连接状态与终止
    public abstract boolean isOpen();
    public abstract TerminationCause terminationCause();
    public abstract ConnectionTerminator connectionTerminator();
    public abstract CompletableFuture<Long> requestSendPing();
}
```

`QuicConnectionImpl` 实现中的关键并发机制：
- 使用 `ReentrantLock` 保护连接状态变更
- `ConcurrentLinkedQueue` 管理待处理帧
- `AtomicBoolean` / `AtomicInteger` 管理连接状态标志
- `VarHandle` 用于原子字段更新
- `SequentialScheduler` 序列化 I/O 事件处理

连接创建流程（源自 `QuicClient.createConnectionFor()`）：

```java
// 通过 AltService 创建连接
public QuicConnectionImpl createConnectionFor(AltService service) {
    InetSocketAddress peerAddress = new InetSocketAddress(
        service.identity().host(), service.identity().port());
    String alpn = service.alpn();  // 必须为 "h3"
    SSLParameters sslParameters = createSSLParameters(new String[]{alpn});
    return new QuicConnectionImpl(null, this, peerAddress,
        service.origin().host(), service.origin().port(),
        sslParameters, "QuicClientConnection(%s)", CONNECTIONS.incrementAndGet());
}
```

### 2.3 QUIC 流层次 (Stream Hierarchy)

QUIC 流通过 sealed interface 建模，严格约束实现类型：

```java
// 源码中的 sealed interface 声明
public sealed interface QuicStream
    permits QuicSenderStream, QuicReceiverStream, QuicBidiStream, AbstractQuicStream {

    sealed interface StreamState permits
        QuicReceiverStream.ReceivingStreamState,
        QuicSenderStream.SendingStreamState,
        QuicBidiStream.BidiStreamState { }
}
```

QUIC 流 ID 编码规则 (RFC 9000 Section 2.1)：
- bit 0: 发起方 (0=客户端, 1=服务端)
- bit 1: 方向 (0=双向, 1=单向)
- 客户端双向流 ID: 0, 4, 8, 12, ...
- 客户端单向流 ID: 2, 6, 10, 14, ...

`QuicConnectionStreams` 管理一个连接上所有流的创建和生命周期，
`StreamCreationPermit` 实现流数量限制（基于对端发送的 `MAX_STREAMS` 帧）。

### 2.4 QUIC 数据包处理 (Packet Processing)

**包**: `jdk/internal/net/http/quic/packets/`

QUIC 定义了多种数据包类型，通过 `PacketSpace` 枚举管理：

```java
// PacketSpace -- 包号空间
// Initial: 初始阶段 (Initial packet)
// Handshake: 握手阶段 (Handshake packet)
// ApplicationData: 应用数据 (1-RTT / 0-RTT packet)
```

数据包类继承结构：
- `QuicPacket` -- 接口
  - `LongHeaderPacket` -- 长头包基类
    - `InitialPacket` -- Initial 包 (含 token, 最小 1200 字节)
    - `HandshakePacket` -- Handshake 包
    - `ZeroRttPacket` -- 0-RTT 包
  - `ShortHeaderPacket` -- 短头包
    - `OneRttPacket` -- 1-RTT 包 (应用数据)
  - `RetryPacket` -- Retry 包 (无状态重试)
  - `VersionNegotiationPacket` -- 版本协商包

`QuicPacketEncoder` 和 `QuicPacketDecoder` 处理数据包的序列化/反序列化，
包括头部保护 (Header Protection) 和包号编码。

### 2.5 拥塞控制 (Congestion Control)

JDK 实现了两种拥塞控制算法：

1. **NewReno** (`QuicRenoCongestionController`): 基于 RFC 9002 的实现
2. **CUBIC** (`QuicCubicCongestionController`): 基于 RFC 9438 的实现

```java
// QuicCubicCongestionController 源码中的常量
public final class QuicCubicCongestionController extends QuicBaseCongestionController {
    public static final double BETA = 0.7;                        // 乘法下降因子
    public static final double ALPHA = 3 * (1 - BETA) / (1 + BETA); // 加法增长因子
    private static final double C = 0.4;                          // CUBIC 参数
    private final QuicRttEstimator rttEstimator;
    private long wMaxBytes;    // CUBIC 曲线拐点 (字节)
    private long cwndPriorBytes; // 最近拥塞事件前的 cwnd
}
```

`QuicPacer` 在拥塞控制基础上平滑发送速率，避免突发流量。
`QuicRttEstimator` 基于采样估算 RTT、RTTVAR 和 MinRTT。

---

## 3. HTTP/3 连接管理 (HTTP/3 Connection Management)

### 3.1 Http3ClientImpl -- HTTP/3 客户端实现

**文件**: `jdk/internal/net/http/Http3ClientImpl.java`

`Http3ClientImpl` 是 `HttpClientImpl` 的 HTTP/3 专属组件：

```java
final class Http3ClientImpl implements AutoCloseable {
    // QUIC 版本配置（默认 v1 + v2，v1 优先）
    private static final List<QuicVersion> availableQuicVersions;
    static {
        // 默认: QUIC_V1, QUIC_V2
        // 可通过 jdk.httpclient.quic.available.versions 配置
        // 值为逗号分隔的十六进制版本号
    }
}
```

版本优先级通过系统属性 `jdk.httpclient.quic.available.versions` 控制。
`QuicClient` 构建时验证 `QuicTLSContext` 是否支持所有请求的 QUIC 版本。

### 3.2 Http3Connection -- HTTP/3 连接核心

**文件**: `jdk/internal/net/http/Http3Connection.java`

`Http3Connection` 封装了一个 QUIC 连接上的所有 HTTP/3 语义：

```java
public final class Http3Connection implements AutoCloseable {
    private final Http3ClientImpl client;
    private final HttpQuicConnection connection;
    private final QuicConnection quicConnection;

    // HTTP/3 关键流 (Critical Streams)
    private final UniStreamPair controlStreamPair;    // 控制流对
    private final UniStreamPair qpackEncoderStreams;   // QPACK 编码器流对
    private final UniStreamPair qpackDecoderStreams;   // QPACK 解码器流对

    // QPACK 编解码器
    private final Encoder qpackEncoder;
    private final Decoder qpackDecoder;

    // 帧解码与验证
    private final FramesDecoder controlFramesDecoder;
    private final H3FrameOrderVerifier frameOrderVerifier;

    // 活跃交换
    private final ConcurrentMap<Long, QuicBidiStream> exchangeStreams;
    private final ConcurrentMap<Long, Http3ExchangeImpl<?>> exchanges;

    // 连接状态
    private volatile boolean settingsFrameReceived;
    private volatile ConnectionSettings peerSettings;
    private volatile ConnectionSettings ourSettings;
    private final AtomicLong lowestGoAwayReceipt;  // GOAWAY 追踪

    // 关闭状态位域
    private static final int GOAWAY_SENT = 1;
    private static final int GOAWAY_RECEIVED = 2;
    private static final int CLOSED = 4;
    volatile int closedState;

    // 推送管理
    private final Http3PushManager pushManager;
    private final AtomicLong maxPushIdSent;
}
```

#### 连接初始化流程

`Http3Connection` 构造函数中完成以下初始化：

1. **创建控制流**: 通过 `UniStreamPair(StreamType.CONTROL, ...)` 创建本地控制流，
   并注册远端流监听器

2. **创建 QPACK 流**: 编码器和解码器分别拥有独立的单向流对

3. **发送 SETTINGS**: 通过 `controlStreamPair.futureSenderStreamWriter()` 异步链
   先发送 SETTINGS 帧，再发送 MAX_PUSH_ID 帧

4. **配置空闲超时**: 通过 `ConnectionTerminator.appLayerMaxIdle()` 配置

```java
// 构造函数中的异步初始化链
controlStreamPair.futureSenderStreamWriter()
    .thenApply(this::sendSettings)        // 先发送 SETTINGS
    .thenApply(this::sendMaxPushId)       // 再发送 MAX_PUSH_ID
    .exceptionally(this::exceptionallyAndClose);  // 异常则关闭连接
```

#### ConnectionSettings (连接设置)

`ConnectionSettings` 是一个 record 类型，表示 HTTP/3 SETTINGS 帧中的参数：

```java
// 源码中的 record 声明
public record ConnectionSettings(
    long maxFieldSectionSize,     // SETTINGS_MAX_FIELD_SECTION_SIZE (默认无限)
    long qpackMaxTableCapacity,   // SETTINGS_QPACK_MAX_TABLE_CAPACITY (默认 0)
    long qpackBlockedStreams       // SETTINGS_QPACK_BLOCKED_STREAMS (默认 0)
) { }
```

### 3.3 Http3Stream / Http3ExchangeImpl -- 请求/响应流

**文件**: `jdk/internal/net/http/Http3Stream.java`, `Http3ExchangeImpl.java`

`Http3Stream` 是一个 sealed 抽象类：

```java
sealed abstract class Http3Stream<T> extends ExchangeImpl<T>
    permits Http3ExchangeImpl, Http3PushPromiseStream {

    enum ResponseState { PERMIT_HEADER, PERMIT_TRAILER, PERMIT_NONE }

    private volatile long receivedQuicBytes;      // 已接收 QUIC 字节数
    private ResponseState responseState;          // 响应帧状态机
    private Long contentLength;                   // Content-Length 值
    private long consumedDataBytes;               // 已消费数据字节
    private volatile boolean readingPaused;       // 读取暂停标志
    final ConcurrentLinkedQueue<List<ByteBuffer>> responseData; // 响应数据缓冲
}
```

`Http3ExchangeImpl` 处理实际的请求发送和响应接收，使用 QPACK 编码请求头、
通过 QUIC 双向流发送 HEADERS 和 DATA 帧、通过 `FramesDecoder` 解码响应帧。

### 3.4 Http3ConnectionPool -- 连接池管理

`Http3ConnectionPool` 管理 HTTP/3 连接的复用。连接以 `connectionKey` 为索引
（基于请求的目标主机和端口），支持多连接并发。当流限制 (`streamLimitReached`)
触发时，可创建到同一服务端的新连接。

---

## 4. HTTP/3 帧处理 (HTTP/3 Frame Processing)

### 4.1 帧类型定义 (Frame Types)

**文件**: `jdk/internal/net/http/http3/frames/Http3FrameType.java`

源码中帧类型定义为枚举，每种帧类型关联一个类型值和最大长度：

```java
public enum Http3FrameType {
    UNKNOWN(-1, MAX_ENCODED_INTEGER),
    DATA(0x00, MAX_ENCODED_INTEGER),          // 数据帧
    HEADERS(0x01, MAX_ENCODED_INTEGER),        // 头部帧
    CANCEL_PUSH(0x03, MAX_INTEGER_LENGTH),     // 取消推送
    SETTINGS(0x04, MAX_SETTINGS_LENGTH),       // 设置帧
    PUSH_PROMISE(0x05, MAX_ENCODED_INTEGER),   // 推送承诺
    GOAWAY(0x07, MAX_INTEGER_LENGTH),          // 连接优雅关闭
    MAX_PUSH_ID(0x0d, MAX_INTEGER_LENGTH);     // 最大推送 ID
}
```

非法帧类型（HTTP/2 帧在 HTTP/3 中无等价物）：
- `0x02` -- 原 HTTP/2 PRIORITY
- `0x06` -- 原 HTTP/2 PING
- `0x08` -- 原 HTTP/2 WINDOW_UPDATE
- `0x09` -- 原 HTTP/2 CONTINUATION

保留帧类型模式: `0x21 + 0x1f * N` (N >= 0)

### 4.2 帧解码 (Frame Decoding)

**文件**: `jdk/internal/net/http/http3/frames/FramesDecoder.java`

`FramesDecoder` 是核心帧解码器，支持增量解码（帧可跨越多个缓冲区）：

- 使用 `PartialFrame` 表示尚未完全接收的帧
- 使用 `MalformedFrame` 表示格式错误的帧
- 通过 `Predicate<Http3FrameType>` 参数过滤特定流上允许的帧类型
  - `FramesDecoder::isAllowedOnControlStream` -- 控制流帧过滤
  - 请求/响应流上允许 DATA、HEADERS、PUSH_PROMISE

### 4.3 帧顺序验证 (Frame Order Verification)

**文件**: `jdk/internal/net/http/H3FrameOrderVerifier.java`

`H3FrameOrderVerifier` 确保帧按 RFC 9114 规定的顺序到达：

控制流帧顺序:
1. 第一帧必须是 SETTINGS
2. 之后可以是 GOAWAY、CANCEL_PUSH、MAX_PUSH_ID 等（不允许 DATA/HEADERS）

请求流帧顺序:
1. HEADERS (请求/响应头部)
2. DATA (零或多个)
3. HEADERS (可选的 trailers)

### 4.4 HTTP/3 流类型 (Stream Types)

**文件**: `jdk/internal/net/http/http3/streams/Http3Streams.java`

HTTP/3 定义了四种单向流类型，通过流上的第一个变长整数标识：

```java
public final class Http3Streams {
    public static final int CONTROL_STREAM_CODE = 0x00;        // 控制流
    public static final int PUSH_STREAM_CODE = 0x01;           // 推送流
    public static final int QPACK_ENCODER_STREAM_CODE = 0x02;  // QPACK 编码器流
    public static final int QPACK_DECODER_STREAM_CODE = 0x03;  // QPACK 解码器流

    public enum StreamType {
        CONTROL(0x00), PUSH(0x01),
        QPACK_ENCODER(0x02), QPACK_DECODER(0x03);
    }
}
```

`UniStreamPair` 管理一对单向流（本地发送 + 远端接收），用于控制流和 QPACK 流。
`PeerUniStreamDispatcher` 根据流类型码将远端创建的单向流分发给对应的处理器。

---

## 5. QPACK 头部压缩 (QPACK Header Compression)

### 5.1 设计对比: HPACK vs QPACK

HPACK (HTTP/2, RFC 7541) 使用单一串行字节流，导致头部解码存在队头阻塞。
QPACK (HTTP/3, RFC 9204) 通过独立流传输编码器/解码器指令，消除阻塞：

```
HPACK (HTTP/2):
  Stream 1 ────────► 共享解码器状态 ← 必须按序处理
  Stream 2 ────────►                   → 队头阻塞
  Stream 3 ────────►

QPACK (HTTP/3):
  请求流 1 ────────────────────► 独立解码 (仅引用已确认的表条目)
  请求流 2 ────────────────────► 独立解码
  编码器指令流 ─────────────────► 更新动态表
  解码器指令流 ◄─────────────────  发送确认
```

### 5.2 QPACK Encoder (编码器)

**文件**: `jdk/internal/net/http/qpack/Encoder.java`

```java
public class Encoder {
    // 敏感头部字段 -- 不压缩，使用字面量编码
    private static final Set<String> SENSITIVE_HEADER_NAMES =
        Set.of("cookie", "authorization", "proxy-authorization");

    private final InsertionPolicy policy;         // 动态表插入策略
    private final TablesIndexer tablesIndexer;     // 表索引器（静态表 + 动态表查找）
    private final DynamicTable dynamicTable;        // 动态表
    private final QueuingStreamPair encoderStreams; // 编码器指令流
    private final DecoderInstructionsReader decoderInstructionsReader; // 读取解码器确认
}
```

编码流程:
1. 使用 `TablesIndexer` 在静态表和动态表中查找匹配的头部字段
2. 完全匹配 → 索引引用 (`FieldLineIndexedWriter`)
3. 名称匹配 → 名称引用 + 字面量值 (`FieldLineIndexedNameWriter`)
4. 无匹配 → 字面量编码 (`FieldLineLiteralsWriter`)
5. 通过 `InsertionPolicy` 决定是否将新条目插入动态表
6. 通过编码器指令流发送 `Insert With Name Reference`、`Insert With Literal Name`、
   `Duplicate`、`Set Dynamic Table Capacity` 等指令
7. `FieldLineSectionPrefixWriter` 写入编码块前缀（Required Insert Count + S-bit + Delta Base）

敏感头部保护 (RFC 9204 Section 7.1.3): `cookie`、`authorization`、`proxy-authorization`
始终使用字面量编码（Never-Indexed Literals），防止 CRIME/BREACH 攻击。

### 5.3 QPACK Decoder (解码器)

**文件**: `jdk/internal/net/http/qpack/Decoder.java`

```java
public final class Decoder {
    private final DynamicTable dynamicTable;
    private final EncoderInstructionsReader encoderInstructionsReader;
    private final QueuingStreamPair decoderStreamPair;
}
```

解码器支持增量解码：头部块可以跨越多个 `ByteBuffer`，通过 `HeaderFrameReader`
逐步解析。解码完成后通过 `DecoderInstructionsWriter` 在解码器指令流上发送
`Section Acknowledgement` 和 `Insert Count Increment` 指令。

### 5.4 静态表与动态表

**文件**: `jdk/internal/net/http/qpack/StaticTable.java`, `DynamicTable.java`

QPACK 静态表包含 99 个预定义条目 (RFC 9204 Appendix A)，涵盖常见 HTTP 头部：
- `:authority`, `:path=/`, `:method=GET`, `:scheme=https` 等伪头部
- `content-type`, `accept`, `cache-control` 等常见头部
- 常见状态码: `200`, `204`, `206`, `304`, `400`, `403`, `404`, `500`

`DynamicTable` 是按 FIFO 顺序维护的环形缓冲区。通过 `ENTRY_SIZE` 常量计算条目大小
(= 头部名长度 + 头部值长度 + 32)。`InsertionPolicy` 控制何时向动态表添加条目，
避免频繁驱逐导致的性能下降。

### 5.5 QPACK 配置属性

以下属性定义在 `Http3ClientProperties` 中：

| 属性 | 说明 |
|------|------|
| `QPACK_ENCODER_TABLE_CAPACITY_LIMIT` | 编码器动态表容量上限 |
| `QPACK_DECODER_MAX_TABLE_CAPACITY` | 解码器 SETTINGS_QPACK_MAX_TABLE_CAPACITY |
| `QPACK_DECODER_BLOCKED_STREAMS` | 解码器 SETTINGS_QPACK_BLOCKED_STREAMS |
| `QPACK_DECODER_MAX_FIELD_SECTION_SIZE` | 最大字段段大小 |
| `QPACK_ENCODER_DRAINING_THRESHOLD` | 编码器排空阈值 |
| `QPACK_ALLOW_BLOCKING_ENCODING` | 是否允许阻塞编码 |

---

## 6. Alt-Svc 发现与协议协商 (Alt-Svc Discovery)

### 6.1 AltSvcProcessor -- Alt-Svc 解析

**文件**: `jdk/internal/net/http/AltSvcProcessor.java`

`AltSvcProcessor` 解析 `Alt-Svc` HTTP 头部和 HTTP/2 ALT_SVC 帧，发现 HTTP/3 端点：

```java
final class AltSvcProcessor {
    private static final String HEADER = "alt-svc";

    // 内部记录类，解析 Alt-Svc 头部值
    private record ParsedHeaderValue(
        String rawValue,
        String alpnName,     // 如 "h3"
        String host,         // 替代主机（可为空，继承 origin）
        int port,            // 替代端口
        Map<String, String> parameters  // ma (max-age) 等参数
    ) { }
}
```

Alt-Svc 头部格式: `h3=":443"; ma=2592000` 表示 HTTP/3 服务在同一主机的 443 端口可用，
最大缓存时间 2592000 秒（30 天）。

### 6.2 AltServicesRegistry -- 替代服务注册表

**文件**: `jdk/internal/net/http/AltServicesRegistry.java`

`AltServicesRegistry` 缓存已发现的替代服务，以 `AltService` 记录存储：

```java
// AltService 包含以下信息：
// - identity: 替代服务的主机和端口
// - origin: 原始服务的主机和端口
// - alpn: 应用层协议名（如 "h3"）
```

`QuicClient.createConnectionFor(AltService service)` 使用 `AltService` 创建 QUIC 连接，
ALPN 从 `AltService.alpn()` 获取。

### 6.3 Http3DiscoveryMode -- 发现模式

`HttpOption.Http3DiscoveryMode` 控制 HTTP/3 的发现策略：
- 基于 Alt-Svc 头部的自动发现
- 直接连接模式（通过 `MAX_DIRECT_CONNECTION_TIMEOUT` 控制超时）

`Http3PendingConnections` 管理正在建立的 HTTP/3 连接，避免重复连接尝试。

---

## 7. 连接建立流程 (Connection Establishment)

### 7.1 QUIC 握手过程

```
客户端                                    服务端
   │                                         │
   │  ──── Initial [CRYPTO(ClientHello)] ──►  │   InitialPacket
   │       + 传输参数 (QuicTransportParameters)│
   │       + 填充至 ≥ 1200 字节              │
   │                                         │
   │  ◄─── Initial [CRYPTO(ServerHello)] ──   │   InitialPacket
   │                                         │
   │  ◄─── Handshake [CRYPTO] ──────────────  │   HandshakePacket
   │       EncryptedExtensions                │
   │       Certificate                        │
   │       CertificateVerify                  │
   │       Finished                           │
   │       + HANDSHAKE_DONE 帧               │
   │                                         │
   │  ──── Handshake [CRYPTO(Finished)] ───►  │   HandshakePacket
   │                                         │
   │  ════ 1-RTT [STREAM(HTTP/3 请求)] ═══►  │   OneRttPacket
   │       此时 HTTP/3 层可以开始工作         │
```

TLS 1.3 是 QUIC 的强制要求（`QuicClient.requireTLS13()` 验证），
SSL 参数中必须包含 `TLSv1.3` 协议。

`QuicConnection.startHandshake()` 返回 `CompletableFuture<QuicEndpoint>`，
握手完成后可通过 `handshakeReachedPeer()` 获取对端确认。

### 7.2 HTTP/3 连接建立

QUIC 握手成功后，`Http3Connection` 构造函数自动执行：

1. 创建本地控制流 (`UniStreamPair` with `StreamType.CONTROL`)
2. 创建 QPACK 编码器/解码器及其对应流
3. 在控制流上发送 SETTINGS 帧
4. 发送 MAX_PUSH_ID 帧
5. 注册远端流监听器 (`addRemoteStreamListener`)
6. 配置空闲超时

---

## 8. HTTP/3 错误处理 (Error Handling)

### 8.1 Http3Error 错误码 (RFC 9114 Section 8)

**文件**: `jdk/internal/net/http/http3/Http3Error.java`

源码中 `Http3Error` 是一个枚举，覆盖所有 RFC 9114 和 RFC 9204 定义的错误码：

```java
public enum Http3Error {
    H3_NO_ERROR                (0x0100),  // 无错误
    H3_GENERAL_PROTOCOL_ERROR  (0x0101),  // 通用协议错误
    H3_INTERNAL_ERROR          (0x0102),  // 内部错误
    H3_STREAM_CREATION_ERROR   (0x0103),  // 流创建错误
    H3_CLOSED_CRITICAL_STREAM  (0x0104),  // 关键流关闭
    H3_FRAME_UNEXPECTED        (0x0105),  // 帧位置不正确
    H3_FRAME_ERROR             (0x0106),  // 帧格式错误
    H3_EXCESSIVE_LOAD          (0x0107),  // 过载
    H3_ID_ERROR                (0x0108),  // Stream ID / Push ID 错误
    H3_SETTINGS_ERROR          (0x0109),  // SETTINGS 帧错误
    H3_MISSING_SETTINGS        (0x010a),  // 缺少 SETTINGS 帧
    H3_REQUEST_REJECTED        (0x010b),  // 请求被拒绝
    H3_REQUEST_CANCELLED       (0x010c),  // 请求取消
    H3_REQUEST_INCOMPLETE      (0x010d),  // 请求不完整
    H3_MESSAGE_ERROR           (0x010e),  // 消息格式错误
    H3_CONNECT_ERROR           (0x010f),  // CONNECT 错误
    H3_VERSION_FALLBACK        (0x0110),  // 需要版本降级

    // QPACK 错误 (RFC 9204 Section 6)
    QPACK_DECOMPRESSION_FAILED     (0x0200),  // 解压失败
    QPACK_ENCODER_STREAM_ERROR     (0x0201),  // 编码器流错误
    QPACK_DECODER_STREAM_ERROR     (0x0202);  // 解码器流错误
}
```

### 8.2 新增公共异常类

- `StreamLimitException` (`java.net.http`): 当 QUIC 流数量达到对端限制时抛出
- `UnsupportedProtocolVersionException` (`java.net.http`): 协议版本不支持时抛出
- `QuicStreamLimitException` (`jdk.internal.net.http.quic`): QUIC 层流限制异常

### 8.3 连接关闭状态机

`Http3Connection` 使用位域追踪关闭状态：

```java
private static final int GOAWAY_SENT = 1;     // 本端已发送 GOAWAY
private static final int GOAWAY_RECEIVED = 2;  // 已接收 GOAWAY
private static final int CLOSED = 4;           // QUIC 连接已关闭
```

收到 GOAWAY 后，`lowestGoAwayReceipt` 记录最低的未处理请求流 ID。
所有 ID >= 该值的请求可以安全重试。连接终止通过 `ConnectionTerminator`
接口管理，支持应用层和 QUIC 层的优雅关闭。

---

## 9. 回退机制 (Fallback to HTTP/2)

### 9.1 版本降级策略

JDK 实现支持从 HTTP/3 自动降级到 HTTP/2 或 HTTP/1.1：

1. **Alt-Svc 发现失败**: 如果无法从 Alt-Svc 头部发现 HTTP/3 端点，继续使用 HTTP/2
2. **QUIC 握手失败**: 如果 QUIC 连接建立失败（超时、证书错误等），回退到 HTTP/2
3. **H3_VERSION_FALLBACK 错误**: 服务端通过此错误码明确要求降级
4. **直连超时**: `MAX_DIRECT_CONNECTION_TIMEOUT` 控制直连模式的超时

`Exchange.java` 和 `MultiExchange.java` 实现了版本协商和重试逻辑。
`Http3ClientImpl` 在发现流限制 (`WAIT_FOR_PENDING_CONNECT`) 时也会考虑
创建新连接或降级。

### 9.2 HttpOption 配置

```java
// java/net/http/HttpOption.java 中的 HTTP/3 相关选项
public enum Http3DiscoveryMode {
    // 控制 HTTP/3 的发现模式
}
```

---

## 10. 流量控制 (Flow Control)

### 10.1 QUIC 层流量控制

QUIC 提供两级流量控制：

- **连接级**: `MaxDataFrame` / `DataBlockedFrame` 控制整个连接的数据量
- **流级**: `MaxStreamDataFrame` / `StreamDataBlockedFrame` 控制单个流的数据量

传输参数 (`QuicTransportParameters.ParameterId`) 设置初始窗口：
- `initial_max_data` -- 初始连接级数据量限制
- `initial_max_stream_data_bidi_local` -- 本地双向流初始数据量
- `initial_max_stream_data_bidi_remote` -- 远端双向流初始数据量
- `initial_max_stream_data_uni` -- 单向流初始数据量

### 10.2 流数量控制

- `initial_max_streams_bidi` -- 初始最大双向流数量
- `initial_max_streams_uni` -- 初始最大单向流数量
- `MaxStreamsFrame` -- 运行时增加流数量限制
- `StreamsBlockedFrame` -- 通知对端已达到流限制

`QuicConnection.openNewLocalBidiStream(Duration limitIncreaseDuration)` 在流限制
达到时等待指定时长（`MAX_STREAM_LIMIT_WAIT_TIMEOUT`），如果超时则抛出
`QuicStreamLimitException`（向上传递为 `StreamLimitException`）。

---

## 11. 性能设计要点 (Performance Design)

### 11.1 零拷贝与缓冲区管理

- `BuffersReader` 管理 QUIC 层的缓冲区读取
- `StreamWriterQueue` / `CryptoWriterQueue` 实现写入队列，避免阻塞
- 使用 `ByteBuffer` 直接操作，最小化数据拷贝

### 11.2 并发模型

- `SequentialScheduler` 序列化 I/O 事件处理（来自 `jdk.internal.net.http.common`）
- `ConcurrentHashMap` 管理活跃交换和流
- `CompletableFuture` 链式异步操作贯穿整个调用栈
- `ReentrantLock` 保护关键状态变更（连接关闭、流创建等）

### 11.3 0-RTT 支持

`ZeroRttPacket` 支持使用之前会话的密钥发送早期数据。
`QuicClient.initialTokenFor()` 管理服务端发放的 NEW_TOKEN，用于后续连接的
Initial 包，减少握手往返。

### 11.4 连接迁移

QUIC 支持连接 ID 迁移：
- `LocalConnIdManager` / `PeerConnIdManager` 管理连接 ID 生命周期
- `NewConnectionIDFrame` / `RetireConnectionIDFrame` 实现 ID 轮换
- `PathChallengeFrame` / `PathResponseFrame` 验证新路径

---

## 12. 配置参数汇总 (Configuration Summary)

| 系统属性 | 默认值 | 说明 |
|---------|--------|------|
| `jdk.httpclient.quic.maxEndpoints` | 1 | 每客户端最大 UDP 端点数 |
| `jdk.httpclient.quic.available.versions` | (QUIC_V1,QUIC_V2) | 可用 QUIC 版本 |
| `jdk.httpclient.http3.*` | - | HTTP/3 相关属性 |
| `jdk.httpclient.qpack.*` | - | QPACK 相关属性 |

---

## 13. 总结 (Summary)

JEP 517 在 JDK 中实现了完整的 HTTP/3 协议栈：

1. **QUIC 传输层**: 纯 Java 实现的完整 QUIC 协议 (RFC 9000/9001/9002/9369)，
   包含连接管理 (`QuicClient`/`QuicConnectionImpl`)、流管理 (sealed `QuicStream` 层次)、
   数据包处理 (6 种包类型)、帧处理 (20+ 种帧类型)、拥塞控制 (NewReno + CUBIC)

2. **HTTP/3 帧层**: 8 种 HTTP/3 帧类型 (`Http3FrameType` 枚举)，
   帧解码器 (`FramesDecoder`)，帧顺序验证 (`H3FrameOrderVerifier`)

3. **QPACK 压缩**: 完整的 RFC 9204 实现，编码器/解码器各自拥有独立的指令流，
   含 12+ 种读取器和 13+ 种写入器，支持阻塞/非阻塞编码模式

4. **Alt-Svc 发现**: `AltSvcProcessor` 解析 Alt-Svc 头部和 HTTP/2 ALT_SVC 帧，
   `AltServicesRegistry` 缓存发现结果

5. **连接管理**: `Http3ConnectionPool` 连接池复用，
   `Http3PendingConnections` 防止重复连接，
   自动降级到 HTTP/2/1.1

6. **安全**: TLS 1.3 强制要求，敏感头部不压缩，连接 ID 迁移
