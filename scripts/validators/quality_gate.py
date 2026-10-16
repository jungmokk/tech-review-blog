import re

def validate_mdx_content(mdx_content, device_obj=None):
    """
    생성된 MDX 콘텐츠가 ITSub 스타일의 심층 품질 게이트를 통과하는지 검증
    (Frontmatter 필수값, 기기명 일치 검증, 필수 분석 섹션, 최소 글자수 1,000자 이상)
    """
    errors = []
    
    # 1. Frontmatter 존재 여부
    if not mdx_content.startswith("---"):
        errors.append("Frontmatter가 존재하지 않습니다.")
        
    # 2. 필수 필드 검사
    required_fields = ["title:", "date:", "device:", "score:", "summary:", "pros:", "cons:"]
    for field in required_fields:
        if field not in mdx_content:
            errors.append(f"필수 필드 누락: {field}")

    # 2-B. 제목 및 요약 오염 검증
    m_title = re.search(r'^title:\s*"(.*?)"', mdx_content, re.M)
    m_sum = re.search(r'^summary:\s*"(.*?)"', mdx_content, re.M)
    title_val = m_title.group(1) if m_title else ""
    sum_val = m_sum.group(1) if m_sum else ""

    if "실사용 벤치마크 및 장단점 분석:" in sum_val or "실사용 벤치마크 및 장단점 분석:" in title_val:
        errors.append("Frontmatter title 또는 summary에 원시 유튜브 메타데이터 오염 문구가 포함되어 있습니다.")

    if device_obj:
        kr_name = re.sub(r'\s*\([^)]*\)', '', device_obj.get("name_kr", "")).strip()
        en_name = re.sub(r'\s*\([^)]*\)', '', device_obj.get("name", "")).strip()
        if kr_name and en_name:
            if kr_name.lower() not in title_val.lower() and en_name.lower() not in title_val.lower():
                errors.append(f"Frontmatter title('{title_val}')에 대상 기기명('{kr_name}' 또는 '{en_name}')이 누락되었습니다.")
            
    # 3. 최소 글자수 검사 (1,000자 이상 심층 리뷰 기준)
    cleaned_len = len(mdx_content.strip())
    if cleaned_len < 1000:
        errors.append(f"글자수 부족 (현재 {cleaned_len}자 / 최소 1,000자 이상 심층 리뷰 필요)")

    # 4. 필수 핵심 분석 섹션 검사 (스펙 백과 최우선)
    essential_sections = [
        ("스펙 백과/명세", ["스펙", "핵심 스펙", "사양", "스펙 백과", "Spec"]),
        ("요약", ["3초 요약", "한줄 요약", "3줄 요약", "요약"]),
        ("단점/체크포인트", ["아쉬운 점", "단점", "체크포인트"]),
        ("구매 가이드/총평", ["구매 가이드", "가이드", "결론", "총평", "살까", "마무리"])
    ]
    for sec_name, keywords in essential_sections:
        if not any(kw in mdx_content for kw in keywords):
            errors.append(f"필수 섹션 누락: '{sec_name}' 관련 내용이 포함되어야 합니다.")

    # 5. 스펙 백과 및 비교 표(Table) 존재 검사
    if mdx_content.count("| :---") < 1:
        errors.append("스펙 백과사전 표(Spec Sheet Table)가 누락되었습니다.")
        
    return len(errors) == 0, errors

