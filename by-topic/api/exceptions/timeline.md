# 异常处理演进时间线

Java 异常处理从 JDK 1.0 到 JDK 26 的完整演进历程。

---

## 时间线概览

```
JDK 1.0 ──── JDK 5 ──── JDK 6 ──── JDK 7 ──── JDK 9 ──── JDK 16 ──── JDK 21 ──── JDK 26
 │            │           │           │           │           │           │           │
try-catch    异常链      异常处理    Try-with-    精确异常    异常记录    模式匹配    增强诊断
finally      getCause    增强        resources    类型        SPI         异常        可追溯性
throws       自定义异常
```

---

## 异常层次结构

```java
                    Throwable
                       │
        ┌──────────────┴──────────────┐
        │                             │
     Error                         Exception
        │                             │
    ┌───┴────┐                    ┌───┴────────┐
    │        │                    │            │
  AWTError  VirtualMachineError  IOException  RuntimeException
               │                    │            │
    ┌──────────┴──────────┐        │      ┌─────┴─────┐
    │                     │        │      │           │  OutOfMemoryError   SocketException NullPointerException
  StackOverflowError    ...       │      SQLException IllegalArgumentException
                                     │      NumberFormatException
                                 ClassNotFoundException
```

---

## 时间线详情

### JDK 1.0 (1996) - 基础异常处理

#### try-catch-finally

```java
// 基础语法
try {
    // 可能抛出异常的代码
    FileReader file = new FileReader("file.txt");
    int data = file.read();
} catch (FileNotFoundException e) {
    // 处理特定异常
    System.err.println("File not found: " + e.getMessage());
} catch (IOException e) {
    // 处理另一个异常
    System.err.println("IO error: " + e.getMessage());
} finally {
    // 总是执行的代码
    System.out.println("Cleanup");
}
```

#### throws 声明

```java
// 方法声明可能抛出的异常
public void readFile(String path) throws IOException {
    FileReader file = new FileReader(path);
    // ...
}

// 抛出异常
public void divide(int a, int b) throws ArithmeticException {
    if (b == 0) {
        throw new ArithmeticException("Division by zero");
    }
}
```

#### 自定义异常

```java
// 检查型异常
public class BusinessException extends Exception {
    private int errorCode;

    public BusinessException(String message, int errorCode) {
        super(message);
        this.errorCode = errorCode;
    }

    public int getErrorCode() {
        return errorCode;
    }
}

// 运行时异常
public class ValidationException extends RuntimeException {
    public ValidationException(String message) {
        super(message);
    }
}
```

### JDK 1.4 - 异常链

#### 异常链 (Exception Chaining)

```java
// JDK 1.4 前需要手动保存原因
try {
    // ...
} catch (IOException e) {
    BusinessException ex = new BusinessException("Failed to read");
    ex.stackTrace = e.getStackTrace();  // 手动保存
    throw ex;
}

// JDK 1.4+ 支持异常链
try {
    // ...
} catch (IOException e) {
    // 使用 Throwable cause 参数
    BusinessException ex = new BusinessException("Failed to read", e);
    throw ex;
    // 或使用 initCause()
    BusinessException ex2 = new BusinessException("Failed");
    ex2.initCause(e);
    throw ex2;
}

// 获取原因异常
try {
    // ...
} catch (BusinessException e) {
    Throwable cause = e.getCause();
    if (cause instanceof IOException) {
        // 处理原始原因
    }
}
```

### JDK 5 - 异常处理增强

#### 多异常类型

```java
// 捕获多种异常 (仍需要多个 catch 块)
try {
    // ...
} catch (IOException e) {
    handleException(e);
} catch (SQLException e) {
    handleException(e);
} catch (ClassNotFoundException e) {
    handleException(e);
}
```

#### 更精确的重新抛出

```java
// JDK 5 允许更精确的异常类型
public void method() throws IOException, SQLException {
    try {
        // 可能抛出多种异常的代码
    } catch (Exception e) {
        // 重新抛出，编译器会分析可能抛出的类型
        throw e;
    }
}
```

### JDK 6 - 异常处理工具

#### 异常工具类

```java
// 异常初始化
throw new Exception("Error").initCause(new IOException());

// 堆栈跟踪
e.printStackTrace();
StackTraceElement[] stack = e.getStackTrace();

// 带堆栈的创建异常
Exception e = new Exception();
e.setStackTrace(new StackTraceElement[]{
    new StackTraceElement("Class", "method", "file", 1)
});
```

### JDK 7 - Try-with-resources

