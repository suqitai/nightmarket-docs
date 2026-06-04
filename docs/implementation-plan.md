# NightMarket 插件使用说明书 — 实施计划 v0.1.0

**作者**：Claude Code 用户
**日期**：2026-06-04
**状态**：草稿
**来源**：[规格说明](./specification.md) | [项目简报](./project-brief.md)

---

## 1. 系统架构

### 1.1 架构概览

本项目为纯静态文档站点，无后端服务。采用 **内容驱动 + 构建时生成** 架构。

```
                        ┌──────────────────────────┐
                        │      GitHub Actions       │
                        │   (CI/CD 自动部署)         │
                        └────────────┬─────────────┘
                                     │ 触发 (push to main)
                                     ▼
┌──────────────┐   构建生成    ┌──────────────┐   部署    ┌──────────────┐
│   Markdown   │─────────────▶│   VitePress   │─────────▶│ GitHub Pages │
│  文档源码     │              │  静态站点生成  │           │ 静态托管     │
│  (23 插件)   │              │              │           │              │
└──────┬───────┘              └──────┬───────┘           └──────┬───────┘
       │                             │                          │
       │ 引用                        │ 复制                     │ 访问
       ▼                             ▼                          ▼
┌──────────────┐              ┌──────────────┐           ┌──────────────┐
│   public/    │              │  .vitepress/ │           │   用  户     │
│  媒体素材     │              │   dist/      │           │  浏览器      │
│ images/gifs  │              │  静态文件     │           │              │
└──────────────┘              └──────────────┘           └──────────────┘
```

### 1.2 组件设计

#### 组件 1：VitePress 站点引擎

**职责**：Markdown → 静态 HTML 站点
**技术**：VitePress ^1.x
**配置**：`.vitepress/config.ts`
**关键能力**：
- Markdown 渲染（含 Vue 组件嵌入）
- 侧边栏/导航栏自动生成
- 内置全文搜索（minisearch）
- 主题定制（CSS 变量覆盖）

#### 组件 2：插件文档内容（23 个 Markdown 文件）

**职责**：每个插件的完整中文使用说明
**位置**：`docs/plugins/*.md`
**模板**：`docs/.templates/plugin-page.md`
**结构**：概述 → 安装 → 命令参考 → 使用场景 → 实战案例 → FAQ → 相关插件

#### 组件 3：导航系统

**职责**：双入口导航（插件分类 + 使用场景）
**位置**：
- 侧边栏：`config.ts` → `sidebar` 配置
- 顶部导航：`config.ts` → `nav` 配置
- 插件索引页：`docs/plugin-index.md`
- 场景导航页：`docs/scenario-nav.md`

#### 组件 4：媒体素材库

**职责**：组织截图和录屏素材
**位置**：`public/images/` + `public/gifs/`
**工具**：phantom（截图）、scry（录屏）
**规范**：按插件名分目录，描述性命名

#### 组件 5：CI/CD 管道

**职责**：自动化构建、验证、部署
**技术**：GitHub Actions
**配置**：`.github/workflows/deploy.yml`
**流程**：代码推送 → 安装依赖 → 构建验证 → 部署到 GitHub Pages

#### 组件 6：质量验证脚本

**职责**：模板一致性、死链检测
**位置**：`scripts/validate.sh`
**触发**：手动运行 + CI 自动执行

### 1.3 数据流

```
用户编写 Markdown 文档
        │
        ▼
  Git Push 到 main 分支
        │
        ▼
  GitHub Actions 触发
        │
        ├──▶ npm ci (安装依赖)
        │
        ├──▶ scripts/validate.sh (模板一致性检查)
        │
        ├──▶ npm run docs:build (VitePress 构建)
        │         │
        │         ├── 解析 Markdown → HTML
        │         ├── 生成搜索索引
        │         ├── 复制 public/ 到 dist/
        │         └── 输出 .vitepress/dist/
        │
        └──▶ deploy to GitHub Pages (gh-pages 分支)
                  │
                  ▼
            用户访问 https://<user>.github.io/<repo>/
```

