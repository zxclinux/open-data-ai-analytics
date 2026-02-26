import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

RAW_PATH = Path("data") / "raw" / "petitions.csv"
FIGURES_PATH = Path("reports") / "figures"


def plot_signatures_dist(df: pd.DataFrame, out_dir: Path) -> None:
    if "count" not in df.columns:
        return
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    c = df["count"]
    axes[0].hist(c, bins=30, edgecolor="black", alpha=0.7)
    axes[0].set_title("Розподіл підписів")
    axes[0].set_xlabel("count")
    axes[1].boxplot(c, vert=True)
    axes[1].set_title("Підписи (boxplot)")
    plt.tight_layout()
    fig.savefig(out_dir / "signatures_dist.png", dpi=120)
    plt.close()


def plot_median_by_kind(df: pd.DataFrame, out_dir: Path) -> None:
    if "kind" not in df.columns or "count" not in df.columns:
        return
    by = df.groupby("kind")["count"].median().sort_values(ascending=True).tail(12)
    fig, ax = plt.subplots(figsize=(8, 5))
    by.plot(kind="barh", ax=ax)
    ax.set_title("Медіана підписів по категорії")
    ax.set_xlabel("медіана count")
    plt.tight_layout()
    fig.savefig(out_dir / "median_by_kind.png", dpi=120)
    plt.close()


def plot_mean_median_by_kind(df: pd.DataFrame, out_dir: Path) -> None:
    if "kind" not in df.columns or "count" not in df.columns:
        return
    by = df.groupby("kind")["count"].agg(["mean", "median"]).sort_values("median", ascending=False).head(12)
    fig, ax = plt.subplots(figsize=(8, 5))
    x = range(len(by))
    w = 0.35
    ax.bar([i - w/2 for i in x], by["mean"], width=w, label="mean")
    ax.bar([i + w/2 for i in x], by["median"], width=w, label="median")
    ax.set_xticks(x)
    ax.set_xticklabels(by.index, rotation=45, ha="right")
    ax.set_title("Середнє та медіана підписів по категорії")
    ax.legend()
    plt.tight_layout()
    fig.savefig(out_dir / "mean_median_by_kind.png", dpi=120)
    plt.close()


def plot_activity_by_year(df: pd.DataFrame, out_dir: Path) -> None:
    if "DateStartPetition" not in df.columns or "count" not in df.columns:
        return
    df = df.copy()
    df["year"] = pd.to_datetime(df["DateStartPetition"], errors="coerce").dt.year
    df = df.dropna(subset=["year"])
    by = df.groupby("year").agg(n=("count", "count"), total=("count", "sum"), mean=("count", "mean"), median=("count", "median"))
    by = by.reset_index()
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
    fig.savefig(out_dir / "activity_by_year.png", dpi=120)
    plt.close()


def plot_duration_dist(df: pd.DataFrame, out_dir: Path) -> None:
    if "DateStartPetition" not in df.columns or "answerDate" not in df.columns:
        return
    df = df.copy()
    df["date_start"] = pd.to_datetime(df["DateStartPetition"], errors="coerce")
    df["date_answer"] = pd.to_datetime(df["answerDate"], errors="coerce")
    with_ans = df[df["date_answer"].notna()].copy()
    with_ans["duration_days"] = (with_ans["date_answer"] - with_ans["date_start"]).dt.days
    if with_ans.empty:
        return
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(with_ans["duration_days"], bins=20, edgecolor="black", alpha=0.7)
    ax.axvline(with_ans["duration_days"].median(), color="red", linestyle="--", label=f"median={with_ans['duration_days'].median():.0f}")
    ax.set_title("Розподіл тривалості (дні до відповіді)")
    ax.set_xlabel("дні")
    ax.legend()
    plt.tight_layout()
    fig.savefig(out_dir / "duration_dist.png", dpi=120)
    plt.close()


def plot_status(df: pd.DataFrame, out_dir: Path) -> None:
    if "status" not in df.columns:
        return
    s = df["status"].value_counts()
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.pie(s, labels=s.index, autopct="%1.1f%%", startangle=90)
    ax.set_title("Статуси петицій")
    plt.tight_layout()
    fig.savefig(out_dir / "status_pie.png", dpi=120)
    plt.close()


def main() -> None:
    if not RAW_PATH.exists():
        print(f"[visualization] File not found: {RAW_PATH}", file=sys.stderr)
        sys.exit(1)
    FIGURES_PATH.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(RAW_PATH)

    plot_signatures_dist(df, FIGURES_PATH)
    plot_median_by_kind(df, FIGURES_PATH)
    plot_mean_median_by_kind(df, FIGURES_PATH)
    plot_activity_by_year(df, FIGURES_PATH)
    plot_duration_dist(df, FIGURES_PATH)
    plot_status(df, FIGURES_PATH)

    print(f"[visualization] Saved figures to {FIGURES_PATH}")


if __name__ == "__main__":
    main()
