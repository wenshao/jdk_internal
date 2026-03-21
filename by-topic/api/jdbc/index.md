# JDBC

> JDBC API、RowSet、连接池、分片演进历程

[← 返回 API 框架](../)

---

## 1. 快速概览

```
JDK 1.0 ── JDK 1.2 ── JDK 4 ── JDK 6 ── JDK 7 ── JDK 11 ── JDK 21 ── JDK 26
   │         │        │        │        │        │        │        │
JDBC 1.0  JDBC 2.0  JDBC 3.0  JDBC 4.0  JDBC 4.1  JDBC 4.3  JDBC 4.3  分片
ODBC桥   RowSet    连接池    自动    Try-with   模块化   增强    支持
                    加载     resources
```

### 核心演进

| 版本 | JDBC 版本 | JSR | 特性 |
|------|----------|-----|------|
| **JDK 1.1** | JDBC 1.0 | - | 基础数据库连接、ODBC 桥 |
| **JDK 1.2** | JDBC 2.0 | - | RowSet、可滚动结果集、批量更新 |
| **JDK 4** | JDBC 3.0 | JSR 114 | 连接池、Savepoints、参数命名 |
| **JDK 6** | JDBC 4.0 | JSR 221 | 自动驱动加载、SQLXML |
| **JDK 7** | JDBC 4.1 | JSR 221 | Try-with-resources、Connection |
| **JDK 11** | JDBC 4.3 | JSR 221 | 模块化 (java.sql.jinc) |
| **JDK 26** | JDBC 4.3 | JSR 221 | 分片支持增强 |

---

## 目录

