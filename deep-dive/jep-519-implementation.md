# JEP 519: Compact Object Headers 实现分析

> 基于 JDK 25 HotSpot 源码的紧凑对象头（Compact Object Headers）内部实现深度解析

---

## 1. 背景与动机

### 传统对象头布局

在 64-bit JVM 中，每个 Java 对象传统上有一个由两部分组成的对象头（object header）：

```
传统对象头 (64-bit JVM, +UseCompressedClassPointers):
┌───────────────────────────────────────────────────────────────────┐
│ Mark Word (8 bytes = 64 bits)                                    │
│ ├── lock 状态 (2 bits)                                           │
│ ├── self-fwd 标记 (1 bit)                                        │
│ ├── GC 年龄 age (4 bits)                                         │
│ ├── unused_gap (4 bits, 保留给 Valhalla)                          │
│ ├── identity hash (31 bits)                                      │
│ └── unused (22 bits)                                             │
├───────────────────────────────────────────────────────────────────┤
│ Klass Pointer (4 bytes, 压缩的 narrowKlass)                       │
│ └── 指向此对象所属的 Klass 元数据                                   │
├───────────────────────────────────────────────────────────────────┤
│ [Klass Gap] (4 bytes, 对齐填充)                                   │
└───────────────────────────────────────────────────────────────────┘
总计: 12 bytes (+ 4 bytes 对齐填充 = 实际占 16 bytes)
```

### 紧凑对象头布局

JEP 519 将 klass 指针编码到 mark word 的高 22 位中，消除独立的 klass 指针字段：

```
紧凑对象头 (64-bit JVM, +UseCompactObjectHeaders):
┌───────────────────────────────────────────────────────────────────┐
│ Mark Word (8 bytes = 64 bits)                                    │
│                                                                   │
│  63         42 41         11 10    7  6    3  2   1  0            │
│  ├─ klass ──┤  ├─ hash ──┤  ├gap─┤  ├age─┤  sf  ├lock┤          │
│  (22 bits)     (31 bits)    (4 b)  (4 b)  (1b)  (2 b)           │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
总计: 8 bytes (无需额外的 klass 指针和填充)
```

### 内存节省效果

```
对象类型               传统头      紧凑头      节省
──────────────────────────────────────────────────────
最小对象（无字段）      16 bytes    8 bytes    50%
Point (2 int)          24 bytes   16 bytes    33%
String (引用+哈希+标志) 40 bytes   32 bytes    20%
ArrayList (数组引用+大小) 24 bytes  16 bytes    33%
HashMap$Node           32 bytes   24 bytes    25%
byte[0]                16 bytes   16 bytes    0% (数组有长度字段)
```

注意：数组对象的节省比例较低，因为它们有额外的 length 字段。

---

## 2. Mark Word 实现

### 位字段定义

