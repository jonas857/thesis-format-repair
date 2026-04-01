# Rule Schema

Convert handbook clauses into a compact rule set before editing the thesis.

## Rule shape

Use a structure like this:

```yaml
- rule_id: "heading.chapter"
  status: "required"
  scope: "body"
  selector: "chapter-title"
  requirement: "Use third-size Heiti and center the chapter title."
  style:
    font_family: "黑体"
    font_size: "三号"
    bold: true
    alignment: "center"
    spacing_before: "2 blank lines below title"
  source_excerpt: "每“章”标题以三号黑体字居中打印。"
  source_file: "<spec.docx>"
  notes: ""
```

## Required fields

- `rule_id`: stable identifier
- `status`: `required` or `inferred`
- `scope`: front-matter, body, back-matter, global, figure, table, citation, etc.
- `selector`: the document region to target
- `requirement`: short human-readable rule
- `source_excerpt`: exact supporting clause for required rules

## Recommended style keys

Use only the keys needed by the rule:

- `font_family`
- `font_size`
- `bold`
- `italic`
- `color`
- `alignment`
- `line_spacing`
- `first_line_indent`
- `space_before`
- `space_after`
- `page_numbering`
- `header_footer`
- `margins`
- `paper_size`
- `caption_position`
- `numbering_pattern`

Use `notes` to record implementation facts that are not handbook rules but affect safe editing, for example:

- chapter headings use numeric CJK `styleId`s
- the running header must bind to a dedicated custom chapter style for Word/WPS compatibility
- the handbook requires a chapter-title header, but the document disables it because long titles exceed printable width and the user approved that fallback

## Extraction categories

Try to group rules into these buckets:

- document structure
- cover and front matter
- abstracts and keywords
- TOC
- heading hierarchy
- body typography
- page setup and pagination
- header/footer rules
- figures, tables, equations
- citations, footnotes, references
- appendices / acknowledgements / required forms

## Inference policy

Mark a rule as `inferred` only when:

- the source file shows a repeated layout pattern but does not state it directly, or
- a sample page clearly encodes a rule needed to repair the document

When a rule is inferred:

- say what evidence supports it
- avoid high-risk structural edits based only on that inference

## What not to encode as format rules

Do not place these into the rule set unless the product later expands to support them:

- thesis topic quality requirements
- originality or plagiarism thresholds
- scoring rubrics
- defense process instructions
- archive or submission logistics

Also do not treat these as handbook formatting rules:

- the specific `STYLEREF` token to use
- the specific `styleId` or internal style name in `styles.xml`
- compatibility workarounds needed for Word/WPS field evaluation
