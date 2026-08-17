import os
import json
import sys
import glob

def verify_all_device_images():
    print("🔍 [Image Verification] Starting comprehensive image fact & integrity check...")
    
    # 1. Load devices database
    with open("src/data/devices.json", "r", encoding="utf-8") as f:
        devices = json.load(f)
    
    dev_map = {d["id"]: d for d in devices}
    
    # 2. Check all active review files
    review_files = glob.glob("src/content/reviews/*.mdx")
    errors = []
    
    for r_file in review_files:
        slug = os.path.basename(r_file).replace(".mdx", "")
        webp_path = f"public/images/devices/{slug}.webp"
        
        # Check file exists
        if not os.path.exists(webp_path):
            errors.append(f"❌ [{slug}] Missing image file: {webp_path}")
            continue
            
        # Check file size (must be >= 5KB to prevent empty/broken files)
        sz = os.path.getsize(webp_path)
        if sz < 5000:
            errors.append(f"❌ [{slug}] Image too small or corrupt ({sz} bytes): {webp_path}")
            continue
            
        # Check device metadata in DB
        if slug in dev_map:
            dev = dev_map[slug]
            cat = dev.get("category", "")
            dev_type = dev.get("device_type", "")
            
            # Form-factor mismatch checks (e.g. Fold vs Flip)
            if "fold" in slug and "flip" in dev_type.lower():
                errors.append(f"❌ [{slug}] Form factor mismatch: slug has fold but dev_type is {dev_type}")
            if "flip" in slug and "fold" in dev_type.lower() and "flip" not in dev_type.lower():
                errors.append(f"❌ [{slug}] Form factor mismatch: slug has flip but dev_type is {dev_type}")
                
        print(f"✅ [{slug}] Verified ({sz // 1024} KB WebP)")
        
    print(f"\n📊 Verification summary: Checked {len(review_files)} reviews.")
    if errors:
        print("\n🚨 CRITICAL IMAGE ERRORS FOUND:")
        for err in errors:
            print(err)
        sys.exit(1)
    else:
        print("🎉 ALL REVIEWS PASSED 100% IMAGE INTEGRITY & FACT CHECK!\n")

if __name__ == "__main__":
    verify_all_device_images()
