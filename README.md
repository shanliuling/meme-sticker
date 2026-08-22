# MemeSticker

English | [简体中文](./README.zh-CN.md)

Turn one uploaded image into a complete 12-piece AI sticker pack.

## Quick start

Clone or copy this folder into your host's skills directory, attach an image,
and ask: `Turn this into a 12-piece sticker pack.` The host must support image
generation; Python 3.10+ is required for extracting and packaging the stickers.

## Core idea
This version fixes the production path to **2 sheets × 6 stickers**:
- Sheet A: 3 columns × 2 rows = 6 stickers
- Sheet B: 3 columns × 2 rows = 6 stickers
- Final output: 12 transparent PNG stickers + combined preview + ZIP

This is a better compromise than:
- 1 big 12-grid sheet (too hard to extract cleanly)
- 12 independent generations (too slow / too inconsistent)

## Included files
- `SKILL.md` — the skill instructions for the agent
- `references/generation-guide.md` — generation contract for each 3x2 sheet
- `scripts/sticker_sheet_lib.py` — reusable extraction logic
- `scripts/extract_sticker_sheet.py` — per-sheet extractor for a 3x2 sticker sheet
- `scripts/package_sticker_pack.py` — combines two extracted sheets into one 12-pack ZIP
- `scripts/requirements.txt` — Python dependencies

## Runtime preparation

The skill requires **Python 3.10+**. It tries `python`, `py -3`, and `python3` on Windows, or `python3` and `python` on macOS/Linux, and verifies that the selected interpreter is Python 3.10 or newer.


Before checking packages, the agent verifies the Python version with:

```text
<python-command> -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)"
```

Before packaging, it checks for NumPy and Pillow:

```text
<python-command> -c "import numpy, PIL"
```

If either dependency is missing, the skill automatically installs the bundled
requirements with the same interpreter:

```text
<python-command> -m pip install -r "scripts/requirements.txt"
```

## Main tool call

The packaging command is intentionally shown on one line so it can be adapted to
PowerShell, Command Prompt, Bash, or zsh without shell-specific continuation
characters.

### Windows PowerShell

```powershell
python scripts/package_sticker_pack.py --sheet-a "C:\path\to\sheet-a.png" --sheet-b "C:\path\to\sheet-b.png" --output-dir "C:\path\to\output"
```

If `python` is unavailable, use `py -3` instead.

### macOS or Linux

```bash
python3 scripts/package_sticker_pack.py --sheet-a "/abs/path/sheet-a.png" --sheet-b "/abs/path/sheet-b.png" --output-dir "/abs/path/output"
```


## Release behavior
Packaging includes edge cleanup and keeps the user-facing output simple. By default the output folder contains only `preview.jpg` and `sticker-pack.zip`. Intermediate Sheet A / Sheet B extraction files are stored in a hidden work directory inside the selected output directory and deleted automatically. This avoids requiring access to the operating system's temporary directory. Use `--keep-debug` only when developing or diagnosing a failed pack.

## User-facing output
By default the output directory is intentionally minimal:

```text
output/
├── preview.jpg
└── sticker-pack.zip
```

The ZIP contains only:

```text
sticker-pack.zip
├── preview.jpg
└── stickers/
    ├── 01.png
    ├── 02.png
    ├── ...
    └── 12.png
```

Use `--keep-debug` only when developing or diagnosing extraction problems.
