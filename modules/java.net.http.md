# java.net.http 模块分析

> HTTP Client API，支持 HTTP/1.1、HTTP/2 和 HTTP/3

---

## 1. 模块概述

`java.net.http` 模块提供了现代化的 HTTP 客户端 API，支持同步和异步请求。

### 模块定义

**文件**: `src/java.net.http/share/classes/module-info.java`

```java
module java.net.http {
    exports java.net.http;

    requires transitive java.base;
    requires transitive java.logging;

    uses java.net.http.spi.HttpClientProvider;
}
```

---

## 2. 包结构

```
java.net.http/
├── HttpClient.java           # HTTP 客户端
├── HttpRequest.java          # HTTP 请求
├── HttpResponse.java         # HTTP 响应
├── WebSocket.java            # WebSocket 客户端
├── HttpHeaders.java          # HTTP 头
├── HttpTimeoutException.java # 超时异常
└── spi/
    └── HttpClientProvider.java  # 服务提供者接口
```

---

## 3. 核心类分析

### HttpClient

**文件**: `src/java.net.http/share/classes/java/net/http/HttpClient.java`

```java
public abstract class HttpClient implements AutoCloseable {

    // HTTP 版本
    public enum Version {
        HTTP_1_1,
        HTTP_2,
        HTTP_3,        // JDK 26 新增
        HTTP_3_AUTO    // JDK 26 新增: 自动协商
    }

    // 获取默认客户端
    public static HttpClient newHttpClient() {
        return HttpClient.newBuilder().build();
    }

    // 构建器
    public static Builder newBuilder() {
        return new HttpClientBuilderImpl();
    }

    // 发送同步请求
    public abstract <T> HttpResponse<T> send(
        HttpRequest request,
        HttpResponse.BodyHandler<T> responseBodyHandler
    ) throws IOException, InterruptedException;

    // 发送异步请求
    public abstract <T> CompletableFuture<HttpResponse<T>> sendAsync(
        HttpRequest request,
        HttpResponse.BodyHandler<T> responseBodyHandler
    );

    // 发送异步请求 (带推送承诺处理器)
    public abstract <T> CompletableFuture<HttpResponse<T>> sendAsync(
        HttpRequest request,
        HttpResponse.BodyHandler<T> responseBodyHandler,
        HttpResponse.PushPromiseHandler<T> pushPromiseHandler
    );

    // 构建器接口
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
        HttpClient build();
    }
}
```

### HttpClientImpl

**文件**: `src/java.net.http/share/classes/jdk/internal/net/http/HttpClientImpl.java`

```java
final class HttpClientImpl extends HttpClient {

    // 连接池
    private final ConnectionPool connections;

    // 选择器管理器 (JDK 26: 虚拟线程)
    private final Thread selectorThread;

    // HTTP/2 客户端
    private final Http2ClientImpl http2Client;

    // HTTP/3 客户端 (JDK 26 新增)
    private final Http3ClientImpl http3Client;

    // 构造函数
    HttpClientImpl(HttpClientBuilderImpl builder) {
        // 初始化连接池
        this.connections = new ConnectionPool();

        // 启动选择器线程 (JDK 26: 虚拟线程)
        this.selectorThread = Thread.ofVirtual()
            .name("HttpClient-Selector-" + id)
            .unstarted(this::runSelector);
        this.selectorThread.start();

        // 初始化 HTTP/2 客户端
        this.http2Client = new Http2ClientImpl(this);

        // 初始化 HTTP/3 客户端 (JDK 26)
        if (version == Version.HTTP_3 || version == Version.HTTP_3_AUTO) {
            this.http3Client = new Http3ClientImpl(this);
        } else {
            this.http3Client = null;
        }
    }

    // 发送请求
    @Override
    public <T> HttpResponse<T> send(
        HttpRequest request,
        HttpResponse.BodyHandler<T> responseHandler
    ) throws IOException, InterruptedException {

        // 选择协议
        Version ver = selectVersion(request);

        switch (ver) {
            case HTTP_1_1:
                return sendHttp1(request, responseHandler);
            case HTTP_2:
                return http2Client.send(request, responseHandler);
            case HTTP_3:
            case HTTP_3_AUTO:
                return http3Client.send(request, responseHandler);
            default:
                throw new AssertionError();
        }
    }

    // 选择 HTTP 版本
    private Version selectVersion(HttpRequest request) {
        if (version == Version.HTTP_3_AUTO) {
            // 检查服务器是否支持 HTTP/3
            if (http3Client.isAvailable(request.uri())) {
                return Version.HTTP_3;
            } else if (http2Client.isAvailable(request.uri())) {
                return Version.HTTP_2;
            } else {
                return Version.HTTP_1_1;
            }
        }
        return version;
    }
}
```

