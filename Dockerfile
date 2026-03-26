FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
# 强制升级 pip 并安装依赖
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
# 修正：使用 uvicorn 直接启动，并绑定端口 8080
CMD ["python3", "-m", "uvicorn", "engine.gateway:app", "--host", "0.0.0.0", "--port", "8080"]
