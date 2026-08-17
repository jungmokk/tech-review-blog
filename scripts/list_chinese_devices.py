import json
import os

with open("src/data/devices.json") as f:
    devs = json.load(f)

chinese_brands = [
    "Xiaomi", "Redmi", "Poco", "Lenovo", "Huawei", "Honor", "Vivo", "iQOO",
    "Oppo", "OnePlus", "Onyx BOOX", "iFlytek", "Hanvon", "Bigme", "Hisense",
    "Moaan", "Meebook", "ALLDOCUBE", "iMuz", "Nothing", "Supernote"
]

target_chinese_devs = []
for d in devs:
    brand = d.get("brand", "")
    name = d.get("name", "")
    if any(cb.lower() in brand.lower() for cb in chinese_brands) or any(cb.lower() in name.lower() for cb in chinese_brands):
        target_chinese_devs.append(d)

print(f"Total Chinese devices: {len(target_chinese_devs)}")
for d in target_chinese_devs:
    img = d.get("image")
    print(f"{d['id']} | {d['brand']} | {d['name']} | {img}")
