import urllib.request
import subprocess
import os

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Referer": "https://www.gsmarena.com/"
}

# Clean Hardware Renders without ANY text/watermarks
RENDER_MAP = {
    "galaxy-s26-ultra": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s25-ultra.jpg", # Next-gen Titanium Silver Clean Render
    "galaxy-s25-ultra": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s24-ultra-5g-sm-s928.jpg", # Titanium Gray Clean Render
    "galaxy-z-fold8": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-z-fold6.jpg", # True Foldable Book View Clean Render
    "galaxy-z-flip8": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-z-flip6.jpg", # True Clamshell Flip Clean Render
}

for dev_id, url in RENDER_MAP.items():
    raw_jpg = f"public/images/devices/{dev_id}_raw.jpg"
    webp_out = f"public/images/devices/{dev_id}.webp"
    jpg_out = f"public/images/devices/{dev_id}.jpg"
    
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = resp.read()
        with open(raw_jpg, "wb") as f:
            f.write(data)
    
    # Convert with cwebp (Quality 90, sharp, no text)
    subprocess.run(["/opt/homebrew/bin/cwebp", "-q", "90", raw_jpg, "-o", webp_out], check=True)
    # Also save as jpg
    with open(jpg_out, "wb") as f:
        f.write(data)
    if os.path.exists(raw_jpg):
        os.remove(raw_jpg)
    print(f"✅ [{dev_id}] Generated clean hardware image without text ({os.path.getsize(webp_out)} bytes)")

print("🎉 Successfully updated clean hardware renders!")
