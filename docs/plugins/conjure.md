# conjure — 外部 LLM 委托

## 概述

conjure 是 Night Market 中的外部 LLM 委托插件，允许你将任务分发给 Gemini、Qwen 等外部模型执行。当任务不需要 Claude Opus 的全部能力时，委托给更便宜或更快的模型可以节省成本和延迟。

**核心能力：**
- 多模型支持：Gemini、Qwen 等外部 LLM
- 任务路由：根据任务复杂度自动选择模型
- 成本优化：简单任务用便宜模型，复杂任务保留 Claude
- 模型对比：同一任务发送给多个模型，对比结果
- 故障切换：主模型不可用时自动切换到备用模型

**适用场景：**
- 批量处理简单重复任务（格式化、翻译、摘要）
- 对比不同模型的输出质量
- 节省高价值模型的 Token 消耗
- 模型不可用时的自动容灾

---

## 安装

```bash
claude plugins install conjure@claude-night-market

# 额外配置外部模型的 API Key
# Gemini: export GEMINI_API_KEY=xxx
# Qwen: export QWEN_API_KEY=xxx

claude plugins list | grep conjure
```

**前置条件：**
- 需要目标外部模型的 API Key
- 网络可访问对应 API 端点

---

## 命令参考

| 命令 | 必需参数 | 可选参数 | 说明 | 使用示例 |
|------|----------|----------|------|----------|
| `/conjure:delegate` | `--task` | `--model`, `--priority` | 委托任务给指定模型 | `/conjure:delegate --task "翻译这段代码注释" --model gemini` |
| `/conjure:compare` | `--task` | `--models` | 多模型对比执行同一任务 | `/conjure:compare --task "审查这个函数" --models claude,gemini,qwen` |
| `/conjure:route` | `--task` | `--budget` | 自动路由到最优模型 | `/conjure:route --task "格式化 JSON" --budget low` |
| `/conjure:models` | — | `--status` | 列出可用模型和状态 | `/conjure:models --status` |
| `/conjure:fallback` | `--task` | `--chain` | 配置故障切换链 | `/conjure:fallback --task "$TASK" --chain "gemini,qwen,claude"` |

---

## 使用场景

### 场景 1：批量翻译代码注释

**问题：** 项目有 200 个文件需要将英文注释翻译成中文，用 Claude Opus 太贵。

**解决方案：** 委托给 Gemini 批量翻译，成本降低 90%。

**命令示例：**
```bash
/conjure:delegate --task "翻译 src/ 下所有文件的英文注释为中文" --model gemini --mode batch
```

**预期结果：** Gemini 逐文件处理，完成后输出变更列表。处理 200 个文件的成本约为 Claude Opus 的 1/10。

---

### 场景 2：三模型对比代码审查

**问题：** 不确定哪个模型最适合做 Python 代码审查。

**解决方案：** 同时发送给 3 个模型，对比审查质量。

**命令示例：**
```bash
/conjure:compare --task "审查 src/auth.py 的安全问题" --models claude-haiku,gemini-pro,qwen-max
```

**预期结果：** 显示 3 份审查报告并排对比，标注各模型发现的问题数量和严重度，帮助你选择最优模型。

---

## 实战案例

### 案例 1：智能路由节省成本

**背景：** 日常开发中大量任务简单（格式检查、命名建议），不需要 Opus 的能力。

**操作步骤：**

1. **配置路由规则**
   - `budget: low` → Gemini / Claude Haiku
   - `budget: medium` → Claude Sonnet
   - `budget: high` → Claude Opus

2. **日常使用自动路由**
   ```bash
   /conjure:route --task "给这个类的方法起更好的名字" --budget low
   # → 路由到 Gemini

   /conjure:route --task "重构这个认证模块的架构" --budget high
   # → 路由到 Claude Opus
   ```

3. **月底查看成本报告** — 对比全用 Opus 的成本节省 60%+

**结果展示：**

<div class="nm-tip">
📸 <strong>截图待制作</strong>：展示 conjure 成本对比面板。运行 <code>bash scripts/screenshot.sh conjure</code> 生成。
</div>

---

### 案例 2：API 故障自动切换

**背景：** Gemini API 偶发不可用，需要零人工干预的故障切换。

**操作步骤：**

1. **配置故障切换链**
   ```bash
   /conjure:fallback --task "生成单元测试" --chain "gemini,qwen,claude-haiku"
   ```

2. **自动切换**：
   - 尝试 Gemini → 返回 503 → 自动切换到 Qwen
   - Qwen 正常响应 → 返回结果
   - 用户无感知此次切换

**结果展示：**

<div class="nm-tip">
📸 <strong>截图待制作</strong>：展示 conjure 故障切换日志。运行 <code>bash scripts/screenshot.sh conjure</code> 生成。
</div>

---

## 常见问题

<details class="faq-item">
<summary>Q: 委托给外部模型的数据安全吗？</summary>
<div class="answer">

**A:** 需要注意：

- **敏感代码/数据**：不建议发送给外部模型（Gemini/Qwen 的服务条款可能允许使用数据训练）
- **公开可用的代码**：风险较低
- **最佳实践**：在 `/conjure:delegate` 前用 `--sanitize` 过滤敏感信息（如密钥、内部 URL）

如果不确定，保持使用 Claude（Anthropic API 默认不训练客户数据）。
</div>
</details>

<details class="faq-item">
<summary>Q: 外部模型产生的结果质量如何保证？</summary>
<div class="answer">

**A:** 几种策略：

1. **结果校验**：conjure 可配置「回答者 + 校验者」模式，外部模型回答，Claude 校验
2. **多模型投票**：发送给 2+ 个模型，只有答案一致时才接受
3. **人工审核**：`--require-approval` 标记，外部模型结果需人工确认后使用

简单任务（翻译、格式化）可以信任，关键决策任务建议保留 Claude。
</div>
</details>

<details class="faq-item">
<summary>Q: 如何知道哪个模型最适合我的任务？</summary>
<div class="answer">

**A:** 使用 compare 做 A/B 测试：

```bash
/conjure:compare --task "你的典型任务" --models claude-sonnet,gemini-pro,qwen-max --runs 10
```

conjure 会输出各模型在 10 次运行中的平均质量评分、延迟、成本，帮你做出数据驱动的模型选择。
</div>
</details>

---

## 相关插件

### 配合使用

| 插件 | 协作方式 |
|------|----------|
| [egregore](./egregore.md) | egregore 编排多 Agent 时，conjure 将部分 Agent 委托给外部模型 |
| [conserve](./conserve.md) | conjure 做成本优化，conserve 做上下文 Token 优化 |

---

> 📝 最后更新：2026-06-04
