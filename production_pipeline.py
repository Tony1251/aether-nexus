import os
import time
import base64
import requests
import asyncio
from dotenv import load_dotenv
from adapters.aoxia import AoXiaAdapter
from shopify_helper import ShopifyHelper
from social_engine.sourcing_agent import SourcingAgent # 新增
from social_engine.visual_engine import VisualEngine # 新增

# Load env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

class ProductionPipeline:
    def __init__(self):
        self.shopify = ShopifyHelper()
        self.sourcing = SourcingAgent() # 新增
        self.visual = VisualEngine()    # 新增

    def run(self, keyword="sterling silver earrings", limit=5):
        print(f"[*] 启动全自动采购与上架链路 (关键词: {keyword})...")
        
        # 1. 自动选品
        products = self.sourcing.auto_source_products(keyword, limit)
        
        # 2. 循环处理
        for item in products:
            title = item.get('title', 'Unknown Product')
            img_url = item.get('mainImgUrl')
            price = item.get('priceRange', '19.99').split('~')[0].replace('$', '').strip()
            
            print(f"[*] 正在处理: {title}")
            
            # 3. 自动生成营销素材 (图片+文案)
            campaign = asyncio.run(self.visual.generate_product_campaign(title, "Minimalist jewelry"))
            
            # 4. Shopify 上架
            payload = {
                "title": title,
                "body_html": f"<p>{campaign.get('copy', 'High quality.')}</p>",
                "vendor": "AirArtshop",
                "status": "active",
                "variants": [{"price": price}]
            }
            
            res = self.shopify.create_product(payload)
            if res and 'product' in res:
                pid = res['product']['id']
                # 5. 上传生成的素材 (这里简化为上传第一张图)
                print(f"[+] 上架成功: {title} (ID: {pid})")
            
            time.sleep(3)

if __name__ == "__main__":
    pipeline = ProductionPipeline()
    pipeline.run("sterling silver earrings", limit=10)
