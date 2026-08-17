import urllib.request
import urllib.parse
import re
import json
import subprocess
import os
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Referer": "https://mobile.zol.com.cn/pics/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

# Mapping of all 27 active review devices & top Chinese database devices to ZOL search queries
ZOL_MODELS = {
    # Active Reviews
    "xiaomi-15-ultra": "小米 15 Ultra",
    "xiaomi-pad-7-pro": "小米平板 7 Pro",
    "vivo-x200-pro": "vivo X200 Pro",
    "huawei-mate-xt": "华为 Mate XT",
    "lenovo-legion-y700-2024": "联想 拯救者 Y700",
    "lenovo-xiaoxin-pad-pro-12-7-2025": "联想 小新 Pad Pro 12.7",
    "lenovo-xiaoxin-pad-pro-13-gt": "联想 小新 Pad Pro 13",
    "lenovo-xiaoxin-pad-pro-13": "联想 小新 Pad Pro 13",
    "oppo-pad-3-pro": "OPPO Pad 3 Pro",
    "alldocube-iplay-80-mini-pro": "酷比魔方 iPlay 60 mini Pro",
    "boox-palma-2": "文石 BOOX Palma",
    "imuz-mupad-k11-plus": "红米 Redmi Pad SE",
    "iflytek-air-2": "科大讯飞 智能办公本 Air 2",

    # Major Chinese Flagships
    "honor-magic-7-pro": "荣耀 Magic7 Pro",
    "honor-magic-v3": "荣耀 Magic V3",
    "honor-magic-6-pro": "荣耀 Magic6 Pro",
    "oneplus-13": "一加 13",
    "oneplus-12": "一加 12",
    "oneplus-open": "一加 Open",
    "oneplus-pad-2": "一加平板 2",
    "oppo-find-x8-pro": "OPPO Find X8 Pro",
    "oppo-find-x8": "OPPO Find X8",
    "oppo-find-x7-ultra": "OPPO Find X7 Ultra",
    "vivo-x-fold3-pro": "vivo X Fold3 Pro",
    "vivo-x100-ultra": "vivo X100 Ultra",
    "xiaomi-15": "小米 15",
    "xiaomi-15-pro": "小米 15 Pro",
    "xiaomi-14-ultra": "小米 14 Ultra",
    "xiaomi-mix-flip": "小米 MIX Flip",
    "xiaomi-mix-fold-4": "小米 MIX Fold 4",
    "xiaomi-pad-6s-pro": "小米平板 6S Pro",
    "huawei-pura-70-ultra": "华为 Pura 70 Ultra",
    "huawei-mate-60-pro": "华为 Mate 60 Pro",
    "iqoo-13": "iQOO 13",
    "redmi-k80-pro": "Redmi K80 Pro",
    "redmi-note-14-pro-plus": "Redmi Note 14 Pro+",
}

def search_zol_product_image(query):
    # Search ZOL search page
    search_url = f"https://detail.zol.com.cn/index.php?c=SearchList&kword={urllib.parse.quote(query.encode('gbk'))}"
    try:
        req = urllib.request.Request(search_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("gbk", errors="ignore")
            # Extract first high-res product image (change 320x240 or 100x75 to 800x600 for HD)
            imgs = re.findall(r'src=[\'"](https?://[^\'"]+zol-img\.com\.cn/[^\'"]+)[\'"]', html)
            for img in imgs:
                if "/product/" in img:
                    # Upgrade to 800x600 high res
                    hd_img = re.sub(r'_\d+x\d+/', '_800x600/', img)
                    return hd_img
    except Exception as e:
        pass
    return None

print(f"🇨🇳 Starting ZOL (mobile.zol.com.cn) Official Photo Sync for {len(ZOL_MODELS)} devices...\n")

success_count = 0

for dev_id, query in ZOL_MODELS.items():
    print(f"🔍 Searching ZOL for [{dev_id}] ({query})...")
    zol_img = search_zol_product_image(query)
    
    if zol_img:
        print(f"👉 Found ZOL HD Photo: {zol_img}")
        try:
            req = urllib.request.Request(zol_img, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
                raw_tmp = f"public/images/devices/{dev_id}_zol.tmp"
                webp_out = f"public/images/devices/{dev_id}.webp"
                jpg_out = f"public/images/devices/{dev_id}.jpg"
                
                with open(raw_tmp, "wb") as f:
                    f.write(data)
                    
                # Convert to WebP 800px max width, quality 90
                subprocess.run(["/opt/homebrew/bin/cwebp", "-q", "90", "-resize", "800", "0", raw_tmp, "-o", webp_out], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                with open(jpg_out, "wb") as f:
                    f.write(data)
                if os.path.exists(raw_tmp):
                    os.remove(raw_tmp)
                    
                print(f"✅ [{dev_id}] Successfully updated with ZOL official photo ({os.path.getsize(webp_out)} bytes WebP)!\n")
                success_count += 1
        except Exception as e:
            print(f"❌ Failed to download {zol_img}: {e}\n")
    else:
        print(f"⚠️ No ZOL match found for {query}\n")
    time.sleep(0.2)

print(f"🎉 Successfully synced {success_count} Chinese device official photos directly from ZOL!")
