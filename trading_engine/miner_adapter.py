import json
from src.adapters.base import BaseServiceAdapter
from typing import Dict, Any

class MinerAdapter(BaseServiceAdapter):
    def __init__(self):
        super().__init__("miner_status")
        self.status_path = '/Users/yuhengluo/.openclaw/workspace/projects/strategy_vault/miner_status.json'

    def transform_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {}

    def execute(self, params: Dict[str, Any]) -> Any:
        try:
            with open(self.status_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"error": "Miner status not available yet"}
        except Exception as e:
            return {"error": str(e)}
