import io
import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

RAW_PATH = Path(os.environ.get("DATA_RAW_PATH", "data/raw/petitions.csv")).resolve()
FIGURES_PATH = Path(os.environ.get("REPORTS_FIGURES_PATH", "reports/figures")).resolve()

AVAILABLE_CHARTS = [
    "signatures_dist",
    "median_by_kind",
    "mean_median_by_kind",
    "activity_by_year",
    "duration_dist",
    "status_pie",
]


def _load_df(csv_path: Path = RAW_PATH) -> pd.DataFrame:
    return pd.read_csv(csv_path)


def plot_signatures_dist(df: pd.DataFrame, bins: int = 30, dpi: int = 120) -> bytes:
    if "count" not in df.columns:
        return b""
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    c = df["count"]
    axes[0].hist(c, bins=bins, edgecolor="black", alpha=0.7)
    axes[0].set_title("Розподіл підписів")
    axes[0].set_xlabel("count")
    axes[1].boxplot(c, vert=True)
    axes[1].set_title("Підписи (boxplot)")
    plt.tight_layout()
    return _fig_to_bytes(fig, dpi)


def plot_median_by_kind(df: pd.DataFrame, top_n: int = 12, dpi: int = 120) -> bytes:
    if "kind" not in df.columns or "count" not in df.columns:
        return b""
    by = df.groupby("kind")["count"].median().sort_values(ascending=True).tail(top_n)
    fig, ax = plt.subplots(figsize=(8, 5))
    by.plot(kind="barh", ax=ax)
    ax.set_title("Медіана підписів по категорії")
    ax.set_xlabel("медіана count")
    plt.tight_layout()
    return _fig_to_bytes(fig, dpi)


def plot_mean_median_by_kind(df: pd.DataFrame, top_n: int = 12, dpi: int = 120) -> bytes:
    if "kind" not in df.columns or "count" not in df.columns:
        return b""
    by = df.groupby("kind")["count"].agg(["mean", "median"]).sort_values("median", ascending=False).head(top_n)
    fig, ax = plt.subplots(figsize=(8, 5))
    x = range(len(by))
    w = 0.35
    ax.bar([i - w / 2 for i in x], by["mean"], width=w, label="mean")
    ax.bar([i + w / 2 for i in x], by["median"], width=w, label="median")
    ax.set_xticks(list(x))
    ax.set_xticklabels(by.index, rotation=45, ha="right")
    ax.set_title("Середнє та медіана підписів по категорії")
    ax.legend()
    plt.tight_layout()
    return _fig_to_bytes(fig, dpi)


def plot_activity_by_year(df: pd.DataFrame, dpi: int = 120) -> bytes:
    if "DateStartPetition" not in df.columns or "count" not in df.columns:
        return b""
    df = df.copy()
    df["year"] = pd.to_datetime(df["DateStartPetition"], errors="coerce").dt.year
    df = df.dropna(subset=["year"])
    by = df.groupby("year").agg(
        n=("count", "count"), total=("count", "sum"),
        mean=("count", "mean"), median=("count", "median"),
    ).reset_index()
    fig, axes = plt.subplots(2, 1, figsize=(8, 7))
    axes[0].bar(by["year"], by["n"])
    axes[0].set_title("Кількість петицій по роках")
    axes[0].set_xlabel("рік")
    axes[1].plot(by["year"], by["mean"], marker="o", label="mean")
    axes[1].plot(by["year"], by["median"], marker="s", label="median")
    axes[1].set_title("Середнє та медіана підписів по роках")
    axes[1].set_xlabel("рік")
    axes[1].legend()
    plt.tight_layout()
    return _fig_to_bytes(fig, dpi)


def plot_duration_dist(df: pd.DataFrame, bins: int = 20, dpi: int = 120) -> bytes:
    if "DateStartPetition" not in df.columns or "answerDate" not in df.columns:
        return b""
    df = df.copy()
    df["date_start"] = pd.to_datetime(df["DateStartPetition"], errors="coerce")
    df["date_answer"] = pd.to_datetime(df["answerDate"], errors="coerce")
    with_ans = df[df["date_answer"].notna()].copy()
    with_ans["duration_days"] = (with_ans["date_answer"] - with_ans["date_start"]).dt.days
    if with_ans.empty:
        return b""
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(with_ans["duration_days"], bins=bins, edgecolor="black", alpha=0.7)
    med = with_ans["duration_days"].median()
    ax.axvline(med, color="red", linestyle="--", label=f"median={med:.0f}")
    ax.set_title("Розподіл тривалості (дні до відповіді)")
    ax.set_xlabel("дні")
    ax.legend()
    plt.tight_layout()
    return _fig_to_bytes(fig, dpi)


def plot_status_pie(df: pd.DataFrame, dpi: int = 120) -> bytes:
    if "status" not in df.columns:
        return b""
    s = df["status"].value_counts()
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.pie(s, labels=s.index, autopct="%1.1f%%", startangle=90)
    ax.set_title("Статуси петицій")
    plt.tight_layout()
    return _fig_to_bytes(fig, dpi)


CHART_FUNCS = {
    "signatures_dist": lambda df, **kw: plot_signatures_dist(df, **kw),
    "median_by_kind": lambda df, **kw: plot_median_by_kind(df, **kw),
    "mean_median_by_kind": lambda df, **kw: plot_mean_median_by_kind(df, **kw),
    "activity_by_year": lambda df, **kw: plot_activity_by_year(df, **kw),
    "duration_dist": lambda df, **kw: plot_duration_dist(df, **kw),
    "status_pie": lambda df, **kw: plot_status_pie(df, **kw),
}


def generate_chart(name: str, csv_path: Path = RAW_PATH, **kwargs) -> bytes:
    df = _load_df(csv_path)
    func = CHART_FUNCS[name]
    return func(df, **kwargs)


def generate_all(csv_path: Path = RAW_PATH, out_dir: Path = FIGURES_PATH,
                 dpi: int = 120) -> list[str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    df = _load_df(csv_path)
    saved: list[str] = []
    for name, func in CHART_FUNCS.items():
        data = func(df, dpi=dpi)
        if data:
            path = out_dir / f"{name}.png"
            path.write_bytes(data)
            saved.append(str(path))
    return saved


def _fig_to_bytes(fig, dpi: int = 120) -> bytes:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi)
    plt.close(fig)
    buf.seek(0)
    return buf.read()
