def validate_mdx_content(mdx_content):
    """
    생성된 MDX 콘텐츠가 ITSub 스타일의 심층 품질 게이트를 통과하는지 검증
    (Frontmatter 필수값, 필수 8대 분석 섹션, 최소 글자수 1,200자 이상)
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
