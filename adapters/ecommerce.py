from src.adapters.base import BaseServiceAdapter
from typing import Dict, Any

class ShopifyAdapter(BaseServiceAdapter):
    def __init__(self):
        super().__init__("shopify")
    
    def transform_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {"product": {"title": params.get("title"), "body_html": params.get("desc")}}

    def execute(self, params: Dict[str, Any]) -> Any:
        # 实际使用 self.api_key 和 self.secret
        print(f"[{self.service_id}] 使用 API Key: {self.api_key[:5]}... 调用 Shopify API")
        return {"status": "success", "shopify_id": "SHP-999"}

class TemuAdapter(BaseServiceAdapter):
    def __init__(self):
        super().__init__("temu")
    
    def transform_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {"goods_name": params.get("title"), "price": params.get("price")}

    def execute(self, params: Dict[str, Any]) -> Any:
        print(f"[{self.service_id}] 调用 Temu API")
        return {"status": "success", "temu_id": "TEMU-888"}

class WalmartAdapter(BaseServiceAdapter):
    def __init__(self):
        super().__init__("walmart")
    
    def transform_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {"itemName": params.get("title"), "price": params.get("price")}

    def execute(self, params: Dict[str, Any]) -> Any:
        print(f"[{self.service_id}] 调用 Walmart API")
        return {"status": "success", "walmart_id": "WMT-777"}
