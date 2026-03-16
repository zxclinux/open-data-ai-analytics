"""CLI entry point: generate all charts and save to disk."""
import sys

from src.visualization.service import RAW_PATH, FIGURES_PATH, generate_all


def main() -> None:
    if not RAW_PATH.exists():
        print(f"[visualization] File not found: {RAW_PATH}", file=sys.stderr)
        sys.exit(1)
    saved = generate_all()
    print(f"[visualization] Saved {len(saved)} figures to {FIGURES_PATH}")


if __name__ == "__main__":
    main()
