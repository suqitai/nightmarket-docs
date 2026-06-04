# egregore — 自主 Agent 编排

## 概述

egregore 是 Night Market 中最强大的 Agent 编排引擎，支持并行 worktree 隔离、多 Agent 协作、崩溃恢复和复杂的任务编排。当单个 Claude 会话不足以完成大型任务时，egregore 允许你将任务分解为多个子 Agent 并行执行。

**核心能力：**
- 并行 worktree：每个 Agent 在独立的 Git worktree 中运行，无文件冲突
- 多 Agent 编排：Workflow 脚本定义复杂的多阶段并行任务
- 崩溃恢复：Agent 异常退出后自动重启并续接上下文
- 进度追踪：实时显示所有子 Agent 的执行状态和输出
- 管道模式：pipeline/parallel/barrier 多种编排模式

**适用场景：**
- 大型代码库的批量重构（每个模块一个 Agent）
- 多维度代码审查（并行跑 Bug/安全/性能审查）
- 跨多个服务的同步更新
- CI/CD 中的并行测试执行

---

## 安装

```bash
claude plugins install egregore@claude-night-market
claude plugins list | grep egregore
```

**前置条件：**
- 项目必须是 Git 仓库（worktree 依赖 Git）
- 推荐搭配 conjure 使用以利用外部 LLM 资源

---

## 命令参考

| 命令 | 必需参数 | 可选参数 | 说明 | 使用示例 |
|------|----------|----------|------|----------|
| `/egregore:workflow` | `--script` | `--args`, `--resume` | 执行多 Agent 编排脚本 | `/egregore:workflow --script review.js` |
| `/egregore:parallel` | `--tasks` | `--max-workers` | 并行执行多个独立任务 | `/egregore:parallel --tasks tasks.md --max-workers 4` |
| `/egregore:pipeline` | `--items` | `--stages` | 流水线模式处理多个项目 | `/egregore:pipeline --items files.txt --stages review,fix,verify` |
| `/egregore:agents` | — | `--status` | 查看所有 Agent 状态 | `/egregore:agents --status` |
| `/egregore:resume` | `--run-id` | — | 恢复中断的编排运行 | `/egregore:resume --run-id wf_abc123` |

---

## 使用场景

### 场景 1：批量重构 20 个模块

**问题：** 需要将 20 个模块从 JavaScript 迁移到 TypeScript，每个模块独立，但逐一处理太慢。

**解决方案：** 使用 workflow 脚本，每个模块分配一个 Agent 在独立 worktree 中并行迁移。

**命令示例：**
```bash
/egregore:workflow --script migrate-to-ts.js --max-workers 8
```

**预期结果：** 8 个 Agent 同时工作，每个在隔离环境中处理一个模块。全部完成后自动汇总结果，显示成功/失败列表。

---

### 场景 2：多维度 PR 审查

**问题：** PR 需要从 Bug、安全、性能、架构 4 个维度审查，串行耗时太长。

**解决方案：** 4 个 Agent 并行审查同一 PR，每个 Agent 专注一个维度。

**命令示例：**
```bash
/egregore:parallel --tasks pr-review-dimensions.md --max-workers 4
```

**预期结果：** 4 个 Agent 分别产出 Bug 报告、安全报告、性能报告、架构报告，最后汇总为一份综合审查报告。

---

## 实战案例

### 案例 1：用 Workflow 脚本审查大 PR

**背景：** 一个涉及 15 个文件、800 行变更的大 PR，需要多维度 + 对抗性验证。

**操作步骤：**

1. **编写 Workflow 脚本** — 定义 3 个阶段：
   - 阶段 1（Find）：4 个 Agent 并行从 Bug/安全/性能/架构角度发现问题
   - 阶段 2（Verify）：每个发现由 2 个独立 Agent 对抗性验证
   - 阶段 3（Report）：汇总确认的问题，生成修复建议

