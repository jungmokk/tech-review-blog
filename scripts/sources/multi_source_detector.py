import os
import re
import urllib.request
import xml.etree.ElementTree as ET
import yaml
import json

def normalize_text(text: str) -> str:
    """비교를 위한 공백/특수문자 제거 소문자 정규화"""
    return re.sub(r'[^a-z0-9가-힣]', '', (text or '').lower())

def match_whitelisted_device(input_text: str, devices_db: list) -> dict:
    """
    입력 텍스트(기사 제목 또는 유튜브 영상 제목)가 201종 공인 기기 DB에 실제로 존재하는지 100% 화이트리스트 검증.
    """
    if not input_text:
        return None
    
    norm_input = normalize_text(input_text)
    
    # 1. Exact ID match (e.g. 'galaxy-s26-ultra')
    for dev in devices_db:
        dev_id_norm = normalize_text(dev.get("id"))
        if dev_id_norm == norm_input:
            return dev

    # 2. Exact Name or Korean Name match
    for dev in devices_db:
        name_norm = normalize_text(dev.get("name"))
        name_kr_norm = normalize_text(dev.get("name_kr"))
        if name_norm and name_norm == norm_input:
            return dev
        if name_kr_norm and name_kr_norm == norm_input:
            return dev

    # 3. Substring match (텍스트 안에 공인 기기 이름이 포함되어 있는지)
    # 더 구체적인(긴) 이름부터 매칭되도록 정렬
    sorted_devs = sorted(devices_db, key=lambda d: len(d.get("name", "")), reverse=True)
    for dev in sorted_devs:
        name_norm = normalize_text(dev.get("name"))
        name_kr_norm = normalize_text(dev.get("name_kr"))
        
        # 최소 4글자 이상의 고유 모델명이어야 오탐 방지
        if name_norm and len(name_norm) >= 4 and name_norm in norm_input:
            return dev
        if name_kr_norm and len(name_kr_norm) >= 4 and name_kr_norm in norm_input:
            return dev

    return None

def detect_new_devices_from_feeds(sources_file="data/sources.yaml", published_file="data/published.json"):
    """
    1. 타겟 테크 블로그 RSS 피드 & 타겟 유튜버 영상 피드 스캔
    2. 201종 공인 기기 매칭
    3. 기존 작성 이력(Deduplication) 검증하여 '새로운 미작성 기기'만 반환
    """
    if not os.path.exists(sources_file):
        print(f"⚠️ [Detector] {sources_file} 설정 파일이 없습니다.")
        return []

    try:
        with open(sources_file, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"⚠️ [Detector] sources.yaml 읽기 오류: {e}")
        return []

    # 201종 공인 DB 로드
    db_path = "src/data/devices.json"
    if not os.path.exists(db_path):
        db_path = "src/data/smartphones.json"
    with open(db_path, "r", encoding="utf-8") as f:
        devices_db = json.load(f)

    # 기존 발행 목록 로드
    published_devices = set()
    if os.path.exists(published_file):
        try:
            with open(published_file, "r", encoding="utf-8") as f:
                pdata = json.load(f)
                published_devices = set(pdata.get("published_devices", []))
        except Exception:
            pass

    # src/content/reviews/ 폴더 내 파일 직접 스캔으로 2중 검증
    reviews_dir = "src/content/reviews"
    if os.path.exists(reviews_dir):
        for fname in os.listdir(reviews_dir):
            if fname.endswith(".mdx") and not fname.startswith("index"):
                slug = fname.replace(".mdx", "")
                published_devices.add(slug)

    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
    detected_candidates = []

    # A. 글로벌/한국 테크 블로그 RSS 스캔
    print("📡 [Detector] 타겟 테크 블로그 RSS 피드 검사 중...")
    for source in config.get("rss_sources", []):
        name = source.get("name")
        url = source.get("url")
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as resp:
                xml_data = resp.read()
                root = ET.fromstring(xml_data)
                for item in root.findall(".//item")[:10]:
                    title = item.findtext("title") or ""
                    link = item.findtext("link") or ""
                    matched = match_whitelisted_device(title, devices_db)
                    if matched:
                        dev_id = matched.get("id")
                        if dev_id in published_devices:
                            print(f"  ⏩ [Skip - 이미 작성됨] '{matched['name']}' ({dev_id}) from {name}")
                        else:
                            print(f"  ✨ [NEW 기기 감지] '{matched['name']}' ({dev_id}) from {name} (제목: {title[:40]}...)")
                            detected_candidates.append({
                                "device": matched,
                                "trigger_type": "RSS",
                                "trigger_source": name,
                                "trigger_title": title,
                                "trigger_link": link
                            })
        except Exception as e:
            # print(f"  [Detector RSS error: {name}] {e}")
            pass

    # B. 타겟 테크 유튜버 최신 영상 피드 스캔
    print("🎥 [Detector] 타겟 테크 유튜버 최신 업로드 영상 검사 중...")
    for channel in config.get("youtube_channels", []):
        cname = channel.get("name")
        rss_url = channel.get("rss_url")
        if not rss_url:
            continue
        try:
            req = urllib.request.Request(rss_url, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as resp:
                xml_data = resp.read()
                root = ET.fromstring(xml_data)
                # Atom Feed (entry -> title)
                for entry in root.findall("{http://www.w3.org/2005/Atom}entry")[:5]:
                    title = entry.findtext("{http://www.w3.org/2005/Atom}title") or ""
                    link_elem = entry.find("{http://www.w3.org/2005/Atom}link")
                    link = link_elem.attrib.get("href", "") if link_elem is not None else ""
                    
                    matched = match_whitelisted_device(title, devices_db)
                    if matched:
                        dev_id = matched.get("id")
                        if dev_id in published_devices:
                            print(f"  ⏩ [Skip - 이미 작성됨] '{matched['name']}' ({dev_id}) from 유튜버 [{cname}]")
                        else:
                            print(f"  🔥 [NEW 유튜브 영상 감지] '{matched['name']}' ({dev_id}) from [{cname}] (제목: {title[:40]}...)")
                            detected_candidates.append({
                                "device": matched,
                                "trigger_type": "YouTube",
                                "trigger_source": cname,
                                "trigger_title": title,
                                "trigger_link": link
                            })
        except Exception as e:
            # print(f"  [Detector YT error: {cname}] {e}")
            pass

    # 중복 제거 (동일 기기가 여러 소스에서 감지된 경우 1개로 병합)
    unique_devices = {}
    for item in detected_candidates:
        d_id = item["device"]["id"]
        if d_id not in unique_devices:
            unique_devices[d_id] = item

    return list(unique_devices.values())
