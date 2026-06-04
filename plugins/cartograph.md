# cartograph — 代码可视化

## 概述

cartograph 是 Night Market 中的代码可视化工具，能将抽象代码关系转化为直观的图表。支持生成架构图、数据流图、依赖关系图、调用链图，帮助你快速理解复杂代码库的结构。

**核心能力：**
- 架构图生成：模块和组件关系的鸟瞰图
- 数据流图：数据的输入、转换和输出路径
- 依赖关系图：文件和模块之间的引用网络
- 调用链图：函数调用关系的深度追踪
- Mermaid/Graphviz 输出：兼容主流图表工具

**适用场景：**
- 接手陌生代码库，快速理解整体结构
- 重构前梳理现有依赖关系
- 技术文档需要配架构图
- 新人培训时展示系统结构

---

## 安装

```bash
claude plugins install cartograph@claude-night-market
claude plugins list | grep cartograph
```

---

## 命令参考

| 命令 | 必需参数 | 可选参数 | 说明 | 使用示例 |
|------|----------|----------|------|----------|
| `/cartograph:map` | `--path` | `--depth`, `--format` | 生成代码结构图 | `/cartograph:map --path src/ --format mermaid` |
| `/cartograph:deps` | `--path` | `--focus`, `--max-depth` | 生成依赖关系图 | `/cartograph:deps --path src/ --focus UserService` |
| `/cartograph:flow` | `--path` | `--entry`, `--format` | 生成数据流图 | `/cartograph:flow --path src/api/ --entry POST /orders` |
| `/cartograph:callchain` | `--function` | `--depth`, `--direction` | 生成函数调用链 | `/cartograph:callchain --function "process_payment" --depth 5` |
| `/cartograph:diff` | `--base`, `--head` | `--output` | 对比两个版本的架构差异 | `/cartograph:diff --base main --head feature/new-module` |

---

## 使用场景

### 场景 1：上手新代码库

**问题：** 刚加入团队，面对一个 200+ 文件的代码库，不知道从哪里开始看。

**解决方案：** 先用 map 生成鸟瞰图，用 deps 找到核心模块。

**命令示例：**
```bash
/cartograph:map --path src/ --depth 2 --format mermaid
/cartograph:deps --path src/ --focus core --max-depth 3
```

**预期结果：** 生成模块鸟瞰图和核心模块的依赖网络，5 分钟内理解系统骨架。

---

### 场景 2：重构前风险评估

**问题：** 想重构 UserService，但担心牵一发动全身。

**解决方案：** 用 callchain 追踪 UserService 的上下游依赖。

**命令示例：**
```bash
/cartograph:callchain --function "UserService.authenticate" --depth 5 --direction both
```

**预期结果：** 展示 authenticate 的完整调用链——上游 3 个入口、下游 8 个依赖，可知哪些模块会受重构影响。

---

## 实战案例

### 案例 1：生成 API 数据流文档

**背景：** 需要为支付接口编写技术文档，需要一个清晰的数据流图。

**操作步骤：**

1. **生成数据流图**
   ```bash
   /cartograph:flow --path src/api/payment/ --entry "POST /api/v1/checkout" --format mermaid
   ```

2. **导出** — 将 Mermaid 代码嵌入 Markdown 文档

3. **文档预览** — 用户下单 → 库存检查 → 价格计算 → 支付网关 → 订单确认，全流程可视化

**结果展示：**

![cartograph 终端预览](/images/cartograph/terminal-preview.png)

*（占位截图 — 用 phantom 替换为实际操作截图）*

---

## 常见问题

<details class="faq-item">
<summary>Q: 生成的图太复杂，全是线怎么办？</summary>
<div class="answer">

**A:** 几种精简方法：

```bash
--depth 2        # 控制层级深度
--focus ModuleA  # 只看某个模块
--max-deps 10    # 限制每条连线的数量
--exclude "test,util"  # 排除测试和工具类
```

先粗后细：先用 `--depth 1` 看顶层，再聚焦具体模块深入。
</div>
</details>

<details class="faq-item">
<summary>Q: diff 功能能看到 PR 级别的架构变化吗？</summary>
<div class="answer">

**A:** 可以。diff 对比两个 git ref 之间的架构变化：

```bash
/cartograph:diff --base main --head feature/refactor --output diff-report.md
```

输出内容包括：新增/删除/修改的模块、依赖关系变化、循环依赖的新增和消除。
</div>
</details>

---

## 相关插件

| 插件 | 协作方式 |
|------|----------|
| [archetypes](./archetypes.md) | archetypes 选范式 → cartograph 可视化架构 |
| [tome](./tome.md) | tome 做代码考古研究，cartograph 可视化考古发现 |

---

> 📝 最后更新：2026-06-04
