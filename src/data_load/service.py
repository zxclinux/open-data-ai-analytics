import os
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
