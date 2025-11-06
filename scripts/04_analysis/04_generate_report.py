#!/usr/bin/env python3
"""
Phase 3: Generate human-readable coherence analysis report.

Usage:
    .venv/bin/python scripts/04_analysis/04_generate_report.py <clusters_json> [output_file]

Example:
    .venv/bin/python scripts/04_analysis/04_generate_report.py \
        output/chapters/04_merged/chapter_05_clusters.json \
        output/chapters/04_merged/chapter_05_coherence_report.md
"""

import sys
import os
from pathlib import Path
import json
from datetime import datetime


def generate_executive_summary(data: dict) -> str:
    """Generate executive summary section."""
    total_sections = data['total_sections']
    num_clusters = data['num_clusters']
    clusters = data['clusters']

    # Calculate overall coherence
    avg_coherence = sum(c['coherence_score'] for c in clusters) / len(clusters)

    # Count outliers
    total_outliers = sum(len(c['outliers']) for c in clusters)

    # Identify issues
    low_coherence_clusters = [c for c in clusters if c['coherence_score'] < 0.70]
    high_outlier_clusters = [c for c in clusters if len(c['outliers']) > 0]

    summary = f"""## Executive Summary

- **Total Sections Analyzed**: {total_sections}
- **Clusters Identified**: {num_clusters}
- **Average Cluster Coherence**: {avg_coherence:.3f}
- **Total Outlier Sections**: {total_outliers}

### Key Findings

"""

    if avg_coherence >= 0.75:
        summary += "- **Overall Coherence**: GOOD - Content is well-organized with clear thematic groupings\n"
    elif avg_coherence >= 0.65:
        summary += "- **Overall Coherence**: MODERATE - Some organizational improvements possible\n"
    else:
        summary += "- **Overall Coherence**: NEEDS IMPROVEMENT - Significant reorganization recommended\n"

    if low_coherence_clusters:
        summary += f"- **Low Coherence Clusters**: {len(low_coherence_clusters)} cluster(s) show weak thematic unity\n"

    if total_outliers > 0:
        summary += f"- **Outlier Sections**: {total_outliers} section(s) weakly connected to their clusters\n"

    return summary


def generate_cluster_details(clusters: list) -> str:
    """Generate detailed cluster analysis."""
    output = "## Cluster Analysis\n\n"

    for cluster in clusters:
        cid = cluster['cluster_id']
        theme = cluster['theme']
        size = cluster['size']
        coherence = cluster['coherence_score']
        sections = cluster['sections']
        outliers = cluster['outliers']

        # Coherence indicator
        if coherence >= 0.80:
            coherence_label = "EXCELLENT"
        elif coherence >= 0.70:
            coherence_label = "GOOD"
        elif coherence >= 0.60:
            coherence_label = "MODERATE"
        else:
            coherence_label = "WEAK"

        output += f"### Cluster {cid}: {theme}\n\n"
        output += f"- **Size**: {size} sections\n"
        output += f"- **Coherence**: {coherence:.3f} ({coherence_label})\n"

        if outliers:
            output += f"- **Outliers**: {len(outliers)} section(s)\n"

        output += "\n**Sections in this cluster:**\n\n"

        for section in sections:
            sid = section['section_id']
            heading = section['heading']
            level = section['level']
            content_type = section.get('content_type', [])
            age_groups = section.get('age_groups', [])

            output += f"- `{sid}` (Level {level}): **{heading}**\n"

            if content_type:
                output += f"  - Content type: {', '.join(content_type)}\n"

            if age_groups:
                output += f"  - Age groups: {', '.join(age_groups)}\n"

        if outliers:
            output += "\n**Outlier sections** (weakly connected to cluster theme):\n\n"
            for outlier in outliers:
                sid = outlier['section_id']
                heading = outlier['heading']
                sim = outlier['similarity_to_centroid']
                output += f"- `{sid}`: {heading} (similarity: {sim:.3f})\n"

        output += "\n---\n\n"

    return output


