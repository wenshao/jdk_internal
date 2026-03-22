#!/usr/bin/env python3
"""
自动修复 by-version/*/README.md 中缺失的 JEP 本地链接。

对于每个提到 JEP NNN 但未链接到本地 jeps/ 文件的引用，
如果本地文件存在，则自动添加链接。

用法:
  python3 scripts/fix-jep-links.py          # 预览变更
  python3 scripts/fix-jep-links.py --fix    # 实际修改文件
"""

import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def find_jep_file(num: str) -> str | None:
    """查找 JEP 编号对应的本地文件路径"""
    jeps_dir = REPO_ROOT / "jeps"
    for f in jeps_dir.rglob(f"jep-{num}.md"):
        # 返回相对于 repo root 的路径，以 / 开头
        return "/" + str(f.relative_to(REPO_ROOT))
    return None


def fix_file(filepath: Path, dry_run: bool) -> int:
    """修复单个文件中的 JEP 链接，返回修复数"""
    content = filepath.read_text(encoding="utf-8")
    fixes = 0

    # 模式 1: | JEP NNN | (表格中的纯文本 JEP)
    # 匹配 "| JEP 507 |" 但不匹配 "| [JEP 507](...) |"
    def replace_table_jep(m):
        nonlocal fixes
        num = m.group(1)
        local = find_jep_file(num)
        if local:
            fixes += 1
            return f"| [JEP {num}]({local}) "
        return m.group(0)

    content = re.sub(
        r'\| JEP (\d{3,4}) ',
        replace_table_jep,
        content,
    )

    # 模式 2: [JEP NNN](https://openjdk.org/jeps/NNN) → 替换为本地链接
    def replace_external_jep(m):
        nonlocal fixes
        num = m.group(1)
        local = find_jep_file(num)
        if local:
            fixes += 1
            return f"[JEP {num}]({local})"
        return m.group(0)

    content = re.sub(
        r'\[JEP (\d{3,4})\]\(https://openjdk\.org/jeps/\d+\)',
        replace_external_jep,
        content,
    )

    if fixes > 0:
        rel = filepath.relative_to(REPO_ROOT)
        if dry_run:
            print(f"  {rel}: {fixes} fix(es) (dry run)")
        else:
            filepath.write_text(content, encoding="utf-8")
            print(f"  {rel}: {fixes} fix(es) applied")

    return fixes


def main():
    dry_run = "--fix" not in sys.argv
    if dry_run:
        print("DRY RUN — pass --fix to apply changes\n")

    total = 0
    files_changed = 0

    for index_file in sorted((REPO_ROOT / "by-version").rglob("README.md")):
        n = fix_file(index_file, dry_run)
        if n > 0:
            total += n
            files_changed += 1

    print(f"\nTotal: {total} fix(es) in {files_changed} file(s)")
    if dry_run and total > 0:
        print("Run with --fix to apply.")


if __name__ == "__main__":
    main()
