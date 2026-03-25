import torch
from diffusers import StableDiffusionXLPipeline
from typing import Dict, Any

class ImageGenerationAdapter:
    def __init__(self, model_id="stabilityai/stable-diffusion-xl-base-1.0"):
        print(f"[*] 正在初始化图像生成模型: {model_id}...")
        self.pipe = StableDiffusionXLPipeline.from_pretrained(
            model_id, 
            torch_dtype=torch.float16, 
            use_safetensors=True
        )
        # 将模型移动到 MPS (Apple Silicon GPU)
        self.device = "mps" if torch.backends.mps.is_available() else "cpu"
        self.pipe.to(self.device)
        print(f"[+] 模型已加载至 {self.device}")

    def generate(self, prompt: str, output_path: str):
        print(f"[*] 正在生成图像: {prompt}")
        image = self.pipe(prompt=prompt).images[0]
        image.save(output_path)
        print(f"[+] 图像已保存至: {output_path}")
        return output_path

    def execute(self, params: Dict[str, Any]) -> Any:
        prompt = params.get("prompt")
        output_path = params.get("output_path", "output.png")
        return self.generate(prompt, output_path)
