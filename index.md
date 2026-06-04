---
layout: home

hero:
  name: Night Market
  text: 插件使用手册
  tagline: Claude Code 插件生态系统的完整中文指南
  actions:
    - theme: brand
      text: 浏览插件
      link: /nightmarket-docs/plugin-index
    - theme: alt
      text: 场景导航
      link: /nightmarket-docs/scenario-nav
  image:
    src: /logo.svg
    alt: Night Market

features:
  - icon: 📦
    title: 23 个插件全覆盖
    details: 从开发流程到代码审查，从安全防护到 Agent 编排，Night Market 生态的全部插件一网打尽。
  - icon: 📖
    title: 场景化导航
    details: 不知道该用哪个插件？按使用场景查找推荐组合，每个场景都有完整的工作流指引。
  - icon: 🎯
    title: 实战案例驱动
    details: 每个插件都配有真实使用案例，附带截图和终端录屏，跟着做就能上手。
  - icon: 🔍
    title: 智能搜索
    details: 支持中英文关键词搜索，快速定位到需要的命令、场景或解决方案。
  - icon: 🔄
    title: 持续更新
    details: 模板驱动的文档体系，插件更新时文档同步维护，确保信息始终准确。
  - icon: 🌐
    title: 全中文编写
    details: 专为中文用户优化，技术术语保留原名的同时，确保每个概念都解释清楚。
---

## 快速开始

```bash
# 安装插件
claude plugins install <plugin-name>@claude-night-market

# 查看已安装插件
claude plugins list

# 在 Claude Code 中使用 (示例)
/attune:brainstorm --domain "web app"
```

## 插件总览

<div class="plugin-grid">
  <a class="plugin-card" href="/nightmarket-docs/plugins/attune">
    <div class="name">attune</div>
    <div class="desc">全周期项目开发 — 从头脑风暴到执行打磨</div>
    <span class="tag">开发流程</span>
  </a>
  <a class="plugin-card" href="/nightmarket-docs/plugins/pensive">
    <div class="name">pensive</div>
    <div class="desc">多维度代码审查 — 架构/Bug/安全/NASA 10 条</div>
    <span class="tag">代码质量</span>
  </a>
  <a class="plugin-card" href="/nightmarket-docs/plugins/leyline">
    <div class="name">leyline</div>
    <div class="desc">基础安全设施 — 认证、配额、注入检测</div>
    <span class="tag">安全</span>
  </a>
  <a class="plugin-card" href="/nightmarket-docs/plugins/egregore">
    <div class="name">egregore</div>
    <div class="desc">自主 Agent 编排 — 并行 worktree、崩溃恢复</div>
    <span class="tag">Agent</span>
  </a>
</div>

<style>
.plugin-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1rem;
  margin: 1.5rem 0;
}
.plugin-card {
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  padding: 1.25rem;
  transition: border-color 0.25s, box-shadow 0.25s;
  text-decoration: none !important;
  color: inherit;
}
.plugin-card:hover {
  border-color: var(--vp-c-brand-1);
  box-shadow: 0 2px 12px rgba(91, 76, 196, 0.15);
}
.plugin-card .name {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
}
.plugin-card .desc {
  font-size: 0.875rem;
  color: var(--vp-c-text-2);
  line-height: 1.5;
}
.plugin-card .tag {
  display: inline-block;
  font-size: 0.75rem;
  padding: 2px 8px;
  border-radius: 4px;
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
  margin-top: 0.5rem;
}
</style>
