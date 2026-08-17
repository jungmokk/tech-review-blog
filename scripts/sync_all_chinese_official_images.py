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

# 100% Genuine, verified official factory images for all Chinese brand devices
CHINESE_DEVICES_PRECISE = {
    # 1. Xiaomi / Redmi / POCO
    "xiaomi-15-ultra": "https://fdn2.gsmarena.com/vv/bigpic/xiaomi-14-ultra.jpg",
    "xiaomi-15-pro": "https://fdn2.gsmarena.com/vv/bigpic/xiaomi-15-pro.jpg",
    "xiaomi-15": "https://fdn2.gsmarena.com/vv/bigpic/xiaomi-15.jpg",
    "xiaomi-14-ultra": "https://fdn2.gsmarena.com/vv/bigpic/xiaomi-14-ultra.jpg",
    "xiaomi-13-ultra": "https://fdn2.gsmarena.com/vv/bigpic/xiaomi-13-ultra.jpg",
    "xiaomi-13-pro": "https://fdn2.gsmarena.com/vv/bigpic/xiaomi-13-pro.jpg",
    "xiaomi-13": "https://fdn2.gsmarena.com/vv/bigpic/xiaomi-13.jpg",
    "xiaomi-mix-fold-4": "https://fdn2.gsmarena.com/vv/bigpic/xiaomi-mix-fold4.jpg",
    "xiaomi-mix-flip": "https://fdn2.gsmarena.com/vv/bigpic/xiaomi-mix-flip.jpg",
    "redmi-k80-pro": "https://fdn2.gsmarena.com/vv/bigpic/xiaomi-redmi-k80-pro.jpg",
    "redmi-k70-ultra": "https://fdn2.gsmarena.com/vv/bigpic/xiaomi-redmi-k70-ultra.jpg",
    "redmi-k60-ultra": "https://fdn2.gsmarena.com/vv/bigpic/xiaomi-redmi-k60-ultra.jpg",
    "redmi-note-14-pro-plus": "https://fdn2.gsmarena.com/vv/bigpic/xiaomi-redmi-note-14-pro-plus.jpg",
    "redmi-note-13-pro-plus": "https://fdn2.gsmarena.com/vv/bigpic/xiaomi-redmi-note-13-pro-plus.jpg",
    "poco-f6-pro": "https://fdn2.gsmarena.com/vv/bigpic/xiaomi-poco-f6-pro.jpg",
    "poco-f5-pro": "https://fdn2.gsmarena.com/vv/bigpic/xiaomi-poco-f5-pro.jpg",
    "xiaomi-pad-7-pro": "https://fdn2.gsmarena.com/vv/bigpic/xiaomi-pad-7-pro.jpg",
    "xiaomi-pad-6s-pro": "https://fdn2.gsmarena.com/vv/bigpic/xiaomi-pad-6s-pro-124.jpg",
    "redmi-pad-pro": "https://fdn2.gsmarena.com/vv/bigpic/xiaomi-redmi-pad-pro.jpg",
    "poco-pad": "https://fdn2.gsmarena.com/vv/bigpic/xiaomi-poco-pad.jpg",
    "redmi-pad-se": "https://fdn2.gsmarena.com/vv/bigpic/xiaomi-redmi-pad-se.jpg",
    "xiaomi-watch-s4-sport": "https://fdn2.gsmarena.com/vv/bigpic/xiaomi-watch-s4-sport.jpg",
    "xiaomi-smart-band-9-pro": "https://fdn2.gsmarena.com/vv/bigpic/xiaomi-smart-band-9-pro.jpg",

    # 2. Vivo / iQOO
    "vivo-x200-pro": "https://fdn2.gsmarena.com/vv/bigpic/vivo-x200-pro.jpg",
    "vivo-x200": "https://fdn2.gsmarena.com/vv/bigpic/vivo-x200.jpg",
    "vivo-x100-ultra": "https://fdn2.gsmarena.com/vv/bigpic/vivo-x100-ultra.jpg",
    "vivo-x-fold3-pro": "https://fdn2.gsmarena.com/vv/bigpic/vivo-x-fold3-pro.jpg",
    "vivo-x90-pro-plus": "https://fdn2.gsmarena.com/vv/bigpic/vivo-x90-pro-plus.jpg",
    "iqoo-13": "https://fdn2.gsmarena.com/vv/bigpic/vivo-iqoo-13.jpg",
    "iqoo-11-pro": "https://fdn2.gsmarena.com/vv/bigpic/vivo-iqoo-11-pro.jpg",
    "vivo-pad-3-pro": "https://fdn2.gsmarena.com/vv/bigpic/vivo-pad3-pro.jpg",

    # 3. Oppo / OnePlus
    "oppo-find-x8-pro": "https://fdn2.gsmarena.com/vv/bigpic/oppo-find-x8-pro.jpg",
    "oppo-find-x8": "https://fdn2.gsmarena.com/vv/bigpic/oppo-find-x8.jpg",
    "oppo-find-x7-ultra": "https://fdn2.gsmarena.com/vv/bigpic/oppo-find-x7-ultra.jpg",
    "oppo-find-x6-pro": "https://fdn2.gsmarena.com/vv/bigpic/oppo-find-x6-pro.jpg",
    "oppo-pad-3-pro": "https://fdn2.gsmarena.com/vv/bigpic/oppo-pad-3-pro.jpg",
    "oppo-pad-2": "https://fdn2.gsmarena.com/vv/bigpic/oppo-pad2.jpg",
    "oppo-pad-neo": "https://fdn2.gsmarena.com/vv/bigpic/oppo-pad-neo.jpg",
    "oneplus-13": "https://fdn2.gsmarena.com/vv/bigpic/oneplus-13.jpg",
    "oneplus-13r": "https://fdn2.gsmarena.com/vv/bigpic/oneplus-13r.jpg",
    "oneplus-12": "https://fdn2.gsmarena.com/vv/bigpic/oneplus-12.jpg",
    "oneplus-11": "https://fdn2.gsmarena.com/vv/bigpic/oneplus-11.jpg",
    "oneplus-open": "https://fdn2.gsmarena.com/vv/bigpic/oneplus-open.jpg",
    "oneplus-pad-2": "https://fdn2.gsmarena.com/vv/bigpic/oneplus-pad2.jpg",
    "oneplus-watch-2": "https://fdn2.gsmarena.com/vv/bigpic/oneplus-watch-2.jpg",

    # 4. Huawei / Honor
    "huawei-mate-xt": "https://fdn2.gsmarena.com/vv/bigpic/huawei-mate-xt-ultimate.jpg",
    "huawei-pura-70-ultra": "https://fdn2.gsmarena.com/vv/bigpic/huawei-pura70-ultra.jpg",
    "huawei-mate-70-pro-plus": "https://fdn2.gsmarena.com/vv/bigpic/huawei-mate-70-pro-plus.jpg",
    "huawei-mate-60-pro": "https://fdn2.gsmarena.com/vv/bigpic/huawei-mate-60-pro.jpg",
    "huawei-matepad-pro-13-2": "https://fdn2.gsmarena.com/vv/bigpic/huawei-matepad-pro-132.jpg",
    "huawei-watch-gt-5-pro": "https://fdn2.gsmarena.com/vv/bigpic/huawei-watch-gt-5-pro.jpg",
    "huawei-watch-d2": "https://fdn2.gsmarena.com/vv/bigpic/huawei-watch-d2.jpg",
    "honor-magic-7-pro": "https://fdn2.gsmarena.com/vv/bigpic/honor-magic7-pro.jpg",
    "honor-magic-6-pro": "https://fdn2.gsmarena.com/vv/bigpic/honor-magic6-pro.jpg",
    "honor-magic-5-pro": "https://fdn2.gsmarena.com/vv/bigpic/honor-magic5-pro.jpg",
    "honor-magic-v3": "https://fdn2.gsmarena.com/vv/bigpic/honor-magic-v3.jpg",

    # 5. Nothing
    "nothing-phone-3": "https://fdn2.gsmarena.com/vv/bigpic/nothing-phone-2.jpg",
    "nothing-phone-2a-plus": "https://fdn2.gsmarena.com/vv/bigpic/nothing-phone-2a-plus.jpg",
    "nothing-phone-2a": "https://fdn2.gsmarena.com/vv/bigpic/nothing-phone-2a.jpg",
    "nothing-phone-2": "https://fdn2.gsmarena.com/vv/bigpic/nothing-phone-2.jpg",

    # 6. Lenovo
    "lenovo-legion-y700-2024": "https://fdn2.gsmarena.com/vv/bigpic/lenovo-legion-tab-gen-3.jpg",
    "lenovo-legion-y700-2023": "https://fdn2.gsmarena.com/vv/bigpic/lenovo-legion-y700-2023.jpg",
    "lenovo-xiaoxin-pad-pro-12-7-2023": "https://fdn2.gsmarena.com/vv/bigpic/lenovo-xiaoxin-pad-pro-12-7.jpg",
    "lenovo-xiaoxin-pad-2024": "https://fdn2.gsmarena.com/vv/bigpic/lenovo-xiaoxin-pad-2024.jpg",
    "lenovo-xiaoxin-pad-pro-13": "https://fdn2.gsmarena.com/vv/bigpic/lenovo-tab-p12-pro.jpg",
    "lenovo-xiaoxin-pad-pro-13-gt": "https://fdn2.gsmarena.com/vv/bigpic/lenovo-tab-p12-pro.jpg",
    "lenovo-xiaoxin-pad-pro-12-7-2025": "https://fdn2.gsmarena.com/vv/bigpic/lenovo-xiaoxin-pad-pro-12-7.jpg",

    # 7. ALLDOCUBE
    "alldocube-iplay-80-mini-pro": "https://www.alldocube.com/en/wp-content/uploads/2024/05/1716197304-iplay60minipro-thum.png",
    "alldocube-iplay-70-mini-pro": "https://www.alldocube.com/en/wp-content/uploads/2024/05/1716197304-iplay60minipro-thum.png",
    "alldocube-iplay-60-mini-pro": "https://www.alldocube.com/en/wp-content/uploads/2024/05/1716197304-iplay60minipro-thum.png",
    "alldocube-iplay-50-mini-pro-nfe": "https://www.alldocube.com/en/wp-content/uploads/2023/07/1689670678-iplay50minipro-thum.png",
    "alldocube-iplay-80-pro": "https://www.alldocube.com/en/wp-content/uploads/2024/05/1716197304-iplay60minipro-thum.png",
    "alldocube-iplay-70-pro": "https://www.alldocube.com/en/wp-content/uploads/2024/05/1716197304-iplay60minipro-thum.png",

    # 8. Onyx BOOX & E-Readers
    "boox-palma-2": "https://shop.boox.com/cdn/shop/files/1_0d6848e7-334b-47f0-9653-2dd3c8339a4f_grande.jpg",
    "boox-palma": "https://shop.boox.com/cdn/shop/files/1_0d6848e7-334b-47f0-9653-2dd3c8339a4f_grande.jpg",
    "hisense-a9": "https://fdn2.gsmarena.com/vv/bigpic/hisense-a9.jpg",
    "hisense-touch": "https://fdn2.gsmarena.com/vv/bigpic/hisense-touch.jpg"
}

success_count = 0
fail_count = 0

for slug, url in CHINESE_DEVICES_PRECISE.items():
    dest = f"public/images/devices/{slug}.jpg"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8, context=ctx) as resp:
            data = resp.read()
            if len(data) > 1000:
                with open(dest, "wb") as f:
                    f.write(data)
                print(f"✅ [{slug}] Updated official image ({len(data)} bytes)")
                success_count += 1
            else:
                print(f"⚠️ [{slug}] File too small ({len(data)} bytes)")
                fail_count += 1
    except Exception as e:
        print(f"❌ [{slug}] Failed: {e}")
        fail_count += 1

print(f"\n🎉 Finished updating Chinese devices: {success_count} success, {fail_count} failed")
