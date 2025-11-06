#!/usr/bin/env python3
"""
Generate PDFs from markdown files using weasyprint (supports Unicode/emojis).
"""

import sys
from pathlib import Path
import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

def markdown_to_html(markdown_content, title="Document"):
    """Convert markdown to HTML with proper styling."""

    # Convert markdown to HTML
    md = markdown.Markdown(extensions=[
        'tables',
        'fenced_code',
        'nl2br',
        'sane_lists',
        'toc',
    ])

    body_html = md.convert(markdown_content)

    # Wrap in full HTML document with CSS
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        @page {{
            size: letter;
            margin: 1in;
            @bottom-center {{
                content: counter(page);
            }}
        }}

        body {{
            font-family: "DejaVu Sans", "Noto Color Emoji", sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #333;
        }}

        h1 {{
            font-size: 24pt;
            margin-top: 20pt;
            margin-bottom: 12pt;
            page-break-before: always;
        }}

        h1:first-of-type {{
            page-break-before: avoid;
        }}

        h2 {{
            font-size: 18pt;
            margin-top: 16pt;
            margin-bottom: 10pt;
        }}

        h3 {{
            font-size: 14pt;
            margin-top: 12pt;
            margin-bottom: 8pt;
        }}

        h4 {{
            font-size: 12pt;
            margin-top: 10pt;
            margin-bottom: 6pt;
        }}

        h5, h6 {{
            font-size: 11pt;
            margin-top: 8pt;
            margin-bottom: 4pt;
        }}

        p {{
            margin-bottom: 8pt;
            text-align: justify;
        }}

        ul, ol {{
            margin-bottom: 8pt;
        }}

        li {{
            margin-bottom: 4pt;
        }}

        code {{
            background-color: #f5f5f5;
            padding: 2pt 4pt;
            font-family: monospace;
            font-size: 10pt;
        }}

        pre {{
            background-color: #f5f5f5;
            padding: 8pt;
            margin-bottom: 8pt;
            overflow-x: auto;
        }}

        pre code {{
            padding: 0;
        }}

        table {{
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 12pt;
        }}

        th, td {{
            border: 1pt solid #ddd;
            padding: 6pt;
            text-align: left;
        }}

        th {{
            background-color: #f5f5f5;
            font-weight: bold;
        }}

        blockquote {{
            border-left: 3pt solid #ddd;
            padding-left: 12pt;
            margin-left: 0;
            color: #666;
        }}

        strong {{
            font-weight: bold;
        }}

        em {{
            font-style: italic;
        }}

        a {{
            color: #0066cc;
            text-decoration: none;
        }}

        .toc {{
            background-color: #f9f9f9;
            padding: 12pt;
            margin-bottom: 20pt;
            border: 1pt solid #ddd;
        }}
    </style>
</head>
<body>
{body_html}
</body>
</html>
"""
    return html


def generate_pdf(input_file, output_file):
    """Generate PDF from markdown file using weasyprint."""

    input_path = Path(input_file)
    output_path = Path(output_file)

    if not input_path.exists():
        print(f"Error: Input file not found: {input_file}")
        return False

    try:
        # Read markdown
        markdown_content = input_path.read_text(encoding='utf-8')

        # Convert to HTML
        title = input_path.stem.replace('_', ' ').title()
        html_content = markdown_to_html(markdown_content, title)

        # Configure fonts for emoji support
        font_config = FontConfiguration()

        # Generate PDF
        html = HTML(string=html_content)
        html.write_pdf(
            output_path,
            font_config=font_config
        )

        print(f"✓ Generated: {output_path.name}")
        return True

    except Exception as e:
        print(f"Error generating PDF for {input_file}:")
        print(f"  {e}")
        return False


def main():
    # Define latest version of each chapter
    # Using repaired chapters (05_repaired) for chapters 1, 4, 5
    chapters = [
        ('output/chapters/03_edited/chapter_00.md', 'output/pdfs/chapter_00.pdf'),
        ('output/chapters/05_repaired/chapter_01_fixed.md', 'output/pdfs/chapter_01.pdf'),
        ('output/chapters/02_removedbullets/chapter_02.md', 'output/pdfs/chapter_02.pdf'),
        ('output/chapters/02_removedbullets/chapter_03.md', 'output/pdfs/chapter_03.pdf'),
        ('output/chapters/05_repaired/chapter_04_fixed.md', 'output/pdfs/chapter_04.pdf'),
        ('output/chapters/05_repaired/chapter_05.md', 'output/pdfs/chapter_05.pdf'),
        ('output/chapters/03_edited/chapter_07.md', 'output/pdfs/chapter_07.pdf'),
        ('output/chapters/03_edited/chapter_08.md', 'output/pdfs/chapter_08.pdf'),
        ('output/chapters/02_removedbullets/chapter_09.md', 'output/pdfs/chapter_09.pdf'),
    ]

    print("Generating PDFs for all chapters using weasyprint...\n")

    success_count = 0
    fail_count = 0

    for input_file, output_file in chapters:
        if generate_pdf(input_file, output_file):
            success_count += 1
        else:
            fail_count += 1

    print(f"\n{'='*50}")
    print(f"PDF Generation Complete")
    print(f"{'='*50}")
    print(f"Successfully generated: {success_count}")
    print(f"Failed: {fail_count}")
    print(f"\nPDFs are in: output/pdfs/")


if __name__ == '__main__':
    main()
