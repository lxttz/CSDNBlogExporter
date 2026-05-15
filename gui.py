#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSDN 博客导出器 - 图形化界面
"""
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import subprocess
from urllib.parse import urlparse

class CSDNGui:
    def __init__(self, root):
        self.root = root
        self.root.title("CSDN 博客导出器")
        self.root.geometry("700x720")
        self.root.configure(bg='#ECEFF1')
        
        # 颜色主题
        self.colors = {
            'primary': '#1E88E5',
            'success': '#43A047',
            'secondary': '#757575',
            'card': '#FFFFFF',
            'text': '#212121',
            'log_bg': '#263238',
            'log_text': '#4CAF50',
        }
        
        self.is_running = False
        self.create_widgets()
        
    def create_widgets(self):
        # ===== 标题区域 =====
        header = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="CSDN 博客导出器", 
                font=("Microsoft YaHei", 22, "bold"),
                fg="white", bg=self.colors['primary']).pack(pady=(18, 3))
        tk.Label(header, text="将 CSDN 博客导出为 Markdown / PDF 格式",
                font=("Microsoft YaHei", 10), fg="#B3D4FC", bg=self.colors['primary']).pack()
        
        # ===== 主容器 =====
        container = tk.Frame(self.root, bg='#ECEFF1', padx=40, pady=15)
        container.pack(fill=tk.BOTH, expand=True)
        
        # ===== 导出类型 =====
        type_card = tk.Frame(container, bg=self.colors['card'], relief=tk.FLAT, bd=0,
                            highlightbackground='#E0E0E0', highlightthickness=1)
        type_card.pack(fill=tk.X, pady=(0, 12))
        
        tk.Label(type_card, text="导出类型", font=("Microsoft YaHei", 11, "bold"),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor=tk.W, padx=15, pady=(12, 5))
        
        type_frame = tk.Frame(type_card, bg=self.colors['card'])
        type_frame.pack(padx=15, pady=(0, 12))
        
        self.export_type = tk.StringVar(value="article")
        
        for text, value in [("单篇文章", "article"), ("整个分类", "category")]:
            rb = tk.Radiobutton(type_frame, text=text, variable=self.export_type, value=value,
                    font=("Microsoft YaHei", 10), bg=self.colors['card'], fg=self.colors['text'],
                    activebackground=self.colors['card'], command=self.on_type_change,
                    indicatoron=0, selectcolor='#1E88E5', width=10)
            rb.pack(side=tk.LEFT, padx=5)
        
        # ===== URL 输入 =====
        url_card = tk.Frame(container, bg=self.colors['card'],
                           highlightbackground='#E0E0E0', highlightthickness=1)
        url_card.pack(fill=tk.X, pady=(0, 12))
        
        tk.Label(url_card, text="CSDN 链接", font=("Microsoft YaHei", 11, "bold"),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor=tk.W, padx=15, pady=(12, 5))
        
        self.url_entry = tk.Entry(url_card, font=("Microsoft YaHei", 10),
                                  bg='#FAFAFA', insertbackground=self.colors['primary'])
        self.url_entry.pack(fill=tk.X, padx=15, pady=(0, 10), ipady=6)
        self.url_entry.insert(0, "https://blog.csdn.net/xxx/article/details/xxxxx")
        
        # ===== 页码设置 =====
        self.page_card = tk.Frame(container, bg=self.colors['card'],
                                 highlightbackground='#E0E0E0', highlightthickness=1)
        
        tk.Label(self.page_card, text="页码设置", font=("Microsoft YaHei", 11, "bold"),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor=tk.W, padx=15, pady=(12, 5))
        
        page_row = tk.Frame(self.page_card, bg=self.colors['card'])
        page_row.pack(pady=(0, 12), padx=15)
        
        tk.Label(page_row, text="起始页:", font=("Microsoft YaHei", 10), bg=self.colors['card']).pack(side=tk.LEFT)
        
        self.start_page = tk.Entry(page_row, width=8, font=("Microsoft YaHei", 10), bg='#FAFAFA')
        self.start_page.insert(0, "1")
        self.start_page.pack(side=tk.LEFT, padx=(5, 15), ipady=4)
        
        tk.Label(page_row, text="导出页数:", font=("Microsoft YaHei", 10), bg=self.colors['card']).pack(side=tk.LEFT)
        
        self.page_num = tk.Entry(page_row, width=8, font=("Microsoft YaHei", 10), bg='#FAFAFA')
        self.page_num.insert(0, "100")
        self.page_num.pack(side=tk.LEFT, padx=5, ipady=4)
        
        # ===== PDF 选项 =====
        option_card = tk.Frame(container, bg=self.colors['card'],
                              highlightbackground='#E0E0E0', highlightthickness=1)
        option_card.pack(fill=tk.X, pady=(0, 12))
        
        self.to_pdf = tk.BooleanVar()
        tk.Checkbutton(option_card, text="同时导出为 PDF", variable=self.to_pdf,
                font=("Microsoft YaHei", 10), bg=self.colors['card'], fg=self.colors['text'],
                activebackground=self.colors['card']).pack(anchor=tk.W, padx=15, pady=8)
        
        # ===== 按钮区域 =====
        btn_frame = tk.Frame(container, bg='#ECEFF1')
        btn_frame.pack(pady=10)
        
        self.start_btn = tk.Button(btn_frame, text="开始导出", font=("Microsoft YaHei", 12, "bold"),
                                   bg=self.colors['success'], fg="white", activebackground='#66BB6A',
                                   relief=tk.FLAT, cursor="hand2", width=12, height=2,
                                   command=self.start_export)
        self.start_btn.pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="终端模式", font=("Microsoft YaHei", 11),
                  bg=self.colors['secondary'], fg="white", activebackground='#9E9E9E',
                  relief=tk.FLAT, cursor="hand2", width=12, height=2,
                  command=self.open_terminal_mode).pack(side=tk.LEFT, padx=10)
        
        # ===== 日志区域 =====
        log_label = tk.Label(container, text="导出日志", font=("Microsoft YaHei", 11, "bold"),
                            bg='#ECEFF1', fg=self.colors['text'])
        log_label.pack(anchor=tk.W, pady=(10, 5))
        
        log_frame = tk.Frame(container, bg=self.colors['log_bg'])
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 0))
        
        self.log_text = tk.Text(log_frame, font=("Consolas", 10),
                                bg=self.colors['log_bg'], fg=self.colors['log_text'],
                                bd=0, insertbackground='white', relief=tk.FLAT)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(log_frame, command=self.log_text.yview, bg=self.colors['log_bg'])
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        
        self.on_type_change()
        
    def on_type_change(self, *args):
        if self.export_type.get() == "article":
            self.page_card.pack_forget()
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, "https://blog.csdn.net/xxx/article/details/xxxxx")
        else:
            self.page_card.pack(fill=tk.X, pady=(0, 12))
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, "https://blog.csdn.net/xxx/category/xxxxx.html")
            
    def log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        
    def start_export(self):
        if self.is_running:
            return
            
        url = self.url_entry.get().strip()
        if not url or "xxx" in url:
            messagebox.showwarning("提示", "请输入有效的 CSDN 链接!")
            return
            
        parsed = urlparse(url)
        clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        
        if self.export_type.get() == "article":
            cmd = f'python main.py --article_url "{clean_url}"'
        else:
            start = self.start_page.get() or "1"
            pages = self.page_num.get() or "100"
            cmd = f'python main.py --category_url "{clean_url}" --start_page {start} --page_num {pages}'
            
        if self.to_pdf.get():
            cmd += " --to_pdf"
            
        self.log(f"$ {cmd}\n" + "="*50)
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED, text="导出中...")
        
        thread = threading.Thread(target=self.run_export, args=(cmd,))
        thread.daemon = True
        thread.start()
        
    def run_export(self, cmd):
        try:
            self.log(f"执行命令: {cmd}")
            self.log("-" * 50)
            
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT)
            
            output_lines = []
            for line in process.stdout:
                # 尝试多种编码
                try:
                    decoded = line.decode('utf-8')
                except:
                    try:
                        decoded = line.decode('gbk')
                    except:
                        decoded = line.decode('latin-1', errors='ignore')
                output_lines.append(decoded.rstrip())
                
            process.wait()
            
            # 显示所有输出
            for line in output_lines:
                if line.strip():
                    self.log(line)
            
            self.log("-" * 50)
            if process.returncode == 0:
                self.log("✅ 导出完成！文件保存在 markdown/ 目录下")
                self.root.after(0, lambda: messagebox.showinfo("完成", "导出完成！\n\n文件保存在 markdown/ 目录下"))
            else:
                self.log("❌ 导出失败")
        except Exception as e:
            self.log(f"❌ 错误: {str(e)}")
            self.root.after(0, lambda: messagebox.showerror("错误", str(e)))
        finally:
            self.is_running = False
            self.start_btn.config(state=tk.NORMAL, text="开始导出")
            
    def open_terminal_mode(self):
        self.root.destroy()
        os.system("python run_interactive.py")

def main():
    root = tk.Tk()
    app = CSDNGui(root)
    root.mainloop()

if __name__ == "__main__":
    main()
