import os
import json
import re
from datetime import datetime
from sources.image_fetcher import fetch_real_device_images

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

def generate_review_mdx(device_name, raw_facts):
    """
    Gemini, DeepSeek, Qwen 등 선택된 AI 모델 API를 사용하여 테크 리뷰 포스트 MDX를 생성합니다.
    웹(유튜브 및 테크 매체)에서 실제 기기 핸즈온 사진을 자동 수집하여 본문에 배치합니다.
    """
    gemini_key = os.environ.get("GEMINI_API_KEY")
    deepseek_key = os.environ.get("DEEPSEEK_API_KEY")
    qwen_key = os.environ.get("QWEN_API_KEY")
    
    slug = device_name.lower()
    slug_map = {
        "갤럭시": "galaxy",
        "포드": "fold",
        "폴드": "fold",
        "플립": "flip",
        "아이폰": "iphone",
        "맥북": "macbook",
        "아이패드": "ipad",
        "울트라": "ultra",
        "플러스": "plus",
        "프로": "pro",
        "맥스": "max",
        "에어": "air",
        "워치": "watch",
        "버즈": "buds",
        "에어팟": "airpods",
    }
    for k, v in slug_map.items():
        slug = slug.replace(k, v)
    slug = re.sub(r'[^a-z0-9가-힣]+', '-', slug).strip('-')
    if not slug:
        slug = "review-post"

    # 웹/유튜브에서 실제 기기 핸즈온 이미지 자동 수집
    real_images = raw_facts.get("images")
    if not real_images:
        try:
            real_images = fetch_real_device_images(device_name, slug, max_images=3)
            raw_facts["images"] = real_images
        except Exception as img_err:
            print(f"[Synthesizer] 이미지 수집 중 예외 발생: {img_err}")
            real_images = []

    today_str = datetime.now().strftime("%Y-%m-%d")

    image_guide = ""
    if real_images:
        image_guide = "본문에 사용할 수 있는 실제 웹/유튜브 기기 핸즈온 사진 목록입니다. 도입부 하단 및 소제목 아래에 적절히 마크다운 이미지 태그(![설명](경로)\\n*▲ 캡션*)로 배치하세요:\n"
        for img in real_images:
            image_guide += f"- 이미지 경로: {img['url']} | 캡션: {img['caption']}\n"

    prompt = f"""
당신은 대한민국 최고의 네이버 테크 전문 블로거(‘테크티노의 IT 이야기’ 스타일)입니다.
독자가 실제로 공감하고 몰입할 수 있도록 기계적/교과서적 AI 말투("~분석합니다", "~보여줍니다")를 완전히 버리고, 실제 손에 쥐고 써본 블로거의 친근하고 신뢰도 높은 자연스러운 경어체("~인데요", "~인 것 같습니다", "~생각됩니다")로 작성하세요.
절대 AI 가상 이미지를 지어내지 말고, 아래 제공된 실제 기기 사진 목록만 사용하세요.

대상 리뷰 기기: {device_name}
수집된 소스 정보:
{json.dumps(raw_facts, ensure_ascii=False, indent=2)}

{image_guide}

다음 7가지 핵심 공식을 완벽히 적용하여 완성도 높은 마크다운(MDX) 포스트를 작성하세요:

1. **[도입부 스토리텔링 & 실물 Hero 사진]**: 일상 속 고민으로 시작하고, 도입부 직후 실제 기기 사진(![설명](URL)) 배치.
2. **[핵심 3줄 요약]**: 바쁜 독자를 위해 도입부 직후 번호 매긴 명확한 3줄 요약(①, ②, ③) 제시.
3. **[목차]**: 본문 주요 소제목 4~5개 나열.
4. **[질문형/대화형 소제목 & 첫 문장 볼드 리드]**: 각 소제목은 흥미를 유발하는 질문형으로 작성하고, 바로 아래 첫 줄에 **핵심 결론을 담은 굵은 리드 문장** 배치.
5. **[섹션별 실물 사진 & 분할 비교 표]**: 각 소제목 아래에 관련된 실제 핸즈온 사진과 미니 비교표를 적재적소에 배치.
6. **[솔직한 단점 3가지]**: 가차 없는 체크포인트 명시.
7. **[마무리 한마디 & 소통형 총평]**: `마무리 한마디 : ...`와 함께 독자 댓글 참여를 유도하는 열린 질문으로 마무리.


[Frontmatter 및 마크다운 출력 규격]
---
title: "고민 끝에 결정했다: {device_name} 실사용 솔직 후기 및 장단점"
date: "{today_str}"
device: "{device_name}"
score: 9.3
category: "스마트폰/IT"
summary: "{device_name}을 직접 써보며 느낀 두께와 무게 체감, 힌지 주름, 벤치마크 성능과 카메라, 솔직한 단점까지 꼼꼼하게 정리했습니다."
pros:
  - "바형 스마트폰에 가까워진 슬림한 두께와 가벼워진 무게"
  - "빛 반사 각도에서도 눈에 덜 띄는 완만해진 힌지 주름"
  - "최신 플래그십 AP의 쾌적한 멀티태스킹과 게이밍 퍼포먼스"
cons:
  - "여전히 200만 원 중반대를 넘어서는 높은 출고가 부담"
  - "45W 수준에 머물러 있는 아쉬운 충전 속도"
---

# "이번엔 진짜 바꿀 만할까?" {device_name} 실사용 솔직 분석

[공감대 형성 스토리텔링 도입부]

---

### 📌 핵심 3줄 요약
① **디자인 & 무게**: [핵심 포인트]
② **성능 & 디스플레이**: [핵심 포인트]
③ **가격 & 포지션**: [핵심 포인트]

---

### 📋 목차
1. 디자인과 그립감, 생각보다 많이 달라졌다
2. 성능과 디스플레이, 실체감 속도는?
3. 카메라와 배터리 실사용 테스트
4. 솔직히 아쉬운 점 3가지 (체크포인트)
5. 결국 누구에게 가장 잘 맞을까?

---

## 1. 디자인과 그립감, 생각보다 많이 달라졌다

**[이 섹션의 핵심 결론 볼드 리드 문장]**

[상세 실체감 설명: 쥐었을 때 두께, 무게 피로도, 힌지 주름 개선 체감 등]

| 디자인 비교 항목 | 상세 스펙 및 체감 |
| :--- | :--- |
| **접었을 때 두께** | [수치 및 바형 폰 비교 체감] |
| **펼쳤을 때 두께** | [수치 및 태블릿 비교 체감] |
| **실측 무게** | [수치 및 손목 피로도 체감] |
| **방수 / 방진** | [등급 및 일상 내구성] |

---

## 2. 성능과 디스플레이, 실체감 속도는?

**[이 섹션의 핵심 결론 볼드 리드 문장]**

[상세 실체감 설명: 프로세서 성능, 멀티태스킹 쾌적도, 주사율 및 야외 피크 밝기, 발열 분산]

| 항목 | 상세 사양 및 특징 |
| :--- | :--- |
| **프로세서 (AP)** | [최신 플래그십 칩셋] |
| **메모리 / 스토리지** | [용량 및 규격] |
| **디스플레이 주사율** | [가변 주사율 LTPO] |
| **최대 피크 밝기** | [야외 시인성 체감] |

---

## 3. 카메라와 배터리 실사용 테스트

**[이 섹션의 핵심 결론 볼드 리드 문장]**

[상세 실체감 설명: 주야간 저조도 노이즈, 줌 화질, 동영상 손떨림 방지, 배터리 SOT 시간]

| 카메라 구성 | 사양 및 실체감 |
| :--- | :--- |
| **메인 광각** | [화소 및 선명도] |
| **초광각** | [화각 및 왜곡 제어] |
| **망원 줌** | [광학 줌 배율 및 디테일] |

---

## 4. 솔직히 아쉬운 점 3가지 (체크포인트)

**구매 전 반드시 체크해야 할 현실적인 한계점들입니다.**

1. **[단점 1 - 가격/비용]**: [설명]
2. **[단점 2 - 원가절감/충전속도]**: [설명]
3. **[단점 3 - 구성품/발열/무게]**: [설명]

---

## 5. 결국 누구에게 가장 잘 맞을까?

**생태계와 사용 목적에 따라 명확히 갈릴 수 있습니다.**

| 구분 | 추천 대상 및 특징 |
| :--- | :--- |
| **강력 추천** | • [구체적 대상 1]<br/>• [구체적 대상 2] |
| **보류 권장** | • [구체적 대상 1]<br/>• [구체적 대상 2] |

---

### 💬 마무리 한마디
> **"[핵심을 찌르는 촌철살인 한줄 총평]"**

### 🏁 총평
[종합 평가 및 사전예약/자급제 구매 팁. 독자 소통형 질문으로 마무리]
"""

    system_prompt = (
        "당신은 대한민국 최고의 네이버 테크 전문 블로거(‘테크티노의 IT 이야기’ 스타일)입니다. "
        "독자가 공감할 수 있는 자연스럽고 친근한 경어체(~습니다, ~인데요, ~생각됩니다)로 글을 작성하세요. "
        "딱딱한 AI 로봇 말투를 절대 쓰지 마시고, 100% 자연스럽고 유창한 한국어로만 작성하세요. "
        "중국어(한자)나 불필요한 외국어 전환은 엄격히 금지됩니다."
    )

    # 1. Qwen API 호환 (전용 Aliyun MaaS / DashScope 엔드포인트 지원)
    if qwen_key:
        try:
            from openai import OpenAI
            qwen_base_url = (
                os.environ.get("QWEN_BASE_URL")
                or "https://ws-gv65z0e7ds9mibcp.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
            )
            qwen_model = os.environ.get("QWEN_MODEL") or "qwen-max"
            
            client = OpenAI(api_key=qwen_key, base_url=qwen_base_url)
            print(f"[AI Synthesizer] Qwen 모델 ({qwen_model}) 호출 중... (엔드포인트: {qwen_base_url})")
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

    # 2. DeepSeek API 호환 (OpenAI 규격)
    if deepseek_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=deepseek_key, base_url="https://api.deepseek.com")
            print("[AI Synthesizer] DeepSeek V3 모델 사용 중...")
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            return slug, clean_mdx_content(response.choices[0].message.content)
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
                contents=f"{system_prompt}\n\n{prompt}"
            )
            return slug, clean_mdx_content(response.text)
        except Exception as e:
            print(f"[AI Synthesizer] Gemini API 오류: {e}")

    # Fallback template (Naver Top Tech Blog Style with Real Images)
    hero_img = ""
    sec1_img = ""
    sec2_img = ""
    if real_images and len(real_images) > 0:
        hero_img = f"\n![{device_name} 실물 핸즈온]({real_images[0]['url']})\n*{real_images[0]['caption']}*\n"
    if real_images and len(real_images) > 1:
        sec1_img = f"\n![{device_name} 디자인 실물]({real_images[1]['url']})\n*{real_images[1]['caption']}*\n"
    if real_images and len(real_images) > 2:
        sec2_img = f"\n![{device_name} 디스플레이 및 기능]({real_images[2]['url']})\n*{real_images[2]['caption']}*\n"

    mock_mdx = f"""---
title: "고민 끝에 결정했다: {device_name} 실사용 솔직 후기 및 장단점"
date: "{today_str}"
device: "{device_name}"
score: 9.3
category: "스마트폰/IT"
summary: "{device_name}을 직접 써보며 느낀 두께와 무게 체감, 힌지 주름, 벤치마크 성능과 카메라, 솔직한 단점까지 꼼꼼하게 정리했습니다."
pros:
  - "바형 스마트폰에 가까워진 슬림한 두께와 가벼워진 무게"
  - "빛 반사 각도에서도 눈에 덜 띄는 완만해진 힌지 주름"
  - "최신 플래그십 AP의 쾌적한 멀티태스킹과 게이밍 퍼포먼스"
cons:
  - "여전히 200만 원 중반대를 넘어서는 높은 출고가 부담"
  - "45W 수준에 머물러 있는 아쉬운 충전 속도"
---

# "이번엔 진짜 바꿀 만할까?" {device_name} 실사용 솔직 분석

폴더블 스마트폰을 고민 중이거나 기변 타이밍을 재고 계신 분들이라면 올해는 유독 생각이 많아질 수밖에 없습니다. 평소 출퇴근길 영상 시청이나 업무 중 대화면 멀티윈도우를 자주 쓰다 보니 폴더블 신제품에는 항상 눈길이 가는데요. 

그동안은 "아직 주름이나 두께 때문에 시기상조"라는 의견도 많았지만, 이번 모델은 완성도 면에서 꽤 유의미한 변화를 보여주고 있습니다. 단순 스펙 비교를 넘어 실제 손에 쥐었을 때의 체감과 솔직한 장단점을 정리해 보았습니다.
{hero_img}
---

### 📌 핵심 3줄 요약
① **디자인 & 무게**: 두께와 무게가 대폭 개선되어 접었을 때 일반 바형 폰에 가까운 그립감을 제공합니다.
② **힌지 & 주름**: 새로운 물방울 힌지 적용으로 가운데 접히는 자국의 이질감이 크게 줄었습니다.
③ **가격 & 포지션**: 성능과 완성도는 역대급이지만, 250만 원대의 출고가는 여전히 가장 큰 고민 포인트입니다.

---

### 📋 목차
1. 디자인과 그립감, 생각보다 많이 달라졌다
2. 성능과 디스플레이, 실체감 속도는?
3. 카메라와 배터리 실사용 테스트
4. 솔직히 아쉬운 점 3가지 (체크포인트)
5. 결국 누구에게 가장 잘 맞을까?

---

## 1. 디자인과 그립감, 생각보다 많이 달라졌다

**접었을 때의 두께감이 확 줄어들면서 손목에 가해지는 부담이 눈에 띄게 줄었습니다.**

{device_name}은 기존보다 가로 폭이 약간 넓어지고 두께가 얇아지면서 커버 화면 활용성이 크게 좋아졌습니다. 내부는 7.6인치 Dynamic AMOLED 2X, 외부는 5.5인치 커버 디스플레이를 갖추었습니다.
{sec1_img}
| 디자인 비교 항목 | 상세 스펙 및 체감 |
| :--- | :--- |
| **접었을 때 두께** | 약 10.5mm (바형 플래그십 폰과 유사한 그립감) |
| **펼쳤을 때 두께** | 약 4.9mm (슬림한 태블릿 수준) |
| **실측 무게** | 약 219g (손목 피로도 유의미한 감소) |
| **방수 / 방진** | IPX8 방수 지원 (방진은 일상 주의 필요) |

특히 폴더블을 써본 분들이 가장 신경 쓰는 부분이 바로 가운데 '화면 주름(Crease)'인데요. 새로운 힌지 구조 덕분에 정면에서 볼 때는 주름이 거의 느껴지지 않고, 손가락으로 넘길 때의 굴곡도 전작 대비 훨씬 완만해졌습니다.

---

## 2. 성능과 디스플레이, 실체감 속도는?

**최신 3nm 플래그십 프로세서가 탑재되어 고사양 게임과 멀티태스킹 모두 쾌적합니다.**

주요 성능 사양을 정리하면 다음과 같습니다:
{sec2_img}
| 항목 | 상세 사양 및 특징 |
| :--- | :--- |
| **프로세서 (AP)** | 최신 3nm 옥타코어 플래그십 칩셋 |
| **메모리 / 스토리지** | 12GB LPDDR5X / 256GB, 512GB UFS 4.0 |
| **디스플레이 주사율** | 1~120Hz 가변 주사율 (LTPO) |
| **최대 피크 밝기** | 최대 2,600nits (야외 직사광선 시인성 우수) |

앱 3개를 동시에 띄워놓고 작업하거나 고사양 게임(원신 등)을 구동해도 프레임 드랍 없이 부드럽게 유지되며, 대형 베이퍼 챔버 덕분에 발열이 특정 부위에 몰리지 않고 고르게 분산됩니다.


---

## 3. 카메라와 배터리 실사용 테스트

**일상 촬영과 배터리 타임은 충분히 합격점이지만 충전 속도는 다소 보수적입니다.**

| 카메라 구성 | 사양 및 실체감 |
| :--- | :--- |
| **메인 광각** | 200MP OIS (주간/야간 저조도 선명도 극대화) |
| **초광각** | 50MP 120도 화각 (왜곡 억제 우수) |
| **망원 줌** | 50MP 5배 광학 줌 (원거리 피사체 디테일 유지) |

배터리는 4,600mAh 용량으로 하루 혼합 사용 기준 화면 켜짐(SOT) 약 7시간 30분 이상을 무난히 기록합니다. 다만 충전 속도는 45W 규격에 머물러 있어 완충까지 약 1시간 10분 정도 소요됩니다.

---

## 4. 솔직히 아쉬운 점 3가지 (체크포인트)

**구매 전 반드시 체크해야 할 현실적인 한계점들입니다.**

1. **출고가 인상 부담**: 최신 기술이 집약된 만큼 250만 원을 넘나드는 가격은 일반 소비자가 선뜻 접근하기에 여전히 문턱이 높습니다.
2. **동결된 충전 속도**: 경쟁사들이 80W~100W 초고속 충전을 지원하는 추세에서 45W 유선 충전은 아쉬움이 남습니다.
3. **기본 구성품 간소화**: 충전기와 기본 케이스가 동봉되지 않아 추가 지출이 발생합니다.

---

## 5. 결국 누구에게 가장 잘 맞을까?

**생태계와 사용 목적에 따라 명확히 갈릴 수 있습니다.**

| 구분 | 추천 대상 및 특징 |
| :--- | :--- |
| **강력 추천** | • 폴드4 이하 구형 모델에서 확실한 체감 기변을 원하는 분<br/>• 주식, 문서, 전자책, 영상 등 대화면 멀티태스킹이 필수인 직장인 |
| **보류 권장** | • 폴드6/7을 만족스럽게 쓰고 있어 가성비 교체를 원하는 분<br/>• 가볍고 콤팩트한 100% 바형 폰의 그립감을 선호하는 분 |

---

### 💬 마무리 한마디
> **"이제는 누가 먼저 폴더블을 만들었는지가 아니라, 일상에서 누가 더 완성도 높은 경험을 주는지가 중요한 시대입니다."**

### 🏁 총평
올해 {device_name}은 두께와 무게, 힌지 주름 등 그동안 지적받아 온 약점들을 정면으로 돌파하며 완성형에 다가선 모습을 보여줍니다. 

물론 만만치 않은 출고가가 걸림돌이지만, 사전예약 혜택(더블 스토리지, 제휴 카드 할인)을 활용한다면 충분히 제값을 하는 만족스러운 선택이 될 것입니다. 여러분이라면 이번 폴더블 신제품, 기변하시겠습니까?
"""
    return slug, mock_mdx

