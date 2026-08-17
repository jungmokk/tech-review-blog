import urllib.request
import urllib.parse
import re
import json
import os
import subprocess
import time

class ZOLEngine:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "Referer": "https://detail.zol.com.cn/",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        }
        
    def search_device(self, keyword):
        """Search ZOL for product ID and basic info via direct query"""
        # Encode with GBK for ZOL search
        try:
            kw_gbk = urllib.parse.quote(keyword.encode('gbk', errors='ignore'))
            search_url = f"https://detail.zol.com.cn/index.php?c=SearchList&kword={kw_gbk}"
            
            req = urllib.request.Request(search_url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                html = resp.read().decode("gbk", errors="ignore")
                
                # Regex for product list items on ZOL search page
                # <a href="/cell_phone/index1428389.shtml" target="_blank">小米15</a>
                matches = re.findall(r'<a[^>]+href=[\'"]([^\'"]*(?:cell_phone|tablepc|smart_watch)[^\'"]*index(\d+)\.shtml)[\'"][^>]*>([^<]+)</a>', html)
                
                results = []
                seen_ids = set()
                
                for link, prod_id, title in matches:
                    title_clean = title.strip()
                    if prod_id not in seen_ids and len(title_clean) > 2 and "对比" not in title_clean and "评测" not in title_clean and "参数" not in title_clean:
                        seen_ids.add(prod_id)
                        cat = "cell_phone" if "cell_phone" in link else ("tablepc" if "tablepc" in link else "smart_watch")
                        results.append({
                            "id": prod_id,
                            "title": title_clean,
                            "category": cat,
                            "url": f"https://detail.zol.com.cn/{cat}/index{prod_id}.shtml",
                            "param_url": f"https://detail.zol.com.cn/{cat}/index{prod_id}/param.shtml",
                            "pic_url": f"https://detail.zol.com.cn/{cat}/index{prod_id}/pic.shtml"
                        })
                return results
        except Exception as e:
            print(f"⚠️ ZOL Search Error for {keyword}: {e}")
            return []

    def get_hardware_specs(self, param_url):
        """Scrape full detailed hardware specifications from ZOL param.shtml"""
        try:
            req = urllib.request.Request(param_url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                html = resp.read().decode("gbk", errors="ignore")
                
                specs = {}
                # Extract spec items from ZOL table
                # ZOL uses <th> (field name) and <td> (value)
                rows = re.findall(r'<th[^>]*>(.*?)</th>\s*<td[^>]*>(.*?)</td>', html, re.DOTALL)
                for th, td in rows:
                    clean_th = re.sub(r'<[^>]+>', '', th).strip()
                    clean_td = re.sub(r'<[^>]+>', '', td).strip()
                    clean_td = re.sub(r'\s+', ' ', clean_td)
                    if clean_th and clean_td and len(clean_th) < 30:
                        specs[clean_th] = clean_td
                        
                return specs
        except Exception as e:
            print(f"⚠️ ZOL Specs Error: {e}")
            return {}

    def get_high_res_images(self, pic_url):
        """Scrape studio official photos from ZOL pic.shtml"""
        try:
            req = urllib.request.Request(pic_url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                html = resp.read().decode("gbk", errors="ignore")
                raw_imgs = re.findall(r'src=[\'"](https?://[^\'"]+zol-img\.com\.cn/[^\'"]+)[\'"]', html)
                
                hd_imgs = []
                for img in raw_imgs:
                    if "/product/" in img or "/article/" in img:
                        # Upgrade to 800x600 HD
                        hd = re.sub(r'_\d+x\d+/', '_800x600/', img)
                        if hd not in hd_imgs:
                            hd_imgs.append(hd)
                return hd_imgs
        except Exception as e:
            print(f"⚠️ ZOL Images Error: {e}")
            return []

if __name__ == "__main__":
    zol = ZOLEngine()
    for test_device in ["小米15", "vivo X200", "华为Mate XT", "联想小新Pad Pro"]:
        print(f"\n🔍 Searching ZOL for: '{test_device}'...")
        results = zol.search_device(test_device)
        print(f"Found {len(results)} matches:")
        for r in results[:2]:
            print(f"  📌 [{r['id']}] {r['title']} ({r['category']})")
            print(f"     URL: {r['url']}")
            specs = zol.get_hardware_specs(r['param_url'])
            print(f"     Specs extracted: {len(specs)} fields")
            if specs:
                sample_keys = list(specs.keys())[:3]
                for k in sample_keys:
                    print(f"       • {k}: {specs[k]}")
