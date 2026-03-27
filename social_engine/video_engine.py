import os
import asyncio
from pathlib import Path
import sys

# 将 submodule 路径加入 sys.path 以便导入
sys.path.append(os.path.join(os.path.dirname(__file__), "moneyprinter_core"))

# 导入 MoneyPrinter 的核心流水线
# 假设 Backend.pipeline 中有可以运行的入口函数或类
from Backend.pipeline import VideoGenerator # 这是一个假设的导入路径，可能需要根据具体源码调整

class VideoEngine:
    def __init__(self):
        self.work_dir = Path("/app/social_engine/temp")
        self.work_dir.mkdir(exist_ok=True)
        self.generator = VideoGenerator()

    async def generate_short_video(self, script_text, output_filename):
        """
        调用 MoneyPrinter 核心引擎渲染视频
        """
        output_path = self.work_dir / f"{output_filename}.mp4"
        
        # 运行核心渲染流水线
        # 根据 MoneyPrinter 源码，这通常是同步调用，建议在子线程中运行以避免阻塞 FastAPI 循环
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.generator.run, script_text, str(output_path))
        
        return str(output_path)