```cpp
// 文件: src/hotspot/share/oops/markWord.hpp

class markWord {
 private:
  uintptr_t _value;

 public:
  // === 通用常量（所有模式共享）===
  static const int age_bits                       = 4;
  static const int lock_bits                      = 2;
  static const int self_fwd_bits                  = 1;
  static const int max_hash_bits                  = BitsPerWord - age_bits - lock_bits - self_fwd_bits;
  static const int hash_bits                      = max_hash_bits > 31 ? 31 : max_hash_bits;
  static const int unused_gap_bits                = LP64_ONLY(4) NOT_LP64(0);
  // unused_gap (4 bits): 保留给 Valhalla 项目使用

  // === 移位量（shift）===
  static const int lock_shift                     = 0;
  static const int self_fwd_shift                 = lock_shift + lock_bits;         // 2
  static const int age_shift                      = self_fwd_shift + self_fwd_bits; // 3
  static const int hash_shift                     = age_shift + age_bits + unused_gap_bits; // 11

  // === 掩码（mask）===
  static const uintptr_t lock_mask                = right_n_bits(lock_bits);         // 0x3
  static const uintptr_t lock_mask_in_place       = lock_mask << lock_shift;
  static const uintptr_t self_fwd_mask            = right_n_bits(self_fwd_bits);     // 0x1
  static const uintptr_t self_fwd_mask_in_place   = self_fwd_mask << self_fwd_shift;
  static const uintptr_t age_mask                 = right_n_bits(age_bits);          // 0xF
  static const uintptr_t age_mask_in_place        = age_mask << age_shift;
  static const uintptr_t hash_mask                = right_n_bits(hash_bits);         // 0x7FFF_FFFF
  static const uintptr_t hash_mask_in_place       = hash_mask << hash_shift;

#ifdef _LP64
  // === 紧凑头专用：klass 指针字段 ===
  static constexpr int klass_offset_in_bytes      = 4;    // klass 在 mark word 中的字节偏移
  static constexpr int klass_shift                = hash_shift + hash_bits;  // 42
  static constexpr int klass_shift_at_offset      = klass_shift - klass_offset_in_bytes * BitsPerByte; // 10
  static constexpr int klass_bits                 = 22;
  static constexpr uintptr_t klass_mask           = right_n_bits(klass_bits);  // 0x3F_FFFF
  static constexpr uintptr_t klass_mask_in_place  = klass_mask << klass_shift;
#endif
};
```

**64-bit mark word 完整位布局**（从低位到高位）：

```
位 [1:0]   lock     (2 bits)  锁状态
位 [2]     self_fwd (1 bit)   自转发标记（GC 使用）
位 [6:3]   age      (4 bits)  GC 年龄（最大 15）
位 [10:7]  gap      (4 bits)  保留（Valhalla）
位 [41:11] hash     (31 bits) 身份哈希值
位 [63:42] klass    (22 bits) 窄类指针（仅 compact headers 模式）
```

### 锁状态编码

```cpp
// 文件: src/hotspot/share/oops/markWord.hpp

static const uintptr_t locked_value             = 0;  // [00] 已锁定（fast-locking 或 stack-locking）
static const uintptr_t unlocked_value           = 1;  // [01] 未锁定
static const uintptr_t monitor_value            = 2;  // [10] 膨胀锁（inflated monitor）
static const uintptr_t marked_value             = 3;  // [11] GC 标记（转发指针）
```

mark word 中的注释说明了锁状态的具体含义：

```
[ptr             | 00]  locked    ptr 指向栈上真实头（stack-locking）
[header          | 00]  locked    锁定的常规对象头（fast-locking）
[header          | 01]  unlocked  正常未锁定状态
[ptr             | 10]  monitor   膨胀锁（UseObjectMonitorTable == false 时头被替换）
[header          | 10]  monitor   膨胀锁（UseObjectMonitorTable == true 时头保留）
[ptr             | 11]  marked    GC 转发指针
```

### 关键访问方法

```cpp
// 文件: src/hotspot/share/oops/markWord.hpp

// 锁状态判断
bool is_locked()   const { return (mask_bits(value(), lock_mask_in_place) != unlocked_value); }
bool is_unlocked() const { return (mask_bits(value(), lock_mask_in_place) == unlocked_value); }
bool is_marked()   const { return (mask_bits(value(), lock_mask_in_place) == marked_value); }
bool has_monitor() const { return ((value() & lock_mask_in_place) == monitor_value); }

// fast-locking 判断
bool is_fast_locked() const { return (value() & lock_mask_in_place) == locked_value; }

// GC 年龄操作
uint age() const { return (uint) mask_bits(value() >> age_shift, age_mask); }
markWord set_age(uint v) const {
    return markWord((value() & ~age_mask_in_place) | ((v & age_mask) << age_shift));
}
markWord incr_age() const {
    return age() == max_age ? markWord(_value) : set_age(age() + 1);
}

// 哈希操作
intptr_t hash() const { return mask_bits(value() >> hash_shift, hash_mask); }
bool has_no_hash() const { return hash() == no_hash; }
markWord copy_set_hash(intptr_t hash) const {
    uintptr_t tmp = value() & (~hash_mask_in_place);
    tmp |= ((hash & hash_mask) << hash_shift);
    return markWord(tmp);
}

// GC 存活性判断 —— 未锁定且无哈希时不需保留
bool must_be_preserved() const {
    return (!is_unlocked() || !has_no_hash());
}

// 原型 mark word（用于初始化）
static markWord prototype() {
    return markWord( no_hash_in_place | no_lock_in_place );  // hash=0, lock=unlocked
}
```

