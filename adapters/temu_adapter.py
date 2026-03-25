from adapters.base import BaseServiceAdapter
from ocbot_bridge import OCBotBridge
import asyncio
from typing import Dict, Any

class TemuListingAdapter(BaseServiceAdapter):
    def __init__(self):
        super().__init__("temu_listing")
        self.bridge = OCBotBridge()

    def transform_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "title": params.get("title"),
            "price": params.get("price"),
            "images": params.get("image_urls", [])
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        print(f"[{self.service_id}] 启动 Temu 自动化上架流程...")
        # 驱动 OCBot 执行上架动作
        # 假设用户已手动导航至 Temu 发布页
        result = asyncio.run(self.bridge.send_command("fill_temu_listing", params))
        return result
