import urllib.request
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

# 1. Targets to match from ZOL
TARGET_MATCHES = {
    "xiaomi-15-ultra": ["小米15", "小米 15", "Xiaomi 15"],
    "xiaomi-pad-7-pro": ["小米平板7", "小米平板 7", "Pad 7 Pro"],
    "vivo-x200-pro": ["vivo X200", "vivo X200 Pro"],
    "huawei-mate-xt": ["Mate XT", "华为Mate XT"],
    "lenovo-legion-y700-2024": ["Y700", "拯救者 Y700", "Legion Y700"],
    "lenovo-xiaoxin-pad-pro-12-7-2025": ["小新 Pad Pro 12.7", "小新Pad Pro 12.7", "小新Pad Pro"],
    "lenovo-xiaoxin-pad-pro-13-gt": ["小新 Pad Pro 13", "小新Pad Pro 13"],
    "lenovo-xiaoxin-pad-pro-13": ["小新 Pad Pro 13", "小新Pad Pro 13"],
    "oppo-pad-3-pro": ["OPPO Pad 3", "OPPO Pad 3 Pro"],
    "alldocube-iplay-80-mini-pro": ["酷比魔方", "iPlay 60", "iPlay 50"],
    "boox-palma-2": ["文石", "Palma", "BOOX"],
    "imuz-mupad-k11-plus": ["Redmi Pad SE", "红米 Pad SE"],
    "iflytek-air-2": ["讯飞", "智能办公本 Air"],
    "honor-magic-7-pro": ["Magic7", "Magic 7 Pro", "荣耀 Magic7"],
    "honor-magic-v3": ["Magic V3", "荣耀 Magic V3"],
    "oneplus-13": ["一加 13", "OnePlus 13", "一加13"],
    "oneplus-open": ["一加 Open", "OnePlus Open"],
    "oppo-find-x8-pro": ["Find X8 Pro", "OPPO Find X8"],
    "oppo-find-x8": ["Find X8", "OPPO Find X8"],
    "vivo-x-fold3-pro": ["X Fold3", "vivo X Fold3"],
    "xiaomi-15": ["小米15", "小米 15"],
    "xiaomi-15-pro": ["小米15 Pro", "小米 15 Pro"],
    "xiaomi-mix-flip": ["MIX Flip", "小米 MIX Flip"],
    "xiaomi-mix-fold-4": ["MIX Fold 4", "小米 MIX Fold 4"],
    "huawei-pura-70-ultra": ["Pura 70", "华为 Pura 70"],
    "huawei-mate-60-pro": ["Mate 60 Pro", "华为 Mate 60"],
    "iqoo-13": ["iQOO 13", "iQOO13"],
    "redmi-k80-pro": ["Redmi K80", "红米 K80"],
}

print("🚀 Step 1: Loading product detail links from ZOL portal snapshot...")

content_file = "/Users/kazisis/.gemini/antigravity-ide/brain/d1531a6a-c6fd-4c64-adc2-e96f8505f1fb/.system_generated/steps/3110/content.md"
product_links = set()

if os.path.exists(content_file):
    with open(content_file, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
        found = re.findall(r'https?://detail\.zol\.com\.cn/(?:cell_phone|tablepc)/index\d+\.shtml', text)
        for p in found:
            product_links.add(p)

print(f"✅ Loaded {len(product_links)} ZOL product candidate links!\n")

print("🚀 Step 2: Scanning products and matching with our device database...")

matched_count = 0

for p_url in list(product_links)[:60]:
    try:
        req = urllib.request.Request(p_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("gbk", errors="ignore")
            title_m = re.search(r'<h1[^>]*>([^<]+)</h1>', html)
            title = title_m.group(1).strip() if title_m else ""
            if not title:
                continue
                
            # Check match against our target list
            for slug, keywords in TARGET_MATCHES.items():
                if any(kw.lower() in title.lower() for kw in keywords):
                    # Found match! Extract main product image
                    imgs = re.findall(r'<img[^>]+src=[\'"](https?://[^\'"]+zol-img\.com\.cn/[^\'"]+)[\'"]', html)
                    product_imgs = [img for img in imgs if "/product/" in img]
                    if product_imgs:
                        raw_img_url = product_imgs[0]
                        # Upgrade resolution to 800x600
                        hd_img_url = re.sub(r'_\d+x\d+/', '_800x600/', raw_img_url)
                        print(f"🎯 MATCHED! [{slug}] -> ZOL Product: {title}")
                        print(f"📸 Downloading ZOL HD Image: {hd_img_url}")
                        
                        img_req = urllib.request.Request(hd_img_url, headers=headers)
                        with urllib.request.urlopen(img_req, timeout=15) as img_resp:
                            data = img_resp.read()
                            raw_tmp = f"public/images/devices/{slug}_zol.tmp"
                            webp_out = f"public/images/devices/{slug}.webp"
                            jpg_out = f"public/images/devices/{slug}.jpg"
                            
                            with open(raw_tmp, "wb") as f:
                                f.write(data)
                            subprocess.run(["/opt/homebrew/bin/cwebp", "-q", "90", "-resize", "800", "0", raw_tmp, "-o", webp_out], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                            with open(jpg_out, "wb") as f:
                                f.write(data)
                            if os.path.exists(raw_tmp):
                                os.remove(raw_tmp)
                            print(f"✅ [{slug}] Successfully saved {os.path.getsize(webp_out)} bytes WebP!\n")
                            matched_count += 1
                            break
        time.sleep(0.1)
    except Exception as e:
        pass

print(f"\n🎉 ZOL Official Photo Ingestion Completed: {matched_count} devices updated!")