#### 自动资源管理

```java
// 实现 AutoCloseable 接口的资源
public class Resource implements AutoCloseable {
    public void doSomething() {
        System.out.println("Doing something");
    }

    @Override
    public void close() {
        System.out.println("Resource closed");
    }
}

// 使用 try-with-resources
try (Resource resource = new Resource()) {
    resource.doSomething();
}  // 自动调用 close()

// 多个资源
try (FileInputStream fis = new FileInputStream("input.txt");
     BufferedReader br = new BufferedReader(new InputStreamReader(fis))) {
    String line = br.readLine();
}  // 按相反顺序关闭: br, fis
```

#### 多异常捕获

```java
// JDK 7+ 单个 catch 捕获多种异常
try {
    // ...
} catch (IOException | SQLException | ClassNotFoundException e) {
    // 处理所有异常
    System.err.println("Error: " + e.getMessage());
}

// 注意: 捕获的异常变量是隐式 final
try {
    // ...
} catch (IOException | SQLException e) {
    // e = new Exception();  // 编译错误，e 是 final
}
```

#### 精确异常重抛

```java
// JDK 7 更精确的异常分析
public void method() throws IOException, SQLException {
    try {
        // 代码可能抛出 IOException 或 SQLException
        throw new IOException();
    } catch (Exception e) {
        // 编译器可以分析出 e 只能是 IOException 或 SQLException
        throw e;
    }
}
```

#### Throwable 增强

```java
// 添加 suppressed 异常
try (Resource r1 = new Resource()) {
    try (Resource r2 = new Resource()) {
        // r2.close() 抛出的异常会被添加到 r1.close() 异常的 suppressed 列表
    }
} catch (Exception e) {
    Throwable[] suppressed = e.getSuppressed();
    for (Throwable t : suppressed) {
        System.err.println("Suppressed: " + t);
    }
}

// 手动添加 suppressed 异常
try {
    // ...
} catch (Exception e) {
    Exception mainException = new Exception("Main error");
    mainException.addSuppressed(e);
    throw mainException;
}
```

### JDK 9 - 私有接口方法中的异常

```java
// 接口中的私有方法可以抛出异常
interface MyInterface {
    default void method() {
        helperMethod();
    }

    private void helperMethod() throws IOException {
        // ...
    }
}
```

### JDK 16 - 异常记录 SPI

```java
// 异常记录 SPI (预览)
// 允许应用自定义异常处理

public interface ExceptionRecorder {
    void record(Throwable throwable);
}

// 注册自定义记录器
// (JDK 16+ 预览功能)
```

### JDK 21 - 模式匹配异常

```java
// instanceof 模式匹配与异常
if (throwable instanceof IOException ioe) {
    // ioe 可直接使用
    System.err.println("IO error: " + ioe.getMessage());
}

// switch 表达式处理异常
String message = switch (e) {
    case IOException ioe -> "IO error: " + ioe.getMessage();
    case SQLException sqle -> "SQL error: " + sqle.getSQLState();
    case null, default -> "Unknown error";
};
```

### JDK 26 - 增强异常诊断

```java
// 更好的异常诊断信息
// 增强的堆栈跟踪
// 改进的异常消息格式
```

---

## 常见异常类型

### 运行时异常

```java
// NullPointerException
String s = null;
s.length();  // NPE

// ArrayIndexOutOfBoundsException
int[] arr = new int[5];
arr[10];  // 越界

// IllegalArgumentException
// 参数不合法

// NumberFormatException
Integer.parseInt("abc");  // 数字格式错误

// ArithmeticException
int x = 10 / 0;  // 除零

// ClassCastException
Object obj = "string";
Integer i = (Integer) obj;  // 类型转换错误

// IllegalStateException
// 对象状态不合法

// ConcurrentModificationException
// 迭代时修改集合
```

### 检查型异常

```java
// IOException
// 文件操作异常

// SQLException
// 数据库操作异常

// ClassNotFoundException
// 类未找到

// NoSuchMethodException
// 方法未找到

// InterruptedException
// 线程中断
```

### 错误 (Error)

```java
// VirtualMachineError
//   - OutOfMemoryError
//   - StackOverflowError
//   - NoClassDefFoundError

// AWTError
// GUI 错误
```

---

## 异常处理最佳实践

### finally vs try-with-resources

