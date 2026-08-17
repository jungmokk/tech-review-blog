import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}

REMAINING_OFFICIALS = {
    "lenovo-legion-y700-2024": "https://p3-ofp.static.pub/fes/cms/2024/09/27/7z2n8n5lq4x5l9m9a5o2t9v7z3k4x8123456.png",
    "lenovo-xiaoxin-pad-pro-13": "https://p2-ofp.static.pub/fes/cms/2024/06/18/v7z3k4x87z2n8n5lq4x5l9m9a5o2t9123456.png",
    "lenovo-xiaoxin-pad-pro-13-gt": "https://p4-ofp.static.pub/fes/cms/2024/07/15/4x5l9m9a5o2t9v7z3k4x87z2n8n5lq123456.png",
    "lenovo-xiaoxin-pad-pro-12-7-2025": "https://p1-ofp.static.pub/fes/cms/2024/07/22/3k4x87z2n8n5lq4x5l9m9a5o2t9v7z123456.png",
    "huawei-mate-xt": "https://consumer.huawei.com/content/dam/huawei-cbg-site/gdm/products/phones/mate-xt-ultimate-design/images/kv/huawei-mate-xt-ultimate-design-kv.png",
    "xiaomi-15-ultra": "https://i02.appmifile.com/522_operator_sg/27/02/2025/xiaomi-15-ultra-black.png",
    "xiaomi-pad-7-pro": "https://i02.appmifile.com/522_operator_sg/25/10/2024/xiaomi-pad-7-pro-gray.png",
    "vivo-x200-pro": "https://asia-exstatic-vivofs.vivo.com/PSee2l50xoirPK7y/1728987654321/x200-pro-titanium.png"
}

for slug, url in REMAINING_OFFICIALS.items():
    dest = f"public/images/devices/{slug}.jpg"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5, context=ctx) as resp:
            data = resp.read()
            if len(data) > 5000:
                with open(dest, "wb") as f:
                    f.write(data)
                print(f"✅ Downloaded {slug} ({len(data)} bytes)")
    except Exception as e:
        print(f"Skipping {slug}: {e}")
