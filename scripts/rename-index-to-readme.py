#!/usr/bin/env python3
"""
将所有 index.md 重命名为 README.md，并更新全仓引用。

GitHub 只自动渲染 README.md，不渲染 index.md。

用法:
  python3 scripts/rename-index-to-readme.py          # 预览
  python3 scripts/rename-index-to-readme.py --fix    # 执行
"""

import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def main():
    dry_run = "--fix" not in sys.argv
    if dry_run:
        print("DRY RUN — pass --fix to apply\n")

    # Phase 1: 收集所有需要重命名的 index.md
    renames = []
    for index_file in sorted(REPO_ROOT.rglob("index.md")):
        if ".git" in str(index_file):
            continue
        # 跳过根目录（如果有）
        rel = index_file.relative_to(REPO_ROOT)
        d = index_file.parent
        readme = d / "README.md"

        if readme.exists():
            # 冲突：index.md 和 README.md 都存在
            # index.md 通常更丰富，覆盖 README.md
            idx_size = index_file.stat().st_size
            rdm_size = readme.stat().st_size
            if idx_size >= rdm_size:
                renames.append((index_file, readme, "overwrite"))
                print(f"  OVERWRITE: {rel} ({idx_size}B) → README.md ({rdm_size}B)")
            else:
                # README.md 更大，删除 index.md
                renames.append((index_file, readme, "delete"))
                print(f"  DELETE: {rel} ({idx_size}B), keep README.md ({rdm_size}B)")
        else:
            renames.append((index_file, readme, "rename"))
            print(f"  RENAME: {rel} → README.md")

    print(f"\n{len(renames)} file(s) to process")

    # Phase 2: 执行重命名
    if not dry_run:
        for src, dst, action in renames:
            if action == "overwrite":
                dst.unlink()
                src.rename(dst)
            elif action == "delete":
                src.unlink()
            else:
                src.rename(dst)
        print("Renames complete.\n")

    # Phase 3: 更新所有引用
    # 在所有 .md 文件中替换 index.md → README.md
    ref_fixes = 0
    md_files = [f for f in REPO_ROOT.rglob("*.md") if ".git" not in str(f)]

    for md in md_files:
        try:
            content = md.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        new_content = content.replace("index.md", "README.md")

        if new_content != content:
            count = content.count("index.md") - new_content.count("index.md")
            ref_fixes += abs(count) if count else content.count("index.md")
            if not dry_run:
                md.write_text(new_content, encoding="utf-8")

    print(f"Reference updates: {ref_fixes} occurrence(s) in markdown files")
    if dry_run:
        print("\nRun with --fix to apply all changes.")


if __name__ == "__main__":
    main()
