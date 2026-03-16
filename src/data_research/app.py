from fastapi import FastAPI, HTTPException

from src.data_research.service import RAW_PATH, full_research

app = FastAPI(title="data_research API", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/research")
def research():
    if not RAW_PATH.exists():
        raise HTTPException(status_code=404, detail=f"CSV not found at {RAW_PATH}")
    return full_research(RAW_PATH)
