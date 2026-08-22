#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import shutil
import zipfile
from collections import deque
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Tuple

import numpy as np
from PIL import Image, ImageFilter


@dataclass
class BoundaryDiagnostic:
    axis: str
    index: int
    ideal: float
    chosen: int
    density: float
    search_start: int
    search_end: int


@dataclass
class StickerDiagnostic:
    index: int
    cell_bbox: Tuple[int, int, int, int]
    content_bbox_in_cell: Tuple[int, int, int, int] | None
    foreground_fraction: float
    edge_contact_fraction: float
    alpha_method: str | None = None
    normalized_bbox: Tuple[int, int, int, int] | None = None
    path: str | None = None


def estimate_background(arr: np.ndarray, band_fraction: float = 0.035) -> np.ndarray:
    h, w, _ = arr.shape
    band = max(1, min(24, int(round(min(h, w) * band_fraction))))
    samples = np.concatenate([
        arr[:band, :, :3].reshape(-1, 3),
        arr[-band:, :, :3].reshape(-1, 3),
        arr[:, :band, :3].reshape(-1, 3),
        arr[:, -band:, :3].reshape(-1, 3),
    ], axis=0)
    return np.median(samples.astype(np.float32), axis=0)


def foreground_mask(arr: np.ndarray, threshold: float) -> Tuple[np.ndarray, np.ndarray]:
    rgb = arr[:, :, :3].astype(np.float32)
    bg = estimate_background(arr)
    dist = np.linalg.norm(rgb - bg[None, None, :], axis=2)
    if arr.shape[2] == 4:
        alpha = arr[:, :, 3]
        edge_alpha = np.concatenate([alpha[0], alpha[-1], alpha[:, 0], alpha[:, -1]])
        if float(np.mean(edge_alpha < 32)) > 0.25:
            return alpha > 24, bg
    return dist > threshold, bg


def smooth_1d(values: np.ndarray, radius: int) -> np.ndarray:
    if radius <= 0:
        return values.astype(np.float64)
    k = radius * 2 + 1
    kernel = np.ones(k, dtype=np.float64) / k
    return np.convolve(values.astype(np.float64), kernel, mode="same")


def pick_boundary(density: np.ndarray, ideal: float, cell_span: float,
                  search_fraction: float, smooth_radius: int,
                  axis: str, index: int) -> BoundaryDiagnostic:
    n = len(density)
    radius = max(4, int(round(cell_span * search_fraction)))
    start = max(1, int(round(ideal)) - radius)
    end = min(n - 2, int(round(ideal)) + radius)
    smoothed = smooth_1d(density, smooth_radius)
    candidates = np.arange(start, end + 1)
    local = smoothed[candidates]
    loc_penalty = np.abs(candidates - ideal) / max(1.0, radius)
    score = local + 0.012 * loc_penalty
    best = int(candidates[int(np.argmin(score))])
    return BoundaryDiagnostic(axis, index, float(ideal), best, float(smoothed[best]), start, end)


def find_boundaries(mask: np.ndarray, rows: int, cols: int, search_fraction: float):
    h, w = mask.shape
    col_density = mask.mean(axis=0)
    row_density = mask.mean(axis=1)
    cell_w, cell_h = w / cols, h / rows
    xs = [pick_boundary(col_density, w*k/cols, cell_w, search_fraction,
                        max(1, int(round(cell_w*0.012))), "x", k)
          for k in range(1, cols)]
    ys = [pick_boundary(row_density, h*k/rows, cell_h, search_fraction,
                        max(1, int(round(cell_h*0.012))), "y", k)
          for k in range(1, rows)]
    return xs, ys


def bbox_from_mask(mask: np.ndarray):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max())+1, int(ys.max())+1


