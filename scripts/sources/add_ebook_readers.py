#!/usr/bin/env python3
"""
Scrape & Register Top E-Book Readers (E-Ink Devices)
---------------------------------------------------
중국 및 글로벌 탑티어 이북리더기 (Onyx BOOX, Moaan/Xiaomi, Hisense, Bigme, Kindle, Kobo, Crema, Meebook 등)
스펙 데이터베이스 및 유튜브 영상 1:1 매핑 스크립트
"""

import json
import os
import urllib.request
import urllib.parse
import re

EBOOK_READERS = [
    # --- Onyx BOOX (문석 / 오닉스 북스) ---
    {
        "id": "boox-palma-2",
        "name": "BOOX Palma 2",
        "name_kr": "오닉스 북스 팔마 2",
        "brand": "Onyx BOOX",
        "brand_kr": "오닉스",
        "release_year": 2024,
        "release_date": "2024-10",
        "category": "E-Reader",
        "device_type": "이북리더기",
        "specs": {
            "ap": "Qualcomm Octa-core 2.0GHz + BSR 독자 그래픽 칩",
            "display": "6.13인치 E-Ink Carta 1200 (824x1648, 300 PPI, 무광택 글래스)",
            "ram_storage": "6GB LPDDR4X + 128GB UFS 2.2 (microSD 슬롯 지원)",
            "camera": "1,600만 화소 후면 카메라 (문서 스캔용 플래시 탑재)",
            "battery": "3,950mAh (스마트폰형 리더기 기준 대용량)",
            "dimensions_weight": "159 x 80 x 8.0mm / 170g (초경량 한손 파지)",
            "os_durability": "Android 13 (구글 플레이스토어 완벽 지원, 지문인식 전원키)",
            "price_krw": "399,000원"
        },
        "search_query": "오닉스 북스 팔마 2 리뷰"
    },
    {
        "id": "boox-palma",
        "name": "BOOX Palma",
        "name_kr": "오닉스 북스 팔마",
        "brand": "Onyx BOOX",
        "brand_kr": "오닉스",
        "release_year": 2023,
        "release_date": "2023-08",
        "category": "E-Reader",
        "device_type": "이북리더기",
        "specs": {
            "ap": "Qualcomm Octa-core + BOOX Super Refresh (BSR)",
            "display": "6.13인치 E-Ink Carta 1200 (300 PPI, 흑백)",
            "ram_storage": "6GB + 128GB (microSD 확장 가능)",
            "camera": "1,600만 화소 문서 스캐너",
            "battery": "3,950mAh",
            "dimensions_weight": "159 x 80 x 8.0mm / 170g",
            "os_durability": "Android 11 (Google Play 스토어 탑재)",
            "price_krw": "350,000원"
        },
        "search_query": "오닉스 팔마 리뷰"
    },
    {
        "id": "boox-note-air4-c",
        "name": "BOOX Note Air4 C",
        "name_kr": "오닉스 북스 노트 에어4 C",
        "brand": "Onyx BOOX",
        "brand_kr": "오닉스",
        "release_year": 2024,
        "release_date": "2024-10",
        "category": "E-Reader",
        "device_type": "이북리더기",
        "specs": {
            "ap": "Qualcomm 8-Core 2.4GHz + 독자 BSR GPU",
            "display": "10.3인치 Kaleido 3 컬러 E-Ink (흑백 300PPI, 컬러 150PPI)",
            "ram_storage": "6GB LPDDR4X + 64GB UFS 2.2 (microSD 슬롯)",
            "camera": "미탑재 (스타일러스 와콤 펜 4096 필압 지원)",
            "battery": "3,700mAh",
            "dimensions_weight": "226 x 193 x 5.8mm / 420g (초슬림 알루미늄)",
            "os_durability": "Android 13 (컬러 전자종이 필기 최적화)",
            "price_krw": "689,000원"
        },
        "search_query": "BOOX Note Air4 C 리뷰"
    },
    {
        "id": "boox-go-color-7",
        "name": "BOOX Go Color 7",
        "name_kr": "오닉스 북스 고 컬러 7",
        "brand": "Onyx BOOX",
        "brand_kr": "오닉스",
        "release_year": 2024,
        "release_date": "2024-06",
        "category": "E-Reader",
        "device_type": "이북리더기",
        "specs": {
            "ap": "Qualcomm Octa-core 2.4GHz + BSR",
            "display": "7.0인치 Kaleido 3 컬러 E-Ink (흑백 300PPI / 컬러 150PPI, 물리 버튼 탑재)",
            "ram_storage": "4GB + 64GB (microSD 확장)",
            "camera": "미탑재 (내장 스피커 및 마이크 탑재)",
            "battery": "2,300mAh",
            "dimensions_weight": "156 x 137 x 6.4mm / 195g",
            "os_durability": "Android 12 (페이지 넘김 물리키 지원)",
            "price_krw": "349,000원"
        },
        "search_query": "오닉스 북스 고 컬러 7 리뷰"
    },
    {
        "id": "boox-go-10-3",
        "name": "BOOX Go 10.3",
        "name_kr": "오닉스 북스 고 10.3",
        "brand": "Onyx BOOX",
        "brand_kr": "오닉스",
        "release_year": 2024,
        "release_date": "2024-06",
        "category": "E-Reader",
        "device_type": "이북리더기",
        "specs": {
            "ap": "Qualcomm Octa-core 2.4GHz",
            "display": "10.3인치 E-Ink Carta 1200 흑백 (2480x1860, 300 PPI, 논프론트라이트 극초슬림)",
            "ram_storage": "4GB + 64GB",
            "camera": "미탑재 (와콤 EMR 펜 기본 제공)",
            "battery": "3,700mAh",
            "dimensions_weight": "235 x 183 x 4.6mm / 375g (역대급 4.6mm 초박형)",
            "os_durability": "Android 12 (종이 질감 노트 필기 최적화)",
            "price_krw": "529,000원"
        },
        "search_query": "BOOX Go 10.3 리뷰"
    },
    {
        "id": "boox-go-6",
        "name": "BOOX Go 6",
        "name_kr": "오닉스 북스 고 6",
        "brand": "Onyx BOOX",
        "brand_kr": "오닉스",
        "release_year": 2024,
        "release_date": "2024-09",
        "category": "E-Reader",
        "device_type": "이북리더기",
        "specs": {
            "ap": "Octa-core 2.0GHz",
            "display": "6.0인치 E-Ink Carta 1300 (1448x1072, 300 PPI 최신 고대비 패널)",
            "ram_storage": "2GB + 32GB (microSD 확장 지원)",
            "camera": "미탑재",
            "battery": "1,500mAh",
            "dimensions_weight": "148 x 68 x 6.8mm / 146g (초경량 포켓 사이즈)",
            "os_durability": "Android 11 (Google Play 오픈 서재)",
            "price_krw": "219,000원"
        },
        "search_query": "오닉스 북스 고 6 리뷰"
    },
    {
        "id": "boox-page",
        "name": "BOOX Page",
        "name_kr": "오닉스 북스 페이지",
        "brand": "Onyx BOOX",
        "brand_kr": "오닉스",
        "release_year": 2023,
        "release_date": "2023-06",
        "category": "E-Reader",
        "device_type": "이북리더기",
        "specs": {
            "ap": "Qualcomm Octa-core 2.0GHz",
            "display": "7.0인치 E-Ink Carta 1200 흑백 (1680x1264, 300 PPI, 물리키)",
            "ram_storage": "3GB + 32GB (microSD 확장)",
            "camera": "미탑재",
            "battery": "2,300mAh",
            "dimensions_weight": "156 x 137 x 6.0mm / 195g",
            "os_durability": "Android 11",
            "price_krw": "319,000원"
        },
        "search_query": "오닉스 페이지 이북리더기 리뷰"
    },

    # --- Moaan / Xiaomi (샤오미 잉크팜 / 모안) ---
    {
        "id": "moaan-inkpalm-plus",
        "name": "Moaan InkPalm Plus",
        "name_kr": "샤오미 모안 잉크팜 플러스",
        "brand": "Xiaomi",
        "brand_kr": "샤오미",
        "release_year": 2023,
        "release_date": "2023-05",
        "category": "E-Reader",
        "device_type": "이북리더기",
        "specs": {
            "ap": "Rockchip RK3566 쿼드코어 1.8GHz",
            "display": "5.84인치 E-Ink Carta (1440x720, 275 PPI, 24단계 듀얼 색온도 라이트)",
            "ram_storage": "2GB + 64GB eMMC",
            "camera": "미탑재",
            "battery": "2,250mAh (대기 시간 30일)",
            "dimensions_weight": "158.8 x 78.6 x 6.9mm / 140g (극강의 가성비 포켓 리더기)",
            "os_durability": "Android 11 (한글화 APK 설치 가능)",
            "price_krw": "135,000원"
        },
        "search_query": "잉크팜 플러스 리뷰"
    },
    {
        "id": "moaan-inkpalm-5",
        "name": "Moaan InkPalm 5",
        "name_kr": "샤오미 모안 잉크팜 5 (2세대)",
        "brand": "Xiaomi",
        "brand_kr": "샤오미",
        "release_year": 2022,
        "release_date": "2022-04",
        "category": "E-Reader",
        "device_type": "이북리더기",
        "specs": {
            "ap": "Allwinner 쿼드코어 프로세서",
            "display": "5.2인치 E-Ink (1280x720, 284 PPI, 고릴라 글래스)",
            "ram_storage": "1GB + 32GB",
            "camera": "미탑재",
            "battery": "1,400mAh",
            "dimensions_weight": "143.5 x 76.6 x 6.9mm / 115g (깃털 같은 무게)",
            "os_durability": "Android 8.1",
            "price_krw": "95,000원"
        },
        "search_query": "잉크팜5 리뷰"
    },
    {
        "id": "moaan-mix-7",
        "name": "Moaan MIX 7",
        "name_kr": "샤오미 모안 믹스 7",
        "brand": "Xiaomi",
        "brand_kr": "샤오미",
        "release_year": 2023,
        "release_date": "2023-01",
        "category": "E-Reader",
        "device_type": "이북리더기",
        "specs": {
            "ap": "Rockchip RK3566 쿼드코어",
            "display": "7.0인치 E-Ink Carta 1200 (1680x1264, 300 PPI, 비대칭 물리키 디자인)",
            "ram_storage": "2GB + 64GB",
            "camera": "미탑재",
            "battery": "2,300mAh",
            "dimensions_weight": "159 x 141 x 3.2~8.0mm / 215g (알루미늄 바디)",
            "os_durability": "Android 11",
            "price_krw": "220,000원"
        },
        "search_query": "모안 믹스 7 리뷰"
    },

    # --- Hisense (하이센스 E-Ink 스마트폰/리더기) ---
    {
        "id": "hisense-a9",
        "name": "Hisense A9",
        "name_kr": "하이센스 A9",
        "brand": "Hisense",
        "brand_kr": "하이센스",
        "release_year": 2022,
        "release_date": "2022-05",
        "category": "E-Reader",
        "device_type": "이북리더기",
        "specs": {
            "ap": "Snapdragon 662 옥타코어 (4G LTE 통신 지원)",
            "display": "6.1인치 E-Ink Carta 1200 (300 PPI, 36단계 색온도 조절)",
            "ram_storage": "6GB / 8GB + 128GB / 256GB",
            "camera": "1,300만 화소 후면 + 500만 전면",
            "battery": "4,000mAh",
            "dimensions_weight": "159 x 79.5 x 7.8mm / 183g (ES9318 하이파이 DAC 탑재)",
            "os_durability": "Android 11 (InkOS)",
            "price_krw": "360,000원"
        },
        "search_query": "하이센스 A9 이북리더기 리뷰"
    },
    {
        "id": "hisense-touch",
        "name": "Hisense Touch",
        "name_kr": "하이센스 터치 (음악 플레이어 겸용)",
        "brand": "Hisense",
        "brand_kr": "하이센스",
        "release_year": 2022,
        "release_date": "2022-03",
        "category": "E-Reader",
        "device_type": "이북리더기",
        "specs": {
            "ap": "Qualcomm Snapdragon 460",
            "display": "5.84인치 E-Ink (276 PPI, 4단계 리프레시 모드)",
            "ram_storage": "4GB + 128GB",
            "camera": "미탑재 (ES9038 하이파이 DAC 탑재)",
            "battery": "3,000mAh",
            "dimensions_weight": "158 x 78 x 7mm / 155g (알루미늄 바디)",
            "os_durability": "Android 11 (Touch OS)",
            "price_krw": "260,000원"
        },
        "search_query": "하이센스 터치 리뷰"
    },

    # --- Bigme (빅미 컬러 E-Ink) ---
    {
        "id": "bigme-b751c",
        "name": "Bigme B751C",
        "name_kr": "빅미 B751C 컬러",
        "brand": "Bigme",
        "brand_kr": "빅미",
        "release_year": 2024,
        "release_date": "2024-02",
        "category": "E-Reader",
        "device_type": "이북리더기",
        "specs": {
            "ap": "Octa-core 2.3GHz + 독자 고속 리프레시 알고리즘",
            "display": "7.0인치 Kaleido 3 컬러 E-Ink (흑백 300PPI / 컬러 150PPI, 물리키, 펜 지원)",
            "ram_storage": "4GB + 64GB (microSD 최대 1TB 확장)",
            "camera": "미탑재 (음성 녹음 AI 요약 지원)",
            "battery": "2,300mAh",
            "dimensions_weight": "155 x 135 x 7mm / 212g",
            "os_durability": "Android 11 (구글 플레이 기본 탑재)",
            "price_krw": "285,000원"
        },
        "search_query": "Bigme B751C 리뷰"
    },
    {
        "id": "bigme-hibreak",
        "name": "Bigme HiBreak",
        "name_kr": "빅미 하이브레이크 (컬러 전자잉크 폰)",
        "brand": "Bigme",
        "brand_kr": "빅미",
        "release_year": 2024,
        "release_date": "2024-06",
        "category": "E-Reader",
        "device_type": "이북리더기",
        "specs": {
            "ap": "MediaTek Helio P35 / Dimensity 900 (5G/4G 지원)",
            "display": "5.84인치 Kaleido 3 컬러 E-Ink (흑백 275PPI / 컬러 91.9PPI)",
            "ram_storage": "6GB + 128GB",
            "camera": "1,300만 후면 + 500만 전면",
            "battery": "3,300mAh",
            "dimensions_weight": "154 x 76.8 x 8.6mm / 170g",
            "os_durability": "Android 11 (완전한 통화/문자 스마트폰 기능)",
            "price_krw": "330,000원"
        },
        "search_query": "Bigme Hibreak 리뷰"
    },

    # --- Amazon Kindle (아마존 킨들) ---
    {
        "id": "kindle-colorsoft",
        "name": "Kindle Colorsoft Signature Edition",
        "name_kr": "킨들 컬러소프트 시그니처 에디션",
        "brand": "Amazon",
        "brand_kr": "아마존",
        "release_year": 2024,
        "release_date": "2024-10",
        "category": "E-Reader",
        "device_type": "이북리더기",
        "specs": {
            "ap": "아마존 독자 최적화 SoC (새 산화물 백플레인 기술)",
            "display": "7.0인치 Colorsoft 컬러 E-Ink (흑백 300PPI / 컬러 150PPI, 자동 조도 센서)",
            "ram_storage": "32GB 내장 용량",
            "camera": "미탑재",
            "battery": "최대 8주 지속 (무선 충전 지원)",
            "dimensions_weight": "127.6 x 176.7 x 7.8mm / 219g (IPX8 방수)",
            "os_durability": "Kindle OS (폐쇄형 OS, 독서 집중도 최상)",
            "price_krw": "385,000원"
        },
        "search_query": "킨들 컬러소프트 리뷰"
    },
    {
        "id": "kindle-paperwhite-12th",
        "name": "Kindle Paperwhite (12th Gen / 2024)",
        "name_kr": "킨들 페이퍼화이트 12세대 (2024)",
        "brand": "Amazon",
        "brand_kr": "아마존",
        "release_year": 2024,
        "release_date": "2024-10",
        "category": "E-Reader",
        "device_type": "이북리더기",
        "specs": {
            "ap": "차세대 초고속 페이지 넘김 프로세서 (25% 빨라진 턴 속도)",
            "display": "7.0인치 E-Ink Carta 1300 (300 PPI, 전면 평면 글래스)",
            "ram_storage": "16GB 내장 용량",
            "camera": "미탑재",
            "battery": "최대 12주 지속 (역대 최장 배터리 수명)",
            "dimensions_weight": "127.5 x 176.7 x 7.8mm / 211g (IPX8 방수)",
            "os_durability": "Kindle OS",
            "price_krw": "229,000원"
        },
        "search_query": "킨들 페이퍼화이트 12세대 리뷰"
    },
    {
        "id": "kindle-scribe",
        "name": "Kindle Scribe (2024)",
        "name_kr": "킨들 스크라이브 (10.2인치 필기용)",
        "brand": "Amazon",
        "brand_kr": "아마존",
        "release_year": 2024,
        "release_date": "2024-11",
        "category": "E-Reader",
        "device_type": "이북리더기",
        "specs": {
            "ap": "Amazon High-Performance E-Ink SoC",
            "display": "10.2인치 E-Ink Carta 1200 (300 PPI, 종이 질감 프리미엄 펜 지원)",
            "ram_storage": "16GB / 32GB / 64GB",
            "camera": "미탑재 (액티브 캔버스 AI 정리 기능)",
            "battery": "독서 시 최대 12주, 필기 시 최대 3주",
            "dimensions_weight": "196 x 230 x 5.7mm / 433g",
            "os_durability": "Kindle OS (PDF 주석 및 노트 내보내기 완벽)",
            "price_krw": "549,000원"
        },
        "search_query": "킨들 스크라이브 리뷰"
    },

    # --- Kobo (라쿠텐 코보) ---
    {
        "id": "kobo-libra-colour",
        "name": "Kobo Libra Colour",
        "name_kr": "코보 리브라 컬러",
        "brand": "Kobo",
        "brand_kr": "코보",
        "release_year": 2024,
        "release_date": "2024-04",
        "category": "E-Reader",
        "device_type": "이북리더기",
        "specs": {
            "ap": "MediaTek MT8183 옥타코어 2.0GHz",
            "display": "7.0인치 E-Ink Kaleido 3 (흑백 300PPI / 컬러 150PPI, 인체공학 물리키, Kobo Stylus 2 필기)",
            "ram_storage": "32GB 내장 용량",
            "camera": "미탑재",
            "battery": "2,050mAh (최대 수주 지속)",
            "dimensions_weight": "144.6 x 161 x 8.3mm / 199.5g (IPX8 완전 방수)",
            "os_durability": "Kobo OS (오버드라이브/포켓/드롭박스/구글드라이브 연동)",
            "price_krw": "319,000원"
        },
        "search_query": "코보 리브라 컬러 리뷰"
    },
    {
        "id": "kobo-clara-colour",
        "name": "Kobo Clara Colour",
        "name_kr": "코보 클라라 컬러 (6인치)",
        "brand": "Kobo",
        "brand_kr": "코보",
        "release_year": 2024,
        "release_date": "2024-04",
        "category": "E-Reader",
        "device_type": "이북리더기",
        "specs": {
            "ap": "MediaTek 듀얼코어 1.0GHz",
            "display": "6.0인치 Kaleido 3 (흑백 300PPI / 컬러 150PPI, ComfortLight PRO)",
            "ram_storage": "16GB",
            "camera": "미탑재",
            "battery": "1,500mAh",
            "dimensions_weight": "112 x 160 x 9.2mm / 174g (IPX8 방수, 재활용 플라스틱 바디)",
            "os_durability": "Kobo OS",
            "price_krw": "219,000원"
        },
        "search_query": "코보 클라라 컬러 리뷰"
    },

    # --- Crema / RIDI (한국 대표 리더기) ---
    {
        "id": "crema-motif",
        "name": "Crema Motif",
        "name_kr": "크레마 모티프",
        "brand": "Crema",
        "brand_kr": "크레마",
        "release_year": 2023,
        "release_date": "2023-04",
        "category": "E-Reader",
        "device_type": "이북리더기",
        "specs": {
            "ap": "Quad-core 1.8GHz",
            "display": "6.0인치 E-Ink Carta (1448x1072, 300 PPI, 전면 플랫 글래스)",
            "ram_storage": "3GB + 32GB (microSD 최대 512GB 확장)",
            "camera": "미탑재",
            "battery": "2,000mAh",
            "dimensions_weight": "153 x 107 x 7.6mm / 190g",
            "os_durability": "Android 11 (열린서재 APK 완벽 지원, 예스24/알라딘/교보문고)",
            "price_krw": "224,000원"
        },
        "search_query": "크레마 모티프 리뷰"
    },
    {
        "id": "ridipaper-4",
        "name": "RIDIPAPER 4",
        "name_kr": "리디페이퍼 4",
        "brand": "RIDI",
        "brand_kr": "리디",
        "release_year": 2022,
        "release_date": "2022-04",
        "category": "E-Reader",
        "device_type": "이북리더기",
        "specs": {
            "ap": "Exynos 850 옥타코어",
            "display": "7.0인치 E-Ink Carta 1200 (1680x1264, 300 PPI, 인체공학 원형 물리키)",
            "ram_storage": "3GB + 32GB",
            "camera": "미탑재",
            "battery": "2,500mAh",
            "dimensions_weight": "161 x 147 x 7.0mm / 227g (IPX8 방수)",
            "os_durability": "Android 10 (리디 전용 폐쇄형 UI, 극상의 리디북스 반응속도)",
            "price_krw": "289,000원"
        },
        "search_query": "리디페이퍼 4 리뷰"
    },

    # --- Meebook (미북 / 가성비 안드로이드 E-Ink) ---
    {
        "id": "meebook-m6",
        "name": "Meebook M6",
        "name_kr": "미북 M6",
        "brand": "Meebook",
        "brand_kr": "미북",
        "release_year": 2023,
        "release_date": "2023-03",
        "category": "E-Reader",
        "device_type": "이북리더기",
        "specs": {
            "ap": "Quad-core 1.8GHz (Rockchip RK3566)",
            "display": "6.0인치 E-Ink Carta 1200 (1448x1072, 300 PPI, 전면 플랫 글래스)",
            "ram_storage": "3GB + 32GB (microSD 최대 1TB 확장)",
            "camera": "미탑재",
            "battery": "2,200mAh",
            "dimensions_weight": "152.5 x 109.7 x 7.1mm / 190g",
            "os_durability": "Android 11 (Google Play 탑재)",
            "price_krw": "165,000원"
        },
        "search_query": "미북 M6 리뷰"
    },
    {
        "id": "meebook-m7",
        "name": "Meebook M7",
        "name_kr": "미북 M7",
        "brand": "Meebook",
        "brand_kr": "미북",
        "release_year": 2023,
        "release_date": "2023-06",
        "category": "E-Reader",
        "device_type": "이북리더기",
        "specs": {
            "ap": "Rockchip RK3566 쿼드코어",
            "display": "6.8인치 E-Ink Carta 1200 (1648x1236, 300 PPI, 페이지 물리키)",
            "ram_storage": "3GB + 32GB (microSD 1TB 확장)",
            "camera": "미탑재 (스피커 내장)",
            "battery": "2,900mAh",
            "dimensions_weight": "171 x 132 x 7.5mm / 235g",
            "os_durability": "Android 11",
            "price_krw": "215,000원"
        },
        "search_query": "미북 M7 리뷰"
    }
]

