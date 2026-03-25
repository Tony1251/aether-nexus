from src.adapters.base import BaseServiceAdapter
from exa_py import Exa
from typing import Dict, Any

class ExaSearchAdapter(BaseServiceAdapter):
    def __init__(self):
        super().__init__("exa_search")
        self.client = Exa(api_key=self.api_key)

    def transform_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "query": params.get("query"),
            "num_results": params.get("limit", 5),
            "type": "neural"
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        query_params = self.transform_params(params)
        print(f"[{self.service_id}] 调用 Exa API: {query_params['query']}")
        response = self.client.search(
            query_params['query'],
            num_results=query_params['num_results'],
            type=query_params['type']
        )
        # 序列化结果返回
        return [r.model_dump() for r in response.results]
