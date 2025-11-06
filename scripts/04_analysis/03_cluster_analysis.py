#!/usr/bin/env python3
"""
Phase 2: Perform semantic clustering analysis on sections.

Usage:
    .venv/bin/python scripts/04_analysis/03_cluster_analysis.py <sections_yaml> <markdown_file> [output_file]

Example:
    .venv/bin/python scripts/04_analysis/03_cluster_analysis.py \
        output/chapters/04_merged/chapter_05_sections.yaml \
        output/chapters/04_merged/chapter_05_deduplicated.md \
        output/chapters/04_merged/chapter_05_clusters.json
"""

import sys
import os
from pathlib import Path
import yaml
import json
import numpy as np
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import cosine
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from utils.embedding_generator import EmbeddingGenerator


def determine_optimal_clusters(embeddings: np.ndarray, min_k=2, max_k=10) -> int:
    """Use elbow method to determine optimal number of clusters."""
    if len(embeddings) < max_k:
        max_k = max(2, len(embeddings) - 1)

    if len(embeddings) < min_k:
        return min(2, len(embeddings))

    silhouette_scores = []
    k_range = range(min_k, min(max_k + 1, len(embeddings)))

    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(embeddings)
        score = silhouette_score(embeddings, labels)
        silhouette_scores.append(score)

    # Find k with highest silhouette score
    optimal_k = k_range[np.argmax(silhouette_scores)]

    print(f"Optimal cluster count: {optimal_k} (silhouette score: {max(silhouette_scores):.3f})")

    return optimal_k


def perform_clustering(embeddings: np.ndarray, n_clusters: int) -> tuple:
    """
    Perform hierarchical clustering.

    Returns:
        labels, linkage_matrix
    """
    # Hierarchical clustering
    clustering = AgglomerativeClustering(
        n_clusters=n_clusters,
        metric='cosine',
        linkage='average'
    )

    labels = clustering.fit_predict(embeddings)

    # Generate linkage matrix for dendrogram
    linkage_matrix = linkage(embeddings, method='average', metric='cosine')

    return labels, linkage_matrix


def calculate_cluster_metrics(embeddings: np.ndarray, labels: np.ndarray,
                              summaries: list) -> list:
    """Calculate metrics for each cluster."""
    unique_labels = np.unique(labels)
    cluster_data = []

    for cluster_id in unique_labels:
        cluster_mask = labels == cluster_id
        cluster_embeddings = embeddings[cluster_mask]
        cluster_summaries = [s for i, s in enumerate(summaries) if cluster_mask[i]]

        # Calculate centroid
        centroid = cluster_embeddings.mean(axis=0)

        # Calculate coherence (intra-cluster similarity)
        similarities = []
        for emb in cluster_embeddings:
            sim = 1 - cosine(emb, centroid)
            similarities.append(sim)

        coherence_score = np.mean(similarities)

        # Identify outliers (sections far from centroid)
        threshold = np.mean(similarities) - np.std(similarities)
        outliers = []

        for i, (sim, summary) in enumerate(zip(similarities, cluster_summaries)):
            if sim < threshold:
                outliers.append({
                    'section_id': summary['section_id'],
                    'heading': summary['heading'],
                    'similarity_to_centroid': float(sim)
                })

        # Extract common themes from headings
        headings = [s['heading'] for s in cluster_summaries]
        theme = extract_theme(headings)

        cluster_info = {
            'cluster_id': int(cluster_id),
            'size': int(cluster_mask.sum()),
            'theme': theme,
            'coherence_score': float(coherence_score),
            'sections': [
                {
                    'section_id': s['section_id'],
                    'heading': s['heading'],
                    'level': s['level'],
                    'content_type': s.get('content_type', []),
                    'age_groups': s.get('age_groups_mentioned', [])
                }
                for s in cluster_summaries
            ],
            'outliers': outliers
        }

        cluster_data.append(cluster_info)

    # Sort by cluster size
    cluster_data.sort(key=lambda x: x['size'], reverse=True)

    return cluster_data


def extract_theme(headings: list) -> str:
    """Extract common theme from a list of headings."""
    # Simple word frequency analysis
    from collections import Counter

    # Tokenize and count words
    words = []
    for heading in headings:
        # Remove common words
        tokens = heading.lower().split()
        tokens = [w for w in tokens if len(w) > 3 and w not in
                 ['with', 'this', 'that', 'from', 'have', 'will', 'when', 'what']]
        words.extend(tokens)

    if not words:
        return "General content"

    # Get most common words
    word_counts = Counter(words)
    common_words = [w for w, c in word_counts.most_common(3)]

    return " & ".join(common_words).title()


