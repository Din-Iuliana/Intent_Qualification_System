# Agent Instructions

## Language
- **Chat with the user** (explanations, questions, status updates): always in **Romanian**.
- **Everything that stays in the project** (code, comments, commit messages, docstrings,
  documentation, README, .md files, variables, functions): always in **English**.

## Teaching Rules
- Always read `CLAUDE.md` first for communication and teaching mode rules.
- Read `docs/project-guide.md` for architecture decisions before making changes.
- Use installed skills from `.claude/skills/` when the task matches a skill's domain.
- ML pipeline changes require explaining the full data flow to the user.
- New algorithm choices require explaining WHY this approach over alternatives.
- One step at a time. Never do multiple things at once without explaining each.

## Code Conventions
- Every new file must have a 1-2 line header comment explaining its purpose.
- Functions must have docstrings explaining what they do, inputs, and outputs.
- No unnecessary libraries. Prefer simple, readable code over clever code.
- Type hints are required for all function signatures.
- Use descriptive variable names — no single-letter variables except loop counters.
- Constants (thresholds, model names, API params) go at the top of the file or in `config.py`.

## ML-Specific Conventions
- All embedding models and LLM model names must be configurable constants, never hardcoded inline.
- Similarity thresholds must be named constants with comments explaining the chosen value.
- Data transformations must be logged or traceable for debugging.
- Company qualification decisions must include confidence scores where possible.
- Never load the full dataset into memory if a streaming/chunked approach is viable at scale.

## Project Structure
- `src/` — Core Python modules. One file per responsibility.
- `src/filters/` — Structured filter logic (location, revenue, employee count, etc.).
- `src/rankers/` — Embedding and similarity ranking logic.
- `src/qualifiers/` — LLM-based qualification for complex queries.
- `src/utils/` — Shared utilities (data loading, text processing, config).
- `data/` — Dataset files (companies.jsonl). Never commit API keys here.
- `tests/` — Test files mirroring src/ structure.
- `docs/` — Project documentation.

## Git
- Small, descriptive commits in English.
- One commit = one logical change.
- Use conventional commit format: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`.
- Explain what each commit does and why before committing.

## Environment & Dependencies
- Use a virtual environment (`venv` or `conda`).
- All dependencies tracked in `requirements.txt` with pinned versions.
- API keys stored in `.env` file (never committed — add to `.gitignore`).
- `.env.example` with placeholder values for documentation.

## When Unsure
- If a task is ambiguous, ask the user instead of guessing.
- If a change could break existing functionality, warn the user first.
- If an ML approach has known limitations for certain query types, document them.
