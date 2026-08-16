import json

with open("src/data/devices.json", "r", encoding="utf-8") as f:
    devs = json.load(f)

for d in devs:
    if d['brand'] == 'Samsung':
        print(f"=== {d['name']} ({d['id']}) ===")
        print(json.dumps(d['specs'], ensure_ascii=False, indent=2))
        print()
