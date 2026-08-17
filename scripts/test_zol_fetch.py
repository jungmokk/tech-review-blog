import urllib.request
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Referer": "https://detail.zol.com.cn/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

url = "https://detail.zol.com.cn/cell_phone/index384594/pic.shtml"
try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode("gbk", errors="ignore")
        imgs = re.findall(r"https?://[a-zA-Z0-9\.\_\-]*zol-img\.com\.cn/[^\s\"\'>]+\.(?:jpg|png|webp)", html)
        print(f"✅ Found {len(imgs)} ZOL images:")
        for img in imgs[:10]:
            print("-", img)
except Exception as e:
    print("❌ Error:", e)
