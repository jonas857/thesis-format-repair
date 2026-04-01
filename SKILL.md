---
name: thesis-format-repair
description: Read a thesis, dissertation, or graduation-project formatting handbook/template/specification, extract explicit formatting requirements, apply those requirements to a target `.docx` thesis, and report the results. Use when Codex needs to handle requests like "读取论文格式规范", "按学校论文规范调整格式", "修复毕业论文版式", "根据手册修改 docx", or any workflow that involves both a formatting specification file and a thesis document to be repaired.
---

# Thesis Format Repair

## Overview

Use this skill for AI-driven, specification-first thesis formatting work. Ground every formatting decision in the provided handbook or template, convert the handbook into explicit rules, apply only the needed `.docx` changes, and finish with a clear repair report.

## Workflow

### 1. Gather the artifacts

Identify three things up front:

- the formatting source: handbook, template, sample thesis, or formal specification
- the target thesis `.docx`
- the requested scope: full-document repair or only certain sections

If the formatting source is missing, stop and say so briefly. Do not invent institution-specific rules from memory.

Default to writing a sibling output copy unless the user explicitly asks for in-place edits.

### 2. Extract the rules from the formatting source

For `.docx` specifications, run:

```bash
python scripts/extract_docx_paragraphs.py <spec.docx>
```

If the file is long, narrow the search first:

```bash
python scripts/extract_docx_paragraphs.py <spec.docx> --grep "摘要|关键词|目录|页码|页眉|行距|黑体|宋体|图|表|参考文献"
```

Then read [references/rule-schema.md](references/rule-schema.md) and convert the relevant clauses into a structured rule set.

When extracting rules:

- keep only actionable format requirements
- label each rule as `required` or `inferred`
- include a short source excerpt for every required rule
- separate content rules from formatting rules

Prefer rules in this order of authority:

1. explicit handbook clauses
2. template/sample pages that clearly encode layout rules
3. cautious inference from repeated patterns

If a rule is only inferred, say so explicitly before using it.

### 3. Analyze the target thesis

Load the installed `minimax-docx` skill before editing the target `.docx`.

Use `minimax-docx` to:

- preview and analyze structure
- inspect section boundaries, headers, footers, page numbering, tables, images, and styles
- separate normative format rules from Word-internal implementation details such as style IDs, style names, and field bindings
- resolve the actual chapter-heading paragraphs and the actual style used by them before building running headers
- decide whether a simple CLI edit is enough or whether direct OpenXML/C# work is safer

Map the target into concrete regions:

- cover
- Chinese abstract
- English abstract
- keywords
- table of contents
- chapter/section/subsection headings
- body text
- figures and tables
- citations / footnotes / references
- appendices / acknowledgements
- headers / footers / page numbers

For header-sensitive documents, also inspect these implementation facts explicitly:

- the `w:styleId` and `w:name` for chapter-heading styles in `styles.xml`
- the actual `<w:pStyle>` values used by body chapter paragraphs in `document.xml`
- whether the document uses built-in heading styles, numeric CJK style IDs, or custom named styles
- whether the right-side running header text can fit inside the printable width after margins

### 4. Build a repair plan before writing

Repair in this order unless the user narrows the scope:

1. page setup, margins, paper size, section/page-number rules
2. front matter: cover, abstracts, keywords, TOC
3. heading hierarchy and body typography
4. figures, tables, captions, equation numbering
5. citations, footnotes, references
6. final normalization and validation

Prefer minimal, targeted edits. Do not rewrite thesis content just because a paragraph could read better.

### 5. Apply the repairs deterministically

Use `minimax-docx` CLI commands when the task is simple and direct. Use direct OpenXML/C# when the task depends on structure, section breaks, header/footer behavior, TOC logic, or fragile style interactions.

When a thesis requires a running header that shows the current chapter title:

- do not hardcode `Heading 1` or `heading 1` for `STYLEREF`
- treat the handbook rule and the Word implementation as separate questions: the handbook tells you that the header should show the chapter title, but it does not tell you which internal style or field token to bind
- resolve the target from the actual heading style after style mapping, using the paragraph style applied to body chapter titles
- verify that the chosen `STYLEREF` target exists in `styles.xml` and that the corresponding chapter paragraphs in `document.xml` actually use that style
- if the document uses numeric or pseudo-built-in CJK styles and `STYLEREF` is unstable in Word/WPS, create or reuse a dedicated chapter paragraph style and remap body chapter headings to it before inserting the field
- prefer a dedicated custom chapter style over guesswork when the document mixes built-in, numeric, and custom heading styles

When a running header is visually too long:

- check paper size and margins first; do not blame overflow on page setup until `A4` and margin values are verified
- compare the longest chapter title against the printable header width, not just the raw paper width
- if the title cannot fit reliably and the handbook does not provide a shorter header pattern, escalate clearly
- if the user allows it, remove the running header while preserving paper size, margins, section breaks, and page numbering
- do not leave a known-overflowing single-line header in place and claim compliance

After each substantial write:

```bash
$CLI merge-runs --input <doc.docx>
$CLI validate --input <doc.docx> --business
```

If the document structure is sensitive, also run:

```bash
$CLI fix-order --input <doc.docx>
```

Preserve:

- thesis content and argument
- existing citations, bookmarks, comments, and tracked metadata unless the task explicitly requires changing them
- required institutional forms and attachments

### 6. Report the result

Use [references/report-schema.md](references/report-schema.md) for the final report.

Always include:

- the formatting source used
- the rule categories extracted
- which rules were applied
- which header strategy was used: preserved, remapped to a dedicated style, shortened under an explicit rule, or disabled
- which edits were skipped and why
- which validations were run
- any remaining manual review points

## Guardrails

- Do not treat handbook examples as universal rules unless the handbook says so or the pattern is clearly normative.
- Do not invent citation or bibliography standards beyond what the source document states.
- Do not silently convert `required` rules into guesses.
- Do not confuse handbook formatting rules with Word implementation details; style binding, field codes, and compatibility fixes must be validated against the actual `.docx`.
- Do not claim full compliance when some sections could not be identified reliably.
- Do not collapse this into a pure style-transfer task; the first job is to extract explicit requirements.

## References

- Read [references/rule-schema.md](references/rule-schema.md) when turning handbook text into structured rules.
- Read [references/report-schema.md](references/report-schema.md) when composing the repair summary.

## Scripts

- `python scripts/extract_docx_paragraphs.py <spec.docx>` extracts non-empty paragraphs from a `.docx` handbook or template for rule review.
