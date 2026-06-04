# memory-palace — 空间记忆宫殿

## 概述

memory-palace 是 Night Market 中的知识管理插件，受「记忆宫殿」记忆术启发，将你与 Claude Code 的交互中积累的知识组织为结构化的空间记忆体系。每个项目、每个主题都可以是记忆宫殿中的一个「房间」。

**核心能力：**
- 空间记忆模型：项目/主题/知识点三层树状结构
- 自动归档：从对话中自动提取关键决策和知识点
- 关联网络：知识点之间建立双向链接（类似 Roam/Obsidian）
- 记忆检索：关键词、语义相似、时间线多模式检索
- 遗忘提醒：基于遗忘曲线的复习提醒

**适用场景：**
- 长期项目管理，需要记住历史决策
- 跨项目复用知识和经验
- 多个技术领域的学习和积累
- 团队知识沉淀和传承

---

## 安装

```bash
claude plugins install memory-palace@claude-night-market
claude plugins list | grep memory-palace
```

---

## 命令参考

| 命令 | 必需参数 | 可选参数 | 说明 | 使用示例 |
|------|----------|----------|------|----------|
| `/memory-palace:store` | `--content` | `--room`, `--tags` | 存储一条知识 | `/memory-palace:store --content "prod DB 是 PG 15" --room project-x` |
| `/memory-palace:recall` | `--query` | `--room`, `--type` | 检索知识 | `/memory-palace:recall --query "数据库配置" --room project-x` |
| `/memory-palace:link` | `--from`, `--to` | — | 建立知识点关联 | `/memory-palace:link --from "部署流程" --to "环境变量"` |
| `/memory-palace:map` | — | `--room` | 查看记忆宫殿结构 | `/memory-palace:map --room project-x` |
| `/memory-palace:review` | — | `--due` | 即将遗忘的复习提醒 | `/memory-palace:review --due today` |

---

## 使用场景

### 场景 1：项目上下文持续积累

**问题：** 一个项目跨度 6 个月，很多早期的技术决策到后期已记不清原因。

**解决方案：** 每次做重要决策后用 store 记录，后续 recall 即可回溯。

**命令示例：**
```bash
/memory-palace:store --content "选择 Redis 而非 Memcached 因为需要持久化和 Pub/Sub" --room project-x --tags "database,decision"

# 3 个月后
/memory-palace:recall --query "为什么用 Redis" --room project-x
```

**预期结果：** 3 个月前存入的决策背景完整呈现，避免「我们为什么选了 Redis 来着？」

---

### 场景 2：跨项目知识复用

**问题：** 在项目 A 中学到的部署经验，项目 B 启动时再来一遍。

**解决方案：** 在项目 B 中跨房间检索项目 A 的知识。

**命令示例：**
```bash
/memory-palace:recall --query "CI/CD GitHub Actions 部署 VitePress" --type decision,lesson
```

**预期结果：** 检索到项目 A 的部署配置决策和踩坑记录，项目 B 直接复用。

---

## 实战案例

### 案例 1：长期项目的知识树

**背景：** 一个持续 1 年的 SaaS 开发项目，积累了无数决策和经验。

**操作步骤：**

1. **初始化项目记忆空间**
   ```bash
   /memory-palace:store --content "项目启动：使用 Django + React 技术栈" --room saas-project --tags "architecture,decision"
   ```

2. **持续记录关键信息** — 每次重要变更都 store 一条

3. **定期 review** — memory-palace 自动提醒即将遗忘的知识

4. **查看记忆地图**
   ```bash
   /memory-palace:map --room saas-project
   ```

**结果展示：**

![memory-palace 终端预览](/images/memory-palace/terminal-preview.png)

*（占位截图 — 用 phantom 替换为实际操作截图）*

---

## 常见问题

<details class="faq-item">
<summary>Q: memory-palace 和 Claude Code 自带 memory 有什么不同？</summary>
<div class="answer">

**A:** Claude Code 自带 memory 是**会话级**的被动记忆（系统自动记录）。memory-palace 是**项目级**的主动知识管理：

- 自带 memory：自动记录，但跨项目/跨会话不可控
- memory-palace：手动记录（可控），支持跨项目检索、结构化组织、遗忘提醒

两者互补：自带 memory 做日常记录，memory-palace 做重要知识的结构化管理。
</div>
</details>

<details class="faq-item">
<summary>Q: 存储的知识会丢失吗？</summary>
<div class="answer">

**A:** memory-palace 的知识存储在项目目录的 `.memory-palace/` 中（纯 Markdown 文件），可以：

- 纳入 Git 版本控制（团队共享）
- 备份到其他地方
- 手动编辑和迁移

不依赖外部服务，数据完全由你掌控。
</div>
</details>

---

## 相关插件

| 插件 | 协作方式 |
|------|----------|
| [gauntlet](./gauntlet.md) | gauntlet 学完代码库后，关键知识存入 memory-palace |
| [tome](./tome.md) | tome 研究成果归档到 memory-palace |

---

> 📝 最后更新：2026-06-04
