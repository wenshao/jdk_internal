# Anjian-Wen

> JDK 26 RISC-V 向量指令专家，字节跳动，12 个 commits

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Anjian-Wen |
| **组织** | 字节跳动 (ByteDance) |
| **GitHub** | [@Anjian-Wen](https://github.com/Anjian-Wen) |
| **OpenJDK** | Author |
| **PRs** | [25 integrated](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3AAnjian-Wen+is%3Aclosed+label%3Aintegrated) |
| **主要领域** | RISC-V 向量指令、Zvbb、Zfa |
| **活跃时间** | 2024 - 至今 |

---

## 贡献概览

### 按类别统计

| 类别 | 数量 | 占比 |
|------|------|------|
| RISC-V 向量指令 | 8 | 67% |
| RISC-V 浮点指令 | 2 | 17% |
| RISC-V intrinsic | 2 | 16% |

### 关键成就

- RISC-V Zvbb 向量指令支持
- RISC-V Zfa 浮点指令支持
- RISC-V 数组填充优化

---

## PR 列表

### RISC-V Zvbb 向量指令

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8329887 | RISC-V: C2: Support Zvbb Vector And-Not instruction | [JBS-8329887](https://bugs.openjdk.org/browse/JDK-8329887) |
| 8355074 | RISC-V: C2: Support Vector-Scalar version of Zvbb Vector And-Not instruction | [JBS-8355074](https://bugs.openjdk.org/browse/JDK-8355074) |
| 8355562 | RISC-V: Cleanup names of vector-scalar instructions in riscv_v.ad | [JBS-8355562](https://bugs.openjdk.org/browse/JDK-8355562) |
| 8355657 | RISC-V: Improve PrintOptoAssembly output of vector-scalar instructions | [JBS-8355657](https://bugs.openjdk.org/browse/JDK-8355657) |
| 8355796 | RISC-V: compiler/vectorapi/AllBitsSetVectorMatchRuleTest.java fails after JDK-8355657 | [JBS-8355796](https://bugs.openjdk.org/browse/JDK-8355796) |

### RISC-V Zfa 浮点指令

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8349632 | RISC-V: Add Zfa fminm/fmaxm | [JBS-8349632](https://bugs.openjdk.org/browse/JDK-8349632) |
| 8352022 | RISC-V: Support Zfa fminm_h/fmaxm_h for float16 | [JBS-8352022](https://bugs.openjdk.org/browse/JDK-8352022) |

### RISC-V 数组填充优化

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8351140 | RISC-V: Intrinsify Unsafe::setMemory | [JBS-8351140](https://bugs.openjdk.org/browse/JDK-8351140) |
| 8356869 | RISC-V: Improve tail handling of array fill stub | [JBS-8356869](https://bugs.openjdk.org/browse/JDK-8356869) |
| 8356700 | RISC-V: Declare incompressible scope in fill_words / zero_memory assembler routines | [JBS-8356700](https://bugs.openjdk.org/browse/JDK-8356700) |
| 8356593 | RISC-V: Small improvement to array fill stub | [JBS-8356593](https://bugs.openjdk.org/browse/JDK-8356593) |
| 8354815 | RISC-V: Change type of bitwise rotation shift to iRegIorL2I | [JBS-8354815](https://bugs.openjdk.org/browse/JDK-8354815) |

---

## 关键贡献详解

### 1. RISC-V Zvbb 向量 And-Not 指令 (JDK-8329887)

**背景**: Zvbb 是 RISC-V 的向量位操作扩展。

**解决方案**: 添加 Zvbb Vector And-Not 指令支持。

```cpp
// 新增指令匹配
instruct vandn_vecI(vecI dst, vecI src1, vecI src2) %{
  predicate(UseZvbb);
  match(Set dst (AndV src1 (XorV src2 (ReplicateBMinus1 src2))));
  ins_cost(INSN_COST);
  format %{ "vandn.vv  $dst, $src1, $src2\t# vector and-not" %}
  ins_encode %{
    __ vandn_vv($dst$$VectorRegister, $src1$$VectorRegister, $src2$$VectorRegister);
  %}
%}
```

**影响**: 提升了位操作性能。

### 2. RISC-V Zfa 浮点 Min/Max 指令 (JDK-8349632)

**背景**: Zfa 是 RISC-V 的附加浮点扩展。

**解决方案**: 添加 Zfa fminm/fmaxm 指令支持。

```cpp
// 新增指令匹配
instruct minF_reg_reg(fRegF dst, fRegF src1, fRegF src2) %{
  predicate(UseZfa);
  match(Set dst (MinF src1 src2));
  ins_cost(INSN_COST);
  format %{ "fminm.s  $dst, $src1, $src2\t# float min" %}
  ins_encode %{
    __ fminm_s($dst$$FloatRegister, $src1$$FloatRegister, $src2$$FloatRegister);
  %}
%}
```

**影响**: 提升了浮点 Min/Max 性能。

### 3. RISC-V Unsafe.setMemory Intrinsic (JDK-8351140)

**问题**: Unsafe.setMemory 在 RISC-V 上没有 intrinsic 实现。

**解决方案**: 添加 intrinsic 实现。

```cpp
// RISC-V setMemory intrinsic
void LIR_Assembler::emit_setmem(CodeBuffer* cb, LIR_Opr src, LIR_Opr cnt, LIR_Opr tmp) {
  Register src_reg = src->as_register();
  Register cnt_reg = cnt->as_register();
  
  // 使用向量指令填充
  if (UseRVV && cnt_reg > 32) {
    __ vsetvli(t0, cnt_reg, Assembler::e8, Assembler::m1);
    __ vmv_v_i(v0, 0);
    __ vse8_v(v0, src_reg);
  } else {
    __ sd(zr, Address(src_reg));
    __ addi(src_reg, src_reg, 8);
    __ addi(cnt_reg, cnt_reg, -8);
  }
}
```

**影响**: 提升了内存填充性能。

---

## 开发风格

Anjian-Wen 的贡献特点:

1. **RISC-V 专家**: 深入理解 RISC-V 向量和浮点扩展
2. **字节跳动**: 代表中国企业在 OpenJDK 的贡献
3. **指令优化**: 专注于新指令支持
4. **测试驱动**: 每个改动都有充分的测试

---

## 相关链接

- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=Anjian-Wen)
- [JBS Issues](https://bugs.openjdk.org/issues/?jql=reporter%20%3D%20Anjian-Wen)