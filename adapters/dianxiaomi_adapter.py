import requests
import json
import time
import hmac
import hashlib

class DianXiaoMiAdapter:
    def __init__(self, app_key: str, app_secret: str, member_id: str):
        self.app_key = app_key
        self.app_secret = app_secret
        self.member_id = member_id
        self.base_url = "https://openapi.dianxiaomi.com/router/api"

    def _generate_sign(self, params: dict) -> str:
        # 店小秘签名逻辑：参数按 key 排序，拼接 Secret，再进行 md5
        keys = sorted(params.keys())
        string_to_sign = ""
        for key in keys:
            if params[key] is not None:
                string_to_sign += f"{key}{params[key]}"
        string_to_sign += self.app_secret
        return hashlib.md5(string_to_sign.encode('utf-8')).hexdigest()

    def publish_product(self, product_data: dict):
        """
        发布商品至店小秘
        product_data 格式: {'title': ..., 'desc': ..., 'price': ..., 'images': [...]}
        """
        params = {
            "appKey": self.app_key,
            "memberId": self.member_id,
            "timestamp": int(time.time()),
            "title": product_data.get("title"),
            "price": product_data.get("price"),
            "description": product_data.get("desc"),
            # 简化版：仅上传主图
            "mainImage": product_data.get("images", [None])[0]
        }
        
        params["sign"] = self._generate_sign(params)
        
        # 实际调用时请替换为真实的接口方法名
        # params["method"] = "dianxiaomi.product.publish"
        
        print(f"[DianXiaoMi] 正在发布商品: {params['title']}")
        # response = requests.post(self.base_url, data=params)
        # return response.json()
        
        # 模拟发布成功
        return {"status": "success", "message": "Product published successfully"}
