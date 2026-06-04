# scry — 媒体生成

## 概述

scry 是 Night Market 中的动态媒体生成插件，支持终端操作录制、浏览器录制和 GIF 导出。与 phantom（静态截图）互补，scry 专注于捕捉动态操作流程。

**核心能力：**
- 终端录制：将 Claude Code 终端操作录制成视频或 GIF
- 浏览器录制：录制 Web 操作流程
- GIF 导出：从录屏中导出高质量 GIF（可控帧率和大小）
- 关键帧标记：在录制中标记关键步骤，自动生成步骤分解图
- 音频可选：支持录制系统音频或麦克风

**适用场景：**
- 制作终端操作的动态演示
- 展示多步骤工作流的完整过程
- Bug 复现步骤的记录和分享
- 教学和培训材料制作

---

## 安装

```bash
claude plugins install scry@claude-night-market
claude plugins list | grep scry
```

**前置条件：**
- macOS 需要授予屏幕录制权限
- GIF 导出依赖 FFmpeg（`brew install ffmpeg`）

---

## 命令参考

| 命令 | 必需参数 | 可选参数 | 说明 | 使用示例 |
|------|----------|----------|------|------|
| `/scry:record` | `--type` | `--fps`, `--max-duration`, `--output` | 录制终端或浏览器 | `/scry:record --type terminal --output demo.gif` |
| `/scry:export` | `--input` | `--format`, `--fps`, `--max-size` | 导出为 GIF/MP4 | `/scry:export --input recording.mp4 --format gif --max-size 5MB` |
| `/scry:markers` | `--input` | `--steps` | 标记关键帧生成分解图 | `/scry:markers --input demo.mp4 --steps "init,execute,result"` |
| `/scry:screencast` | `--url` | `--actions`, `--output` | 浏览器操作录制 | `/scry:screencast --url "http://localhost:3000" --actions steps.json` |

---

## 使用场景

### 场景 1：录制 attune 全流程演示

**问题：** 想展示 attune 从 brainstorm 到 execute 的完整流程，静态截图不够生动。

**解决方案：** 用 scry 录制终端操作流程，导出为 GIF。

**命令示例：**
```bash
/scry:record --type terminal --fps 15 --max-duration 45 --output public/gifs/attune/full-flow.gif
```

**预期结果：** 一段 45 秒的流畅 GIF，展示完整的四阶段工作流，文件大小 < 5MB。

---

### 场景 2：Bug 复现录屏

**问题：** 一个间歇性 Bug 难以用文字描述，需要录屏记录复现步骤。

**解决方案：** 用 scry 录制触发 Bug 的完整操作过程。

**命令示例：**
```bash
/scry:record --type terminal --fps 10 --max-duration 60 --output bug-repro.mp4
/scry:export --input bug-repro.mp4 --format gif --max-size 4MB
```

**预期结果：** 清晰的复现步骤 GIF，可附加到 GitHub Issue 中。

---

## 实战案例

### 案例 1：为本项目生成流程演示 GIF

**背景：** Night Market 文档需要为每个核心插件录制操作演示 GIF。

**操作步骤：**

1. **准备演示脚本** — 列出要执行的关键命令
2. **开始录制**
   ```bash
   /scry:record --type terminal --fps 15 --max-duration 30 --output demo-raw.mp4
   ```
3. **执行操作** — 按脚本执行命令
4. **导出 GIF**
   ```bash
   /scry:export --input demo-raw.mp4 --format gif --fps 15 --max-size 5MB --output final.gif
   ```

**结果展示：**

![scry 终端预览](/images/scry/terminal-preview.png)

*（占位截图 — 用 phantom 替换为实际操作截图）*

---

## 常见问题

<details class="faq-item">
<summary>Q: GIF 文件太大怎么办？</summary>
<div class="answer">

**A:** 几种优化手段：

```bash
--fps 10          # 降低帧率（15→10 大小减半）
--max-duration 20 # 缩短时长
--resolution 50%  # 降低分辨率
--palette 128     # 减少颜色数
```

目标是 30 秒以内的操作流程 GIF 控制在 3-5MB。
</div>
</details>

<details class="faq-item">
<summary>Q: scry 和 phantom 怎么选择？</summary>
<div class="answer">

**A:** 
- **需要展示动态过程**（多步骤工作流、命令执行过程）→ scry 录屏
- **需要展示静态状态**（命令结果、配置界面、代码输出）→ phantom 截图
- **两者结合**：用 scry 录整体过程 + phantom 截关键步骤的特写

本文档的策略：每个插件至少 1 张 phantom 截图 + 1 段 scry GIF（核心插件）。
</div>
</details>

---

## 相关插件

| 插件 | 协作方式 |
|------|----------|
| [phantom](./phantom.md) | phantom 截图 + scry 录屏 → 完整媒体素材库 |

---

> 📝 最后更新：2026-06-04
