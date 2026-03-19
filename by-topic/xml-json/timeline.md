# XML/JSON 处理演进时间线

Java XML 和 JSON 处理从 JDK 1.0 到 JDK 26 的完整演进历程。

---

## 时间线概览

```
JDK 1.0 ──── JDK 4 ──── JDK 6 ──── JDK 9 ──── JDK 11 ──── JDK 21 ──── JDK 26
 │             │           │           │           │            │            │
No XML        DOM/SAX     StAX       JAXB      JSON API   JSON-P     Structured
              JAXP       (JSR 173)  废弃预览   2.0       2.1        Validation
```

---

## XML 处理

### XML 处理模型对比

```
┌─────────────────────────────────────────────────────────┐
│                  XML 处理模型                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  DOM (Document Object Model)                            │
│  ├── 将整个 XML 加载到内存                              │
│  ├── 树形结构                                          │
│  ├── 可随机访问                                         │
│  └── 大文件内存占用高                                   │
│                                                         │
│  SAX (Simple API for XML)                               │
│  ├── 事件驱动                                           │
│  ├── 流式读取                                           │
│  ├── 单向遍历                                           │
│  └── 内存占用低                                         │
│                                                         │
│  StAX (Streaming API for XML)                           │
│  ├── 拉模式 (Pull)                                      │
│  ├── 流式读写                                           │
│  ├── 双向可控                                           │
│  └── 性能好                                             │
│                                                         │
│  JAXB (Java Architecture for XML Binding)               │
│  ├── XML 与 Java 对象绑定                               │
│  ├── 注解驱动                                           │
│  └── JDK 9 标记废弃                                     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## JDK 4 - DOM 和 SAX

### DOM 解析

```java
import javax.xml.parsers.*;
import org.w3c.dom.*;

// DOM 解析
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
DocumentBuilder builder = factory.newDocumentBuilder();

// 解析文件
Document document = builder.parse("input.xml");

// 获取根元素
Element root = document.getDocumentElement();

// 遍历子节点
NodeList children = root.getChildNodes();
for (int i = 0; i < children.getLength(); i++) {
    Node node = children.item(i);
    if (node.getNodeType() == Node.ELEMENT_NODE) {
        Element element = (Element) node;
        String tagName = element.getTagName();
        String textContent = element.getTextContent();
    }
}

// 获取指定标签
NodeList elements = root.getElementsByTagName("book");
for (int i = 0; i < elements.getLength(); i++) {
    Element book = (Element) elements.item(i);
    String id = book.getAttribute("id");
    String title = book.getElementsByTagName("title")
                         .item(0)
                         .getTextContent();
}

// 创建新文档
Document newDoc = builder.newDocument();
Element rootElement = newDoc.createElement("library");
newDoc.appendChild(rootElement);

Element bookElement = newDoc.createElement("book");
bookElement.setAttribute("id", "1");
rootElement.appendChild(bookElement);
```

### SAX 解析

```java
import org.xml.sax.*;
import org.xml.sax.helpers.*;

// SAX 解析 (事件驱动)
SAXParserFactory factory = SAXParserFactory.newInstance();
SAXParser parser = factory.newSAXParser();

// 自定义 Handler
DefaultHandler handler = new DefaultHandler() {

    @Override
    public void startDocument() throws SAXException {
        System.out.println("开始解析文档");
    }

    @Override
    public void endDocument() throws SAXException {
        System.out.println("文档解析结束");
    }

    @Override
    public void startElement(String uri, String localName,
                           String qName, Attributes attributes)
            throws SAXException {

        System.out.println("开始元素: " + qName);

        // 属性
        for (int i = 0; i < attributes.getLength(); i++) {
            String name = attributes.getQName(i);
            String value = attributes.getValue(i);
            System.out.println("  属性: " + name + "=" + value);
        }
    }

    @Override
    public void endElement(String uri, String localName, String qName)
            throws SAXException {
        System.out.println("结束元素: " + qName);
    }

    @Override
    public void characters(char[] ch, int start, int length)
            throws SAXException {
        String text = new String(ch, start, length).trim();
        if (!text.isEmpty()) {
            System.out.println("  文本: " + text);
        }
    }
};

// 解析
parser.parse("input.xml", handler);
```

---

## JDK 6 - StAX (JSR 173)

### XMLStreamWriter

```java
import javax.xml.stream.*;

