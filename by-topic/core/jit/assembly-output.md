# 汇编输出分析

> 如何查看和分析 JIT 生成的机器码？

[← 返回 JIT 编译](../)

---
## 目录

1. [结论先行](#1-结论先行)
2. [一眼看懂](#2-一眼看懂)
3. [生成汇编输出](#3-生成汇编输出)
4. [安装 hsdis](#4-安装-hsdis)
5. [汇编输出解读](#5-汇编输出解读)
6. [优化模式识别](#6-优化模式识别)
7. [实战案例分析](#7-实战案例分析)
8. [汇编分析技巧](#8-汇编分析技巧)
9. [ARM 汇编](#9-arm-汇编)
10. [常见问题](#10-常见问题)
11. [相关链接](#11-相关链接)

---


## 1. 结论先行

| 问题 | 答案 |
|------|------|
| **如何生成汇编？** | `-XX:+PrintAssembly` + hsdis 插件 |
| **hsdis 是什么？** | HotSpot 反汇编插件 |
| **如何解读汇编？** | 需要了解 x86/ARM 指令集基础 |
| **有什么用？** | 验证优化效果、调试性能问题 |

---

## 2. 一眼看懂

### 汇编输出的价值

```
为什么看汇编？
├── 验证优化是否生效
│   ├── 真的向量化了吗？
│   ├── 真的内联了吗？
│   └── 真的常量折叠了吗？
├── 调试性能问题
│   ├── 为什么这么慢？
│   ├── 哪里有额外开销？
│   └── 找到瓶颈代码
└── 学习编译器工作原理
    ├── 如何生成代码
    ├── 如何优化代码
    └── CPU 指令利用
```

### 汇编输出示例

```asm
; 简单的 Java 方法: int add(int a, int b) { return a + b; }

; JIT 生成的 x86-64 汇编:
mov    eax, DWORD PTR [rdx+8]   ; 加载参数 a
add    eax, DWORD PTR [r8+8]    ; 加上参数 b
ret                             ; 返回

; 优化后的版本 (内联后):
lea    eax, [rdx+8+r8*1+8]      ; 直接计算地址和值
ret
```

---

## 3. 生成汇编输出

### 方法 1: PrintAssembly (推荐)

```bash
# 1. 下载 hsdis 插件
# https://github.com/JetBrains/jdk-dist/raw/master/jdks/hsdis/

# 2. 放置到正确位置
# Linux: hsdis-amd64.so → jre/lib/amd64/hsdis-amd64.so
# Windows: hsdis-amd64.dll → bin/hsdis-amd64.dll
# macOS: hsdis-amd64.dylib → lib/hsdis-amd64.dylib

# 3. 启用 PrintAssembly
java -XX:+UnlockDiagnosticVMOptions \
     -XX:+PrintAssembly \
     MyApp

# 4. 输出大量汇编到标准输出
```

### 方法 2: hsdis + 特定方法

```bash
# 只打印特定方法的汇编
java -XX:+PrintAssembly \
     -XX:CompileCommand=print,*Class.method \
     MyApp

# 只打印特定类的汇编
java -XX:+PrintAssembly \
     -XX:CompileCommand=print,*String.* \
     MyApp
```

### 方法 3: JITWatch (GUI 工具)

```bash
# 1. 记录编译日志
java -XX:+UnlockDiagnosticVMOptions \
     -XX:+PrintCompilation \
     -XX:+LogCompilation \
     -XX:LogFile=compilation.log \
     MyApp

# 2. 使用 JITWatch 打开
# https://github.com/AdoptOpenJDK/jitwatch
java -jar jitwatch.jar compilation.log
```

### 方法 4: PrintAssemblyDump

```bash
# JDK 17+ 新方法
java -XX:+UnlockDiagnosticVMOptions \
     -XX:+PrintAssembly \
     -XX:PrintAssemblyOptions=syntax \
     MyApp
```

---

## 4. 安装 hsdis

### Linux

```bash
# 下载预编译版本
wget https://github.com/JetBrains/jdk-dist/raw/master/jdks/hsdis/hsdis-amd64.so

# 放到正确位置
sudo cp hsdis-amd64.so $JAVA_HOME/lib/server/hsdis-amd64.so

# 或放到当前目录
export LD_LIBRARY_PATH=.:$LD_LIBRARY_PATH
```

### macOS

```bash
# macOS 需要自己编译或下载
brew install hsdis

# 或手动放置
cp hsdis-amd64.dylib $JAVA_HOME/lib/server/
```

### Windows

```bash
# 下载 hsdis-amd64.dll
# 放到 JAVA_HOME/bin/ 或 PATH 目录
```

### 验证安装

```bash
java -XX:+UnlockDiagnosticVMOptions \
     -XX:+PrintAssembly \
     -version

# 如果看到汇编输出 = 安装成功
# 如果报错 "hsdis not found" = 安装失败
```

---

## 5. 汇编输出解读

### x86-64 寄存器

| 寄存器 | 用途 |
|--------|------|
| **rax/eax** | 返回值 |
| **rbx/ebx** | 被调用者保存 |
| **rcx/ecx** | 第 4 个参数 / this |
| **rdx/edx** | 第 3 个参数 |
| **rsi/esi** | 第 2 个参数 |
| **rdi/edi** | 第 1 个参数 |
| **rbp/ebp** | 帧指针 |
| **rsp/esp** | 栈指针 |
| **r8-r15** | 额外参数 / 临时 |

### 调用约定

```java
// Java 方法
int add(int a, int b, int c, int d)

// x86-64 寄存器传参:
// a → rsi (第 1 个)
// b → rdx (第 2 个)
// c → rcx (第 3 个)
// d → r8  (第 4 个)

// 返回值 → rax
```

### 常见指令

| 指令 | 说明 | 示例 |
|------|------|------|
| **mov** | 数据传送 | `mov eax, ebx` |
| **lea** | 加载有效地址 | `lea eax, [rbx+4]` |
| **add/sub** | 加减 | `add eax, 10` |
| **imul** | 乘法 | `imul eax, ebx` |
| **cmp/test** | 比较 | `cmp eax, 10` |
| **jmp** | 跳转 | `jmp label` |
| **call** | 调用 | `call function` |
| **ret** | 返回 | `ret` |

### SIMD 指令

| 指令集 | 宽度 | 指令示例 |
|--------|------|----------|
| **MMX** | 64-bit | `movq` |
| **SSE** | 128-bit | `movdqu`, `addps` |
| **AVX** | 256-bit | `vmovdqu`, `vaddps` |
| **AVX-512** | 512-bit | `vmovdqu64`, `vaddps` |

---

## 6. 优化模式识别

### 1. 内联验证

```java
// 原始代码
int result = add(a, b);

// 未内联 (有调用)
call    AddClass.add    ; 调用方法

// 已内联 (无调用)
mov     eax, [rsi]      ; 直接加载 a
add     eax, [rdx]      ; 直接加上 b
; 无 call 指令
```

### 2. 常量折叠

```java
// 原始代码
return 100 * 60 * 60 * 24;

// 未优化
mov     eax, 100
imul    eax, 60
imul    eax, 60
imul    eax, 24

// 已优化 (常量折叠)
mov     eax, 8640000    ; 直接使用计算结果
```

### 3. 循环展开

```java
// 原始代码
for (int i = 0; i < 4; i++) {
    sum += array[i];
}

// 未展开 (有循环)
mov     rcx, 0
loop_start:
add     eax, [rdi+rcx*4]
inc     rcx
cmp     rcx, 4
jl      loop_start

// 已展开 (无循环)
add     eax, [rdi]
add     eax, [rdi+4]
add     eax, [rdi+8]
add     eax, [rdi+12]
; 无循环指令
```

### 4. 向量化

```java
// 原始代码
for (int i = 0; i < 1024; i++) {
    a[i] = b[i] + c[i];
}

// 未向量化 (标量循环)
loop_start:
mov     eax, [rdi+rcx*4]
add     eax, [rsi+rcx*4]
mov     [rdx+rcx*4], eax
inc     rcx
cmp     rcx, 1024
jl      loop_start

// 已向量化 (SIMD)
vmovups ymm0, [rdi]      ; 加载 8 个 float
vaddps ymm0, ymm0, [rsi]  ; SIMD 加法
vmovups [rdx], ymm0       ; 存储 8 个 float
; 每次迭代处理 8 个元素
```

### 5. 分支消除

```java
// 原始代码
final int X = 10;
if (x > X) {
    doSomething();
}

// 未消除 (有分支)
cmp     eax, 10
jle     skip
call    doSomething
skip:

// 已消除 (无分支)
; 整个 if 块被优化掉
call    doSomething    ; 直接调用
```

---

## 7. 实战案例分析

### 案例 1: 验证 MergeStore

```java
// 原始代码
buf[0] = 'a';
buf[1] = 'b';
buf[2] = 'c';
buf[3] = 'd';

// 未优化
mov     byte ptr [rdi], 97
mov     byte ptr [rdi+1], 98
mov     byte ptr [rdi+2], 99
mov     byte ptr [rdi+3], 100

// 已优化 (MergeStore)
mov     dword ptr [rdi], 1684234846
; 0x64636261 = "abcd"
; 一次写入 4 字节
```

### 案例 2: 验证逃逸分析

```java
// 原始代码
Point p = new Point(10, 20);
return p.x + p.y;

// 未优化 (有对象分配)
mov     rdi, [Class_Point_addr]
call    allocate_object    ; 分配对象
mov     [rdi+8], 10
mov     [rdi+12], 20
mov     eax, [rdi+8]
add     eax, [rdi+12]

// 已优化 (标量替换)
mov     eax, 10          ; p.x
add     eax, 20          ; p.y
; 无对象分配
```

### 案例 3: 验证 SuperWord

```java
// 原始代码
for (int i = 0; i < 256; i++) {
    result[i] = input[i] * 2;
}

// 未向量化 (标量)
mov     eax, [rsi+rcx*4]
add     eax, eax
mov     [rdi+rcx*4], eax
inc     rcx
cmp     rcx, 256
jl      loop

// 已向量化 (AVX2, 256-bit = 8 × int)
vmovdqu ymm0, [rsi]      ; 加载 8 个 int
vpslld ymm0, ymm0, 1     ; 左移 1 位 (= ×2)
vmovdqu [rdi], ymm0       ; 存储 8 个 int
add     rsi, 32
add     rdi, 32
cmp     rcx, 256
jl      loop
; 每次处理 8 个元素
```

---

## 8. 汇编分析技巧

### 1. 对比优化前后

```bash
# 生成两个版本的汇编
# 版本 1: 优化前
java -XX:+PrintAssembly \
     -XX:CompileCommand=dontinline,*Class.method \
     OldVersion

# 版本 2: 优化后
java -XX:+PrintAssembly \
     NewVersion

# 使用 diff 对比
diff old_asm.txt new_asm.txt
```

### 2. 查找特定模式

```bash
# 查找是否有某个指令
grep "call" assembly.txt      ; 查找方法调用
grep "vmov" assembly.txt       ; 查找 SIMD 指令
grep "loop" assembly.txt       ; 查找循环

# 统计指令数量
grep -c "call" assembly.txt    ; 统计调用次数
grep -c "vmov" assembly.txt     ; 统计 SIMD 指令
```

### 3. 性能热点分析

```bash
# 使用 perf 结合汇编
perf record -e instructions:u ./MyApp
perf report
# 找到热点函数
# 然后查看该函数的汇编
```

---

## 9. ARM 汇编

### ARM64 寄存器

| 寄存器 | 用途 |
|--------|------|
| **x0-x7** | 参数/返回值 |
| **x19-x28** | 被调用者保存 |
| **x29** | 帧指针 |
| **x30** | 返回地址 |
| **sp** | 栈指针 |
| **v0-v31** | SIMD/FP |

### ARM64 指令示例

```asm
; 简单加法
ldr     w0, [x19]       ; 加载
ldr     w1, [x20]
add     w0, w0, w1      ; 相加
ret                     ; 返回

; SIMD 向量化
ld1     {v0.4s}, [x0]   ; 加载 4 个 float
ld1     {v1.4s}, [x1]
fadd    v0.4s, v0.4s, v1.4s  ; SIMD 加法
st1     {v0.4s}, [x2]   ; 存储
```

---

## 10. 常见问题

### Q1: hsdis 找不到？

```bash
# 错误: "hsdis not found"

# 解决:
1. 确认 hsdis 文件存在
2. 确认路径正确
3. Linux: export LD_LIBRARY_PATH=.
4. 或使用绝对路径
```

### Q2: 汇编输出太多？

```bash
# 限制输出
-XX:CompileCommand=print,*Class.method  ; 只打印特定方法
-XX:CompileCommand=exclude,*java.*     ; 排除 java.* 包
```

### Q3: 如何学习汇编？

```
推荐资源:
├── Intel 指令集手册
├── AMD64 架构手册
├── "Introduction to 64 Bit Assembly Programming"
└── 实践: 多看、多对比
```

---

## 11. 相关链接

### 本地文档

- [C2 优化阶段](c2-phases.md) - 代码生成
- [SuperWord 向量化](superword.md) - SIMD 优化
- [诊断工具](diagnostics.md) - 其他诊断方法
- [IGV 实战](igv-tutorial.md) - IR 图可视化

### 外部资源

- [x86-64 Assembly Reference](https://www.felixcloutier.com/x86/)
- [ARM64 Instruction Set](https://developer.arm.com/documentation/ddi0602/latest/)
- [JITWatch](https://github.com/AdoptOpenJDK/jitwatch)

---

**最后更新**: 2026-03-21
