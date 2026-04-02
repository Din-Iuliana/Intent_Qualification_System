---
name: embedding-strategies
description: "Design and implement embedding-based semantic search and ranking strategies. Use when choosing embedding models, building company profile embeddings, implementing cosine similarity ranking, or optimizing retrieval quality for intent matching."
metadata:
  tags: embeddings, semantic-search, sentence-transformers, cosine-similarity, ranking
  platforms: Claude
---

# Embedding Strategies for Intent Matching

## When to use this skill
- Choosing an embedding model for company profile matching
- Building rich text representations for embedding
- Implementing cosine similarity ranking
- Debugging poor embedding retrieval results
- Optimizing embedding quality for specific query types

## Instructions

### Step 1: Choose Embedding Model

| Model | Dimensions | Speed | Quality | Use Case |
|-------|-----------|-------|---------|----------|
| `all-MiniLM-L6-v2` | 384 | Fast | Good | Default, prototyping |
| `all-mpnet-base-v2` | 768 | Medium | Better | Production quality |
| `e5-large-v2` | 1024 | Slow | Best | Maximum accuracy |
| `bge-small-en-v1.5` | 384 | Fast | Good | Balanced alternative |

```python
from sentence_transformers import SentenceTransformer

# Default choice — good balance of speed and quality
model = SentenceTransformer("all-MiniLM-L6-v2")
```

### Step 2: Build Company Text for Embedding

The quality of embeddings depends heavily on what text you encode.

```python
def build_company_embedding_text(company: dict) -> str:
    """
    Build rich text representation combining multiple fields.
    Order matters — put most important information first.
    """
    parts = []

    # Primary: description is the richest signal
    if company.get("description"):
        parts.append(company["description"])

    # Secondary: structured offerings and markets
    if company.get("core_offerings"):
        offerings = company["core_offerings"]
        if isinstance(offerings, list):
            parts.append("Products and services: " + ", ".join(offerings))

    if company.get("target_markets"):
        markets = company["target_markets"]
        if isinstance(markets, list):
            parts.append("Target markets: " + ", ".join(markets))

    # Tertiary: industry classification
    if company.get("primary_naics"):
        naics = company["primary_naics"]
        if isinstance(naics, dict) and naics.get("label"):
            parts.append("Industry: " + naics["label"])

    # Context: business model and location
    if company.get("business_model"):
        bm = company["business_model"]
        if isinstance(bm, list):
            parts.append("Business model: " + ", ".join(bm))

    if company.get("address"):
        parts.append("Location: " + company["address"])

    return " | ".join(parts)
```

### Step 3: Encode and Rank

```python
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def rank_by_similarity(query: str, companies: list, model, top_k: int = 50) -> list:
    """
    Rank companies by cosine similarity to query.
    Returns list of (company, score) tuples sorted by score descending.
    """
    # Encode query
    query_embedding = model.encode([query])

    # Encode companies
    company_texts = [build_company_embedding_text(c) for c in companies]
    company_embeddings = model.encode(company_texts, show_progress_bar=True)

    # Compute similarities
    similarities = cosine_similarity(query_embedding, company_embeddings)[0]

    # Sort and return top-K
    ranked_indices = np.argsort(similarities)[::-1][:top_k]
    return [(companies[i], float(similarities[i])) for i in ranked_indices]
```

### Step 4: Cache Embeddings

```python
import pickle
from pathlib import Path

CACHE_PATH = Path("data/embeddings_cache.pkl")

def load_or_compute_embeddings(companies: list, model) -> np.ndarray:
    """Load cached embeddings or compute and cache them."""
    if CACHE_PATH.exists():
        with open(CACHE_PATH, "rb") as f:
            return pickle.load(f)

    texts = [build_company_embedding_text(c) for c in companies]
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=32)

    with open(CACHE_PATH, "wb") as f:
        pickle.dump(embeddings, f)

    return embeddings
```

## Known Limitations

### Similarity != Relevance
**Problem**: Query "Companies supplying packaging for cosmetics brands" ranks cosmetics companies higher than packaging suppliers.

**Why**: Embedding models measure semantic proximity. "Cosmetics" and "packaging for cosmetics" are closer in embedding space than "packaging manufacturer" and "packaging for cosmetics".

**Mitigations**:
1. **Query reformulation**: Expand query to "packaging manufacturer supplier materials" before embedding.
2. **Field-weighted encoding**: Give more weight to `core_offerings` than `description` for supply chain queries.
3. **Negative examples**: If available, use contrastive signals.
4. **LLM fallback**: Route ambiguous results to LLM verification.

### Short/Missing Descriptions
**Problem**: Companies with short or missing descriptions get poor embeddings.

**Mitigation**: Build text from ALL available fields, not just description. Even `core_offerings` + `primary_naics` + `address` produces a usable embedding.

## Scaling Considerations

For 100K+ companies:
- Pre-compute and cache all embeddings
- Use FAISS or Annoy for approximate nearest neighbor search
- Batch encoding with `batch_size=64` or higher
- Consider dimensionality reduction (PCA) for very large datasets

```python
# FAISS example for large-scale search
import faiss

def build_faiss_index(embeddings: np.ndarray) -> faiss.IndexFlatIP:
    """Build FAISS index for fast similarity search."""
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)  # Inner product (cosine with normalized vectors)

    # Normalize for cosine similarity
    faiss.normalize_L2(embeddings)
    index.add(embeddings)
    return index
```
