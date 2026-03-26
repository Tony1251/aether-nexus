import os
import time
import base64
import requests
from dotenv import load_dotenv
from adapters.aoxia import AoXiaAdapter
from shopify_helper import ShopifyHelper

# Load env
load_dotenv(dotenv_path="/Users/yuhengluo/.openclaw/workspace/projects/Aether-Omni/.env")

class ProductionPipeline:
    def __init__(self):
        self.aoxia = AoXiaAdapter()
        self.shopify = ShopifyHelper()

    def run(self, keyword="sterling silver earrings", limit=10):
        print(f"[*] 启动已验证稳健流水线 (关键词: {keyword})...")
        
        # 1. Get existing to avoid duplicates
        existing_products = {p['title']: p['id'] for p in self.shopify.get_all_products()}
        
        # 2. Search Products
        self.aoxia.set_endpoint("opp.selection.newproduct.report/1.0")
        report_data = self.aoxia.execute({
            "productKeyword": keyword,
            "targetCountry": "US",
            "targetPlatform": "amazon",
            "userId": "0"
        })
        
        if report_data is None: return
            
        products = report_data.get('result', {}).get('data', {}).get('productList', [])
        
        # 3. Process products
        count = 0
        for item in products:
            if count >= limit: break
            
            title = item.get('title', 'Unknown Product')
            img_url = item.get('mainImgUrl')
            price = item.get('priceRange', '19.99').split('~')[0].replace('$', '').strip()
            
            # Skip if exists
            if title in existing_products:
                print(f"[-] 跳过: {title}")
                continue
                
            print(f"[*] 创建: {title}")
            payload = {
                "title": title,
                "body_html": "<p>High-quality silver earrings, perfect for everyday wear.</p>",
                "vendor": "AirArtshop",
                "status": "active",
                "variants": [{"price": price}]
            }
            
            res = self.shopify.create_product(payload)
            if res and 'product' in res:
                pid = res['product']['id']
                if img_url:
                    img_data = requests.get(img_url).content
                    encoded = base64.b64encode(img_data).decode('utf-8')
                    self.shopify.upload_product_image(pid, encoded)
                count += 1
                print(f"[+] 成功: {title} (ID: {pid})")
            
            time.sleep(3) # Rate limit

if __name__ == "__main__":
    pipeline = ProductionPipeline()
    pipeline.run("sterling silver earrings", limit=10)
