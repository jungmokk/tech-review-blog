import os
import subprocess
import sys

# Masterpieces (대작 기계들)
MASTERPIECES = [
    "galaxy-s26-ultra",
    "galaxy-s26-plus",
    "galaxy-s25-ultra",
    "iphone-17-pro-max",
    "iphone-16-pro-max",
    "iphone-16",
    "ipad-pro-13-m4",
    "macbook-air-m3",
    "m4-mac-mini"
]

# Chinese ZOL Devices
ZOL_DEVICES = [
    "xiaomi-15-ultra",
    "xiaomi-pad-7-pro",
    "vivo-x200-pro",
    "huawei-mate-xt",
    "lenovo-legion-y700-2024",
    "lenovo-xiaoxin-pad-pro-12-7-2025",
    "lenovo-xiaoxin-pad-pro-13-gt",
    "lenovo-xiaoxin-pad-pro-13",
    "oppo-pad-3-pro",
    "alldocube-iplay-80-mini-pro",
    "boox-palma-2",
    "imuz-mupad-k11-plus",
    "iflytek-air-2",
    "honor-magic-7-pro",
    "honor-magic-v3",
    "oneplus-13",
    "oneplus-open",
    "oppo-find-x8-pro",
    "vivo-x-fold3-pro",
    "xiaomi-15",
    "xiaomi-mix-flip",
    "xiaomi-mix-fold-4",
    "huawei-pura-70-ultra"
]

ALL_DEVICES = MASTERPIECES + ZOL_DEVICES
REVIEWS_DIR = "src/content/reviews"

def main():
    print(f"🚀 [Auto-Generator] Starting generation for {len(ALL_DEVICES)} target devices...")
    
    success_count = 0
    skip_count = 0
    error_count = 0

    for dev in ALL_DEVICES:
        mdx_path = os.path.join(REVIEWS_DIR, f"{dev}.mdx")
        if os.path.exists(mdx_path):
            print(f"⏩ [Skip] {dev} is already published.")
            skip_count += 1
            continue
            
        print(f"\n🔄 [Generating] Initiating pipeline for {dev}...")
        try:
            # Run generate.py
            result = subprocess.run([sys.executable, "scripts/generate.py", "--device", dev], check=True)
            success_count += 1
        except subprocess.CalledProcessError as e:
            print(f"❌ [Error] Failed to generate {dev}: {e}")
            error_count += 1
            
    print(f"\n🎉 [Auto-Generator Complete] Success: {success_count} | Skipped: {skip_count} | Errors: {error_count}")

if __name__ == "__main__":
    main()
