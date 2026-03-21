# java.xml 模块分析

> JAXP (Java API for XML Processing)，XML 处理标准 API

---

## 1. 模块概述

`java.xml` 是 Java 处理 XML 文档的标准 API，提供 DOM、SAX、StAX、XSLT、XPath 等多种 XML 处理方式。

### 模块定义

**文件**: `src/java.xml/share/classes/module-info.java`

```java
module java.xml {
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
    exports org.xml.sax;
    exports org.xml.sax.ext;
    exports org.xml.sax.helpers;
}
```

### 架构

```
┌─────────────────────────────────────────────────────────┐
│                     应用代码                              │
│  DOM / SAX / StAX / XPath / XSLT                        │
├─────────────────────────────────────────────────────────┤
│                   JAXP API                               │
│  javax.xml.parsers / javax.xml.stream / ...             │
├─────────────────────────────────────────────────────────┤
│                  Xerces / Xalan                          │
│  (默认实现: 内置 Xerces / Xalan)                         │
├─────────────────────────────────────────────────────────┤
│                    XML 文档                              │
└─────────────────────────────────────────────────────────┘
```

---

## 2. XML 处理模型

### 2.1 对比

| 模型 | 特点 | 适用场景 | JDK 26 状态 |
|------|------|----------|-------------|
| **DOM** | 树形结构, 随机访问 | 文档修改, 小文件 | ✓ |
| **SAX** | 事件驱动, 流式 | 大文件, 只读 | ✓ |
| **StAX** | 拉模式, 流式 | 大文件, 性能 | ✓ |
| **XPath** | 路径查询 | 节点查找 | ✓ |
| **XSLT** | 转换 | 文档转换 | ✓ |

### 2.2 DOM (Document Object Model)

**源码**: `src/java.xml/share/classes/org/w3c/dom/`

```java
// 解析文档
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
DocumentBuilder builder = factory.newDocumentBuilder();
Document doc = builder.parse(new File("input.xml"));

// 遍历
Element root = doc.getDocumentElement();
NodeList nodes = root.getElementsByTagName("item");
for (int i = 0; i < nodes.getLength(); i++) {
    Element item = (Element) nodes.item(i);
    String name = item.getTextContent();
}

// 修改
Element newItem = doc.createElement("item");
newItem.setTextContent("New Item");
root.appendChild(newItem);

// 写入
TransformerFactory tf = TransformerFactory.newInstance();
Transformer transformer = tf.newTransformer();
transformer.transform(new DOMSource(doc), new StreamResult("output.xml"));
```

**优点**: 随机访问, 易于修改
**缺点**: 内存占用大

### 2.3 SAX (Simple API for XML)

**源码**: `src/java.xml/share/classes/org/xml/sax/`

```java
SAXParserFactory factory = SAXParserFactory.newInstance();
SAXParser parser = factory.newSAXParser();

parser.parse("input.xml", new DefaultHandler() {
    @Override
    public void startElement(String uri, String localName,
                           String qName, Attributes attributes) {
        System.out.println("Start: " + qName);
    }

    @Override
    public void endElement(String uri, String localName, String qName) {
        System.out.println("End: " + qName);
    }

    @Override
    public void characters(char[] ch, int start, int length) {
        String content = new String(ch, start, length);
        System.out.println("Content: " + content);
    }
});
```

**优点**: 内存占用小, 流式处理
**缺点**: 只读, 不能修改文档

### 2.4 StAX (Streaming API for XML)

**源码**: `src/java.xml/share/classes/javax/xml/stream/`

```java
XMLInputFactory factory = XMLInputFactory.newInstance();
XMLStreamReader reader = factory.createXMLStreamReader(new FileInputStream("input.xml"));

while (reader.hasNext()) {
    int event = reader.next();
    switch (event) {
        case XMLStreamConstants.START_ELEMENT:
            System.out.println("Start: " + reader.getLocalName());
            break;
        case XMLStreamConstants.CHARACTERS:
            System.out.println("Content: " + reader.getText());
            break;
        case XMLStreamConstants.END_ELEMENT:
            System.out.println("End: " + reader.getLocalName());
            break;
    }
}

// 写入
XMLOutputFactory outFactory = XMLOutputFactory.newInstance();
XMLStreamWriter writer = outFactory.createXMLStreamWriter(new FileOutputStream("output.xml"));
writer.writeStartDocument();
writer.writeStartElement("root");
writer.writeCharacters("Content");
writer.writeEndElement();
writer.writeEndDocument();
```

**优点**: 拉模式, 性能好, 可读写
**缺点**: 只能顺序访问

---

## 3. XPath

**源码**: `src/java.xml/share/classes/javax/xml/xpath/XPath.java`

```java
XPathFactory xPathFactory = XPathFactory.newInstance();
XPath xpath = xPathFactory.newXPath();

// 编译表达式
XPathExpression expr = xpath.compile("//book[price>35]");

// 求值
InputSource source = new InputSource(new FileInputStream("books.xml"));
NodeList nodes = (NodeList) expr.evaluate(source, XPathConstants.NODESET);

// 简化 API
String title = xpath.evaluate("//book[1]/title", source);
double price = (Double) xpath.evaluate("sum(//book/price)", source, XPathConstants.NUMBER);
```

