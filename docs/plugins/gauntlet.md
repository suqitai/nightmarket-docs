# gauntlet — 代码库学习

## 概述

gauntlet 是 Night Market 中的代码库学习工具，通过构建知识图谱和间隔重复挑战帮你快速掌握一个新代码库。它不是简单的文件索引，而是建立模块、类、函数之间的语义关系网络。

**核心能力：**
- 知识图谱：自动构建代码实体（类/函数/模块）的关系网络
- 间隔重复：基于遗忘曲线的复习挑战，巩固学习成果
- 概念提取：从代码中提取核心业务概念和领域模型
- 学习路径：根据依赖关系推荐最佳阅读顺序
- 进度追踪：可视化学习覆盖率和掌握程度

**适用场景：**
- 入职新人快速上手团队代码库
- 接手一个遗留系统需要理解核心逻辑
- 准备系统面试前的代码复习
- 大型重构前全面理解业务逻辑

---

## 安装

```bash
claude plugins install gauntlet@claude-night-market
claude plugins list | grep gauntlet
```

---

## 命令参考

| 命令 | 必需参数 | 可选参数 | 说明 | 使用示例 |
|------|----------|----------|------|----------|
| `/gauntlet:learn` | `--path` | `--focus`, `--depth` | 启动交互式学习会话 | `/gauntlet:learn --path src/ --focus core` |
| `/gauntlet:graph` | `--path` | `--output` | 生成知识图谱 | `/gauntlet:graph --path src/ --output knowledge-graph.md` |
| `/gauntlet:challenge` | `--path` | `--count` | 间隔重复挑战 | `/gauntlet:challenge --path src/ --count 10` |
| `/gauntlet:concepts` | `--path` | `--format` | 提取核心业务概念 | `/gauntlet:concepts --path src/domain/` |
| `/gauntlet:progress` | `--path` | — | 查看学习进度 | `/gauntlet:progress --path src/` |

---

## 使用场景

### 场景 1：新人 30 分钟理解核心模块

**问题：** 第一天入职，面对 500 个文件的代码库，不知道从哪读起。

**解决方案：** 用 learn 启动引导式学习，gauntlet 按依赖关系推荐阅读路径。

**命令示例：**
```bash
/gauntlet:learn --path src/ --focus core --depth 3
```

**预期结果：** gauntlet 从入口文件开始，按依赖关系引导阅读——先读接口定义、再读核心实现、最后读辅助工具。每读完一个模块给出关键要点摘要。

---

### 场景 2：间隔重复巩固知识

**问题：** 上周学了一个模块，今天已经忘了大半。

**解决方案：** 用 challenge 进行间隔重复测验。

**命令示例：**
```bash
/gauntlet:challenge --path src/ --count 15
```

**预期结果：** gauntlet 根据遗忘曲线出题：上次正确率高的问题间隔更长，错过的题更频繁出现。

---

## 实战案例

### 案例 1：1 周掌握遗留系统

**背景：** 接手一个 3 年历史的 Django 项目，没有文档，前任已离职。

**操作步骤：**

1. **生成知识图谱**
   ```bash
   /gauntlet:graph --path . --output codebase-map.md
   ```

2. **提取核心概念**
   ```bash
   /gauntlet:concepts --path src/domain/ --format markdown
   ```
   *输出：Order、Invoice、Claim、Policy 等核心领域概念及关系*

3. **按推荐路径学习**，每天 1 小时 guided learning

4. **每日 challenge** 巩固前一天的学习内容

**结果展示：**

<div class="nm-tip">
📸 <strong>截图待制作</strong>：展示 gauntlet 知识图谱。运行 <code>bash scripts/screenshot.sh gauntlet</code> 生成。
</div>

---

## 常见问题

<details class="faq-item">
<summary>Q: gauntlet 生成的知识图谱能导出吗？</summary>
<div class="answer">

**A:** 可以导出为多种格式：

```bash
--format mermaid   # Markdown 可嵌入
--format json      # 供程序处理
--format dot       # Graphviz 可视化
```

导出的知识图谱可作为团队文档，后续新人可以直接参考。
</div>
</details>

<details class="faq-item">
<summary>Q: 对大型代码库（1000+ 文件）效果如何？</summary>
<div class="answer">

**A:** gauntlet 对大代码库做了优化：

- 默认 `--depth 3` 避免图谱爆炸
- 自动识别「核心模块」（被引用最多的前 20%）优先展示
- 支持 `--exclude "vendor,third_party,generated"` 排除无关代码

对于超大型代码库，建议分模块学习：先学 `--focus domain`，再学 `--focus infrastructure`。
</div>
</details>

---

## 相关插件

| 插件 | 协作方式 |
|------|----------|
| [tome](./tome.md) | tome 做代码考古研究历史背景，gauntlet 学当前代码结构 |
| [cartograph](./cartograph.md) | cartograph 可视化结构，gauntlet 建立语义理解 |
| [memory-palace](./memory-palace.md) | gauntlet 学完后用 memory-palace 长期记忆管理 |

---

> 📝 最后更新：2026-06-04
