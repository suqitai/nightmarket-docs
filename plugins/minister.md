# minister — GitHub Issue 管理

## 概述

minister 是 Night Market 中的 GitHub Issue 管理工具，提供看板仪表盘、Issue 生命周期管理和团队协作功能。它将 GitHub Issues 从「简单的任务列表」升级为「项目管理仪表盘」。

**核心能力：**
- 看板仪表盘：Kanban 视图展示 Issue 状态分布
- Issue 生命周期：从创建到关闭的完整管理
- 批量操作：批量更新标签、分配、里程碑
- 进度追踪：关联 PR 自动更新 Issue 状态
- 报告生成：Sprint 总结、燃尽图、团队贡献统计

**适用场景：**
- 日常 Issue 管理和优先级调整
- Sprint 规划和进度追踪
- 跨仓库 Issue 汇总视图
- 自动化 Issue 工作流

---

## 安装

```bash
claude plugins install minister@claude-night-market
claude plugins list | grep minister
```

**前置条件：**
- GitHub 仓库访问权限
- 建议配合 herald 使用以自动发送通知

---

## 命令参考

| 命令 | 必需参数 | 可选参数 | 说明 | 使用示例 |
|------|----------|----------|------|----------|
| `/minister:dashboard` | — | `--repo`, `--milestone` | 显示看板仪表盘 | `/minister:dashboard --repo org/project --milestone sprint-5` |
| `/minister:issue` | `--title` | `--body`, `--labels`, `--assignee` | 创建新 Issue | `/minister:issue --title "修复登录超时" --labels bug,high --assignee alice` |
| `/minister:triage` | `--repo` | `--filter` | 批量分类和优先级排序 | `/minister:triage --repo org/project --filter "no-label"` |
| `/minister:report` | — | `--type`, `--since` | 生成工作报告 | `/minister:report --type sprint --since "2 weeks ago"` |
| `/minister:batch` | `--action` | `--issues`, `--labels` | 批量操作 Issue | `/minister:batch --action add-label --issues 12,15,23 --labels "sprint-6"` |

---

## 使用场景

### 场景 1：Sprint 看板一览

**问题：** 需要快速了解当前 Sprint 的整体进度和各成员负载。

**解决方案：** 使用 dashboard 生成可视化看板。

**命令示例：**
```bash
/minister:dashboard --milestone "Sprint 6" --repo org/project
```

**预期结果：** 显示 To Do / In Progress / Review / Done 四列分布，每个 Issue 显示负责人和标签，高亮逾期和阻塞项。

---

### 场景 2：批量整理无标签 Issue

**问题：** 仓库有 30 个 Issue 缺乏标签，需要逐一分类打标签。

**解决方案：** 使用 triage 自动建议标签并批量应用。

**命令示例：**
```bash
/minister:triage --filter "no-label"
```

**预期结果：** minister 分析每个 Issue 的内容，建议标签和优先级，确认后批量应用。

---

## 实战案例

### 案例 1：Sprint 规划会议

**背景：** Sprint 开始前，需要从 Backlog 挑选 Issue 并分配到人。

**操作步骤：**

1. **查看当前 Backlog**
   ```bash
   /minister:dashboard --repo org/project
   ```
   *看板显示 45 个待处理 Issue，按优先级排列*

2. **批量分配到 Sprint**
   ```bash
   /minister:batch --action add-milestone --issues "12,15,23,28,31,35" --milestone "Sprint 7"
   ```

3. **分配负责人**
   ```bash
   /minister:batch --action assign --issues "12,15" --assignee alice
   /minister:batch --action assign --issues "23,28" --assignee bob
   /minister:batch --action assign --issues "31,35" --assignee carol
   ```

4. **确认规划** — 看板更新，每人 2 个 Issue 工作量均衡

**结果展示：**

![minister 终端预览](/images/minister/terminal-preview.png)

*（占位截图 — 用 phantom 替换为实际操作截图）*

---

### 案例 2：Sprint 结束自动生成总结

**背景：** Sprint 结束时需要向团队汇报完成情况和遗留问题。

**操作步骤：**

1. **生成 Sprint 报告**
   ```bash
   /minister:report --type sprint --milestone "Sprint 6"
   ```

2. **报告内容**：
   - 完成 8/10 Issue（80% 完成率）
   - 2 个 Issue 遗留到下一 Sprint（附原因）
   - 燃尽图：前期平稳，最后 2 天加速
   - 团队贡献：Alice 4 个、Bob 3 个、Carol 3 个（含 PR 统计）

3. **分享到团队频道**（配合 herald）
   ```bash
   /herald:notify --channel slack --content "$(cat sprint-6-report.md)"
   ```

**结果展示：**

![minister 终端预览](/images/minister/terminal-preview.png)

*（占位截图 — 用 phantom 替换为实际操作截图）*

---

## 常见问题

<details class="faq-item">
<summary>Q: minister 和 GitHub 自带的 Projects 有什么区别？</summary>
<div class="answer">

**A:** 
- **GitHub Projects**：Web 端可视化项目管理，拖拽式操作
- **minister**：终端内的 Issue 管理，AI 辅助分类和批量操作

minister 适合「键盘流」开发者在 Claude Code 中直接管理 Issue，不用切换浏览器。两者可以配合使用：minister 做批量操作，Projects 做可视化展示。
</div>
</details>

<details class="faq-item">
<summary>Q: triage 的自动标签建议准确吗？</summary>
<div class="answer">

**A:** triage 分析 Issue 标题和描述进行语义分类，准确率约 85-90%。建议流程：

1. 运行 triage 获得建议
2. 快速浏览确认（标注「不确定」的项重点复核）
3. 确认后批量应用

对于团队常用的非标准标签（如 `needs-design`、`blocked-by-legal`），可以在 `.minister/config.yml` 中定义标签规则提高准确率。
</div>
</details>

<details class="faq-item">
<summary>Q: 支持跨多个仓库的管理吗？</summary>
<div class="answer">

**A:** 支持。指定 `--repo` 参数或使用通配模式：

```bash
/minister:dashboard --repo org/*   # 组织下所有仓库的汇总看板
/minister:report --repo org/backend,org/frontend   # 跨两个仓库的报告
```

跨仓库模式下，Issue 会标注来源仓库，方便追溯。
</div>
</details>

---

## 相关插件

### 配合使用

| 插件 | 协作方式 |
|------|----------|
| [herald](./herald.md) | herald 将 minister 的 Issue 变更自动通知到 Slack/Discord |
| [egregore](./egregore.md) | egregore 的多 Agent 任务进度同步到 minister Issue |
| [sanctum](./sanctum.md) | sanctum 的 PR 自动关联 minister 管理的 Issue |

---

> 📝 最后更新：2026-06-04
