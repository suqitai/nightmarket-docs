# tome — 多源研究

## 概述

tome 是 Night Market 中的多源研究工具，能从代码考古、Hacker News、Reddit、arXiv、技术博客等多渠道搜集和分析信息。当你需要做技术调研、了解某个决策的历史背景、或寻找最佳实践时，tome 提供跨源的综合研究能力。

**核心能力：**
- 代码考古：从 Git 历史挖掘代码变更的原因和上下文
- 社区调研：搜索 HN/Reddit 上的技术讨论和实战经验
- 论文检索：arXiv 上相关学术研究
- TRIZ 分析：用创新方法论分析技术矛盾
- 综合报告：跨源信息汇总为结构化研究报告

**适用场景：**
- 技术选型前的全面调研
- 理解项目代码中的「为什么这样写」
- 寻找某个技术问题的最佳实践
- 跟踪某个技术趋势的发展

---

## 安装

```bash
claude plugins install tome@claude-night-market
claude plugins list | grep tome
```

---

## 命令参考

| 命令 | 必需参数 | 可选参数 | 说明 | 使用示例 |
|------|----------|----------|------|----------|
| `/tome:research` | `--topic` | `--sources`, `--depth` | 多源主题研究 | `/tome:research --topic "PostgreSQL vs MySQL 2024"` |
| `/tome:archaeology` | `--file` | `--since`, `--blame` | 代码考古分析 | `/tome:archaeology --file src/payment.py --since "1 year ago"` |
| `/tome:community` | `--question` | `--sources` | 搜索社区讨论 | `/tome:community --question "Django async 生产经验" --sources hn,reddit` |
| `/tome:paper` | `--query` | `--category` | 搜索学术论文 | `/tome:paper --query "eventual consistency tradeoffs"` |
| `/tome:trize` | `--contradiction` | — | TRIZ 矛盾分析 | `/tome:trize --contradiction "性能 vs 可维护性"` |

---

## 使用场景

### 场景 1：技术选型调研

**问题：** 团队在选 Redis vs Kafka 做消息队列，需要全面对比。

**解决方案：** 用 research 跨源调研，综合学术论文、社区经验、代码案例。

**命令示例：**
```bash
/tome:research --topic "Redis Pub/Sub vs Kafka for message queue" --depth comprehensive
```

**预期结果：** 汇总报告包含：学术性能对比、HN 实战经验帖、Reddit 踩坑记录、各方案的延迟/吞吐/可靠性矩阵。

---

### 场景 2：理解一段「奇怪」代码的历史

**问题：** 代码中有一段看起来很怪异的 workaround，注释只有一句「fix edge case」。

**解决方案：** 用 archaeology 追踪这段代码的 Git 历史和相关 Issue。

**命令示例：**
```bash
/tome:archaeology --file src/api/throttle.py --since "2 years ago" --blame
```

**预期结果：** 追溯到 2023 年的一个 Issue 和 PR——原来是某个第三方 API 偶尔返回畸形数据，这个 workaround 是唯一可靠的修复方式。

---

## 实战案例

### 案例 1：为重构做背景调研

**背景：** 准备将项目的认证系统从 Session 改为 JWT，需要全面了解 JWT 的坑。

**操作步骤：**

1. **社区调研**
   ```bash
   /tome:community --question "JWT authentication pitfalls production" --sources hn,reddit
   ```

2. **代码考古**
   ```bash
   /tome:archaeology --file src/auth/ --since "all" --blame
   ```
   *发现当前 Session 方案也是从 JWT 迁回来的，原因是 token 撤销困难*

3. **综合报告** — tome 汇总所有发现，建议保留 Session 方案但优化 Session 存储

**结果展示：**

![tome 终端预览](/images/tome/terminal-preview.png)

*（占位截图 — 用 phantom 替换为实际操作截图）*

---

## 常见问题

<details class="faq-item">
<summary>Q: research 的信息来源可靠吗？</summary>
<div class="answer">

**A:** tome 按来源标注可靠性：

- 🟢 **高**：学术论文（arXiv）、官方文档
- 🟡 **中**：HN/Reddit 高票讨论、知名技术博客
- 🟠 **需验证**：个人博客、低票讨论

研究报告中每个结论标注来源和可靠性等级，避免把社区观点当真理。
</div>
</details>

<details class="faq-item">
<summary>Q: archaeology 能分析非 git 项目吗？</summary>
<div class="answer">

**A:** archaeology 依赖 Git 历史。如果你的项目没有 Git 记录，可以使用：

```bash
/tome:research --topic "[你的问题]" --sources web
```

tome 会搜索网络上的公开资料、文档、Issue 来替代 Git 考古。
</div>
</details>

---

## 相关插件

| 插件 | 协作方式 |
|------|----------|
| [gauntlet](./gauntlet.md) | gauntlet 学代码现状，tome 研究代码历史 |
| [cartograph](./cartograph.md) | tome 考古发现 + cartograph 可视化时序 |

---

> 📝 最后更新：2026-06-04