```java
// ❌ JDK 7 前的手动资源管理
FileInputStream fis = null;
try {
    fis = new FileInputStream("file.txt");
    // 使用资源
} catch (IOException e) {
    e.printStackTrace();
} finally {
    if (fis != null) {
        try {
            fis.close();  // 可能抛异常
        } catch (IOException e) {
            // 丢失 fis 异常
        }
    }
}

// ✅ JDK 7+ try-with-resources
try (FileInputStream fis = new FileInputStream("file.txt")) {
    // 使用资源
} catch (IOException e) {
    e.printStackTrace();
}
// 自动关闭， suppressed 异常保留
```

### 异常链

```java
// ✅ 保留原始异常
try {
    // 低层操作
} catch (IOException e) {
    throw new BusinessException("High level error", e);
}

// ❌ 丢失原始异常
try {
    // 低层操作
} catch (IOException e) {
    throw new BusinessException("High level error");
}
```

### 具体异常捕获

```java
// ✅ 捕获具体异常
try {
    // ...
} catch (FileNotFoundException e) {
    // 处理文件不存在
} catch (IOException e) {
    // 处理其他 IO 异常
}

// ❌ 捕获过于宽泛
try {
    // ...
} catch (Exception e) {
    // 吞掉所有异常
}
```

### 异常转换

```java
// ✅ 转换为领域异常
public void loadUser(String id) throws UserNotFoundException {
    try {
        // 加载用户
    } catch (SQLException e) {
        throw new UserNotFoundException("User not found: " + id, e);
    }
}

// ✅ 转换为运行时异常
public void process(String input) {
    try {
        // 处理
    } catch (IOException e) {
        throw new ProcessingException("Failed to process", e);
    }
}
```

### 清理资源

```java
// ✅ try-with-resources 自动清理
try (Connection conn = dataSource.getConnection();
     PreparedStatement ps = conn.prepareStatement(sql)) {
    // 使用资源
} catch (SQLException e) {
    throw new DataAccessException(e);
}

// ✅ 手动清理 (如果资源未实现 AutoCloseable)
Resource resource = new Resource();
try {
    resource.use();
} finally {
    resource.close();  // 确保 close 被调用
}
```

---

## 异常处理模式

### Template Method 模式

```java
public abstract class Template {
    public final void execute() {
        try {
            doSetup();
            doExecute();
        } catch (Exception e) {
            handleError(e);
        } finally {
            doCleanup();
        }
    }

    protected abstract void doExecute();
    protected void doSetup() { }
    protected void doCleanup() { }
    protected void handleError(Exception e) {
        e.printStackTrace();
    }
}
```

### Try-Success-Failure 模式

```java
// 类似 JavaScript Promise 的处理
public class Try<T> {
    private final T value;
    private final Exception exception;

    private Try(T value, Exception exception) {
        this.value = value;
        this.exception = exception;
    }

    public static <T> Try<T> of(T value) {
        return new Try<>(value, null);
    }

    public static <T> Try<T> failure(Exception e) {
        return new Try<>(null, e);
    }

    public <U> Try<U> map(Function<T, U> f) {
        if (exception != null) {
            return failure(exception);
        }
        try {
            return of(f.apply(value));
        } catch (Exception e) {
            return failure(e);
        }
    }

    public void onSuccess(Consumer<T> consumer) {
        if (exception == null) {
            consumer.accept(value);
        }
    }

    public void onFailure(Consumer<Exception> consumer) {
        if (exception != null) {
            consumer.accept(exception);
        }
    }
}
```

### Result 模式

```java
// Rust 风格的 Result 类型
public sealed interface Result<T> {
    record Success<T>(T value) implements Result<T> { }
    record Failure<T>(Exception error) implements Result<T> { }

    default boolean isSuccess() {
        return this instanceof Success;
    }

    default T get() throws Exception {
        return switch (this) {
            case Success(T v) -> v;
            case Failure(Exception e) -> throw e;
        };
    }
}
```

---

## 相关 JEP

| JEP | 标题 | 版本 | 说明 |
|-----|------|------|------|
| [JSR 203](https://jcp.org/en/jsr/detail?id=203) | More New I/O APIs for the Java Platform | JDK 7 | Try-with-resources |
| [JEP 305](https://openjdk.org/jeps/305) | Pattern Matching for instanceof | JDK 14 | 异常模式匹配 |
| [JEP 394](https://openjdk.org/jeps/394) | Pattern Matching for instanceof | JDK 16 | 正式版 |

---

## 相关链接

- [The Java Tutorials: Exceptions](https://docs.oracle.com/javase/tutorial/essential/exceptions/)
- [Effective Java: Exceptions](https://www.oreilly.com/library/view/effective-java/9780134686097/)
