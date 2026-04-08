import re
from src.query_analyzer.constants import BUSINESS_MODELS


def extract_business_model(query: str) -> dict:
    found = []
    for model in BUSINESS_MODELS:
        pattern = r"\b" + re.escape(model) + r"\b"
        if re.search(pattern, query, re.IGNORECASE):
            found.append(model)
    if found:
        return {"business_model": found}
    return {}