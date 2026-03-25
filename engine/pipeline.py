import time
import base64
import requests
from adapters.aoxia import AoXiaAdapter
from engine.shopify import ShopifyManager

class ProductionPipeline:
    def __init__(self):
        self.aoxia = AoXiaAdapter()
        self.shopify = ShopifyManager()
        self.aoxia.set_endpoint("opp.selection.newproduct.report/1.0")

    def run(self, keyword, limit=10):
        print(f"[*] 启动 Nexus-Core 稳健同步引擎: {keyword}...")
        
        # 1. Idempotency Check
        existing_products = {p['title']: p['id'] for p in self.shopify.get_products()}
        
        # 2. Fetch
        report_data = self.aoxia.execute({
            "productKeyword": keyword,
            "targetCountry": "US",
            "targetPlatform": "amazon",
            "userId": "0"
        })
        
        if not report_data or 'result' not in report_data:
            print("[!] 数据获取异常")
            return
            
        products = report_data.get('result', {}).get('data', {}).get('productList', [])
        
        # 3. Process
        for item in products[:limit]:
            title = item.get('title', 'Unknown')
            if title in existing_products:
                print(f"[-] 跳过已存在: {title}")
                continue
                
            img_url = item.get('mainImgUrl')
            price = item.get('priceRange', '19.99').split('~')[0].replace('$', '').strip()
            
            payload = {
                "title": title,
                "body_html": "<p>Premium jewelry, carefully selected.</p>",
                "vendor": "AirArtshop",
                "status": "active",
                "variants": [{"price": price}]
            }
            
            res = self.shopify.create_product(payload)
            if res and 'product' in res:
                pid = res['product']['id']
                print(f"[+] 创建成功: {title} (ID: {pid})")
                
                # Image Sync
                if img_url:
                    try:
                        img_data = requests.get(img_url).content
                        encoded = base64.b64encode(img_data).decode('utf-8')
                        self.shopify.upload_image(pid, encoded)
                        print(f"    -> 图片挂载成功")
                    except Exception as e:
                        print(f"    -> [!] 图片挂载失败: {e}")
            
            time.sleep(3)
