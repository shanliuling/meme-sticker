#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from sticker_sheet_lib import split_sheet_to_dir


def main() -> int:
    p = argparse.ArgumentParser(description="Extract one 3x2 AI sticker sheet into 6 transparent PNG stickers.")
    p.add_argument("--input-image", required=True)
    p.add_argument("--output-dir", required=True)
    p.add_argument("--rows", type=int, default=2)
    p.add_argument("--cols", type=int, default=3)
    p.add_argument("--foreground-threshold", type=float, default=30.0)
    p.add_argument("--search-fraction", type=float, default=0.24)
    p.add_argument("--max-gutter-density", type=float, default=0.075)
    p.add_argument("--max-edge-contact", type=float, default=0.22)
    p.add_argument("--min-cell-foreground", type=float, default=0.01)
    p.add_argument("--background-tolerance", type=float, default=42.0)
    p.add_argument("--white-fallback-threshold", type=float, default=20.0)
    p.add_argument("--white-border-fraction", type=float, default=0.026)
    p.add_argument("--canvas-size", type=int, default=512)
    p.add_argument("--content-fraction", type=float, default=0.82)
    p.add_argument("--force", action="store_true")
    args = p.parse_args()

    result = split_sheet_to_dir(
        input_image=Path(args.input_image),
        output_dir=Path(args.output_dir),
        rows=args.rows,
        cols=args.cols,
        foreground_threshold=args.foreground_threshold,
        search_fraction=args.search_fraction,
        max_gutter_density=args.max_gutter_density,
        max_edge_contact=args.max_edge_contact,
        min_cell_foreground=args.min_cell_foreground,
        background_tolerance=args.background_tolerance,
        white_fallback_threshold=args.white_fallback_threshold,
        white_border_fraction=args.white_border_fraction,
        canvas_size=args.canvas_size,
        content_fraction=args.content_fraction,
        force=args.force,
        preview_columns=args.cols,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("ok") else 3


if __name__ == "__main__":
    raise SystemExit(main())
