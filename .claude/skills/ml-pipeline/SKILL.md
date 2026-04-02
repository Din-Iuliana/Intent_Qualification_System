---
name: ml-pipeline
description: "Design and implement ML qualification pipelines combining structured filtering, embedding similarity, and LLM verification. Use when building multi-stage ranking systems, company matching, intent qualification, or hybrid retrieval pipelines."
metadata:
  tags: ml-pipeline, ranking, qualification, embeddings, LLM, hybrid-search
  platforms: Claude
---

# ML Pipeline Design

## When to use this skill
- Designing multi-stage ranking/qualification pipelines
- Implementing query analysis and intent decomposition
- Building hybrid retrieval systems (filters + embeddings + LLM)
- Optimizing pipeline stages for cost/accuracy tradeoffs
- Handling missing data in entity matching

## Instructions

### Step 1: Query Analysis

Decompose the user query into:
- **Structured constraints**: fields that can be filtered directly (location, revenue, employee_count, year_founded, is_public, business_model)
- **Semantic intent**: what the user means beyond literal field matches (industry role, supply chain position, competitive landscape)
- **Complexity classification**: structured (filters only), mixed (filters + semantics), or semantic (reasoning required)

```python
# Query analysis output structure
{
    "structured_filters": {
        "location": "Romania",
        "is_public": True,
        "employee_count_min": 1000
    },
    "semantic_intent": "logistics companies",
    "complexity": "structured"  # or "mixed" or "semantic"
}
```

### Step 2: Structured Filtering

Apply hard filters on known fields:

```python
def apply_structured_filters(companies: list, filters: dict) -> list:
    """
    Filter companies based on structured constraints.
    Missing fields should NOT exclude a company — only contradicting data should.
    """
    pass
```

Key rules:
- Missing data != negative match. If `employee_count` is None, do NOT exclude.
- Location matching should handle partial matches (country, city, region).
- NAICS codes provide industry classification — use both primary and secondary.
- Revenue/employee filters should use >= or <= comparisons.

### Step 3: Embedding Ranking

Encode and rank remaining candidates:

```python
from sentence_transformers import SentenceTransformer
import numpy as np

def build_company_text(company: dict) -> str:
    """Build a rich text representation for embedding."""
    parts = []
    if company.get("description"):
        parts.append(company["description"])
    if company.get("core_offerings"):
        parts.append("Offerings: " + ", ".join(company["core_offerings"]))
    if company.get("target_markets"):
        parts.append("Markets: " + ", ".join(company["target_markets"]))
    if company.get("primary_naics"):
        parts.append("Industry: " + company["primary_naics"].get("label", ""))
    return " | ".join(parts)
```

Key rules:
- Build rich text from multiple fields for better embedding quality.
- Use cosine similarity for ranking, NOT as a binary classifier.
- Select top-K candidates (configurable) for next stage.
- Cache embeddings — recompute only when data changes.

### Step 4: LLM Qualification (selective)

Only for complex queries or borderline candidates:

```python
def qualify_with_llm(company: dict, query: str) -> dict:
    """
    Ask LLM to judge if company matches query.
    Returns: {"match": bool, "confidence": float, "reasoning": str}
    """
    pass
```

Key rules:
- Skip LLM for purely structured queries.
- Batch companies where possible to reduce API calls.
- Include company profile AND query in the prompt.
- Ask for structured output (yes/no + confidence + reasoning).
- Set cost budgets — never send all candidates to LLM.

### Step 5: Result Assembly

Combine scores from all stages:

```python
def compute_final_score(filter_pass: bool, similarity: float, llm_result: dict) -> float:
    """Weighted combination of pipeline stage signals."""
    pass
```

## Tradeoff Guidelines

| Query Type | Filters | Embeddings | LLM | Expected Cost |
|------------|---------|------------|-----|---------------|
| Structured | Heavy   | Light      | Skip | Minimal |
| Mixed      | Medium  | Medium     | Top-K only | Low |
| Semantic   | Light   | Heavy      | Top-K | Medium |

## Missing Data Strategy

- Never exclude companies solely because a field is missing.
- If a filter field is missing, treat the company as "possibly matching" and let later stages decide.
- Log which fields were missing for error analysis.

## Performance Targets

- Structured queries: < 1 second for 500 companies
- Mixed queries: < 5 seconds for 500 companies
- Semantic queries: < 15 seconds for 500 companies (including LLM calls)

## Common Pitfalls

1. **Similarity != relevance**: "packaging for cosmetics" query ranks cosmetics companies above packaging suppliers.
2. **Missing data bias**: excluding companies with missing fields biases toward well-documented companies.
3. **LLM inconsistency**: same borderline company may get different results across runs. Use temperature=0 and structured prompts.
4. **Over-filtering**: too aggressive structured filters remove valid candidates before semantic analysis.
