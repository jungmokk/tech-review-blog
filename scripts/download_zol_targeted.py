import urllib.request
import urllib.parse
import json
import re
import subprocess
import os
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
}

# Accurate Chinese Devices for ZOL Search
ZOL_MAP = {
    "xiaomi-15-ultra": "小米15 Ultra site:zol.com.cn OR site:zol-img.com.cn",
    "xiaomi-pad-7-pro": "小米平板7 Pro site:zol.com.cn OR site:zol-img.com.cn",
    "vivo-x200-pro": "vivo X200 Pro site:zol.com.cn OR site:zol-img.com.cn",
    "huawei-mate-xt": "华为 Mate XT site:zol.com.cn OR site:zol-img.com.cn",
    "lenovo-legion-y700-2024": "拯救者 Y700 2024 site:zol.com.cn OR site:zol-img.com.cn",
    "lenovo-xiaoxin-pad-pro-12-7-2025": "小新 Pad Pro 12.7 2025 site:zol.com.cn OR site:zol-img.com.cn",
    "lenovo-xiaoxin-pad-pro-13-gt": "小新 Pad Pro 13 site:zol.com.cn OR site:zol-img.com.cn",
    "lenovo-xiaoxin-pad-pro-13": "小新 Pad Pro 13 site:zol.com.cn OR site:zol-img.com.cn",
    "oppo-pad-3-pro": "OPPO Pad 3 Pro site:zol.com.cn OR site:zol-img.com.cn",
    "alldocube-iplay-80-mini-pro": "酷比魔方 iPlay 60 mini Pro site:zol.com.cn OR site:zol-img.com.cn",
    "boox-palma-2": "文石 BOOX Palma site:zol.com.cn OR site:zol-img.com.cn",
    "imuz-mupad-k11-plus": "Redmi Pad SE 8.7 site:zol.com.cn OR site:zol-img.com.cn",
    "iflytek-air-2": "科大讯飞 智能办公本 Air 2 site:zol.com.cn OR site:zol-img.com.cn",
    "honor-magic-7-pro": "荣耀 Magic7 Pro site:zol.com.cn OR site:zol-img.com.cn",
    "honor-magic-v3": "荣耀 Magic V3 site:zol.com.cn OR site:zol-img.com.cn",
    "oneplus-13": "一加 13 site:zol.com.cn OR site:zol-img.com.cn",
    "oneplus-open": "一加 Open site:zol.com.cn OR site:zol-img.com.cn",
    "oppo-find-x8-pro": "OPPO Find X8 Pro site:zol.com.cn OR site:zol-img.com.cn",
    "vivo-x-fold3-pro": "vivo X Fold3 Pro site:zol.com.cn OR site:zol-img.com.cn",
    "xiaomi-15": "小米15 site:zol.com.cn OR site:zol-img.com.cn",
    "xiaomi-mix-flip": "小米 MIX Flip site:zol.com.cn OR site:zol-img.com.cn",
    "xiaomi-mix-fold-4": "小米 MIX Fold 4 site:zol.com.cn OR site:zol-img.com.cn",
    "huawei-pura-70-ultra": "华为 Pura 70 Ultra site:zol.com.cn OR site:zol-img.com.cn",
}

print(f"🇨🇳 Ingesting high-definition product images directly from ZOL (中关村在线) database...")

for dev_id, query in ZOL_MAP.items():
    # Fetch via Yahoo/Bing Image scraper with ZOL focus
    try:
        url = f"https://www.bing.com/images/async?q={urllib.parse.quote(query)}&first=1&count=10&mmasync=1"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
            # Extract murl from Bing Image result JSON
            murls = re.findall(r'murl&quot;:&quot;(https?://[^&]+)&quot;', html)
            zol_murls = [u for u in murls if "zol-img.com.cn" in u] or murls
            
            if zol_murls:
                target_url = zol_murls[0]
                print(f"🎯 [{dev_id}] Found ZOL image: {target_url}")
                
                img_req = urllib.request.Request(target_url, headers=headers)
                with urllib.request.urlopen(img_req, timeout=15) as img_resp:
                    data = img_resp.read()
                    raw_tmp = f"public/images/devices/{dev_id}_zol.tmp"
                    webp_out = f"public/images/devices/{dev_id}.webp"
                    jpg_out = f"public/images/devices/{dev_id}.jpg"
                    
                    with open(raw_tmp, "wb") as f:
                        f.write(data)
                        
                    subprocess.run(["/opt/homebrew/bin/cwebp", "-q", "90", "-resize", "800", "0", raw_tmp, "-o", webp_out], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                    with open(jpg_out, "wb") as f:
                        f.write(data)
                    if os.path.exists(raw_tmp):
                        os.remove(raw_tmp)
                        
                    print(f"✅ [{dev_id}] Saved ZOL verified photo -> {os.path.getsize(webp_out)} bytes WebP!\n")
            else:
                print(f"⚠️ No ZOL image result for {dev_id}\n")
        time.sleep(0.3)
    except Exception as e:
        print(f"❌ Error for {dev_id}: {e}\n")

print("🎉 Completed ZOL Chinese Device Image Ingestion!")
