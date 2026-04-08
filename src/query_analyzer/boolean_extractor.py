import re
from src.query_analyzer.constants import PUBLIC_KEYWORDS

def extract_boolean(query: str) -> dict:
    sorted_keywords = sorted(PUBLIC_KEYWORDS, key=len, reverse=True)
    for keyword in sorted_keywords:
        pattern = r"\b" + re.escape(keyword) + r"\b"
        if re.search(pattern, query):
            return {"is_public": True}
    return {}