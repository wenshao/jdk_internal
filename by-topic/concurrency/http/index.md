# HTTP 客户端

> 从 HttpURLConnection 到 HTTP/3 的完整演进历程

[← 返回并发网络](../)

---

## 快速概览

```
JDK 1.0 ── JDK 5 ── JDK 9 ── JDK 11 ── JDK 16 ── JDK 21 ── JDK 22 ── JDK 26
   │         │        │        │        │        │        │        │
HttpURL   HTTP    HTTP    HTTP    HTTP/2  WebSocket  多项    HTTP/3
Connection URLConn Client  Client   支持      支持    优化    (预览)
(旧API)   (改进)  (孵化)  (标准)  (ALPN)   (RFC 6455)  (预览)  JEP 517
```

### 协议演进

| 版本 | 协议 | 特性 | 状态 |
|------|------|------|------|
| **JDK 1.0** | HTTP/1.0 | 基础支持 | 已过时 |
| **JDK 1.1** | HTTP/1.1 | 持久连接 | 已过时 |
| **JDK 9** | HTTP/2 | 多路复用 (孵化) | 孵化 |
| **JDK 11** | HTTP/2 | 标准化 | 标准 |
| **JDK 20** | HTTP/2 | 推送支持 | 标准 |
| **JDK 26** | HTTP/3 | 基于 QUIC (预览) | 预览 |

### API 演进

| API | 首发版本 | 设计目标 | 当前状态 |
|-----|----------|----------|----------|
| `HttpURLConnection` | JDK 1.0 | 简单 HTTP | 不推荐 |
| `Apache HttpClient` | 第三方 | 功能丰富 | 外部 |
| `OkHttp` | 第三方 | 高性能 | 外部 |
| `java.net.http.HttpClient` | JDK 11 | 现代 HTTP | 推荐 |

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### HTTP Client 团队 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Daniel Fuchs | 95 | Oracle | HTTP Client, HTTP/3 |
| 2 | Michael McMahon | 19 | Oracle | HTTP Client (JEP 321) |
| 3 | Jaikiran Pai | 18 | Red Hat/Oracle | HTTP/2, 连接池 |
| 4 | Volkan Yazıcı | 17 | Oracle | HTTP/3, WebSocket |
| 5 | Chris Hegarty | 17 | Oracle | HTTP Client 基础 |
| 6 | Daniel Jeliński | 16 | Oracle | HTTP/2, 连接池 |
| 7 | Conor Cleary | 14 | Oracle | HTTP/3 (QUIC) |

---

## HttpURLConnection (旧 API)

### 基础用法

```java
// GET 请求
URL url = new URL("https://example.com/api");
HttpURLConnection conn = (HttpURLConnection) url.openConnection();
conn.setRequestMethod("GET");

try {
    BufferedReader br = new BufferedReader(
        new InputStreamReader(conn.getInputStream()));
    String line;
    while ((line = br.readLine()) != null) {
        System.out.println(line);
    }
} finally {
    conn.disconnect();
}
```

### POST 请求

```java
URL url = new URL("https://example.com/api");
HttpURLConnection conn = (HttpURLConnection) url.openConnection();
conn.setRequestMethod("POST");
conn.setDoOutput(true);
conn.setRequestProperty("Content-Type", "application/json");

try (OutputStream os = conn.getOutputStream()) {
    byte[] input = "{\"key\":\"value\"}".getBytes(StandardCharsets.UTF_8);
    os.write(input);
}
```

### 问题

1. **阻塞式**: 同步 I/O，不适合高并发
2. **API 复杂**: 连接管理繁琐
3. **HTTP/2 不支持**: 无法使用现代协议
4. **连接池困难**: 需要手动管理

---

## HttpClient (JDK 11+)

### JEP 321: HTTP Client

**标准化**: JDK 11 (JEP 321)

**设计目标**:
- HTTP/2 支持
- WebSocket 支持
- 异步非阻塞
- 流式处理
- 响应式集成

### 基础用法

```java
import java.net.http.*;
import java.net.URI;

// 创建客户端
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_2)
    .connectTimeout(Duration.ofSeconds(10))
    .build();

// GET 请求
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://example.com/api"))
    .GET()
    .build();

HttpResponse<String> response = client.send(request,
    HttpResponse.BodyHandlers.ofString());

System.out.println(response.statusCode());
System.out.println(response.body());
```