def edge_contact_fraction(mask: np.ndarray, guard_fraction: float = 0.035) -> float:
    h, w = mask.shape
    gx = max(1, int(round(w * guard_fraction)))
    gy = max(1, int(round(h * guard_fraction)))
    strips = np.concatenate([mask[:gy].ravel(), mask[-gy:].ravel(), mask[:, :gx].ravel(), mask[:, -gx:].ravel()])
    return float(strips.mean()) if strips.size else 0.0


def validate_geometry(xdiag, ydiag, width, height, rows, cols, max_gutter_density):
    reasons = []
    for d in [*xdiag, *ydiag]:
        if d.density > max_gutter_density:
            reasons.append(f"{d.axis}-gutter-{d.index} is too busy (density={d.density:.4f})")
    xs = [0] + [d.chosen for d in xdiag] + [width]
    ys = [0] + [d.chosen for d in ydiag] + [height]
    ew, eh = width/cols, height/rows
    for i, span in enumerate(np.diff(xs), 1):
        if span < ew*0.65 or span > ew*1.35:
            reasons.append(f"column-{i} width is implausible ({span}px)")
    for i, span in enumerate(np.diff(ys), 1):
        if span < eh*0.65 or span > eh*1.35:
            reasons.append(f"row-{i} height is implausible ({span}px)")
    return reasons


def connected_edge_background(rgb: np.ndarray, bg: np.ndarray, tolerance: float) -> np.ndarray:
    h, w = rgb.shape[:2]
    dist = np.linalg.norm(rgb.astype(np.float32) - bg[None, None, :], axis=2)
    eligible = dist <= tolerance
    seen = np.zeros((h, w), dtype=np.uint8)
    q = deque()
    for x in range(w):
        if eligible[0, x]: seen[0, x] = 1; q.append((0, x))
        if eligible[h-1, x] and not seen[h-1, x]: seen[h-1, x] = 1; q.append((h-1, x))
    for y in range(h):
        if eligible[y, 0] and not seen[y, 0]: seen[y, 0] = 1; q.append((y, 0))
        if eligible[y, w-1] and not seen[y, w-1]: seen[y, w-1] = 1; q.append((y, w-1))
    while q:
        y, x = q.popleft()
        if x > 0 and eligible[y, x-1] and not seen[y, x-1]: seen[y, x-1] = 1; q.append((y, x-1))
        if x+1 < w and eligible[y, x+1] and not seen[y, x+1]: seen[y, x+1] = 1; q.append((y, x+1))
        if y > 0 and eligible[y-1, x] and not seen[y-1, x]: seen[y-1, x] = 1; q.append((y-1, x))
        if y+1 < h and eligible[y+1, x] and not seen[y+1, x]: seen[y+1, x] = 1; q.append((y+1, x))
    return seen.astype(bool)


def dilate_mask(mask: np.ndarray, radius: int) -> np.ndarray:
    if radius <= 0:
        return mask.astype(np.uint8) * 255
    img = Image.fromarray(mask.astype(np.uint8) * 255, mode="L")
    size = max(3, radius * 2 + 1)
    if size % 2 == 0:
        size += 1
    return np.array(img.filter(ImageFilter.MaxFilter(size=size)))


def erode_mask(mask: np.ndarray, radius: int) -> np.ndarray:
    if radius <= 0:
        return mask.astype(bool)
    img = Image.fromarray(mask.astype(np.uint8) * 255, mode="L")
    size = max(3, radius * 2 + 1)
    if size % 2 == 0:
        size += 1
    return np.array(img.filter(ImageFilter.MinFilter(size=size))) > 0


