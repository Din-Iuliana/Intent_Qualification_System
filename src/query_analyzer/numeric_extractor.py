import re
from src.query_analyzer.constants import NUMERIC_KEYWORDS, MIN_OPERATORS, MAX_OPERATORS
from src.query_analyzer.number_parser import parse_number

NUMBER_PATTERN = r"\$?\b\d[\d,\.]*\s*(?:billion|million|thousand|bn|b|m|k)?\b"
CONTEXT_WINDOW = 40
OPERATOR_WINDOW = 20


def extract_numeric(query: str) -> dict:
    result = {}
    result.update(_extract_filter(query, "employees"))
    result.update(_extract_filter(query, "revenue"))
    result.update(_extract_filter(query, "year_founded"))
    return result


def _extract_filter(query: str, filter_type: str) -> dict:
    keywords = NUMERIC_KEYWORDS[filter_type]

    keyword_span = _find_keyword(query, keywords)
    if keyword_span is None:
        return {}

    kw_start, kw_end = keyword_span

    number_abs_start, number_text = _find_nearest_number(query, kw_start, kw_end)
    if number_text is None:
        return {}

    try:
        number = parse_number(number_text)
    except (ValueError, IndexError):
        return {}

    op_start = max(0, number_abs_start - OPERATOR_WINDOW)
    operator = _find_operator_in_context(query[op_start:number_abs_start])

    if operator == "min":
        return {f"min_{filter_type}": number}
    if operator == "max":
        return {f"max_{filter_type}": number}
    if filter_type == "year_founded":
        return {f"min_{filter_type}": number, f"max_{filter_type}": number}
    return {f"min_{filter_type}": number}


def _find_keyword(query: str, keywords: list):
    sorted_kws = sorted(keywords, key=len, reverse=True)
    for kw in sorted_kws:
        pattern = r"\b" + re.escape(kw) + r"\b"
        match = re.search(pattern, query)
        if match:
            return match.start(), match.end()
    return None


def _find_nearest_number(query: str, kw_start: int, kw_end: int):
    forward = query[kw_end:kw_end + CONTEXT_WINDOW]
    match = re.search(NUMBER_PATTERN, forward, re.IGNORECASE)
    if match:
        return kw_end + match.start(), match.group()
      
    backward_start = max(0, kw_start - CONTEXT_WINDOW)
    backward = query[backward_start:kw_start]
    matches = list(re.finditer(NUMBER_PATTERN, backward, re.IGNORECASE))
    if matches:
        last = matches[-1]
        return backward_start + last.start(), last.group()

    return -1, None


def _find_operator_in_context(context: str) -> str:
    for op in MIN_OPERATORS:
        if op in context:
            return "min"
    for op in MAX_OPERATORS:
        if op in context:
            return "max"
    return None