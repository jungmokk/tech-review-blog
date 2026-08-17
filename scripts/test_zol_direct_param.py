import urllib.request
import urllib.parse
import re
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Referer": "https://detail.zol.com.cn/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

def get_zol_param_url_via_search(device_name):
    # Query Bing for direct ZOL param page
    q = f"site:detail.zol.com.cn \"{device_name}\" \"param.shtml\""
    url = f"https://www.bing.com/search?q={urllib.parse.quote(q)}"
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
            # Extract URLs matching https://detail.zol.com.cn/.../param.shtml
            param_urls = re.findall(r'https://detail\.zol\.com\.cn/[a-zA-Z0-9\_]+/index\d+/param\.shtml', html)
            if param_urls:
                return param_urls[0]
            # Fallback to indexXXXXX.shtml
            detail_urls = re.findall(r'https://detail\.zol\.com\.cn/([a-zA-Z0-9\_]+)/index(\d+)\.shtml', html)
            if detail_urls:
                cat, pid = detail_urls[0]
                return f"https://detail.zol.com.cn/{cat}/index{pid}/param.shtml"
    except Exception as e:
        print(f"Error for {device_name}: {e}")
    return None

test_devices = [
    "小米15 Ultra",
    "vivo X200 Pro",
    "华为 Mate XT",
    "联想 拯救者 Y700 2024",
    "OPPO Pad 3 Pro"
]

for dev in test_devices:
    p_url = get_zol_param_url_via_search(dev)
    print(f"🎯 [{dev}] => ZOL Param URL: {p_url}")
    if p_url:
        try:
            req = urllib.request.Request(p_url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as r:
                page_html = r.read().decode("gbk", errors="ignore")
                rows = re.findall(r'<th[^>]*>(.*?)</th>\s*<td[^>]*>(.*?)</td>', page_html, re.DOTALL)
                print(f"   📋 Extracted {len(rows)} technical parameters from ZOL:")
                for th, td in rows[:5]:
                    clean_th = re.sub(r'<[^>]+>', '', th).strip()
                    clean_td = re.sub(r'<[^>]+>', '', td).strip()
                    clean_td = re.sub(r'\s+', ' ', clean_td)
                    print(f"     • {clean_th}: {clean_td}")
        except Exception as e:
            print("   Error reading param page:", e)
    print()
