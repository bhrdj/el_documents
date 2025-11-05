# Spec-Kit Documentation System

This project uses [GitHub Spec-Kit](https://github.com/github/spec-kit) for spec-driven development.

## Core Documents

### Constitution
**[CLAUDE.md](../CLAUDE.md)** - Non-negotiable principles and governance

**MUST READ for all contributors.** Defines:
- Documentation-First principle (update docs before every commit)
- Virtual Environment Standard (`.venv/bin/python` execution pattern)
- Spec-Driven Development workflow
- Document processing standards
- Development environment setup

*(This replaces the traditional `.specify/memory/constitution.md` pattern - the constitution is now at repository root)*

### Feature Specifications

Features are documented in `specs/[feature-name]/` with:
- **spec.md** - Functional requirements and user stories
- **plan.md** - Technical architecture and implementation details
- **tasks.md** - Actionable work breakdown

**Current Features:**
- *(No features yet - use `/speckit.specify` to create your first feature)*

## Spec-Kit Slash Commands

The `.claude/commands/` directory contains workflow commands for use with Claude Code:

| Command | Purpose |
|---------|---------|
| `/speckit.constitution` | Review or update the project constitution |
| `/speckit.specify` | Create feature specifications |
| `/speckit.plan` | Generate implementation plans |
| `/speckit.tasks` | Break down features into actionable tasks |
| `/speckit.implement` | Execute implementation with spec guidance |
| `/speckit.analyze` | Analyze existing code against specs |
| `/speckit.checklist` | Generate implementation checklists |
| `/speckit.clarify` | Clarify spec ambiguities |

## Templates

The `.specify/templates/` directory contains templates for creating new specifications:
- `spec-template.md` - Feature specification template
- `plan-template.md` - Implementation plan template
- `tasks-template.md` - Task breakdown template
- `checklist-template.md` - Implementation checklist template
- `agent-file-template.md` - Agent context template

## Scripts

The `.specify/scripts/` directory contains automation scripts:
- `create-new-feature.sh` - Create new feature specification
- `setup-plan.sh` - Initialize implementation plan
- `update-agent-context.sh` - Update agent context files
- `check-prerequisites.sh` - Verify required tools
- `common.sh` - Shared utility functions

## Directory Structure

```
.specify/               # Spec-kit infrastructure (version controlled)
├── memory/
│   └── constitution.md # Template constitution (actual at ../CLAUDE.md)
├── templates/          # Spec/plan/task templates
└── scripts/            # Automation scripts

.claude/                # Claude Code configuration (version controlled)
└── commands/           # Spec-kit slash commands

specs/                  # Feature specifications (version controlled)
└── [feature-name]/
    ├── spec.md         # Functional requirements
    ├── plan.md         # Implementation plan
    └── tasks.md        # Work breakdown

.venv/                  # Virtual environment (NOT version controlled)
```

## Getting Started

1. Read the [Constitution](../CLAUDE.md)
2. Ensure virtual environment is set up:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Use `/speckit.*` commands in Claude Code for spec-driven workflow
4. Always use `.venv/bin/python` for script execution

## Python Execution Pattern

**ALWAYS use the virtual environment's Python directly:**
```bash
.venv/bin/python path/to/script.py
```

**Why**: This ensures consistent environment without relying on shell activation state.
