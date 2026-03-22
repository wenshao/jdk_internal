# java.sql 模块分析

> JDBC (Java Database Connectivity)，Java 数据库连接标准 API

---

## 1. 模块概述 (Module Overview)

`java.sql` 是 Java 访问关系型数据库的标准 API 模块，定义了统一的数据库连接、SQL 执行、
结果集处理和事务管理接口。模块本身只包含接口和抽象类定义，具体实现由数据库厂商的 JDBC 驱动提供。

**源码统计**: 78 个 Java 文件 (java.sql 包 56 个 + javax.sql 包 21 个 + module-info.java)

### 模块定义 (Module Declaration)

**文件**: `src/java.sql/share/classes/module-info.java`

```java
module java.sql {
    requires transitive java.logging;
    requires transitive java.transaction.xa;
    requires transitive java.xml;

    exports java.sql;
    exports javax.sql;

    uses java.sql.Driver;  // ServiceLoader 自动发现 JDBC 驱动
}
```

关键设计:
- `requires transitive java.transaction.xa` - XA 分布式事务支持
- `requires transitive java.xml` - SQLXML 数据类型支持
- `uses java.sql.Driver` - 通过 ServiceLoader 机制自动发现和加载 JDBC 驱动

### 架构 (Architecture)

```
┌──────────────────────────────────────────────────────────┐
│                      应用代码                              │
│  DataSource / Connection / Statement / ResultSet          │
├──────────────────────────────────────────────────────────┤
│                    JDBC API 层                            │
│  java.sql (核心接口) / javax.sql (扩展接口)                │
├──────────────────────────────────────────────────────────┤
│                  DriverManager                            │
│  ServiceLoader 驱动发现 / 驱动注册 / 连接路由               │
├──────────────────────────────────────────────────────────┤
│                  JDBC 驱动实现                             │
│  MySQL Connector/J / PostgreSQL JDBC / Oracle JDBC / ... │
│  (通过 META-INF/services/java.sql.Driver 注册)            │
├──────────────────────────────────────────────────────────┤
│                     数据库                                │
│  MySQL / PostgreSQL / Oracle / SQL Server / H2 / ...     │
└──────────────────────────────────────────────────────────┘
```

---

## 2. 包结构 (Package Structure)

### java.sql (核心 JDBC API)

**核心接口 (Core Interfaces)**:

```
java.sql/
├── Driver.java                  # JDBC 驱动接口
├── DriverManager.java           # 驱动管理器 (唯一的具体类)
├── DriverAction.java            # 驱动注销回调
├── DriverPropertyInfo.java      # 驱动属性信息
├── Connection.java              # 数据库连接
├── ConnectionBuilder.java       # 连接构建器 (JDBC 4.3)
├── Statement.java               # SQL 语句
├── PreparedStatement.java       # 预编译 SQL 语句
├── CallableStatement.java       # 存储过程调用
├── ResultSet.java               # 结果集
├── ResultSetMetaData.java       # 结果集元数据
├── ParameterMetaData.java       # 参数元数据
├── DatabaseMetaData.java        # 数据库元数据
├── Savepoint.java               # 事务保存点
├── Wrapper.java                 # 包装器接口
├── SQLData.java                 # SQL 用户定义类型映射
├── SQLInput.java                # SQL 输入流
├── SQLOutput.java               # SQL 输出流
├── SQLXML.java                  # SQL XML 数据类型
├── ShardingKey.java             # 分片键 (JDBC 4.3)
├── ShardingKeyBuilder.java      # 分片键构建器 (JDBC 4.3)
│
├── # SQL 数据类型 (Data Types)
├── Array.java                   # SQL ARRAY
├── Blob.java                    # SQL BLOB (二进制大对象)
├── Clob.java                    # SQL CLOB (字符大对象)
├── NClob.java                   # SQL NCLOB (国际化字符大对象)
├── Ref.java                     # SQL REF (引用)
├── RowId.java                   # SQL ROWID
├── Struct.java                  # SQL STRUCT (结构化类型)
├── Date.java                    # SQL DATE
├── Time.java                    # SQL TIME
├── Timestamp.java               # SQL TIMESTAMP
├── Types.java                   # JDBC 类型常量
├── JDBCType.java                # JDBC 类型枚举 (JDBC 4.2)
├── SQLType.java                 # SQL 类型接口
│
├── # 异常体系 (Exception Hierarchy)
├── SQLException.java            # JDBC 异常基类 (Iterable)
├── SQLWarning.java              # SQL 警告
├── BatchUpdateException.java    # 批量更新异常
├── SQLTimeoutException.java     # 超时异常
├── SQLDataException.java        # 数据异常
├── SQLSyntaxErrorException.java          # SQL 语法错误
├── SQLIntegrityConstraintViolationException.java  # 完整性约束违反
├── SQLInvalidAuthorizationSpecException.java      # 授权错误
├── SQLNonTransientConnectionException.java        # 不可恢复连接异常
├── SQLTransientConnectionException.java           # 可重试连接异常
├── SQLTransactionRollbackException.java           # 事务回滚异常
├── SQLRecoverableException.java                   # 可恢复异常
├── SQLNonTransientException.java                  # 不可恢复异常
├── SQLTransientException.java                     # 暂时性异常
├── SQLFeatureNotSupportedException.java           # 不支持的特性
├── SQLClientInfoException.java                    # 客户端信息异常
├── DataTruncation.java          # 数据截断警告
│
├── # 其他
├── ClientInfoStatus.java        # 客户端信息状态枚举
├── PseudoColumnUsage.java       # 伪列用法枚举
├── RowIdLifetime.java           # RowId 生命周期枚举
├── SQLPermission.java           # SQL 权限
├── SQLUtils.java                # SQL 工具方法
└── package-info.java
```

