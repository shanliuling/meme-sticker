#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import zipfile
import tempfile
from contextlib import contextmanager
from pathlib import Path

from sticker_sheet_lib import split_sheet_to_dir, make_preview


@contextmanager
def _managed_work_dir(output_dir: Path):
    """Create a unique temporary work directory inside the approved output tree."""
    # mkdtemp creates a directory owned by this run, so cleanup can never remove
    # a pre-existing user directory that merely happens to have the same name.
    work_root = Path(tempfile.mkdtemp(prefix=".meme-sticker-work-", dir=output_dir))
    try:
        yield work_root
    finally:
        shutil.rmtree(work_root, ignore_errors=True)


def _copy_debug_tree(work_root: Path, output_dir: Path, report: dict) -> None:
    debug_dir = output_dir / "debug"
    if debug_dir.exists():
        shutil.rmtree(debug_dir)
    debug_dir.mkdir(parents=True, exist_ok=True)
    for name in ("sheet-a", "sheet-b"):
        src = work_root / name
        if src.exists():
            shutil.copytree(src, debug_dir / name)
    (debug_dir / "pack-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def _build_clean_zip(zip_path: Path, preview_path: Path, sticker_paths: list[Path]) -> None:
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(preview_path, arcname="preview.jpg")
        for i, p in enumerate(sticker_paths, 1):
            zf.write(p, arcname=f"stickers/{i:02d}.png")


def main() -> int:
    p = argparse.ArgumentParser(description="Build a clean 12-sticker pack from two 3x2 sticker sheets.")
    p.add_argument("--sheet-a", required=True)
    p.add_argument("--sheet-b", required=True)
    p.add_argument("--output-dir", required=True)
    p.add_argument("--canvas-size", type=int, default=512)
    p.add_argument("--content-fraction", type=float, default=0.82)
    p.add_argument("--force", action="store_true")
    p.add_argument(
        "--keep-debug",
        action="store_true",
        help="Keep intermediate Sheet A / Sheet B extraction folders and JSON diagnostics under output/debug.",
    )
    args = p.parse_args()

    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    # Clean old user-facing artifacts so the final folder is predictable.
    for name in ("preview.jpg", "sticker-pack.zip"):
        target = output_dir / name
        if target.exists():
            target.unlink()
    if not args.keep_debug:
        old_debug = output_dir / "debug"
        if old_debug.exists():
            shutil.rmtree(old_debug)

    with _managed_work_dir(output_dir) as work_root:
        sheet_a_out = work_root / "sheet-a"
        sheet_b_out = work_root / "sheet-b"

        res_a = split_sheet_to_dir(
            input_image=Path(args.sheet_a),
            output_dir=sheet_a_out,
            rows=2,
            cols=3,
            canvas_size=args.canvas_size,
            content_fraction=args.content_fraction,
            force=args.force,
            preview_columns=3,
        )
        if not res_a.get("ok"):
            result = {
                "ok": False,
                "reason": "sheet_a_failed",
                "sheet_a": res_a,
                "message": "Sheet A could not be safely extracted. Regenerate only Sheet A.",
            }
            if args.keep_debug:
                _copy_debug_tree(work_root, output_dir, result)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 3

        res_b = split_sheet_to_dir(
            input_image=Path(args.sheet_b),
            output_dir=sheet_b_out,
            rows=2,
            cols=3,
            canvas_size=args.canvas_size,
            content_fraction=args.content_fraction,
            force=args.force,
            preview_columns=3,
        )
        if not res_b.get("ok"):
            result = {
                "ok": False,
                "reason": "sheet_b_failed",
                "sheet_b": res_b,
                "message": "Sheet B could not be safely extracted. Regenerate only Sheet B.",
            }
            if args.keep_debug:
                _copy_debug_tree(work_root, output_dir, result)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 3

        combined_work = work_root / "combined"
        combined_work.mkdir(parents=True, exist_ok=True)
        combined_paths: list[Path] = []
        idx = 1
        for section in (sheet_a_out / "stickers", sheet_b_out / "stickers"):
            for src in sorted(section.glob("*.png")):
                dst = combined_work / f"{idx:02d}.png"
                shutil.copyfile(src, dst)
                combined_paths.append(dst)
                idx += 1

        if len(combined_paths) != 12:
            result = {
                "ok": False,
                "reason": "unexpected_sticker_count",
                "count": len(combined_paths),
                "message": "Expected 12 stickers after combining the two sheets.",
            }
            if args.keep_debug:
                _copy_debug_tree(work_root, output_dir, result)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 3

        preview_path = output_dir / "preview.jpg"
        zip_path = output_dir / "sticker-pack.zip"
        make_preview(combined_paths, preview_path, columns=4)
        _build_clean_zip(zip_path, preview_path, combined_paths)

        result = {
            "ok": True,
            "strategy": "2x6",
            "count": 12,
            "preview": str(preview_path),
            "zip": str(zip_path),
            "canvas_size": [args.canvas_size, args.canvas_size],
            "debug_kept": bool(args.keep_debug),
        }
        if args.keep_debug:
            _copy_debug_tree(work_root, output_dir, {
                **result,
                "sheet_a": res_a,
                "sheet_b": res_b,
            })

        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
