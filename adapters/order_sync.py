from src.adapters.base import BaseServiceAdapter
from typing import Dict, Any
import json
import os

class OrderSyncAdapter(BaseServiceAdapter):
    """
    订单同步适配器：连接 Merchant 系统与 Nexus 网关。
    """
    def __init__(self):
        super().__init__("order_sync")
        self.db_path = '/Users/yuhengluo/.openclaw/workspace/projects/Aether-Nexus/data/orders.json'

    def transform_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return params

    def execute(self, params: Dict[str, Any]) -> Any:
        # 将传入的订单数据存入本地 JSON 仓库
        order_data = params.get("order")
        if not order_data:
            return {"status": "error", "message": "No order data provided"}
        
        # 追加写入模拟持久化
        orders = []
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f:
                try:
                    orders = json.load(f)
                except:
                    orders = []
        
        orders.append(order_data)
        
        with open(self.db_path, 'w') as f:
            json.dump(orders, f, indent=2)
            
        print(f"[{self.service_id}] 订单已同步，订单号: {order_data.get('order_id')}")
        return {"status": "success", "order_id": order_data.get('order_id')}
