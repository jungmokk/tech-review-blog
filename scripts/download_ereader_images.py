import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

EREADER_OFFICIALS = {
    # 1. BOOX Palma 2 - Official BOOX Shop Product Shot (Phone-sized E-Ink device)
    "boox-palma-2": "https://shop.boox.com/cdn/shop/files/1_0d6848e7-334b-47f0-9653-2dd3c8339a4f_grande.jpg?v=1694677873",
    
    # 2. Kindle Colorsoft - Amazon Official E-Reader Shot
    "kindle-colorsoft": "https://m.media-amazon.com/images/I/71u9sW1aKFL._AC_SL1500_.jpg",

    # 3. iFlytek Air 2 - Official E-Ink Smart Note
    "iflytek-air-2": "https://img.alicdn.com/imgextra/i4/2200724608678/O1CN01Z7z6hJ1w7z5yX9z7a_!!2200724608678.jpg"
}

for slug, url in EREADER_OFFICIALS.items():
    dest = f"public/images/devices/{slug}.jpg"
    print(f"Downloading official product photo for {slug}...")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            data = resp.read()
            if len(data) > 1000:
                with open(dest, "wb") as f:
                    f.write(data)
                print(f"✅ Successfully updated {slug} ({len(data)} bytes)")
    except Exception as e:
        print(f"❌ Failed {slug}: {e}")
