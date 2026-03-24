## 目录

1. [Basic Information](#1-basic-information)
2. [Contribution Overview](#2-contribution-overview)
3. [Complete PR List](#3-complete-pr-list)
4. [Key Contributions](#4-key-contributions)
5. [Development Style](#5-development-style)
6. [Related Links](#6-related-links)

---

# Prasanta Sadhukhan

## 1. Basic Information

| Attribute | Value |
|-----------|-------|
| **Name** | Prasanta Sadhukhan |
| **Current Organization** | Oracle |
| **Location** | India |
| **GitHub** | [@prsadhuk](https://github.com/prsadhuk) |
| **Organizations** | @oracle |
| **LinkedIn** | [Prasanta Sadhukhan](https://in.linkedin.com/in/prasantasadhukhan) |
| **Connections** | 84+ |
| **Email** | psadhukhan@openjdk.org |
| **OpenJDK** | [@psadhukhan](https://openjdk.org/census#psadhukhan) |
| **角色** | OpenJDK Member, JDK Reviewer, OpenJFX Committer (2017-09), Client Libraries Group Member (2021-09) |
| **主要领域** | Swing, AWT, JavaFX, Client Libraries, Focus Management |
| **活跃时间** | 2015+ |

> **数据来源**: [GitHub](https://github.com/prsadhuk), [LinkedIn](https://in.linkedin.com/in/prasantasadhukhan), [OpenJDK](https://openjdk.org/census#psadhukhan), [CFV OpenJFX Committer](https://mail.openjdk.org/pipermail/openjfx-dev/2017-September/020857.html), [CFV Client Libraries Group Member](https://mail.openjdk.org/pipermail/client-libs-dev/2021-September/000502.html)

## 2. Contribution Overview

### By Category

| Category | Count | Description |
|----------|-------|-------------|
| Swing Fixes | 28 | JComponent, JMenu, JMenuItem, JSplitPane, JTable fixes |
| AWT Fixes | 12 | Focus management, Graphics, Dialog handling |
| Test Improvements | 15 | Test open-sourcing, test fixes, problem listing |
| Documentation | 5 | Javadoc corrections, API clarifications |
| Platform-Specific | 10 | macOS, Windows, Linux specific fixes |

### Key Areas of Expertise

- **Swing Look and Feel**: Metal, Nimbus, GTK, Windows L&F
- **Focus Management**: Initial focus, keyboard navigation, focus traversal
- **Text Components**: GlyphView, StyledEditorKit, Caret handling
- **Graphics**: BufferedImage, copyArea, rendering
- **Cross-Platform Testing**: macOS, Windows, Linux compatibility

## 3. Complete PR List

| Issue | Title | PR Link |
|-------|-------|---------|
| 8372103 | Metal JButton doesn't show focus if no text or icon | [JBS](https://bugs.openjdk.org/browse/JDK-8372103) |
| 8370467 | BorderFactory.createBevelBorder and createSoftBevelBorder throws NPE for null highlight and shadow | [JBS](https://bugs.openjdk.org/browse/JDK-8370467) |
| 8299304 | Test "java/awt/print/PrinterJob/PageDialogTest.java" fails on macOS 13 x64 | [JBS](https://bugs.openjdk.org/browse/JDK-8299304) |
| 8371163 | Make GlyphView/TestGlyphBGHeight.java headless | [JBS](https://bugs.openjdk.org/browse/JDK-8371163) |
| 8370465 | Right to Left Orientation Issues with MenuItem Component | [JBS](https://bugs.openjdk.org/browse/JDK-8370465) |
| 8017266 | Background is painted taller than needed for styled text | [JBS](https://bugs.openjdk.org/browse/JDK-8017266) |
| 8370560 | Remove non-public API reference from public API javadoc | [JBS](https://bugs.openjdk.org/browse/JDK-8370560) |
| 8068293 | Test closed/com/sun/java/swing/plaf/motif/InternalFrame/4150591/bug4150591.java fails with GTKLookAndFeel | [JBS](https://bugs.openjdk.org/browse/JDK-8068293) |
| 8026776 | Broken API names in API doc | [JBS](https://bugs.openjdk.org/browse/JDK-8026776) |
| 8068310 | Test javax/swing/JColorChooser/Test4234761.java fails with GTKL&F | [JBS](https://bugs.openjdk.org/browse/JDK-8068310) |
| 8342401 | [TESTBUG] javax/swing/JSpinner/8223788/JSpinnerButtonFocusTest.java test fails in ubuntu 22.04 | [JBS](https://bugs.openjdk.org/browse/JDK-8342401) |
| 8369251 | Opensource few tests | [JBS](https://bugs.openjdk.org/browse/JDK-8369251) |
| 8365886 | JSplitPane loses track of the left component when the component orientation is changed | [JBS](https://bugs.openjdk.org/browse/JDK-8365886) |
| 8335646 | Nimbus : JLabel not painted with LAF defined foreground color on Ubuntu 24.04 | [JBS](https://bugs.openjdk.org/browse/JDK-8335646) |
| 8368185 | Test javax/swing/plaf/synth/SynthButtonUI/6276188/bug6276188.java failed | [JBS](https://bugs.openjdk.org/browse/JDK-8368185) |
| 8368181 | ProblemList java/awt/Dialog/ModalExcludedTest/ModalExcludedTest.java | [JBS](https://bugs.openjdk.org/browse/JDK-8368181) |
| 8367784 | java/awt/Focus/InitialFocusTest/InitialFocusTest1.java failed with Wrong focus owner | [JBS](https://bugs.openjdk.org/browse/JDK-8367784) |
| 8015444 | java/awt/Focus/KeyStrokeTest.java sometimes fails | [JBS](https://bugs.openjdk.org/browse/JDK-8015444) |
| 8023263 | [TESTBUG] Test closed/java/awt/Focus/InactiveWindowTest/InactiveFocusRace fails | [JBS](https://bugs.openjdk.org/browse/JDK-8023263) |
| 8256289 | java/awt/Focus/AppletInitialFocusTest/AppletInitialFocusTest1.java failed | [JBS](https://bugs.openjdk.org/browse/JDK-8256289) |
| 8144124 | [macosx] The tabs can't be aligned when we pressing the key of 'R','B','L','C' or 'T' | [JBS](https://bugs.openjdk.org/browse/JDK-8144124) |
| 8162380 | [TEST_BUG] MouseEvent/.../AltGraphModifierTest.java has only "Fail" button | [JBS](https://bugs.openjdk.org/browse/JDK-8162380) |
| 8159055 | Clarify handling of null and invalid image data for ImageIcon constructors and setImage method | [JBS](https://bugs.openjdk.org/browse/JDK-8159055) |
| 8361610 | Avoid wasted work in ImageIcon(Image) for setting description | [JBS](https://bugs.openjdk.org/browse/JDK-8361610) |
| 8365425 | [macos26] javax/swing/JInternalFrame/8160248/JInternalFrameDraggingTest.java fails on macOS 26 | [JBS](https://bugs.openjdk.org/browse/JDK-8365425) |
| 8365375 | Method SU3.setAcceleratorSelectionForeground assigns to acceleratorForeground | [JBS](https://bugs.openjdk.org/browse/JDK-8365375) |
| 8348760 | RadioButton is not shown if JRadioButtonMenuItem is rendered with ImageIcon in WindowsLookAndFeel | [JBS](https://bugs.openjdk.org/browse/JDK-8348760) |
| 4938801 | The popup does not go when the component is removed | [JBS](https://bugs.openjdk.org/browse/JDK-4938801) |
| 8349111 | Enhance Swing supports | [JBS](https://bugs.openjdk.org/browse/JDK-8349111) |
| 6955128 | Spec for javax.swing.plaf.basic.BasicTextUI.getVisibleEditorRect contains inappropriate wording | [JBS](https://bugs.openjdk.org/browse/JDK-6955128) |
| 8346753 | Test javax/swing/JMenuItem/RightLeftOrientation/RightLeftOrientation.java fails on Windows Server 2025 | [JBS](https://bugs.openjdk.org/browse/JDK-8346753) |
| 8360462 | [macosx] row selection not working with Ctrl+Shift+Down/Up in AquaL&F | [JBS](https://bugs.openjdk.org/browse/JDK-8360462) |
| 8335986 | Test javax/swing/JCheckBox/4449413/bug4449413.java fails on Windows 11 x64 | [JBS](https://bugs.openjdk.org/browse/JDK-8335986) |
| 8359428 | Test 'javax/swing/JTabbedPane/bug4499556.java' failed | [JBS](https://bugs.openjdk.org/browse/JDK-8359428) |
| 6798061 | The removal of System.out.println from KeyboardManager | [JBS](https://bugs.openjdk.org/browse/JDK-6798061) |
| 8356594 | JSplitPane loses divider location when reopened via JOptionPane.createDialog() | [JBS](https://bugs.openjdk.org/browse/JDK-8356594) |
| 8357299 | Graphics copyArea doesn't copy any pixels when there is overflow | [JBS](https://bugs.openjdk.org/browse/JDK-8357299) |
| 8355179 | Reinstate javax/swing/JScrollBar/4865918/bug4865918.java headful and macos run | [JBS](https://bugs.openjdk.org/browse/JDK-8355179) |
| 8343007 | Enhance Buffered Image handling | [JBS](https://bugs.openjdk.org/browse/JDK-8343007) |
| 8352682 | Opensource JComponent tests | [JBS](https://bugs.openjdk.org/browse/JDK-8352682) |
| 8352687 | Opensource few JInternalFrame and JTextField tests | [JBS](https://bugs.openjdk.org/browse/JDK-8352687) |
| 8352686 | Opensource JInternalFrame tests - series3 | [JBS](https://bugs.openjdk.org/browse/JDK-8352686) |
| 8352684 | Opensource JInternalFrame tests - series1 | [JBS](https://bugs.openjdk.org/browse/JDK-8352684) |
| 8352685 | Opensource JInternalFrame tests - series2 | [JBS](https://bugs.openjdk.org/browse/JDK-8352685) |
| 8352680 | Opensource few misc swing tests | [JBS](https://bugs.openjdk.org/browse/JDK-8352680) |
| 8352677 | Opensource JMenu tests - series2 | [JBS](https://bugs.openjdk.org/browse/JDK-8352677) |
| 8352678 | Opensource few JMenuItem tests | [JBS](https://bugs.openjdk.org/browse/JDK-8352678) |
| 8352676 | Opensource JMenu tests - series1 | [JBS](https://bugs.openjdk.org/browse/JDK-8352676) |
| 4466930 | JTable.selectAll boundary handling | [JBS](https://bugs.openjdk.org/browse/JDK-4466930) |
| 8350924 | javax/swing/JMenu/4213634/bug4213634.java fails | [JBS](https://bugs.openjdk.org/browse/JDK-8350924) |
| 8350224 | Test javax/swing/JComboBox/TestComboBoxComponentRendering.java fails in ubuntu 23.x and later | [JBS](https://bugs.openjdk.org/browse/JDK-8350224) |
| 8347019 | Test javax/swing/JRadioButton/8033699/bug8033699.java still fails | [JBS](https://bugs.openjdk.org/browse/JDK-8347019) |
| 8318577 | Windows Look-and-Feel JProgressBarUI does not render correctly on 2x UI scale | [JBS](https://bugs.openjdk.org/browse/JDK-8318577) |
| 8345618 | javax/swing/text/Caret/8163124/CaretFloatingPointAPITest.java leaves Caret is not complete | [JBS](https://bugs.openjdk.org/browse/JDK-8345618) |
| 8346828 | javax/swing/JScrollBar/4865918/bug4865918.java still fails in CI | [JBS](https://bugs.openjdk.org/browse/JDK-8346828) |
| 8346260 | Test "javax/swing/JOptionPane/bug4174551.java" failed | [JBS](https://bugs.openjdk.org/browse/JDK-8346260) |
| 8346324 | javax/swing/JScrollBar/4865918/bug4865918.java fails in CI | [JBS](https://bugs.openjdk.org/browse/JDK-8346324) |
| 8346234 | javax/swing/text/DefaultEditorKit/4278839/bug4278839.java still fails in CI | [JBS](https://bugs.openjdk.org/browse/JDK-8346234) |
| 8346055 | javax/swing/text/StyledEditorKit/4506788/bug4506788.java fails in ubuntu22.04 | [JBS](https://bugs.openjdk.org/browse/JDK-8346055) |
| 8334581 | Remove no-arg constructor BasicSliderUI() | [JBS](https://bugs.openjdk.org/browse/JDK-8334581) |
| 8345767 | javax/swing/JSplitPane/4164779/JSplitPaneKeyboardNavigationTest.java fails in ubuntu22.04 | [JBS](https://bugs.openjdk.org/browse/JDK-8345767) |
| 8268145 | [macos] Rendering artifacts is seen when text inside the JTable with TableCellEditor having JTextfield | [JBS](https://bugs.openjdk.org/browse/JDK-8268145) |

> **JBS Link**: https://bugs.openjdk.org/browse/JDK-[Issue Number]

## 4. Key Contributions

### 1. JSplitPane Component Orientation Fix (JDK-8365886)

Fixed an issue where JSplitPane loses track of the left component when component orientation is changed.

```java
// Before: Component tracking lost during orientation change
// After: Properly maintain component reference during orientation switch

public void setComponentOrientation(ComponentOrientation o) {
    // Preserve left/right component references
    Component leftComp = getLeftComponent();
    Component rightComp = getRightComponent();
    super.setComponentOrientation(o);
    // Restore components after orientation change
    if (leftComp != null) setLeftComponent(leftComp);
    if (rightComp != null) setRightComponent(rightComp);
}
```

### 2. ImageIcon Null Handling Enhancement (JDK-8159055)

Clarified and improved handling of null and invalid image data for ImageIcon constructors.

```java
/**
 * Clarifies behavior for null/invalid image data
 * @param image the image to use, may be null
 * @throws IllegalArgumentException if image data is invalid
 */
public ImageIcon(Image image) {
    this(image, null);
}

public ImageIcon(Image image, String description) {
    if (image == null) {
        // Avoid wasted work - don't set description for null image
        return;
    }
    this.image = image;
    this.description = description;
}
```

### 3. Graphics copyArea Overflow Fix (JDK-8357299)

Fixed an issue where Graphics.copyArea doesn't copy any pixels when there is overflow.

```java
// Fixed: Handle integer overflow in copyArea calculations
public void copyArea(int x, int y, int width, int height, int dx, int dy) {
    // Check for overflow before performing copy
    long destX = (long)x + dx;
    long destY = (long)y + dy;
    if (destX < Integer.MIN_VALUE || destX > Integer.MAX_VALUE ||
        destY < Integer.MIN_VALUE || destY > Integer.MAX_VALUE) {
        return; // No pixels to copy when overflow occurs
    }
    // ... rest of implementation
}
```

### 4. JTable selectAll Boundary Handling (JDK-4466930)

Fixed boundary handling in JTable.selectAll method.

```java
public void selectAll() {
    if (getRowCount() <= 0 || getColumnCount() <= 0) {
        return; // Handle empty table case
    }
    // Properly select all rows and columns
    setRowSelectionInterval(0, getRowCount() - 1);
    setColumnSelectionInterval(0, getColumnCount() - 1);
}
```

### 5. RTL Orientation for MenuItem (JDK-8370465)

Fixed Right-to-Left orientation issues with MenuItem component.

```java
// Fixed RTL orientation for menu items
public void applyComponentOrientation(ComponentOrientation o) {
    if (o == null) {
        return;
    }
    super.applyComponentOrientation(o);
    // Ensure proper text and icon positioning for RTL
    if (!o.isLeftToRight()) {
        // Adjust accelerator and icon positioning
        updateAcceleratorPosition();
    }
}
```

## 5. Development Style

### Code Quality Focus

1. **Cross-Platform Testing**: Ensures fixes work across macOS, Windows, and Linux
2. **Look and Feel Coverage**: Tests across Metal, Nimbus, GTK, and Windows L&F
3. **Test Open-Sourcing**: Actively converts closed tests to open-source
4. **Documentation**: Improves Javadoc clarity and correctness

### Testing Approach

- Headful and headless test support
- Platform-specific test handling
- Problem listing for known issues
- Test stability improvements

### Commit Patterns

- Often groups related test fixes together
- Includes both bug fixes and test improvements
- Focuses on UI component behavior consistency

## 6. Related Links

- [OpenJDK Profile](https://openjdk.org/people/psadhukhan)
- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=psadhukhan)
- [JBS Issues](https://bugs.openjdk.org/issues/?jql=reporter%20%3D%20psadhukhan)

## 审查统计

| 指标 | 值 |
|------|-----|
| **总审查次数** | 535 |
| **活跃仓库数** | 2 |
