# JDBC 演进时间线

Java 数据库连接从 JDK 1.1 到 JDK 26 的完整演进历程。

---

## 时间线概览

```
JDK 1.1 ──── JDK 4 ──── JDK 5 ──── JDK 7 ──── JDK 9 ──── JDK 11 ──── JDK 26
 │             │           │           │           │           │            │
JDBC          JDBC 4.0    自动资源   RowSet      模块化      JDBC 4.3    JDBC 4.4
ODBC Bridge   注解        管理       Generics    java.sql   连接池      增强
              元数据      try-with-
```

---

## JDBC 架构

```
┌─────────────────────────────────────────────────────────┐
│                    JDBC 架构                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Java Application                                       │
│       │                                                 │
│       ▼                                                 │
│  ┌─────────────────────────────────────────────┐        │
│  │              JDBC API                        │        │
│  │  java.sql.*                                  │        │
│  │  javax.sql.*                                 │        │
│  └─────────────────┬───────────────────────────┘        │
│                    │                                    │
│         ┌──────────┴──────────┐                         │
│         │                     │                         │
│  ┌──────▼──────┐      ┌──────▼──────┐                 │
│  │  JDBC Driver│      │Connection  │                 │
│  │  Manager    │      │Pool        │                 │
│  └──────┬──────┘      └──────┬──────┘                 │
│         │                     │                         │
│         └──────────┬──────────┘                         │
│                    │                                    │
│         ┌──────────┴──────────┐                         │
│         │                     │                         │
│  ┌──────▼──────┐      ┌──────▼──────┐                 │
│  │   MySQL     │      │  Oracle     │                 │
│  │   Driver    │      │  Driver     │                 │
│  └─────────────┘      └─────────────┘                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## JDK 1.1 - JDBC 1.x

### 基础连接

```java
import java.sql.*;

// 加载驱动 (JDBC 4.0 之前需要)
try {
    Class.forName("com.mysql.cj.jdbc.Driver");
} catch (ClassNotFoundException e) {
    e.printStackTrace();
}

// 建立连接
String url = "jdbc:mysql://localhost:3306/mydb";
String user = "username";
String password = "password";

Connection conn = DriverManager.getConnection(url, user, password);

// 执行查询
Statement stmt = conn.createStatement();
ResultSet rs = stmt.executeQuery("SELECT * FROM users");

while (rs.next()) {
    int id = rs.getInt("id");
    String name = rs.getString("name");
    System.out.println(id + ": " + name);
}

// 关闭资源
rs.close();
stmt.close();
conn.close();
```

### PreparedStatement

```java
// PreparedStatement - 防止 SQL 注入
String sql = "INSERT INTO users (name, email) VALUES (?, ?)";
PreparedStatement pstmt = conn.prepareStatement(sql);

pstmt.setString(1, "Alice");
pstmt.setString(2, "alice@example.com");

int rows = pstmt.executeUpdate();

// 查询
String query = "SELECT * FROM users WHERE id = ?";
PreparedStatement pstmt2 = conn.prepareStatement(query);
pstmt2.setInt(1, 1);
ResultSet rs = pstmt2.executeQuery();
```

### CallableStatement

```java
// CallableStatement - 存储过程
String sql = "{call get_user_info(?)}";
CallableStatement cstmt = conn.prepareCall(sql);

cstmt.setInt(1, 1);
ResultSet rs = cstmt.executeQuery();

// 带输出参数
String sql2 = "{call get_user_count(?)}";
CallableStatement cstmt2 = conn.prepareCall(sql2);
cstmt2.registerOutParameter(1, Types.INTEGER);
cstmt2.execute();
int count = cstmt2.getInt(1);
```

### Transaction

```java
// 事务管理
conn.setAutoCommit(false);

try {
    Statement stmt = conn.createStatement();
    stmt.executeUpdate("UPDATE accounts SET balance = balance - 100 WHERE id = 1");
    stmt.executeUpdate("UPDATE accounts SET balance = balance + 100 WHERE id = 2");

    conn.commit();
} catch (SQLException e) {
    conn.rollback();
    throw e;
} finally {
    conn.setAutoCommit(true);
}
```

---

## JDK 4 - JDBC 3.0

### Savepoint

```java
// Savepoint - 保存点
conn.setAutoCommit(false);

Statement stmt = conn.createStatement();
stmt.executeUpdate("UPDATE accounts SET balance = balance - 100 WHERE id = 1");

// 创建保存点
Savepoint savepoint = conn.setSavepoint("before_transfer");

try {
    stmt.executeUpdate("UPDATE accounts SET balance = balance + 100 WHERE id = 2");
    conn.commit();
} catch (SQLException e) {
    // 回滚到保存点
    conn.rollback(savepoint);
    conn.commit();
}
```

### ParameterMetaData

```java
// ParameterMetaData - 参数元数据
PreparedStatement pstmt = conn.prepareStatement(
    "SELECT * FROM users WHERE name = ? AND age > ?"
);

