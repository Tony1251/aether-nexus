import requests
import os
import time
from dotenv import load_dotenv

class ShopifyHelper:
    def __init__(self):
        load_dotenv(dotenv_path="/Users/yuhengluo/.openclaw/workspace/projects/Aether-Omni/.env")
        self.token = os.getenv("SHOPIFY_ACCESS_TOKEN")
        self.shop_name = "ygxne3-5b"
        self.base_url = f"https://{self.shop_name}.myshopify.com/admin/api/2024-04"
        self.headers = {"X-Shopify-Access-Token": self.token, "Content-Type": "application/json"}

    def _request_with_retry(self, method, endpoint, payload=None, retries=5):
        url = f"{self.base_url}/{endpoint}"
        for i in range(retries):
            try:
                response = requests.request(method, url, headers=self.headers, json=payload)
                
                # 智能限流：读取 Shopify 限流 Header
                limit_header = response.headers.get("X-Shopify-Shop-Api-Call-Limit")
                if limit_header:
                    used, total = map(int, limit_header.split('/'))
                    if used >= total * 0.8:
                        print(f"[*] API 高水位 ({used}/{total})，正在自适应降速...")
                        time.sleep(2)
                
                if response.status_code in [200, 201]:
                    return response.json()
                elif response.status_code == 429:
                    # 遭遇限流，强制休眠更久
                    print(f"[!] 触发 API 限流，休眠重试...")
                    time.sleep(10)
                    continue
                else:
                    print(f"[!] API Error ({response.status_code}): {response.text}")
                    return None
            except Exception as e:
                print(f"[!] Request Error: {e}")
                time.sleep(2)
        return None

    def create_product(self, payload):
        return self._request_with_retry("POST", "products.json", payload={"product": payload})

    def get_all_products(self):
        # Shopify API defaults to 50 items per page, need to handle pagination if > 50.
        # Simple for now, but safer.
        response = self._request_with_retry("GET", "products.json?limit=250")
        return response.get('products', []) if response else []

    def update_product(self, product_id, payload):
        return self._request_with_retry("PUT", f"products/{product_id}.json", payload={"product": payload})

    def upload_product_image(self, product_id, encoded_image):
        return self._request_with_retry("POST", f"products/{product_id}/images.json", 
                                        payload={"image": {"attachment": encoded_image}})
