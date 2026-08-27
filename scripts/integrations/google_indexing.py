import os
import glob
import json
import argparse

def get_google_indexing_client():
    """
    구글 서비스 계정 인증 객체를 생성합니다.
    1순위: GOOGLE_SERVICE_ACCOUNT_KEY 환경 변수 (JSON 문자열)
    2순위: 프로젝트 루트 또는 data/ 폴더 내 서비스 계정 키 파일 (*.json)
    """
    env_key = os.environ.get("GOOGLE_SERVICE_ACCOUNT_KEY")
    credentials = None

    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        print("⚠️ [Google Indexing] google-auth 및 google-api-python-client 모듈이 필요합니다.")
        return None

    # 1. 환경변수 JSON 파싱
    if env_key:
        try:
            key_data = json.loads(env_key.strip())
            credentials = service_account.Credentials.from_service_account_info(
                key_data,
                scopes=['https://www.googleapis.com/auth/indexing']
            )
            print("🔑 [Google Indexing] 환경 변수 'GOOGLE_SERVICE_ACCOUNT_KEY'를 통해 인증을 구성했습니다.")
        except Exception as e:
            print(f"⚠️ [Google Indexing] 환경 변수 JSON 파싱 실패: {e}")

    # 2. 로컬 키 파일 탐색
    if not credentials:
        candidate_patterns = [
            "indexing-*.json",
            "google-service-account*.json",
            "service-account*.json",
            "data/indexing-*.json",
            "data/google-service-account*.json"
        ]
        
        matched_file = None
        for pattern in candidate_patterns:
            matches = glob.glob(pattern)
            if matches:
                matched_file = matches[0]
                break

        if matched_file and os.path.exists(matched_file):
            try:
                credentials = service_account.Credentials.from_service_account_file(
                    matched_file,
                    scopes=['https://www.googleapis.com/auth/indexing']
                )
                print(f"🔑 [Google Indexing] 로컬 키 파일 '{matched_file}'을 로드하여 인증을 구성했습니다.")
            except Exception as e:
                print(f"⚠️ [Google Indexing] 로컬 파일 로드 실패: {e}")

    if not credentials:
        return None

    try:
        service = build('indexing', 'v3', credentials=credentials, cache_discovery=False)
        return service
    except Exception as e:
        print(f"⚠️ [Google Indexing] 서비스 빌드 실패: {e}")
        return None

def request_google_indexing(target_url: str, notification_type: str = "URL_UPDATED") -> bool:
    """
    Google Indexing API를 호출하여 특정 URL의 실시간 색인(Crawling)을 요청합니다.
    """
    if not target_url:
        return False

    client = get_google_indexing_client()
    if not client:
        print(f"ℹ️ [Google Indexing] 서비스 계정 키가 설정되지 않아 색인 요청을 건너뜁니다: {target_url}")
        return False

    try:
        print(f"📡 [Google Indexing] 구글 실시간 색인 요청 전송 중... ({notification_type}) -> {target_url}")
        body = {
            "url": target_url,
            "type": notification_type
        }
        response = client.urlNotifications().publish(body=body).execute()
        status = response.get("urlNotificationMetadata", {})
        print(f"✅ [Google Indexing] 색인 요청 성공! 최신 통지 일시: {status.get('latestUpdate', {}).get('notifyTime', '성공')}")
        return True
    except Exception as e:
        print(f"❌ [Google Indexing] 색인 API 호출 오류: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Google Indexing API 실시간 색인 요청 도구")
    parser.add_argument("--url", type=str, required=True, help="색인을 요청할 전체 URL (예: https://tech.thesinoreport.com/reviews/galaxy-s26-ultra)")
    parser.add_argument("--type", type=str, default="URL_UPDATED", choices=["URL_UPDATED", "URL_DELETED"], help="알림 타입 (기본값: URL_UPDATED)")
    args = parser.parse_args()

    request_google_indexing(args.url, args.type)

if __name__ == "__main__":
    main()
