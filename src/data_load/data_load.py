import sys
from pathlib import Path

from src.data_load.service import download_csv, DEFAULT_DATASET_URL
from src.data_load.db_service import load_csv_to_db


def main() -> None:
    url = DEFAULT_DATASET_URL
    if len(sys.argv) >= 2:
        arg = sys.argv[1]
        if "://" in arg:
            url = arg
        else:
            path = Path(arg).resolve()
            if path.exists():
                print(f"[data_load] CSV exists at {path}, loading into SQLite...")
                n = load_csv_to_db(path)
                print(f"[data_load] Loaded {n} rows into SQLite.")
                return

    try:
        csv_path = download_csv(url=url, force=False)
        print(f"[data_load] CSV ready at {csv_path}")
    except RuntimeError as exc:
        print(f"[data_load] {exc}", file=sys.stderr)
        raise SystemExit(1)

    n = load_csv_to_db(csv_path)
    print(f"[data_load] Loaded {n} rows into SQLite.")


if __name__ == "__main__":
    main()