### javax.sql (JDBC 扩展 API)

```
javax.sql/
├── DataSource.java              # 数据源接口 (推荐替代 DriverManager)
├── CommonDataSource.java        # 数据源公共接口
├── ConnectionPoolDataSource.java # 连接池数据源
├── PooledConnection.java        # 池化连接
├── PooledConnectionBuilder.java # 池化连接构建器 (JDBC 4.3)
├── ConnectionEvent.java         # 连接事件
├── ConnectionEventListener.java # 连接事件监听
├── StatementEvent.java          # 语句事件
├── StatementEventListener.java  # 语句事件监听
├── XAConnection.java            # XA 分布式事务连接
├── XAConnectionBuilder.java     # XA 连接构建器 (JDBC 4.3)
├── XADataSource.java            # XA 数据源
├── RowSet.java                  # 行集接口
├── RowSetInternal.java          # 行集内部接口
├── RowSetMetaData.java          # 行集元数据
├── RowSetReader.java            # 行集读取器
├── RowSetWriter.java            # 行集写入器
├── RowSetEvent.java             # 行集事件
├── RowSetListener.java          # 行集监听器
└── package-info.java
```

---

## 3. 核心接口详解 (Core Interfaces)

### 3.1 Driver (驱动接口)

**文件**: `src/java.sql/share/classes/java/sql/Driver.java`

```java
public interface Driver {
    // 连接数据库
    Connection connect(String url, Properties info) throws SQLException;

    // 判断是否支持该 URL
    boolean acceptsURL(String url) throws SQLException;

    // 获取驱动属性信息
    DriverPropertyInfo[] getPropertyInfo(String url, Properties info)
        throws SQLException;

    // 版本信息
    int getMajorVersion();
    int getMinorVersion();
    boolean jdbcCompliant();
    Logger getParentLogger() throws SQLFeatureNotSupportedException;
}
```

### 3.2 DriverManager (驱动管理器)

**文件**: `src/java.sql/share/classes/java/sql/DriverManager.java`

```java
public class DriverManager {
    // 获取连接 (主要入口)
    public static Connection getConnection(String url) throws SQLException;
    public static Connection getConnection(String url, String user,
        String password) throws SQLException;
    public static Connection getConnection(String url, Properties info)
        throws SQLException;

    // 驱动注册
    public static void registerDriver(Driver driver) throws SQLException;
    public static void deregisterDriver(Driver driver) throws SQLException;

    // 驱动自动发现 (内部方法)
    // ensureDriversInitialized() 使用 ServiceLoader<Driver> 加载驱动
    // JDBC 驱动通过 META-INF/services/java.sql.Driver 文件注册
}
```

**驱动发现流程 (Driver Discovery)**:

```
DriverManager.getConnection(url)
    │
    ▼ ensureDriversInitialized() (仅首次调用)
    │  ├── 读取 jdbc.drivers 系统属性
    │  └── ServiceLoader.load(Driver.class) 扫描驱动
    │
    ▼ 遍历已注册的 Driver
    │  对每个 Driver 调用 connect(url, info)
    │  第一个返回非 null Connection 的驱动胜出
    │
    ▼ 返回 Connection
```

