# 网络编程

> Socket, ServerSocket, HTTP Client, Unix Domain Sockets, 网络编程演进历程

[← 返回主题索引](../)

---

## 1. 快速概览

```
JDK 1.0 ── JDK 1.4 ── JDK 7 ── JDK 11 ── JDK 13/14 ── JDK 16 ── JDK 21 ── JDK 26
   │         │        │        │          │           │        │        │
Socket   NIO     NIO.2    HTTP/2      Socket      Unix     Virtual  HTTP/3
ServerSocket (JSR51)  (JSR203)  Client    Reimpl     Domain   Threads  Client
                              (JEP 321)  (353/373)  Sockets  (JEP    (JEP
                                                    (JEP     444)    517)
                                                     380)
```

### 核心演进

| 版本 | 特性 | JEP | 说明 |
|------|------|-----|------|
| **JDK 1.0** | Socket/ServerSocket | - | TCP 网络基础 |
| **JDK 1.1** | HttpURLConnection | - | HTTP 支持 |
| **JDK 1.4** | NIO | JSR 51 | 非阻塞 I/O, Selector |
| **JDK 7** | NIO.2 | JSR 203 | 异步通道, 文件系统 API |
| **JDK 11** | HTTP Client | JEP 321 | 支持 HTTP/1.1 和 HTTP/2 |
| **JDK 13** | Socket API 重新实现 | JEP 353 | 替换 PlainSocketImpl |
| **JDK 15** | DatagramSocket API 重新实现 | JEP 373 | 替换 PlainDatagramSocketImpl |
| **JDK 16** | Unix Domain Sockets | JEP 380 | SocketChannel/ServerSocketChannel 支持 AF_UNIX |
| **JDK 21** | Virtual Threads | JEP 444 | 轻量级并发, 简化阻塞式网络编程 |
| **JDK 25** | HTTP/3 Client | JEP 517 | 基于 QUIC 的 HTTP/3 支持 (预览) |

---

## 目录

