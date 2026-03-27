from fastapi import FastAPI, Request, HTTPException, Header
from engine.controller import AetherController
from social_engine.visual_engine import VisualEngine
from social_engine.video_engine import VideoEngine
import os
import hmac
import hashlib
import base64
import time

app = FastAPI(title="Aether-Nexus-Commercial-Gateway")

# 初始化控制器
script_path = "/Users/yuhengluo/.openclaw/workspace/projects/Aether-Omni/engine/pipeline.py"
controller = AetherController(script_path)
visual_engine = VisualEngine()
video_engine = VideoEngine()

# 获取 Webhook 密钥
SHOPIFY_SECRET = os.environ.get("SHOPIFY_WEBHOOK_SECRET")
AIRWALLEX_SECRET = os.environ.get("AIRWALLEX_WEBHOOK_SECRET")

def verify_shopify_hmac(data: bytes, hmac_header: str) -> bool:
    if not SHOPIFY_SECRET: return True
    computed_hmac = base64.b64encode(
        hmac.new(SHOPIFY_SECRET.encode('utf-8'), data, hashlib.sha256).digest()
    ).decode('utf-8')
    return hmac.compare_digest(computed_hmac, hmac_header)

def verify_airwallex_hmac(data: bytes, timestamp: str, signature: str) -> bool:
    if not AIRWALLEX_SECRET: return True
    payload = timestamp + data.decode('utf-8')
    computed_hmac = hmac.new(AIRWALLEX_SECRET.encode('utf-8'), payload.encode('utf-8'), hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed_hmac, signature)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/api/social/generate-campaign")
async def generate_campaign(product_title: str, product_desc: str):
    campaign = await visual_engine.generate_product_campaign(product_title, product_desc)
    return {"status": "success", "data": campaign}

@app.post("/api/social/generate-video")
async def generate_video(script_text: str, output_filename: str):
    video_url = await video_engine.generate_short_video(script_text, output_filename)
    return {"status": "success", "video_url": video_url}

@app.post("/webhook/shopify")
async def handle_shopify_webhook(request: Request, x_shopify_hmac_sha256: str = Header(None)):
    data = await request.body()
    if not verify_shopify_hmac(data, x_shopify_hmac_sha256):
        raise HTTPException(status_code=401, detail="Invalid Shopify Signature")
    
    controller.execute_with_healing()
    return {"status": "success"}

@app.post("/webhook/airwallex")
async def handle_airwallex_webhook(request: Request, x_signature: str = Header(None), x_timestamp: str = Header(None)):
    data = await request.body()
    if not verify_airwallex_hmac(data, x_timestamp, x_signature):
        raise HTTPException(status_code=401, detail="Invalid Airwallex Signature")
    
    controller.execute_with_healing()
    return {"status": "success"}
