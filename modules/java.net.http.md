# java.net.http 模块分析

> HTTP Client API，支持 HTTP/1.1、HTTP/2 和 HTTP/3 (JDK 26 新增)

---

## 1. 模块概述 (Module Overview)

`java.net.http` 模块提供了现代化的 HTTP 客户端 API，支持同步和异步请求、WebSocket，
以及 JDK 26 新增的 HTTP/3 (基于 QUIC 协议)。

**源码统计**: 313 个 Java 文件 (公开 API 14 个 + 内部实现 299 个)

### 模块定义 (Module Declaration)

**文件**: `src/java.net.http/share/classes/module-info.java`

```java
module java.net.http {
    exports java.net.http;
}
```

模块仅导出一个公开包 `java.net.http`，内部实现全部在 `jdk.internal.net.http` 下。
模块不声明 `requires` (隐式依赖 `java.base`)，也不声明 `uses` (无 SPI 机制)。

---

## 2. 包结构 (Package Structure)

### 公开 API (`java.net.http`)

```
java.net.http/
├── HttpClient.java                          # HTTP 客户端 (抽象类)
├── HttpRequest.java                         # HTTP 请求 (抽象类)
├── HttpResponse.java                        # HTTP 响应接口 + BodyHandler/BodySubscriber
├── HttpHeaders.java                         # HTTP 头 (不可变)
├── HttpOption.java                          # 请求配置提示 (sealed interface, JDK 26)
├── HttpRequestOptionImpl.java               # HttpOption 实现 (JDK 26)
├── WebSocket.java                           # WebSocket 客户端接口
├── HttpTimeoutException.java                # 超时异常
├── HttpConnectTimeoutException.java         # 连接超时异常
├── WebSocketHandshakeException.java         # WebSocket 握手异常
├── StreamLimitException.java                # 流限制异常 (JDK 26)
├── UnsupportedProtocolVersionException.java # 不支持的协议版本异常 (JDK 26)
└── package-info.java
```

### 内部实现 (`jdk.internal.net.http`)

```
jdk/internal/net/http/
├── HttpClientImpl.java            # HttpClient 核心实现
├── HttpClientBuilderImpl.java     # Builder 实现
├── HttpClientFacade.java          # 外观类 (弱引用跟踪)
├── HttpRequestImpl.java           # HttpRequest 实现
├── HttpResponseImpl.java          # HttpResponse 实现
├── Exchange.java                  # 单次请求交换
├── MultiExchange.java             # 多次交换 (重定向/重试)
├── ExchangeImpl.java              # 交换抽象实现
├── ConnectionPool.java            # HTTP/1.1 连接池
├── Http1Exchange.java             # HTTP/1.1 交换
├── Http1Request.java              # HTTP/1.1 请求编码
├── Http1Response.java             # HTTP/1.1 响应解码
├── Http2ClientImpl.java           # HTTP/2 客户端
├── Http2Connection.java           # HTTP/2 连接 (多路复用)
├── Stream.java                    # HTTP/2 流
├── Http3ClientImpl.java           # HTTP/3 客户端 (JDK 26)
├── Http3Connection.java           # HTTP/3 连接 (JDK 26)
├── Http3ExchangeImpl.java         # HTTP/3 交换 (JDK 26)
├── Http3ConnectionPool.java       # HTTP/3 连接池 (JDK 26)
├── Http3Stream.java               # HTTP/3 流 (JDK 26)
├── HttpQuicConnection.java        # QUIC 之上的 HTTP 连接
├── AltServicesRegistry.java       # Alt-Svc 注册表 (HTTP/3 发现)
├── AltSvcProcessor.java           # Alt-Svc 头处理器
├── PlainHttpConnection.java       # 明文 HTTP 连接
├── AsyncSSLConnection.java        # 异步 SSL 连接
├── SocketTube.java                # NIO SocketChannel 封装
├── SSLFlowDelegate.java           # SSL/TLS 流代理
├── SSLTube.java                   # SSL 管道
├── FilterFactory.java             # 请求过滤器工厂
├── AuthenticationFilter.java      # 认证过滤器
├── CookieFilter.java              # Cookie 过滤器
├── RedirectFilter.java            # 重定向过滤器
├── frame/                         # HTTP/2 帧定义
├── hpack/                         # HPACK 头部压缩 (HTTP/2)
├── qpack/                         # QPACK 头部压缩 (HTTP/3, JDK 26)
│   ├── readers/                   # QPACK 解码器
│   └── writers/                   # QPACK 编码器
├── http3/                         # HTTP/3 帧和流 (JDK 26)
│   ├── frames/                    # HTTP/3 帧定义
│   └── streams/                   # HTTP/3 流管理
├── quic/                          # QUIC 协议实现 (JDK 26)
│   ├── QuicClient.java            # QUIC 客户端
│   ├── QuicConnectionImpl.java    # QUIC 连接实现
│   ├── QuicSelector.java          # QUIC 事件选择器
│   ├── QuicCubicCongestionController.java  # CUBIC 拥塞控制
│   ├── QuicRenoCongestionController.java   # Reno 拥塞控制
│   ├── QuicRttEstimator.java      # RTT 估算器
│   ├── QuicPacer.java             # 发送速率控制
│   ├── frames/                    # QUIC 帧定义
│   ├── packets/                   # QUIC 包编解码
│   └── streams/                   # QUIC 流管理
├── websocket/                     # WebSocket 实现
└── common/                        # 通用工具类
```

