import sys
import os
import re
import json
import argparse
from sources.rss_fetcher import fetch_rss_items
from ai.synthesizer import generate_review_mdx
from validators.quality_gate import validate_mdx_content

def extract_clean_device_name(title: str) -> str:
    """RSS 기사 제목에서 핵심 테크 기기 명칭을 추출 및 정제"""
    # 불필요한 언론사명, 접두사, 특수문자 제거
    clean = re.sub(r'\[.*?\]|\(.*?\)|Review:|Hands-on:|Leak:', '', title, flags=re.IGNORECASE).strip()
    
    # 대표 IT 제품 라인업 패턴 탐색
    patterns = [
        r'(Galaxy\s+[A-Za-z0-9\s]+(?:Ultra|Plus|Fold|Flip|FE|\d+)?)',
        r'(갤럭시\s+[A-Za-z0-9가-힣\s]+(?:울트라|플러스|폴드|플립|FE|\d+)?)',
        r'(iPhone\s+\d+(?:\s+Pro(?:\s+Max)?|\s+Plus|\s+Air|\s+SE)?)',
        r'(아이폰\s+\d+(?:\s+프로(?:\s+맥스)?|\s+플러스|\s+에어|\s+SE)?)',
        r'(iPad\s+[A-Za-z0-9\s]+)',
        r'(아이패드\s+[A-Za-z0-9가-힣\s]+)',
        r'(MacBook\s+[A-Za-z0-9\s]+)',
        r'(맥북\s+[A-Za-z0-9가-힣\s]+)',
        r'(AirPods\s+[A-Za-z0-9\s]+)',
        r'(에어팟\s+[A-Za-z0-9가-힣\s]+)',
        r'(Pixel\s+\d+(?:\s+Pro|\s+Fold|\s+a)?)',
        r'(픽셀\s+\d+(?:\s+프로|\s+폴드)?)',
        r'(PlayStation\s+\d+(?:\s+Pro)?)',
        r'(Nintendo\s+Switch\s+\d*)',
    ]
    for pat in patterns:
        m = re.search(pat, clean, re.IGNORECASE)
        if m:
            return m.group(1).strip()

    # 특정 패턴이 없을 경우 단어 수 제한하여 간결하게 반환
    words = clean.split()
    if len(words) > 4:
        return " ".join(words[:4])
    return clean or "신규 테크 기기"

def main():
    parser = argparse.ArgumentParser(description="테크 기기 리뷰 자동 포스팅 생성을 위한 파이프라인 CLI")
    parser.add_argument("--device", type=str, help="리뷰를 생성할 특정 기기명 (예: 'M4 Mac Mini')")
    parser.add_argument("--force", action="store_true", help="중복 체크 무시하고 강제 생성")
    args = parser.parse_args()

    published_file = "data/published.json"
    published_data = {"published_devices": []}
    if os.path.exists(published_file):
        try:
            with open(published_file, "r", encoding="utf-8") as f:
                published_data = json.load(f)
        except Exception:
            pass

    target_device = args.device
    if not target_device:
        print("[Pipeline] 수집 모드 시작: RSS 피드 탐색...")
        rss_items = fetch_rss_items()
        
        # 발행되지 않은 신규 기기 우선 탐색
        selected = None
        for item in rss_items:
            extracted = extract_clean_device_name(item.get("title", ""))
            if extracted and extracted not in published_data.get("published_devices", []):
                selected = extracted
                break
        
        target_device = selected if selected else "Galaxy Z Fold 8"
        print(f"[Pipeline] 감지된 항목 중 수집 대상 결정: {target_device}")

    # 중복 체크
    if target_device in published_data.get("published_devices", []) and not args.force:
        print(f"[Pipeline] '{target_device}'는 이미 발행된 기기입니다. (--force 옵션으로 재발행 가능)")
        return

    print(f"[Pipeline] '{target_device}' 리뷰 생성 및 합성 진행 중...")
    raw_facts = {"device": target_device, "sources": ["RSS Feeds", "Tech Media"]}
    slug, mdx_content = generate_review_mdx(target_device, raw_facts)

    # 품질 검증
    is_valid, errors = validate_mdx_content(mdx_content)
    if not is_valid:
        print(f"[Pipeline ERROR] 품질 검증 실패: {errors}")
        sys.exit(1)

    # MDX 저장
    os.makedirs("src/content/reviews", exist_ok=True)
    file_path = f"src/content/reviews/{slug}.mdx"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(mdx_content)

    # 레지스트리 업데이트
    published_data.setdefault("published_devices", []).append(target_device)
    with open(published_file, "w", encoding="utf-8") as f:
        json.dump(published_data, f, ensure_ascii=False, indent=2)

    print(f"🎉 성공적으로 리뷰가 생성되었습니다: {file_path}")

if __name__ == "__main__":
    main()
