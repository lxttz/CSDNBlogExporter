#!/usr/bin/env python3
"""
本地测试服务器 - 模拟 Cloudflare Worker
运行: python server.py
然后访问: http://localhost:8787
"""
import http.server
import urllib.request
import urllib.parse
import ssl
import json
import sys
import os

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE
ssl._create_default_https_context = ssl._create_unverified_context

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == '/' or not parsed.path.startswith('/api/'):
            if parsed.path == '/':
                self.path = '/index.html'
            return super().do_GET()

        # API: /api/article?url=...
        if parsed.path in ('/api/article', '/api/category'):
            params = urllib.parse.parse_qs(parsed.query)
            url = params.get('url', [None])[0]
            if not url:
                self._json({'error': 'Missing url'}, 400)
                return

            try:
                req = urllib.request.Request(url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                })
                with urllib.request.urlopen(req, timeout=60) as resp:
                    html = resp.read()

                # 尝试解码
                try:
                    decoded = html.decode('utf-8')
                except:
                    try:
                        decoded = html.decode('gbk')
                    except:
                        decoded = html.decode('latin-1', errors='ignore')

                self._json({'html': decoded})
            except Exception as e:
                print(f'[ERROR] 抓取失败: {url} -> {e}')
                import traceback
                traceback.print_exc()
                self._json({'error': str(e)}, 502)
            return

        self._json({'error': 'Not found'}, 404)

    def _json(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()

    def log_message(self, format, *args):
        sys.stdout.write("[%s] %s\n" % (self.log_date_time_string(), format % args))

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    port = 8787
    print(f'本地测试服务器启动: http://localhost:{port}')
    print('按 Ctrl+C 停止')
    http.server.HTTPServer(('0.0.0.0', port), Handler).serve_forever()
