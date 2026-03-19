# HTTP 客户端演进时间线

从 HttpURLConnection 到 HTTP/3 的演进历程。

---

## 时间线概览

```
JDK 1.0 ──── JDK 9 ──── JDK 11 ──── JDK 16 ──── JDK 22 ──── JDK 26
 │             │             │             │             │             │
HttpURL       HTTP Client   HTTP Client   HTTP/2       多项改进      HTTP/3
Connection    (孵化器)      (标准)        支持          连接复用       (预览)
(旧 API)      JEP 110       JEP 321                    优化          JEP 517
```

---

## JDK 1.0 - HttpURLConnection

### 特点

- 同步阻塞 API
- 支持 HTTP/1.0 和 HTTP/1.1
- 连接池管理复杂
- 位于 `java.net` 包

```java
URL url = new URL("https://example.com");
HttpURLConnection conn = (HttpURLConnection) url.openConnection();
conn.setRequestMethod("GET");
conn.setConnectTimeout(5000);
conn.setReadTimeout(5000);

try (BufferedReader br = new BufferedReader(
        new InputStreamReader(conn.getInputStream()))) {
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
HttpURLConnection conn = (HttpURLConnection) url.openConnection();
conn.setRequestMethod("POST");
conn.setDoOutput(true);
conn.setRequestProperty("Content-Type", "application/json");

try (OutputStream os = conn.getOutputStream()) {
    byte[] input = json.getBytes(StandardCharsets.UTF_8);
    os.write(input, 0, input.length);
}
```

### 问题

- API 设计陈旧，不符合现代编程风格
- 不支持 HTTP/2
- 超时配置复杂
- 异步请求困难
- 连接池需要手动管理

---

## JDK 9 - HTTP Client (孵化器) - JEP 110

### 特点

- 位于 `jdk.incubator.httpclient` 包
- 同步 + 异步 API
- HTTP/2 支持
- WebSocket 支持
- 响应式流

```java
// JDK 9 使用模块
module com.example {
    requires jdk.incubator.httpclient;
}

// 使用孵化器 API
HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://example.com"))
    .build();
HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
```

---

## JDK 11 - HTTP Client (标准) - JEP 321

### 变化

- 从 `jdk.incubator.httpclient` 移至 `java.net.http`
- 标准化完成
- 成为推荐使用的 HTTP 客户端

### 模块声明

```java
module com.example {
    requires java.net.http;
}
```

### 同步请求

```java
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_2)
    .connectTimeout(Duration.ofSeconds(10))
    .build();

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/data"))
    .header("Authorization", "Bearer token")
    .GET()
    .build();

HttpResponse<String> response = client.send(request,
    HttpResponse.BodyHandlers.ofString());

System.out.println("Status: " + response.statusCode());
System.out.println("Body: " + response.body());
```

### 异步请求

```java
CompletableFuture<HttpResponse<String>> future =
    client.sendAsync(request, HttpResponse.BodyHandlers.ofString());

future.thenApply(HttpResponse::body)
    .thenAccept(this::process)
    .exceptionally(e -> {
        log.error("Request failed", e);
        return null;
    });
```

### POST JSON

```java
String json = """
    {
        "name": "John",
        "age": 30
    }
    """;

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/users"))
    .header("Content-Type", "application/json")
    .POST(HttpRequest.BodyPublishers.ofString(json))
    .build();
```

### 流式处理

```java`
HttpResponse<Stream<String>> response = client.send(request,
    HttpResponse.BodyHandlers.ofLines());

response.body().forEach(line -> processLine(line));
```

---

## JDK 16 - HTTP/2 支持

### 特性

- 自动协议协商
- 多路复用
- 服务器推送

```java
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_2)
    .build();

