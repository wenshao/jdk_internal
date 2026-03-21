# ZoneId 源码分析

> java.time.ZoneId 的完整实现分析

---
## 目录

1. [类声明](#1-类声明)
2. [类型层次结构](#2-类型层次结构)
3. [字段定义](#3-字段定义)
4. [工厂方法](#4-工厂方法)
5. [ZoneRegion 内部实现](#5-zoneregion-内部实现)
6. [抽象方法](#6-抽象方法)
7. [实例方法](#7-实例方法)
8. [序列化机制](#8-序列化机制)
9. [时区 ID 类型](#9-时区-id-类型)
10. [可用时区 ID](#10-可用时区-id)
11. [线程安全](#11-线程安全)
12. [性能特性](#12-性能特性)
13. [与旧 API 对比](#13-与旧-api-对比)
14. [常见使用场景](#14-常见使用场景)
15. [最佳实践](#15-最佳实践)
16. [相关文档](#16-相关文档)

---


## 1. 类声明

```java
@jdk.internal.ValueBased
public abstract sealed class ZoneId implements Serializable
    permits ZoneOffset, ZoneRegion {
```

**关键设计决策**:
- `abstract sealed` - 密封类，只允许两个子类
- `permits ZoneOffset, ZoneRegion` - 固定偏移和地理区域两种实现
- `@jdk.internal.ValueBased` - 基于值的类
- `Serializable` - 支持序列化

**设计模式**: 策略模式 + 工厂模式

---

## 2. 类型层次结构

```
                    ZoneId (abstract sealed)
                           /    \
                          /      \
               ZoneOffset        ZoneRegion
              (固定偏移)         (地理区域)
```

### ZoneOffset

表示固定的 UTC 偏移量，如 `+08:00`, `-05:00`, `Z` (UTC)。

**特点**:
- 偏移量永不变化
- 无夏令时
- 适用于海洋区域、科学研究等

### ZoneRegion

表示地理区域，如 `Asia/Shanghai`, `America/New_York`。

**特点**:
- 偏移量根据规则变化（夏令时）
- 规则由政府定义，频繁变更
- 与 IANA TZDB 数据库同步

---

## 3. 字段定义

### SHORT_IDS - 短时区名称映射

```java
/**
 * 短时区名称到标准 ID 的映射
 * 用于兼容旧 API (java.util.TimeZone)
 */
public static final Map<String, String> SHORT_IDS = Map.ofEntries(
    entry("ACT", "Australia/Darwin"),
    entry("AET", "Australia/Sydney"),
    entry("AGT", "America/Argentina/Buenos_Aires"),
    entry("ART", "Africa/Cairo"),
    entry("AST", "America/Anchorage"),
    entry("BET", "America/Sao_Paulo"),
    entry("BST", "Asia/Dhaka"),
    entry("CAT", "Africa/Harare"),
    entry("CNT", "America/St_Johns"),
    entry("CST", "America/Chicago"),
    entry("CTT", "Asia/Shanghai"),
    entry("EAT", "Africa/Addis_Ababa"),
    entry("ECT", "Europe/Paris"),
    entry("EST", "America/Panama"),
    entry("HST", "Pacific/Honolulu"),
    entry("IET", "America/Indiana/Indianapolis"),
    entry("IST", "Asia/Kolkata"),
    entry("JST", "Asia/Tokyo"),
    entry("MIT", "Pacific/Apia"),
    entry("MST", "America/Phoenix"),
    entry("NET", "Asia/Yerevan"),
    entry("NST", "Pacific/Auckland"),
    entry("PLT", "Asia/Karachi"),
    entry("PNT", "America/Phoenix"),
    entry("PRT", "America/Puerto_Rico"),
    entry("PST", "America/Los_Angeles"),
    entry("SST", "Pacific/Guadalcanal"),
    entry("VST", "Asia/Ho_Chi_Minh")
);
```

**重要变更 (JDK 23+)**:
- `EST` 现在映射到 `America/Panama`（无夏令时）
- `MST` 映射到 `America/Phoenix`（无夏令时）
- `HST` 映射到 `Pacific/Honolulu`（无夏令时）

**设计原因**: 短缩写有歧义，不推荐使用，但为向后兼容保留。

---

## 4. 工厂方法

### systemDefault() - 获取系统默认时区

```java
public static ZoneId systemDefault() {
    return TimeZone.getDefault().toZoneId();
}
```

**来源**:
- 操作系统时区设置
- JVM 参数 `-Duser.timezone`
- 环境变量 `TZ`

### of(String) - 从 ID 创建

```java
public static ZoneId of(String zoneId) {
    return of(zoneId, true);
}

static ZoneId of(String zoneId, boolean checkAvailable) {
    Objects.requireNonNull(zoneId, "zoneId");

    // 1. 单字符或 +/- 开头 -> ZoneOffset
    if (zoneId.length() <= 1 || zoneId.startsWith("+") || zoneId.startsWith("-")) {
        return ZoneOffset.of(zoneId);
    }
    // 2. UTC 或 GMT 前缀
    else if (zoneId.startsWith("UTC") || zoneId.startsWith("GMT")) {
        return ofWithPrefix(zoneId, 3, checkAvailable);
    }
    // 3. UT 前缀
    else if (zoneId.startsWith("UT")) {
        return ofWithPrefix(zoneId, 2, checkAvailable);
    }
    // 4. 区域 ID
    return ZoneRegion.ofId(zoneId, checkAvailable);
}
```

**解析规则**:

| 输入格式 | 示例 | 返回类型 |
|---------|------|---------|
| `Z` | `Z` | `ZoneOffset.UTC` |
| `+hh:mm` | `+08:00` | `ZoneOffset` |
| `-hh:mm` | `-05:00` | `ZoneOffset` |
| `UTC` | `UTC` | `ZoneRegion` with UTC rules |
| `UTC+hh:mm` | `UTC+08:00` | `ZoneRegion` with prefix |
| `GMT+hh:mm` | `GMT+02:00` | `ZoneRegion` with prefix |
| `Area/City` | `Asia/Shanghai` | `ZoneRegion` |

### of(String, Map) - 使用别名映射

```java
public static ZoneId of(String zoneId, Map<String, String> aliasMap) {
    Objects.requireNonNull(zoneId, "zoneId");
    Objects.requireNonNull(aliasMap, "aliasMap");
    String id = Objects.requireNonNullElse(aliasMap.get(zoneId), zoneId);
    return of(id);
}
```

**使用示例**:
```java
Map<String, String> aliases = Map.of("PST", "America/Los_Angeles");
ZoneId zone = ZoneId.of("PST", aliases);  // 使用别名
```

### ofOffset() - 创建带前缀的偏移 ID

```java
public static ZoneId ofOffset(String prefix, ZoneOffset offset) {
    Objects.requireNonNull(prefix, "prefix");
    Objects.requireNonNull(offset, "offset");

    if (prefix.isEmpty()) {
        return offset;
    }
    if (!prefix.equals("GMT") && !prefix.equals("UTC") && !prefix.equals("UT")) {
        throw new IllegalArgumentException("prefix should be GMT, UTC or UT, is: " + prefix);
    }
    if (offset.getTotalSeconds() != 0) {
        prefix = prefix.concat(offset.getId());
    }
    return new ZoneRegion(prefix, offset.getRules());
}
```

---

## 5. ZoneRegion 内部实现

### 字段存储

```java
final class ZoneRegion extends ZoneId implements Serializable {
    private static final long serialVersionUID = 8386373296231747096L;

    /** 时区 ID，非 null */
    private final String id;

    /** 时区规则，可为 null (延迟加载) */
    private final transient ZoneRules rules;
}
```

**设计特点**:
- `final String id` - 不可变 ID
- `final transient ZoneRules rules` - 规则不序列化，按需加载
- `transient` - 序列化时只保存 ID，规则从提供者获取

### ofId() - 创建区域 ID

```java
static ZoneRegion ofId(String zoneId, boolean checkAvailable) {
    Objects.requireNonNull(zoneId, "zoneId");
    checkName(zoneId);

    ZoneRules rules = null;
    try {
        // 总是尝试加载规则，以便反序列化后有更好的行为
        rules = ZoneRulesProvider.getRules(zoneId, true);
    } catch (ZoneRulesException ex) {
        if (checkAvailable) {
            throw ex;
        }
    }
    return new ZoneRegion(zoneId, rules);
}
```

### checkName() - 验证 ID 格式

```java
private static void checkName(String zoneId) {
    int n = zoneId.length();
    if (n < 2) {
        throw new DateTimeException("Invalid ID for region-based ZoneId, invalid format: " + zoneId);
    }
    for (int i = 0; i < n; i++) {
        char c = zoneId.charAt(i);
        if (c >= 'a' && c <= 'z') continue;
        if (c >= 'A' && c <= 'Z') continue;
        if (c == '/' && i != 0) continue;
        if (c >= '0' && c <= '9' && i != 0) continue;
        if (c == '~' && i != 0) continue;      // 组名分隔符
        if (c == '.' && i != 0) continue;
        if (c == '_' && i != 0) continue;
        if (c == '+' && i != 0) continue;
        if (c == '-' && i != 0) continue;
        throw new DateTimeException("Invalid ID for region-based ZoneId, invalid format: " + zoneId);
    }
}
```

**正则表达式等价**: `[A-Za-z][A-Za-z0-9~/._+-]+`

**命名约定**:
- IANA TZDB: `Area/City` (如 `Europe/Paris`)
- 其他组: `group~region` (如 `IATA~UTC`)

### getRules() - 获取时区规则

```java
@Override
public ZoneRules getRules() {
    // rules 为 null 时重新查询，允许提供者在创建后更新
    return (rules != null ? rules : ZoneRulesProvider.getRules(id, false));
}
```

**延迟加载设计**:
- 首次访问时加载规则
- 支持规则动态更新
- 减少启动时开销

---

## 6. 抽象方法

### getId() - 获取时区 ID

```java
public abstract String getId();
```

**返回值**:
- `ZoneOffset`: `+08:00`, `-05:00`, `Z`
- `ZoneRegion`: `Asia/Shanghai`, `America/New_York`, `UTC+08:00`

### getRules() - 获取时区规则

```java
public abstract ZoneRules getRules();
```

**ZoneRules 提供**:
- 特定时刻的偏移量
- 夏令时转换规则
- 历史偏移变更

### getOffset(long) - 获取特定时刻的偏移

```java
abstract ZoneOffset getOffset(long epochSecond);
```

**包私有方法**，用于内部优化。

---

## 7. 实例方法

### normalized() - 规范化

```java
public ZoneId normalized() {
    try {
        ZoneRules rules = getRules();
        if (rules.isFixedOffset()) {
            return rules.getOffset(Instant.EPOCH);
        }
    } catch (ZoneRulesException ex) {
        // 无效的 ZoneRegion 对此方法不重要
    }
    return this;
}
```

**行为**:
- 固定偏移时区 → 返回 `ZoneOffset`
- 变化偏移时区 → 返回 `this`

**使用场景**:
```java
ZoneId utc = ZoneId.of("UTC").normalized();        // ZoneOffset.of("Z")
ZoneId shanghai = ZoneId.of("Asia/Shanghai").normalized();  // ZoneId("Asia/Shanghai")
```

### getDisplayName() - 获取显示名称

```java
public String getDisplayName(TextStyle style, Locale locale) {
    return new DateTimeFormatterBuilder()
        .appendZoneText(style)
        .toFormatter(locale)
        .format(toTemporal());
}
```

**使用示例**:
```java
ZoneId zone = ZoneId.of("America/New_York");

String fullName = zone.getDisplayName(TextStyle.FULL, Locale.US);    // "Eastern Time"
String shortName = zone.getDisplayName(TextStyle.SHORT, Locale.US);  // "ET"
```

### from() - 从 TemporalAccessor 获取

```java
public static ZoneId from(TemporalAccessor temporal) {
    ZoneId obj = temporal.query(TemporalQueries.zone());
    if (obj == null) {
        throw new DateTimeException("Unable to obtain ZoneId from TemporalAccessor: " +
            temporal + " of type " + temporal.getClass().getName());
    }
    return obj;
}
```

**方法引用**:
```java
// 作为方法引用使用
stream.map(ZoneId::from)
```

---

## 8. 序列化机制

### ZoneId 序列化

```java
private Object writeReplace() {
    return new Ser(Ser.ZONE_REGION_TYPE, this);
}

private void readObject(ObjectInputStream s) throws InvalidObjectException {
    throw new InvalidObjectException("Deserialization via serialization delegate");
}
```

**序列化格式**:
```
out.writeByte(7);           // ZoneId 类型标识
out.writeUTF(getId());      // 时区 ID 字符串
```

### ZoneRegion 序列化

```java
void writeExternal(DataOutput out) throws IOException {
    out.writeUTF(id);        // 只写 ID
}

static ZoneId readExternal(DataInput in) throws IOException {
    String id = in.readUTF();
    return ZoneId.of(id, false);  // lenient 模式，允许未知 ID
}
```

**关键设计**:
- 只序列化 ID，不序列化规则
- 反序列化时从 `ZoneRulesProvider` 获取规则
- 支持跨版本序列化（新 JVM → 旧 JVM）

**未知 ID 处理**:
```java
// 在旧 JVM 上反序列化新时区 ID
ZoneId unknown = deserialize("Asia/New_City_2025");
unknown.getId();           // 正常返回 "Asia/New_City_2025"
unknown.equals(other);     // 正常工作
unknown.getRules();        // 抛出 ZoneRulesException
```

---

## 9. 时区 ID 类型

### 类型 1: 固定偏移 (ZoneOffset)

```
Z          - UTC (零偏移)
+08:00     - 东八区
-05:00     - 西五区
```

### 类型 2: 前缀偏移

```
UTC+08:00  - UTC 前缀 + 偏移
GMT+02:00  - GMT 前缀 + 偏移
UT-05:00   - UT 前缀 + 偏移
```

**特点**:
- 规则等同于固定偏移
- ID 保留前缀格式

### 类型 3: 地理区域

```
Asia/Shanghai
America/New_York
Europe/London
Australia/Sydney
```

**IANA TZDB 命名规范**:
- `Area/Location` 格式
- Area: 洲或大洋 (Africa, America, Antarctica, Arctic, Asia, Atlantic, Australia, Europe, Indian, Pacific)
- Location: 城市或地区
- 使用下划线代替空格

---

## 10. 可用时区 ID

```java
public static Set<String> getAvailableZoneIds() {
    return new HashSet<>(ZoneRulesProvider.getAvailableZoneIds());
}
```

**数量**: 约 600 个区域 ID (随 TZDB 版本更新)

**示例**:
```java
ZoneId.getAvailableZoneIds().stream()
    .filter(id -> id.startsWith("Asia/"))
    .sorted()
    .forEach(System.out::println);
// 输出:
// Asia/Aden
// Asia/Almaty
// Asia/Amman
// Asia/Anadyr
// Asia/Aqtau
// ...
```

---

## 11. 线程安全

### ZoneId 线程安全保证

```java
// 所有字段都是 final
private final String id;          // ZoneRegion
private final transient ZoneRules rules;

// 所有方法返回新对象或不可变对象
public ZoneId normalized() { ... }
public String getDisplayName(...) { ... }
```

**线程安全策略**:
1. 不可变对象
2. `ZoneRules` 本身也是不可变的
3. `ZoneRulesProvider` 保证线程安全

---

## 12. 性能特性

### 规则缓存

```java
private final transient ZoneRules rules;
```

- 首次 `getRules()` 调用时加载
- 后续调用直接返回缓存
- 跨序列化边界时重新加载

### 规范化优化

```java
ZoneId zone = ZoneId.of("UTC");     // ZoneRegion 实例
ZoneId normalized = zone.normalized();  // ZoneOffset 实例
```

**优化效果**:
- 固定偏移时区使用更轻量的 `ZoneOffset`
- 避免不必要的规则查询

### 短 ID 映射

```java
ZoneId.of("CTT", ZoneId.SHORT_IDS);  // Asia/Shanghai
```

- `Map.ofEntries()` 创建不可变映射
- O(1) 查找时间

---

## 13. 与旧 API 对比

### java.util.TimeZone vs ZoneId

| 特性 | TimeZone | ZoneId |
|------|----------|--------|
| 可变性 | 可变 | 不可变 |
| 线程安全 | ❌ | ✅ |
| ID 类型 | 整数偏移 + 字符串 | 统一字符串 |
| 序列化 | 序列化完整状态 | 只序列化 ID |
| 夏令时 | 内置复杂逻辑 | 委托给 ZoneRules |
| 规则更新 | 需要更新 JDK | 可通过提供者更新 |

### 迁移示例

```java
// 旧 API
TimeZone tz = TimeZone.getTimeZone("America/New_York");
int offset = tz.getOffset(System.currentTimeMillis());

// 新 API
ZoneId zone = ZoneId.of("America/New_York");
ZoneRules rules = zone.getRules();
ZoneOffset offset = rules.getOffset(Instant.now());
```

---

## 14. 常见使用场景

### 获取系统时区

```java
ZoneId systemZone = ZoneId.systemDefault();
System.out.println(systemZone);  // Asia/Shanghai (取决于系统设置)
```

### 创建固定偏移时区

```java
ZoneId utc = ZoneId.of("Z");
ZoneId plus8 = ZoneId.of("+08:00");
ZoneId minus5 = ZoneId.of("-05:00");
```

### 创建地理时区

```java
ZoneId shanghai = ZoneId.of("Asia/Shanghai");
ZoneId newYork = ZoneId.of("America/New_York");
ZoneId london = ZoneId.of("Europe/London");
```

### 使用短 ID (不推荐)

```java
ZoneId cst = ZoneId.of("CST", ZoneId.SHORT_IDS);  // America/Chicago
```

### 规范化

```java
ZoneId utc1 = ZoneId.of("UTC");
ZoneId utc2 = utc1.normalized();
System.out.println(utc2);  // Z
```

### 转换为 ZonedDateTime

```java
ZoneId zone = ZoneId.of("Asia/Shanghai");
ZonedDateTime now = ZonedDateTime.now(zone);
```

---

## 15. 最佳实践

### ✅ 推荐

```java
// 使用地理区域 ID
ZoneId zone = ZoneId.of("Asia/Shanghai");

// 缓存 ZoneId 实例
private static final ZoneId SYSTEM_ZONE = ZoneId.systemDefault();

// 使用 ZoneOffset 处理固定偏移
ZoneOffset offset = ZoneOffset.of("+08:00");
```

### ❌ 避免

```java
// 使用短 ID (有歧义)
ZoneId zone = ZoneId.of("EST");  // 不要这样做

// 使用三字母缩写
ZoneId zone = ZoneId.of("CST");  // CST 可能是中美、中国、古巴标准时间

// 频繁创建相同 ZoneId
for (int i = 0; i < 1000; i++) {
    ZoneId zone = ZoneId.of("Asia/Shanghai");  // 缓存它
}
```

---

## 16. 相关文档

- [ZoneOffset 实现](zoneoffset.md)
- [ZoneRules 实现](zonerules.md)
- [ZonedDateTime 实现](../zoneddatetime/index.md)
- [主索引](../index.md)

---

> **更新时间**: 2026-03-20
> **源码版本**: OpenJDK 23
> **文件路径**: `src/java.base/share/classes/java/time/ZoneId.java`
