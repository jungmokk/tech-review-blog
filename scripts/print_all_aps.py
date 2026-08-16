import json

with open("src/data/devices.json", "r", encoding="utf-8") as f:
    devs = json.load(f)

for d in devs:
    ap = d.get("specs", {}).get("ap", "")
    print(f"[{d['brand']}] {d['name']} -> {ap}")
