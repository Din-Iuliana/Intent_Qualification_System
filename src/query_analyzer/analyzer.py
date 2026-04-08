from src.query_analyzer.country_extractor import extract_country
from src.query_analyzer.boolean_extractor import extract_boolean
from src.query_analyzer.business_model_extractor import extract_business_model
from src.query_analyzer.numeric_extractor import extract_numeric


class QueryAnalyzer:
    def analyze(self, query: str) -> dict:
        normalized = query.lower().strip()

        filters = {}
        filters.update(extract_country(normalized))
        filters.update(extract_boolean(normalized))
        filters.update(extract_business_model(normalized))
        filters.update(extract_numeric(normalized))

        return {
            "filters": filters,
            "semantic_intent": normalized,
            "raw_query": query,
        }