def save_dendrogram(linkage_matrix: np.ndarray, output_path: str, summaries: list):
    """Save dendrogram visualization."""
    plt.figure(figsize=(15, 10))

    # Create labels from section IDs
    labels = [f"{s['section_id']}: {s['heading'][:30]}..." for s in summaries]

    dendrogram(
        linkage_matrix,
        labels=labels,
        orientation='right',
        leaf_font_size=8
    )

    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('Distance (Cosine)')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"Saved dendrogram to: {output_path}")


def load_section_content(markdown_file: str, line_start: int, line_end: int) -> str:
    """Load section content from markdown file."""
    with open(markdown_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Convert from 1-indexed to 0-indexed
    content_lines = lines[line_start - 1:line_end]
    content = ''.join(content_lines)

    # Remove the heading line and extract just the content
    lines_list = content.split('\n')
    content_lines = [l for l in lines_list if not l.strip().startswith('#')]

    return '\n'.join(content_lines).strip()


def cluster_analysis(sections_yaml: str, markdown_file: str, output_file: str = None):
    """Perform clustering analysis on section content."""

    # Load sections
    if not os.path.exists(sections_yaml):
        print(f"Error: Sections file not found: {sections_yaml}")
        sys.exit(1)

    if not os.path.exists(markdown_file):
        print(f"Error: Markdown file not found: {markdown_file}")
        sys.exit(1)

    with open(sections_yaml, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    all_sections = data['sections']

    # Focus on major sections (level 2-3) for clustering
    sections = [s for s in all_sections if 2 <= s['level'] <= 3]
    print(f"Loaded {len(sections)} major sections (levels 2-3) from {sections_yaml}")

    # Load content for each section
    print("\nLoading section content...")
    texts = []
    valid_sections = []

    for section in sections:
        content = load_section_content(
            markdown_file,
            section['line_range'][0],
            section['line_range'][1]
        )

        # Skip empty sections
        if content and len(content) > 50:
            texts.append(content)
            valid_sections.append(section)

    print(f"Processing {len(valid_sections)} sections with content")

    # Generate embeddings
    print("\nGenerating embeddings...")
    generator = EmbeddingGenerator(method='sentence-transformer')
    embeddings = generator.generate_embeddings(texts)

    print(f"Generated embeddings: {embeddings.shape}")

    # Determine optimal cluster count
    print("\nDetermining optimal cluster count...")
    n_clusters = determine_optimal_clusters(embeddings)

    # Perform clustering
    print(f"\nPerforming clustering with {n_clusters} clusters...")
    labels, linkage_matrix = perform_clustering(embeddings, n_clusters)

    # Calculate cluster metrics
    print("\nCalculating cluster metrics...")
    cluster_data = calculate_cluster_metrics(embeddings, labels, valid_sections)

    # Prepare output
    results = {
        'source_sections': sections_yaml,
        'source_markdown': markdown_file,
        'total_sections': len(valid_sections),
        'num_clusters': n_clusters,
        'embedding_method': generator.method,
        'embedding_dim': int(generator.embedding_dim),
        'clusters': cluster_data
    }

    # Generate output filename if not provided
    if not output_file:
        input_path = Path(sections_yaml)
        output_file = str(input_path.parent / f"{input_path.stem.replace('_sections', '')}_clusters.json")

    # Save results
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nSaved cluster analysis to: {output_file}")

    # Save dendrogram
    dendrogram_path = str(output_path.parent / f"{output_path.stem}_dendrogram.png")
    save_dendrogram(linkage_matrix, dendrogram_path, valid_sections)

    # Print cluster summary
    print("\n--- Cluster Summary ---")
    for cluster in cluster_data:
        print(f"\nCluster {cluster['cluster_id']}: {cluster['theme']}")
        print(f"  Size: {cluster['size']} sections")
        print(f"  Coherence: {cluster['coherence_score']:.3f}")
        print(f"  Outliers: {len(cluster['outliers'])}")

        print("  Sections:")
        for section in cluster['sections'][:5]:
            print(f"    - {section['section_id']}: {section['heading']}")

        if len(cluster['sections']) > 5:
            print(f"    ... and {len(cluster['sections']) - 5} more")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    sections_yaml = sys.argv[1]
    markdown_file = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else None

    cluster_analysis(sections_yaml, markdown_file, output_file)
