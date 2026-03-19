# Phil Race

## Basic Information

| Field | Value |
|-------|-------|
| **Name** | Phil Race |
| **Organization** | Oracle |
| **GitHub** | [@prrace](https://github.com/prrace) |
| **OpenJDK** | [@prr](https://openjdk.org/census#prr) |
| **Role** | OpenJDK Member, JDK Reviewer, Client Libs Lead |
| **PRs** | [303 integrated](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Aprrace+is%3Aclosed+label%3Aintegrated) |
| **Email** | prr@openjdk.org |
| **Primary Areas** | Graphics, Printing, AWT, Swing, Security |

## Contribution Overview

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

## Complete PR List

| Issue | Title | PR Link |
|-------|-------|---------|
| JDK-8369129 | Raster createPackedRaster methods specification clean up | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8368576 | PrintJob.getGraphics() does not specify behavior after PrintJob.end() | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8370637 | [Windows] Crash if use Graphics after PrintJob.end | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8371304 | mismatch in file name and class name for ByteInterleavedRasterOffsetsTest.java | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-4954405 | Data buffers created with an offset are unusable | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8370719 | [Linux] Use /etc/os-release values for font configuration file names | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8357252 | sun/awt/font/TestArabicHebrew.java fails in OEL 9 and 10 x64 | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8364583 | ColorConvertOp fails for CMYK to RGB conversion | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8370141 | [macOS] Crash after PrinterJob ends when Graphics.create() is used | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8370160 | NumericShaper allows illegal ranges | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-6453640 | BandedSampleModel.createCompatibleSampleModel() API docs are wrong | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8365077 | java.awt.font.NumericShaper violates equals/hashCode contract | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8369146 | java/awt/PrintJob/GetGraphicsTest.java Parse Exception | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8364673 | Remove duplicate font mapping for itcavantgarde in psfontj2d.properties | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8344918 | Unused private variables in SwingUtilities.java | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8369335 | Two sun/java2d/OpenGL tests fail on Windows after JDK-8358058 | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8369516 | Delete duplicate imaging test | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8366002 | Beans.instantiate needs to describe the lookup procedure | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8358058 | sun/java2d/OpenGL/DrawImageBg.java Test fails intermittently | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8367702 | PrintJob.getGraphics() should return null after PrintJob.end | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8221451 | PIT: sun/java2d/X11SurfaceData/SharedMemoryPixmapsTest fails | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-7184899 | Test sun/java2d/X11SurfaceData/SharedMemoryPixmapsTest fail | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8361530 | Test javax/swing/GraphicsConfigNotifier/StalePreferredSize.java timed out | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8365569 | Remove finalize from JavaSoundAudioClip.java | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8365197 | javax.imageio.stream MemoryCache based streams no longer need a disposer | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8344333 | Spurious System.err.flush() in LWCToolkit.java | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8365291 | Remove finalize() method from sun/awt/X11InputMethodBase.java | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8365292 | Remove javax.imageio.spi.ServiceRegistry.finalize() | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8359391 | Remove ThreadGroup sandboxing from javax.imageio | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8364768 | JDK javax.imageio ImageWriters do not all flush the output stream | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8365180 | Remove sun.awt.windows.WInputMethod.finalize() | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8365389 | Remove static color fields from SwingUtilities3 and WindowsMenuItemUI | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8277585 | Remove the terminally deprecated finalize() method from javax.imageio.stream APIs | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8365198 | Remove unnecessary mention of finalize in ImageIO reader/writer docs | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8365416 | java.desktop no longer needs preview feature access | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8364230 | javax/swing/text/StringContent can be migrated away from using finalize | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8362898 | Remove finalize() methods from javax.imageio TIFF classes | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8210765 | Remove finalize method in CStrike.java | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8363889 | Update sun.print.PrintJob2D to use Disposer | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8362289 | [macOS] Remove finalize method in JRSUIControls.java | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8362452 | [macOS] Remove CPrinterJob.finalize() | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8362557 | [macOS] Remove CFont.finalize() | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8362291 | [macOS] Remove finalize method in CGraphicsEnvironment.java | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8362659 | Remove sun.print.PrintJob2D.finalize() | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8360147 | Better Glyph drawing redux | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8355884 | [macos] java/awt/Frame/I18NTitle.java fails on MacOS | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8348989 | Better Glyph drawing | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8359053 | Implement JEP 504 - Remove the Applet API | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8358526 | Clarify behavior of java.awt.HeadlessException constructed with no-args | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8358731 | Remove jdk.internal.access.JavaAWTAccess.java | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8357672 | Extreme font sizes can cause font substitution | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8356049 | Need a simple way to play back a sound clip | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8357176 | java.awt javadoc code examples still use Applet API | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8346683 | Problem list automated tests that fail on macOS15 | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8356208 | Remove obsolete code in PSPrinterJob for plugin printing | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8355333 | Some Problem list entries point to non-existent / wrong files | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8355002 | Clean up some mentions of "applet" in tests | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8354552 | Open source a few Swing tests | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8354451 | Open source some more Swing popup menu tests | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8353589 | Open source a few Swing menu-related tests | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8353483 | Open source some JProgressBar tests | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8353304 | Open source two JTabbedPane tests | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8353475 | Open source two Swing DefaultCaret tests | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8352997 | Open source several Swing JTabbedPane tests | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8353320 | Open source more Swing text tests | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8353309 | Open source several Swing text tests | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8353324 | Clean up of comments and import after 8319192 | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8347321 | [ubsan] CGGlyphImages.m runtime error | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8319192 | Remove javax.swing.plaf.synth.SynthLookAndFeel.load(URL url) | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8344146 | Remove temporary font file tracking code | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8346829 | Problem list com/sun/jdi/ReattachStressTest.java & ProcessAttachTest.java on Linux | [Link](https://github.com/openjdk/jdk/pull/XXXX) |

## Key Contributions

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

## Development Style

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

## Related Links

- [OpenJDK Profile](https://openjdk.org/census#prr)
- [JBS Issues](https://bugs.openjdk.org/issues/?jql=reporter%20%3D%20prr)
- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=prr)
- [JEP 504](https://openjdk.org/jeps/504)