### 1.4 导航架构

```
首页 (/)
├── 欢迎信息
├── 快速入口（搜索框 + 热门插件）
└── 分类卡片预览

插件索引 (/plugin-index.html)
├── 🔧 开发流程 (attune, spec-kit, imbue, sanctum)
├── 📝 代码质量 (pensive, scribe, abstract)
├── 🏗️ 架构设计 (archetypes, cartograph)
├── 🔒 安全基础设施 (leyline, hookify)
├── 🤖 Agent 编排 (egregore, conjure, minister)
├── 📚 知识管理 (gauntlet, tome, memory-palace)
├── 🎬 媒体制作 (phantom, scry)
├── 📢 通知集成 (herald)
└── ⚡ 性能优化 (conserve, parseltongue, oracle)

场景导航 (/scenario-nav.html)
├── 🚀 从零开始新项目
├── 🔍 代码审查
├── 🏗️ 架构重构
├── 🤖 多 Agent 协作
├── 📖 学习代码库
├── 🔒 插件安全开发
├── 📢 团队协作
└── ⚡ 性能调优

插件详情 (/plugins/<name>.html) × 23
├── 概述
├── 安装
├── 命令参考
├── 使用场景 (≥ 2)
├── 实战案例 (≥ 2, 含截图/录屏)
├── 常见问题 (≥ 3)
└── 相关插件

关于 (/about.html)
└── 项目说明 + 贡献指南链接
```

---

## 2. 任务分解

### 2.1 阶段总览

| 阶段 | 名称 | 任务数 | 预计工作量 | 关键交付物 |
|------|------|:---:|:---:|------|
| 1 | 基础设施 | 5 | 2-3 天 | VitePress 站点骨架 + CI/CD 打通 + 模板验证 |
| 2 | 核心插件 I：开发流程 + 代码质量 | 7 | 3-4 天 | 7 个插件完整文档 + 媒体素材 |
| 3 | 核心插件 II：安全 + Agent | 5 | 2-3 天 | 5 个插件完整文档 + 媒体素材 |
| 4 | 扩展插件 I：架构 + 知识 | 5 | 2-3 天 | 5 个插件完整文档 + 媒体素材 |
| 5 | 扩展插件 II：媒体/通知/性能 | 6 | 2-3 天 | 6 个插件完整文档 + 媒体素材 |
| 6 | 导航完善 + 质量收尾 | 6 | 2-3 天 | 索引页 + 场景页 + QA 通过 |
| **总计** | | **34** | **12-18 天** | 站点上线 |

---

### 2.2 阶段 1：基础设施

---

### TASK-001：初始化 VitePress 项目结构

**描述**：创建 VitePress 项目骨架，配置站点元数据、目录结构。

**类型**：Implementation
**优先级**：P0（阻塞所有后续任务）
**预估工时**：2h
**依赖**：无

**验收标准**：
- [ ] `package.json` 包含 VitePress 依赖
- [ ] `.vitepress/config.ts` 配置站点标题、描述、语言
- [ ] 目录结构按规格说明创建（`docs/plugins/`, `public/images/`, `public/gifs/`, `scripts/`）
- [ ] `npm run docs:dev` 本地开发服务器正常启动
- [ ] `npm run docs:build` 成功生成静态文件
- [ ] `.gitignore` 包含 `.vitepress/dist/`, `.vitepress/cache/`, `node_modules/`

**技术说明**：
- VitePress 使用 ESM 导入、TypeScript 配置
- 初始配置仅包含首页，插件页面后续逐步添加

---

### TASK-002：配置 GitHub 仓库和 CI/CD

**描述**：初始化 Git 仓库，配置 GitHub Actions 自动部署到 GitHub Pages。

**类型**：Implementation
**优先级**：P0（阻塞部署）
**预估工时**：1.5h
**依赖**：TASK-001