---

## 3. Klass 指针编码

### 从 Mark Word 提取 Klass

紧凑头模式下，klass 指针编码为 22-bit 的 narrowKlass，存储在 mark word 的高 22 位：

```cpp
// 文件: src/hotspot/share/oops/markWord.inline.hpp

narrowKlass markWord::narrow_klass() const {
#ifdef _LP64
    assert(UseCompactObjectHeaders, "only used with compact object headers");
    return narrowKlass(value() >> klass_shift);  // 右移 42 位，提取高 22 位
#else
    ShouldNotReachHere();
    return 0;
#endif
}

markWord markWord::set_narrow_klass(narrowKlass narrow_klass) const {
#ifdef _LP64
    assert(UseCompactObjectHeaders, "only used with compact object headers");
    return markWord((value() & ~klass_mask_in_place) | ((uintptr_t) narrow_klass << klass_shift));
#else
    ShouldNotReachHere();
    return markWord(0);
#endif
}

Klass* markWord::klass() const {
#ifdef _LP64
    assert(UseCompactObjectHeaders, "only used with compact object headers");
    return CompressedKlassPointers::decode_not_null(narrow_klass());
#else
    ShouldNotReachHere();
    return nullptr;
#endif
}
```

### CompressedKlassPointers 编解码

22-bit narrowKlass 到完整 Klass* 指针的编解码：

```cpp
// 文件: src/hotspot/share/oops/compressedKlass.inline.hpp

// 解码: narrowKlass → Klass*
inline Klass* CompressedKlassPointers::decode_not_null_without_asserts(
        narrowKlass v, address narrow_base, int shift) {
    return (Klass*)((uintptr_t)narrow_base + ((uintptr_t)v << shift));
}

// 编码: Klass* → narrowKlass
inline narrowKlass CompressedKlassPointers::encode_not_null_without_asserts(
        const Klass* k, address narrow_base, int shift) {
    return (narrowKlass)(pointer_delta(k, narrow_base, 1) >> shift);
}
```

编码公式：
- **编码**: `narrowKlass = (klass_address - base) >> shift`
- **解码**: `klass_address = base + (narrowKlass << shift)`

### COH 模式下的编码参数

```cpp
// 文件: src/hotspot/share/oops/compressedKlass.hpp

class CompressedKlassPointers : public AllStatic {
    // 非 COH 模式：32-bit narrowKlass
    static constexpr int narrow_klass_pointer_bits_noncoh = 32;
    // COH 模式：22-bit narrowKlass
    static constexpr int narrow_klass_pointer_bits_coh = 22;

    // 非 COH 模式：最大移位 3
    static constexpr int max_shift_noncoh = 3;
    // COH 模式：最大移位 10
    static constexpr int max_shift_coh = 10;

    static int _narrow_klass_pointer_bits;  // 运行时确定
    static int _max_shift;                  // 运行时确定
    static address _base;                   // 编码基地址
    static int _shift;                      // 编码移位量
    static address _klass_range_start;      // Klass 范围起始
    static address _klass_range_end;        // Klass 范围结束
};
```

