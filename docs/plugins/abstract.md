# abstract — Skill/Hook 开发与评估

## 概述

abstract 是 Night Market 中专门用于 **插件开发** 的元工具集。它帮助开发者创建、测试、评估和优化 Claude Code 的 Skill 和 Hook。如果你需要开发自己的 Night Market 插件，abstract 是必不可少的工具箱。

**核心能力：**
- Skill 创建：TDD 驱动的 Skill 脚手架生成（create-skill）
- Hook 开发：安全优先的 Hook 创建（create-hook）
- 质量评估：skills-eval / hooks-eval 对现有 Skill 和 Hook 打分
- 插件验证：validate-plugin 检查插件结构合规性
- 复杂度分析：analyze-skill 生成模块化拆分建议
- 防绕过加固：bulletproof-skill 硬化 Skill 防止 prompt 注入和绕过

**适用场景：**
- 开发新的 Claude Code Skill
- 开发新的 Hook（生命周期钩子）
- 审查现有插件的质量和合规性
- 评估插件的 Token 效率
- 加固生产环境的 Skill 安全性

---

## 安装

```bash
claude plugins install abstract@claude-night-market
claude plugins list | grep abstract
```

---

## 命令参考

| 命令 | 必需参数 | 可选参数 | 说明 | 使用示例 |
|------|----------|----------|------|----------|
| `/abstract:create-skill` | — | `--name`, `--desc` | 创建新 Skill（含 TDD 测试） | `/abstract:create-skill --name "code-reviewer"` |
| `/abstract:create-hook` | — | `--event`, `--action` | 创建新 Hook | `/abstract:create-hook --event "pre-commit"` |
| `/abstract:skills-eval` | `--path` | `--dimensions` | 评估 Skill 质量 | `/abstract:skills-eval --path skills/ --dimensions all` |
| `/abstract:hooks-eval` | `--path` | `--dimensions` | 评估 Hook 质量 | `/abstract:hooks-eval --path hooks/` |
| `/abstract:validate-plugin` | `--path` | — | 验证插件结构合规 | `/abstract:validate-plugin --path plugins/my-plugin/` |
| `/abstract:analyze-skill` | `--path` | `--output` | 复杂度分析和拆分建议 | `/abstract:analyze-skill --path skills/big-skill.md` |
| `/abstract:bulletproof-skill` | `--path` | `--level` | 安全加固 Skill | `/abstract:bulletproof-skill --path skills/prod.md --level strict` |
| `/abstract:test-skill` | `--path` | `--scenarios` | 在子 Agent 中 TDD 测试 | `/abstract:test-skill --path skills/new-skill.md` |

---

## 使用场景

### 场景 1：从零创建一个新 Skill

**问题：** 想开发一个自定义的 Claude Code Skill，但不清楚标准结构和最佳实践。

**解决方案：** 使用 create-skill，通过 TDD 流程引导完成 Skill 开发。

**命令示例：**
```bash
/abstract:create-skill --name "deploy-checker" --desc "部署前检查清单自动化"
```

**预期结果：** 进入交互式流程：头脑风暴 Skill 功能 → 编写测试用例 → 生成 Skill 框架 → 实现功能 → 测试验证 → 产出合规 Skill 文件。

---

### 场景 2：安全加固线上 Skill

**问题：** 生产用的 Skill 需要防止 prompt 注入和意图绕过。

**解决方案：** 使用 bulletproof-skill 进行安全加固。

**命令示例：**
```bash
/abstract:bulletproof-skill --path skills/prod/critical-ops.md --level strict
```

**预期结果：** 自动检测并修复常见的注入和绕过漏洞，添加输入校验和输出过滤层。

---

## 实战案例

### 案例 1：创建 + 测试 + 加固一个完整的 Skill

**背景：** 你要开发一个「PR 标题规范化」Skill，检查 PR 标题是否符合团队规范。

**操作步骤：**

