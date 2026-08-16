#!/usr/bin/env python3
"""
AI-Powered Native i18n Translation Engine (Gemini / DeepSeek / Qwen)
-------------------------------------------------------------------
한국어 테크 리뷰 원본을 The Verge / Engadget / Gizmodo 수준의
고품질 네이티브 영어(en) 및 일본어(ja) 전문 테크 매거진 기사로 자동 번역 및 생성합니다.
"""

import os
import glob
import re
import json
import argparse
import urllib.request
from typing import Dict, Any, Optional

ENV_PATH = os.path.join(os.path.dirname(__file__), "../.env")

def load_env():
    env_vars = {}
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    env_vars[k.strip()] = v.strip().strip('"').strip("'")
    return env_vars

ENV = load_env()

def get_api_key(key_name: str) -> Optional[str]:
    return os.environ.get(key_name) or ENV.get(key_name)

GEMINI_API_KEY = get_api_key("GEMINI_API_KEY")
DEEPSEEK_API_KEY = get_api_key("DEEPSEEK_API_KEY")
QWEN_API_KEY = get_api_key("QWEN_API_KEY")

TECH_TRANSLATION_PROMPT = {
    "en": """You are an elite senior tech editor at The Verge and Wired.
Translate the following Korean tech review MDX into fluent, engaging, and professional English.

RULES:
1. Preserve all Frontmatter keys exactly (title, date, device, category, score, summary, pros, cons, layout, etc.).
2. Translate Frontmatter values (title, summary, pros, cons) into crisp, natural English tech journalism style.
3. Translate all markdown body sections, retaining markdown tables, bullet points, spec numbers, and benchmarks.
4. Maintain proper English tech terminology:
   - 칩셋/프로세서 -> SoC / Processor / Chipset
   - 급나누기 -> Market segmentation / Tier differentiation
   - 가성비 -> Value for money / Price-to-performance ratio
   - 방열/발열 제어 -> Thermal management / Vapor chamber cooling
   - 주사율 -> Refresh rate (e.g. 120Hz LTPO)
5. Output ONLY the translated valid MDX text without any markdown code wrappers (no ```mdx).
""",
    "ja": """あなたは日本のトップテックメディア（Gizmodo Japan、Engadget日本版）のシニアテックエディターです。
以下の韓国語テックレビューMDXを、自然で専門性の高い日本語に翻訳してください。

ルール:
1. Frontmatterのキー（title, date, device, category, score, summary, pros, cons 등）はそのまま維持してください。
2. Frontmatterの値（タイトル、要約、メリット、デメリット）を自然な日本語に翻訳してください。
3. 本文のマークダウン表、スペック数値、ベンチマーク結果を正確に維持しながら翻訳してください。
4. 正しい日本語テック用語（SoC、リフレッシュレート、コスパ、サーマルスロットリングなど）を使用してください。
5. MDXコードラッパー（```mdxなど）なしで、完成したMDXテキストのみを出力してください。
"""
}

def translate_with_gemini(text: str, target_lang: str) -> Optional[str]:
    if not GEMINI_API_KEY:
        return None
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={GEMINI_API_KEY}"
    prompt = TECH_TRANSLATION_PROMPT.get(target_lang, TECH_TRANSLATION_PROMPT["en"])
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt + "\n\n=== SOURCE KOREAN MDX ===\n" + text}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 8192
        }
    }
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        print(f"⚠️ Gemini Translation API Error: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="AI Multi-Language Tech Review Translator")
    parser.add_argument("--lang", choices=["en", "ja"], default="en", help="Target language (en: English, ja: Japanese)")
    parser.add_argument("--file", help="Specific file to translate (optional)")
    args = parser.parse_args()

    reviews_dir = os.path.join(os.path.dirname(__file__), "../src/content/reviews")
    out_dir = os.path.join(reviews_dir, args.lang)
    os.makedirs(out_dir, exist_ok=True)

    target_files = [args.file] if args.file else glob.glob(os.path.join(reviews_dir, "*.mdx"))

    print(f"🌐 Starting AI High-Quality Tech Translation to [{args.lang.upper()}] (Total: {len(target_files)} files)")

    for src_file in target_files:
        base_name = os.path.basename(src_file)
        dest_file = os.path.join(out_dir, base_name)

        print(f"📄 Processing: {base_name} ...")
        with open(src_file, "r", encoding="utf-8") as f:
            korean_content = f.read()

        translated = translate_with_gemini(korean_content, args.lang)
        if translated:
            with open(dest_file, "w", encoding="utf-8") as f:
                f.write(translated)
            print(f"  ✅ Saved native {args.lang.upper()} review: {dest_file}")
        else:
            print(f"  ⚠️ Skipping (API key needed or rate limit): {base_name}")

if __name__ == "__main__":
    main()