**22-bit + shift=10 的可寻址范围**：
- 最大可编码 Klass 数量：`2^22 = 4,194,304`（约 400 万个类）
- 最大 Klass Range：`2^22 << 10 = 2^32 = 4 GB`（因为 Klass 必须按 `1 << shift` 对齐）
- 当 shift=0 时：`2^22 = 4 MB` Klass Range（适合小型应用）

Klass 对齐要求：`max(8, 1 << shift)` 字节。COH 模式下 shift 可达 10，即 Klass 最小间隔 1KB。

### Klass Range 与 Encoding Range

```
// 文件: src/hotspot/share/oops/compressedKlass.hpp（注释）

CDS 启用, 128MB CDS + 1GB class space, base 指向 CDS 起始, shift=0:
  Encoding Range: [0x8_0000_0000 .. 0x9_0000_0000 ) (4 GB)
  Klass Range:    [0x8_0000_0000 .. 0x8_4800_0000 ) (128 MB + 1 GB)

  _base
 _klass_range_start                   _klass_range_end              encoding end
   |//////////|///////////////////////////|                               |
   |///CDS////|////1gb class space////////|        ...    ...             |
   |//////////|///////////////////////////|                               |
 0x8_0000_0000                      0x8_4800_0000                  0x9_0000_0000
```

### 编码范围的保护区

```cpp
// 文件: src/hotspot/share/oops/compressedKlass.hpp

// 是否在编码范围内
static inline bool is_encodable(const void* addr) {
    return (address)addr >= _klass_range_start && (address)addr < _klass_range_end &&
        is_aligned(addr, klass_alignment_in_bytes());
}
```

---

## 4. oopDesc：统一的对象头访问

### ObjLayout 模式分派

所有对象头操作通过 `ObjLayout::klass_mode()` 分派到正确的实现：

```cpp
// 文件: src/hotspot/share/oops/objLayout.hpp

class ObjLayout {
public:
  enum Mode {
    Compact,       // +UseCompactObjectHeaders (隐含 +UseCompressedClassPointers)
    Compressed,    // +UseCompressedClassPointers (-UseCompactObjectHeaders)
    Uncompressed,  // -UseCompressedClassPointers (-UseCompactObjectHeaders)
    Undefined      // 尚未初始化
  };

private:
  static Mode _klass_mode;
  static int  _oop_base_offset_in_bytes;  // 对象实例数据起始偏移
  static bool _oop_has_klass_gap;         // 是否有 klass gap 填充
};
```

### Klass 指针的三路获取

```cpp
// 文件: src/hotspot/share/oops/oop.inline.hpp

Klass* oopDesc::klass() const {
  switch (ObjLayout::klass_mode()) {
    case ObjLayout::Compact:
      return mark().klass();      // 从 mark word 高 22 位解码
    case ObjLayout::Compressed:
      return CompressedKlassPointers::decode_not_null(_metadata._compressed_klass);
    default:
      return _metadata._klass;    // 直接读取 8 字节指针
  }
}
```

### 对象头大小

```cpp
// 文件: src/hotspot/share/oops/oop.hpp

static int header_size() {
    if (UseCompactObjectHeaders) {
        return sizeof(markWord) / HeapWordSize;   // 8 / 8 = 1 word
    } else {
        return sizeof(oopDesc) / HeapWordSize;    // 16 / 8 = 2 words
    }
}
```

`oopDesc` 的内存布局：

```cpp
// 文件: src/hotspot/share/oops/oop.hpp

class oopDesc {
 private:
  volatile markWord _mark;        // 8 bytes —— 始终存在
  union _metadata {
    Klass*      _klass;           // 8 bytes —— 非压缩模式
    narrowKlass _compressed_klass; // 4 bytes —— 压缩模式
  } _metadata;                    // 仅在非 compact 模式使用
};
```

Compact 模式下，`_metadata` 字段不再被读写，klass 信息完全来自 `_mark`。

### Klass 指针偏移计算

