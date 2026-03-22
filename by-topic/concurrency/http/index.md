# HTTP 客户端

> 从 HttpURLConnection 到 HTTP/3 的完整演进历程

[← 返回并发网络](../)

---
## 目录

1. [快速概览](#1-快速概览)
2. [核心贡献者](#2-核心贡献者)
3. [HttpURLConnection (旧 API)](#3-httpurlconnection-旧-api)
4. [HttpClient (JDK 11+)](#4-httpclient-jdk-11)
5. [HTTP/2 支持](#5-http2-支持)
6. [WebSocket 支持](#6-websocket-支持)
7. [HTTP/3 (JDK 26+)](#7-http3-jdk-26)
8. [配置选项](#8-配置选项)
9. [Body Handler 和 Publisher](#9-body-handler-和-publisher)
10. [性能优化](#10-性能优化)
11. [错误处理](#11-错误处理)
12. [对比其他客户端](#12-对比其他客户端)
13. [重要 PR 分析](#13-重要-pr-分析)
14. [性能优化最佳实践](#14-性能优化最佳实践)
15. [相关链接](#15-相关链接)

---


## 1. 快速概览

```
JDK 1.0 ── JDK 1.1 ── JDK 5 ── JDK 9 ── JDK 11 ── JDK 16 ── JDK 21 ── JDK 26
   │         │          │        │        │        │        │        │
HttpURL   HTTP/1.1   HTTP     HTTP    HTTP    HTTP/2  虚拟线程   HTTP/3
Connection 持久连接   URLConn  Client  Client   ALPN   +HttpClient (预览)
(旧API)   Keep-Alive (改进)   (孵化)  (标准)  Server   完美搭配  JEP 517
                                       JEP321   Push              QUIC
```

### HTTP Client 演进 (Evolution)

Java HTTP 客户端经历了三个重要阶段:

| 阶段 | 时期 | API | 协议 | 传输层 | 设计模式 |
|------|------|-----|------|--------|----------|
| **第一代** | JDK 1.1 (1997) | `HttpURLConnection` | HTTP/1.1 | TCP | 阻塞式 (Blocking I/O) |
| **第二代** | JDK 11 (2018) | `java.net.http.HttpClient` (JEP 321) | HTTP/1.1 + HTTP/2 | TCP + TLS/ALPN | 同步+异步 (Sync + Async) |
| **第三代** | JDK 26 (2026) | `HttpClient` + HTTP/3 (JEP 517) | HTTP/3 | QUIC (UDP) | 0-RTT 连接 |

**为什么要演进?**

- **HttpURLConnection 的痛点**: 设计于 1997 年，API 笨重 (verbose)，不支持 HTTP/2，无异步能力，连接管理困难
- **JEP 321 的目标**: 提供现代化 (modern)、流式 (streaming)、异步 (asynchronous) 的 HTTP 客户端
- **JEP 517 的目标**: 拥抱 QUIC 协议，消除队头阻塞 (Head-of-Line Blocking)，支持连接迁移 (Connection Migration)

### 协议演进

| 版本 | 协议 | 特性 | 传输层 | 状态 |
|------|------|------|--------|------|
| **JDK 1.0** | HTTP/1.0 | 基础支持，每次请求新连接 | TCP | 已过时 |
| **JDK 1.1** | HTTP/1.1 | 持久连接 (Keep-Alive)、分块传输 (Chunked Transfer) | TCP | 已过时 |
| **JDK 9** | HTTP/2 | 多路复用 (Multiplexing)、孵化 API | TCP + TLS | 孵化 |
| **JDK 11** | HTTP/2 | 标准化 (JEP 321)、Server Push | TCP + TLS/ALPN | 标准 |
| **JDK 26** | HTTP/3 | 基于 QUIC、0-RTT、连接迁移 | UDP (QUIC) | 预览 |

### API 演进

| API | 首发版本 | 设计目标 | 当前状态 |
|-----|----------|----------|----------|
| `HttpURLConnection` | JDK 1.0 | 简单 HTTP | 不推荐 (Deprecated in spirit) |
| `Apache HttpClient` | 第三方 | 功能丰富 | 外部 |
| `OkHttp` | 第三方 | 高性能 | 外部 |
| `java.net.http.HttpClient` | JDK 11 | 现代 HTTP | 推荐 (Recommended) |

---

## 2. 核心贡献者

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

## 3. HttpURLConnection (旧 API)

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

## 4. HttpClient (JDK 11+)

### JEP 321: HTTP Client

**标准化**: JDK 11 (JEP 321)

**设计目标**:
- HTTP/2 支持 (Multiplexing)
- WebSocket 支持 (RFC 6455)
- 异步非阻塞 (Async non-blocking)
- 流式处理 (Streaming)
- 响应式集成 (Reactive Streams)

### HttpClient API 深入: Builder 模式 (Builder Pattern)

HttpClient 采用不可变 Builder 模式，所有配置在构建时确定:

```java
import java.net.http.*;
import java.net.URI;
import javax.net.ssl.*;

// 完整 Builder 配置示例
HttpClient client = HttpClient.newBuilder()
    // 协议版本 (Protocol Version)
    .version(HttpClient.Version.HTTP_2)
    // 连接超时 (Connection Timeout)
    .connectTimeout(Duration.ofSeconds(10))
    // 重定向策略 (Redirect Policy)
    .followRedirects(HttpClient.Redirect.NORMAL)
    // 代理设置 (Proxy Configuration)
    .proxy(ProxySelector.of(new InetSocketAddress("proxy.example.com", 8080)))
    // SSL 上下文 (SSL Context)
    .sslContext(SSLContext.getDefault())
    // SSL 参数 (SSL Parameters) - 自定义协议版本和密码套件
    .sslParameters(new SSLParameters(
        new String[]{"TLS_AES_128_GCM_SHA256"},  // Cipher Suites
        new String[]{"TLSv1.3"}))                // Protocols
    // 认证器 (Authenticator)
    .authenticator(new Authenticator() {
        @Override
        protected PasswordAuthentication getPasswordAuthentication() {
            return new PasswordAuthentication("user", "pass".toCharArray());
        }
    })
    // Cookie 管理 (Cookie Handler)
    .cookieHandler(new CookieManager(null, CookiePolicy.ACCEPT_ALL))
    // 执行器 (Executor) - 控制线程池
    .executor(Executors.newVirtualThreadPerTaskExecutor())  // JDK 21+
    // HTTP/2 优先级 (Priority, 1-256)
    .priority(1)
    .build();
```

**Builder 配置项一览**:

| 方法 | 说明 | 默认值 |
|------|------|--------|
| `version()` | HTTP 协议版本 | HTTP_2 (降级到 HTTP/1.1) |
| `connectTimeout()` | TCP 连接超时 | 无限等待 |
| `followRedirects()` | 重定向策略 | NEVER |
| `proxy()` | 代理选择器 | 系统默认 |
| `sslContext()` | SSL/TLS 上下文 | 默认 SSLContext |
| `authenticator()` | HTTP 认证 | 无 |
| `cookieHandler()` | Cookie 管理 | 无 |
| `executor()` | 异步执行线程池 | 内部默认池 |
| `priority()` | HTTP/2 请求优先级 | 无 |

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

### 同步 vs 异步: send() vs sendAsync()

**同步调用 (Synchronous)** — 阻塞当前线程直到响应返回:

```java
// send() - 阻塞式调用，适合简单场景
HttpResponse<String> response = client.send(request,
    HttpResponse.BodyHandlers.ofString());
// 线程在此等待直到响应完成
```

**异步调用 (Asynchronous)** — 立即返回 CompletableFuture，非阻塞:

```java
// sendAsync() - 非阻塞式调用，返回 CompletableFuture
CompletableFuture<HttpResponse<String>> future =
    client.sendAsync(request, HttpResponse.BodyHandlers.ofString());

// CompletableFuture 链式调用 (Chaining)
future
    .thenApply(HttpResponse::body)                    // 提取响应体
    .thenApply(body -> parseJson(body))               // 解析 JSON
    .thenAccept(data -> processData(data))            // 处理数据
    .exceptionally(ex -> {                            // 异常处理
        System.err.println("Error: " + ex.getMessage());
        return null;
    });
```

**多请求异步编排 (Orchestrating Multiple Async Requests)**:

```java
// 并行发送多个请求，聚合结果
CompletableFuture<String> user = client.sendAsync(
    HttpRequest.newBuilder(URI.create("https://api.example.com/user/1")).build(),
    HttpResponse.BodyHandlers.ofString())
    .thenApply(HttpResponse::body);

CompletableFuture<String> orders = client.sendAsync(
    HttpRequest.newBuilder(URI.create("https://api.example.com/orders?userId=1")).build(),
    HttpResponse.BodyHandlers.ofString())
    .thenApply(HttpResponse::body);

// 合并结果 (Combine Results)
CompletableFuture<String> combined = user.thenCombine(orders,
    (u, o) -> "User: " + u + ", Orders: " + o);
```

**选择建议**:

| 场景 | 推荐 | 原因 |
|------|------|------|
| 简单脚本/工具 | `send()` | 代码简单直观 |
| Web 服务器中 | `sendAsync()` | 不阻塞请求处理线程 |
| 批量 API 调用 | `sendAsync()` + `allOf()` | 并行执行，高吞吐 |
| 虚拟线程环境 (JDK 21+) | `send()` | 虚拟线程自动非阻塞 |

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

## 5. HTTP/2 支持

### HTTP/2 核心特性一览

| 特性 | 说明 | HTTP/1.1 对比 |
|------|------|---------------|
| **多路复用 (Multiplexing)** | 单连接并行多个请求/响应 | HTTP/1.1 需要多个连接 |
| **Server Push** | 服务器主动推送资源 | 无此能力 |
| **HPACK 头压缩 (Header Compression)** | 二进制编码 + 静态/动态表压缩 | 文本头，无压缩 |
| **流优先级 (Stream Priority)** | 请求可设置优先级权重 | 先进先出 |
| **二进制帧 (Binary Framing)** | DATA / HEADERS / SETTINGS 等帧 | 文本协议 |

### 多路复用 (Multiplexing)

HTTP/2 在单个 TCP 连接上并行传输多个请求和响应，每个请求/响应是一个独立的 "流" (Stream):

```
HTTP/1.1: 连接1 → 请求A → 响应A (队头阻塞)
          连接2 → 请求B → 响应B
          连接3 → 请求C → 响应C

HTTP/2:   连接1 → ┌─ 流1: 请求A → 响应A ─┐
                  ├─ 流2: 请求B → 响应B ─┤  单连接，并行传输
                  └─ 流3: 请求C → 响应C ─┘
```

```java
// HTTP/2 自动多路复用
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_2)  // 优先 HTTP/2，自动 ALPN 协商
    .build();

// 多个请求共享同一 TCP 连接
List<HttpRequest> requests = List.of(
    HttpRequest.newBuilder()
        .uri(URI.create("https://example.com/api/1"))
        .build(),
    HttpRequest.newBuilder()
        .uri(URI.create("https://example.com/api/2"))
        .build()
);

// 并发执行，共享 TCP 连接 (同一 host:port 自动复用)
List<CompletableFuture<String>> futures = requests.stream()
    .map(req -> client.sendAsync(req,
        HttpResponse.BodyHandlers.ofString())
        .thenApply(HttpResponse::body))
    .toList();
```

### HPACK 头压缩 (Header Compression)

HTTP/2 使用 HPACK 压缩算法 (RFC 7541) 减少头部大小:

- **静态表 (Static Table)**: 61 个预定义的常见头字段 (如 `:method GET`, `content-type`)
- **动态表 (Dynamic Table)**: 连接级别的自适应表，缓存重复出现的头
- **Huffman 编码**: 对头字段值进行二进制压缩

典型压缩效果: 头部大小减少 **85-95%** (尤其是重复请求 Cookie 等大头场景)。

### 流优先级 (Stream Priority)

```java
// 通过 HttpClient.Builder 设置默认优先级 (1 = 最高, 256 = 最低)
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_2)
    .priority(1)  // 高优先级
    .build();
```

> **注意**: 流优先级在 HTTP/2 中是建议性的 (advisory)，服务器可以忽略。
> HTTP/3 使用不同的优先级机制 (RFC 9218, Extensible Priorities)。

### HTTP/2 Server Push

```java
// 服务器推送 (JDK 11+, PushPromiseHandler)
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_2)
    .build();

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://example.com/api"))
    .build();

// PushPromiseHandler is passed to send()/sendAsync()
ConcurrentMap<HttpRequest, CompletableFuture<HttpResponse<String>>>
    pushPromises = new ConcurrentHashMap<>();

HttpResponse.PushPromiseHandler<String> pushHandler =
    HttpResponse.PushPromiseHandler.of(
        HttpResponse.BodyHandlers.ofString(), pushPromises);

HttpResponse<String> response = client.send(request,
    HttpResponse.BodyHandlers.ofString(), pushHandler);

// 检查推送的资源
pushPromises.forEach((pushReq, futureResp) -> {
    System.out.println("Pushed: " + pushReq.uri());
});
```

> **注意**: Server Push 在实践中使用较少。Chrome 等浏览器已移除支持。
> HTTP/3 (RFC 9114) 已不再包含 Server Push 作为核心特性。

---

## 6. WebSocket 支持

### WebSocket API 概述

HttpClient 内置 WebSocket 支持 (RFC 6455)，提供双向通信 (Bidirectional Communication) 能力:

```
HTTP 请求/响应:    客户端 ──请求──→ 服务器
                  客户端 ←──响应── 服务器

WebSocket:        客户端 ←─────────→ 服务器  (全双工，持久连接)
                     │  实时推送 / 双向消息  │
```

### 基础用法

```java
import java.net.http.*;
import java.net.URI;

HttpClient client = HttpClient.newHttpClient();

WebSocket ws = client.newWebSocketBuilder()
    // 可选: 设置子协议 (Subprotocol) 和自定义头
    .subprotocols("graphql-ws")
    .header("Authorization", "Bearer token123")
    .buildAsync(URI.create("wss://example.com/ws"),
        new WebSocket.Listener() {
            @Override
            public void onOpen(WebSocket ws) {
                System.out.println("Connected");
                ws.request(1);  // 背压控制 (Backpressure): 请求接收 1 条消息
            }

            @Override
            public CompletionStage<?> onText(
                    WebSocket ws,
                    CharSequence data,
                    boolean last) {
                // last=true 表示消息完整; last=false 表示分片 (Fragment)
                System.out.println("Received: " + data);
                ws.request(1);  // 请求更多消息
                return null;    // 返回 null 表示同步处理完成
            }

            @Override
            public CompletionStage<?> onBinary(
                    WebSocket ws,
                    ByteBuffer data,
                    boolean last) {
                // 处理二进制消息 (如图片、protobuf)
                ws.request(1);
                return null;
            }

            @Override
            public CompletionStage<?> onPing(
                    WebSocket ws, ByteBuffer message) {
                // 心跳 Ping，框架自动回复 Pong
                ws.request(1);
                return null;
            }

            @Override
            public CompletionStage<?> onPong(
                    WebSocket ws, ByteBuffer message) {
                // 心跳 Pong 响应
                ws.request(1);
                return null;
            }

            @Override
            public CompletionStage<?> onClose(
                    WebSocket ws, int statusCode, String reason) {
                System.out.println("Closed: " + statusCode + " " + reason);
                return null;
            }

            @Override
            public void onError(WebSocket ws, Throwable error) {
                System.err.println("Error: " + error.getMessage());
            }
        })
    .join();

// 发送文本消息 (last=true 表示完整消息)
ws.sendText("Hello", true);

// 发送二进制消息
ws.sendBinary(ByteBuffer.wrap(new byte[]{1, 2, 3}), true);

// 主动发送 Ping 心跳
ws.sendPing(ByteBuffer.allocate(0));

// 关闭连接
ws.sendClose(WebSocket.NORMAL_CLOSURE, "Goodbye");
```

### WebSocket 背压机制 (Backpressure)

`ws.request(n)` 是背压控制的核心 — 告诉框架客户端准备好接收 n 条消息:

- 不调用 `request()` → 框架暂停接收，防止内存溢出
- 调用 `request(1)` → 每次只接收一条，处理完再请求下一条
- 调用 `request(Long.MAX_VALUE)` → 无限接收 (禁用背压)

---

## 7. HTTP/3 (JDK 26+)

### JEP 517: HTTP/3 Client

**状态**: 预览 (Preview, JDK 26)

### HTTP/3 vs HTTP/2 核心差异

| 维度 | HTTP/2 | HTTP/3 |
|------|--------|--------|
| **传输协议** | TCP + TLS 1.2/1.3 | QUIC (基于 UDP) |
| **连接建立** | TCP 3 次握手 + TLS 握手 (2-3 RTT) | QUIC 1-RTT，支持 0-RTT 恢复 |
| **队头阻塞** | TCP 层仍存在 | 完全消除 (每个流独立) |
| **连接迁移** | IP 变化需重建连接 | Connection ID 支持无缝迁移 |
| **丢包恢复** | 影响所有流 | 仅影响丢包的流 |
| **头压缩** | HPACK | QPACK (适配无序传输) |
| **Server Push** | 支持 (PushPromiseHandler) | 不再作为核心特性 |

### QUIC 协议关键特性

```
HTTP/2 连接建立 (2-3 RTT):           HTTP/3 连接建立 (1 RTT / 0-RTT):
┌────────┐     ┌────────┐            ┌────────┐     ┌────────┐
│ Client │     │ Server │            │ Client │     │ Server │
└───┬────┘     └───┬────┘            └───┬────┘     └───┬────┘
    │── SYN ──────→│  TCP             │── QUIC Initial ─→│  QUIC + TLS
    │←─ SYN+ACK ──│  握手                │←─ Handshake ────│  一体化
    │── ACK ──────→│                      │── Data ─────────→│  1 RTT 即可发数据
    │── ClientHello→│  TLS
    │←─ ServerHello│  握手            0-RTT 恢复 (已建立过连接):
    │── Finished ──→│                     │── 0-RTT Data ───→│  立即发送数据!
    │── Data ──────→│  终于可以发数据
```

**0-RTT 连接恢复 (Zero Round-Trip Time)**: 客户端缓存之前的连接参数，重连时直接发送加密数据，无需等待握手完成。

**连接迁移 (Connection Migration)**: 手机从 Wi-Fi 切换到 4G 时，QUIC 使用 Connection ID 而非 IP 四元组标识连接，无需重建:

```
传统 TCP:  Wi-Fi (IP: 192.168.1.5) → 4G (IP: 10.0.0.3) → 连接断开，重新建立
QUIC:      Wi-Fi (IP: 192.168.1.5) → 4G (IP: 10.0.0.3) → Connection ID 不变，无缝切换
```

### 使用 HTTP/3

```java
// HTTP/3 (预览, 需 --enable-preview)
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_3)  // JDK 26+
    .build();

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://example.com/api"))
    .build();

HttpResponse<String> response = client.send(request,
    HttpResponse.BodyHandlers.ofString());

// 检查实际使用的协议版本
System.out.println("Protocol: " + response.version());  // HTTP_3
```

**降级策略 (Fallback)**: 如果服务器不支持 HTTP/3，HttpClient 自动降级到 HTTP/2 或 HTTP/1.1。
服务器通过 `Alt-Svc` 响应头广告 HTTP/3 支持: `Alt-Svc: h3=":443"`。

---

## 8. 配置选项

### 超时设置 (Timeout Configuration)

```java
// 两层超时控制
HttpClient client = HttpClient.newBuilder()
    .connectTimeout(Duration.ofSeconds(10))  // TCP 连接超时 (Connection Timeout)
    .build();

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://example.com/api"))
    .timeout(Duration.ofSeconds(30))  // 请求超时 (Request Timeout): 整个请求-响应周期
    .build();
```

> **注意**: `connectTimeout` 仅控制 TCP 建连，`request.timeout` 控制整个请求生命周期。
> 如果需要读取超时 (Read Timeout)，可通过 `BodyHandlers.ofInputStream()` 配合 `InputStream.read()` 超时实现。

### 重定向策略 (Redirect Policy)

```java
HttpClient client = HttpClient.newBuilder()
    .followRedirects(HttpClient.Redirect.NORMAL)  // 自动重定向 (不含 HTTPS→HTTP 降级)
    // .followRedirects(HttpClient.Redirect.ALWAYS)  // 总是重定向 (含降级，不安全)
    // .followRedirects(HttpClient.Redirect.NEVER)   // 不重定向
    .build();
```

| 策略 | 301/302 | HTTPS→HTTP | 安全性 |
|------|---------|------------|--------|
| `NEVER` | 不跟随 | — | 最安全 |
| `NORMAL` | 跟随 | 拒绝降级 | 推荐 |
| `ALWAYS` | 跟随 | 允许降级 | 不推荐 |

### 认证 (Authentication)

```java
// Basic 认证 (服务器返回 401 时自动发送凭据)
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

// Bearer Token 认证 (通过 Header 手动设置)
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/data"))
    .header("Authorization", "Bearer eyJhbGciOiJIUzI1NiIs...")
    .build();
```

### 连接池 (Connection Pool)

HttpClient 内置连接池，同一 host:port 的请求自动复用连接:

```java
// 自定义线程池控制并发度
HttpClient client = HttpClient.newBuilder()
    .executor(Executors.newFixedThreadPool(10))  // 平台线程池
    .build();

// JDK 21+: 使用虚拟线程 — 更高并发，更低资源消耗
HttpClient client = HttpClient.newBuilder()
    .executor(Executors.newVirtualThreadPerTaskExecutor())
    .build();
```

> **连接池行为**: HttpClient 自动管理 TCP 连接的创建、复用和回收。
> HTTP/2 模式下，同一服务器通常只建立一个连接 (多路复用)。
> 系统属性 `jdk.httpclient.connectionPoolSize` 可控制池大小。

---

## 9. Body Handler 和 Publisher

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

## 10. 性能优化

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

## 11. 错误处理

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

## 12. 对比其他客户端

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

## 13. 重要 PR 分析

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

→ [JEP 517](/jeps/network/jep-517.md)

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

## 14. 性能优化最佳实践

### 连接复用 (Connection Reuse)

```java
// ✅ 推荐：单例 HttpClient — 连接池在客户端生命周期内复用
private static final HttpClient CLIENT = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_2)
    .connectTimeout(Duration.ofSeconds(10))
    .executor(Executors.newVirtualThreadPerTaskExecutor())  // JDK 21+
    .build();

// ❌ 避免：每次请求创建新客户端 — 每次都建立新连接，浪费资源
public HttpResponse<String> get(String url) throws Exception {
    HttpClient client = HttpClient.newHttpClient();  // 每次创建，浪费 TCP 握手 + TLS 握手
    // ...
}
```

**连接复用关键系统属性 (System Properties)**:

| 属性 | 默认值 | 说明 |
|------|--------|------|
| `jdk.httpclient.connectionPoolSize` | 0 (无限) | 连接池大小上限 |
| `jdk.httpclient.keepalive.timeout` | 1200 (秒) | 空闲连接存活时间 |
| `jdk.httpclient.maxRetries` | 5 | 连接失败重试次数 |
| `jdk.httpclient.receiveBufferSize` | OS 默认 | 接收缓冲区大小 |

### 超时配置建议 (Timeout Best Practices)

```java
// ✅ 推荐：分层超时控制
HttpClient client = HttpClient.newBuilder()
    .connectTimeout(Duration.ofSeconds(5))   // 快速失败 (Fail Fast)
    .build();

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/data"))
    .timeout(Duration.ofSeconds(30))         // 允许大响应
    .build();

// ❌ 避免：无超时配置 — 可能导致线程永久阻塞
HttpClient client = HttpClient.newHttpClient();  // 无 connectTimeout
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/data"))
    .build();                                     // 无 request timeout
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

### 虚拟线程 + HttpClient (JDK 21+)

虚拟线程与 HttpClient 是天然的搭配 — 虚拟线程在阻塞 I/O 时自动让出载体线程 (Carrier Thread):

```java
// 方式 1: 虚拟线程 + 同步 send() — 代码简单，性能优秀
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    List<Future<HttpResponse<String>>> futures = new ArrayList<>();
    for (String url : urls) {
        futures.add(executor.submit(() ->
            CLIENT.send(
                HttpRequest.newBuilder(URI.create(url)).build(),
                HttpResponse.BodyHandlers.ofString()
            )
        ));
    }
    // 收集结果
    for (var future : futures) {
        HttpResponse<String> response = future.get();
        // 处理响应
    }
}

// 方式 2: 虚拟线程作为 HttpClient 的执行器
HttpClient client = HttpClient.newBuilder()
    .executor(Executors.newVirtualThreadPerTaskExecutor())
    .build();
// sendAsync() 内部使用虚拟线程，无需 sendAsync — 直接 send() 即可
```

**为什么虚拟线程 + send() 优于 sendAsync()?**

| 对比 | `sendAsync()` + 平台线程 | `send()` + 虚拟线程 |
|------|--------------------------|---------------------|
| 代码复杂度 | CompletableFuture 链 | 直接顺序代码 |
| 并发数 | 受线程池大小限制 | 轻松百万级 |
| 调试难度 | 异步栈帧难追踪 | 完整调用栈 |
| 异常处理 | `exceptionally()` / `handle()` | try-catch |

---

## 15. 相关链接

### 本地文档

- [并发编程](../concurrency/) - 线程、异步
- [网络编程](../network/) - Socket、NIO

### 外部参考

**JEP 文档:**
- [JEP 321](/jeps/network/jep-321.md) - 标准化
- [JEP 517](/jeps/network/jep-517.md) - HTTP/3 预览

**RFC 文档:**
- [RFC 9114: HTTP/3](https://datatracker.ietf.org/doc/html/rfc9114)
- [RFC 9000: QUIC](https://datatracker.ietf.org/doc/html/rfc9000)
- [RFC 6455: WebSocket](https://datatracker.ietf.org/doc/html/rfc6455)

**技术博客:**
- [New HTTP Client](https://openjdk.org/groups/net/httpclient/intro.html)
- [HTTP/2 Support](https://inside.java/2021/07/13/http2/)
