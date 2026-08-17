import urllib.request
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

url = "https://detail.zol.com.cn/cell_phone_index/subcat57_list.html"
try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode("gbk", errors="ignore")
        # Extract images and titles
        matches = re.findall(r'<img[^>]+src=[\'"]([^\'"]+zol-img\.com\.cn[^\'"]+)[\'"][^>]*alt=[\'"]([^\'"]+)[\'"]', html)
        if not matches:
            matches = re.findall(r'<img[^>]+alt=[\'"]([^\'"]+)[\'"][^>]*src=[\'"]([^\'"]+zol-img\.com\.cn[^\'"]+)[\'"]', html)
            matches = [(m[1], m[0]) for m in matches]
            
        print(f"✅ Found {len(matches)} devices from ZOL catalog:")
        for img, title in matches[:20]:
            print(f"- [{title}]: {img}")
except Exception as e:
    print("❌ Error:", e)
