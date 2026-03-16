# Build from repo root: docker build -f src/data_load/Dockerfile .
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

ENV PYTHONPATH=/app
ENV PYTHONUTF8=1
ENV OUTPUT_PATH=/app/data/raw/petitions.csv
ENV DB_PATH=/app/data/petitions.db

EXPOSE 8000

# FastAPI server by default; override CMD for CLI mode
# CLI:  docker run --rm -v $(pwd)/data:/app/data <image> python -m src.data_load.data_load
# API:  docker run --rm -p 8000:8000 -v $(pwd)/data:/app/data <image>
CMD ["uvicorn", "src.data_load.app:app", "--host", "0.0.0.0", "--port", "8000"]
