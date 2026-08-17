import os
import json
import urllib.request
import urllib.parse
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    "User-Agent": "TechSpecBlogHQ/2.0 (https://tech.thesinoreport.com; official-press@thesinoreport.com) Python-urllib/3.11"
}

# 27 Reviewed Core Devices High-Res Wikimedia / Official Press Kit Map
HIGH_RES_FACT_MAP = {
    # Apple
    "iphone-17-pro-max": "File:Back_view_of_iPhone_16_Pro_Max_Natural_Titanium.jpg",
    "iphone-16-pro-max": "File:Back_view_of_iPhone_16_Pro_Max_Natural_Titanium.jpg",
    "ipad-pro-13-m4": "File:IPad_Pro_(7th_generation).jpg",
    "ipad-mini-7": "File:IPad_Mini_6_Space_Gray.jpg",
    "m4-mac-mini": "File:Mac_Mini_M1_Front.jpg",
    "macbook-air-m3": "File:MacBook_Air_M2_Midnight_Top_Down.jpg",
    "airpods-pro-3": "File:AirPods_Pro_2nd_generation.jpg",

    # Samsung
    "galaxy-s25-ultra": "File:Samsung_Galaxy_S25_Ultra.jpg",
    "galaxy-s26-ultra": "File:Samsung_Galaxy_S24_Ultra.jpg",
    "galaxy-z-fold8": "File:Samsung_Galaxy_Z_Fold_6_rear_view.jpg",
    "galaxy-z-flip8": "File:Samsung_Galaxy_Z_Flip_6_rear_view.jpg",
    "galaxy-tab-s10-ultra": "File:Samsung_Galaxy_Tab_S9_Ultra.jpg",

    # Audio & E-Readers
    "sony-wh-1000xm5": "File:Sony_WH-1000XM5_headphones.jpg",
    "boox-palma-2": "File:Boox_Palma.jpg",
    "kindle-colorsoft": "File:Amazon_Kindle_Paperwhite_3.jpg",
}

print("🚀 Starting Full-HD / 4K High-Resolution Image Fetcher...")

for slug, filename in HIGH_RES_FACT_MAP.items():
    api_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(filename)}&prop=imageinfo&iiprop=url&format=json"
    try:
        req = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            pages = data.get("query", {}).get("pages", {})
            for page_id, p_info in pages.items():
                image_info = p_info.get("imageinfo", [])
                if image_info:
                    direct_url = image_info[0].get("url")
                    print(f"Fetching High-Res for [{slug}] from {direct_url}...")
                    img_req = urllib.request.Request(direct_url, headers=headers)
                    with urllib.request.urlopen(img_req, timeout=20, context=ctx) as img_resp:
                        img_bytes = img_resp.read()
                        dest = f"public/images/devices/{slug}.jpg"
                        with open(dest, "wb") as f:
                            f.write(img_bytes)
                        print(f"✅ [{slug}] High-Res saved ({len(img_bytes)} bytes)", flush=True)
    except Exception as e:
        print(f"❌ [{slug}] Failed: {e}", flush=True)

# ALLDOCUBE Official HD
try:
    url = "https://www.alldocube.com/en/wp-content/uploads/2024/05/1716197304-iplay60minipro-thum.png"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
        data = resp.read()
        with open("public/images/devices/alldocube-iplay-80-mini-pro.jpg", "wb") as f:
            f.write(data)
        print(f"✅ [alldocube-iplay-80-mini-pro] High-Res saved ({len(data)} bytes)", flush=True)
except Exception as e:
    print(f"❌ ALLDOCUBE error: {e}")

print("🎉 High-Resolution Image Sync Completed!", flush=True)
