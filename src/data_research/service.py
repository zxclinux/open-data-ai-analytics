import os
from pathlib import Path

import pandas as pd

RAW_PATH = Path(os.environ.get("DATA_RAW_PATH", "data/raw/petitions.csv")).resolve()


def _load_df(csv_path: Path = RAW_PATH) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df["date_start"] = pd.to_datetime(df["DateStartPetition"], errors="coerce")
    df["date_answer"] = pd.to_datetime(df["answerDate"], errors="coerce")
    return df


def signatures_distribution(df: pd.DataFrame) -> dict:
    if "count" not in df.columns:
        return {}
    c = df["count"]
    percentiles = {f"p{p}": int(c.quantile(p / 100)) for p in [25, 50, 75, 90, 95, 99]}
    buckets = {
        "zero": int((c == 0).sum()),
        "1_to_10": int(((c >= 1) & (c <= 10)).sum()),
        "11_to_100": int(((c > 10) & (c <= 100)).sum()),
        "over_100": int((c > 100).sum()),
    }
    return {"percentiles": percentiles, "buckets": buckets}


def duration_stats(df: pd.DataFrame) -> dict:
    with_answer = df[df["date_answer"].notna()].copy()
    if with_answer.empty:
        return {}
    with_answer["duration_days"] = (with_answer["date_answer"] - with_answer["date_start"]).dt.days
    d = with_answer["duration_days"]
    result: dict = {
        "count": int(len(d)),
        "min": int(d.min()),
        "max": int(d.max()),
        "mean": round(float(d.mean()), 1),
        "median": int(d.median()),
    }
    if "count" in df.columns:
        result["corr_signatures_duration"] = round(
            float(with_answer["count"].corr(with_answer["duration_days"])), 3
        )
    return result


def signatures_by_kind(df: pd.DataFrame, top_n: int = 12) -> list[dict]:
    if "kind" not in df.columns or "count" not in df.columns:
        return []
    by = df.groupby("kind")["count"].agg(["count", "sum", "mean", "median"])
    by = by.sort_values("sum", ascending=False).head(top_n).reset_index()
    by.columns = ["kind", "petitions", "total_signatures", "mean", "median"]
    by["mean"] = by["mean"].round(1)
    by["median"] = by["median"].round(1)
    return by.to_dict(orient="records")


def success_rate_by_kind(df: pd.DataFrame, top_n: int = 12) -> list[dict]:
    if "kind" not in df.columns or "status" not in df.columns:
        return []
    ok = df["status"] == "з відповіддю"
    rate = ok.groupby(df["kind"]).agg(["sum", "count"])
    rate["pct"] = (100 * rate["sum"] / rate["count"]).round(1)
    rate = rate.sort_values("pct", ascending=False).head(top_n).reset_index()
    rate.columns = ["kind", "with_answer", "total", "pct"]
    return rate.to_dict(orient="records")


def top_by_signatures(df: pd.DataFrame, top_n: int = 10) -> list[dict]:
    if "count" not in df.columns or "title" not in df.columns:
        return []
    top = df.nlargest(top_n, "count")[["title", "count", "status"]].copy()
    top.columns = ["title", "signatures", "status"]
    return top.to_dict(orient="records")


def full_research(csv_path: Path = RAW_PATH) -> dict:
    df = _load_df(csv_path)
    return {
        "rows": len(df),
        "signatures_distribution": signatures_distribution(df),
        "duration_stats": duration_stats(df),
        "signatures_by_kind": signatures_by_kind(df),
        "success_rate_by_kind": success_rate_by_kind(df),
        "top_by_signatures": top_by_signatures(df),
    }
