#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSDN 博客导出器 - 交互式启动脚本
"""
import os
import sys
from urllib.parse import urlparse

def main():
    print("=" * 50)
    print("   CSDN 博客导出器")
    print("=" * 50)
    print()

    print("请选择导出类型:")
    print("  1. 导出单篇文章")
    print("  2. 导出整个分类专栏")
    print()

    choice = input("请输入选项 (1/2): ").strip()

    url = input("请输入 CSDN URL: ").strip()
    if not url:
        print("错误: URL 不能为空!")
        sys.exit(1)

    # 清理 URL (去掉查询参数)
    parsed = urlparse(url)
    clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    
    if choice == "1":
        cmd = f'python main.py --article_url "{clean_url}"'
    elif choice == "2":
        start = input("起始页 (直接回车默认1): ").strip() or "1"
        pages = input("页数 (直接回车默认100): ").strip() or "100"
        cmd = f'python main.py --category_url "{clean_url}" --start_page {start} --page_num {pages}'
    else:
        print("无效选项!")
        sys.exit(1)

    print()
    to_pdf = input("是否同时导出 PDF? (y/N): ").strip().lower()
    if to_pdf == 'y':
        cmd += " --to_pdf"

    print()
    print("=" * 50)
    print("开始执行...")
    print(f"命令: {cmd}")
    print("=" * 50)
    print()

    os.system(cmd)

    print()
    print("导出完成!")

if __name__ == "__main__":
    main()
