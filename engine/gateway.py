from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import HTMLResponse
from engine.controller import AetherController
from social_engine.visual_engine import VisualEngine
from social_engine.video_engine import VideoEngine
from core.event_bus import EventBus
from core.events import EventTypes
import os
import hmac
import hashlib
import base64
import asyncio
import functools

app = FastAPI(title="Aether-OS-Commercial-Gateway")

# 初始化控制器
script_path = "/Users/yuhengluo/.openclaw/workspace/projects/Aether-Omni/engine/pipeline.py"
controller = AetherController(script_path)
visual_engine = VisualEngine()
video_engine = VideoEngine()
event_bus = EventBus()

# 启动事件总线与桥接逻辑
@app.on_event("startup")
async def startup_event():
    # 1. 启动事件总线任务
    asyncio.create_task(event_bus.start())
    
    # 2. 桥接逻辑：将同步控制器封装为异步订阅者
    async def pipeline_subscriber(payload):
        loop = asyncio.get_event_loop()
        # 在线程池中执行阻塞的流水线任务，不阻塞总线循环
        await loop.run_in_executor(None, controller.execute_with_healing)
    
    # 3. 注册订阅者
    event_bus.subscribe(EventTypes.SHOPIFY_ORDER_CREATED, pipeline_subscriber)
    event_bus.subscribe(EventTypes.PAYMENT_SUCCEEDED, pipeline_subscriber)
    print("[*] Event Bus Subscribers Registered.")

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

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <script src="https://cdn.tailwindcss.com"></script>
        <title>Aether-Nexus | SaaS AI Gateway</title>
    </head>
    <body class="bg-gray-900 text-gray-100 min-h-screen">
        <div class="grid grid-cols-3 gap-4 p-6 h-screen">
            <!-- Instruction Panel -->
            <div class="bg-gray-800 p-4 rounded-lg shadow">
                <h2 class="text-xl font-bold mb-4">Intent Engine (Input)</h2>
                <textarea class="w-full h-32 bg-gray-700 text-white p-2 rounded" placeholder="Input AI Agent instructions..."></textarea>
                <button class="mt-2 bg-blue-600 hover:bg-blue-700 w-full py-2 rounded">Execute Intent</button>
            </div>
            <!-- Pipeline View -->
            <div class="bg-gray-800 p-4 rounded-lg shadow">
                <h2 class="text-xl font-bold mb-4">Pipeline View (Status)</h2>
                <div class="space-y-2 text-sm text-gray-400">
                    <p>Status: Running Pipeline #889</p>
                    <div class="w-full bg-gray-700 rounded-full h-2">
                        <div class="bg-blue-500 h-2 rounded-full w-3/4"></div>
                    </div>
                </div>
            </div>
            <!-- Physical Bridge Monitor -->
            <div class="bg-gray-800 p-4 rounded-lg shadow">
                <h2 class="text-xl font-bold mb-4">Physical Bridge (Monitor)</h2>
                <div class="space-y-2">
                    <p class="text-green-500">Flipper Zero: Connected</p>
                    <p class="text-green-500">XLeRobot: Active</p>
                    <p class="text-yellow-500">RPi Node: Latency 23ms</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

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
    
    await event_bus.publish(EventTypes.SHOPIFY_ORDER_CREATED, {"data": data})
    return {"status": "success"}

@app.post("/webhook/airwallex")
async def handle_airwallex_webhook(request: Request, x_signature: str = Header(None), x_timestamp: str = Header(None)):
    data = await request.body()
    if not verify_airwallex_hmac(data, x_timestamp, x_signature):
        raise HTTPException(status_code=401, detail="Invalid Airwallex Signature")
    
    await event_bus.publish(EventTypes.PAYMENT_SUCCEEDED, {"data": data})
    return {"status": "success"}