### POST 请求

```java
// JSON POST
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://example.com/api"))
    .header("Content-Type", "application/json")
    .POST(HttpRequest.BodyPublishers.ofString(
        "{\"key\":\"value\"}"))
    .build();

HttpResponse<String> response = client.send(request,
    HttpResponse.BodyHandlers.ofString());
```

### 异步请求

```java
// 异步发送
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://example.com/api"))
    .build();

CompletableFuture<HttpResponse<String>> future =
    client.sendAsync(request, HttpResponse.BodyHandlers.ofString());

future.thenAccept(response -> {
    System.out.println(response.statusCode());
    System.out.println(response.body());
});
```

### 流式处理

```java
// 流式响应
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://example.com/large-data"))
    .build();

HttpResponse<Stream<String>> response = client.send(request,
    HttpResponse.BodyHandlers.ofLines());

response.body().forEach(System.out::println);
```

---

## HTTP/2 支持

### 多路复用

```java
// HTTP/2 自动多路复用
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_2)  // 强制 HTTP/2
    .build();

// 多个请求共享连接
List<HttpRequest> requests = List.of(
    HttpRequest.newBuilder()
        .uri(URI.create("https://example.com/api/1"))
        .build(),
    HttpRequest.newBuilder()
        .uri(URI.create("https://example.com/api/2"))
        .build()
);

// 并发执行，共享 TCP 连接
List<CompletableFuture<String>> futures = requests.stream()
    .map(req -> client.sendAsync(req,
        HttpResponse.BodyHandlers.ofString())
        .thenApply(HttpResponse::body))
    .toList();
```

### HTTP/2 推送

```java
// 服务器推送 (JDK 20+)
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_2)
    .build();

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://example.com/api"))
    .build();

// 接收推送的额外资源
HttpResponse<String> response = client.send(request,
    HttpResponse.BodyHandlers.ofString());

// 检查推送的流
response.pushPromises().forEach(pushPromise -> {
    System.out.println("Pushed: " + pushPromise.requestedUri());
});
```

---

## WebSocket 支持

### 基础用法

```java
import java.net.http.*;
import java.net.URI;

HttpClient client = HttpClient.newHttpClient();

WebSocket ws = client.newWebSocketBuilder()
    .buildAsync(URI.create("wss://example.com/ws"),
        new WebSocket.Listener() {
            @Override
            public void onOpen(WebSocket ws) {
                System.out.println("Connected");
                ws.request(1);  // 请求更多消息
            }

            @Override
            public CompletionStage<?> onText(
                    WebSocket ws,
                    CharSequence data,
                    boolean last) {
                System.out.println("Received: " + data);
                ws.request(1);  // 请求更多消息
                return null;
            }

            @Override
            public void onClose(WebSocket ws,
                               int statusCode,
                               String reason) {
                System.out.println("Closed: " + reason);
            }
        })
    .join();

// 发送消息
ws.sendText("Hello", true);
ws.sendClose(NORMAL_CLOSURE, "Goodbye");
```

---

## HTTP/3 (JDK 26+)

### JEP 517: HTTP/3 Client

**状态**: 预览 (JDK 26)

**特性**:
- 基于 QUIC 协议
- UDP 传输
- 连接迁移支持
- 更好的网络切换

### 使用 HTTP/3

```java
// HTTP/3 (预览)
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_3)  // JDK 26+
    .build();

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://example.com/api"))
    .build();

HttpResponse<String> response = client.send(request,
    HttpResponse.BodyHandlers.ofString());
```

---

## 配置选项

### 超时设置

```java
HttpClient client = HttpClient.newBuilder()
    .connectTimeout(Duration.ofSeconds(10))
    .build();

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://example.com/api"))
    .timeout(Duration.ofSeconds(30))  // 请求超时
    .build();
```

### 重定向策略

```java
HttpClient client = HttpClient.newBuilder()
    .followRedirects(HttpClient.Redirect.NORMAL)  // 自动重定向
    // .followRedirects(HttpClient.Redirect.NEVER)  // 不重定向
    .build();
```

### 认证

```java
// Basic 认证
HttpClient client = HttpClient.newBuilder()
    .authenticator(new Authenticator() {
        @Override
        protected PasswordAuthentication getPasswordAuthentication() {
            return new PasswordAuthentication(
                "username",
                "password".toCharArray());
        }
    })
    .build();
```

