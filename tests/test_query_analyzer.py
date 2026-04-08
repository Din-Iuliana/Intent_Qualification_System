from src.query_analyzer import QueryAnalyzer

def test_analyze_returns_three_keys():
    qa = QueryAnalyzer()
    result = qa.analyze("Public companies in Germany")
    assert set(result.keys()) == {"filters", "semantic_intent", "raw_query"}

def test_filters_is_a_dict():
    qa = QueryAnalyzer()
    result = qa.analyze("Public companies in Germany")
    assert isinstance(result["filters"], dict)

def test_empty_query_has_empty_filters():
    qa = QueryAnalyzer()
    result = qa.analyze("")
    assert result["filters"] == {}


def test_raw_query_preserves_original_casing():
    qa = QueryAnalyzer()
    result = qa.analyze("Public B2B SaaS Companies")
    assert result["raw_query"] == "Public B2B SaaS Companies"

def test_semantic_intent_is_lowercased():
    qa = QueryAnalyzer()
    result = qa.analyze("Public B2B SaaS Companies")
    assert result["semantic_intent"] == "public b2b saas companies"

def test_semantic_intent_is_stripped():
    qa = QueryAnalyzer()
    result = qa.analyze("   public companies   ")
    assert result["semantic_intent"] == "public companies"


def test_integration_query_1_bug_debug():
    qa = QueryAnalyzer()
    result = qa.analyze("Public B2B SaaS companies in Germany with more than 1000 employees")
    filters = result["filters"]
    assert filters["country"] == "de"
    assert filters["is_public"] is True
    assert filters["business_model"] == ["B2B", "SaaS"]
    assert filters["min_employees"] == 1000
    assert "max_employees" not in filters

def test_integration_query_2_bug_debug():
    qa = QueryAnalyzer()
    result = qa.analyze("European marketplace startups founded after 2018 with revenue under 50 million")
    filters = result["filters"]
    assert "country_in" in filters
    assert "de" in filters["country_in"]
    assert filters["business_model"] == ["marketplace"]
    assert filters["min_year_founded"] == 2018
    assert "max_year_founded" not in filters
    assert filters["max_revenue"] == 50_000_000



def test_brief_query_1_logistics_romania():
    qa = QueryAnalyzer()
    result = qa.analyze("Logistic companies in Romania")
    assert result["filters"]["country"] == "ro"

def test_brief_query_2_public_software():
    qa = QueryAnalyzer()
    result = qa.analyze("Public software companies with more than 1,000 employees")
    filters = result["filters"]
    assert filters["is_public"] is True
    assert filters["min_employees"] == 1000

def test_brief_query_5_us_construction_revenue():
    qa = QueryAnalyzer()
    result = qa.analyze("Construction companies in the United States with revenue over $50 million")
    filters = result["filters"]
    assert filters["country"] == "us"
    assert filters["min_revenue"] == 50_000_000

def test_brief_query_8_clean_energy_startups():
    qa = QueryAnalyzer()
    result = qa.analyze("Clean energy startups founded after 2018 with fewer than 200 employees")
    filters = result["filters"]
    assert filters["min_year_founded"] == 2018
    assert filters["max_employees"] == 200

def test_brief_query_11_nordic_renewables():
    qa = QueryAnalyzer()
    result = qa.analyze("Renewable energy equipment manufacturers in Scandinavia")
    assert result["filters"]["country_in"] == ["dk", "fi", "no", "se"]