---

## 3. 核心类分析 (Core Classes)

### 3.1 HttpClient

**文件**: `src/java.net.http/share/classes/java/net/http/HttpClient.java`

```java
public abstract class HttpClient implements AutoCloseable {

    // HTTP 版本 (Version enum)
    public enum Version {
        HTTP_1_1,   // HTTP/1.1
        HTTP_2,     // HTTP/2
        HTTP_3      // HTTP/3 (since JDK 26)
    }

    // 重定向策略 (Redirect enum)
    public enum Redirect {
        NEVER,      // 不重定向
        ALWAYS,     // 总是重定向
        NORMAL      // 正常重定向 (不从 HTTPS→HTTP)
    }

    // 构建器
    public static Builder newBuilder();
    public static HttpClient newHttpClient();

    // 同步发送 (Synchronous send)
    public abstract <T> HttpResponse<T> send(
        HttpRequest request,
        HttpResponse.BodyHandler<T> responseBodyHandler
    ) throws IOException, InterruptedException;

    // 异步发送 (Asynchronous send)
    public abstract <T> CompletableFuture<HttpResponse<T>> sendAsync(
        HttpRequest request,
        HttpResponse.BodyHandler<T> responseBodyHandler
    );

    // 异步发送 + Push Promise (HTTP/2)
    public abstract <T> CompletableFuture<HttpResponse<T>> sendAsync(
        HttpRequest request,
        HttpResponse.BodyHandler<T> responseBodyHandler,
        HttpResponse.PushPromiseHandler<T> pushPromiseHandler
    );

    // Builder 接口
    public interface Builder {
        Builder cookieHandler(CookieHandler cookieHandler);
        Builder connectTimeout(Duration duration);
        Builder sslContext(SSLContext sslContext);
        Builder sslParameters(SSLParameters sslParameters);
        Builder executor(Executor executor);
        Builder followRedirects(Redirect policy);
        Builder version(Version version);
        Builder priority(int priority);
        Builder proxy(ProxySelector proxySelector);
        Builder authenticator(Authenticator authenticator);
        Builder localAddress(InetAddress localAddr);  // JDK 26
        HttpClient build();
    }
}
```

注意: JDK 26 中 `Version` 枚举有 3 个值 (`HTTP_1_1`, `HTTP_2`, `HTTP_3`)。
之前文档中的 `HTTP_3_AUTO` 并不存在；HTTP/3 发现模式通过 `HttpOption.H3_DISCOVERY` 控制。

### 3.2 HttpOption (JDK 26 新增)

**文件**: `src/java.net.http/share/classes/java/net/http/HttpOption.java`

```java
// 密封接口 (sealed interface)，用于提供请求配置提示
public sealed interface HttpOption<T> permits HttpRequestOptionImpl {

    // HTTP/3 发现模式 (H3_DISCOVERY hint)
    HttpOption<Http3DiscoveryMode> H3_DISCOVERY =
        new HttpRequestOptionImpl<>(Http3DiscoveryMode.class, "H3_DISCOVERY");

    // HTTP/3 发现模式枚举
    enum Http3DiscoveryMode {
        ALWAYS,          // 总是尝试 HTTP/3
        ANY,             // 默认: 通过 Alt-Svc 发现 HTTP/3
        HTTP_3_URI_ONLY  // 仅当 URI 明确指定 HTTP/3 时才使用
    }
}
```

### 3.3 HttpClientImpl (核心实现)

**文件**: `src/java.net.http/share/classes/jdk/internal/net/http/HttpClientImpl.java`

