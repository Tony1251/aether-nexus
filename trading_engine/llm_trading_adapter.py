from typing import Dict, Any, List
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv(dotenv_path="/Users/yuhengluo/.openclaw/workspace/projects/Aether-Omni/.env")

class LLMSignalAnalyzer:
    def __init__(self, model_name: str = "deepseek-reasoner"):
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )
        self.model = model_name

    def analyze_market_data(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        核心逻辑：将市场数据 (K线/因子) 传给 LLM，让其返回交易信号
        """
        prompt = f"""
        你是一位专业的量化交易员。请分析以下市场数据并给出交易决策：
        数据摘要: {json.dumps(market_data)}
        
        要求返回 JSON 格式：
        {{
            "signal": "buy/sell/hold",
            "confidence": 0.0-1.0,
            "reasoning": "分析逻辑"
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                stream=False
            )
            content = response.choices[0].message.content
            # 简单清洗 markdown 格式
            return json.loads(content.replace("```json", "").replace("```", "").strip())
        except Exception as e:
            return {"signal": "hold", "confidence": 0, "reasoning": f"分析出错: {str(e)}"}

# 封装为适配器格式，便于集成进交易流水线
class LLMTradingAdapter:
    def __init__(self, model_name: str = "deepseek-reasoner"):
        self.analyzer = LLMSignalAnalyzer(model_name=model_name)

    def execute(self, params: Dict[str, Any]) -> Any:
        # params 应包含当前的 market_data
        market_data = params.get("market_data", {})
        return self.analyzer.analyze_market_data(market_data)
