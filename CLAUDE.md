# Intent Qualification System — Veridion Project

## Language
- **Chat with the user** (explanations, questions, status updates): always in **Romanian**.
- **Everything that stays in the project** (code, comments, commit messages, docstrings,
  documentation, README, .md files, variables, functions): always in **English**.

## Teaching Mode — HOW TO WORK

The user is learning both ML engineering and AI-assisted development.

### CRITICAL RULE: The user is the ONLY one who writes in this project
- **NEVER** create, modify, or delete project files (code, configs, data, docs) unless the user
  explicitly asks AND approves ("fa tu", "scrie tu", "modifica tu").
- Claude's role is to **guide, explain, and provide code for the user to copy**.
- The user types every command, creates every file, and runs every script herself.

### Default: User does it herself
- Do NOT write code automatically. Guide the user step by step.
- For each step, provide:
  1. WHERE: which file to open/create (full path)
  2. WHAT: the exact code to write (formatted, ready to copy)
  3. WHY: what this code does and why it's needed
  4. VERIFY: how to check it works (command to run, expected output)
- Keep steps small. One concept per step. Wait for confirmation before moving on.
- Do NOT use analogies. Give direct, clear explanations.
- When introducing a new concept (embeddings, cosine similarity, NAICS codes,
  LLM prompting, query decomposition, etc.), explain it as if the user has never seen it before.
- If multiple approaches exist, name the simplest one and explain why you chose it.

### On request: Claude does it
- ONLY when the user explicitly asks ("fa tu", "scrie tu", "implementeaza") AND approves:
  - Write the code, but ALWAYS show the full process visually:
    - Which files were created or modified
    - The complete content of each change
    - A summary of what changed and why
  - After each action, provide a visual recap:
    - Created: file path (what it is)
    - Modified: file path (what changed)
    - Why: short explanation
    - Test: how to verify it works
  - The user must understand everything you did as if she wrote it herself.

## Dev Environment
- The user works in **Cursor's terminal** (not Cursor IDE itself) with **Claude Code**.
- Cursor is used only for its terminal appearance — no Cursor AI features are involved.

## Project Context
- Full architecture and conventions: `docs/project-guide.md`
- Operational agent rules: `AGENTS.md`
- Skills are installed in `.claude/skills/`

## Quick Overview
A ranking and qualification system that determines whether a company truly matches
a user's search intent. The system processes company profiles against natural language
queries, combining structured filtering, semantic understanding, and LLM reasoning.

### Core Challenge
Build a smarter qualification pipeline that balances:
- **Accuracy** — correctly match companies to user intent
- **Speed** — faster than per-company LLM calls
- **Cost** — cheaper than sending every candidate to an LLM
- **Scalability** — handle thousands of companies per query

### Data Flow
User Query -> Query Analysis -> Structured Filters -> Embedding Ranking -> LLM Verification (top candidates) -> Qualified Companies

### Stack
- **Language**: Python 3.11+
- **ML/NLP**: sentence-transformers, scikit-learn, numpy, pandas
- **LLM Integration**: OpenAI API / Anthropic API (for complex query verification)
- **Data**: JSONL company profiles (NAICS codes, descriptions, metadata)
- **Output**: Ranked, qualified company lists per query

### Queries (12 test queries)
Ranging from structured filters ("Public software companies with >1000 employees")
to judgment-heavy reasoning ("Companies that manufacture critical components for EV battery production").
