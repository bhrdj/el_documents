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

**Version**: 1.0.0 | **Ratified**: 2025-11-05 | **Last Amended**: 2025-11-05
