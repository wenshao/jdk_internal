# HTTP 客户端演进时间线

从 HttpURLConnection 到 HTTP/3 的演进历程。

---

## 时间线概览

```
JDK 8 ───── JDK 11 ───── JDK 16 ───── JDK 21 ───── JDK 26
│              │              │              │              │
HttpURLConnection  HTTP Client   HTTP/2        HTTP Client   HTTP/3
(旧 API)         (新 API)      支持          正式版        (正式)
```

---

## JDK 8 及之前 - HttpURLConnection

### 特点

- 同步阻塞 API
- 支持 HTTP/1.0 和 HTTP/1.1
- 连接池管理复杂

```java
URL url = new URL("https://example.com");
HttpURLConnection conn = (HttpURLConnection) url.openConnection();
conn.setRequestMethod("GET");

try (BufferedReader br = new BufferedReader(
        new InputStreamReader(conn.getInputStream()))) {
    String line;
    while ((line = br.readLine()) != null) {
        System.out.println(line);
    }
}
```

### 问题

- API 设计陈旧
- 不支持 HTTP/2
- 超时配置复杂
- 异步请求困难

---

## JDK 11 - HTTP Client (新 API)

### 特点

- 同步 + 异步 API
- 支持 HTTP/2
- WebSocket 支持
- 响应式流

```java
// 同步请求
HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://example.com"))
    .build();
HttpResponse<String> response = client.send(request, BodyHandlers.ofString());

// 异步请求
client.sendAsync(request, BodyHandlers.ofString())
    .thenApply(HttpResponse::body)
    .thenAccept(System.out::println);
```

### 模块

```java
module com.example {
    requires java.net.http;
}
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
HttpResponse<String> response = client.send(request, ...);
```

---

## JDK 21 - HTTP Client 正式版

### 变化

- 从 `jdk.incubator.httpclient` 移至 `java.net.http`
- 标准化完成

---

## JDK 26 - HTTP/3 支持

### 特性

- 基于 QUIC 协议
- 0-RTT 连接恢复
- 内置拥塞控制 (CUBIC)

```java
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_3)  // 新增
    .build();

// 自动协商 HTTP/3
HttpResponse<String> response = client.send(request, ...);
```

### HTTP/3 vs HTTP/2

| 特性 | HTTP/2 | HTTP/3 |
|------|--------|--------|
| 传输层 | TCP | QUIC (UDP) |
| 队头阻塞 | 有 | 无 |
| 连接建立 | 3-RTT | 1-RTT |
| 连接迁移 | 困难 | 原生支持 |

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

---

## 使用示例

### 基本请求

```java
HttpClient client = HttpClient.newBuilder()
    .connectTimeout(Duration.ofSeconds(10))
    .build();

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/data"))
    .header("Authorization", "Bearer token")
    .GET()
    .build();

HttpResponse<String> response = client.send(request,
    HttpResponse.BodyHandlers.ofString());
```

### POST JSON

```java
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/users"))
    .header("Content-Type", "application/json")
    .POST(BodyPublishers.ofString(jsonString))
    .build();
```

### 异步请求

```java
client.sendAsync(request, BodyHandlers.ofString())
    .thenApply(HttpResponse::body)
    .thenAccept(this::process)
    .exceptionally(e -> {
        e.printStackTrace();
        return null;
    });
```

---

## 性能对比

### 连接建立时间

| 协议 | RTT 次数 | 时间 |
|------|---------|------|
| HTTP/1.1 | 3-RTT | ~150ms |
| HTTP/2 | 3-RTT | ~150ms |
| HTTP/3 | 1-RTT | ~50ms |

### 吞吐量

```
HTTP/1.1: 100 req/s
HTTP/2:  500 req/s (多路复用)
HTTP/3:  800 req/s (UDP, 无队头阻塞)
```

---

## 时间线总结

| 版本 | 特性 | 状态 |
|------|------|------|
| JDK 1.0 | HttpURLConnection | 标准库 |
| JDK 9 | HTTP Client (孵化) | 实验性 |
| JDK 10 | HTTP Client (孵化) | 实验性 |
| JDK 11 | HTTP Client (标准) | 标准库 |
| JDK 16 | HTTP/2 支持 | 标准库 |
| JDK 21 | HTTP Client 正式 | 标准库 |
| JDK 26 | HTTP/3 支持 | 标准库 |

---

## 迁移指南

### HttpURLConnection → HttpClient

```java
// 旧代码
URL url = new URL("https://example.com");
HttpURLConnection conn = (HttpURLConnection) url.openConnection();

// 新代码
HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://example.com"))
    .GET()
    .build();
HttpResponse<String> response = client.send(request, BodyHandlers.ofString());
```

---

## 相关链接

- [HTTP Client 文档](https://docs.oracle.com/en/java/javase/11/docs/api/java.net.http/java/net/http/package-summary.html)
- [HTTP/3 深度分析](../../by-version/jdk26/deep-dive/http3-implementation.md)
- [JEP 321: HTTP Client](https://openjdk.org/jeps/321)
- [JEP 517: HTTP/3](https://openjdk.org/jeps/517)
