import sys
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

DEFAULT_OUTPUT_PATH = Path("data") / "raw" / "petitions.csv"

def download_file(url: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists():
        print(f"[data_load] File already exists at {output_path}. Remove it first if you want to re-download.")
        return

    try:
        with urlopen(url) as response:
            if response.status != 200:
                raise HTTPError(url, response.status, "Non-200 response", response.headers, None)

            with output_path.open("wb") as f:
                while True:
                    chunk = response.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)

        print(f"[data_load] Saved dataset to: {output_path}")
    except (URLError, HTTPError) as exc:
        print(f"[data_load] Failed to download data: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


def main() -> None:

    url = sys.argv[1]
    download_file(url=url, output_path=DEFAULT_OUTPUT_PATH)


if __name__ == "__main__":
    main()

