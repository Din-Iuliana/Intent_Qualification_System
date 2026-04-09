import re
from src.query_analyzer.constants import COUNTRY_NAMES, REGION_NAMES

def extract_country(query: str) -> dict:
    sorted_regions = sorted(REGION_NAMES.keys(), key=len, reverse=True)
    for region_name in sorted_regions:
        pattern = r"\b" + re.escape(region_name) + r"\b"
        if re.search(pattern, query):
            return {"country": sorted(REGION_NAMES[region_name])}

    sorted_countries = sorted(COUNTRY_NAMES.keys(), key=len, reverse=True)
    for country_name in sorted_countries:
        pattern = r"\b" + re.escape(country_name) + r"\b"
        if re.search(pattern, query):
            return {"country": [COUNTRY_NAMES[country_name]]}
        
    return {}