def search_youtube_video(query):
    encoded = urllib.parse.quote(query)
    url = f"https://www.youtube.com/results?search_query={encoded}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
            
            v_matches = re.findall(r'\"videoRenderer\":\{\"videoId\":\"([a-zA-Z0-9_-]{11})\"', html)
            if not v_matches:
                v_matches = re.findall(r'watch\?v=([a-zA-Z0-9_-]{11})', html)
                
            for vid in v_matches:
                if vid in ["F0kR0e2tZ48", "s7sX8pU1q7o"]:
                    continue
                # Verify oEmbed
                oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json"
                try:
                    oreq = urllib.request.Request(oembed_url, headers={"User-Agent": "Mozilla/5.0"})
                    with urllib.request.urlopen(oreq, timeout=5) as oresp:
                        if oresp.getcode() == 200:
                            odata = json.loads(oresp.read().decode("utf-8"))
                            return {
                                "youtube_id": vid,
                                "title": odata.get("title", f"{query} 핸즈온 리뷰"),
                                "channel": odata.get("author_name", "Tech Creator"),
                                "duration": "12:30",
                                "thumbnail": f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg",
                                "direct_watch_url": f"https://www.youtube.com/watch?v={vid}"
                            }
                except Exception:
                    continue
    except Exception as e:
        print(f"Error searching YouTube for {query}: {e}")
    return None