def generate_recommendations(data: dict) -> str:
    """Generate improvement recommendations."""
    clusters = data['clusters']

    output = "## Recommendations\n\n"

    # Identify specific issues

    # 1. Low coherence clusters
    low_coherence = [c for c in clusters if c['coherence_score'] < 0.70]

    if low_coherence:
        output += "### 1. Address Low-Coherence Clusters\n\n"
        output += "The following clusters show weak thematic unity and may benefit from reorganization:\n\n"

        for cluster in low_coherence:
            cid = cluster['cluster_id']
            theme = cluster['theme']
            coherence = cluster['coherence_score']

            output += f"**Cluster {cid}: {theme}** (coherence: {coherence:.3f})\n\n"
            output += "Recommendations:\n"
            output += "- Review sections for thematic consistency\n"
            output += "- Consider splitting into multiple focused subsections\n"
            output += "- Add clearer transitions between topics\n\n"

    # 2. Outlier sections
    outlier_sections = []
    for cluster in clusters:
        for outlier in cluster['outliers']:
            outlier_sections.append({
                'cluster_id': cluster['cluster_id'],
                'cluster_theme': cluster['theme'],
                **outlier
            })

    if outlier_sections:
        output += "### 2. Review Outlier Sections\n\n"
        output += "These sections are weakly connected to their cluster themes:\n\n"

        for outlier in outlier_sections[:10]:  # Show top 10
            sid = outlier['section_id']
            heading = outlier['heading']
            cluster_theme = outlier['cluster_theme']

            output += f"- `{sid}`: **{heading}**\n"
            output += f"  - Currently in cluster: {cluster_theme}\n"
            output += f"  - **Action**: Review placement, may belong elsewhere or need content clarification\n\n"

        if len(outlier_sections) > 10:
            output += f"*...and {len(outlier_sections) - 10} more outliers*\n\n"

    # 3. Structural improvements
    output += "### 3. Structural Improvements\n\n"

    # Check for very large clusters
    large_clusters = [c for c in clusters if c['size'] > 10]

    if large_clusters:
        output += "**Large Clusters**:\n\n"
        for cluster in large_clusters:
            output += f"- Cluster {cluster['cluster_id']} ({cluster['theme']}) has {cluster['size']} sections\n"
            output += "  - Consider breaking into smaller, more focused subsections\n\n"

    # Check for very small clusters
    small_clusters = [c for c in clusters if c['size'] < 3]

    if small_clusters:
        output += "**Small Clusters**:\n\n"
        for cluster in small_clusters:
            output += f"- Cluster {cluster['cluster_id']} ({cluster['theme']}) has only {cluster['size']} section(s)\n"
            output += "  - Consider merging with related clusters\n\n"

    # General recommendations
    output += "### 4. General Recommendations\n\n"
    output += "1. **Improve Transitions**: Add bridging content between major sections\n"
    output += "2. **Consistent Structure**: Ensure parallel structure across similar section types\n"
    output += "3. **Clear Headings**: Review headings to ensure they accurately reflect content\n"
    output += "4. **Content Completeness**: Address any orphaned or incomplete sections\n\n"

    return output


def generate_appendix(data: dict) -> str:
    """Generate appendix with metadata."""
    output = "## Appendix: Analysis Metadata\n\n"
    output += f"- **Source Sections**: {data.get('source_sections', data.get('source_summaries', 'N/A'))}\n"
    output += f"- **Source Markdown**: {data.get('source_markdown', 'N/A')}\n"
    output += f"- **Embedding Method**: {data['embedding_method']}\n"
    output += f"- **Embedding Dimensions**: {data['embedding_dim']}\n"
    output += f"- **Number of Clusters**: {data['num_clusters']}\n"
    output += f"- **Total Sections**: {data['total_sections']}\n\n"

    output += "### Cluster Statistics\n\n"
    output += "| Cluster | Theme | Size | Coherence | Outliers |\n"
    output += "|---------|-------|------|-----------|----------|\n"

    for cluster in data['clusters']:
        cid = cluster['cluster_id']
        theme = cluster['theme'][:30]
        size = cluster['size']
        coherence = cluster['coherence_score']
        outliers = len(cluster['outliers'])

        output += f"| {cid} | {theme} | {size} | {coherence:.3f} | {outliers} |\n"

    output += "\n"

    return output


def generate_report(clusters_json: str, output_file: str = None):
    """Generate coherence analysis report."""

    # Load cluster data
    if not os.path.exists(clusters_json):
        print(f"Error: Clusters file not found: {clusters_json}")
        sys.exit(1)

    with open(clusters_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Loaded cluster data from {clusters_json}")

    # Generate report sections
    source_file = data.get('source_markdown', data.get('source_summaries', 'N/A'))
    report = f"""# Semantic Coherence Analysis Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Source**: {source_file}

---

"""

    report += generate_executive_summary(data)
    report += "\n---\n\n"
    report += generate_cluster_details(data['clusters'])
    report += "---\n\n"
    report += generate_recommendations(data)
    report += "---\n\n"
    report += generate_appendix(data)

    # Generate output filename if not provided
    if not output_file:
        input_path = Path(clusters_json)
        output_file = str(input_path.parent / f"{input_path.stem.replace('_clusters', '')}_coherence_report.md")

    # Save report
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\nGenerated coherence report: {output_file}")
    print(f"Report length: {len(report)} characters")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    clusters_json = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    generate_report(clusters_json, output_file)