**验收标准**：
- [ ] Git 仓库初始化完成，关联 GitHub 远程仓库
- [ ] `.github/workflows/deploy.yml` 配置完整（安装 → 构建 → 部署）
- [ ] GitHub Pages 在仓库设置中启用，Source 设为 GitHub Actions
- [ ] 推送代码后，GitHub Actions 自动触发且运行成功
- [ ] 站点可通过 GitHub Pages URL 访问（初始状态，仅有首页）
- [ ] `README.md` 包含项目说明和本地开发指引

---

### TASK-003：设计并验证文档模板

**描述**：创建插件页面 Markdown 模板，用 3 个核心插件（attune、leyline、pensive）验证模板可行性。

**类型**：Design + Implementation
**优先级**：P0（阻塞后续内容编写）
**预估工时**：4h
**依赖**：TASK-001

**验收标准**：
- [ ] `docs/.templates/plugin-page.md` 模板文件创建完成
- [ ] 模板包含全部必需章节（概述、安装、命令参考、使用场景、实战案例、FAQ、相关插件）
- [ ] 模板包含注释说明，指导填充各章节内容
- [ ] 用 attune 插件作为第一个完整示例，验证模板可用性
- [ ] 用 leyline 插件验证模板的通用性（不同类型插件的适配）
- [ ] 用 pensive 插件做第三次验证，确认模板无需再调整
- [ ] 3 个示例页面的结构一致性检查通过

---

### TASK-004：建立媒体素材工作流

**描述**：编写 phantom 截图和 scry 录屏的自动化脚本，建立素材目录规范。

**类型**：Implementation
**优先级**：P1（内容编写时需要）
**预估工时**：3h
**依赖**：TASK-001

**验收标准**：
- [ ] `scripts/screenshot.sh` 脚本：接收插件名作为参数，使用 phantom 捕获终端截图
- [ ] `scripts/record.sh` 脚本：接收插件名作为参数，使用 scry 录制终端操作 GIF
- [ ] `public/images/{plugin-name}/` 和 `public/gifs/{plugin-name}/` 目录结构就绪
- [ ] 脚本生成的素材自动按正确目录存放
- [ ] `docs/media-inventory.md` 清单模板就绪，记录每个素材文件的信息
- [ ] 至少为 1 个插件（如 attune）成功生成示例截图和录屏

---

### TASK-005：VitePress 主题定制

**描述**：定制 VitePress 默认主题，使其匹配 NightMarket 品牌风格。

**类型**：Implementation
**优先级**：P2
**预估工时**：2h
**依赖**：TASK-001

**验收标准**：
- [ ] `.vitepress/theme/style.css` 自定义 CSS 变量（主色调、字体、间距）
- [ ] `.vitepress/theme/index.ts` 主题入口文件配置
- [ ] 首页 Hero 区域包含项目名称、简介、快速开始按钮
- [ ] 代码块样式清晰（语法高亮、复制按钮）
- [ ] 自定义容器样式（info/tip/warning/danger）配色协调
- [ ] 中文 Web 字体配置（如 Noto Sans SC 或系统默认中文字体栈）

---

### 2.3 阶段 2：核心插件 I — 开发流程 + 代码质量（7 个插件）

---

### TASK-006：attune 插件文档

**描述**：编写 attune（全周期项目开发）插件的完整中文文档。

**类型**：Documentation
**优先级**：P0
**预估工时**：3h
**依赖**：TASK-003

**验收标准**：
- [ ] 概述：介绍 attune 的全周期项目管理能力（brainstorm → specify → blueprint → execute → dorodango）
- [ ] 安装：准确的安装命令，含前置条件
- [ ] 命令参考：`/attune:brainstorm`, `/attune:specify`, `/attune:blueprint`, `/attune:execute`, `/attune:mission`, `/attune:dorodango`, `/attune:war-room` 等完整命令表格
- [ ] 使用场景 ≥ 2：从零开始新项目、中途恢复项目开发
- [ ] 实战案例 ≥ 2：完整走通一个项目全流程；war-room 专家评审
- [ ] FAQ ≥ 3
- [ ] 相关插件：spec-kit（配合）、imbue（质量门禁）
- [ ] ≥ 1 张截图 + 1 段录屏

