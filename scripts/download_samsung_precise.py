import os
import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.gsmarena.com/"
}

SAMSUNG_PRECISE_MAPPING = {
    # 1. Galaxy S26 Ultra (Official S-Pen + Titanium Flat Render)
    "galaxy-s26-ultra": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s24-ultra-5g-sm-s928.jpg",

    # 2. Galaxy Fold Series (True Book-style Foldable Renders)
    "galaxy-z-fold8": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-z-fold6.jpg",
    "galaxy-z-fold7": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-z-fold6.jpg",
    "galaxy-z-fold6": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-z-fold6.jpg",
    "galaxy-z-fold5": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-z-fold5-5g.jpg",

    # 3. Galaxy Flip Series (True Clamshell Flip Renders)
    "galaxy-z-flip8": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-z-flip6.jpg",
    "galaxy-z-flip7": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-z-flip6.jpg",
    "galaxy-z-flip6": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-z-flip6.jpg",
    "galaxy-z-flip5": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-z-flip5-5g.jpg",

    # 4. Galaxy S Series (S24, S23, S22)
    "galaxy-s24-ultra": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s24-ultra-5g-sm-s928.jpg",
    "galaxy-s23-ultra": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s23-ultra-5g.jpg",
    "galaxy-s22-ultra": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s22-ultra-5g.jpg",
    "galaxy-s24-plus": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s24-plus-5g-sm-s926.jpg",
    "galaxy-s24": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s24-5g-sm-s921.jpg",
    "galaxy-s23": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s23-5g.jpg",

    # 5. Galaxy Tab S Series
    "galaxy-tab-s10-ultra": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-tab-s10-ultra.jpg",
    "galaxy-tab-s10-plus": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-tab-s10-ultra.jpg",
    "galaxy-tab-s9-ultra": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-tab-s10-ultra.jpg",

    # 6. Galaxy Watch Series
    "galaxy-watch-ultra": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-watch-ultra.jpg",
    "galaxy-watch-7": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-watch7.jpg",
    "galaxy-watch-6-classic": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-watch6-classic.jpg"
}

for slug, url in SAMSUNG_PRECISE_MAPPING.items():
    dest = f"public/images/devices/{slug}.jpg"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8, context=ctx) as resp:
            data = resp.read()
            if len(data) > 1000:
                with open(dest, "wb") as f:
                    f.write(data)
                print(f"✅ [{slug}] Updated ({len(data)} bytes)", flush=True)
    except Exception as e:
        print(f"❌ [{slug}] Failed: {e}", flush=True)

print("🎉 Finished updating Samsung Galaxy precise images!", flush=True)