### Http3ClientImpl (JDK 26 新增)

**文件**: `src/java.net.http/share/classes/jdk/internal/net/http/Http3ClientImpl.java`

```java
final class Http3ClientImpl {

    // QUIC 连接管理
    private final QuicConnectionManager connectionManager;

    // 拥塞控制器 (JDK 26: CUBIC)
    private final QuicCongestionController congestionController;

    Http3ClientImpl(HttpClientImpl client) {
        this.connectionManager = new QuicConnectionManager(client);

        // 使用 CUBIC 拥塞控制
        this.congestionController = new QuicCubicCongestionController();
    }

    // 发送 HTTP/3 请求
    <T> HttpResponse<T> send(
        HttpRequest request,
        HttpResponse.BodyHandler<T> responseHandler
    ) throws IOException, InterruptedException {

        // 获取或创建 QUIC 连接
        QuicConnection conn = connectionManager.getConnection(request.uri());

        // 创建 HTTP/3 流
        Http3Stream stream = conn.createStream();

        // 发送请求头
        stream.sendHeaders(request.headers());

        // 发送请求体
        if (request.bodyPublisher() != null) {
            stream.sendBody(request.bodyPublisher());
        }

        // 接收响应
        Http3Response response = stream.receiveResponse();

        // 处理响应体
        T body = responseHandler.apply(
            response.statusCode(),
            response.headers(),
            response.bodyStream()
        );

        return new HttpResponseImpl<>(
            request,
            response.statusCode(),
            response.headers(),
            body,
            HttpClient.Version.HTTP_3
        );
    }
}
```

---

## 4. HTTP/3 实现 (JEP 517)

### QUIC 协议栈

```
┌─────────────────────────────────────────────────────────┐
│                    HTTP/3 层                            │
│  QPACK (头部压缩) | 请求/响应处理                        │
├─────────────────────────────────────────────────────────┤
│                    QUIC 传输层                          │
│  流管理 | 拥塞控制 | 流量控制                            │
├─────────────────────────────────────────────────────────┤
│                    UDP 传输                             │
│  数据报发送/接收                                        │
└─────────────────────────────────────────────────────────┘
```

### CUBIC 拥塞控制

**文件**: `src/java.net.http/share/classes/jdk/internal/net/http/QuicCubicCongestionController.java`

```java
class QuicCubicCongestionController extends QuicBaseCongestionController {

    // CUBIC 参数
    private static final double C = 0.4;     // CUBIC 常数
    private static final double BETA = 0.7;  // 乘法减少因子

    private long wMax;          // 上次拥塞时的窗口大小
    private long k;             // 窗口增长到 wMax 的时间
    private long epochStart;    // 拥塞事件开始时间

    @Override
    public long getCwnd(long rtt) {
        long t = currentTime() - epochStart;

        // CUBIC 窗口计算: W(t) = C(t - k)^3 + wMax
        double w = C * Math.pow((t - k) / 1000.0, 3) + wMax;

        // TCP 友好性调整
        double wTcp = getTcpFriendlyWindow(t, rtt);

        return (long) Math.max(w, wTcp);
    }

    @Override
    public void onPacketLoss() {
        // 乘法减少
        wMax = getCwnd(0);
        k = Math.cbrt(wMax * BETA / C);
        epochStart = currentTime();
    }
}
```

---

## 5. 使用示例