// StAX 写入
XMLOutputFactory factory = XMLOutputFactory.newInstance();
XMLStreamWriter writer = factory.createXMLStreamWriter(
    new FileOutputStream("output.xml"), "UTF-8");

writer.writeStartDocument("UTF-8", "1.0");
writer.writeStartElement("library");

writer.writeStartElement("book");
writer.writeAttribute("id", "1");

writer.writeStartElement("title");
writer.writeCharacters("Java Programming");
writer.writeEndElement();

writer.writeStartElement("author");
writer.writeCharacters("James Gosling");
writer.writeEndElement();

writer.writeEndElement();  // book
writer.writeEndElement();  // library
writer.writeEndDocument();
writer.close();
```

### XMLStreamReader

```java
// StAX 读取
XMLInputFactory factory = XMLInputFactory.newInstance();
XMLStreamReader reader = factory.createXMLStreamReader(
    new FileInputStream("input.xml"));

while (reader.hasNext()) {
    int event = reader.next();

    switch (event) {
        case XMLStreamReader.START_ELEMENT:
            System.out.println("开始元素: " + reader.getLocalName());
            // 属性
            for (int i = 0; i < reader.getAttributeCount(); i++) {
                System.out.println("  属性: " +
                    reader.getAttributeLocalName(i) + "=" +
                    reader.getAttributeValue(i));
            }
            break;

        case XMLStreamReader.CHARACTERS:
            String text = reader.getText().trim();
            if (!text.isEmpty()) {
                System.out.println("  文本: " + text);
            }
            break;

        case XMLStreamReader.END_ELEMENT:
            System.out.println("结束元素: " + reader.getLocalName());
            break;
    }
}
reader.close();
```

### Iterator API

```java
// StAX Iterator API
XMLInputFactory factory = XMLInputFactory.newInstance();
XMLEventReader eventReader = factory.createXMLEventReader(
    new FileInputStream("input.xml"));

while (eventReader.hasNext()) {
    XMLEvent event = eventReader.nextEvent();

    if (event.isStartElement()) {
        StartElement start = event.asStartElement();
        System.out.println("开始元素: " + start.getName());

        // 属性
        Iterator<Attribute> attributes = start.getAttributes();
        while (attributes.hasNext()) {
            Attribute attr = attributes.next();
            System.out.println("  属性: " + attr.getName() + "=" + attr.getValue());
        }
    }

    if (event.isCharacters()) {
        Characters characters = event.asCharacters();
        String text = characters.getData().trim();
        if (!text.isEmpty()) {
            System.out.println("  文本: " + text);
        }
    }

    if (event.isEndElement()) {
        EndElement end = event.asEndElement();
        System.out.println("结束元素: " + end.getName());
    }
}
```

---

## JAXB (XML 绑定)

### JAXB 注解

```java
import jakarta.xml.bind.annotation.*;

// JAXB 注解
@XmlRootElement(name = "book")
@XmlAccessorType(XmlAccessType.FIELD)
public class Book {

    @XmlAttribute
    private String id;

    @XmlElement
    private String title;

    @XmlElement(name = "author_name")
    private String author;

    @XmlElement
    private double price;

    // 构造器、getter、setter
    public Book() {}

    public Book(String id, String title, String author, double price) {
        this.id = id;
        this.title = title;
        this.author = author;
        this.price = price;
    }

    // getters and setters...
}
```

### JAXB 使用

```java
import jakarta.xml.bind.*;

// Java 对象 → XML
Book book = new Book("1", "Java Programming", "James Gosling", 49.99);

JAXBContext context = JAXBContext.newInstance(Book.class);
Marshaller marshaller = context.createMarshaller();
marshaller.setProperty(Marshaller.JAXB_FORMATTED_OUTPUT, true);

marshaller.marshal(book, new File("book.xml"));
// 输出到控制台
marshaller.marshal(book, System.out);

