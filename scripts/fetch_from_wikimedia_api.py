import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    "User-Agent": "TechReviewBot/1.0 (https://tech.thesinoreport.com; contact@thesinoreport.com)"
}

WIKIMEDIA_FILES = {
    "galaxy-s26-ultra": "File:Samsung_Galaxy_S25_Ultra.jpg",
    "galaxy-s25-ultra": "File:Samsung_Galaxy_S25_Ultra.jpg",
    "galaxy-z-fold8": "File:Samsung_Galaxy_Z_Fold_6_rear_view.jpg",
    "galaxy-z-flip8": "File:Samsung_Galaxy_Z_Flip_6_rear_view.jpg",
    "iphone-17-pro-max": "File:Back_view_of_iPhone_16_Pro_Max_Natural_Titanium.jpg",
    "iphone-16-pro-max": "File:Back_view_of_iPhone_16_Pro_Max_Natural_Titanium.jpg",
    "ipad-pro-13-m4": "File:IPad_Pro_(7th_generation).jpg",
    "ipad-mini-7": "File:IPad_Mini_6_Space_Gray.jpg",
    "boox-palma-2": "File:Boox_Palma.jpg",
    "sony-wh-1000xm5": "File:Sony_WH-1000XM5_headphones.jpg",
    "kindle-colorsoft": "File:Amazon_Kindle_Paperwhite_3.jpg"
}

for slug, filename in WIKIMEDIA_FILES.items():
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
                    print(f"Fetching {slug} from {direct_url}...")
                    img_req = urllib.request.Request(direct_url, headers=headers)
                    with urllib.request.urlopen(img_req, timeout=15, context=ctx) as img_resp:
                        img_bytes = img_resp.read()
                        with open(f"public/images/devices/{slug}.jpg", "wb") as f:
                            f.write(img_bytes)
                        print(f"✅ Success {slug} ({len(img_bytes)} bytes)")
    except Exception as e:
        print(f"❌ Error {slug}: {e}")
