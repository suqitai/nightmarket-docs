# imbue — TDD 质量门禁

## 概述

imbue 是 Night Market 中负责质量保障的插件，强制执行 TDD（测试驱动开发）工作流，提供 RICE/WSJF/Kano 等多种需求评分模型，并设置可配置的质量门禁。它确保代码「先有测试、再有实现、通过审查」。

**核心能力：**
- TDD 强制执行：红 → 绿 → 重构的严格工作流管控
- 质量门禁：可配置的检查关卡（测试覆盖率、lint 通过、类型检查）
- RICE 评分：基于 Reach/Impact/Confidence/Effort 的需求优先级计算
- WSJF 评分：加权最短作业优先（Weighted Shortest Job First）的敏捷优先级模型
- Kano 模型：需求满意度分类（基本型/期望型/兴奋型）
- 特性审查（feature-review）：评估功能是否值得开发

**适用场景：**
- 团队希望强制执行 TDD 开发纪律
- 需求池太大需要科学的优先级排序
- 需要量化评估功能的投入产出比
- PR 合并前需要多维度质量检查

---

## 安装

```bash
claude plugins install imbue@claude-night-market

# 验证安装
claude plugins list | grep imbue
```

**前置条件：**
- Claude Code 已安装
- 项目需要已有测试框架（如 pytest、jest 等）
- 推荐与 attune 和 spec-kit 配合使用

---

## 命令参考

| 命令 | 必需参数 | 可选参数 | 说明 | 使用示例 |
|------|----------|----------|------|----------|
| `/imbue:tdd` | — | `--file`, `--strict` | 启动 TDD 严格开发流程 | `/imbue:tdd --file src/auth.py --strict` |
| `/imbue:quality-gate` | — | `--level`, `--config` | 设置和执行质量门禁 | `/imbue:quality-gate --level strict` |
| `/imbue:rice` | — | `--items` | RICE 评分排序需求 | `/imbue:rice --items docs/features.md` |
| `/imbue:wsjf` | — | `--backlog` | WSJF 优先级计算 | `/imbue:wsjf --backlog docs/backlog.md` |
| `/imbue:kano` | — | `--feature` | Kano 模型需求分类 | `/imbue:kano --feature "暗黑模式"` |
| `/imbue:feature-review` | — | `--proposal` | 功能价值评审 | `/imbue:feature-review --proposal docs/proposal.md` |
| `/imbue:scope-guard` | — | `--scope` | 范围蔓延检测和告警 | `/imbue:scope-guard --scope docs/specification.md` |

---

## 使用场景

### 场景 1：TDD 红绿重构循环

**问题：** 团队成员经常先写实现再补测试，导致测试覆盖率和质量都不理想。

**解决方案：** 使用 TDD 模式强制执行先写失败测试 → 最小实现 → 重构的循环。

**命令示例：**
```bash
# 启动 TDD 模式
/imbue:tdd --file src/user_service.py --strict
```

**预期结果：** Claude 会要求你先生成测试用例，确认测试失败后，再引导你编写最小实现使测试通过，最后进行重构。任一步骤未完成不允许进入下一步。

---

### 场景 2：需求优先级科学排序

**问题：** Backlog 里有 30 个需求，团队对先做哪个争论不休。

**解决方案：** 使用 RICE 模型对每个需求打分，按分数排序。

**命令示例：**
```bash
/imbue:rice --items docs/features.md
```

**预期结果：** 每个需求获得 RICE 总分和拆解分数（Reach 多少用户、Impact 多大影响、Confidence 多确定、Effort 多少人周），按总分降序排列，决策有据可依。

---

## 实战案例

### 案例 1：用 imbue 管控一个登录功能开发

**背景：** 团队要开发用户登录功能，希望全程强制 TDD。

**操作步骤：**

1. **启动 TDD 流程**
   ```bash
   /imbue:tdd --file src/login.py --strict
   ```

2. **第一阶段：红**
   *Claude 引导编写测试用例：成功登录、密码错误、账号不存在、锁定账号、token 生成*

3. **第二阶段：绿**
   *逐个实现功能使测试通过，每通过一个测试 Claude 确认进度*

4. **第三阶段：重构**
   *提取公共方法、优化异常处理、添加日志*

**结果展示：**

<div class="nm-tip">
📸 <strong>截图待制作</strong>：展示 imbue TDD 的红绿状态切换。运行 <code>bash scripts/screenshot.sh imbue</code> 生成。
</div>

---

### 案例 2：用 RICE 给 Backlog 排序

**背景：** SaaS 产品 Backlog 有 15 个功能需求，需要决定下个 Sprint 做什么。

**操作步骤：**

1. **输入需求列表**
   ```bash
   /imbue:rice --items docs/backlog-q3.md
   ```

2. **逐项评估**
   *Claude 引导你对每个需求估算 Reach/Impact/Confidence/Effort，并给出参数建议*

3. **获得排序结果**
   *导出按 RICE 分数排序的需求列表，附带每项拆解分值和推理*

**结果展示：**

<div class="nm-tip">
📸 <strong>截图待制作</strong>：展示 RICE 评分矩阵和排序结果。运行 <code>bash scripts/screenshot.sh imbue</code> 生成。
</div>

---

## 常见问题

<details class="faq-item">
<summary>Q: 不想每行代码都 TDD，怎么放宽限制？</summary>
<div class="answer">

**A:** 使用非 strict 模式：

```bash
/imbue:tdd --file src/utils.py    # 默认模式，允许跳过简单工具函数
/imbue:tdd --file src/core.py --strict  # 严格模式，每行必须测试先行
```

非 strict 模式下，Claude 会自动判断哪些代码必须 TDD（业务逻辑），哪些可以放宽（简单 getter/setter）。
</div>
</details>

<details class="faq-item">
<summary>Q: RICE、WSJF、Kano 该用哪个模型？</summary>
<div class="answer">

**A:** 按场景选择：

- **RICE**：有明确用户基数和时间估算的产品需求（最通用）
- **WSJF**：敏捷/Scrum 团队，需求之间有明显依赖关系
- **Kano**：在做用户满意度调研和特性分类时（区分基本功能 vs 惊喜功能）

不确定时从 RICE 开始，它最直观也最常用。
</div>
</details>

<details class="faq-item">
<summary>Q: 质量门禁配置太严格导致 PR 无法合并？</summary>
<div class="answer">

**A:** 质量门禁支持渐进式升级。建议策略：

1. 初期设 `--level basic`（仅检查测试是否通过）
2. 团队适应后升级到 `--level standard`（覆盖率 ≥ 80%）
3. 核心模块设 `--level strict`（覆盖率 ≥ 95% + 类型检查 + lint 零告警）

门禁配置存储在项目根目录的 `.imbue/gates.yml` 中，可按目录设置不同级别。
</div>
</details>

---

## 相关插件

### 配合使用

| 插件 | 协作方式 |
|------|----------|
| [attune](./attune.md) | attune 执行阶段自动触发 imbue 的质量门禁 |
| [spec-kit](./spec-kit.md) | imbue 读取 spec-kit 生成的验收标准，转化为 TDD 测试用例 |
| [pensive](./pensive.md) | pensive 代码审查通过后，imbue 质量门禁才放行 |

### 替代方案

| 插件 | 差异对比 |
|------|----------|
| [pensive](./pensive.md) | pensive 做代码审查（静态分析），imbue 做流程管控（动态门禁），互补而非替代 |

---

> 📝 最后更新：2026-06-04
