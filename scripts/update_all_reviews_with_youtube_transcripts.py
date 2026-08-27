import os
import sys
import json
import glob
from datetime import datetime

sys.path.append(os.path.dirname(__file__))

from ai.deep_researcher import conduct_10_source_deep_research
from ai.synthesizer import generate_review_mdx
from sources.multi_source_detector import match_whitelisted_device

def update_all_reviews():
    print("🚀 [Batch Upgrade] 기 작성된 모든 리뷰글에 '5+ 유튜브 영상 트랜스크립트 교차 분석' 원칙 전면 적용 시작...\n")

    with open("src/data/devices.json", "r", encoding="utf-8") as f:
        devices_db = json.load(f)

    review_files = sorted(glob.glob("src/content/reviews/*.mdx"))
    print(f"📋 총 {len(review_files)}개 리뷰 파일 발견. 순차적 트랜스크립트 추출 및 심층 재합성 진행...")

    updated_count = 0

    for idx, r_file in enumerate(review_files, 1):
        slug = os.path.basename(r_file).replace(".mdx", "")
        print(f"\n========================================================")
        print(f"[{idx}/{len(review_files)}] 기기 처리 중: {slug}")
        print(f"========================================================")

        matched_dev = None
        for d in devices_db:
            if d.get("id") == slug:
                matched_dev = d
                break
        
        if not matched_dev:
            matched_dev = match_whitelisted_device(slug, devices_db)

        if not matched_dev:
            print(f"⚠️ [Skip] DB에서 '{slug}' 기기 매칭 실패. 스킵합니다.")
            continue

        dev_name = matched_dev.get("name_kr") or matched_dev.get("name")
        # 1. 5+ 유튜브 트랜스크립트 및 10+ 출처 심층 리서치
        deep_data = conduct_10_source_deep_research(matched_dev)

        # 1.5 기기 정품 이미지 자동 수집 & 검증
        try:
            from auto_image_fetcher import fetch_device_image
            fetch_device_image(slug)
        except Exception as e:
            print(f"⚠️ [Image Warning] {e}")

        # 2. 5대 유튜버 자막 교차 분석 및 정밀 MDX 재합성
        res = generate_review_mdx(
            device_obj=matched_dev,
            raw_facts={"specs": matched_dev.get("specs", {}), "release_date": matched_dev.get("release_date", "2026")},
            deep_research_data=deep_data
        )
        if isinstance(res, tuple):
            _, mdx_content = res
        else:
            mdx_content = res

        # 3. 파일 저장
        with open(r_file, "w", encoding="utf-8") as f:
            f.write(mdx_content)

        updated_count += 1
        print(f"✅ [{slug}] 5+ 유튜브 트랜스크립트 기반 리뷰 갱신 완료!")

    print(f"\n🎉 [Batch Upgrade Complete] 총 {updated_count}개 리뷰 글 갱신 완료!")
    print("\n🌐 [Multilingual Sync] 영어(en/) 및 일본어(ja/) 글로벌 에디션 동기화 시작...")
    import subprocess
    subprocess.run(["python3", "scripts/generate_multilingual_reviews.py"], check=True)

if __name__ == "__main__":
    update_all_reviews()
