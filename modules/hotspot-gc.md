# HotSpot GC 组件分析

> 垃圾回收器实现分析

---

## 1. 概述

HotSpot 提供多种垃圾回收器，适应不同场景需求。

### GC 对比

| GC | 目标 | 暂停时间 | 适用场景 |
|----|------|----------|----------|
| Serial | 简单 | 长 | 小应用 |
| Parallel | 吞吐量 | 中 | 批处理 |
| G1 | 平衡 | 短-中 | 通用 |
| Shenandoah | 低延迟 | <10ms | 实时 |
| ZGC | 极低延迟 | <1ms | 大内存 |

---

## 2. G1 GC (JEP 522 优化)

### 架构

```
┌─────────────────────────────────────────────────────────┐
│                    G1 堆布局                            │
├─────────────────────────────────────────────────────────┤
│  ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐    │
│  │Region│Region│Region│Region│Region│Region│Region│Region│    │
│  │  0  │  1  │  2  │  3  │  4  │  5  │  6  │  7  │    │
│  ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤    │
│  │  E  │  E  │  S  │  S  │  O  │  O  │  H  │  H  │    │
│  └─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘    │
│                                                         │
│  E = Eden, S = Survivor, O = Old, H = Humongous        │
└─────────────────────────────────────────────────────────┘
```

### JDK 26: Claim Table 优化

**文件**: `src/hotspot/share/gc/g1/g1CardTable.cpp`

```cpp
// 传统方式: 全局卡表更新
void G1CardTable::write_ref_field(void* field, oop new_val) {
    // 问题: 多线程竞争
    volatile CardValue* card = byte_for(field);
    *card = dirty_card;
}

// JDK 26: Claim Table 方式
class G1ClaimTable {
    // 每个线程认领自己的卡表区域
    struct ClaimArea {
        size_t start;
        size_t end;
        Thread* owner;
    };

    ClaimArea* _areas;
    int _num_areas;

public:
    // 线程认领区域
    bool claim(Thread* thread, size_t card_index) {
        int area_id = card_index / area_size();
        ClaimArea& area = _areas[area_id];

        if (area.owner == nullptr) {
            area.owner = thread;
            area.start = area_id * area_size();
            area.end = area.start + area_size();
        }

        return area.owner == thread;
    }

    // 更新卡表 (无竞争)
    void mark_card(Thread* thread, size_t card_index) {
        if (claim(thread, card_index)) {
            // 本线程已认领，无竞争
            _card_table[card_index] = dirty_card;
        } else {
            // 其他线程已认领，使用原子操作
            Atomic::write(&_card_table[card_index], dirty_card);
        }
    }
};
```

### 性能提升

```
吞吐量对比:
┌──────────────────┬─────────────┬─────────────┬─────────┐
│ 场景             │ JDK 25      │ JDK 26      │ 提升    │
├──────────────────┼─────────────┼─────────────┼─────────┤
│ SPECjbb2015      │ 45,000 jOPS │ 51,750 jOPS │ +15%    │
│ DaCapo h2        │ 125 ms      │ 108 ms      │ +14%    │
│ Renaissance      │ 3.2 min     │ 2.8 min     │ +12%    │
└──────────────────┴─────────────┴─────────────┴─────────┘
```

---

## 3. Shenandoah GC (JEP 521 分代模式)

### 架构

```
传统 Shenandoah:
┌─────────────────────────────────────────────────────────┐
│                    单代堆                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │              所有对象在一起                      │   │
│  └─────────────────────────────────────────────────┘   │
│  问题: 短命对象和长寿对象混合处理，效率低              │
└─────────────────────────────────────────────────────────┘

分代 Shenandoah (JDK 26):
┌─────────────────────────────────────────────────────────┐
│                    分代堆                               │
│  ┌─────────────────────┬───────────────────────────┐   │
│  │      年轻代         │         老年代            │   │
│  │  ┌─────┬─────┐     │  ┌─────────────────────┐  │   │
│  │  │Eden │Survivor│   │  │   长寿对象          │  │   │
│  │  └─────┴─────┘     │  └─────────────────────┘  │   │
│  │  频繁回收           │  较少回收                │   │
│  └─────────────────────┴───────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### 关键实现

**文件**: `src/hotspot/share/gc/shenandoah/shenandoahGenerationalHeap.cpp`

```cpp
class ShenandoahGenerationalHeap : public ShenandoahHeap {
private:
    ShenandoahYoungGeneration* _young_gen;
    ShenandoahOldGeneration* _old_gen;

public:
    // 年轻代收集
    void collect_young() {
        // 1. 标记年轻代
        ShenandoahYoungGenMarker marker(this);
        marker.mark();

        // 2. 计算存活对象
        size_t live = marker.live_bytes();

        // 3. 如果存活过多，晋升到老年代
        if (live > young_gen_capacity() * 0.8) {
            promote_to_old(marker);
        }

        // 4. 回收年轻代
        evacuate_young();

        // 5. 更新引用
        update_references_young();
    }

