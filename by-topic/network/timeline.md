# 网络编程演进时间线

Java 网络编程从 JDK 1.0 到 JDK 26 的完整演进历程。

---

## 时间线概览

```
JDK 1.0 ──── JDK 1.1 ──── JDK 5 ──── JDK 7 ──── JDK 9 ──── JDK 11 ──── JDK 18 ──── JDK 26
 │             │           │           │           │           │           │           │
Socket/       URL          NIO        Asynchronous HTTP/2  HTTP/3    Unix    SCTP
ServerSocket  Handler     Selector   I/O         (ALPN)    (QUIC)   Domain  (Unix)
```

---

## JDK 1.0 - 基础网络

### Socket 客户端

```java
import java.net.*;

// TCP 客户端
Socket socket = new Socket("localhost", 8080);

// 获取输入输出流
InputStream input = socket.getInputStream();
OutputStream output = socket.getOutputStream();

// 发送数据
output.write("Hello Server".getBytes());

// 接收数据
byte[] buffer = new byte[1024];
int bytesRead = input.read(buffer);
String response = new String(buffer, 0, bytesRead);

// 关闭
socket.close();
```

### ServerSocket 服务端

```java
import java.net.*;

// TCP 服务端
ServerSocket serverSocket = new ServerSocket(8080);
System.out.println("服务器启动，等待连接...");

while (true) {
    // 接受连接
    Socket socket = serverSocket.accept();
    System.out.println("客户端连接: " + socket.getInetAddress());

    // 处理连接
    try (InputStream input = socket.getInputStream();
         OutputStream output = socket.getOutputStream()) {

        // 读取请求
        byte[] buffer = new byte[1024];
        int bytesRead = input.read(buffer);

        // 发送响应
        output.write("HTTP/1.1 200 OK\r\n\r\nHello".getBytes());
    } finally {
        socket.close();
    }
}
```

### UDP Socket

```java
import java.net.*;

// UDP 发送
DatagramSocket socket = new DatagramSocket();
byte[] data = "Hello UDP".getBytes();
DatagramPacket packet = new DatagramPacket(
    data, data.length, InetAddress.getByName("localhost"), 8080
);
socket.send(packet);

// UDP 接收
DatagramSocket receiveSocket = new DatagramSocket(8080);
byte[] buffer = new byte[1024];
DatagramPacket receivePacket = new DatagramPacket(buffer, buffer.length);
receiveSocket.receive(receivePacket);
String received = new String(receivePacket.getData(), 0, receivePacket.getLength());
```

---

## JDK 1.1 - URL 和 URLConnection

### URL 类

```java
import java.net.*;

// URL 解析
URL url = new URL("https://example.com/path?query=value");

// 获取各部分
String protocol = url.getProtocol();    // https
String host = url.getHost();            // example.com
int port = url.getPort();               // 443 (默认)
String path = url.getPath();            // /path
String query = url.getQuery();          // query=value
String ref = url.getRef();             // fragment

// 读取内容
try (InputStream input = url.openStream()) {
    int data;
    while ((data = input.read()) != -1) {
        System.out.print((char) data);
    }
}
```

### HttpURLConnection

```java
// HttpURLConnection (JDK 1.1 之前)
URL url = new URL("https://example.com");
HttpURLConnection conn = (HttpURLConnection) url.openConnection();

conn.setRequestMethod("GET");
conn.setConnectTimeout(5000);
conn.setReadTimeout(5000);

int responseCode = conn.getResponseCode();
if (responseCode == HttpURLConnection.HTTP_OK) {
    try (BufferedReader br = new BufferedReader(
            new InputStreamReader(conn.getInputStream()))) {
        String line;
        while ((line = br.readLine()) != null) {
            System.out.println(line);
        }
    }
}
```

---

## JDK 5 - URLHandler

### 自定义协议处理器

```java
import java.net.*;

// 自定义 URL 协议
public class CustomURLHandler extends URLStreamHandler {
    @Override
    protected URLConnection openConnection(URL u) throws IOException {
        return new CustomURLConnection(u);
    }
}

public class CustomURLConnection extends URLConnection {
    protected CustomURLConnection(URL url) {
        super(url);
    }

    @Override
    public void connect() throws IOException {
        // 连接逻辑
    }

    @Override
    public InputStream getInputStream() throws IOException {
        // 返回输入流
        return new ByteArrayInputStream("Hello Custom".getBytes());
    }
}

// 注册处理器
URL.setURLStreamHandlerFactory(protocol -> {
    if (protocol.equals("custom")) {
        return new CustomURLHandler();
    }
    return null;
});

// 使用
URL url = new URL("custom://example.com");
String content = url.openConnection().getContent().toString();
```

---

## JDK 7 - NIO.2 异步 I/O

### AsynchronousSocketChannel

