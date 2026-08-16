import json
import os
import sys

def validate_smartphones_db(filepath="src/data/smartphones.json"):
    """
    스마트폰 스펙 데이터베이스 무결성 정밀 검증기
    """
    if not os.path.exists(filepath):
        print(f"❌ [Validator ERROR] 데이터베이스 파일이 존재하지 않습니다: {filepath}")
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except Exception as e:
            print(f"❌ [Validator ERROR] JSON 파싱 오류: {e}")
            return False

    if not isinstance(data, list) or len(data) == 0:
        print("❌ [Validator ERROR] 데이터베이스가 비어있거나 올바른 리스트 형식이 아닙니다.")
        return False

    required_top_keys = ["id", "name", "name_kr", "brand", "brand_kr", "release_year", "release_date", "specs"]
    required_spec_keys = ["ap", "display", "ram_storage", "camera", "battery", "dimensions_weight", "os_durability", "price_krw"]

    seen_ids = set()
    errors = []

    for i, item in enumerate(data):
        item_name = item.get("name", f"Item #{i}")
        
        # 1. 상위 필수 키 검사
        for key in required_top_keys:
            if key not in item or not item[key]:
                errors.append(f"[{item_name}] 필수 키 누락 또는 공백: '{key}'")

        # 2. ID 중복 검사
        item_id = item.get("id")
        if item_id:
            if item_id in seen_ids:
                errors.append(f"[{item_name}] 중복된 ID 발견: '{item_id}'")
            seen_ids.add(item_id)

        # 3. 출시 연도 범위 검사 (2023 ~ 2026)
        year = item.get("release_year")
        if year not in [2023, 2024, 2025, 2026]:
            errors.append(f"[{item_name}] 비정상 출시 연도: {year} (2023~2026 범위 필요)")

        # 4. 스펙 하위 키 검사
        specs = item.get("specs", {})
        if not isinstance(specs, dict):
            errors.append(f"[{item_name}] 'specs' 필드가 딕셔너리 형태가 아닙니다.")
        else:
            for spec_key in required_spec_keys:
                if spec_key not in specs or not str(specs[spec_key]).strip():
                    errors.append(f"[{item_name}] 스펙 항목 누락 또는 공백: 'specs.{spec_key}'")

    if errors:
        print(f"❌ [Validator ERROR] 총 {len(errors)}개의 데이터 결함이 발견되었습니다:")
        for err in errors[:10]:
            print(f"  - {err}")
        if len(errors) > 10:
            print(f"  ... 외 {len(errors) - 10}개 오류 생략")
        return False

    print(f"✅ [Validator SUCCESS] 총 {len(data)}개 스마트폰 스펙 데이터가 100% 무결성 검증을 통과했습니다!")
    return True

if __name__ == "__main__":
    success = validate_smartphones_db()
    if not success:
        sys.exit(1)