```java
final class HttpClientImpl extends HttpClient implements Trackable {

    // 核心字段
    private final CookieHandler cookieHandler;
    private final Duration connectTimeout;
    private final Redirect followRedirects;
    private final ProxySelector proxySelector;
    private final Authenticator authenticator;
    private final Version version;
    private final ConnectionPool connections;      // HTTP/1.1 连接池
    private final DelegatingExecutor delegatingExecutor;
    private final SSLContext sslContext;
    private final SSLParameters sslParams;
    private final Thread selmgrThread;             // 选择器管理器线程
    private final SelectorManager selmgr;          // NIO Selector 管理器
    private final FilterFactory filters;           // 请求过滤器链
    private final Http2ClientImpl client2;         // HTTP/2 客户端
    private final Http3ClientImpl client3;         // HTTP/3 客户端 (JDK 26)
    private final AltServicesRegistry registry;    // Alt-Svc 注册表
    private final InetAddress localAddr;           // 本地绑定地址

    // 连接超时配置
    static final long KEEP_ALIVE_TIMEOUT;         // 默认 30 秒
    static final long IDLE_CONNECTION_TIMEOUT_H2;  // HTTP/2 空闲超时
    static final long IDLE_CONNECTION_TIMEOUT_H3;  // HTTP/3 空闲超时

    // SelectorManager: 内部类，管理 NIO Selector 事件循环
    private static final class SelectorManager implements Runnable { ... }

    // DelegatingExecutor: 在选择器线程和用户线程之间调度任务
    static final class DelegatingExecutor implements Executor { ... }
}
```

### 3.4 请求处理流程 (Request Pipeline)

```
HttpClient.send(request, bodyHandler)
    │
    ▼
MultiExchange                   ← 管理重定向和重试
    │
    ▼
Exchange                        ← 单次 HTTP 交换
    │
    ├── AuthenticationFilter     ← 认证处理
    ├── CookieFilter             ← Cookie 管理
    ├── RedirectFilter           ← 重定向检测
    │
    ▼
ExchangeImpl (协议选择)
    ├── Http1Exchange            ← HTTP/1.1
    ├── Stream (Http2Connection) ← HTTP/2
    └── Http3ExchangeImpl        ← HTTP/3 (JDK 26)
```

---

## 4. HTTP/2 实现 (HTTP/2 Implementation)

### Http2Connection (多路复用)

**文件**: `src/java.net.http/share/classes/jdk/internal/net/http/Http2Connection.java`

```java
class Http2Connection implements Closeable {
    // HTTP/2 多路复用: 单个 TCP 连接上多个并发流
    // 每个流由 Stream 对象表示，通过 streamId 标识
    // 支持 HPACK 头部压缩 (RFC 7541)
    // 支持流优先级和流量控制
    // 支持 Server Push (可通过 jdk.httpclient.enablepush 禁用)
}
```

### HPACK 头部压缩

**包**: `jdk/internal/net/http/hpack/`

```
hpack/
├── HPACK.java           # HPACK 入口
├── Encoder.java         # HPACK 编码器
├── Decoder.java         # HPACK 解码器
├── HeaderTable.java     # 动态头部表
├── Huffman.java         # Huffman 编码
├── QuickHuffman.java    # 优化的 Huffman 实现
└── ...                  # 各种 Writer (Indexed, Literal 等)
```

---

## 5. HTTP/3 和 QUIC 实现 (JDK 26)

### 5.1 协议栈架构

```
┌──────────────────────────────────────────────┐
│               HTTP/3 层                        │
│  Http3Connection / Http3Stream                │
│  Http3ExchangeImpl / Http3PushManager         │
│  QPACK 头部压缩                                │
├──────────────────────────────────────────────┤
│               QUIC 传输层                      │
│  QuicConnectionImpl / QuicClient              │
│  流管理 (QuicBidiStream / QuicSenderStream)    │
│  拥塞控制 (Cubic / Reno)                       │
│  丢包恢复 / RTT 估算 / 流量控制                 │
├──────────────────────────────────────────────┤
│               UDP 传输                         │
│  DatagramChannel (NIO)                        │
│  QuicSelector / QuicPacketReceiver            │
│  QuicPacketEncoder / QuicPacketDecoder        │
└──────────────────────────────────────────────┘
```

### 5.2 Http3ClientImpl

**文件**: `src/java.net.http/share/classes/jdk/internal/net/http/Http3ClientImpl.java`

```java
final class Http3ClientImpl implements AutoCloseable {
    // 管理 HTTP/3 连接生命周期
    // 通过 Http3ConnectionPool 复用连接
    // 支持连接恢复 (ConnectionRecovery sealed interface)

    sealed interface ConnectionRecovery
        permits PendingConnection, StreamLimitReached { }
}
```

### 5.3 Http3Connection

