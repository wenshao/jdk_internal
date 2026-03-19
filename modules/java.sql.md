# java.sql 模块分析

> JDBC (Java Database Connectivity)，Java 数据库连接 API

---

## 1. 模块概述

`java.sql` 是 Java 访问关系型数据库的标准 API，提供统一的数据库连接方式，支持 SQL 查询、事务管理、元数据访问等功能。

### 模块定义

**文件**: `src/java.sql/share/classes/module-info.java`

```java
module java.sql {
    requires transitive java.logging;
    requires transitive java.transaction.xa;
    requires transitive java.xml;

    exports java.sql;
    exports javax.sql;

    uses java.sql.Driver;  // ServiceLoader 加载驱动
}
```

### 架构

```
┌─────────────────────────────────────────────────────────┐
│                     应用代码                              │
│  DataSource / Connection / Statement / ResultSet        │
├─────────────────────────────────────────────────────────┤
│                   JDBC API                               │
│  java.sql / javax.sql                                   │
├─────────────────────────────────────────────────────────┤
│                 JDBC Driver                             │
│  MySQL / PostgreSQL / Oracle / SQL Server ...           │
│  (通过 ServiceLoader 自动发现)                           │
├─────────────────────────────────────────────────────────┤
│                    数据库                                │
│  MySQL / PostgreSQL / Oracle / SQL Server ...           │
└─────────────────────────────────────────────────────────┘
```

---

## 2. 核心接口

### 2.1 Driver

**源码**: `src/java.sql/share/classes/java/sql/Driver.java`

```java
public interface Driver {
    // 连接数据库
    Connection connect(String url, Properties info) throws SQLException;

    // 判断是否支持该 URL
    boolean acceptsURL(String url) throws SQLException;

    // 获取驱动属性
    DriverPropertyInfo[] getPropertyInfo(String url, Properties info);
}
```

**JDBC URL 格式**:
```
jdbc:subprotocol:subname
jdbc:mysql://localhost:3306/db
jdbc:postgresql://localhost:5432/db
jdbc:oracle:thin:@localhost:1521:orcl
```

### 2.2 Connection

**源码**: `src/java.sql/share/classes/java/sql/Connection.java`

```java
public interface Connection extends Wrapper, AutoCloseable {
    // 创建语句
    Statement createStatement() throws SQLException;
    PreparedStatement prepareStatement(String sql) throws SQLException;
    CallableStatement prepareCall(String sql) throws SQLException;

    // 事务管理
    void setAutoCommit(boolean autoCommit) throws SQLException;
    void commit() throws SQLException;
    void rollback() throws SQLException;
    Savepoint setSavepoint() throws SQLException;

    // 元数据
    DatabaseMetaData getMetaData() throws SQLException;
}
```

### 2.3 Statement

**层次结构**:
```
Statement (静态 SQL)
    ↓
PreparedStatement (预编译 SQL, 参数化)
    ↓
CallableStatement (存储过程调用)
```

**PreparedStatement 示例**:

```java
String sql = "SELECT id, name FROM users WHERE email = ?";
PreparedStatement ps = conn.prepareStatement(sql);
ps.setString(1, "user@example.com");
ResultSet rs = ps.executeQuery();
```

### 2.4 ResultSet

**源码**: `src/java.sql/share/classes/java/sql/ResultSet.java`

```java
public interface ResultSet extends Wrapper, AutoCloseable {
    // 光标移动
    boolean next() throws SQLException;
    boolean previous() throws SQLException;
    boolean absolute(int row) throws SQLException;

    // 获取数据
    String getString(String columnLabel) throws SQLException;
    int getInt(String columnLabel) throws SQLException;
    // ... 其他类型

    // 更新数据 (可更新 ResultSet)
    void updateString(String columnLabel, String x) throws SQLException;
    void insertRow() throws SQLException;
    void deleteRow() throws SQLException;
}
```

---

## 3. 数据源 (DataSource)

### 3.1 DataSource vs DriverManager

| 特性 | DriverManager | DataSource |
|------|--------------|------------|
| 连接池 | ❌ | ✓ |
| 分布式事务 | ❌ | ✓ |
| JNDI | ❌ | ✓ |
| JDK 26 推荐 | ✗ | ✓ |

### 3.2 使用 DataSource

```java
// HikariCP 示例 (推荐连接池)
HikariConfig config = new HikariConfig();
config.setJdbcUrl("jdbc:mysql://localhost:3306/mydb");
config.setUsername("user");
config.setPassword("password");
config.setMaximumPoolSize(10);

HikariDataSource ds = new HikariDataSource(config);

try (Connection conn = ds.getConnection()) {
    // 使用连接
}
```

### 3.3 JDBC 连接池

**JDK 26 内置**: 无内置连接池实现

**推荐第三方**:
- HikariCP (最快)
- Apache DBCP
- Tomcat JDBC Pool

---

## 4. JDBC 版本历史

| JDBC 版本 | JDK | 特性 |
|-----------|-----|------|
| 4.0 | JDK 6 | 自动关闭, RowSet |
| 4.1 | JDK 7 | Try-with-resources |
| 4.2 | JDK 8 | REF CURSOR, SQLException 增强 |
| 4.3 | JDK 9 | DriverManager 改进 |
| 4.4 | JDK 26 (待定) | 异步 API 计划 |

---

## 5. JDK 26 变更

### 5.1 性能改进

- `PreparedStatement` 参数绑定优化
- `ResultSet` 遍历性能提升

