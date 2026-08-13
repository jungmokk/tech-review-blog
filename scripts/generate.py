import sys
import os
import json
import argparse
from sources.rss_fetcher import fetch_rss_items
from ai.synthesizer import generate_review_mdx
from validators.quality_gate import validate_mdx_content

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
        if rss_items:
            target_device = rss_items[0].get("title", "M4 Mac Mini")
            print(f"[Pipeline] 감지된 항목 중 수집 대상 결정: {target_device}")
        else:
            target_device = "M4 Mac Mini"

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
