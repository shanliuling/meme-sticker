<div align="center">

# MemeSticker 🐾

<p>
  <a href="./assets/sticker-ok-selfie.png"><img src="./assets/sticker-ok-selfie.png" width="18%" alt="Transparent selfie sticker saying OK" /></a>
  <a href="./assets/sticker-ok-cat.png"><img src="./assets/sticker-ok-cat.png" width="18%" alt="Transparent cat sticker saying OK" /></a>
  <a href="./assets/sticker-nice-character.png"><img src="./assets/sticker-nice-character.png" width="18%" alt="Transparent character sticker saying NICE" /></a>
</p>

### One image → a complete AI sticker pack.

**Turn pets, selfies, characters, toys — almost anything — into a complete set of chat stickers.**

**MemeSticker is not tied to any fixed model or platform. It is an open-source Skill you can install into any Agent.**

As long as the host supports Skills and image generation/editing, MemeSticker can turn one source image into a complete sticker pack.

⚡ **One generation → a full sticker pack**  
💰 **Uses fewer image-generation credits than generating stickers one by one**  
✂️ **Automatically splits the generated sheet into individual stickers**  
🪄 **Automatically removes backgrounds and exports transparent PNGs**  
📦 **Outputs a preview plus a ready-to-use `sticker-pack.zip`**

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

Most AI sticker workflows generate stickers one by one. MemeSticker takes a different approach:

```text
1 source image
      ↓
1 image-generation call
      ↓
a complete sticker sheet
      ↓
automatic splitting + background removal
      ↓
individual transparent PNG stickers
```

That makes the workflow faster, easier to automate, and more credit-efficient.

### Built for Agents, not one model

MemeSticker is a Skill rather than a model-specific sticker feature. You can take the same workflow to compatible Agents instead of rebuilding it around one image provider or one chat product.

### Generate the whole pack at once

Instead of spending one generation on every sticker, MemeSticker asks the image model to create a complete sheet in one call, then handles the rest locally.

### Automatic post-processing

After generation, MemeSticker automatically splits the sheet, removes backgrounds, and exports individual transparent PNG files together with a preview and ZIP package.

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
