---
name: meme-sticker
description: >-
  Turn one uploaded image into a complete 12-piece chat sticker pack by generating
  two 3x2 sticker sheets, extracting transparent PNGs, normalizing their canvases,
  and packaging the result as a ZIP. Use this skill whenever a user provides a
  photo and asks for chat stickers, reaction stickers, meme stickers, custom emoji,
  or messaging-app sticker packs, including requests that use terms such as
  表情包, 贴纸包, 微信表情, QQ表情, or Telegram stickers.
compatibility: Supports Windows PowerShell, macOS, and Linux. Requires Python 3.10+; bundled Python dependencies are installed automatically when missing.
---

# MemeSticker

Create a complete 12-piece sticker pack from a single user image.

The subject may be a person, pet, toy, mascot, object, or another recognizable subject.

## Fixed production strategy
This skill does **not** use 12 separate generations.
This skill also does **not** rely on one single 12-grid sheet as the main path.

The required strategy is fixed:
- generate **2 sheets**
- each sheet contains **6 stickers**
- each sheet uses a **3-column x 2-row** layout
- total output is **12 stickers**

This is the default and only path unless the user explicitly asks for something else.

## Desired result
Return:
- a combined 12-sticker preview image
- one ZIP containing all 12 transparent PNG files

Each final sticker should be:
- transparent PNG
- 512 x 512 canvas by default
- consistent visual size across the set
- no rectangular white card background
- subject + caption + small decorations preserved together

## Workflow

### 1) Understand the subject
Use the uploaded image as the visual reference.
Preserve the subject's important identity traits.

For people, preserve face, hairstyle, glasses, clothing, and distinctive accessories.
For pets, preserve species/breed cues, fur color, face shape, ears, markings, and accessories.
For objects / toys / mascots, preserve shape, proportions, color, and iconic details.

### 2) Plan 12 reactions internally
Plan a useful 12-sticker set.
Do not ask the user to manually provide all 12 captions unless they explicitly want control.

Let the image model create the short captions, text treatment, poses, and small decorative details.
Prefer short chat-friendly captions.

Caption language rules:
- Follow the language used by the user or the current conversation.
- If the user explicitly requests a language, use that language.
- Keep all 12 stickers in the same language unless the user asks otherwise.

### 3) Generate Sheet A (first 6 stickers)
Use the generation contract in `references/generation-guide.md`.

Generate one **pure sticker sheet** with these requirements:
- exactly 6 stickers
- exactly 3 columns x 2 rows
- landscape canvas
- clean, sticker-like style
- one flat continuous key background color across the whole sheet
- each sticker fully contained inside its own territory
- leave clear empty gutters between stickers
- output only the sheet artwork, nothing else

Do **not** generate chat UI, app UI, posters, cards, headers, or download panels.

### 4) Generate Sheet B (remaining 6 stickers)
Generate the second **3x2 sheet** for the remaining 6 reactions.
Keep it visually consistent with Sheet A.

When the available image tool supports style/reference continuity, use Sheet A as an extra style reference.
Keep these elements consistent across both sheets:
- subject identity
- art style
- white outline / die-cut sticker feel
- caption energy and overall tone
- key background approach
- relative sticker scale and spacing

### 5) Extract and package the final 12-sticker pack
After both sheets exist, prepare the Python runtime before packaging. This keeps
the workflow self-recovering on a new machine instead of failing on a missing
interpreter alias or dependency.

1. Resolve the directory containing this `SKILL.md` as `<skill-root>`.
2. Find a working Python **3.10+** command. On Windows, try `python`, `py -3`, then `python3`. On macOS or Linux, try `python3`, then `python`.
   Validate each candidate with:

   ```text
   <python-command> -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)"
   ```

   Use the first command that exits successfully. Refer to it as `<python-command>` below.
3. Check the runtime dependencies with:

   ```text
   <python-command> -c "import numpy, PIL"
   ```

4. If the dependency check fails, install the bundled requirements immediately:

   ```text
   <python-command> -m pip install -r "<skill-root>/scripts/requirements.txt"
   ```

   Continue automatically after installation. Ask the user only if the execution
   environment requires explicit approval. If installation fails, report the
   exact error instead of attempting to package incomplete output.
5. Run the dependency check again. Once it passes, package the stickers with one
   shell-independent line:

   ```text
   <python-command> "<skill-root>/scripts/package_sticker_pack.py" --sheet-a "/absolute/path/to/sheet-a.png" --sheet-b "/absolute/path/to/sheet-b.png" --output-dir "/absolute/path/to/sticker-pack-output"
   ```

Replace `<python-command>` and `<skill-root>` with the resolved values. Do not copy Bash
line continuations into PowerShell or assume that `python3` exists on Windows.

The tool will:
- use a temporary hidden work directory inside the output directory for Sheet A / Sheet B
- split Sheet A as a 3x2 sheet
- split Sheet B as a 3x2 sheet
- remove the key background / preserve sticker content
- clean cyan/green/magenta key-color spill around sticker edges
- normalize all 12 stickers to a consistent 512x512 transparent canvas
- create a combined 12-piece preview
- create one ZIP package containing only `stickers/01.png` ... `stickers/12.png` and `preview.jpg`
- delete intermediate work files automatically after success

### 6) Retry behavior
If either sheet cannot be safely extracted, regenerate **only the failing sheet**.
Do not throw away the successful sheet.

When regenerating the failing sheet, strengthen these constraints:
- make each sticker slightly smaller
- increase empty gutters
- keep all text farther away from sticker edges
- keep all decorations attached to the same sticker
- keep the background perfectly flat and continuous

### 7) Return the result
On success, return only the user-facing artifacts:
- `preview.jpg`
- `sticker-pack.zip`

Do not expose Sheet A / Sheet B work folders, extraction diagnostics, or JSON reports unless the user explicitly asks for debug output.

Keep the final response short.

## Do not
- do not default to 12 single-image generations
- do not default to one 12-grid sheet as the main production path
- do not generate surrounding UI / promo layouts
- do not package failed / unsafe extraction results
- do not hard-code one fixed list of captions
