<div align="center">

# MemeSticker 🐾

<p>
  <a href="./assets/sticker-ok-selfie.png"><img src="./assets/sticker-ok-selfie.png" width="18%" alt="Transparent selfie sticker saying OK" /></a>
  <a href="./assets/sticker-ok-cat.png"><img src="./assets/sticker-ok-cat.png" width="18%" alt="Transparent cat sticker saying OK" /></a>
  <a href="./assets/sticker-nice-character.png"><img src="./assets/sticker-nice-character.png" width="18%" alt="Transparent character sticker saying NICE" /></a>
</p>

### One image → a full sticker pack.

**An open-source sticker-making Skill for any Agent — not tied to one model or platform.**

Generate the whole pack in one image call, then auto-split, remove backgrounds, and export transparent PNGs.

**One generation · Fewer credits · Auto split · Transparent PNG**

[![GitHub stars](https://img.shields.io/github/stars/shanliuling/meme-sticker?style=flat)](https://github.com/shanliuling/meme-sticker/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![LINUX DO](https://img.shields.io/badge/LINUX%20DO-社区友链-555?style=flat)](https://linux.do/)

**English** · [简体中文](./README.zh-CN.md)

<br/>

<img src="./assets/hero-en.jpg" width="900" alt="MemeSticker — one image to a complete sticker pack" />

</div>

---

## ✨ Why MemeSticker?

- **Agent-native** — install the Skill and reuse the same workflow across compatible Agents.
- **One call, full pack** — generate a complete sticker sheet instead of spending one image call per sticker.
- **Ready to use** — splitting, background removal, transparent PNG export, preview and ZIP are handled automatically.

---

## 🎬 Real outputs

<p align="center">
  <a href="./assets/example-girl.jpg"><img src="./assets/example-girl.jpg" width="31%" alt="Selfie sticker example" /></a>
  <a href="./assets/example-cat.jpg"><img src="./assets/example-cat.jpg" width="31%" alt="Pet sticker example" /></a>
  <a href="./assets/example-character.jpg"><img src="./assets/example-character.jpg" width="31%" alt="Character sticker example" /></a>
</p>

<div align="center">

**Selfies · Pets · Characters · Toys · Mascots · Objects**

**Captions follow your language.**

</div>

---

## ⚡ Install and use

```bash
npx skills add shanliuling/meme-sticker
```

Upload an image, then simply say:

> **Turn this into a cute sticker pack.**

Or add the theme you want:

> Make a sarcastic reaction sticker pack from this character.

> Turn this pet photo into a work-chat meme pack.

The result includes a preview and `sticker-pack.zip`, containing individual transparent PNG stickers.

> [!IMPORTANT]
> The host must support Skills plus image generation or image editing, and provide Python 3.10+. The first run may need to install NumPy and Pillow.

> [!NOTE]
> Character consistency, generated text and complex-background handling depend on the host image model. Importing the PNGs into WhatsApp, Telegram or other messaging apps is handled separately.

## 📄 License

MIT © 2026 shanliuling
