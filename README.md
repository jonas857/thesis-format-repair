# thesis-format-repair

`thesis-format-repair` is a Codex skill for specification-first thesis formatting repair.

It is designed for workflows where you have:

- a thesis formatting handbook, template, or sample document
- a target thesis `.docx`
- a request to repair formatting without inventing school-specific rules

The skill tells Codex how to extract explicit formatting requirements from the source specification, analyze the target thesis structure, apply deterministic `.docx` repairs, and produce a clear repair report.

## What This Skill Does

- Reads a handbook, template, or sample thesis as the formatting authority
- Converts explicit clauses into a structured rule set
- Separates required rules from inferred rules
- Repairs thesis formatting in a controlled order
- Preserves thesis content unless the task explicitly requires content changes
- Reports what was changed, skipped, and validated

This skill is especially useful for requests such as:

- reading a university thesis formatting specification
- repairing a graduation thesis layout based on a handbook
- adjusting an existing `.docx` thesis to match institutional rules

## Workflow

The skill follows a six-step workflow:

1. Gather the formatting source, target thesis, and repair scope.
2. Extract actionable formatting rules from the source.
3. Analyze the target thesis structure and relevant `.docx` implementation details.
4. Build a repair plan before writing.
5. Apply deterministic repairs with validation after substantial edits.
6. Produce a repair report with remaining manual checks.

The workflow intentionally prioritizes explicit handbook rules over guesswork.

## Directory Structure

```text
SKILL.md
agents/openai.yaml
references/report-schema.md
references/rule-schema.md
scripts/extract_docx_paragraphs.py
```

## Files

- `SKILL.md`: the main skill definition and end-to-end workflow
- `agents/openai.yaml`: agent configuration used by the skill
- `references/rule-schema.md`: schema for turning handbook clauses into structured formatting rules
- `references/report-schema.md`: schema for writing the final repair report
- `scripts/extract_docx_paragraphs.py`: utility for extracting non-empty paragraphs from a `.docx` specification

## Typical Usage

Start by extracting text from the specification document:

```bash
python scripts/extract_docx_paragraphs.py <spec.docx>
```

If the specification is long, narrow the search to likely formatting sections:

```bash
python scripts/extract_docx_paragraphs.py <spec.docx> --grep "<keywords>"
```

Then use the extracted clauses together with:

- `references/rule-schema.md` to build a structured rule set
- `references/report-schema.md` to write the final repair report

## Repair Principles

- Use the provided specification as the source of truth.
- Do not invent institution-specific formatting rules from memory.
- Label rules as `required` or `inferred`.
- Prefer minimal, targeted `.docx` edits.
- Preserve original thesis content, citations, bookmarks, and metadata unless the task says otherwise.
- Do not claim full compliance when some sections or rules cannot be verified.

## Related Tooling

The skill expects Codex to load the `minimax-docx` skill before editing the target thesis document. That companion skill is used for:

- structure inspection
- section and style analysis
- header/footer and page-number handling
- safer OpenXML-based repairs when direct CLI edits are not enough

## Output

A typical run should produce:

- a repaired thesis `.docx` file, usually as a sibling copy
- a structured summary of extracted rules
- a repair report listing applied changes, skipped changes, validations, and manual review points

## Repository Purpose

This repository packages the full `thesis-format-repair` skill so it can be versioned, shared, and reused independently of the larger local Codex skill collection.
