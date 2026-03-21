# HTTP 客户端演进时间线

从 HttpURLConnection 到 HTTP/3 的演进历程。

---
## 目录

1. [时间线概览](#1-时间线概览)
2. [HTTP 协议演进](#2-http-协议演进)
3. [JDK 1.0 - HttpURLConnection](#3-jdk-10---httpurlconnection)
4. [JDK 9 - HTTP Client (孵化器) - JEP 110](#4-jdk-9---http-client-孵化器---jep-110)
5. [JDK 11 - HTTP Client (标准) - JEP 321](#5-jdk-11---http-client-标准---jep-321)
6. [HTTP/2 支持](#6-http2-支持)
7. [HTTP/3 (JDK 26, JEP 517)](#7-http3-jdk-26-jep-517)
8. [性能对比](#8-性能对比)
9. [最佳实践](#9-最佳实践)
10. [故障排查](#10-故障排查)
11. [时间线总结](#11-时间线总结)
12. [相关链接](#12-相关链接)

---


## 1. 时间线概览

```
JDK 1.0 ──── JDK 9 ──── JDK 11 ──── JDK 16 ──── JDK 22 ──── JDK 26
 │             │             │             │             │             │
HttpURL       HTTP Client   HTTP Client   HTTP/2       多项改进      HTTP/3
Connection    (孵化器)      (标准)        支持          连接复用       (预览)
(旧 API)      JEP 110       JEP 321                    优化          JEP 517
```

---

## 2. HTTP 协议演进

```
┌─────────────────────────────────────────────────────────┐
│                   HTTP 协议演进                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  HTTP/0.9 (1991)  - 极简协议，仅 GET                    │
│       ↓                                                 │
│  HTTP/1.0 (1996)  - 增加 POST、Header、状态码           │
│       ↓                                                 │
│  HTTP/1.1 (1997)  - 持久连接、分块传输、缓存            │
│       ↓                                                 │
│  HTTP/2 (2015)   - 二进制分帧、多路复用、头部压缩        │
│       ↓                                                 │
│  HTTP/3 (2022)   - 基于 QUIC、无队头阻塞、UDP 传输      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### HTTP 版本对比

| 特性 | HTTP/1.1 | HTTP/2 | HTTP/3 |
|------|----------|--------|--------|
| 传输层 | TCP | TCP | QUIC (UDP) |
| 协议格式 | 文本 | 二进制 | 二进制 |
| 多路复用 | 否 | 是 | 是 |
| 队头阻塞 | 有 | 应用层无，TCP 层有 | 无 |
| 头部压缩 | 无 | HPACK | QPACK |
| 服务器推送 | 不支持 | 支持 | 支持 |
| 连接迁移 | 困难 | 困难 | 原生支持 |
| 握手 RTT | 3-RTT | 3-RTT | 1-RTT |
| 0-RTT 恢复 | 否 | 否 | 是 |

---

## 3. JDK 1.0 - HttpURLConnection

### 架构

```
┌─────────────────────────────────────────────────────────┐
│            HttpURLConnection 架构                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Application                                            │
│       │                                                 │
│       ▼                                                 │
│  ┌─────────────────┐                                   │
│  │ URL             │                                   │
│  │ openConnection()│                                   │
│  └────────┬────────┘                                   │
│           │                                             │
│           ▼                                             │
│  ┌─────────────────┐                                   │
│  │HttpURLConnection│                                   │
│  │  - connect()    │                                   │
│  │  - getInputStream()                                 │
│  └────────┬────────┘                                   │
│           │                                             │
│           ▼                                             │
│  ┌─────────────────┐                                   │
│  │  Socket (TCP)   │                                   │
│  └─────────────────┘                                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 基础用法

```java
// GET 请求
URL url = new URL("https://example.com");
HttpURLConnection conn = (HttpURLConnection) url.openConnection();
conn.setRequestMethod("GET");
conn.setConnectTimeout(5000);
conn.setReadTimeout(5000);
conn.setRequestProperty("User-Agent", "MyApp/1.0");

try (BufferedReader br = new BufferedReader(
        new InputStreamReader(conn.getInputStream(), StandardCharsets.UTF_8))) {
    StringBuilder response = new StringBuilder();
    String line;
    while ((line = br.readLine()) != null) {
        response.append(line);
    }
    return response.toString();
} finally {
    conn.disconnect();
}
```

### POST 请求

```java
URL url = new URL("https://api.example.com/users");
HttpURLConnection conn = (HttpURLConnection) url.openConnection();
conn.setRequestMethod("POST");
conn.setDoOutput(true);
conn.setRequestProperty("Content-Type", "application/json");

// 写入请求体
String json = """
    {"name": "John", "age": 30}
    """;

try (OutputStream os = conn.getOutputStream()) {
    byte[] input = json.getBytes(StandardCharsets.UTF_8);
    os.write(input, 0, input.length);
}

// 读取响应
int responseCode = conn.getResponseCode();
if (responseCode == HttpURLConnection.HTTP_OK) {
    try (BufferedReader br = new BufferedReader(
            new InputStreamReader(conn.getInputStream()))) {
        // 处理响应
    }
}
```

### 处理重定向

```java
conn.setInstanceFollowRedirects(false);  // 手动处理
int status = conn.getResponseCode();
if (status == HttpURLConnection.HTTP_MOVED_TEMP
    || status == HttpURLConnection.HTTP_MOVED_PERM
    || status == HttpURLConnection.HTTP_SEE_OTHER) {

    String newUrl = conn.getHeaderField("Location");
    URL nextUrl = new URL(newUrl);
    // 递归处理
}
```

### HttpURLConnection 问题

| 问题 | 说明 | 影响 |
|------|------|------|
| API 设计陈旧 | 不符合现代编程风格 | 代码冗长 |
| 不支持 HTTP/2 | 无法利用 HTTP/2 优势 | 性能受限 |
| 超时配置复杂 | connectTimeout/readTimeout 分离 | 易出错 |
| 异步请求困难 | 需要自己实现线程池 | 开发成本高 |
| 连接池管理 | 手动管理或使用系统默认 | 难以优化 |

---

## 4. JDK 9 - HTTP Client (孵化器) - JEP 110

### 模块声明

```java
module com.example {
    requires jdk.incubator.httpclient;
}
```

### 基础使用

```java
import jdk.incubator.http.*;
import java.net.URI;

HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://example.com"))
    .GET()
    .build();

HttpResponse<String> response = client.send(request,
    HttpResponse.BodyHandlers.ofString());
```

---

## 5. JDK 11 - HTTP Client (标准) - JEP 321

### 架构

```
┌─────────────────────────────────────────────────────────┐
│              HttpClient 架构                             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────┐        │
│  │              HttpClient                      │        │
│  │  - 连接池                                   │        │
│  │  - 异步调度器                                │        │
│  │  - 协议协商                                  │        │
│  └─────────────────┬───────────────────────────┘        │
│                    │                                    │
│         ┌──────────┴──────────┐                         │
│         │                     │                         │
│    ┌────▼────┐           ┌────▼────┐                   │
│    │ HttpRequest│        │ HttpResponse│                │
│    │  - URI   │           │  - BodyHandler             │
│    │  - Headers│          │  - StatusCode              │
│    │  - Timeout│          │  - Version                 │
│    └────┬────┘           └────┬────┘                   │
│         │                     │                         │
│         ▼                     ▼                         │
│  ┌─────────────────────────────────────┐               │
│  │        HTTP/1.1   HTTP/2   HTTP/3  │               │
│  │           ┆          ┆         ┆    │               │
│  └─────────────────────────────────────┘               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 完整 API 示例

```java
import java.net.http.*;
import java.net.URI;
import java.time.Duration;
import java.util.concurrent.CompletableFuture;

public class HttpClientExample {
    private final HttpClient client;

    public HttpClientExample() {
        this.client = HttpClient.newBuilder()
            .version(HttpClient.Version.HTTP_2)
            .connectTimeout(Duration.ofSeconds(10))
            .followRedirects(HttpClient.Redirect.NORMAL)
            .executor(Executors.newFixedThreadPool(10))
            .build();
    }

    // 同步 GET
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

    // 异步 GET
    public CompletableFuture<String> getAsync(String url) {
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(url))
            .GET()
            .build();

        return client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
            .thenApply(response -> {
                if (response.statusCode() >= 400) {
                    throw new RuntimeException("HTTP error: " + response.statusCode());
                }
                return response.body();
            });
    }

    // POST JSON
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

    // POST 表单
    public String postForm(String url, Map<String, String> form) throws Exception {
        String formData = form.entrySet().stream()
            .map(e -> URLEncoder.encode(e.getKey(), UTF_8) + "=" +
                       URLEncoder.encode(e.getValue(), UTF_8))
            .collect(Collectors.joining("&"));

        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(url))
            .header("Content-Type", "application/x-www-form-urlencoded")
            .POST(HttpRequest.BodyPublishers.ofString(formData))
            .build();

        HttpResponse<String> response = client.send(request,
            HttpResponse.BodyHandlers.ofString());

        return response.body();
    }
}
```

### BodyHandler 和 BodyPublisher

```java
// BodyHandler - 处理响应
HttpResponse<String>      response1 = client.send(request, HttpResponse.BodyHandlers.ofString());
HttpResponse<byte[]>      response2 = client.send(request, HttpResponse.BodyHandlers.ofByteArray());
HttpResponse<Path>        response3 = client.send(request, HttpResponse.BodyHandlers.ofFile(Paths.get("output.txt")));
HttpResponse<Stream<String>> response4 = client.send(request, HttpResponse.BodyHandlers.ofLines());
HttpResponse<InputSteam>   response5 = client.send(request, HttpResponse.BodyHandlers.ofInputStream());

// BodyPublisher - 发送请求体
HttpRequest.BodyPublishers.ofString("Hello")           // 字符串
HttpRequest.BodyPublishers.ofByteArray(bytes)           // 字节数组
HttpRequest.BodyPublishers.ofFile(Paths.get("file.txt")) // 文件
HttpRequest.BodyPublishers.ofInputStream(stream)        // 流
```

### 批量请求

```java
List<String> urls = List.of(
    "https://api.example.com/users/1",
    "https://api.example.com/users/2",
    "https://api.example.com/users/3"
);

// 并发请求
List<CompletableFuture<HttpResponse<String>>> futures = urls.stream()
    .map(url -> {
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(url))
            .GET()
            .build();
        return client.sendAsync(request, HttpResponse.BodyHandlers.ofString());
    })
    .toList();

// 等待全部完成
CompletableFuture.allOf(futures.toArray(new CompletableFuture[0])).join();

// 收集结果
List<String> results = futures.stream()
    .map(CompletableFuture::join)
    .map(HttpResponse::body)
    .toList();
```

---

## 6. HTTP/2 支持

### HTTP/2 特性

```java
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_2)
    .build();

// 检查实际使用的协议
HttpResponse<String> response = client.send(request, ...);
System.out.println("Protocol: " + response.version());  // HTTP_2
```

### HTTP/2 多路复用

```
┌─────────────────────────────────────────────────────────┐
│                HTTP/2 多路复用                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  HTTP/1.1                         HTTP/2                │
│  ┌─────┐ ┌─────┐ ┌─────┐         ┌─────────────────┐   │
│  │Conn1│ │Conn2│ │Conn3│         │     Conn        │   │
│  └──┬──┘ └──┬──┘ └──┬──┘         └────────┬────────┘   │
│     │       │       │                    │             │
│     ▼       ▼       ▼        ┌───────┬───┴───┬───────┐  │
│  Stream1 Stream2 Stream3      │Stream1│Stream2│Stream3│ │
│                                └───────┴───────┴───────┘  │
│                                                         │
│  一个连接一个请求              一个连接多个请求           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### HTTP/2 Push Promise

```java
// 服务器推送会在响应中体现
HttpResponse<String> response = client.send(request,
    HttpResponse.BodyHandlers.ofString());

// 检查推送的资源
response.pushPromises().forEach(promise -> {
    System.out.println("Pushed: " + promise.request().uri());
});
```

---

## 7. HTTP/3 (JDK 26, JEP 517)

### QUIC 协议栈

```
┌─────────────────────────────────────────────────────────┐
│                 HTTP/3 协议栈                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────┐        │
│  │              HTTP/3                          │        │
│  │  - QPACK (头部压缩)                          │        │
│  │  - Stream 帧 (DATA, HEADERS, SETTINGS)       │        │
│  └─────────────────┬───────────────────────────┘        │
│                    │                                    │
│  ┌─────────────────┴───────────────────────────┐        │
│  │              QUIC                            │        │
│  │  - 传输层 (UDP)                              │        │
│  │  - TLS 1.3 (内置)                            │        │
│  │  - 连接迁移                                  │        │
│  │  - 0-RTT 恢复                                │        │
│  └─────────────────┬───────────────────────────┘        │
│                    │                                    │
│  ┌─────────────────┴───────────────────────────┐        │
│  │              UDP                            │        │
│  └─────────────────────────────────────────────┘        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### HTTP/3 使用

```java
import java.net.http.*;

// 启用 HTTP/3
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_3)
    .connectTimeout(Duration.ofSeconds(10))
    .build();

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://cloudflare.com/"))
    .build();

HttpResponse<String> response = client.send(request,
    HttpResponse.BodyHandlers.ofString());

System.out.println("Version: " + response.version());  // HTTP_3
System.out.println("Status: " + response.statusCode());
```

### 自动协议协商

```java
// HTTP_3_AUTO - 自动选择最佳协议
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_3_AUTO)  // HTTP/3 > HTTP/2 > HTTP/1.1
    .build();

// 协议协商过程:
// 1. 尝试 HTTP/3
// 2. 如果失败 (UDP 被阻止/服务器不支持)，降级到 HTTP/2
// 3. 如果失败，降级到 HTTP/1.1
```

### HTTP/3 帧类型

```java
// HTTP/3 帧类型 (内部实现)
enum Http3FrameType {
    DATA(0x00),           // 数据帧
    HEADERS(0x01),        // 头部帧
    CANCEL_PUSH(0x03),    // 取消推送
    SETTINGS(0x04),       // 设置帧
    PUSH_PROMISE(0x05),   // 推送承诺
    GOAWAY(0x07),         // 关闭连接
    MAX_PUSH_ID(0x0D);    // 最大推送 ID
}
```

### Alt-Svc 发现

```java
// 服务器通过 Alt-Svc 头宣告 HTTP/3 支持
// HTTP/1.1 响应:
// Alt-Svc: h3=":443"; ma=2592000

// 后续请求自动升级到 HTTP/3
// HttpClient 会缓存 Alt-Svc 信息
```

---

## 8. 性能对比

### 连接建立时间

| 协议 | RTT 次数 | 说明 |
|------|---------|------|
| HTTP/1.1 | TCP(1) + TLS(2) = 3-RTT | ~150ms |
| HTTP/2 | TCP(1) + TLS(2) = 3-RTT | ~150ms |
| HTTP/3 | QUIC(1+TLS) = 1-RTT | ~50ms |
| HTTP/3 (0-RTT) | 恢复连接 = 0-RTT | ~0ms |

### 丢包恢复

```
场景: 1% 丢包率，10 个并发请求

HTTP/2 (TCP):
┌─────────────────────────────────────────┐
│ Stream1 │ Stream2 │ Stream3 │ Stream4 │
└────┬────┴────┬────┴────┬────┴────┬────┘
     │         │         │         │
     └─────────┴─────────┴─────────┘
                  │
              丢包阻塞
                  │
             ▼     ▼     ▼     ▼
          全部等待重传

HTTP/3 (QUIC):
┌─────────────────────────────────────────┐
│ Stream1 │ Stream2 │ Stream3 │ Stream4 │
└────┬────┴────┬────┴────┬────┴────┬────┘
     │         │         │         │
     └─────────┴─────────┴─────────┘
              独立流，互不影响
     │         │         │         │
  仅丢包流重传，其他流继续
```

### 吞吐量对比

| 场景 | HTTP/1.1 | HTTP/2 | HTTP/3 |
|------|----------|--------|--------|
| 单连接 | 100 req/s | 500 req/s | 800 req/s |
| 高并发 (100连接) | 需100个连接 | 需10个连接 | 需1个连接 |
| 1% 丢包 | 吞吐量下降 50% | 吞吐量下降 30% | 吞吐量下降 5% |

---

## 9. 最佳实践

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
    .connectTimeout(Duration.ofSeconds(10))  // 连接超时
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
    // 可能原因: UDP 被阻止、服务器不支持
}
```

### 5. 使用响应式流处理大数据

```java
HttpResponse<Stream<String>> response = client.send(request,
    HttpResponse.BodyHandlers.ofLines());

response.body()
    .filter(line -> line.contains("keyword"))
    .limit(100)
    .forEach(this::processLine);
```

---

## 10. 故障排查

### HTTP/3 不可用

```bash
# 检查 UDP 是否被阻止
telnet example.com 443

# 检查防火墙
sudo iptables -L -n | grep 443

# 启用详细日志
-Djava.util.logging.config.file=logging.properties

# logging.properties
java.net.http.level=FINE
jdk.internal.net.http.level=FINE
```

### 连接泄漏

```java
// 使用 try-with-resources 自动释放
try (var client = HttpClient.newBuilder().build()) {
    // 使用 client
}

// 或者确保 HttpClient 正确关闭
client.shutdown();        // 优雅关闭
client.shutdownNow();     // 立即关闭
```

---

## 11. 时间线总结

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

## 12. 相关链接

- [HTTP Client 文档](https://docs.oracle.com/en/java/javase/11/docs/api/java.net.http/java/net/http/package-summary.html)
- [JEP 321](/jeps/network/jep-321.md)
- [JEP 517](/jeps/network/jep-517.md)
- [RFC 9114: HTTP/3](https://www.rfc-editor.org/rfc/rfc9114)
- [RFC 9000: QUIC](https://www.rfc-editor.org/rfc/rfc9000)
