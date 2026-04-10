"""
Intent Qualification System — Solution Entry Point

A multi-stage pipeline that determines whether companies truly match
a user's search intent, combining structured filtering, semantic ranking,
and LLM verification.

Pipeline: Query Analysis → Structured Filters → Embedding Ranking → LLM Verification
"""

import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

from src.config import (
    EMBEDDING_MODEL,
    GROQ_API_KEY,
    GROQ_MODEL,
    LLM_CACHE_PATH,
)
from src.utils.data_loader import load_companies
from src.query_analyzer import QueryAnalyzer
from src.filters import StructuredFilter
from src.ranker import EmbeddingRanker
from src.llm_verifier import GroqVerifier, CachedLLMVerifier

EMBEDDINGS_PATH = "data/embeddings.npy"
TOP_K = 10

QUERIES = [
    "Logistic companies in Romania",
    "Public software companies with more than 1,000 employees.",
    "Food and beverage manufacturers in France",
    "Companies that could supply packaging materials for a direct-to-consumer cosmetics brand",
    "Construction companies in the United States with revenue over $50 million",
    "Pharmaceutical companies in Switzerland",
    "B2B SaaS companies providing HR solutions in Europe",
    "Clean energy startups founded after 2018 with fewer than 200 employees",
    "Fast-growing fintech companies competing with traditional banks in Europe.",
    "E-commerce companies using Shopify or similar platforms",
    "Renewable energy equipment manufacturers in Scandinavia",
    "Companies that manufacture or supply critical components for electric vehicle battery production",
]


def build_structured_context(row: pd.Series) -> str:
    """Build a structured context string from verified company data."""
    parts = []
    if pd.notna(row.get("employee_count")):
        parts.append(f"Employee count: {int(row['employee_count'])}")
    if pd.notna(row.get("revenue")):
        parts.append(f"Revenue: ${row['revenue']:,.0f}")
    if pd.notna(row.get("year_founded")):
        parts.append(f"Founded: {int(row['year_founded'])}")
    if pd.notna(row.get("is_public")):
        parts.append(f"Public company: {'Yes' if row['is_public'] else 'No'}")
    if pd.notna(row.get("country_code")):
        parts.append(f"Country: {row['country_code'].upper()}")
    if isinstance(row.get("business_model"), list):
        parts.append(f"Business model: {', '.join(row['business_model'])}")
    if isinstance(row.get("core_offerings"), list):
        parts.append(f"Core offerings: {', '.join(row['core_offerings'])}")
    if isinstance(row.get("target_markets"), list):
        parts.append(f"Target markets: {', '.join(row['target_markets'])}")
    if pd.notna(row.get("industry_label")):
        parts.append(f"Industry: {row['industry_label']}")
    return "\n".join(parts) if parts else "None available"


def run_pipeline(query: str, analyzer, structured_filter_data, ranker, verifier):
    """Run the full qualification pipeline for a single query."""
    # Stage 1 — Query analysis
    analysis = analyzer.analyze(query)
    filters = analysis["filters"]

    # Stage 2 — Structured filtering
    filtered = StructuredFilter(structured_filter_data).apply(filters)

    if len(filtered) == 0:
        return [], filters, 0, 0

    # Stage 3 — Embedding ranking
    top_candidates = ranker.rank(query, filtered, top_k=TOP_K)

    # Stage 4 — LLM verification
    results = []
    for _, row in top_candidates.iterrows():
        structured_context = build_structured_context(row)
        result = verifier.verify(
            query,
            row["description"],
            company_name=row["operational_name"],
            structured_context=structured_context,
        )
        results.append((row, result))

    # Fallback for numeric-heavy queries where LLM can't verify from descriptions
    qualified_count = sum(1 for _, r in results if r.qualified)
    numeric_keys = {
        "min_employees", "max_employees", "min_revenue", "max_revenue",
        "is_public", "min_year_founded", "max_year_founded",
    }
    used_fallback = False
    if qualified_count == 0 and numeric_keys & set(filters.keys()):
        used_fallback = True
        qualified_count = len(results)

    return results, filters, len(filtered), used_fallback


def main():
    # Load shared resources
    print("Loading companies and embeddings...")
    companies = load_companies()
    embeddings = np.load(EMBEDDINGS_PATH)
    model = SentenceTransformer(EMBEDDING_MODEL)
    print(f"Loaded {len(companies)} companies.\n")

    # Initialize pipeline components
    analyzer = QueryAnalyzer()
    ranker = EmbeddingRanker(model=model, embeddings=embeddings)
    base_verifier = GroqVerifier(api_key=GROQ_API_KEY, model=GROQ_MODEL)
    verifier = CachedLLMVerifier(
        base_verifier,
        cache_path=LLM_CACHE_PATH,
        model_id=GROQ_MODEL,
    )

    summary = []

    for i, query in enumerate(QUERIES, 1):
        print(f"{'=' * 70}")
        print(f"QUERY {i}/{len(QUERIES)}: {query}")
        print(f"{'=' * 70}\n")

        results, filters, filtered_count, used_fallback = run_pipeline(
            query, analyzer, companies, ranker, verifier
        )

        print(f"  Filters: {filters}")
        print(f"  After structured filter: {filtered_count} companies")

        if not results:
            print("  No companies passed the structured filter.\n")
            summary.append((query, filtered_count, 0, 0))
            continue

        print(f"  Top candidates: {len(results)}\n")

        qualified_count = 0
        for row, result in results:
            status = "[YES]" if result.qualified or used_fallback else "[NO] "
            print(f"  {status} ({row['similarity']:.3f}) {row['operational_name']}")
            print(f"         {result.reason}")
            if result.qualified or used_fallback:
                qualified_count += 1

        if used_fallback:
            print(f"\n  [FALLBACK] Structural filters already verified: {filters}")
            print(f"  Accepting {qualified_count} candidates based on structural + embedding match.")

        summary.append((query, filtered_count, len(results), qualified_count))
        print()

    # Summary table
    print(f"\n{'=' * 70}")
    print("SUMMARY")
    print(f"{'=' * 70}")
    print(f"{'Query':<75} {'Filtered':>8} {'Top-K':>6} {'Qual':>6}")
    print("-" * 100)
    for query, filt, topk, qual in summary:
        short_q = query[:72] + "..." if len(query) > 75 else query
        print(f"{short_q:<75} {filt:>8} {topk:>6} {qual:>6}")


if __name__ == "__main__":
    main()