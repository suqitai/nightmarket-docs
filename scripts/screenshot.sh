#!/bin/bash
# ===================================================
# Night Market Docs — Phantom 截图脚本
# 用法: bash scripts/screenshot.sh <plugin-name>
# ===================================================

set -e

PLUGIN_NAME="${1:?请提供插件名，例如: bash scripts/screenshot.sh attune}"
OUTPUT_DIR="public/images/${PLUGIN_NAME}"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

echo "📸 准备为 ${PLUGIN_NAME} 截图..."
echo "输出目录: ${OUTPUT_DIR}"
echo ""
echo "⚠️  请确保 phantom 插件已安装: claude plugins list | grep phantom"
echo ""
echo "📋 操作步骤:"
echo "1. 在 Claude Code 中打开要截图的内容"
echo "2. 使用 phantom 插件捕获屏幕"
echo "3. 将截图保存到 ${OUTPUT_DIR}/"
echo ""
echo "💡 提示: 在 Claude Code 中执行以下命令进行截图:"
echo "   /phantom:screenshot --output ${OUTPUT_DIR}/<场景名>.png"
echo ""
echo "命名规范:"
echo "  {场景/案例}-{描述}.png"
echo "  例如: case1-brainstorm-flow.png"
echo "        scenario1-new-project.png"
echo "        command-reference.png"

# 尝试列出已有截图
if [ -d "$OUTPUT_DIR" ] && [ "$(ls -A "$OUTPUT_DIR" 2>/dev/null)" ]; then
  echo ""
  echo "📁 已有截图:"
  ls -la "$OUTPUT_DIR"
fi
