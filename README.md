# docling-101

This repository contains experiments around measuring **PDF-to-Markdown conversion quality**, with the current design centered on the `mmcq` package.

## Current direction

The original `mmcq` design treated conversion quality as a mix of text similarity, table quality, headings, and lists. After review, the project direction has been refined to focus on a narrower and more reliable target:

- **Primary goal:** very high-quality conversion of **single-language English or Dutch text documents**
- **Primary success criteria:** preserve the **same text**, in the **same logical reading order**, with the **right markdown structure**
- **Out of scope for now:** multilingual robustness, figures/images, captions for non-text objects, and formula-heavy documents

## Prioritised improvement plan

The roadmap below reflects the recommended order of work.

### 1. Make exact text preservation the primary metric

Conversion quality should be judged first by whether the markdown preserves the original wording, not whether it is merely semantically similar.

Planned changes:

- add **character error rate (CER)** or equivalent character-level edit metrics
- add **word/token error rate (WER)** or token-level edit metrics
- report **insertions, deletions, and substitutions**
- keep **ROUGE-L** only as a secondary diagnostic
- make embedding-based semantic similarity **optional**, not central

Why this is first:

- for conversion, **paraphrase is usually a failure**
- exactness is the most important quality signal for legal, regulatory, and other text-heavy documents

### 2. Add omission and hallucination metrics

Length ratio alone is too weak. The evaluator should distinguish:

- **omissions**: source text missing from markdown
- **additions/hallucinations**: markdown text not supported by the source

These should be surfaced explicitly in the per-file report.

### 3. Add logical reading-order evaluation

One of the biggest remaining risks is good text extracted in the **wrong sequence**, especially in multi-column or complex layouts.

Planned changes:

- compare content at **page** and **block** level, not only whole-document level
- add an **order-sensitive score**
- flag likely reorderings when adjacent source blocks appear far apart or inverted in markdown

### 4. Move structure evaluation to gold markdown where possible

The previous design relied heavily on heuristics inferred from the PDF. That remains useful, but it is not strong enough as the only reference.

Planned changes:

- create a **small manually verified benchmark set**
- compare generated markdown against **gold markdown** for headings, lists, and paragraph boundaries
- keep PDF-derived structure only as a fallback or supporting signal

### 5. Keep structural checks, but align them to the narrowed scope

For the current scope, structure still matters, but after text exactness and reading order.

Priority structural metrics:

- **headings**: presence, text match, and level accuracy
- **lists**: item match and nesting depth
- **paragraph/block boundaries** where markdown readability matters
- **tables** only when present in text-centric documents

For tables:

- keep **TEDS** as the main structural comparison metric
- add **table presence/count matching** so missing tables are visible before structure scoring

### 6. Calibrate for English and Dutch document cleanup

The evaluator should normalise expected document-conversion artefacts without hiding real errors.

Planned normalization:

- line-break hyphenation repair
- quote, dash, and whitespace normalization
- handling of ligatures and common OCR-like character confusions
- English/Dutch-friendly tokenization

### 7. Define a weighted overall quality score

Once the stronger metrics exist, the project should publish a stable weighted score.

Suggested starting weights:

- **50%** text exactness
- **25%** reading order
- **20%** structure
- **5%** tables when applicable

If a document contains no tables, that weight should be redistributed across exactness and structure.

### 8. Add actionable reporting

The output should explain *why* a file scored badly.

Per-file reporting should include:

- overall score
- text exactness score
- omission/addition diagnostics
- reading-order score
- structure score
- representative error examples

### 9. Validate against human judgment

Before treating the score as reliable, the metric suite should be checked against human review.

Planned validation:

- sample English and Dutch documents
- obtain human rankings of conversion quality
- adjust weights and thresholds until the automatic score aligns with those rankings

## Summary of what changes most

The key shift is:

- **from** broad similarity-based evaluation
- **to** exactness-first evaluation for high-quality text conversion

In practical terms, `mmcq` should evolve from a general document-comparison prototype into a **text-faithfulness and reading-order evaluator** for English and Dutch PDFs that mostly contain text.

## Next repository focus

The next implementation milestones should be:

1. exact text metrics
2. omission/addition metrics
3. reading-order scoring
4. benchmark dataset creation
5. structure scoring against gold markdown
6. calibrated overall score