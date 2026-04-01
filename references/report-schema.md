# Report Schema

Use this structure for the final repair report.

## Report sections

### 1. Inputs

- formatting source file
- target thesis file
- repair scope

### 2. Extracted rule summary

Summarize the rule buckets you found, for example:

- front matter
- heading hierarchy
- body typography
- page numbering
- figure/table captions
- references

Mention which rules were explicit and which were inferred.

### 3. Applied changes

For each changed area, report:

- region
- what changed
- rule basis

If headers/footers were involved, also report:

- whether the running header was kept, remapped to a safer style, or removed
- whether the decision was driven by handbook rules, Word/WPS compatibility, or overflow risk

Example:

```text
- Title paragraph: set to SimSun, 10.5pt, bold, black
  Basis: handbook clause requiring title style
```

### 4. Validation

List the checks you ran:

- structural analysis
- merge-runs
- business validation
- fix-order if used
- spot-check of XML or rendered output if needed
- explicit header checks if applicable: field target exists, chapter paragraphs actually use that style, and the header text fits the printable width or was intentionally disabled

### 5. Remaining manual checks

Call out issues that need a human look, for example:

- ambiguous heading mapping
- long chapter titles that may overflow a one-line running header
- sample-based rules that were inferred
- figures/tables spread across multiple sections
- reference formatting that requires semantic review

### 6. Output

- output file path
- whether the original was preserved

## Tone

Keep the report operational and specific. Avoid vague claims like "format optimized" or "fully compliant" unless every required rule was actually checked.