```cpp
// 文件: src/hotspot/share/oops/oop.hpp

static int klass_offset_in_bytes() {
#ifdef _LP64
    if (UseCompactObjectHeaders) {
        // C2 编译器和 JVMCI 使用此偏移访问 mark word 中的 klass
        return mark_offset_in_bytes() + markWord::klass_offset_in_bytes;
        // = 0 + 4 = 4 （即 mark word 的第 4 字节处开始读取）
    } else
#endif
    {
        return (int)offset_of(oopDesc, _metadata._klass);
    }
}
```

这表明在 compact 模式下，C2 编译器可以通过从对象地址偏移 4 字节处加载 4 字节来直接获取 narrow klass，然后右移 `klass_shift_at_offset`（= 10）位得到 22-bit narrowKlass。

---

## 5. Prototype Header 与对象分配

### Klass 中的 Prototype Header

每个 Klass 预计算（pre-compute）一个包含自身 narrowKlass 编码的 prototype mark word：

```cpp
// 文件: src/hotspot/share/oops/klass.hpp

class Klass {
    markWord _prototype_header;  // 预计算的对象头模板
};

// 文件: src/hotspot/share/oops/klass.inline.hpp

inline markWord Klass::prototype_header() const {
    assert(UseCompactObjectHeaders, "only use with compact object headers");
    assert(_prototype_header.narrow_klass() > 0,
           "Klass " PTR_FORMAT ": invalid prototype (" PTR_FORMAT ")",
           p2i(this), _prototype_header.value());
    return _prototype_header;
}

inline void Klass::set_prototype_header(markWord header) {
    assert(UseCompactObjectHeaders, "only with compact headers");
    _prototype_header = header;
}
```

### 对象分配路径

```cpp
// 文件: src/hotspot/share/gc/shared/memAllocator.cpp

oop MemAllocator::finish(HeapWord* mem) const {
    assert(mem != nullptr, "null object pointer");
    if (UseCompactObjectHeaders) {
        // 紧凑头：用 Klass 的 prototype header 初始化 mark word
        // prototype header 已包含编码的 narrowKlass
        oopDesc::release_set_mark(mem, _klass->prototype_header());
    } else {
        // 传统：分别设置 mark word 和 klass 指针
        oopDesc::set_mark(mem, markWord::prototype());
        oopDesc::release_set_klass(mem, _klass);
    }
    // ...
}
```

compact 模式下对象分配更简单：**只需一次写操作**（写入 8 字节 mark word），而传统模式需要两次写操作（8 字节 mark word + 4/8 字节 klass pointer）。

### Prototype Mark 初始化

```cpp
// 文件: src/hotspot/share/oops/oop.inline.hpp

markWord oopDesc::prototype_mark() const {
    if (UseCompactObjectHeaders) {
        return klass()->prototype_header();  // 从 Klass 获取预计算的头
    } else {
        return markWord::prototype();        // 通用原型（hash=0, lock=unlocked）
    }
}

void oopDesc::init_mark() {
    set_mark(prototype_mark());
}
```

---

## 6. set_klass 的禁用

Compact 模式下，不能通过传统方式设置 klass 指针：

```cpp
// 文件: src/hotspot/share/oops/oop.inline.hpp

void oopDesc::set_klass(Klass* k) {
    assert(Universe::is_bootstrapping() || (k != nullptr && k->is_klass()), "incorrect Klass");
    assert(!UseCompactObjectHeaders, "don't set Klass* with compact headers");
    // compact 模式下此断言会失败 —— klass 信息只能通过 prototype_header 在分配时设置
    if (UseCompressedClassPointers) {
        _metadata._compressed_klass = CompressedKlassPointers::encode_not_null(k);
    } else {
        _metadata._klass = k;
    }
}
```

---

## 7. Identity Hash 处理

### 传统模式与紧凑模式的一致性

在两种模式下，identity hash 都存储在 mark word 的 bits [41:11]，为 31 位：

