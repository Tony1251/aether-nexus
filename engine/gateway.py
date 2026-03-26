from fastapi import FastAPI, Request
from engine.controller import AetherController
import os

app = FastAPI(title="Aether-Nexus-Commercial-Gateway")

# 初始化控制器 (假设 script_path 依然可用)
script_path = "/Users/yuhengluo/.openclaw/workspace/projects/Aether-Omni/engine/pipeline.py"
controller = AetherController(script_path)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/webhook/shopify")
async def handle_shopify_webhook(request: Request):
    # 接收 Shopify 支付/订单状态更新
    data = await request.json()
    print(f"[*] 收到 Shopify Webhook: {data}")
    
    # 触发自动处理流程
    success = controller.execute_with_healing()
    
    if success:
        return {"status": "success", "message": "Pipeline triggered"}
    else:
        return {"status": "error", "message": "Pipeline failed"}
