# oracle — 本地 ML 推理

## 概述

oracle 是 Night Market 中的本地机器学习推理插件，基于 ONNX Runtime 在本地运行 ML 模型。它让你在不依赖云服务的情况下进行模型推理，保护数据隐私的同时降低延迟。

**核心能力：**
- ONNX 模型加载：支持从 HuggingFace 或本地加载 ONNX 模型
- 本地推理：所有计算在本地完成，数据不出机器
- 多模型管理：切换和管理多个模型
- 性能优化：自动选择最优执行提供者（CPU/CoreML/CUDA）
- 结果解释：推理结果的人类可读解释

**适用场景：**
- 需要 ML 辅助但数据不能上云（隐私/合规）
- 低延迟推理（无网络往返）
- 离线环境下的 ML 任务
- 代码分析中的辅助分类

---

## 安装

```bash
claude plugins install oracle@claude-night-market
claude plugins list | grep oracle
```

**前置条件：**
- Python ≥ 3.10
- `pip install onnxruntime`（CPU 版本）或 `onnxruntime-gpu`（GPU 加速）

---

## 命令参考

| 命令 | 必需参数 | 可选参数 | 说明 | 使用示例 |
|------|----------|----------|------|------|
| `/oracle:load` | `--model` | `--source`, `--provider` | 加载 ONNX 模型 | `/oracle:load --model "codebert-base" --source huggingface` |
| `/oracle:infer` | `--model`, `--input` | `--task` | 执行推理 | `/oracle:infer --model codebert --input "$CODE" --task classify` |
| `/oracle:models` | — | `--status` | 列出已加载的模型 | `/oracle:models --status` |
| `/oracle:benchmark` | `--model` | `--iterations` | 模型性能基准测试 | `/oracle:benchmark --model codebert --iterations 100` |
| `/oracle:unload` | `--model` | — | 卸载模型释放内存 | `/oracle:unload --model codebert` |

---

## 使用场景

### 场景 1：本地代码分类

**问题：** 需要将 1000 个文件按功能分类，但代码不能上传到外部 API。

**解决方案：** 用 oracle 加载本地代码分类模型，离线处理。

**命令示例：**
```bash
/oracle:load --model "code-classifier" --source local --provider cpu
/oracle:infer --model code-classifier --input "$FILE_CONTENT" --task classify
```

**预期结果：** 模型在本地 CPU 上推理，返回「API Handler」「Database Model」「Business Logic」等分类标签，全程无数据外传。

---

### 场景 2：代码质量快速扫描

**问题：** 需要在提交前快速扫描代码是否有明显问题。

**解决方案：** 加载本地代码质量评估模型，做预筛选。

**命令示例：**
```bash
/oracle:load --model "code-quality-scorer"
/oracle:infer --model code-quality-scorer --input "$DIFF" --task score
```

**预期结果：** 返回 0-100 质量评分和低分原因（如「嵌套层级过深」「函数过长」），高分则跳过详细审查节省时间。

---

## 实战案例

### 案例 1：离线环境下 ML 辅助代码审查

**背景：** 某金融公司开发环境完全离线，但希望用 ML 模型辅助代码审查。

**操作步骤：**

1. **在有网环境下载模型**
   ```bash
   /oracle:load --model "code-review-bert" --source huggingface
   ```
   *模型缓存到本地，可移植到离线环境*

2. **在离线环境使用**
   ```bash
   /oracle:infer --model code-review-bert --input "$PR_DIFF" --task analyze
   ```
   *完全本地推理，零网络依赖*

**结果展示：**

<div class="nm-tip">
📸 <strong>截图待制作</strong>：展示 oracle 推理结果。运行 <code>bash scripts/screenshot.sh oracle</code> 生成。
</div>

---

## 常见问题

<details class="faq-item">
<summary>Q: oracle 和云上 LLM 推理有什么区别？</summary>
<div class="answer">

**A:** 

| 维度 | oracle (ONNX) | 云 LLM (Claude/GPT) |
|------|:---:|:---:|
| 数据隐私 | ✅ 完全本地 | ⚠️ 数据上传云端 |
| 延迟 | < 100ms | 1-10s |
| 模型能力 | 专用小模型 | 通用大模型 |
| 硬件要求 | CPU 即可 | 无要求 |
| 适用任务 | 分类/评分/检测 | 生成/推理/对话 |

oracle 不是 Claude 的替代品，而是特定任务（分类、评分）的本地加速方案。
</div>
</details>

<details class="faq-item">
<summary>Q: 支持哪些模型格式和来源？</summary>
<div class="answer">

**A:** 
- **格式**：ONNX（`.onnx`）、部分 PyTorch/TensorFlow 可自动转换
- **来源**：
  - HuggingFace Hub（自动下载转换）
  - 本地 `.onnx` 文件
  - 自定义训练的模型

推荐使用 HuggingFace 上的预训练 ONNX 模型，质量有保障。
</div>
</details>

---

## 相关插件

| 插件 | 协作方式 |
|------|----------|
| [pensive](./pensive.md) | pensive 做全面审查，oracle 做快速预筛选 |
| [conserve](./conserve.md) | oracle 本地推理节省 Token，conserve 管理 Token 预算 |

---

> 📝 最后更新：2026-06-04
