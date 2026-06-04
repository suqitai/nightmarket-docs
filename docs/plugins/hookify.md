# hookify — 行为规则引擎

## 概述

hookify 是 Night Market 中的声明式规则引擎，允许你通过 Markdown 配置文件定义 Claude Code 的运行行为规则。无需编写代码，只需在 `.claude/hooks/` 目录下放置 Markdown 文件，hookify 自动将其转化为可执行的 Hook。

**核心能力：**
- 声明式 Hook：Markdown 编写，自动转化为生命周期钩子
- 安全规则：定义在特定事件前/后执行的安全检查
- 行为定制：自动化重复操作（如提交前格式化、推送前测试）
- 作用域控制：Plugin / Project / Global 三级作用域
- 条件触发：基于文件类型、目录、分支等条件精确匹配

**适用场景：**
- 团队统一开发规范（提交信息格式、代码风格检查）
- 敏感操作安全拦截（如禁止在生产分支直接推送）
- 自动化工作流（PR 创建时自动添加标签和 Reviewer）
- 新人引导（在特定操作前给出提示和建议）

---

## 安装

```bash
claude plugins install hookify@claude-night-market
claude plugins list | grep hookify
```

---

## 命令参考

| 命令 | 必需参数 | 可选参数 | 说明 | 使用示例 |
|------|----------|----------|------|----------|
| `/hookify:create` | `--name` | `--event`, `--scope` | 创建新 Hook 规则文件 | `/hookify:create --name "commit-check" --event pre-commit` |
| `/hookify:validate` | `--path` | — | 验证 Hook 配置正确性 | `/hookify:validate --path .claude/hooks/` |
| `/hookify:list` | — | `--scope`, `--event` | 列出已激活的 Hook | `/hookify:list --event pre-push` |
| `/hookify:test` | `--hook` | `--simulate` | 模拟测试 Hook 行为 | `/hookify:test --hook commit-check --simulate` |
| `/hookify:disable` | `--hook` | `--temporary` | 禁用 Hook | `/hookify:disable --hook commit-check --temporary` |

---

## 使用场景

### 场景 1：提交前自动检查

**问题：** 团队成员经常提交包含 TODO、console.log 的代码到仓库。

**解决方案：** 创建 pre-commit Hook，提交前自动扫描禁止模式。

**命令示例：**
```bash
/hookify:create --name "no-todo-commit" --event pre-commit --scope project
```

**生成的 Hook 规则**（Markdown 文件）：
```markdown
---
hook: pre-commit
scope: project
---

# 禁止提交调试代码

检查暂存区是否包含：
- `console.log` / `print(` / `TODO`
- 未使用的 import

发现匹配项时阻止提交并显示具体文件和行号。
```

**预期结果：** 任何包含禁止模式的提交被自动拦截，开发者修复后才能提交。

---

### 场景 2：保护生产分支

**问题：** 需要防止任何人直接推送到 main 分支（必须走 PR）。

**解决方案：** 创建 pre-push Hook 检查目标分支。

**命令示例：**
```bash
/hookify:create --name "protect-main" --event pre-push --scope project
```

**预期结果：** 直接推送到 main 时被拦截，显示「请通过 PR 合并到 main 分支」。

---

## 实战案例

### 案例 1：建立团队标准 Hook 集

**背景：** 新团队需要统一开发规范，一套 Hook 覆盖提交、推送、PR 全流程。

**操作步骤：**

1. **创建 3 个核心 Hook**
   ```bash
   /hookify:create --name "format-check" --event pre-commit
   /hookify:create --name "test-before-push" --event pre-push
   /hookify:create --name "pr-checklist" --event pre-pr
   ```

2. **逐个配置规则**
   - `format-check`：检查代码格式化状态
   - `test-before-push`：推送前运行 `npm test`
   - `pr-checklist`：PR 创建时自动填充 Checklist 模板

3. **验证和测试**
   ```bash
   /hookify:validate --path .claude/hooks/
   /hookify:test --hook format-check --simulate
   ```

4. **提交到仓库**，团队成员 pull 后自动生效

**结果展示：**

<div class="nm-tip">
📸 <strong>截图待制作</strong>：展示 hookify Hook 列表和测试结果。运行 <code>bash scripts/screenshot.sh hookify</code> 生成。
</div>

---

### 案例 2：临时放宽规则处理紧急修复

**背景：** 生产环境紧急 Bug，需要跳过常规检查快速推送 hotfix。

**操作步骤：**

1. **临时禁用相关 Hook**
   ```bash
   /hookify:disable --hook format-check --temporary
   /hookify:disable --hook test-before-push --temporary
   ```

2. **提交 hotfix**
   *Hook 暂时放行，允许快速修复*

3. **自动恢复** — `--temporary` 标记的 Hook 在 30 分钟后自动重新激活

**结果展示：**

<div class="nm-tip">
📸 <strong>截图待制作</strong>：展示 hookify 临时禁用和自动恢复。运行 <code>bash scripts/screenshot.sh hookify</code> 生成。
</div>

---

## 常见问题

<details class="faq-item">
<summary>Q: Hook 配置文件和手动写 Hook 代码有什么区别？</summary>
<div class="answer">

**A:** hookify 的 Markdown 配置是对 Claude Code 原生 Hook 的高级封装：

- **原生 Hook**：需写 TypeScript/JavaScript 代码，灵活但门槛高
- **hookify Markdown**：声明式配置，用自然语言描述规则，hookify 自动转化为可执行 Hook

适合不需要复杂逻辑的场景（如模式匹配、条件拦截）；复杂逻辑仍建议写原生 Hook。
</div>
</details>

<details class="faq-item">
<summary>Q: 多个 Hook 有冲突怎么办？</summary>
<div class="answer">

**A:** hookify 按优先级处理：

1. **安全 Hook** 优先级最高（即使其他 Hook 放行，安全 Hook 仍可阻止）
2. **作用域从窄到宽**：Plugin > Project > Global
3. **同优先级**：按字母序执行

使用 `/hookify:list --verbose` 查看每个 Hook 的优先级和执行顺序。
</div>
</details>

<details class="faq-item">
<summary>Q: 团队成员可以绕过 Hook 吗？</summary>
<div class="answer">

**A:** hookify 本身不提供强制绕过保护（这是 Git 层面的责任），但提供检测告警：

- 如果检测到 Hook 被删除或修改，下一次运行时会告警
- Project 级别的 Hook 建议配合 `.claude/settings.json` 权限配置限制修改
- 核心安全 Hook 建议放在 Plugin 或 Global 作用域（用户不可修改）
</div>
</details>

---

## 相关插件

### 配合使用

| 插件 | 协作方式 |
|------|----------|
| [leyline](./leyline.md) | leyline 提供注入检测等底层能力，hookify 配置何时触发这些检查 |
| [abstract](./abstract.md) | abstract 开发复杂的自定义 Hook，hookify 管理轻量级规则配置 |
| [sanctum](./sanctum.md) | sanctum 管理 Git 工作流，hookify 在关键节点添加检查 Hook |

---

> 📝 最后更新：2026-06-04
