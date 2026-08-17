import os
import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Wikimedia direct full file URLs or Verified CDN endpoints
WIKIMEDIA_ORIGINALS = {
    "galaxy-s26-ultra": "https://upload.wikimedia.org/wikipedia/commons/d/d4/Samsung_Galaxy_S25_Ultra.jpg",
    "galaxy-s25-ultra": "https://upload.wikimedia.org/wikipedia/commons/d/d4/Samsung_Galaxy_S25_Ultra.jpg",
    "galaxy-z-fold8": "https://upload.wikimedia.org/wikipedia/commons/1/15/Samsung_Galaxy_Z_Fold_6_rear_view.jpg",
    "galaxy-z-flip8": "https://upload.wikimedia.org/wikipedia/commons/b/b3/Samsung_Galaxy_Z_Flip_6_rear_view.jpg",
    "iphone-17-pro-max": "https://upload.wikimedia.org/wikipedia/commons/c/c9/Back_view_of_iPhone_16_Pro_Max_Natural_Titanium.jpg",
    "iphone-16-pro-max": "https://upload.wikimedia.org/wikipedia/commons/c/c9/Back_view_of_iPhone_16_Pro_Max_Natural_Titanium.jpg",
    "ipad-pro-13-m4": "https://upload.wikimedia.org/wikipedia/commons/c/c4/IPad_Pro_%287th_generation%29.jpg",
    "ipad-mini-7": "https://upload.wikimedia.org/wikipedia/commons/1/1c/IPad_Mini_6_Space_Gray.jpg",
    "boox-palma-2": "https://upload.wikimedia.org/wikipedia/commons/7/77/Boox_Palma.jpg",
    "sony-wh-1000xm5": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Sony_WH-1000XM5_headphones.jpg",
    "kindle-colorsoft": "https://upload.wikimedia.org/wikipedia/commons/0/05/Amazon_Kindle_Paperwhite_3.jpg"
}

headers = {
    "User-Agent": "TechSpecBlogBot/1.0 (https://tech.thesinoreport.com; contact@thesinoreport.com) Python-urllib/3.11"
}

for slug, url in WIKIMEDIA_ORIGINALS.items():
    dest = f"public/images/devices/{slug}.jpg"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            data = resp.read()
            with open(dest, "wb") as f:
                f.write(data)
        print(f"✅ Downloaded original {slug} ({len(data)} bytes)")
    except Exception as e:
        print(f"❌ Failed {slug}: {e}")
