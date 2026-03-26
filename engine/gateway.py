from fastapi import FastAPI, Request, HTTPException, Header
from engine.controller import AetherController
import os
import hmac
import hashlib
import base64

app = FastAPI(title="Aether-Nexus-Commercial-Gateway")

# 初始化控制器
script_path = "/Users/yuhengluo/.openclaw/workspace/projects/Aether-Omni/engine/pipeline.py"
controller = AetherController(script_path)

# 获取 Webhook 密钥
WEBHOOK_SECRET = os.environ.get("SHOPIFY_WEBHOOK_SECRET")

def verify_shopify_hmac(data: bytes, hmac_header: str) -> bool:
    if not WEBHOOK_SECRET:
        return True # 如果没设 Secret，默认放行 (生产环境不推荐)
    
    computed_hmac = base64.b64encode(
        hmac.new(WEBHOOK_SECRET.encode('utf-8'), data, hashlib.sha256).digest()
    ).decode('utf-8')
    
    return hmac.compare_digest(computed_hmac, hmac_header)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/webhook/shopify")
async def handle_shopify_webhook(request: Request, x_shopify_hmac_sha256: str = Header(None)):
    # 读取原始数据
    data = await request.body()
    
    # 校验签名
    if not verify_shopify_hmac(data, x_shopify_hmac_sha256):
        raise HTTPException(status_code=401, detail="Invalid Shopify Signature")
    
    # 签名校验通过，处理请求
    print(f"[*] 收到真实 Shopify Webhook")
    
    # 触发自动处理流程
    success = controller.execute_with_healing()
    
    if success:
        return {"status": "success", "message": "Pipeline triggered"}
    else:
        return {"status": "error", "message": "Pipeline failed"}
