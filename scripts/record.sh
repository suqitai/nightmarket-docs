#!/bin/bash
# ===================================================
# Night Market Docs — Scry 录屏脚本
# 用法: bash scripts/record.sh <plugin-name>
# ===================================================

set -e

PLUGIN_NAME="${1:?请提供插件名，例如: bash scripts/record.sh attune}"
OUTPUT_DIR="public/gifs/${PLUGIN_NAME}"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

echo "🎬 准备为 ${PLUGIN_NAME} 录制终端操作..."
echo "输出目录: ${OUTPUT_DIR}"
echo ""
echo "⚠️  请确保 scry 插件已安装: claude plugins list | grep scry"
echo ""
echo "📋 操作步骤:"
echo "1. 准备好要录制的命令序列"
echo "2. 使用 scry 插件开始录制"
echo "3. 执行操作，完成后停止录制"
echo "4. GIF 将保存到 ${OUTPUT_DIR}/"
echo ""
echo "💡 提示: 在 Claude Code 中执行以下命令进行录制:"
echo "   /scry:record terminal --output ${OUTPUT_DIR}/<场景名>.gif --fps 15 --max-duration 30"
echo ""
echo "录制要求:"
echo "  - 帧率: ≥ 15fps"
echo "  - 时长: ≤ 30 秒"
echo "  - 文件大小: < 5MB"
echo "  - 内容: 清晰展示操作流程"
echo ""
echo "命名规范:"
echo "  {场景/案例}-{描述}.gif"
echo "  例如: case1-full-workflow.gif"
echo "        scenario1-code-review.gif"

# 尝试列出已有录屏
if [ -d "$OUTPUT_DIR" ] && [ "$(ls -A "$OUTPUT_DIR" 2>/dev/null)" ]; then
  echo ""
  echo "📁 已有录屏:"
  ls -la "$OUTPUT_DIR"
fi
