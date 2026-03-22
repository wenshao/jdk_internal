# Text Blocks 深入 (JEP 378)

Text Blocks (文本块) 是 JDK 15 正式引入的多行字符串字面量 (multi-line string literals)。

[← 返回 Project Amber 概览](index.md)

---

## 演进历程

```
JEP 355 (Preview)     JDK 13   Text Blocks 第一预览
    |
JEP 368 (2nd Preview) JDK 14   Text Blocks 第二预览 (新增 \s 和 \ 转义)
    |
JEP 378 (Final)       JDK 15   Text Blocks 正式发布
```

---

## 缩进管理 (Indentation Management)

```java
// Text Block 的缩进由**结束分隔符 (closing delimiter) 的位置**决定
// 编译器会自动调用 String::stripIndent 移除"附带缩进" (incidental whitespace)

// 示例 1: 结束符与内容同级 -> 无附带缩进
String s1 = """
    line 1
    line 2
    """;
// 等价于 "line 1\nline 2\n"  (4 个空格被视为附带缩进, 被移除)

// 示例 2: 结束符更靠左 -> 保留部分缩进
String s2 = """
    line 1
    line 2
""";
// 等价于 "    line 1\n    line 2\n"  (结束符在第 0 列, 所以 4 个空格保留)

// 示例 3: 结束符更靠右 -> 不影响缩进移除
String s3 = """
    line 1
    line 2
        """;
// 等价于 "line 1\nline 2\n"  (最小缩进仍是 4 个空格)

// String::stripIndent() 算法:
// 1. 找到所有非空行的最小公共前导空白 (common leading whitespace)
// 2. 移除每行的该前缀
// 3. 移除尾部空白 (trailing whitespace from each line)
```

---

## 转义序列 (Escape Sequences)

```java
// \s - 保留尾部空格 (preserve trailing space)
// 普通 text block 会移除每行尾部空白, \s 阻止这种移除
String table = """
    Name   \s
    Alice  \s
    Bob    \s
    """;
// 每行保留了尾部的空格 (不含 \s 本身, \s 转义为一个空格)

// \ - 行连续符 (line continuation), 取消行尾换行
String longLine = """
    This is a very long line that \
    we want to keep on a single line \
    in the output.""";
// 等价于 "This is a very long line that we want to keep on a single line in the output."
// 注意: \ 后面不能有空格!

// 组合使用
String poem = """
    Roses are red,\s\s\s
    Violets are blue.\
     Sugar is sweet.""";
// "Roses are red,   \nViolets are blue. Sugar is sweet."
// 第1行: \s\s\s 保留 3 个尾部空格
// 第2行: \ 取消换行, 第3行的前导空格成为连接的一部分
```

---

## String.formatted() 与 Text Blocks

```java
// String.formatted() 是 String.format() 的实例方法版本 (JDK 15+)
// 非常适合与 text blocks 搭配使用

String html = """
    <html>
        <body>
            <h1>%s</h1>
            <p>Welcome, %s! You have %d messages.</p>
        </body>
    </html>
    """.formatted(title, userName, messageCount);

String json = """
    {
        "name": "%s",
        "age": %d,
        "email": "%s"
    }
    """.formatted(name, age, email);

// SQL 查询
String sql = """
    SELECT u.name, u.email, COUNT(o.id) as order_count
    FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
    WHERE u.status = '%s'
      AND u.created_at > '%s'
    GROUP BY u.name, u.email
    HAVING COUNT(o.id) > %d
    ORDER BY order_count DESC
    """.formatted(status, startDate, minOrders);

// 注意: 对于 SQL, 实际项目中应使用 PreparedStatement 防止注入
// formatted() 主要用于日志、模板、测试等场景
```

---

## 相关 JEP

| JEP | 版本 | 状态 | 说明 |
|-----|------|------|------|
| [JEP 355](https://openjdk.org/jeps/355) | JDK 13 | Preview | Text Blocks 第一预览 |
| [JEP 368](https://openjdk.org/jeps/368) | JDK 14 | Preview | Text Blocks 第二预览 |
| [JEP 378](/jeps/language/jep-378.md) | JDK 15 | Final | Text Blocks 正式 |
