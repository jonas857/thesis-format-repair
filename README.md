# thesis-format-repair

中文说明在前，英文说明在后。

## 中文

`thesis-format-repair` 是一个面向 Codex 的论文格式修复 skill，用于“先读规范，再改文档”的论文排版修复流程。

它适合处理这类任务：

- 已有学校论文格式手册、模板或样例
- 已有待修复的论文 `.docx`
- 目标是按规范修正格式，而不是凭经验猜学校要求

这个 skill 的核心思路是：

1. 先从格式规范中提取明确规则
2. 再分析目标论文的结构与 `.docx` 实现细节
3. 最后做最小化、可验证的格式修复

### 能做什么

- 读取论文格式手册、模板或样例文档
- 将规范条款整理成结构化规则
- 区分 `required` 和 `inferred` 规则
- 按固定顺序修复论文格式
- 尽量保留原始正文内容、引用、书签和元数据
- 输出修复报告，说明改了什么、为什么改、哪些地方仍需人工复核

### 典型使用场景

- 读取高校毕业论文格式规范
- 按论文手册修复现有 `.docx`
- 基于模板或样例统一论文版式
- 检查页眉、页脚、页码、标题层级、摘要、目录、参考文献等格式问题

### 工作流程

这个 skill 的标准流程分为 6 步：

1. 收集输入材料
2. 从规范中提取规则
3. 分析目标论文结构
4. 制定修复计划
5. 执行确定性的格式修复
6. 输出修复报告

它强调“规范优先”，避免把经验判断误当成学校明确要求。

### 仓库结构

```text
SKILL.md
agents/openai.yaml
references/report-schema.md
references/rule-schema.md
scripts/extract_docx_paragraphs.py
```

### 主要文件说明

- `SKILL.md`：skill 主定义和完整工作流
- `agents/openai.yaml`：skill 使用的 agent 配置
- `references/rule-schema.md`：规范条款转结构化规则的参考格式
- `references/report-schema.md`：修复报告的参考格式
- `scripts/extract_docx_paragraphs.py`：从 `.docx` 规范文档中提取非空段落的脚本

### 基本用法

先从格式规范文档中提取段落：

```bash
python scripts/extract_docx_paragraphs.py <spec.docx>
```

如果规范较长，可以先按关键词筛选：

```bash
python scripts/extract_docx_paragraphs.py <spec.docx> --grep "<keywords>"
```

之后结合：

- `references/rule-schema.md` 整理格式规则
- `references/report-schema.md` 输出修复报告

### 修复原则

- 以用户提供的规范为准
- 不凭记忆臆造学校格式要求
- 明确标记 `required` 和 `inferred`
- 优先做最小化、定点式修改
- 不随意改写论文内容
- 无法确认的部分不宣称“完全符合规范”

### 相关依赖

这个 skill 预期会配合 `minimax-docx` skill 一起使用，用于：

- 分析文档结构
- 检查节、样式、页眉页脚、页码
- 在简单 CLI 修改不够稳妥时执行更安全的 OpenXML 修复

### 输出结果

一次典型运行通常会产出：

- 修复后的论文 `.docx`，默认尽量保留原文件并输出副本
- 结构化规则摘要
- 修复报告，说明已应用规则、跳过项、校验过程和人工复核点

### 仓库用途

这个仓库用于单独发布和维护 `thesis-format-repair` skill，方便版本管理、分享和复用。

### 许可证

本仓库使用 `Apache-2.0` 许可证，详见 `LICENSE` 文件。

## English

`thesis-format-repair` is a Codex skill for specification-first thesis formatting repair.

It is built for workflows where you have:

- a thesis formatting handbook, template, or sample document
- a target thesis `.docx`
- a request to repair formatting without inventing institution-specific rules

The skill follows a simple idea:

1. extract explicit formatting requirements from the source specification
2. analyze the target thesis structure and `.docx` implementation details
3. apply minimal, deterministic, and verifiable repairs

### What It Does

- Reads a handbook, template, or sample thesis as the formatting authority
- Converts explicit clauses into a structured rule set
- Separates `required` rules from `inferred` rules
- Repairs thesis formatting in a controlled order
- Preserves thesis content unless the task explicitly requires content edits
- Produces a repair report with applied changes, skipped items, validations, and manual review points

### Typical Use Cases

- reading a university thesis formatting specification
- repairing a graduation thesis layout based on a handbook
- adjusting an existing `.docx` thesis to match institutional rules
- checking headers, footers, page numbering, heading hierarchy, abstracts, TOC, and references

### Workflow

The standard workflow has six steps:

1. Gather the input artifacts.
2. Extract rules from the specification.
3. Analyze the target thesis structure.
4. Build a repair plan.
5. Apply deterministic repairs.
6. Produce a repair report.

This workflow keeps explicit handbook rules ahead of guesswork.

### Repository Layout

```text
SKILL.md
agents/openai.yaml
references/report-schema.md
references/rule-schema.md
scripts/extract_docx_paragraphs.py
```

### Files

- `SKILL.md`: main skill definition and end-to-end workflow
- `agents/openai.yaml`: agent configuration used by the skill
- `references/rule-schema.md`: schema for turning handbook clauses into structured rules
- `references/report-schema.md`: schema for writing the final repair report
- `scripts/extract_docx_paragraphs.py`: helper script for extracting non-empty paragraphs from a `.docx` specification

### Basic Usage

Extract text from the specification document:

```bash
python scripts/extract_docx_paragraphs.py <spec.docx>
```

If the specification is long, narrow it first:

```bash
python scripts/extract_docx_paragraphs.py <spec.docx> --grep "<keywords>"
```

Then use:

- `references/rule-schema.md` to build the rule set
- `references/report-schema.md` to write the repair summary

### Repair Principles

- Use the provided specification as the source of truth.
- Do not invent school-specific formatting rules from memory.
- Mark rules as `required` or `inferred`.
- Prefer minimal, targeted `.docx` edits.
- Preserve original thesis content, citations, bookmarks, and metadata unless the task says otherwise.
- Do not claim full compliance when some sections or rules cannot be verified.

### Related Tooling

This skill is intended to work with the `minimax-docx` skill for:

- structure inspection
- section and style analysis
- header/footer and page-number handling
- safer OpenXML-based repairs when simple CLI edits are not enough

### Expected Output

A typical run should produce:

- a repaired thesis `.docx`, usually as a sibling copy
- a structured rule summary
- a repair report listing applied rules, skipped changes, validations, and manual review items

### Repository Purpose

This repository packages the full `thesis-format-repair` skill so it can be versioned, shared, and reused independently.

### License

This repository is licensed under `Apache-2.0`. See `LICENSE` for details.
