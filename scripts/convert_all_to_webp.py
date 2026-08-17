import os
import glob
import subprocess
import json

devices_dir = "/Volumes/data/Projects/blog/public/images/devices"
all_images = glob.glob(os.path.join(devices_dir, "*.jpg")) + glob.glob(os.path.join(devices_dir, "*.png"))

print(f"Total image files to convert to WebP: {len(all_images)}")

total_before = 0
total_after = 0

for img_path in all_images:
    basename = os.path.basename(img_path)
    name_no_ext, ext = os.path.splitext(basename)
    if ext == ".webp":
        continue
    
    webp_path = os.path.join(devices_dir, f"{name_no_ext}.webp")
    size_before = os.path.getsize(img_path)
    total_before += size_before

    # Run cwebp: resize to max-width 800 (keeping aspect ratio), quality 85
    cmd = ["/opt/homebrew/bin/cwebp", "-q", "85", "-resize", "800", "0", img_path, "-o", webp_path]
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        size_after = os.path.getsize(webp_path)
        total_after += size_after
        reduction = (1 - (size_after / size_before)) * 100
        print(f"✅ {name_no_ext}.webp: {size_before//1024}KB -> {size_after//1024}KB ({reduction:.1f}% reduced)")
    except Exception as e:
        print(f"❌ Failed {basename}: {e}")

print(f"\n🎉 Compression complete!")
print(f"Total Before: {total_before / (1024*1024):.2f} MB")
print(f"Total After: {total_after / (1024*1024):.2f} MB")
print(f"Total Saved: {(1 - total_after/total_before)*100:.1f}% bandwidth reduction!")
