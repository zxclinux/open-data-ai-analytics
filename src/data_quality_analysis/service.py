import os
from pathlib import Path

import pandas as pd

RAW_PATH = Path(os.environ.get("DATA_RAW_PATH", "data/raw/petitions.csv")).resolve()


def _load_df(csv_path: Path = RAW_PATH) -> pd.DataFrame:
    return pd.read_csv(csv_path)


def numeric_stats(df: pd.DataFrame) -> dict:
    if "count" not in df.columns:
        return {}
    c = df["count"]
    return {
        "min": int(c.min()),
        "max": int(c.max()),
        "mean": round(float(c.mean()), 1),
        "median": int(c.median()),
    }


def date_range(df: pd.DataFrame) -> dict:
    if "DateStartPetition" not in df.columns:
        return {}
    d = pd.to_datetime(df["DateStartPetition"], errors="coerce").dropna()
    if d.empty:
        return {}
    return {"min": str(d.min().date()), "max": str(d.max().date())}


def petitions_by_year(df: pd.DataFrame) -> dict[str, int]:
    if "DateStartPetition" not in df.columns:
        return {}
    years = pd.to_datetime(df["DateStartPetition"], errors="coerce").dt.year
    return {
        str(int(y)): int(n)
        for y, n in years.value_counts().sort_index().items()
        if pd.notna(y)
    }


def kind_counts(df: pd.DataFrame, top_n: int = 10) -> dict[str, int]:
    if "kind" not in df.columns:
        return {}
    return {str(k): int(v) for k, v in df["kind"].value_counts().head(top_n).items()}


def status_counts(df: pd.DataFrame) -> dict[str, int]:
    if "status" not in df.columns:
        return {}
    return {str(k): int(v) for k, v in df["status"].value_counts().items()}


def answer_stats(df: pd.DataFrame) -> dict:
    result: dict = {}
    if "status" in df.columns:
        with_ans = int((df["status"] == "з відповіддю").sum())
        total = len(df)
        result["with_answer"] = with_ans
        result["total"] = total
        result["with_answer_pct"] = round(100 * with_ans / total, 1) if total else 0
    if "count" in df.columns:
        over_zero = int((df["count"] > 0).sum())
        total = len(df)
        result["signatures_gt_zero"] = over_zero
        result["signatures_gt_zero_pct"] = round(100 * over_zero / total, 1) if total else 0
    return result


def full_quality_analysis(csv_path: Path = RAW_PATH) -> dict:
    df = _load_df(csv_path)
    return {
        "rows": len(df),
        "columns": list(df.columns),
        "numeric": numeric_stats(df),
        "date_range": date_range(df),
        "by_year": petitions_by_year(df),
        "kind": kind_counts(df),
        "status": status_counts(df),
        "answer_stats": answer_stats(df),
    }
