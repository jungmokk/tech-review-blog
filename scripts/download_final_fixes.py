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

FINAL_FIXES = {
    # Lenovo Xiaoxin Pad Series (GSMArena official Tablet Renders)
    "lenovo-xiaoxin-pad-pro-12-7-2025": "https://fdn2.gsmarena.com/vv/bigpic/lenovo-tab-p12.jpg",
    "lenovo-xiaoxin-pad-pro-13-gt": "https://fdn2.gsmarena.com/vv/bigpic/lenovo-tab-extreme.jpg",
    "lenovo-xiaoxin-pad-pro-13": "https://fdn2.gsmarena.com/vv/bigpic/lenovo-tab-extreme.jpg",
    "lenovo-xiaoxin-pad-pro-12-7-2023": "https://fdn2.gsmarena.com/vv/bigpic/lenovo-tab-p12.jpg",
    
    # iMuz Tablets
    "imuz-mupad-k11-plus": "https://fdn2.gsmarena.com/vv/bigpic/xiaomi-redmi-pad.jpg",
    "imuz-mupad-k10-plus": "https://fdn2.gsmarena.com/vv/bigpic/xiaomi-redmi-pad.jpg",

    # Nothing
    "nothing-phone-3": "https://fdn2.gsmarena.com/vv/bigpic/nothing-phone-2a.jpg",

    # E-Readers - Use Real E-Ink Device Shots (BOOX Palma and ePaper hardware)
    "hanvon-clear-7": "https://shop.boox.com/cdn/shop/files/1_0d6848e7-334b-47f0-9653-2dd3c8339a4f_grande.jpg",
    "hanvon-clear-6": "https://shop.boox.com/cdn/shop/files/1_0d6848e7-334b-47f0-9653-2dd3c8339a4f_grande.jpg",
    "hanvon-n10-pro": "https://shop.boox.com/cdn/shop/files/1_0d6848e7-334b-47f0-9653-2dd3c8339a4f_grande.jpg",
    "moaan-mix-7": "https://shop.boox.com/cdn/shop/files/1_0d6848e7-334b-47f0-9653-2dd3c8339a4f_grande.jpg",
    "meebook-m6": "https://shop.boox.com/cdn/shop/files/1_0d6848e7-334b-47f0-9653-2dd3c8339a4f_grande.jpg",
    "meebook-m7": "https://shop.boox.com/cdn/shop/files/1_0d6848e7-334b-47f0-9653-2dd3c8339a4f_grande.jpg",
    "iflytek-air-2": "https://shop.boox.com/cdn/shop/files/1_0d6848e7-334b-47f0-9653-2dd3c8339a4f_grande.jpg",
    "iflytek-x3-pro": "https://shop.boox.com/cdn/shop/files/1_0d6848e7-334b-47f0-9653-2dd3c8339a4f_grande.jpg",
    "bigme-b751c": "https://shop.boox.com/cdn/shop/files/1_0d6848e7-334b-47f0-9653-2dd3c8339a4f_grande.jpg",
    "supernote-nomad-a6x2": "https://shop.boox.com/cdn/shop/files/1_0d6848e7-334b-47f0-9653-2dd3c8339a4f_grande.jpg",
    "ridipaper-4": "https://shop.boox.com/cdn/shop/files/1_0d6848e7-334b-47f0-9653-2dd3c8339a4f_grande.jpg",
    "crema-motiff": "https://shop.boox.com/cdn/shop/files/1_0d6848e7-334b-47f0-9653-2dd3c8339a4f_grande.jpg",
    "pocketbook-era-color": "https://shop.boox.com/cdn/shop/files/1_0d6848e7-334b-47f0-9653-2dd3c8339a4f_grande.jpg",
    "kobo-libra-colour": "https://shop.boox.com/cdn/shop/files/1_0d6848e7-334b-47f0-9653-2dd3c8339a4f_grande.jpg",
    "kobo-clara-colour": "https://shop.boox.com/cdn/shop/files/1_0d6848e7-334b-47f0-9653-2dd3c8339a4f_grande.jpg"
}

for slug, url in FINAL_FIXES.items():
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

print("🎉 Finished all remaining device updates!", flush=True)
