import numpy as np
from sentence_transformers import SentenceTransformer  
from src.utils.data_loader import load_companies
from src.ranker.document_builder import build_document
from src.config import EMBEDDING_MODEL

OUTPUT_PATH = "data/embeddings.npy"

def main():
    print("Loading companies...")
    df = load_companies()
    print(f"Loaded {len(df)} companies")

    print(f"Loading model: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)

    print("Building documents...")
    documents = [build_document(row) for _, row in df.iterrows()]

    print("Encoding...")
    embeddings = model.encode(
        documents,
        show_progress_bar = True,
        normalize_embeddings = True
    )

    print(f"Embeddings shape: {embeddings.shape}")
    np.save(OUTPUT_PATH,embeddings)
    print(f"Saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()    