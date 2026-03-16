import os
import sqlite3
from pathlib import Path

DB_PATH = Path(os.environ.get("DB_PATH", "data/petitions.db")).resolve()
TABLE = "petitions"


def _conn() -> sqlite3.Connection:
    c = sqlite3.connect(str(DB_PATH))
    c.row_factory = sqlite3.Row
    return c


def petitions_list(limit: int = 50, offset: int = 0) -> list[dict]:
    with _conn() as c:
        rows = c.execute(
            f"SELECT uid, kind, title, count, status, DateStartPetition "
            f"FROM {TABLE} ORDER BY uid LIMIT ? OFFSET ?",
            (limit, offset),
        ).fetchall()
    return [dict(r) for r in rows]


def petitions_count() -> int:
    with _conn() as c:
        return c.execute(f"SELECT count(*) FROM {TABLE}").fetchone()[0]


def top_petitions(n: int = 10) -> list[dict]:
    with _conn() as c:
        rows = c.execute(
            f"SELECT uid, kind, title, count, status "
            f"FROM {TABLE} ORDER BY count DESC LIMIT ?",
            (n,),
        ).fetchall()
    return [dict(r) for r in rows]


def petitions_by_status() -> list[dict]:
    with _conn() as c:
        rows = c.execute(
            f"SELECT status, count(*) as cnt FROM {TABLE} GROUP BY status ORDER BY cnt DESC"
        ).fetchall()
    return [dict(r) for r in rows]


def search_petitions(q: str, limit: int = 50) -> list[dict]:
    with _conn() as c:
        rows = c.execute(
            f"SELECT uid, kind, title, count, status "
            f"FROM {TABLE} WHERE title LIKE ? LIMIT ?",
            (f"%{q}%", limit),
        ).fetchall()
    return [dict(r) for r in rows]


def drop_table() -> None:
    with _conn() as c:
        c.execute(f"DROP TABLE IF EXISTS {TABLE}")
    if DB_PATH.exists():
        DB_PATH.unlink()
