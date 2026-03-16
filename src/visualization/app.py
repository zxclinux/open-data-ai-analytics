from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import Response

from src.visualization.service import (
    RAW_PATH, AVAILABLE_CHARTS, generate_chart, generate_all, FIGURES_PATH,
)

app = FastAPI(title="visualization API", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/charts")
def list_charts():
    return {"available": AVAILABLE_CHARTS}


@app.get("/charts/{name}")
def get_chart(
    name: str,
    dpi: int = Query(120, ge=50, le=300),
    bins: int = Query(30, ge=5, le=200),
    top_n: int = Query(12, ge=1, le=50),
):
    if name not in AVAILABLE_CHARTS:
        raise HTTPException(status_code=404, detail=f"Unknown chart '{name}'. Available: {AVAILABLE_CHARTS}")
    if not RAW_PATH.exists():
        raise HTTPException(status_code=404, detail=f"CSV not found at {RAW_PATH}")

    kwargs: dict = {"dpi": dpi}
    if name in ("signatures_dist", "duration_dist"):
        kwargs["bins"] = bins
    if name in ("median_by_kind", "mean_median_by_kind"):
        kwargs["top_n"] = top_n

    data = generate_chart(name, **kwargs)
    if not data:
        raise HTTPException(status_code=422, detail=f"Not enough data to build '{name}'")
    return Response(content=data, media_type="image/png")


@app.post("/generate")
def generate(dpi: int = Query(120, ge=50, le=300)):
    if not RAW_PATH.exists():
        raise HTTPException(status_code=404, detail=f"CSV not found at {RAW_PATH}")
    saved = generate_all(dpi=dpi)
    return {"saved": saved, "count": len(saved)}
