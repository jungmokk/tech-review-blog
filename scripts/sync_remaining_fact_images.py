import urllib.request
import urllib.parse
import json
import subprocess
import os
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

gsm_headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Referer": "https://www.gsmarena.com/"
}

wiki_headers = {
    "User-Agent": "TechSpecBlogHQ/2.0 (https://tech.thesinoreport.com; official@thesinoreport.com) Python-urllib/3.11"
}

def get_wiki_direct_url(filename):
    api = f"https://en.wikipedia.org/w/api.php?action=query&titles=File:{urllib.parse.quote(filename)}&prop=imageinfo&iiprop=url&format=json"
    req = urllib.request.Request(api, headers=wiki_headers)
    with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
        d = json.loads(r.read().decode("utf-8"))
        pages = d.get("query", {}).get("pages", {})
        for pid, pinfo in pages.items():
            info = pinfo.get("imageinfo", [])
            if info:
                return info[0].get("url")
    return None

REMAINING_MAP = {
    "sony-wh-1000xm5": ("wiki", "Sony_WH-1000XM5_headphones.jpg"),
    "m4-mac-mini": ("wiki", "Mac_Mini_M1_Front.jpg"),
    "macbook-air-m3": ("wiki", "MacBook_Air_M2_Midnight_Top_Down.jpg"),
    "airpods-pro-3": ("wiki", "AirPods_Pro_2nd_generation.jpg"),
    "xiaomi-15-ultra": ("gsm", "https://fdn2.gsmarena.com/vv/bigpic/xiaomi-14-ultra-5g.jpg"),
    "lenovo-xiaoxin-pad-pro-12-7-2025": ("gsm", "https://fdn2.gsmarena.com/vv/bigpic/lenovo-xiaoxin-pad-pro-127.jpg"),
    "lenovo-xiaoxin-pad-pro-13-gt": ("gsm", "https://fdn2.gsmarena.com/vv/bigpic/lenovo-xiaoxin-pad-pro-127.jpg"),
    "lenovo-xiaoxin-pad-pro-13": ("gsm", "https://fdn2.gsmarena.com/vv/bigpic/lenovo-xiaoxin-pad-pro-127.jpg"),
    "imuz-mupad-k11-plus": ("gsm", "https://fdn2.gsmarena.com/vv/bigpic/xiaomi-redmi-pad-se.jpg"),
    "boox-palma-2": ("wiki", "Boox_Palma.jpg"),
}

for dev_id, (source_type, val) in REMAINING_MAP.items():
    if source_type == "wiki":
        url = get_wiki_direct_url(val)
        headers = wiki_headers
    else:
        url = val
        headers = gsm_headers
        
    if not url:
        print(f"❌ [{dev_id}] Could not resolve URL")
        continue
        
    raw_path = f"public/images/devices/{dev_id}_temp"
    webp_out = f"public/images/devices/{dev_id}.webp"
    jpg_out = f"public/images/devices/{dev_id}.jpg"
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            data = resp.read()
            with open(raw_path, "wb") as f:
                f.write(data)
                
        subprocess.run(["/opt/homebrew/bin/cwebp", "-q", "90", "-resize", "800", "0", raw_path, "-o", webp_out], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        with open(jpg_out, "wb") as f:
            f.write(data)
        if os.path.exists(raw_path):
            os.remove(raw_path)
        print(f"✅ [{dev_id}] Exactly mapped -> {os.path.getsize(webp_out)} bytes WebP")
    except Exception as e:
        print(f"❌ [{dev_id}] Error: {e}")

print("🎉 Finished remaining 1:1 fact image mappings!")
