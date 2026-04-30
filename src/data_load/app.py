import threading
from fastapi import FastAPI, HTTPException, Query

from src.data_load.service import download_csv, download_petition_texts, DEFAULT_DATASET_URL, DEFAULT_OUTPUT_PATH
from src.data_load.db_service import load_csv_to_db, query_all, row_count, DB_PATH

app = FastAPI(title="data_load API", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/download")
def download(url: str = DEFAULT_DATASET_URL, force: bool = False):
    try:
        path = download_csv(url=url, force=force)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    return {"csv_path": str(path)}


@app.post("/load")
def load():
    csv_path = DEFAULT_OUTPUT_PATH.resolve()
    if not csv_path.exists():
        raise HTTPException(status_code=404, detail=f"CSV not found at {csv_path}. Call /download first.")
    n = load_csv_to_db(csv_path)
    return {"rows_loaded": n, "db_path": str(DB_PATH)}


@app.post("/pipeline")
def pipeline(url: str = DEFAULT_DATASET_URL, force: bool = False):
    try:
        csv_path = download_csv(url=url, force=force)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    n = load_csv_to_db(csv_path)
    threading.Thread(
        target=download_petition_texts,
        args=(csv_path,),
        daemon=True,
    ).start()
    return {
        "rows_loaded": n,
        "csv_path": str(csv_path),
        "db_path": str(DB_PATH),
        "texts": "downloading in background",
    }


@app.get("/petitions")
def petitions(limit: int = Query(100, ge=1, le=1000),
              offset: int = Query(0, ge=0)):
    try:
        rows = query_all(limit=limit, offset=offset)
    except Exception:
        raise HTTPException(status_code=404, detail="DB not ready. Call /load or /pipeline first.")
    return {"count": row_count(), "limit": limit, "offset": offset, "data": rows}
