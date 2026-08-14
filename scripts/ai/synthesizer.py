import os
import json
import re

def generate_review_mdx(device_name, raw_facts):
    """
    Gemini, DeepSeek, Qwen 등 선택된 AI 모델 API를 사용하여 테크 리뷰 포스트 MDX를 생성합니다.
    """
    gemini_key = os.environ.get("GEMINI_API_KEY")
    deepseek_key = os.environ.get("DEEPSEEK_API_KEY")
    qwen_key = os.environ.get("QWEN_API_KEY")
    
    slug = re.sub(r'[^a-z0-9]+', '-', device_name.lower()).strip('-')

    prompt = f"""
당신은 대한민국 최고 수준의 IT/테크 전문 리뷰 에디터입니다.
대상 리뷰 기기: {device_name}
수집된 팩트 및 정보 소스:
{json.dumps(raw_facts, ensure_ascii=False, indent=2)}

다음 요구사항에 맞춰 고품질 마크다운(MDX) 리뷰 포스트를 완성하세요:

[필수 Frontmatter 형식]
---
title: "{device_name} 심층 리뷰: 장단점과 실사용 퍼포먼스 총정리"
date: "2026-08-14"
device: "{device_name}"
score: 9.2
category: "스마트폰/IT"
summary: "{device_name}의 핵심 변경사항과 실제 실사용 성능, 그리고 아쉬운 점까지 꼼꼼하게 비교 분석합니다."
pros:
  - "압도적인 전력 효율과 뛰어난 성능"
  - "완성도 높은 디자인과 우수한 디스플레이"
cons:
  - "전작 대비 상승한 가격 부담"
---

# {device_name} 심층 리뷰 및 실사용 가이드

해외 주요 매체와 수집된 사용자 데이터 및 벤치마크 결과를 바탕으로 종합 정리한 **{device_name}** 리뷰입니다.

## ⚡ 3초 한줄 요약
> **"{device_name}는 훌륭한 완성도와 고성능을 제공하며, 추천할 만한 기기입니다."**

---

## 📊 주요 핵심 스펙 명세

| 항목 | 상세 스펙 |
| --- | --- |
| **프로세서** | 최신 차세대 고성능 프로세서 |
| **디스플레이** | 120Hz 가변 주사율 지원 |
| **배터리 / 충전** | 올데이 배터리 타임 지원 |
| **추천 대상** | 성능과 완성도를 최우선으로 생각하는 사용자 |

---

## 🔍 주요 장점 및 세부 분석
### 1. 강력한 벤치마크 성능
### 2. 향상된 디스플레이 & 디자인

---

## ⚠️ 아쉬운 점 및 체크포인트
- **가격 정책**: 이전 세대 대비 가격 인상 부담
- **발열 관리**: 최고 부하 시 체크포인트

---

## 💡 총평 및 구매 가이드
"""

    # 1. Qwen API 호환 (전용 Aliyun MaaS / DashScope 엔드포인트 지원)
    if qwen_key:
        try:
            from openai import OpenAI
            qwen_base_url = os.environ.get(
                "QWEN_BASE_URL", 
                "https://ws-gv65z0e7ds9mibcp.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
            )
            qwen_model = os.environ.get("QWEN_MODEL", "qwen-max")
            
            client = OpenAI(api_key=qwen_key, base_url=qwen_base_url)
            print(f"[AI Synthesizer] Qwen 모델 ({qwen_model}) 호출 중... (엔드포인트: {qwen_base_url})")
            response = client.chat.completions.create(
                model=qwen_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return slug, response.choices[0].message.content
        except Exception as e:
            print(f"[AI Synthesizer] Qwen API 오류: {e}")

    # 2. DeepSeek API 호환 (OpenAI 규격)
    if deepseek_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=deepseek_key, base_url="https://api.deepseek.com")
            print("[AI Synthesizer] DeepSeek V3 모델 사용 중...")
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return slug, response.choices[0].message.content
        except Exception as e:
            print(f"[AI Synthesizer] DeepSeek API 오류: {e}")

    # 3. Gemini API 호환
    if gemini_key:
        try:
            from google import genai
            client = genai.Client(api_key=gemini_key)
            print("[AI Synthesizer] Gemini 2.5 Flash 모델 사용 중...")
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            return slug, response.text
        except Exception as e:
            print(f"[AI Synthesizer] Gemini API 오류: {e}")

    # Fallback template
    mock_mdx = f"""---
title: "{device_name} 심층 리뷰: 장단점과 가성비 총정리"
date: "2026-08-14"
device: "{device_name}"
score: 9.2
category: "스마트폰/IT"
summary: "{device_name}의 핵심 변경사항과 실제 실사용 성능, 그리고 아쉬운 점까지 꼼꼼하게 비교 분석합니다."
pros:
  - "압도적인 전력 효율과 뛰어난 성능"
  - "더욱 가벼워진 무게와 완성도 높은 디자인"
cons:
  - "전작 대비 상승한 가격 부담"
---

# {device_name} 심층 리뷰 및 실사용 가이드

해외 주요 매체와 수집된 사용자 데이터 및 벤치마크 결과를 바탕으로 종합 정리한 **{device_name}** 리뷰입니다.

## ⚡ 3초 한줄 요약

> **"{device_name}는 훌륭한 완성도와 고성능을 제공하며, 성능 중심 유저에게 최고의 선택이 될 수 있습니다."**

---

## 📊 주요 핵심 스펙 명세

| 항목 | 상세 스펙 |
| --- | --- |
| **프로세서** | 최신 차세대 고성능 프로세서 |
| **디스플레이** | 120Hz 가변 주사율 지원 OLED |
| **배터리 / 충전** | 올데이 배터리 타임 지원 |
| **추천 대상** | 성능과 완성도를 최우선으로 생각하는 사용자 |

---

## 🔍 주요 장점 및 세부 분석

### 1. 강력한 벤치마크 성능
실사용 및 고사양 작업에서 끊김 없는 유연한 퍼포먼스를 보여줍니다. 

### 2. 향상된 디스플레이 & 디자인
야외 가독성이 향상되었으며, 그립감과 디테일한 텍스처 마감이 돋보입니다.

---

## ⚠️ 아쉬운 점 및 체크포인트

- **가격 정책**: 이전 세대 대비 가격 인상 부담이 일부 존재합니다.
- **발열 관리**: 지속적인 최고 부하 시 약간의 스로틀링이 관찰될 수 있습니다.

---

## 💡 총평 및 구매 가이드

성능과 디자인 모두를 선점하고자 한다면 **{device_name}**는 충분히 돈값을 하는 기기입니다. 
"""
    return slug, mock_mdx
