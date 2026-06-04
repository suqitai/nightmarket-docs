#!/usr/bin/env python3
"""扫描并替换所有 nm-tip 占位块为图片引用。"""
import os, re

PLUGINS_DIR = "docs/plugins"

def replace_all_tips(content, plugin_name):
    """替换所有 nm-tip div 为图片引用。"""
    img_path = f"/images/{plugin_name}/terminal-preview.png"
    replacement = f'![{plugin_name} 终端预览]({img_path})\n\n*（占位截图 — 用 phantom 替换为实际操作截图）*'

    start = '<div class="nm-tip">'
    end = '</div>'
    result = []
    i = 0
    count = 0

    while i < len(content):
        idx = content.find(start, i)
        if idx == -1:
            result.append(content[i:])
            break

        # 之前的内容
        result.append(content[i:idx])

        # 找到 </div>
        end_idx = content.find(end, idx)
        if end_idx == -1:
            result.append(content[idx:])
            break

        # 替换整个块
        result.append(replacement)
        count += 1
        i = end_idx + len(end)

    return ''.join(result), count

def main():
    total = 0
    for fname in sorted(os.listdir(PLUGINS_DIR)):
        if not fname.endswith(".md") or fname in ("index.md", "template.md"):
            continue

        filepath = os.path.join(PLUGINS_DIR, fname)
        with open(filepath, "r") as f:
            original = f.read()

        plugin_name = fname.replace(".md", "")
        new_content, count = replace_all_tips(original, plugin_name)

        if count > 0:
            with open(filepath, "w") as f:
                f.write(new_content)
            print(f"  ✅ {fname} ({count} 处)")
            total += count
        else:
            print(f"  ⏭️ {fname}")

    print(f"\n🎉 完成 · 共更新 {total} 处")

if __name__ == "__main__":
    main()
