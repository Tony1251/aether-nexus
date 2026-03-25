import requests
import time
import jwt
import json
import os
from typing import Dict, Any, List
from dotenv import load_dotenv

# 加载环境变量
load_dotenv(dotenv_path="/Users/yuhengluo/.openclaw/workspace/projects/Aether-Omni/.env")

class AoXiaKeywordAdapter:
    def __init__(self):
        self.access_key = os.getenv("ALPHASHOP_ACCESS_KEY")
        self.secret_key = os.getenv("ALPHASHOP_SECRET_KEY")
        self.api_url = "https://api.alphashop.cn/opp.selection.keyword.search/1.0"

    def _get_jwt_token(self) -> str:
        current_time = int(time.time())
        payload = {
            "iss": self.access_key,
            "exp": current_time + 1800,
            "nbf": current_time - 5
        }
        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        return token if isinstance(token, str) else token.decode("utf-8")

    def execute(self, params: Dict[str, Any]) -> Any:
        platform = params.get("platform", "amazon")
        payload = {
            "platform": platform,
            "region": params.get("region", "US"),
            "keyword": params.get("keyword", "yoga pants")
        }
        
        token = self._get_jwt_token()
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
        
        try:
            response = requests.post(self.api_url, json=payload, headers=headers)
            if response.status_code == 200:
                return self._parse_response(response.json(), platform)
            else:
                return {"status": "error", "message": response.text}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _parse_response(self, data: Dict[str, Any], platform: str) -> List[Dict[str, Any]]:
        """多态解析：自动区分 Amazon 和 TikTok 数据结构"""
        items = []
        if platform.lower() == 'amazon':
            # Amazon path: result.data.keywordList
            items = data.get('result', {}).get('data', {}).get('keywordList', [])
        else:
            # TikTok path: data
            items = data.get('data', [])
            
        # 统一输出结构
        standardized_items = []
        for item in items:
            radar = item.get('radar', {}).get('propertyList', [])
            # 补全缺失维度 (如TikTok缺少市场需求分)
            radar_dict = {r['name']: r['value'] for r in radar}
            radar_dict.setdefault('市场需求分', 'N/A')
            
            standardized_items.append({
                "keyword": item.get('keyword'),
                "keywordCn": item.get('keywordCn'),
                "oppScore": item.get('oppScore'),
                "radar": radar_dict,
                "sales": item.get('salesInfo', {}).get('soldCnt30d', {}).get('value', '0')
            })
        return standardized_items
