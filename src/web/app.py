import os

import httpx
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates

from src.web.db_queries import (
    petitions_list, petitions_count, top_petitions,
    petitions_by_status, search_petitions, drop_table,
)

DATA_LOAD_URL = os.environ.get("DATA_LOAD_URL", "http://localhost:8001")
QUALITY_URL = os.environ.get("QUALITY_URL", "http://localhost:8002")
RESEARCH_URL = os.environ.get("RESEARCH_URL", "http://localhost:8003")
VIZ_URL = os.environ.get("VIZ_URL", "http://localhost:8004")

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

app = FastAPI(title="Open Data Analytics", version="1.0.0")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        name="index.html",
        request=request,
        context={"request": request},
    )


@app.get("/ui/petitions", response_class=HTMLResponse)
async def ui_petitions(request: Request,
                       page: int = Query(1, ge=1),
                       limit: int = Query(50, ge=1, le=200)):
    offset = (page - 1) * limit
    try:
        rows = petitions_list(limit=limit, offset=offset)
        total = petitions_count()
    except Exception:
        rows, total = [], 0
    return templates.TemplateResponse(
        name="petitions.html",
        request=request,
        context={
            "request": request,
            "rows": rows,
            "total": total,
            "page": page,
            "limit": limit,
        },
    )


@app.get("/ui/quality", response_class=HTMLResponse)
async def ui_quality(request: Request):
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            r = await client.get(f"{QUALITY_URL}/quality")
            data = r.json() if r.status_code == 200 else {"error": r.text}
        except httpx.RequestError as e:
            data = {"error": str(e)}
    return templates.TemplateResponse(
        name="quality.html",
        request=request,
        context={"request": request, "data": data},
    )


@app.get("/ui/research", response_class=HTMLResponse)
async def ui_research(request: Request):
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            r = await client.get(f"{RESEARCH_URL}/research")
            data = r.json() if r.status_code == 200 else {"error": r.text}
        except httpx.RequestError as e:
            data = {"error": str(e)}
    return templates.TemplateResponse(
        name="research.html",
        request=request,
        context={"request": request, "data": data},
    )


@app.get("/ui/charts", response_class=HTMLResponse)
async def ui_charts(request: Request):
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            r = await client.get(f"{VIZ_URL}/charts")
            charts = r.json().get("available", []) if r.status_code == 200 else []
        except httpx.RequestError:
            charts = []
    return templates.TemplateResponse(
        name="charts.html",
        request=request,
        context={"request": request, "charts": charts, "viz_url": VIZ_URL},
    )

@app.get("/api/petitions")
def api_petitions(limit: int = Query(50, ge=1, le=500),
                  offset: int = Query(0, ge=0)):
    try:
        return {"total": petitions_count(), "data": petitions_list(limit, offset)}
    except Exception:
        raise HTTPException(404, "DB not ready. Run data_load pipeline first.")


@app.get("/api/top")
def api_top(n: int = Query(10, ge=1, le=100)):
    try:
        return {"data": top_petitions(n)}
    except Exception:
        raise HTTPException(404, "DB not ready.")


@app.get("/api/by-status")
def api_by_status():
    try:
        return {"data": petitions_by_status()}
    except Exception:
        raise HTTPException(404, "DB not ready.")


@app.get("/api/search")
def api_search(q: str = Query(..., min_length=1),
               limit: int = Query(50, ge=1, le=200)):
    try:
        return {"data": search_petitions(q, limit)}
    except Exception:
        raise HTTPException(404, "DB not ready.")

@app.delete("/api/db")
def api_clear_db():
    try:
        drop_table()
    except Exception as e:
        raise HTTPException(500, str(e))
    return {"status": "cleared"}


@app.post("/api/pipeline")
async def api_pipeline(force: bool = False):
    async with httpx.AsyncClient(timeout=120) as client:
        try:
            r = await client.post(f"{DATA_LOAD_URL}/pipeline", params={"force": force})
        except httpx.RequestError as e:
            raise HTTPException(502, f"data-load service unavailable: {e}")
    if r.status_code != 200:
        raise HTTPException(r.status_code, r.text)
    return r.json()


@app.get("/api/charts/{name}")
async def proxy_chart(name: str, dpi: int = Query(120, ge=50, le=300)):
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            r = await client.get(f"{VIZ_URL}/charts/{name}", params={"dpi": dpi})
        except httpx.RequestError as e:
            raise HTTPException(502, str(e))
    if r.status_code != 200:
        raise HTTPException(r.status_code, r.text)
    return Response(content=r.content, media_type="image/png")


@app.get("/health")
def health():
    return {"status": "ok"}