---

### TASK-007：spec-kit 插件文档

**描述**：编写 spec-kit（规格驱动开发）插件文档。

**类型**：Documentation
**优先级**：P0
**预估工时**：2.5h
**依赖**：TASK-003

**验收标准**：
- [ ] 完整模板各章节填充
- [ ] 命令参考覆盖 `/speckit-specify`, `/speckit-clarify`, `/speckit-plan`, `/speckit-tasks` 等
- [ ] 使用场景 ≥ 2
- [ ] 实战案例 ≥ 2，含截图/录屏
- [ ] 相关插件：attune（集成使用）

---

### TASK-008：imbue 插件文档

**描述**：编写 imbue（TDD 强制执行、质量门禁）插件文档。

**类型**：Documentation
**优先级**：P1
**预估工时**：2.5h
**依赖**：TASK-003

**验收标准**：
- [ ] 完整模板各章节填充
- [ ] 覆盖 TDD 工作流、RICE/WSJF/Kano 评分功能
- [ ] 实战案例包含质量门禁配置场景
- [ ] 相关插件：attune（执行阶段集成）、pensive（代码审查配合）

---

### TASK-009：sanctum 插件文档

**描述**：编写 sanctum（Git 工作流管理）插件文档。

**类型**：Documentation
**优先级**：P1
**预估工时**：2h
**依赖**：TASK-003

**验收标准**：
- [ ] 完整模板各章节填充
- [ ] 覆盖 Commit、PR、版本管理功能
- [ ] 实战案例包含标准 PR 工作流

---

### TASK-010：pensive 插件文档

**描述**：编写 pensive（多维度代码审查）插件文档。

**类型**：Documentation
**优先级**：P0
**预估工时**：2.5h
**依赖**：TASK-003

**验收标准**：
- [ ] 完整模板各章节填充
- [ ] 覆盖架构审查、Bug 检测、安全检查、NASA 10 条
- [ ] 实战案例展示多维度审查流程
- [ ] 相关插件：scribe（文档审查配合）、imbue（质量门禁）

---

### TASK-011：scribe 插件文档

**描述**：编写 scribe（文档审查、AI 废话检测）插件文档。

**类型**：Documentation
**优先级**：P1
**预估工时**：2h
**依赖**：TASK-003

**验收标准**：
- [ ] 完整模板各章节填充
- [ ] 覆盖文档质量审查、AI 废话检测功能
- [ ] 相关插件：pensive（代码+文档联合审查）

---

### TASK-012：abstract 插件文档

**描述**：编写 abstract（Skill/Hook 编写和评估）插件文档。

**类型**：Documentation
**优先级**：P1
**预估工时**：2.5h
**依赖**：TASK-003

**验收标准**：
- [ ] 完整模板各章节填充
- [ ] 覆盖 create-skill, create-hook, skills-eval, hooks-eval 等核心命令
- [ ] 实战案例包含从零创建和评估一个 skill
- [ ] 相关插件：leyline（安全开发）、hookify（Hook 规则引擎）

---

### 2.4 阶段 3：核心插件 II — 安全 + Agent（5 个插件）

---

### TASK-013：leyline 插件文档

**描述**：编写 leyline（基础安全设施）插件文档。

**类型**：Documentation
**优先级**：P0
**预估工时**：3h
**依赖**：TASK-003

**验收标准**：
- [ ] 完整模板各章节填充
- [ ] 覆盖认证模式、配额管理、注入检测、供应链审计等核心安全功能
- [ ] 实战案例包含安全审计完整流程
- [ ] 相关插件：hookify（Hook 安全规则）、abstract（安全开发规范）

---

### TASK-014：hookify 插件文档

**描述**：编写 hookify（行为规则引擎）插件文档。

**类型**：Documentation
**优先级**：P1
**预估工时**：2h
**依赖**：TASK-003