def _remove_key_color_spill(foreground: np.ndarray, rgb: np.ndarray, bg: np.ndarray,
                            band_radius: int = 8, min_chroma: float = 14.0,
                            min_cosine: float = 0.72, max_bg_distance: float = 160.0) -> np.ndarray:
    """Remove chroma-key shadow / antialias spill only near the outer silhouette.

    AI image models often draw a soft cyan/green shadow around an otherwise white
    die-cut border. A simple flood-fill removes the flat key background but leaves
    that colored halo. We detect pixels whose chroma points in the same direction
    as the key color, but only in a narrow band along the foreground boundary.
    This avoids damaging blue/green details inside the sticker.
    """
    if not foreground.any():
        return foreground
    inner = erode_mask(foreground, band_radius)
    boundary_band = foreground & ~inner

    rgbf = rgb.astype(np.float32)
    bgf = bg.astype(np.float32)
    bg_vec = bgf - float(np.mean(bgf))
    bg_norm = float(np.linalg.norm(bg_vec))
    if bg_norm < 6.0:
        return foreground

    means = rgbf.mean(axis=2, keepdims=True)
    vec = rgbf - means
    norms = np.linalg.norm(vec, axis=2)
    cosine = np.zeros_like(norms, dtype=np.float32)
    valid = norms > 1e-6
    cosine[valid] = (vec[valid] @ bg_vec) / (norms[valid] * bg_norm)
    dist = np.linalg.norm(rgbf - bgf[None, None, :], axis=2)

    spill = boundary_band & (norms > min_chroma) & (cosine > min_cosine) & (dist < max_bg_distance)
    return foreground & ~spill


def drop_small_edge_fragments(mask: np.ndarray, dominant_ratio: float = 0.025, edge_margin_fraction: float = 0.02) -> np.ndarray:
    h, w = mask.shape
    seen = np.zeros((h, w), dtype=np.uint8)
    comps = []
    for y in range(h):
        for x in range(w):
            if not mask[y, x] or seen[y, x]:
                continue
            q = deque([(y, x)])
            seen[y, x] = 1
            pixels = []
            minx = maxx = x
            miny = maxy = y
            while q:
                cy, cx = q.popleft()
                pixels.append((cy, cx))
                minx, maxx = min(minx, cx), max(maxx, cx)
                miny, maxy = min(miny, cy), max(maxy, cy)
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        if dx == 0 and dy == 0:
                            continue
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not seen[ny, nx]:
                            seen[ny, nx] = 1
                            q.append((ny, nx))
            comps.append((pixels, len(pixels), (minx, miny, maxx + 1, maxy + 1)))
    if not comps:
        return mask
    dominant = max(area for _, area, _ in comps)
    margin_x = max(1, int(round(w * edge_margin_fraction)))
    margin_y = max(1, int(round(h * edge_margin_fraction)))
    out = np.zeros_like(mask, dtype=bool)
    for pixels, area, (l, t, r, b) in comps:
        touches_edge = l <= margin_x or t <= margin_y or r >= w - margin_x or b >= h - margin_y
        if touches_edge and area < dominant * dominant_ratio:
            continue
        for py, px in pixels:
            out[py, px] = True
    return out


def _soft_key_alpha(rgb: np.ndarray, bg: np.ndarray, low: float = 10.0, high: float = 72.0) -> np.ndarray:
    """Estimate a soft alpha matte from distance to a known flat key background.

    This is designed for AI-generated sticker sheets where the key color is
    intentionally excluded from the sticker artwork. It gives us a smooth
    antialiased edge instead of a hard binary cut.
    """
    dist = np.linalg.norm(rgb.astype(np.float32) - bg[None, None, :], axis=2)
    x = np.clip((dist - low) / max(1e-6, high - low), 0.0, 1.0)
    # Smoothstep reduces stair-stepping and gives a more natural matte.
    x = x * x * (3.0 - 2.0 * x)
    return x


def _unmix_key_color(rgb: np.ndarray, bg: np.ndarray, alpha01: np.ndarray) -> np.ndarray:
    """Recover foreground color from C = aF + (1-a)B for edge pixels.

    This is the important de-spill step. It removes cyan/green/magenta
    contamination from antialiased pixels instead of simply making them white.
    """
    c = rgb.astype(np.float32)
    b = bg.astype(np.float32)[None, None, :]
    a = alpha01[..., None].astype(np.float32)
    safe = np.maximum(a, 0.08)
    f = (c - (1.0 - a) * b) / safe
    f = np.clip(f, 0.0, 255.0)
    # Fully opaque pixels should keep their original exact color.
    opaque = a[..., 0] >= 0.985
    f[opaque] = c[opaque]
    return f.astype(np.uint8)


