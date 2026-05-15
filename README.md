# CSDN Blog Exporter

> 一键将 CSDN 博客导出为 Markdown / PDF 格式，支持单篇文章和批量分类导出

## 功能特性

- **图形界面**：可视化操作，一键导出
- **终端模式**：命令行交互，简单易用
- **单篇导出**：输入文章链接，一键导出为 Markdown
- **批量导出**：输入分类链接，批量导出该分类下所有文章
- **保留图片**：图片保持原始 URL，兼容各类 Markdown 阅读器
- **PDF 转换**（可选）：支持将 Markdown 转换为 PDF
- **跨平台**：支持 Windows、macOS、Linux

## 环境要求

- Python 3.6+
- BeautifulSoup4
- tkinter（Python 内置，用于图形界面）
- Pandoc（可选，用于生成 PDF）
- aria2（可选，用于下载图片到本地）

## 安装

```bash
# 克隆项目
git clone https://github.com/yourusername/csdn-blog-exporter.git
cd csdn-blog-exporter

# 安装依赖
pip install beautifulsoup4

# 可选：安装 aria2（用于下载图片到本地）
# 下载地址：https://github.com/aria2/aria2/releases

# 可选：安装 pandoc（用于生成 PDF）
# 下载地址：https://pandoc.org/installing.html
```

## 快速开始

**Windows 用户**：双击 `启动导出器.bat`，根据提示选择运行模式即可。

## 使用方法

### 图形界面（推荐）

双击 `启动导出器.bat`，选择 **1** 进入图形界面模式：

- 可视化操作，无需记忆命令
- 实时显示导出日志
- 支持单篇文章/分类导出切换
- 支持 PDF 导出选项

### 终端交互模式

双击 `启动导出器.bat`，选择 **2** 进入终端模式：

```bash
python run_interactive.py
```

交互式引导，输入 URL 即可开始导出。

### 命令行参数

#### 导出单篇文章

```bash
python main.py --article_url "https://blog.csdn.net/username/article/details/123456789"
```

#### 导出整个分类

```bash
# 导出分类下所有文章
python main.py --category_url "https://blog.csdn.net/username/category/123456.html"

# 指定页码范围
python main.py --category_url "分类URL" --start_page 1 --page_num 10
```

#### 导出为 PDF

```bash
python main.py --article_url "文章URL" --to_pdf
```

#### 其他选项

| 参数 | 说明 |
|------|------|
| `--markdown_dir` | Markdown 保存目录（默认：`markdown`） |
| `--pdf_dir` | PDF 保存目录（默认：`pdf`） |
| `--combine_together` | 合并所有 Markdown 为一个文件 |
| `--rm_cache` | 删除缓存文件 |

## 项目结构

```
csdn-blog-exporter/
├── main.py              # 主程序
├── utils.py             # HTML 解析工具
├── gui.py               # 图形界面
├── run_interactive.py   # 终端交互脚本
├── 启动导出器.bat        # Windows 一键启动
└── markdown/            # 导出的 Markdown 文件
    └── pdf/             # 导出的 PDF 文件
```

## 界面预览

### 图形界面

双击 `启动导出器.bat` → 选择 1 → 进入图形界面

### 终端交互

```
==================================================
           CSDN 博客导出器 - 启动菜单
==================================================

    1. 图形界面模式 (推荐)
    2. 终端交互模式
    3. 退出

请选择运行模式 (1/2/3): 2

==================================================
   CSDN 博客导出器
==================================================

请选择导出类型:
  1. 导出单篇文章
  2. 导出整个分类

请输入选项 (1/2): 1
请输入 CSDN URL: https://blog.csdn.net/xxx/article/details/123456
是否同时导出 PDF? (y/N): n

导出完成!
```

## License

MIT License