**验收标准**：
- [ ] 完整模板各章节填充
- [ ] 覆盖 Markdown 配置安全 Hook 的方式
- [ ] 实战案例包含自定义 Hook 规则编写

---

### TASK-015：egregore 插件文档

**描述**：编写 egregore（自主 Agent 编排）插件文档。

**类型**：Documentation
**优先级**：P1
**预估工时**：2.5h
**依赖**：TASK-003

**验收标准**：
- [ ] 完整模板各章节填充
- [ ] 覆盖并行 worktree、崩溃恢复、多 Agent 协调
- [ ] 实战案例展示多 Agent 并行任务
- [ ] 相关插件：conjure（外部 LLM 委托）、minister（Issue 管理）

---

### TASK-016：conjure 插件文档

**描述**：编写 conjure（外部 LLM 委托）插件文档。

**类型**：Documentation
**优先级**：P2
**预估工时**：2h
**依赖**：TASK-003

**验收标准**：
- [ ] 完整模板各章节填充
- [ ] 覆盖 Gemini、Qwen 等外部模型委托
- [ ] 实战案例展示任务分发流程

---

### TASK-017：minister 插件文档

**描述**：编写 minister（GitHub Issue 管理）插件文档。

**类型**：Documentation
**优先级**：P2
**预估工时**：2h
**依赖**：TASK-003

**验收标准**：
- [ ] 完整模板各章节填充
- [ ] 覆盖 Issue 管理、看板仪表盘
- [ ] 相关插件：herald（通知集成）

---

### 2.5 阶段 4：扩展插件 I — 架构 + 知识（5 个插件）

---

### TASK-018：archetypes 插件文档

**描述**：编写 archetypes（架构范式选择）插件文档。

**类型**：Documentation
**优先级**：P2
**预估工时**：2.5h
**依赖**：TASK-003

**验收标准**：
- [ ] 覆盖 14 种架构范式（六边形、CQRS、微服务等）
- [ ] 实战案例包含架构选型决策过程
- [ ] 相关插件：cartograph（架构可视化）

---

### TASK-019：cartograph 插件文档

**描述**：编写 cartograph（代码可视化）插件文档。

**类型**：Documentation
**优先级**：P2
**预估工时**：2h
**依赖**：TASK-003

**验收标准**：
- [ ] 覆盖架构图、数据流图、依赖图、调用链生成
- [ ] 实战案例展示可视化输出

---

### TASK-020：gauntlet 插件文档

**描述**：编写 gauntlet（代码库学习）插件文档。

**类型**：Documentation
**优先级**：P2
**预估工时**：2h
**依赖**：TASK-003

**验收标准**：
- [ ] 覆盖知识图谱构建、间隔重复挑战
- [ ] 相关插件：tome（多源研究配合）

---

### TASK-021：tome 插件文档

**描述**：编写 tome（多源研究）插件文档。

**类型**：Documentation
**优先级**：P2
**预估工时**：2.5h
**依赖**：TASK-003

**验收标准**：
- [ ] 覆盖代码考古、HN/Reddit、arXiv、TRIZ 等多源研究
- [ ] 实战案例展示研究流程

---

### TASK-022：memory-palace 插件文档

**描述**：编写 memory-palace（空间记忆宫殿知识管理）插件文档。

**类型**：Documentation
**优先级**：P2
**预估工时**：2h
**依赖**：TASK-003

**验收标准**：
- [ ] 覆盖知识管理理念和使用方法
- [ ] 相关插件：gauntlet、tome（知识管理工具链）

---

### 2.6 阶段 5：扩展插件 II — 媒体/通知/性能（6 个插件）

---

### TASK-023：phantom 插件文档

**描述**：编写 phantom（桌面自动化）插件文档。

**类型**：Documentation
**优先级**：P2
**预估工时**：2h
**依赖**：TASK-003, TASK-004

**验收标准**：
- [ ] 覆盖截图、鼠标键盘控制功能
- [ ] 实战案例直接引用本项目自身的截图工作流
- [ ] 相关插件：scry（录屏配合）

---

