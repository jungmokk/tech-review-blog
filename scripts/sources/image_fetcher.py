import os
import re
import requests
import yt_dlp

def fetch_real_device_images(device_name: str, slug: str, max_images: int = 3) -> list[dict]:
    """
    웹(유튜브 공식/인기 테크 리뷰 등)에서 실제 기기 핸즈온 이미지(고화질 썸네일)를 수집하여 
    public/images/reviews/ 에 저장하고 마크다운에 삽입할 이미지 목록을 반환합니다.
    """
    output_dir = "public/images/reviews"
    os.makedirs(output_dir, exist_ok=True)

    search_queries = [
        f"ytsearch5:{device_name} 잇섭",
        f"ytsearch5:{device_name} review",
        f"ytsearch5:{device_name} 실사용",
    ]

    ydl_opts = {
        "quiet": True,
        "extract_flat": "in_playlist",
    }

    found_videos = []
    seen_ids = set()

    for query in search_queries:
        if len(found_videos) >= max_images:
            break
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                res = ydl.extract_info(query, download=False)
                for entry in res.get("entries", []):
                    vid = entry.get("id")
                    title = entry.get("title", "")
                    if vid and vid not in seen_ids:
                        seen_ids.add(vid)
                        found_videos.append({
                            "id": vid,
                            "title": title
                        })
                        if len(found_videos) >= max_images:
                            break
        except Exception as e:
            print(f"[ImageFetcher] 검색 중 오류 ({query}): {e}")

    images = []
    for i, video in enumerate(found_videos):
        vid = video["id"]
        title = video["title"]
        saved = False

        for quality in ["maxresdefault.jpg", "hqdefault.jpg", "sddefault.jpg"]:
            url = f"https://i.ytimg.com/vi/{vid}/{quality}"
            try:
                resp = requests.get(url, timeout=10)
                if resp.status_code == 200 and len(resp.content) > 5000:
                    local_filename = f"{slug}-real-{i+1}.jpg"
                    local_path = os.path.join(output_dir, local_filename)
                    with open(local_path, "wb") as f:
                        f.write(resp.content)
                    
                    web_path = f"/images/reviews/{local_filename}"
                    clean_title = re.sub(r'[\r\n\t]', ' ', title).strip()
                    images.append({
                        "url": web_path,
                        "caption": f"▲ {clean_title} (실제 리뷰 실물 사진)",
                        "video_id": vid,
                        "title": clean_title
                    })
                    print(f"[ImageFetcher] 실제 기기 이미지 수집 완료: {web_path} ({clean_title[:30]}...)")
                    saved = True
                    break
            except Exception as err:
                print(f"[ImageFetcher] 다운로드 실패 ({url}): {err}")
        
        if not saved:
            # Fallback direct link
            web_path = f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
            images.append({
                "url": web_path,
                "caption": f"▲ {title} (실제 리뷰 영상)",
                "video_id": vid,
                "title": title
            })

    return images
