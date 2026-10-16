import os
import json
import sys
import glob
import hashlib
from collections import defaultdict

KNOWN_PLACEHOLDER_HASHES = {
    "9df43f75a9c99610b72cefc856625344",  # category-스마트폰
    "3031fcf50d0c24322e0dc74df6531390",  # category-스마트워치
    "dbd2333d6a227ab31d73157cf67085f7",  # generic e-reader placeholder 1
    "ea1aa2a112b32331b538108e733b2e33",  # category-이북리더기
    "b0b86fda571758a122026576c29d17b1",  # category-태블릿
}


def compute_md5(path: str) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def verify_all_device_images():
    print("🔍 [Image Verification] Starting comprehensive image fact, uniqueness & integrity check...")

    with open("src/data/devices.json", "r", encoding="utf-8") as f:
        devices = json.load(f)

    dev_map = {d["id"]: d for d in devices}

    # Precompute hashes of category-* files
    category_hashes = set(KNOWN_PLACEHOLDER_HASHES)
    for cat_file in glob.glob("public/images/devices/category-*.webp"):
        category_hashes.add(compute_md5(cat_file))

    review_files = sorted(glob.glob("src/content/reviews/*.mdx"))
    errors = []
    hash_to_slugs = defaultdict(list)

    for r_file in review_files:
        slug = os.path.basename(r_file).replace(".mdx", "")
        webp_path = f"public/images/devices/{slug}.webp"

        if not os.path.exists(webp_path):
            errors.append(f"❌ [{slug}] Missing image file: {webp_path}")
            continue

        sz = os.path.getsize(webp_path)
        if sz < 2500:
            errors.append(f"❌ [{slug}] Image too small or corrupt ({sz} bytes): {webp_path}")
            continue

        img_hash = compute_md5(webp_path)
        if img_hash in category_hashes:
            errors.append(f"❌ [{slug}] Image is a generic category placeholder (hash {img_hash[:10]}): {webp_path}")
            continue

        hash_to_slugs[img_hash].append(slug)

        if slug in dev_map:
            dev = dev_map[slug]
            dev_type = dev.get("device_type", "")
            if "fold" in slug and "flip" in dev_type.lower():
                errors.append(f"❌ [{slug}] Form factor mismatch: slug has fold but dev_type is {dev_type}")
            if "flip" in slug and "fold" in dev_type.lower() and "flip" not in dev_type.lower():
                errors.append(f"❌ [{slug}] Form factor mismatch: slug has flip but dev_type is {dev_type}")

    for img_hash, slugs in hash_to_slugs.items():
        if len(slugs) > 1:
            errors.append(f"❌ [Duplicate Image Hash {img_hash[:10]}] Shared across {len(slugs)} devices: {slugs}")

    print(f"\n📊 Verification summary: Checked {len(review_files)} reviews.")
    if errors:
        print(f"\n🚨 CRITICAL IMAGE ERRORS FOUND ({len(errors)}):")
        for err in errors:
            print(err)
        sys.exit(1)
    else:
        print("🎉 ALL REVIEWS PASSED 100% IMAGE INTEGRITY, UNIQUENESS & FACT CHECK!\n")


if __name__ == "__main__":
    verify_all_device_images()
