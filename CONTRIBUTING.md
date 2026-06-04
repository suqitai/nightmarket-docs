# 贡献指南

感谢你为 Night Market 插件文档做贡献！

## 新增插件文档

### 1. 复制模板

```bash
cp docs/.templates/plugin-page.md docs/plugins/<plugin-name>.md
```

### 2. 填充内容

按照模板中的章节顺序逐项填充：

| 章节 | 要求 |
|------|------|
| 概述 | 2-3 句话介绍 + 核心能力列表 + 适用场景 |
| 安装 | 安装命令 + 前置条件 + 验证方法 |
| 命令参考 | 完整命令表格，每个命令至少一个示例 |
| 使用场景 | ≥ 2 个场景，每个包含问题/解决/示例 |
| 实战案例 | ≥ 2 个案例，带操作步骤和截图/录屏 |
| 常见问题 | ≥ 3 个 FAQ |
| 相关插件 | 配合使用 + 替代方案 |

### 3. 制作截图

```bash
# 使用 phantom 插件截图
bash scripts/screenshot.sh <plugin-name>

# 或在 Claude Code 中直接执行
/phantom:screenshot --output public/images/<plugin-name>/<场景名>.png
```

### 4. 录制终端操作

```bash
# 使用 scry 插件录制
bash scripts/record.sh <plugin-name>

# 或在 Claude Code 中直接执行
/scry:record terminal --output public/gifs/<plugin-name>/<场景名>.gif --fps 15 --max-duration 30
```

### 5. 本地预览

```bash
npm run docs:dev
```

打开浏览器访问 `http://localhost:5173` 预览效果。

### 6. 通过验证

```bash
bash scripts/validate.sh
```

### 7. 提交

```bash
git add docs/plugins/<plugin-name>.md public/images/<plugin-name>/ public/gifs/<plugin-name>/
git commit -m "docs: 添加 <plugin-name> 插件文档"
git push
```

## 内容质量标准

- [ ] 中文表述通顺、无语病、无错别字
- [ ] 技术术语保留英文原名（如 plugin、slash command、hook）
- [ ] 中英文混排时空格规范（英文单词前后有空格）
- [ ] 中文内容使用全角标点，英文内容使用半角标点
- [ ] 所有命令示例已在 Claude Code 中实际测试
- [ ] 所有截图和录屏清晰可读
- [ ] 无占位符或 TODO 标记残留

## 更新现有文档

当插件版本更新时，使用检查清单：

1. 复制 `docs/.templates/update-checklist.md`
2. 按清单逐项检查
3. 更新文档内容
4. 更新「最后更新」日期
5. 提交变更

## 目录规范

```
docs/plugins/<name>.md     → 插件文档
public/images/<name>/      → 截图素材
public/gifs/<name>/        → 录屏 GIF 素材
```

## Git 提交规范

```
docs: 添加 <plugin-name> 插件文档
docs: 更新 <plugin-name> 至 vX.Y.Z
fix: 修复 <plugin-name> 文档中的错误
media: 更新 <plugin-name> 截图/录屏
```
