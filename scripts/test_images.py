import json
import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

with open("src/data/devices.json") as f:
    devs = json.load(f)

print(f"Total devices: {len(devs)}")
failed = []
ok = []

for d in devs:
    img = d.get("image")
    d_id = d.get("id")
    if not img:
        print(f"[NO IMAGE] {d_id}")
        failed.append((d_id, "NO IMAGE"))
        continue
    try:
        req = urllib.request.Request(img, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://tech.thesinoreport.com/"
        })
        with urllib.request.urlopen(req, timeout=3, context=ctx) as resp:
            if resp.status == 200:
                ok.append(d_id)
            else:
                failed.append((d_id, f"HTTP {resp.status}"))
    except Exception as e:
        failed.append((d_id, str(e)))

print(f"\n--- RESULTS ---")
print(f"OK: {len(ok)}")
print(f"FAILED: {len(failed)}")
print("\nFailed list (first 20):")
for f_id, err in failed[:20]:
    print(f"  {f_id}: {err}")
