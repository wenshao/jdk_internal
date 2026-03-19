# JDK 26 发布说明

> 基于 openjdk/jdk 仓库标签 `jdk-26+26` 分析

## 概述

JDK 26 包含 **23 个 JEP**（JDK Enhancement Proposals），涵盖语言特性、API、性能优化、垃圾回收等多个领域。

---

## 语言特性

### JEP 511: Module Import Declarations

**状态**: 新增  
**Commit**: `0a697f6ff4c` - 8344708: Implement JEP 511: Module Import Declarations  
**作者**: Jan Lahoda  
**Reviewer**: mcimadamore, vromero, alanb

**概述**:
允许使用 `import module <module-name>` 导入整个模块的所有导出包，简化模块化开发。

**代码变更**:
- 32 个文件修改，358 行新增，216 行删除
- 主要涉及 `jdk.internal.module.ModuleInfo`、编译器解析器
- JShell 工具支持模块导入

**关键文件**:
- `src/jdk.compiler/share/classes/com/sun/tools/javac/parser/`
- `src/jdk.jshell/share/classes/jdk/jshell/`

---

### JEP 512: Compact Source Files and Instance Main Methods

**状态**: 新增  
**Commit**: `d29700cc800` - 8344706: Implement JEP 512: Compact Source Files and Instance Main Methods  
**作者**: Jan Lahoda  
**Co-author**: Stuart Marks  
**Reviewer**: liach, cstein, vromero, naoto

**概述**:
进一步简化 Java 入门体验，允许隐式类声明，无需显式类包装。

**代码变更**:
- 59 个文件修改，476 行新增，725 行删除
- `java.io.IO` 移动到 `java.lang.IO`
- 编译器和启动器支持隐式类

**关键文件**:
- `src/java.base/share/classes/java/lang/IO.java` (新增)
- `src/java.base/share/classes/sun/launcher/LauncherHelper.java`

---

### JEP 530: Primitive Types in Patterns, instanceof, and switch (Fourth Preview)

**状态**: 第四次预览  
**Commit**: `99135d2e05b` - 8359145: Implement JEP 530  
**作者**: Aggelos Biboudis  
**Reviewer**: jlahoda

**概述**:
允许在模式匹配中使用原始类型，增强 instanceof 和 switch 的类型匹配能力。

**代码变更**:
- 22 个文件修改，776 行新增，59 行删除
- 编译器类型系统增强
- 新增原始类型模式匹配测试

**关键文件**:
- `src/jdk.compiler/share/classes/com/sun/tools/javac/comp/`
- `test/langtools/tools/javac/patterns/`

---

### JEP 526: Lazy Constants (Second Preview)

**状态**: 第二次预览  
**Commit**: `f9464499976` - 8366178: Implement JEP 526: Lazy Constants  
**作者**: Chen Liang

**概述**:
引入延迟初始化的常量声明，支持在运行时计算常量值。

**代码变更**:
- 编译器和 JVM 支持延迟常量语义
- 文档改进

---

## 核心库

### JEP 502: Stable Values (Preview)

**状态**: 预览  
**Commit**: `fbc4691bfa1` - 8351565: Implement JEP 502: Stable Values (Preview)  
**作者**: Per Minborg  
**Co-author**: Maurizio Cimadamore  
**Reviewer**: vklang, jvernee, alanb, liach

**概述**:
引入 `StableValue` 类型，表示只会被设置一次的值，提供线程安全的一次写入语义。

**代码变更**:
- 30 个文件修改，4806 行新增，11 行删除
- 新增 `java.lang.StableValue` 类
- 新增 `jdk.internal.lang.stable.*` 内部实现

**关键文件**:
- `src/java.base/share/classes/java/lang/StableValue.java` (新增，757行)
- `src/java.base/share/classes/java/util/ImmutableCollections.java`
- `test/jdk/java/lang/StableValue/` (大量测试)

---

### JEP 506: Scoped Values

**状态**: 正式发布  
**Commit**: `4e1878ca452` - 8355022: Implement JEP 506: Scoped Values  
**作者**: Andrew Haley  
**Reviewer**: liach, alanb

**概述**:
Scoped Values 正式发布，提供线程局部变量的替代方案，支持有作用域的值共享。

**代码变更**:
- 6 个文件修改，9 行新增，18 行删除
- 移除预览标记，成为正式特性