**JDBC URL 格式 (URL Formats)**:

```
jdbc:mysql://localhost:3306/mydb
jdbc:postgresql://localhost:5432/mydb
jdbc:oracle:thin:@localhost:1521:orcl
jdbc:sqlserver://localhost:1433;databaseName=mydb
jdbc:h2:mem:testdb
jdbc:sqlite:mydb.db
```

### 3.3 Connection (连接)

**文件**: `src/java.sql/share/classes/java/sql/Connection.java`

```java
public interface Connection extends Wrapper, AutoCloseable {
    // 语句创建 (Statement Creation)
    Statement createStatement() throws SQLException;
    PreparedStatement prepareStatement(String sql) throws SQLException;
    CallableStatement prepareCall(String sql) throws SQLException;

    // 带参数的语句创建
    Statement createStatement(int resultSetType, int resultSetConcurrency)
        throws SQLException;
    PreparedStatement prepareStatement(String sql, int autoGeneratedKeys)
        throws SQLException;

    // 事务管理 (Transaction Management)
    void setAutoCommit(boolean autoCommit) throws SQLException;
    boolean getAutoCommit() throws SQLException;
    void commit() throws SQLException;
    void rollback() throws SQLException;
    Savepoint setSavepoint() throws SQLException;
    Savepoint setSavepoint(String name) throws SQLException;
    void rollback(Savepoint savepoint) throws SQLException;

    // 事务隔离级别
    void setTransactionIsolation(int level) throws SQLException;
    // TRANSACTION_READ_UNCOMMITTED (1)
    // TRANSACTION_READ_COMMITTED (2)
    // TRANSACTION_REPEATABLE_READ (4)
    // TRANSACTION_SERIALIZABLE (8)

    // 元数据
    DatabaseMetaData getMetaData() throws SQLException;

    // 类型创建
    Array createArrayOf(String typeName, Object[] elements) throws SQLException;
    Struct createStruct(String typeName, Object[] attributes) throws SQLException;
    SQLXML createSQLXML() throws SQLException;
    Blob createBlob() throws SQLException;
    Clob createClob() throws SQLException;
    NClob createNClob() throws SQLException;

    // 分片键 (JDBC 4.3)
    void setShardingKeyIfValid(ShardingKey shardingKey, int timeout)
        throws SQLException;

    // 连接构建器 (JDBC 4.3)
    // ConnectionBuilder createConnectionBuilder() throws SQLException;
}
```

### 3.4 Statement 层次结构 (Statement Hierarchy)

```
Statement                        ← 静态 SQL 执行
    │
    ├── PreparedStatement         ← 预编译 SQL，参数化查询
    │       │
    │       └── CallableStatement ← 存储过程/函数调用
    │
    └── (无其他子接口)
```

**PreparedStatement 示例 (Parameterized Query)**:

```java
String sql = "SELECT id, name, email FROM users WHERE status = ? AND age > ?";
try (PreparedStatement ps = conn.prepareStatement(sql)) {
    ps.setString(1, "active");
    ps.setInt(2, 18);
    try (ResultSet rs = ps.executeQuery()) {
        while (rs.next()) {
            long id = rs.getLong("id");
            String name = rs.getString("name");
            String email = rs.getString("email");
        }
    }
}
```

### 3.5 ResultSet (结果集)

**文件**: `src/java.sql/share/classes/java/sql/ResultSet.java`

```java
public interface ResultSet extends Wrapper, AutoCloseable {
    // 游标移动 (Cursor Navigation)
    boolean next() throws SQLException;
    boolean previous() throws SQLException;
    boolean first() throws SQLException;
    boolean last() throws SQLException;
    boolean absolute(int row) throws SQLException;
    boolean relative(int rows) throws SQLException;

    // 数据获取 (Data Retrieval) - 按列名或索引
    String getString(String columnLabel) throws SQLException;
    int getInt(String columnLabel) throws SQLException;
    long getLong(String columnLabel) throws SQLException;
    double getDouble(String columnLabel) throws SQLException;
    BigDecimal getBigDecimal(String columnLabel) throws SQLException;
    Date getDate(String columnLabel) throws SQLException;
    Timestamp getTimestamp(String columnLabel) throws SQLException;
    Blob getBlob(String columnLabel) throws SQLException;
    Clob getClob(String columnLabel) throws SQLException;
    Object getObject(String columnLabel) throws SQLException;
    // ... 以及对应的 getXxx(int columnIndex) 方法

    // 更新操作 (Updatable ResultSet)
    void updateString(String columnLabel, String x) throws SQLException;
    void updateRow() throws SQLException;
    void insertRow() throws SQLException;
    void deleteRow() throws SQLException;
    void moveToInsertRow() throws SQLException;

    // 元数据
    ResultSetMetaData getMetaData() throws SQLException;
}
```

