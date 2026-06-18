/**
 * Cloudflare Pages Function - CSDN 页面抓取代理
 */
export async function onRequest(context) {
  const { request } = context;
  const url = new URL(request.url);

  // CORS preflight
  if (request.method === 'OPTIONS') {
    return new Response(null, {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': '*',
      }
    });
  }

  const targetUrl = url.searchParams.get('url');
  if (!targetUrl) return json({ error: '缺少 url 参数' }, 400);

  try {
    const parsed = new URL(targetUrl);
    if (!parsed.hostname.includes('csdn.net')) {
      return json({ error: '仅支持 CSDN 链接' }, 400);
    }
  } catch {
    return json({ error: '无效 URL' }, 400);
  }

  // 尝试多种方式抓取
  let lastErr = '';
  const headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
  };

  for (const strategy of ['direct', 'resolveOverride']) {
    try {
      const opts = {
        method: 'GET',
        headers,
        redirect: 'follow',
      };

      if (strategy === 'resolveOverride') {
        opts.cf = {
          resolveOverride: 'blog.csdn.net',
        };
      }

      const resp = await fetch(targetUrl, opts);

      if (resp.ok) {
        const html = await resp.text();
        return json({ html });
      }

      lastErr = `HTTP ${resp.status} (${strategy})`;
    } catch (e) {
      lastErr = `${e.message} (${strategy})`;
    }
  }

  return json({ error: `请求 CSDN 失败: ${lastErr}。Cloudflare 边缘节点可能无法访问 CSDN 服务器，建议本地运行 server.py` }, 502);
}

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Access-Control-Allow-Origin': '*',
    }
  });
}
