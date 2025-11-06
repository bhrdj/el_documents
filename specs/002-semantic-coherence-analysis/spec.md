# Feature Specification: Semantic Coherence Analysis

**Feature Branch**: `002-semantic-coherence-analysis`
**Created**: 2025-11-06
**Status**: Implemented (retroactive documentation)

## Overview

Transformer-inspired ML clustering analysis to assess logical structure and semantic coherence of large document chapters, identifying thematic patterns, structural issues, and organizational opportunities.

## User Scenarios & Testing

### User Story 1 - Analyze Chapter Structure (Priority: P1)

As a document editor, I want to analyze a chapter's semantic coherence so that I can identify structural issues and reorganization opportunities in large, complex chapters.

**Why this priority**: This is the core value proposition - understanding the thematic organization of complex documents to improve readability and coherence.

**Independent Test**: Can be fully tested by running the analysis pipeline on any markdown chapter and verifying that coherence metrics are calculated and visualizations are generated.

**Acceptance Scenarios**:

1. **Given** a markdown chapter file, **When** I run the section extraction script, **Then** section hierarchy with metadata (completeness, content type, age groups) is extracted and saved to YAML
2. **Given** a sections YAML file and markdown source, **When** I run the clustering analysis, **Then** sections are grouped by semantic similarity with coherence scores calculated
3. **Given** cluster analysis results, **When** I generate the report, **Then** I receive actionable recommendations for improving document organization

---

### User Story 2 - Identify Structural Issues (Priority: P2)

As a document editor, I want to identify outlier sections and low-coherence clusters so that I can prioritize which sections need reorganization or clarification.

**Why this priority**: Helps editors focus effort on the most problematic sections rather than reviewing the entire document.

**Independent Test**: Can be tested by analyzing a known problematic chapter and verifying that outlier sections are correctly identified.

**Acceptance Scenarios**:

1. **Given** clustering results, **When** outlier sections are identified, **Then** sections weakly connected to their cluster theme are flagged with similarity scores
2. **Given** cluster coherence scores, **When** low-coherence clusters are found (< 0.70), **Then** specific reorganization recommendations are provided
3. **Given** cluster sizes, **When** very large or very small clusters exist, **Then** recommendations to split or merge are generated

---

### User Story 3 - Visualize Thematic Relationships (Priority: P3)

As a document editor, I want to see dendrogram visualizations of section relationships so that I can understand hierarchical thematic patterns at a glance.

**Why this priority**: Visual representations help quickly communicate findings to stakeholders and identify patterns not obvious in tabular data.

**Independent Test**: Can be tested by verifying that dendrogram PNG files are generated with proper labels and structure.

**Acceptance Scenarios**:

1. **Given** clustering results, **When** dendrogram is generated, **Then** a hierarchical clustering visualization is saved as PNG with section IDs and headings as labels
2. **Given** the dendrogram, **When** reviewing section relationships, **Then** thematically similar sections appear close together in the tree structure

---

### Edge Cases

- What happens when a chapter has very few sections (< 5)? → Minimum cluster count adjusted automatically
- What happens when sections have very little content? → Sections with < 50 characters are filtered out during clustering
- How does the system handle chapters without clear thematic groupings? → Reports low coherence scores and recommends clarification
- What happens if sentence-transformers library is not available? → Automatic fallback to TF-IDF embeddings
- What happens if Claude API key is not available for summarization? → Fallback to simple text extraction

## Requirements

### Functional Requirements

- **FR-001**: System MUST extract markdown section hierarchy with heading levels, line ranges, and content
- **FR-002**: System MUST assess section completeness (complete, partial, orphaned) based on content analysis
- **FR-003**: System MUST identify age groups mentioned in sections (infants, toddlers, preschool, school-age)
- **FR-004**: System MUST classify content types (activities, examples, theory, guidelines, procedures)
- **FR-005**: System MUST generate semantic embeddings for section content using sentence-transformers or TF-IDF fallback
- **FR-006**: System MUST perform hierarchical agglomerative clustering with optimal cluster count determination
- **FR-007**: System MUST calculate cluster coherence scores based on intra-cluster similarity
- **FR-008**: System MUST identify outlier sections within each cluster
- **FR-009**: System MUST generate dendrogram visualizations showing hierarchical relationships
- **FR-010**: System MUST produce human-readable reports with executive summary, detailed cluster analysis, and recommendations
- **FR-011**: System MUST work without external APIs (self-contained clustering on section content)
- **FR-012**: System MAY use Claude API for enhanced summarization when API key is available

### Key Entities

- **Section**: Markdown section with ID, heading, level, line range, content, parent relationship, metadata (completeness, content type, age groups)
- **Cluster**: Group of semantically similar sections with theme, coherence score, member sections, and outliers
- **Embedding**: Numeric vector representation of section content (384-dimensional for sentence-transformers, configurable for TF-IDF)
- **Report**: Analysis document with executive summary, cluster details, recommendations, and metadata

## Success Criteria

### Measurable Outcomes

- **SC-001**: Coverage: 95%+ of section content processed and clustered (excluding very short sections < 50 chars)
- **SC-002**: Cluster Coherence: Average intra-cluster similarity > 0.75 for well-organized documents
- **SC-003**: Issue Detection: Identify and report outlier sections and low-coherence clusters
- **SC-004**: Actionability: Generate specific, implementable recommendations for each identified issue
- **SC-005**: Performance: Complete analysis of a 50-section chapter in under 5 minutes (excluding optional API summarization)
- **SC-006**: Visualization: Generate clear dendrogram with readable section labels
- **SC-007**: Robustness: Graceful fallback when optional dependencies (sentence-transformers, Claude API) are unavailable

## Technical Constraints

- **TC-001**: Must work with CPU-only environments (no GPU requirement)
- **TC-002**: Must handle chapters with variable section counts (2-100+ sections)
- **TC-003**: Must produce deterministic results (fixed random seed for clustering)
- **TC-004**: Must preserve section hierarchy information throughout pipeline
- **TC-005**: Must use virtual environment (.venv) for all Python dependencies
