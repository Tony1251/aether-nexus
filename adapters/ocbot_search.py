from src.adapters.base import BaseServiceAdapter
import asyncio
import json
import requests
from typing import Dict, Any

class OCBotSearchAdapter(BaseServiceAdapter):
    def __init__(self):
        super().__init__("ocbot_search")
        # 直接使用本地桥梁与 OCBot 通信
        from src.ocbot_bridge import OCBotBridge
        self.bridge = OCBotBridge()

    def transform_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {"query": params.get("query")}

    def execute(self, params: Dict[str, Any]) -> Any:
        query = params.get("query")
        print(f"[{self.service_id}] 通过 OCBot 执行搜索: {query}")
        
        # 定义搜索流程指令序列
        # 1. 导航至 Google
        # 2. 输入查询并回车
        # 3. 等待并提取结果
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # 发送一系列操作指令到 OCBot
        # 这里简化为直接调用搜索接口（假设 OCBot 提供了搜索 action）
        result = loop.run_until_complete(self.bridge.send_command("search", {"query": query}))
        
        return result
