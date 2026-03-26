import subprocess
import time
import os
import sys

class AetherController:
    def __init__(self, script_path):
        self.script_path = script_path
        self.max_retries = 3

    def execute_with_healing(self):
        attempt = 0
        while attempt < self.max_retries:
            print(f"[*] 启动智能体同步任务 (Attempt {attempt + 1})...")
            
            # 使用 sys.executable 确保使用当前的容器 Python 解释器
            result = subprocess.run(
                [sys.executable, self.script_path],
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
        print(f"[!!!] 捕获到流水线错误详情: {stderr}") # 新增：强制打印到控制台
        error_log_path = os.path.join(os.path.dirname(__file__), "error.log")
        with open(error_log_path, "a") as f:
            f.write(stderr)
        print("[+] 错误日志已记录，准备触发自愈流程。")

if __name__ == "__main__":
    # 使用相对于项目根目录的路径
    controller = AetherController("production_pipeline.py")
    controller.execute_with_healing()
