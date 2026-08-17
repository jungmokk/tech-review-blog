import urllib.request
import urllib.parse
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Referer": "https://detail.zol.com.cn/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

kw = "小米15"
url = f"https://detail.zol.com.cn/index.php?c=SearchList&kword={urllib.parse.quote(kw.encode('gbk'))}"
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=10) as r:
    html = r.read().decode("gbk", errors="ignore")
    print("Page length:", len(html))
    links = re.findall(r'href=[\'"]([^\'"]+)[\'"]', html)
    print(f"Found {len(links)} href links. Sample:")
    for l in links[:30]:
        print("-", l)
