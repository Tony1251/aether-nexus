from adapters.base import BaseServiceAdapter
from ocbot_bridge import OCBotBridge
import asyncio
from typing import Dict, Any

class PddListingAdapter(BaseServiceAdapter):
    def __init__(self):
        super().__init__("pdd_listing")
        self.bridge = OCBotBridge()

    def transform_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return params

    def execute(self, params: Dict[str, Any]) -> Any:
        print(f"[{self.service_id}] 启动全自动上架流程...")
        # 调用 OCBot 执行原子操作序列
        # 注意：此处必须在运行中环境中处理 asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(self.bridge.send_command("fill_pdd_listing", params))
        return result
