# System Setup

System-level dependencies required for the el_documents project.

## Document Conversion Tools

### Pandoc

**Purpose:** Convert markdown files to PDF and other formats.

**Installation:**
```bash
sudo apt update
sudo apt install -y pandoc texlive-latex-base texlive-latex-recommended texlive-latex-extra
```

**Installed version:** 2.17.1.1

**Package details:**
- `pandoc` - Core document converter (supports markdown, HTML, LaTeX, and many other formats)
- `texlive-latex-base` - Basic LaTeX packages for PDF generation
- `texlive-latex-recommended` - Recommended LaTeX packages
- `texlive-latex-extra` - Additional LaTeX packages for advanced formatting

**Basic usage:**
```bash
# Simple conversion
pandoc input.md -o output.pdf

# With custom styling
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V geometry:margin=1in \
  -V fontsize=12pt

# With table of contents
pandoc input.md -o output.pdf --toc

# Convert to other formats
pandoc input.md -o output.html
pandoc input.md -o output.docx
```

**Common options:**
- `--pdf-engine=xelatex` - Use XeLaTeX for better font support
- `-V geometry:margin=1in` - Set page margins
- `-V fontsize=12pt` - Set font size
- `--toc` - Generate table of contents
- `--number-sections` - Add section numbers
- `--standalone` - Create standalone document with headers

**Documentation:** https://pandoc.org/MANUAL.html

## Verification

To verify installations:

```bash
# Check pandoc
pandoc --version

# Test basic conversion
echo "# Test" > test.md
pandoc test.md -o test.pdf
rm test.md test.pdf
```

---

**Last updated:** 2025-11-06
