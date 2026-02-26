import sys
from pathlib import Path

import pandas as pd

RAW_PATH = Path("data") / "raw" / "petitions.csv"

def print_analysis(df: pd.DataFrame) -> None:
    print("\nNumeric ")
    if "count" in df.columns:
        c = df["count"]
        print(f"signatures: min={c.min()}, max={c.max()}, mean={c.mean():.1f}, median={c.median():.0f}")

    print("\nDates ")
    if "DateStartPetition" in df.columns:
        d = pd.to_datetime(df["DateStartPetition"], errors="coerce").dropna()
        if len(d):
            print(f"DateStartPetition: {d.min().date()} .. {d.max().date()}")

    print("\nBy year ")
    if "DateStartPetition" in df.columns:
        years = pd.to_datetime(df["DateStartPetition"], errors="coerce").dt.year
        for y, n in years.value_counts().sort_index().items():
            if pd.notna(y):
                print(f"  {int(y)}: {n}")

    print("\nKind ")
    if "kind" in df.columns:
        print(df["kind"].value_counts().head(10).to_string())

    print("\nStatus ")
    if "status" in df.columns:
        print(df["status"].value_counts().to_string())

    print("\nWith answer ")
    if "status" in df.columns:
        with_ans = (df["status"] == "з відповіддю").sum()
        print(f"{with_ans} / {len(df)} ({100 * with_ans / len(df):.1f}%)")
    if "count" in df.columns:
        over_zero = (df["count"] > 0).sum()
        print(f"signatures > 0: {over_zero} / {len(df)} ({100 * over_zero / len(df):.1f}%)")


def main() -> None:
    if not RAW_PATH.exists():
        print(f"[data_quality] File not found: {RAW_PATH}", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(RAW_PATH)
    print(f"Rows: {len(df)}, columns: {list(df.columns)}")
    print_analysis(df)


if __name__ == "__main__":
    main()