ParameterMetaData pmd = pstmt.getParameterMetaData();
int count = pmd.getParameterCount();
for (int i = 1; i <= count; i++) {
    int sqlType = pmd.getParameterType(i);
    String typeName = pmd.getParameterTypeName(i);
    boolean isNullable = pmd.isNullable(i) == ParameterMetaData.parameterNullable;
}
```

---

## JDK 5 - JDBC 4.0

### 自动加载驱动

```java
// JDBC 4.0+ 不需要 Class.forName()
// Driver 类在 META-INF/services/java.sql.Driver 中注册

// 直接连接
Connection conn = DriverManager.getConnection(
    "jdbc:mysql://localhost:3306/mydb",
    "username",
    "password"
);
```

### SQLXML 类型

```java
// SQLXML - XML 数据类型
SQLXML xml = conn.createSQLXML();
xml.setString("<user><name>Alice</name></user>");

PreparedStatement pstmt = conn.prepareStatement(
    "INSERT INTO users (data) VALUES (?)"
);
pstmt.setSQLXML(1, xml);
pstmt.executeUpdate();

// 读取 XML
ResultSet rs = stmt.executeQuery("SELECT data FROM users WHERE id = 1");
if (rs.next()) {
    SQLXML xmlData = rs.getSQLXML("data");
    String xmlString = xmlData.getString();
    InputStream stream = xmlData.getBinaryStream();
}
```

### RowId

```java
// RowId - 行标识符
PreparedStatement pstmt = conn.prepareStatement(
    "SELECT id, name FROM users WHERE ROWID = ?"
);

// 获取 ROWID
ResultSet rs = stmt.executeQuery("SELECT ROWID, * FROM users");
if (rs.next()) {
    RowId rowId = rs.getRowId(1);
}
```

---

## JDK 7 - JDBC 4.1

### try-with-resources

```java
// try-with-resources - 自动关闭资源
String sql = "SELECT * FROM users";

try (Connection conn = DriverManager.getConnection(url, user, password);
     Statement stmt = conn.createStatement();
     ResultSet rs = stmt.executeQuery(sql)) {

    while (rs.next()) {
        System.out.println(rs.getString("name"));
    }
}  // 自动关闭 rs, stmt, conn
```

### RowSetFactory

```java
// RowSet - 离线数据集
import javax.sql.rowset.*;

RowSetFactory factory = RowSetProvider.newFactory();

// CachedRowSet - 离线行集
CachedRowSet cachedRowSet = factory.createCachedRowSet();
cachedRowSet.setUrl("jdbc:mysql://localhost:3306/mydb");
cachedRowSet.setUsername("username");
cachedRowSet.setPassword("password");
cachedRowSet.setCommand("SELECT * FROM users");
cachedRowSet.execute();

// 离线操作
while (cachedRowSet.next()) {
    // 修改数据
    cachedRowSet.updateString("name", "Updated");
    cachedRowSet.updateRow();
}

// 同步回数据库
cachedRowSet.acceptChanges();
```

### SQLException 增强

```java
// SQLException 增强
try {
    // 数据库操作
} catch (SQLException e) {
    // 迭代异常链
    while (e != null) {
        System.out.println("Message: " + e.getMessage());
        System.out.println("SQL State: " + e.getSQLState());
        System.out.println("Error Code: " + e.getErrorCode());
        e = e.getNextException();
    }

    // 获取迭代器
    for (Throwable t : e.iterate()) {
        System.out.println(t);
    }
}
```

---

## JDK 8 - JDBC 4.2

### ResultSet 增强

```java
// JDBC 4.2 - 增强的 ResultSet
try (Statement stmt = conn.createStatement();
     ResultSet rs = stmt.executeQuery("SELECT * FROM users")) {

    // 使用 getObject 获取特定类型
    while (rs.next()) {
        // 获取 LocalDateTime
        LocalDateTime createdAt = rs.getObject("created_at", LocalDateTime.class);

        // 获取 Instant
        Instant instant = rs.getObject("timestamp", Instant.class);

        // 获取自定义类型
        User user = rs.getObject("user_data", User.class);
    }
}
```

### 大数据量处理

```java
// 流式 ResultSet - 处理大数据量
try (Connection conn = DriverManager.getConnection(url, user, password);
     Statement stmt = conn.createStatement(
         ResultSet.TYPE_FORWARD_ONLY,
         ResultSet.CONCUR_READ_ONLY)) {

    // 设置流式获取
    stmt.setFetchSize(Integer.MIN_VALUE);

    try (ResultSet rs = stmt.executeQuery("SELECT * FROM large_table")) {
        while (rs.next()) {
            // 处理每一行
        }
    }
}
```

---

## JDK 11 - JDBC 4.3

### Connection 增强

```java
// JDBC 4.3 - Connection 增强
try (Connection conn = DriverManager.getConnection(url)) {

    // 禁用 SQL 验证
    conn.beginRequest();  // JDK 9+

    try (Statement stmt = conn.createStatement()) {
        // 执行查询
    }

    conn.endRequest();  // JDK 9+

    // 网络超时
    conn.setNetworkTimeout(Executors.newSingleThreadExecutor(), 5000);

    // 检查连接有效性
    int timeout = 5;
    boolean isValid = conn.isValid(timeout);
}
```

### Sharding 支持

```java
// 分片连接示例
try (Connection conn = DriverManager.getConnection(
    "jdbc:mysql:replication://host1,host2,host3/database")) {

    // 配置复制
    // host1 - 主库 (写)
    // host2, host3 - 从库 (读)
}
```

---

## JDK 26 - JDBC 4.4

### 新增特性

```java
// JDBC 4.4 新增

