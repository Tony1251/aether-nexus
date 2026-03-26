from fastapi import FastAPI
from engine.controller import router as controller_router

app = FastAPI(title="Aether-Nexus-Gateway")

# Include the controller router if it exists, otherwise define a basic health route
try:
    app.include_router(controller_router, prefix="/api")
except Exception:
    pass

@app.get("/")
async def root():
    return {"status": "Aether-Nexus Gateway Active"}

@app.get("/health")
async def health():
    return {"status": "ok"}