**ResultSet 类型**:

| 类型 | 常量 | 特点 |
|------|------|------|
| 只进 | `TYPE_FORWARD_ONLY` | 只能向前移动游标 (默认) |
| 滚动不敏感 | `TYPE_SCROLL_INSENSITIVE` | 可双向滚动，不反映底层数据变化 |
| 滚动敏感 | `TYPE_SCROLL_SENSITIVE` | 可双向滚动，反映底层数据变化 |

---

## 4. 异常体系 (Exception Hierarchy)

```
SQLException (可迭代，支持链式异常)
├── SQLNonTransientException         ← 不可恢复错误
│   ├── SQLDataException             ← 数据错误
│   ├── SQLSyntaxErrorException      ← SQL 语法错误
│   ├── SQLIntegrityConstraintViolationException ← 约束违反
│   ├── SQLInvalidAuthorizationSpecException     ← 授权失败
│   └── SQLFeatureNotSupportedException          ← 不支持的特性
├── SQLTransientException            ← 可重试错误
│   ├── SQLTransientConnectionException ← 暂时性连接错误
│   ├── SQLTimeoutException             ← 超时
│   └── SQLTransactionRollbackException ← 事务回滚
├── SQLRecoverableException          ← 可恢复错误
├── SQLClientInfoException           ← 客户端信息错误
├── SQLWarning                       ← 警告 (非致命)
│   └── DataTruncation              ← 数据截断
└── BatchUpdateException             ← 批量更新错误
```

---

## 5. DataSource vs DriverManager

### 对比 (Comparison)

| 特性 | DriverManager | DataSource |
|------|--------------|------------|
| 连接方式 | 静态方法获取 | 接口，支持多种实现 |
| 连接池 | 不支持 | 支持 (ConnectionPoolDataSource) |
| 分布式事务 | 不支持 | 支持 (XADataSource) |
| JNDI 查找 | 不支持 | 支持 |
| 推荐程度 | 仅用于简单场景 | 生产环境推荐 |

### DataSource 使用 (DataSource Usage)

```java
// javax.sql.DataSource 接口
public interface DataSource extends CommonDataSource, Wrapper {
    Connection getConnection() throws SQLException;
    Connection getConnection(String username, String password)
        throws SQLException;
}

// 连接池数据源 (由第三方实现)
// 推荐: HikariCP, Apache DBCP, Tomcat JDBC Pool
```

---

## 6. 使用示例 (Usage Examples)

### 6.1 基本 CRUD 操作

```java
// INSERT (带自动生成键)
String insertSql = "INSERT INTO users (name, email) VALUES (?, ?)";
try (PreparedStatement ps = conn.prepareStatement(
        insertSql, Statement.RETURN_GENERATED_KEYS)) {
    ps.setString(1, "John Doe");
    ps.setString(2, "john@example.com");
    ps.executeUpdate();

    try (ResultSet keys = ps.getGeneratedKeys()) {
        if (keys.next()) {
            long id = keys.getLong(1);
        }
    }
}

// SELECT
String selectSql = "SELECT id, name, email FROM users WHERE id = ?";
try (PreparedStatement ps = conn.prepareStatement(selectSql)) {
    ps.setLong(1, userId);
    try (ResultSet rs = ps.executeQuery()) {
        if (rs.next()) {
            String name = rs.getString("name");
            String email = rs.getString("email");
        }
    }
}

// UPDATE
String updateSql = "UPDATE users SET email = ? WHERE id = ?";
try (PreparedStatement ps = conn.prepareStatement(updateSql)) {
    ps.setString(1, "new@example.com");
    ps.setLong(2, userId);
    int affected = ps.executeUpdate();
}

// DELETE
String deleteSql = "DELETE FROM users WHERE id = ?";
try (PreparedStatement ps = conn.prepareStatement(deleteSql)) {
    ps.setLong(1, userId);
    int affected = ps.executeUpdate();
}
```

### 6.2 事务管理 (Transaction Management)