def _cleanup_alpha(alpha_u8: np.ndarray) -> np.ndarray:
    """Small morphological / blur cleanup without inflating the silhouette."""
    im = Image.fromarray(alpha_u8, mode="L")
    # Median removes isolated pinholes/specks; tiny blur keeps antialiasing smooth.
    im = im.filter(ImageFilter.MedianFilter(size=3)).filter(ImageFilter.GaussianBlur(radius=0.35))
    arr = np.array(im)
    arr[arr < 4] = 0
    arr[arr > 251] = 255
    return arr


def extract_alpha(cell: Image.Image, bg_tolerance: float, white_fallback_threshold: float,
                  white_border_radius: int) -> Tuple[Image.Image, str]:
    arr = np.array(cell.convert("RGBA"))
    rgb = arr[:, :, :3]
    alpha = arr[:, :, 3]

    edge_alpha = np.concatenate([alpha[0], alpha[-1], alpha[:, 0], alpha[:, -1]])
    if float(np.mean(edge_alpha < 32)) > 0.20:
        # Already transparent: only do a very small alpha cleanup.
        out = arr.copy()
        out[:, :, 3] = _cleanup_alpha(alpha)
        return Image.fromarray(out), "existing-alpha-cleanup"

    bg = estimate_background(arr, band_fraction=0.06)
    lum = float(np.mean(bg))
    chroma = float(np.max(bg) - np.min(bg))
    is_near_white = lum > 235 and chroma < 18

    if not is_near_white:
        # Preferred v1.2 path: soft chroma-key matte + mathematical decontamination.
        # The generation contract guarantees one flat key color that is not reused
        # inside sticker artwork, so this is both faster and cleaner than semantic
        # segmentation for text + character + decorations.
        alpha01 = _soft_key_alpha(rgb, bg, low=10.0, high=max(58.0, bg_tolerance * 1.65))

        # Force edge-connected near-key background to fully transparent so tiny
        # compression/noise variations in the sheet background cannot survive.
        edge_bg = connected_edge_background(rgb, bg, max(bg_tolerance, 48.0))
        alpha01[edge_bg] = 0.0

        alpha_u8 = np.clip(np.round(alpha01 * 255.0), 0, 255).astype(np.uint8)
        alpha_u8 = _cleanup_alpha(alpha_u8)
        alpha01_clean = alpha_u8.astype(np.float32) / 255.0

        clean_rgb = _unmix_key_color(rgb, bg, alpha01_clean)
        out = arr.copy()
        out[:, :, :3] = clean_rgb
        out[:, :, 3] = np.minimum(alpha_u8, alpha)
        return Image.fromarray(out), "soft-key-matte+despill"

    # Legacy fallback only. White backgrounds are fundamentally ambiguous when
    # the sticker itself contains a white outline, so generation should avoid them.
    dist = np.linalg.norm(rgb.astype(np.float32) - bg[None, None, :], axis=2)
    core = dist > white_fallback_threshold
    core = drop_small_edge_fragments(core)
    expanded = dilate_mask(core, white_border_radius)
    alpha_img = Image.fromarray(expanded, mode="L").filter(ImageFilter.GaussianBlur(radius=0.45))
    new_alpha = _cleanup_alpha(np.array(alpha_img))
    out = arr.copy()
    out[:, :, 3] = np.minimum(new_alpha, alpha)
    return Image.fromarray(out), "white-background-fallback"