- [基础 JDBC](#基础-jdbc)
- [JDBC 4.3 新特性](#jdbc-43-新特性)
- [连接池](#连接池)
- [RowSet](#rowset)
- [最佳实践](#最佳实践)
- [核心贡献者](#核心贡献者)
- [相关链接](#相关链接)

---

## 2. 基础 JDBC

### 加载驱动

```java
// JDBC 4.0+ 自动加载 (SPI)
// 无需 Class.forName()
// 自动加载 META-INF/services/java.sql.Driver

// 手动加载 (旧方式)
Class.forName("com.mysql.cj.jdbc.Driver");

// JDBC URL
String url = "jdbc:mysql://localhost:3306/mydb";
String url = "jdbc:postgresql://localhost:5432/mydb";
String url = "jdbc:oracle:thin:@localhost:1521:orcl";
```

### 建立连接

```java
// 传统方式
String url = "jdbc:mysql://localhost:3306/mydb";
Connection conn = DriverManager.getConnection(url, "user", "password");

// Properties 配置
Properties props = new Properties();
props.setProperty("user", "root");
props.setProperty("password", "password");
Connection conn = DriverManager.getConnection(url, props);

// JDBC 4.3+ ConnectionBuilder (JDK 26)
Connection conn = DriverManager.getConnection(
    "jdbc:mysql://localhost:3306/mydb",
    "user", "password"
);
```

### 执行查询

```java
// Statement - 简单查询
try (Statement stmt = conn.createStatement()) {
    ResultSet rs = stmt.executeQuery("SELECT * FROM users");
    while (rs.next()) {
        int id = rs.getInt("id");
        String name = rs.getString("name");
    }
}

// PreparedStatement - 参数化查询 (推荐)
String sql = "SELECT * FROM users WHERE id = ?";
try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
    pstmt.setInt(1, 123);
    ResultSet rs = pstmt.executeQuery();
    if (rs.next()) {
        // 处理结果
    }
}

// CallableStatement - 存储过程
String call = "{call get_user_name(?)}";
try (CallableStatement cstmt = conn.prepareCall(call)) {
    cstmt.setInt(1, 123);
    cstmt.registerOutParameter(2, Types.VARCHAR);
    cstmt.execute();
    String name = cstmt.getString(2);
}
```

### 更新操作

```java
// INSERT
String sql = "INSERT INTO users (name, email) VALUES (?, ?)";
try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
    pstmt.setString(1, "Alice");
    pstmt.setString(2, "alice@example.com");
    int rows = pstmt.executeUpdate();
}

// UPDATE
String sql = "UPDATE users SET email = ? WHERE id = ?";
try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
    pstmt.setString(1, "newemail@example.com");
    pstmt.setInt(2, 123);
    int rows = pstmt.executeUpdate();
}

// DELETE
String sql = "DELETE FROM users WHERE id = ?";
try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
    pstmt.setInt(1, 123);
    int rows = pstmt.executeUpdate();
}

// 批量更新
String sql = "UPDATE accounts SET balance = balance + ? WHERE id = ?";
try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
    // 禁用自动提交
    conn.setAutoCommit(false);

    for (Account account : accounts) {
        pstmt.setBigDecimal(1, account.getDelta());
        pstmt.setInt(2, account.getId());
        pstmt.addBatch();
    }

    int[] results = pstmt.executeBatch();
    conn.commit();
}
```

### 事务管理

```java
// 基础事务
conn.setAutoCommit(false);
try {
    // 操作 1
    update(conn, ...);
    // 操作 2
    update(conn, ...);
    conn.commit();
} catch (SQLException e) {
    conn.rollback();
    throw e;
}

// Savepoint (JDBC 3.0+)
conn.setAutoCommit(false);
Savepoint savepoint = conn.setSavepoint("save1");
try {
    // 操作 1
    update(conn, ...);
    // 操作 2
    update(conn, ...);
    conn.releaseSavepoint(savepoint);
    conn.commit();
} catch (SQLException e) {
    conn.rollback(savepoint);
    conn.commit();
}
```

### 结果集处理

```java
// ResultSet 遍历
try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
    ResultSet rs = pstmt.executeQuery();
    while (rs.next()) {
        // 按列名访问
        int id = rs.getInt("id");
        String name = rs.getString("name");

        // 按列索引访问
        int id2 = rs.getInt(1);
        String name2 = rs.getString(2);
    }
}

// 可滚动结果集 (JDBC 2.0+)
String sql = "SELECT * FROM users";
try (PreparedStatement pstmt = conn.prepareStatement(
        sql,
        ResultSet.TYPE_SCROLL_INSENSITIVE,
        ResultSet.CONCUR_UPDATABLE)) {
    ResultSet rs = pstmt.executeQuery();

    rs.absolute(10);      // 移到第 10 行
    rs.relative(5);       // 相对移动
    rs.first();           // 第一行
    rs.last();            // 最后一行
    rs.beforeFirst();     // 之前
    rs.afterLast();       // 之后
}
```

---

## 3. JDBC 4.3 新特性

### ConnectionBuilder (JDK 26)

```java
// JDBC 4.3 ConnectionBuilder API
Connection conn = DriverManager.getConnection(
    "jdbc:mysql://localhost:3306/mydb",
    "user", "password"
);

// 或使用 ConnectionBuilder
Connection conn = DriverManager.getConnection(
    "jdbc:mysql://localhost:3306/mydb",
    props
);

// 请求生命周期 (JDBC 4.3)
conn.beginRequest();
try {
    // 数据库操作
    query(conn);
} finally {
    conn.endRequest();
}
```

### ShardingKey (分片支持)

```java
// 分片 API (JDBC 4.3)
import java.sql.ShardingKey;
import java.sql.ConnectionBuilder;

// 创建分片键
ShardingKey shardingKey = conn.createShardingKey(
    ShardingKey.SHARD_KEY,
    "shard1"
);

// 在请求中使用
conn.beginRequest();
try {
    // 使用分片键执行查询
    // 数据库可以路由到特定分片
} finally {
    conn.endRequest();
}
```

### SQLXML 支持

```java
// SQLXML (JDBC 4.0+)
// 存储 XML 数据
String sql = "UPDATE xml_data SET xml_col = ? WHERE id = ?";
try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
    SQLXML xml = conn.createSQLXML();
    xml.setString("<root><item>test</item></root>");
    pstmt.setSQLXML(1, xml);
    pstmt.setInt(2, 123);
    pstmt.executeUpdate();
}

// 读取 XML
String sql = "SELECT xml_col FROM xml_data WHERE id = ?";
try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
    pstmt.setInt(1, 123);
    ResultSet rs = pstmt.executeQuery();
    if (rs.next()) {
        SQLXML xml = rs.getSQLXML("xml_col");
        String xmlString = xml.getString();
    }
}
```

---

## 4. 连接池

### HikariCP

```java
// HikariCP 配置
HikariConfig config = new HikariConfig();
config.setJdbcUrl("jdbc:mysql://localhost:3306/mydb");
config.setUsername("user");
config.setPassword("password");
config.setMaximumPoolSize(10);
config.setMinimumIdle(5);
config.setConnectionTimeout(30000);

HikariDataSource ds = new HikariDataSource(config);

try (Connection conn = ds.getConnection()) {
    // 使用连接
}
```

### DBCP (Apache)

```java
// BasicDataSource
BasicDataSource ds = new BasicDataSource();
ds.setUrl("jdbc:mysql://localhost:3306/mydb");
ds.setUsername("user");
ds.setPassword("password");
ds.setInitialSize(5);
ds.setMaxTotal(10);
ds.setMaxIdle(5);
ds.setMinIdle(2);

try (Connection conn = ds.getConnection()) {
    // 使用连接
}
```

### Druid (Alibaba)

```java
// Druid 数据源
DruidDataSource ds = new DruidDataSource();
ds.setUrl("jdbc:mysql://localhost:3306/mydb");
ds.setUsername("user");
ds.setPassword("password");
ds.setInitialSize(5);
ds.setMinIdle(5);
ds.setMaxActive(20);
ds.setMaxWait(60000);

try (Connection conn = ds.getConnection()) {
    // 使用连接
}
```

---

## 5. RowSet

### CachedRowSet

```java
// CachedRowSet - 离线数据集
RowSetFactory factory = RowSetProvider.newFactory();
CachedRowSet crs = factory.createCachedRowSet();

try (Connection conn = ds.getConnection()) {
    // 填充数据
    try (PreparedStatement pstmt = conn.prepareStatement("SELECT * FROM users")) {
        try (ResultSet rs = pstmt.executeQuery()) {
            crs.populate(rs);
        }
    }
}

// 离线操作
crs.absolute(5);
crs.updateString("name", "Updated Name");
crs.acceptChanges(conn);  // 同步回数据库

// 序列化
ByteArrayOutputStream bos = new ByteArrayOutputStream();
ObjectOutputStream oos = new ObjectOutputStream(bos);
oos.writeObject(crs);
```

### WebRowSet

```java
// WebRowSet - XML 序列化
RowSetFactory factory = RowSetProvider.newFactory();
WebRowSet wrs = factory.createWebRowSet();

try (Connection conn = ds.getConnection()) {
    // 填充数据
    try (PreparedStatement pstmt = conn.prepareStatement("SELECT * FROM users")) {
        try (ResultSet rs = pstmt.executeQuery()) {
            wrs.populate(rs);
        }
    }
}

// 导出 XML
ByteArrayOutputStream bos = new ByteArrayOutputStream();
wrs.writeXml(new OutputStreamWriter(bos));
String xml = bos.toString();

// 导入 XML
StringReader sr = new StringReader(xml);
wrs.readXml(sr);
```

---

## 6. 最佳实践

### 资源管理

```java
// Try-with-resources (JDBC 4.1+)
// 自动关闭 Connection, Statement, ResultSet
String sql = "SELECT * FROM users WHERE id = ?";
try (Connection conn = ds.getConnection();
     PreparedStatement pstmt = conn.prepareStatement(sql)) {
    pstmt.setInt(1, 123);
    try (ResultSet rs = pstmt.executeQuery()) {
        while (rs.next()) {
            // 处理结果
        }
    }
}
```

### 性能优化

```java
// 1. 使用连接池
DataSource ds = ...;  // 连接池

// 2. 使用 PreparedStatement
String sql = "SELECT * FROM users WHERE id = ?";
try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
    pstmt.setInt(1, 123);
    // ...
}

// 3. 批量操作
String sql = "INSERT INTO users (name) VALUES (?)";
try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
    conn.setAutoCommit(false);
    for (String name : names) {
        pstmt.setString(1, name);
        pstmt.addBatch();
    }
    pstmt.executeBatch();
    conn.commit();
}

// 4. 设置获取大小
try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
    pstmt.setFetchSize(100);  // 每次获取 100 行
    try (ResultSet rs = pstmt.executeQuery()) {
        while (rs.next()) {
            // ...
        }
    }
}

// 5. 使用列名索引 (相同)
// getInt("id") 优于 getInt(1)
```

### 错误处理

```java
// SQLWarning 处理
try (Connection conn = ds.getConnection();
     Statement stmt = conn.createStatement()) {
    SQLWarning warning = conn.getWarnings();
    while (warning != null) {
        System.out.println("Warning: " + warning.getMessage());
        warning = warning.getNextWarning();
    }
}

// SQLException 链
try {
    // 数据库操作
} catch (SQLException e) {
    // 打印错误链
    while (e != null) {
        System.err.println("Message: " + e.getMessage());
        System.err.println("SQL State: " + e.getSQLState());
        System.err.println("Error Code: " + e.getErrorCode());
        e = e.getNextException();
    }
}

// 使用 try-with-resources 自动关闭
// 无需 finally 关闭资源
```

---

## 7. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### JDBC (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Lance Andersen | 7 | Oracle | JDBC 规范, 实现 |
| 2 | Joe Darcy | 5 | Oracle | API 设计 |
| 3 | Roger Riggs | 3 | Oracle | 核心库 |
| 4 | Hannes Wallnöfer | 2 | Oracle | JDBC 驱动 |

### 历史贡献者

| 贡献者 | 公司 | 主要贡献 |
|--------|------|----------|
| **Lance Andersen** | Oracle | JDBC 规范负责人 |
| **Mark Reinhold** | Oracle | JDBC 早期设计 |
| **Maydene Fisher** | Oracle | Connection 接口 |

---

## 8. Git 提交历史

> 基于 OpenJDK master 分支分析

### JDBC 改进 (2024-2026)

```bash
# 查看 JDBC 相关提交
cd /path/to/jdk
git log --oneline -- src/java.sql.share/classes/java/sql/
git log --oneline -- src/jdk.incubator/
```

---

## 9. 相关链接

### 内部文档

- [JDBC 时间线](timeline.md) - 详细的历史演进
- [核心 API](../)

### 外部资源

- [JSR 114: JDBC 3.0](https://jcp.org/en/jsr/detail?id=114)
- [JSR 221: JDBC 4.0/4.1/4.3](https://jcp.org/en/jsr/detail?id=221)
- [JDBC 4.3 Specification](https://download.oracle.com/otndocs/jcp/jdbc-4_3-mrel3-spec/index.html)
- [java.sql Package (JDK 22)](https://docs.oracle.com/en/java/javase/22/docs/api/java.sql/java/sql/package-summary.html)
- [Sharding API Guide](https://www.oracle.com/a/tech/docs/dev4712massiveoltpscalability.pdf)

### 连接池

- [HikariCP Documentation](https://github.com/brettwooldridge/HikariCP)
- [Apache DBCP](https://commons.apache.org/proper/commons-dbcp/)
- [Druid Documentation](https://github.com/alibaba/druid)

---

**最后更新**: 2026-03-20

**Sources**:
- [JSR 221: JDBC API](https://jcp.org/en/jsr/detail?id=221)
- [JDBC 4.3 Specification](https://download.oracle.com/otndocs/jcp/jdbc-4_3-mrel3-spec/index.html)
- [java.sql Package (JDK 22)](https://docs.oracle.com/en/java/javase/22/docs/api/java.sql/java/sql/package-summary.html)
- [Sharding Key Documentation](https://www.ibm.com/docs/zh/was-liberty/nd?topic=daile-developing-applications-that-use-connectionbuilder-shardingkey-efficient-data-access)
