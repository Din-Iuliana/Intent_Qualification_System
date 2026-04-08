from src.query_analyzer.business_model_extractor import extract_business_model

def test_extract_b2b():
    assert extract_business_model("b2b companies") == {"business_model": ["B2B"]}

def test_extract_b2c():
    assert extract_business_model("b2c companies") == {"business_model": ["B2C"]}

def test_extract_saas():
    assert extract_business_model("saas companies") == {"business_model": ["SaaS"]}

def test_extract_marketplace():
    assert extract_business_model("marketplace startups") == {"business_model": ["marketplace"]}

def test_extract_subscription():
    assert extract_business_model("subscription services") == {"business_model": ["subscription"]}

def test_extract_freemium():
    assert extract_business_model("freemium apps") == {"business_model": ["freemium"]}


def test_extract_multiple_models():
    result = extract_business_model("b2b saas companies")
    assert result == {"business_model": ["B2B", "SaaS"]}


def test_preserves_original_casing():
    result = extract_business_model("b2b saas companies")
    assert "B2B" in result["business_model"]
    assert "SaaS" in result["business_model"]


def test_case_insensitive_uppercase():
    assert extract_business_model("B2B COMPANIES") == {"business_model": ["B2B"]}

def test_case_insensitive_mixed_case():
    assert extract_business_model("SaaS platforms") == {"business_model": ["SaaS"]}


def test_no_business_model_returns_empty():
    assert extract_business_model("software companies in germany") == {}

def test_empty_query_returns_empty():
    assert extract_business_model("") == {}