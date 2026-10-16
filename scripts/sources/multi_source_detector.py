import os
import re
import urllib.request
import xml.etree.ElementTree as ET
import yaml
import json
from sources.queue_manager import is_within_release_cutoff

VARIANT_TOKENS = {
    "pro", "ultra", "plus", "mini", "fe", "air", "fold", "flip",
    "se", "lite", "gt", "neo", "xl", "max", "edge", "nfe",
    "프로", "울트라", "플러스", "미니", "폴드", "플립", "에어", "맥스", "엣지"
}

def normalize_text(text: str) -> str:
    """비교를 위한 공백/특수문자 제거 소문자 정규화"""
    return re.sub(r'[^a-z0-9가-힣]', '', (text or '').lower())

def clean_parentheses(text: str) -> str:
    """괄호 부연 설명 제거 (예: '어메이즈핏 밸런스 (AI 헬스케어 워치)' -> '어메이즈핏 밸런스')"""
    return re.sub(r'\s*\([^)]*\)', '', (text or '')).strip()

def check_variant_boundary(candidate_name: str, input_text: str) -> bool:
    """
    후보 기기명이 입력 텍스트에 포함될 때, 후보 기기명에 없는 상위/변형 접미사(Pro, Ultra, Plus, Mini, FE, T 등)가
    입력 텍스트의 기기명 직후에 붙어 다른 모델을 가리키는 경우 오탐으로 판정하여 차단합니다.
    """
    cand_clean = clean_parentheses(candidate_name).lower().replace("+", " plus ")
    inp_clean = (input_text or "").lower().replace("+", " plus ")

    # 후보 기기명의 핵심 영숫자/한글 토큰들이 모두 입력 텍스트에 존재하는지 확인
    cand_tokens = re.findall(r'[a-z0-9가-힣]+', cand_clean)
    if not cand_tokens:
        return False

    norm_inp = normalize_text(inp_clean)
    norm_cand = normalize_text(cand_clean)
    if norm_cand not in norm_inp:
        return False

    # 숫자 토큰이 정확히 일치하는지 확인 (예: '14'가 '140'이나 '14t'에 매칭되는 것 방지)
    cand_nums = re.findall(r'\d+', cand_clean)
    inp_alnum_tokens = set(re.findall(r'[a-z]*\d+[a-z]*', inp_clean))
    for num in cand_nums:
        # cand_clean 내에서 해당 숫자가 포함된 전체 영숫자 토큰 확인 (예: 's26', '13r', 'y700')
        cand_num_tokens = [t for t in cand_tokens if num in t]
        for cnt in cand_num_tokens:
            if cnt not in inp_alnum_tokens and not any(t == num for t in re.findall(r'\d+', inp_clean)):
                return False
            # 만약 cand에서는 순수 숫자('14')인데 입력에서는 '14t', '14r', '14c' 등으로만 존재하면 불일치
            if cnt == num:
                exact_num_matches = re.findall(rf'(?<![a-z0-9]){re.escape(num)}(?![a-z0-9])', inp_clean)
                if not exact_num_matches:
                    return False

    # 후보 기기명에 없는 변형 접미사가 입력 텍스트에서 기기명 바로 뒤에 따라붙는지 검사
    cand_token_set = set(cand_tokens)
    pattern = r'\b' + r'[\s\-_]*'.join(re.escape(t) for t in cand_tokens) + r'[\s\-_]+([a-z0-9가-힣]+)'
    m = re.search(pattern, inp_clean)
    if m:
        next_word = m.group(1)
        if next_word in VARIANT_TOKENS and next_word not in cand_token_set:
            return False

    return True