2. **执行 Workflow**
   ```bash
   /egregore:workflow --script pr-audit-workflow.js --args "pr=42"
   ```

3. **查看进度** — egregore 实时显示每个 Agent 的状态

4. **获得最终报告** — 12 个 Agent 协作产出的综合审查报告

**结果展示：**

![egregore 终端预览](/images/egregore/terminal-preview.png)

*（占位截图 — 用 phantom 替换为实际操作截图）*

---

### 案例 2：崩溃恢复续接任务

**背景：** 一个运行 30 分钟的 Agent 编排任务中，其中一个 Agent 因上下文溢出崩溃。

**操作步骤：**

1. **崩溃自动检测** — egregore 报告 Agent-3（处理 user-service）崩溃，误差信息：context overflow

2. **恢复运行**
   ```bash
   /egregore:resume --run-id wf_xyz789
   ```

3. **智能续接** — 系统恢复 Agent-3 时自动：
   - 保留前 3 个已完成子任务的缓存结果
   - 只重新执行崩溃的子任务
   - 其他 7 个正常运行的 Agent 结果不受影响

4. **全部完成** — 所有 Agent 完成后正常汇总

**结果展示：**

![egregore 终端预览](/images/egregore/terminal-preview.png)

*（占位截图 — 用 phantom 替换为实际操作截图）*

---

## 常见问题

<details class="faq-item">
<summary>Q: Workflow 脚本怎么写？必须用 JavaScript 吗？</summary>
<div class="answer">

**A:** Workflow 脚本使用 JavaScript（Node.js 子集），提供 `agent()`、`parallel()`、`pipeline()` 等高级 API。示例：

```javascript
export const meta = {
  name: 'review-changes',
  description: '多维度审查变更文件',
}

// 阶段 1：并行发现问题
const findings = await parallel(
  DIMENSIONS.map(d => () => agent(d.prompt, { schema: FINDINGS_SCHEMA }))
)

// 阶段 2：对抗性验证
const verified = await parallel(
  findings.flat().map(f => () =>
    agent(`验证: ${f.title}`, { schema: VERDICT_SCHEMA }))
)

return verified.filter(v => v.isReal)
```

不需要写文件，直接在 `/egregore:workflow --script` 中传内联脚本。
</div>
</details>

<details class="faq-item">
<summary>Q: 并行 Agent 有数量限制吗？</summary>
<div class="answer">

**A:** 有限制：

- 同时运行的 Agent 上限：`min(16, CPU核心数 - 2)`
- 单个 Workflow 总 Agent 调用上限：1000（防止失控循环）
- worktree 隔离模式额外开销：每个 Agent 约 200-500ms 初始化

最佳实践：4-8 个 Agent 并行效率最高，超过后边际收益递减。
</div>
</details>

<details class="faq-item">
<summary>Q: worktree 隔离有什么好处？</summary>
<div class="answer">

**A:** 

| 场景 | 无 worktree | 有 worktree |
|------|:---:|:---:|
| 多个 Agent 同时编辑同一文件 | ❌ 冲突 | ✅ 各自独立 |
| Agent A 的更改被 Agent B 覆盖 | ❌ 可能发生 | ✅ 完全隔离 |
| 任务失败需要回滚 | ❌ 手动回滚 | ✅ 删除 worktree 即可 |
| 磁盘占用 | 低 | 较高（每个 worktree 一份文件副本） |

对于只读任务（如搜索、审查），不需要 worktree 隔离。读写任务建议使用。
</div>
</details>

---

## 相关插件

### 配合使用

| 插件 | 协作方式 |
|------|----------|
| [conjure](./conjure.md) | conjure 将部分 Agent 委托给外部 LLM（Gemini/Qwen），降低成本 |
| [minister](./minister.md) | minister 将 egregore 任务进度同步到 GitHub Issue |
| [attune](./attune.md) | attune 的执行阶段可启动 egregore 进行多 Agent 并行实施 |

---

> 📝 最后更新：2026-06-04
