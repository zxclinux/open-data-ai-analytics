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

CMD ["uvicorn", "src.data_load.app:app", "--host", "0.0.0.0", "--port", "8000"]
