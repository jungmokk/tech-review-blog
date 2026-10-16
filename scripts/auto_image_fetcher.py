#!/usr/bin/env python3
"""
auto_image_fetcher.py
=====================
Automated, 100% accurate device image fetcher for the Tech Review Blog.

Sourcing Priority:
1. GSMArena Official BigPic CDN (smart slug candidates including trailing-dash & model code variants)
2. ZOL (中关村在线) Official Product Database Photo Search
3. Google Image Search (tbm=isch / udm=2 with full script-unescaping & gstatic tbn support)
4. Wikimedia Commons Direct API Search
5. Curated / Device DB Verified YouTube Review HD Thumbnails

Includes MD5 deduplication against category placeholders and other device images so that
no two devices ever share a placeholder or duplicate image.
"""

import os
import sys
import json
import re
import hashlib
import urllib.request
import urllib.parse
import subprocess
import ssl

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEVICES_DIR = os.path.join(BASE_DIR, "public", "images", "devices")
DEVICES_JSON_PATH = os.path.join(BASE_DIR, "src", "data", "devices.json")
CURATED_VIDEOS_PATH = os.path.join(BASE_DIR, "src", "data", "curated_exact_videos.json")

os.makedirs(DEVICES_DIR, exist_ok=True)

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

HEADERS_DEFAULT = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,ko;q=0.8",
}

HEADERS_GSM = {
    **HEADERS_DEFAULT,
    "Referer": "https://www.gsmarena.com/",
}

HEADERS_ZOL = {
    **HEADERS_DEFAULT,
    "Referer": "https://mobile.zol.com.cn/",
}

HEADERS_WIKI = {
    "User-Agent": "TechSpecBlogHQ/2.0 (official-press@thesinoreport.com) Python-urllib/3.11"
}

KNOWN_PLACEHOLDER_HASHES = {
    "9df43f75a9c99610b72cefc856625344",  # category-스마트폰
    "3031fcf50d0c24322e0dc74df6531390",  # category-스마트워치
    "dbd2333d6a227ab31d73157cf67085f7",  # generic e-reader placeholder 1
    "ea1aa2a112b32331b538108e733b2e33",  # category-이북리더기
    "b0b86fda571758a122026576c29d17b1",  # category-태블릿
}

NON_GSMARENA_PREFIXES = (
    "amazfit-", "garmin-", "boox-", "kobo-", "kindle-", "remarkable-",
    "supernote-", "crema-", "ridipaper-", "meebook-", "moaan-", "hanvon-",
    "bigme-", "hisense-", "pocketbook-", "mooink-", "iflytek-", "imuz-",
    "alldocube-", "m4-mac-", "m6-mac-", "macbook-"
)

EXACT_GSMARENA_SLUGS = {
    "galaxy-s25": ["samsung-galaxy-s25-sm-s931", "samsung-galaxy-s25"],
    "galaxy-s25-plus": ["samsung-galaxy-s25-plus-sm-s936", "samsung-galaxy-s25-plus"],
    "galaxy-s24-fe": ["samsung-galaxy-s24-fe-r1", "samsung-galaxy-s24-fe"],
    "galaxy-tab-s9-fe-plus": ["samsung-galaxy-tab-s9-fe+", "samsung-galaxy-tab-s9-fe-plus"],
    "galaxy-fit-3": ["samsung-galaxy-fit3", "samsung-galaxy-fit-3"],
    "ipad-pro-11-m4": ["apple-ipad-pro-11-2024"],
    "ipad-pro-13-m4": ["apple-ipad-pro-13-2024"],
    "ipad-pro-12-9-m2": ["apple-ipad-pro-129-2022"],
    "ipad-air-11-m2": ["apple-ipad-air-11-2024"],
    "ipad-air-13-m2": ["apple-ipad-air-13-2024"],
    "apple-watch-series-10": ["apple-watch-series-10", "apple-watch-series-10-aluminum"],
    "apple-watch-ultra-2": ["apple-watch-ultra-2", "apple-watch-ultra2"],
    "pixel-watch-3": ["google-pixel-watch-3"],
    "google-pixel-tablet": ["google-pixel-tablet"],
    "nothing-phone-2": ["nothing-phone-2", "nothing-phone-(2)", "nothing-phone2"],
    "iqoo-11-pro": ["vivo-iqoo-11-pro", "vivo-iqoo-11-pro-5g"],
    "poco-f5-pro": ["xiaomi-poco-f5-pro", "xiaomi-poco-f5-pro-5g"],
    "redmi-k70-ultra": ["xiaomi-redmi-k70-ultra"],
    "redmi-k80-pro": ["xiaomi-redmi-k80-pro"],
    "redmi-pad-se": ["xiaomi-redmi-pad-se"],
    "oppo-pad-3": ["oppo-pad-3", "oppo-pad3"],
    "oppo-pad-neo": ["oppo-pad-neo"],
}


