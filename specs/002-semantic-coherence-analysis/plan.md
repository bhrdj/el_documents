# Implementation Plan: Semantic Coherence Analysis

**Feature**: 002-semantic-coherence-analysis
**Created**: 2025-11-06
**Status**: Implemented (retroactive documentation)

## Tech Stack

### Core Technologies
- **Python 3.x**: Primary language (using .venv virtual environment)
- **PyYAML**: YAML file I/O for section metadata and summaries
- **JSON**: Output format for cluster analysis results

### Machine Learning & NLP
- **scikit-learn**: Clustering algorithms (KMeans, AgglomerativeClustering), metrics (silhouette_score)
- **sentence-transformers**: Semantic embeddings (all-MiniLM-L6-v2 model, 384-dimensional)
- **PyTorch**: Backend for sentence-transformers (CPU-only mode)
- **scipy**: Hierarchical clustering (linkage, dendrogram), distance metrics (cosine)
- **numpy**: Array operations and numerical computing

### Visualization
- **matplotlib**: Dendrogram generation (using Agg backend for headless environments)

### Optional Dependencies
- **anthropic**: Claude API integration for enhanced summarization (optional, has fallback)

## Architecture

### Pipeline Overview

```
┌─────────────────┐
│  Markdown File  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│ Phase 1: Extract Sections   │
│ (01_extract_sections.py)    │
└────────┬────────────────────┘
         │ sections.yaml
         ▼
┌─────────────────────────────┐
│ Phase 2: Summarize (Optional)│
│ (02_summarize_sections.py)  │
└────────┬────────────────────┘
         │ summaries.yaml
         ▼
┌─────────────────────────────┐
│ Phase 3: Cluster Analysis   │
│ (03_cluster_analysis.py)    │
└────────┬────────────────────┘
         │ clusters.json + dendrogram.png
         ▼
┌─────────────────────────────┐
│ Phase 4: Generate Report    │
│ (04_generate_report.py)     │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────┐
│ Coherence Report│
└─────────────────┘
```

### Component Design

#### 1. Markdown Parser (`utils/markdown_parser.py`)
- **Responsibility**: Extract hierarchical section structure from markdown files
- **Key Classes**:
  - `Section`: Dataclass representing a markdown section with metadata
  - `MarkdownParser`: Parser for extracting sections from markdown
- **Methods**:
  - `parse()`: Extract all sections with hierarchy
  - `_generate_section_id()`: Create hierarchical IDs (e.g., "1.2.3")
  - `_find_parent_id()`: Establish parent-child relationships
  - `_build_subsection_tree()`: Build subsection lists

#### 2. Embedding Generator (`utils/embedding_generator.py`)
- **Responsibility**: Generate semantic embeddings with multiple backend support
- **Key Classes**:
  - `EmbeddingGenerator`: Unified interface for embeddings
- **Methods**:
  - `generate_embeddings()`: Convert texts to numeric vectors
  - `_generate_sentence_transformer()`: Use sentence-transformers
  - `_generate_tfidf()`: Fallback to TF-IDF
- **Backends**:
  - Primary: sentence-transformers (all-MiniLM-L6-v2, 384-dim)
  - Fallback: TF-IDF (configurable dimensions, defaults to 384)

#### 3. Section Extractor (`01_extract_sections.py`)
- **Input**: Markdown file
- **Output**: YAML file with section metadata
- **Key Functions**:
  - `extract_sections()`: Main extraction logic
  - `assess_completeness()`: Classify sections (complete/partial/orphaned)
  - `extract_age_groups()`: Identify mentioned age groups
  - `classify_content_type()`: Categorize content (activities/examples/theory/guidelines)

#### 4. Section Summarizer (`02_summarize_sections.py`)
- **Input**: Sections YAML + Markdown file
- **Output**: Summaries YAML
- **Key Functions**:
  - `summarize_sections()`: Main summarization loop
  - `summarize_with_claude()`: Use Claude API for high-quality summaries
  - `summarize_fallback()`: Extract first paragraph when API unavailable
- **Note**: This phase is optional; clustering can work directly on section content

#### 5. Cluster Analyzer (`03_cluster_analysis.py`)
- **Input**: Sections YAML + Markdown file
- **Output**: Clusters JSON + Dendrogram PNG
- **Key Functions**:
  - `cluster_analysis()`: Main analysis pipeline
  - `determine_optimal_clusters()`: Use silhouette score to find optimal k
  - `perform_clustering()`: Hierarchical agglomerative clustering
  - `calculate_cluster_metrics()`: Compute coherence scores and identify outliers
  - `extract_theme()`: Generate cluster theme from heading word frequency
  - `save_dendrogram()`: Create visualization

#### 6. Report Generator (`04_generate_report.py`)
- **Input**: Clusters JSON
- **Output**: Markdown report
- **Key Functions**:
  - `generate_report()`: Main report generation
  - `generate_executive_summary()`: High-level overview with key findings
  - `generate_cluster_details()`: Detailed cluster breakdowns
  - `generate_recommendations()`: Actionable improvement suggestions
  - `generate_appendix()`: Analysis metadata and statistics

## File Structure

```
scripts/04_analysis/
├── README.md                           # Usage documentation
├── 01_extract_sections.py              # Phase 1: Section extraction
├── 02_summarize_sections.py            # Phase 2: Summarization (optional)
├── 03_cluster_analysis.py              # Phase 3: Clustering
├── 04_generate_report.py               # Phase 4: Report generation
└── utils/
    ├── markdown_parser.py              # Section parsing utilities
    └── embedding_generator.py          # Embedding generation
```

