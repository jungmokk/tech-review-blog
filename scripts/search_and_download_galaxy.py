import urllib.request
import urllib.parse
import json
import re
import subprocess
import os

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
}

def get_vqd(query):
    url = f"https://duckduckgo.com/?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as r:
        html = r.read().decode("utf-8")
        match = re.search(r"vqd=([\d-]+)&", html) or re.search(r'vqd="([\d-]+)"', html)
        if match:
            return match.group(1)
    return None

def fetch_first_image(query):
    vqd = get_vqd(query)
    if not vqd:
        print(f"❌ Failed to get vqd token for {query}")
        return None
    api = f"https://duckduckgo.com/i.js?l=us-en&o=json&q={urllib.parse.quote(query)}&vqd={vqd}&f=,,,"
    req = urllib.request.Request(api, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read().decode("utf-8"))
        results = data.get("results", [])
        for res in results[:5]:
            img_url = res.get("image")
            if img_url and ("samsung" in img_url or "fold" in img_url or "galaxy" in img_url or "cdn" in img_url):
                return img_url
        if results:
            return results[0].get("image")
    return None

TARGETS = {
    "galaxy-z-fold8": "Samsung Galaxy Z Fold 8 official press render",
    "galaxy-z-flip8": "Samsung Galaxy Z Flip 8 official press render",
    "galaxy-s26-ultra": "Samsung Galaxy S26 Ultra official titanium press render",
    "galaxy-s25-ultra": "Samsung Galaxy S25 Ultra official press render titanium",
}

for dev_id, q in TARGETS.items():
    print(f"🔍 Searching image for [{dev_id}] with query: '{q}'...")
    img_url = fetch_first_image(q)
    if img_url:
        print(f"👉 Found URL: {img_url}")
        try:
            req = urllib.request.Request(img_url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
                raw_temp = f"public/images/devices/{dev_id}_raw.tmp"
                webp_out = f"public/images/devices/{dev_id}.webp"
                jpg_out = f"public/images/devices/{dev_id}.jpg"
                with open(raw_temp, "wb") as f:
                    f.write(data)
                subprocess.run(["/opt/homebrew/bin/cwebp", "-q", "90", "-resize", "800", "0", raw_temp, "-o", webp_out], check=True)
                with open(jpg_out, "wb") as f:
                    f.write(data)
                if os.path.exists(raw_temp):
                    os.remove(raw_temp)
                print(f"✅ [{dev_id}] Successfully saved {os.path.getsize(webp_out)} bytes WebP!")
        except Exception as e:
            print(f"❌ Failed to download {img_url}: {e}")
    else:
        print(f"⚠️ No image found for {dev_id}")