1. **创建 Skill 脚手架**
   ```bash
   /abstract:create-skill --name "pr-title-check" --desc "验证 PR 标题格式"
   ```
   *生成包含 frontmatter、核心逻辑框架、测试用例的 Skill 文件*

2. **在子 Agent 中 TDD 测试**
   ```bash
   /abstract:test-skill --path skills/pr-title-check.md --scenarios "valid,invalid,edge"
   ```
   *在隔离的沙箱环境中测试正常/异常/边界情况*

3. **质量评估**
   ```bash
   /abstract:skills-eval --path skills/pr-title-check.md
   ```
   *获得 Token 效率、激活可靠性、内容质量等维度评分*

4. **安全加固**
   ```bash
   /abstract:bulletproof-skill --path skills/pr-title-check.md --level standard
   ```

**结果展示：**

![abstract 终端预览](/images/abstract/terminal-preview.png)

*（占位截图 — 用 phantom 替换为实际操作截图）*

---

### 案例 2：审计现有插件的质量和合规性

**背景：** 你的团队有 5 个自制插件，需要全面审计质量和安全性。

**操作步骤：**

1. **全量评估**
   ```bash
   /abstract:skills-eval --path skills/ --dimensions all
   ```

2. **查看评估报告**
   *每个 Skill 按以下维度评分：*
   - Frontmatter 完整性（标题、描述、触发条件）
   - Token 效率（是否过度加载）
   - 激活可靠性（误触发率）
   - 内容质量（结构、可读性）
   - 安全性（注入风险）

3. **按优先级修复**，从低分 Skill 开始

**结果展示：**

![abstract 终端预览](/images/abstract/terminal-preview.png)

*（占位截图 — 用 phantom 替换为实际操作截图）*

---

## 常见问题

<details class="faq-item">
<summary>Q: create-skill 和手动写 Markdown 有什么区别？</summary>
<div class="answer">

**A:** create-skill 不只是模板填充，它提供：

1. **TDD 流程**：先定义测试场景，再实现功能
2. **自动合规**：生成的 Skill 自动通过 validate-plugin 检查
3. **安全默认值**：包含基本的 prompt 注入防护
4. **测试环境**：在隔离子 Agent 中运行，不影响主会话

适合首次开发 Skill 或希望遵循最佳实践的团队。
</div>
</details>

<details class="faq-item">
<summary>Q: skills-eval 的打分标准是什么？</summary>
<div class="answer">

**A:** 每个维度 0-100 分，详细标准和权重见 [abstract 评分框架](https://github.com/anthropics/claude-code/tree/main/plugins/abstract)：

| 维度 | 权重 | 及格线 |
|------|:---:|:---:|
| Frontmatter 完整性 | 15% | 80 |
| Token 效率 | 25% | 70 |
| 激活可靠性 | 20% | 75 |
| 内容质量 | 25% | 70 |
| 安全性 | 15% | 85 |

总分 ≥ 75 为合格，≥ 85 为优秀。
</div>
</details>

<details class="faq-item">
<summary>Q: bulletproof-skill 会不会改坏我的 Skill？</summary>
<div class="answer">

**A:** bulletproof-skill 默认生成加固后版本到新文件 `{name}-hardened.md`，原文件不修改：

```bash
/abstract:bulletproof-skill --path skills/my-skill.md --level strict
# 输出: skills/my-skill-hardened.md
```

审阅加固版本后，手动替换原文件。
</div>
</details>

---

## 相关插件

### 配合使用

| 插件 | 协作方式 |
|------|----------|
| [leyline](./leyline.md) | leyline 提供安全基础设施（注入检测），abstract 在 Skill 层面应用 |
| [hookify](./hookify.md) | abstract 开发 Hook，hookify 配置 Hook 的运行规则 |
| [pensive](./pensive.md) | abstract 做插件层面的元审查，pensive 做业务代码审查 |

### 替代方案

| 插件 | 差异对比 |
|------|----------|
| [hookify](./hookify.md) | hookify 侧重 Hook **运行时配置**，abstract 侧重 Hook **开发和评估** |

---

> 📝 最后更新：2026-06-04