## Data Models

### Section Metadata (YAML)
```yaml
source_file: "path/to/chapter.md"
total_sections: 42
sections:
  - section_id: "1.2.3"
    heading: "Activity Examples"
    level: 3
    line_range: [45, 78]
    line_count: 34
    token_estimate: 856
    parent_id: "1.2"
    subsections: ["1.2.3.1", "1.2.3.2"]
    age_groups_mentioned: ["toddler", "preschool"]
    content_type: ["activities", "examples"]
    completeness: "complete"
```

### Cluster Results (JSON)
```json
{
  "source_sections": "path/to/sections.yaml",
  "source_markdown": "path/to/chapter.md",
  "total_sections": 38,
  "num_clusters": 5,
  "embedding_method": "sentence-transformer",
  "embedding_dim": 384,
  "clusters": [
    {
      "cluster_id": 0,
      "size": 12,
      "theme": "Activity & Games",
      "coherence_score": 0.823,
      "sections": [
        {
          "section_id": "2.1",
          "heading": "Indoor Activities",
          "level": 2,
          "content_type": ["activities"],
          "age_groups": ["toddler"]
        }
      ],
      "outliers": [
        {
          "section_id": "2.8",
          "heading": "Safety Guidelines",
          "similarity_to_centroid": 0.512
        }
      ]
    }
  ]
}
```

### Coherence Report (Markdown)
```markdown
# Semantic Coherence Analysis Report

**Generated**: 2025-11-06 08:30:00
**Source**: path/to/chapter.md

## Executive Summary
- Total Sections Analyzed: 38
- Clusters Identified: 5
- Average Cluster Coherence: 0.756
- Total Outlier Sections: 3

### Key Findings
- Overall Coherence: GOOD
- Low Coherence Clusters: 1 cluster(s) show weak thematic unity
- Outlier Sections: 3 section(s) weakly connected to their clusters

## Cluster Analysis
[Detailed cluster breakdowns...]

## Recommendations
[Actionable improvement suggestions...]

## Appendix: Analysis Metadata
[Technical details and statistics...]
```

## Algorithms

### Optimal Cluster Detection
- **Method**: Silhouette score maximization
- **Range**: k = 2 to min(10, n_sections - 1)
- **Metric**: Average silhouette coefficient
- **Selection**: k with highest silhouette score

### Clustering Algorithm
- **Type**: Hierarchical Agglomerative Clustering
- **Distance Metric**: Cosine similarity
- **Linkage Method**: Average linkage
- **Determinism**: Fixed random seed (42) for reproducibility

### Coherence Scoring
- **Metric**: Mean cosine similarity of cluster members to centroid
- **Range**: 0.0 (random) to 1.0 (identical)
- **Thresholds**:
  - Excellent: ≥ 0.80
  - Good: 0.70-0.79
  - Moderate: 0.60-0.69
  - Weak: < 0.60

### Outlier Detection
- **Method**: Statistical threshold based on mean and standard deviation
- **Threshold**: similarity < (μ - σ)
- **Action**: Flag sections for review

## Configuration

### Embedding Configuration
- **Primary Model**: all-MiniLM-L6-v2 (384-dimensional)
- **Fallback**: TF-IDF with 384 max features
- **Text Preprocessing**: Handled by model/vectorizer

### Clustering Configuration
- **Min Clusters**: 2
- **Max Clusters**: 10
- **Section Filtering**: Minimum 50 characters to include
- **Section Levels**: Focus on levels 2-3 for major themes

### Visualization Configuration
- **Figure Size**: 15x10 inches
- **DPI**: 150
- **Label Length**: Section ID + first 30 chars of heading
- **Orientation**: Right (horizontal tree)

## Error Handling

### Graceful Degradation
1. **Missing sentence-transformers**: Automatic fallback to TF-IDF
2. **Missing Claude API key**: Use simple text extraction for summaries
3. **Too few sections**: Adjust cluster count automatically
4. **Empty sections**: Filter out during processing
5. **Missing files**: Clear error messages with exit code 1

### Validation
- Check file existence before processing
- Validate section content length before clustering
- Handle edge cases (very small/large clusters)
- Ensure output directories exist before writing

## Performance Considerations

### Memory Efficiency
- Load markdown file once, extract line ranges
- Process sections in batches for embedding generation
- Use sparse matrices where applicable (TF-IDF)

### Computation Efficiency
- Cache embeddings (no re-computation)
- Use CPU-optimized PyTorch settings
- Limit API calls with rate limiting (1 second between calls)

### Expected Performance
- **Small chapter** (20 sections): < 1 minute
- **Medium chapter** (50 sections): 2-5 minutes
- **Large chapter** (100 sections): 5-10 minutes
- **Note**: Excludes optional Claude API summarization time

## Dependencies Management

### Installation
```bash
source .venv/bin/activate
pip install scikit-learn sentence-transformers scipy pyyaml matplotlib torch
pip install anthropic  # Optional for summarization
pip freeze > requirements.txt
```

### Version Pinning
All dependencies are pinned in requirements.txt for reproducibility.

## Future Enhancements

1. **Cross-chapter analysis**: Compare coherence across multiple chapters
2. **Interactive dashboard**: Web-based visualization of clusters
3. **Automated reorganization**: Generate suggested section reorderings
4. **Content duplication detection**: Identify similar content across chapters
5. **Incremental updates**: Re-analyze only changed sections
6. **Custom embedding models**: Support for domain-specific transformers
