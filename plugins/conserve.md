# conserve — 上下文优化

## 概述

conserve 是 Night Market 中的上下文和 Token 优化插件，帮助你分析 Claude Code 会话的 Token 消耗、检测上下文膨胀、并给出优化建议。在长会话或复杂项目中，conserve 帮你保持上下文在预算内。

**核心能力：**
- Token 分析：会话 Token 消耗的实时监控和分布报告
- 膨胀检测：识别上下文中的冗余内容（重复信息、过时上下文）
- 优化建议：自动生成 Token 节省方案
- 预算管理：设置 Token 消耗上限和告警阈值
- 压缩策略：智能上下文压缩和优先级排序

**适用场景：**
- 长会话中 Token 消耗监控
- 优化插件的 Token 效率
- 项目级 Token 预算规划
- 调试上下文溢出问题

---

## 安装

```bash
claude plugins install conserve@claude-night-market
claude plugins list | grep conserve
```

---

## 命令参考

| 命令 | 必需参数 | 可选参数 | 说明 | 使用示例 |
|------|----------|----------|------|------|
| `/conserve:analyze` | — | `--scope`, `--period` | Token 消耗分析 | `/conserve:analyze --scope session --period "last 10m"` |
| `/conserve:bloat` | — | `--path`, `--threshold` | 检测上下文膨胀 | `/conserve:bloat --path skills/ --threshold 5000` |
| `/conserve:budget` | `--limit` | `--alert` | 设置 Token 预算 | `/conserve:budget --limit 100000 --alert 80%` |
| `/conserve:compress` | `--context` | `--strategy` | 智能压缩上下文 | `/conserve:compress --context current --strategy priority` |
| `/conserve:report` | — | `--since`, `--format` | 生成消耗报告 | `/conserve:report --since "today"` |

---

## 使用场景

### 场景 1：长会话 Token 预算管理

**问题：** 一个持续 2 小时的开发会话，担心 Token 超预算。

**解决方案：** 设置预算，到达阈值自动告警。

**命令示例：**
```bash
/conserve:budget --limit 200000 --alert 80%
```

**预期结果：** Token 到达 160000（80%）时收到告警，到达 190000（95%）时建议压缩或结束会话。

---

### 场景 2：检测插件的 Token 效率

**问题：** 自制的 Skill 似乎加载了很多不必要的内容。

**解决方案：** 用 bloat 检测 Skill 的 Token 膨胀。

**命令示例：**
```bash
/conserve:bloat --path skills/my-skill.md --threshold 3000
```

**预期结果：** 报告显示 Skill 总 Token 8500，其中 3000 为冗余内容——过度详细的例子、重复的背景信息，给出裁剪建议。

---

## 实战案例

### 案例 1：优化 Skill 的 Token 效率

**背景：** 一个 Skill 文件太大导致每次激活都消耗大量 Token。

**操作步骤：**

1. **分析膨胀**
   ```bash
   /conserve:bloat --path skills/large-skill.md
   ```

2. **获得优化建议**：
   - 「概述」章节从 800 token 精简到 200 token
   - 3 个相似案例合并为 1 个代表性的
   - 使用 progressive-loading 模式延迟加载不常用子模块

3. **实施优化** — 按建议修改，token 从 8500 降到 3200（减少 62%）

**结果展示：**

![conserve 终端预览](/images/conserve/terminal-preview.png)

*（占位截图 — 用 phantom 替换为实际操作截图）*

---

## 常见问题

<details class="faq-item">
<summary>Q: compress 压缩上下文会丢信息吗？</summary>
<div class="answer">

**A:** compress 不是简单截断，而是智能压缩：

- **保留**：当前任务的直接上下文、关键决策、未解决的讨论
- **摘要化**：已完成的子任务压缩为 1-2 句摘要
- **移除**：纯重复内容、已解决的错误信息、文件内容的历史版本

压缩目标是保留语义理解的前提下减少 30-50% Token。
</div>
</details>

<details class="faq-item">
<summary>Q: 预算超了后会怎样？</summary>
<div class="answer">

**A:** conserve 不做硬截断（可能破坏工作流），而是：

1. 80% — 温和告警：「Token 消耗已达 80%，建议压缩不重要的上下文」
2. 95% — 强烈建议：「即将达到预算上限，建议结束当前子任务后开始新会话」
3. 100% — 最后通知并提供最佳停止点

你始终可以手动调高预算：`/conserve:budget --limit 300000`。
</div>
</details>

---

## 相关插件

| 插件 | 协作方式 |
|------|----------|
| [parseltongue](./parseltongue.md) | conserve 优化对话 Token，parseltongue 优化 Python 代码性能 |
| [abstract](./abstract.md) | abstract 的 analyze-skill 与 conserve 互补评估 Skill 效率 |

---

> 📝 最后更新：2026-06-04
