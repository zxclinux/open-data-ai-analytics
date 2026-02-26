import sys
from pathlib import Path

import pandas as pd

RAW_PATH = Path("data") / "raw" / "petitions.csv"

def run(df: pd.DataFrame) -> None:
    df["date_start"] = pd.to_datetime(df["DateStartPetition"], errors="coerce")
    df["date_answer"] = pd.to_datetime(df["answerDate"], errors="coerce")

    print("--- Signatures distribution ---")
    if "count" in df.columns:
        c = df["count"]
        for p in [25, 50, 75, 90, 95, 99]:
            print(f"  p{p}: {c.quantile(p/100):.0f}")
        print(f"  zero: {(c == 0).sum()}, 1–10: {((c >= 1) & (c <= 10)).sum()}, 11–100: {((c > 10) & (c <= 100)).sum()}, 100+: {(c > 100).sum()}")

    print("\n--- Duration (start → answer), days ---")
    with_answer = df[df["date_answer"].notna()].copy()
    with_answer["duration_days"] = (with_answer["date_answer"] - with_answer["date_start"]).dt.days
    if len(with_answer):
        d = with_answer["duration_days"]
        print(f"  count: {len(d)}, min={d.min()}, max={d.max()}, mean={d.mean():.0f}, median={d.median():.0f}")
        if "count" in df.columns:
            r = with_answer["count"].corr(with_answer["duration_days"])
            print(f"  corr(signatures, duration): {r:.3f}")

    print("\n--- Signatures by kind ---")
    if "kind" in df.columns and "count" in df.columns:
        by_kind = df.groupby("kind")["count"].agg(["count", "sum", "mean", "median"])
        by_kind = by_kind.sort_values("sum", ascending=False).head(12)
        print(by_kind.to_string())

    print("\n--- Success rate by kind (% with answer) ---")
    if "kind" in df.columns and "status" in df.columns:
        ok = df["status"] == "з відповіддю"
        rate = ok.groupby(df["kind"]).agg(["sum", "count"])
        rate["pct"] = 100 * rate["sum"] / rate["count"]
        rate = rate.sort_values("pct", ascending=False).head(12)
        print(rate[["sum", "count", "pct"]].to_string())

    print("\n--- Top 10 by signatures ---")
    if "count" in df.columns and "title" in df.columns:
        top = df.nlargest(10, "count")[["title", "count", "status"]]
        for _, row in top.iterrows():
            title = (row["title"][:60] + "…") if len(str(row["title"])) > 60 else row["title"]
            print(f"  {row['count']:4.0f}  {row['status']}  {title}")


def main() -> None:
    if not RAW_PATH.exists():
        print(f"[data_research] File not found: {RAW_PATH}", file=sys.stderr)
        sys.exit(1)
    df = pd.read_csv(RAW_PATH)
    run(df)


if __name__ == "__main__":
    main()
