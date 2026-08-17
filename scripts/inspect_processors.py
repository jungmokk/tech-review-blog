import json
import glob
import re

with open("src/data/devices.json", "r", encoding="utf-8") as f:
    devices = json.load(f)

print(f"📊 Total devices in DB: {len(devices)}")
print("=== Checking Processors for Chinese & Flagship Devices ===")
for d in devices:
    d_name = d.get("name", "")
    d_id = d.get("id", "")
    d_proc = d.get("processor", "")
    if any(cn in d_name.lower() or cn in d_id.lower() for cn in ["xiaomi", "vivo", "huawei", "oppo", "lenovo", "honor", "oneplus", "iqoo", "realme", "nubia", "redmi", "alldocube", "boox", "galaxy", "ipad"]):
        print(f"- [{d_id}] {d_name} => AP: {d_proc}")
