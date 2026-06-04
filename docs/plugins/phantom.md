# phantom — 桌面自动化

## 概述

phantom 是 Night Market 中的桌面自动化插件，提供截图、鼠标键盘控制等功能。在编写技术文档、演示操作流程或自动化 UI 测试时，phantom 帮你捕获真实的操作画面。

**核心能力：**
- 桌面截图：全屏、窗口、区域三种模式
- 终端截图：精准捕获 Claude Code 终端界面
- 鼠标键盘控制：自动化重复性操作
- 截图标注：添加箭头、高亮、文字标注
- 批量截图：按脚本批量生成多张截图

**适用场景：**
- 编写技术文档时需要终端操作截图
- 制作操作演示的静态引导
- 自动化 UI 回归测试
- 批量生成多个界面的截图素材

---

## 安装

```bash
claude plugins install phantom@claude-night-market
claude plugins list | grep phantom
```

**前置条件：**
- macOS 需要授予「屏幕录制」和「辅助功能」权限
- Linux 需要 `xdotool` 或 `gnome-screenshot`

---

## 命令参考

| 命令 | 必需参数 | 可选参数 | 说明 | 使用示例 |
|------|----------|----------|------|----------|
| `/phantom:screenshot` | — | `--mode`, `--output`, `--delay` | 捕获截图 | `/phantom:screenshot --mode window --output result.png` |
| `/phantom:click` | `--x`, `--y` | `--button`, `--count` | 模拟鼠标点击 | `/phantom:click --x 500 --y 300 --button right` |
| `/phantom:type` | `--text` | `--delay`, `--speed` | 模拟键盘输入 | `/phantom:type --text "hello world" --speed fast` |
| `/phantom:record` | — | `--fps`, `--duration` | 录制屏幕操作序列 | `/phantom:record --fps 10 --duration 30` |
| `/phantom:annotate` | `--image` | `--arrows`, `--text` | 截图添加标注 | `/phantom:annotate --image shot.png --arrows "100,200→300,400"` |

---

## 使用场景

### 场景 1：为文档生成终端截图

**问题：** 写 Night Market 插件文档时需要大量终端截图，手动截图效率低。

**解决方案：** 用 phantom 编写截图脚本，一键批量生成。

**命令示例：**
```bash
/phantom:screenshot --mode terminal --output public/images/attune/case1-flow.png --delay 2
```

**预期结果：** 高分辨率终端截图，自动保存到指定路径，可直接嵌入 Markdown 文档。

---

### 场景 2：自动化 UI 操作录制

**问题：** 需要展示一个多步骤操作的完整流程。

**解决方案：** 用 record 录制一系列截图序列。

**命令示例：**
```bash
/phantom:record --fps 5 --duration 30 --output demo-steps/
```

**预期结果：** 生成 150 张截图（30 秒 × 5fps），可按帧挑选关键步骤用于文档。

---

## 实战案例

### 案例 1：为本项目批量生成插件截图

**背景：** Night Market 文档需要为 23 个插件生成截图。

**操作步骤：**

1. **编写截图脚本**
   ```bash
   # 对每个插件执行典型命令并截图
   for plugin in attune spec-kit leyline; do
     /phantom:screenshot --mode terminal --output "public/images/$plugin/command-ref.png"
   done
   ```

2. **逐插件执行** — 每个插件运行一个典型命令，捕获输出

3. **标注关键区域**（可选）
   ```bash
   /phantom:annotate --image command-ref.png --arrows "100,200→300,200" --text "命令输出"
   ```

**结果展示：**

![phantom 终端预览](/images/phantom/terminal-preview.png)

*（占位截图 — 用 phantom 替换为实际操作截图）*

---

## 常见问题

<details class="faq-item">
<summary>Q: phantom 截图和手动截图有什么优势？</summary>
<div class="answer">

**A:** 
- **一致性**：所有截图尺寸、分辨率、窗口位置一致
- **可脚本化**：23 个插件的截图可以一条命令批量完成
- **精确时机**：`--delay` 控制在命令执行后的精确时刻截图
- **可重复**：插件更新后重新跑脚本即可更新所有截图
</div>
</details>

<details class="faq-item">
<summary>Q: macOS 权限怎么配置？</summary>
<div class="answer">

**A:** 
1. 系统偏好设置 → 安全性与隐私 → 隐私 → 屏幕录制 → 勾选 Terminal
2. 同样路径 → 辅助功能 → 勾选 Terminal
3. 配置后重启 Terminal 生效

phantom 首次运行时如果权限不足会报错并给出配置指引。
</div>
</details>

---

## 相关插件

| 插件 | 协作方式 |
|------|----------|
| [scry](./scry.md) | phantom 做静态截图，scry 做动态录屏 → 全媒体覆盖 |

---

> 📝 最后更新：2026-06-04
