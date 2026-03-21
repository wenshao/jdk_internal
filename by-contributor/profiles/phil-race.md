# Phil Race

> **GitHub**: [@prrace](https://github.com/prrace)
> **Organization**: Oracle
> **Position**: Consulting Member of Technical Staff, Client Libraries Lead
> **OpenJDK Governing Board Member**

---
## 目录

1. [概述](#1-概述)
2. [Basic Information](#2-basic-information)
3. [职业时间线](#3-职业时间线)
4. [Contribution Overview](#4-contribution-overview)
5. [Complete PR List](#5-complete-pr-list)
6. [Key Contributions](#6-key-contributions)
7. [Development Style](#7-development-style)
8. [Related Links](#8-related-links)
9. [外部资源](#9-外部资源)

---


## 1. 概述

Phil Race 是 Oracle 的 Consulting Member of Technical Staff，OpenJDK Client Libraries 团队负责人，负责核心 Swing、Java 2D 和 AWT API。他是 OpenJDK Governing Board 成员（Oracle 代表），在 Java 2D 图形、打印、Swing GUI 组件和桌面应用开发方面做出重要贡献。他在 2D 计算机图形行业有丰富经验，并在 FOSDEM 2024 和 JavaOne 2026 等会议上担任演讲者和程序委员会成员。截至 2026 年 3 月，他已有 **303 个 Integrated PRs**，主导了 AppContext 移除和 finalize() 方法清理等重大重构工作。

---

## 2. Basic Information

| Field | Value |
|-------|-------|
| **Name** | Phil Race |
| **Current Organization** | Oracle |
| **Position** | Consulting Member of Technical Staff, Client Libraries Lead |
| **GitHub** | [@prrace](https://github.com/prrace) |
| **OpenJDK** | [@prr](https://openjdk.org/census#prr) |
| **角色** | OpenJDK Member, JDK Reviewer, JDK Updates Reviewer, Brisbane Reviewer, Client Libraries Group Lead, Build Group Member, CSR Group Member, OpenJDK Governing Board Member |
| **PRs** | [303 integrated](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Aprrace+is%3Aclosed+label%3Aintegrated) |
| **主要领域** | Graphics, Printing, AWT, Swing, Desktop, AppContext Removal |

> **数据来源**: [FOSDEM 2024](https://archive.fosdem.org/2024/schedule/speaker/BD3NMJ/), [OpenJDK Governing Board](https://openjdk.org/poll/gb/2024/), [GitHub](https://github.com/prrace), [Client Libraries Group CFV](https://mail.openjdk.org/pipermail/gb-discuss/2021-June/000358.html)

## 3. 职业时间线

| 时间 | 事件 | 详情 |
|------|------|------|
| **1990s** | Sun Microsystems | 开始从事 Java 2D 图形开发 |
| **2010** | Oracle 收购 Sun | 随 Sun Microsystems 并入 Oracle |
| **2015** | Marlin Renderer | 与 Jim Graham 合作集成 Marlin 渲染器 |
| **2021-07** | Client Libraries Group Lead | OpenJDK 管理委员会全票通过，成立 Client Libraries Group |
| **2021-09** | swing-dev 邮件列表退役 | 原 AWT/2D/Swing/Sound 组合并 |
| **2023-2025** | OpenJDK GB 成员 | Oracle 代表，多次当选 |

### 最近 10 个 Integrated PRs (2026 年 2-3 月)

| PR # | Issue | 标题 | 日期 |
|------|-------|------|------|
| #30226 | 8379937 | NullActiveWindowOnFocusLost.java fails intermittently | Mar 12, 2026 |
| #30060 | 8379229 | Remove AppContext from javax.swing.JComponent | Mar 9, 2026 |
| #30028 | 8379137 | Remove AppContext from javax.swing.JOptionPane | Mar 9, 2026 |
| #29990 | 8378920 | Remove AppContext from SequencedEvent | Mar 11, 2026 |
| #30008 | 8378999 | BeanContextSupport.add(Object) synchronizes on its argument | Mar 6, 2026 |
| #29987 | 8378917 | InputEvent checks for SystemClipboard access are unused | Mar 5, 2026 |
| #29985 | 8378899 | Remove AppContext from java.awt.Toolkit implementation | Mar 10, 2026 |
| #29969 | 8378865 | After fix for JDK-8378385 two tests are failing on windows | Feb 27, 2026 |
| #29904 | 8378607 | GlyphLayout cache can prevent Fonts from being GC'd | Feb 28, 2026 |
| #29901 | 8376152 | Test javax/sound/sampled/Clip/bug5070081.java timed out | Feb 25, 2026 |

> **观察**: 最近工作集中在 **AppContext 移除** 和 **Client 库测试修复**

## 4. Contribution Overview

### By Category

| Category | Count | Description |
|----------|-------|-------------|
| finalize() Removal | 20 | Removing deprecated finalize methods |
| Applet API Removal | 8 | JEP 504 implementation |
| Graphics/2D | 12 | Java 2D improvements |
| Printing | 10 | PrintJob and PrinterJob fixes |
| Swing | 10 | UI component improvements |
| Testing | 9 | Test fixes and open-sourcing |

### Key Areas of Expertise
- **Java 2D API** - Graphics rendering and imaging
- **Printing** - Java Print Service API
- **AWT** - Abstract Window Toolkit
- **Swing** - GUI components
- **Desktop APIs** - java.desktop module

## 5. Complete PR List

| Issue | Title | PR Link |
|-------|-------|---------|
| JDK-8369129 | Raster createPackedRaster methods specification clean up | [Link]([需要补充 PR 链接]) |
| JDK-8368576 | PrintJob.getGraphics() does not specify behavior after PrintJob.end() | [Link]([需要补充 PR 链接]) |
| JDK-8370637 | [Windows] Crash if use Graphics after PrintJob.end | [Link]([需要补充 PR 链接]) |
| JDK-8371304 | mismatch in file name and class name for ByteInterleavedRasterOffsetsTest.java | [Link]([需要补充 PR 链接]) |
| JDK-4954405 | Data buffers created with an offset are unusable | [Link]([需要补充 PR 链接]) |
| JDK-8370719 | [Linux] Use /etc/os-release values for font configuration file names | [Link]([需要补充 PR 链接]) |
| JDK-8357252 | sun/awt/font/TestArabicHebrew.java fails in OEL 9 and 10 x64 | [Link]([需要补充 PR 链接]) |
| JDK-8364583 | ColorConvertOp fails for CMYK to RGB conversion | [Link]([需要补充 PR 链接]) |
| JDK-8370141 | [macOS] Crash after PrinterJob ends when Graphics.create() is used | [Link]([需要补充 PR 链接]) |
| JDK-8370160 | NumericShaper allows illegal ranges | [Link]([需要补充 PR 链接]) |
| JDK-6453640 | BandedSampleModel.createCompatibleSampleModel() API docs are wrong | [Link]([需要补充 PR 链接]) |
| JDK-8365077 | java.awt.font.NumericShaper violates equals/hashCode contract | [Link]([需要补充 PR 链接]) |
| JDK-8369146 | java/awt/PrintJob/GetGraphicsTest.java Parse Exception | [Link]([需要补充 PR 链接]) |
| JDK-8364673 | Remove duplicate font mapping for itcavantgarde in psfontj2d.properties | [Link]([需要补充 PR 链接]) |
| JDK-8344918 | Unused private variables in SwingUtilities.java | [Link]([需要补充 PR 链接]) |
| JDK-8369335 | Two sun/java2d/OpenGL tests fail on Windows after JDK-8358058 | [Link]([需要补充 PR 链接]) |
| JDK-8369516 | Delete duplicate imaging test | [Link]([需要补充 PR 链接]) |
| JDK-8366002 | Beans.instantiate needs to describe the lookup procedure | [Link]([需要补充 PR 链接]) |
| JDK-8358058 | sun/java2d/OpenGL/DrawImageBg.java Test fails intermittently | [Link]([需要补充 PR 链接]) |
| JDK-8367702 | PrintJob.getGraphics() should return null after PrintJob.end | [Link]([需要补充 PR 链接]) |
| JDK-8221451 | PIT: sun/java2d/X11SurfaceData/SharedMemoryPixmapsTest fails | [Link]([需要补充 PR 链接]) |
| JDK-7184899 | Test sun/java2d/X11SurfaceData/SharedMemoryPixmapsTest fail | [Link]([需要补充 PR 链接]) |
| JDK-8361530 | Test javax/swing/GraphicsConfigNotifier/StalePreferredSize.java timed out | [Link]([需要补充 PR 链接]) |
| JDK-8365569 | Remove finalize from JavaSoundAudioClip.java | [Link]([需要补充 PR 链接]) |
| JDK-8365197 | javax.imageio.stream MemoryCache based streams no longer need a disposer | [Link]([需要补充 PR 链接]) |
| JDK-8344333 | Spurious System.err.flush() in LWCToolkit.java | [Link]([需要补充 PR 链接]) |
| JDK-8365291 | Remove finalize() method from sun/awt/X11InputMethodBase.java | [Link]([需要补充 PR 链接]) |
| JDK-8365292 | Remove javax.imageio.spi.ServiceRegistry.finalize() | [Link]([需要补充 PR 链接]) |
| JDK-8359391 | Remove ThreadGroup sandboxing from javax.imageio | [Link]([需要补充 PR 链接]) |
| JDK-8364768 | JDK javax.imageio ImageWriters do not all flush the output stream | [Link]([需要补充 PR 链接]) |
| JDK-8365180 | Remove sun.awt.windows.WInputMethod.finalize() | [Link]([需要补充 PR 链接]) |
| JDK-8365389 | Remove static color fields from SwingUtilities3 and WindowsMenuItemUI | [Link]([需要补充 PR 链接]) |
| JDK-8277585 | Remove the terminally deprecated finalize() method from javax.imageio.stream APIs | [Link]([需要补充 PR 链接]) |
| JDK-8365198 | Remove unnecessary mention of finalize in ImageIO reader/writer docs | [Link]([需要补充 PR 链接]) |
| JDK-8365416 | java.desktop no longer needs preview feature access | [Link]([需要补充 PR 链接]) |
| JDK-8364230 | javax/swing/text/StringContent can be migrated away from using finalize | [Link]([需要补充 PR 链接]) |
| JDK-8362898 | Remove finalize() methods from javax.imageio TIFF classes | [Link]([需要补充 PR 链接]) |
| JDK-8210765 | Remove finalize method in CStrike.java | [Link]([需要补充 PR 链接]) |
| JDK-8363889 | Update sun.print.PrintJob2D to use Disposer | [Link]([需要补充 PR 链接]) |
| JDK-8362289 | [macOS] Remove finalize method in JRSUIControls.java | [Link]([需要补充 PR 链接]) |
| JDK-8362452 | [macOS] Remove CPrinterJob.finalize() | [Link]([需要补充 PR 链接]) |
| JDK-8362557 | [macOS] Remove CFont.finalize() | [Link]([需要补充 PR 链接]) |
| JDK-8362291 | [macOS] Remove finalize method in CGraphicsEnvironment.java | [Link]([需要补充 PR 链接]) |
| JDK-8362659 | Remove sun.print.PrintJob2D.finalize() | [Link]([需要补充 PR 链接]) |
| JDK-8360147 | Better Glyph drawing redux | [Link]([需要补充 PR 链接]) |
| JDK-8355884 | [macos] java/awt/Frame/I18NTitle.java fails on MacOS | [Link]([需要补充 PR 链接]) |
| JDK-8348989 | Better Glyph drawing | [Link]([需要补充 PR 链接]) |
| JDK-8359053 | Implement JEP 504 - Remove the Applet API | [Link]([需要补充 PR 链接]) |
| JDK-8358526 | Clarify behavior of java.awt.HeadlessException constructed with no-args | [Link]([需要补充 PR 链接]) |
| JDK-8358731 | Remove jdk.internal.access.JavaAWTAccess.java | [Link]([需要补充 PR 链接]) |
| JDK-8357672 | Extreme font sizes can cause font substitution | [Link]([需要补充 PR 链接]) |
| JDK-8356049 | Need a simple way to play back a sound clip | [Link]([需要补充 PR 链接]) |
| JDK-8357176 | java.awt javadoc code examples still use Applet API | [Link]([需要补充 PR 链接]) |
| JDK-8346683 | Problem list automated tests that fail on macOS15 | [Link]([需要补充 PR 链接]) |
| JDK-8356208 | Remove obsolete code in PSPrinterJob for plugin printing | [Link]([需要补充 PR 链接]) |
| JDK-8355333 | Some Problem list entries point to non-existent / wrong files | [Link]([需要补充 PR 链接]) |
| JDK-8355002 | Clean up some mentions of "applet" in tests | [Link]([需要补充 PR 链接]) |
| JDK-8354552 | Open source a few Swing tests | [Link]([需要补充 PR 链接]) |
| JDK-8354451 | Open source some more Swing popup menu tests | [Link]([需要补充 PR 链接]) |
| JDK-8353589 | Open source a few Swing menu-related tests | [Link]([需要补充 PR 链接]) |
| JDK-8353483 | Open source some JProgressBar tests | [Link]([需要补充 PR 链接]) |
| JDK-8353304 | Open source two JTabbedPane tests | [Link]([需要补充 PR 链接]) |
| JDK-8353475 | Open source two Swing DefaultCaret tests | [Link]([需要补充 PR 链接]) |
| JDK-8352997 | Open source several Swing JTabbedPane tests | [Link]([需要补充 PR 链接]) |
| JDK-8353320 | Open source more Swing text tests | [Link]([需要补充 PR 链接]) |
| JDK-8353309 | Open source several Swing text tests | [Link]([需要补充 PR 链接]) |
| JDK-8353324 | Clean up of comments and import after 8319192 | [Link]([需要补充 PR 链接]) |
| JDK-8347321 | [ubsan] CGGlyphImages.m runtime error | [Link]([需要补充 PR 链接]) |
| JDK-8319192 | Remove javax.swing.plaf.synth.SynthLookAndFeel.load(URL url) | [Link]([需要补充 PR 链接]) |
| JDK-8344146 | Remove temporary font file tracking code | [Link]([需要补充 PR 链接]) |
| JDK-8346829 | Problem list com/sun/jdi/ReattachStressTest.java & ProcessAttachTest.java on Linux | [Link]([需要补充 PR 链接]) |

## 6. Key Contributions

### 1. JEP 504 - Remove the Applet API

**JDK-8359053: Implement JEP 504 - Remove the Applet API**

This major contribution removes the deprecated Applet API from the JDK:

```java
// Removed classes:
// - java.applet.Applet
// - java.applet.AppletContext
// - java.applet.AppletStub
// - java.applet.AudioClip
// - java.beans.AppletInitializer

// Migration path for audio playback
// Before:
Applet.newAudioClip(url).play();

// After (JDK-8356049):
AudioSystem.getAudioClip(url).play();
```

### 2. finalize() Method Removal

**JDK-8277585: Remove the terminally deprecated finalize() method from javax.imageio.stream APIs**

Systematically removed deprecated finalize() methods across java.desktop:

```java
// Before:
public class MemoryCacheImageOutputStream extends ImageOutputStreamImpl {
    @Override
    protected void finalize() throws Throwable {
        try {
            close();
        } finally {
            super.finalize();
        }
    }
}

// After: Use Disposer pattern
public class MemoryCacheImageOutputStream extends ImageOutputStreamImpl {
    private final DisposerRecord disposerRecord = new DisposerRecord() {
        public void dispose() {
            try {
                close();
            } catch (IOException e) {
                // Ignore
            }
        }
    };
}
```

### 3. PrintJob Graphics Handling

**JDK-8367702: PrintJob.getGraphics() should return null after PrintJob.end()**

Fixed PrintJob behavior to be more predictable:

```java
public class PrintJob {
    private boolean ended = false;
    
    public Graphics getGraphics() {
        if (ended) {
            return null;  // Return null after end() is called
        }
        return peer.getGraphics();
    }
    
    public void end() {
        ended = true;
        peer.end();
    }
}
```

### 4. Data Buffer Offset Fix

**JDK-4954405: Data buffers created with an offset are unusable**

Fixed a long-standing issue with data buffer offsets:

```java
// Before: Offset was incorrectly applied
public DataBufferInt(int size, int offset) {
    super(size, offset);
    data = new int[size + offset];  // Wrong: offset applied to array size
}

// After: Correct offset handling
public DataBufferInt(int size, int offset) {
    super(size, offset);
    data = new int[size];  // Correct: size is the usable size
    // offset is used for getElem/setElem operations
}
```

### 5. Color Conversion Fix

**JDK-8364583: ColorConvertOp fails for CMYK to RGB conversion**

Fixed color space conversion for CMYK images:

```java
// Fixed handling of CMYK color space
public BufferedImage filter(BufferedImage src, BufferedImage dest) {
    ColorSpace srcCS = src.getColorModel().getColorSpace();
    if (srcCS.getType() == ColorSpace.TYPE_CMYK) {
        // Properly handle CMYK to RGB conversion
        return convertCMYKtoRGB(src, dest);
    }
    // ... standard conversion
}
```

## 7. Development Style

### Code Characteristics
- **API modernization**: Focus on removing deprecated APIs
- **Cross-platform**: Ensures graphics work on Windows, macOS, Linux
- **Documentation**: Improves API documentation and examples
- **Test coverage**: Opens and improves internal tests

### Typical Commit Pattern
1. Identify deprecated or problematic API
2. Research impact and migration paths
3. Implement removal or fix
4. Update documentation and examples
5. Add/update tests

### Review Style
- Often reviewed by Alexey Ivanov (aivanov), Sergey Bylokhov (serb)
- Focuses on backward compatibility
- Ensures proper documentation

## 8. Related Links

- **GitHub**: [prrace](https://github.com/prrace)
- **OpenJDK Census**: [prr](https://openjdk.org/census#prr)
- **JBS Issues**: [bugs.openjdk.org](https://bugs.openjdk.org/issues/?jql=reporter%20%3D%20prr)
- **GitHub Commits**: [github.com/openjdk/jdk](https://github.com/openjdk/jdk/commits?author=prr)
- **JEP 504**: [Remove the Applet API](https://openjdk.org/jeps/504)

---

## 9. 外部资源

### 演讲与会议

| 会议 | 年份 | 主题 | 链接 |
|------|------|------|------|
| FOSDEM | 2024 | Client Libraries Lead 演讲 | [FOSDEM](https://archive.fosdem.org/2024/schedule/speaker/BD3NMJ/) |
| JavaOne | 2026 | Program Committee Member | [Inside.java](https://inside.java/) |

### OpenJDK 治理

- **OpenJDK Governing Board Member** (At-Large for Oracle)
- **多次当选**: 2023, 2024, 2025
- **Area Lead**: Client Libraries (Swing, Java 2D, AWT, Sound)
- **Project Lead**: Lanai (macOS Metal rendering pipeline)

---

> **文档版本**: 2.0
> **最后更新**: 2026-03-20
> **更新内容**: 补充职位（Client Libraries Lead、CMTS）、OpenJDK Governing Board 成员、FOSDEM 演讲、2D 图形行业背景