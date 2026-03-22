# Dmitry Markov

> **GitHub**: [@dmarkov20](https://github.com/dmarkov20)
> **Organization**: Oracle
> **OpenJDK Contributions**: 63 to openjdk/jdk (9 integrated PRs on GitHub)

---
## 目录

1. [概述](#1-概述)
2. [Basic Information](#2-basic-information)
3. [Contribution Overview](#3-contribution-overview)
4. [Key Contributions](#4-key-contributions)
5. [Recent Activity](#5-recent-activity)
6. [Development Style](#6-development-style)
7. [Related Links](#7-related-links)

---

## 1. 概述

Dmitry Markov is an Oracle engineer based in Dublin, Ireland, specializing in AWT/Swing, client libraries, and platform-specific desktop integration. With 63 contributions to openjdk/jdk, he focuses on Windows and macOS desktop client issues including input method handling, drag-and-drop, accessibility, and native UI integration. The majority of his contributions predate the GitHub migration, with 9 integrated PRs on GitHub. His work ensures that Java desktop applications interact correctly with native platform features like keyboard layouts, focus management, and accessibility APIs.

---

## 2. Basic Information

| Attribute | Value |
|-----------|-------|
| **Name** | Dmitry Markov |
| **Current Organization** | Oracle |
| **Location** | Dublin, Ireland |
| **GitHub** | [@dmarkov20](https://github.com/dmarkov20) |
| **PRs** | [9 integrated](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Admarkov20+is%3Aclosed+label%3Aintegrated) |
| **Total Contributions** | 63 (mostly pre-GitHub commits) |
| **主要领域** | AWT/Swing, Client Libraries, Input Methods, Accessibility, Drag and Drop |

---

## 3. Contribution Overview

### By Category

| Category | Approx. Count | Description |
|----------|---------------|-------------|
| Input Methods / Keyboard | 10+ | Windows IME handling, keyboard layout state management |
| Drag and Drop | 8+ | DnD hang fixes on Windows, IME interaction during DnD |
| Accessibility | 5+ | macOS accessibility permissions, screen reader integration |
| AWT Native Integration | 15+ | Focus management, window decorations, native style masks |
| Java2D / Color Management | 5+ | Color conversion tests, LCMS profile handling |
| macOS Client | 10+ | Deprecated API cleanup, macOS-specific rendering and input |

### Key Areas of Expertise

- **Windows Input Method Handling**: Fixing complex interactions between the Windows Input Method Editor (IME) and Java's AWT layer, including state preservation across dialogs and DnD operations.
- **Drag and Drop**: Resolving platform-specific DnD hangs on Windows, a notoriously difficult area involving OLE/COM threading and native message loops.
- **macOS Accessibility**: Documenting and implementing accessibility permission requirements for Java applications on macOS.
- **AWT Native Integration**: Platform-specific fixes for window management, focus handling, and native UI element interaction on Windows and macOS.

---

## 4. Key Contributions

### 4.1 Windows Drag and Drop Hang Fixes (JDK-8262446, JDK-8274751)

Fixed recurring drag-and-drop hangs on Windows in two separate efforts ([PR #2825](https://github.com/openjdk/jdk/pull/2825), [PR #7125](https://github.com/openjdk/jdk/pull/7125)). DnD hangs on Windows are among the most difficult AWT bugs to diagnose and fix, involving complex interactions between OLE/COM threading, Windows message loops, and Java's event dispatch thread.

### 4.2 Windows IME State After DnD (JDK-8261231)

Fixed a bug where the Windows Input Method Editor was disabled after a drag-and-drop operation ([PR #2448](https://github.com/openjdk/jdk/pull/2448)). This affected East Asian language users who rely on IME for text input, as DnD operations would break their ability to type in Japanese, Chinese, or Korean.

### 4.3 Keyboard Layout State Preservation (JDK-8324491)

Fixed a bug where the keyboard layout didn't keep its state when it was changed while a dialog was active ([PR #22411](https://github.com/openjdk/jdk/pull/22411)). This affected users who switch between keyboard layouts (e.g., English and Japanese) while interacting with Java dialog boxes.

### 4.4 Japanese Mouse Click Input Fix (JDK-8258805)

Fixed an issue where Japanese characters could not be entered by mouse click on Windows 10 ([PR #2142](https://github.com/openjdk/jdk/pull/2142)). This was a regression affecting the IME candidate window interaction in AWT applications.

### 4.5 macOS Accessibility Documentation (JDK-8303130)

Documented the required accessibility permissions on macOS ([PR #12772](https://github.com/openjdk/jdk/pull/12772)) that Java applications need to properly interact with screen readers and other assistive technologies on macOS.

### 4.6 DrawFocusRect Assertion Failure (JDK-8346887)

Fixed an assertion failure in `DrawFocusRect()` on Windows ([PR #22973](https://github.com/openjdk/jdk/pull/22973)), a native rendering issue that could crash debug builds when drawing focus rectangles in AWT components.

### 4.7 macOS Deprecated Style Masks Cleanup (JDK-8281555)

Removed usage of deprecated NSWindow style mask constants on macOS ([PR #7408](https://github.com/openjdk/jdk/pull/7408)), keeping the AWT macOS backend aligned with current Apple API conventions.

---

## 5. Recent Activity

| Date | PR | Title |
|------|-----|-------|
| 2025-01 | [#22973](https://github.com/openjdk/jdk/pull/22973) | DrawFocusRect() may cause an assertion failure |
| 2024-12 | [#22411](https://github.com/openjdk/jdk/pull/22411) | Keyboard layout didn't keep its state if changed when dialog was active |
| 2024-03 | [#18097](https://github.com/openjdk/jdk/pull/18097) | ColConvTest.java assumes profiles were generated by LCMS |
| 2023-02 | [#12772](https://github.com/openjdk/jdk/pull/12772) | Document required Accessibility permissions on macOS |
| 2022-02 | [#7408](https://github.com/openjdk/jdk/pull/7408) | [macos] Get rid of deprecated Style Masks constants |
| 2022-01 | [#7125](https://github.com/openjdk/jdk/pull/7125) | Drag And Drop hangs on Windows |
| 2021-03 | [#2825](https://github.com/openjdk/jdk/pull/2825) | DragAndDrop hangs on Windows |
| 2021-02 | [#2448](https://github.com/openjdk/jdk/pull/2448) | Windows IME was disabled after DnD operation |

---

## 6. Development Style

### Patterns

- **Platform-specific expertise**: Nearly all contributions involve native platform interactions on Windows or macOS, requiring deep knowledge of Win32 APIs, COM/OLE, Cocoa/AppKit, and how AWT bridges to these native systems.
- **Low volume, high impact**: Each contribution addresses a difficult, user-facing bug in desktop Java applications rather than incremental improvements.
- **Cross-platform coverage**: While most work targets Windows (IME, DnD), Markov also maintains macOS client code, indicating broad desktop platform knowledge.
- **Pre-GitHub veteran**: With 54 of 63 contributions predating the GitHub migration, Markov is a long-tenured contributor to the JDK client libraries.

### Commit Style

Commits follow the standard OpenJDK format: `JDK-NNNNNNN: <description>`. Messages are concise and typically describe the symptom being fixed.

---

## 7. Related Links

- [GitHub Profile](https://github.com/dmarkov20)
- [GitHub Commits to openjdk/jdk](https://github.com/openjdk/jdk/commits?author=dmarkov20)
- [Integrated PRs](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Admarkov20+is%3Aclosed+label%3Aintegrated)