### 连接池

```java
// 默认连接池配置
HttpClient client = HttpClient.newBuilder()
    .executor(Executors.newFixedThreadPool(10))  // 自定义线程池
    .build();
```

---

## Body Handler 和 Publisher

### Body Handlers

```java
// String
HttpResponse<String> response1 = client.send(request,
    HttpResponse.BodyHandlers.ofString());

// byte[]
HttpResponse<byte[]> response2 = client.send(request,
    HttpResponse.BodyHandlers.ofByteArray());

// File
HttpResponse<Path> response3 = client.send(request,
    HttpResponse.BodyHandlers.ofFile(Paths.get("output.txt")));

// InputStream
HttpResponse<InputStream> response4 = client.send(request,
    HttpResponse.BodyHandlers.ofInputStream());

// 自定义
HttpResponse<String> response5 = client.send(request,
    HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
```

### Body Publishers

```java
// String
HttpRequest.BodyPublishers.ofString("Hello")

// byte[]
HttpRequest.BodyPublishers.ofByteArray(data)

// File
HttpRequest.BodyPublishers.ofFile(Paths.get("input.txt"))

// InputStream
HttpRequest.BodyPublishers.ofInputStream(() -> inputStream)

// 表单
HttpRequest.BodyPublishers.ofString(
    "key1=value1&key2=value2")

// Multipart
HttpRequest.BodyPublishers.ofByteArray(
    ("--boundary\r\n" +
     "Content-Disposition: form-data; name=\"file\"; filename=\"test.txt\"\r\n" +
     "\r\n" +
     "content\r\n" +
     "--boundary--\r\n").getBytes())
```

---

## 性能优化

### 连接复用

```java
// 单例 HttpClient
private static final HttpClient CLIENT = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_2)
    .connectTimeout(Duration.ofSeconds(10))
    .build();

// 所有请求共享连接池
public HttpResponse<String> get(String url) {
    HttpRequest request = HttpRequest.newBuilder()
        .uri(URI.create(url))
        .build();
    return CLIENT.send(request,
        HttpResponse.BodyHandlers.ofString());
}
```

### 异步批处理

```java
List<String> urls = List.of(
    "https://example.com/api/1",
    "https://example.com/api/2",
    "https://example.com/api/3"
);

List<CompletableFuture<HttpResponse<String>>> futures = urls.stream()
    .map(url -> HttpRequest.newBuilder()
        .uri(URI.create(url))
        .build())
    .map(req -> client.sendAsync(req,
        HttpResponse.BodyHandlers.ofString()))
    .toList();

// 等待所有完成
CompletableFuture.allOf(futures.toArray(new CompletableFuture[0])).join();
```

---

## 错误处理

### 超时异常

```java
try {
    HttpResponse<String> response = client.send(request,
        HttpResponse.BodyHandlers.ofString());
} catch (HttpTimeoutException e) {
    // 超时处理
    System.err.println("Request timeout");
} catch (IOException e) {
    // I/O 错误
    System.err.println("I/O error: " + e.getMessage());
} catch (InterruptedException e) {
    // 中断
    Thread.currentThread().interrupt();
}
```

### HTTP 错误

```java
HttpResponse<String> response = client.send(request,
    HttpResponse.BodyHandlers.ofString());

if (response.statusCode() >= 400) {
    throw new RuntimeException("HTTP error: " + response.statusCode());
}
```

---

## 对比其他客户端

### 与 OkHttp 对比

| 特性 | HttpClient | OkHttp |
|------|-----------|--------|
| HTTP/2 | 支持 | 支持 |
| WebSocket | 支持 | 支持 |
| 异步 | 支持 | 支持 |
| 拦截器 | 无 | 支持 |
| 依赖 | JDK 内置 | 外部库 |

### 迁移建议

```java
// OkHttp
OkHttpClient client = new OkHttpClient();
Request request = new Request.Builder()
    .url("https://example.com/api")
    .build();
Response response = client.newCall(request).execute();

// HttpClient (迁移目标)
HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://example.com/api"))
    .build();
HttpResponse<String> response = client.send(request,
    HttpResponse.BodyHandlers.ofString());
```

---

## 重要 PR 分析

