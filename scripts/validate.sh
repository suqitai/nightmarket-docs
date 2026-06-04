#!/bin/bash
# ===================================================
# Night Market Docs — 模板一致性验证脚本
# 用法: bash scripts/validate.sh
# ===================================================

set -e

PLUGINS_DIR="docs/plugins"
REQUIRED_SECTIONS=(
  "## 概述"
  "## 安装"
  "## 命令参考"
  "## 使用场景"
  "## 实战案例"
  "## 常见问题"
  "## 相关插件"
)

ERRORS=0
WARNINGS=0

echo "🔍 Night Market Docs — 文档验证"
echo "=================================="
echo ""

# 检查 plugins 目录是否存在
if [ ! -d "$PLUGINS_DIR" ]; then
  echo "⚠️  $PLUGINS_DIR 目录尚不存在 — 跳过插件页面验证"
  exit 0
fi

# 遍历每个插件页面
for file in "$PLUGINS_DIR"/*.md; do
  # 跳过 index.md 和 template.md
  filename=$(basename "$file")
  if [ "$filename" = "index.md" ] || [ "$filename" = "template.md" ]; then
    continue
  fi

  plugin_name="${filename%.md}"
  echo "📄 检查: $plugin_name"

  # 检查每个必需章节
  for section in "${REQUIRED_SECTIONS[@]}"; do
    if ! grep -q "$section" "$file"; then
      echo "  ❌ 缺失章节: $section"
      ERRORS=$((ERRORS + 1))
    fi
  done

  # 检查是否有 TODO 或占位符
  if grep -q "\[插件名\]" "$file" 2>/dev/null; then
    echo "  ⚠️  发现未替换的占位符: [插件名]"
    WARNINGS=$((WARNINGS + 1))
  fi

  # 检查最后更新日期
  if ! grep -q "最后更新：" "$file"; then
    echo "  ⚠️  缺少「最后更新」日期"
    WARNINGS=$((WARNINGS + 1))
  fi

  # 检查媒体引用是否存在
  image_refs=$(grep -oP '\/images\/[^)\s]+' "$file" 2>/dev/null || true)
  for img in $image_refs; do
    img_path="public${img}"
    if [ ! -f "$img_path" ]; then
      echo "  ⚠️  图片缺失: $img_path (页面引用但文件不存在)"
      WARNINGS=$((WARNINGS + 1))
    fi
  done

  gif_refs=$(grep -oP '\/gifs\/[^)\s]+' "$file" 2>/dev/null || true)
  for gif in $gif_refs; do
    gif_path="public${gif}"
    if [ ! -f "$gif_path" ]; then
      echo "  ⚠️  GIF 缺失: $gif_path (页面引用但文件不存在)"
      WARNINGS=$((WARNINGS + 1))
    fi
  done

  echo ""
done

echo "=================================="
echo "验证完成: $ERRORS 个错误, $WARNINGS 个警告"
echo ""

if [ "$ERRORS" -gt 0 ]; then
  echo "❌ 存在章节缺失，请补充后再提交"
  exit 1
fi

if [ "$WARNINGS" -gt 0 ]; then
  echo "⚠️  存在警告，建议修复后提交"
else
  echo "✅ 所有检查通过！"
fi
