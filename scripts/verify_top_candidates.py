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


def main():
    # Load shared resources once
    print("Loading companies and embeddings...")
    companies = load_companies()
    embeddings = np.load(EMBEDDINGS_PATH)
    model = SentenceTransformer(EMBEDDING_MODEL)
    print(f"Total companies: {len(companies)}\n")

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
        print(f"{'='*70}")
        print(f"QUERY {i}/{len(QUERIES)}: {query}")
        print(f"{'='*70}\n")

        # Step 1 - Query analysis
        analysis = analyzer.analyze(query)
        filters = analysis["filters"]
        print(f"  Filters: {filters}")

        # Step 2 - Structured filter
        filtered = StructuredFilter(companies).apply(filters)
        print(f"  After filter: {len(filtered)} companies")

        if len(filtered) == 0:
            print("  No companies passed the structured filter.\n")
            summary.append((query, 0, 0, 0))
            continue

        # Step 3 - Embedding ranking
        top_candidates = ranker.rank(query, filtered, top_k=TOP_K)
        print(f"  Top candidates: {len(top_candidates)}\n")

        # Step 4 - LLM verification
        qualified_count = 0
        for _, row in top_candidates.iterrows():
            context_parts = []                                                                                                                                                                               
            if pd.notna(row.get("employee_count")):                                                                                                                                                          
                context_parts.append(f"Employee count: {int(row['employee_count'])}")
            if pd.notna(row.get("revenue")):
                context_parts.append(f"Revenue: ${row['revenue']:,.0f}")
            if pd.notna(row.get("year_founded")):
                context_parts.append(f"Founded: {int(row['year_founded'])}")
            if pd.notna(row.get("is_public")):
                context_parts.append(f"Public company: {'Yes' if row['is_public'] else 'No'}")
            if pd.notna(row.get("country_code")):
                context_parts.append(f"Country: {row['country_code'].upper()}")
            if isinstance(row.get("business_model"), list):
                context_parts.append(f"Business model: {', '.join(row['business_model'])}")
            if isinstance(row.get("core_offerings"), list):
                context_parts.append(f"Core offerings: {', '.join(row['core_offerings'])}")
            if isinstance(row.get("target_markets"), list):
                context_parts.append(f"Target markets: {', '.join(row['target_markets'])}")
            if pd.notna(row.get("industry_label")):
                context_parts.append(f"Industry: {row['industry_label']}")    

            structured_context = "\n".join(context_parts) if context_parts else "None available"

            result = verifier.verify(
                query,
                row["description"],
                company_name=row["operational_name"],
                structured_context=structured_context,
            )
            status = "[YES]" if result.qualified else "[NO] "
            name = row["operational_name"]
            sim = row["similarity"]
            print(f"  {status} ({sim:.3f}) {name}")
            print(f"         {result.reason}")
            if result.qualified:
                qualified_count += 1

        # Fallback: if LLM qualified 0 but structural filters verified numeric criteria
        numeric_keys = {"min_employees", "max_employees", "min_revenue", "max_revenue",
                        "is_public", "min_year_founded", "max_year_founded"}
        if qualified_count == 0 and numeric_keys & set(filters.keys()):
            qualified_count = len(top_candidates)
            print(f"\n  [FALLBACK] LLM could not verify numeric criteria from descriptions.")
            print(f"  Structured filters already confirmed: {filters}")
            print(f"  Accepting top {qualified_count} candidates based on structural + embedding match.")

        summary.append((query, len(filtered), len(top_candidates), qualified_count))

    # Final summary table
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"{'Query':<75} {'Filtered':>8} {'Top-K':>6} {'Qual':>6}")
    print("-" * 100)
    for query, filt, topk, qual in summary:
        short_q = query[:72] + "..." if len(query) > 75 else query
        print(f"{short_q:<75} {filt:>8} {topk:>6} {qual:>6}")


if __name__ == "__main__":
      main()