# java.xml 模块分析

> JAXP (Java API for XML Processing)，XML 处理标准 API

---

## 1. 模块概述 (Module Overview)

`java.xml` 是 Java 处理 XML 文档的标准 API 模块，提供 DOM、SAX、StAX、XPath、XSLT、
XML Schema 验证和 XML Catalog 等完整的 XML 处理能力。内部实现基于 Apache Xerces (解析)
和 Apache Xalan (转换) 的 JDK 内置分支。

**源码统计**: 1855 个 Java 文件

### 模块定义 (Module Declaration)

**文件**: `src/java.xml/share/classes/module-info.java`

```java
module java.xml {
    // 公开 API 导出
    exports javax.xml;
    exports javax.xml.catalog;
    exports javax.xml.datatype;
    exports javax.xml.namespace;
    exports javax.xml.parsers;
    exports javax.xml.stream;
    exports javax.xml.stream.events;
    exports javax.xml.stream.util;
    exports javax.xml.transform;
    exports javax.xml.transform.dom;
    exports javax.xml.transform.sax;
    exports javax.xml.transform.stax;
    exports javax.xml.transform.stream;
    exports javax.xml.validation;
    exports javax.xml.xpath;
    exports org.w3c.dom;
    exports org.w3c.dom.bootstrap;
    exports org.w3c.dom.events;
    exports org.w3c.dom.ls;
    exports org.w3c.dom.ranges;
    exports org.w3c.dom.traversal;
    exports org.w3c.dom.views;
    exports org.xml.sax;
    exports org.xml.sax.ext;
    exports org.xml.sax.helpers;

    // 限定导出 (供 jdk.javadoc 等使用)
    exports com.sun.org.apache.xml.internal.dtm to ...;
    exports com.sun.org.apache.xml.internal.utils to ...;
    exports com.sun.org.apache.xpath.internal to ...;
    // ...

    // SPI 服务发现
    uses javax.xml.datatype.DatatypeFactory;
    uses javax.xml.parsers.DocumentBuilderFactory;
    uses javax.xml.parsers.SAXParserFactory;
    uses javax.xml.stream.XMLEventFactory;
    uses javax.xml.stream.XMLInputFactory;
    uses javax.xml.stream.XMLOutputFactory;
    uses javax.xml.transform.TransformerFactory;
    uses javax.xml.validation.SchemaFactory;
}
```

### 架构 (Architecture)

```
┌──────────────────────────────────────────────────────────┐
│                      应用代码                              │
│  DOM / SAX / StAX / XPath / XSLT / Validation / Catalog │
├──────────────────────────────────────────────────────────┤
│                    JAXP 抽象工厂层                         │
│  DocumentBuilderFactory / SAXParserFactory                │
│  XMLInputFactory / TransformerFactory                     │
│  XPathFactory / SchemaFactory / CatalogManager            │
├──────────────────────────────────────────────────────────┤
│                    内置实现 (Internal)                      │
│  Xerces (解析/验证) / Xalan (XSLT) / 内置 StAX           │
│  com.sun.org.apache.xerces.internal.*                     │
│  com.sun.org.apache.xalan.internal.*                      │
│  com.sun.xml.internal.stream.*                            │
├──────────────────────────────────────────────────────────┤
│                    安全管理                                │
│  jdk.xml.internal.XMLSecurityManager                     │
│  jdk.xml.internal.JdkXmlFeatures                         │
└──────────────────────────────────────────────────────────┘
```

---

## 2. 包结构 (Package Structure)

### 公开 API 包