**关键文件**:
- `src/java.base/share/classes/java/lang/ScopedValue.java`
- `src/java.base/share/classes/javax/security/auth/Subject.java`

---

### JEP 510: Key Derivation Function API

**状态**: 新增  
**Commit**: `079fccfa9a0` - 8353888: Implement JEP 510: Key Derivation Function API  
**作者**: Weijun Wang  
**Reviewer**: valeriep, mullan, liach

**概述**:
提供标准化的密钥派生函数 (KDF) API，支持 HKDF 等算法。

**代码变更**:
- 18 个文件修改，180 行新增，49 行删除
- 增强 `javax.crypto.KDF` API
- 移除预览标记

**关键文件**:
- `src/java.base/share/classes/javax/crypto/KDF.java`
- `src/java.base/share/classes/javax/crypto/spec/HKDFParameterSpec.java`

---

## 并发与多线程

### JEP 525: Structured Concurrency (Sixth Preview)

**状态**: 第六次预览  
**Commit**: `0bae56b6149` - 8367857: Implement JEP 525: Structured Concurrency (Sixth Preview)  
**作者**: Alan Bateman  
**Reviewer**: vklang

**概述**:
结构化并发继续预览，简化多线程编程模型，确保子任务的生命周期与父任务一致。

**代码变更**:
- 6 个文件修改，784 行新增，313 行删除
- `StructuredTaskScope` API 重构
- `Joiners` 工具类改进

**关键文件**:
- `src/java.base/share/classes/java/util/concurrent/StructuredTaskScope.java`
- `src/java.base/share/classes/java/util/concurrent/Joiners.java`

---

## 性能与监控

### JEP 509: JFR CPU-Time Profiling

**状态**: 新增  
**Commit**: `ace70a6d6ac` - 8358666: [REDO] Implement JEP 509: JFR CPU-Time Profiling  
**作者**: Johannes Bechberger  
**Reviewer**: mgronlun

**概述**:
JFR 支持 CPU 时间采样，提供更准确的性能分析数据。

**代码变更**:
- 41 个文件修改，2191 行新增，140 行删除
- 新增 `jfrCPUTimeThreadSampler.cpp/hpp`
- 新增 `CPUThrottleSetting` 配置

**关键文件**:
- `src/hotspot/share/jfr/periodic/sampling/jfrCPUTimeThreadSampler.cpp` (新增，780行)
- `src/jdk.jfr/share/classes/jdk/jfr/internal/settings/CPUThrottleSetting.java`

---

### JEP 514: Ahead-of-Time Command Line Ergonomics

**状态**: 新增  
**Commit**: `dede3532f72` - 8355798: Implement JEP 514: Ahead-of-Time Command Line Ergonomics  
**作者**: Ioi Lam  
**Reviewer**: erikj, kvn, asmehra

**概述**:
改进 AOT 缓存的命令行参数处理，优化启动性能。

**代码变更**:
- 25 个文件修改，1278 行新增，173 行删除
- CDS 配置增强
- 新增 `jdk.internal.misc.CDS` API

**关键文件**:
- `src/hotspot/share/cds/cdsConfig.cpp`
- `src/hotspot/share/runtime/arguments.cpp`

---

### JEP 515: Ahead-of-Time Method Profiling

**状态**: 新增  
**Commit**: `e3f85c961b4` - 8355003: Implement JEP 515: Ahead-of-Time Method Profiling  
**作者**: Igor Veresov  
**Co-author**: John R Rose, Vladimir Ivanov, Ioi Lam, Vladimir Kozlov, Aleksey Shipilev  
**Reviewer**: kvn, ihse, cjplummer, iklam

**概述**:
支持在 AOT 阶段收集方法分析数据，优化 JIT 编译决策。

**代码变更**:
- 大量文件修改，涉及 CDS、编译器、方法计数器
- 编译策略增强

**关键文件**:
- `src/hotspot/share/compiler/compilationPolicy.cpp`
- `src/hotspot/share/oops/methodCounters.cpp`

---

### JEP 518: JFR Cooperative Sampling

**状态**: 新增  
**Commit**: `bbceab07255` - 8352251: Implement JEP 518: JFR Cooperative Sampling  
**作者**: Markus Grönlund  
**Co-author**: Aleksey Shipilev, Erik Österlund, Boris Ulasevich, Patricio Chilano Mateo, Martin Doerr, Fei Yang, Amit Kumar  
**Reviewer**: eosterlund, egahlin