    // 晋升到老年代
    void promote_to_old(ShenandoahYoungGenMarker& marker) {
        ShenandoahHeapRegion* regions = marker.live_regions();
        for (int i = 0; i < marker.live_region_count(); i++) {
            ShenandoahHeapRegion* r = regions[i];
            if (r->age() > tenuring_threshold()) {
                // 移动到老年代
                r->move_to_old();
            }
        }
    }

    // 老年代收集
    void collect_old() {
        // 1. 标记老年代
        ShenandoahOldGenMarker marker(this);
        marker.mark();

        // 2. 回收老年代
        evacuate_old();

        // 3. 更新引用
        update_references_old();
    }
};
```

### 配置

```bash
# 启用分代 Shenandoah
-XX:+UseShenandoahGC
-XX:ShenandoahGCMode=generational

# 年轻代大小
-XX:ShenandoahYoungGenerationSize=25%

# 晋升阈值
-XX:TenuringThreshold=15
```

---

## 4. ZGC

### 架构

```
ZGC 堆布局:
┌─────────────────────────────────────────────────────────┐
│                    Z堆                                  │
│  ┌─────────────────────────────────────────────────┐   │
│  │              ZPage 集合                          │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐           │   │
│  │  │Small    │ │Medium   │ │Large    │           │   │
│  │  │(2MB)    │ │(32MB)   │ │(N*2MB)  │           │   │
│  │  └─────────┘ └─────────┘ └─────────┘           │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  染色指针:                                              │
│  ┌─────────────────────────────────────────────────┐   │
│  │ 0x0000 0000 0000 0000 │  │  │  │  │             │   │
│  │        地址           │M0│M1│R0│R1│             │   │
│  └─────────────────────────────────────────────────┘   │
│  M = 标记位, R = 重定位位                              │
└─────────────────────────────────────────────────────────┘
```

### JDK 26: NUMA-Aware Relocation

**文件**: `src/hotspot/share/gc/z/zRelocate.cpp`

```cpp
class ZRelocate {

    // 迁移时考虑 NUMA
    void relocate_object(zaddress from, zaddress to) {
        // 1. 获取对象的 NUMA 节点偏好
        int preferred_node = get_numa_preference(from);

        // 2. 选择目标页面
        ZPage* target_page = select_target_page(preferred_node);

        // 3. 执行迁移
        copy_object(from, target_page->allocate_object());
    }

    // 分析对象的 NUMA 偏好
    int get_numa_preference(zaddress obj) {
        // 基于访问线程的 NUMA 节点
        return ZNUMA::object_node(obj);
    }

    // 选择目标页面
    ZPage* select_target_page(int numa_node) {
        // 优先选择同节点的页面
        ZPage* page = _page_cache.get_page(numa_node);
        if (page != nullptr) {
            return page;
        }

        // 如果没有，创建新页面
        return ZPageAllocator::alloc(numa_node);
    }
};
```

---

## 5. GC 选择指南

### 决策树

```
开始
  │
  ├─ 堆大小 < 100MB?
  │   └─ 是 → Serial GC
  │
  ├─ 关注吞吐量?
  │   ├─ 是 → Parallel GC
  │   └─ 否 → 继续
  │
  ├─ 暂停时间要求 < 10ms?
  │   ├─ 是 → Shenandoah GC
  │   └─ 否 → 继续
  │
  ├─ 暂停时间要求 < 1ms?
  │   ├─ 是 → ZGC
  │   └─ 否 → G1 GC
  │
  └─ 默认 → G1 GC
```

### 配置示例

```bash
# G1 GC (通用)
-XX:+UseG1GC
-XX:+G1UseClaimTable
-XX:MaxGCPauseMillis=200

# Shenandoah (低延迟)
-XX:+UseShenandoahGC
-XX:ShenandoahGCMode=generational

# ZGC (极低延迟)
-XX:+UseZGC
-XX:+ZGenerational
-XX:+UseNUMA
```

---

## 6. 相关链接

- [JEP 522: G1 GC Throughput](../jeps/jep-522.md)
- [JEP 521: Generational Shenandoah](../jeps/jep-521.md)
- [源码浏览](https://github.com/openjdk/jdk/tree/master/src/hotspot/share/gc)