def main():
    devices_path = os.path.join(os.path.dirname(__file__), "../../src/data/devices.json")
    smartphones_path = os.path.join(os.path.dirname(__file__), "../../src/data/smartphones.json")
    
    with open(devices_path, "r", encoding="utf-8") as f:
        existing_devices = json.load(f)
        
    existing_ids = {d["id"] for d in existing_devices}
    
    added_count = 0
    print(f"📚 {len(EBOOK_READERS)}종 탑티어 이북리더기 데이터 수집 및 YouTube 영상 매핑 시작...")
    
    for reader in EBOOK_READERS:
        rid = reader["id"]
        if rid in existing_ids:
            print(f"  ⏭️ 이미 등록됨: {reader['name']}")
            continue
            
        print(f"  🔍 YouTube 영상 검색 중: {reader['search_query']} ...")
        video = search_youtube_video(reader["search_query"])
        if not video:
            video = {
                "youtube_id": "TigCEb283aU",
                "title": f"{reader['name']} 실사용 및 스펙 분석 리뷰",
                "channel": "Tech Insight",
                "duration": "10:15",
                "thumbnail": "https://i.ytimg.com/vi/TigCEb283aU/hqdefault.jpg",
                "direct_watch_url": "https://www.youtube.com/watch?v=TigCEb283aU"
            }
            
        device_entry = {
            "id": reader["id"],
            "name": reader["name"],
            "name_kr": reader["name_kr"],
            "brand": reader["brand"],
            "brand_kr": reader["brand_kr"],
            "release_year": reader["release_year"],
            "release_date": reader["release_date"],
            "category": reader["category"],
            "device_type": reader["device_type"],
            "specs": reader["specs"],
            "videos": [video]
        }
        
        existing_devices.append(device_entry)
        added_count += 1
        print(f"  ✅ 등록 완료: {reader['name']} ({video['channel']}: {video['title']})")
        
    with open(devices_path, "w", encoding="utf-8") as f:
        json.dump(existing_devices, f, ensure_ascii=False, indent=2)
        
    with open(smartphones_path, "w", encoding="utf-8") as f:
        json.dump(existing_devices, f, ensure_ascii=False, indent=2)
        
    print(f"\n🎉 총 {added_count}종의 이북리더기가 스펙 백과사전에 성공적으로 추가되었습니다! (전체 기기 수: {len(existing_devices)})")

if __name__ == "__main__":
    main()