// 1. 增强 SQL 支持
try (Connection conn = DriverManager.getConnection(url)) {

    // 数组参数
    String sql = "SELECT * FROM users WHERE id IN (?)";
    try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
        pstmt.setArray(1, conn.createArrayOf("INTEGER", new Object[]{1, 2, 3}));
    }

    // 2. 增强 Batch
    try (PreparedStatement pstmt = conn.prepareStatement(
        "INSERT INTO users (name) VALUES (?)")) {

        pstmt.setString(1, "Alice");
        pstmt.addBatch();

        pstmt.setString(1, "Bob");
        pstmt.addBatch();

        int[] counts = pstmt.executeLargeBatch();  // 返回 long[]
    }

    // 3. 连接池增强
    // 更好的连接池管理和监控
}
```

---

## 连接池

### HikariCP

```java
import com.zaxxer.hikari.*;

// HikariCP - 高性能 JDBC 连接池
HikariConfig config = new HikariConfig();
config.setJdbcUrl("jdbc:mysql://localhost:3306/mydb");
config.setUsername("username");
config.setPassword("password");

// 连接池配置
config.setMaximumPoolSize(10);
config.setMinimumIdle(5);
config.setConnectionTimeout(30000);
config.setIdleTimeout(600000);
config.setMaxLifetime(1800000);

HikariDataSource ds = new HikariDataSource(config);

try (Connection conn = ds.getConnection()) {
    // 使用连接
}
```

### DBCP

```java
import org.apache.commons.dbcp2.*;

// DBCP - Apache 连接池
BasicDataSource ds = new BasicDataSource();
ds.setUrl("jdbc:mysql://localhost:3306/mydb");
ds.setUsername("username");
ds.setPassword("password");

ds.setInitialSize(5);
ds.setMaxTotal(20);
ds.setMaxIdle(10);
ds.setMinIdle(5);

try (Connection conn = ds.getConnection()) {
    // 使用连接
}
```

---

## JDBC 最佳实践

### 资源管理

```java
// ✅ 推荐: try-with-resources
try (Connection conn = ds.getConnection();
     PreparedStatement pstmt = conn.prepareStatement(sql);
     ResultSet rs = pstmt.executeQuery()) {
    // 使用资源
}

// ❌ 避免: 手动关闭
Connection conn = null;
try {
    conn = ds.getConnection();
    // ...
} finally {
    if (conn != null) {
        try {
            conn.close();
        } catch (SQLException e) {
            // 忽略
        }
    }
}
```

### 批量操作

```java
// ✅ 推荐: 使用 Batch
try (Connection conn = ds.getConnection();
     PreparedStatement pstmt = conn.prepareStatement(
         "INSERT INTO users (name) VALUES (?)")) {

    conn.setAutoCommit(false);

    for (String name : names) {
        pstmt.setString(1, name);
        pstmt.addBatch();

        // 每 1000 条执行一次
        if (batchCount++ % 1000 == 0) {
            pstmt.executeBatch();
            conn.commit();
        }
    }

    pstmt.executeBatch();
    conn.commit();
}

// ❌ 避免: 单条插入
for (String name : names) {
    try (Statement stmt = conn.createStatement()) {
        stmt.executeUpdate("INSERT INTO users (name) VALUES ('" + name + "')");
    }
}
```

---

## 时间线总结

| 版本 | 特性 | 说明 |
|------|------|------|
| JDK 1.1 | JDBC 1.x | 基础 JDBC API |
| JDK 4 | JDBC 3.0 | Savepoint, ParameterMetaData |
| JDK 5 | JDBC 4.0 | 自动加载驱动, SQLXML |
| JDK 7 | JDBC 4.1 | try-with-resources, RowSetFactory |
| JDK 8 | JDBC 4.2 | ResultSet 增强, 流式结果 |
| JDK 11 | JDBC 4.3 | Connection 增强, Sharding |
| JDK 26 | JDBC 4.4 | 数组参数, 增强 Batch |

---

## 相关链接

- [JDBC API](https://docs.oracle.com/javase/8/docs/api/java/sql/package-summary.html)
- [RowSet](https://docs.oracle.com/javase/8/docs/api/javax/sql/rowset/package-summary.html)