**文件**: `src/java.net.http/share/classes/jdk/internal/net/http/Http3Connection.java`

```java
public final class Http3Connection implements AutoCloseable {
    // 封装 QUIC 连接之上的 HTTP/3 语义
    // 管理请求/控制/推送等不同类型的流
    // 内部类 Http3StreamDispatcher 分发对端发起的单向流
    // 空闲连接超时通过 IdleConnectionTimeoutEvent 管理
}
```

### 5.4 QPACK 头部压缩

**包**: `jdk/internal/net/http/qpack/`

```
qpack/
├── QPACK.java              # QPACK 入口
├── Encoder.java            # QPACK 编码器
├── Decoder.java            # QPACK 解码器
├── DynamicTable.java       # 动态表
├── HeadersTable.java       # 头部表
├── StaticTable.java        # 静态表
├── InsertionPolicy.java    # 插入策略
├── readers/                # 解码相关读取器
│   ├── FieldLineIndexedReader.java
│   ├── FieldLineLiteralsReader.java
│   ├── HeaderFrameReader.java
│   └── ...
└── writers/                # 编码相关写入器
    ├── FieldLineIndexedWriter.java
    ├── HeaderFrameWriter.java
    ├── EncoderInstructionsWriter.java
    └── ...
```

### 5.5 QUIC 协议实现

**包**: `jdk/internal/net/http/quic/`

```
quic/
├── QuicClient.java                   # QUIC 客户端入口
├── QuicConnection.java               # QUIC 连接接口
├── QuicConnectionImpl.java           # QUIC 连接实现
├── QuicEndpoint.java                 # QUIC 端点
├── QuicInstance.java                 # QUIC 实例管理
├── QuicSelector.java                 # QUIC 事件选择器 (基于 DatagramChannel)
├── QuicPacketReceiver.java           # 数据包接收器
├── QuicCongestionController.java     # 拥塞控制器接口
├── QuicBaseCongestionController.java # 拥塞控制基类
├── QuicCubicCongestionController.java # CUBIC 拥塞控制算法
├── QuicRenoCongestionController.java  # Reno 拥塞控制算法
├── QuicRttEstimator.java             # RTT 往返时间估算
├── QuicPacer.java                    # 发送速率控制
├── QuicTransportParameters.java      # QUIC 传输参数
├── QuicConnectionIdFactory.java      # 连接 ID 工厂
├── QuicTimerQueue.java               # 定时器队列
├── frames/                           # QUIC 帧 (ACK, CRYPTO, STREAM 等)
├── packets/                          # QUIC 包编解码
│   ├── QuicPacket.java               # 包抽象
│   ├── QuicPacketEncoder.java        # 包编码器
│   ├── QuicPacketDecoder.java        # 包解码器
│   └── QuicPacketNumbers.java        # 包号管理
└── streams/                          # QUIC 流管理
    ├── QuicStream.java               # 流接口
    ├── QuicBidiStream.java           # 双向流接口
    ├── QuicBidiStreamImpl.java       # 双向流实现
    ├── QuicSenderStream.java         # 发送单向流
    ├── QuicReceiverStream.java       # 接收单向流
    ├── QuicConnectionStreams.java     # 连接级流管理
    ├── QuicStreamReader.java         # 流读取器
    └── QuicStreamWriter.java         # 流写入器
```

### 5.6 关键系统属性 (Key System Properties)

| 属性 | 默认值 | 说明 |
|------|--------|------|
| `jdk.httpclient.connectionPoolSize` | 0 (无限) | HTTP/1.1 连接池大小 |
| `jdk.httpclient.keepalive.timeout` | 30 | 空闲连接存活秒数 |
| `jdk.httpclient.keepalive.timeout.h2` | 同上 | HTTP/2 空闲超时 |
| `jdk.httpclient.keepalive.timeout.h3` | 同 h2 | HTTP/3 空闲超时 |
| `jdk.httpclient.maxstreams` | 100 | HTTP/2/3 最大推送流数 |
| `jdk.httpclient.windowsize` | 16MB | HTTP/2 流窗口大小 |
| `jdk.httpclient.connectionWindowSize` | 64MB | HTTP/2 连接窗口大小 |
| `jdk.httpclient.qpack.decoderMaxTableCapacity` | 0 | QPACK 解码器动态表大小 |
| `jdk.httpclient.qpack.encoderTableCapacityLimit` | 4096 | QPACK 编码器动态表上限 |
| `jdk.httpclient.quic.defaultMTU` | 1200 | QUIC 默认 MTU |
| `jdk.httpclient.quic.maxBytesInFlight` | 16MB | QUIC 最大在途字节数 |
| `jdk.httpclient.quic.maxInitialData` | 15MB | QUIC 连接初始流控限制 |
| `jdk.httpclient.quic.maxStreamInitialData` | 6MB | QUIC 流初始流控限制 |
| `jdk.httpclient.quic.maxInitialTimeout` | 30 | QUIC 初始握手超时秒数 |

