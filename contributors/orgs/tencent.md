# 腾讯

> G1 GC 优化和容器支持

---

## 概览

腾讯参与 OpenJDK 开发，专注于 G1 GC 优化、容器资源检测和编译器修复。

| 指标 | 值 |
|------|-----|
| **总 Commits** | 44 |
| **贡献者数** | 13 |
| **主要领域** | G1 GC、容器、编译器 |

---

## 影响的模块分布

基于 git 修改文件统计：

| 模块 | 文件数 | 说明 |
|------|--------|------|
| C2 编译器 | 9 | 服务端编译器 |
| G1 GC | 9 | G1 垃圾收集器 |
| 解释器 | 5 | 字节码解释器 |
| 容器测试 | 4 | Docker 容器测试 |
| Linux 平台 | 4 | Linux 操作系统支持 |
| 工具类 | 3 | HotSpot 工具 |
| Epsilon GC | 3 | 无操作 GC |

---

## Top 贡献者

| 排名 | 贡献者 | Commits | 领域 |
|------|--------|---------|------|
| 1 | Bob Peng Xie | 15 | 测试、构建 |
| 2 | Caspar Wang | 7 | 测试 |
| 3 | [Tongbao Zhang](../tongbao-zhang.md) | 5 | G1 GC |
| 4 | Emory Zheng | 4 | 测试 |
| 5 | Lin Zang | 2 | 测试 |
| 6 | Lehua Ding | 2 | 编译器 |
| 7 | Junji Wang | 2 | 测试 |
| 8 | Buddy Liao | 2 | 测试 |

---

## 关键贡献

### G1 GC 优化

| Issue | 标题 | 说明 |
|-------|------|------|
| 8354145 | G1 压缩指针边界计算修复 | **重要修复** - 使用最大堆区大小而非最大人体工程学堆区大小 |
| 8287771 | 移除无用的 G1 After GC summary refinement | 代码清理 |
| 8274259 | G1 assert check_alignment 失败修复 | 正确性修复 |

**G1 压缩指针边界问题**:
- 问题：UseCompressedOops 边界计算错误
- 影响：可能导致大堆内存场景下的崩溃
- 修复：使用正确的堆区大小计算边界

### 容器支持

| Issue | 标题 | 说明 |
|-------|------|------|
| 8293472 | 手动 cgroup fs 挂载导致容器资源检测错误 | **重要修复** |
| 8284950 | CgroupV1 应考虑 memory.swappiness | 内存限制检测 |
| 8283903 | GetContainerCpuLoad 在 share 模式下返回错误结果 | CPU 负载检测 |

**容器资源检测问题**:
- 问题：手动挂载 cgroup 文件系统导致资源限制检测失败
- 影响：Kubernetes 环境下 JVM 无法正确识别容器资源
- 修复：改进 cgroup 检测逻辑

### 编译器修复

| Issue | 标题 | 说明 |
|-------|------|------|
| 8293978 | 重复简单循环回边导致 VM 崩溃 | **崩溃修复** |
| 8275854 | C2 assert(stride_con != 0) 失败 | 正确性修复 |
| 8293782 | Shenandoah 锁排名检查测试失败 | 测试修复 |

### 构建修复

| Issue | 标题 | 说明 |
|-------|------|------|
| 8322513 | minimal 构建失败 | 构建修复 |
| 8314688 | 无 C1 构建失败 | 构建修复 |
| 8308283 | GCC12 & GCC13 构建失败 | 编译器兼容 |

---

## 技术特点

### 云原生支持

腾讯的贡献聚焦云原生场景：
- 容器资源检测修复
- Kubernetes 环境适配
- cgroup v1/v2 兼容

### GC 稳定性

- G1 GC 正确性修复
- 大堆内存场景支持
- 压缩指针边界修复

---

## 数据来源

- **统计方法**: `git log upstream_master --author="tencent"`
- **模块分析**: 基于修改文件路径统计
- **贡献者**: 13 位腾讯员工

---

## 相关链接

- [腾讯云 Java](https://cloud.tencent.com/product/tke)
- [Tencent Kona JDK](https://github.com/Tencent/TencentKona-8)