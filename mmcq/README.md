# mmcq — Measure Markdown Conversion Quality

`mmcq` evaluates the quality of PDF-to-markdown conversion by comparing source PDF files against their converted markdown counterparts. It is designed to work with any converter (e.g. [Docling](https://github.com/DS4SD/docling), Marker, Mathpix) and produces per-file scores across four quality dimensions.

## Objective

Given two folders — one containing source PDFs and one containing converted markdown files — `mmcq` matches files by stem and computes a structured quality score for each pair. Results are printed as a formatted table and optionally exported to CSV.

```
mmcq ./documents/source ./documents/target/native --output report.csv
```

## Comparison approach

Each matched PDF/MD pair is evaluated in four independent dimensions:

### 1. Text fidelity
Plain text is extracted from the PDF (via `pdfplumber`) and from the markdown (via `markdown-it-py`). Two complementary metrics are applied:

- **Semantic similarity** — cosine similarity between sentence-transformer embeddings. Robust to rephrasing, whitespace differences, and minor OCR artefacts.
- **ROUGE-L** — longest common subsequence F1. Sensitive to verbatim content loss.
- **Coverage ratio** — character count of the markdown relative to the PDF. Flags truncation or bloat.

### 2. Table quality
Tables are extracted from both sources and compared using **TEDS (Tree Edit Distance Similarity)**, the standard metric for table structure evaluation introduced by the [PubTabNet](https://github.com/ibm-aur-nlp/PubTabNet) benchmark. TEDS compares tables as trees, capturing merged cells, row/column structure, and cell content simultaneously.

### 3. Heading structure
Headings are extracted from the PDF by inferring H-levels from relative font size and weight. Markdown headings are parsed directly from ATX/Setext syntax. Three sub-metrics are reported:

- **Precision** — fraction of markdown headings that match a PDF heading.
- **Recall** — fraction of PDF headings present in the markdown.
- **Level accuracy** — fraction of matched headings where the H-level (H1–H6) is also correct.

### 4. List structure
List items are detected in the PDF via bullet/number prefix and indentation analysis, and parsed directly from the markdown AST. Two sub-metrics are reported:

- **F1** — harmonic mean of list-item precision and recall over text content.
- **Depth accuracy** — fraction of matched items with the correct nesting depth.

## Metrics summary

| Dimension | Metric | Range | Library |
|---|---|---|---|
| Text | Semantic similarity | 0–1 | `sentence-transformers` |
| Text | ROUGE-L F1 | 0–1 | `rouge-score` |
| Text | Coverage ratio | 0–∞ (1.0 = ideal) | — |
| Tables | TEDS | 0–1 | `apted` |
| Headings | Precision / Recall | 0–1 | `markdown-it-py` |
| Headings | Level accuracy | 0–1 | `markdown-it-py` |
| Lists | F1 | 0–1 | `markdown-it-py` |
| Lists | Depth accuracy | 0–1 | `markdown-it-py` |

## Limitations

- **PDF heading inference is heuristic.** `mmcq` infers H-levels from font size and boldness because PDFs have no semantic heading tags. Results may be unreliable for scanned documents, inconsistently styled PDFs, or documents where heading fonts vary between sections.

- **PDF list detection is heuristic.** List items are identified by bullet/number prefixes and indentation. Complex multi-column layouts or lists with non-standard markers may be missed or misclassified.

- **Table pairing is positional.** Tables are matched by their order of appearance in the document. If the converter reorders tables, TEDS scores will be meaningless. A more robust approach would use content-based matching.

- **TEDS requires well-formed tables.** Severely malformed markdown tables (missing delimiters, inconsistent column counts) may fail to parse and will receive a score of 0 rather than a partial score.

- **Semantic similarity is document-length sensitive.** Sentence-transformer models have a token limit (~512 tokens by default). Very long documents are truncated before embedding, which can understate similarity for lengthy PDFs. Chunking strategies may be needed for large documents.

- **No visual or layout comparison.** `mmcq` operates on extracted text and structure only. It cannot detect misaligned columns, incorrect reading order across multi-column layouts, or missing figures beyond noting their absence as a coverage drop.

- **Language support.** The default sentence-transformer model (`all-MiniLM-L6-v2`) is optimised for English. Multi-lingual documents will produce less reliable semantic similarity scores unless a multilingual model is configured.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Print results to stdout
mmcq ./pdfs ./markdowns

# Write CSV report
mmcq ./pdfs ./markdowns --output report.csv

# Custom similarity threshold for warnings
mmcq ./pdfs ./markdowns --threshold 0.75
```
