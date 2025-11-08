# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Context

This is the **el_documents** repository: AI-assisted revisions of EL (Early Learning) manuals and other documents.

## Core Principles

### I. Documentation-First (NON-NEGOTIABLE)

**Before EVERY commit, documentation must be updated:**
- Project/feature README files reflecting current status and implementation notes
- Conceptual specification files if the plan or approach changes
- Requirements files (`requirements.txt`) with any new dependencies

**Why**: Documentation synchronized with code prevents knowledge loss and ensures reproducibility.

### II. Virtual Environment Standard

**All Python work must use the .venv virtual environment:**

```bash
# First time setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Execution Pattern (NON-NEGOTIABLE):**
```bash
.venv/bin/python PATH/SOME_PYFILE.py
```

**Why**: Using `.venv/bin/python` directly ensures consistent environment without relying on shell activation state.

**Requirements management:**
- Root `requirements.txt` for all dependencies
- Update requirements file immediately when installing new packages
- Use `pip freeze > requirements.txt` to capture exact versions

### III. Spec-Driven Development

**This project uses [GitHub Spec-Kit](https://github.com/github/spec-kit) for spec-driven development.**

**Before making ANY changes:**
1. Read this file (CLAUDE.md)
2. Check relevant specs in `specs/` directory
3. Use `/speckit.*` slash commands for spec-driven workflow

**Core workflow:**
- `/speckit.constitution` - Review or update project principles
- `/speckit.specify` - Define what you want to build
- `/speckit.plan` - Create technical implementation plans
- `/speckit.tasks` - Generate actionable task lists
- `/speckit.implement` - Execute implementation

### IV. Document Processing Standards

**File organization:**
- Source documents in repository root (e.g., `EL_CgManual_CURRENT_v016.pdf`)
- Processing scripts organized by function
- Output artifacts clearly versioned

**Version control:**
- ✅ Source documents (PDFs, text files)
- ✅ Processing scripts and utilities
- ✅ Output documents and revisions
- ✅ Metadata and configuration files
- ❌ Virtual environment directories
- ❌ Temporary/intermediate processing files

## Development Workflow

**Commit Message Standards (NON-NEGOTIABLE):**
- **NEVER include AI tool attributions** (no "Generated with Claude Code", no "Co-Authored-By: Claude")
- **NEVER include emoji or decorative elements** in commit messages
- Keep commit messages focused on what changed and why
- Use conventional commit format when appropriate (e.g., "feat:", "fix:", "docs:")
- First line: concise summary (50-72 characters)
- Optional body: detailed explanation of changes and rationale

## Environment Setup

**Virtual Environment: .venv (NON-NEGOTIABLE)**
```bash
# First time setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Subsequent usage:**
```bash
# Always use direct path to Python interpreter
.venv/bin/python your_script.py

# Or activate for interactive work
source .venv/bin/activate
```

## System Dependencies

**Required:** See `docs/system-setup.md` for system-level dependencies (pandoc, etc.)

## Common Patterns

### Running Python Scripts

**ALWAYS use the virtual environment's Python directly:**
```bash
.venv/bin/python scripts/process_document.py input.pdf
```

### Installing New Dependencies

```bash
source .venv/bin/activate
pip install package-name
pip freeze > requirements.txt  # Update requirements immediately
```

## AI API Standards

### Gemini API (NON-NEGOTIABLE)

**Standard Model: gemini-2.5-pro**

All Gemini API calls MUST use `gemini-2.5-pro` unless there's a specific documented reason to use another model.

**Why:**
- Most capable model for document processing and reorganization
- Supports context caching (75-90% cost savings on repeated context)
- Better reasoning and content preservation
- Consistent quality across the project

**Context Caching:**
- Gemini 2.5 Pro supports automatic implicit caching (min 2,048 tokens)
- Explicit caching available for 90% savings (min 4,096 tokens)
- Always enable for documents >4K tokens

**Usage in scripts:**
```python
from lib.gemini_api import call_gemini

response = call_gemini(
    prompt,
    model="gemini-2.5-pro",  # Standard model
    temperature=0.2,          # Lower for deterministic tasks
    max_output_tokens=50000
)
```

**Parallel Processing:**
- Use `concurrent.futures` for independent API calls
- Process sections/chunks in parallel when possible
- Example: Document reorganization with 8 sections = 8 parallel calls

## Governance

**CLAUDE.md supersedes all other documentation.**

**Amendments require:**
1. Documentation update in this file
2. Documented reasoning for changes
3. Migration plan for existing code/data if applicable

**Compliance verification:**
- Pre-commit checklist includes this file review
- Complexity must be justified (document in implementation plans)
- YAGNI principles: Start simple, add complexity only when needed

## Key Documentation

**This File** (MUST READ): `CLAUDE.md` - Core principles and development standards

**Spec-Kit System**: `.specify/README.md`
- Slash commands: `/speckit.*` for spec-driven workflow
- Templates for specs, plans, and tasks

**Feature Specs**: `specs/` directory
- Feature-specific specifications and implementation plans

## Troubleshooting

**Virtual environment missing:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Import errors:**
```bash
# Ensure using venv Python
.venv/bin/python --version

# Reinstall requirements
source .venv/bin/activate
pip install -r requirements.txt
```

**Scripts fail with path errors:**
- Run from repository root
- Use `.venv/bin/python` prefix for all script executions

---

**Version**: 1.1.0 | **Ratified**: 2025-11-05 | **Last Amended**: 2025-11-08

## Active Technologies
- Python 3.11 + markdown, pdfplumber, PyPDF2, sentence-transformers, regex, python-docx (005-document-structure-repair)
- Gemini 2.5 Pro API with context caching (document reorganization, content processing)
- File-based markdown documents in `output/markdown/` with staged processing directories (005-document-structure-repair)
- Parallel processing with `concurrent.futures` for AI API calls

## Recent Changes
- 2025-11-08: Added AI API Standards section - standardized on gemini-2.5-pro for all Gemini API calls
- 2025-11-08: Added parallel processing patterns for document reorganization
- 005-document-structure-repair: Added Python 3.11 + markdown, pdfplumber, PyPDF2, sentence-transformers, regex, python-docx
