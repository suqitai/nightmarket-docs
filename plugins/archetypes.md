# archetypes — 架构范式选择

## 概述

archetypes 是 Night Market 中的架构决策辅助工具，内置 14 种经过验证的架构范式（六边形架构、CQRS、微服务、事件溯源等）。它根据你的项目需求推荐最合适的架构范式，并生成对应的项目脚手架。

**核心能力：**
- 14 种架构范式：六边形、CQRS、事件驱动、微服务、分层架构等
- 需求驱动的推荐：根据项目特征（规模、并发、团队）推荐范式
- 范式对比：多范式并排比较，附权衡分析
- 脚手架生成：选中范式后自动生成项目结构

**适用场景：**
- 新项目启动时选架构范式
- 评估现有架构是否需要切换
- 学习不同架构范式的适用场景
- 重构前探索更好的架构选项

---

## 安装

```bash
claude plugins install archetypes@claude-night-market
claude plugins list | grep archetypes
```

---

## 命令参考

| 命令 | 必需参数 | 可选参数 | 说明 | 使用示例 |
|------|----------|----------|------|----------|
| `/archetypes:select` | — | `--domain`, `--requirements` | 根据需求推荐架构范式 | `/archetypes:select --domain "电商平台"` |
| `/archetypes:compare` | `--a`, `--b` | `--criteria` | 并排比较两种范式 | `/archetypes:compare --a hexagonal --b layered` |
| `/archetypes:list` | — | `--domain` | 列出所有范式及简介 | `/archetypes:list --domain web` |
| `/archetypes:scaffold` | `--archetype` | `--lang`, `--name` | 按范式生成项目脚手架 | `/archetypes:scaffold --archetype hexagonal --lang python` |
| `/archetypes:audit` | `--path` | `--expected` | 审计现有代码是否符合范式 | `/archetypes:audit --path src/ --expected hexagonal` |

---

## 使用场景

### 场景 1：新项目架构选型

**问题：** 要做一个 SaaS 产品，不确定用单体还是微服务，六边形还是分层。

**解决方案：** 用 select 描述项目特征，archetypes 推荐最佳范式。

**命令示例：**
```bash
/archetypes:select --domain "SaaS 多租户 B2B 平台"
```

**预期结果：** 分析需求特征（多租户、B2B、预计 500+ 租户），推荐「模块化单体 + 六边形架构」并附推理——当前规模下微服务收益不足以抵消复杂度。

---

### 场景 2：范式合规审计

**问题：** 项目宣称使用六边形架构，但端口和适配器边界模糊。

**解决方案：** 用 audit 检查实际代码结构是否符合范式规范。

**命令示例：**
```bash
/archetypes:audit --path src/ --expected hexagonal
```

**预期结果：** 报告显示 3 处违规：领域层直接 import 了数据库驱动、端口接口未定义、适配器与领域耦合。

---

## 实战案例

### 案例 1：从单体到微服务的渐进式拆分

**背景：** 一个快速增长的 Django 单体，日活从 500 增长到 50000，团队从 3 人扩展到 20 人。

**操作步骤：**

1. **评估是否需要切换**
   ```bash
   /archetypes:compare --a modular-monolith --b microservices --criteria "django,50k-dau,20-devs"
   ```

2. **获得对比报告** — modular-monolith 评分 72 vs 微服务评分 68

3. **结论**：先做模块化单体改造（低风险高收益），1 年后视增长再评估微服务

**结果展示：**

![archetypes 终端预览](/images/archetypes/terminal-preview.png)

*（占位截图 — 用 phantom 替换为实际操作截图）*

---

## 常见问题

<details class="faq-item">
<summary>Q: 14 种范式中哪个最常用？</summary>
<div class="answer">

**A:** 按使用频率：

1. **六边形架构**（端口与适配器）— 最通用，适合 80% 的业务项目
2. **分层架构** — 简单 CRUD 应用
3. **CQRS** — 读写负载差异大的场景
4. **事件驱动** — 异步和实时处理需求
5. **微服务** — 大规模多团队场景

不确定时从六边形架构开始，它提供了最清晰的依赖方向。
</div>
</details>

<details class="faq-item">
<summary>Q: scaffold 生成的项目能直接用吗？</summary>
<div class="answer">

**A:** scaffold 生成的是**经过范式验证的项目骨架**，包含正确的目录结构和依赖方向。它不包含业务逻辑，但包含：

- 正确的包/模块划分（如六边形的 domain/application/infrastructure）
- 基础接口定义
- 依赖注入的基本结构

可以作为项目的起点，在上面添加业务代码。配合 `/attune:project-init` 使用效果更佳。
</div>
</details>

---

## 相关插件

| 插件 | 协作方式 |
|------|----------|
| [cartograph](./cartograph.md) | archetypes 选完范式后，cartograph 可视化生成的架构 |
| [attune](./attune.md) | attune 项目初始化时可用 archetypes 进行架构选型 |

---

> 📝 最后更新：2026-06-04