| 包 | 说明 |
|---|------|
| `javax.xml` | 核心常量 (`XMLConstants`) |
| `javax.xml.catalog` | XML Catalog API (JDK 9+) |
| `javax.xml.datatype` | XML 数据类型 (`Duration`, `XMLGregorianCalendar`) |
| `javax.xml.namespace` | 命名空间支持 (`QName`, `NamespaceContext`) |
| `javax.xml.parsers` | 解析器工厂 (`DocumentBuilderFactory`, `SAXParserFactory`) |
| `javax.xml.stream` | StAX 流式 API (`XMLStreamReader`, `XMLStreamWriter`) |
| `javax.xml.stream.events` | StAX 事件 API (`XMLEvent`, `StartElement` 等) |
| `javax.xml.stream.util` | StAX 工具 (`StreamReaderDelegate`, `EventReaderDelegate`) |
| `javax.xml.transform` | XSLT 转换 API (`Transformer`, `TransformerFactory`) |
| `javax.xml.transform.dom` | DOM 源/结果 (`DOMSource`, `DOMResult`) |
| `javax.xml.transform.sax` | SAX 源/结果 (`SAXSource`, `SAXResult`) |
| `javax.xml.transform.stax` | StAX 源/结果 (`StAXSource`, `StAXResult`) |
| `javax.xml.transform.stream` | 流源/结果 (`StreamSource`, `StreamResult`) |
| `javax.xml.validation` | XML Schema 验证 (`SchemaFactory`, `Validator`) |
| `javax.xml.xpath` | XPath 查询 (`XPath`, `XPathExpression`, `XPathFactory`) |
| `org.w3c.dom` | DOM API (W3C 标准接口) |
| `org.w3c.dom.bootstrap` | DOM 实现注册 (`DOMImplementationRegistry`) |
| `org.w3c.dom.events` | DOM 事件 |
| `org.w3c.dom.ls` | DOM Load/Save |
| `org.w3c.dom.ranges` | DOM Range |
| `org.w3c.dom.traversal` | DOM Traversal (`NodeIterator`, `TreeWalker`) |
| `org.xml.sax` | SAX API (`XMLReader`, `ContentHandler`, `ErrorHandler`) |
| `org.xml.sax.ext` | SAX 扩展 (`LexicalHandler`, `DeclHandler`) |
| `org.xml.sax.helpers` | SAX 工具 (`DefaultHandler`, `XMLReaderFactory`) |

### 内部实现包

| 包前缀 | 说明 |
|--------|------|
| `com.sun.org.apache.xerces.internal.*` | Xerces XML 解析器 (DOM/SAX 实现) |
| `com.sun.org.apache.xerces.internal.dom` | DOM 实现 (DocumentImpl, ElementImpl 等) |
| `com.sun.org.apache.xerces.internal.impl` | 解析器核心实现 |
| `com.sun.org.apache.xerces.internal.impl.dtd` | DTD 处理 |
| `com.sun.org.apache.xerces.internal.impl.xs` | XML Schema 实现 |
| `com.sun.org.apache.xerces.internal.jaxp` | JAXP 桥接 (工厂实现) |
| `com.sun.org.apache.xerces.internal.jaxp.validation` | Schema 验证实现 |
| `com.sun.org.apache.xerces.internal.parsers` | SAX/DOM 解析器 |
| `com.sun.org.apache.xalan.internal.*` | Xalan XSLT 处理器 |
| `com.sun.org.apache.xalan.internal.xsltc` | XSLTC 编译型 XSLT |
| `com.sun.org.apache.xalan.internal.xsltc.compiler` | XSLT 编译器 |
| `com.sun.org.apache.xalan.internal.xsltc.trax` | TrAX 桥接 |
| `com.sun.org.apache.xml.internal.dtm` | Document Table Model |
| `com.sun.org.apache.xml.internal.serializer` | XML 序列化 |
| `com.sun.org.apache.xml.internal.utils` | XML 工具类 |
| `com.sun.org.apache.xpath.internal` | XPath 实现 |
| `com.sun.org.apache.bcel.internal` | 字节码工程库 (XSLTC 使用) |
| `com.sun.xml.internal.stream` | StAX 实现 |
| `jdk.xml.internal` | JDK 安全配置和工具类 |

---

## 3. XML 处理模型对比 (Processing Models)