def match_whitelisted_device(input_text: str, devices_db: list) -> dict:
    """
    입력 텍스트(기사 제목 또는 유튜브 영상 제목)가 공인 기기 DB에 실제로 존재하는지 엄격한 경계 검증 수행.
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
        name_norm = normalize_text(clean_parentheses(dev.get("name")))
        name_kr_norm = normalize_text(clean_parentheses(dev.get("name_kr")))
        if name_norm and name_norm == norm_input:
            return dev
        if name_kr_norm and name_kr_norm == norm_input:
            return dev

    # 3. Strict Token & Variant Boundary Substring Match
    # 더 구체적인(긴) 이름과 최신 출시 기기부터 매칭되도록 정렬
    sorted_devs = sorted(
        devices_db,
        key=lambda d: (len(clean_parentheses(d.get("name", ""))), d.get("release_year", 0)),
        reverse=True
    )
    for dev in sorted_devs:
        raw_name = clean_parentheses(dev.get("name", ""))
        raw_kr = clean_parentheses(dev.get("name_kr", ""))
        name_norm = normalize_text(raw_name)
        name_kr_norm = normalize_text(raw_kr)
        
        if name_norm and len(name_norm) >= 5 and name_norm in norm_input:
            if check_variant_boundary(raw_name, input_text):
                return dev
        if name_kr_norm and len(name_kr_norm) >= 4 and name_kr_norm in norm_input:
            if check_variant_boundary(raw_kr, input_text):
                return dev

    return None

def detect_new_devices_from_feeds(sources_file="data/sources.yaml", published_file="data/published.json", enforce_cutoff: bool = True):
    """
    1. 타겟 테크 블로그 RSS 피드 & 타겟 유튜버 영상 피드 스캔
    2. 공인 기기 엄격 매칭
    3. 출시일 하한선(최근 1개월 이내) 검증으로 과거 구형 기기 리뷰 생성 100% 차단
    4. 기존 작성 이력(Deduplication) 검증하여 '새로운 미작성 최신 기기'만 반환
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

    # 공인 DB 로드
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
                        elif enforce_cutoff and not is_within_release_cutoff(matched):
                            print(f"  ⏩ [Skip - 출시 1개월 경과 구형 기기] '{matched['name']}' (출시: {matched.get('release_date')}) from {name}")
                        else:
                            print(f"  ✨ [NEW 최신 기기 감지] '{matched['name']}' ({dev_id}, 출시: {matched.get('release_date')}) from {name} (제목: {title[:40]}...)")
                            detected_candidates.append({
                                "device": matched,
                                "trigger_type": "RSS",
                                "trigger_source": name,
                                "trigger_title": title,
                                "trigger_link": link
                            })
        except Exception:
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
                for entry in root.findall("{http://www.w3.org/2005/Atom}entry")[:5]:
                    title = entry.findtext("{http://www.w3.org/2005/Atom}title") or ""
                    link_elem = entry.find("{http://www.w3.org/2005/Atom}link")
                    link = link_elem.attrib.get("href", "") if link_elem is not None else ""
                    yt_vid = None
                    m_vid = re.search(r'(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})', link)
                    if m_vid:
                        yt_vid = m_vid.group(1)
                    
                    matched = match_whitelisted_device(title, devices_db)
                    if matched:
                        dev_id = matched.get("id")
                        if dev_id in published_devices:
                            print(f"  ⏩ [Skip - 이미 작성됨] '{matched['name']}' ({dev_id}) from 유튜버 [{cname}]")
                        elif enforce_cutoff and not is_within_release_cutoff(matched):
                            print(f"  ⏩ [Skip - 출시 1개월 경과 구형 기기] '{matched['name']}' (출시: {matched.get('release_date')}) from 유튜버 [{cname}]")
                        else:
                            print(f"  🔥 [NEW 최신 유튜브 영상 감지] '{matched['name']}' ({dev_id}, 출시: {matched.get('release_date')}) from [{cname}] (제목: {title[:40]}...)")
                            detected_candidates.append({
                                "device": matched,
                                "trigger_type": "YouTube",
                                "trigger_source": cname,
                                "trigger_title": title,
                                "trigger_link": link,
                                "trigger_youtube_id": yt_vid
                            })
        except Exception:
            pass

    # 중복 제거 (동일 기기가 여러 소스에서 감지된 경우 1개로 병합)
    unique_devices = {}
    for item in detected_candidates:
        d_id = item["device"]["id"]
        if d_id not in unique_devices:
            unique_devices[d_id] = item

    return list(unique_devices.values())

