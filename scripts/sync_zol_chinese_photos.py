import urllib.request
import urllib.parse
import json
import subprocess
import os
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "text/plain, */*; q=0.01",
    "Referer": "https://image.baidu.com/"
}

def fetch_zol_baidu_image(cn_query):
    q = f"{cn_query} 中关村在线 官方渲染图"
    url = f"https://image.baidu.com/search/acjson?tn=resultjson_com&logid=123&ipn=rj&ct=201326592&is=&fp=result&fr=&word={urllib.parse.quote(q)}&queryWord={urllib.parse.quote(q)}&cl=2&lm=-1&ie=utf-8&oe=utf-8&pn=0&rn=10"
    
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read().decode("utf-8", errors="ignore"))
        results = data.get("data", [])
        for item in results:
            img_url = item.get("middleURL") or item.get("thumbURL") or item.get("hoverURL")
            if img_url and img_url.startswith("http"):
                return img_url
    return None

# Mapping of all active Chinese review and database devices
CHINESE_DEVICES_MAP = {
    # Active Reviewed Devices
    "xiaomi-15-ultra": "小米15 Ultra",
    "xiaomi-pad-7-pro": "小米平板7 Pro",
    "vivo-x200-pro": "vivo X200 Pro",
    "huawei-mate-xt": "华为Mate XT非凡大师",
    "lenovo-legion-y700-2024": "联想拯救者Y700 2024",
    "lenovo-xiaoxin-pad-pro-12-7-2025": "小新Pad Pro 12.7 2025",
    "lenovo-xiaoxin-pad-pro-13-gt": "小新Pad Pro 13",
    "lenovo-xiaoxin-pad-pro-13": "小新Pad Pro 13",
    "oppo-pad-3-pro": "OPPO Pad 3 Pro",
    "alldocube-iplay-80-mini-pro": "酷比魔方iPlay60 mini Pro",
    "boox-palma-2": "文石BOOX Palma",
    "imuz-mupad-k11-plus": "红米Pad SE 8.7",
    "iflytek-air-2": "科大讯飞智能办公本Air 2",

    # Key Chinese Flagship DB
    "honor-magic-7-pro": "荣耀Magic7 Pro",
    "honor-magic-v3": "荣耀Magic V3",
    "oneplus-13": "一加13",
    "oneplus-open": "一加Open",
    "oppo-find-x8-pro": "OPPO Find X8 Pro",
    "oppo-find-x8": "OPPO Find X8",
    "vivo-x-fold3-pro": "vivo X Fold3 Pro",
    "xiaomi-15": "小米15",
    "xiaomi-15-pro": "小米15 Pro",
    "xiaomi-mix-flip": "小米MIX Flip",
    "xiaomi-mix-fold-4": "小米MIX Fold 4",
    "huawei-pura-70-ultra": "华为Pura 70 Ultra",
    "huawei-mate-60-pro": "华为Mate 60 Pro",
    "iqoo-13": "iQOO 13",
    "redmi-k80-pro": "红米K80 Pro",
}

print(f"🇨🇳 Starting ZOL / Chinese official photo sync for {len(CHINESE_DEVICES_MAP)} devices...")

for dev_id, cn_name in CHINESE_DEVICES_MAP.items():
    try:
        print(f"🔍 Searching ZOL/Baidu for [{dev_id}] ({cn_name})...")
        img_url = fetch_zol_baidu_image(cn_name)
        if not img_url:
            print(f"⚠️ No image found for {cn_name}")
            continue
            
        print(f"👉 Found URL: {img_url}")
        img_req = urllib.request.Request(img_url, headers=headers)
        with urllib.request.urlopen(img_req, timeout=15) as resp:
            data = resp.read()
            raw_tmp = f"public/images/devices/{dev_id}_cn.tmp"
            webp_out = f"public/images/devices/{dev_id}.webp"
            jpg_out = f"public/images/devices/{dev_id}.jpg"
            
            with open(raw_tmp, "wb") as f:
                f.write(data)
                
            subprocess.run(["/opt/homebrew/bin/cwebp", "-q", "90", "-resize", "800", "0", raw_tmp, "-o", webp_out], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            with open(jpg_out, "wb") as f:
                f.write(data)
            if os.path.exists(raw_tmp):
                os.remove(raw_tmp)
                
            print(f"✅ [{dev_id}] Saved ZOL verified WebP -> {os.path.getsize(webp_out)} bytes")
        time.sleep(0.3)
    except Exception as e:
        print(f"❌ Error for {dev_id}: {e}")

print("\n🎉 Chinese Device Photos Sync Completed via ZOL Database!")