### TASK-024：scry 插件文档

**描述**：编写 scry（媒体生成）插件文档。

**类型**：Documentation
**优先级**：P2
**预估工时**：2h
**依赖**：TASK-003, TASK-004

**验收标准**：
- [ ] 覆盖终端录制、浏览器录制、GIF 生成
- [ ] 实战案例直接引用本项目自身的录屏工作流
- [ ] 相关插件：phantom（截图配合）

---

### TASK-025：herald 插件文档

**描述**：编写 herald（通知系统）插件文档。

**类型**：Documentation
**优先级**：P2
**预估工时**：1.5h
**依赖**：TASK-003

**验收标准**：
- [ ] 覆盖 GitHub Issue、Slack、Discord webhook 通知
- [ ] 实战案例展示通知配置流程

---

### TASK-026：conserve 插件文档

**描述**：编写 conserve（上下文优化）插件文档。

**类型**：Documentation
**优先级**：P2
**预估工时**：2h
**依赖**：TASK-003

**验收标准**：
- [ ] 覆盖上下文优化、膨胀检测、Token 节省
- [ ] 相关插件：parseltongue（Python 性能）

---

### TASK-027：parseltongue 插件文档

**描述**：编写 parseltongue（Python 开发套件）插件文档。

**类型**：Documentation
**优先级**：P2
**预估工时**：2h
**依赖**：TASK-003

**验收标准**：
- [ ] 覆盖测试、性能分析、异步模式
- [ ] 相关插件：conserve（性能优化配合）

---

### TASK-028：oracle 插件文档

**描述**：编写 oracle（ONNX Runtime 本地 ML 推理）插件文档。

**类型**：Documentation
**优先级**：P2
**预估工时**：2h
**依赖**：TASK-003

**验收标准**：
- [ ] 覆盖 ONNX 模型加载和本地推理
- [ ] 实战案例展示本地 ML 推理场景

---

### 2.7 阶段 6：导航完善 + 质量收尾

---

### TASK-029：插件分类索引页

**描述**：创建 `plugin-index.md`，按 9 大功能域展示全部 23 个插件卡片。

**类型**：Implementation
**优先级**：P1
**预估工时**：3h
**依赖**：TASK-003（页面设计依赖），TASK-006 ~ TASK-028（内容链接依赖）

**验收标准**：
- [ ] 页面按功能域分组，每组包含插件卡片
- [ ] 每个卡片包含：插件名、一句话中文描述、分类标签、链接
- [ ] 每组显示插件数量统计
- [ ] 9 个功能域全部有代表性图标
- [ ] 页面响应式：桌面 3 列、平板 2 列、手机 1 列
- [ ] 全部 23 个插件卡片链接有效

---

### TASK-030：场景化导航页

**描述**：创建 `scenario-nav.md`，按 8 大使用场景推荐插件组合。

**类型**：Implementation
**优先级**：P1
**预估工时**：2.5h
**依赖**：TASK-029

**验收标准**：
- [ ] 8 个场景卡片全部创建
- [ ] 每个场景包含：名称、描述、推荐插件列表（含链接）、简要工作流说明
- [ ] 至少 3 个场景包含 ASCII 流程图或 mermaid 流程图
- [ ] 所有插件链接有效

---

### TASK-031：全局搜索优化

**描述**：配置并测试 VitePress 内置搜索（minisearch），确保中英文搜索体验良好。

**类型**：Configuration
**优先级**：P1
**预估工时**：1.5h
**依赖**：TASK-006 ~ TASK-028（需有足够内容才能测试搜索质量）

**验收标准**：
- [ ] 搜索框在任意页面可用（Ctrl+K 快捷键）
- [ ] 中文关键词搜索返回相关结果（如"代码审查" → pensive、scribe 页面）
- [ ] 英文关键词搜索返回相关结果（如"attune" → attune 页面）
- [ ] 搜索结果包含内容预览片段
- [ ] 搜索结果可键盘导航（↑↓ 选择，Enter 跳转）
- [ ] 无搜索结果时显示友好提示

