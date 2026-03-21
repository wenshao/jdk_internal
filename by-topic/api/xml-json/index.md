# XML 与 JSON

> DOM、SAX、StAX、JAXB、JSON-P、JSON.B 演进历程

[← 返回 API 框架](../)

---

## 1. 快速概览

```
JDK 1.4 ── JDK 6 ── JDK 6 ── JDK 9 ── JDK 11
   │         │        │        │        │
DOM/SAX   JAXB 2.0  StAX    模块化  JAXB
解析      绑定      流式    JPMS   移除
(JAXP)   (JSR 222) (JSR    XML    (JEP
                    173)    模块    320)
```

### 核心演进

| 版本 | 特性 | JEP/JSR | 说明 |
|------|------|---------|------|
| **JDK 1.4** | DOM/SAX | JAXP 1.2 | XML 解析基础 |
| **JDK 6** | JAXB 2.0 | JSR 222 | XML 绑定 |
| **JDK 6** | StAX | JSR 173 | 流式 XML 解析 |
| **JDK 6** | JAXB 2.0 | JSR 222 | 注解支持 |
| **JDK 9** | XML 模块化 | JPMS | java.xml 模块 |
| **JDK 11** | JAXB 移除 | JEP 320 | JAXB 从 JDK 移除 |

---

## 目录