// 自动使用 HTTP/2
// 如果服务器不支持 HTTP/2，自动降级到 HTTP/1.1
HttpResponse<String> response = client.send(request, ...);
System.out.println("Version: " + response.version());  // HTTP_2
```

### HTTP/2 优势

| 特性 | HTTP/1.1 | HTTP/2 |
|------|----------|--------|
| 连接数 | 每个请求一个 | 多路复用 |
| 头部压缩 | 无 | HPACK |
| 服务器推送 | 不支持 | 支持 |
| 二进制协议 | 文本 | 二进制 |

---

## JDK 21 - HTTP Client 正式版

### 变化

- 完全稳定，无预览特性
- 性能优化
- 更好的错误处理

---

## JDK 22-23 - 连接复用优化

### 改进

- HTTP/2 连接复用改进
- 连接池优化
- 更好的并发性能

---

## JDK 26 - HTTP/3 支持 (预览) - JEP 517

### 特性

- 基于 QUIC 协议
- 0-RTT 连接恢复
- 内置拥塞控制
- 无队头阻塞

```java
// 启用 HTTP/3
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_3)
    .connectTimeout(Duration.ofSeconds(10))
    .build();

// 自动协商
HttpClient autoClient = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_3_AUTO)  // HTTP/3 > HTTP/2 > HTTP/1.1
    .build();

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://cloudflare.com/"))
    .build();

HttpResponse<String> response = client.send(request,
    HttpResponse.BodyHandlers.ofString());

System.out.println("Version: " + response.version());  // HTTP_3
```

### HTTP/3 vs HTTP/2

| 特性 | HTTP/2 | HTTP/3 |
|------|--------|--------|
| 传输层 | TCP | QUIC (UDP) |
| 队头阻塞 | 有 | 无 |
| 连接建立 | 3-RTT | 1-RTT |
| 连接迁移 | 困难 | 原生支持 |
| 0-RTT 恢复 | 不支持 | 支持 |

### QUIC 架构

```
Application: HTTP/3
    ↓
Transport:   QUIC (UDP)
    ↓
Security:   TLS 1.3 (内置)
```

### Alt-Svc 支持

HTTP/3 通过 Alt-Svc 头发现：

```java
// 服务器返回
HTTP/1.1 200 OK
Alt-Svc: h3=":443"; ma=2592000

// 后续请求自动升级到 HTTP/3
```

---

## API 对比

### HttpURLConnection → HttpClient

| 操作 | HttpURLConnection | HttpClient |
|------|-------------------|--------------|
| GET 请求 | 10+ 行代码 | 3 行代码 |
| POST 请求 | 复杂 | 简洁 |
| 异步请求 | 需要自己实现 | 内置支持 |
| 超时设置 | 复杂 | 简单 |
| 连接池 | 手动管理 | 自动管理 |
| HTTP/2 | 不支持 | 支持 |
| HTTP/3 | 不支持 | 支持 (JDK 26+) |

### 代码对比

```java
// HttpURLConnection (旧)
URL url = new URL("https://api.example.com/data");
HttpURLConnection conn = (HttpURLConnection) url.openConnection();
conn.setRequestMethod("GET");
conn.setConnectTimeout(5000);
conn.setRequestProperty("Authorization", "Bearer token");

try (BufferedReader br = new BufferedReader(
        new InputStreamReader(conn.getInputStream()))) {
    StringBuilder response = new StringBuilder();
    String line;
    while ((line = br.readLine()) != null) {
        response.append(line);
    }
    return response.toString();
} finally {
    conn.disconnect();
}

// HttpClient (新)
HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/data"))
    .header("Authorization", "Bearer token")
    .timeout(Duration.ofSeconds(5))
    .GET()
    .build();

return client.send(request,
    HttpResponse.BodyHandlers.ofString()).body();
```

---

## 性能对比

### 连接建立时间

| 协议 | RTT 次数 | 时间 (假设 RTT=50ms) |
|------|---------|---------------------|
| HTTP/1.1 | 3-RTT | ~150ms |
| HTTP/2 | 3-RTT | ~150ms |
| HTTP/3 | 1-RTT | ~50ms |
| HTTP/3 (0-RTT 恢复) | 0-RTT | ~0ms |

### 丢包恢复

```
场景: 1% 丢包率，10 个并发请求

HTTP/2 (TCP): 所有请求受影响（TCP 队头阻塞）
HTTP/3 (QUIC): 仅丢包的流受影响（独立流）
```

### 吞吐量对比

| 场景 | HTTP/1.1 | HTTP/2 | HTTP/3 |
|------|----------|--------|--------|
| 单连接 | 100 req/s | 500 req/s | 800 req/s |
| 高并发 | 需要多连接 | 多路复用 | 无队头阻塞 |

---

## 完整使用示例

### 基础配置

```java
public class HttpClientExample {
    private final HttpClient client;

