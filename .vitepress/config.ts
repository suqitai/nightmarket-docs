import { defineConfig } from 'vitepress'

// 插件分类侧边栏
const pluginSidebar = [
  {
    text: '🔧 开发流程',
    collapsed: false,
    items: [
      { text: 'attune — 全周期项目开发', link: '/plugins/attune' },
      { text: 'spec-kit — 规格驱动开发', link: '/plugins/spec-kit' },
      { text: 'imbue — TDD 质量门禁', link: '/plugins/imbue' },
      { text: 'sanctum — Git 工作流', link: '/plugins/sanctum' },
    ],
  },
  {
    text: '📝 代码质量',
    collapsed: false,
    items: [
      { text: 'pensive — 多维度代码审查', link: '/plugins/pensive' },
      { text: 'scribe — 文档审查', link: '/plugins/scribe' },
      { text: 'abstract — Skill/Hook 开发', link: '/plugins/abstract' },
    ],
  },
  {
    text: '🏗️ 架构设计',
    collapsed: true,
    items: [
      { text: 'archetypes — 架构范式选择', link: '/plugins/archetypes' },
      { text: 'cartograph — 代码可视化', link: '/plugins/cartograph' },
    ],
  },
  {
    text: '🔒 安全基础设施',
    collapsed: true,
    items: [
      { text: 'leyline — 基础安全设施', link: '/plugins/leyline' },
      { text: 'hookify — 行为规则引擎', link: '/plugins/hookify' },
    ],
  },
  {
    text: '🤖 Agent 编排',
    collapsed: true,
    items: [
      { text: 'egregore — 自主 Agent 编排', link: '/plugins/egregore' },
      { text: 'conjure — 外部 LLM 委托', link: '/plugins/conjure' },
      { text: 'minister — Issue 管理', link: '/plugins/minister' },
    ],
  },
  {
    text: '📚 知识管理',
    collapsed: true,
    items: [
      { text: 'gauntlet — 代码库学习', link: '/plugins/gauntlet' },
      { text: 'tome — 多源研究', link: '/plugins/tome' },
      { text: 'memory-palace — 记忆宫殿', link: '/plugins/memory-palace' },
    ],
  },
  {
    text: '🎬 媒体制作',
    collapsed: true,
    items: [
      { text: 'phantom — 桌面自动化', link: '/plugins/phantom' },
      { text: 'scry — 媒体生成', link: '/plugins/scry' },
    ],
  },
  {
    text: '📢 通知集成',
    collapsed: true,
    items: [
      { text: 'herald — 通知系统', link: '/plugins/herald' },
    ],
  },
  {
    text: '⚡ 性能优化',
    collapsed: true,
    items: [
      { text: 'conserve — 上下文优化', link: '/plugins/conserve' },
      { text: 'parseltongue — Python 开发套件', link: '/plugins/parseltongue' },
      { text: 'oracle — 本地 ML 推理', link: '/plugins/oracle' },
    ],
  },
]

export default defineConfig({
  title: 'Night Market 插件手册',
  description: 'Claude Code Night Market 插件中文使用说明书',
  lang: 'zh-CN',

  // 增量构建期间忽略死链，最终 QA 阶段移除（TASK-035）
  ignoreDeadLinks: true,

  head: [
    ['link', { rel: 'icon', href: '/favicon.ico' }],
  ],

  themeConfig: {
    // 顶部导航
    nav: [
      { text: '首页', link: '/' },
      { text: '插件索引', link: '/plugin-index' },
      { text: '场景导航', link: '/scenario-nav' },
      { text: '关于', link: '/about' },
    ],

    // 侧边栏
    sidebar: {
      '/plugins/': pluginSidebar,
    },

    // 搜索
    search: {
      provider: 'local',
      options: {
        locales: {
          'zh-CN': {
            translations: {
              button: {
                buttonText: '搜索',
                buttonAriaLabel: '搜索',
              },
              modal: {
                noResultsText: '无法找到相关结果',
                resetButtonTitle: '清除查询',
                footer: {
                  selectText: '选择',
                  navigateText: '切换',
                  closeText: '关闭',
                },
              },
            },
          },
        },
      },
    },

    // 社交链接
    socialLinks: [
      { icon: 'github', link: 'https://github.com' },
    ],

    // 页脚
    footer: {
      message: '基于 VitePress 构建',
      copyright: 'Copyright © 2026 Night Market Docs',
    },

    // 编辑链接
    editLink: {
      pattern: 'https://github.com/your-repo/edit/main/docs/:path',
      text: '在 GitHub 上编辑此页',
    },

    // 最后更新时间
    lastUpdated: {
      text: '最后更新于',
      formatOptions: {
        dateStyle: 'short',
        timeStyle: 'short',
      },
    },

    // 大纲
    outline: {
      level: [2, 3],
      label: '页面导航',
    },

    // 文档页脚
    docFooter: {
      prev: '上一页',
      next: '下一页',
    },
  },

  markdown: {
    lineNumbers: true,
  },
})