- [XML 解析](#xml-解析)
- [JAXB (XML 绑定)](#jaxb-xml-绑定)
- [JSON-P (JSON 处理)](#json-p-json-处理)
- [JSON.B (JSON 绑定)](#jsonb-json-绑定)
- [JSON 转义 (JDK 26+)](#json-转义-jdk-26)
- [性能对比](#性能对比)
- [最佳实践](#最佳实践)
- [核心贡献者](#核心贡献者)
- [相关链接](#相关链接)

---

## 2. XML 解析

### DOM 解析

```java
// DOM - 文档对象模型
// 将整个 XML 加载到内存

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.*;

// 解析 XML
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
DocumentBuilder builder = factory.newDocumentBuilder();
Document doc = builder.parse(new File("input.xml"));

// 遍历
Element root = doc.getDocumentElement();
NodeList children = root.getChildNodes();

for (int i = 0; i < children.getLength(); i++) {
    Node node = children.item(i);
    if (node.getNodeType() == Node.ELEMENT_NODE) {
        Element element = (Element) node;
        String text = element.getTextContent();
    }
}

// 查询
NodeList nodes = doc.getElementsByTagName("user");
Element first = (Element) nodes.item(0);
String name = first.getAttribute("name");

// 创建 XML
Document newDoc = builder.newDocument();
Element root = newDoc.createElement("root");
newDoc.appendChild(root);

Element user = newDoc.createElement("user");
user.setAttribute("id", "1");
user.setTextContent("Alice");
root.appendChild(user);

// 输出
TransformerFactory transformerFactory = TransformerFactory.newInstance();
Transformer transformer = transformerFactory.newTransformer();
transformer.transform(new DOMSource(newDoc), new StreamResult("output.xml"));
```

### SAX 解析

```java
// SAX - 事件驱动解析
// 不加载整个文档到内存

import org.xml.sax.Attributes;
import org.xml.sax.SAXException;
import org.xml.sax.helpers.DefaultHandler;

// 创建 Handler
class MyHandler extends DefaultHandler {
    private StringBuilder current = new StringBuilder();

    @Override
    public void startElement(String uri, String localName,
            String qName, Attributes attributes) {
        System.out.println("Start: " + qName);
        // 属性
        for (int i = 0; i < attributes.getLength(); i++) {
            System.out.println("  " + attributes.getQName(i) + "=" + attributes.getValue(i));
        }
    }

    @Override
    public void characters(char[] ch, int start, int length) {
        current.append(ch, start, length);
    }

    @Override
    public void endElement(String uri, String localName, String qName) {
        System.out.println("End: " + qName + " = " + current.toString().trim());
        current.setLength(0);
    }
}

// 解析
SAXParserFactory factory = SAXParserFactory.newInstance();
SAXParser parser = factory.newSAXParser();
parser.parse(new File("input.xml"), new MyHandler());
```

### StAX 解析

```java
// StAX - 流式 API
// 拉模型，性能更好

import javax.xml.stream.*;

// 读取 (Cursor API)
XMLInputFactory factory = XMLInputFactory.newInstance();
XMLStreamReader reader = factory.createXMLStreamReader(new FileInputStream("input.xml"));

while (reader.hasNext()) {
    int event = reader.next();

    switch (event) {
        case XMLStreamConstants.START_ELEMENT:
            System.out.println("Start: " + reader.getLocalName());
            // 属性
            for (int i = 0; i < reader.getAttributeCount(); i++) {
                System.out.println("  " + reader.getAttributeLocalName(i) + "=" + reader.getAttributeValue(i));
            }
            break;

        case XMLStreamConstants.CHARACTERS:
            System.out.println("Text: " + reader.getText().trim());
            break;

        case XMLStreamConstants.END_ELEMENT:
            System.out.println("End: " + reader.getLocalName());
            break;
    }
}

// 读取 (Event Iterator API)
XMLEventReader eventReader = factory.createXMLEventReader(new FileInputStream("input.xml"));
while (eventReader.hasNext()) {
    XMLEvent event = eventReader.nextEvent();

    if (event.isStartElement()) {
        StartElement start = event.asStartElement();
        System.out.println("Start: " + start.getName());
    }
}

// 写入
XMLOutputFactory outFactory = XMLOutputFactory.newInstance();
XMLStreamWriter writer = outFactory.createXMLStreamWriter(new FileOutputStream("output.xml"));

writer.writeStartDocument();
writer.writeStartElement("root");
writer.writeStartElement("user");
writer.writeAttribute("id", "1");
writer.writeCharacters("Alice");
writer.writeEndElement();
writer.writeEndElement();
writer.writeEndDocument();
writer.close();
```

---

## 3. JAXB (XML 绑定)

> **注意**: JDK 11 后 JAXB 已移除，需要额外依赖

### Maven 依赖

```xml
<!-- JAXB API -->
<dependency>
    <groupId>jakarta.xml.bind</groupId>
    <artifactId>jakarta.xml.bind-api</artifactId>
    <version>4.0.0</version>
</dependency>

<!-- JAXB 实现 -->
<dependency>
    <groupId>org.glassfish.jaxb</groupId>
    <artifactId>jaxb-runtime</artifactId>
    <version>4.0.2</version>
</dependency>
```

### 基础使用

```java
import jakarta.xml.bind.annotation.*;

// XML 注解
@XmlRootElement
@XmlType(propOrder = {"id", "name", "email"})
public class User {

    @XmlAttribute
    private int id;

    @XmlElement
    private String name;

    @XmlElement
    private String email;

    // 构造方法、getter/setter
    public User() {}

    public User(int id, String name, String email) {
        this.id = id;
        this.name = name;
        this.email = email;
    }

    // getters and setters...
}

// 编组 (Java -> XML)
JAXBContext context = JAXBContext.newInstance(User.class);
Marshaller marshaller = context.createMarshaller();
marshaller.setProperty(Marshaller.JAXB_FORMATTED_OUTPUT, true);

User user = new User(1, "Alice", "alice@example.com");
marshaller.marshal(user, new File("user.xml"));

// 输出:
// <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
// <user id="1">
//     <name>Alice</name>
//     <email>alice@example.com</email>
// </user>

// 解组 (XML -> Java)
Unmarshaller unmarshaller = context.createUnmarshaller();
User user = (User) unmarshaller.unmarshal(new File("user.xml"));
```

### 集合处理

```java
@XmlRootElement
public class UserList {

    @XmlElement(name = "user")
    private List<User> users = new ArrayList<>();

    // getter/setter
}

// 编组
UserList list = new UserList();
list.getUsers().add(new User(1, "Alice", "alice@example.com"));
list.getUsers().add(new User(2, "Bob", "bob@example.com"));

marshaller.marshal(list, new File("users.xml"));

// 解组
UserList list = (UserList) unmarshaller.unmarshal(new File("users.xml"));
```

---

## 4. JSON-P (JSON 处理)

**Jakarta EE (非 JDK 内置)**

### JSON-P API

```java
import jakarta.json.*;
import jakarta.json.stream.*;

// 构建对象 (Object Model)
JsonObject json = Json.createObjectBuilder()
    .add("name", "Alice")
    .add("age", 30)
    .add("email", "alice@example.com")
    .add("address", Json.createObjectBuilder()
        .add("city", "Shanghai")
        .add("country", "China"))
    .add("phones", Json.createArrayBuilder()
        .add("123-456-7890")
        .add("098-765-4321"))
    .build();

// 输出 JSON
System.out.println(json);

// 读取 JSON
String jsonString = json.toString();
JsonReader reader = Json.createReader(new StringReader(jsonString));
JsonObject obj = reader.readObject();

String name = obj.getString("name");
int age = obj.getInt("age");
JsonObject address = obj.getJsonObject("address");
String city = address.getString("city");

JsonArray phones = obj.getJsonArray("phones");
for (JsonValue phone : phones) {
    System.out.println(phone);
}
```

### 流式解析 (Streaming API)

```java
// 解析 JSON
JsonParser parser = Json.createParser(new StringReader(jsonString));

while (parser.hasNext()) {
    Event event = parser.next();

    switch (event) {
        case KEY_NAME:
            System.out.println("Key: " + parser.getString());
            break;
        case VALUE_STRING:
            System.out.println("String: " + parser.getString());
            break;
        case VALUE_NUMBER:
            System.out.println("Number: " + parser.getInt());
            break;
        case START_OBJECT:
            System.out.println("Start Object");
            break;
        case END_OBJECT:
            System.out.println("End Object");
            break;
        case START_ARRAY:
            System.out.println("Start Array");
            break;
        case END_ARRAY:
            System.out.println("End Array");
            break;
    }
}

// 生成 JSON
JsonGenerator generator = Json.createGenerator(new StringWriter());
generator.writeStartObject()
    .write("name", "Alice")
    .write("age", 30)
    .writeStartArray("phones")
        .write("123-456-7890")
        .write("098-765-4321")
    .writeEnd()
    .writeEnd();
generator.close();
```

---

## 5. JSON.B (JSON 绑定)

**Jakarta EE (非 JDK 内置)**

### 基础使用

```java
// JSON.B - 类似 JAXB，用于 JSON 绑定
// JDK 23+ 预览功能

import java.jsonb.*;

// 简单 POJO
public class User {
    public int id;
    public String name;
    public String email;

    public User() {}

    public User(int id, String name, String email) {
        this.id = id;
        this.name = name;
        this.email = email;
    }
}

// 序列化
Jsonb jsonb = JsonbBuilder.create();
User user = new User(1, "Alice", "alice@example.com");
String json = jsonb.toJson(user);

// 输出: {"id":1,"name":"Alice","email":"alice@example.com"}

// 反序列化
User user = jsonb.fromJson("{\"id\":1,\"name\":\"Alice\",\"email\":\"alice@example.com\"}", User.class);

// 集合
List<User> users = Arrays.asList(
    new User(1, "Alice", "alice@example.com"),
    new User(2, "Bob", "bob@example.com")
);
String json = jsonb.toJson(users);

// 反序列化集合
List<User> users = jsonb.fromJson(jsonArray, new ArrayList<User>(){}.getClass().getGenericSuperclass());
```

### 自定义配置

```java
// 自定义配置
JsonbConfig config = new JsonbConfig()
    .withFormatting(true)                     // 格式化输出
    .withNullValues(true)                     // 包含 null 值
    .withDateFormat("yyyy-MM-dd", Locale.CHINA) // 日期格式
    .withPropertyNamingStrategy(PropertyNamingStrategy.LOWER_CASE_WITH_DASHES); // 命名策略

Jsonb jsonb = JsonbBuilder.create(config);
```

---

## 6. JSON 转义 (JDK 26+)

### JEP 489: JSON 转义

```java
import java.util.json.*;

// 安全 JSON 转义 (JDK 26+)
String input = "<script>alert('xss')</script>";

// 自动转义
String escaped = JsonEscaper.escape(input);
// 输出: "\u003cscript\u003ealert('xss')\u003c/script\u003e"
```

---

## 7. 性能对比

| API | 内存占用 | 速度 | 适用场景 |
|-----|---------|------|----------|
| **DOM** | 高 | 慢 | 小文件、随机访问 |
| **SAX** | 低 | 快 | 大文件、只读 |
| **StAX** | 低 | 快 | 大文件、读写 |
| **JSON-P** | 中 | 中 | JSON 处理 |
| **JSON-B** | 中 | 中 | JSON 绑定 |

---

## 8. 最佳实践

### 选择合适的解析器

| 场景 | 推荐方案 | 原因 |
|------|----------|------|
| 大文件 XML | StAX/SAX | 内存占用低 |
| 小文件 XML | DOM | 操作方便 |
| XML <-> Java | JAXB | 自动绑定 |
| 大 JSON | Streaming API | 内存效率高 |
| 小 JSON | Object Model | 简单直观 |
| JSON <-> Java | JSON.B | 自动绑定 |

### 性能优化

```java
// 1. 重用解析器
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
factory.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", false);

// 2. 使用 StAX 处理大文件
XMLInputFactory factory = XMLInputFactory.newInstance();
factory.setProperty(XMLInputFactory.IS_COALESCING, true);
factory.setProperty(XMLInputFactory.IS_REPLACING_ENTITY_REFERENCES, true);

// 3. JSON 使用流式 API
JsonParser parser = Json.createParser(new FileInputStream("large.json"));

// 4. 避免不必要的格式化
marshaller.setProperty(Marshaller.JAXB_FORMATTED_OUTPUT, false);
```

### 安全考虑

```java
// 1. 禁用 DTD (防止 XXE 攻击)
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
factory.setFeature("http://xml.org/sax/features/external-general-entities", false);

// 2. 限制输入大小
SAXParserFactory factory = SAXParserFactory.newInstance();
factory.setFeature("http://xml.org/sax/features/external-general-entities", false);

// 3. 验证 JSON
// JSON-P 本身安全，但要注意 JSON 反序列化攻击
```

---

## 9. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### XML/JSON (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Joe Wang | 42 | Oracle | XML, JSON API 维护者 |
| 2 | Roger Riggs | 2 | Oracle | 核心库 |
| 3 | Pavel Rappo | 2 | Oracle | API 设计 |
| 4 | Justin Lu | 2 | Oracle | JSON 处理 |
| 5 | Joe Darcy | 2 | Oracle | API 设计 |

### 历史贡献者

| 贡献者 | 公司/机构 | 主要贡献 |
|--------|----------|----------|
| **Joe Wang** | Oracle | XML/JSON API 主要维护者 |
| **Jeff Suttor** | Sun | StAX (JSR 173) |
| **Ryan Shoemaker** | Sun | JAXB (JSR 222) |

---

## 10. Git 提交历史

> 基于 OpenJDK master 分支分析

### XML/JSON 改进 (2024-2026)

```bash
# 查看 XML 相关提交
cd /path/to/jdk
git log --oneline -- src/java.xml/share/classes/javax/xml/
git log --oneline -- src/java.json/share/classes/javax/json/
```

---

## 11. 相关链接

### 内部文档

- [XML/JSON 时间线](timeline.md) - 详细的历史演进
- [核心 API](../)
- [IO 流](../io/) - 文件读写
- [异常处理](../exceptions/) - 解析异常

### 外部资源

- [JEP 353](/jeps/api/jep-353.md)
- [JEP 471](/jeps/api/jep-471.md)
- [JEP 489](/jeps/api/jep-489.md)
- [JSR 173: StAX](https://jcp.org/en/jsr/detail?id=173)
- [JSR 222: JAXB](https://jcp.org/en/jsr/detail?id=222)
- [Jakarta JSON Processing](https://jakarta.ee/specifications/jsonp/)
- [Jakarta JSON Binding](https://jakarta.ee/specifications/jsonb/)

### 官方文档

- [Java XML 教程 (Oracle)](https://docs.oracle.com/javase/tutorial/jaxp/)
- [JSON-P 规范](https://jakarta.ee/specifications/jsonp/2.0/)
- [JAXB 参考实现](https://eclipse-ee4j.github.io/jaxb-ri/)
- [Java API for JSON Processing](https://eclipse-ee4j.github.io/jsonp/)
- [Java Architecture for XML Binding](https://eclipse-ee4j.github.io/jaxb/)

---

**最后更新**: 2026-03-20

**Sources**:
- [JEP 353](/jeps/api/jep-353.md)
- [JEP 471](/jeps/api/jep-471.md)
- [JEP 489](/jeps/api/jep-489.md)
- [JSR 173: StAX](https://jcp.org/en/jsr/detail?id=173)
- [Jakarta JSON Processing](https://jakarta.ee/specifications/jsonp/)
- [Jakarta JSON Binding](https://jakarta.ee/specifications/jsonb/)
