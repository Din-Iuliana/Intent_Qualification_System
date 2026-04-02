# Project Guide — Intent Qualification System

## Architecture

```text
+------------------+      +---------------------+      +-------------------+
|  User Query      | ---> |  Query Analyzer     | ---> |  Structured       |
|  (natural lang)  |      |  (decompose intent) |      |  Filters          |
+------------------+      +---------------------+      |  (location, size, |
                                                       |   industry, etc.) |
                                                       +--------+----------+
                                                                |
                                                    candidates (fast, cheap)
                                                                |
                                                       +--------v----------+
                                                       |  Embedding        |
                                                       |  Ranker           |
                                                       |  (semantic sim.)  |
                                                       +--------+----------+
                                                                |
                                                      top-K candidates
                                                                |
                                                       +--------v----------+
                                                       |  LLM Qualifier    |
                                                       |  (verify complex  |
                                                       |   matches only)   |
                                                       +--------+----------+
                                                                |
                                                       +--------v----------+
                                                       |  Qualified        |
                                                       |  Companies        |
                                                       +-------------------+
```

## Pipeline Stages

### Stage 1: Query Analysis
- Parse the user query to extract structured constraints (location, revenue, employee count, year founded, is_public).
- Identify the semantic intent (industry, role in supply chain, business model).
- Classify query complexity: **structured** (field-based filters suffice) vs. **semantic** (requires reasoning).

### Stage 2: Structured Filtering
- Apply hard filters on known fields: address, employee_count, revenue, year_founded, is_public, business_model.
- Uses NAICS codes (primary_naics, secondary_naics) for industry matching.
- Fast elimination of clearly irrelevant companies.
- Tolerant of missing data — companies with missing fields are not automatically excluded.

### Stage 3: Embedding Ranking
- Encode company profiles (description + core_offerings + target_markets) into embeddings.
- Encode the query into the same embedding space.
- Rank remaining candidates by cosine similarity.
- Select top-K candidates for further evaluation.

### Stage 4: LLM Qualification (selective)
- Only invoked for complex/ambiguous queries or borderline candidates.
- Sends company profile + query to LLM for yes/no/maybe decision with reasoning.
- Batched where possible to reduce API calls.
- Skipped entirely for purely structured queries.

## Project Structure

```text
Intent_Qualification_Project/
├── CLAUDE.md                    # Claude Code configuration
├── AGENTS.md                    # Agent operational rules
├── Brief_Veridion_Project.txt   # Original project brief
├── requirements.txt             # Python dependencies (pinned)
├── .env.example                 # Environment variable template
├── .gitignore                   # Git ignore rules
├── solution.py                  # Main entry point
├── WRITEUP.md                   # Solution writeup (deliverable)
│
├── src/
│   ├── __init__.py
│   ├── config.py                # Constants, thresholds, model names
│   ├── pipeline.py              # Main orchestration pipeline
│   │
│   ├── analyzers/
│   │   ├── __init__.py
│   │   └── query_analyzer.py    # Query parsing and classification
│   │
│   ├── filters/
│   │   ├── __init__.py
│   │   └── structured_filter.py # Field-based filtering logic
│   │
│   ├── rankers/
│   │   ├── __init__.py
│   │   └── embedding_ranker.py  # Semantic similarity ranking
│   │
│   ├── qualifiers/
│   │   ├── __init__.py
│   │   └── llm_qualifier.py     # LLM-based verification
│   │
│   └── utils/
│       ├── __init__.py
│       ├── data_loader.py       # JSONL loading and preprocessing
│       └── text_processing.py   # Text cleaning, profile building
│
├── data/
│   └── companies.jsonl          # Company dataset
│
├── tests/
│   ├── __init__.py
│   ├── test_query_analyzer.py
│   ├── test_structured_filter.py
│   ├── test_embedding_ranker.py
│   └── test_llm_qualifier.py
│
├── docs/
│   └── project-guide.md         # This file
│
└── .claude/
    ├── settings.local.json      # Claude Code permissions
    └── skills/                  # Claude Code skills
```

## Design Decisions

- **Multi-stage pipeline** — each stage progressively narrows candidates, balancing cost and accuracy.
- **Structured filters first** — cheap, fast elimination before expensive operations.
- **Embeddings for ranking, not classification** — similarity score is a signal, not a final answer.
- **LLM as a last resort** — only used for complex queries or borderline cases, keeping cost low.
- **Missing data tolerance** — companies with incomplete profiles are not penalized; the system uses whatever fields are available.
- **Query complexity routing** — simple structured queries skip the LLM stage entirely.

## Company Data Fields

| Field | Type | Used In |
|-------|------|---------|
| `operational_name` | string | Display, identification |
| `website` | string | Display |
| `year_founded` | int | Structured filter |
| `address` | string | Structured filter (location) |
| `employee_count` | int | Structured filter |
| `revenue` | float | Structured filter |
| `primary_naics` | object | Structured filter (industry) |
| `secondary_naics` | array | Structured filter (industry) |
| `description` | string | Embedding, LLM qualifier |
| `business_model` | array | Structured filter |
| `target_markets` | array | Embedding, LLM qualifier |
| `core_offerings` | array | Embedding, LLM qualifier |
| `is_public` | bool | Structured filter |

## Environment Variables

- `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` — LLM API key (never commit)
- `EMBEDDING_MODEL` — sentence-transformer model name (default in config.py)
- `LLM_MODEL` — LLM model for qualification (default in config.py)
- `TOP_K` — number of candidates to send to LLM (default in config.py)

## 12 Test Queries

| # | Query | Complexity |
|---|-------|------------|
| 1 | Logistic companies in Romania | Structured |
| 2 | Public software companies with more than 1,000 employees | Structured |
| 3 | Food and beverage manufacturers in France | Structured |
| 4 | Companies that could supply packaging materials for a D2C cosmetics brand | Semantic |
| 5 | Construction companies in the US with revenue over $50M | Structured |
| 6 | Pharmaceutical companies in Switzerland | Structured |
| 7 | B2B SaaS companies providing HR solutions in Europe | Mixed |
| 8 | Clean energy startups founded after 2018 with <200 employees | Structured |
| 9 | Fast-growing fintech companies competing with traditional banks in Europe | Semantic |
| 10 | E-commerce companies using Shopify or similar platforms | Semantic |
| 11 | Renewable energy equipment manufacturers in Scandinavia | Mixed |
| 12 | Companies that manufacture/supply critical components for EV battery production | Semantic |
