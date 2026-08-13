def validate_mdx_content(mdx_content):
    """
    생성된 MDX 콘텐츠가 품질 게이트(Frontmatter 필수값, 최소 글자수 등)를 통과하는지 검증
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
            
    # 3. 최소 글자수 검사 (300자 이상)
    if len(mdx_content) < 300:
        errors.append(f"글자수 부족 (현재 {len(mdx_content)}자 / 최소 300자 필요)")
        
    return len(errors) == 0, errors
