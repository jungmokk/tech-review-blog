import feedparser
import yaml
import re

def fetch_rss_items(sources_file="data/sources.yaml"):
    """RSS 피드에서 최신 기사 타이틀 및 원문 링크 수집"""
    try:
        with open(sources_file, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"[RSS] sources.yaml 읽기 오류: {e}")
        return []

    items = []
    for source in config.get("rss_sources", []):
        name = source.get("name")
        url = source.get("url")
        print(f"[RSS] 수집 중: {name} ({url})")
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:  # 상위 5개 수집
                items.append({
                    "source": name,
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "summary": re.sub("<.*?>", "", entry.get("summary", ""))[:300]
                })
        except Exception as err:
            print(f"[RSS] {name} 수집 중 오류: {err}")

    return items