// XML → Java 对象
Unmarshaller unmarshaller = context.createUnmarshaller();
Book parsedBook = (Book) unmarshaller.unmarshal(new File("book.xml"));
```

---

## JSON 处理

### JSON 处理模型

```
┌─────────────────────────────────────────────────────────┐
│                  JSON 处理模型                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  JSON-P (JSON Processing)                               │
│  ├── 流式 API (javax.json.stream)                      │
│  ├── 对象模型 API (javax.json)                          │
│  └── JDK EE 标准                                       │
│                                                         │
│  JSON-B (JSON Binding)                                  │
│  ├── 类似 JAXB                                         │
│  ├── 注解驱动                                          │
│  └── JDK EE 标准                                       │
│                                                         │
│  Jackson (事实标准)                                     │
│  ├── 最流行的 JSON 库                                  │
│  ├── Tree Model, Streaming API, Data Binding           │
│  └── Spring Boot 默认                                  │
│                                                         │
│  Gson                                                   │
│  ├── Google 开发                                        │
│  ├── 简单易用                                          │
│  └── 性能优秀                                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## JSON-P (javax.json)

### 对象模型 API

```java
import javax.json.*;

// JSON-P 对象模型
JsonObject jsonObject = Json.createObjectBuilder()
    .add("name", "Alice")
    .add("age", 25)
    .add("email", "alice@example.com")
    .add("address", Json.createObjectBuilder()
        .add("street", "123 Main St")
        .add("city", "Boston")
        .add("zip", "02101"))
    .add("hobbies", Json.createArrayBuilder()
        .add("reading")
        .add("programming")
        .add("gaming"))
    .build();

// 输出 JSON
System.out.println(jsonObject);

// 读取值
String name = jsonObject.getString("name");
int age = jsonObject.getInt("age");
JsonObject address = jsonObject.getJsonObject("address");
String city = address.getString("city");
JsonArray hobbies = jsonObject.getJsonArray("hobbies");
```

### JsonReader / JsonWriter

```java
// JsonReader - 流式读取
JsonReader reader = Json.createReader(new FileReader("input.json"));
JsonObject jsonObject = reader.readObject();
reader.close();

// JsonWriter - 流式写入
JsonWriter writer = Json.createWriter(new FileWriter("output.json"));
writer.writeObject(jsonObject);
writer.close();
```

### Streaming API

```java
// JSON-P Streaming API
JsonParser parser = Json.createParser(new FileReader("large.json"));

while (parser.hasNext()) {
    JsonParser.Event event = parser.next();

    switch (event) {
        case START_OBJECT:
            System.out.println("开始对象");
            break;
        case START_ARRAY:
            System.out.println("开始数组");
            break;
        case KEY_NAME:
            System.out.println("键: " + parser.getString());
            break;
        case VALUE_STRING:
            System.out.println("  字符串: " + parser.getString());
            break;
        case VALUE_NUMBER:
            System.out.println("  数字: " + parser.getBigDecimal());
            break;
        case VALUE_TRUE:
            System.out.println("  布尔: true");
            break;
        case VALUE_FALSE:
            System.out.println("  布尔: false");
            break;
        case VALUE_NULL:
            System.out.println("  null");
            break;
        case END_OBJECT:
            System.out.println("结束对象");
            break;
        case END_ARRAY:
            System.out.println("结束数组");
            break;
    }
}
```

---

## Jackson

### ObjectMapper

```java
import com.fasterxml.jackson.databind.*;

// Jackson ObjectMapper
ObjectMapper mapper = new ObjectMapper();

// Java 对象 → JSON
User user = new User("Alice", 25);
String json = mapper.writeValueAsString(user);

// 美化输出
String prettyJson = mapper.writerWithDefaultPrettyPrinter()
                               .writeValueAsString(user);

// 写入文件
mapper.writeValue(new File("user.json"), user);

// JSON → Java 对象
User parsedUser = mapper.readValue(json, User.class);

// 读取为 JsonNode
JsonNode root = mapper.readTree(json);
String name = root.path("name").asText();
int age = root.path("age").asInt();
```

### 注解

```java
import com.fasterxml.jackson.annotation.*;

// Jackson 注解
public class User {

    @JsonProperty("user_name")  // 重命名属性
    private String name;

    @JsonIgnore               // 忽略属性
    private String password;

    @JsonInclude(JsonInclude.Include.NON_NULL)  // null 不序列化
    private String email;

    @JsonFormat(pattern = "yyyy-MM-dd")  // 日期格式
    private LocalDate birthDate;

    @JsonCreator               // 自定义构造器
    public User(@JsonProperty("name") String name) {
        this.name = name;
    }

    @JsonPropertyOrder({"name", "age"})  // 属性顺序
    // getters and setters
}
```

### 集合处理

