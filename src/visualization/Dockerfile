# Build from repo root: docker build -f src/visualization/Dockerfile .
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

ENV PYTHONPATH=/app
ENV PYTHONUTF8=1
ENV DATA_RAW_PATH=/app/data/raw/petitions.csv
ENV REPORTS_FIGURES_PATH=/app/reports/figures

EXPOSE 8000

# API:  docker run --rm -p 8000:8000 -v $(pwd)/data:/app/data -v $(pwd)/reports:/app/reports <image>
# CLI:  docker run --rm -v $(pwd)/data:/app/data -v $(pwd)/reports:/app/reports <image> python -m src.visualization.visualization
CMD ["uvicorn", "src.visualization.app:app", "--host", "0.0.0.0", "--port", "8000"]
