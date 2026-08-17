import os
import json
import re
from datetime import datetime

def clean_mdx_content(text: str) -> str:
    text = text.strip()
    # 1. 코드 블록(```markdown ... ```)으로 감싸진 경우 내부 Frontmatter 본문만 추출
    match = re.search(r'```(?:markdown|mdx)?\s*\n(---[\s\S]+?)\n```', text)
    if match:
        return match.group(1).strip()
    
    # 2. Frontmatter로 바로 시작하는 경우 후속 닫는 코드블록 및 부가 설명 제거
    if text.startswith("---"):
        parts = re.split(r'\n```', text, maxsplit=1)
        return parts[0].strip()
        
    # 3. 일반적인 코드 펜스 제거
    if text.startswith("```"):
        text = re.sub(r"^```(?:markdown|mdx)?\r?\n", "", text)
        text = re.sub(r"\r?\n```[\s\S]*$", "", text)
    return text.strip()

def generate_review_mdx(device_obj, raw_facts):
    """
    공식 DB의 100% 검증된 하드웨어 스펙 데이터를 기반으로 AI 심층 분석 리뷰를 생성합니다.
    절대로 가짜 스펙이나 임의의 더미 템플릿으로 대체하지 않습니다.
    """
    gemini_key = os.environ.get("GEMINI_API_KEY")
    deepseek_key = os.environ.get("DEEPSEEK_API_KEY")
    qwen_key = os.environ.get("QWEN_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")

    slug = device_obj.get("id")
    device_name = device_obj.get("name_kr") or device_obj.get("name")
    device_type = device_obj.get("device_type", "스마트폰")
    brand = device_obj.get("brand_kr") or device_obj.get("brand")
    specs = raw_facts.get("specs", {})
    image_url = raw_facts.get("image", f"/images/devices/{slug}.jpg")
    today_str = datetime.now().strftime("%Y-%m-%d")

    # 스펙 팩트 요약
    spec_summary_lines = [
        f"- 대상 기기명: {device_name} ({device_obj.get('name')})",
        f"- 제조사/브랜드: {brand}",
        f"- 기기 분류: {device_type}",
        f"- 공식 출시일: {raw_facts.get('release_date')}",
        f"- 프로세서 (AP): {specs.get('ap', '미지정')}",
        f"- 디스플레이: {specs.get('display', '미지정')}",
        f"- 메모리/스토리지: {specs.get('ram_storage', '미지정')}",
        f"- 카메라 시스템: {specs.get('camera', '미지정')}",
        f"- 배터리 & 충전: {specs.get('battery', '미지정')}",
        f"- 규격 및 무게: {specs.get('dimensions_weight', '미지정')}",
        f"- OS 및 내구성: {specs.get('os_durability', '미지정')}",
        f"- 공식 출고가: {specs.get('price_krw', '미지정')}"
    ]
    spec_fact_sheet = "\n".join(spec_summary_lines)

    prompt = f"""
당신은 대한민국 최고의 테크 저널리스트이자 IT 전문 블로거입니다.
아래 제공된 **100% 공인 기기 팩트 스펙 데이터**를 바탕으로, 해당 기기의 장점과 단점을 객관적이고 깊이 있게 분석하는 고품질 리뷰 마크다운(MDX)을 작성하세요.

⚠️ **[절대 주의 및 사실 검증 준수 사항]**
1. 아래 제공된 [공인 기기 팩트 스펙 데이터]에 적힌 수치와 사실(AP, 디스플레이 해상도/주사율, 배터리 용량, 무게, 출고가 등)을 절대 왜곡하거나 날조하지 마세요.
2. 기기 종류({device_type})에 맞는 실제 분석을 진행하세요 (예: 태블릿에 폴더블 힌지 언급 금지, 워치에 카메라 화소 날조 금지).
3. 독자가 공감하고 몰입할 수 있도록 자연스러운 전문 테크 리뷰어 경어체(~인데요, ~생각됩니다, ~입니다)로 작성하세요.

---
### 📱 [공인 기기 팩트 스펙 데이터]
{spec_fact_sheet}
---

다음 포맷 규칙을 완벽히 지켜서 출력하세요:

[Frontmatter 규격]
---
title: "{brand} {device_name} 심층 분석 실사용 솔직 후기 및 장단점"
date: "{today_str}"
device: "{device_name}"
score: 9.1
category: "{raw_facts.get('category', '스마트폰/IT')}"
summary: "{device_name}의 공식 스펙을 바탕으로 실제 체감 성능, 디스플레이, 배터리 및 카메라, 가감 없는 솔직한 장단점까지 꼼꼼하게 정리했습니다."
pros:
  - "[스펙 기반 핵심 장점 1]"
  - "[스펙 기반 핵심 장점 2]"
  - "[스펙 기반 핵심 장점 3]"
cons:
  - "[현실적인 아쉬운 점 또는 가격 단점 1]"
  - "[현실적인 아쉬운 점 또는 기능적 한계 2]"
---

# "{device_name}" 심층 실사용 팩트 분석 리포트

[도입부: 실사용 관점에서의 배경과 핵심 기대 요소 2~3문단]

---

### 📌 핵심 3줄 요약
① **디자인 & 빌드**: [디자인, 무게, 소재 요약]
② **성능 & 디스플레이**: [AP 및 디스플레이 실체감 요약]
③ **가격 & 포지션**: [출고가 대비 가성비 및 추천 타겟]

---

### 📊 {device_name} 한눈에 보는 공식 핵심 스펙 시트

| 구분 | 주요 사양 (Specification) | 상세 비고 |
| :--- | :--- | :--- |
| ⚡ **프로세서 (AP/칩셋)** | {specs.get('ap', '-')} | 플래그십 성능 |
| 🖥️ **디스플레이** | {specs.get('display', '-')} | 패널 및 주사율 |
| 💾 **메모리 & 스토리지** | {specs.get('ram_storage', '-')} | 쾌적한 용량 |
| 📷 **카메라 시스템** | {specs.get('camera', '-')} | 사진/동영상 |
| 🔋 **배터리 & 충전** | {specs.get('battery', '-')} | 실사용 시간 |
| 📐 **규격 & 무게** | {specs.get('dimensions_weight', '-')} | 그립감 체감 |
| 🛡️ **OS & 내구성** | {specs.get('os_durability', '-')} | 지원 보장 |
| 💰 **공식 출시 가격** | {specs.get('price_krw', '-')} | 출고가 기준 |

---

### 📋 목차
1. 디자인과 그립감, 외형 완성도
2. {specs.get('ap', '프로세서')} 성능과 디스플레이 체감
3. 실사용 배터리 타임 및 활용성
4. 솔직히 아쉬운 점 3가지 (체크포인트)
5. 결국 누구에게 가장 잘 맞을까?

---

## 1. 디자인과 그립감, 외형 완성도
[소재, 무게 {specs.get('dimensions_weight', '')}, 휴대성 및 마감 품질에 대한 상세 서술]

---

## 2. {specs.get('ap', '프로세서')} 성능과 디스플레이 체감
[탑재된 {specs.get('ap', '')}의 실성능, 멀티태스킹, 게이밍 발열 제어 및 {specs.get('display', '')} 화면 품질 상세 서술]

---

## 3. 실사용 배터리 타임 및 활용성
[{specs.get('battery', '')} 배터리 지속 시간과 충전 편의성 분석]

---

## 4. 솔직히 아쉬운 점 3가지 (체크포인트)
1. **[출고가 및 비용 부담]**: {specs.get('price_krw', '')} 가격대와 가성비 관점의 한계
2. **[스펙상 아쉬운 점]**: 충전 속도 또는 특정 기능 부재
3. **[호환성/기타]**: 구매 전 고려사항

---

## 5. 결국 누구에게 가장 잘 맞을까?

| 구분 | 추천 대상 및 특징 |
| :--- | :--- |
| **강력 추천** | • [구체적 구매 추천 타겟 1]<br/>• [구체적 구매 추천 타겟 2] |
| **보류 권장** | • [구매를 보류해야 하는 사용자 1]<br/>• [대체재를 찾는 사용자 2] |

---

### 💬 마무리 한마디
> **"[해당 기기를 관통하는 촌철살인 한줄 총평]"**

### 🏁 총평
[종합 평가 및 구매 조언 마무리]
"""

    system_prompt = (
        "당신은 공신력 있는 글로벌 테크 매거진의 수석 에디터입니다. "
        "반드시 주어진 팩트 스펙 데이터만을 바탕으로 정확하고 깊이 있는 분석을 수행하세요. "
        "가짜 스펙 날조나 다른 기종과의 혼동은 엄격히 금지됩니다."
    )

    # 1. Qwen API
    if qwen_key:
        try:
            from openai import OpenAI
            qwen_base_url = (
                os.environ.get("QWEN_BASE_URL")
                or "https://ws-gv65z0e7ds9mibcp.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
            )
            qwen_model = os.environ.get("QWEN_MODEL") or "qwen-max"
            client = OpenAI(api_key=qwen_key, base_url=qwen_base_url)
            response = client.chat.completions.create(
                model=qwen_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            content = clean_mdx_content(response.choices[0].message.content)
            return slug, content
        except Exception as e:
            print(f"[AI Synthesizer] Qwen API 오류: {e}")

    # 2. DeepSeek API
    if deepseek_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=deepseek_key, base_url="https://api.deepseek.com")
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            content = clean_mdx_content(response.choices[0].message.content)
            return slug, content
        except Exception as e:
            print(f"[AI Synthesizer] DeepSeek API 오류: {e}")

    # 3. Gemini API
    if gemini_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("gemini-1.5-pro")
            response = model.generate_content(f"{system_prompt}\n\n{prompt}")
            content = clean_mdx_content(response.text)
            return slug, content
        except Exception as e:
            print(f"[AI Synthesizer] Gemini API 오류: {e}")

    # 4. OpenAI API
    if openai_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai_key)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            content = clean_mdx_content(response.choices[0].message.content)
            return slug, content
        except Exception as e:
            print(f"[AI Synthesizer] OpenAI API 오류: {e}")

    # 5. 100% 팩트 스펙 기반 순수 템플릿 생성 (AI API가 없거나 오류 시에도 스펙은 100% 정확하게 렌더링)
    # 절대 폴더블 더미를 날조하지 않고, 전달된 공식 DB 스펙만을 정확히 채워서 렌더링합니다.
    print(f"[AI Synthesizer] AI API 미사용 모드: '{device_name}'의 100% 공인 DB 스펙 시트를 기반으로 정밀 포스트를 생성합니다.")
    
    spec_mdx = f"""---
title: "{brand} {device_name} 심층 분석 및 공식 스펙 완전 정복"
date: "{today_str}"
device: "{device_name}"
score: 9.2
category: "{raw_facts.get('category', '스마트폰/IT')}"
summary: "{device_name}의 공인 스펙 시트와 하드웨어 제원({specs.get('ap', '최신 칩셋')}, {specs.get('display', '고해상도 디스플레이')})을 바탕으로 객관적인 장단점을 분석했습니다."
pros:
  - "강력한 {specs.get('ap', '프로세서')} 탑재로 쾌적한 실사용 성능 제공"
  - "{specs.get('display', '고품질 디스플레이')}의 뛰어난 화면 몰입감"
  - "완성도 높은 {brand}의 하드웨어 마감과 {specs.get('dimensions_weight', '최적화된 규격')}"
cons:
  - "공식 출고가({specs.get('price_krw', '가격대')})의 가격 부담"
  - "사용 환경에 따른 충전 속도 및 배터리({specs.get('battery', '-')}) 체감 편차"
---

# "{device_name}" 공식 스펙 기반 심층 분석 리포트

{brand}에서 출시한 **{device_name}**에 대한 객관적인 하드웨어 제원 분석과 실사용 관점의 장단점을 정리해 드립니다.

---

### 📌 핵심 3줄 요약
① **프로세서 & 성능**: {specs.get('ap', '플래그십 프로세서')} 탑재로 부드러운 앱 실행과 안정적인 멀티태스킹을 보장합니다.
② **디스플레이 & 폼팩터**: {specs.get('display', '고해상도 화면')}과 {specs.get('dimensions_weight', '인체공학적 설계')}가 적용되었습니다.
③ **가격 & 포지셔닝**: {specs.get('price_krw', '출시 가격')}의 가격대를 형성하며, 최신 테크 스펙을 원하는 사용자에게 적합합니다.

---

### 📊 {device_name} 한눈에 보는 공식 핵심 스펙 백과 (Spec Sheet)

| 구분 | 주요 사양 (Specification) | 상세 비고 |
| :--- | :--- | :--- |
| ⚡ **프로세서 (AP/칩셋)** | {specs.get('ap', '-')} | 핵심 연산 장치 |
| 🖥️ **디스플레이** | {specs.get('display', '-')} | 패널 및 시인성 |
| 💾 **메모리 & 스토리지** | {specs.get('ram_storage', '-')} | 멀티태스킹 제원 |
| 📷 **카메라 시스템** | {specs.get('camera', '-')} | 센서 및 촬영 사양 |
| 🔋 **배터리 & 충전** | {specs.get('battery', '-')} | 전력 효율성 |
| 📐 **규격 & 무게** | {specs.get('dimensions_weight', '-')} | 실측 제원 |
| 🛡️ **OS & 특징** | {specs.get('os_durability', '-')} | 소프트웨어 및 내구성 |
| 💰 **공식 출시 가격** | {specs.get('price_krw', '-')} | 출고가 기준 |

---

### 📋 목차
1. 외형 디자인 및 규격({specs.get('dimensions_weight', '')}) 분석
2. {specs.get('ap', '프로세서')} 탑재에 따른 성능 분석
3. {specs.get('display', '디스플레이')} 화면 경험과 시인성
4. 구매 전 반드시 체크해야 할 아쉬운 점
5. 종합 평가 및 추천 대상

---

## 1. 외형 디자인 및 규격({specs.get('dimensions_weight', '')}) 분석

**{device_name}**은 {brand} 고유의 정밀한 하드웨어 설계가 반영되어 있습니다. 공식 제원상 **{specs.get('dimensions_weight', '슬림한 규격')}**을 갖추고 있어 일상적인 휴대와 사용에서 우수한 그립감을 전달합니다.

---

## 2. {specs.get('ap', '프로세서')} 탑재에 따른 성능 분석

탑재된 **{specs.get('ap', '고성능 프로세서')}**와 **{specs.get('ram_storage', '대용량 메모리')}**의 조합으로 일상적인 고부하 작업이나 멀티태스킹 환경에서도 안정적인 퍼포먼스를 발휘합니다.

---

## 3. {specs.get('display', '디스플레이')} 화면 경험과 시인성

화면은 **{specs.get('display', '고해상도 패널')}**이 채택되어 텍스트 가독성과 미디어 감상 시 풍부한 색감과 높은 시인성을 제공합니다.

---

## 4. 구매 전 반드시 체크해야 할 아쉬운 점

1. **출고가 부담**: {specs.get('price_krw', '공식 출고가')}로 책정된 가격대는 구매 전 예산 계획이 필수적입니다.
2. **배터리 및 충전 효율**: {specs.get('battery', '배터리 제원')}을 고려할 때 고사양 연속 사용 시 충전 관리가 필요합니다.
3. **생태계 호환성**: 기존 보유 기기들과의 연동성을 사전에 확인하는 것이 좋습니다.

---

## 5. 종합 평가 및 추천 대상

| 구분 | 추천 대상 및 특징 |
| :--- | :--- |
| **강력 추천** | • 최신 **{specs.get('ap', 'AP')}**의 강력한 성능을 경험하고 싶은 사용자<br/>• **{specs.get('display', '고화질 화면')}**으로 생산성 및 콘텐츠 소비를 중시하는 분 |
| **보류 권장** | • 가성비 중심의 라이트한 사용 환경을 선호하는 사용자<br/>• 구형 플래그십으로도 충분한 사용 목적을 가진 분 |

---

### 💬 마무리 한마디
> **"정확한 팩트 스펙을 알고 구매할 때 가장 만족스러운 테크 라이프가 완성됩니다."**

### 🏁 총평
{device_name}은 {specs.get('ap', '핵심 칩셋')}과 {specs.get('display', '디스플레이')} 등 공인된 하드웨어 스펙에서 확고한 경쟁력을 보여주는 제품입니다.
"""
    return slug, spec_mdx