**概述**:
JFR 协作式采样，减少采样开销，提高准确性。

**代码变更**:
- 涉及多个 CPU 架构的实现 (aarch64, arm, ppc, riscv, s390, x86)
- 解释器和运行时修改

**关键文件**:
- `src/hotspot/cpu/*/interp_masm_*.cpp`
- `src/hotspot/cpu/*/frame_*.inline.hpp`

---

### JEP 519: Compact Object Headers

**状态**: 新增  
**Commit**: `1e57648abd5` - 8350457: Implement JEP 519: Compact Object Headers  
**作者**: Roman Kennke  
**Reviewer**: mdoerr, coleenp, zgu

**概述**:
压缩对象头，减少内存占用，提高缓存效率。

**代码变更**:
- 25 个文件修改，70 行新增，83 行删除
- 全局配置调整
- 测试用例更新

**关键文件**:
- `src/hotspot/share/runtime/globals.hpp`

---

### JEP 520: JFR Method Timing and Tracing

**状态**: 新增  
**Commit**: `07f5b762a09` - 8352738: Implement JEP 520: JFR Method Timing and Tracing  
**作者**: Erik Gahlin  
**Co-author**: Markus Grönlund  
**Reviewer**: shade, mgronlun

**概述**:
JFR 方法级计时和追踪，提供细粒度的性能分析能力。

**代码变更**:
- 大量新增文件，实现方法追踪框架
- 新增 `jfrMethodTracer.cpp/hpp`
- 新增过滤器和管理器

**关键文件**:
- `src/hotspot/share/jfr/support/methodtracer/jfrMethodTracer.cpp` (新增，411行)
- `src/hotspot/share/jfr/support/methodtracer/jfrFilter.cpp` (新增，270行)

---

## 垃圾回收

### JEP 521: Generational Shenandoah

**状态**: 新增  
**Commit**: `2e8b195a96e` - 8354078: Implement JEP 521: Generational Shenandoah  
**作者**: William Kemper  
**Reviewer**: ysr

**概述**:
Shenandoah GC 支持分代模式，提升年轻代对象的处理效率。

**代码变更**:
- 2 个文件修改，启用分代模式

**关键文件**:
- `src/hotspot/share/gc/shenandoah/mode/shenandoahGenerationalMode.hpp`

---

### JEP 522: G1 GC: Improve Throughput by Reducing Synchronization

**状态**: 新增  
**Commit**: `8d5c0056420` - 8342382: Implement JEP 522: G1 GC: Improve Throughput by Reducing Synchronization  
**作者**: Thomas Schatzl  
**Co-author**: Amit Kumar, Martin Doerr, Carlo Refice, Fei Yang  
**Reviewer**: iwalulya, rcastanedalo, aph, ayang

**概述**:
优化 G1 GC 的同步机制，提升吞吐量。

**代码变更**:
- 大量文件修改，涉及所有 CPU 架构的屏障集
- 新增 `G1CardTableClaimTable`
- 重构 `G1ConcurrentRefine`

**关键文件**:
- `src/hotspot/share/gc/g1/g1BarrierSet.cpp`
- `src/hotspot/share/gc/g1/g1CardTableClaimTable.cpp` (新增)
- `src/hotspot/cpu/*/gc/g1/g1BarrierSetAssembler_*.cpp`

---

## 网络

### JEP 517: HTTP/3 for the HTTP Client API

**状态**: 新增  
**Commit**: `e8db14f584f` - 8349910: Implement JEP 517: HTTP/3 for the HTTP Client API  
**作者**: Daniel Fuchs  
**Co-author**: Aleksei Efimov, Bradford Wetmore, Daniel Jeliński, Darragh Clarke, Jaikiran Pai, Michael McMahon, Volkan Yazici, Conor Cleary, Patrick Concannon, Rahul Yadav  
**Reviewer**: djelinski, jpai, aefimov, abarashev, michaelm

**概述**:
HTTP Client API 正式支持 HTTP/3 (QUIC) 协议。

**代码变更**:
- 大量新增文件，实现 QUIC 和 HTTP/3 支持
- 新增 `jdk.internal.net.quic.*` 包
- TLS 层支持 QUIC 加密

