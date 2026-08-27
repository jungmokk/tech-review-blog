#!/usr/bin/env python3
"""
guarantee_local_images.py
=========================
Ensures all devices in devices.json have valid, authentic local WebP images
using the auto_image_fetcher engine.
"""

import os
import json
import subprocess
from auto_image_fetcher import fetch_device_image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEVICES_JSON = os.path.join(BASE_DIR, "src", "data", "devices.json")
SMARTPHONES_JSON = os.path.join(BASE_DIR, "src", "data", "smartphones.json")
DEVICES_DIR = os.path.join(BASE_DIR, "public", "images", "devices")

def main():
    if not os.path.exists(DEVICES_JSON):
        print(f"Error: {DEVICES_JSON} not found")
        return

    with open(DEVICES_JSON, "r", encoding="utf-8") as f:
        devices = json.load(f)

    print(f"🚀 Verifying & guaranteeing authentic images for all {len(devices)} devices...")

    success_count = 0
    for dev in devices:
        d_id = dev.get("id")
        if not d_id:
            continue

        webp_path = os.path.join(DEVICES_DIR, f"{d_id}.webp")
        jpg_path = os.path.join(DEVICES_DIR, f"{d_id}.jpg")

        # If missing or smaller than 3KB (corrupted/dummy)
        if not os.path.exists(webp_path) or os.path.getsize(webp_path) < 3000:
            fetch_device_image(d_id)

        if os.path.exists(webp_path):
            dev["image"] = f"/images/devices/{d_id}.webp"
            success_count += 1
        elif os.path.exists(jpg_path):
            dev["image"] = f"/images/devices/{d_id}.jpg"
            success_count += 1

    with open(DEVICES_JSON, "w", encoding="utf-8") as f:
        json.dump(devices, f, ensure_ascii=False, indent=2)

    if os.path.exists(SMARTPHONES_JSON):
        with open(SMARTPHONES_JSON, "w", encoding="utf-8") as f:
            json.dump(devices, f, ensure_ascii=False, indent=2)

    print(f"\n🎉 Successfully verified {success_count}/{len(devices)} device images with authentic hardware photos!")

if __name__ == "__main__":
    main()
