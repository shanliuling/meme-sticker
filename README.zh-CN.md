# MemeSticker

[English](./README.md) | 简体中文

将一张宠物、自拍、角色或任意主体图片，变成一套完整的 12 张 AI 聊天表情包。

## 快速开始

将本仓库克隆或复制到宿主的 Skills 目录，上传一张图片，然后告诉智能体：
`把这张图做成一套 12 张的聊天表情包。`

宿主必须具备图片生成能力；表情拆分与打包需要 Python 3.10+。

## 核心方案

本 Skill 固定采用 **2 张大图 × 每张 6 个表情** 的生成流程：

- A 图：3 列 × 2 行，共 6 个表情
- B 图：3 列 × 2 行，共 6 个表情
- 最终输出：12 张透明 PNG 表情 + 合集预览图 + ZIP 压缩包

这是生成速度、角色一致性和切图质量之间更稳妥的折中方案：

- 不使用一张包含 12 个表情的大网格图，因为难以稳定切分
- 不逐张生成 12 次，因为速度慢且角色风格容易漂移

## 文件说明

- `SKILL.md` — 智能体执行本 Skill 时遵循的完整说明
- `references/generation-guide.md` — 每张 3×2 表情大图的生成规范
- `scripts/sticker_sheet_lib.py` — 可复用的表情提取处理逻辑
- `scripts/extract_sticker_sheet.py` — 将一张 3×2 大图拆成 6 张表情
- `scripts/package_sticker_pack.py` — 合并两组结果并生成 12 张表情包 ZIP
- `scripts/requirements.txt` — Python 依赖

## 运行环境准备

本 Skill 需要 **Python 3.10+**。在 Windows 上会依次尝试 `python`、
`py -3` 和 `python3`；在 macOS/Linux 上会依次尝试 `python3` 和
`python`，并检查解释器版本是否符合要求。

智能体会先验证 Python 版本：

```text
<python-command> -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)"
```

打包前会检查 NumPy 和 Pillow：

```text
<python-command> -c "import numpy, PIL"
```

如果依赖缺失，Skill 会使用同一个 Python 解释器自动安装仓库内的依赖：

```text
<python-command> -m pip install -r "scripts/requirements.txt"
```

## 主要命令

打包命令保持为单行格式，方便直接用于 PowerShell、命令提示符、Bash 或 zsh。

### Windows PowerShell

```powershell
python scripts/package_sticker_pack.py --sheet-a "C:\path\to\sheet-a.png" --sheet-b "C:\path\to\sheet-b.png" --output-dir "C:\path\to\output"
```

如果无法使用 `python`，请改用 `py -3`。

### macOS 或 Linux

```bash
python3 scripts/package_sticker_pack.py --sheet-a "/abs/path/sheet-a.png" --sheet-b "/abs/path/sheet-b.png" --output-dir "/abs/path/output"
```

## 输出行为

打包流程会清理表情边缘，并保持最终输出目录简洁。默认只会输出
`preview.jpg` 和 `sticker-pack.zip`。A/B 大图的中间处理文件会保存到
输出目录内的隐藏工作目录，并在成功后自动删除，因此不依赖操作系统的临时目录。
只有在开发或排查失败原因时才需要使用 `--keep-debug`。

## 最终产物

默认输出目录：

```text
output/
├── preview.jpg
└── sticker-pack.zip
```

ZIP 压缩包仅包含：

```text
sticker-pack.zip
├── preview.jpg
└── stickers/
    ├── 01.png
    ├── 02.png
    ├── ...
    └── 12.png
```

只有在开发或诊断表情提取问题时才需要使用 `--keep-debug`。
