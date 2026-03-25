import requests
import os
import time
from dotenv import load_dotenv

class ShopifyManager:
    def __init__(self):
        load_dotenv(dotenv_path="/Users/yuhengluo/.openclaw/workspace/projects/Aether-Omni/.env")
        self.token = os.getenv("SHOPIFY_ACCESS_TOKEN")
        self.shop_name = "ygxne3-5b"
        self.base_url = f"https://{self.shop_name}.myshopify.com/admin/api/2024-04"
        self.headers = {"X-Shopify-Access-Token": self.token, "Content-Type": "application/json"}

    def _request(self, method, endpoint, payload=None):
        url = f"{self.base_url}/{endpoint}"
        for _ in range(5): # 5 retries
            try:
                response = requests.request(method, url, headers=self.headers, json=payload)
                limit_header = response.headers.get("X-Shopify-Shop-Api-Call-Limit")
                if limit_header:
                    used, total = map(int, limit_header.split('/'))
                    if used >= total * 0.8: time.sleep(2)
                
                if response.status_code in [200, 201]: return response.json()
                elif response.status_code == 429: time.sleep(10)
                else: return None
            except: time.sleep(2)
        return None

    def get_products(self): return self._request("GET", "products.json?limit=250").get('products', [])
    def create_product(self, payload): return self._request("POST", "products.json", payload={"product": payload})
    def upload_image(self, pid, encoded): return self._request("POST", f"products/{pid}/images.json", payload={"image": {"attachment": encoded}})
