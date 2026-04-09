import numpy as np
import pandas as pd
import pytest
from src.ranker import EmbeddingRanker


class FakeModel:
    def __init__(self, mapping):
        self.mapping = mapping

    def encode(self, text, normalize_embeddings=True):
        if text not in self.mapping:
            raise KeyError(f"FakeModel has no mapping for: {text}")
        return self.mapping[text]


@pytest.fixture
def candidates_df():
    return pd.DataFrame([
        {"operational_name": "AlphaCorp", "description": "Alpha description"},
        {"operational_name": "BetaCorp", "description": "Beta description"},
        {"operational_name": "GammaCorp", "description": "Gamma description"},
        {"operational_name": "DeltaCorp", "description": "Delta description"},
    ])


@pytest.fixture
def normalized_embeddings():
    return np.array([
        [1.0, 0.0, 0.0],          
        [0.0, 1.0, 0.0],         
        [0.0, 0.0, 1.0],          
        [0.7071, 0.7071, 0.0],    
    ])


def test_perfect_match_alpha(candidates_df, normalized_embeddings):
    model = FakeModel({"alpha query": np.array([1.0, 0.0, 0.0])})
    ranker = EmbeddingRanker(model, normalized_embeddings)
    result = ranker.rank("alpha query", candidates_df, top_k=1)
    assert result.iloc[0]["operational_name"] == "AlphaCorp"
    assert result.iloc[0]["similarity"] == pytest.approx(1.0)

def test_perfect_match_beta(candidates_df, normalized_embeddings):
    model = FakeModel({"beta query": np.array([0.0, 1.0, 0.0])})
    ranker = EmbeddingRanker(model, normalized_embeddings)
    result = ranker.rank("beta query", candidates_df, top_k=1)
    assert result.iloc[0]["operational_name"] == "BetaCorp"


def test_top_k_returns_correct_count(candidates_df, normalized_embeddings):
    model = FakeModel({"q": np.array([1.0, 0.0, 0.0])})
    ranker = EmbeddingRanker(model, normalized_embeddings)
    result = ranker.rank("q", candidates_df, top_k=3)
    assert len(result) == 3

def test_top_k_larger_than_candidates(candidates_df, normalized_embeddings):
    model = FakeModel({"q": np.array([1.0, 0.0, 0.0])})
    ranker = EmbeddingRanker(model, normalized_embeddings)
    result = ranker.rank("q", candidates_df, top_k=100)
    assert len(result) == 4


def test_results_sorted_descending(candidates_df, normalized_embeddings):
    model = FakeModel({"q": np.array([1.0, 0.0, 0.0])})
    ranker = EmbeddingRanker(model, normalized_embeddings)
    result = ranker.rank("q", candidates_df, top_k=4)
    similarities = result["similarity"].tolist()
    assert similarities == sorted(similarities, reverse=True)

def test_similarity_column_added(candidates_df, normalized_embeddings):
    model = FakeModel({"q": np.array([1.0, 0.0, 0.0])})
    ranker = EmbeddingRanker(model, normalized_embeddings)
    result = ranker.rank("q", candidates_df, top_k=4)
    assert "similarity" in result.columns


def test_empty_candidates_returns_empty(candidates_df, normalized_embeddings):
    model = FakeModel({})
    ranker = EmbeddingRanker(model, normalized_embeddings)
    empty_df = candidates_df.iloc[0:0]
    result = ranker.rank("q", empty_df, top_k=10)
    assert len(result) == 0


def test_filtered_indices_respected(candidates_df, normalized_embeddings):
    model = FakeModel({"beta query": np.array([0.0, 1.0, 0.0])})
    ranker = EmbeddingRanker(model, normalized_embeddings)
    filtered = candidates_df.iloc[[1, 2]]  
    result = ranker.rank("beta query", filtered, top_k=2)
    assert result.iloc[0]["operational_name"] == "BetaCorp"
    assert result.iloc[0]["similarity"] == pytest.approx(1.0)


def test_does_not_mutate_input(candidates_df, normalized_embeddings):
    model = FakeModel({"q": np.array([1.0, 0.0, 0.0])})
    ranker = EmbeddingRanker(model, normalized_embeddings)
    _ = ranker.rank("q", candidates_df, top_k=4)
    assert "similarity" not in candidates_df.columns