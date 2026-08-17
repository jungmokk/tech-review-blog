import os
import re
import urllib.request
import xml.etree.ElementTree as ET
import yaml

def fetch_rss_items(sources_file="data/sources.yaml"):
    """RSS 피드에서 최신 기사 타이틀 및 원문 링크 수집 (외부 종속성 없는 내장 파서 지원)"""
    if not os.path.exists(sources_file):
        return []

    try:
        with open(sources_file, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"[RSS] sources.yaml 읽기 오류: {e}")
        return []

    items = []
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}

    for source in config.get("rss_sources", []):
        name = source.get("name")
        url = source.get("url")
        print(f"[RSS] 수집 중: {name} ({url})")
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as resp:
                xml_data = resp.read()
                root = ET.fromstring(xml_data)

                # RSS 2.0 (channel -> item)
                for item in root.findall(".//item")[:5]:
                    title_elem = item.find("title")
                    link_elem = item.find("link")
                    desc_elem = item.find("description")
                    title = title_elem.text if title_elem is not None and title_elem.text else ""
                    link = link_elem.text if link_elem is not None and link_elem.text else ""
                    desc = desc_elem.text if desc_elem is not None and desc_elem.text else ""
                    clean_desc = re.sub("<.*?>", "", desc)[:300]
                    if title:
                        items.append({
                            "source": name,
                            "title": title.strip(),
                            "link": link.strip(),
                            "summary": clean_desc.strip()
                        })
        except Exception as err:
            print(f"[RSS] {name} 수집 중 오류: {err}")

    return items
