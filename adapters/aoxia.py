import os
import requests
import time
import jwt
import json
from typing import Dict, Any
from dotenv import load_dotenv

# 加载环境变量
load_dotenv(dotenv_path="/Users/yuhengluo/.openclaw/workspace/projects/Aether-Omni/.env")

class AoXiaAdapter:
    def __init__(self, endpoint_suffix="ai.sel.global1688.image.opp.analyze/1.0"):
        # 使用 AlphaShop API 凭证
        self.access_key = os.getenv("ALPHASHOP_ACCESS_KEY")
        self.secret_key = os.getenv("ALPHASHOP_SECRET_KEY")
        self.base_url = "https://api.alphashop.cn"
        self.api_url = f"{self.base_url}/{endpoint_suffix}"

    def set_endpoint(self, endpoint_suffix):
        self.api_url = f"{self.base_url}/{endpoint_suffix}"

    def _get_jwt_token(self) -> str:
        """生成 JWT token 用于 AlphaShop API 认证"""
        current_time = int(time.time())
        payload = {
            "iss": self.access_key,
            "exp": current_time + 1800,
            "nbf": current_time - 5
        }
        # 使用 secret_key，算法 HS256
        token = jwt.encode(
            payload=payload,
            key=self.secret_key,
            algorithm="HS256",
            headers={"alg": "HS256"}
        )
        # jwt.encode 在较新版本中直接返回字符串
        if isinstance(token, bytes):
            token = token.decode("utf-8")
        return token

    def execute(self, params: Dict[str, Any]) -> Any:
        print(f"[AoXiaAPI] 正在通过 AlphaShop API 请求真实数据...")
        
        # 构造请求参数
        payload = {
            "userId": "0" 
        }
        # Update to generic payload update based on input params
        payload.update(params)
        
        print(f"[AoXiaAPI] Request Payload: {json.dumps(payload)}")
        
        # Get JWT Token
        token = self._get_jwt_token()
        
        try:
            # 执行生产级 HTTP 请求
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
            response = requests.post(self.api_url, json=payload, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                print(f"[AoXiaAPI] 响应成功: {data}")
                return data
            else:
                print(f"[AoXiaAPI] 请求失败: {response.status_code}, {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            print(f"[AoXiaAPI] 请求异常: {e}")
            return {"status": "error", "message": str(e)}