    public HttpClientExample() {
        this.client = HttpClient.newBuilder()
            .version(HttpClient.Version.HTTP_3_AUTO)
            .connectTimeout(Duration.ofSeconds(10))
            .followRedirects(HttpClient.Redirect.NORMAL)
            .executor(Executors.newVirtualThreadPerTaskExecutor())
            .build();
    }

    public String get(String url) throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(url))
            .GET()
            .build();

        HttpResponse<String> response = client.send(request,
            HttpResponse.BodyHandlers.ofString());

        if (response.statusCode() >= 400) {
            throw new RuntimeException("HTTP error: " + response.statusCode());
        }

        return response.body();
    }

    public CompletableFuture<String> getAsync(String url) {
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(url))
            .GET()
            .build();

        return client.sendAsync(request,
            HttpResponse.BodyHandlers.ofString())
            .thenApply(response -> {
                if (response.statusCode() >= 400) {
                    throw new RuntimeException("HTTP error: " + response.statusCode());
                }
                return response.body();
            });
    }

    public String postJson(String url, String json) throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(url))
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(json))
            .build();

        HttpResponse<String> response = client.send(request,
            HttpResponse.BodyHandlers.ofString());

        return response.body();
    }
}
```

### 批量请求

```java
List<String> urls = List.of(
    "https://api.example.com/users/1",
    "https://api.example.com/users/2",
    "https://api.example.com/users/3"
);

// 并发请求
List<CompletableFuture<String>> futures = urls.stream()
    .map(url -> client.sendAsync(
        HttpRequest.newBuilder(URI.create(url)).GET().build(),
        HttpResponse.BodyHandlers.ofString()))
    .map(f -> f.thenApply(HttpResponse::body))
    .toList();

// 等待全部完成
CompletableFuture.allOf(futures.toArray(new CompletableFuture[0])).join();

List<String> results = futures.stream()
    .map(CompletableFuture::join)
    .toList();
```

---

## 最佳实践

### 1. 重用 HttpClient 实例

```java
// ✅ 推荐: 单例 HttpClient
private static final HttpClient CLIENT = HttpClient.newHttpClient();

// ❌ 避免: 每次请求创建新实例
public void badExample() {
    HttpClient client = HttpClient.newHttpClient();  // 每次创建
}
```

### 2. 使用虚拟线程执行器 (JDK 21+)

```java
HttpClient client = HttpClient.newBuilder()
    .executor(Executors.newVirtualThreadPerTaskExecutor())
    .build();
```

### 3. 设置合理的超时

```java
HttpClient client = HttpClient.newBuilder()
    .connectTimeout(Duration.ofSeconds(10))
    .build();

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create(url))
    .timeout(Duration.ofSeconds(30))  // 读取超时
    .build();
```

### 4. 处理 HTTP/3 降级

```java
HttpResponse<String> response = client.send(request, ...);
if (response.version() != HttpClient.Version.HTTP_3) {
    log.info("HTTP/3 不可用，使用 " + response.version());
}
```

---

## 时间线总结

| 版本 | 特性 | JEP | 状态 |
|------|------|-----|------|
| JDK 1.0 | HttpURLConnection | - | 标准 |
| JDK 9 | HTTP Client (孵化) | JEP 110 | 实验性 |
| JDK 10 | HTTP Client (孵化) | - | 实验性 |
| JDK 11 | HTTP Client (标准) | JEP 321 | 标准 |
| JDK 16 | HTTP/2 支持 | - | 标准 |
| JDK 21 | HTTP Client 正式 | - | 标准 |
| JDK 22 | 连接复用优化 | - | 标准 |
| JDK 26 | HTTP/3 支持 | JEP 517 | 预览 |

---

## 相关链接

- [HTTP Client 文档](https://docs.oracle.com/en/java/javase/11/docs/api/java.net.http/java/net/http/package-summary.html)
- [JEP 321: HTTP Client](https://openjdk.org/jeps/321)
- [JEP 517: HTTP/3](https://openjdk.org/jeps/517)
