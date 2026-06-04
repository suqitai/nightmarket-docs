# attune — 全周期项目开发

## 概述

attune 是 Night Market 中最核心的项目管理插件，提供从**头脑风暴 → 规格说明 → 架构规划 → 系统执行 → 代码打磨**的全周期开发流程。它将松散的项目想法转化为结构化、可追踪的开发计划，并逐步落地实施。

**核心能力：**
- 头脑风暴（brainstorm）：通过苏格拉底式提问，将模糊想法转化为结构化项目简报
- 规格说明（specify）：将简报转化为可测试的详细需求规格
- 架构规划（blueprint）：从规格生成依赖排序的实施方案
- 系统执行（execute）：按计划逐步实施，带进度追踪和质量门禁
- 代码打磨（dorodango）：多维度品质优化，在独立子 Agent 中逐步精炼
- 战争会议室（war-room）：多 LLM 专家小组对抗性评审，验证重大决策
- 全自动任务（mission）：自动检测项目状态，路由到正确开发阶段

**适用场景：**
- 从零开始一个新项目，需求还不清晰
- 接手一个已有项目，需要系统性地规划和重构
- 需要对关键架构决策进行多方验证
- 希望建立标准化的项目开发流程
- 代码功能完成但需要多维度品质优化

---

## 安装

```bash
# 安装 attune 插件
claude plugins install attune@claude-night-market

# 验证安装
claude plugins list | grep attune
```

**前置条件：**
- Claude Code 已安装并正常运行
- 建议配合 spec-kit 和 imbue 使用，实现完整的规格驱动开发

---

## 命令参考

| 命令 | 必需参数 | 可选参数 | 说明 | 使用示例 |
|------|----------|----------|------|----------|
| `/attune:brainstorm` | — | `--domain` | 项目头脑风暴，产出项目简报 | `/attune:brainstorm --domain "web application"` |
| `/attune:specify` | — | `--input`, `--feature`, `--clarify` | 将简报转化为详细规格说明 | `/attune:specify --input docs/project-brief.md` |
| `/attune:blueprint` | — | `--input`, `--component`, `--detailed` | 从规格生成实施计划 | `/attune:blueprint --input docs/specification.md --detailed` |
| `/attune:execute` | — | `--plan`, `--phase` | 按计划逐步执行实施 | `/attune:execute --plan docs/implementation-plan.md` |
| `/attune:dorodango` | — | `--file`, `--dimensions` | 多维度代码打磨优化 | `/attune:dorodango --file src/main.py` |
| `/attune:war-room` | — | `--decision`, `--panel-size` | 多 LLM 专家对抗性评审 | `/attune:war-room --decision "选择数据库方案"` |
| `/attune:mission` | — | `--auto` | 自动检测状态并路由到正确阶段 | `/attune:mission --auto` |
| `/attune:project-init` | — | `--lang`, `--name`, `--author` | 初始化新项目结构 | `/attune:project-init --lang python --name my-project` |
| `/attune:validate` | — | `--path` | 验证项目结构和配置 | `/attune:validate --path .` |

---

## 使用场景

### 场景 1：从零开始新项目

**问题：** 你有一个项目想法但需求不清晰，不知道从哪里开始，需要系统性地把想法落地。

**解决方案：** 使用 attune 的全周期流程，从头脑风暴开始逐步推进，每个阶段产出结构化文档。

**命令示例：**
```bash
# 第 1 步：头脑风暴
/attune:brainstorm --domain "web application"
# → 产出 docs/project-brief.md

# 第 2 步：规格说明（自动接续）
# → 产出 docs/specification.md

# 第 3 步：架构规划（自动接续）
# → 产出 docs/implementation-plan.md

# 第 4 步：项目初始化（自动接续）
# → 搭建项目骨架

# 第 5 步：执行实施
/attune:execute
```

**预期结果：** 从模糊想法到可运行的初始版本，每个阶段的决策都有文档记录。

---

### 场景 2：对重大决策进行多方验证

**问题：** 你面临一个重大的技术决策（如选择数据库、架构范式），需要多方意见来避免盲区。

**解决方案：** 使用 war-room 召集多个 LLM 专家角色，从不同维度对抗性评审你的决策。

**命令示例：**
```bash
/attune:war-room --decision "将单体应用拆分为微服务的时机和策略"
```

**预期结果：** 获得包含风险评估、替代方案、可逆性分析的结构化评审报告。

---

### 场景 3：代码完成后的品质打磨

**问题：** 代码功能已实现、测试已通过，但代码质量（可读性、性能、错误处理）还有提升空间。

**解决方案：** 使用 dorodango 在独立子 Agent 中多维度优化代码，每个维度独立评审和改进。

**命令示例：**
```bash
/attune:dorodango --file src/main.py
```

**预期结果：** 代码经过可读性、性能、错误处理、文档等多轮独立优化，每个维度有改善报告。

---

## 实战案例

### 案例 1：用 attune 构建一个 CLI 工具

**背景：** 你想开发一个命令行工具来管理代码片段，但只有初步想法，需要完整的开发流程指导。

**操作步骤：**

