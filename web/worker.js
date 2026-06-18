/**
 * CSDN Blog Exporter - Cloudflare Worker
 * 作为后端代理，抓取 CSDN 页面并返回内容，解决 CORS 问题
 */

export default {
    async fetch(request, env, ctx) {
        const url = new URL(request.url);
        const pathname = url.pathname;

        // CORS 预检处理
        if (request.method === 'OPTIONS') {
            return corsResponse();
        }

        // API: 获取 CSDN 页面内容
        if (pathname === '/api/article' || pathname === '/api/category') {
            const targetUrl = url.searchParams.get('url');
            if (!targetUrl) {
                return corsJson({ error: '缺少 url 参数' }, 400);
            }

            // 验证 URL 是 CSDN 域名
            try {
                const parsed = new URL(targetUrl);
                if (!parsed.hostname.includes('csdn.net')) {
                    return corsJson({ error: '仅支持 CSDN 链接' }, 400);
                }
            } catch {
                return corsJson({ error: '无效的 URL' }, 400);
            }

            try {
                const resp = await fetch(targetUrl, {
                    headers: {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0'
                    }
                });

                if (!resp.ok) {
                    return corsJson({ error: `CSDN 返回状态码 ${resp.status}` }, 502);
                }

                const html = await resp.text();
                return corsJson({ html: html });
            } catch (e) {
                return corsJson({ error: `请求失败: ${e.message}` }, 502);
            }
        }

        // 其他路径返回 404
        return corsJson({ error: 'Not Found' }, 404);
    }
};

function corsResponse() {
    return new Response(null, {
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
    });
}

function corsJson(data, status = 200) {
    return new Response(JSON.stringify(data), {
        status: status,
        headers: {
            'Content-Type': 'application/json; charset=utf-8',
            'Access-Control-Allow-Origin': '*',
        }
    });
}
