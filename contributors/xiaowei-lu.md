# Xiaowei Lu

> ZGC 优化贡献者，阿里巴巴

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Xiaowei Lu |
| **当前组织** | 阿里巴巴 (Alibaba) |
| **GitHub** | [@weixlu](https://github.com/weixlu) |
| **Integrated PRs** | [3](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Aweixlu+is%3Aclosed+label%3Aintegrated) |
| **主要领域** | ZGC |
| **活跃时间** | 2021 |

---

## PR 列表

| Issue | 标题 | 合入时间 |
|-------|------|----------|
| 8273112 | -Xloggc:<filename> should override -verbose:gc | 2021-04 |
| 8272138 | ZGC: Adopt relaxed ordering for self-healing | 2021-03 |
| 8270347 | ZGC: Adopt release-acquire ordering for forwarding table | 2021-02 |

---

## 关键贡献

### ZGC 自愈宽松顺序优化 (JDK-8272138)

**问题**: ZGC 自愈操作使用过于严格的内存顺序，影响性能。

**解决方案**: 使用宽松的内存顺序：

```cpp
// 变更前: 使用强顺序
oop result = Atomic::cmpxchg(addr, expected, new_value);

// 变更后: 使用宽松顺序
oop result = Atomic::cmpxchg_relaxed(addr, expected, new_value);
```

**影响**: 提升 ZGC 自愈操作性能。

### ZGC 转发表访问顺序修复 (JDK-8270347)

**问题**: ZGC 转发表访问需要正确的内存顺序保证。

**解决方案**: 使用 release-acquire 顺序：

```cpp
// 变更后: 使用 release-acquire 顺序
ZForwardingEntry* entry = forwarding->find(addr);
if (entry != nullptr) {
  return Atomic::load_acquire(&entry->to());
}
```

**影响**: 确保 ZGC 在弱内存模型平台上的正确性。

### GC 日志覆盖修复 (JDK-8273112)

**问题**: `-Xloggc:<filename>` 不能正确覆盖 `-verbose:gc`。

**解决方案**: 修复日志选项优先级：

```cpp
// 变更后: -Xloggc 优先级高于 -verbose:gc
if (Arguments::has_xloggc()) {
  // 使用 -Xloggc 指定的文件
  gclog_file = new fileStream(Arguments::xloggc_file());
}
```

**影响**: 用户可以正确使用 `-Xloggc` 覆盖默认日志设置。

---

## 数据来源

- **统计方法**: GitHub PR search `repo:openjdk/jdk author:weixlu type:pr label:integrated`
- **统计时间**: 2026-03-19

---

## 相关链接

- [GitHub Profile](https://github.com/weixlu)
- [OpenJDK PRs](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Aweixlu)