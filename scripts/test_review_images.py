import os, glob, json, urllib.request, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

with open("src/data/devices.json") as f:
    devs = json.load(f)

dev_map = {d["id"]: d for d in devs}

review_files = glob.glob("src/content/reviews/*.mdx")
review_slugs = [os.path.splitext(os.path.basename(p))[0] for p in review_files]

print(f"Review posts count: {len(review_slugs)}")

for slug in review_slugs:
    dev = dev_map.get(slug)
    if not dev:
        print(f"❌ [NO DEV MATCH] {slug}")
        continue
    img = dev.get("image")
    if not img:
        print(f"❌ [NO IMAGE FIELD] {slug}")
        continue
    try:
        req = urllib.request.Request(img, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
        with urllib.request.urlopen(req, timeout=3, context=ctx) as resp:
            print(f"✅ [{resp.status}] {slug} -> {img[:50]}...")
    except Exception as e:
        print(f"❌ [FAIL: {e}] {slug} -> {img}")
