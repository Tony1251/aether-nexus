import os
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseServiceAdapter(ABC):
    """
    所有 Aether-Nexus 服务适配器的基类。
    """
    def __init__(self, service_id: str):
        self.service_id = service_id
        # 初始化时不查询 DB，避免上下文问题
        self.api_key = None
        self.secret = None

    def refresh_config(self):
        """在 Flask 上下文中显式调用此方法刷新配置"""
        from src.models import ChannelConfig
        config = ChannelConfig.query.filter_by(service_id=self.service_id).first()
        if config:
            self.api_key = config.api_key
            self.secret = config.secret
        else:
            self.api_key = os.environ.get(f"{self.service_id.upper()}_API_KEY")
            self.secret = os.environ.get(f"{self.service_id.upper()}_SECRET")
        
        if not self.api_key:
            print(f"Warning: 服务 {self.service_id} 缺少凭证")

    @abstractmethod
    def transform_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """将 Agent 的通用参数转化为该特定产品 API 的格式"""
        pass

    @abstractmethod
    def execute(self, params: Dict[str, Any]) -> Any:
        """执行该产品的具体 API 调用逻辑"""
        pass

# 示例：Google Search 适配器实现
class GoogleSearchAdapter(BaseServiceAdapter):
    def __init__(self):
        super().__init__("google_search")

    def transform_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {"q": params.get("query"), "num": params.get("limit", 10)}

    def execute(self, params: Dict[str, Any]) -> Any:
        transformed = self.transform_params(params)
        print(f"[{self.service_id}] 调用接口: key={self.api_key[:5]}..., params={transformed}")
        # 在此处接入 requests.get(...)
        return {"results": ["样本结果1", "样本结果2"]}
