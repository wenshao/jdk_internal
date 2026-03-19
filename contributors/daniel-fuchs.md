# Daniel Fuchs

> HTTP/3 核心开发者，JEP 517 主导者

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Daniel Fuchs |
| **组织** | Oracle |
| **GitHub** | [@dfuchs](https://github.com/dfuchs) |
| **OpenJDK** | [@dfuchs](https://openjdk.org/census#dfuchs) |
| **角色** | OpenJDK Member, JDK Reviewer |
| **Commits** | 49 |
| **主要领域** | HttpClient, HTTP/3, QUIC |
| **主导 JEP** | JEP 517: HTTP/3 for the HTTP Client API |
| **活跃时间** | 2017 - 至今 |

---

## 贡献概览

### 按类别统计

| 类别 | 数量 | 占比 |
|------|------|------|
| HTTP/3 实现 | 15 | 31% |
| HttpClient 改进 | 20 | 41% |
| Bug 修复 | 10 | 20% |
| 测试 | 4 | 8% |

### 关键成就

- **JEP 517**: HTTP/3 完整实现
- **虚拟线程支持**: HttpClient 使用虚拟线程
- **QUIC 协议栈**: 底层传输实现

---

## PR 列表

### JEP 517: HTTP/3 实现

| Issue | 标题 | 描述 |
|-------|------|------|
| 8349910 | Implement JEP 517: HTTP/3 for the HTTP Client API | **核心实现** |

### HTTP/3 优化

| Issue | 标题 | 描述 |
|-------|------|------|
| 8372159 | HttpClient SelectorManager thread could be a VirtualThread | 虚拟线程支持 |
| 8369920 | HttpClient QuicSelectorThread could be a VirtualThread | QUIC 虚拟线程 |
| 8371471 | HttpClient: Log HTTP/3 handshake failures if logging errors is enabled | 握手失败日志 |
| 8371557 | H3RequestRejectedTest.java: SSLHandshakeException | 测试修复 |

### HttpClient 改进

| Issue | 标题 | 描述 |
|-------|------|------|
| 8371366 | RawChannelTestDriver.java fails intermittently | 测试稳定性 |
| 8371722 | BufferSizePropertyClampTest.java should use Locale.ROOT | Locale 修复 |
| 8369313 | TimeoutBasic.java should accept HttpTimeoutException in cause chain | 超时处理 |
| 8369434 | AltServiceUsageTest.java fails intermittently | 测试稳定性 |
| 8368630 | H3ServerPushTest.java succeeds but fails in jtreg timeout | 超时修复 |
| 8368546 | RedirectTimeoutTest.java fails intermittently for HTTP/3 | 重定向超时 |
| 8361249 | PlainHttpConnection connection logic can be simplified | 连接逻辑简化 |
| 8359364 | EarlyOrDelayedParsing test fails intermittently | 测试稳定性 |
| 8357639 | DigestEchoClient fails intermittently | 测试稳定性 |
| 8353642 | Deprecate URL::getPermission method and networking permission classes | 废弃 API |
| 8352623 | MultiExchange should cancel exchange impl if responseFilters throws | 异常处理 |

### HTTP/2 改进

| Issue | 标题 | 描述 |
|-------|------|------|
| 8349662 | SSLTube SSLSubscriptionWrapper has potential races | 竞态条件修复 |
| 8348108 | Race condition in AggregatePublisher.AggregateSubscription | 竞态条件修复 |
| 8347995 | Race condition in FixedResponseHttpClient.java | 竞态条件修复 |
| 8348107 | HttpsTunnelAuthTest.java fails intermittently | 测试稳定性 |
| 8347597 | HttpClient: improve exception reporting when closing connection | 异常报告改进 |
| 8347373 | HTTP/2 flow control checks may count unprocessed data twice | 流控修复 |

---

## 关键贡献详解

### 1. JEP 517: HTTP/3 实现

**背景**: HTTP/3 是下一代 HTTP 协议，基于 QUIC 传输层。

**架构**:

```
java.net.http API
    │
    ▼
HttpClient (HTTP/3 支持)
    │
    ├── Http3ClientImpl
    │   ├── Http3Connection
    │   └── AltSvcProcessor
    │
    ├── QUIC Layer
    │   ├── QuicTLSEngine
    │   ├── QuicOneRttContext
    │   └── QuicVersion
    │
    └── TLS Layer
        ├── QuicCipher
        └── QuicKeyManager
```

**核心代码**:

```java
// HTTP/3 客户端使用
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_3_AUTO)  // 自动协商
    .connectTimeout(Duration.ofSeconds(10))
    .build();

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://example.com"))
    .build();

HttpResponse<String> response = client.send(
    request, HttpResponse.BodyHandlers.ofString()
);

// 检查实际使用的协议
System.out.println("Protocol: " + response.version());
```

**性能影响**:

| 场景 | HTTP/2 | HTTP/3 |
|------|--------|--------|
| 高延迟网络 | 差 | 良好 |
| 丢包环境 | 差 | 优秀 |
| 连接迁移 | 不支持 | 支持 |

### 2. HttpClient 虚拟线程支持 (JDK-8372159)

**问题**: HttpClient 的 SelectorManager 使用平台线程，内存占用高。

**解决方案**: 改用虚拟线程。

```java
// 变更前
Thread selectorThread = new Thread(this::runSelector);

// 变更后
Thread selectorThread = Thread.ofVirtual()
    .name("HttpClient-Selector")
    .unstarted(this::runSelector);
```

**影响**:

| 指标 | 平台线程 | 虚拟线程 |
|------|----------|----------|
| 内存占用 | ~1MB/线程 | ~1KB/线程 |
| 创建开销 | 高 | 低 |

### 3. HTTP/2 流控修复 (JDK-8347373)

**问题**: HTTP/2 流控检查可能重复计算未处理数据。

**解决方案**: 修正流控计算逻辑。

```java
// 变更前: 可能重复计算
int unprocessed = getUnprocessedData();
int window = getWindowSize() - unprocessed;

// 变更后: 正确计算
int unprocessed = getUnprocessedData();
int inFlight = getInFlightData();
int window = getWindowSize() - unprocessed - inFlight;
```

---

## 开发风格

Daniel 的贡献特点:

1. **协议专家**: 深入理解 HTTP/2、HTTP/3、QUIC
2. **测试驱动**: 每个改动都有充分的测试
3. **稳定性优先**: 大量修复间歇性测试失败
4. **文档完善**: 详细的 API 文档和注释

---

## 协作者

JEP 517 的主要协作者:

| 开发者 | 贡献 |
|--------|------|
| Daniel Jeliński | CUBIC 拥塞控制 |
| Volkan Yazici | API 改进 |
| Aleksei Efimov | TLS 集成 |
| Bradford Wetmore | 安全审查 |
| Jaikiran Pai | Bug 修复 |

---

## 相关链接

- [OpenJDK Changesets](https://hg.openjdk.org/jdk/jdk/user?user=dfuchs)
- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=Daniel%20Fuchs)
- [JBS Issues](https://bugs.openjdk.org/issues/?jql=assignee%20%3D%20dfuchs)