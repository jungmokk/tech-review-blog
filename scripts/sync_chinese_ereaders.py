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

SPECIAL_EINK_CHINESE = {
    "oneplus-open": "https://fdn2.gsmarena.com/vv/bigpic/oppo-find-n3.jpg",
    "nothing-phone-3": "https://fdn2.gsmarena.com/vv/bigpic/nothing-phone-2.jpg",
    
    # E-Ink Devices
    "hanvon-clear-7": "https://shop.boox.com/cdn/shop/files/Page-1.jpg",
    "hanvon-clear-6": "https://shop.boox.com/cdn/shop/files/Go6-1.jpg",
    "hanvon-n10-pro": "https://shop.boox.com/cdn/shop/files/Go10.3-1.jpg",
    
    "moaan-inkpalm-5": "https://shop.boox.com/cdn/shop/files/1_0d6848e7-334b-47f0-9653-2dd3c8339a4f_grande.jpg",
    "moaan-inkpalm-plus": "https://shop.boox.com/cdn/shop/files/1_0d6848e7-334b-47f0-9653-2dd3c8339a4f_grande.jpg",
    "moaan-mix-7": "https://shop.boox.com/cdn/shop/files/GoColor7-1.jpg",
    
    "meebook-m6": "https://shop.boox.com/cdn/shop/files/Go6-1.jpg",
    "meebook-m7": "https://shop.boox.com/cdn/shop/files/GoColor7-1.jpg",
    
    "iflytek-air-2": "https://shop.boox.com/cdn/shop/files/Go10.3-1.jpg",
    "iflytek-x3-pro": "https://shop.boox.com/cdn/shop/files/Go10.3-1.jpg",
    
    "bigme-b751c": "https://shop.boox.com/cdn/shop/files/GoColor7-1.jpg",
    "bigme-hibreak": "https://shop.boox.com/cdn/shop/files/1_0d6848e7-334b-47f0-9653-2dd3c8339a4f_grande.jpg",
    "supernote-nomad-a6x2": "https://shop.boox.com/cdn/shop/files/Go10.3-1.jpg",
    "ridipaper-4": "https://shop.boox.com/cdn/shop/files/GoColor7-1.jpg",
    "crema-motiff": "https://shop.boox.com/cdn/shop/files/Go6-1.jpg",
    "pocketbook-era-color": "https://shop.boox.com/cdn/shop/files/GoColor7-1.jpg",
    "kobo-libra-colour": "https://shop.boox.com/cdn/shop/files/GoColor7-1.jpg",
    "kobo-clara-colour": "https://shop.boox.com/cdn/shop/files/Go6-1.jpg"
}

for slug, url in SPECIAL_EINK_CHINESE.items():
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

print("🎉 Finished Special Chinese E-Reader sync!", flush=True)
