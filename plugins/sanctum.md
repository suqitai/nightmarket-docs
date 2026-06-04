# sanctum — Git 工作流管理

## 概述

sanctum 是 Night Market 中的 Git 工作流管理插件，简化了 Commit、PR、版本管理和发布流程。它将 Git 最佳实践封装为简单命令，减少操作失误，确保提交历史和发布流程的规范性。

**核心能力：**
- 规范化 Commit：自动生成符合 Conventional Commits 规范的提交信息
- PR 生命周期管理：从创建到合并的全流程自动化
- 版本管理：语义化版本（SemVer）的自动升级和标签管理
- Changelog 生成：自动从提交历史生成变更日志
- 分支策略执行：确保 Git Flow / Trunk-Based 等策略的一致性

**适用场景：**
- 团队需要统一的 Git 提交规范
- 频繁创建和管理 PR 的项目
- 需要自动化版本发布和 Changelog 生成
- 新手开发者不熟悉 Git 高级操作

---

## 安装

```bash
claude plugins install sanctum@claude-night-market

# 验证安装
claude plugins list | grep sanctum
```

---

## 命令参考

| 命令 | 必需参数 | 可选参数 | 说明 | 使用示例 |
|------|----------|----------|------|----------|
| `/sanctum:commit` | — | `--type`, `--scope`, `--message` | 生成规范化提交信息并提交 | `/sanctum:commit --type feat --scope auth --message "添加邮箱登录"` |
| `/sanctum:pr` | — | `--base`, `--draft`, `--reviewers` | 创建和管理 Pull Request | `/sanctum:pr --base main --reviewers alice,bob` |
| `/sanctum:release` | — | `--level`, `--notes`, `--dry-run` | 语义化版本发布 | `/sanctum:release --level minor` |
| `/sanctum:changelog` | — | `--from`, `--to`, `--format` | 生成变更日志 | `/sanctum:changelog --from v1.0.0 --to HEAD` |
| `/sanctum:branch` | — | `--name`, `--type`, `--from` | 按规范创建分支 | `/sanctum:branch --type feature --name "user-auth"` |
| `/sanctum:history` | — | `--since`, `--author` | 查看格式化的提交历史 | `/sanctum:history --since "2 weeks ago"` |

---

## 使用场景

### 场景 1：自动化规范提交

**问题：** 团队提交信息格式混乱，`fix bug`、`update`、`WIP` 随处可见，Changelog 无法自动生成。

**解决方案：** 使用 sanctum 的 commit 命令，自动格式化为 Conventional Commits 规范。

**命令示例：**
```bash
/sanctum:commit --type feat --scope payment --message "集成 Stripe 支付网关"
```

**预期结果：** 自动生成 `feat(payment): 集成 Stripe 支付网关` 格式的提交信息，并在 body 中附加相关文件变更摘要。

---

### 场景 2：一键创建规范化 PR

**问题：** 每次提 PR 都要手动写描述、关联 Issue、添加 Reviewer，容易遗漏步骤。

**解决方案：** 使用 PR 命令自动完成所有配置。

**命令示例：**
```bash
/sanctum:pr --base main --reviewers alice,bob --label "enhancement,payment"
```

**预期结果：** 自动生成包含变更摘要、关联 Issue、Checklist 的 PR 描述，分配 Reviewer 和标签。

---

## 实战案例

### 案例 1：一个完整的功能分支工作流

**背景：** 你要开发用户资料编辑功能，需要从创建分支到合并 PR 的完整流程。

**操作步骤：**

1. **创建功能分支**
   ```bash
   /sanctum:branch --type feature --name "profile-edit"
   ```

2. **开发并规范化提交**
   ```bash
   /sanctum:commit --type feat --scope profile --message "添加头像上传和昵称编辑"
   ```

3. **创建 PR**
   ```bash
   /sanctum:pr --base main --reviewers team-lead
   ```

4. **PR 合并后自动清理分支**
   *sanctum 检测到 PR 合并后提示删除远程和本地分支*

**结果展示：**

![sanctum 终端预览](/images/sanctum/terminal-preview.png)

*（占位截图 — 用 phantom 替换为实际操作截图）*

---

### 案例 2：语义化版本发布

**背景：** 项目需要发布 v1.2.0 版本，包含新功能和一些 Bug 修复。

**操作步骤：**

1. **预览发布**
   ```bash
   /sanctum:release --level minor --dry-run
   ```
   *预览会显示：版本号变化 v1.1.0 → v1.2.0，包含的提交列表，生成的 Changelog 内容*

2. **正式发布**
   ```bash
   /sanctum:release --level minor --notes "新增支付模块，修复登录超时问题"
   ```

3. **验证结果**
   *自动创建 git tag v1.2.0，生成 CHANGELOG.md 更新，推送 tag 到远程*

**结果展示：**

![sanctum 终端预览](/images/sanctum/terminal-preview.png)

*（占位截图 — 用 phantom 替换为实际操作截图）*

---

## 常见问题

<details class="faq-item">
<summary>Q: sanctum 强制使用 Conventional Commits 吗？</summary>
<div class="answer">

**A:** 不强制，但强烈推荐。如果不指定 `--type`，sanctum 会根据变更内容智能推荐类型：

- 新增文件/函数 → `feat`
- 修改已有逻辑 → `fix`
- 仅文档变更 → `docs`
- 重构（无行为变化）→ `refactor`

你也可以使用 `--type custom` 自由输入。
</div>
</details>

<details class="faq-item">
<summary>Q: 如何处理合并冲突？</summary>
<div class="answer">

**A:** sanctum 不会自动解决冲突，但会辅助你处理：

1. 检测到冲突时，sanctum 列出冲突文件和冲突内容
2. 解决冲突后运行 `/sanctum:commit --type merge` 完成合并提交
3. PR 自动更新状态

sanctum 确保你在解决冲突后不会忘记添加所有文件。
</div>
</details>

<details class="faq-item">
<summary>Q: 支持 Git Flow 还是 Trunk-Based？</summary>
<div class="answer">

**A:** 两者都支持。在项目初始化时通过 `/sanctum:branch --type` 的行为可以适配：

- **Git Flow**：使用 `feature/`、`release/`、`hotfix/` 前缀创建分支
- **Trunk-Based**：分支前缀为 `feat/`、`fix/`，sanctum 会提醒短生命周期分支及时合并

默认行为可以通过 `.sanctum/config.yml` 配置。
</div>
</details>

---

## 相关插件

### 配合使用

| 插件 | 协作方式 |
|------|----------|
| [attune](./attune.md) | attune 执行阶段通过 sanctum 管理代码提交和 PR |
| [imbue](./imbue.md) | imbue 质量门禁通过后，sanctum 才允许提交和合并 |
| [minister](./minister.md) | minister 管理 GitHub Issue，sanctum 的 PR 自动关联相关 Issue |

---

> 📝 最后更新：2026-06-04
