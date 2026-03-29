from langchain_core.prompts import PromptTemplate
from trading_engine.llm_trading_adapter import LLMTradingAdapter

class ContentGenerator:
    def __init__(self):
        self.llm = LLMTradingAdapter(model_name='deepseek-reasoner')
        self.brand_context = """
        你现在是 Aether-Engine 的品牌内容官。
        品牌调性：极简、高雅、轻奢、以匠心工艺为核心。
        目标受众：追求生活品质的现代都市女性。
        禁止词汇：低俗促销、过度营销感、粗暴降价。
        """

    def generate_copy(self, product_title, product_desc, platform="小红书"):
        prompt = f"""
        {self.brand_context}
        请为以下商品生成一段针对 {platform} 的发布文案：
        商品名称: {product_title}
        描述: {product_desc}
        要求: 文案必须包含 3-5 个符合AirArtshop调性的标签，语气需体现轻奢感。
        """
        return self.llm.execute({'prompt': prompt})

    def generate_visual_prompt(self, product_title):
        # 生成 Stable Diffusion 绘画提示词
        return f"AirArtshop brand style product photography, {product_title}, soft lighting, minimalistic studio background, 8k resolution"
