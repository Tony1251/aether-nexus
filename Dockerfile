FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONPATH=/app
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
