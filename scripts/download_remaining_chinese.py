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

REMAINING_CHINESE = {
    # 1. Huawei / Honor
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

    # 2. OnePlus / Nothing
    "oneplus-11": "https://fdn2.gsmarena.com/vv/bigpic/oneplus-11.jpg",
    "oneplus-open": "https://fdn2.gsmarena.com/vv/bigpic/oneplus-open.jpg",
    "oneplus-pad-2": "https://fdn2.gsmarena.com/vv/bigpic/oneplus-pad2.jpg",
    "oneplus-watch-2": "https://fdn2.gsmarena.com/vv/bigpic/oneplus-watch-2.jpg",
    "nothing-phone-3": "https://fdn2.gsmarena.com/vv/bigpic/nothing-phone-2.jpg",
    "nothing-phone-2a-plus": "https://fdn2.gsmarena.com/vv/bigpic/nothing-phone-2a-plus.jpg",
    "nothing-phone-2a": "https://fdn2.gsmarena.com/vv/bigpic/nothing-phone-2a.jpg",
    "nothing-phone-2": "https://fdn2.gsmarena.com/vv/bigpic/nothing-phone-2.jpg",

    # 3. Lenovo
    "lenovo-legion-y700-2024": "https://fdn2.gsmarena.com/vv/bigpic/lenovo-legion-tab-gen-3.jpg",
    "lenovo-legion-y700-2023": "https://fdn2.gsmarena.com/vv/bigpic/lenovo-legion-y700-2023.jpg",
    "lenovo-xiaoxin-pad-pro-12-7-2023": "https://fdn2.gsmarena.com/vv/bigpic/lenovo-xiaoxin-pad-pro-12-7.jpg",
    "lenovo-xiaoxin-pad-2024": "https://fdn2.gsmarena.com/vv/bigpic/lenovo-xiaoxin-pad-2024.jpg",
    "lenovo-xiaoxin-pad-pro-13": "https://fdn2.gsmarena.com/vv/bigpic/lenovo-tab-p12-pro.jpg",
    "lenovo-xiaoxin-pad-pro-13-gt": "https://fdn2.gsmarena.com/vv/bigpic/lenovo-tab-p12-pro.jpg",
    "lenovo-xiaoxin-pad-pro-12-7-2025": "https://fdn2.gsmarena.com/vv/bigpic/lenovo-xiaoxin-pad-pro-12-7.jpg",

    # 4. Hisense
    "hisense-a9": "https://fdn2.gsmarena.com/vv/bigpic/hisense-a9.jpg",
    "hisense-touch": "https://fdn2.gsmarena.com/vv/bigpic/hisense-touch.jpg"
}

for slug, url in REMAINING_CHINESE.items():
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

print("🎉 Completed remaining downloads!", flush=True)
