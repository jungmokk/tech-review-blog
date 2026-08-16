import json

with open("src/data/devices.json", "r", encoding="utf-8") as f:
    devs = json.load(f)

print(f"Total registered devices: {len(devs)}")
unreleased = []
for d in devs:
    year = d.get("release_year")
    name = d.get("name", "")
    did = d.get("id", "")
    if year == 2026 or "S26" in name or "Fold8" in name or "Flip8" in name or "iPhone 17" in name or "AirPods Pro 3" in name:
        unreleased.append(d)

print(f"Unreleased / Speculative devices found: {len(unreleased)}")
for u in unreleased:
    print(f"  - [{u['id']}] {u['name']} (Year: {u.get('release_year')})")
