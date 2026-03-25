from src.adapters.base import BaseServiceAdapter
from src.ocbot_bridge import OCBotBridge
import asyncio
from typing import Dict, Any

class PddListingAdapter(BaseServiceAdapter):
    def __init__(self):
        super().__init__("pdd_listing")
        self.bridge = OCBotBridge()

    def transform_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return params

    def execute(self, params: Dict[str, Any]) -> Any:
        print(f"[{self.service_id}] 启动上架流程，传入数据: {params.get('name')}")
        # 通过桥梁驱动 OCBot 执行填表操作
        # 假设 OCBot 已由用户手动导航至 PDD 商品发布页
        result = asyncio.run(self.bridge.send_command("fill_pdd_listing", params))
        return result
