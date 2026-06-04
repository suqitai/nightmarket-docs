# spec-kit — 规格驱动开发

## 概述

spec-kit 是 Night Market 中的规格驱动开发工具，专注于将模糊需求转化为结构化、可测试的规格说明。它提供需求澄清、规格编写、任务分解的完整工作流，确保开发「做正确的事」而非仅仅「正确地做事」。

**核心能力：**
- 需求澄清（clarify）：对已有规格进行歧义检测和细化提问
- 规格编写（specify）：按结构化模板生成详细规格说明
- 任务分解（plan/tasks）：从规格自动生成依赖排序的任务列表
- 验收标准锚定：每个需求绑定 Given-When-Then 格式的测试标准
- 章程合规检查：确保规格符合项目章程和架构约束

**适用场景：**
- 接手需求模糊的项目，需要系统性地澄清和定义
- 需要生成可测试的需求文档，对接后续 TDD 流程
- 多人协作项目，需要统一的需求理解基线
- 复杂功能需要分步骤拆解为可管理的任务

---

## 安装

```bash
claude plugins install spec-kit@claude-night-market

# 验证安装
claude plugins list | grep spec-kit
```

**前置条件：**
- Claude Code 已安装
- 建议搭配 attune 使用（attune 在 specify 阶段会自动调用 spec-kit 增强）

---

## 命令参考

| 命令 | 必需参数 | 可选参数 | 说明 | 使用示例 |
|------|----------|----------|------|----------|
| `/speckit-specify` | — | `--input`, `--feature`, `--output` | 从简报生成详细规格 | `/speckit-specify --feature "用户认证"` |
| `/speckit-clarify` | — | `--spec`, `--depth` | 检测规格中的歧义并细化 | `/speckit-clarify --spec docs/specification.md` |
| `/speckit-plan` | — | `--spec`, `--sprint-length` | 从规格生成实施计划 | `/speckit-plan --spec docs/specification.md` |
| `/speckit-tasks` | — | `--plan`, `--format` | 从计划生成可执行任务列表 | `/speckit-tasks --plan docs/implementation-plan.md` |
| `/speckit-constitution` | — | `--set`, `--show` | 管理项目章程和架构约束 | `/speckit-constitution --show` |
| `/speckit-analyze` | — | `--input` | 分析需求完整性和一致性 | `/speckit-analyze --input docs/requirements.md` |

---

## 使用场景

### 场景 1：澄清模糊需求

**问题：** 产品给的 PRD 充满「系统应该快」「用户体验要好」这类不可测试的描述，开发无法直接使用。

**解决方案：** 使用 clarify 模式对 PRD 进行系统性歧义检测，自动生成需要澄清的问题清单。

**命令示例：**
```bash
/speckit-clarify --spec docs/prd-draft.md --depth high
```

**预期结果：** 获得一份结构化的问题清单，每项都有关键词指明歧义类型（性能指标缺失、边界条件不明、并发场景未定义等），可直接发给产品确认。

---

### 场景 2：从功能描述生成可测试规格

**问题：** 你有一个功能描述但需要转化为团队可执行、测试可验证的需求文档。

**解决方案：** 使用 specify 生成包含功能和验收标准的完整规格。

**命令示例：**
```bash
/speckit-specify --feature "用户可以通过邮箱和密码注册账号，需要邮箱验证"
```

**预期结果：** 自动生成包含邮箱格式校验、密码强度规则、验证邮件发送、过期重发、异常处理等完整场景的规格说明，每个场景都有 Given-When-Then 验收标准。

---

## 实战案例

### 案例 1：用 spec-kit 澄清一个电商需求

**背景：** 团队接到「实现购物车功能」的需求，但这个描述过于简单，缺少大量细节。

**操作步骤：**

1. **提交需求描述**
   ```bash
   /speckit-clarify --spec docs/cart-requirement-v1.md
   ```

2. **查看澄清结果**
   *spec-kit 检测到 12 个歧义点，包括：未登录时加购行为、库存不足处理、多端同步策略、优惠券叠加规则、价格变动通知等*

3. **补充回答后生成规格**
   ```bash
   /speckit-specify --feature "购物车功能" --input docs/cart-answers.md
   ```

4. **审查生成的规格**
   *获得包含 18 个功能需求、45 条验收标准的完整规格文档*

**结果展示：**

![spec-kit 终端预览](/images/spec-kit/terminal-preview.png)

*（占位截图 — 用 phantom 替换为实际操作截图）*

---

### 案例 2：从规格到任务的一键分解

**背景：** 规格文档已完成，需要拆分为开发任务分配给团队。

**操作步骤：**

1. **生成实施计划**
   ```bash
   /speckit-plan --spec docs/specification.md --sprint-length 2w
   ```

2. **生成任务列表**
   ```bash
   /speckit-tasks --plan docs/implementation-plan.md --format markdown
   ```

**结果展示：**

![spec-kit 终端预览](/images/spec-kit/terminal-preview.png)

*（占位截图 — 用 phantom 替换为实际操作截图）*

---

## 常见问题

<details class="faq-item">
<summary>Q: spec-kit 和 attune 的 specify 有什么区别？</summary>
<div class="answer">

**A:** 两者在功能上有重叠但侧重不同：

- **attune specify**：作为全周期流程的一个环节，侧重「从简报驱动」的规格生成，自动接续头脑风暴的结果
- **spec-kit**：提供更精细的规格工程能力，可以独立分析任意需求文档、检测歧义、管理章程，更适合已有部分需求的场景

两者可以配合使用：attune 在流程中检测到 spec-kit 已安装时，会自动调用其增强能力。
</div>
</details>

<details class="faq-item">
<summary>Q: clarify 检测出来的问题太多怎么办？</summary>
<div class="answer">

**A:** 使用 `--depth` 参数控制粒度：

```bash
/speckit-clarify --depth low     # 只检测阻塞性问题
/speckit-clarify --depth medium  # 默认级别
/speckit-clarify --depth high    # 全面检测（问题较多）
```

建议先按优先级回答阻塞性问题（标记为 P0 的），其余可以在开发过程中逐步澄清。
</div>
</details>

<details class="faq-item">
<summary>Q: 规格写完后需求变了怎么办？</summary>
<div class="answer">

**A:** spec-kit 支持增量更新。修改需求描述后重新运行：

```bash
/speckit-specify --feature "更新后的功能描述" --base docs/specification.md
```

系统会生成变更 diff，只更新受影响的需求和验收标准，保留未变更部分。
</div>
</details>

---

## 相关插件

### 配合使用

| 插件 | 协作方式 |
|------|----------|
| [attune](./attune.md) | attune 的全周期流程自动调用 spec-kit 增强规格阶段 |
| [imbue](./imbue.md) | imbue 读取 spec-kit 的验收标准，强制执行 TDD 质量门禁 |
| [abstract](./abstract.md) | 用 abstract 评估 spec-kit 生成的规格质量 |

### 替代方案

| 插件 | 差异对比 |
|------|----------|
| [attune](./attune.md) | 如果你需要的是全周期项目管理，而非单纯的规格工程能力 |

---

> 📝 最后更新：2026-06-04
