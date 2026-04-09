import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

class EmbeddingRanker:
    def __init__(self, model: SentenceTransformer, embeddings: np.ndarray):
        self.model = model
        self.embeddings = embeddings

    def rank(self, query: str, candidates: pd.DataFrame, top_k: int) -> pd.DataFrame:
        if len(candidates) == 0:
            return candidates

        query_embedding = self.model.encode(query, normalize_embeddings = True)
        candidate_embeddings = self.embeddings[candidates.index.values]   

        scores = candidate_embeddings @ query_embedding

        result = candidates.copy()
        result["similarity"] = scores
        return result.sort_values("similarity",ascending=False).head(top_k)