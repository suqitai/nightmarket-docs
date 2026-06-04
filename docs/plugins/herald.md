# herald — 通知系统

## 概述

herald 是 Night Market 中的通知集成插件，将 Claude Code 的事件和工作流状态推送到外部通信平台。支持 GitHub Issue 评论、Slack 消息、Discord webhook 等多种通知渠道。

**核心能力：**
- GitHub Issue 通知：在 Issue 中自动评论进度更新
- Slack 集成：发送消息到指定频道或用户
- Discord webhook：通过 webhook 发送格式化消息
- 事件驱动：支持 on-complete、on-error、on-milestone 等触发条件
- 消息模板：预定义多种消息格式（进度、告警、总结）

**适用场景：**
- 长任务完成后自动通知团队
- CI/CD 中的构建状态通知
- Agent 任务完成后同步进度到 Issue
- 团队协作的自动化状态更新

---

## 安装

```bash
claude plugins install herald@claude-night-market
claude plugins list | grep herald
```

**前置条件：**
- Slack 通知需要配置 Slack Webhook URL
- Discord 通知需要配置 Discord Webhook URL
- GitHub 通知需要仓库的 Issue 写入权限

---

## 命令参考

| 命令 | 必需参数 | 可选参数 | 说明 | 使用示例 |
|------|----------|----------|------|------|
| `/herald:notify` | `--channel` | `--message`, `--template` | 发送通知到指定渠道 | `/herald:notify --channel slack --message "部署完成"` |
| `/herald:watch` | `--event` | `--channel`, `--action` | 监听事件并自动通知 | `/herald:watch --event on-build-complete --channel discord` |
| `/herald:issue` | `--issue` | `--comment`, `--status` | 更新 GitHub Issue | `/herald:issue --issue 42 --comment "PR #56 已合并，此 Issue 自动关闭"` |
| `/herald:configure` | `--channel` | `--webhook`, `--test` | 配置通知渠道 | `/herald:configure --channel slack --webhook "$SLACK_URL" --test` |

---

## 使用场景

### 场景 1：长任务完成自动通知

**问题：** 一个 20 分钟的 Agent 任务运行时你去做别的事，完成后需要主动通知你。

**解决方案：** 用 watch 监听任务完成事件，自动推送 Slack。

**命令示例：**
```bash
/herald:watch --event on-task-complete --channel slack --action "发送结果摘要到 #dev 频道"
```

**预期结果：** Agent 任务完成后，Slack 自动收到一条包含状态（成功/失败）、耗时、关键输出的消息。

---

### 场景 2：PR 合并自动关闭 Issue

**问题：** PR 合并后经常忘记手动关闭关联的 Issue。

**解决方案：** 用 Herald 在 PR 合并时自动评论并关闭 Issue。

**命令示例：**
```bash
/herald:issue --issue 42 --comment "✅ 已通过 PR #56 实现，自动关闭" --status close
```

---

## 实战案例

### 案例 1：多 Agent 任务的进度播报

**背景：** egregore 运行一个 12 Agent 的并行任务，希望在 Slack 收到阶段性进度。

**操作步骤：**

1. **配置进度播报**
   ```bash
   /herald:watch --event on-milestone --channel slack --action "每完成 25% 播报一次"
   ```

2. **任务运行中** — Slack 实时收到进度更新：
   - 「🔄 3/12 Agent 完成 (25%)」
   - 「🔄 6/12 Agent 完成 (50%)」
   - 「✅ 12/12 Agent 完成 (100%)，总耗时 8 分钟」

**结果展示：**

<div class="nm-tip">
📸 <strong>截图待制作</strong>：展示 herald Slack 通知消息。运行 <code>bash scripts/screenshot.sh herald</code> 生成。
</div>

---

## 常见问题

<details class="faq-item">
<summary>Q: Webhook URL 怎么安全存储？</summary>
<div class="answer">

**A:** 使用环境变量，不要硬编码：

```bash
export HERALD_SLACK_WEBHOOK="https://hooks.slack.com/..."
export HERALD_DISCORD_WEBHOOK="https://discord.com/api/webhooks/..."

/herald:configure --channel slack --webhook "$HERALD_SLACK_WEBHOOK"
```

也可以存在 `.env` 文件中（确保 `.gitignore`），herald 会自动读取。
</div>
</details>

<details class="faq-item">
<summary>Q: 能同时通知多个渠道吗？</summary>
<div class="answer">

**A:** 可以。一次配置多个渠道：

```bash
/herald:watch --event on-error --channel "slack#alerts,discord#dev,github-issue#42"
```

关键事件（如错误、阻塞）建议多渠道通知，确保有人看到。
</div>
</details>

---

## 相关插件

| 插件 | 协作方式 |
|------|----------|
| [minister](./minister.md) | minister 管理 Issue，herald 发送 Issue 变更通知 |
| [egregore](./egregore.md) | egregore 任务进度通过 herald 实时播报 |

---

> 📝 最后更新：2026-06-04
