# Stage 04: Semantic Coherence Analysis

Transformer-inspired analysis to assess logical structure and semantic coherence of document chapters.

## Overview

This analysis uses ML clustering to identify thematic patterns, structural issues, and organizational opportunities in large chapters.

### Three-Phase Process

1. **Phase 1: Section Extraction & Summarization**
   - Extract markdown section hierarchy
   - Generate AI-powered summaries of major sections

2. **Phase 2: Semantic Clustering**
   - Convert summaries to embeddings
   - Cluster similar sections using hierarchical clustering
   - Identify coherence patterns and outliers

3. **Phase 3: Coherence Reporting**
   - Generate human-readable analysis report
   - Provide actionable reorganization recommendations

## Usage

### Quick Start (Chapter 5 Example)

```bash
# 1. Extract sections
.venv/bin/python scripts/04_analysis/01_extract_sections.py \
    output/chapters/04_merged/chapter_05_deduplicated.md

# 2. Perform clustering (directly on section content)
.venv/bin/python scripts/04_analysis/03_cluster_analysis.py \
    output/chapters/04_merged/chapter_05_sections.yaml \
    output/chapters/04_merged/chapter_05_deduplicated.md

# 3. Generate report
.venv/bin/python scripts/04_analysis/04_generate_report.py \
    output/chapters/04_merged/chapter_05_clusters.json
```

**Note**: The summarization script (02_summarize_sections.py) is optional and only needed if you want to use Claude API for higher-quality summaries before clustering. By default, we cluster directly on section content.

### Individual Script Usage

#### 01_extract_sections.py

Extract section hierarchy and metadata from markdown files.

```bash
.venv/bin/python scripts/04_analysis/01_extract_sections.py <input_file> [output_file]
```

**Output**: YAML file with section metadata (ID, heading, line ranges, token estimates, completeness)

#### 02_summarize_sections.py

Generate AI summaries for major sections (levels 2-3).

```bash
export ANTHROPIC_API_KEY="your-key-here"
.venv/bin/python scripts/04_analysis/02_summarize_sections.py <sections_yaml> <markdown_file> [output_file]
```

**Note**: Falls back to simple text extraction if API key not available.

**Output**: YAML file with section summaries

#### 03_cluster_analysis.py

Perform semantic clustering on section content.

```bash
.venv/bin/python scripts/04_analysis/03_cluster_analysis.py <sections_yaml> <markdown_file> [output_file]
```

**Output**:
- JSON file with cluster assignments and metrics
- PNG dendrogram visualization

#### 04_generate_report.py

Generate human-readable coherence analysis report.

```bash
.venv/bin/python scripts/04_analysis/04_generate_report.py <clusters_json> [output_file]
```

**Output**: Markdown report with findings and recommendations

## Dependencies

Install required packages:

```bash
source .venv/bin/activate
pip install scikit-learn sentence-transformers scipy pyyaml matplotlib
pip freeze > requirements.txt
```

**Optional**: Install `anthropic` if you want to use Claude API for summarization:
```bash
pip install anthropic
```

## Output Files

For a chapter analysis, the following files are generated:

- `chapter_XX_sections.yaml` - Section hierarchy and metadata
- `chapter_XX_clusters.json` - Cluster assignments and metrics
- `chapter_XX_dendrogram.png` - Hierarchical clustering visualization
- `chapter_XX_coherence_report.md` - Final analysis report

**Optional** (if using summarization script):
- `chapter_XX_summaries.yaml` - AI-generated section summaries

## Success Metrics

- **Coverage**: 95%+ of content summarized
- **Cluster Coherence**: Average intra-cluster similarity > 0.75
- **Issue Detection**: Identify 5+ structural improvement opportunities
- **Actionability**: Generate specific, implementable recommendations

## Technical Details

### Embedding Methods

- **Primary**: sentence-transformers (all-MiniLM-L6-v2) - 384-dimensional embeddings
- **Fallback**: TF-IDF vectors - for environments without GPU/large models

### Clustering Algorithm

- Hierarchical agglomerative clustering
- Distance metric: Cosine similarity
- Linkage method: Average
- Optimal cluster count: Determined by silhouette score

### Coherence Scoring

- Intra-cluster similarity to centroid
- Range: 0.0 (low coherence) to 1.0 (perfect coherence)
- Thresholds:
  - 0.80+: Excellent
  - 0.70-0.79: Good
  - 0.60-0.69: Moderate
  - <0.60: Weak

## Future Enhancements

- Cross-chapter analysis for global patterns
- Interactive visualization dashboard
- Automated reorganization suggestions
- Content duplication detection across chapters