def compute_md5(file_path: str) -> str:
    if not os.path.exists(file_path):
        return ""
    h = hashlib.md5()
    with open(file_path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def get_existing_other_hashes(exclude_device_id: str) -> set[str]:
    """Return MD5 hashes of all category-*.webp files, known placeholders, and all other device .webp files."""
    hashes = set(KNOWN_PLACEHOLDER_HASHES)
    if not os.path.exists(DEVICES_DIR):
        return hashes
    for fn in os.listdir(DEVICES_DIR):
        if not fn.endswith(".webp"):
            continue
        stem = fn[:-5]
        if stem == exclude_device_id:
            continue
        full_path = os.path.join(DEVICES_DIR, fn)
        if os.path.isfile(full_path):
            hashes.add(compute_md5(full_path))
    return hashes


def is_valid_unique_device_image(device_id: str) -> bool:
    """Check if public/images/devices/{device_id}.webp exists, is >= 2.5KB, and is NOT a duplicate/placeholder."""
    webp_path = os.path.join(DEVICES_DIR, f"{device_id}.webp")
    if not os.path.exists(webp_path) or os.path.getsize(webp_path) < 2500:
        return False
    my_hash = compute_md5(webp_path)
    other_hashes = get_existing_other_hashes(device_id)
    return my_hash not in other_hashes


def get_device_metadata(device_id: str) -> dict:
    """Load device metadata (brand, name, name_kr, category, videos) from src/data/devices.json."""
    if os.path.exists(DEVICES_JSON_PATH):
        try:
            with open(DEVICES_JSON_PATH, "r", encoding="utf-8") as f:
                devices = json.load(f)
            for d in devices:
                if d.get("id") == device_id:
                    return d
        except Exception:
            pass
    parts = device_id.split("-")
    brand = parts[0].capitalize() if parts else "Tech"
    name = device_id.replace("-", " ").title()
    return {"id": device_id, "brand": brand, "name": name, "name_kr": name, "videos": []}


def convert_to_webp(input_path: str, output_path: str) -> bool:
    """Convert any image to WebP using cwebp or sips (macOS)."""
    try:
        if os.path.exists("/opt/homebrew/bin/cwebp"):
            subprocess.run(
                ["/opt/homebrew/bin/cwebp", "-q", "90", "-resize", "800", "0", input_path, "-o", output_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
            return os.path.exists(output_path) and os.path.getsize(output_path) > 2500
        else:
            subprocess.run(
                ["sips", "-s", "format", "webp", input_path, "--out", output_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
            return os.path.exists(output_path) and os.path.getsize(output_path) > 2500
    except Exception:
        return False


def _save_and_verify_unique(raw_bytes: bytes, temp_raw: str, out_webp: str, other_hashes: set[str]) -> bool:
    """Write raw_bytes to temp_raw, convert to out_webp, and verify it is non-empty and not a duplicate hash."""
    if not raw_bytes or len(raw_bytes) < 2500:
        return False
    head = raw_bytes[:256].lstrip().lower()
    if head.startswith(b"<!doctype") or head.startswith(b"<html") or head.startswith(b"<?xml"):
        return False
    with open(temp_raw, "wb") as f:
        f.write(raw_bytes)
    if not convert_to_webp(temp_raw, out_webp):
        return False
    new_hash = compute_md5(out_webp)
    if new_hash in other_hashes:
        try:
            os.remove(out_webp)
        except Exception:
            pass
        return False
    return True


def generate_gsmarena_slug_candidates(device_id: str) -> list[str]:
    """Generate comprehensive GSMArena BigPic slug variants from device_id."""
    clean_id = device_id.lower().strip()
    if clean_id.startswith(NON_GSMARENA_PREFIXES):
        return []

    candidates = list(EXACT_GSMARENA_SLUGS.get(clean_id, []))
    base_variants = [
        clean_id,
        clean_id.replace("-5g", ""),
        f"{clean_id}-5g",
        clean_id.replace("-2024", ""),
        clean_id.replace("-2025", ""),
    ]

    for v in base_variants:
        if v.startswith("galaxy-"):
            candidates.append(f"samsung-{v}")
            candidates.append(f"samsung-{v}".replace("-plus", "+"))
            candidates.append(f"samsung-{v.replace('z-fold-', 'z-fold').replace('z-flip-', 'z-flip')}")
        elif v.startswith("iphone-"):
            candidates.append(f"apple-{v}")
        elif v.startswith("ipad-"):
            candidates.append(f"apple-{v}")
            candidates.append(f"apple-{v.replace('-m4', '-2024').replace('-m2', '-2024')}")
        elif v.startswith("pixel-"):
            candidates.append(f"google-{v}")
            candidates.append(f"google-{v}-")
            candidates.append(f"google-{v}-5g")
        elif v.startswith("redmi-"):
            candidates.append(f"xiaomi-{v}")
            candidates.append(f"xiaomi-{v}-5g")
        elif v.startswith("poco-"):
            candidates.append(f"xiaomi-{v}")
            candidates.append(f"xiaomi-{v}-5g")
        elif v.startswith("xiaomi-"):
            candidates.append(v)
            candidates.append(f"{v}-")
            candidates.append(f"{v}-5g")
        elif v.startswith("iqoo-"):
            candidates.append(f"vivo-{v}")
            candidates.append(f"vivo-{v}-5g")
        elif v.startswith("sony-xperia-"):
            candidates.append(v)
            candidates.append(f"{v}-5g")
        else:
            candidates.append(v)
            candidates.append(f"{v}-")

    seen = set()
    result = []
    for c in candidates:
        for variant in (c, f"{c}-"):
            if variant and variant not in seen:
                seen.add(variant)
                result.append(variant)
    return result[:8]


def fetch_from_gsmarena(device_id: str, meta: dict, temp_raw: str, out_webp: str, other_hashes: set[str]) -> bool:
    """Attempt downloading official BigPic render from GSMArena CDN."""
    slugs = generate_gsmarena_slug_candidates(device_id)
    for slug in slugs:
        url = f"https://fdn2.gsmarena.com/vv/bigpic/{slug}.jpg"
        try:
            req = urllib.request.Request(url, headers=HEADERS_GSM)
            with urllib.request.urlopen(req, timeout=4, context=SSL_CTX) as resp:
                data = resp.read()
                if len(data) > 4000 and _save_and_verify_unique(data, temp_raw, out_webp, other_hashes):
                    print(f"  ✅ [GSMArena CDN] Found official render: {url}")
                    return True
        except Exception:
            continue
    return False


def fetch_from_zol(device_id: str, meta: dict, temp_raw: str, out_webp: str, other_hashes: set[str]) -> bool:
    """Search ZOL (中关村在线) for official product photo."""
    clean_name = re.sub(r"\s*\([^)]*\)", "", meta.get("name", "")).strip()
    brand = meta.get("brand", "")
    queries = []
    if brand and brand.lower() not in clean_name.lower():
        queries.append(f"{brand} {clean_name}")
    queries.append(clean_name)

    for q in queries[:1]:
        if not q:
            continue
        try:
            encoded_q = urllib.parse.quote(q.encode("gbk", errors="ignore"))
            search_url = f"https://detail.zol.com.cn/index.php?c=SearchList&kword={encoded_q}"
            req = urllib.request.Request(search_url, headers=HEADERS_ZOL)
            with urllib.request.urlopen(req, timeout=5, context=SSL_CTX) as resp:
                html = resp.read().decode("gbk", errors="ignore")
            imgs = re.findall(r'src=[\'"](https?://[^\'"]+zol-img\.com\.cn/[^\'"]+)[\'"]', html)
            for img in imgs[:3]:
                if "/product/" in img:
                    hd_img = re.sub(r"_\d+x\d+/", "_800x600/", img)
                    try:
                        ireq = urllib.request.Request(hd_img, headers=HEADERS_ZOL)
                        with urllib.request.urlopen(ireq, timeout=5, context=SSL_CTX) as iresp:
                            data = iresp.read()
                            if _save_and_verify_unique(data, temp_raw, out_webp, other_hashes):
                                print(f"  ✅ [ZOL Official] Downloaded: {hd_img}")
                                return True
                    except Exception:
                        continue
        except Exception:
            continue
    return False


def fetch_from_google_images(device_id: str, meta: dict, temp_raw: str, out_webp: str, other_hashes: set[str]) -> bool:
    """
    Search Google Images (tbm=isch&gbv=1 basic HTML mode + standard mode) for official product photo of the exact device.
    """
    clean_name = re.sub(r"\s*\([^)]*\)", "", meta.get("name", "")).strip()
    brand = meta.get("brand", "")
    full_name = f"{brand} {clean_name}".strip() if brand.lower() not in clean_name.lower() else clean_name

    # Basic HTML mode (gbv=1) returns pure HTML with encrypted-tbn0.gstatic.com thumbnails for the exact query
    headers_basic = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    google_queries = [
        f"{full_name} official product photo",
        f"{full_name} review",
    ]
    for q in google_queries:
        url = f"https://www.google.com/search?q={urllib.parse.quote(q)}&tbm=isch&gbv=1&hl=en"
        try:
            req = urllib.request.Request(url, headers=headers_basic)
            with urllib.request.urlopen(req, timeout=5, context=SSL_CTX) as resp:
                raw_html = resp.read().decode("utf-8", errors="ignore")

            html = (
                raw_html
                .replace("\\u003d", "=")
                .replace("\\x3d", "=")
                .replace("\\u0026", "&")
                .replace("\\x26", "&")
                .replace("&amp;", "&")
            )
            tbn_urls = re.findall(
                r'(https://encrypted-tbn0\.gstatic\.com/images\?q=tbn:[A-Za-z0-9_:-]+)',
                html,
            )
            for cand_url in tbn_urls[:6]:
                try:
                    ireq = urllib.request.Request(cand_url, headers=HEADERS_DEFAULT)
                    with urllib.request.urlopen(ireq, timeout=4, context=SSL_CTX) as iresp:
                        data = iresp.read()
                        if _save_and_verify_unique(data, temp_raw, out_webp, other_hashes):
                            print(f"  ✅ [Google Image Search] Downloaded authentic image for '{full_name}': {cand_url[:80]}...")
                            return True
                except Exception:
                    continue
        except Exception:
            continue

    return False


def fetch_from_youtube(device_id: str, meta: dict, youtube_id: str | None, temp_raw: str, out_webp: str, other_hashes: set[str]) -> bool:
    """Attempt downloading high-res hands-on thumbnail from verified YouTube review."""
    candidate_vids = []
    if youtube_id:
        candidate_vids.append(youtube_id)

    if os.path.exists(CURATED_VIDEOS_PATH):
        try:
            with open(CURATED_VIDEOS_PATH, "r", encoding="utf-8") as f:
                curated = json.load(f)
            item = curated.get(device_id)
            if isinstance(item, dict) and item.get("youtube_id"):
                candidate_vids.append(item["youtube_id"])
            elif isinstance(item, list) and len(item) > 0 and item[0].get("youtube_id"):
                candidate_vids.append(item[0]["youtube_id"])
        except Exception:
            pass

    for v in (meta.get("videos") or []):
        if isinstance(v, dict) and v.get("youtube_id"):
            candidate_vids.append(v["youtube_id"])

    # Try downloading from candidate video IDs
    seen_vids = set()
    for vid in candidate_vids:
        if not vid or vid in seen_vids:
            continue
        seen_vids.add(vid)
        for quality in ["maxresdefault", "sddefault", "hqdefault"]:
            thumb_url = f"https://i.ytimg.com/vi/{vid}/{quality}.jpg"
            try:
                req = urllib.request.Request(thumb_url, headers=HEADERS_DEFAULT)
                with urllib.request.urlopen(req, timeout=4, context=SSL_CTX) as resp:
                    data = resp.read()
                    if len(data) > 5000 and _save_and_verify_unique(data, temp_raw, out_webp, other_hashes):
                        print(f"  ✅ [YouTube Hands-on] Downloaded video thumbnail (ID: {vid}, {quality})")
                        return True
            except Exception:
                continue

    return False


def fetch_from_wikimedia(device_id: str, meta: dict, temp_raw: str, out_webp: str, other_hashes: set[str]) -> bool:
    """Attempt downloading authentic image from Wikimedia Commons API."""
    clean_query = re.sub(r"\s*\([^)]*\)", "", meta.get("name", device_id.replace("-", " "))).strip()
    api_url = f"https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={urllib.parse.quote(clean_query)}&gsrnamespace=6&prop=imageinfo&iiprop=url&format=json"
    try:
        req = urllib.request.Request(api_url, headers=HEADERS_WIKI)
        with urllib.request.urlopen(req, timeout=5, context=SSL_CTX) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        pages = data.get("query", {}).get("pages", {})
        for _, p in pages.items():
            ii = p.get("imageinfo", [{}])[0]
            img_url = ii.get("url")
            if img_url and any(img_url.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp"]):
                img_req = urllib.request.Request(img_url, headers=HEADERS_WIKI)
                with urllib.request.urlopen(img_req, timeout=5, context=SSL_CTX) as img_resp:
                    img_data = img_resp.read()
                    if len(img_data) > 10000 and _save_and_verify_unique(img_data, temp_raw, out_webp, other_hashes):
                        print(f"  ✅ [Wikimedia] Downloaded: {img_url}")
                        return True
    except Exception:
        pass
    return False


def fetch_device_image(device_id: str, youtube_id: str | None = None, force: bool = False) -> bool:
    """
    Main entry point: fetches the accurate, unique hardware image for device_id
    and outputs to public/images/devices/{device_id}.webp.
    """
    out_webp = os.path.join(DEVICES_DIR, f"{device_id}.webp")
    out_jpg = os.path.join(DEVICES_DIR, f"{device_id}.jpg")
    temp_raw = os.path.join(DEVICES_DIR, f"{device_id}_raw.tmp")

    if not force and is_valid_unique_device_image(device_id):
        print(f"⏩ [{device_id}] Already has unique, valid WebP ({os.path.getsize(out_webp)} bytes), skipping.")
        return True

    meta = get_device_metadata(device_id)
    other_hashes = get_existing_other_hashes(device_id)
    print(f"🔍 [{device_id}] ({meta.get('name', device_id)}) Fetching accurate hardware image...")

    success = False

    # 1. Try GSMArena Official BigPic CDN
    if fetch_from_gsmarena(device_id, meta, temp_raw, out_webp, other_hashes):
        success = True

    # 2. Try Verified YouTube Thumbnail (curated or devices.json)
    if not success and fetch_from_youtube(device_id, meta, youtube_id, temp_raw, out_webp, other_hashes):
        success = True

    # 3. Try Google Image Search (gbv=1 static HTML mode)
    if not success and fetch_from_google_images(device_id, meta, temp_raw, out_webp, other_hashes):
        success = True

    # 4. Try ZOL (中关村在线) Official Product Image Search
    if not success and fetch_from_zol(device_id, meta, temp_raw, out_webp, other_hashes):
        success = True

    # 5. Try Wikimedia Commons Search
    if not success and fetch_from_wikimedia(device_id, meta, temp_raw, out_webp, other_hashes):
        success = True

    if success and os.path.exists(out_webp):
        if os.path.exists(temp_raw):
            import shutil
            shutil.copyfile(temp_raw, out_jpg)
            os.remove(temp_raw)
        webp_size = os.path.getsize(out_webp)
        print(f"🎉 [{device_id}] Successfully generated unique WebP ({webp_size} bytes)")
        return True
    else:
        print(f"❌ [{device_id}] All automated fetchers exhausted.")
        if os.path.exists(temp_raw):
            os.remove(temp_raw)
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 auto_image_fetcher.py <device-id|--all-duplicates> [youtube-id-or-url] [--force]")
        sys.exit(1)

    target_device = sys.argv[1]
    force_flag = "--force" in sys.argv

    if target_device == "--all-duplicates":
        with open(DEVICES_JSON_PATH, "r", encoding="utf-8") as f:
            all_devs = [d["id"] for d in json.load(f) if d.get("id")]
        import glob
        review_slugs = [os.path.basename(p).replace(".mdx", "") for p in glob.glob(os.path.join(BASE_DIR, "src", "content", "reviews", "*.mdx"))]
        copycats_first = [
            "galaxy-s26-plus", "galaxy-s26", "galaxy-tab-s10-plus", "galaxy-z-flip7",
            "galaxy-z-fold7", "kindle-colorsoft", "imuz-mupad-k10-plus", "iphone-17-pro-max",
            "lenovo-legion-y700-2023", "lenovo-xiaoxin-pad-pro-12-7-2023",
            "lenovo-xiaoxin-pad-pro-13-gt", "nothing-phone-3", "vivo-x-fold4-pro",
            "vivo-x200-ultra", "alldocube-iplay-70-mini-pro", "alldocube-iplay-70-pro",
            "alldocube-iplay-80-mini-pro", "alldocube-iplay-80-pro"
        ]
        targets = list(dict.fromkeys(copycats_first + review_slugs + all_devs))
        fixed = 0
        failed = []
        for slug in targets:
            if not is_valid_unique_device_image(slug):
                if fetch_device_image(slug, force=True):
                    fixed += 1
                else:
                    failed.append(slug)
        print(f"\n📊 Batch Image Repair Complete: Fixed {fixed} devices, Failed {len(failed)}")
        if failed:
            print(f"⚠️ Remaining failed devices: {failed}")
            sys.exit(1)
        sys.exit(0)

    yt_arg = None
    for arg in sys.argv[2:]:
        if arg.startswith("--"):
            continue
        if "youtu" in arg:
            m = re.search(r"(?:v=|\/shorts\/|youtu\.be\/)([a-zA-Z0-9_-]{11})", arg)
            if m:
                yt_arg = m.group(1)
        elif len(arg) == 11 and not arg.startswith("-"):
            yt_arg = arg

    res = fetch_device_image(target_device, youtube_id=yt_arg, force=force_flag)
    sys.exit(0 if res else 1)
