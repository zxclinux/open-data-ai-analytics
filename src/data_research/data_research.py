"""CLI entry point: run research and print JSON."""
import json
import sys

from src.data_research.service import RAW_PATH, full_research


def main() -> None:
    if not RAW_PATH.exists():
        print(f"[data_research] File not found: {RAW_PATH}", file=sys.stderr)
        sys.exit(1)
    result = full_research(RAW_PATH)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