- [TCP 网络编程](#tcp-网络编程)
- [Socket 重新实现 (JDK 13/14)](#socket-重新实现-jdk-1314)
- [HTTP 编程](#http-编程)
- [HTTP Client (JDK 11+)](#http-client-jdk-11)
- [HTTP/3 Client (JDK 26)](#http3-client-jdk-26)
- [Unix Domain Sockets (JDK 16+)](#unix-domain-sockets-jdk-16)
- [NIO 网络编程](#nio-网络编程)
- [最佳实践](#最佳实践)
- [核心贡献者](#核心贡献者)
- [相关链接](#相关链接)

---

## 2. TCP 网络编程

### Socket 客户端

```java
import java.net.*;
import java.io.*;

// TCP 客户端
try (Socket socket = new Socket("localhost", 8080);
     InputStream input = socket.getInputStream();
     OutputStream output = socket.getOutputStream()) {

    // 发送数据
    String request = "Hello, Server!";
    output.write(request.getBytes());

    // 接收响应
    byte[] buffer = new byte[1024];
    int bytesRead = input.read(buffer);
    String response = new String(buffer, 0, bytesRead);
    System.out.println("Server: " + response);
}
```

### ServerSocket 服务端

```java
import java.net.*;
import java.io.*;

// TCP 服务端
try (ServerSocket serverSocket = new ServerSocket(8080)) {
    System.out.println("Server started on port 8080");

    while (true) {
        try (Socket client = serverSocket.accept();
             BufferedReader in = new BufferedReader(
                 new InputStreamReader(client.getInputStream()));
             PrintWriter out = new PrintWriter(
                 client.getOutputStream(), true)) {

            String line;
            while ((line = in.readLine()) != null) {
                System.out.println("Client: " + line);
                out.println("Echo: " + line);
            }
        }
    }
}
```

### Socket 选项

```java
// Socket 配置选项
socket.setSoTimeout(5000);              // 读超时 (ms)
socket.setTcpNoDelay(true);             // 禁用 Nagle 算法
socket.setKeepAlive(true);              // 保持连接
socket.setReuseAddress(true);            // 地址复用
socket.setReceiveBufferSize(8192);       // 接收缓冲区
socket.setSendBufferSize(8192);          // 发送缓冲区

// ServerSocket 选项
serverSocket.setSoTimeout(5000);         // accept 超时
serverSocket.setReuseAddress(true);      // 地址复用
serverSocket.setReceiveBufferSize(8192); // 接收缓冲区
```

---

## 3. Socket 重新实现 (JDK 13/14)

### JEP 353: 重新实现旧版 Socket API (JDK 13)

JDK 13 用全新的 `NioSocketImpl` 替换了 `PlainSocketImpl`：

| 方面 | 旧实现 (PlainSocketImpl) | 新实现 (NioSocketImpl) |
|------|--------------------------|------------------------|
| 代码来源 | JDK 1.0, 混合 Java/C | 纯 Java (基于 NIO) |
| 线程安全 | 依赖平台原生锁 | Java locks |
| 维护性 | 脆弱, 难以维护 | 清晰, 易于维护 |
| 虚拟线程 | 不兼容 | 天然兼容 |

```java
// 对应用程序透明, 无需代码修改
// 可通过系统属性回退到旧实现 (已在后续版本移除):
// -Djdk.net.usePlainSocketImpl=true
```

### JEP 373: 重新实现旧版 DatagramSocket API (JDK 15)

与 JEP 353 类似, 将 `DatagramSocket` 和 `MulticastSocket` 的底层实现替换为基于 NIO 的版本。

---

## 4. HTTP 编程

### HttpURLConnection (JDK 1.1+)

```java
import java.net.*;
import java.io.*;

// GET 请求
URL url = new URL("https://api.example.com/data");
HttpURLConnection conn = (HttpURLConnection) url.openConnection();
conn.setRequestMethod("GET");
conn.setConnectTimeout(5000);
conn.setReadTimeout(5000);

try {
    int responseCode = conn.getResponseCode();
    if (responseCode == HttpURLConnection.HTTP_OK) {
        try (BufferedReader in = new BufferedReader(
                new InputStreamReader(conn.getInputStream()))) {
            String line;
            StringBuilder response = new StringBuilder();
            while ((line = in.readLine()) != null) {
                response.append(line);
            }
            System.out.println(response.toString());
        }
    }
} finally {
    conn.disconnect();
}

// POST 请求 (表单)
URL url = new URL("https://api.example.com/form");
HttpURLConnection conn = (HttpURLConnection) url.openConnection();
conn.setRequestMethod("POST");
conn.setDoOutput(true);
conn.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");

try (OutputStream out = conn.getOutputStream()) {
    String params = "name=John&age=30";
    out.write(params.getBytes());
}

int responseCode = conn.getResponseCode();
```

### URL 和 URI

```java
import java.net.*;

// URL 解析
URL url = new URL("https://user:pass@example.com:8080/path?query=value#fragment");
System.out.println("Protocol: " + url.getProtocol());  // https
System.out.println("Host: " + url.getHost());          // example.com
System.out.println("Port: " + url.getPort());           // 8080
System.out.println("Path: " + url.getPath());           // /path
System.out.println("Query: " + url.getQuery());         // query=value
System.out.println("Ref: " + url.getRef());             // fragment
System.out.println("UserInfo: " + url.getUserInfo());    // user:pass

// URI (JDK 1.4+)
URI uri = new URI("https://example.com/path?query=value");
System.out.println("Path: " + uri.getPath());
System.out.println("Query: " + uri.getQuery());

// URL 编码
String encoded = URLEncoder.encode("Hello World!", "UTF-8");
System.out.println(encoded);  // Hello+World%21

String decoded = URLDecoder.decode(encoded, "UTF-8");
```

---

## 5. HTTP Client (JDK 11+)

**JEP 321: HTTP Client**

### 基础使用

```java
import java.net.URI;
import java.net.http.*;
import java.time.Duration;

// 创建 HTTP Client
HttpClient client = HttpClient.newBuilder()
    .connectTimeout(Duration.ofSeconds(10))
    .version(HttpClient.Version.HTTP_2)
    .build();

// GET 请求
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/data"))
    .timeout(Duration.ofSeconds(5))
    .GET()
    .build();

HttpResponse<String> response = client.send(request,
    HttpResponse.BodyHandlers.ofString());

System.out.println("Status: " + response.statusCode());
System.out.println("Body: " + response.body());
```

### POST 请求

```java
// JSON POST
import java.net.http.*;

String json = "{\"name\":\"John\",\"age\":30}";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/users"))
    .header("Content-Type", "application/json")
    .POST(HttpRequest.BodyPublishers.ofString(json))
    .build();

HttpResponse<String> response = client.send(request,
    HttpResponse.BodyHandlers.ofString());
```

### 异步请求

```java
// 异步 GET
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/data"))
    .GET()
    .build();

client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
    .thenApply(HttpResponse::body)
    .thenAccept(System.out::println)
    .exceptionally(e -> {
        System.err.println("Error: " + e);
        return null;
    });
```

### 文件上传

```java
// 上传文件
Path file = Paths.get("example.txt");
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/upload"))
    .POST(HttpRequest.BodyPublishers.ofFile(file))
    .build();

HttpResponse<String> response = client.send(request,
    HttpResponse.BodyHandlers.ofString());
```

### 流式响应

```java
// 流式处理大响应
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/large-data"))
    .GET()
    .build();

HttpResponse<Stream<String>> response = client.send(request,
    HttpResponse.BodyHandlers.ofLines());

try (Stream<String> lines = response.body()) {
    lines.forEach(System.out::println);
}
```

### WebSocket

```java
import java.net.http.*;
import java.net.URI;

// WebSocket 客户端
WebSocket.Listener listener = new WebSocket.Listener() {
    @Override
    public void onOpen(WebSocket webSocket) {
        System.out.println("Connected!");
        webSocket.request(1); // 接收消息
    }

    @Override
    public CompletionStage<?> onText(WebSocket webSocket, CharSequence data,
                                        boolean last) {
        System.out.println("Received: " + data);
        return WebSocket.Listener.super.onText(webSocket, data, last);
    }

    @Override
    public void onClose(WebSocket webSocket, int statusCode, String reason) {
        System.out.println("Closed: " + reason);
    }
};

HttpClient client = HttpClient.newHttpClient();
WebSocket ws = client.newWebSocketBuilder()
    .buildAsync(URI.create("ws://echo.websocket.org"), listener)
    .join();

// 发送消息
ws.sendText("Hello, WebSocket!", true);

// 关闭
ws.sendClose(WebSocket.NORMAL_CLOSURE, "Goodbye", true);
```

---

## 6. HTTP/3 Client (JDK 26)

**JEP 517: HTTP/3 for the HTTP Client API (Preview)**

JDK 26 为 `java.net.http.HttpClient` 添加 HTTP/3 支持, 基于 QUIC 协议。

### 关键特性

| 特性 | 说明 |
|------|------|
| **QUIC 传输** | 基于 UDP, 减少连接建立延迟 |
| **0-RTT 握手** | 复用已知连接, 首次请求即可发送数据 |
| **多路复用** | 无队头阻塞 (区别于 HTTP/2 的 TCP 层队头阻塞) |
| **连接迁移** | 网络切换时无需重新连接 |

### 使用方式

```java
// HTTP/3 使用与 HTTP/2 相同的 API
// 需要启用预览特性: --enable-preview
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_2)  // 自动协商升级到 HTTP/3
    .connectTimeout(Duration.ofSeconds(10))
    .build();

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/data"))
    .GET()
    .build();

// 如果服务器支持 HTTP/3, 客户端会自动升级
HttpResponse<String> response = client.send(request,
    HttpResponse.BodyHandlers.ofString());

System.out.println("Protocol: " + response.version());  // 可能是 HTTP_3
```

### HTTP 协议演进对比

| 特性 | HTTP/1.1 | HTTP/2 | HTTP/3 |
|------|----------|--------|--------|
| 传输层 | TCP | TCP | QUIC (UDP) |
| 多路复用 | 无 | 有 (TCP 队头阻塞) | 有 (无队头阻塞) |
| 头部压缩 | 无 | HPACK | QPACK |
| 连接建立 | TCP + TLS | TCP + TLS | 0-RTT / 1-RTT |
| JDK 支持 | JDK 1.1+ | JDK 11+ | JDK 26+ (预览) |

---

## 7. Unix Domain Sockets (JDK 16+)

**JEP 380: Unix-Domain Socket Channels**

JDK 16 为 `SocketChannel` 和 `ServerSocketChannel` 添加 Unix 域套接字支持 (AF_UNIX), 适用于同一主机上的进程间通信。

### 优势

| 方面 | TCP Loopback | Unix Domain Socket |
|------|-------------|-------------------|
| 性能 | 经过网络栈 | 绕过网络栈, 更快 |
| 安全 | 需要端口管理 | 文件系统权限控制 |
| 可移植 | 所有平台 | Linux, macOS, Windows 10+ |

### 服务端

```java
import java.net.UnixDomainSocketAddress;
import java.nio.channels.*;
import java.nio.ByteBuffer;
import java.nio.file.Path;

// Unix Domain Socket 服务端
Path socketPath = Path.of("/tmp/my-server.sock");
UnixDomainSocketAddress address = UnixDomainSocketAddress.of(socketPath);

try (ServerSocketChannel server = ServerSocketChannel.open(StandardProtocolFamily.UNIX)) {
    server.bind(address);

    try (SocketChannel client = server.accept()) {
        ByteBuffer buffer = ByteBuffer.allocate(1024);
        client.read(buffer);
        buffer.flip();
        // 处理数据...
    }
} finally {
    Files.deleteIfExists(socketPath);
}
```

### 客户端

```java
// Unix Domain Socket 客户端
Path socketPath = Path.of("/tmp/my-server.sock");
UnixDomainSocketAddress address = UnixDomainSocketAddress.of(socketPath);

try (SocketChannel channel = SocketChannel.open(StandardProtocolFamily.UNIX)) {
    channel.connect(address);

    ByteBuffer buffer = ByteBuffer.wrap("Hello".getBytes());
    channel.write(buffer);
}
```

---

## 8. NIO 网络编程

**JDK 1.4 (JSR 51)**

### Selector 多路复用

```java
import java.nio.*;
import java.nio.channels.*;
import java.net.*;

// NIO Server
Selector selector = Selector.open();
ServerSocketChannel server = ServerSocketChannel.open();
server.bind(new InetSocketAddress(8080));
server.configureBlocking(false);
server.register(selector, SelectionKey.OP_ACCEPT);

while (true) {
    selector.select();  // 阻塞直到有事件
    Set<SelectionKey> keys = selector.selectedKeys();

    for (SelectionKey key : keys) {
        if (key.isAcceptable()) {
            // 新连接
            SocketChannel client = server.accept();
            client.configureBlocking(false);
            client.register(selector, SelectionKey.OP_READ);
        }

        if (key.isReadable()) {
            // 读取数据
            SocketChannel client = (SocketChannel) key.channel();
            ByteBuffer buffer = ByteBuffer.allocate(256);
            int bytesRead = client.read(buffer);

            if (bytesRead == -1) {
                // 连接关闭
                key.cancel();
            } else {
                buffer.flip();
                // 处理数据...
            }
        }
    }
    keys.clear();
}
```

### NIO Client

```java
// NIO Client
SocketChannel client = SocketChannel.open();
client.configureBlocking(false);
client.connect(new InetSocketAddress("localhost", 8080));

// 等待连接完成
while (!client.finishConnect()) {
    // 注册到 Selector...
}

// 读写
ByteBuffer buffer = ByteBuffer.allocate(256);
buffer.put("Hello".getBytes());
buffer.flip();
while (buffer.hasRemaining()) {
    client.write(buffer);
}
```

---

## 9. 最佳实践

### 超时设置

```java
// HTTP Client
HttpClient client = HttpClient.newBuilder()
    .connectTimeout(Duration.ofSeconds(10))
    .build();

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/data"))
    .timeout(Duration.ofSeconds(5))
    .build();

// Socket
socket.setSoTimeout(5000);  // 读超时
```

### 连接池

```java
// HTTP Client 自动管理连接池
HttpClient client = HttpClient.newBuilder()
    .connectTimeout(Duration.ofSeconds(10))
    .executor(Executors.newFixedThreadPool(10))
    .build();
```

### 重试机制

```java
// 使用 HttpClient 的自动重试
HttpClient client = HttpClient.newBuilder()
    .connectTimeout(Duration.ofSeconds(10))
    .version(HttpClient.Version.HTTP_2)
    .followRedirects(HttpClient.Redirect.NORMAL)
    .build();
```

### 虚拟线程并发 (JDK 21+)

```java
// 使用虚拟线程处理大量并发请求
HttpClient client = HttpClient.newHttpClient();

try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    List<HttpRequest> requests = IntStream.range(0, 100)
        .mapToObj(i -> HttpRequest.newBuilder()
            .uri(URI.create("https://api.example.com/item/" + i))
            .GET()
            .build())
        .toList();

    List<CompletableFuture<String>> futures = requests.stream()
        .map(request -> client.sendAsync(request,
            HttpResponse.BodyHandlers.ofString())
            .thenApply(HttpResponse::body))
        .toList();

    CompletableFuture.allOf(futures.toArray(new CompletableFuture[0])).join();
}
```

### 同机进程间通信

```java
// 优先使用 Unix Domain Sockets (JDK 16+) 进行本机 IPC
// 比 TCP loopback 更快, 且无需占用端口
Path socketPath = Path.of("/tmp/app.sock");
UnixDomainSocketAddress addr = UnixDomainSocketAddress.of(socketPath);

try (SocketChannel channel = SocketChannel.open(StandardProtocolFamily.UNIX)) {
    channel.connect(addr);
    // ...
}
```

---

## 10. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 网络 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | [Alan Bateman](/by-contributor/profiles/alan-bateman.md) | 20+ | Oracle | NIO, NIO.2, Unix Domain Sockets (JEP 380), Virtual Threads |
| 2 | [Chris Hegarty](/by-contributor/profiles/chris-hegarty.md) | 25+ | Oracle | HTTP Client (JEP 321), 网络基础 |
| 3 | [Daniel Fuchs](/by-contributor/profiles/daniel-fuchs.md) | 8+ | Oracle | HTTP Client, 网络安全 |
| 4 | Michael McMahon | 10+ | Oracle | Socket 重新实现 (JEP 353/373), HTTP Client |

### 历史贡献者

| 贡献者 | 公司/机构 | 主要贡献 |
|--------|----------|----------|
| **Alan Bateman** | Oracle | NIO.2 (JSR 203), JEP 380 Unix Domain Sockets |
| **Chris Hegarty** | Oracle | HTTP Client API 实现 |
| **Michael McMahon** | Oracle | Socket/DatagramSocket 重新实现 |

---

## 11. 相关链接

### 内部文档

- 网络时间线 - 详细的历史演进
- [I/O 处理](../api/io/) - 文件 I/O
- [并发编程](../concurrency/concurrency/) - 并发基础
- [HTTP 客户端](../concurrency/http/) - HTTP Client 详解

### 外部资源

- [JSR 51: New I/O APIs](https://jcp.org/en/jsr/detail?id=51)
- [JSR 203: More New I/O APIs](https://jcp.org/en/jsr/detail?id=203)
- [JEP 321: HTTP Client](/jeps/network/jep-321.md)
- [JEP 353: Reimplement the Legacy Socket API](https://openjdk.org/jeps/353)
- [JEP 373: Reimplement the Legacy DatagramSocket API](https://openjdk.org/jeps/373)
- [JEP 380: Unix-Domain Socket Channels](https://openjdk.org/jeps/380)
- [JEP 517: HTTP/3 for the HTTP Client API (Preview)](https://openjdk.org/jeps/517)
- [Java Networking Tutorial](https://docs.oracle.com/javase/tutorial/networking/)
- [WebSocket RFC](https://tools.ietf.org/html/rfc6455)

---

**最后更新**: 2026-03-22