---

### TASK-032：响应式设计验证

**描述**：全面测试站点的移动端、平板、桌面端体验。

**类型**：Testing
**优先级**：P1
**预估工时**：2h
**依赖**：TASK-001, TASK-029, TASK-030

**验收标准**：
- [ ] 桌面端（≥ 1280px）：侧边栏 + 内容区双栏布局正常
- [ ] 平板端（768px-1279px）：侧边栏可折叠，内容区自适应
- [ ] 手机端（< 768px）：侧边栏隐藏，代码块可横向滚动
- [ ] 图片在所有设备不超出屏幕宽度
- [ ] 命令参考表格在窄屏可横向滚动或自适应
- [ ] 导航汉堡菜单功能正常

---

### TASK-033：交叉引用完整性检查

**描述**：验证所有插件页面间的「相关插件」链接有效，无死链。

**类型**：Testing
**优先级**：P1
**预估工时**：1h
**依赖**：TASK-006 ~ TASK-028

**验收标准**：
- [ ] `scripts/validate.sh` 死链检测通过（0 死链）
- [ ] 每个被引用的插件确实存在对应页面
- [ ] 交叉引用图完整（无孤立插件，每个插件至少被 1 个其他插件引用）

---

### TASK-034：CONTRIBUTING.md 维护指南

**描述**：编写文档贡献指南，指导后续维护者新增/更新插件文档。

**类型**：Documentation
**优先级**：P1
**预估工时**：1.5h
**依赖**：TASK-003

**验收标准**：
- [ ] 包含文档模板使用说明
- [ ] 包含新增插件页面的分步指南
- [ ] 包含截图/录屏制作流程（phantom + scry 脚本用法）
- [ ] 包含内容质量检查清单
- [ ] 包含 Git 提交和 PR 规范
- [ ] `docs/.templates/update-checklist.md` 更新检查清单模板完成

---

### TASK-035：最终 QA 和性能审计

**描述**：全站质量审计，包含 Lighthouse 性能评分、内容一致性检查。

**类型**：Testing
**优先级**：P0
**预估工时**：2h
**依赖**：TASK-029 ~ TASK-034

**验收标准**：
- [ ] Lighthouse Performance ≥ 90
- [ ] Lighthouse Accessibility ≥ 90
- [ ] Lighthouse Best Practices ≥ 90
- [ ] 全部 23 个插件页面模板一致性检查通过
- [ ] 全部 23 个插件页面「最后更新日期」已填写
- [ ] 媒体素材清单 `media-inventory.md` 与 `public/` 实际文件一致
- [ ] 无占位符或 TODO 标记残留
- [ ] 首页加载时间 (LCP) < 2 秒
- [ ] 站点在 Chrome、Firefox、Safari 最新版渲染一致

---

## 3. 依赖关系图

```
阶段 1：基础设施
TASK-001 (VitePress初始化)
 ├── TASK-002 (GitHub CI/CD)
 ├── TASK-003 (文档模板) ─────────────────────────────────────┐
 │    └── TASK-034 (维护指南)                                  │
 ├── TASK-004 (媒体工作流)                                     │
 └── TASK-005 (主题定制)                                       │
                                                               │
阶段 2：核心插件 I (7个)  ← 全部依赖 TASK-003                   │
TASK-006 (attune)  TASK-007 (spec-kit)  TASK-008 (imbue)       │
TASK-009 (sanctum) TASK-010 (pensive)   TASK-011 (scribe)      │
TASK-012 (abstract)                                             │
                                                               │
阶段 3：核心插件 II (5个)  ← 全部依赖 TASK-003                  │
TASK-013 (leyline) TASK-014 (hookify)  TASK-015 (egregore)     │
TASK-016 (conjure) TASK-017 (minister)                         │
                                                               │
阶段 4：扩展插件 I (5个)  ← 全部依赖 TASK-003                   │
TASK-018 (archetypes) TASK-019 (cartograph)                     │
TASK-020 (gauntlet)   TASK-021 (tome)   TASK-022 (memory-palace)│
                                                               │
阶段 5：扩展插件 II (6个)  ← 全部依赖 TASK-003                  │
TASK-023 (phantom)  TASK-024 (scry)    TASK-025 (herald)       │
TASK-026 (conserve) TASK-027 (parseltongue) TASK-028 (oracle)  │
                                                               │
阶段 6：导航 + 质量收尾                                         │
TASK-006~028 ──▶ TASK-029 (索引页) ──▶ TASK-030 (场景导航)     │
TASK-006~028 ──▶ TASK-033 (交叉引用检查)                        │
TASK-001 ──▶ TASK-032 (响应式验证)                              │
TASK-006~028 ──▶ TASK-031 (搜索优化)                            │
TASK-029~034 ──▶ TASK-035 (最终QA)                              │
```

