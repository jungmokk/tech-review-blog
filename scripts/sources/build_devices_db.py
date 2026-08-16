import json
import os

# 기존 스마트폰 리스트 로드 (스마트폰만 필터링)
with open("src/data/smartphones.json", "r", encoding="utf-8") as f:
    raw_list = json.load(f)

smartphones = []
for item in raw_list:
    if item.get("device_type") == "태블릿":
        continue
    item["device_type"] = "스마트폰"
    smartphones.append(item)

# 2023 ~ 2026년 8월 현재까지 주요 프리미엄 및 가성비 태블릿 데이터베이스
tablets = [
    # ==========================================
    # Apple iPad 라인업 (2023~2026)
    # ==========================================
    {
        "id": "ipad-pro-13-m4",
        "name": "iPad Pro 13 (M4)",
        "name_kr": "아이패드 프로 13인치 7세대 (M4)",
        "brand": "Apple",
        "brand_kr": "애플",
        "device_type": "태블릿",
        "release_year": 2024,
        "release_date": "2024-05",
        "category": "Pro Tablet",
        "specs": {
            "ap": "Apple M4 칩셋 (TSMC 2세대 3nm / 38TOPS NPU)",
            "display": "13.0인치 Ultra Retina XDR 탠덤 OLED (2752x2064, 10~120Hz ProMotion, 1600nits 피크, 나노텍스처 옵션)",
            "ram_storage": "8GB / 16GB RAM + 256GB / 512GB / 1TB / 2TB",
            "camera": "1200만 화소 메인 + LiDAR 스캐너 / 전면 가로형 1200만 센터스테이지",
            "battery": "38.99Wh (약 10,290mAh 상당, 10시간 웹서핑)",
            "dimensions_weight": "281.6 x 215.5 x 5.1mm / 579g (역대 애플 기기 중 최박형)",
            "os_durability": "iPadOS 18 (Apple Intelligence) / 애플펜슬 프로 & 신형 매직키보드 지원",
            "price_krw": "1,999,000원부터"
        }
    },
    {
        "id": "ipad-pro-11-m4",
        "name": "iPad Pro 11 (M4)",
        "name_kr": "아이패드 프로 11인치 5세대 (M4)",
        "brand": "Apple",
        "brand_kr": "애플",
        "device_type": "태블릿",
        "release_year": 2024,
        "release_date": "2024-05",
        "category": "Pro Tablet",
        "specs": {
            "ap": "Apple M4 칩셋 (TSMC 2세대 3nm)",
            "display": "11.1인치 Ultra Retina XDR 탠덤 OLED (2420x1668, 10~120Hz ProMotion, 1600nits 피크)",
            "ram_storage": "8GB / 16GB RAM + 256GB / 512GB / 1TB / 2TB",
            "camera": "1200만 메인 + LiDAR 스캐너 / 전면 가로형 1200만",
            "battery": "31.29Wh (약 8,160mAh 상당)",
            "dimensions_weight": "249.7 x 177.5 x 5.3mm / 444g",
            "os_durability": "iPadOS 18 / 애플펜슬 프로 지원",
            "price_krw": "1,499,000원부터"
        }
    },
    {
        "id": "ipad-air-13-m2",
        "name": "iPad Air 13 (M2)",
        "name_kr": "아이패드 에어 13인치 (M2)",
        "brand": "Apple",
        "brand_kr": "애플",
        "device_type": "태블릿",
        "release_year": 2024,
        "release_date": "2024-05",
        "category": "High-End Tablet",
        "specs": {
            "ap": "Apple M2 칩셋 (8코어 CPU / 9코어 GPU / 16코어 Neural Engine)",
            "display": "12.9인치 Liquid Retina IPS LCD (2732x2048, 60Hz, 600nits, P3 색영역)",
            "ram_storage": "8GB RAM + 128GB / 256GB / 512GB / 1TB",
            "camera": "1200만 후면 와이드 / 1200만 가로형 전면 센터스테이지",
            "battery": "36.59Wh (약 9,650mAh 상당)",
            "dimensions_weight": "280.6 x 214.9 x 6.1mm / 617g",
            "os_durability": "iPadOS 18 / 애플펜슬 프로 및 USB-C 지원",
            "price_krw": "1,199,000원부터"
        }
    },
    {
        "id": "ipad-air-11-m2",
        "name": "iPad Air 11 (M2)",
        "name_kr": "아이패드 에어 11인치 6세대 (M2)",
        "brand": "Apple",
        "brand_kr": "애플",
        "device_type": "태블릿",
        "release_year": 2024,
        "release_date": "2024-05",
        "category": "High-End Tablet",
        "specs": {
            "ap": "Apple M2 칩셋 (8코어 CPU / 9코어 GPU)",
            "display": "10.86인치 Liquid Retina IPS LCD (2360x1640, 60Hz, 500nits, P3)",
            "ram_storage": "8GB RAM + 128GB / 256GB / 512GB / 1TB",
            "camera": "1200만 후면 와이드 / 1200만 가로형 전면",
            "battery": "28.93Wh (약 7,600mAh 상당)",
            "dimensions_weight": "247.6 x 178.5 x 6.1mm / 462g",
            "os_durability": "iPadOS 18 / 애플펜슬 프로 지원",
            "price_krw": "899,000원부터"
        }
    },
    {
        "id": "ipad-mini-7",
        "name": "iPad mini 7",
        "name_kr": "아이패드 미니 7세대 (A17 Pro)",
        "brand": "Apple",
        "brand_kr": "애플",
        "device_type": "태블릿",
        "release_year": 2024,
        "release_date": "2024-10",
        "category": "Compact Tablet",
        "specs": {
            "ap": "Apple A17 Pro (3nm / 하드웨어 가속 레이트레이싱)",
            "display": "8.3인치 Liquid Retina IPS LCD (2266x1488, 60Hz, 500nits, 젤리스크롤 완화)",
            "ram_storage": "8GB RAM + 128GB / 256GB / 512GB",
            "camera": "1200만 후면 와이드(스마트 HDR 4) + 1200만 전면 초광각",
            "battery": "19.3Wh (약 5,078mAh 상당, 20W 유선)",
            "dimensions_weight": "195.4 x 134.8 x 6.3mm / 293g (궁극의 휴대용 태블릿)",
            "os_durability": "iPadOS 18 (Apple Intelligence 지원) / 애플펜슬 프로 지원",
            "price_krw": "749,000원부터"
        }
    },
    {
        "id": "ipad-pro-12-9-m2",
        "name": "iPad Pro 12.9 (M2)",
        "name_kr": "아이패드 프로 12.9인치 6세대 (M2)",
        "brand": "Apple",
        "brand_kr": "애플",
        "device_type": "태블릿",
        "release_year": 2023,
        "release_date": "2023-01",
        "category": "Pro Tablet",
        "specs": {
            "ap": "Apple M2 칩셋 (8코어 CPU / 10코어 GPU)",
            "display": "12.9인치 Liquid Retina XDR Mini-LED (2732x2048, 120Hz ProMotion, 1600nits HDR)",
            "ram_storage": "8GB / 16GB RAM + 128GB / 256GB / 512GB / 1TB / 2TB",
            "camera": "1200만 광각 + 1000만 초광각 + LiDAR / 전면 1200만",
            "battery": "40.88Wh (약 10,758mAh)",
            "dimensions_weight": "280.6 x 214.9 x 6.4mm / 682g",
            "os_durability": "iPadOS 16 -> 18 지원 / 애플펜슬 2세대 호버 기능",
            "price_krw": "1,729,000원부터"
        }
    },

    # ==========================================
    # Samsung Galaxy Tab 라인업 (2023~2026)
    # ==========================================
    {
        "id": "galaxy-tab-s10-ultra",
        "name": "Galaxy Tab S10 Ultra",
        "name_kr": "갤럭시 탭 S10 울트라",
        "brand": "Samsung",
        "brand_kr": "삼성",
        "device_type": "태블릿",
        "release_year": 2024,
        "release_date": "2024-10",
        "category": "Pro Tablet",
        "specs": {
            "ap": "MediaTek Dimensity 9300+ (4nm / All-Big-Core 설계)",
            "display": "14.6인치 Dynamic AMOLED 2X (2960x1848, 120Hz, 반사방지 AR 코팅 탑재, 930nits)",
            "ram_storage": "12GB / 16GB RAM + 256GB / 512GB / 1TB + MicroSD 확장(최대 1.5TB)",
            "camera": "1300만 메인 + 800만 초광각 / 전면 1200만 듀얼 와이드",
            "battery": "11,200mAh (45W 초고속 충전 2.0)",
            "dimensions_weight": "326.4 x 208.6 x 5.4mm / 718g (초대화면 슬림)",
            "os_durability": "Android 14 (Galaxy AI 태블릿 최적화) / IP68 방수방진 / 아머 알루미늄",
            "price_krw": "1,598,300원부터"
        }
    },
    {
        "id": "galaxy-tab-s10-plus",
        "name": "Galaxy Tab S10+",
        "name_kr": "갤럭시 탭 S10 플러스",
        "brand": "Samsung",
        "brand_kr": "삼성",
        "device_type": "태블릿",
        "release_year": 2024,
        "release_date": "2024-10",
        "category": "Pro Tablet",
        "specs": {
            "ap": "MediaTek Dimensity 9300+ (4nm)",
            "display": "12.4인치 Dynamic AMOLED 2X (2800x1752, 120Hz, 저반사 코팅, 650nits)",
            "ram_storage": "12GB RAM + 256GB / 512GB + MicroSD 확장",
            "camera": "1300만 메인 + 800만 초광각 / 전면 1200만 초광각",
            "battery": "10,090mAh (45W 초고속 충전 2.0)",
            "dimensions_weight": "285.4 x 185.4 x 5.6mm / 571g",
            "os_durability": "Android 14 (One UI 6.1.1, Galaxy AI) / IP68 / 향상된 아머 알루미늄",
            "price_krw": "1,248,500원부터"
        }
    },
    {
        "id": "galaxy-tab-s9-ultra",
        "name": "Galaxy Tab S9 Ultra",
        "name_kr": "갤럭시 탭 S9 울트라",
        "brand": "Samsung",
        "brand_kr": "삼성",
        "device_type": "태블릿",
        "release_year": 2023,
        "release_date": "2023-07",
        "category": "Pro Tablet",
        "specs": {
            "ap": "Snapdragon 8 Gen 2 for Galaxy (4nm)",
            "display": "14.6인치 Dynamic AMOLED 2X (2960x1848, 120Hz, 930nits)",
            "ram_storage": "12GB / 16GB RAM + 256GB / 512GB / 1TB + MicroSD",
            "camera": "1300만 메인 + 800만 초광각 / 전면 1200만 듀얼",
            "battery": "11,200mAh (45W 고속 충전)",
            "dimensions_weight": "326.4 x 208.6 x 5.5mm / 732g",
            "os_durability": "Android 13 -> 14 지원 / 갤탭 최초 IP68 방수방진 도입 / S펜 기본 동봉",
            "price_krw": "1,598,300원부터"
        }
    },
    {
        "id": "galaxy-tab-s9",
        "name": "Galaxy Tab S9",
        "name_kr": "갤럭시 탭 S9 기본형",
        "brand": "Samsung",
        "brand_kr": "삼성",
        "device_type": "태블릿",
        "release_year": 2023,
        "release_date": "2023-07",
        "category": "High-End Tablet",
        "specs": {
            "ap": "Snapdragon 8 Gen 2 for Galaxy (4nm)",
            "display": "11.0인치 Dynamic AMOLED 2X (2560x1600, 120Hz, OLED 최초 기본형 탑재)",
            "ram_storage": "8GB / 12GB RAM + 128GB / 256GB + MicroSD",
            "camera": "1300만 후면 / 1200만 전면 초광각",
            "battery": "8,400mAh (45W 고속 충전)",
            "dimensions_weight": "254.3 x 165.8 x 5.9mm / 498g",
            "os_durability": "Android 13 / IP68 방수방진 / 아머 알루미늄",
            "price_krw": "998,800원부터"
        }
    },
    {
        "id": "galaxy-tab-s9-fe-plus",
        "name": "Galaxy Tab S9 FE+",
        "name_kr": "갤럭시 탭 S9 FE 플러스",
        "brand": "Samsung",
        "brand_kr": "삼성",
        "device_type": "태블릿",
        "release_year": 2023,
        "release_date": "2023-10",
        "category": "Mid-Range Tablet",
        "specs": {
            "ap": "Exynos 1380 (5nm)",
            "display": "12.4인치 LCD (2560x1600, 90Hz, 비전 부스터)",
            "ram_storage": "8GB / 12GB RAM + 128GB / 256GB + MicroSD",
            "camera": "800만 듀얼 후면 / 1200만 전면 초광각",
            "battery": "10,090mAh (45W 충전)",
            "dimensions_weight": "285.4 x 185.4 x 6.5mm / 627g",
            "os_durability": "Android 13 / IP68 방수방진 (FE 시리즈 최초 방수 지원) / S펜 포함",
            "price_krw": "799,700원부터"
        }
    },
    {
        "id": "galaxy-tab-a9-plus",
        "name": "Galaxy Tab A9+",
        "name_kr": "갤럭시 탭 A9 플러스",
        "brand": "Samsung",
        "brand_kr": "삼성",
        "device_type": "태블릿",
        "release_year": 2023,
        "release_date": "2023-11",
        "category": "Budget Tablet",
        "specs": {
            "ap": "Snapdragon 695 5G (6nm)",
            "display": "11.0인치 TFT LCD (1920x1200, 90Hz 주사율, 16:10 비율)",
            "ram_storage": "4GB / 8GB RAM + 64GB / 128GB + MicroSD",
            "camera": "800만 후면 AF / 500만 전면",
            "battery": "7,040mAh (15W 충전)",
            "dimensions_weight": "257.1 x 168.7 x 6.9mm / 480g / 쿼드 스피커(Dolby Atmos)",
            "os_durability": "Android 13 (Samsung DeX 화면 분할 지원)",
            "price_krw": "368,500원부터"
        }
    },

    # ==========================================
    # Xiaomi & Vivo & OnePlus & Lenovo & Huawei 태블릿
    # ==========================================
    {
        "id": "xiaomi-pad-7-pro",
        "name": "Xiaomi Pad 7 Pro",
        "name_kr": "샤오미 패드 7 프로",
        "brand": "Xiaomi",
        "brand_kr": "샤오미",
        "device_type": "태블릿",
        "release_year": 2025,
        "release_date": "2025-01",
        "category": "High-End Tablet",
        "specs": {
            "ap": "Snapdragon 8s Gen 3 (4nm 플래그십 코어)",
            "display": "11.2인치 3.2K LCD (3200x2136, 144Hz, 3:2 생산성 비율, 800nits, 나노 매트 옵션)",
            "ram_storage": "8GB / 12GB LPDDR5X + 128GB / 256GB / 512GB UFS 4.0",
            "camera": "5000만 메인 후면 / 3200만 전면 AON 인물 센서",
            "battery": "8,850mAh (67W 고속 충전)",
            "dimensions_weight": "251.2 x 173.4 x 6.18mm / 500g (풀 메탈 일체형 유니바디)",
            "os_durability": "Xiaomi HyperOS 2 (PC급 멀티윈도우 워크스테이션 지원)",
            "price_krw": "약 49만 원부터"
        }
    },
    {
        "id": "xiaomi-pad-6s-pro",
        "name": "Xiaomi Pad 6S Pro 12.4",
        "name_kr": "샤오미 패드 6S 프로 12.4",
        "brand": "Xiaomi",
        "brand_kr": "샤오미",
        "device_type": "태블릿",
        "release_year": 2024,
        "release_date": "2024-02",
        "category": "Pro Tablet",
        "specs": {
            "ap": "Snapdragon 8 Gen 2 (4nm)",
            "display": "12.4인치 3K IPS LCD (3048x2032, 144Hz, 3:2 비율, 900nits 피크)",
            "ram_storage": "8GB / 12GB / 16GB RAM + 256GB / 512GB / 1TB",
            "camera": "5000만 메인 + 200만 심도 / 3200만 전면",
            "battery": "10,000mAh (120W 하이퍼차지, 35분 완충)",
            "dimensions_weight": "278.7 x 191.6 x 6.26mm / 590g (6개 쿼드 스피커)",
            "os_durability": "Xiaomi HyperOS / Wi-Fi 7 지원",
            "price_krw": "약 65만 원부터"
        }
    },
    {
        "id": "vivo-pad-3-pro",
        "name": "Vivo Pad 3 Pro",
        "name_kr": "비보 패드 3 프로",
        "brand": "Vivo",
        "brand_kr": "비보",
        "device_type": "태블릿",
        "release_year": 2024,
        "release_date": "2024-03",
        "category": "Pro Tablet",
        "specs": {
            "ap": "MediaTek Dimensity 9300 (4nm 플래그십)",
            "display": "13.0인치 3.1K LCD (3096x2064, 144Hz, 3:2 비율, 900nits HDR)",
            "ram_storage": "8GB / 12GB / 16GB LPDDR5X + 128GB / 256GB / 512GB UFS 4.0",
            "camera": "1300만 후면 / 800만 전면",
            "battery": "11,500mAh 대용량 (66W 고속 플래시차지)",
            "dimensions_weight": "289.6 x 198.3 x 6.64mm / 678g (8스피커 사운드 시스템)",
            "os_durability": "OriginOS 4 for Pad / 블루엘엠 AI 생산성 도구",
            "price_krw": "약 58만 원부터"
        }
    },
    {
        "id": "oneplus-pad-2",
        "name": "OnePlus Pad 2",
        "name_kr": "원플러스 패드 2",
        "brand": "OnePlus",
        "brand_kr": "원플러스",
        "device_type": "태블릿",
        "release_year": 2024,
        "release_date": "2024-07",
        "category": "High-End Tablet",
        "specs": {
            "ap": "Snapdragon 8 Gen 3 (4nm)",
            "display": "12.1인치 3K ReadFit IPS LCD (3000x2120, 144Hz, 7:5 비율, 900nits)",
            "ram_storage": "12GB RAM + 256GB UFS 3.1",
            "camera": "1300만 후면 / 800만 전면",
            "battery": "9,510mAh (67W SUPERVOOC 유선 충전)",
            "dimensions_weight": "268.7 x 195.1 x 6.49mm / 584g / 6스피커 옴니베어링",
            "os_durability": "OxygenOS 14.1 (Open Canvas 태블릿 멀티태스킹 최강)",
            "price_krw": "약 69만 원부터"
        }
    },
    {
        "id": "lenovo-legion-y700-2024",
        "name": "Lenovo Legion Y700 2024 (3세대)",
        "name_kr": "레노버 리전 Y700 3세대 (2024)",
        "brand": "Lenovo",
        "brand_kr": "레노버",
        "device_type": "태블릿",
        "release_year": 2024,
        "release_date": "2024-09",
        "category": "Gaming Tablet",
        "specs": {
            "ap": "Snapdragon 8 Gen 3 (4nm) + 대형 베이퍼 챔버",
            "display": "8.8인치 2.5K IPS LCD (2560x1600, 165Hz 초고주사율, 500nits, DCI-P3)",
            "ram_storage": "12GB / 16GB LPDDR5X + 256GB / 512GB UFS 4.0",
            "camera": "1300만 후면 + 200만 매크로 / 800만 전면",
            "battery": "6,550mAh (68W 초고속 충전, 바이패스 충전 지원)",
            "dimensions_weight": "208.5 x 129.5 x 7.6mm / 350g (듀얼 USB-C 포트 탑재)",
            "os_durability": "ZUI 16 (Android 14) / 듀얼 X축 리니어 진동 모터 / 최고의 8인치 안드로이드 게이밍 태블릿",
            "price_krw": "약 49만 원부터"
        }
    },
    {
        "id": "lenovo-legion-y700-2023",
        "name": "Lenovo Legion Y700 2023 (2세대)",
        "name_kr": "레노버 리전 Y700 2세대 (2023)",
        "brand": "Lenovo",
        "brand_kr": "레노버",
        "device_type": "태블릿",
        "release_year": 2023,
        "release_date": "2023-07",
        "category": "Gaming Tablet",
        "specs": {
            "ap": "Snapdragon 8+ Gen 1 (4nm)",
            "display": "8.8인치 2.5K LCD (2560x1600, 144Hz, 500nits)",
            "ram_storage": "12GB / 16GB LPDDR5 + 256GB / 512GB + MicroSD 지원",
            "camera": "1300만 메인 + 200만 접사 / 800만 전면",
            "battery": "6,550mAh (45W 고속 충전, 바이패스 충전)",
            "dimensions_weight": "208.9 x 129.5 x 7.6mm / 348g (듀얼 Type-C 포트)",
            "os_durability": "ZUI 15 / 가성비 최고의 8.8인치 컴팩트 태블릿",
            "price_krw": "약 36만 원부터"
        }
    },
    # ==========================================
    # OPPO Pad 라인업 (2023~2026)
    # ==========================================
    {
        "id": "oppo-pad-3-pro",
        "name": "OPPO Pad 3 Pro",
        "name_kr": "오포 패드 3 프로",
        "brand": "Oppo",
        "brand_kr": "오포",
        "device_type": "태블릿",
        "release_year": 2024,
        "release_date": "2024-10",
        "category": "Pro Tablet",
        "specs": {
            "ap": "Snapdragon 8 Gen 3 Leading Edition (3.4GHz)",
            "display": "12.1인치 3K ReadFit LCD (3000x2120, 144Hz, 7:5 황금비율, 900nits 피크)",
            "ram_storage": "8GB / 12GB / 16GB LPDDR5X + 256GB / 512GB / 1TB UFS 4.0",
            "camera": "1300만 메인 후면 / 800만 전면",
            "battery": "9,510mAh (67W SUPERVOOC 유선 고속 충전)",
            "dimensions_weight": "268.66 x 195.06 x 6.49mm / 586g (풀 메탈 일체형)",
            "os_durability": "ColorOS 14.1 for Pad / 6개 옴니베어링 스피커(Hi-Res 인증)",
            "price_krw": "약 65만~79만 원"
        }
    },
    {
        "id": "oppo-pad-3",
        "name": "OPPO Pad 3",
        "name_kr": "오포 패드 3",
        "brand": "Oppo",
        "brand_kr": "오포",
        "device_type": "태블릿",
        "release_year": 2024,
        "release_date": "2024-11",
        "category": "High-End Tablet",
        "specs": {
            "ap": "MediaTek Dimensity 8350 (4nm)",
            "display": "11.6인치 2.8K LCD (2800x2000, 144Hz, 7:5 비율, 700nits, 저반사 매트 옵션)",
            "ram_storage": "8GB / 12GB LPDDR5X + 128GB / 256GB / 512GB UFS 3.1",
            "camera": "800만 후면 / 800만 전면",
            "battery": "9,510mAh (67W 고속 충전)",
            "dimensions_weight": "258.03 x 189.39 x 6.29mm / 533g",
            "os_durability": "ColorOS 15 for Pad / 파노라마 사운드 쿼드 스피커",
            "price_krw": "약 45만~55만 원"
        }
    },
    {
        "id": "oppo-pad-2",
        "name": "OPPO Pad 2",
        "name_kr": "오포 패드 2",
        "brand": "Oppo",
        "brand_kr": "오포",
        "device_type": "태블릿",
        "release_year": 2023,
        "release_date": "2023-03",
        "category": "High-End Tablet",
        "specs": {
            "ap": "MediaTek Dimensity 9000 (4nm)",
            "display": "11.61인치 2.8K IPS LCD (2800x2000, 144Hz, 7:5 황금비율, 500nits)",
            "ram_storage": "8GB / 12GB LPDDR5 + 256GB / 512GB UFS 3.1",
            "camera": "1300만 후면(중앙 원형 모듈) + 800만 전면",
            "battery": "9,510mAh (67W SUPERVOOC 충전)",
            "dimensions_weight": "258.03 x 189.39 x 6.54mm / 552g (성운 은하수 패턴 백)",
            "os_durability": "ColorOS 13.1 for Pad / 돌비 비전 & 돌비 애트모스",
            "price_krw": "약 58만 원부터"
        }
    },
    {
        "id": "oppo-pad-neo",
        "name": "OPPO Pad Neo (Air 2)",
        "name_kr": "오포 패드 네오 / 에어2 (LTE)",
        "brand": "Oppo",
        "brand_kr": "오포",
        "device_type": "태블릿",
        "release_year": 2024,
        "release_date": "2024-01",
        "category": "Budget/Mid-Range Tablet",
        "specs": {
            "ap": "MediaTek Helio G99 (6nm)",
            "display": "11.4인치 2.4K ReadFit LCD (2408x1720, 90Hz, 7:5 비율, 400nits, 저블루라이트)",
            "ram_storage": "6GB / 8GB LPDDR4X + 128GB UFS 2.2 + MicroSD",
            "camera": "800만 후면 / 800만 전면",
            "battery": "8,000mAh (33W 고속 충전)",
            "dimensions_weight": "255.12 x 188.04 x 6.89mm / 538g (투톤 매트 메탈 디자인)",
            "os_durability": "ColorOS 13.2 / 4개 돌비 애트모스 스피커 / 4G LTE 데이터 지원 모델",
            "price_krw": "약 28만~34만 원"
        }
    },
    # ==========================================
    # 가성비 태블릿 명작 (샤오신패드, 뮤패드, 올도큐브, 레드미/포코 등)
    # ==========================================
    {
        "id": "lenovo-xiaoxin-pad-pro-12-7-2025",
        "name": "Lenovo Xiaoxin Pad Pro 12.7 (2025)",
        "name_kr": "레노버 샤오신패드 프로 12.7 2025",
        "brand": "Lenovo",
        "brand_kr": "레노버",
        "device_type": "태블릿",
        "release_year": 2024,
        "release_date": "2024-07",
        "category": "Budget/Mid-Range Tablet",
        "specs": {
            "ap": "MediaTek Dimensity 8300 (4nm 고성능 AP)",
            "display": "12.7인치 2.9K LCD (2944x1840, 144Hz, 400nits, DCI-P3, 나노 매트 소프트 에디션 옵션)",
            "ram_storage": "8GB / 12GB LPDDR5X + 128GB / 256GB UFS 4.0 + MicroSD 지원(최대 1TB)",
            "camera": "1300만 메인 후면 / 800만 전면",
            "battery": "10,200mAh (45W 고속 충전 지원)",
            "dimensions_weight": "291.8 x 189.2 x 6.9mm / 615g (메탈 유니바디)",
            "os_durability": "ZUI 16 (Android 14) / 4개 JBL 스피커(Dolby Atmos)",
            "price_krw": "약 26만~32만 원 (가성비 종결자)"
        }
    },
    {
        "id": "lenovo-xiaoxin-pad-pro-12-7-2023",
        "name": "Lenovo Xiaoxin Pad Pro 12.7 (2023)",
        "name_kr": "레노버 샤오신패드 프로 12.7 2023",
        "brand": "Lenovo",
        "brand_kr": "레노버",
        "device_type": "태블릿",
        "release_year": 2023,
        "release_date": "2023-08",
        "category": "Budget/Mid-Range Tablet",
        "specs": {
            "ap": "Snapdragon 870 (7nm 명작 칩셋)",
            "display": "12.7인치 2.9K LCD (2944x1840, 144Hz, 400nits, HDR10)",
            "ram_storage": "8GB LPDDR5 + 128GB / 256GB UFS 3.1 + MicroSD 지원",
            "camera": "800만 후면 / 1300만 전면 초광각",
            "battery": "10,200mAh (20W 고속 충전)",
            "dimensions_weight": "293.4 x 190.8 x 6.9mm / 615g (풀 메탈 유니바디)",
            "os_durability": "ZUI 15 (Android 13) / 쿼드 JBL 스피커",
            "price_krw": "약 21만~25만 원 (역대급 직구 가성비 대란템)"
        }
    },
    {
        "id": "lenovo-xiaoxin-pad-2024",
        "name": "Lenovo Xiaoxin Pad 2024",
        "name_kr": "레노버 샤오신패드 2024 11인치",
        "brand": "Lenovo",
        "brand_kr": "레노버",
        "device_type": "태블릿",
        "release_year": 2023,
        "release_date": "2023-11",
        "category": "Budget Tablet",
        "specs": {
            "ap": "Snapdragon 685 (6nm)",
            "display": "11.0인치 FHD+ IPS LCD (1920x1200, 90Hz, 400nits, TUV 라인란드 시력보호)",
            "ram_storage": "6GB / 8GB LPDDR4X + 128GB UFS 2.2 + MicroSD 슬롯",
            "camera": "800만 후면 / 800만 전면",
            "battery": "7,040mAh (20W 유선 충전)",
            "dimensions_weight": "255.3 x 166.9 x 7.1mm / 465g / 3.5mm 이어폰 잭 탑재",
            "os_durability": "ZUI 15 / 쿼드 스피커 / 인강 및 영상감상 최적화",
            "price_krw": "약 11만~14만 원 (입문용 극가성비)"
        }
    },
    {
        "id": "imuz-mupad-k11-plus",
        "name": "iMuz muPAD K11 PLUS",
        "name_kr": "아이뮤즈 뮤패드 K11 PLUS (LTE)",
        "brand": "iMuz",
        "brand_kr": "아이뮤즈",
        "device_type": "태블릿",
        "release_year": 2024,
        "release_date": "2024-03",
        "category": "Budget/Mid-Range Tablet",
        "specs": {
            "ap": "MediaTek Helio G99 (6nm 옥타코어)",
            "display": "11.0인치 2K IPS LCD (2000x1200, 90Hz 고주사율, 400nits, 인셀 터치)",
            "ram_storage": "8GB LPDDR4X + 128GB / 256GB UFS 2.2 + MicroSD(최대 2TB)",
            "camera": "1300만 후면(AF/플래시) + 500만 전면",
            "battery": "8,590mAh (20W 고속 충전, PD 지원)",
            "dimensions_weight": "256.9 x 168.4 x 7.4mm / 506g (알루미늄 바디)",
            "os_durability": "Android 14 순정 OS / LTE 통신 & GPS & 지자기 센서 완비(네비게이션 최강) / 와이드바인 L1",
            "price_krw": "199,000원부터 (국내 정발 A/S 1티어)"
        }
    },
    {
        "id": "imuz-mupad-k10-plus",
        "name": "iMuz muPAD K10 PLUS",
        "name_kr": "아이뮤즈 뮤패드 K10 PLUS",
        "brand": "iMuz",
        "brand_kr": "아이뮤즈",
        "device_type": "태블릿",
        "release_year": 2023,
        "release_date": "2023-09",
        "category": "Budget Tablet",
        "specs": {
            "ap": "MediaTek Helio G99 (6nm)",
            "display": "10.4인치 2K IPS LCD (2000x1200, 60Hz, 400nits, 완벽 밀착 인셀)",
            "ram_storage": "4GB / 8GB RAM + 64GB / 128GB UFS 2.1 + MicroSD 확장",
            "camera": "500만 후면 / 500만 전면",
            "battery": "6,100mAh (20W 고속 충전)",
            "dimensions_weight": "246.8 x 156.6 x 7.7mm / 453g",
            "os_durability": "Android 13 / 와이드바인 L1 넷플릭스 FHD / 쿼드 스피커",
            "price_krw": "149,000원부터 (국민 가성비 태블릿)"
        }
    },
    {
        "id": "alldocube-iplay-80-mini-pro",
        "name": "ALLDOCUBE iPlay 80 mini Pro",
        "name_kr": "올도큐브 iPlay 80 미니 프로 (2026)",
        "brand": "ALLDOCUBE",
        "brand_kr": "올도큐브",
        "device_type": "태블릿",
        "release_year": 2026,
        "release_date": "2026-03",
        "category": "Compact Tablet",
        "specs": {
            "ap": "MediaTek Dimensity 7050 / Helio G100 (6nm/8nm)",
            "display": "8.4인치 2.5K IPS LCD (2560x1600, 120Hz 고주사율, 450nits, 인셀 터치)",
            "ram_storage": "8GB / 12GB LPDDR4X + 256GB UFS 2.2 + MicroSD(최대 1TB)",
            "camera": "1600만 후면(AF/LED) + 800만 전면",
            "battery": "7,000mAh (33W 고속 충전, 바이패스 충전)",
            "dimensions_weight": "202.5 x 125.8 x 7.4mm / 315g (CNC 알루미늄 일체형)",
            "os_durability": "Android 15 / 5G & LTE 듀얼 SIM / GPS / 넷플릭스 와이드바인 L1",
            "price_krw": "약 17만~21만 원 (2026 가성비 8인치 종결)"
        }
    },
    {
        "id": "alldocube-iplay-80-pro",
        "name": "ALLDOCUBE iPlay 80 Pro",
        "name_kr": "올도큐브 iPlay 80 프로 11인치",
        "brand": "ALLDOCUBE",
        "brand_kr": "올도큐브",
        "device_type": "태블릿",
        "release_year": 2026,
        "release_date": "2026-05",
        "category": "Budget/Mid-Range Tablet",
        "specs": {
            "ap": "MediaTek Dimensity 7050 (6nm)",
            "display": "11.0인치 2.5K IPS LCD (2560x1600, 120Hz, 400nits, DCI-P3)",
            "ram_storage": "8GB / 12GB RAM + 128GB / 256GB + MicroSD",
            "camera": "1300만 후면 + 800만 전면",
            "battery": "8,500mAh (33W 고속 충전)",
            "dimensions_weight": "256.5 x 168.0 x 7.3mm / 495g (쿼드 스피커)",
            "os_durability": "Android 15 / LTE 듀얼 SIM & GPS 지원",
            "price_krw": "약 19만~23만 원"
        }
    },
    {
        "id": "alldocube-iplay-70-mini-pro",
        "name": "ALLDOCUBE iPlay 70 mini Pro",
        "name_kr": "올도큐브 iPlay 70 미니 프로 (2025)",
        "brand": "ALLDOCUBE",
        "brand_kr": "올도큐브",
        "device_type": "태블릿",
        "release_year": 2025,
        "release_date": "2025-02",
        "category": "Compact Tablet",
        "specs": {
            "ap": "MediaTek Helio G99 Ultimate (6nm)",
            "display": "8.4인치 2K IPS LCD (2000x1200, 90Hz, 400nits, 인셀 풀라미네이션)",
            "ram_storage": "8GB RAM + 128GB / 256GB UFS 2.2 + MicroSD",
            "camera": "1300만 후면(플래시) + 500만 전면",
            "battery": "6,500mAh (20W 고속 충전)",
            "dimensions_weight": "202.7 x 126.0 x 7.8mm / 312g",
            "os_durability": "Android 14 / LTE 듀얼 SIM & GPS & 자이로 센서 / 와이드바인 L1",
            "price_krw": "약 15만~18만 원"
        }
    },
    {
        "id": "alldocube-iplay-70-pro",
        "name": "ALLDOCUBE iPlay 70 Pro",
        "name_kr": "올도큐브 iPlay 70 프로 11인치",
        "brand": "ALLDOCUBE",
        "brand_kr": "올도큐브",
        "device_type": "태블릿",
        "release_year": 2025,
        "release_date": "2025-04",
        "category": "Budget Tablet",
        "specs": {
            "ap": "MediaTek Helio G99 Ultimate (6nm)",
            "display": "11.0인치 2K IPS LCD (2000x1200, 90Hz, 400nits)",
            "ram_storage": "8GB RAM + 128GB / 256GB + MicroSD",
            "camera": "1300만 후면 / 800만 전면",
            "battery": "7,500mAh (20W 충전)",
            "dimensions_weight": "256.8 x 168.2 x 7.5mm / 485g (쿼드 스피커)",
            "os_durability": "Android 14 / LTE 듀얼 SIM / 넷플릭스 L1",
            "price_krw": "약 16만~19만 원"
        }
    },
    {
        "id": "alldocube-iplay-60-mini-pro",
        "name": "ALLDOCUBE iPlay 60 mini Pro",
        "name_kr": "올도큐브 iPlay 60 미니 프로",
        "brand": "ALLDOCUBE",
        "brand_kr": "올도큐브",
        "device_type": "태블릿",
        "release_year": 2024,
        "release_date": "2024-05",
        "category": "Compact Tablet",
        "specs": {
            "ap": "MediaTek Helio G99 (6nm)",
            "display": "8.4인치 FHD+ IPS LCD (1920x1200, 90Hz, 350nits, 인셀 풀라미네이션)",
            "ram_storage": "8GB RAM + 128GB / 256GB UFS 2.2 + MicroSD",
            "camera": "1300만 후면(플래시) + 500만 전면",
            "battery": "6,050mAh (18W 고속 충전)",
            "dimensions_weight": "202.7 x 126 x 7.9mm / 310g (한 손에 쏙 들어오는 크기)",
            "os_durability": "Android 14 / LTE 듀얼 SIM & GPS 지원 / 와이드바인 L1 넷플릭스 인증",
            "price_krw": "약 13만~16만 원 (8인치 LTE 가성비 최강)"
        }
    },
    {
        "id": "alldocube-iplay-50-mini-pro-nfe",
        "name": "ALLDOCUBE iPlay 50 mini Pro NFE",
        "name_kr": "올도큐브 iPlay 50 미니 프로 NFE",
        "brand": "ALLDOCUBE",
        "brand_kr": "올도큐브",
        "device_type": "태블릿",
        "release_year": 2023,
        "release_date": "2023-12",
        "category": "Compact Tablet",
        "specs": {
            "ap": "MediaTek Helio G99 (6nm)",
            "display": "8.4인치 FHD+ IPS LCD (1920x1200, 60Hz, 320nits)",
            "ram_storage": "8GB RAM + 128GB / 256GB UFS 2.2 + MicroSD",
            "camera": "1300만 후면 / 500만 전면",
            "battery": "5,000mAh (18W 충전)",
            "dimensions_weight": "202.7 x 126 x 7.5mm / 306g",
            "os_durability": "Android 13 / 넷플릭스 L1 공식 인증 / LTE 데이터 가능",
            "price_krw": "약 12만~14만 원"
        }
    },
    {
        "id": "redmi-pad-pro",
        "name": "Redmi Pad Pro",
        "name_kr": "샤오미 레드미 패드 프로 12.1",
        "brand": "Xiaomi",
        "brand_kr": "샤오미",
        "device_type": "태블릿",
        "release_year": 2024,
        "release_date": "2024-04",
        "category": "Budget/Mid-Range Tablet",
        "specs": {
            "ap": "Snapdragon 7s Gen 2 (4nm)",
            "display": "12.1인치 2.5K LCD (2560x1600, 120Hz, 16:10 비율, 600nits, 고릴라 글래스 3)",
            "ram_storage": "6GB / 8GB LPDDR4X + 128GB / 256GB UFS 2.2 + MicroSD 확장(최대 1.5TB)",
            "camera": "800만 후면 / 800만 전면",
            "battery": "10,000mAh 대용량 (33W 고속 충전)",
            "dimensions_weight": "280.0 x 181.85 x 7.52mm / 571g (메탈 일체형 바디)",
            "os_durability": "Xiaomi HyperOS (Android 14) / 4개 돌비 애트모스 스피커 / 3.5mm 이어폰 잭",
            "price_krw": "279,000원부터 (12인치 대화면 가성비 종결)"
        }
    },
    {
        "id": "poco-pad",
        "name": "POCO Pad",
        "name_kr": "포코 패드 12.1",
        "brand": "Xiaomi",
        "brand_kr": "샤오미",
        "device_type": "태블릿",
        "release_year": 2024,
        "release_date": "2024-05",
        "category": "Budget/Mid-Range Tablet",
        "specs": {
            "ap": "Snapdragon 7s Gen 2 (4nm)",
            "display": "12.1인치 2.5K LCD (2560x1600, 120Hz, 600nits 피크)",
            "ram_storage": "8GB LPDDR4X + 256GB UFS 2.2 + MicroSD",
            "camera": "800만 후면 / 800만 전면",
            "battery": "10,000mAh (33W 고속 유선 충전)",
            "dimensions_weight": "280.0 x 181.85 x 7.52mm / 571g",
            "os_durability": "Xiaomi HyperOS for POCO / 쿼드 스피커",
            "price_krw": "약 28만~31만 원"
        }
    },
    {
        "id": "redmi-pad-se",
        "name": "Redmi Pad SE",
        "name_kr": "샤오미 레드미 패드 SE 11인치",
        "brand": "Xiaomi",
        "brand_kr": "샤오미",
        "device_type": "태블릿",
        "release_year": 2023,
        "release_date": "2023-08",
        "category": "Budget Tablet",
        "specs": {
            "ap": "Snapdragon 680 (6nm)",
            "display": "11.0인치 FHD+ IPS LCD (1920x1200, 90Hz, 400nits)",
            "ram_storage": "4GB / 6GB / 8GB RAM + 128GB / 256GB + MicroSD(최대 1TB)",
            "camera": "800만 후면 / 500만 전면",
            "battery": "8,000mAh (10W/18W 충전)",
            "dimensions_weight": "255.5 x 167.1 x 7.36mm / 478g (알루미늄 유니바디)",
            "os_durability": "MIUI Pad 14 -> HyperOS / 쿼드 스피커 / 3.5mm 잭",
            "price_krw": "149,000원부터 (학생·인강용 국민 태블릿)"
        }
    }
]

# 전체 디바이스 = 스마트폰 + 태블릿 (ID 중복 제거)
unique_devices_map = {}
for dev in smartphones + tablets:
    unique_devices_map[dev["id"]] = dev

all_devices = list(unique_devices_map.values())

def build():
    os.makedirs("src/data", exist_ok=True)
    
    # 1. smartphones.json 업데이트 (전체 스마트폰+태블릿 통합)
    out_path_sp = "src/data/smartphones.json"
    with open(out_path_sp, "w", encoding="utf-8") as f:
        json.dump(all_devices, f, ensure_ascii=False, indent=2)
    
    # 2. devices.json 생성
    out_path_devices = "src/data/devices.json"
    with open(out_path_devices, "w", encoding="utf-8") as f:
        json.dump(all_devices, f, ensure_ascii=False, indent=2)
        
    sp_count = sum(1 for d in all_devices if d.get("device_type") == "스마트폰")
    tb_count = sum(1 for d in all_devices if d.get("device_type") == "태블릿")
    print(f"✅ 총 {len(all_devices)}개 (스마트폰 {sp_count}종 + 태블릿 {tb_count}종) 디바이스 데이터베이스가 생성되었습니다.")

if __name__ == "__main__":
    build()
