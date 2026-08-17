import urllib.request
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Referer": "https://mobile.zol.com.cn/pics/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

url = "https://detail.zol.com.cn/cell_phone/index1227467.shtml"
try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode("gbk", errors="ignore")
        # Find product title
        title_m = re.search(r'<h1[^>]*>([^<]+)</h1>', html)
        title = title_m.group(1).strip() if title_m else "Unknown"
        
        # Find big main product image
        imgs = re.findall(r'<img[^>]+src=[\'"](https?://[^\'"]+zol-img\.com\.cn/[^\'"]+)[\'"]', html)
        print(f"✅ Product: {title}")
        print(f"📸 Found {len(imgs)} images:")
        for img in imgs[:5]:
            print("-", img)
except Exception as e:
    print("❌ Error:", e)
