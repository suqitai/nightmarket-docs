#!/usr/bin/env python3
"""为每个插件生成终端风格的占位截图。等 phantom 截图后替换。"""

from PIL import Image, ImageDraw, ImageFont
import os

WIDTH, HEIGHT = 800, 450
BG_COLOR = (30, 30, 40)
TITLE_BG = (50, 50, 65)
TEXT_COLOR = (200, 210, 220)
ACCENT = (120, 160, 255)
GREEN = (100, 220, 130)
YELLOW = (240, 200, 80)
DIM = (120, 130, 145)

PLUGINS = [
    ("attune", "全周期项目开发", [
        "$ /attune:brainstorm --domain \"web app\"",
        "🧠 头脑风暴 → 项目简报 docs/project-brief.md",
        "$ /attune:specify",
        "📋 规格说明 → 24 FRs + 5 NFRs",
        "$ /attune:blueprint --detailed",
        "🏗️ 实施计划 → 35 tasks · 6 phases",
    ]),
    ("spec-kit", "规格驱动开发", [
        "$ /speckit-clarify --spec docs/prd.md --depth high",
        "🔍 检测到 12 个歧义点",
        "$ /speckit-specify --feature \"用户认证\"",
        "📋 生成 8 个 FR · 22 条验收标准",
    ]),
    ("imbue", "TDD 质量门禁", [
        "$ /imbue:tdd --file src/auth.py --strict",
        "🔴 RED   → 测试失败 (expected)",
        "🟢 GREEN → 测试通过 (4/4)",
        "🔵 REFACTOR → 提取 validate_email()",
        "$ /imbue:rice --items docs/backlog.md",
        "📊 RICE 排序完成 · 15 需求已优先",
    ]),
    ("sanctum", "Git 工作流管理", [
        "$ /sanctum:branch --type feature --name \"payment\"",
        "🌿 分支 feature/payment 已创建",
        "$ /sanctum:commit --type feat --scope payment",
        "✅ feat(payment): 集成 Stripe 支付",
        "$ /sanctum:pr --base main --reviewers alice,bob",
        "📤 PR #56 已创建 · 等待审查",
    ]),
    ("pensive", "多维度代码审查", [
        "$ /pensive:review --dimensions arch,bug,security",
        "🔍 审查 src/payment/ · 3 维度",
        "🔴 CRITICAL: SQL 注入风险 (line 142)",
        "🟡 HIGH: 缺少事务回滚 (line 89)",
        "🟢 MEDIUM: 函数过长 (line 200, 62行)",
    ]),
    ("scribe", "文档审查", [
        "$ /scribe:fluff --file docs/api.md --threshold medium",
        "📝 检测到 8 处 AI 废话",
        "  • \"强大的\" → 替换为具体功能描述",
        "  • \"无缝\" → 说明集成步骤",
        "$ /scribe:sync --code src/api/ --docs docs/",
        "⚠️ 3 处不一致: user_id→userId 未更新",
    ]),
    ("abstract", "Skill/Hook 开发", [
        "$ /abstract:create-skill --name \"pr-check\"",
        "🔨 TDD 流程: 红 → 绿 → 重构",
        "$ /abstract:skills-eval --path skills/",
        "📊 评分: 85/100 (优秀)",
        "  Token效率: 90 · 内容质量: 82 · 安全: 88",
    ]),
    ("leyline", "基础安全设施", [
        "$ /leyline:audit-deps --path . --severity all",
        "🔒 扫描 127 依赖 · 0 CRITICAL · 2 HIGH",
        "$ /leyline:check-injection --type prompt",
        "🛡️ 注入检测: 安全 ✅",
        "$ /leyline:risk-classify --task \"删除数据库\"",
        "🔴 CRITICAL · 需二次确认",
    ]),
    ("hookify", "行为规则引擎", [
        "$ /hookify:create --name \"no-todo\" --event pre-commit",
        "✅ Hook 已创建: .claude/hooks/no-todo.md",
        "$ /hookify:list --event pre-commit",
        "  📋 format-check · no-todo · test-before-push",
        "$ /hookify:validate --path .claude/hooks/",
        "✅ 3/3 Hooks 验证通过",
    ]),
    ("egregore", "自主 Agent 编排", [
        "$ /egregore:workflow --script review.js --max-workers 4",
        "🤖 Agent-1: 架构审查 ████████ ✅",
        "🤖 Agent-2: Bug 检测  ██████░░ 🔄",
        "🤖 Agent-3: 安全审查 ████░░░░ 🔄",
        "🤖 Agent-4: 性能分析 ██░░░░░░ 🔄",
    ]),
    ("conjure", "外部 LLM 委托", [
        "$ /conjure:route --task \"翻译注释\" --budget low",
        "🔀 路由到: Gemini Flash (低成本)",
        "$ /conjure:compare --models claude,gemini,qwen",
        "📊 三模型对比结果:",
        "  Claude: 92 · Gemini: 78 · Qwen: 81",
    ]),
    ("minister", "GitHub Issue 管理", [
        "$ /minister:dashboard --milestone \"Sprint 6\"",
        "📋 TODO: 5 · 🔄 IN PROGRESS: 3 · ✅ DONE: 8",
        "$ /minister:triage --filter \"no-label\"",
        "🔖 建议标签 · 30 issues 待分类",
        "$ /minister:report --type sprint",
        "📊 Sprint 6: 80% 完成率 · 燃尽图 →",
    ]),
    ("archetypes", "架构范式选择", [
        "$ /archetypes:select --domain \"SaaS 多租户\"",
        "🏗️ 推荐: 模块化单体 + 六边形架构",
        "  理由: 当前规模(500租户)微服务ROI<1",
        "$ /archetypes:compare --a hexagonal --b layered",
        "  六边形: 依赖反转 · 可测试性高 · 学习曲线中",
        "  分层:   简单直观 · 易耦合 · 学习曲线低",
    ]),
    ("cartograph", "代码可视化", [
        "$ /cartograph:map --path src/ --depth 2",
        "```mermaid",
        "graph TD",
        "  API[API Layer] --> Core[Core Domain]",
        "  Core --> DB[(Database)]",
        "  Core --> Cache[(Redis)]",
        "```",
    ]),
    ("gauntlet", "代码库学习", [
        "$ /gauntlet:learn --path src/ --focus core",
        "🧠 知识图谱: 45 实体 · 128 关系",
        "$ /gauntlet:challenge --count 10",
        "📝 Q1: OrderService 依赖哪些模块?",
        "   ✅ 正确! · 上次复习: 3天前",
        "📝 Q2: PaymentGateway 接口在哪?",
        "   ❌ · 将加入高频复习队列",
    ]),
    ("tome", "多源研究", [
        "$ /tome:research --topic \"JWT vs Session\"",
        "🔍 搜索中: HN · Reddit · arXiv · 技术博客",
        "📄 HN: \"JWT pitfalls\" (342 points, 156 comments)",
        "📄 Reddit: r/webdev · \"Session still better?\"",
        "📊 综合建议: 普通场景 Session · 微服务 JWT",
    ]),
    ("memory-palace", "记忆宫殿", [
        "$ /memory-palace:store --room project-x",
        "💾 已存储: 选择 PG 而非 MySQL 因为 JSONB",
        "$ /memory-palace:map --room project-x",
        "📂 project-x/",
        "  ├── 📄 架构决策 (3 条)",
        "  ├── 📄 部署流程 (2 条)",
        "  └── 📄 API 设计 (5 条)",
    ]),
    ("phantom", "桌面自动化", [
        "$ /phantom:screenshot --mode terminal --delay 2",
        "📸 截图已保存: result.png (2880×1800)",
        "$ /phantom:annotate --image shot.png",
        "✏️ 添加箭头 (120,80→300,80)",
        "✏️ 添加文字 \"关键步骤\"",
    ]),
    ("scry", "媒体生成", [
        "$ /scry:record --type terminal --fps 15",
        "🎬 录制中... 00:28 / 00:30",
        "$ /scry:export --input demo.mp4 --format gif",
        "🔄 导出 GIF · 优化中...",
        "✅ demo.gif · 4.2MB · 15fps · 720p",
    ]),
    ("herald", "通知系统", [
        "$ /herald:watch --event on-build-complete",
        "🔔 监听: 构建完成 → Slack #dev",
        "$ /herald:notify --channel slack",
        "📤 [Slack #dev] 部署成功 · 耗时 2m34s",
        "$ /herald:issue --issue 42 --status close",
        "✅ Issue #42 已关闭 · 附 PR #56 链接",
    ]),
    ("conserve", "上下文优化", [
        "$ /conserve:analyze --scope session",
        "📊 Token消耗: 85,200 / 200,000 (42%)",
        "$ /conserve:bloat --path skills/large-skill.md",
        "🔍 膨胀检测: 8500 tokens · 冗余 37%",
        "✂️ 建议: 3案例→1 · 概述 800→200 tokens",
    ]),
    ("parseltongue", "Python 开发套件", [
        "$ /parseltongue:profile --file src/bottleneck.py",
        "🔥 Top 5 CPU 热点:",
        "  1. serialize_response()  380ms ████████",
        "  2. db_query()            120ms ███",
        "  3. validate_input()       45ms █",
    ]),
    ("oracle", "ONNX 本地推理", [
        "$ /oracle:load --model \"code-classifier\"",
        "📦 加载 ONNX 模型: code-classifier (128MB)",
        "$ /oracle:infer --input \"$CODE\" --task classify",
        "🏷️ 分类结果: API Handler (置信度 92%)",
        "$ /oracle:benchmark --iterations 100",
        "⚡ 平均延迟: 48ms · 吞吐: 21 req/s",
    ]),
]