### 基本 HTTP 请求

```java
// 创建客户端
HttpClient client = HttpClient.newHttpClient();

// 创建请求
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/data"))
    .header("Accept", "application/json")
    .GET()
    .build();

// 发送请求
HttpResponse<String> response = client.send(
    request,
    HttpResponse.BodyHandlers.ofString()
);

System.out.println("Status: " + response.statusCode());
System.out.println("Body: " + response.body());
```

### HTTP/3 请求

```java
// 创建支持 HTTP/3 的客户端
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_3_AUTO)  // 自动协商
    .connectTimeout(Duration.ofSeconds(10))
    .build();

// 发送请求
HttpResponse<String> response = client.send(
    HttpRequest.newBuilder()
        .uri(URI.create("https://cloudflare.com"))
        .build(),
    HttpResponse.BodyHandlers.ofString()
);

// 检查使用的协议
System.out.println("Protocol: " + response.version());
```

### 异步请求

```java
HttpClient client = HttpClient.newHttpClient();

// 异步发送
CompletableFuture<HttpResponse<String>> future = client.sendAsync(
    HttpRequest.newBuilder()
        .uri(URI.create("https://api.example.com/data"))
        .build(),
    HttpResponse.BodyHandlers.ofString()
);

// 处理响应
future.thenAccept(response -> {
    System.out.println("Status: " + response.statusCode());
    System.out.println("Body: " + response.body());
});

// 等待完成
future.join();
```

### POST 请求

```java
// JSON 请求体
String json = "{\"name\":\"John\",\"email\":\"john@example.com\"}";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/users"))
    .header("Content-Type", "application/json")
    .POST(HttpRequest.BodyPublishers.ofString(json))
    .build();

HttpResponse<String> response = client.send(
    request,
    HttpResponse.BodyHandlers.ofString()
);
```

### WebSocket

```java
HttpClient client = HttpClient.newHttpClient();

WebSocket webSocket = client.newWebSocketBuilder()
    .buildAsync(URI.create("wss://example.com/ws"), new WebSocket.Listener() {
        @Override
        public void onOpen(WebSocket webSocket) {
            System.out.println("WebSocket opened");
            webSocket.request(1);
        }

        @Override
        public CompletionStage<?> onText(WebSocket webSocket, CharSequence data, boolean last) {
            System.out.println("Received: " + data);
            webSocket.request(1);
            return null;
        }

        @Override
        public CompletionStage<?> onClose(WebSocket webSocket, int statusCode, String reason) {
            System.out.println("WebSocket closed: " + reason);
            return null;
        }
    })
    .join();

// 发送消息
webSocket.sendText("Hello, WebSocket!", true);
```

---

## 6. 性能特性

### 连接池

```java
// 连接池配置
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_2)
    .connectTimeout(Duration.ofSeconds(10))
    .build();

// 连接池自动管理
// - HTTP/1.1: Keep-Alive 连接复用
// - HTTP/2: 多路复用
// - HTTP/3: QUIC 连接复用
```

### 虚拟线程支持

```java
// JDK 26: HttpClient 内部使用虚拟线程
// SelectorManager 线程现在是虚拟线程

// 在虚拟线程中使用 HttpClient
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    List<Future<String>> futures = new ArrayList<>();

    for (int i = 0; i < 1000; i++) {
        final int id = i;
        futures.add(executor.submit(() -> {
            HttpResponse<String> response = client.send(
                HttpRequest.newBuilder()
                    .uri(URI.create("https://api.example.com/" + id))
                    .build(),
                HttpResponse.BodyHandlers.ofString()
            );
            return response.body();
        }));
    }

    // 等待所有请求完成
    for (Future<String> future : futures) {
        System.out.println(future.get());
    }
}
```

---

## 7. 相关链接

- [java.net.http API 文档](https://download.java.net/java/early_access/jdk26/docs/api/java.net.http/module-summary.html)
- [JEP 517: HTTP/3](../jeps/jep-517.md)
- [源码浏览](https://github.com/openjdk/jdk/tree/master/src/java.net.http)