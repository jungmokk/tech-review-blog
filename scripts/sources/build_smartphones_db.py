import json
import os

smartphones = [
    # ==========================================
    # 2026년 1월 (최신 플래그십 & 상반기 라인업)
    # ==========================================
    {
        "id": "galaxy-s26-ultra",
        "name": "Galaxy S26 Ultra",
        "name_kr": "갤럭시 S26 울트라",
        "brand": "Samsung",
        "brand_kr": "삼성",
        "release_year": 2026,
        "release_date": "2026-01",
        "category": "Flagship",
        "specs": {
            "ap": "Snapdragon 8 Elite Gen 2 / Exynos 2600 (2nm)",
            "display": "6.9인치 Dynamic AMOLED 2X (3120x1440, 1~120Hz LTPO, 3000nits)",
            "ram_storage": "16GB RAM + 256GB / 512GB / 1TB",
            "camera": "2억 화소 광각(OIS) + 5000만(5x 폴디드 망원) + 5000만(3x 망원) + 5000만(초광각)",
            "battery": "5,200mAh (65W 유선, 25W 무선)",
            "dimensions_weight": "163.0 x 78.0 x 8.1mm / 221g",
            "os_durability": "Android 16 (One UI 8) / IP68 / 2세대 티타늄 아머",
            "price_krw": "약 175만 원부터"
        }
    },
    {
        "id": "galaxy-s26-plus",
        "name": "Galaxy S26+",
        "name_kr": "갤럭시 S26 플러스",
        "brand": "Samsung",
        "brand_kr": "삼성",
        "release_year": 2026,
        "release_date": "2026-01",
        "category": "Flagship",
        "specs": {
            "ap": "Snapdragon 8 Elite Gen 2 / Exynos 2600 (2nm)",
            "display": "6.7인치 Dynamic AMOLED 2X (3120x1440, 1~120Hz LTPO, 2800nits)",
            "ram_storage": "12GB RAM + 256GB / 512GB",
            "camera": "5000만 메인(OIS) + 1000만(3x 망원) + 5000만(초광각)",
            "battery": "4,900mAh (45W 유선, 15W 무선)",
            "dimensions_weight": "158.5 x 75.8 x 7.6mm / 193g",
            "os_durability": "Android 16 (One UI 8) / IP68 / 아머 알루미늄",
            "price_krw": "약 139만 원부터"
        }
    },
    {
        "id": "galaxy-s26",
        "name": "Galaxy S26",
        "name_kr": "갤럭시 S26",
        "brand": "Samsung",
        "brand_kr": "삼성",
        "release_year": 2026,
        "release_date": "2026-01",
        "category": "Flagship",
        "specs": {
            "ap": "Snapdragon 8 Elite Gen 2 / Exynos 2600 (2nm)",
            "display": "6.2인치 Dynamic AMOLED 2X (2340x1080, 1~120Hz LTPO, 2800nits)",
            "ram_storage": "12GB RAM + 256GB / 512GB",
            "camera": "5000만 메인(OIS) + 1000만(3x 망원) + 5000만(초광각)",
            "battery": "4,100mAh (30W 유선, 15W 무선)",
            "dimensions_weight": "147.0 x 70.6 x 7.5mm / 166g",
            "os_durability": "Android 16 (One UI 8) / IP68 / 아머 알루미늄",
            "price_krw": "약 118만 원부터"
        }
    },
    {
        "id": "oneplus-13r",
        "name": "OnePlus 13R",
        "name_kr": "원플러스 13R",
        "brand": "OnePlus",
        "brand_kr": "원플러스",
        "release_year": 2026,
        "release_date": "2026-01",
        "category": "High-End",
        "specs": {
            "ap": "Snapdragon 8 Gen 3 (4nm)",
            "display": "6.78인치 1.5K LTPO 4.0 AMOLED (120Hz, 4500nits 피크)",
            "ram_storage": "12GB / 16GB LPDDR5X + 256GB / 512GB UFS 4.0",
            "camera": "5000만 메인(Sony IMX906 OIS) + 5000만(3x 망원) + 800만(초광각)",
            "battery": "6,000mAh 실리콘 음극 배터리 (100W 초고속 유선)",
            "dimensions_weight": "162.7 x 75.4 x 8.6mm / 206g",
            "os_durability": "OxygenOS 15 (Android 15) / IP65",
            "price_krw": "약 72만 원부터"
        }
    },
    {
        "id": "honor-magic-7-pro",
        "name": "Honor Magic 7 Pro",
        "name_kr": "아너 매직 7 프로",
        "brand": "Honor",
        "brand_kr": "아너",
        "release_year": 2026,
        "release_date": "2026-01",
        "category": "Flagship",
        "specs": {
            "ap": "Snapdragon 8 Elite (3nm)",
            "display": "6.8인치 LTPO OLED (2800x1280, 1~120Hz, 5000nits HDR)",
            "ram_storage": "12GB / 16GB RAM + 512GB / 1TB 스토리지",
            "camera": "5000만 가변조리개 메인 + 2억 화소 잠망경 망원(OIS) + 5000만 초광각",
            "battery": "5,850mAh 탄소 실리콘 배터리 (100W 유선, 80W 무선)",
            "dimensions_weight": "162.7 x 77.1 x 8.8mm / 223g",
            "os_durability": "MagicOS 9.0 (Android 15) / IP69 & IP68",
            "price_krw": "약 115만 원부터"
        }
    },
    {
        "id": "redmi-k80-pro",
        "name": "Redmi K80 Pro",
        "name_kr": "레드미 K80 프로",
        "brand": "Xiaomi",
        "brand_kr": "샤오미",
        "release_year": 2026,
        "release_date": "2026-01",
        "category": "High-End",
        "specs": {
            "ap": "Snapdragon 8 Elite (3nm)",
            "display": "6.67인치 2K TCL M9 OLED (3200x1440, 120Hz, 3200nits)",
            "ram_storage": "12GB / 16GB / 24GB LPDDR5X + 256GB / 512GB / 1TB",
            "camera": "5000만 메인(Light Hunter 800 OIS) + 5000만(2.5x 망원) + 3200만(초광각)",
            "battery": "6,000mAh (120W 유선, 50W 무선)",
            "dimensions_weight": "160.3 x 75.0 x 8.4mm / 212g",
            "os_durability": "Xiaomi HyperOS 2 / IP68",
            "price_krw": "약 68만 원부터"
        }
    },

    # ==========================================
    # 2025년 (플래그십 & 주요 모델들)
    # ==========================================
    {
        "id": "galaxy-s25-ultra",
        "name": "Galaxy S25 Ultra",
        "name_kr": "갤럭시 S25 울트라",
        "brand": "Samsung",
        "brand_kr": "삼성",
        "release_year": 2025,
        "release_date": "2025-01",
        "category": "Flagship",
        "specs": {
            "ap": "Snapdragon 8 Elite for Galaxy (3nm)",
            "display": "6.86인치 Dynamic AMOLED 2X (3120x1440, 1~120Hz LTPO, 2600nits)",
            "ram_storage": "12GB / 16GB RAM + 256GB / 512GB / 1TB",
            "camera": "2억 메인(OIS) + 5000만(5x 망원) + 5000만(초광각) + 1000만(3x 망원)",
            "battery": "5,000mAh (45W 유선, 15W 무선)",
            "dimensions_weight": "162.8 x 77.6 x 8.2mm / 218g",
            "os_durability": "Android 15 (One UI 7) / IP68 / 티타늄 프레임",
            "price_krw": "약 169만 원부터"
        }
    },
    {
        "id": "galaxy-s25-plus",
        "name": "Galaxy S25+",
        "name_kr": "갤럭시 S25 플러스",
        "brand": "Samsung",
        "brand_kr": "삼성",
        "release_year": 2025,
        "release_date": "2025-01",
        "category": "Flagship",
        "specs": {
            "ap": "Snapdragon 8 Elite / Exynos 2500 (3nm)",
            "display": "6.7인치 Dynamic AMOLED 2X (3120x1440, 1~120Hz LTPO, 2600nits)",
            "ram_storage": "12GB RAM + 256GB / 512GB",
            "camera": "5000만 메인(OIS) + 1000만(3x 망원) + 1200만(초광각)",
            "battery": "4,900mAh (45W 유선, 15W 무선)",
            "dimensions_weight": "158.4 x 75.7 x 7.3mm / 190g",
            "os_durability": "Android 15 (One UI 7) / IP68 / 아머 알루미늄",
            "price_krw": "약 135만 원부터"
        }
    },
    {
        "id": "galaxy-s25",
        "name": "Galaxy S25",
        "name_kr": "갤럭시 S25",
        "brand": "Samsung",
        "brand_kr": "삼성",
        "release_year": 2025,
        "release_date": "2025-01",
        "category": "Flagship",
        "specs": {
            "ap": "Snapdragon 8 Elite / Exynos 2500 (3nm)",
            "display": "6.2인치 Dynamic AMOLED 2X (2340x1080, 1~120Hz LTPO, 2600nits)",
            "ram_storage": "12GB RAM + 128GB / 256GB / 512GB",
            "camera": "5000만 메인(OIS) + 1000만(3x 망원) + 1200만(초광각)",
            "battery": "4,000mAh (25W 유선, 15W 무선)",
            "dimensions_weight": "146.9 x 70.4 x 7.2mm / 162g",
            "os_durability": "Android 15 (One UI 7) / IP68 / 아머 알루미늄",
            "price_krw": "약 115만 원부터"
        }
    },
    {
        "id": "galaxy-z-fold7",
        "name": "Galaxy Z Fold7",
        "name_kr": "갤럭시 Z 폴드7",
        "brand": "Samsung",
        "brand_kr": "삼성",
        "release_year": 2025,
        "release_date": "2025-07",
        "category": "Foldable",
        "specs": {
            "ap": "Snapdragon 8 Elite for Galaxy (3nm)",
            "display": "메인 7.6인치 (2160x1856, 120Hz LTPO) / 커버 6.3인치 와이드 (120Hz)",
            "ram_storage": "12GB / 16GB LPDDR5X + 256GB / 512GB / 1TB",
            "camera": "5000만 메인(OIS) + 1000만(3x 망원) + 1200만(초광각)",
            "battery": "4,500mAh (45W 유선, 15W 무선)",
            "dimensions_weight": "접었을 때 11.2mm / 펼쳤을 때 5.2mm / 229g",
            "os_durability": "Android 15 (One UI 7.1) / IP48 / 아머 알루미늄",
            "price_krw": "약 228만 원부터"
        }
    },
    {
        "id": "galaxy-z-flip7",
        "name": "Galaxy Z Flip7",
        "name_kr": "갤럭시 Z 플립7",
        "brand": "Samsung",
        "brand_kr": "삼성",
        "release_year": 2025,
        "release_date": "2025-07",
        "category": "Foldable",
        "specs": {
            "ap": "Snapdragon 8 Elite for Galaxy (3nm)",
            "display": "메인 6.7인치 FHD+ 120Hz LTPO / 커버 3.9인치 FlexWindow 120Hz",
            "ram_storage": "12GB RAM + 256GB / 512GB",
            "camera": "5000만 메인(OIS) + 1200만 초광각",
            "battery": "4,100mAh (25W 유선, 15W 무선)",
            "dimensions_weight": "접었을 때 14.5mm / 펼쳤을 때 6.7mm / 185g",
            "os_durability": "Android 15 (One UI 7.1) / IP48 / 아머 알루미늄",
            "price_krw": "약 148만 원부터"
        }
    },
    {
        "id": "iphone-17-pro-max",
        "name": "iPhone 17 Pro Max",
        "name_kr": "아이폰 17 프로 맥스",
        "brand": "Apple",
        "brand_kr": "애플",
        "release_year": 2025,
        "release_date": "2025-09",
        "category": "Flagship",
        "specs": {
            "ap": "Apple A19 Pro (TSMC 2nm / N2P)",
            "display": "6.9인치 Super Retina XDR OLED (1~120Hz ProMotion, 3000nits 피크)",
            "ram_storage": "12GB RAM + 256GB / 512GB / 1TB / 2TB",
            "camera": "4800만 메인(센서시프트 OIS) + 4800만(5x 테트라프리즘 망원) + 4800만(초광각)",
            "battery": "4,750mAh (35W 고속 유선, 25W MagSafe)",
            "dimensions_weight": "163.0 x 77.6 x 8.25mm / 221g",
            "os_durability": "iOS 19 / IP68 / 5등급 티타늄",
            "price_krw": "약 190만 원부터"
        }
    },
    {
        "id": "iphone-17-pro",
        "name": "iPhone 17 Pro",
        "name_kr": "아이폰 17 프로",
        "brand": "Apple",
        "brand_kr": "애플",
        "release_year": 2025,
        "release_date": "2025-09",
        "category": "Flagship",
        "specs": {
            "ap": "Apple A19 Pro (TSMC 2nm / N2P)",
            "display": "6.3인치 Super Retina XDR OLED (1~120Hz ProMotion, 3000nits 피크)",
            "ram_storage": "12GB RAM + 256GB / 512GB / 1TB",
            "camera": "4800만 메인(센서시프트 OIS) + 4800만(5x 테트라프리즘 망원) + 4800만(초광각)",
            "battery": "3,650mAh (30W 유선, 25W MagSafe)",
            "dimensions_weight": "149.6 x 71.5 x 8.25mm / 195g",
            "os_durability": "iOS 19 / IP68 / 5등급 티타늄",
            "price_krw": "약 155만 원부터"
        }
    },
    {
        "id": "iphone-17-air",
        "name": "iPhone 17 Air (Slim)",
        "name_kr": "아이폰 17 에어",
        "brand": "Apple",
        "brand_kr": "애플",
        "release_year": 2025,
        "release_date": "2025-09",
        "category": "Flagship",
        "specs": {
            "ap": "Apple A19 (TSMC 3nm N3P)",
            "display": "6.6인치 Super Retina XDR OLED (120Hz ProMotion 지원, 2500nits)",
            "ram_storage": "8GB RAM + 128GB / 256GB / 512GB",
            "camera": "4800만 싱글 퓨전 메인 카메라(센서시프트 OIS)",
            "battery": "3,300mAh 초슬림 배터리 (25W 유선, MagSafe)",
            "dimensions_weight": "157.0 x 74.8 x 5.6mm / 165g (극단적 초슬림)",
            "os_durability": "iOS 19 / IP68 / 알루미늄-티타늄 하이브리드",
            "price_krw": "약 150만 원부터"
        }
    },
    {
        "id": "iphone-17",
        "name": "iPhone 17",
        "name_kr": "아이폰 17",
        "brand": "Apple",
        "brand_kr": "애플",
        "release_year": 2025,
        "release_date": "2025-09",
        "category": "Standard",
        "specs": {
            "ap": "Apple A19 (TSMC 3nm N3P)",
            "display": "6.3인치 Super Retina XDR OLED (120Hz ProMotion 최초 탑재, 2500nits)",
            "ram_storage": "8GB RAM + 128GB / 256GB / 512GB",
            "camera": "4800만 메인(센서시프트 OIS) + 4800만 초광각",
            "battery": "3,600mAh (25W 유선, 25W MagSafe)",
            "dimensions_weight": "149.6 x 71.6 x 7.8mm / 172g",
            "os_durability": "iOS 19 / IP68 / 항공우주 등급 알루미늄",
            "price_krw": "약 125만 원부터"
        }
    },
    {
        "id": "pixel-10-pro-xl",
        "name": "Pixel 10 Pro XL",
        "name_kr": "픽셀 10 프로 XL",
        "brand": "Google",
        "brand_kr": "구글",
        "release_year": 2025,
        "release_date": "2025-10",
        "category": "Flagship",
        "specs": {
            "ap": "Google Tensor G5 (TSMC 3nm 공정 최초 전환)",
            "display": "6.8인치 Super Actua OLED (1344x2992, 1~120Hz LTPO, 3000nits)",
            "ram_storage": "16GB RAM + 128GB / 256GB / 512GB / 1TB",
            "camera": "5000만 메인 + 4800만(5x 망원) + 4800만(초광각) / 전면 4200만 AF",
            "battery": "5,100mAh (37W 유선, 23W 무선 Pixels Stand)",
            "dimensions_weight": "162.8 x 76.6 x 8.5mm / 221g",
            "os_durability": "Android 16 / IP68 / 폴리시드 알루미늄 프레임",
            "price_krw": "약 150만 원부터"
        }
    },
    {
        "id": "xiaomi-15-ultra",
        "name": "Xiaomi 15 Ultra",
        "name_kr": "샤오미 15 울트라",
        "brand": "Xiaomi",
        "brand_kr": "샤오미",
        "release_year": 2025,
        "release_date": "2025-02",
        "category": "Flagship",
        "specs": {
            "ap": "Snapdragon 8 Elite (3nm)",
            "display": "6.73인치 2K OLED (3200x1440, 1~120Hz LTPO, 3200nits, 초음파 지문)",
            "ram_storage": "12GB / 16GB LPDDR5X + 256GB / 512GB / 1TB UFS 4.0",
            "camera": "라이카 5000만 1인치 메인(LYT-900 OIS) + 2억 화소(4.3x 잠망경) + 5000만(3.2x 망원) + 5000만(초광각)",
            "battery": "6,000mAh 실리콘-탄소 배터리 (90W 유선, 80W 무선)",
            "dimensions_weight": "161.4 x 75.3 x 9.2mm / 225g",
            "os_durability": "Xiaomi HyperOS 2 / IP68 & IP69",
            "price_krw": "약 130만 원부터"
        }
    },
    {
        "id": "xiaomi-15-pro",
        "name": "Xiaomi 15 Pro",
        "name_kr": "샤오미 15 프로",
        "brand": "Xiaomi",
        "brand_kr": "샤오미",
        "release_year": 2025,
        "release_date": "2025-01",
        "category": "Flagship",
        "specs": {
            "ap": "Snapdragon 8 Elite (3nm)",
            "display": "6.73인치 2K M9 OLED (3200x1440, 120Hz LTPO, 3200nits)",
            "ram_storage": "12GB / 16GB RAM + 256GB / 512GB / 1TB",
            "camera": "5000만 메인(Light Hunter 900 OIS) + 5000만(5x 잠망경 망원) + 5000만(초광각)",
            "battery": "6,100mAh 대용량 배터리 (90W 유선, 50W 무선)",
            "dimensions_weight": "161.3 x 75.3 x 8.35mm / 213g",
            "os_durability": "Xiaomi HyperOS 2 / IP68",
            "price_krw": "약 105만 원부터"
        }
    },
    {
        "id": "xiaomi-15",
        "name": "Xiaomi 15",
        "name_kr": "샤오미 15",
        "brand": "Xiaomi",
        "brand_kr": "샤오미",
        "release_year": 2025,
        "release_date": "2025-01",
        "category": "Flagship",
        "specs": {
            "ap": "Snapdragon 8 Elite (3nm)",
            "display": "6.36인치 1.5K OLED (2670x1200, 1~120Hz LTPO, 3200nits, 초슬림 1.38mm 베젤)",
            "ram_storage": "12GB / 16GB RAM + 256GB / 512GB / 1TB",
            "camera": "5000만 메인(Light Hunter 900 OIS) + 5000만(3.2x 망원) + 5000만(초광각)",
            "battery": "5,400mAh 배터리 (90W 유선, 50W 무선)",
            "dimensions_weight": "152.3 x 71.2 x 8.08mm / 191g",
            "os_durability": "Xiaomi HyperOS 2 / IP68",
            "price_krw": "약 88만 원부터"
        }
    },
    {
        "id": "vivo-x200-pro",
        "name": "Vivo X200 Pro",
        "name_kr": "비보 X200 프로",
        "brand": "Vivo",
        "brand_kr": "비보",
        "release_year": 2025,
        "release_date": "2025-01",
        "category": "Flagship",
        "specs": {
            "ap": "MediaTek Dimensity 9400 (3nm)",
            "display": "6.78인치 1.5K 8T LTPO OLED (2800x1260, 120Hz, 4500nits 피크)",
            "ram_storage": "12GB / 16GB LPDDR5X + 256GB / 512GB / 1TB UFS 4.0",
            "camera": "자이스 5000만 메인(LYT-818 OIS) + 2억 화소(3.7x 잠망경 망원 APO OIS) + 5000만(초광각)",
            "battery": "6,000mAh 3세대 실리콘 음극 블루오션 배터리 (90W 유선, 30W 무선)",
            "dimensions_weight": "162.36 x 75.95 x 8.20mm / 223g",
            "os_durability": "OriginOS 5 (Android 15) / IP68 & IP69",
            "price_krw": "약 105만 원부터"
        }
    },
    {
        "id": "vivo-x200",
        "name": "Vivo X200",
        "name_kr": "비보 X200",
        "brand": "Vivo",
        "brand_kr": "비보",
        "release_year": 2025,
        "release_date": "2025-01",
        "category": "High-End",
        "specs": {
            "ap": "MediaTek Dimensity 9400 (3nm)",
            "display": "6.67인치 LTPS AMOLED (2800x1260, 120Hz, 4500nits 피크)",
            "ram_storage": "12GB / 16GB RAM + 256GB / 512GB / 1TB",
            "camera": "5000만 메인(Sony IMX921 OIS) + 5000만(3x 잠망경) + 5000만(초광각)",
            "battery": "5,800mAh (90W 유선 충전)",
            "dimensions_weight": "160.27 x 74.81 x 7.99mm / 197g",
            "os_durability": "OriginOS 5 / IP68 & IP69",
            "price_krw": "약 85만 원부터"
        }
    },
    {
        "id": "iqoo-13",
        "name": "iQOO 13",
        "name_kr": "아이쿠 13",
        "brand": "Vivo",
        "brand_kr": "비보",
        "release_year": 2025,
        "release_date": "2025-01",
        "category": "Gaming/Flagship",
        "specs": {
            "ap": "Snapdragon 8 Elite (3nm) + Q2 자체 게이밍 슈퍼컴퓨팅 칩",
            "display": "6.82인치 2K BOE Q10 OLED (3168x1440, 144Hz LTPO, 1800nits 글로벌)",
            "ram_storage": "12GB / 16GB LPDDR5X Ultra + 256GB / 512GB / 1TB UFS 4.0",
            "camera": "5000만 메인(Sony IMX921 OIS) + 5000만(2x 망원) + 5000만(초광각)",
            "battery": "6,150mAh 3세대 실리콘 블루오션 배터리 (120W 초고속 유선)",
            "dimensions_weight": "163.37 x 76.71 x 7.99mm / 207g",
            "os_durability": "OriginOS 5 / IP68 & IP69 / 카메라 링 몬스터 헤일로 LED",
            "price_krw": "약 78만 원부터"
        }
    },
    {
        "id": "oppo-find-x8-pro",
        "name": "Oppo Find X8 Pro",
        "name_kr": "오포 파인드 X8 프로",
        "brand": "Oppo",
        "brand_kr": "오포",
        "release_year": 2025,
        "release_date": "2025-01",
        "category": "Flagship",
        "specs": {
            "ap": "MediaTek Dimensity 9400 (3nm)",
            "display": "6.78인치 1.5K LTPO AMOLED (2780x1264, 120Hz, 4500nits 피크)",
            "ram_storage": "12GB / 16GB LPDDR5X + 256GB / 512GB / 1TB",
            "camera": "핫셀블라드 쿼드 5000만 화소 (메인 LYT-800 OIS + 3배 망원 + 6배 잠망경 망원 + 초광각)",
            "battery": "5,910mAh 글레이셔 실리콘 배터리 (80W 유선, 50W 무선)",
            "dimensions_weight": "162.27 x 76.67 x 8.24mm / 215g / 퀵버튼 탑재",
            "os_durability": "ColorOS 15 (Android 15) / IP68 & IP69",
            "price_krw": "약 108만 원부터"
        }
    },
    {
        "id": "oppo-find-x8",
        "name": "Oppo Find X8",
        "name_kr": "오포 파인드 X8",
        "brand": "Oppo",
        "brand_kr": "오포",
        "release_year": 2025,
        "release_date": "2025-01",
        "category": "High-End",
        "specs": {
            "ap": "MediaTek Dimensity 9400 (3nm)",
            "display": "6.59인치 1.5K AMOLED (2760x1256, 120Hz LTPO, 4500nits)",
            "ram_storage": "12GB / 16GB RAM + 256GB / 512GB / 1TB",
            "camera": "핫셀블라드 5000만(Sony LYT-700 OIS) + 5000만(3x 잠망경) + 5000만(초광각)",
            "battery": "5,630mAh (80W 유선, 50W 무선)",
            "dimensions_weight": "157.35 x 74.33 x 7.85mm / 193g",
            "os_durability": "ColorOS 15 / IP68 & IP69",
            "price_krw": "약 82만 원부터"
        }
    },
    {
        "id": "oneplus-13",
        "name": "OnePlus 13",
        "name_kr": "원플러스 13",
        "brand": "OnePlus",
        "brand_kr": "원플러스",
        "release_year": 2025,
        "release_date": "2025-01",
        "category": "Flagship",
        "specs": {
            "ap": "Snapdragon 8 Elite (3nm)",
            "display": "6.82인치 2K BOE X2 Oriental OLED (3168x1440, 1~120Hz LTPO, 4500nits)",
            "ram_storage": "12GB / 16GB / 24GB LPDDR5X + 256GB / 512GB / 1TB UFS 4.0",
            "camera": "핫셀블라드 5000만(Sony LYT-808 OIS) + 5000만(3x 잠망경 망원) + 5000만(초광각)",
            "battery": "6,000mAh 글레이셔 배터리 (100W 유선, 50W 무선 에어보크)",
            "dimensions_weight": "162.9 x 76.5 x 8.5mm / 213g",
            "os_durability": "OxygenOS 15 (Android 15) / IP68 & IP69",
            "price_krw": "약 92만 원부터"
        }
    },
    {
        "id": "huawei-mate-70-pro-plus",
        "name": "Huawei Mate 70 Pro+",
        "name_kr": "화웨이 메이트 70 프로+",
        "brand": "Huawei",
        "brand_kr": "화웨이",
        "release_year": 2025,
        "release_date": "2025-01",
        "category": "Flagship",
        "specs": {
            "ap": "HiSilicon Kirin 9020 자체 칩셋",
            "display": "6.9인치 1.5K LTPO OLED (2832x1316, 120Hz, 2500nits, 2세대 쿤룬 글래스)",
            "ram_storage": "16GB RAM + 512GB / 1TB",
            "camera": "XMAGE 5000만 가변조리개(F1.4~F4.0 OIS) + 4800만(4배 잠망경 망원 매크로) + 4000만 초광각",
            "battery": "5,700mAh 배터리 (100W 유선, 80W 무선)",
            "dimensions_weight": "164.6 x 79.5 x 8.25mm / 226g / 티타늄 바잘트 아키텍처",
            "os_durability": "HarmonyOS NEXT (자체 순수 OS) / IP68 & IP69 / 위성 통신",
            "price_krw": "약 165만 원부터"
        }
    },
    {
        "id": "huawei-pura-70-ultra",
        "name": "Huawei Pura 70 Ultra",
        "name_kr": "화웨이 퓨라 70 울트라",
        "brand": "Huawei",
        "brand_kr": "화웨이",
        "release_year": 2025,
        "release_date": "2025-04",
        "category": "Flagship",
        "specs": {
            "ap": "HiSilicon Kirin 9010",
            "display": "6.8인치 LTPO OLED (2844x1260, 120Hz, 2500nits, 현무 템퍼드 쿤룬 글래스)",
            "ram_storage": "16GB RAM + 512GB / 1TB",
            "camera": "1인치 5000만 화소 팝업 텔레스코픽 가변조리개 메인(OIS) + 5000만(3.5x 매크로 망원) + 4000만(초광각)",
            "battery": "5,200mAh (100W 유선, 80W 무선)",
            "dimensions_weight": "162.6 x 75.1 x 8.4mm / 226g",
            "os_durability": "HarmonyOS 4.2 / IP68 / 위성 메시지/콜",
            "price_krw": "약 190만 원부터"
        }
    },
    {
        "id": "asus-rog-phone-9-pro",
        "name": "Asus ROG Phone 9 Pro",
        "name_kr": "에이수스 ROG 폰 9 프로",
        "brand": "Asus",
        "brand_kr": "에이수스",
        "release_year": 2025,
        "release_date": "2025-01",
        "category": "Gaming",
        "specs": {
            "ap": "Snapdragon 8 Elite (3nm)",
            "display": "6.78인치 삼성 E6 AMOLED (2400x1080, 185Hz 초고주사율 LTPO, 2500nits)",
            "ram_storage": "16GB / 24GB LPDDR5X + 512GB / 1TB UFS 4.0",
            "camera": "5000만(Sony Lytia 700 6축 짐벌 OIS) + 3200만(3x 망원 OIS) + 1300만(초광각)",
            "battery": "5,800mAh (65W 유선, 15W 무선)",
            "dimensions_weight": "163.8 x 76.8 x 8.9mm / 227g / 후면 AniMe Vision 648개 Mini-LED",
            "os_durability": "ROG UI (Android 15) / IP68 / 에어트리거 초음파 버튼",
            "price_krw": "약 160만 원부터"
        }
    },
    {
        "id": "sony-xperia-1-vii",
        "name": "Sony Xperia 1 VII",
        "name_kr": "소니 엑스페리아 1 VII",
        "brand": "Sony",
        "brand_kr": "소니",
        "release_year": 2025,
        "release_date": "2025-05",
        "category": "Flagship",
        "specs": {
            "ap": "Snapdragon 8 Elite (3nm)",
            "display": "6.5인치 19.5:9 FHD+ OLED (1~120Hz LTPO Bravia 튜닝, 2000nits)",
            "ram_storage": "12GB / 16GB RAM + 256GB / 512GB + MicroSD 확장 슬롯",
            "camera": "Exmor T 4800만 메인(OIS) + 85-170mm 연속 광학 줌 망원(1200만 OIS) + 1200만 초광각",
            "battery": "5,000mAh (30W 유선, 무선 충전 지원)",
            "dimensions_weight": "162.0 x 74.0 x 8.2mm / 192g / 3.5mm 헤드폰 잭 탑재",
            "os_durability": "Android 15 / IP65 & IP68 / 고릴라 글래스 빅터스 2",
            "price_krw": "약 175만 원부터"
        }
    },
    {
        "id": "nothing-phone-3",
        "name": "Nothing Phone (3)",
        "name_kr": "낫싱 폰 (3)",
        "brand": "Nothing",
        "brand_kr": "낫싱",
        "release_year": 2025,
        "release_date": "2025-07",
        "category": "High-End",
        "specs": {
            "ap": "Snapdragon 8s Gen 3 / 8 Gen 3 (4nm)",
            "display": "6.7인치 플렉시블 OLED (120Hz LTPO, 2000nits 피크)",
            "ram_storage": "12GB / 16GB RAM + 256GB / 512GB",
            "camera": "5000만 메인(Sony OIS) + 5000만(3x 잠망경 망원) + 5000만(초광각)",
            "battery": "5,200mAh (65W 유선, 15W 무선)",
            "dimensions_weight": "162.1 x 76.4 x 8.4mm / 203g",
            "os_durability": "Nothing OS 3.0 (Android 15) / IP68 / 차세대 글리프 인터페이스",
            "price_krw": "약 89만 원부터"
        }
    },

    # ==========================================
    # 2024년 (주요 스마트폰 라인업)
    # ==========================================
    {
        "id": "galaxy-s24-ultra",
        "name": "Galaxy S24 Ultra",
        "name_kr": "갤럭시 S24 울트라",
        "brand": "Samsung",
        "brand_kr": "삼성",
        "release_year": 2024,
        "release_date": "2024-01",
        "category": "Flagship",
        "specs": {
            "ap": "Snapdragon 8 Gen 3 for Galaxy (4nm)",
            "display": "6.8인치 Dynamic AMOLED 2X (3120x1440, 1~120Hz LTPO, 2600nits)",
            "ram_storage": "12GB RAM + 256GB / 512GB / 1TB",
            "camera": "2억 메인(OIS) + 5000만(5x 망원 OIS) + 1000만(3x 망원 OIS) + 1200만(초광각)",
            "battery": "5,000mAh (45W 유선, 15W 무선)",
            "dimensions_weight": "162.3 x 79.0 x 8.6mm / 232g",
            "os_durability": "Android 14 (One UI 6.1, Galaxy AI 최초 탑재) / IP68 / 티타늄 프레임",
            "price_krw": "1,698,400원부터"
        }
    },
    {
        "id": "galaxy-s24-plus",
        "name": "Galaxy S24+",
        "name_kr": "갤럭시 S24 플러스",
        "brand": "Samsung",
        "brand_kr": "삼성",
        "release_year": 2024,
        "release_date": "2024-01",
        "category": "Flagship",
        "specs": {
            "ap": "Exynos 2400 (4nm)",
            "display": "6.7인치 Dynamic AMOLED 2X (3120x1440 QHD+, 1~120Hz, 2600nits)",
            "ram_storage": "12GB RAM + 256GB / 512GB",
            "camera": "5000만 메인(OIS) + 1000만(3x 망원) + 1200만(초광각)",
            "battery": "4,900mAh (45W 유선, 15W 무선)",
            "dimensions_weight": "158.5 x 75.9 x 7.7mm / 196g",
            "os_durability": "Android 14 (One UI 6.1) / IP68 / 아머 알루미늄 2",
            "price_krw": "1,353,000원부터"
        }
    },
    {
        "id": "galaxy-s24",
        "name": "Galaxy S24",
        "name_kr": "갤럭시 S24",
        "brand": "Samsung",
        "brand_kr": "삼성",
        "release_year": 2024,
        "release_date": "2024-01",
        "category": "Flagship",
        "specs": {
            "ap": "Exynos 2400 (4nm)",
            "display": "6.2인치 Dynamic AMOLED 2X (2340x1080, 1~120Hz, 2600nits)",
            "ram_storage": "8GB RAM + 256GB / 512GB",
            "camera": "5000만 메인(OIS) + 1000만(3x 망원) + 1200만(초광각)",
            "battery": "4,000mAh (25W 유선, 15W 무선)",
            "dimensions_weight": "147.0 x 70.6 x 7.6mm / 167g",
            "os_durability": "Android 14 (One UI 6.1) / IP68 / 아머 알루미늄 2",
            "price_krw": "1,155,000원부터"
        }
    },
    {
        "id": "galaxy-z-fold6",
        "name": "Galaxy Z Fold6",
        "name_kr": "갤럭시 Z 폴드6",
        "brand": "Samsung",
        "brand_kr": "삼성",
        "release_year": 2024,
        "release_date": "2024-07",
        "category": "Foldable",
        "specs": {
            "ap": "Snapdragon 8 Gen 3 for Galaxy (4nm)",
            "display": "메인 7.6인치 (2160x1856, 120Hz LTPO, 2600nits) / 커버 6.3인치 (120Hz)",
            "ram_storage": "12GB RAM + 256GB / 512GB / 1TB",
            "camera": "5000만 메인(OIS) + 1000만(3x 망원) + 1200만(초광각)",
            "battery": "4,400mAh (25W 유선, 15W 무선)",
            "dimensions_weight": "접었을 때 12.1mm / 펼쳤을 때 5.6mm / 239g (각진 플랫 디자인)",
            "os_durability": "Android 14 (One UI 6.1.1) / IP48 최초 방진방수 / 아머 알루미늄",
            "price_krw": "2,229,700원부터"
        }
    },
    {
        "id": "galaxy-z-flip6",
        "name": "Galaxy Z Flip6",
        "name_kr": "갤럭시 Z 플립6",
        "brand": "Samsung",
        "brand_kr": "삼성",
        "release_year": 2024,
        "release_date": "2024-07",
        "category": "Foldable",
        "specs": {
            "ap": "Snapdragon 8 Gen 3 for Galaxy (4nm)",
            "display": "메인 6.7인치 FHD+ 120Hz LTPO (2600nits) / 커버 3.4인치 Super AMOLED",
            "ram_storage": "12GB RAM (플립 최초 12GB) + 256GB / 512GB",
            "camera": "5000만 메인(OIS, 2x 센서 크롭 줌) + 1200만 초광각",
            "battery": "4,000mAh (플립 최초 베이퍼 챔버 탑재, 25W 충전)",
            "dimensions_weight": "접었을 때 14.9mm / 펼쳤을 때 6.9mm / 187g",
            "os_durability": "Android 14 / IP48 방진방수 / 강화된 아머 알루미늄",
            "price_krw": "1,485,000원부터"
        }
    },
    {
        "id": "galaxy-s24-fe",
        "name": "Galaxy S24 FE",
        "name_kr": "갤럭시 S24 FE",
        "brand": "Samsung",
        "brand_kr": "삼성",
        "release_year": 2024,
        "release_date": "2024-10",
        "category": "High-End",
        "specs": {
            "ap": "Exynos 2400e (4nm)",
            "display": "6.7인치 Dynamic AMOLED 2X (2340x1080, 120Hz, 1900nits)",
            "ram_storage": "8GB RAM + 256GB / 512GB",
            "camera": "5000만 메인(OIS) + 800만(3x 망원 OIS) + 1200만(초광각)",
            "battery": "4,700mAh (25W 유선, 15W 무선)",
            "dimensions_weight": "162.0 x 77.3 x 8.0mm / 213g",
            "os_durability": "Android 14 (Galaxy AI 지원) / IP68 / 알루미늄 프레임",
            "price_krw": "946,000원부터"
        }
    },
    {
        "id": "galaxy-a55-5g",
        "name": "Galaxy A55 5G (Quantum 5)",
        "name_kr": "갤럭시 A55 5G / 퀀텀5",
        "brand": "Samsung",
        "brand_kr": "삼성",
        "release_year": 2024,
        "release_date": "2024-03",
        "category": "Mid-Range",
        "specs": {
            "ap": "Exynos 1480 (4nm, AMD RDNA 기반 Xclipse 530 GPU)",
            "display": "6.6인치 Super AMOLED (2340x1080, 120Hz, 1000nits)",
            "ram_storage": "8GB / 12GB RAM + 128GB / 256GB + MicroSD 지원",
            "camera": "5000만 메인(OIS) + 1200만(초광각) + 500만(접사)",
            "battery": "5,000mAh (25W 유선)",
            "dimensions_weight": "161.1 x 77.4 x 8.2mm / 213g (A시리즈 최초 메탈 프레임)",
            "os_durability": "Android 14 (One UI 6.1) / IP67 / 고릴라 글래스 빅터스+",
            "price_krw": "618,200원"
        }
    },
    {
        "id": "iphone-16-pro-max",
        "name": "iPhone 16 Pro Max",
        "name_kr": "아이폰 16 프로 맥스",
        "brand": "Apple",
        "brand_kr": "애플",
        "release_year": 2024,
        "release_date": "2024-09",
        "category": "Flagship",
        "specs": {
            "ap": "Apple A18 Pro (2세대 3nm N3E)",
            "display": "6.9인치 Super Retina XDR OLED (1~120Hz ProMotion, 2000nits, 초슬림 베젤)",
            "ram_storage": "8GB RAM + 256GB / 512GB / 1TB",
            "camera": "4800만 퓨전 메인 + 4800만 초광각 + 1200만(5x 테트라프리즘 망원) / 카메라 컨트롤 버튼 탑재",
            "battery": "4,685mAh (역대 최장 배터리 수명, 25W MagSafe)",
            "dimensions_weight": "163.0 x 77.6 x 8.25mm / 227g",
            "os_durability": "iOS 18 (Apple Intelligence) / IP68 / 5등급 티타늄",
            "price_krw": "1,900,000원부터"
        }
    },
    {
        "id": "iphone-16-pro",
        "name": "iPhone 16 Pro",
        "name_kr": "아이폰 16 프로",
        "brand": "Apple",
        "brand_kr": "애플",
        "release_year": 2024,
        "release_date": "2024-09",
        "category": "Flagship",
        "specs": {
            "ap": "Apple A18 Pro (2세대 3nm N3E)",
            "display": "6.3인치 Super Retina XDR OLED (1~120Hz ProMotion, 2000nits)",
            "ram_storage": "8GB RAM + 128GB / 256GB / 512GB / 1TB",
            "camera": "4800만 퓨전 메인 + 4800만 초광각 + 1200만(5x 테트라프리즘 망원 탑재) / 카메라 컨트롤",
            "battery": "3,582mAh (25W MagSafe)",
            "dimensions_weight": "149.6 x 71.5 x 8.25mm / 199g",
            "os_durability": "iOS 18 / IP68 / 5등급 티타늄",
            "price_krw": "1,550,000원부터"
        }
    },
    {
        "id": "iphone-16-plus",
        "name": "iPhone 16 Plus",
        "name_kr": "아이폰 16 플러스",
        "brand": "Apple",
        "brand_kr": "애플",
        "release_year": 2024,
        "release_date": "2024-09",
        "category": "Standard",
        "specs": {
            "ap": "Apple A18 (3nm N3E)",
            "display": "6.7인치 Super Retina XDR OLED (60Hz, 2000nits, 다이내믹 아일랜드)",
            "ram_storage": "8GB RAM + 128GB / 256GB / 512GB",
            "camera": "4800만 퓨전 메인(2x 광학 퀄리티 줌) + 1200만 초광각(매크로 지원) / 수직 카메라 배치",
            "battery": "4,674mAh (25W MagSafe)",
            "dimensions_weight": "160.9 x 77.8 x 7.8mm / 199g",
            "os_durability": "iOS 18 (Apple Intelligence) / IP68 / 항공우주 알루미늄",
            "price_krw": "1,350,000원부터"
        }
    },
    {
        "id": "iphone-16",
        "name": "iPhone 16",
        "name_kr": "아이폰 16",
        "brand": "Apple",
        "brand_kr": "애플",
        "release_year": 2024,
        "release_date": "2024-09",
        "category": "Standard",
        "specs": {
            "ap": "Apple A18 (3nm N3E)",
            "display": "6.1인치 Super Retina XDR OLED (60Hz, 2000nits)",
            "ram_storage": "8GB RAM + 128GB / 256GB / 512GB",
            "camera": "4800만 퓨전 메인 + 1200만 초광각 / 공간 비디오 촬영 / 카메라 컨트롤 버튼",
            "battery": "3,561mAh (25W MagSafe)",
            "dimensions_weight": "147.6 x 71.6 x 7.8mm / 170g",
            "os_durability": "iOS 18 / IP68 / 항공우주 알루미늄",
            "price_krw": "1,250,000원부터"
        }
    },
    {
        "id": "pixel-9-pro-fold",
        "name": "Pixel 9 Pro Fold",
        "name_kr": "픽셀 9 프로 폴드",
        "brand": "Google",
        "brand_kr": "구글",
        "release_year": 2024,
        "release_date": "2024-08",
        "category": "Foldable",
        "specs": {
            "ap": "Google Tensor G4 (4nm)",
            "display": "메인 8.0인치 Super Actua Flex OLED (120Hz LTPO, 2700nits) / 커버 6.3인치 (120Hz)",
            "ram_storage": "16GB RAM + 256GB / 512GB",
            "camera": "4800만 메인(OIS) + 1080만(5x 망원 OIS) + 1050만(초광각 매크로)",
            "battery": "4,650mAh (45W 급속 유선, 무선 충전)",
            "dimensions_weight": "접었을 때 10.5mm / 펼쳤을 때 5.1mm / 257g (역대 폴더블 중 최상위 슬림)",
            "os_durability": "Android 14 (Gemini Nano 지원) / IPX8 / 새틴 마감 항공우주 알루미늄",
            "price_krw": "약 240만 원부터"
        }
    },
    {
        "id": "pixel-9-pro-xl",
        "name": "Pixel 9 Pro XL",
        "name_kr": "픽셀 9 프로 XL",
        "brand": "Google",
        "brand_kr": "구글",
        "release_year": 2024,
        "release_date": "2024-08",
        "category": "Flagship",
        "specs": {
            "ap": "Google Tensor G4 (4nm)",
            "display": "6.8인치 Super Actua OLED (1344x2992, 1~120Hz LTPO, 3000nits)",
            "ram_storage": "16GB RAM + 128GB / 256GB / 512GB / 1TB",
            "camera": "5000만 메인(OIS) + 4800만(5x 망원 OIS) + 4800만(초광각 AF) / 전면 4200만 AF",
            "battery": "5,060mAh (37W 고속 유선, 23W 무선)",
            "dimensions_weight": "162.8 x 76.6 x 8.5mm / 221g",
            "os_durability": "Android 14 (7년 OS 업데이트) / IP68 / 폴리시드 알루미늄",
            "price_krw": "약 145만 원부터"
        }
    },
    {
        "id": "pixel-9-pro",
        "name": "Pixel 9 Pro",
        "name_kr": "픽셀 9 프로",
        "brand": "Google",
        "brand_kr": "구글",
        "release_year": 2024,
        "release_date": "2024-08",
        "category": "Flagship",
        "specs": {
            "ap": "Google Tensor G4 (4nm)",
            "display": "6.3인치 Super Actua OLED (1280x2856, 1~120Hz LTPO, 3000nits)",
            "ram_storage": "16GB RAM + 128GB / 256GB / 512GB",
            "camera": "5000만 메인(OIS) + 4800만(5x 망원 OIS) + 4800만(초광각) / 전면 4200만",
            "battery": "4,700mAh (27W 유선, 21W 무선)",
            "dimensions_weight": "152.8 x 72.0 x 8.5mm / 199g",
            "os_durability": "Android 14 / IP68 / 폴리시드 알루미늄",
            "price_krw": "약 130만 원부터"
        }
    },
    {
        "id": "pixel-8a",
        "name": "Pixel 8a",
        "name_kr": "픽셀 8a",
        "brand": "Google",
        "brand_kr": "구글",
        "release_year": 2024,
        "release_date": "2024-05",
        "category": "Mid-Range",
        "specs": {
            "ap": "Google Tensor G3 (4nm)",
            "display": "6.1인치 Actua OLED (1080x2400, 120Hz, 2000nits)",
            "ram_storage": "8GB RAM + 128GB / 256GB",
            "camera": "6400만 쿼드PD 메인(OIS) + 1300만 초광각",
            "battery": "4,492mAh (18W 유선, 무선 충전 지원)",
            "dimensions_weight": "152.1 x 72.7 x 8.9mm / 188g",
            "os_durability": "Android 14 (7년 지원) / IP67 / 매트 마감 백",
            "price_krw": "약 65만 원부터"
        }
    },
    {
        "id": "xiaomi-14-ultra",
        "name": "Xiaomi 14 Ultra",
        "name_kr": "샤오미 14 울트라",
        "brand": "Xiaomi",
        "brand_kr": "샤오미",
        "release_year": 2024,
        "release_date": "2024-02",
        "category": "Flagship",
        "specs": {
            "ap": "Snapdragon 8 Gen 3 (4nm)",
            "display": "6.73인치 2K C8 OLED (3200x1440, 1~120Hz LTPO, 3000nits)",
            "ram_storage": "16GB LPDDR5X + 512GB / 1TB UFS 4.0",
            "camera": "라이카 쿼드 5000만 (1인치 LYT-900 무단 가변조리개 F1.63~F4.0 + 3.2x 망원 + 5x 잠망경 망원 + 초광각)",
            "battery": "5,300mAh (90W 유선, 80W 무선 초고속)",
            "dimensions_weight": "161.4 x 75.3 x 9.2mm / 224g (비건 레더 / 티타늄 에디션)",
            "os_durability": "Xiaomi HyperOS (Android 14) / IP68 / 샤오미 쉴드 글래스",
            "price_krw": "약 145만 원부터"
        }
    },
    {
        "id": "redmi-k70-ultra",
        "name": "Redmi K70 Ultra",
        "name_kr": "레드미 K70 울트라",
        "brand": "Xiaomi",
        "brand_kr": "샤오미",
        "release_year": 2024,
        "release_date": "2024-07",
        "category": "High-End",
        "specs": {
            "ap": "MediaTek Dimensity 9300+ (4nm)",
            "display": "6.67인치 1.5K TCL C8+ OLED (2712x1220, 144Hz, 4000nits 피크)",
            "ram_storage": "12GB / 16GB / 24GB RAM + 256GB / 512GB / 1TB",
            "camera": "5000만 메인(Sony IMX906 OIS) + 800만 초광각 + 200만 접사",
            "battery": "5,500mAh (120W 유선, 완전충전 약 20분)",
            "dimensions_weight": "160.4 x 75.1 x 8.4mm / 211g",
            "os_durability": "Xiaomi HyperOS / IP68 / 메탈 프레임",
            "price_krw": "약 52만 원부터"
        }
    },
    {
        "id": "redmi-note-14-pro-plus",
        "name": "Redmi Note 14 Pro+",
        "name_kr": "레드미 노트 14 프로+",
        "brand": "Xiaomi",
        "brand_kr": "샤오미",
        "release_year": 2024,
        "release_date": "2024-09",
        "category": "Mid-Range",
        "specs": {
            "ap": "Snapdragon 7s Gen 3 (4nm)",
            "display": "6.67인치 1.5K 커브드 OLED (120Hz, 3000nits, 고릴라 글래스 빅터스 2)",
            "ram_storage": "12GB / 16GB RAM + 256GB / 512GB",
            "camera": "5000만 메인(Light Hunter 800 OIS) + 5000만(2.5x 망원) + 800만(초광각)",
            "battery": "6,200mAh 대용량 실리콘-탄소 배터리 (90W 유선)",
            "dimensions_weight": "162.5 x 74.7 x 8.7mm / 211g",
            "os_durability": "Xiaomi HyperOS / IP68 & IP69K 방수 최고 등급",
            "price_krw": "약 38만 원부터"
        }
    },
    {
        "id": "poco-f6-pro",
        "name": "POCO F6 Pro",
        "name_kr": "포코 F6 프로",
        "brand": "Xiaomi",
        "brand_kr": "샤오미",
        "release_year": 2024,
        "release_date": "2024-05",
        "category": "High-End",
        "specs": {
            "ap": "Snapdragon 8 Gen 2 (4nm)",
            "display": "6.67인치 WQHD+ Flow AMOLED (3200x1440, 120Hz, 4000nits)",
            "ram_storage": "12GB / 16GB LPDDR5X + 256GB / 512GB / 1TB UFS 4.0",
            "camera": "5000만 메인(Light Fusion 800 OIS) + 800만 초광각 + 200만 접사",
            "battery": "5,000mAh (120W 하이퍼차지, 19분 만충)",
            "dimensions_weight": "160.9 x 75.0 x 8.2mm / 209g (알루미늄 메탈 프레임)",
            "os_durability": "Xiaomi HyperOS / IP54",
            "price_krw": "약 58만 원부터"
        }
    },
    {
        "id": "vivo-x100-ultra",
        "name": "Vivo X100 Ultra",
        "name_kr": "비보 X100 울트라 (타노스)",
        "brand": "Vivo",
        "brand_kr": "비보",
        "release_year": 2024,
        "release_date": "2024-05",
        "category": "Flagship",
        "specs": {
            "ap": "Snapdragon 8 Gen 3 (4nm)",
            "display": "6.78인치 2K E7 AMOLED (3200x1440, 120Hz LTPO, 3000nits, 초음파 지문)",
            "ram_storage": "12GB / 16GB LPDDR5X + 256GB / 512GB / 1TB",
            "camera": "자이스 5000만 1인치(Sony LYT-900 짐벌 OIS) + 2억 화소(HP9 3.7x 잠망경 망원 CIPA 4.5급 OIS) + 5000만 초광각",
            "battery": "5,500mAh 2세대 실리콘 배터리 (80W 유선, 30W 무선)",
            "dimensions_weight": "164.07 x 75.57 x 9.23mm / 229g",
            "os_durability": "OriginOS 4 / IP68 & IP69 / V3+ 영상 이미징 칩",
            "price_krw": "약 135만 원부터"
        }
    },
    {
        "id": "vivo-x-fold3-pro",
        "name": "Vivo X Fold3 Pro",
        "name_kr": "비보 X 폴드3 프로",
        "brand": "Vivo",
        "brand_kr": "비보",
        "release_year": 2024,
        "release_date": "2024-03",
        "category": "Foldable",
        "specs": {
            "ap": "Snapdragon 8 Gen 3 (4nm)",
            "display": "메인 8.03인치 2K+ E7 AMOLED (120Hz LTPO) / 커버 6.53인치 120Hz (듀얼 초음파 지문)",
            "ram_storage": "16GB RAM + 512GB / 1TB",
            "camera": "자이스 5000만 메인(OV50H OIS) + 6400만(3배 잠망경 망원 OIS) + 5000만 초광각",
            "battery": "5,700mAh 대용량 실리콘 음극 (100W 유선, 50W 무선)",
            "dimensions_weight": "접었을 때 11.2mm / 펼쳤을 때 5.2mm / 236g (당시 폴더블 최경량·최강스펙)",
            "os_durability": "OriginOS 4 / IPX8 방수 / 탄소 섬유 초경량 힌지",
            "price_krw": "약 190만 원부터"
        }
    },
    {
        "id": "oppo-find-x7-ultra",
        "name": "Oppo Find X7 Ultra",
        "name_kr": "오포 파인드 X7 울트라",
        "brand": "Oppo",
        "brand_kr": "오포",
        "release_year": 2024,
        "release_date": "2024-01",
        "category": "Flagship",
        "specs": {
            "ap": "Snapdragon 8 Gen 3 (4nm)",
            "display": "6.82인치 2K LTPO AMOLED (3168x1440, 1~120Hz, 4500nits 피크)",
            "ram_storage": "12GB / 16GB LPDDR5X + 256GB / 512GB",
            "camera": "세계 최초 듀얼 잠망경 망원 탑재: 5000만 1인치(LYT-900) + 5000만(3x 잠망경 OIS) + 5000만(6x 잠망경 OIS) + 5000만 초광각",
            "battery": "5,000mAh (100W 유선, 50W 무선)",
            "dimensions_weight": "164.3 x 76.2 x 9.5mm / 221g (투톤 가죽-유리 마감)",
            "os_durability": "ColorOS 14 / IP68 / VIP 프라이버시 물리 슬라이더",
            "price_krw": "약 120만 원부터"
        }
    },
    {
        "id": "oneplus-12",
        "name": "OnePlus 12",
        "name_kr": "원플러스 12",
        "brand": "OnePlus",
        "brand_kr": "원플러스",
        "release_year": 2024,
        "release_date": "2024-01",
        "category": "Flagship",
        "specs": {
            "ap": "Snapdragon 8 Gen 3 (4nm)",
            "display": "6.82인치 2K BOE X1 Oriental OLED (3168x1440, 120Hz LTPO, 4500nits)",
            "ram_storage": "12GB / 16GB / 24GB RAM + 256GB / 512GB / 1TB",
            "camera": "핫셀블라드 5000만(Sony LYT-808 OIS) + 6400만(3x 잠망경 망원 OIS) + 4800만 초광각",
            "battery": "5,400mAh (100W 유선, 50W 무선 에어보크)",
            "dimensions_weight": "164.3 x 75.8 x 9.15mm / 220g",
            "os_durability": "OxygenOS 14 / IP65 / 아쿠아 터치 (젖은 손 터치 완벽 지원)",
            "price_krw": "약 95만 원부터"
        }
    },
    {
        "id": "oneplus-open",
        "name": "OnePlus Open",
        "name_kr": "원플러스 오픈",
        "brand": "OnePlus",
        "brand_kr": "원플러스",
        "release_year": 2024,
        "release_date": "2024-01",
        "category": "Foldable",
        "specs": {
            "ap": "Snapdragon 8 Gen 2 (4nm)",
            "display": "메인 7.82인치 2K+ Flexi-fluid AMOLED (120Hz LTPO, 2800nits) / 커버 6.31인치 (120Hz)",
            "ram_storage": "16GB LPDDR5X + 512GB UFS 4.0",
            "camera": "핫셀블라드 4800만 픽셀스택 메인(LYT-T808 OIS) + 6400만(3배 잠망경 OIS) + 4800만 초광각",
            "battery": "4,805mAh (67W 유선 고속 충전)",
            "dimensions_weight": "접었을 때 11.7mm / 펼쳤을 때 5.8mm / 239g (캔버스 멀티태스킹 최강)",
            "os_durability": "OxygenOS 14 Fold / IPX4 / 알림 슬라이더 탑재",
            "price_krw": "약 210만 원부터"
        }
    },
    {
        "id": "honor-magic-6-pro",
        "name": "Honor Magic 6 Pro",
        "name_kr": "아너 매직 6 프로",
        "brand": "Honor",
        "brand_kr": "아너",
        "release_year": 2024,
        "release_date": "2024-01",
        "category": "Flagship",
        "specs": {
            "ap": "Snapdragon 8 Gen 3 (4nm)",
            "display": "6.8인치 LTPO OLED (2800x1280, 1~120Hz, 5000nits HDR 피크)",
            "ram_storage": "12GB / 16GB RAM + 512GB / 1TB",
            "camera": "5000만 가변조리개(F1.4~F2.0 OIS) + 1억 8000만(2.5x 잠망경 망원 OIS) + 5000만 초광각",
            "battery": "5,600mAh 2세대 실리콘 탄소 배터리 (80W 유선, 66W 무선)",
            "dimensions_weight": "162.5 x 75.8 x 8.9mm / 229g",
            "os_durability": "MagicOS 8.0 (Android 14) / IP68 / 3D 안면인식 ToF",
            "price_krw": "약 120만 원부터"
        }
    },
    {
        "id": "honor-magic-v3",
        "name": "Honor Magic V3",
        "name_kr": "아너 매직 V3",
        "brand": "Honor",
        "brand_kr": "아너",
        "release_year": 2024,
        "release_date": "2024-07",
        "category": "Foldable",
        "specs": {
            "ap": "Snapdragon 8 Gen 3 (4nm)",
            "display": "메인 7.92인치 OLED (120Hz LTPO) / 커버 6.43인치 120Hz (5000nits 피크)",
            "ram_storage": "12GB / 16GB RAM + 256GB / 512GB / 1TB",
            "camera": "5000만 메인(OIS) + 5000만(3.5x 잠망경 망원 OIS) + 4000만 초광각",
            "battery": "5,150mAh 실리콘 탄소 배터리 (66W 유선, 50W 무선)",
            "dimensions_weight": "접었을 때 9.2mm / 펼쳤을 때 4.35mm / 226g (2024 세계 최박형 폴더블)",
            "os_durability": "MagicOS 8.0 / IPX8 방수 / 특수 항공우주 섬유 백",
            "price_krw": "약 215만 원부터"
        }
    },
    {
        "id": "asus-rog-phone-8-pro",
        "name": "Asus ROG Phone 8 Pro",
        "name_kr": "에이수스 ROG 폰 8 프로",
        "brand": "Asus",
        "brand_kr": "에이수스",
        "release_year": 2024,
        "release_date": "2024-01",
        "category": "Gaming",
        "specs": {
            "ap": "Snapdragon 8 Gen 3 (4nm)",
            "display": "6.78인치 삼성 E6 AMOLED (1~120Hz LTPO / 최대 165Hz 게이밍, 2500nits)",
            "ram_storage": "16GB / 24GB LPDDR5X + 512GB / 1TB UFS 4.0",
            "camera": "5000만(Sony IMX890 6축 하이브리드 짐벌 OIS) + 3200만(3x 망원 OIS) + 1300만 초광각",
            "battery": "5,500mAh (65W 유선, 15W Qi 무선)",
            "dimensions_weight": "163.8 x 76.8 x 8.9mm / 225g / 후면 341개 Mini-LED AniMe Vision",
            "os_durability": "ROG UI / IP68 방수방진 게이밍폰 최초 획득",
            "price_krw": "약 155만 원부터"
        }
    },
    {
        "id": "sony-xperia-1-vi",
        "name": "Sony Xperia 1 VI",
        "name_kr": "소니 엑스페리아 1 VI",
        "brand": "Sony",
        "brand_kr": "소니",
        "release_year": 2024,
        "release_date": "2024-05",
        "category": "Flagship",
        "specs": {
            "ap": "Snapdragon 8 Gen 3 (4nm)",
            "display": "6.5인치 19.5:9 FHD+ OLED (1~120Hz LTPO 전환, 1500nits)",
            "ram_storage": "12GB / 16GB RAM + 256GB / 512GB + MicroSD 슬롯",
            "camera": "Exmor T 4800만 메인(OIS) + 85-170mm 연속 광학 줌(1200만 OIS, 매크로 지원) + 1200만 초광각",
            "battery": "5,000mAh (30W 유선, 무선 충전 / 이틀 배터리 수명)",
            "dimensions_weight": "162.0 x 74.0 x 8.2mm / 192g / 3.5mm 오디오 잭",
            "os_durability": "Android 14 / IP65 & IP68 / 고릴라 빅터스 2",
            "price_krw": "약 180만 원부터"
        }
    },
    {
        "id": "nothing-phone-2a-plus",
        "name": "Nothing Phone (2a) Plus",
        "name_kr": "낫싱 폰 (2a) 플러스",
        "brand": "Nothing",
        "brand_kr": "낫싱",
        "release_year": 2024,
        "release_date": "2024-07",
        "category": "Mid-Range",
        "specs": {
            "ap": "MediaTek Dimensity 7350 Pro (4nm)",
            "display": "6.7인치 플렉시블 AMOLED (120Hz, 1300nits 피크)",
            "ram_storage": "12GB RAM + 256GB 스토리지",
            "camera": "5000만 메인(OIS) + 5000만 초광각 / 전면 5000만 셀피",
            "battery": "5,000mAh (50W 고속 충전)",
            "dimensions_weight": "161.7 x 76.3 x 8.5mm / 190g",
            "os_durability": "Nothing OS 2.6 (Android 14) / IP54 / 글리프 인터페이스",
            "price_krw": "499,000원"
        }
    },
    {
        "id": "nothing-phone-2a",
        "name": "Nothing Phone (2a)",
        "name_kr": "낫싱 폰 (2a)",
        "brand": "Nothing",
        "brand_kr": "낫싱",
        "release_year": 2024,
        "release_date": "2024-03",
        "category": "Mid-Range",
        "specs": {
            "ap": "MediaTek Dimensity 7200 Pro (4nm)",
            "display": "6.7인치 플렉시블 AMOLED (120Hz, 1300nits)",
            "ram_storage": "8GB / 12GB RAM + 128GB / 256GB",
            "camera": "5000만 메인(OIS) + 5000만 초광각",
            "battery": "5,000mAh (45W 고속 충전)",
            "dimensions_weight": "161.7 x 76.3 x 8.55mm / 190g",
            "os_durability": "Nothing OS 2.5 / IP54 / 3구역 글리프 LED",
            "price_krw": "429,000원부터"
        }
    },

    # ==========================================
    # 2023년 (명작 및 기념비적 라인업)
    # ==========================================
    {
        "id": "galaxy-s23-ultra",
        "name": "Galaxy S23 Ultra",
        "name_kr": "갤럭시 S23 울트라",
        "brand": "Samsung",
        "brand_kr": "삼성",
        "release_year": 2023,
        "release_date": "2023-02",
        "category": "Flagship",
        "specs": {
            "ap": "Snapdragon 8 Gen 2 for Galaxy (4nm)",
            "display": "6.8인치 Dynamic AMOLED 2X (3088x1440, 1~120Hz LTPO, 1750nits)",
            "ram_storage": "12GB RAM + 256GB / 512GB / 1TB",
            "camera": "2억 화소(ISOCELL HP2 OIS) + 1000만(10x 폴디드 망원 OIS) + 1000만(3x 망원 OIS) + 1200만(초광각)",
            "battery": "5,000mAh (45W 유선, 15W 무선)",
            "dimensions_weight": "163.4 x 78.1 x 8.9mm / 233g / 빌트인 S펜",
            "os_durability": "Android 13 (One UI 5.1 -> 6.1 지원) / IP68 / 아머 알루미늄",
            "price_krw": "1,599,400원부터"
        }
    },
    {
        "id": "galaxy-s23-plus",
        "name": "Galaxy S23+",
        "name_kr": "갤럭시 S23 플러스",
        "brand": "Samsung",
        "brand_kr": "삼성",
        "release_year": 2023,
        "release_date": "2023-02",
        "category": "Flagship",
        "specs": {
            "ap": "Snapdragon 8 Gen 2 for Galaxy (4nm)",
            "display": "6.6인치 Dynamic AMOLED 2X (2340x1080, 48~120Hz, 1750nits)",
            "ram_storage": "8GB RAM + 256GB / 512GB",
            "camera": "5000만 메인(OIS) + 1000만(3x 망원) + 1200만(초광각)",
            "battery": "4,700mAh (45W 유선, 15W 무선)",
            "dimensions_weight": "157.8 x 76.2 x 7.6mm / 195g",
            "os_durability": "Android 13 / IP68 / 아머 알루미늄",
            "price_krw": "1,353,000원부터"
        }
    },
    {
        "id": "galaxy-s23",
        "name": "Galaxy S23",
        "name_kr": "갤럭시 S23",
        "brand": "Samsung",
        "brand_kr": "삼성",
        "release_year": 2023,
        "release_date": "2023-02",
        "category": "Flagship",
        "specs": {
            "ap": "Snapdragon 8 Gen 2 for Galaxy (4nm)",
            "display": "6.1인치 Dynamic AMOLED 2X (2340x1080, 48~120Hz, 1750nits)",
            "ram_storage": "8GB RAM + 256GB / 512GB",
            "camera": "5000만 메인(OIS) + 1000만(3x 망원) + 1200만(초광각)",
            "battery": "3,900mAh (25W 유선, 15W 무선)",
            "dimensions_weight": "146.3 x 70.9 x 7.6mm / 168g (컴팩트 플래그십)",
            "os_durability": "Android 13 / IP68 / 아머 알루미늄",
            "price_krw": "1,155,000원부터"
        }
    },
    {
        "id": "galaxy-z-fold5",
        "name": "Galaxy Z Fold5",
        "name_kr": "갤럭시 Z 폴드5",
        "brand": "Samsung",
        "brand_kr": "삼성",
        "release_year": 2023,
        "release_date": "2023-07",
        "category": "Foldable",
        "specs": {
            "ap": "Snapdragon 8 Gen 2 for Galaxy (4nm)",
            "display": "메인 7.6인치 (2176x1812, 120Hz LTPO, 1750nits) / 커버 6.2인치 120Hz",
            "ram_storage": "12GB RAM + 256GB / 512GB / 1TB",
            "camera": "5000만 메인(OIS) + 1000만(3x 망원 OIS) + 1200만(초광각)",
            "battery": "4,400mAh (25W 유선, 15W 무선)",
            "dimensions_weight": "접었을 때 13.4mm / 펼쳤을 때 6.1mm / 253g (플렉스 힌지 도입)",
            "os_durability": "Android 13 (One UI 5.1.1) / IPX8 방수 / 아머 알루미늄",
            "price_krw": "2,097,700원부터"
        }
    },
    {
        "id": "galaxy-z-flip5",
        "name": "Galaxy Z Flip5",
        "name_kr": "갤럭시 Z 플립5",
        "brand": "Samsung",
        "brand_kr": "삼성",
        "release_year": 2023,
        "release_date": "2023-07",
        "category": "Foldable",
        "specs": {
            "ap": "Snapdragon 8 Gen 2 for Galaxy (4nm)",
            "display": "메인 6.7인치 FHD+ 120Hz LTPO / 커버 3.4인치 플렉스 윈도우 (최초 대화면 커버)",
            "ram_storage": "8GB RAM + 256GB / 512GB",
            "camera": "1200만 듀얼 픽셀 메인(OIS) + 1200만 초광각",
            "battery": "3,700mAh (25W 유선, 15W 무선)",
            "dimensions_weight": "접었을 때 15.1mm / 펼쳤을 때 6.9mm / 187g",
            "os_durability": "Android 13 / IPX8 방수 / 아머 알루미늄",
            "price_krw": "1,399,200원부터"
        }
    },
    {
        "id": "galaxy-a54-5g",
        "name": "Galaxy A54 5G (Quantum 4)",
        "name_kr": "갤럭시 A54 5G / 퀀텀4",
        "brand": "Samsung",
        "brand_kr": "삼성",
        "release_year": 2023,
        "release_date": "2023-03",
        "category": "Mid-Range",
        "specs": {
            "ap": "Exynos 1380 (5nm)",
            "display": "6.4인치 Super AMOLED (2340x1080, 120Hz, 1000nits)",
            "ram_storage": "8GB RAM + 128GB / 256GB + MicroSD 지원",
            "camera": "5000만 메인(플래그십급 GN5 센서 OIS) + 1200만(초광각) + 500만(접사)",
            "battery": "5,000mAh (25W 유선)",
            "dimensions_weight": "158.2 x 76.7 x 8.2mm / 202g (글래스 후면 마감)",
            "os_durability": "Android 13 / IP67 방수방진 / 고릴라 빅터스",
            "price_krw": "618,200원"
        }
    },
    {
        "id": "iphone-15-pro-max",
        "name": "iPhone 15 Pro Max",
        "name_kr": "아이폰 15 프로 맥스",
        "brand": "Apple",
        "brand_kr": "애플",
        "release_year": 2023,
        "release_date": "2023-09",
        "category": "Flagship",
        "specs": {
            "ap": "Apple A17 Pro (세계 최초 TSMC 3nm N3B / 콘솔급 하드웨어 레이트레이싱)",
            "display": "6.7인치 Super Retina XDR OLED (1~120Hz ProMotion, 2000nits)",
            "ram_storage": "8GB RAM + 256GB / 512GB / 1TB",
            "camera": "4800만 메인(센서시프트 2세대 OIS) + 1200만(5x 테트라프리즘 망원 OIS) + 1200만 초광각",
            "battery": "4,422mAh (USB-C 3.0 최초 전환 10Gbps)",
            "dimensions_weight": "159.9 x 76.7 x 8.25mm / 221g (최초 5등급 티타늄 프레임)",
            "os_durability": "iOS 17 (Apple Intelligence 지원) / IP68 / 액션 버튼 도입",
            "price_krw": "1,900,000원부터"
        }
    },
    {
        "id": "iphone-15-pro",
        "name": "iPhone 15 Pro",
        "name_kr": "아이폰 15 프로",
        "brand": "Apple",
        "brand_kr": "애플",
        "release_year": 2023,
        "release_date": "2023-09",
        "category": "Flagship",
        "specs": {
            "ap": "Apple A17 Pro (3nm)",
            "display": "6.1인치 Super Retina XDR OLED (1~120Hz ProMotion, 2000nits)",
            "ram_storage": "8GB RAM + 128GB / 256GB / 512GB / 1TB",
            "camera": "4800만 메인(센서시프트 OIS) + 1200만(3x 망원 OIS) + 1200만 초광각",
            "battery": "3,274mAh (USB-C 3.0 10Gbps)",
            "dimensions_weight": "146.6 x 70.6 x 8.25mm / 187g (초경량 티타늄)",
            "os_durability": "iOS 17 / IP68 / 동작(Action) 버튼",
            "price_krw": "1,550,000원부터"
        }
    },
    {
        "id": "iphone-15-plus",
        "name": "iPhone 15 Plus",
        "name_kr": "아이폰 15 플러스",
        "brand": "Apple",
        "brand_kr": "애플",
        "release_year": 2023,
        "release_date": "2023-09",
        "category": "Standard",
        "specs": {
            "ap": "Apple A16 Bionic (4nm)",
            "display": "6.7인치 Super Retina XDR OLED (60Hz, 2000nits, 다이내믹 아일랜드 도입)",
            "ram_storage": "6GB RAM + 128GB / 256GB / 512GB",
            "camera": "4800만 메인(2x 크롭 무손실 줌) + 1200만 초광각",
            "battery": "4,383mAh (USB-C 도입, 역대 최장 배터리 효율)",
            "dimensions_weight": "160.9 x 77.8 x 7.8mm / 201g (컬러 인퓨즈드 글래스)",
            "os_durability": "iOS 17 / IP68 / 알루미늄",
            "price_krw": "1,350,000원부터"
        }
    },
    {
        "id": "iphone-15",
        "name": "iPhone 15",
        "name_kr": "아이폰 15",
        "brand": "Apple",
        "brand_kr": "애플",
        "release_year": 2023,
        "release_date": "2023-09",
        "category": "Standard",
        "specs": {
            "ap": "Apple A16 Bionic (4nm)",
            "display": "6.1인치 Super Retina XDR OLED (60Hz, 2000nits, 다이내믹 아일랜드)",
            "ram_storage": "6GB RAM + 128GB / 256GB / 512GB",
            "camera": "4800만 메인(2x 크롭 무손실 줌) + 1200만 초광각",
            "battery": "3,349mAh (USB-C 충전)",
            "dimensions_weight": "147.6 x 71.6 x 7.8mm / 171g",
            "os_durability": "iOS 17 / IP68 / 알루미늄",
            "price_krw": "1,250,000원부터"
        }
    },
    {
        "id": "pixel-8-pro",
        "name": "Pixel 8 Pro",
        "name_kr": "픽셀 8 프로",
        "brand": "Google",
        "brand_kr": "구글",
        "release_year": 2023,
        "release_date": "2023-10",
        "category": "Flagship",
        "specs": {
            "ap": "Google Tensor G3 (4nm)",
            "display": "6.7인치 Super Actua OLED (1344x2992, 1~120Hz LTPO, 2400nits, 플랫 패널)",
            "ram_storage": "12GB RAM + 128GB / 256GB / 512GB / 1TB",
            "camera": "5000만 메인(OIS) + 4800만(5x 망원 OIS) + 4800만 초광각 / 온도 센서 탑재",
            "battery": "5,050mAh (30W 유선, 23W 무선)",
            "dimensions_weight": "162.6 x 76.5 x 8.8mm / 213g (매트 무광 유리)",
            "os_durability": "Android 14 (최초 7년 판올림 보장) / IP68 / 폴리시드 알루미늄",
            "price_krw": "약 130만 원부터"
        }
    },
    {
        "id": "pixel-8",
        "name": "Pixel 8",
        "name_kr": "픽셀 8",
        "brand": "Google",
        "brand_kr": "구글",
        "release_year": 2023,
        "release_date": "2023-10",
        "category": "Standard",
        "specs": {
            "ap": "Google Tensor G3 (4nm)",
            "display": "6.2인치 Actua OLED (1080x2400, 60~120Hz, 2000nits)",
            "ram_storage": "8GB RAM + 128GB / 256GB",
            "camera": "5000만 메인(OIS) + 1200만 초광각(매크로 지원)",
            "battery": "4,575mAh (27W 유선, 18W 무선)",
            "dimensions_weight": "150.5 x 70.8 x 8.9mm / 187g",
            "os_durability": "Android 14 (7년 지원) / IP68 / 새틴 알루미늄",
            "price_krw": "약 90만 원부터"
        }
    },
    {
        "id": "pixel-fold",
        "name": "Pixel Fold",
        "name_kr": "픽셀 폴드 1세대",
        "brand": "Google",
        "brand_kr": "구글",
        "release_year": 2023,
        "release_date": "2023-06",
        "category": "Foldable",
        "specs": {
            "ap": "Google Tensor G2 (5nm)",
            "display": "메인 7.6인치 (1840x2208, 120Hz) / 커버 5.8인치 와이드 120Hz (17.4:9)",
            "ram_storage": "12GB RAM + 256GB / 512GB",
            "camera": "4800만 메인(OIS) + 1080만(5x 망원 OIS) + 1080만 초광각",
            "battery": "4,821mAh (30W 유선, 무선 충전)",
            "dimensions_weight": "접었을 때 12.1mm / 펼쳤을 때 5.8mm / 283g",
            "os_durability": "Android 13 / IPX8 방수 / 폴리시드 스테인리스 힌지",
            "price_krw": "약 230만 원부터"
        }
    },
    {
        "id": "pixel-7a",
        "name": "Pixel 7a",
        "name_kr": "픽셀 7a",
        "brand": "Google",
        "brand_kr": "구글",
        "release_year": 2023,
        "release_date": "2023-05",
        "category": "Mid-Range",
        "specs": {
            "ap": "Google Tensor G2 (5nm)",
            "display": "6.1인치 OLED (1080x2400, 90Hz)",
            "ram_storage": "8GB RAM + 128GB UFS 3.1",
            "camera": "6400만 쿼드PD 메인(OIS) + 1300만 초광각",
            "battery": "4,385mAh (18W 유선, 7.5W 무선 충전 A시리즈 최초 지원)",
            "dimensions_weight": "152.0 x 72.9 x 9.0mm / 193.5g",
            "os_durability": "Android 13 / IP67 / 알루미늄 프레임",
            "price_krw": "약 60만 원부터"
        }
    },
    {
        "id": "xiaomi-13-ultra",
        "name": "Xiaomi 13 Ultra",
        "name_kr": "샤오미 13 울트라",
        "brand": "Xiaomi",
        "brand_kr": "샤오미",
        "release_year": 2023,
        "release_date": "2023-04",
        "category": "Flagship",
        "specs": {
            "ap": "Snapdragon 8 Gen 2 (4nm)",
            "display": "6.73인치 2K C7 OLED (3200x1440, 120Hz LTPO, 2600nits)",
            "ram_storage": "12GB / 16GB LPDDR5X + 256GB / 512GB / 1TB",
            "camera": "라이카 쿼드 5000만: 1인치 IMX989 가변조리개(F1.9/F4.0 OIS) + 3.2x 망원(OIS) + 5x 잠망경(OIS) + 초광각",
            "battery": "5,000mAh (90W 유선, 50W 무선)",
            "dimensions_weight": "163.18 x 74.64 x 9.06mm / 227g (카메라 그립 키트 지원)",
            "os_durability": "MIUI 14 (Android 13) / IP68 / 항균 나노 가죽",
            "price_krw": "약 120만 원부터"
        }
    },
    {
        "id": "xiaomi-13-pro",
        "name": "Xiaomi 13 Pro",
        "name_kr": "샤오미 13 프로",
        "brand": "Xiaomi",
        "brand_kr": "샤오미",
        "release_year": 2023,
        "release_date": "2023-01",
        "category": "Flagship",
        "specs": {
            "ap": "Snapdragon 8 Gen 2 (4nm)",
            "display": "6.73인치 2K E6 AMOLED (3200x1440, 120Hz LTPO, 1900nits)",
            "ram_storage": "8GB / 12GB RAM + 128GB / 256GB / 512GB",
            "camera": "라이카 5000만 1인치(Sony IMX989 OIS) + 5000만(3.2x 플로팅 망원 OIS) + 5000만 초광각",
            "battery": "4,820mAh (120W 유선 19분 만충, 50W 무선)",
            "dimensions_weight": "162.9 x 74.6 x 8.38mm / 229g (세라믹 바디)",
            "os_durability": "MIUI 14 / IP68",
            "price_krw": "약 110만 원부터"
        }
    },
    {
        "id": "xiaomi-13",
        "name": "Xiaomi 13",
        "name_kr": "샤오미 13",
        "brand": "Xiaomi",
        "brand_kr": "샤오미",
        "release_year": 2023,
        "release_date": "2023-01",
        "category": "Flagship",
        "specs": {
            "ap": "Snapdragon 8 Gen 2 (4nm)",
            "display": "6.36인치 FHD+ E6 AMOLED (120Hz, 1900nits, 플랫 디자인)",
            "ram_storage": "8GB / 12GB RAM + 128GB / 256GB / 512GB",
            "camera": "라이카 5000만 메인(IMX800 OIS) + 1000만(3.2x 망원 OIS) + 1200만 초광각",
            "battery": "4,500mAh (67W 유선, 50W 무선, 10W 역무선)",
            "dimensions_weight": "152.8 x 71.5 x 7.98mm / 189g",
            "os_durability": "MIUI 14 / IP68 / 유광 알루미늄",
            "price_krw": "약 85만 원부터"
        }
    },
    {
        "id": "redmi-k60-ultra",
        "name": "Redmi K60 Ultra",
        "name_kr": "레드미 K60 울트라",
        "brand": "Xiaomi",
        "brand_kr": "샤오미",
        "release_year": 2023,
        "release_date": "2023-08",
        "category": "High-End",
        "specs": {
            "ap": "MediaTek Dimensity 9200+ (4nm) + X7 독립 그래픽 칩",
            "display": "6.67인치 1.5K OLED (2712x1220, 144Hz, 2600nits)",
            "ram_storage": "12GB / 16GB / 24GB LPDDR5X + 256GB / 512GB / 1TB UFS 4.0",
            "camera": "5000만 메인(Sony IMX800 OIS) + 800만 초광각 + 200만 접사",
            "battery": "5,000mAh (120W 유선 초고속)",
            "dimensions_weight": "162.15 x 75.7 x 8.49mm / 204g",
            "os_durability": "MIUI 14 / IP68 최초 획득",
            "price_krw": "약 49만 원부터"
        }
    },
    {
        "id": "redmi-note-13-pro-plus",
        "name": "Redmi Note 13 Pro+",
        "name_kr": "레드미 노트 13 프로+",
        "brand": "Xiaomi",
        "brand_kr": "샤오미",
        "release_year": 2023,
        "release_date": "2023-09",
        "category": "Mid-Range",
        "specs": {
            "ap": "MediaTek Dimensity 7200-Ultra (4nm)",
            "display": "6.67인치 1.5K 커브드 OLED (120Hz, 1800nits, 고릴라 빅터스)",
            "ram_storage": "8GB / 12GB / 16GB RAM + 256GB / 512GB",
            "camera": "2억 화소(Samsung ISOCELL HP3 OIS 4x 무손실 줌) + 800만 초광각 + 200만 접사",
            "battery": "5,000mAh (120W 유선 하이퍼차지, 19분 만충)",
            "dimensions_weight": "161.4 x 74.2 x 8.9mm / 204.5g",
            "os_durability": "MIUI 14 / IP68 방수방진 (노트 시리즈 최초)",
            "price_krw": "399,000원부터"
        }
    },
    {
        "id": "poco-f5-pro",
        "name": "POCO F5 Pro",
        "name_kr": "포코 F5 프로",
        "brand": "Xiaomi",
        "brand_kr": "샤오미",
        "release_year": 2023,
        "release_date": "2023-05",
        "category": "High-End",
        "specs": {
            "ap": "Snapdragon 8+ Gen 1 (4nm)",
            "display": "6.67인치 WQHD+ AMOLED (3200x1440, 120Hz, 1400nits)",
            "ram_storage": "8GB / 12GB LPDDR5 + 256GB / 512GB UFS 3.1",
            "camera": "6400만 메인(OIS) + 800만 초광각 + 200만 매크로",
            "battery": "5,160mAh (67W 유선, 30W 무선 충전 POCO 최초 탑재)",
            "dimensions_weight": "162.78 x 75.44 x 8.59mm / 204g",
            "os_durability": "MIUI 14 for POCO / IP53",
            "price_krw": "약 53만 원부터"
        }
    },
    {
        "id": "vivo-x90-pro-plus",
        "name": "Vivo X90 Pro+",
        "name_kr": "비보 X90 프로+",
        "brand": "Vivo",
        "brand_kr": "비보",
        "release_year": 2023,
        "release_date": "2023-01",
        "category": "Flagship",
        "specs": {
            "ap": "Snapdragon 8 Gen 2 (4nm)",
            "display": "6.78인치 2K Samsung E6 AMOLED (3200x1440, 120Hz LTPO 4.0, 1800nits, 초음파 지문)",
            "ram_storage": "12GB LPDDR5X + 256GB / 512GB UFS 4.0",
            "camera": "자이스 5000만 1인치(Sony IMX989 OIS) + 6400만(3.5x 잠망경 망원 OIS) + 5000만(2x 인물 망원 OIS) + 4800만 초광각",
            "battery": "4,700mAh (80W 유선, 50W 무선)",
            "dimensions_weight": "164.35 x 75.29 x 9.7mm / 221g (비건 레더)",
            "os_durability": "OriginOS 3 / IP68 / V2 자체 ISP 칩",
            "price_krw": "약 125만 원부터"
        }
    },
    {
        "id": "iqoo-11-pro",
        "name": "iQOO 11 Pro",
        "name_kr": "아이쿠 11 프로",
        "brand": "Vivo",
        "brand_kr": "비보",
        "release_year": 2023,
        "release_date": "2023-01",
        "category": "Gaming/Flagship",
        "specs": {
            "ap": "Snapdragon 8 Gen 2 (4nm) + V2 칩",
            "display": "6.78인치 2K Samsung E6 AMOLED (3200x1440, 144Hz LTPO 4.0, 1800nits)",
            "ram_storage": "8GB / 12GB / 16GB LPDDR5X + 256GB / 512GB UFS 4.0",
            "camera": "5000만 메인(Sony VCS IMX866 OIS) + 5000만(150도 어안 초광각) + 1300만(2x 인물 망원)",
            "battery": "4,700mAh (200W 초고속 유선 10분 만충, 50W 무선)",
            "dimensions_weight": "164.76 x 75.3 x 8.89mm / 210.5g / BMW M 모터스포츠 에디션",
            "os_durability": "OriginOS 3 / 3D 초음파 광역 지문인식",
            "price_krw": "약 98만 원부터"
        }
    },
    {
        "id": "oppo-find-x6-pro",
        "name": "Oppo Find X6 Pro",
        "name_kr": "오포 파인드 X6 프로",
        "brand": "Oppo",
        "brand_kr": "오포",
        "release_year": 2023,
        "release_date": "2023-03",
        "category": "Flagship",
        "specs": {
            "ap": "Snapdragon 8 Gen 2 (4nm)",
            "display": "6.82인치 2K Samsung E6 AMOLED (3168x1440, 120Hz LTPO 3.0, 2500nits)",
            "ram_storage": "12GB / 16GB LPDDR5X + 256GB / 512GB UFS 4.0",
            "camera": "핫셀블라드 트리플 5000만 1/1.56인치 이상급(1인치 IMX989 메인 + IMX890 3x 잠망경 망원 + IMX890 초광각)",
            "battery": "5,000mAh (100W 유선, 50W 무선)",
            "dimensions_weight": "164.8 x 76.2 x 9.1mm / 218g (클래식 카메라 가죽 디자인)",
            "os_durability": "ColorOS 13.1 / IP68 / 마리아나X 칩",
            "price_krw": "약 115만 원부터"
        }
    },
    {
        "id": "oneplus-11",
        "name": "OnePlus 11",
        "name_kr": "원플러스 11",
        "brand": "OnePlus",
        "brand_kr": "원플러스",
        "release_year": 2023,
        "release_date": "2023-01",
        "category": "Flagship",
        "specs": {
            "ap": "Snapdragon 8 Gen 2 (4nm)",
            "display": "6.7인치 2K Super Fluid AMOLED (3216x1440, 120Hz LTPO 3.0, 1300nits)",
            "ram_storage": "8GB / 16GB LPDDR5X + 128GB / 256GB / 512GB UFS 4.0",
            "camera": "핫셀블라드 5000만(Sony IMX890 OIS) + 3200만(2x 인물 망원) + 4800만 초광각",
            "battery": "5,000mAh (100W SUPERVOOC 유선 충전 25분 만충)",
            "dimensions_weight": "163.1 x 74.1 x 8.53mm / 205g / 블랙홀 카메라 모듈",
            "os_durability": "OxygenOS 13 / IP64 / 알림 슬라이더 복귀",
            "price_krw": "약 89만 원부터"
        }
    },
    {
        "id": "huawei-mate-60-pro",
        "name": "Huawei Mate 60 Pro",
        "name_kr": "화웨이 메이트 60 프로",
        "brand": "Huawei",
        "brand_kr": "화웨이",
        "release_year": 2023,
        "release_date": "2023-08",
        "category": "Flagship",
        "specs": {
            "ap": "HiSilicon Kirin 9000S (중국 자체 7nm 제조 칩셋)",
            "display": "6.82인치 1.5K LTPO OLED (2720x1260, 120Hz, 2세대 쿤룬 글래스)",
            "ram_storage": "12GB RAM + 256GB / 512GB / 1TB + NM 카드 확장",
            "camera": "XMAGE 5000만 가변조리개(F1.4~F4.0 OIS) + 4800만(3.5x 잠망경 망원 매크로 OIS) + 1200만 초광각",
            "battery": "5,000mAh (88W 유선, 50W 무선, 20W 역무선)",
            "dimensions_weight": "163.65 x 79.0 x 8.1mm / 225g / 상단 3개 펀치홀",
            "os_durability": "HarmonyOS 4.0 / IP68 / 세계 최초 일반 스마트폰 위성 통화 지원",
            "price_krw": "약 130만 원부터"
        }
    },
    {
        "id": "honor-magic-5-pro",
        "name": "Honor Magic 5 Pro",
        "name_kr": "아너 매직 5 프로",
        "brand": "Honor",
        "brand_kr": "아너",
        "release_year": 2023,
        "release_date": "2023-03",
        "category": "Flagship",
        "specs": {
            "ap": "Snapdragon 8 Gen 2 (4nm)",
            "display": "6.81인치 LTPO OLED (2848x1312, 120Hz, 1800nits)",
            "ram_storage": "12GB / 16GB RAM + 512GB UFS 4.0",
            "camera": "트리플 5000만 (메인 1/1.12인치 커스텀 센서 OIS + 3.5x 잠망경 망원 OIS + 초광각)",
            "battery": "5,100mAh (66W 유선, 50W 무선)",
            "dimensions_weight": "162.9 x 76.7 x 8.77mm / 219g (아이 오브 뮤즈 서큘러 디자인)",
            "os_durability": "MagicOS 7.1 / IP68 / 3D 안면인식",
            "price_krw": "약 115만 원부터"
        }
    },
    {
        "id": "nothing-phone-2",
        "name": "Nothing Phone (2)",
        "name_kr": "낫싱 폰 (2)",
        "brand": "Nothing",
        "brand_kr": "낫싱",
        "release_year": 2023,
        "release_date": "2023-07",
        "category": "High-End",
        "specs": {
            "ap": "Snapdragon 8+ Gen 1 (4nm)",
            "display": "6.7인치 플렉시블 OLED (1~120Hz LTPO, 1600nits)",
            "ram_storage": "8GB / 12GB RAM + 128GB / 256GB / 512GB",
            "camera": "5000만 메인(Sony IMX890 OIS) + 5000만 초광각",
            "battery": "4,700mAh (45W 유선, 15W 무선, 5W 역무선)",
            "dimensions_weight": "162.1 x 76.4 x 8.6mm / 201.2g",
            "os_durability": "Nothing OS 2.0 / IP54 / 33개 구역 글리프 LED",
            "price_krw": "899,000원부터"
        }
    }
]

def build():
    os.makedirs("src/data", exist_ok=True)
    out_path = "src/data/smartphones.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(smartphones, f, ensure_ascii=False, indent=2)
    print(f"✅ 총 {len(smartphones)}개 스마트폰 스펙 데이터베이스가 생성되었습니다: {out_path}")

if __name__ == "__main__":
    build()
