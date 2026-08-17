import urllib.request
import urllib.parse
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Referer": "https://mobile.zol.com.cn/pics/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

q = "小米15"
url = f"https://search.zol.com.cn/s/article.php?kword={urllib.parse.quote(q.encode('gbk'))}"
try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as r:
        html = r.read().decode("gbk", errors="ignore")
        imgs = re.findall(r'src=[\'"](https?://[^\s\'"<>]*zol-img\.com\.cn/[^\s\'"<>]+)[\'"]', html)
        print(f"✅ Found {len(imgs)} images on ZOL for {q}:")
        for img in imgs[:10]:
            print("-", img)
except Exception as e:
    print("❌ Error:", e)
