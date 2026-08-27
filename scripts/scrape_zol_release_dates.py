import urllib.request
import urllib.parse
import re
import json
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Referer": "https://detail.zol.com.cn/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

def search_zol_product(query):
    try:
        gbk_query = urllib.parse.quote(query.encode("gbk"))
        search_url = f"https://detail.zol.com.cn/index.php?c=SearchList&kword={gbk_query}"
        req = urllib.request.Request(search_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("gbk", errors="ignore")
            
            # Find first product link
            # Look for /cell_phone/indexXXXXX.shtml, /digital_player/indexXXXXX.shtml, /tablepc/indexXXXXX.shtml, /headphone/indexXXXXX.shtml, /ebook/indexXXXXX.shtml
            param_matches = re.findall(r'href=["\'](/[^"\']+/index\d+/param\.shtml)["\']', html)
            if param_matches:
                return "https://detail.zol.com.cn" + param_matches[0]
                
            detail_matches = re.findall(r'href=["\'](/([a-zA-Z0-9\_]+)/index(\d+)\.shtml)["\']', html)
            for dm in detail_matches:
                full_path, cat, pid = dm
                if cat in ['cell_phone', 'tablepc', 'notebook', 'headphone', 'digital_player', 'ebook', 'smart_watch', 'audio']:
                    return f"https://detail.zol.com.cn/{cat}/index{pid}/param.shtml"
                    
            if detail_matches:
                full_path, cat, pid = detail_matches[0]
                return f"https://detail.zol.com.cn/{cat}/index{pid}/param.shtml"
    except Exception as e:
        print(f"  [Search Error for {query}]: {e}")
    return None

def fetch_zol_release_date(param_url):
    try:
        req = urllib.request.Request(param_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            page_html = resp.read().decode("gbk", errors="ignore")
            
            # Extract title / product name
            title_m = re.findall(r'<h1[^>]*>(.*?)</h1>', page_html, re.DOTALL)
            title = re.sub(r'<[^>]+>', '', title_m[0]).strip() if title_m else ""
            
            rows = re.findall(r'<th[^>]*>(.*?)</th>\s*<td[^>]*>(.*?)</td>', page_html, re.DOTALL)
            specs = {}
            for th, td in rows:
                clean_th = re.sub(r'<[^>]+>', '', th).strip()
                clean_td = re.sub(r'<[^>]+>', '', td).strip()
                clean_td = re.sub(r'\s+', ' ', clean_td)
                specs[clean_th] = clean_td
                
            # Check keys
            release_date = None
            for key in ["上市日期", "上市时间", "发布时间", "曝光日期", "发布日期"]:
                if key in specs:
                    release_date = specs[key]
                    break
                    
            return {
                "title": title,
                "release_date": release_date,
                "specs": specs
            }
    except Exception as e:
        print(f"  [Fetch Error for {param_url}]: {e}")
    return None

def main():
    with open("src/data/smartphones.json", "r", encoding="utf-8") as f:
        devices = json.load(f)
        
    queries = {
        "airpods-pro-3": "苹果 AirPods Pro 3",
        "airpods-4": "苹果 AirPods 4",
        "airpods-pro-2": "苹果 AirPods Pro 2",
        "galaxy-s25-ultra": "三星 Galaxy S25 Ultra",
        "galaxy-s24-ultra": "三星 Galaxy S24 Ultra",
        "galaxy-z-fold6": "三星 Galaxy Z Fold6",
        "galaxy-z-flip6": "三星 Galaxy Z Flip6",
        "iphone-16-pro-max": "苹果 iPhone 16 Pro Max",
        "iphone-16": "苹果 iPhone 16",
        "huawei-mate-xt": "华为 Mate XT 非凡大师",
        "xiaomi-15-ultra": "小米 15 Ultra",
        "xiaomi-pad-7-pro": "小米平板 7 Pro",
        "vivo-x200-pro": "vivo X200 Pro",
        "oneplus-13": "一加 13",
        "oppo-pad-3-pro": "OPPO Pad 3 Pro",
        "lenovo-legion-y700-2024": "联想 拯救者 Y700 2024",
        "lenovo-xiaoxin-pad-pro-12-7-2025": "联想 小新 Pad Pro 12.7 2025",
        "lenovo-xiaoxin-pad-pro-13": "联想 小新 Pad Pro 13",
        "ipad-pro-13-m4": "苹果 iPad Pro 13英寸 2024",
        "ipad-mini-7": "苹果 iPad mini 7",
        "m4-mac-mini": "苹果 Mac mini M4",
        "boox-palma-2": "文石 BOOX Palma",
        "sony-wh-1000xm5": "索尼 WH-1000XM5"
    }
    
    results = []
    print(f"🚀 Starting ZOL (detail.zol.com.cn) live query & scraping...\n")
    
    for dev_id, query in queries.items():
        print(f"🔍 Searching ZOL for: [{dev_id}] => '{query}'")
        url = search_zol_product(query)
        if url:
            data = fetch_zol_release_date(url)
            if data:
                print(f"   ✅ Found: {data.get('title')}")
                print(f"   📅 Release Info: {data.get('release_date')}")
                results.append({
                    "id": dev_id,
                    "query": query,
                    "zol_title": data.get("title"),
                    "zol_release_date": data.get("release_date"),
                    "zol_url": url
                })
            else:
                print(f"   ⚠️ Could not fetch specs from {url}")
        else:
            print(f"   ❌ No product page found on ZOL")
        time.sleep(0.5)
        
    print("\n" + "="*80)
    print("📊 ZOL OFFICIAL SCRAPED RESULTS:")
    print("="*80)
    for r in results:
        print(f"• [{r['id']}] {r['zol_title']} -> {r['zol_release_date']} ({r['zol_url']})")

if __name__ == "__main__":
    main()
