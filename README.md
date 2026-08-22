<div align="center">

# MemeSticker 🐾

### One image in, 12 usable stickers out.

**Turn pets, selfies, characters, toys — almost anything — into a complete AI chat sticker pack.**

一张图进去，12 张能用的表情包出来。

[![skills.sh](https://skills.sh/b/shanliuling/meme-sticker)](https://skills.sh/shanliuling/meme-sticker)
[![GitHub stars](https://img.shields.io/github/stars/shanliuling/meme-sticker?style=flat)](https://github.com/shanliuling/meme-sticker/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)

**English** · [简体中文](./README.zh-CN.md)

</div>

---

## ✨ Not just a sticker sheet

Most AI image tools stop after generating one big sticker sheet.

**MemeSticker goes one step further.** It generates the set, separates every sticker, removes the key background, cleans edge color spill, normalizes the canvas, and packages everything for you.

You get **12 individual transparent PNG stickers**, not just one preview image.

- 🎨 AI-generated reactions, captions, poses, and decorations
- ✂️ Automatic sticker extraction
- 🪄 Transparent background + edge cleanup
- 📐 Consistent 512 × 512 output
- 📦 Preview + ready-to-use ZIP
- ⚡ Only 2 image generations for the full 12-piece pack

---

## ⚡ 30 seconds to start

Install with the open Agent Skills CLI:

```bash
npx skills add shanliuling/meme-sticker
```

Then upload an image and simply say:

> **Turn this into a cute sticker pack.**

Or be more specific:

> Make 12 sarcastic reaction stickers from this character.

> Turn this pet photo into a work-chat meme pack.

> 把这张图做成一套打工人表情包。

> 给这个角色做一套可爱聊天贴纸。

No need to write 12 prompts manually. MemeSticker plans the full reaction set for you.

---

## 🧩 Anything can become a meme pack

| 🐶 Pets | 🤳 Selfies | 🎮 Characters | 🧸 Toys & mascots |
| --- | --- | --- | --- |
| Dogs, cats, rabbits... | Portraits and selfies | Anime, game and OC characters | Plushies, mascots, objects |

As long as the subject is visually recognizable, MemeSticker can turn it into a consistent sticker set.

---

## 🎁 What you get

```text
output/
├── preview.jpg
└── sticker-pack.zip
```

Inside the ZIP:

```text
sticker-pack.zip
├── preview.jpg
└── stickers/
    ├── 01.png
    ├── 02.png
    ├── ...
    └── 12.png
```

Each sticker is exported as an individual transparent PNG, ready for you to import into the messaging app or workflow of your choice.

---

## 🧠 Why 2 × 6?

MemeSticker uses a fixed production strategy:

```text
1 source image
      ↓
Sheet A · 6 stickers
      +
Sheet B · 6 stickers
      ↓
Automatic extraction
      ↓
Background removal + edge cleanup
      ↓
12 transparent PNGs
      ↓
Preview + ZIP
```

Why not one giant 12-grid image? It is harder to separate cleanly and gives each sticker less room.

Why not generate 12 images one by one? It is slower and character/style consistency drifts more easily.

**2 × 6 is the practical middle ground: fast enough, consistent enough, and much easier to extract cleanly.**

---

## 📦 Manual installation

If you do not use the `skills` CLI, clone this repository and copy the folder into your agent's skills directory:

```bash
git clone https://github.com/shanliuling/meme-sticker.git
```

The host agent must support **image generation or image editing**. MemeSticker uses the host's image model to create the sticker sheets, while the bundled Python scripts handle extraction, transparency cleanup, normalization, and packaging.

---

## ⚙️ Requirements

- Agent Skills-compatible host
- Image generation / image editing capability
- Python **3.10+**
- NumPy and Pillow

If NumPy or Pillow is missing, the skill can install the required packages from `scripts/requirements.txt` using the selected Python interpreter. Network / pip access may therefore be required on first run.

---

## 🛠 What's inside

```text
meme-sticker/
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── references/
│   └── generation-guide.md
└── scripts/
    ├── package_sticker_pack.py
    ├── extract_sticker_sheet.py
    ├── sticker_sheet_lib.py
    └── requirements.txt
```

The image model owns the creative work: captions, typography, poses, expressions, and decorations.

The Python tools only handle the deterministic production work: splitting, background extraction, de-spill, normalization, preview generation, and ZIP packaging.

---

## ⚠️ Limitations

- Character consistency still depends on the host image model.
- AI-generated text may occasionally contain spelling errors.
- Very complex subjects or backgrounds can reduce extraction quality.
- MemeSticker outputs standard transparent PNG files; importing them into WeChat, QQ, Telegram, or other apps is handled by the user.

---

## ❤️ Why this exists

AI can already make great sticker sheets. The annoying part is everything after that: cropping, removing backgrounds, fixing ugly color spill, resizing, and exporting every sticker one by one.

**MemeSticker turns that whole process into one reusable Agent Skill.**

If you find it useful, a ⭐ helps more people discover the project.

## 📄 License

MIT © MemeSticker contributors
