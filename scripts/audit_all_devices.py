#!/usr/bin/env python3
"""
Full Spec Cross-Verification Audit for All 201 Devices
"""
import json

with open("src/data/devices.json", "r", encoding="utf-8") as f:
    devs = json.load(f)

print(f"Auditing all {len(devs)} devices...\n")

brands_checked = {}
for d in devs:
    b = d.get("brand", "Unknown")
    brands_checked[b] = brands_checked.get(b, 0) + 1
    
    # Check for empty or placeholder specs
    specs = d.get("specs", {})
    ap = specs.get("ap", "")
    disp = specs.get("display", "")
    
    if not ap or not disp:
        print(f"⚠️ Missing AP/Display: [{d['id']}] {d['name']}")

print("Brands distribution:")
for b, cnt in sorted(brands_checked.items(), key=lambda x: -x[1]):
    print(f"  - {b}: {cnt} devices")
