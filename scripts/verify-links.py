#!/usr/bin/env python3
"""
链接验证脚本
验证所有markdown文件中的链接：
1. 本地文件是否存在
2. GitHub原始URL是否可访问
3. 生成损坏链接报告
"""

import os
import re
import sys
import json
from pathlib import Path
from urllib.parse import urlparse
import subprocess
from typing import List, Dict, Tuple, Set
from dataclasses import dataclass

@dataclass
class Link:
    """链接信息"""
    source_file: str
    line_number: int
    link_text: str
    url: str
    is_external: bool
    is_github_raw: bool
    is_anchor: bool
    
    def __str__(self):
        return f"{self.source_file}:{self.line_number} - [{self.link_text}]({self.url})"

class LinkVerifier:
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir).resolve()
        self.links: List[Link] = []
        self.broken_links: List[Tuple[Link, str]] = []
        self.checked_count = 0
        
    def find_markdown_files(self) -> List[Path]:
        """查找所有markdown文件"""
        md_files = []
        for ext in ['*.md', '*.markdown']:
            md_files.extend(self.root_dir.rglob(ext))
        return md_files
    
    def extract_links(self, file_path: Path) -> List[Link]:
        """从markdown文件中提取链接"""
        links = []
        try:
            content = file_path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            print(f"警告: 无法解码文件 {file_path}")
            return links
            
        # Markdown链接模式: [text](url) 或 [text](url "title")
        pattern = r'\[([^\]]+)\]\(([^)"\']+)(?:\s+["\']([^"\']+)["\'])?\)'
        
        for match in re.finditer(pattern, content, re.MULTILINE):
            line_number = content[:match.start()].count('\n') + 1
            link_text = match.group(1)
            url = match.group(2).strip()
            
            # 跳过空URL
            if not url:
                continue
                
            # 判断链接类型
            is_external = url.startswith(('http://', 'https://'))
            is_github_raw = 'raw.githubusercontent.com' in url
            is_anchor = url.startswith('#')
            
            link = Link(
                source_file=str(file_path.relative_to(self.root_dir)),
                line_number=line_number,
                link_text=link_text,
                url=url,
                is_external=is_external,
                is_github_raw=is_github_raw,
                is_anchor=is_anchor
            )
            links.append(link)
            
        return links
    
    def resolve_local_path(self, source_file: str, url: str) -> Path:
        """解析本地路径"""
        source_dir = (self.root_dir / source_file).parent
        
        # 移除URL中的锚点部分
        url_without_anchor = url.split('#')[0]
        if not url_without_anchor:
            return None
            
        # 处理相对路径
        if url_without_anchor.startswith('/'):
            # 从根目录开始的绝对路径
            return self.root_dir / url_without_anchor.lstrip('/')
        else:
            # 相对于源文件的路径
            return source_dir / url_without_anchor
    
    def check_local_file_exists(self, link: Link) -> bool:
        """检查本地文件是否存在"""
        if link.is_external or link.is_anchor:
            return True
            
        local_path = self.resolve_local_path(link.source_file, link.url)
        if not local_path:
            return False
            
        return local_path.exists()
    
    def check_github_raw_url(self, link: Link) -> bool:
        """检查GitHub原始URL是否可访问"""
        if not link.is_github_raw:
            return True
            
        # 使用web_fetch工具验证URL
        try:
            # 这里我们尝试使用curl进行简单验证
            result = subprocess.run(
                ['curl', '-I', '-s', '-o', '/dev/null', '-w', '%{http_code}', link.url],
                capture_output=True,
                text=True,
                timeout=10
            )
            status_code = result.stdout.strip()
            return status_code == '200'
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
            return False
    
    def verify_all_links(self):
        """验证所有链接"""
        print("查找markdown文件...")
        md_files = self.find_markdown_files()
        print(f"找到 {len(md_files)} 个markdown文件")
        
        # 提取所有链接
        for md_file in md_files:
            links = self.extract_links(md_file)
            self.links.extend(links)
        
        print(f"找到 {len(self.links)} 个链接")
        
        # 验证链接
        for link in self.links:
            self.checked_count += 1
            
            # 跳过锚点链接
            if link.is_anchor:
                continue
                
            # 检查本地文件
            if not link.is_external:
                if not self.check_local_file_exists(link):
                    self.broken_links.append((link, "本地文件不存在"))
                    continue
                    
            # 检查GitHub原始URL
            if link.is_github_raw:
                if not self.check_github_raw_url(link):
                    self.broken_links.append((link, "GitHub原始URL不可访问"))
                    continue
                    
            # 外部链接暂不验证（需要网络请求）
            if link.is_external and not link.is_github_raw:
                # 可以添加外部链接验证，但需要小心超时
                pass
    
    def generate_report(self) -> str:
        """生成报告"""
        report = f"""# 链接验证报告

## 统计
- 检查的文件: {len(self.find_markdown_files())}
- 找到的链接: {len(self.links)}
- 检查的链接: {self.checked_count}
- 损坏的链接: {len(self.broken_links)}

## 损坏链接详情
"""
        if self.broken_links:
            for link, reason in self.broken_links:
                report += f"""
### {link.source_file}:{link.line_number}
- **链接**: [{link.link_text}]({link.url})
- **原因**: {reason}
- **类型**: {'GitHub原始URL' if link.is_github_raw else '外部链接' if link.is_external else '本地链接'}
"""
        else:
            report += "\n✅ 所有链接检查通过！"
            
        # 按类型统计
        local_links = [l for l in self.links if not l.is_external and not l.is_anchor]
        github_raw_links = [l for l in self.links if l.is_github_raw]
        external_links = [l for l in self.links if l.is_external and not l.is_github_raw]
        anchor_links = [l for l in self.links if l.is_anchor]
        
        report += f"""

## 链接类型统计
- 本地链接: {len(local_links)}
- GitHub原始URL: {len(github_raw_links)}
- 外部链接: {len(external_links)}
- 锚点链接: {len(anchor_links)}

## 建议
1. 修复损坏的本地链接
2. 验证GitHub原始URL是否有效
3. 定期运行此脚本以确保链接健康
"""
        
        return report
    
    def save_json_report(self, output_file: str):
        """保存JSON格式的报告"""
        report_data = {
            "stats": {
                "files_checked": len(self.find_markdown_files()),
                "links_found": len(self.links),
                "links_checked": self.checked_count,
                "broken_links": len(self.broken_links)
            },
            "broken_links": [
                {
                    "source_file": link.source_file,
                    "line_number": link.line_number,
                    "link_text": link.link_text,
                    "url": link.url,
                    "reason": reason,
                    "type": "github_raw" if link.is_github_raw else "external" if link.is_external else "local"
                }
                for link, reason in self.broken_links
            ]
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

def main():
    """主函数"""
    root_dir = "/root/git/jdk_internal-1"
    
    print(f"开始验证链接，根目录: {root_dir}")
    print("=" * 60)
    
    verifier = LinkVerifier(root_dir)
    verifier.verify_all_links()
    
    # 生成文本报告
    report = verifier.generate_report()
    print(report)
    
    # 保存报告
    reports_dir = Path(root_dir) / "reports"
    reports_dir.mkdir(exist_ok=True)
    
    report_file = reports_dir / "link_verification_report.md"
    report_file.write_text(report, encoding='utf-8')
    print(f"\n报告已保存到: {report_file}")
    
    # 保存JSON报告
    json_file = reports_dir / "link_verification_report.json"
    verifier.save_json_report(str(json_file))
    print(f"JSON报告已保存到: {json_file}")
    
    # 如果有损坏链接，返回错误代码
    if verifier.broken_links:
        print(f"\n❌ 发现 {len(verifier.broken_links)} 个损坏链接")
        sys.exit(1)
    else:
        print("\n✅ 所有链接检查通过！")
        sys.exit(0)

if __name__ == "__main__":
    main()