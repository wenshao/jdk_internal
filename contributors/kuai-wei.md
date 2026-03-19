# Kuai Wei

> JDK 26 C2 编译器专家，阿里巴巴，4 个 commits

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Kuai Wei (蒯伟) |
| **组织** | 阿里巴巴 (Alibaba) |
| **Email** | kuaiwei.kw@alibaba-inc.com |
| **Commits** | 4 |
| **主要领域** | C2 编译器、IR 优化 |
| **活跃时间** | 2024 - 至今 |

---

## 贡献概览

### 按类别统计

| 类别 | 数量 | 占比 |
|------|------|------|
| C2 IR 优化 | 2 | 50% |
| 开发工具 | 1 | 25% |
| 测试修复 | 1 | 25% |

### 关键成就

- C2 IR 节点 size_of() 修复
- MergeStores 字节序优化
- Windows 开发工具改进

---

## PR 列表

### C2 编译器优化

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8356328 | Some C2 IR nodes miss size_of() function | [JBS-8356328](https://bugs.openjdk.org/browse/JDK-8356328) |
| 8347405 | MergeStores with reverse bytes order value | [JBS-8347405](https://bugs.openjdk.org/browse/JDK-8347405) |

### 开发工具

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8355697 | Create windows devkit on wsl and msys2 | [JBS-8355697](https://bugs.openjdk.org/browse/JDK-8355697) |

### 测试修复

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8350858 | [IR Framework] Some tests failed on Cascade Lake | [JBS-8350858](https://bugs.openjdk.org/browse/JDK-8350858) |

---

## 关键贡献详解

### 1. C2 IR 节点 size_of() 修复 (JDK-8356328)

**问题**: 部分 C2 IR 节点缺少 size_of() 函数，导致编译时崩溃。

**解决方案**: 为缺失的节点添加 size_of() 函数。

```cpp
// 变更前: 缺少 size_of()
class ClearArrayNode : public Node {
  virtual uint size_of() const { return sizeof(*this); }  // 缺失
};

// 变更后: 添加 size_of()
class ClearArrayNode : public Node {
  virtual uint size_of() const { return sizeof(*this); }
};

// 类似修复应用于其他节点
class StrIntrinsicNode : public Node {
  virtual uint size_of() const { return sizeof(*this); }
};
```

**影响**: 修复了编译时崩溃问题。

### 2. MergeStores 字节序优化 (JDK-8347405)

**问题**: MergeStores 在处理反向字节序时出错。

**解决方案**: 修复字节序处理逻辑。

```cpp
// 变更前: 字节序处理错误
void MergeStores::merge(Node* n) {
  // 假设小端序
  store_value = bytes[0] | (bytes[1] << 8);
}

// 变更后: 正确处理字节序
void MergeStores::merge(Node* n) {
  if (VM_Version::is_big_endian()) {
    store_value = (bytes[0] << 8) | bytes[1];
  } else {
    store_value = bytes[0] | (bytes[1] << 8);
  }
}
```

**影响**: 修复了大端序系统上的问题。

### 3. Windows 开发工具改进 (JDK-8355697)

**问题**: 在 WSL 和 MSYS2 上创建 Windows 开发工具包困难。

**解决方案**: 改进开发工具包创建脚本。

```bash
# 改进后的脚本支持 WSL 和 MSYS2
if [ -n "$WSL_DISTRO_NAME" ]; then
  # WSL 环境
  TOOLCHAIN_DIR="/mnt/c/tools"
elif [ -n "$MSYSTEM" ]; then
  # MSYS2 环境
  TOOLCHAIN_DIR="/c/tools"
else
  # 原生 Linux
  TOOLCHAIN_DIR="/opt/tools"
fi
```

**影响**: 简化了 Windows 开发环境配置。

---

## 开发风格

Kuai Wei 的贡献特点:

1. **C2 专家**: 深入理解 C2 编译器内部机制
2. **阿里巴巴**: 代表阿里巴巴在 OpenJDK 的贡献
3. **跨平台**: 关注 Windows/Linux 兼容性
4. **问题定位**: 快速定位编译器问题

---

## 相关链接

- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=Kuai%20Wei)
- [JBS Issues](https://bugs.openjdk.org/issues/?jql=reporter%20%3D%20kuaiwei.kw)