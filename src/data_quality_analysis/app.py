from fastapi import FastAPI, HTTPException

from src.data_quality_analysis.service import RAW_PATH, full_quality_analysis

app = FastAPI(title="data_quality_analysis API", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/quality")
def quality():
    if not RAW_PATH.exists():
        raise HTTPException(status_code=404, detail=f"CSV not found at {RAW_PATH}")
    return full_quality_analysis(RAW_PATH)