### HTTP/3 实现

#### JEP 517: HTTP/3 Client

> **负责人**: Daniel Fuchs, Volkan Yazıcı, Conor Cleary
> **状态**: JDK 26 预览
> **影响**: ⭐⭐⭐⭐⭐ 网络性能革命性提升

**关键特性**:
- 基于 QUIC 协议 (UDP 传输)
- 连接迁移支持
- 更好的网络切换
- 队止队头阻塞

**性能优势**:
- 连接建立: -50% 延迟
- 网络切换: 0ms 中断 (vs TCP 数秒)
- 丢包恢复: 快 3-4 倍

```java
// HTTP/3 使用示例
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_3)
    .build();

// 自动使用 QUIC 传输
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://example.com/api"))
    .build();
```

→ [JEP 517](https://openjdk.org/jeps/517)

### HTTP/2 优化

#### 连接池复用优化

> **贡献者**: Jaikiran Pai, Daniel Jeliński
> **影响**: ⭐⭐⭐ 多路复用性能提升

**优化点**:
- 连接池智能管理
- HTTP/2 流复用
- 并发请求优化

**适用场景**:
- 高并发 API 调用
- 微服务间通信
- gRPC 服务

### WebSocket 增强

#### WebSocket 稳定性改进

> **贡献者**: Volkan Yazıcı
> **影响**: ⭐⭐⭐ 生产就绪度提升

**改进内容**:
- 自动重连机制
- Ping/Pong 心跳
- 大消息分片处理

```java
WebSocket ws = client.newWebSocketBuilder()
    .buildAsync(URI.create("wss://example.com/ws"),
        new WebSocket.Listener() {
            @Override
            public void onOpen(WebSocket ws) {
                // 连接建立
                ws.request(1);
            }

            @Override
            public void onClose(WebSocket ws, int statusCode, String reason) {
                // 连接关闭
            }
        })
    .join();
```

---

## 性能优化最佳实践

### 连接池管理

```java
// ✅ 推荐：单例 HttpClient
private static final HttpClient CLIENT = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_2)
    .connectTimeout(Duration.ofSeconds(10))
    .executor(Executors.newVirtualThreadPerTaskExecutor())  // JDK 21+
    .build();

// ❌ 避免：每次请求创建新客户端
public HttpResponse<String> get(String url) throws Exception {
    HttpClient client = HttpClient.newHttpClient();  // 每次创建，浪费资源
    // ...
}
```

### HTTP/2 多路复用

```java
// ✅ 推荐：利用 HTTP/2 多路复用
List<CompletableFuture<HttpResponse<String>>> futures = urls.stream()
    .map(url -> HttpRequest.newBuilder()
        .uri(URI.create(url))
        .build())
    .map(req -> CLIENT.sendAsync(req,
        HttpResponse.BodyHandlers.ofString()))
    .toList();

// 所有请求共享单个 TCP 连接
CompletableFuture.allOf(futures.toArray(new CompletableFuture[0])).join();
```

### 虚拟线程 + HTTP Client

```java
// ✅ 推荐：虚拟线程执行 HTTP 请求 (JDK 21+)
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (String url : urls) {
        executor.submit(() -> {
            HttpResponse<String> response = CLIENT.send(
                HttpRequest.newBuilder(URI.create(url)).build(),
                HttpResponse.BodyHandlers.ofString()
            );
            // 处理响应
        });
    }
}
```

---

## 相关链接

### 本地文档

- [并发编程](../concurrency/) - 线程、异步
- [网络编程](../network/) - Socket、NIO

### 外部参考

**JEP 文档:**
- [JEP 321: HTTP Client](https://openjdk.org/jeps/321) - 标准化
- [JEP 517: HTTP/3 Client](https://openjdk.org/jeps/517) - HTTP/3 预览

**RFC 文档:**
- [RFC 9114: HTTP/3](https://datatracker.ietf.org/doc/html/rfc9114)
- [RFC 9000: QUIC](https://datatracker.ietf.org/doc/html/rfc9000)
- [RFC 6455: WebSocket](https://datatracker.ietf.org/doc/html/rfc6455)

**技术博客:**
- [New HTTP Client](https://openjdk.org/groups/net/httpclient/intro.html)
- [HTTP/2 Support](https://inside.java/2021/07/13/http2/)
