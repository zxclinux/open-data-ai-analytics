FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

ENV PYTHONPATH=/app
ENV PYTHONUTF8=1
ENV DB_PATH=/app/data/petitions.db
ENV DATA_LOAD_URL=http://data-load:8000
ENV QUALITY_URL=http://data-quality:8000
ENV RESEARCH_URL=http://data-research:8000
ENV VIZ_URL=http://visualization:8000

EXPOSE 8000

CMD ["uvicorn", "src.web.app:app", "--host", "0.0.0.0", "--port", "8000"]
