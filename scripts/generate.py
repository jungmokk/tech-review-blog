import sys
import os
import re
import json
import argparse
import subprocess
from sources.multi_source_detector import detect_new_devices_from_feeds, match_whitelisted_device
from ai.deep_researcher import conduct_10_source_deep_research
from ai.synthesizer import generate_review_mdx
from validators.quality_gate import validate_mdx_content

def load_whitelisted_devices():
    """src/data/devices.json에서 201종 100% 공인 기기 데이터베이스 로드"""
    db_path = "src/data/devices.json"
    if not os.path.exists(db_path):
        db_path = "src/data/smartphones.json"
    with open(db_path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description="이벤트 기반 10+ 다각도 출처 종합 심층 테크 리뷰 생성 파이프라인")
    parser.add_argument("--device", type=str, help="특정 공인 기기 수동 지정 발행 (예: 'galaxy-s26-ultra')")
    parser.add_argument("--force", action="store_true", help="중복 체크 무시하고 강제 재생성")
    args = parser.parse_args()

    devices_db = load_whitelisted_devices()
    print(f"📦 [Pipeline Init] 201종 공인 하드웨어 DB 로드 완료 (총 {len(devices_db)}개 기기)")

    published_file = "data/published.json"
    published_data = {"published_devices": []}
    if os.path.exists(published_file):
        try:
            with open(published_file, "r", encoding="utf-8") as f:
                published_data = json.load(f)
        except Exception:
            pass

    target_candidate = None

    if args.device:
        # 사용자가 특정 기기를 수동 지정하여 실행한 경우
        matched = match_whitelisted_device(args.device, devices_db)
        if not matched:
            print(f"\n⛔ [Pipeline REJECTED] '{args.device}'는 공식 201종 하드웨어 기기 DB에 등록되지 않은 항목입니다.")
            sys.exit(1)
        target_candidate = {
            "device": matched,
            "trigger_type": "Manual CLI",
            "trigger_source": "User Manual Input",
            "trigger_title": args.device
        }
    else:
        # 타겟 RSS 피드 및 타겟 유튜버 최신 영상 피드 스캔
        print("\n📡 [Pipeline Step 1] 타겟 RSS 피드 및 주요 테크 유튜버 최신 업로드 감지 시작...")
        candidates = detect_new_devices_from_feeds(sources_file="data/sources.yaml", published_file=published_file)
        
        if not candidates:
            print("\n☕ [Pipeline Idle] 타겟 RSS 피드 및 유튜버 채널에 새로운 미발행 하드웨어 기기가 감지되지 않았습니다.")
            print("   (매일 무의미하게 글을 쓰지 않고, 새로운 기기 소식이 감지될 때만 10개 이상 출처를 심층 분석하여 발행합니다.)")
            return

        target_candidate = candidates[0]
        print(f"\n🎯 [Target Detected] {target_candidate['trigger_type']} [{target_candidate['trigger_source']}]에서 신규 기기 감지!")
        print(f"   기기명: {target_candidate['device']['name']} (ID: {target_candidate['device']['id']})")
        print(f"   트리거 제목: {target_candidate['trigger_title']}")

    dev_obj = target_candidate["device"]
    dev_id = dev_obj.get("id")
    dev_name = dev_obj.get("name_kr") or dev_obj.get("name")

    # 기존 발행 이력 중복 검증 (Deduplication Gate)
    if dev_id in published_data.get("published_devices", []) and not args.force:
        print(f"\n⏩ [Pipeline SKIP] '{dev_name}' ({dev_id})는 이미 블로그에 발행된 기기입니다. 생성을 안전하게 스킵합니다.")
        return

    # STEP 2: 10개 이상 다각도 출처(유튜버 실사용기 + 테크 블로그 + 랩 테스트) 심층 리서치
    print(f"\n🔬 [Pipeline Step 2] '{dev_name}'에 대한 10개 이상 출처 심층 종합 리서치 수행 중...")
    deep_research_data = conduct_10_source_deep_research(dev_obj)

    # STEP 3: 100% 팩트 스펙 + 10+ 출처 종합 고품질 리뷰 MDX 생성
    print(f"\n✍️ [Pipeline Step 3] 10+ 출처 리포트 기반 심층 테크 리뷰 MDX 합성 중...")
    raw_facts = {
        "id": dev_id,
        "device": dev_name,
        "brand": dev_obj.get("brand_kr") or dev_obj.get("brand"),
        "category": dev_obj.get("category", "스마트폰/IT"),
        "device_type": dev_obj.get("device_type", "스마트폰"),
        "release_date": dev_obj.get("release_date", "2026"),
        "release_year": dev_obj.get("release_year", 2026),
        "specs": dev_obj.get("specs", {}),
        "image": dev_obj.get("image", f"/images/devices/{dev_id}.webp"),
        "sources": [ref["name"] for ref in deep_research_data.get("references", [])]
    }

    slug, mdx_content = generate_review_mdx(dev_obj, raw_facts, deep_research_data=deep_research_data)

    # STEP 4: 품질 검증 (Quality Gate)
    is_valid, errors = validate_mdx_content(mdx_content)
    if not is_valid:
        print(f"\n⛔ [Pipeline ERROR] 품질 검증 실패: {errors}")
        sys.exit(1)

    # MDX 저장
    os.makedirs("src/content/reviews", exist_ok=True)
    file_path = f"src/content/reviews/{slug}.mdx"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(mdx_content)

    # 레지스트리 업데이트 (Deduplication 기록)
    if dev_id not in published_data.get("published_devices", []):
        published_data.setdefault("published_devices", []).append(dev_id)
    with open(published_file, "w", encoding="utf-8") as f:
        json.dump(published_data, f, ensure_ascii=False, indent=2)

    # STEP 5: 글로벌 다국어(en, ja) 리뷰 자동 동기화 생성
    try:
        print("\n🌐 [Pipeline Step 5] 영어(en/) 및 일본어(ja/) 글로벌 에디션 동시 생성 중...")
        subprocess.run([sys.executable, "scripts/generate_multilingual_reviews.py"], check=True)
    except Exception as e:
        print(f"⚠️ [Multilingual Sync Warning] 다국어 생성 중 경고: {e}")

    # STEP 6: 이미지 무결성 검증
    try:
        print("\n🖼️ [Pipeline Step 6] 전체 기기 이미지 무결성 검증 수행 중...")
        subprocess.run([sys.executable, "scripts/verify_images.py"], check=True)
    except Exception as e:
        print(f"⚠️ [Image Verify Warning] 이미지 검증 중 경고: {e}")

    print(f"\n🎉 [Pipeline SUCCESS] 10+ 출처가 완벽히 반영된 최고 품질의 심층 리뷰가 발행되었습니다: {file_path}")

if __name__ == "__main__":
    main()
