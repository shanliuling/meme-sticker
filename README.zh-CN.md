<div align="center">

# MemeSticker 🐾

### 一张图进去，12 张能用的表情包出来。

**宠物、自拍、角色、玩偶，几乎任何主体都能变成一整套 AI 聊天表情。**

One image in, 12 usable stickers out.

[![GitHub stars](https://img.shields.io/github/stars/shanliuling/meme-sticker?style=flat)](https://github.com/shanliuling/meme-sticker/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)

[English](./README.md) · **简体中文**

<br/>

<img src="./assets/hero.png" width="900" alt="MemeSticker 一张图生成整套表情包" />

</div>

---

## ✨ 为什么是 MemeSticker？

AI 早就会画“表情包大图”了，真正麻烦的是后面：**裁图、抠背景、修边缘、统一尺寸、逐张导出。**

**MemeSticker 把整套流程一次做完。**

| 🎨 生成 | ✂️ 拆分 | 🪄 清理 | 📦 打包 |
| --- | --- | --- | --- |
| 自动设计表情、文案和动作 | 自动识别并拆出每一张 | 透明背景 + 边缘去色 | 预览图 + 12 PNG + ZIP |

> **不是只给你一张 12 宫格大图，而是真的给你 12 张独立透明 PNG。**

---

## 🎬 实际效果

同一个 Skill，不同主体都能做：

<p align="center">
  <a href="./assets/example-girl.jpg"><img src="./assets/example-girl.jpg" width="31%" alt="真人表情包效果" /></a>
  <a href="./assets/example-cat.jpg"><img src="./assets/example-cat.jpg" width="31%" alt="宠物表情包效果" /></a>
  <a href="./assets/example-character.jpg"><img src="./assets/example-character.jpg" width="31%" alt="角色表情包效果" /></a>
</p>

<div align="center">

**自拍 · 宠物 · 二次元 / 游戏角色 · 玩偶 · 吉祥物 · 物体**

</div>

---

## ⚡ 30 秒开始

```bash
npx skills add shanliuling/meme-sticker
```

上传一张图片，直接说：

> **把这张图做成一套表情包。**

也可以指定主题：

> 把这只猫做成一套打工人表情包。

> 给这个角色做 12 张阴阳怪气的聊天表情。

> 把这张自拍做成可爱风聊天贴纸。

不需要自己写 12 条 Prompt，MemeSticker 会自动规划整套反应、文案和动作。

---

## 🔥 不只是一张“表情包大图”

很多 AI 工作流生成完 12 宫格就结束了。MemeSticker 会继续自动拆图、去背景、清理边缘、统一尺寸，并把成品打包好。

<p align="center">
  <img src="./assets/not-just-a-sheet.png" width="820" alt="普通表情大图与 MemeSticker 独立透明 PNG 对比" />
</p>

---

## 🧠 为什么是 2 × 6？

MemeSticker 固定使用 **两次 3×2 生图**，而不是一张 12 宫格，也不是逐张生成 12 次。

- **1 × 12** → 每张空间更小，也更难拆干净
- **12 × 1** → 太慢，人物 / 角色一致性也更容易漂
- **2 × 6** → 速度、一致性和切图质量之间更稳的平衡

<p align="center">
  <img src="./assets/workflow-2x6.png" width="900" alt="MemeSticker 2x6 生成流程" />
</p>

---

## 🎁 最终会得到什么？

```text
output/
├── preview.jpg
└── sticker-pack.zip
```

ZIP 内：

```text
sticker-pack.zip
├── preview.jpg
└── stickers/
    ├── 01.png
    ├── 02.png
    ├── ...
    └── 12.png
```

每张都是独立透明 PNG，可以自行导入聊天软件或继续用于设计、创作。

---

<details>
<summary><strong>📦 手动安装</strong></summary>

<br/>

```bash
git clone https://github.com/shanliuling/meme-sticker.git
```

将仓库文件夹放进你的 Agent Skills 目录即可。

宿主智能体需要本身具备 **图片生成 / 图片编辑能力**。MemeSticker 使用宿主的图片模型负责创作，Python 脚本负责拆图、透明化、边缘清理、尺寸统一和打包。

</details>

<details>
<summary><strong>⚙️ 运行要求</strong></summary>

<br/>

- 支持 Agent Skills 的宿主
- 图片生成 / 图片编辑能力
- Python **3.10+**
- NumPy + Pillow

依赖缺失时可根据 `scripts/requirements.txt` 自动安装，因此首次运行可能需要网络和 pip 权限。

</details>

<details>
<summary><strong>🛠 项目结构</strong></summary>

<br/>

```text
meme-sticker/
├── assets/
├── references/
│   └── generation-guide.md
├── scripts/
│   ├── package_sticker_pack.py
│   ├── extract_sticker_sheet.py
│   ├── sticker_sheet_lib.py
│   └── requirements.txt
├── LICENSE
├── README.md
├── README.zh-CN.md
└── SKILL.md
```

创意部分交给图片模型：文案、字体、动作、表情、装饰。

Python 只负责确定性的生产流程：切分、去背景、de-spill、尺寸统一、预览图和 ZIP 打包。

</details>

<details>
<summary><strong>⚠️ 已知限制</strong></summary>

<br/>

- 角色一致性仍取决于宿主使用的图片模型。
- AI 生成文字偶尔可能出现错字。
- 主体或背景过于复杂时，拆分和透明化质量可能下降。
- MemeSticker 输出标准透明 PNG，导入具体聊天平台由用户自行完成。

</details>

---

## ❤️ 给真正想“拿去用”的表情包

**一张图进去，一整套表情包出来。**

如果 MemeSticker 帮你省掉了裁图、抠背景这些麻烦事，欢迎点一个 ⭐，也方便更多人发现这个项目。

## 📄 License

MIT © 2026 shanliuling