1. **启动头脑风暴**
   ```bash
   /attune:brainstorm --domain "CLI tool"
   ```
   *进入苏格拉底式提问，Claude 会引导你定义问题、识别约束、探索方案*

2. **确认项目简报**
   *头脑风暴完成后，自动生成 `docs/project-brief.md`，包含问题陈述、目标、约束、方案选择*

3. **自动进入规格阶段**
   *系统自动调用 `/attune:specify`，生成 24 个功能需求、5 个非功能需求、完整的验收标准*

4. **自动进入规划阶段**
   *系统生成实施计划，包含 35 个依赖排序的任务、预估工时、风险矩阵*

5. **执行第一个阶段**
   ```bash
   /attune:execute --phase 1
   ```
   *按照计划逐步执行基础设施搭建*

**结果展示：**

<!-- TODO: 添加截图 ![attune 头脑风暴流程](/images/attune/case1-brainstorm-flow.png) -->
<div class="nm-tip">
📸 <strong>截图待制作</strong>：展示 attune:brainstorm 的苏格拉底式提问过程。运行 <code>bash scripts/screenshot.sh attune</code> 生成截图。
</div>

---

### 案例 2：用 war-room 评审架构决策

**背景：** 你正在考虑将一个 Django 单体应用拆分为微服务，但担心过早拆分带来的复杂度。

**操作步骤：**

1. **启动战争会议室**
   ```bash
   /attune:war-room --decision "是否应该将 Django 单体拆分为微服务？当前日活 500 用户"
   ```

2. **专家小组评审**
   *系统召集多个 LLM 专家角色（架构师、DevOps 工程师、安全专家、成本分析师），从各自角度给出评估*

3. **获得评审报告**
   *产出包含各维度评分、风险分析、替代方案（如模块化单体）、可逆性评估的综合报告*

**结果展示：**

<!-- TODO: 添加截图 ![war-room 评审结果](/images/attune/case2-warroom-report.png) -->
<div class="nm-tip">
📸 <strong>截图待制作</strong>：展示 war-room 的多维度评分和建议。运行 <code>bash scripts/screenshot.sh attune</code> 生成截图。
</div>

---

## 常见问题

<details class="faq-item">
<summary>Q: attune 和 spec-kit 有什么区别？我该用哪个？</summary>
<div class="answer">

**A:** attune 是**全周期流程管理**，spec-kit 专注于**规格驱动开发**的单个环节。它们是互补关系：

- **attune**：管理 brainstorming → specify → blueprint → execute 的完整流程
- **spec-kit**：在 specify 阶段提供更精细的需求澄清工具

推荐做法：用 attune 管理整体流程，在规格阶段它会自动检测并使用 spec-kit（如果已安装）来增强需求定义能力。
</div>
</details>

<details class="faq-item">
<summary>Q: 头脑风暴中途退出了，怎么恢复？</summary>
<div class="answer">

**A:** 使用恢复功能：

```bash
/attune:brainstorm --resume
```

系统会从 `.attune/brainstorm-session.json` 加载上一次的会话状态，继续未完成的阶段。你也可以直接查看已生成的 `docs/project-brief.md` 了解已完成的讨论。
</div>
</details>

<details class="faq-item">
<summary>Q: war-room 的专家数量和观点是否可靠？</summary>
<div class="answer">

**A:** war-room 默认召集 3-5 个不同角色的 LLM 专家。它通过 **对抗性评审** 机制提升可靠性——每个专家被要求从自己的视角审视决策，提出反对意见。建议你在以下情况使用：

- 决策**不可逆或极难回退**时（如数据库选型、架构范式）
- 你对该领域**不够熟悉**，需要补充视角
- 团队对方案有**分歧**，需要结构化分析

注意：war-room 提供的是分析参考，最终决策仍应由你结合实际情况做出。
</div>
</details>

<details class="faq-item">
<summary>Q: 实施计划能中途修改吗？</summary>
<div class="answer">

**A:** 可以。实施计划是活的文档。你可以：

1. 直接编辑 `docs/implementation-plan.md` 调整任务
2. 在 `/attune:execute` 执行过程中跳过或重新排序任务
3. 完成一个阶段后，重新运行 `/attune:blueprint` 根据实际情况调整后续计划

系统会自动检测变化并调整执行策略。
</div>
</details>

---

## 相关插件

### 配合使用

| 插件 | 协作方式 |
|------|----------|
| [spec-kit](../plugins/spec-kit.md) | 在 specify 阶段提供更精细的需求澄清和验收标准定义 |
| [imbue](../plugins/imbue.md) | 在 execute 阶段强制执行 TDD、质量门禁和评分 |
| [sanctum](../plugins/sanctum.md) | 在执行阶段管理 Git 工作流和版本发布 |
| [pensive](../plugins/pensive.md) | 在 dorodango 阶段辅助代码审查 |

### 替代方案

| 插件 | 差异对比 |
|------|----------|
| [spec-kit](../plugins/spec-kit.md) | 如果你只需要规格定义（不需要全周期管理），spec-kit 更轻量专注 |

---

> 📝 最后更新：2026-06-04
