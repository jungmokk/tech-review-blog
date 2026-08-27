import glob
import os

def get_priority_score(dev: dict) -> int:
    """
    기기별 우선순위 가중치 계산 함수:
    1. 출시 연도 (2026년 최우선 > 2025년 > 2024년)
    2. 폼팩터/카테고리 (Foldable, Flagship > High-End, Gaming > Mid-Range)
    3. 수요 및 브랜드 (샤오미, 비보, 화웨이, 오포, 원플러스, 아너, 삼성, 애플 등)
    """
    year = dev.get('release_year', 2024)
    cat = dev.get('category', '')
    brand = dev.get('brand_kr') or dev.get('brand', '')
    
    score = 0
    # Year weight
    if year >= 2026:
        score += 1000
    elif year == 2025:
        score += 700
    elif year == 2024:
        score += 400
    else:
        score += 100
    
    # Category weight
    if cat in ['Foldable', 'Flagship']:
        score += 300
    elif cat in ['High-End', 'Gaming']:
        score += 200
    elif cat in ['Mid-Range', '태블릿']:
        score += 100
        
    # Brand / ZOL Chinese Tech & Global Flagship Priority
    if brand in ['샤오미', '비보', '화웨이', '오포', '원플러스', '아너']:
        score += 150
    elif brand in ['삼성', '애플']:
        score += 120
    elif brand in ['구글', '소니', '낫싱', '에이수스']:
        score += 90
        
    return score

def get_next_priority_device(devices_db: list, published_ids: list) -> dict:
    """
    미발행 기기 중 가중치 점수가 가장 높은 1개 기기를 반환합니다.
    """
    # src/content/reviews 폴더 파일 직접 스캔하여 2중 중복 방지
    review_files = glob.glob("src/content/reviews/*.mdx")
    disk_published = set([os.path.basename(f).replace('.mdx', '') for f in review_files])
    all_published = set(published_ids) | disk_published

    unpublished = [d for d in devices_db if d.get('id') not in all_published]
    if not unpublished:
        return None

    sorted_queue = sorted(unpublished, key=get_priority_score, reverse=True)
    return sorted_queue[0]

def get_full_priority_queue(devices_db: list, published_ids: list) -> list:
    """
    미발행 전체 큐를 우선순위 순으로 정렬하여 반환합니다.
    """
    review_files = glob.glob("src/content/reviews/*.mdx")
    disk_published = set([os.path.basename(f).replace('.mdx', '') for f in review_files])
    all_published = set(published_ids) | disk_published

    unpublished = [d for d in devices_db if d.get('id') not in all_published]
    return sorted(unpublished, key=get_priority_score, reverse=True)
