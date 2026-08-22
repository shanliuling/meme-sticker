<div align="center">

# MemeSticker 🐾

### 一张图进去，12 张能用的表情包出来。

**宠物、自拍、角色、玩偶，几乎任何主体都能变成一整套 AI 聊天表情。**

One image in, 12 usable stickers out.

[![skills.sh](https://skills.sh/b/shanliuling/meme-sticker)](https://skills.sh/shanliuling/meme-sticker)
[![GitHub stars](https://img.shields.io/github/stars/shanliuling/meme-sticker?style=flat)](https://github.com/shanliuling/meme-sticker/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)

[English](./README.md) · **简体中文**

</div>

---

## ✨ 不只是一张表情包大图

很多 AI 生图工具做到这里就结束了：生成一张 12 宫格表情包大图。

**MemeSticker 会继续把后面的脏活也做完。**

它会自动生成整套表情、拆分每一张、去掉色键背景、清理边缘溢色、统一尺寸，最后直接打包。

最终拿到的是 **12 张独立透明 PNG**，不是只有一张预览图。

- 🎨 AI 自动设计表情、文案、动作和小装饰
- ✂️ 自动识别并拆分每张表情
- 🪄 自动去背景 + 边缘清理 / de-spill
- 📐 默认统一为 512 × 512
- 📦 自动生成合集预览 + ZIP
- ⚡ 整套 12 张只需要 2 次生图

---

## ⚡ 30 秒开始

使用通用 Agent Skills CLI 安装：

```bash
npx skills add shanliuling/meme-sticker
```

然后上传一张图片，直接告诉智能体：

> **把这张图做成一套表情包。**

也可以指定主题：

> 把这只狗做成一套打工人表情包。

> 给这个角色做 12 张阴阳怪气的聊天表情。

> 把这张自拍做成可爱风微信聊天贴纸。

你不需要自己准备 12 条 Prompt，MemeSticker 会自动规划整套反应和文案。

---

## 🧩 什么都能变成 Meme Pack

| 🐶 宠物 | 🤳 自拍 / 真人 | 🎮 角色 | 🧸 玩偶 / 吉祥物 |
| --- | --- | --- | --- |
| 猫、狗、兔子... | 人像、自拍、朋友 | 二次元、游戏、OC | 毛绒玩具、吉祥物、物体 |

只要主体足够清晰、可识别，就可以尝试做成一整套表情。

---

## 🎁 最终会得到什么

```text
output/
├── preview.jpg
└── sticker-pack.zip
```

ZIP 里面是：

```text
sticker-pack.zip
├── preview.jpg
└── stickers/
    ├── 01.png
    ├── 02.png
    ├── ...
    └── 12.png
```

每张都是独立透明 PNG，可以再导入微信、QQ、Telegram 或其他聊天 / 创作工具。

---

## 🧠 为什么固定用 2 × 6？

MemeSticker 的主流程固定为：

```text
1 张原图
   ↓
Sheet A · 6 张
   +
Sheet B · 6 张
   ↓
自动拆分
   ↓
去背景 + 边缘清理
   ↓
12 张透明 PNG
   ↓
预览图 + ZIP
```

为什么不直接生成一张 12 宫格？因为每张表情空间更小，而且更难稳定拆干净。

为什么不单独生成 12 次？因为太慢，而且人物 / 角色风格更容易漂。

**2 × 6 是目前更实用的平衡点：生成够快、角色更稳、后处理也更干净。**

---

## 📦 手动安装

如果你不使用 `skills` CLI，也可以直接克隆：

```bash
git clone https://github.com/shanliuling/meme-sticker.git
```

然后把整个 `meme-sticker` 文件夹放进你的 Agent 的 Skills 目录。

宿主智能体必须本身具备 **图片生成 / 图片编辑能力**。MemeSticker 使用宿主的图片模型完成创作，Python 脚本主要负责拆图、透明化、边缘清理、尺寸统一和打包。

---

## ⚙️ 运行要求

- 支持 Agent Skills 的宿主
- 图片生成 / 图片编辑能力
- Python **3.10+**
- NumPy + Pillow

如果 NumPy 或 Pillow 缺失，Skill 可以根据 `scripts/requirements.txt` 自动安装，因此首次运行可能需要网络和 pip 权限。

---

## 🛠 项目结构

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

创意部分交给图片模型：文案、字体、动作、表情、装饰。

Python 只负责确定性的生产流程：切分、去背景、de-spill、尺寸统一、预览图和 ZIP 打包。

---

## ⚠️ 已知限制

- 角色一致性仍取决于宿主使用的图片模型。
- AI 生成文字偶尔会有错字。
- 主体或背景过于复杂时，拆分和透明化质量可能下降。
- MemeSticker 输出的是标准透明 PNG；导入微信、QQ、Telegram 等平台由用户自己完成。

---

## ❤️ 为什么做这个

AI 现在已经很会画“表情包大图”了，麻烦的是后面：裁图、抠背景、修边缘、统一尺寸、逐张导出。

**MemeSticker 就是把这些流程做成一个可以复用的 Agent Skill。**

如果这个项目对你有用，欢迎点一个 ⭐，也方便更多人看到它。

## 📄 License

MIT © MemeSticker contributors
