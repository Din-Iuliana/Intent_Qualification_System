# Intent Qualification System — Writeup

## 1. Approach

The system uses a 4-stage pipeline that progressively filters companies, from hundreds down to a few dozen final candidates. The core idea: not every company needs the same level of evaluation. Those that clearly don't match are eliminated early and cheaply, while the LLM only verifies plausible candidates.

### The 4 Stages

**Stage 1 — Query Analysis**

Parses the user query and extracts structured constraints: country, employee count, revenue, year founded, company type (public/private), business model. For example, *"Public software companies with more than 1,000 employees"* yields `is_public: True` and `min_employees: 1000`. The semantic intent (industry, supply chain role) is left for later stages.

**Stage 2 — Structured Filtering**

Applies the extracted filters directly on dataset fields: `country_code`, `employee_count`, `revenue`, `year_founded`, `is_public`, `business_model`. It's fast (DataFrame operations) and eliminates companies that clearly don't match. Companies with missing data are not excluded — only those that explicitly contradict a filter.

**Stage 3 — Embedding Ranking**

Encodes the query and company profiles into the same vector space using `all-MiniLM-L6-v2` (a sentence-transformers model). Computes cosine similarity and selects the top 10 candidates. Company profiles are enriched with industry label, core offerings, and target markets — not just the text description — which improves result relevance.

**Stage 4 — LLM Verification**

Sends each of the top 10 candidates to an LLM (`llama-3.1-8b-instant` via Groq API) which decides YES/NO with explicit reasoning. The prompt distinguishes between **VERIFIABLE** criteria (industry, location, size — marked MET only if confirmed) and **INFERRABLE** criteria (growth rate, competitive positioning — marked LIKELY MET if evidence suggests it). Responses are cached to disk (JSON with SHA256 keys) for reproducibility and token savings.

**Fallback logic:** If the LLM qualifies 0 companies but the query had numeric criteria already verified by structural filters (employees, revenue, public status), all top 10 candidates are accepted. This compensates for the 8B model's limitation in reasoning about numbers.

### Why This Design?

Each stage handles a different type of complexity. Structural filters are perfect for *"companies in France"* or *"revenue over $50M"*. Embeddings capture semantic similarity (*"packaging for cosmetics"* → packaging suppliers). The LLM handles complex reasoning (*"companies competing with traditional banks"*). By combining them, the system avoids both the cost of sending every company to an LLM and the imprecision of plain vector search.

## 2. Tradeoffs

**Optimized for:**

- **Accuracy** — each stage adds a layer of verification; the LLM is the final check.
- **Cost** — the LLM sees only 10 companies per query, not 477; the cache eliminates duplicate calls.
- **Robustness to missing data** — companies with missing fields pass through filters (they are not automatically excluded).

**Intentional tradeoffs:**

- **Recall vs. Precision in structural filtering:** The filter is permissive — companies with missing data pass through. This means more companies reach the embedding ranker (e.g., 477 for queries without structural filters), but we don't lose good candidates.
- **8B model vs. larger model:** I used `llama-3.1-8b-instant` instead of a 70B model. It's faster and free on Groq's API, but has limitations with numeric reasoning (which is why the fallback exists).
- **Fixed Top-K (10):** The number of candidates sent to the LLM is not dynamically adapted. A larger K would increase recall but also cost.
- **Fallback accepts all top 10:** When the LLM can't verify numeric criteria, all candidates are accepted. This is a conservative choice — we prefer false positives over zero results.

## 3. Error Analysis

### False positives

**Query 1 — "Logistic companies in Romania":**
- *European Drinks* (a bottled water manufacturer) was marked YES. The model considered that being a large Romanian company with a wholesale model made it logistics-related. It's not — it's a beverage producer.
- *Valbur* (an industrial supplies distributor) — marked YES based on its wholesale model, but it is not a logistics company.

**Query 10 — "E-commerce companies using Shopify":**
- *PEZ Candy* and *GreenLeaf Mate* (manufacturers) were marked YES because they have e-commerce in their business model. But the query asked for companies that *use* Shopify, not just any company with an online presence.

### False negatives

**Query 3 — "Food and beverage manufacturers in France":**
- *La Limonaderie de Paris* (a juice manufacturer) was marked NO because it only has 4 employees. But the query didn't require a minimum size — the LLM added an implicit criterion.

**Query 7 — "B2B SaaS companies providing HR solutions in Europe":**
- *BCS HR Software* and *Global HR* — parse errors (the LLM response was truncated at the 200 token limit). Perfectly valid companies, lost due to the token cap.

**Query 8 — "Clean energy startups founded after 2018":**
- Companies founded in 2025 were marked NOT MET for "founded after 2018" — the 8B model confused the direction of the temporal comparison.

### Where the system works extremely well

- **Query 6 (Pharmaceutical companies in Switzerland):** 10/10 — clear filters (country + industry), easy for the LLM to verify.
- **Query 11 (Renewable energy equipment manufacturers in Scandinavia):** 10/10 — same combination of structural filters and clear industry.
- **Query 12 (EV battery components):** 8/10 — even complex supply chain queries work well when companies have rich descriptions.

## 4. Scaling

If the system needed to handle 100,000 companies per query:

1. **Structured Filtering** — scales naturally. DataFrame operations are O(n) and remain fast even at hundreds of thousands of rows.

2. **Embedding Ranking** — precomputing embeddings (once) is already implemented. Cosine similarity with numpy/scikit-learn on 100K vectors takes milliseconds. For millions, I would use a vector index (FAISS or Annoy) that performs approximate nearest neighbor search in O(log n).

3. **LLM Verification** — this is the bottleneck. At 100K companies, top-K would remain small (10–50), so LLM cost doesn't increase. But if we wanted to verify more candidates, I would introduce batch processing and parallel API calls.

4. **Cache** — becomes critical at scale. The current JSON file works for hundreds of evaluations, but at tens of thousands I would migrate to a database (SQLite or Redis).

5. **Embeddings storage** — the current `.npy` file (477 companies) is under 1MB. At 100K it would be ~50MB, still manageable. At millions, I would use memory-mapped files or a vector database (Pinecone, Weaviate).

## 5. Failure Modes

### When the system produces confident but incorrect results

1. **Vague or generic descriptions:** A company described as "We provide innovative solutions for businesses worldwide" could be marked YES for almost any semantic query, because nothing explicitly contradicts it.

2. **Multi-domain companies:** A company that does both logistics and manufacturing could be marked YES for both types of queries, even if one of those activities is minor.

3. **Semantic embedding confusion:** Embeddings capture lexical similarity, not supply chain relationships. *"Companies that supply packaging for cosmetics"* could return cosmetics companies (which *mention* packaging) instead of actual packaging suppliers.

4. **8B model limitations with numeric logic:** The model marks companies with 21,000 employees as NOT MET for "more than 1,000 employees". Our fallback compensates, but doesn't cover all edge cases.

### What I would monitor in production

- **Parse error rate:** If it increases, the LLM output is no longer following the required format (possibly due to token limits or prompt drift).
- **Fallback activation rate:** If it triggers too often, the LLM model is no longer useful for numeric queries.
- **Similarity score distribution:** If top candidates have low similarity (below 0.3), the query is probably not well covered by the dataset.
- **Qualified ratio per query:** If it drops suddenly (0/10), something is wrong with the structural filter or the embeddings.
- **Cache hit rate:** A high miss rate means new uncovered queries or data drift.