| 特性 | DOM | SAX | StAX (拉模式) |
|------|-----|-----|---------------|
| 解析方式 | 全部加载到内存 | 事件推送 (Push) | 事件拉取 (Pull) |
| 内存占用 | 高 (整个文档树) | 低 (流式) | 低 (流式) |
| 随机访问 | 支持 | 不支持 | 不支持 |
| 文档修改 | 支持 | 不支持 | 不支持 |
| 写入 XML | 通过 Transformer | 不支持 | XMLStreamWriter |
| 适用场景 | 小文档、需修改 | 大文档、只读 | 大文档、需控制 |
| 工厂类 | DocumentBuilderFactory | SAXParserFactory | XMLInputFactory |

### 3.1 DOM (Document Object Model)

**解析器工厂**: `javax.xml.parsers.DocumentBuilderFactory`
**内部实现**: `com.sun.org.apache.xerces.internal.jaxp.DocumentBuilderFactoryImpl`

```java
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
factory.setNamespaceAware(true);
DocumentBuilder builder = factory.newDocumentBuilder();
Document doc = builder.parse(new File("input.xml"));

// 遍历 (Traversal)
Element root = doc.getDocumentElement();
NodeList nodes = root.getElementsByTagName("item");
for (int i = 0; i < nodes.getLength(); i++) {
    Element item = (Element) nodes.item(i);
    String name = item.getTextContent();
}

// 修改 (Modification)
Element newItem = doc.createElement("item");
newItem.setTextContent("New Item");
root.appendChild(newItem);

// 输出 (Serialization)
TransformerFactory tf = TransformerFactory.newInstance();
Transformer transformer = tf.newTransformer();
transformer.setOutputProperty(OutputKeys.INDENT, "yes");
transformer.transform(new DOMSource(doc), new StreamResult("output.xml"));
```

### 3.2 SAX (Simple API for XML)

**解析器工厂**: `javax.xml.parsers.SAXParserFactory`
**内部实现**: `com.sun.org.apache.xerces.internal.jaxp.SAXParserFactoryImpl`

```java
SAXParserFactory factory = SAXParserFactory.newInstance();
factory.setNamespaceAware(true);
SAXParser parser = factory.newSAXParser();

parser.parse("input.xml", new DefaultHandler() {
    @Override
    public void startElement(String uri, String localName,
                           String qName, Attributes attributes) {
        System.out.println("Start: " + localName);
    }

    @Override
    public void characters(char[] ch, int start, int length) {
        System.out.println("Text: " + new String(ch, start, length));
    }

    @Override
    public void endElement(String uri, String localName, String qName) {
        System.out.println("End: " + localName);
    }
});
```

### 3.3 StAX (Streaming API for XML)

**输入工厂**: `javax.xml.stream.XMLInputFactory`
**输出工厂**: `javax.xml.stream.XMLOutputFactory`
**内部实现**: `com.sun.xml.internal.stream.*`

```java
// 读取 (XMLStreamReader - 游标 API)
XMLInputFactory factory = XMLInputFactory.newInstance();
XMLStreamReader reader = factory.createXMLStreamReader(
    new FileInputStream("input.xml"));

while (reader.hasNext()) {
    int event = reader.next();
    switch (event) {
        case XMLStreamConstants.START_ELEMENT:
            System.out.println("Start: " + reader.getLocalName());
            break;
        case XMLStreamConstants.CHARACTERS:
            System.out.println("Text: " + reader.getText());
            break;
        case XMLStreamConstants.END_ELEMENT:
            System.out.println("End: " + reader.getLocalName());
            break;
    }
}

// 写入 (XMLStreamWriter)
XMLOutputFactory outFactory = XMLOutputFactory.newInstance();
XMLStreamWriter writer = outFactory.createXMLStreamWriter(
    new FileOutputStream("output.xml"));
writer.writeStartDocument("UTF-8", "1.0");
writer.writeStartElement("root");
writer.writeAttribute("version", "1.0");
writer.writeStartElement("item");
writer.writeCharacters("Content");
writer.writeEndElement();
writer.writeEndElement();
writer.writeEndDocument();
writer.close();
```

