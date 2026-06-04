# pensive — 多维度代码审查

## 概述

pensive 是 Night Market 中功能最全面的代码审查插件，支持从架构、Bug 检测、安全漏洞、性能、可读性等多个维度对代码进行系统性审查。它内置了 NASA 的 10 条代码规则，也支持自定义审查维度。

**核心能力：**
- 多维度审查：架构/Bug/安全/性能/可维护性/可读性 6 大维度
- NASA 10 条规则：航天级代码质量检查
- 差异审查：只审查变更部分，适合 PR Review
- 严重度分级：Critical/High/Medium/Low 四级，附带修复建议
- 审查报告：结构化输出，可集成 CI

**适用场景：**
- PR 合并前的强制性代码审查
- 遗留代码的质量评估和债务识别
- 安全敏感模块的专项审查
- 新人代码的培训性审查

---

## 安装

```bash
claude plugins install pensive@claude-night-market
claude plugins list | grep pensive
```

---

## 命令参考

| 命令 | 必需参数 | 可选参数 | 说明 | 使用示例 |
|------|----------|----------|------|----------|
| `/pensive:review` | — | `--file`, `--scope`, `--dimensions` | 多维度代码审查 | `/pensive:review --file src/ --dimensions arch,bug,security` |
| `/pensive:review-pr` | — | `--pr`, `--base` | 审查 PR 变更 | `/pensive:review-pr --pr 42` |
| `/pensive:nasa` | — | `--file` | NASA 10 条规则检查 | `/pensive:nasa --file src/critical.py` |
| `/pensive:audit` | — | `--path`, `--severity` | 全量审计，按严重度过滤 | `/pensive:audit --path . --severity critical` |

---

## 使用场景

### 场景 1：PR 多维度审查

**问题：** PR 审查常只看代码风格，遗漏架构问题和安全漏洞。

**解决方案：** 使用 `review-pr` 对 PR 变更做架构、Bug、安全、性能 4 维度自动审查。

**命令示例：**
```bash
/pensive:review-pr --pr 42 --dimensions arch,bug,security,performance
```

**预期结果：** 获得结构化审查报告，问题按严重度排列，Critical 问题附带修复代码建议。

---

### 场景 2：安全敏感模块审查

**问题：** 支付模块上线前需要严格的安全审查。

**解决方案：** 针对特定文件做安全和 Bug 双维度深度审查。

**命令示例：**
```bash
/pensive:review --file src/payment/ --dimensions bug,security --severity critical,high
```

**预期结果：** 只输出 Critical 和 High 级别的问题，避免噪音干扰。

---

## 实战案例

### 案例 1：CI 中集成 pensive 做 PR 门禁

**背景：** 团队需要在 CI 中自动审查所有 PR，Critical 问题阻塞合并。

**操作步骤：**

1. **在 CI 配置中添加 pensive 步骤**
   ```yaml
   - name: Code Review
     run: |
       /pensive:review-pr --pr ${{ github.event.pull_request.number }} --dimensions arch,bug,security,performance
   ```

2. **设置严重度阈值** — Critical 问题直接失败，High 问题告警通知

3. **开发者修复后重新触发** — 审查通过后自动解除阻塞

**结果展示：**

<div class="nm-tip">
📸 <strong>截图待制作</strong>：展示 pensive PR 审查报告。运行 <code>bash scripts/screenshot.sh pensive</code> 生成。
</div>

---

### 案例 2：NASA 规则审查遗留 C 代码

**背景：** 一个嵌入式系统的 C 代码需要满足高可靠性要求。

**操作步骤：**

1. **运行 NASA 10 条检查**
   ```bash
   /pensive:nasa --file src/controller/
   ```

2. **得到 10 条规则逐条检查结果**，如：
   - 规则 2（循环上限）：3 个 while 循环无显式上限
   - 规则 5（函数长度）：2 个函数超过 60 行
   - 规则 9（goto 使用）：发现 1 处 goto 跳转

3. **逐项修复并重新检查**

**结果展示：**

<div class="nm-tip">
📸 <strong>截图待制作</strong>：展示 NASA 规则检查结果。运行 <code>bash scripts/screenshot.sh pensive</code> 生成。
</div>

---

## 常见问题

<details class="faq-item">
<summary>Q: pensive 和普通 linter 有什么区别？</summary>
<div class="answer">

**A:** linter（如 ESLint、Pylint）做**语法和风格**检查。pensive 做**语义和架构**分析：

- Linter：变量未使用、缩进错误、命名规范
- pensive：架构层次混乱、潜在 Bug 模式、安全漏洞、性能反模式

两者互补。建议 CI 中先跑 linter，通过后再跑 pensive。
</div>
</details>

<details class="faq-item">
<summary>Q: 审查报告太长怎么办？</summary>
<div class="answer">

**A:** 几种过滤方式：

```bash
# 只看 Critical 和 High
/pensive:audit --severity critical,high

# 只看安全维度
/pensive:review --dimensions security

# 只看特定文件
/pensive:review --file src/core/
```

首次全量审查问题多很正常，建议优先修复 Critical 然后渐进改善。
</div>
</details>

<details class="faq-item">
<summary>Q: NASA 10 条规则对我的语言适用吗？</summary>
<div class="answer">

**A:** NASA 规则最初为 C 语言设计，但大部分规则是语言无关的：

- 规则 1（简单控制流）— 适用于所有语言
- 规则 2（循环上限）— 适用于所有语言
- 规则 5（函数长度）— 适用于所有语言
- 规则 9（goto）— 仅 C/C++ 等有 goto 的语言

pensive 会根据语言自动调整规则适用范围。
</div>
</details>

---

## 相关插件

### 配合使用

| 插件 | 协作方式 |
|------|----------|
| [scribe](./scribe.md) | pensive 审查代码，scribe 审查文档 → 全项目质量覆盖 |
| [imbue](./imbue.md) | pensive 审查报告作为 imbue 质量门禁的输入 |
| [abstract](./abstract.md) | abstract 的 skills-eval 评估代码质量，pensive 做详细审查 |

---

> 📝 最后更新：2026-06-04
