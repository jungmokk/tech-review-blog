import json
import os

def enrich_devices_with_zol_standards():
    file_path = "src/data/devices.json"
    with open(file_path, "r", encoding="utf-8") as f:
        devices = json.load(f)
        
    print(f"🔧 Starting ZOL Hardware Standard Enrichment for {len(devices)} devices...")
    
    ZOL_ENRICHMENTS = {
        "xiaomi-15-ultra": {
            "ap": "Snapdragon 8 Elite (3nm TSMC N3E 플래그십)",
            "display": "6.73인치 2K OLED (1~120Hz LTPO, 3,200nits 피크 밝기, 1920Hz 고주파 PWM 조광)",
            "camera": "Sony LYT-900 1인치 50MP 메인(가변 조리개 f/1.63~f/4.0, OIS) + 200MP 망원(Samsung HP9 4.3x 페리스코프) + 50MP 망원(Sony IMX858 3x) + 50MP 초광각",
            "battery": "6,000mAh (90W 유선 고속 충전, 80W 무선 충전, 역충전 지원)",
            "zol_score": "134점 (ZOL 플래그십 AP 1위)"
        },
        "vivo-x200-pro": {
            "ap": "MediaTek Dimensity 9400 (3nm TSMC N3E 차세대 코어)",
            "display": "6.78인치 1.5K 8T LTPO AMOLED (4,500nits 로컬 피크, 2160Hz 초고주파 PWM 조광, Zeiss 내추럴 컬러)",
            "camera": "Sony LYT-818 50MP 1/1.28인치 메인(VCS 3.0, OIS) + 200MP APO 망원(Samsung HP9 1/1.4인치, 3.7x 광학 줌) + 50MP 초광각",
            "battery": "6,000mAh 실리콘-카본 3세대 블루오션 배터리 (90W FlashCharge, 30W 무선 충전)",
            "zol_score": "128점 (ZOL 카메라 & AP 종합 1위)"
        },
        "huawei-mate-xt": {
            "ap": "HiSilicon Kirin 9010 (7nm 중국 자체 공정 옥타코어)",
            "display": "10.2인치 트리플 폴더블 3K OLED (1~120Hz LTPO, 2232x3184 해상도, 1440Hz PWM 조광)",
            "camera": "5,000만 화소 메인(10단 물리 가변 조리개 f/1.4~f/4.0, OIS) + 12MP 초광각 + 12MP 망원(5.5x 광학 줌)",
            "battery": "5,600mAh 초슬림 실리콘 음극 배터리 (66W 유선 초고속 충전, 50W 무선 충전)",
            "zol_score": "125점 (ZOL 폴더블 폼팩터 혁신 1위)"
        },
        "xiaomi-pad-7-pro": {
            "ap": "Snapdragon 8s Gen 3 (4nm TSMC N4P 고성능 코어)",
            "display": "11.2인치 3.2K 초고해상도 LCD (3200x2136, 144Hz 고주사율, 800nits, 풀레인지 DC 디밍)",
            "camera": "5,000만 화소 후면 카메라 + 3,200만 화소 전면 와이드 카메라",
            "battery": "8,850mAh 대용량 배터리 (67W 유선 고속 충전, 45분 완충)",
            "zol_score": "118점 (ZOL 가성비 플래그십 태블릿 1위)"
        },
        "lenovo-legion-y700-2024": {
            "ap": "Snapdragon 8 Gen 3 (4nm TSMC N4P 게이밍 특화 코어)",
            "display": "8.8인치 2.5K 순수 게이밍 패널 (2560x1600, 165Hz 고주사율, 500nits, DCI-P3 100%, DC 조광)",
            "camera": "1,300만 화소 광각 메인 + 200만 화소 매크로",
            "battery": "6,550mAh 대용량 배터리 (68W Super Flash Charge, 듀얼 Type-C 바이패스 충전)",
            "zol_score": "122점 (ZOL 8인치 게이밍 태블릿 1위)"
        },
        "oppo-pad-3-pro": {
            "ap": "Snapdragon 8 Gen 3 Leading Edition (3.4GHz 오버클럭 칩셋)",
            "display": "12.1인치 3K 7:5 황금비율 디스플레이 (3000x2120, 144Hz, 900nits 피크 밝기, Dolby Vision)",
            "camera": "1,300만 화소 후면 카메라 + 800만 화소 전면 카메라",
            "battery": "9,510mAh 대용량 배터리 (67W SUPERVOOC 초고속 충전)",
            "zol_score": "123점 (ZOL 프리미엄 대화면 태블릿 1위)"
        },
        "alldocube-iplay-80-mini-pro": {
            "ap": "MediaTek Dimensity 7050 / Helio G100 (6nm 저전력 고효율)",
            "display": "8.4인치 FHD+ IPS (1920x1200, 90Hz 주사율, 350nits 밝기, 인셀 터치)",
            "camera": "1,300만 화소 후면(AF 지원) + 500만 화소 전면",
            "battery": "5,000mAh 배터리 (18W PD 급속 충전 지원)",
            "zol_score": "95점 (ZOL 초소형 가성비 e-리딩 태블릿)"
        },
        "boox-palma-2": {
            "ap": "Qualcomm Octa-core 2.0GHz + BSR 독자 GPU 가속 칩",
            "display": "6.13인치 E Ink Carta 1200 (1648x824, 300 PPI, 전면 듀얼 조명 CTM 색온도 조절)",
            "camera": "1,600만 화소 후면 문서 스캔 카메라 (LED 플래시 탑재)",
            "battery": "3,950mAh 장시간 리튬 폴리머 배터리",
            "zol_score": "100점 (ZOL 포켓 e-Paper 디바이스 1위)"
        },
        "imuz-mupad-k11-plus": {
            "ap": "MediaTek Helio G99 (6nm 옥타코어)",
            "display": "11.0인치 2K IPS LCD (2000x1200, 90Hz 주사율, 400nits)",
            "camera": "1,300만 화소 후면 + 500만 화소 전면",
            "battery": "7,700mAh 배터리 (20W 고속 충전)",
            "zol_score": "96점 (국내 보급형 가성비 태블릿)"
        },
        "lenovo-xiaoxin-pad-pro-12-7-2025": {
            "ap": "MediaTek Dimensity 8300 (4nm TSMC 고성능 코어)",
            "display": "12.7인치 2.9K 초대화면 LCD (2944x1840, 144Hz 주사율, 400nits, 매트 종이질감 옵션)",
            "camera": "1,300만 화소 후면 + 800만 화소 전면",
            "battery": "10,200mAh 초대용량 배터리 (45W 고속 충전)",
            "zol_score": "115점 (ZOL 12인치급 학습/인강 태블릿 1위)"
        }
    }
    
    updated = 0
    for dev in devices:
        dev_id = dev.get("id")
        if dev_id in ZOL_ENRICHMENTS:
            enrich = ZOL_ENRICHMENTS[dev_id]
            specs = dev.setdefault("specs", {})
            for k, v in enrich.items():
                specs[k] = v
            updated += 1
            print(f"✅ Updated ZOL specs for [{dev_id}]")
            
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(devices, f, ensure_ascii=False, indent=2)
        
    print(f"\n🎉 Successfully enriched {updated} key devices with ZOL Precision Specs standards!")

if __name__ == "__main__":
    enrich_devices_with_zol_standards()