---

## 4. XPath

**工厂**: `javax.xml.xpath.XPathFactory`
**内部实现**: `com.sun.org.apache.xpath.internal.*`

```java
XPathFactory xPathFactory = XPathFactory.newInstance();
XPath xpath = xPathFactory.newXPath();

Document doc = ...; // DOM 文档

// 简单查询 (Simple query)
String title = xpath.evaluate("//book[1]/title", doc);

// 编译表达式 (Compiled expression)
XPathExpression expr = xpath.compile("//book[price>35]");
NodeList nodes = (NodeList) expr.evaluate(doc, XPathConstants.NODESET);

// 数值查询 (Numeric query)
double total = (Double) xpath.evaluate(
    "sum(//book/price)", doc, XPathConstants.NUMBER);

// 带命名空间 (With namespace)
xpath.setNamespaceContext(new NamespaceContext() {
    public String getNamespaceURI(String prefix) {
        if ("ns".equals(prefix)) return "http://example.com/ns";
        return null;
    }
    public String getPrefix(String namespaceURI) { return null; }
    public Iterator<String> getPrefixes(String namespaceURI) {
        return Collections.emptyIterator();
    }
});
String value = xpath.evaluate("//ns:element/text()", doc);
```

**常用 XPath 表达式 (Common XPath Expressions)**:

| 表达式 | 说明 |
|--------|------|
| `/bookstore/book` | 根下 bookstore 下所有 book |
| `//book` | 任意位置的 book |
| `//book[@category='web']` | category 属性为 web 的 book |
| `//book[price>35]` | 价格大于 35 的 book |
| `//book/title/text()` | 所有 title 的文本内容 |
| `count(//book)` | book 元素数量 |
| `//book[last()]` | 最后一个 book |

---

## 5. XSLT 转换 (XSLT Transformation)

**工厂**: `javax.xml.transform.TransformerFactory`
**内部实现**: `com.sun.org.apache.xalan.internal.xsltc.trax.TransformerFactoryImpl`

JDK 内置的 XSLT 处理器使用 XSLTC (编译型)，将 XSLT 样式表编译为 Java 字节码执行，
使用内置的 BCEL (Byte Code Engineering Library) 生成字节码。

```java
TransformerFactory factory = TransformerFactory.newInstance();
Source xslt = new StreamSource(new File("transform.xsl"));
Transformer transformer = factory.newTransformer(xslt);

// 设置输出属性
transformer.setOutputProperty(OutputKeys.INDENT, "yes");
transformer.setOutputProperty(OutputKeys.ENCODING, "UTF-8");

// 执行转换
transformer.transform(
    new StreamSource(new File("input.xml")),
    new StreamResult(new File("output.html"))
);
```

---

## 6. XML Schema 验证 (Validation)

**工厂**: `javax.xml.validation.SchemaFactory`
**内部实现**: `com.sun.org.apache.xerces.internal.jaxp.validation.*`

```java
SchemaFactory sf = SchemaFactory.newInstance(XMLConstants.W3C_XML_SCHEMA_NS_URI);
Schema schema = sf.newSchema(new File("schema.xsd"));
Validator validator = schema.newValidator();

try {
    validator.validate(new StreamSource(new File("document.xml")));
    System.out.println("Valid");
} catch (SAXException e) {
    System.out.println("Invalid: " + e.getMessage());
}
```

---

## 7. XML Catalog (JDK 9+)

**包**: `javax.xml.catalog`

XML Catalog 提供本地 URI 解析，避免外部实体引用带来的安全风险和网络依赖。

