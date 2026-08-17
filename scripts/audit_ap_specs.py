import json
import glob
import re

with open("src/data/devices.json", "r", encoding="utf-8") as f:
    devices = json.load(f)

print("=== 📋 Current Devices DB: AP Specs vs Actual Flagship Mapping ===\n")

for d in devices:
    d_name = d.get("name", "")
    d_id = d.get("id", "")
    specs = d.get("specs", {})
    ap = specs.get("ap", "N/A")
    brand = d.get("brand", "")
    
    # Check key models
    if any(k in d_id for k in ["xiaomi-15", "xiaomi-14", "xiaomi-13", "vivo-x200", "vivo-x100", "vivo-x90", "huawei-mate", "huawei-pura", "oppo-find", "oneplus-13", "oneplus-12", "oneplus-11", "iqoo-13", "iqoo-12", "iqoo-11", "redmi-k80", "redmi-k70", "redmi-k60", "honor-magic", "lenovo-legion-y700", "lenovo-xiaoxin", "alldocube", "boox", "galaxy-s26", "galaxy-s25", "galaxy-s24", "galaxy-z-fold8", "galaxy-z-flip8", "oppo-pad", "xiaomi-pad"]):
        print(f"[{d_id}] {d_name} ({brand})")
        print(f"  👉 DB AP: {ap}\n")
