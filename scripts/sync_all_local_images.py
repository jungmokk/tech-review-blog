import os
import shutil
import json

with open("src/data/devices.json", "r", encoding="utf-8") as f:
    devices = json.load(f)

# Ensure base categories exist
for cat in ["스마트폰", "태블릿", "스마트워치", "이북리더기", "default"]:
    cat_file = f"public/images/devices/category-{cat}.jpg"
    if not os.path.exists(cat_file):
        # copy from existing
        src = "public/images/devices/galaxy-s26-ultra.jpg"
        if os.path.exists(src):
            shutil.copyfile(src, cat_file)

# For every single device in json:
missing = 0
for dev in devices:
    d_id = dev["id"]
    cat = dev.get("device_type", "스마트폰")
    local_filename = f"{d_id}.jpg"
    local_path = f"public/images/devices/{local_filename}"

    if not os.path.exists(local_path) or os.path.getsize(local_path) == 0:
        cat_file = f"public/images/devices/category-{cat}.jpg"
        if not os.path.exists(cat_file):
            cat_file = "public/images/devices/category-스마트폰.jpg"
        if not os.path.exists(cat_file):
            cat_file = "public/images/devices/category-default.jpg"
        shutil.copyfile(cat_file, local_path)
        missing += 1

    dev["image"] = f"/images/devices/{local_filename}"

with open("src/data/devices.json", "w", encoding="utf-8") as f:
    json.dump(devices, f, ensure_ascii=False, indent=2)

with open("src/data/smartphones.json", "w", encoding="utf-8") as f:
    json.dump(devices, f, ensure_ascii=False, indent=2)

print(f"✅ Success! All {len(devices)} devices now have local images. Filled {missing} devices with category hardware visuals.")
