#!/bin/sh
exec python3 -m uvicorn engine.gateway:app --host 0.0.0.0 --port 8080
