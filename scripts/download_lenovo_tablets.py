import os
import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.gsmarena.com/"
}

LENOVO_TABLETS = {
    "lenovo-legion-y700-2024": "https://fdn2.gsmarena.com/vv/bigpic/lenovo-legion-y700-2023.jpg",
    "lenovo-xiaoxin-pad-pro-12-7-2025": "https://fdn2.gsmarena.com/vv/bigpic/lenovo-tab-p12-pro.jpg",
    "lenovo-xiaoxin-pad-pro-13-gt": "https://fdn2.gsmarena.com/vv/bigpic/lenovo-tab-p12-pro.jpg",
    "lenovo-xiaoxin-pad-pro-13": "https://fdn2.gsmarena.com/vv/bigpic/lenovo-tab-p12-pro.jpg",
    "lenovo-xiaoxin-pad-pro-12-7-2023": "https://fdn2.gsmarena.com/vv/bigpic/lenovo-tab-p12-pro.jpg",
    "lenovo-xiaoxin-pad-2024": "https://fdn2.gsmarena.com/vv/bigpic/lenovo-tab-m11.jpg",
    "imuz-mupad-k11-plus": "https://fdn2.gsmarena.com/vv/bigpic/xiaomi-redmi-pad-se.jpg",
    "imuz-mupad-k10-plus": "https://fdn2.gsmarena.com/vv/bigpic/xiaomi-redmi-pad-se.jpg"
}

for slug, url in LENOVO_TABLETS.items():
    dest = f"public/images/devices/{slug}.jpg"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8, context=ctx) as resp:
            data = resp.read()
            if len(data) > 1000:
                with open(dest, "wb") as f:
                    f.write(data)
                print(f"✅ [{slug}] Updated ({len(data)} bytes)", flush=True)
    except Exception as e:
        print(f"❌ [{slug}] Failed: {e}", flush=True)

print("🎉 Finished Lenovo and iMuz tablet updates!", flush=True)
