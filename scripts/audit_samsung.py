import json

with open("src/data/devices.json", "r", encoding="utf-8") as f:
    devs = json.load(f)

samsung_devs = [d for d in devs if d.get("brand") == "Samsung"]
print(f"Total Samsung Devices: {len(samsung_devs)}")
for d in samsung_devs:
    print(f"ID: {d['id']} | Name: {d['name']} | AP: {d.get('specs', {}).get('ap')}")
