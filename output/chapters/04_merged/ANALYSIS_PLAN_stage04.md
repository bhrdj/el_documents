# Stage 04: Transformer-Inspired Coherence Analysis

**Purpose**: Assess logical structure and semantic coherence of large chapters using ML-based clustering analysis inspired by transformer attention mechanisms.

**Status**: Planning phase

---

## Conceptual Framework

This analysis mimics transformer architecture layers:
- **Attention Layer**: Summarize local context windows (major sections)
- **Semantic Encoding**: Convert summaries to embeddings for clustering
- **Cross-Attention**: Review clusters to identify relationships and confusion points

---

## Three-Phase Analysis Plan

### Phase 1: Local Context Summarization (Attention)

**Objective**: Create digestible summaries of major sections whose total content fits within a manageable window.

**Process**:
1. **Extract Section Hierarchy**
   - Parse markdown to identify all heading levels (##, ###, ####, etc.)
   - Calculate line ranges and token estimates for each section
   - Identify "summarizable units" (sections fitting within ~3000 token windows)

2. **Generate Section Summaries**
   - For each major section (typically ## or ### level):
     - Read the complete section content
     - Generate structured summary capturing:
       - Main topic/purpose
       - Key activities or concepts described
       - Target age groups (if applicable)
       - Subsection count and types
       - Completeness indicators (trailing content, orphaned headings)

3. **Output Format**
   - JSON/YAML file with structure:
     ```yaml
     section_id: "5.1.1"
     heading: "Examples of big group activities"
     line_range: [15, 42]
     summary: "..."
     subsections: [...]
     age_groups_mentioned: [...]
     content_type: ["activities", "games"]
     completeness: "complete" | "partial" | "orphaned"
     ```

### Phase 2: Semantic Clustering Analysis (Pattern Recognition)

**Objective**: Use ML clustering to group semantically similar sections, revealing structural patterns and potential issues.

**Process**:
1. **Embedding Generation**
   - Convert section summaries to semantic embeddings
   - Options:
     - Use Claude API with embedding model
     - Use sentence-transformers (e.g., `all-MiniLM-L6-v2`)
     - Simple TF-IDF vectors as baseline

2. **Clustering Algorithm**
   - Apply hierarchical clustering or K-means
   - Parameters:
     - Distance metric: cosine similarity
     - Initial cluster count: sqrt(num_sections) or elbow method
   - Generate dendrogram for hierarchical relationships

3. **Cluster Analysis Output**
   - For each cluster, identify:
     - Common themes/topics
     - Section IDs grouped together
     - Coherence score (intra-cluster similarity)
     - Outliers (sections weakly connected to cluster)

4. **Output Format**
   ```yaml
   cluster_id: 1
   theme: "Motor skills games for infants"
   sections: ["5.10.7.1.1", "5.10.7.2.1", ...]
   coherence_score: 0.87
   outliers: []
   ```

### Phase 3: Cross-Attention Review (Coherence Validation)

**Objective**: Human-in-the-loop review of clusters to identify logical issues.

**Process**:
1. **Cluster-by-Cluster Review**
   - For each cluster:
     - Read all section summaries in the cluster together
     - Assess: Do these sections logically belong together?
     - Identify:
       - Well-grouped sections (expected clustering)
       - Misplaced sections (should be in different cluster)
       - Duplicate content (similar sections that should be merged)
       - Missing transitions (gaps in logical flow)

2. **Confusion Detection Patterns**
   - **Type A: Unexpected Grouping**
     - Sections from different major topics clustered together
     - Indicates: Possible content duplication or mislabeling

   - **Type B: Expected Separation**
     - Related sections in different clusters
     - Indicates: Possible structural fragmentation

   - **Type C: Outlier Sections**
     - Sections weakly connected to any cluster
     - Indicates: Orphaned content or unique/incomplete sections

3. **Structural Issue Report**
   - Generate findings document with:
     - Coherence score by major section
     - List of problematic clusters with recommendations
     - Suggested reorganization or merges
     - Orphaned/incomplete sections flagged

---

## Implementation Roadmap

### Step 1: Chapter 5 Pilot (Current Focus)
- **Input**: `output/chapters/04_merged/chapter_05_deduplicated.md`
- **Output**:
  - `chapter_05_section_summaries.yaml`
  - `chapter_05_clusters.json`
  - `chapter_05_coherence_report.md`

### Step 2: Chapter 4 Analysis
- Apply same process to chapter 4
- Compare clustering patterns between chapters
- Refine analysis parameters based on Chapter 5 learnings

### Step 3: Cross-Chapter Analysis
- **Input**: All deduplicated chapters (0-9)
- **Process**:
  - Generate summaries for all chapters
  - Perform clustering across entire document set
  - Identify:
    - Cross-chapter content duplication
    - Inconsistent terminology or structure
    - Global organizational issues
- **Output**:
  - `all_chapters_coherence_report.md`
  - Recommendations for global restructuring

---

## Technical Requirements

### Python Dependencies
```python
# requirements additions
scikit-learn>=1.3.0
sentence-transformers>=2.2.0  # for embeddings
scipy>=1.11.0  # for clustering
pyyaml>=6.0  # for structured output
matplotlib>=3.7.0  # for visualization
```

### Script Structure
```
scripts/
  analysis_stage04/
    01_extract_sections.py      # Parse MD, extract section hierarchy
    02_summarize_sections.py    # Generate summaries using Claude API
    03_cluster_analysis.py      # ML clustering with embeddings
    04_generate_report.py       # Human-readable coherence report
    utils/
      markdown_parser.py
      embedding_generator.py
      cluster_visualizer.py
```

---

## Success Metrics

1. **Coverage**: All major sections summarized (target: 95%+ of content)
2. **Cluster Coherence**: Average intra-cluster similarity > 0.75
3. **Issue Detection**: Identify 5+ structural improvement opportunities
4. **Actionability**: Generate specific, implementable recommendations

---

## Timeline

- **Phase 1 (Chapter 5)**: 2-3 hours
- **Phase 2 (Chapter 4)**: 1-2 hours (process refinement)
- **Phase 3 (All Chapters)**: 3-4 hours
- **Total Estimated**: 6-9 hours of processing + review time

---

**Status**: Ready to begin Phase 1 with Chapter 5
**Next Action**: Create section extraction script