```cpp
// 文件: src/hotspot/share/oops/markWord.hpp

// 两种模式共享相同的哈希位定义
static const int hash_bits = max_hash_bits > 31 ? 31 : max_hash_bits;

// 哈希存取方法相同
intptr_t hash() const {
    return mask_bits(value() >> hash_shift, hash_mask);
}

markWord copy_set_hash(intptr_t hash) const {
    uintptr_t tmp = value() & (~hash_mask_in_place);
    tmp |= ((hash & hash_mask) << hash_shift);
    return markWord(tmp);
}
```

### 紧凑头的哈希设置特殊性

在传统模式下，设置 identity hash 时 mark word 的高位是 unused 的（无信息）。在紧凑头模式下，高 22 位存储 narrowKlass，`copy_set_hash()` 必须保留这些位不变。从代码可以看到 `copy_set_hash()` 使用掩码 `~hash_mask_in_place` 确保只修改 hash 位域，klass 位域不受影响。

### 锁定状态下的哈希与 Klass 访问

当对象被锁定（lock bits != unlocked）时：
- **stack-locking**: mark word 被替换为指向栈上 displaced header 的指针。displaced header 保留了原始的 hash 和 klass 信息。
- **UseObjectMonitorTable**: mark word 保留原值（header 位域不变），monitor 指针存储在外部表中。

```cpp
// 文件: src/hotspot/share/oops/markWord.hpp

bool has_displaced_mark_helper() const {
    intptr_t lockbits = value() & lock_mask_in_place;
    return !UseObjectMonitorTable && lockbits == monitor_value;
}
```

---

## 8. UseCompactObjectHeaders 与相关标志

### 标志定义

```cpp
// 文件: src/hotspot/share/runtime/globals.hpp

#ifdef _LP64
product(bool, UseCompactObjectHeaders, false,
        "Use compact 64-bit object headers in 64-bit VM")
#else
const bool UseCompactObjectHeaders = false;  // 32-bit VM 不支持
#endif
```

### 标志联动逻辑

`UseCompactObjectHeaders` 必须与 `UseCompressedClassPointers` 和 `UseObjectMonitorTable` 协同：

```cpp
// 文件: src/hotspot/share/runtime/arguments.cpp

void Arguments::set_compact_headers_flags() {
#ifdef _LP64
    // 1) COH 需要压缩类指针
    if (UseCompactObjectHeaders
        && FLAG_IS_CMDLINE(UseCompressedClassPointers)
        && !UseCompressedClassPointers) {
        warning("Compact object headers require compressed class pointers. "
                "Disabling compact object headers.");
        FLAG_SET_DEFAULT(UseCompactObjectHeaders, false);
    }

    // 2) COH 需要 UseObjectMonitorTable（因为锁不能替换 mark word 中的 klass）
    if (UseCompactObjectHeaders && !UseObjectMonitorTable) {
        if (FLAG_IS_CMDLINE(UseCompactObjectHeaders)) {
            FLAG_SET_DEFAULT(UseObjectMonitorTable, true);
        } else if (FLAG_IS_CMDLINE(UseObjectMonitorTable)) {
            FLAG_SET_DEFAULT(UseCompactObjectHeaders, false);
        } else {
            FLAG_SET_DEFAULT(UseObjectMonitorTable, true);
        }
    }

    // 3) COH 模式下强制启用压缩类指针
    if (UseCompactObjectHeaders && !UseCompressedClassPointers) {
        FLAG_SET_DEFAULT(UseCompressedClassPointers, true);
    }
#endif
}
```

**为什么必须使用 UseObjectMonitorTable?**

传统的 monitor 膨胀方式会将 mark word 替换为指向 ObjectMonitor 的指针，这会丢失编码在 mark word 中的 narrowKlass。使用 ObjectMonitorTable 将 monitor 指针存储在外部哈希表中，使 mark word 保持不变（或只修改 lock bits），从而保留 klass 信息。

---

## 9. GC 影响

### G1 GC：对象复制时的 Klass 获取