def draw_placeholder(name, desc, lines, output_path):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # 标题栏
    draw.rectangle([0, 0, WIDTH, 42], fill=TITLE_BG)
    draw.text((16, 10), f"Claude Code — Terminal", fill=DIM)

    # 标题分隔线
    draw.line([0, 42, WIDTH, 42], fill=(70, 70, 85))

    # 插件名
    draw.text((28, 60), f"# {name} — {desc}", fill=ACCENT)

    # 终端内容
    y = 100
    for line in lines:
        if line.startswith("$"):
            # 命令提示符行
            prompt = line[:2]
            cmd = line[2:]
            draw.text((28, y), prompt, fill=GREEN)
            draw.text((48, y), cmd, fill=TEXT_COLOR)
        elif line.startswith("🔴") or line.startswith("🟡") or line.startswith("🟢"):
            draw.text((28, y), line, fill=TEXT_COLOR)
        elif line.startswith("✅") or line.startswith("🎬") or line.startswith("📸"):
            draw.text((28, y), line, fill=GREEN)
        elif line.startswith("⚠️") or line.startswith("🔍") or line.startswith("📝"):
            draw.text((28, y), line, fill=YELLOW)
        elif line.startswith("🔒") or line.startswith("🛡️") or line.startswith("🤖"):
            draw.text((28, y), line, fill=ACCENT)
        else:
            draw.text((28, y), line, fill=TEXT_COLOR)
        y += 24

    # 底部标注
    draw.text((16, HEIGHT - 28), "📸 placeholder — 用 phantom 替换为实际截图", fill=DIM)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"  ✅ {output_path}")

def main():
    base = "public/images"
    for name, desc, lines in PLUGINS:
        path = os.path.join(base, name, "terminal-preview.png")
        draw_placeholder(name, desc, lines, path)
    print(f"\n🎉 生成了 {len(PLUGINS)} 个占位截图")

if __name__ == "__main__":
    main()
