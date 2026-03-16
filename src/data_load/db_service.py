import os
import sqlite3
from pathlib import Path

import pandas as pd

DB_PATH = Path(os.environ.get("DB_PATH", "data/petitions.db")).resolve()
TABLE = "petitions"


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(str(db_path))


def load_csv_to_db(csv_path: Path, db_path: Path = DB_PATH) -> int:
    df = pd.read_csv(csv_path)
    with get_connection(db_path) as conn:
        df.to_sql(TABLE, conn, if_exists="replace", index=False)
    return len(df)


def query_all(db_path: Path = DB_PATH,
              limit: int = 100, offset: int = 0) -> list[dict]:
    with get_connection(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            f"SELECT * FROM {TABLE} LIMIT ? OFFSET ?", (limit, offset)
        ).fetchall()
    return [dict(r) for r in rows]


def row_count(db_path: Path = DB_PATH) -> int:
    with get_connection(db_path) as conn:
        return conn.execute(f"SELECT count(*) FROM {TABLE}").fetchone()[0]
