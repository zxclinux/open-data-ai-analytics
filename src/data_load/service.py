import csv
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

DEFAULT_OUTPUT_PATH = Path(
    os.environ.get("OUTPUT_PATH", "data/raw/petitions.csv")
)
DEFAULT_DATASET_URL = os.environ.get(
    "DATASET_URL",
    "https://data.gov.ua/dataset/dbfff194-ca0c-47e8-9434-6670236894a1"
    "/resource/2af4e39b-d6a3-4c1c-a5a8-f25597326f4d/download/petitions.csv",
)
PETITIONS_DIR = Path(os.environ.get("PETITIONS_DIR", "data/petitions")).resolve()


def download_csv(url: str = DEFAULT_DATASET_URL,
                 output_path: Path = DEFAULT_OUTPUT_PATH,
                 force: bool = False) -> Path:
    output_path = output_path.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists() and not force:
        return output_path

    try:
        with urlopen(url) as resp:
            if resp.status != 200:
                raise HTTPError(url, resp.status, "Non-200", resp.headers, None)
            with output_path.open("wb") as f:
                while chunk := resp.read(8192):
                    f.write(chunk)
    except (URLError, HTTPError) as exc:
        raise RuntimeError(f"Download failed: {exc}") from exc

    return output_path


def _fetch_one(uid: str, url: str, dest: Path, max_attempts: int) -> str:
    """Download one petition text file; return 'ok', 'skipped', or 'failed:<reason>'."""
    if dest.exists():
        return "skipped"
    last_exc = None
    for attempt in range(max_attempts):
        try:
            with urlopen(url, timeout=15) as resp:
                dest.write_bytes(resp.read())
            return "ok"
        except Exception as exc:
            last_exc = exc
            if attempt < max_attempts - 1:
                time.sleep(2 ** attempt)   # 1 s, 2 s between retries
    return f"failed:{last_exc}"


def download_petition_texts(
    csv_path: Path,
    output_dir: Path = PETITIONS_DIR,
    max_workers: int = 10,
    retries: int = 3,
) -> dict:
    """Download all petition text files listed in the CSV, concurrently with retries."""
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    petitions: list[tuple[str, str, str]] = []
    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            url      = row.get("url",  "").strip()
            filename = row.get("text", "").strip()
            if url and filename:
                petitions.append((row["uid"], url, filename))

    stats = {"downloaded": 0, "skipped": 0, "failed": 0}

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        future_to_uid = {
            pool.submit(_fetch_one, uid, url, output_dir / filename, retries): uid
            for uid, url, filename in petitions
        }
        for future in as_completed(future_to_uid):
            result = future.result()
            if result == "ok":
                stats["downloaded"] += 1
            elif result == "skipped":
                stats["skipped"] += 1
            else:
                stats["failed"] += 1
                print(f"[texts] uid={future_to_uid[future]} {result}", flush=True)

    return stats