---

## 4. 风险管理

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|:---:|------|
| 文档模板需要频繁调整 | 中 | 中 | 阶段 1 用 3 个不同类型的插件充分验证模板后再批量展开 |
| phantom/scry 插件学习曲线 | 低 | 中 | 这两插件本身就是文档内容，学习过程产出案例 |
| 23 个插件信息量过大导致进展缓慢 | 高 | 中 | 分批推进，每完成一批就可见成果，保持动力 |
| VitePress 版本升级导致配置不兼容 | 低 | 低 | 锁定主版本号（^1.x），升级前先在分支测试 |
| GitHub Pages 部署权限配置问题 | 中 | 低 | 阶段 1 优先打通部署链路，后续变更不影响部署流程 |
| 插件内容准确性问题 | 高 | 中 | 每个插件页面编写时实际调用插件验证命令和功能 |
| 媒体素材占用仓库空间过大 | 低 | 中 | GIF 文件限制 < 5MB，超过的转为静态截图 + 文字描述 |

---

## 5. 成功指标

| 指标 | 目标 | 当前状态 |
|------|------|:---:|
| VitePress 站点构建成功 | `npm run docs:build` 无错误 | ⬜ |
| GitHub Pages 部署成功 | URL 可访问 | ⬜ |
| 插件文档覆盖率 | 23/23 (100%) | ⬜ |
| 模板一致性 | 23/23 页面通过验证 | ⬜ |
| 媒体素材覆盖率 | 23/23 页面至少 1 张截图 | ⬜ |
| 死链数量 | 0 | ⬜ |
| Lighthouse Performance | ≥ 90 | ⬜ |
| Lighthouse Accessibility | ≥ 90 | ⬜ |
| CONTRIBUTING.md 完成 | 已创建 | ⬜ |

---

## 6. 时间线

```
Week 1  ████████ 阶段 1: 基础设施 (TASK-001~005)
                 ├─ VitePress 骨架 + CI/CD + 模板 + 媒体工作流

Week 2  ████████ 阶段 2: 核心插件 I (TASK-006~012)
                 ├─ attune, spec-kit, imbue, sanctum, pensive, scribe, abstract

Week 3  ████████ 阶段 3: 核心插件 II (TASK-013~017)
                 ├─ leyline, hookify, egregore, conjure, minister
                 ├─ 阶段 4: 扩展插件 I (TASK-018~022)
                 └─ archetypes, cartograph, gauntlet, tome, memory-palace

Week 4  ████████ 阶段 5: 扩展插件 II (TASK-023~028)
                 ├─ phantom, scry, herald, conserve, parseltongue, oracle
                 ├─ 阶段 6: 导航 + 质量收尾 (TASK-029~035)
                 └─ 索引页 + 场景页 + 搜索 + QA → 上线 🚀
```

---

## 7. 下一步

1. `attune:project-init` — 初始化 VitePress 项目结构，创建 Git 仓库
2. 开始执行阶段 1：基础设施搭建
3. `/attune:execute` — 使用执行引擎系统化推进任务

---

> 📅 创建日期：2026-06-04
> 🔄 最后更新：2026-06-04
> 📌 状态：草稿 — 等待评审
