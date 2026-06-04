# scribe — 文档审查

## 概述

scribe 是 Night Market 中的文档质量审查插件，专注于检测技术文档中的问题：AI 生成的废话（空话、套话、重复）、过时内容、格式不一致、阅读体验问题等。让技术文档保持「人类可读」的高质量标准。

**核心能力：**
- AI 废话检测：识别空洞表述、无信息量的填充句、过度修饰
- 过时内容标记：对比代码库检测文档与实现不一致的地方
- 可读性评分：基于中文阅读难度评估文档可读性
- 格式一致性检查：标题层级、代码块语言标注、链接格式
- 术语规范性：检测术语使用是否前后一致

**适用场景：**
- README、API 文档等面向用户的文档审查
- 检测 AI 辅助生成的文档中的「废话」
- 确保文档与代码保持同步
- 多作者协作的文档一致性检查

---

## 安装

```bash
claude plugins install scribe@claude-night-market
claude plugins list | grep scribe
```

---

## 命令参考

| 命令 | 必需参数 | 可选参数 | 说明 | 使用示例 |
|------|----------|----------|------|----------|
| `/scribe:review` | — | `--file`, `--lang` | 文档全面审查 | `/scribe:review --file README.md --lang zh` |
| `/scribe:fluff` | — | `--file`, `--threshold` | AI 废话检测 | `/scribe:fluff --file docs/api.md` |
| `/scribe:sync` | `--code`, `--docs` | — | 代码与文档同步检查 | `/scribe:sync --code src/ --docs docs/` |
| `/scribe:readability` | — | `--file`, `--target` | 可读性评分 | `/scribe:readability --file docs/ --target grade7` |
| `/scribe:terminology` | — | `--file`, `--glossary` | 术语一致性检查 | `/scribe:terminology --file docs/ --glossary .scribe/terms.yml` |

---

## 使用场景

### 场景 1：清理 AI 生成的文档

**问题：** 用 AI 生成了 API 文档初稿，但充满「强大的」「无缝的」「直观的」等空洞形容词，需要去水。

**解决方案：** 使用 fluff 检测，自动标记废话密度高的段落。

**命令示例：**
```bash
/scribe:fluff --file docs/api-reference.md --threshold medium
```

**预期结果：** 每个废话段落被高亮标记，附带具体问题（空泛形容词、无信息量承诺、同义重复），给出简洁改写建议。

---

### 场景 2：API 文档与代码同步检查

**问题：** 代码更新了参数名，但文档还用的旧参数名，用户按文档调用会报错。

**解决方案：** 使用 sync 对比代码和文档，自动发现不一致。

**命令示例：**
```bash
/scribe:sync --code src/api/ --docs docs/api/
```

**预期结果：** 列出所有文档与代码不一致的条目（参数名、返回值类型、错误码、示例输出等）。

---

## 实战案例

### 案例 1：AI 废话检测 — 优化 README

**背景：** 项目 README 用 AI 写了一稿，感觉「读起来很空」。

**操作步骤：**

1. **运行废话检测**
   ```bash
   /scribe:fluff --file README.md
   ```

2. **查看到标记的问题**，例如：
   - 「利用先进的技术」→ 没说具体是什么技术
   - 「无缝集成」→ 是否真的无缝？有无配置步骤？
   - 「高性能」→ 无具体指标

3. **按建议逐条修改**，每个形容词替换为具体数字或操作步骤

**结果展示：**

<div class="nm-tip">
📸 <strong>截图待制作</strong>：展示 scribe fluff 的废话检测报告。运行 <code>bash scripts/screenshot.sh scribe</code> 生成。
</div>

---

### 案例 2：代码与文档同步

**背景：** 重构了 API 的参数命名，需要检查哪些文档需要更新。

**操作步骤：**

1. **运行同步检查**
   ```bash
   /scribe:sync --code src/api/v2/ --docs docs/api/
   ```

2. **获得差异报告**：
   - `docs/api/endpoints.md`：`user_id` 参数已重命名为 `userId`，文档未更新
   - `docs/api/examples.md`：第 3 个示例的返回格式与实际不匹配

3. **修正文档并重新检查**

**结果展示：**

<div class="nm-tip">
📸 <strong>截图待制作</strong>：展示 scribe sync 的差异报告。运行 <code>bash scripts/screenshot.sh scribe</code> 生成。
</div>

---

## 常见问题

<details class="faq-item">
<summary>Q: scribe 会不会把正常的说明文字也当废话？</summary>
<div class="answer">

**A:** fluff 检测有三档敏感度：

```bash
--threshold low     # 只标记明显的废话（如"世界级""行业领先"）
--threshold medium  # 默认，标记空洞形容词和重复表述
--threshold high    # 激进模式，可能误报，适合严格审查
```

建议从 medium 开始，人工复核后再调高。减少「误杀」：如果某段被误标记，可在段落后加 `<!-- scribe:no-fluff -->` 排除。
</div>
</details>

<details class="faq-item">
<summary>Q: sync 检查能对比哪些维度？</summary>
<div class="answer">

**A:** 当前支持：
- 函数/方法签名（参数名、类型、默认值）
- 返回值类型和结构
- 错误码和异常类型
- 代码示例的正确性（能否运行）
- 配置项和常量值

不支持（但后续可能支持）：描述性文本的语义一致性（如文档说「快速」但代码有 3 秒延迟）。
</div>
</details>

<details class="faq-item">
<summary>Q: 团队有自己的术语表，怎么配置？</summary>
<div class="answer">

**A:** 创建 `.scribe/terms.yml`：

```yaml
terms:
  - preferred: "用户"
    avoid: ["User", "使用者", "账户持有者"]
  - preferred: "API 端点"
    avoid: ["API Endpoint", "接口地址", "URL 路径"]
```

然后运行：
```bash
/scribe:terminology --file docs/ --glossary .scribe/terms.yml
```

scribe 会报告使用「User」而非「用户」的位置和行号。
</div>
</details>

---

## 相关插件

### 配合使用

| 插件 | 协作方式 |
|------|----------|
| [pensive](./pensive.md) | pensive 审查代码质量 + scribe 审查文档质量 → 完整项目质量保障 |
| [abstract](./abstract.md) | abstract 的 skills-eval 可评估 scribe 自身生成内容的质量 |

---

> 📝 最后更新：2026-06-04