```cpp
// 文件: src/hotspot/share/gc/g1/g1ParScanThreadState.cpp

// 复制对象前获取 Klass（并发安全考虑）
assert(!old_mark.is_forwarded(), "precondition");
Klass* klass = UseCompactObjectHeaders
    ? old_mark.klass()   // compact: 从已加载的 mark word 提取（避免并发问题）
    : old->klass();      // 传统: 从 _metadata 字段读取
const size_t word_sz = old->size_given_klass(klass);
```

关键细节：在 G1 的并行扫描中，另一个 GC 线程可能已经转发了对象（设置了 forwarding pointer），此时 mark word 会变成转发指针。因此必须使用**之前已加载的 mark word**（`old_mark`）来提取 klass，而不是重新读取。

### ZGC：大数组的增量清零

```cpp
// 文件: src/hotspot/share/gc/z/zObjArrayAllocator.cpp
// ZGC 在分配大数组时需要处理 compact headers 的对象头大小差异
```

### Shenandoah GC：转发指针处理

```cpp
// 文件: src/hotspot/share/gc/shenandoah/shenandoahForwarding.inline.hpp
// Shenandoah 在转发对象时需要保留 mark word 中的 klass 信息
```

### GC 通用路径：对象大小计算

```cpp
// 文件: src/hotspot/share/oops/oop.inline.hpp

size_t oopDesc::size_given_klass(Klass* klass) {
    int lh = klass->layout_helper();
    size_t s;
    // layout_helper 在类加载时计算，已经考虑了 UseCompactObjectHeaders
    // 对于实例对象：lh 直接等于对象大小（以字节为单位，右移后得到 word 数）
    // compact 模式下，layout_helper 在 Klass 初始化时就减去了 klass pointer 的空间
    // ...
}
```

### 对象分配通用路径

```cpp
// 文件: src/hotspot/share/gc/shared/collectedHeap.cpp
// 所有 GC 的对象分配最终走 MemAllocator::finish()
// compact 模式下使用 prototype_header 一次性初始化
```

### Parallel GC：full GC 转发

```cpp
// 文件: src/hotspot/share/gc/shared/fullGCForwarding.cpp
// Full GC 的对象转发需要处理 compact headers 模式下 klass 信息的保留
```

---

## 10. 对 C2 编译器的影响

### Klass 指针访问路径

C2 编译器在生成代码时需要知道 klass 指针的位置：

```cpp
// 文件: src/hotspot/share/oops/oop.hpp

static int klass_offset_in_bytes() {
    if (UseCompactObjectHeaders) {
        // compact 模式：klass 在 mark word 内部，偏移 4 字节
        return mark_offset_in_bytes() + markWord::klass_offset_in_bytes;
        // = 0 + 4 = 4
    } else {
        return offset_of(oopDesc, _metadata._klass);  // = 8
    }
}
```

compact 模式下 C2 生成的代码从对象偏移 4 处加载 32-bit 值，然后根据 `klass_shift_at_offset`（= 10）右移得到 22-bit narrowKlass，再解码为 Klass*。

### GC Barrier 调整

```cpp
// 文件: src/hotspot/share/gc/shared/c2/barrierSetC2.cpp
// GC barrier 代码在 C2 中需要根据 UseCompactObjectHeaders 调整加载路径
```

---

## 11. 启用与配置

### JVM 参数

```bash
# 启用紧凑对象头（JDK 25 中默认关闭，实验性功能）
-XX:+UseCompactObjectHeaders

# 禁用（默认值）
-XX:-UseCompactObjectHeaders
```

启用 `+UseCompactObjectHeaders` 会自动启用：
- `+UseCompressedClassPointers`（强制）
- `+UseObjectMonitorTable`（自动）

### 诊断信息

```bash
# 打印压缩类指针编码信息
-Xlog:cds+init
```

