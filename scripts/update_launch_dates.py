import json
import os

# Exact launch dates verified via Google Search / AI Overview
LAUNCH_DATES = {
    # 2026 Releases
    "galaxy-z-fold8": {"release_date": "2026-07-22", "release_year": 2026},
    "galaxy-z-flip8": {"release_date": "2026-07-22", "release_year": 2026},
    "alldocube-iplay-80-mini-pro": {"release_date": "2026-03-15", "release_year": 2026},
    "galaxy-s26-ultra": {"release_date": "2026-02-25", "release_year": 2026},
    "galaxy-s26-plus": {"release_date": "2026-02-25", "release_year": 2026},

    # 2025 Releases
    "airpods-pro-3": {"release_date": "2025-09-09", "release_year": 2025},
    "iphone-17-pro-max": {"release_date": "2025-09-09", "release_year": 2025},
    "lenovo-xiaoxin-pad-pro-13-gt": {"release_date": "2025-03-20", "release_year": 2025},
    "xiaomi-15-ultra": {"release_date": "2025-02-27", "release_year": 2025},
    "galaxy-s25-ultra": {"release_date": "2025-01-22", "release_year": 2025},
    "lenovo-xiaoxin-pad-pro-13": {"release_date": "2025-01-15", "release_year": 2025},

    # 2024 Releases
    "m4-mac-mini": {"release_date": "2024-10-29", "release_year": 2024},
    "xiaomi-pad-7-pro": {"release_date": "2024-10-29", "release_year": 2024},
    "oneplus-13": {"release_date": "2024-10-31", "release_year": 2024},
    "oppo-pad-3-pro": {"release_date": "2024-10-24", "release_year": 2024},
    "boox-palma-2": {"release_date": "2024-10-23", "release_year": 2024},
    "vivo-x200-pro": {"release_date": "2024-10-14", "release_year": 2024},
    "ipad-mini-7": {"release_date": "2024-10-15", "release_year": 2024},
    "kindle-colorsoft": {"release_date": "2024-10-16", "release_year": 2024},
    "galaxy-tab-s10-ultra": {"release_date": "2024-09-26", "release_year": 2024},
    "lenovo-legion-y700-2024": {"release_date": "2024-09-29", "release_year": 2024},
    "huawei-mate-xt": {"release_date": "2024-09-10", "release_year": 2024},
    "iphone-16-pro-max": {"release_date": "2024-09-09", "release_year": 2024},
    "iphone-16": {"release_date": "2024-09-09", "release_year": 2024},
    "lenovo-xiaoxin-pad-pro-12-7-2025": {"release_date": "2024-07-27", "release_year": 2024},
    "iflytek-air-2": {"release_date": "2024-05-20", "release_year": 2024},
    "ipad-pro-13-m4": {"release_date": "2024-05-07", "release_year": 2024},
    "imuz-mupad-k11-plus": {"release_date": "2024-03-15", "release_year": 2024},
    "macbook-air-m3": {"release_date": "2024-03-04", "release_year": 2024},

    # 2022 Releases
    "sony-wh-1000xm5": {"release_date": "2022-05-12", "release_year": 2022},
}

def update_db(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        devices = json.load(f)

    updated = 0
    for dev in devices:
        dev_id = dev.get("id")
        if dev_id in LAUNCH_DATES:
            info = LAUNCH_DATES[dev_id]
            dev["release_date"] = info["release_date"]
            dev["release_year"] = info["release_year"]
            updated += 1

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(devices, f, ensure_ascii=False, indent=2)

    print(f"✅ Updated {updated} devices in {filepath}")

update_db("src/data/smartphones.json")
if os.path.exists("src/data/devices.json"):
    update_db("src/data/devices.json")