**常用 XPath 表达式**:

| 表达式 | 结果 |
|--------|------|
| `/bookstore/book` | 所有 book 元素 |
| `//book` | 任意位置的 book 元素 |
| `//book[@category='web']` | category 属性为 web 的 book |
| `//book[price>35]` | 价格大于 35 的 book |
| `//book/title/text()` | 所有 title 的文本 |

---

## 4. XSLT

**源码**: `src/java.xml/share/classes/javax/xml/transform/`

```java
TransformerFactory factory = TransformerFactory.newInstance();
Source xslt = new StreamSource(new File("transform.xsl"));
Transformer transformer = factory.newTransformer(xslt);

Source text = new StreamSource(new File("input.xml"));
Result result = new StreamResult(new File("output.xml"));

transformer.transform(text, result);
```

**XSLT 示例** (`transform.xsl`):

```xml
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <html>
            <body>
                <h2>Book Catalog</h2>
                <table border="1">
                    <tr>
                        <th>Title</th>
                        <th>Author</th>
                        <th>Price</th>
                    </tr>
                    <xsl:for-each select="bookstore/book">
                        <tr>
                            <td><xsl:value-of select="title"/></td>
                            <td><xsl:value-of select="author"/></td>
                            <td><xsl:value-of select="price"/></td>
                        </tr>
                    </xsl:for-each>
                </table>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
```

---

## 5. JDK 26 变更

### 5.1 性能改进

- StAX 解析器优化
- XPath 求值性能提升
- 减少内存占用

### 5.2 安全增强

- XXE (XML External Entity) 防护默认启用
- 禁用外部 DTD

```java
// JDK 26 默认配置
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
factory.setFeature("http://xml.org/sax/features/external-general-entities", false);
factory.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
```

### 5.3 新增 API

```java
// JDK 11+ 新增: XML Catalog 支持
CatalogResolver resolver = CatalogManager.catalogResolver(catalog);
```

---

## 6. 使用示例

### 6.1 读取配置文件

```java
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
DocumentBuilder builder = factory.newDocumentBuilder();
Document doc = builder.parse("config.xml");

// 读取属性
String value = (String) xpath.evaluate("//property[@name='timeout']/@value",
                                      doc, XPathConstants.STRING);
```

### 6.2 生成 XML

```java
// DOM 方式
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
DocumentBuilder builder = factory.newDocumentBuilder();
Document doc = builder.newDocument();

Element root = doc.createElement("config");
doc.appendChild(root);

Element prop = doc.createElement("property");
prop.setAttribute("name", "timeout");
prop.setAttribute("value", "5000");
root.appendChild(prop);

// 写入
TransformerFactory tf = TransformerFactory.newInstance();
Transformer transformer = tf.newTransformer();
transformer.setOutputProperty(OutputKeys.INDENT, "yes");
transformer.transform(new DOMSource(doc), new StreamResult("config.xml"));
```

### 6.3 StAX 大文件处理

```java
XMLInputFactory factory = XMLInputFactory.newInstance();
XMLStreamReader reader = factory.createXMLStreamReader(new FileInputStream("large.xml"));

StringBuilder buffer = new StringBuilder();
while (reader.hasNext()) {
    if (reader.next() == XMLStreamConstants.START_ELEMENT &&
        "item".equals(reader.getLocalName())) {
        // 只处理需要的元素
        buffer.append(reader.getElementText()).append("\n");
    }
}
```

### 6.4 命名空间处理

```java
// 配置命名空间感知
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
factory.setNamespaceAware(true);

// XPath 带命名空间
xpath.setNamespaceContext(new NamespaceContext() {
    public String getNamespaceURI(String prefix) {
        return "http://example.com/ns".equals(prefix) ? "http://example.com/ns" : null;
    }
    // ...
});

String expr = "//ex:book/ex:title";
```

---

## 7. 最佳实践

### 7.1 选择合适的 API

| 场景 | 推荐 |
|------|------|
| 小文件修改 | DOM |
| 大文件只读 | SAX / StAX |
| 需要随机访问 | DOM |
| 性能敏感 | StAX |
| 节点查询 | XPath |

### 7.2 安全配置

```java
// 防止 XXE 攻击
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
factory.setFeature("http://xml.org/sax/features/external-general-entities", false);
factory.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
factory.setXIncludeAware(false);
factory.setExpandEntityReferences(false);
```

### 7.3 性能优化

```java
// 重用 TransformerFactory (线程安全)
private static final TransformerFactory TRANSFORMER_FACTORY = TransformerFactory.newInstance();

// 使用 StAX 而不是 SAX (更好的控制)
XMLInputFactory factory = XMLInputFactory.newInstance();
factory.setProperty(XMLInputFactory.IS_COALESCING, true);
factory.setProperty(XMLInputFactory.IS_REPLACING_ENTITY_REFERENCES, false);
```

---

## 8. 相关链接

- [JAXP 规范](https://javaee.github.io/jaxp-spec/)
- [StAX 规范](https://jcp.org/en/jsr/detail?id=173)
- [XPath 规范](https://www.w3.org/TR/xpath/)
- [源码](https://github.com/openjdk/jdk/tree/master/src/java.xml/share/classes)
