# Yang Yi

> Metaspace 和文件流修复专家，阿里巴巴

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Yang Yi |
| **当前组织** | 阿里巴巴 (Alibaba) |
| **邮箱** | qingfeng.yy@alibaba-inc.com |
| **Commits** | 2 |
| **主要领域** | Metaspace, 文件操作 |
| **活跃时间** | 2020 |

---

## 贡献列表

| Issue | 标题 | 说明 |
|-------|------|------|
| 8262099 | jcmd VM.metaspace should report unlimited size if MaxMetaspaceSize isn't specified | 功能修复 |
| 8261949 | fileStream::readln returns incorrect line string | **正确性修复** |

---

## 关键贡献

### Metaspace 无限制大小报告修复 (JDK-8262099)

**问题**: 当 `MaxMetaspaceSize` 未设置时，`jcmd VM.metaspace` 显示错误的大小值。

**解决方案**: 正确处理无限制情况：

```cpp
// 变更前: 显示 0 或错误值
output->print_cr("MaxMetaspaceSize: " SIZE_FORMAT, MaxMetaspaceSize);

// 变更后: 显示 "unlimited"
if (MaxMetaspaceSize == max_uintx) {
  output->print_cr("MaxMetaspaceSize: unlimited");
} else {
  output->print_cr("MaxMetaspaceSize: " SIZE_FORMAT, MaxMetaspaceSize);
}
```

**影响**: 用户可以正确了解 Metaspace 的限制设置。

### fileStream::readln 修复 (JDK-8261949)

**问题**: `fileStream::readln` 返回不正确的行字符串。

**解决方案**: 修复行读取逻辑：

```cpp
// 变更前: 行尾处理错误
while ((c = fgetc(_file)) != EOF && c != '\n') {
  buf[i++] = c;
}

// 变更后: 正确处理各种行尾
while ((c = fgetc(_file)) != EOF) {
  if (c == '\n' || c == '\r') {
    break;
  }
  buf[i++] = c;
}
```

**影响**: 文件读取操作返回正确的行内容。

---

## 相关链接

- [JBS Issues](https://bugs.openjdk.org/issues/?jql=reporter%20%3D%20qingfeng.yy)