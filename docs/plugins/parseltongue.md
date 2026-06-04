# parseltongue — Python 开发套件

## 概述

parseltongue 是 Night Market 中的 Python 开发工具集，覆盖测试、性能分析、异步模式、类型检查等 Python 开发的核心需求。它是 Python 项目的「瑞士军刀」，将最常用的开发工具整合为一致的命令行体验。

**核心能力：**
- 测试增强：pytest 配置生成、fixture 管理、覆盖率报告
- 性能分析：CPU/内存 profiling、热点函数识别
- 异步模式：asyncio 最佳实践检查、协程泄漏检测
- 类型检查：mypy 配置和增量类型注解
- 代码质量：自动化 lint、format、import 排序

**适用场景：**
- Python 项目的测试基础设施搭建
- 性能瓶颈定位和优化
- 异步代码的正确性检查
- 渐进式类型注解的引入

---

## 安装

```bash
claude plugins install parseltongue@claude-night-market
claude plugins list | grep parseltongue
```

**前置条件：**
- Python ≥ 3.10
- pytest、mypy、ruff 等工具会自动按需安装

---

## 命令参考

| 命令 | 必需参数 | 可选参数 | 说明 | 使用示例 |
|------|----------|----------|------|------|
| `/parseltongue:test` | — | `--file`, `--cov`, `--parallel` | 运行测试和分析 | `/parseltongue:test --file tests/ --cov --parallel` |
| `/parseltongue:profile` | `--file` | `--type`, `--top` | 性能 profiling | `/parseltongue:profile --file src/bottleneck.py --type cpu --top 10` |
| `/parseltongue:async` | `--path` | `--check` | 异步代码检查 | `/parseltongue:async --path src/ --check blocking` |
| `/parseltongue:types` | `--path` | `--strict` | 类型检查和建议 | `/parseltongue:types --path src/ --strict` |
| `/parseltongue:setup` | — | `--lang`, `--features` | 初始化 Python 项目配置 | `/parseltongue:setup --features "test,lint,typecheck"` |

---

## 使用场景

### 场景 1：定位性能瓶颈

**问题：** API 响应从 50ms 涨到 500ms，不知道哪里变慢了。

**解决方案：** 用 profile 做 CPU profiling，找出热点函数。

**命令示例：**
```bash
/parseltongue:profile --file src/api/endpoints.py --type cpu --top 10
```

**预期结果：** 显示 Top 10 耗时函数，发现 `serialize_response()` 耗时从 2ms 涨到 400ms——某个字段的序列化逻辑有问题。

---

### 场景 2：异步代码阻塞检测

**问题：** asyncio 服务偶尔出现 2 秒的「暂停」，怀疑有同步阻塞代码。

**解决方案：** 用 async check 扫描阻塞调用。

**命令示例：**
```bash
/parseltongue:async --path src/ --check blocking
```

**预期结果：** 发现 2 处同步阻塞——`time.sleep()` 应为 `asyncio.sleep()`，数据库调用未使用 async driver。

---

## 实战案例

### 案例 1：新 Python 项目一键配置

**背景：** 启动一个新 Django 项目，需要配置 pytest、mypy、ruff。

**操作步骤：**

1. **一键配置**
   ```bash
   /parseltongue:setup --features "test,lint,typecheck,profile"
   ```

2. **自动生成** — `pyproject.toml` 配置段、`pytest.ini`、`.pre-commit-config.yaml`

3. **验证**
   ```bash
   /parseltongue:test --cov
   ```

**结果展示：**

<div class="nm-tip">
📸 <strong>截图待制作</strong>：展示 parseltongue profile 输出。运行 <code>bash scripts/screenshot.sh parseltongue</code> 生成。
</div>

---

## 常见问题

<details class="faq-item">
<summary>Q: parseltongue 和 pytest 本身有什么区别？</summary>
<div class="answer">

**A:** parseltongue 不是替代品，而是增强层：

- 自动生成最优配置（`pytest.ini`、覆盖率阈值、并行策略）
- 集成 profiling 和测试（一次命令同时跑测试+性能分析）
- AI 辅助的失败分析（测试失败时自动分析原因并建议修复）

底层的测试执行仍然是 pytest。
</div>
</details>

<details class="faq-item">
<summary>Q: 支持非纯 Python 项目（如 Django、FastAPI）吗？</summary>
<div class="answer">

**A:** 完全支持。parseltongue 自动检测框架并调整配置：

- **Django**：自动配置 `DJANGO_SETTINGS_MODULE`，pytest-django fixture
- **FastAPI**：自动配置 TestClient，异步测试支持
- **纯库**：标准 pytest 配置

`/parseltongue:setup` 会自动检测项目类型并生成对应配置。
</div>
</details>

---

## 相关插件

| 插件 | 协作方式 |
|------|----------|
| [conserve](./conserve.md) | conserve 优化 Token，parseltongue 优化代码性能 |
| [imbue](./imbue.md) | imbue 的 TDD 流程使用 parseltongue 的测试增强 |

---

> 📝 最后更新：2026-06-04