```java
import java.nio.channels.*;
import java.net.*;

// 异步 Socket 客户端
AsynchronousSocketChannel client =
    AsynchronousSocketChannel.open();

// 连接
Future<Void> connectFuture = client.connect(
    new InetSocketAddress("localhost", 8080)
);

// 等待连接完成
connectFuture.get();

// 异步读写
ByteBuffer buffer = ByteBuffer.allocate(1024);
buffer.put("Hello Server".getBytes());
buffer.flip();

Future<Integer> writeFuture = client.write(buffer);
writeFuture.get();  // 等待写入完成

buffer.clear();
Future<Integer> readFuture = client.read(buffer);
int bytesRead = readFuture.get();  // 等待读取完成
```

### AsynchronousServerSocketChannel

```java
// 异步 Socket 服务端
AsynchronousServerSocketChannel server =
    AsynchronousServerSocketChannel.open();
server.bind(new InetSocketAddress(8080));

// 接受连接
server.accept(null, new CompletionHandler<AsynchronousSocketChannel, Void>() {
    @Override
    public void completed(AsynchronousSocketChannel client, Void attachment) {
        // 处理新连接
        System.out.println("客户端连接: " + client.getRemoteAddress());

        // 继续接受下一个连接
        server.accept(null, this);
    }

    @Override
    public void failed(Throwable exc, Void attachment) {
        exc.printStackTrace();
    }
});
```

---

## JDK 9 - HTTP/2 支持

### HTTP/2 Client

```java
// JDK 9+ HTTP/2 支持
HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://example.com"))
    .version(HttpClient.Version.HTTP_2)
    .build();

client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
    .thenApply(HttpResponse::body)
    .thenAccept(System.out::println);
```

---

## JDK 11+ - HTTP Client

### 标准化 HTTP Client

```java
// JDK 11+ 标准化
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_2)
    .connectTimeout(Duration.ofSeconds(10))
    .build();

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/data"))
    .header("Content-Type", "application/json")
    .GET()
    .build();

HttpResponse<String> response = client.send(request,
    HttpResponse.BodyHandlers.ofString());
```

---

## JDK 18 - Unix Domain Sockets

### Unix Socket 支持

```java
import java.net.*;
import java.io.*;
import jdk.net.unix.*;

// Unix Domain Socket (JDK 18+)
// 仅限 Unix-like 系统

// 客户端
SocketAddress unixAddress = new UnixDomainSocketAddress("/tmp/myapp.sock");
SocketChannel channel = SocketChannel.open(unixAddress);

// 写入
ByteBuffer buffer = ByteBuffer.wrap("Hello Unix Socket".getBytes());
channel.write(buffer);

// 读取
buffer.clear();
int bytesRead = channel.read(buffer);
```

---

## 网络协议支持

### 协议支持

| 协议 | JDK | 说明 |
|------|-----|------|
| TCP | 1.0+ | Socket, ServerSocket |
| UDP | 1.0+ | DatagramSocket |
| HTTP/1.1 | 1.0+ | HttpURLConnection |
| HTTP/2 | 9+ | HttpClient |
| HTTP/3 | 26+ | HttpClient (预览) |
| SCTP | 7+ | 仅部分系统 |
| Unix Domain Socket | 16+ | Unix-like |

---

## 网络编程最佳实践

### 超时设置

```java
// ✅ 推荐: 设置超时
Socket socket = new Socket();
socket.connect(new InetSocketAddress(host, port), 5000);  // 连接超时
socket.setSoTimeout(10000);  // 读取超时

// HttpURLConnection
conn.setConnectTimeout(5000);
conn.setReadTimeout(10000);

// HttpClient
HttpClient client = HttpClient.newBuilder()
    .connectTimeout(Duration.ofSeconds(5))
    .build();
```

### 资源清理

```java
// ✅ 推荐: try-with-resources
try (Socket socket = new Socket(host, port);
     InputStream input = socket.getInputStream();
     OutputStream output = socket.getOutputStream()) {
    // 使用资源
}

// ❌ 避免: 手动清理
Socket socket = new Socket(host, port);
try {
    // 使用
} finally {
    socket.close();  // 可能抛异常
}
```

---

## 时间线总结

| 版本 | 特性 | 说明 |
|------|------|------|
| JDK 1.0 | Socket/ServerSocket | TCP/UDP 基础 |
| JDK 1.1 | URL/HttpURLConnection | HTTP 支持 |
| JDK 5 | URLHandler | 自定义协议 |
| JDK 7 | Asynchronous I/O | 异步网络 |
| JDK 9 | HTTP/2 | 多路复用 |
| JDK 11 | HTTP Client 标准化 | 新 API |
| JDK 16 | HTTP/2 ALPN | TLS 扩展 |
| JDK 18 | Unix Domain Socket | 本地 IPC |
| JDK 26 | HTTP/3 | QUIC 支持 |

---

## 相关链接

- [Networking Tutorial](https://docs.oracle.com/javase/tutorial/networking/)
- [Socket](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/net/Socket.html)