```java
try (Connection conn = dataSource.getConnection()) {
    conn.setAutoCommit(false);
    try {
        // 转账: 扣款
        try (PreparedStatement ps = conn.prepareStatement(
                "UPDATE accounts SET balance = balance - ? WHERE id = ?")) {
            ps.setBigDecimal(1, amount);
            ps.setLong(2, fromId);
            ps.executeUpdate();
        }
        // 转账: 入账
        try (PreparedStatement ps = conn.prepareStatement(
                "UPDATE accounts SET balance = balance + ? WHERE id = ?")) {
            ps.setBigDecimal(1, amount);
            ps.setLong(2, toId);
            ps.executeUpdate();
        }
        conn.commit();
    } catch (SQLException e) {
        conn.rollback();
        throw e;
    }
}
```

### 6.3 批量操作 (Batch Operations)

```java
String sql = "INSERT INTO orders (product_id, quantity) VALUES (?, ?)";
try (PreparedStatement ps = conn.prepareStatement(sql)) {
    conn.setAutoCommit(false);
    for (Order order : orders) {
        ps.setLong(1, order.getProductId());
        ps.setInt(2, order.getQuantity());
        ps.addBatch();
    }
    int[] results = ps.executeBatch();
    conn.commit();
}
```

### 6.4 存储过程 (Stored Procedures)

```java
String sql = "{call get_user_by_id(?, ?)}";
try (CallableStatement cs = conn.prepareCall(sql)) {
    cs.setLong(1, userId);
    cs.registerOutParameter(2, Types.VARCHAR);
    cs.execute();
    String userName = cs.getString(2);
}
```

### 6.5 元数据查询 (Metadata Query)

```java
DatabaseMetaData meta = conn.getMetaData();

// 数据库信息
System.out.println("Database: " + meta.getDatabaseProductName());
System.out.println("Version: " + meta.getDatabaseProductVersion());
System.out.println("JDBC Version: " + meta.getJDBCMajorVersion()
    + "." + meta.getJDBCMinorVersion());

// 表信息
try (ResultSet tables = meta.getTables(
        null, null, "%", new String[]{"TABLE"})) {
    while (tables.next()) {
        System.out.println("Table: " + tables.getString("TABLE_NAME"));
    }
}

// 列信息
try (ResultSet columns = meta.getColumns(null, null, "users", null)) {
    while (columns.next()) {
        System.out.printf("%s: %s (%s)%n",
            columns.getString("COLUMN_NAME"),
            columns.getString("TYPE_NAME"),
            columns.getInt("COLUMN_SIZE"));
    }
}
```

---

## 7. 最佳实践 (Best Practices)

### 7.1 资源管理 (Resource Management)

```java
// 推荐: try-with-resources (JDBC 4.1+, AutoCloseable)
try (Connection conn = dataSource.getConnection();
     PreparedStatement ps = conn.prepareStatement(sql);
     ResultSet rs = ps.executeQuery()) {
    while (rs.next()) {
        // 处理结果
    }
} // 自动关闭: ResultSet → PreparedStatement → Connection
```

### 7.2 防止 SQL 注入 (Preventing SQL Injection)

```java
// 正确: 使用 PreparedStatement 参数化查询
String sql = "SELECT * FROM users WHERE email = ?";
PreparedStatement ps = conn.prepareStatement(sql);
ps.setString(1, userInput);  // 自动转义

// 危险: 字符串拼接 (SQL Injection 风险)
// String sql = "SELECT * FROM users WHERE email = '" + userInput + "'";
```

### 7.3 JDBC 类型映射 (Type Mapping)

| SQL 类型 | Java 类型 | JDBC 方法 |
|----------|-----------|-----------|
| CHAR/VARCHAR | String | getString() |
| INTEGER | int | getInt() |
| BIGINT | long | getLong() |
| DECIMAL/NUMERIC | BigDecimal | getBigDecimal() |
| BOOLEAN | boolean | getBoolean() |
| DATE | java.sql.Date | getDate() |
| TIMESTAMP | java.sql.Timestamp | getTimestamp() |
| BLOB | java.sql.Blob | getBlob() |
| CLOB | java.sql.Clob | getClob() |
| ARRAY | java.sql.Array | getArray() |

---

## 8. 相关链接 (Related Links)

- [JDBC 规范 (JSR 221)](https://jcp.org/en/jsr/detail?id=221)
- [JDBC API 文档](https://docs.oracle.com/en/java/javase/21/docs/api/java.sql/module-summary.html)
- [源码](https://github.com/openjdk/jdk/tree/master/src/java.sql/share/classes)
