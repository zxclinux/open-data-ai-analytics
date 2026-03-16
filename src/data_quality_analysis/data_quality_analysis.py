"""CLI entry point: run quality analysis and print JSON."""
import json
import sys

from src.data_quality_analysis.service import RAW_PATH, full_quality_analysis


def main() -> None:
    if not RAW_PATH.exists():
        print(f"[data_quality] File not found: {RAW_PATH}", file=sys.stderr)
        sys.exit(1)
    result = full_quality_analysis(RAW_PATH)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
