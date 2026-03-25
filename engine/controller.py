import subprocess
import time
import os

class AetherController:
    def __init__(self, script_path):
        self.script_path = script_path
        self.max_retries = 3

    def execute_with_healing(self):
        attempt = 0
        while attempt < self.max_retries:
            print(f"[*] 启动智能体同步任务 (Attempt {attempt + 1})...")
            
            # 使用 subprocess 运行 Pipeline 并捕获输出
            result = subprocess.run(
                ["/Users/yuhengluo/.openclaw/workspace/projects/Aether-Omni/venv/bin/python3", self.script_path],
                capture_output=True, text=True
            )

            if result.returncode == 0:
                print("[+] 任务执行成功！")
                return True
            else:
                print(f"[!] 任务崩溃，捕获日志...")
                self._handle_error(result.stderr)
                attempt += 1
                time.sleep(5)
        
        print("[!] 任务重试次数耗尽，请人工审核。")
        return False

    def _handle_error(self, stderr):
        # 核心逻辑：将错误日志输出到指定位置供 Agent 读取和修复
        with open("/Users/yuhengluo/.openclaw/workspace/projects/Aether-Omni/engine/error.log", "a") as f:
            f.write(stderr)
        print("[+] 错误日志已记录，准备触发自愈流程。")

if __name__ == "__main__":
    controller = AetherController("/Users/yuhengluo/.openclaw/workspace/projects/Aether-Omni/engine/pipeline.py")
    controller.execute_with_healing()