```java
// 创建 Catalog
CatalogFeatures features = CatalogFeatures.builder()
    .with(CatalogFeatures.Feature.FILES, "catalog.xml")
    .build();

Catalog catalog = CatalogManager.catalog(features);

// 创建 CatalogResolver 用于解析外部实体
CatalogResolver resolver = CatalogManager.catalogResolver(catalog);

// 在解析器中使用
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
DocumentBuilder builder = factory.newDocumentBuilder();
builder.setEntityResolver(resolver);
Document doc = builder.parse("document.xml");
```

---

## 8. 安全配置 (Security Configuration)

### JDK XML 安全管理 (jdk.xml.internal)

| 文件 | 说明 |
|------|------|
| `XMLSecurityManager.java` | XML 处理安全限制管理 |
| `XMLSecurityPropertyManager.java` | 安全属性管理 |
| `JdkXmlFeatures.java` | JDK XML 特性开关 |
| `JdkXmlConfig.java` | JDK XML 配置 |
| `JdkConstants.java` | JDK XML 常量 |
| `JdkXmlUtils.java` | 安全相关工具方法 |
| `XMLLimitAnalyzer.java` | XML 限制分析器 (防 DoS) |

### 防止 XXE 攻击 (Preventing XXE)

```java
// 推荐的安全配置
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();

// 禁用外部实体
factory.setFeature(
    "http://apache.org/xml/features/disallow-doctype-decl", true);
factory.setFeature(
    "http://xml.org/sax/features/external-general-entities", false);
factory.setFeature(
    "http://xml.org/sax/features/external-parameter-entities", false);
factory.setXIncludeAware(false);
factory.setExpandEntityReferences(false);

DocumentBuilder builder = factory.newDocumentBuilder();
```

### JAXP 属性配置 (Configuration Properties)

JAXP 属性优先级 (从高到低):
1. **API 调用**: `factory.setFeature()` / `factory.setAttribute()`
2. **系统属性**: `-Djavax.xml...` / `System.setProperty()`
3. **配置文件**: `$JAVA_HOME/conf/jaxp.properties`
4. **默认值**

`jaxp.properties` 文件位于 `$JAVA_HOME/conf/jaxp.properties`，也可通过
`java.xml.config.file` 系统属性指定自定义配置文件。

---

## 9. 使用建议 (Best Practices)

### 选择合适的 API

| 场景 | 推荐 API | 理由 |
|------|----------|------|
| 小文档修改 | DOM | 支持随机访问和修改 |
| 大文件只读 | SAX 或 StAX | 流式处理，低内存 |
| 性能敏感解析 | StAX (XMLStreamReader) | 拉模式，更好的控制 |
| 节点查询 | XPath | 声明式查询 |
| 文档转换 | XSLT | 声明式转换 |
| XML 验证 | SchemaFactory + Validator | W3C XML Schema |

### 性能优化

```java
// 重用工厂实例 (Factory 本身是线程安全的)
private static final DocumentBuilderFactory DOM_FACTORY =
    DocumentBuilderFactory.newInstance();

// StAX: 启用合并文本节点
XMLInputFactory factory = XMLInputFactory.newInstance();
factory.setProperty(XMLInputFactory.IS_COALESCING, true);

// StAX: 大文件分批处理
XMLStreamReader reader = factory.createXMLStreamReader(input);
while (reader.hasNext()) {
    if (reader.next() == XMLStreamConstants.START_ELEMENT
        && "item".equals(reader.getLocalName())) {
        processItem(reader.getElementText());
    }
}
```

---

## 10. 相关链接 (Related Links)

- [JAXP 教程](https://docs.oracle.com/javase/tutorial/jaxp/)
- [StAX 规范 (JSR 173)](https://jcp.org/en/jsr/detail?id=173)
- [XPath 规范](https://www.w3.org/TR/xpath/)
- [XML Catalog 规范 (OASIS)](https://www.oasis-open.org/committees/entity/)
- [源码](https://github.com/openjdk/jdk/tree/master/src/java.xml/share/classes)
