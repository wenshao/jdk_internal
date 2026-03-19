# 语言特性

语法、类型、反射等语言层面演进。

---

## 主题列表

### [字符串处理](string/)

字符串相关优化和新特性。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 8 | StringJoiner | - |
| JDK 9 | **Compact Strings** (JEP 254)、invokedynamic 拼接 (JEP 280) | JEP 254, JEP 280 |
| JDK 11 | repeat()、strip()、isBlank()、lines() | - |
| JDK 15 | **Text Blocks** (正式) | JEP 378 |
| JDK 21 | String Templates (预览) | JEP 430 |
| JDK 24 | 隐藏类拼接策略 (+40% 启动性能) | JDK-8336856 |
| JDK 25 | String Templates (第二次预览) | JEP 459 |
| JDK 26 | Integer/Long.toString 优化 | JDK-8370503 |

→ [字符串优化时间线](string/timeline.md)

### [反射与元数据](reflection/)

反射、注解和字节码操作的演进。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 1.0 | 反射 API | - |
| JDK 5 | Annotations (JSR 175) | JSR 175 |
| JDK 6 | Pluggable Annotation Processing | JSR 269 |
| JDK 7 | MethodHandle (JSR 292) | JSR 292 |
| JDK 8 | Lambda invokedynamic, Parameter 反射 | - |
| JDK 11 | Constable/ConstantDesc | - |
| JDK 16 | ClassFile API | JEP 395 |
| JDK 26 | Mirror API | - |

→ [反射时间线](reflection/timeline.md)

### [语法演进](syntax/)

语言语法从 JDK 1.0 到 JDK 26 的完整演进。

| 特性 | 引入版本 | 说明 |
|------|----------|------|
| 内部类 | JDK 1.1 | 匿名类、成员类 |
| 断言 | JDK 1.4 | assert |
| 泛型 | JDK 5 | 类型参数化 |
| 枚举 | JDK 5 | enum |
| 变参 | JDK 5 | T... |
| 注解 | JDK 5 | @interface |
| 增强 for | JDK 5 | for (T : collection) |
| Lambda | JDK 8 | → 表达式 |
| 方法引用 | JDK 8 | Object::method |
| var | JDK 10 | 局部变量类型推断 |
| Records | JDK 16 | 不可变数据类 |
| instanceof 模式 | JDK 16 | obj instanceof Type t |
| Sealed Classes | JDK 17 | 密封类 |
| switch 模式 | JDK 21 | case Type t → ... |
| String Templates | JDK 21+ | STR."\{value}" |
| 隐式类 | JDK 25 | void main() {} |

→ [语法演进时间线](syntax/timeline.md)

### [注解与元编程](annotations/)

注解处理器、编译期元编程。

| 版本 | 主要变化 | JSR |
|------|----------|-----|
| JDK 5 | 注解引入 | JSR 175 |
| JDK 6 | Pluggable Annotation Processing API | JSR 269 |
| JDK 7 | 类型注解 | JSR 308 |
| JDK 8 | 重复注解 @Repeatable | - |
| JDK 17 | Sealed Classes 支持 | - |

→ [注解时间线](annotations/timeline.md)

---

## 学习路径

1. **入门**: [字符串处理](string/) → 日常开发必备
2. **进阶**: [语法演进](syntax/) → 掌握现代 Java 语法
3. **深入**: [反射与元数据](reflection/) → [注解与元编程](annotations/) → 元编程能力