### 5.2 新增方法

```java
// JDBC 4.3+ 新增
Connection conn = ...;
conn.createArrayOf(type, elements);
conn.createStruct(type, attributes);

// SQL 类型支持
JDBCType.valueOf("VARCHAR");
```

### 5.3 SQLXML 支持

```java
SQLXML xml = conn.createSQLXML();
xml.setString("<root/>");
PreparedStatement ps = conn.prepareStatement("INSERT INTO data (xml_col) VALUES (?)");
ps.setSQLXML(1, xml);
```

---

## 6. 使用示例

### 6.1 基本 CRUD

```java
// INSERT
String sql = "INSERT INTO users (name, email) VALUES (?, ?)";
try (PreparedStatement ps = conn.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
    ps.setString(1, "John Doe");
    ps.setString(2, "john@example.com");
    ps.executeUpdate();

    try (ResultSet rs = ps.getGeneratedKeys()) {
        if (rs.next()) {
            long id = rs.getLong(1);
        }
    }
}

// SELECT
String sql = "SELECT id, name, email FROM users WHERE id = ?";
try (PreparedStatement ps = conn.prepareStatement(sql)) {
    ps.setLong(1, userId);
    try (ResultSet rs = ps.executeQuery()) {
        if (rs.next()) {
            String name = rs.getString("name");
            String email = rs.getString("email");
        }
    }
}

// UPDATE
String sql = "UPDATE users SET email = ? WHERE id = ?";
try (PreparedStatement ps = conn.prepareStatement(sql)) {
    ps.setString(1, "new@example.com");
    ps.setLong(2, userId);
    int updated = ps.executeUpdate();
}

// DELETE
String sql = "DELETE FROM users WHERE id = ?";
try (PreparedStatement ps = conn.prepareStatement(sql)) {
    ps.setLong(1, userId);
    int deleted = ps.executeUpdate();
}
```

### 6.2 事务管理

```java
try (Connection conn = ds.getConnection()) {
    conn.setAutoCommit(false);

    try {
        // 操作 1
        updateAccount(conn, fromId, -amount);
        // 操作 2
        updateAccount(conn, toId, amount);

        conn.commit();
    } catch (SQLException e) {
        conn.rollback();
        throw e;
    }
}
```

### 6.3 批量操作

```java
String sql = "INSERT INTO orders (product_id, quantity) VALUES (?, ?)";
try (PreparedStatement ps = conn.prepareStatement(sql)) {
    for (Order order : orders) {
        ps.setLong(1, order.getProductId());
        ps.setInt(2, order.getQuantity());
        ps.addBatch();
    }
    int[] results = ps.executeBatch();
}
```

### 6.4 存储过程

```java
String sql = "{call get_user_details(?, ?)}";
try (CallableStatement cs = conn.prepareCall(sql)) {
    cs.setLong(1, userId);
    cs.registerOutParameter(2, Types.REF_CURSOR);
    cs.execute();

    try (ResultSet rs = (ResultSet) cs.getObject(2)) {
        while (rs.next()) {
            // 处理结果
        }
    }
}
```

### 6.5 元数据查询

```java
DatabaseMetaData meta = conn.getMetaData();

// 数据库信息
String dbName = meta.getDatabaseProductName();
String dbVersion = meta.getDatabaseProductVersion();

// 表信息
try (ResultSet rs = meta.getTables(null, null, "users", new String[]{"TABLE"})) {
    while (rs.next()) {
        System.out.println("Table: " + rs.getString("TABLE_NAME"));
    }
}

// 列信息
try (ResultSet rs = meta.getColumns(null, null, "users", null)) {
    while (rs.next()) {
        String column = rs.getString("COLUMN_NAME");
        String type = rs.getString("TYPE_NAME");
        System.out.println(column + ": " + type);
    }
}
```

---

## 7. 最佳实践

### 7.1 资源管理

```java
// 推荐: Try-with-resources (JDBC 4.1+)
try (Connection conn = ds.getConnection();
     PreparedStatement ps = conn.prepareStatement(sql);
     ResultSet rs = ps.executeQuery()) {
    // 使用资源
}  // 自动关闭

// 避免: 手动关闭
Connection conn = null;
try {
    conn = ds.getConnection();
    // ...
} finally {
    if (conn != null) conn.close();  // 容易出错
}
```

### 7.2 防止 SQL 注入

```java
// 推荐: PreparedStatement
String sql = "SELECT * FROM users WHERE email = ?";
PreparedStatement ps = conn.prepareStatement(sql);
ps.setString(1, userEmail);

// 避免: 字符串拼接
String sql = "SELECT * FROM users WHERE email = '" + userEmail + "'";  // 危险!
Statement stmt = conn.createStatement();
stmt.execute(sql);
```

### 7.3 连接池配置

```java
// HikariCP 推荐配置
config.setMaximumPoolSize(10);          // 最大连接数
config.setMinimumIdle(5);                // 最小空闲连接
config.setConnectionTimeout(30000);      // 连接超时 30s
config.setIdleTimeout(600000);           // 空闲超时 10min
config.setMaxLifetime(1800000);          // 最大生命周期 30min
```

---

## 8. 相关链接

- [JDBC 规范](https://jcp.org/en/jsr/detail?id=221)
- [JDBC API 文档](https://docs.oracle.com/en/java/javase/26/docs/api/java.sql/package-summary.html)
- [源码](https://github.com/openjdk/jdk/tree/master/src/java.sql/share/classes/java/sql)