def normalize_sticker(sticker: Image.Image, canvas_size: int, content_fraction: float) -> Tuple[Image.Image, Tuple[int,int,int,int] | None]:
    rgba = sticker.convert("RGBA")
    a = np.array(rgba)[:, :, 3]
    bbox = bbox_from_mask(a > 16)
    canvas = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    if bbox is None:
        return canvas, None
    l, t, r, b = bbox
    crop = rgba.crop((l, t, r, b))
    cw, ch = crop.size
    target = max(1, int(round(canvas_size * content_fraction)))
    scale = min(target / max(1, cw), target / max(1, ch))
    nw, nh = max(1, int(round(cw * scale))), max(1, int(round(ch * scale)))
    crop = crop.resize((nw, nh), Image.Resampling.LANCZOS)
    x = (canvas_size - nw) // 2
    y = (canvas_size - nh) // 2
    canvas.alpha_composite(crop, (x, y))
    return canvas, (x, y, x+nw, y+nh)


def make_preview(sticker_paths: List[Path], out_path: Path, columns: int = 4, tile: int = 320):
    thumbs = [Image.open(p).convert("RGBA") for p in sticker_paths]
    if not thumbs:
        return
    rows = math.ceil(len(thumbs) / columns)
    preview = Image.new("RGBA", (columns*tile, rows*tile), (248, 248, 246, 255))
    for i, im in enumerate(thumbs):
        bg = Image.new("RGBA", (tile, tile), (248, 248, 246, 255))
        small = im.resize((tile, tile), Image.Resampling.LANCZOS)
        bg.alpha_composite(small)
        preview.alpha_composite(bg, ((i % columns)*tile, (i // columns)*tile))
    preview.convert("RGB").save(out_path, quality=94)


def build_zip(zip_path: Path, preview_path: Path, extra_files: List[Tuple[Path, str]], sticker_paths: List[Path]):
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        if preview_path.exists():
            zf.write(preview_path, arcname=preview_path.name)
        for fs_path, arcname in extra_files:
            if fs_path.exists():
                zf.write(fs_path, arcname=arcname)
        for p in sticker_paths:
            zf.write(p, arcname=f"stickers/{p.name}")


def split_sheet_to_dir(
    input_image: Path,
    output_dir: Path,
    rows: int = 2,
    cols: int = 3,
    foreground_threshold: float = 30.0,
    search_fraction: float = 0.24,
    max_gutter_density: float = 0.075,
    max_edge_contact: float = 0.22,
    min_cell_foreground: float = 0.01,
    background_tolerance: float = 42.0,
    white_fallback_threshold: float = 20.0,
    white_border_fraction: float = 0.026,
    canvas_size: int = 512,
    content_fraction: float = 0.82,
    force: bool = False,
    preview_columns: int | None = None,
) -> dict:
    input_path = Path(input_image).resolve()
    output_dir = Path(output_dir).resolve()
    if not input_path.exists():
        return {"ok": False, "reason": "input_missing", "message": str(input_path)}

    image = Image.open(input_path).convert("RGBA")
    arr = np.array(image)
    mask, bg = foreground_mask(arr, foreground_threshold)
    h, w = mask.shape
    if w < cols * 80 or h < rows * 80:
        return {"ok": False, "reason": "image_too_small", "message": f"Sheet is only {w}x{h}."}

    xdiag, ydiag = find_boundaries(mask, rows, cols, search_fraction)
    reasons = validate_geometry(xdiag, ydiag, w, h, rows, cols, max_gutter_density)
    xs = [0] + [d.chosen for d in xdiag] + [w]
    ys = [0] + [d.chosen for d in ydiag] + [h]

    diagnostics: List[StickerDiagnostic] = []
    cells = []
    idx = 1
    for r in range(rows):
        for c in range(cols):
            l, t, rr, bb = xs[c], ys[r], xs[c+1], ys[r+1]
            cell_mask = mask[t:bb, l:rr]
            bbox = bbox_from_mask(cell_mask)
            fg = float(cell_mask.mean()) if cell_mask.size else 0.0
            edge = edge_contact_fraction(cell_mask)
            if bbox is None or fg < min_cell_foreground:
                reasons.append(f"sticker-{idx:02d} appears empty")
            if edge > max_edge_contact:
                reasons.append(f"sticker-{idx:02d} content is too close to a cell edge (edge_contact={edge:.4f})")
            diagnostics.append(StickerDiagnostic(idx, (l,t,rr,bb), bbox, fg, edge))
            cells.append((idx, image.crop((l,t,rr,bb))))
            idx += 1

    result = {
        "ok": not reasons,
        "input_image": str(input_path),
        "sheet_size": [w, h],
        "background_rgb": [round(float(v), 2) for v in bg],
        "cuts": {"x": [d.chosen for d in xdiag], "y": [d.chosen for d in ydiag]},
        "boundary_diagnostics": [asdict(d) for d in [*xdiag, *ydiag]],
    }
    if reasons and not force:
        result.update({
            "reason": "unsafe_sheet_layout",
            "message": "The sheet is not safe enough for automatic extraction. Regenerate this sheet with larger gutters and a flat background, or rerun with force for testing.",
            "problems": reasons,
            "sticker_diagnostics": [asdict(d) for d in diagnostics],
        })
        return result

    # Safety: never delete an arbitrary user-supplied output directory.
    # A directory created by this extractor is marked so later runs can clean
    # only files that belong to MemeSticker. Existing non-empty unmarked
    # directories are refused instead of being removed.
    marker_path = output_dir / ".meme-sticker-managed"
    managed_names = {
        ".meme-sticker-managed",
        "stickers",
        "source-sheet.png",
        "preview.jpg",
        "split-report.json",
        "sticker-pack.zip",
    }

    if output_dir.exists():
        entries = list(output_dir.iterdir())
        if entries and not marker_path.exists():
            result.update({
                "ok": False,
                "reason": "unsafe_output_dir",
                "message": (
                    "Refusing to overwrite a non-empty output directory that was not "
                    "created by MemeSticker. Choose a new/empty output directory."
                ),
            })
            return result

        # Clean only MemeSticker-managed artifacts; preserve anything unknown.
        for child in entries:
            if child.name not in managed_names:
                continue
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
    else:
        output_dir.mkdir(parents=True, exist_ok=True)

    marker_path.touch()
    stickers_dir = output_dir / "stickers"
    stickers_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(input_path, output_dir / "source-sheet.png")

    paths = []
    alpha_methods = []
    for (i, cell), diag in zip(cells, diagnostics):
        radius = max(3, int(round(min(cell.size) * white_border_fraction)))
        extracted, method = extract_alpha(cell, background_tolerance, white_fallback_threshold, radius)
        normalized, nbbox = normalize_sticker(extracted, canvas_size, content_fraction)
        out_path = stickers_dir / f"{i:02d}_sticker.png"
        normalized.save(out_path)
        diag.alpha_method = method
        diag.normalized_bbox = nbbox
        diag.path = str(out_path)
        paths.append(out_path)
        alpha_methods.append(method)

    preview_path = output_dir / "preview.jpg"
    make_preview(paths, preview_path, columns=preview_columns or cols)
    report_path = output_dir / "split-report.json"
    zip_path = output_dir / "sticker-pack.zip"
    result.update({
        "ok": True,
        "forced": bool(reasons),
        "warnings": reasons,
        "preview": str(preview_path),
        "source_sheet": str(output_dir / "source-sheet.png"),
        "stickers_dir": str(stickers_dir),
        "zip": str(zip_path),
        "report": str(report_path),
        "count": len(paths),
        "canvas_size": [canvas_size, canvas_size],
        "alpha_methods": alpha_methods,
        "sticker_diagnostics": [asdict(d) for d in diagnostics],
    })
    report_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    build_zip(zip_path, preview_path, [
        (output_dir / "source-sheet.png", "source-sheet.png"),
        (report_path, "split-report.json"),
    ], paths)
    return result
