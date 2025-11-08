#!/usr/bin/env python3
"""
Fix heading depth in ch05_v03.md to prevent LaTeX rendering issues.

LaTeX can't properly handle headings deeper than 5 levels.
This script flattens 6-level headings to 4 levels maximum.
"""

import re
from pathlib import Path


def fix_heading_depth(content: str, max_depth: int = 4) -> str:
    """
    Reduce heading depth to max_depth levels.

    Converts:
    ###### Heading -> #### Heading (if max_depth=4)
    """
    lines = content.split('\n')
    fixed_lines = []

    for line in lines:
        # Match markdown headings
        match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if match:
            hashes = match.group(1)
            heading_text = match.group(2)
            current_depth = len(hashes)

            if current_depth > max_depth:
                # Reduce to max depth
                new_hashes = '#' * max_depth
                fixed_line = f"{new_hashes} {heading_text}"
                fixed_lines.append(fixed_line)
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)

    return '\n'.join(fixed_lines)


def main():
    """Main execution."""
    input_file = Path("/home/steven/git/el_documents/output/markdown/05_repaired/ch05_v03.md")
    output_file = Path("/home/steven/git/el_documents/output/markdown/05_repaired/ch05_v03_fixed.md")

    print("Fixing heading depth in ch05_v03.md...")
    print(f"Input: {input_file}")

    # Read content
    content = input_file.read_text()

    # Check current depth
    max_depth_found = 0
    for line in content.split('\n'):
        match = re.match(r'^(#{1,6})\s', line)
        if match:
            depth = len(match.group(1))
            if depth > max_depth_found:
                max_depth_found = depth

    print(f"Current max heading depth: {max_depth_found}")

    # Fix heading depth
    fixed_content = fix_heading_depth(content, max_depth=4)

    # Check new depth
    max_depth_new = 0
    for line in fixed_content.split('\n'):
        match = re.match(r'^(#{1,6})\s', line)
        if match:
            depth = len(match.group(1))
            if depth > max_depth_new:
                max_depth_new = depth

    print(f"New max heading depth: {max_depth_new}")

    # Save
    output_file.write_text(fixed_content)
    print(f"\n✓ Fixed version saved to: {output_file}")

    # Count changes
    original_lines = content.split('\n')
    fixed_lines = fixed_content.split('\n')
    changes = sum(1 for o, f in zip(original_lines, fixed_lines) if o != f)
    print(f"Modified {changes} heading lines")


if __name__ == "__main__":
    main()