---

## 6. 使用示例 (Usage Examples)

### 6.1 基本 HTTP 请求 (Basic Request)

```java
HttpClient client = HttpClient.newHttpClient();

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/data"))
    .header("Accept", "application/json")
    .GET()
    .build();

HttpResponse<String> response = client.send(
    request, HttpResponse.BodyHandlers.ofString()
);

System.out.println("Status: " + response.statusCode());
System.out.println("Body: " + response.body());
```

### 6.2 异步请求 (Async Request)

```java
HttpClient client = HttpClient.newHttpClient();

CompletableFuture<HttpResponse<String>> future = client.sendAsync(
    HttpRequest.newBuilder()
        .uri(URI.create("https://api.example.com/data"))
        .build(),
    HttpResponse.BodyHandlers.ofString()
);

future.thenAccept(response -> {
    System.out.println("Status: " + response.statusCode());
    System.out.println("Body: " + response.body());
}).join();
```

### 6.3 HTTP/3 请求 (JDK 26)

```java
// 创建支持 HTTP/3 的客户端
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_3)
    .connectTimeout(Duration.ofSeconds(10))
    .build();

// 使用 HttpOption 控制 HTTP/3 发现模式
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://example.com"))
    .setOption(HttpOption.H3_DISCOVERY, HttpOption.Http3DiscoveryMode.ANY)
    .build();

HttpResponse<String> response = client.send(
    request, HttpResponse.BodyHandlers.ofString()
);

System.out.println("Protocol: " + response.version()); // HTTP_3
```

### 6.4 POST 请求 (POST Request)

```java
String json = """
    {"name": "John", "email": "john@example.com"}
    """;

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/users"))
    .header("Content-Type", "application/json")
    .POST(HttpRequest.BodyPublishers.ofString(json))
    .build();

HttpResponse<String> response = client.send(
    request, HttpResponse.BodyHandlers.ofString()
);
```

### 6.5 WebSocket

```java
HttpClient client = HttpClient.newHttpClient();

WebSocket ws = client.newWebSocketBuilder()
    .buildAsync(URI.create("wss://example.com/ws"), new WebSocket.Listener() {
        @Override
        public void onOpen(WebSocket webSocket) {
            System.out.println("Connected");
            webSocket.request(1);
        }

        @Override
        public CompletionStage<?> onText(WebSocket webSocket,
                CharSequence data, boolean last) {
            System.out.println("Received: " + data);
            webSocket.request(1);
            return null;
        }
    })
    .join();

ws.sendText("Hello!", true);
```

---

## 7. 连接管理 (Connection Management)

### ConnectionPool (HTTP/1.1)

**文件**: `src/java.net.http/share/classes/jdk/internal/net/http/ConnectionPool.java`

```java
final class ConnectionPool {
    // HTTP/1.1 Keep-Alive 连接复用
    // 通过 jdk.httpclient.connectionPoolSize 配置最大连接数
    // 空闲连接超时由 jdk.httpclient.keepalive.timeout 控制
}
```

### Http2Connection (HTTP/2 多路复用)

单个 TCP 连接上并发多个流，每个流独立传输请求/响应。
使用 HPACK 压缩 HTTP 头部，减少传输开销。

### Http3ConnectionPool (HTTP/3)

基于 QUIC 连接复用，QUIC 本身提供多路复用和 0-RTT 恢复。
使用 QPACK 压缩头部 (针对 QUIC 无序传输优化的 HPACK 变体)。

---

## 8. 日志和调试 (Logging and Debugging)

通过 `jdk.httpclient.HttpClient.log` 系统属性启用日志:

```
# 可选值 (逗号分隔):
errors,requests,headers,content,frames,ssl,trace,channel,http3,quic

# frames 子选项: control,data,window,all
# quic 子选项: ack,cc,control,crypto,data,dbb,ping,processed,retransmit,timer,all

# 示例: 调试 QUIC 问题
-Djdk.httpclient.HttpClient.log=quic:control:retransmit
```

---

## 9. 相关链接 (Related Links)

- [java.net.http API 文档](https://download.java.net/java/early_access/jdk26/docs/api/java.net.http/module-summary.html)
- [源码浏览](https://github.com/openjdk/jdk/tree/master/src/java.net.http)
