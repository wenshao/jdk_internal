# java.net 低层网络 API

> Socket, ServerSocket, DatagramSocket, InetAddress, URL/URI, Proxy, SSL — java.net 包核心 API

[← 返回主题索引](../)

---

## 1. 快速概览

```
JDK 1.0 ── JDK 1.1 ── JDK 1.4 ── JDK 7 ── JDK 9 ── JDK 13/15 ── JDK 16 ── JDK 21
   │         │           │         │        │         │            │        │
Socket    HttpURL-    URI       NIO.2    URL 废弃   Socket      Unix     虚拟线程
Server-   Connection  InetAddr  更新     构造器     Reimpl      Domain   + Socket
Socket                 v6                           (353/373)   Sockets  I/O
Datagram-                                                      (380)
Socket
```

### 与 concurrency/network/ 的区分

| 维度 | **net/** (本文) | **concurrency/network/** |
|------|----------------|--------------------------|
| **聚焦层次** | java.net 低层 API | NIO / HTTP Client 高层 |
| **核心类** | Socket, InetAddress, URL/URI, Proxy | SocketChannel, Selector, HttpClient |
| **编程模型** | 阻塞式 BIO | NIO 多路复用 / 异步 / 虚拟线程 |
| **典型场景** | DNS 解析、代理配置、SSL 握手、URI 解析 | 高并发服务器、HTTP/2/3、WebSocket |
| **关注点** | 协议细节、地址解析、安全 | 吞吐量、并发模型、连接池 |

### 核心演进

| 版本 | 特性 | JEP/JSR | 说明 |
|------|------|---------|------|
| **JDK 1.0** | Socket/ServerSocket/DatagramSocket | - | TCP/UDP 基础 |
| **JDK 1.1** | HttpURLConnection | - | HTTP 支持 |
| **JDK 1.4** | URI, Inet6Address | JSR 51 | URI 类、IPv6 支持 |
| **JDK 5** | Proxy, ProxySelector | - | 代理 API |
| **JDK 9** | URL 构造器废弃 | - | 推荐 URI.toURL() |
| **JDK 13** | Socket 重新实现 | JEP 353 | NioSocketImpl 替换 PlainSocketImpl |
| **JDK 15** | DatagramSocket 重新实现 | JEP 373 | NIO 后端 |
| **JDK 16** | Unix Domain Sockets | JEP 380 | AF_UNIX 通道支持 |
| **JDK 20** | URL 构造器正式废弃 | JEP 在讨论 | @Deprecated(forRemoval) |
| **JDK 21** | Virtual Threads | JEP 444 | Socket I/O 自动 yield |

---

## 目录

- [Socket 与 ServerSocket](#2-socket-与-serversocket)
- [DatagramSocket (UDP)](#3-datagramsocket-udp)
- [InetAddress 与 DNS 解析](#4-inetaddress-与-dns-解析)
- [URL 与 URI](#5-url-与-uri)
- [Proxy 代理](#6-proxy-代理)
- [网络安全: HTTPS 与 SSL](#7-网络安全-https-与-ssl)
- [Unix Domain Sockets (JEP 380)](#8-unix-domain-sockets-jep-380)
- [Socket 重新实现 (JEP 353/373)](#9-socket-重新实现-jep-353373)
- [虚拟线程与 Socket I/O](#10-虚拟线程与-socket-io)
- [HttpURLConnection (遗留 API)](#11-httpurlconnection-遗留-api)
- [Socket 选项与调优](#12-socket-选项与调优)
- [核心贡献者](#13-核心贡献者)
- [相关链接](#14-相关链接)

---

## 2. Socket 与 ServerSocket

### Socket 客户端 (TCP Client)

```java
import java.net.*;
import java.io.*;

// TCP 客户端 — 阻塞式连接
try (Socket socket = new Socket("localhost", 8080);
     InputStream input = socket.getInputStream();
     OutputStream output = socket.getOutputStream()) {

    // 发送数据 (send data)
    String request = "Hello, Server!";
    output.write(request.getBytes());
    output.flush();

    // 接收响应 (receive response)
    byte[] buffer = new byte[1024];
    int bytesRead = input.read(buffer);
    String response = new String(buffer, 0, bytesRead);
    System.out.println("Server: " + response);
}

// 带超时的连接 (connect with timeout)
Socket socket = new Socket();
socket.connect(new InetSocketAddress("example.com", 80), 5000); // 5秒超时
```

### ServerSocket 服务端 (TCP Server)

```java
import java.net.*;
import java.io.*;

// TCP 服务端 — 每连接一线程 (thread-per-connection)
try (ServerSocket serverSocket = new ServerSocket(8080)) {
    serverSocket.setReuseAddress(true);
    System.out.println("Server started on port 8080");

    while (true) {
        Socket client = serverSocket.accept(); // 阻塞等待连接
        new Thread(() -> handleClient(client)).start();
    }
}

private static void handleClient(Socket client) {
    try (client;
         BufferedReader in = new BufferedReader(
             new InputStreamReader(client.getInputStream()));
         PrintWriter out = new PrintWriter(
             client.getOutputStream(), true)) {

        String line;
        while ((line = in.readLine()) != null) {
            out.println("Echo: " + line);
        }
    } catch (IOException e) {
        e.printStackTrace();
    }
}
```

### Socket 生命周期

```
┌───────────────────────────────────────────────────┐
│              Socket 生命周期 (Lifecycle)            │
├───────────────────────────────────────────────────┤
│                                                     │
│  客户端 (Client):                                   │
│  new Socket() → connect() → getI/OStream()         │
│    → read/write → close()                           │
│                                                     │
│  服务端 (Server):                                   │
│  new ServerSocket(port) → bind() → accept()        │
│    → 返回 Socket → read/write → close()            │
│                                                     │
│  状态 (States):                                    │
│  CLOSED → BOUND → CONNECTED → CLOSE_WAIT → CLOSED │
│                                                     │
│  检查:                                              │
│  socket.isBound()      // 是否已绑定                │
│  socket.isConnected()  // 是否已连接                │
│  socket.isClosed()     // 是否已关闭                │
│  socket.isInputShutdown()   // 输入流是否关闭       │
│  socket.isOutputShutdown()  // 输出流是否关闭       │
│                                                     │
│  半关闭 (Half-close):                               │
│  socket.shutdownInput()   // 关闭输入, 保持输出     │
│  socket.shutdownOutput()  // 关闭输出, 保持输入     │
│                                                     │
└───────────────────────────────────────────────────┘
```

---

## 3. DatagramSocket (UDP)

### UDP 发送与接收

```java
import java.net.*;

// UDP 发送端 (Sender)
try (DatagramSocket socket = new DatagramSocket()) {
    byte[] data = "Hello UDP".getBytes();
    InetAddress address = InetAddress.getByName("localhost");
    DatagramPacket packet = new DatagramPacket(data, data.length, address, 9090);
    socket.send(packet);
}

// UDP 接收端 (Receiver)
try (DatagramSocket socket = new DatagramSocket(9090)) {
    byte[] buffer = new byte[1024];
    DatagramPacket packet = new DatagramPacket(buffer, buffer.length);

    socket.receive(packet); // 阻塞等待
    String message = new String(packet.getData(), 0, packet.getLength());
    System.out.println("Received: " + message +
        " from " + packet.getAddress() + ":" + packet.getPort());
}
```

### MulticastSocket (组播)

```java
import java.net.*;

// 组播接收 (Multicast receiver)
// 注意: MulticastSocket 在 JDK 14+ 标记为废弃, 推荐 DatagramChannel
InetAddress group = InetAddress.getByName("230.0.0.1");
int port = 4446;

try (MulticastSocket socket = new MulticastSocket(port)) {
    socket.joinGroup(group);

    byte[] buffer = new byte[1024];
    DatagramPacket packet = new DatagramPacket(buffer, buffer.length);
    socket.receive(packet);

    String message = new String(packet.getData(), 0, packet.getLength());
    System.out.println("Multicast: " + message);

    socket.leaveGroup(group);
}
```

### TCP vs UDP 对比

| 特性 | TCP (Socket) | UDP (DatagramSocket) |
|------|-------------|---------------------|
| **连接** | 面向连接 (connection-oriented) | 无连接 (connectionless) |
| **可靠性** | 可靠传输, 有序, 不丢包 | 不可靠, 可能丢包/乱序 |
| **传输方式** | 字节流 (stream) | 数据报 (datagram), 有边界 |
| **适用场景** | HTTP, 文件传输, 邮件 | DNS, 视频流, 游戏 |
| **开销** | 高 (三次握手, 确认机制) | 低 (无连接建立) |
| **Java 类** | Socket, ServerSocket | DatagramSocket, DatagramPacket |

---

## 4. InetAddress 与 DNS 解析

### InetAddress 基础

```java
import java.net.*;

// 获取地址 (resolve address)
InetAddress addr = InetAddress.getByName("www.example.com");
System.out.println("IP: " + addr.getHostAddress());      // 93.184.216.34
System.out.println("Host: " + addr.getHostName());        // www.example.com
System.out.println("Canonical: " + addr.getCanonicalHostName()); // 反向 DNS

// 获取所有地址 (多个 A 记录)
InetAddress[] addrs = InetAddress.getAllByName("www.google.com");
for (InetAddress a : addrs) {
    System.out.println(a.getHostAddress());
}

// 本地地址 (local address)
InetAddress localhost = InetAddress.getLocalHost();
InetAddress loopback = InetAddress.getLoopbackAddress(); // 127.0.0.1

// IPv4 vs IPv6
Inet4Address ipv4 = (Inet4Address) InetAddress.getByName("127.0.0.1");
Inet6Address ipv6 = (Inet6Address) InetAddress.getByName("::1");

// 可达性检测 (reachability check)
boolean reachable = addr.isReachable(3000); // 3秒超时, 类似 ping
```

### DNS 缓存策略 (DNS Cache Policy)

JVM 内置 DNS 缓存, 通过安全属性 (Security Property) 控制:

```java
// 查看/设置 DNS 缓存 TTL
// 正向缓存 (成功解析的结果)
// 默认值: -1 (永久缓存, 如果有 SecurityManager)
// 默认值: 30 (30秒, JDK 12+ 无 SecurityManager 时)
java.security.Security.setProperty("networkaddress.cache.ttl", "60");

// 负向缓存 (解析失败的结果)
// 默认值: 10 (10秒)
java.security.Security.setProperty("networkaddress.cache.negative.ttl", "0");
```

**通过 JVM 参数设置**:

```bash
# 在 $JAVA_HOME/conf/security/java.security 中配置:
networkaddress.cache.ttl=30        # 正向缓存 30 秒
networkaddress.cache.negative.ttl=10  # 负向缓存 10 秒

# 或通过系统属性 (System Property):
-Dsun.net.inetaddr.ttl=30
-Dsun.net.inetaddr.negative.ttl=10
```

**缓存行为对比**:

| 配置值 | 含义 | 适用场景 |
|--------|------|----------|
| `-1` | 永久缓存 (cache forever) | 有 SecurityManager 的默认值 |
| `0` | 不缓存 (no cache) | 频繁变化的 DNS, 如服务发现 |
| `30` | 缓存 30 秒 | JDK 12+ 默认值, 平衡性能与时效 |
| `N` | 缓存 N 秒 | 自定义 TTL |

**注意事项**:
- 长期运行的服务如果 DNS 永久缓存, IP 变更后无法感知 — 导致连接失败
- 微服务/容器化环境建议设置合理的 TTL (如 30-60 秒)
- `networkaddress.cache.ttl` 是安全属性, 优先级高于系统属性 `sun.net.inetaddr.ttl`

### 自定义 DNS 解析 (NameService SPI)

```java
// JDK 9+ 使用 InetAddressResolverProvider SPI (JDK 18+, JEP 418)
// 允许替换内置 DNS 解析器

// JDK 18 之前: 使用 sun.net.spi.nameservice.NameService (内部 API)
// JDK 18+: 标准化的 InetAddressResolverProvider

// 实现自定义解析器:
public class CustomResolverProvider extends InetAddressResolverProvider {
    @Override
    public InetAddressResolver get(Configuration config) {
        return new InetAddressResolver() {
            @Override
            public Stream<InetAddress> lookupByName(String host, LookupPolicy policy)
                    throws UnknownHostException {
                // 自定义解析逻辑 (如从配置文件、服务注册中心获取)
                if ("my-service".equals(host)) {
                    return Stream.of(InetAddress.getByAddress(
                        host, new byte[]{10, 0, 0, 1}));
                }
                // 回退到系统解析
                return builtinResolver.lookupByName(host, policy);
            }

            @Override
            public String lookupByAddress(byte[] addr) throws UnknownHostException {
                return builtinResolver.lookupByAddress(addr);
            }
        };
    }

    @Override
    public String name() { return "custom"; }
}
```

### NetworkInterface (网络接口)

```java
import java.net.*;
import java.util.*;

// 枚举所有网络接口 (list all network interfaces)
Enumeration<NetworkInterface> interfaces = NetworkInterface.getNetworkInterfaces();
while (interfaces.hasMoreElements()) {
    NetworkInterface ni = interfaces.nextElement();
    System.out.printf("Interface: %s (%s)%n", ni.getName(), ni.getDisplayName());
    System.out.printf("  Up: %s, Loopback: %s, Virtual: %s%n",
        ni.isUp(), ni.isLoopback(), ni.isVirtual());
    System.out.printf("  MTU: %d%n", ni.getMTU());

    // 地址列表
    Enumeration<InetAddress> addrs2 = ni.getInetAddresses();
    while (addrs2.hasMoreElements()) {
        System.out.println("  Address: " + addrs2.nextElement().getHostAddress());
    }
}
```

---

## 5. URL 与 URI

### URL 的问题 (Problems with URL)

`java.net.URL` 是 JDK 1.0 的设计, 存在严重缺陷:

```java
import java.net.*;

// 问题 1: URL.equals() 做 DNS 解析 (会阻塞!)
URL url1 = new URL("http://example.com/page");
URL url2 = new URL("http://93.184.216.34/page");
url1.equals(url2);  // 可能返回 true! 因为 equals() 解析域名比较 IP
// 这意味着:
// - equals() 会阻塞线程 (DNS 查询)
// - 结果不确定 (依赖网络状态)
// - 不能安全用作 HashMap 的 key

// 问题 2: URL.hashCode() 同样做 DNS 解析
// → HashMap<URL, V> 性能极差

// 问题 3: URL 构造器不验证语法
new URL("not a valid url"); // 不会抛异常 (某些情况下)

// 问题 4: URL 构造器在 JDK 20+ 已废弃
@Deprecated(since = "20")
public URL(String spec) throws MalformedURLException { ... }
```

### URI 推荐 (Prefer URI)

```java
import java.net.*;

// URI 不做 DNS 解析, equals() 是纯字符串比较
URI uri1 = URI.create("http://example.com/path?query=value#fragment");
URI uri2 = URI.create("http://example.com/path?query=value#fragment");
uri1.equals(uri2);  // true, 纯字符串比较, 无网络操作

// URI 解析组件 (parse components)
System.out.println("Scheme: " + uri1.getScheme());      // http
System.out.println("Host: " + uri1.getHost());            // example.com
System.out.println("Port: " + uri1.getPort());            // -1 (未指定)
System.out.println("Path: " + uri1.getPath());            // /path
System.out.println("Query: " + uri1.getQuery());          // query=value
System.out.println("Fragment: " + uri1.getFragment());    // fragment
System.out.println("Authority: " + uri1.getAuthority());  // example.com

// URI 解析与相对化 (resolve & relativize)
URI base = URI.create("http://example.com/a/b/");
URI resolved = base.resolve("c/d");          // http://example.com/a/b/c/d
URI relative = base.relativize(resolved);    // c/d

// URI → URL 转换 (推荐方式)
URL url = uri1.toURL();  // URI 先验证, 再转换

// URL 编码/解码 (URL encoding/decoding)
String encoded = URLEncoder.encode("Hello World! 你好", "UTF-8");
// Hello+World%21+%E4%BD%A0%E5%A5%BD
String decoded = URLDecoder.decode(encoded, "UTF-8");
// Hello World! 你好
```

### URL → URI 迁移指南

| 旧写法 (URL) | 新写法 (URI) | 说明 |
|--------------|-------------|------|
| `new URL(spec)` | `URI.create(spec).toURL()` | JDK 20+ URL 构造器废弃 |
| `url.equals(other)` | `uri.equals(other)` | 避免 DNS 解析 |
| `url.openConnection()` | `HttpClient.send(request, ...)` | 推荐用 HttpClient |
| `url.openStream()` | `URI.create(s).toURL().openStream()` | 过渡写法 |

---

## 6. Proxy 代理

### Proxy 类型 (Proxy Types)

```java
import java.net.*;

// 创建 Proxy 对象
// HTTP 代理
Proxy httpProxy = new Proxy(Proxy.Type.HTTP,
    new InetSocketAddress("proxy.example.com", 8080));

// SOCKS 代理
Proxy socksProxy = new Proxy(Proxy.Type.SOCKS,
    new InetSocketAddress("socks.example.com", 1080));

// 直连 (无代理)
Proxy direct = Proxy.NO_PROXY;
```

### 通过 Proxy 连接

```java
// Socket 使用 SOCKS 代理
Socket socket = new Socket(socksProxy);
socket.connect(new InetSocketAddress("target.example.com", 80));

// URL 使用 HTTP 代理
URL url = URI.create("http://example.com").toURL();
URLConnection conn = url.openConnection(httpProxy);

// HTTP 代理认证 (Proxy Authentication)
Authenticator.setDefault(new Authenticator() {
    @Override
    protected PasswordAuthentication getPasswordAuthentication() {
        if (getRequestorType() == RequestorType.PROXY) {
            return new PasswordAuthentication("user", "pass".toCharArray());
        }
        return null;
    }
});
```

### ProxySelector (代理选择器)

```java
import java.net.*;
import java.util.*;

// 系统默认代理选择器 (读取系统配置)
ProxySelector defaultSelector = ProxySelector.getDefault();
List<Proxy> proxies = defaultSelector.select(URI.create("http://example.com"));

// 自定义 ProxySelector
ProxySelector.setDefault(new ProxySelector() {
    @Override
    public List<Proxy> select(URI uri) {
        if (uri.getHost().endsWith(".internal.com")) {
            return List.of(Proxy.NO_PROXY);  // 内网直连
        }
        return List.of(new Proxy(Proxy.Type.HTTP,
            new InetSocketAddress("proxy.corp.com", 8080)));
    }

    @Override
    public void connectFailed(URI uri, SocketAddress sa, IOException e) {
        System.err.println("Proxy connection failed: " + uri);
    }
});
```

### 系统代理属性 (System Proxy Properties)

```bash
# HTTP 代理
-Dhttp.proxyHost=proxy.example.com
-Dhttp.proxyPort=8080
-Dhttp.nonProxyHosts="localhost|*.internal.com|10.*"

# HTTPS 代理
-Dhttps.proxyHost=proxy.example.com
-Dhttps.proxyPort=8443

# SOCKS 代理
-DsocksProxyHost=socks.example.com
-DsocksProxyPort=1080
-Djava.net.socks.username=user
-Djava.net.socks.password=pass

# FTP 代理
-Dftp.proxyHost=proxy.example.com
-Dftp.proxyPort=8080

# nonProxyHosts: 不使用代理的主机列表
# 支持 * 通配符, 使用 | 分隔
-Dhttp.nonProxyHosts="localhost|127.0.0.1|*.corp.com"
```

---

## 7. 网络安全: HTTPS 与 SSL

### SSLSocket (SSL/TLS 加密连接)

```java
import javax.net.ssl.*;
import java.net.*;

// 创建 SSL Socket
SSLSocketFactory factory = (SSLSocketFactory) SSLSocketFactory.getDefault();
try (SSLSocket sslSocket = (SSLSocket) factory.createSocket("example.com", 443)) {
    // 配置 TLS 版本
    sslSocket.setEnabledProtocols(new String[]{"TLSv1.3", "TLSv1.2"});

    // 配置密码套件 (cipher suites)
    sslSocket.setEnabledCipherSuites(new String[]{
        "TLS_AES_256_GCM_SHA384",
        "TLS_AES_128_GCM_SHA256"
    });

    // 开始握手 (handshake)
    sslSocket.startHandshake();

    // 获取会话信息
    SSLSession session = sslSocket.getSession();
    System.out.println("Protocol: " + session.getProtocol());       // TLSv1.3
    System.out.println("Cipher: " + session.getCipherSuite());
    System.out.println("Peer: " + session.getPeerPrincipal());

    // 正常读写...
    var out = sslSocket.getOutputStream();
    out.write("GET / HTTP/1.1\r\nHost: example.com\r\n\r\n".getBytes());
    out.flush();
}
```

### SSLContext 配置

```java
import javax.net.ssl.*;
import java.security.*;

// 自定义 SSLContext
SSLContext sslContext = SSLContext.getInstance("TLSv1.3");

// 加载信任库 (TrustStore) — 信任哪些 CA 证书
KeyStore trustStore = KeyStore.getInstance("JKS");
try (var fis = new FileInputStream("/path/to/truststore.jks")) {
    trustStore.load(fis, "changeit".toCharArray());
}
TrustManagerFactory tmf = TrustManagerFactory.getInstance("PKIX");
tmf.init(trustStore);

// 加载密钥库 (KeyStore) — 客户端证书 (双向 TLS / mTLS)
KeyStore keyStore = KeyStore.getInstance("PKCS12");
try (var fis = new FileInputStream("/path/to/keystore.p12")) {
    keyStore.load(fis, "password".toCharArray());
}
KeyManagerFactory kmf = KeyManagerFactory.getInstance("SunX509");
kmf.init(keyStore, "password".toCharArray());

// 初始化 SSLContext
sslContext.init(kmf.getKeyManagers(), tmf.getTrustManagers(), new SecureRandom());

// 使用自定义 SSLContext 创建 Socket
SSLSocketFactory factory = sslContext.getSocketFactory();
SSLSocket socket = (SSLSocket) factory.createSocket("example.com", 443);
```

### 证书验证 (Certificate Verification)

```java
// 默认行为: JVM 使用 cacerts 信任库验证服务器证书
// 位置: $JAVA_HOME/lib/security/cacerts

// 自定义 HostnameVerifier (用于 HTTPS)
HttpsURLConnection.setDefaultHostnameVerifier((hostname, session) -> {
    // 自定义主机名验证逻辑
    return hostname.endsWith(".trusted.com");
});

// 禁用证书验证 (仅用于开发/测试, 生产环境绝不可用!)
TrustManager[] trustAll = new TrustManager[]{
    new X509TrustManager() {
        public void checkClientTrusted(X509Certificate[] chain, String authType) {}
        public void checkServerTrusted(X509Certificate[] chain, String authType) {}
        public X509Certificate[] getAcceptedIssuers() { return new X509Certificate[0]; }
    }
};
SSLContext unsafeContext = SSLContext.getInstance("TLS");
unsafeContext.init(null, trustAll, new SecureRandom());
// ⚠️ 警告: 这会信任所有证书, 容易遭受中间人攻击 (MITM)
```

### TLS 版本演进

| TLS 版本 | JDK 支持 | 状态 | 说明 |
|----------|---------|------|------|
| SSL 3.0 | JDK 1.0-8 | 已禁用 | POODLE 漏洞 |
| TLS 1.0 | JDK 1.4-15 | JDK 16 默认禁用 | 安全性不足 |
| TLS 1.1 | JDK 5-15 | JDK 16 默认禁用 | 安全性不足 |
| TLS 1.2 | JDK 7+ | 推荐 | 广泛使用 |
| TLS 1.3 | JDK 11+ | 推荐 (最佳) | 更快握手, 更安全 |

---

## 8. Unix Domain Sockets (JEP 380)

**JDK 16+**: 为 `SocketChannel` 和 `ServerSocketChannel` 添加 AF_UNIX 支持。

### 优势对比

| 方面 | TCP Loopback (127.0.0.1) | Unix Domain Socket |
|------|--------------------------|-------------------|
| **性能** | 经过完整网络栈 | 绕过网络栈, 更快 |
| **安全** | 任何进程可连接端口 | 文件系统权限控制 |
| **资源** | 占用端口号 | 文件路径, 不占端口 |
| **可移植** | 所有平台 | Linux, macOS, Windows 10+ |
| **适用场景** | 跨网络通信 | 同机进程间通信 (IPC) |

### UnixDomainSocketAddress

```java
import java.net.UnixDomainSocketAddress;
import java.nio.channels.*;
import java.nio.ByteBuffer;
import java.nio.file.*;

// 服务端 (Server)
Path socketPath = Path.of("/tmp/my-server.sock");
Files.deleteIfExists(socketPath); // 清理残留 socket 文件
UnixDomainSocketAddress address = UnixDomainSocketAddress.of(socketPath);

try (ServerSocketChannel server = ServerSocketChannel.open(StandardProtocolFamily.UNIX)) {
    server.bind(address);
    System.out.println("Listening on " + socketPath);

    try (SocketChannel client = server.accept()) {
        ByteBuffer buffer = ByteBuffer.allocate(1024);
        client.read(buffer);
        buffer.flip();

        byte[] data = new byte[buffer.remaining()];
        buffer.get(data);
        System.out.println("Received: " + new String(data));

        // 回复
        client.write(ByteBuffer.wrap("ACK".getBytes()));
    }
} finally {
    Files.deleteIfExists(socketPath); // 清理
}

// 客户端 (Client)
UnixDomainSocketAddress address = UnixDomainSocketAddress.of(Path.of("/tmp/my-server.sock"));
try (SocketChannel channel = SocketChannel.open(StandardProtocolFamily.UNIX)) {
    channel.connect(address);
    channel.write(ByteBuffer.wrap("Hello Unix Domain!".getBytes()));

    ByteBuffer response = ByteBuffer.allocate(256);
    channel.read(response);
    response.flip();
    System.out.println("Response: " + new String(response.array(), 0, response.limit()));
}
```

### 典型用途

- **容器化环境**: Docker 中通过挂载 socket 文件实现宿主机通信 (如 Docker API `/var/run/docker.sock`)
- **数据库连接**: PostgreSQL, MySQL 支持 Unix socket 连接, 比 TCP 更快
- **微服务 sidecar**: 同 Pod 内的服务间通信

---

## 9. Socket 重新实现 (JEP 353/373)

### JEP 353: 重新实现旧版 Socket API (JDK 13)

JDK 13 用全新的 `NioSocketImpl` 替换了 `PlainSocketImpl`:

```
┌─────────────────────────────────────────────────────────────────┐
│                Socket 实现演进 (Implementation Evolution)        │
├─────────────────────────────┬───────────────────────────────────┤
│ 旧实现 (PlainSocketImpl)     │ 新实现 (NioSocketImpl)            │
├─────────────────────────────┼───────────────────────────────────┤
│ JDK 1.0 遗留代码             │ JDK 13 全新实现                   │
│ Java + C 混合               │ 纯 Java (基于 NIO 内部机制)       │
│ 依赖平台原生锁               │ Java ReentrantLock               │
│ 脆弱, 难以维护              │ 清晰, 易于维护                    │
│ 不兼容虚拟线程               │ 天然兼容虚拟线程                  │
│ Thread.interrupt() 行为不一致│ 统一的中断行为                    │
└─────────────────────────────┴───────────────────────────────────┘
```

**NioSocketImpl 关键改进**:
- 使用 `sun.nio.ch.NioSocketImpl` 替换 `java.net.PlainSocketImpl`
- 阻塞 I/O 操作在内部使用 NIO 的 `java.nio.channels` 机制
- 当虚拟线程在 Socket 上阻塞时, 底层平台线程可以释放去执行其他任务
- `Thread.interrupt()` 在阻塞 I/O 期间的行为更加一致

### JEP 373: 重新实现旧版 DatagramSocket API (JDK 15)

与 JEP 353 相同思路, 将 `DatagramSocket` 和 `MulticastSocket` 的底层实现替换为基于 NIO 的版本。

```java
// 对应用程序完全透明, 无需代码修改
// JDK 13 可通过系统属性回退到旧实现 (JDK 17+ 已移除回退选项):
// -Djdk.net.usePlainSocketImpl=true  // 仅 JDK 13-16 可用
```

---

## 10. 虚拟线程与 Socket I/O

### 虚拟线程上的 Socket 行为 (JDK 21+)

虚拟线程 (Virtual Threads, JEP 444) 改变了传统阻塞式 Socket I/O 的运行机制:

```
┌──────────────────────────────────────────────────────────────┐
│          虚拟线程 + Socket I/O 工作原理                       │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  传统线程 (Platform Thread):                                   │
│  socket.read() → 平台线程阻塞 → OS 线程阻塞 → 资源浪费       │
│                                                                │
│  虚拟线程 (Virtual Thread):                                    │
│  socket.read() → 虚拟线程 park → 平台线程释放 → 执行其他任务  │
│              ↓                                                 │
│          数据就绪 → 虚拟线程 unpark → 继续执行                 │
│                                                                │
│  关键: NioSocketImpl 内部使用 NIO 实现阻塞语义                 │
│  虚拟线程不会真正阻塞底层平台线程                              │
│                                                                │
└──────────────────────────────────────────────────────────────┘
```

### 编程模型对比

```java
// 传统模型: 每连接一线程, 受限于平台线程数 (通常几千个)
try (ServerSocket server = new ServerSocket(8080)) {
    ExecutorService pool = Executors.newFixedThreadPool(200); // 最多 200 并发
    while (true) {
        Socket client = server.accept();
        pool.submit(() -> handleClient(client));
    }
}

// 虚拟线程模型: 每连接一虚拟线程, 可支持数十万并发
try (ServerSocket server = new ServerSocket(8080)) {
    while (true) {
        Socket client = server.accept();
        Thread.startVirtualThread(() -> handleClient(client));
    }
}

// 或使用虚拟线程执行器
try (ServerSocket server = new ServerSocket(8080);
     var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    while (true) {
        Socket client = server.accept();
        executor.submit(() -> handleClient(client));
    }
}
```

### 虚拟线程 + Socket 注意事项

| 注意点 | 说明 |
|--------|------|
| **synchronized 块中的 I/O** | 虚拟线程在 `synchronized` 中做 Socket I/O 会 pin 住平台线程; 改用 `ReentrantLock` |
| **JNI 调用** | 原生方法中的阻塞不会自动 yield |
| **连接数限制** | 虽然虚拟线程很轻量, 但仍受 OS 文件描述符限制 (`ulimit -n`) |
| **DNS 解析** | `InetAddress.getByName()` 在虚拟线程上仍会短暂 pin (内部有 synchronized) |

---

## 11. HttpURLConnection (遗留 API)

> **推荐**: JDK 11+ 请使用 `java.net.http.HttpClient` (参见 [concurrency/network/](../concurrency/network/))

### 基础用法

```java
import java.net.*;
import java.io.*;

// GET 请求
URL url = URI.create("https://api.example.com/data").toURL(); // JDK 20+ 推荐写法
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
        }
    }
} finally {
    conn.disconnect();
}

// POST 请求
URL url = URI.create("https://api.example.com/form").toURL();
HttpURLConnection conn = (HttpURLConnection) url.openConnection();
conn.setRequestMethod("POST");
conn.setDoOutput(true);
conn.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");

try (OutputStream out = conn.getOutputStream()) {
    out.write("name=John&age=30".getBytes());
}
int responseCode = conn.getResponseCode();
```

### HttpURLConnection 的缺陷

| 缺陷 | 说明 |
|------|------|
| **API 笨拙** | 需要手动管理流和连接 |
| **不支持 HTTP/2** | 仅 HTTP/1.1 |
| **异步困难** | 原生不支持异步请求 |
| **不可变请求** | 无法复用 Request 对象 |
| **流式处理差** | 大响应体处理不优雅 |

---

## 12. Socket 选项与调优

### TCP Socket 选项

```java
// Socket 配置选项 (Socket Options)
Socket socket = new Socket();

// 超时设置 (Timeouts)
socket.setSoTimeout(5000);            // 读超时 (read timeout), 0=无限
socket.connect(addr, 5000);           // 连接超时 (connect timeout)

// 性能调优 (Performance Tuning)
socket.setTcpNoDelay(true);           // 禁用 Nagle 算法 (低延迟场景)
socket.setKeepAlive(true);            // 启用 TCP Keep-Alive
socket.setReceiveBufferSize(65536);   // 接收缓冲区 (receive buffer)
socket.setSendBufferSize(65536);      // 发送缓冲区 (send buffer)

// 地址复用 (Address Reuse)
socket.setReuseAddress(true);         // 允许重用 TIME_WAIT 状态的地址

// Linger 选项 (关闭行为)
socket.setSoLinger(true, 5);          // close() 最多等待 5 秒发送剩余数据

// 流量类型 (Traffic Class / DSCP)
socket.setTrafficClass(0x10);         // 低延迟 DSCP 标记

// OOB 数据 (Out-of-Band)
socket.setOOBInline(true);            // 允许接收紧急数据

// ServerSocket 选项
ServerSocket serverSocket = new ServerSocket();
serverSocket.setReuseAddress(true);
serverSocket.setReceiveBufferSize(65536);
serverSocket.setSoTimeout(5000);      // accept() 超时
```

### 扩展 Socket 选项 (JDK 9+)

```java
import java.net.*;
import jdk.net.ExtendedSocketOptions;

// JDK 9+ 扩展选项
socket.setOption(StandardSocketOptions.SO_KEEPALIVE, true);
socket.setOption(StandardSocketOptions.TCP_NODELAY, true);

// 获取所有支持的选项
Set<SocketOption<?>> options = socket.supportedOptions();

// JDK 11+: TCP Keep-Alive 细粒度控制 (Linux)
socket.setOption(ExtendedSocketOptions.TCP_KEEPIDLE, 60);     // 空闲 60 秒后开始探测
socket.setOption(ExtendedSocketOptions.TCP_KEEPINTERVAL, 10); // 每 10 秒探测一次
socket.setOption(ExtendedSocketOptions.TCP_KEEPCOUNT, 5);     // 探测 5 次后断开
```

### 常见调优场景

| 场景 | 推荐配置 | 原因 |
|------|---------|------|
| **低延迟 RPC** | `TCP_NODELAY=true` | 禁用 Nagle 算法, 减少小包延迟 |
| **大文件传输** | 大缓冲区 + Nagle 开 | 减少系统调用次数 |
| **长连接服务** | `SO_KEEPALIVE=true` | 检测死连接 |
| **服务重启** | `SO_REUSEADDR=true` | 避免 "Address already in use" |
| **超时控制** | `SO_TIMEOUT` + 连接超时 | 避免无限阻塞 |

---

## 13. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### java.net 相关 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | [Alan Bateman](/by-contributor/profiles/alan-bateman.md) | 20+ | Oracle | NIO, NIO.2, Unix Domain Sockets (JEP 380), Virtual Threads |
| 2 | [Chris Hegarty](/by-contributor/profiles/chris-hegarty.md) | 25+ | Oracle | HTTP Client (JEP 321), 网络基础 |
| 3 | [Daniel Fuchs](/by-contributor/profiles/daniel-fuchs.md) | 8+ | Oracle | HTTP Client, 网络安全 |
| 4 | Michael McMahon | 10+ | Oracle | Socket 重新实现 (JEP 353/373), HTTP Client |

### 历史贡献者

| 贡献者 | 组织 | 主要贡献 |
|--------|------|----------|
| **Alan Bateman** | Oracle | NIO.2 (JSR 203), JEP 380 Unix Domain Sockets |
| **Chris Hegarty** | Oracle | HTTP Client API 实现 |
| **Michael McMahon** | Oracle | Socket/DatagramSocket 重新实现 |

---

## 14. 相关链接

### 内部文档

- [并发网络编程](../concurrency/network/) - NIO, HTTP Client, 虚拟线程网络编程
- [I/O 处理](../api/io/) - 文件 I/O
- [并发编程](../concurrency/concurrency/) - 并发基础

### 外部资源

- [JEP 353: Reimplement the Legacy Socket API](https://openjdk.org/jeps/353)
- [JEP 373: Reimplement the Legacy DatagramSocket API](https://openjdk.org/jeps/373)
- [JEP 380: Unix-Domain Socket Channels](https://openjdk.org/jeps/380)
- [JEP 418: Internet-Address Resolution SPI](https://openjdk.org/jeps/418)
- [JEP 444: Virtual Threads](https://openjdk.org/jeps/444)
- [Java Networking Tutorial](https://docs.oracle.com/javase/tutorial/networking/)
- [RFC 6455: WebSocket Protocol](https://tools.ietf.org/html/rfc6455)

---

**最后更新**: 2026-03-22