```cpp
// 文件: src/hotspot/share/oops/compressedKlass.cpp

void CompressedKlassPointers::print_mode(outputStream* st) {
    st->print_cr("UseCompressedClassPointers %d, UseCompactObjectHeaders %d",
                 UseCompressedClassPointers, UseCompactObjectHeaders);
    // ... 打印 base, shift, range 等信息
}
```

### 平台限制

- **仅 64-bit**: 32-bit JVM 中 `UseCompactObjectHeaders` 为 compile-time 常量 `false`
- **CDS 兼容**: 编码参数在 CDS archive 创建时确定，运行时恢复
- **架构特定优化**: AArch64 有专用的 `check_klass_decode_mode()` 验证编码方案是否适合该平台的指令集

```cpp
// 文件: src/hotspot/share/oops/compressedKlass.hpp

#if defined(AARCH64) && !defined(ZERO)
  static bool check_klass_decode_mode(address base, int shift, const size_t range);
  static bool set_klass_decode_mode();
#else
  static bool check_klass_decode_mode(address base, int shift, const size_t range) { return true; }
  static bool set_klass_decode_mode() { return true; }
#endif
```

---

## 12. 实际影响与注意事项

### 内存节省的实际观测

典型 Java 应用中，小对象（wrapper, node, entry 等）占多数。由于每个对象节省 4-8 字节的头开销，整体堆内存使用通常可减少 10-20%。对于小对象密集的应用（如图数据结构、大量 HashMap 条目），节省更为显著。

### 性能特性

1. **对象分配更快**: compact 模式只需一次 8 字节写入（`release_set_mark`），传统模式需要两次写入
2. **Klass 读取略慢**: 需要从 mark word 提取并解码 narrowKlass，比直接读取 `_metadata._klass` 多几条指令
3. **GC 受益**: 堆更小意味着更少的 GC 压力，年轻代和老年代 GC 暂停时间均有改善
4. **缓存友好**: 更小的对象头意味着更高的 CPU 缓存利用率

### 兼容性考虑

- **JVMTI 和 SA**: 调试工具需要理解新的对象头布局
- **序列化框架**: 使用 Unsafe 直接访问对象内存的框架可能受影响
- **JNI**: 通过 JNI 访问对象头的代码需要更新
- **锁实现**: 必须使用 ObjectMonitorTable 而非传统的 displaced header 方式

---

## 13. 源码文件索引

| 文件路径 | 内容 |
|---------|------|
| `src/hotspot/share/oops/markWord.hpp` | mark word 位字段定义、锁状态、hash/age 访问 |
| `src/hotspot/share/oops/markWord.inline.hpp` | narrow_klass/klass 的提取与设置 |
| `src/hotspot/share/oops/compressedKlass.hpp` | CompressedKlassPointers 类定义、编码参数 |
| `src/hotspot/share/oops/compressedKlass.inline.hpp` | encode/decode 实现 |
| `src/hotspot/share/oops/oop.hpp` | oopDesc 对象头结构、header_size() |
| `src/hotspot/share/oops/oop.inline.hpp` | klass() 三路分派、set_klass 禁用断言 |
| `src/hotspot/share/oops/objLayout.hpp` | ObjLayout::Mode 枚举 |
| `src/hotspot/share/oops/klass.inline.hpp` | prototype_header() 实现 |
| `src/hotspot/share/gc/shared/memAllocator.cpp` | 对象分配初始化路径 |
| `src/hotspot/share/runtime/globals.hpp` | UseCompactObjectHeaders 标志定义 |
| `src/hotspot/share/runtime/arguments.cpp` | 标志联动逻辑 |
| `src/hotspot/share/gc/g1/g1ParScanThreadState.cpp` | G1 GC klass 获取适配 |

---

## 14. 相关链接

- [JEP 519: Compact Object Headers](/jeps/gc/jep-519.md)
- [源码浏览](https://github.com/openjdk/jdk/tree/master/src/hotspot/share/oops)