**关键文件**:
- `src/java.base/share/classes/jdk/internal/net/quic/` (新增)
- `src/java.base/share/classes/sun/security/ssl/Quic*.java` (新增)
- `src/java.net.http/share/classes/jdk/internal/net/http/Http3*.java` (新增)

---

## 安全

### JEP 470: PEM Encodings of Cryptographic Objects (Preview)

**状态**: 预览  
**Commit**: `bb2c80c0e99` - 8298420: Implement JEP 470: PEM Encodings of Cryptographic Objects (Preview)  
**作者**: Anthony Scarpino  
**Reviewer**: weijun, mr, mullan, jnimeh

**概述**:
支持 PEM 格式的加密对象编码/解码，便于密钥和证书的文本传输。

**代码变更**:
- 39 个文件修改，3519 行新增，402 行删除
- 新增 `PEMEncoder`、`PEMDecoder`、`PEMRecord` 类
- 增强 `EncryptedPrivateKeyInfo`

**关键文件**:
- `src/java.base/share/classes/java/security/PEMEncoder.java` (新增，382行)
- `src/java.base/share/classes/java/security/PEMDecoder.java` (新增，512行)
- `src/java.base/share/classes/java/security/PEMRecord.java` (新增，136行)

---

### JEP 524: PEM Encodings of Cryptographic Objects (Second Preview)

**状态**: 第二次预览  
**Commit**: `ad3dfaf1fc4` - 8360564: Implement JEP 524: PEM Encodings (Second Preview)

**概述**:
JEP 470 的第二次预览，根据反馈进行改进。

---

## 移除与清理

### JEP 500: Prepare to Make Final Mean Final

**状态**: 新增  
**Commit**: `26460b6f12c` - 8353835: Implement JEP 500: Prepare to Make Final Mean Final  
**作者**: Alan Bateman  
**Reviewer**: liach, vlivanov, dholmes, vyazici

**概述**:
为最终字段提供更强的不可变性保证，限制通过反射和 JNI 修改 final 字段。

**代码变更**:
- 大量文件修改，涉及反射、模块系统、JFR 事件
- 新增 `FinalFieldMutationEvent`
- 新增命令行选项控制行为

**关键文件**:
- `src/java.base/share/classes/java/lang/reflect/Field.java`
- `src/java.base/share/classes/java/lang/Module.java`
- `test/jdk/java/lang/reflect/Field/mutateFinals/` (新增测试)

---

### JEP 503: Remove the 32-bit x86 Port

**状态**: 移除  
**Commit**: `ee710fec21c` - 8345169: Implement JEP 503: Remove the 32-bit x86 Port  
**作者**: Aleksey Shipilev  
**Reviewer**: ihse, mdoerr, vlivanov, kvn, coleenp, dholmes

**概述**:
正式移除 32位 x86 平台支持，简化代码维护。

**代码变更**:
- 25 个文件删除，29729 行代码移除
- 删除所有 `*_x86_32.*` 文件
- 更新构建配置

**删除的关键文件**:
- `src/hotspot/cpu/x86/x86_32.ad` (13702行)
- `src/hotspot/cpu/x86/stubGenerator_x86_32.cpp` (4314行)
- `src/hotspot/os_cpu/linux_x86/linux_x86_32.S`

---

### JEP 504: Remove the Applet API

**状态**: 移除  
**Commit**: `5cf672e7784` - 8359053: Implement JEP 504 - Remove the Applet API  
**作者**: Phil Race  
**Reviewer**: aivanov, kizune, kcr, achung, serb

**概述**:
正式移除已废弃的 Applet API，包括 `java.applet` 包和相关 Swing 组件。

**代码变更**:
- 大量文件修改，移除 Applet 相关代码
- 删除 `java.applet` 包
- 删除 `JApplet` 类

**删除的关键文件**:
- `src/java.base/share/classes/java/applet/Applet.java` (609行)
- `src/java.desktop/share/classes/javax/swing/JApplet.java` (580行)
- `src/java.base/share/classes/java/applet/AppletContext.java` (200行)

---

## 相关链接

- [OpenJDK JDK 26 项目页面](https://openjdk.org/projects/jdk/26/)
- [JDK 26 JEP 列表](https://openjdk.org/projects/jdk/26/spec/)
- [GitHub: openjdk/jdk](https://github.com/openjdk/jdk)