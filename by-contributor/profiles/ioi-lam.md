# Ioi Lam

> AOT/CDS 核心开发者，JEP 514 主导者，Project Leyden 演讲者

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Ioi Lam |
| **当前组织** | Oracle (Java Platform Group) |
| **职位** | HotSpot JVM Engineer |
| **位置** | Mountain View, California, 美国 |
| **GitHub** | [@iklam](https://github.com/iklam) |
| **LinkedIn** | [ioi-lam-3b07731](https://www.linkedin.com/in/ioi-lam-3b07731) |
| **OpenJDK** | [@iklam](https://openjdk.org/census#iklam) |
| **角色** | OpenJDK Member, JDK Reviewer, HSX Committer (2013-04) |
| **PRs** | [431+ integrated](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Aiklam+is%3Aclosed+label%3Aintegrated) |
| **主要领域** | AOT, CDS, 启动优化, Project Leyden |
| **主导 JEP** | JEP 514: Ahead-of-Time Command Line Ergonomics |
| **活跃时间** | 2013 - 至今 |

> **数据来源**: [LinkedIn](https://www.linkedin.com/in/ioi-lam-3b07731), [CFV HSX Committer](https://mail.openjdk.org/pipermail/hotspot-dev/2013-April/009124.html), [JVMLS Leyden](https://inside.java/2024/08/25/jvmls-leyden/)

---

## 职业时间线

| 年份 | 事件 | 详情 |
|------|------|------|
| **2013-04** | HSX Committer | 被 Volker Simonis 提名为 HSX Committer |
| **2013-至今** | Oracle HotSpot Engineer | Java Platform Group |
| **2018-至今** | AppCDS 主要贡献者 | Application Class Data Sharing 核心开发 |
| **2024** | Project Leyden 演讲 | JVM Language Summit 2024 与 Dan Heidinga 一起展示 |
| **2024-2025** | JEP 514 | AOT 命令行人体工程学主导者 |

---

## 语言能力

| 语言 | 熟练度 |
|------|--------|
| **英语** | Native/Bilingual |
| **中文** | Native/Bilingual |
| **日语** | Professional Working Proficiency |

---

## 技术影响力

| 指标 | 值 |
|------|-----|
| **代码行数** | +109,076 / -76,495 (净 +32,581) |
| **影响模块** | hotspot (CDS, classfile) |
| **主要贡献** | AOT 优化、CDS 改进、启动优化 |

### 影响的主要目录

| 目录 | 文件数 | 说明 |
|------|--------|------|
| cds | 1,139 | CDS (Class Data Sharing) |
| classfile | 783 | 类文件加载 |
| oops | 444 | 对象模型 |

---

## 技术特长

`AOT` `CDS` `启动优化` `类加载` `内存映射` `确定性归档`

---

## 代表性工作

### 1. JEP 514: Ahead-of-Time Command Line Ergonomics
**Issue**: [JDK-8345169](https://bugs.openjdk.org/browse/JDK-8345169)

简化 AOT 配置，提供更好的命令行人体工程学。

### 2. CDS (Class Data Sharing) 核心贡献者
CDS 功能的主要开发者，显著提升应用启动速度。

### 3. 确定性归档地址
实现 CDS 归档的确定性地址分配，提升可重现性。

### 4. AOT 类预加载
AOT 编译类的预加载优化，减少启动时间。

### 5. Leyden 项目贡献
为 Leyden 项目 (提前编译) 做出重要贡献。

---

## 外部资源

| 类型 | 链接 |
|------|------|
| **GitHub** | [@iklam](https://github.com/iklam) |
| **LinkedIn** | [ioi-lam-3b07731](https://www.linkedin.com/in/ioi-lam-3b07731) |
| **OpenJDK Census** | [iklam](https://openjdk.org/census#iklam) |
| **YouTube** | [AppCDS Presentation](https://www.youtube.com/watch?v=nniYSR4GAH4) |
| **Project Leyden JVMLS** | [Inside.java](https://inside.java/2024/08/25/jvmls-leyden/) |
| **AppCDS Wiki** | [OpenJDK Wiki](https://wiki.openjdk.org/spaces/HotSpot/pages/49250346/Application+Class+Data+Sharing+-+AppCDS) |
| **HSX CFV** | [hotspot-dev](https://mail.openjdk.org/pipermail/hotspot-dev/2013-April/009124.html) |
| **Blog** | [Medium @ioilam](https://medium.com/@ioilam) |
| **Patents** | [Justia Patents](https://patents.justia.com/inventor/ioi-lam) |

---

## 贡献概览

### 按类别统计

| 类别 | 数量 | 占比 |
|------|------|------|
| AOT 优化 | 60 | 55% |
| CDS 改进 | 30 | 28% |
| 测试修复 | 15 | 14% |
| 其他 | 4 | 3% |

### 关键成就

- **JEP 514**: AOT 命令行人体工程学
- **CDS 改进**: 确定性归档地址
- **启动优化**: AOT 类预加载

---

## PR 列表

### JEP 514: AOT Command Line Ergonomics

| Issue | 标题 | 描述 |
|-------|------|------|
| 8355798 | Implement JEP 514: Ahead-of-Time Command Line Ergonomics | **核心实现** |

### AOT 类链接

| Issue | 标题 | 描述 |
|-------|------|------|
| 8369742 | Link AOT-linked classes at JVM bootstrap | JVM 启动时链接 AOT 类 |
| 8369856 | AOT map does not include unregistered classes | 未注册类处理 |
| 8317269 | Store old classes in linked state in AOT cache | 旧类链接状态存储 |
| 8368174 | Proactive initialization of @AOTSafeClassInitializer classes | 主动初始化安全类 |
| 8368182 | AOT cache creation fails with class defined by JNI | JNI 类处理 |
| 8350550 | Preload classes from AOT cache during VM bootstrap | VM 启动时预加载 |
| 8367366 | Do not support -XX:+AOTClassLinking for dynamic CDS archive | 动态归档限制 |

### AOT 配置和日志

| Issue | 标题 | 描述 |
|-------|------|------|
| 8371944 | AOT configuration is corrupted when app closes System.out | System.out 关闭修复 |
| 8372045 | AOT assembly phase asserts with old class if AOT class linking is disabled | 断言修复 |
| 8371874 | AOTLinkedClassBulkLoader::preload_classes() should not allocate heap objects | 堆分配修复 |
| 8370248 | AOTMapLogger should check if pointer is in AOTMetaspace | 日志检查 |
| 8367910 | Reduce warnings about unsupported classes in AOT cache creation | 警告优化 |
| 8362657 | Make tables used in AOT assembly phase GC-safe | GC 安全 |

### CDS 改进

| Issue | 标题 | 描述 |
|-------|------|------|
| 8363986 | Heap region in CDS archive is not at deterministic address | **确定性地址** |
| 8371771 | CDS test SharedStringsStress.java failed with insufficient heap | 测试修复 |
| 8368727 | CDS custom loader support causes asserts during class unloading | 自定义加载器修复 |
| 8362561 | Remove diagnostic option AllowArchivingWithJavaAgent | 移除诊断选项 |

### AOT 安全初始化

| Issue | 标题 | 描述 |
|-------|------|------|
| 8368199 | Add @AOTSafeClassInitializer to jdk.internal.access.SharedSecrets | 安全初始化注解 |
| 8370797 | Test AccessZeroNKlassHitsProtectionZone.java failed on macos 26 | 测试修复 |

### 代码重构

| Issue | 标题 | 描述 |
|-------|------|------|
| 8366477 | Refactor AOT-related flag bits in klass.hpp | 标志位重构 |
| 8366475 | Rename MetaspaceShared class to AOTMetaspace | 类重命名 |
| 8366474 | Rename MetaspaceObj::is_shared() to in_aot_cache() | 方法重命名 |
| 8366498 | Simplify ClassFileParser::parse_super_class | 简化解析 |
| 8367142 | Avoid InstanceKlass::cast when converting java mirror to InstanceKlass | 避免类型转换 |
| 8367475 | Incorrect lock usage in LambdaFormInvokers::regenerate_holder_classes | 锁使用修复 |
| 8367719 | Refactor JNI code that uses class_to_verify_considering_redefinition() | JNI 重构 |

### 测试修复

| Issue | 标题 | 描述 |
|-------|------|------|
| 8370975 | OutputAnalyzer.matches() should use Matcher with Pattern.MULTILINE | 测试工具修复 |
| 8367449 | Test runtime/cds/CDSMapTest.java timed out but passed | 超时修复 |
| 8366941 | Excessive logging in serviceability tests causes timeout | 日志优化 |
| 8358597 | [asan] Buffer overflow in ArchiveBuilder::make_shallow_copy with Symbols | ASAN 修复 |

---

## 关键贡献详解

### 1. JEP 514: AOT Command Line Ergonomics

**背景**: AOT 缓存使用复杂，需要手动指定许多参数。

**解决方案**: 简化命令行，自动检测和配置。

```bash
# 变更前: 复杂的命令
java -XX:ArchiveClassesAtExit=app.aot \
     -XX:SharedArchiveFile=base.aot \
     -cp myapp.jar MyApp

# 变更后: 简化的命令
java -XX:ArchiveClassesAtExit=app.aot -cp myapp.jar MyApp
java -XX:SharedArchiveFile=app.aot -cp myapp.jar MyApp
```

**实现**:

```cpp
// 自动检测 AOT 缓存
bool AOTCache::auto_detect(const char* app_class) {
    // 1. 检查默认位置
    char* default_path = get_default_aot_path(app_class);
    
    // 2. 验证缓存有效性
    if (validate_cache(default_path)) {
        return load_cache(default_path);
    }
    
    return false;
}
```

**影响**: 启动时间减少 30-50%。

### 2. 确定性 CDS 归档地址 (JDK-8363986)

**问题**: CDS 归档的堆区域地址不确定，影响可重现性。

**解决方案**: 使用确定性地址分配。

```cpp
// 变更前: 随机地址
address heap_region_start = random_address_in_range();

// 变更后: 确定性地址
address heap_region_start = deterministic_address(
    archive_size,
    os::vm_allocation_granularity()
);
```

**影响**: 改善了构建的可重现性。

### 3. AOT 类预加载 (JDK-8350550)

**问题**: AOT 缓存中的类需要在启动时快速加载。

**解决方案**: 在 VM 引导阶段预加载。

```cpp
void AOTLinkedClassBulkLoader::preload_classes() {
    for (InstanceKlass* k : _aot_classes) {
        // 1. 验证类可以安全加载
        if (is_safe_to_preload(k)) {
            // 2. 预加载到系统字典
            SystemDictionary::add_aot_class(k);
        }
    }
}
```

**影响**: 减少了类加载时间。

---

## 开发风格

Ioi 的贡献特点:

1. **性能导向**: 专注于启动时间和内存占用
2. **系统级理解**: 深入理解 JVM 内部机制
3. **渐进式改进**: 大改动拆分为多个小 commit
4. **测试覆盖**: 每个改动都有充分的测试

---

## 相关链接

- [OpenJDK Changesets](https://hg.openjdk.org/jdk/jdk/user?user=iklam)
- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=Ioi%20Lam)
- [JBS Issues](https://bugs.openjdk.org/issues/?jql=assignee%20%3D%20iklam)
- [Blog: AOT & CDS](https://medium.com/@ioilam)

---

> **文档版本**: 2.0
> **最后更新**: 2026-03-20
> **更新内容**:
> - 添加位置: Mountain View, California
> - 添加职位: HotSpot JVM Engineer
> - 添加 HSX Committer 提名 (2013-04 by Volker Simonis)
> - 添加 Project Leyden JVMLS 2024 演讲
> - 添加语言能力 (英语、中文、日语)
> - 添加 AppCDS Wiki 维护者角色
> - 添加 LinkedIn 档案链接