```java
// List 处理
List<User> users = List.of(
    new User("Alice", 25),
    new User("Bob", 30)
);

String json = mapper.writeValueAsString(users);
List<User> parsedUsers = mapper.readValue(json,
    new TypeReference<List<User>>() {});

// Map 处理
Map<String, Object> data = new HashMap<>();
data.put("name", "Alice");
data.put("age", 25);

String json = mapper.writeValueAsString(data);
Map<String, Object> parsedMap = mapper.readValue(json,
    new TypeReference<Map<String, Object>>() {});
```

---

## Gson

### 基础使用

```java
import com.google.gson.*;

// Gson 基础
Gson gson = new Gson();

// Java 对象 → JSON
User user = new User("Alice", 25);
String json = gson.toJson(user);

// 美化输出
Gson prettyGson = new GsonBuilder()
    .setPrettyPrinting()
    .create();
String prettyJson = prettyGson.toJson(user);

// JSON → Java 对象
User parsedUser = gson.fromJson(json, User.class);

// 集合处理
List<User> users = List.of(
    new User("Alice", 25),
    new User("Bob", 30)
);

String json = gson.toJson(users);
Type userListType = new TypeToken<List<User>>() {}.getType();
List<User> parsedUsers = gson.fromJson(json, userListType);
```

### 注解

```java
import com.google.gson.annotations.*;

// Gson 注解
public class User {

    @SerializedName("user_name")  // 重命名
    private String name;

    @Expose(serialize = true, deserialize = true)  // 控制序列化
    private String email;

    @Since(1.0)  // 版本控制
    private int age;

    @Until(2.0)  // 版本控制
    private boolean deprecated;
}
```

---

## JDK 21+ - JSON API 更新

### JSON-P 2.0

```java
// JSON-P 2.0 增强
// 1. JSON Pointer
JsonPointer pointer = Json.createPointer("/address/city");
JsonNode city = pointer.getValue(jsonObject);

// 2. JSON Patch
JsonPatch patch = Json.createPatchBuilder()
    .add("/address/country", "USA")
    .remove("/email")
    .build();

JsonArray patched = patch.apply(jsonObject);

// 3. JSON Merge Patch
JsonValue mergePatch = Json.createObjectBuilder()
    .add("age", 26)
    .build();

JsonObject merged = Json.createMergePatch(mergePatch)
    .apply(jsonObject);
```

---

## XML vs JSON

| 特性 | XML | JSON |
|------|-----|------|
| 可读性 | 高 | 高 |
| 冗余 | 高 (标签) | 低 |
| 注释 | 支持 | 大多不支持 |
| 属性 | 支持 | 不支持 |
| 数据类型 | 需 Schema | 原生支持 |
| 解析复杂度 | 高 | 低 |
| 文件大小 | 大 | 小 |
| 浏览器支持 | 需解析器 | 原生支持 |

---

## 选择建议

### XML 处理

| 场景 | 推荐 | 说明 |
|------|------|------|
| 大文件 | StAX/SAX | 流式处理 |
| 小文件 | DOM | 随机访问 |
| 对象绑定 | JAXB | 已废弃，替代方案 |
| 简单解析 | StAX | 易用性好 |

### JSON 处理

| 场景 | 推荐 | 说明 |
|------|------|------|
| Spring 应用 | Jackson | 默认集成 |
| Android | Gson | 轻量级 |
| 标准 API | JSON-P | JDK EE |
| 大文件 | Jackson Streaming | 流式处理 |

---

## 时间线总结

| 版本 | 特性 | 说明 |
|------|------|------|
| JDK 4 | DOM/SAX | XML 基础解析 |
| JDK 5 | JAXB 1.0 | XML 绑定 |
| JDK 6 | StAX | 流式 XML |
| JDK 6 | JAXB 2.0 | 注解支持 |
| JDK 7 | JSON-P 1.0 | JSON 处理 API |
| JDK 9 | JAXB 标记废弃 | 移除 JDK 默认 |
| JDK 11 | JSON-P 1.1 | JSON Pointer/Patch |
| JDK 21 | JSON-P 2.1 | 增强 JSON 处理 |

---

## 相关链接

- [JAXP](https://docs.oracle.com/javase/8/docs/api/javax/xml/parsers/package-summary.html)
- [JSON-P](https://eclipse-ee4j.github.io/jsonp/)
- [Jackson](https://github.com/FasterXML/jackson)
- [Gson](https://github.com/google/gson)
