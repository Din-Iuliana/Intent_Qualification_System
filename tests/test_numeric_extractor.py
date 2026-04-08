from src.query_analyzer.numeric_extractor import extract_numeric                                                                                                                                             

def test_more_than_employees_is_min():
    assert extract_numeric("more than 1000 employees") == {"min_employees": 1000}

def test_fewer_than_employees_is_max():
    assert extract_numeric("fewer than 200 employees") == {"max_employees": 200}

def test_over_employees_is_min():
    assert extract_numeric("over 500 employees") == {"min_employees": 500}

def test_employees_without_operator_defaults_to_min():
    assert extract_numeric("1000 employees") == {"min_employees": 1000}

def test_comma_separated_employee_count():
    assert extract_numeric("more than 1,000 employees") == {"min_employees": 1000}

def test_alternative_keyword_people():
    assert extract_numeric("with more than 100 people") == {"min_employees": 100}

def test_alternative_keyword_staff():
    assert extract_numeric("more than 50 staff") == {"min_employees": 50}


def test_revenue_over_million_is_min():
    assert extract_numeric("revenue over $50 million") == {"min_revenue": 50_000_000}

def test_revenue_under_million_is_max():
    result = extract_numeric("revenue under 50 million")
    assert result.get("max_revenue") == 50_000_000

def test_revenue_with_m_suffix():
    result = extract_numeric("revenue over $100M")
    assert result.get("min_revenue") == 100_000_000

def test_revenue_in_billions():
    result = extract_numeric("annual revenue more than 1 billion")
    assert result.get("min_revenue") == 1_000_000_000


def test_founded_in_is_exact_match():
    assert extract_numeric("founded in 2015") == {
        "min_year_founded": 2015,
        "max_year_founded": 2015,
    }

def test_founded_after_is_min_only():
    assert extract_numeric("founded after 2018") == {"min_year_founded": 2018}

def test_founded_before_is_max_only():
    assert extract_numeric("founded before 2020") == {"max_year_founded": 2020}

def test_established_in_is_exact_match():
    assert extract_numeric("established in 2010") == {
        "min_year_founded": 2010,
        "max_year_founded": 2010,
    }


def test_regression_no_false_billion_from_b2b():
    result = extract_numeric("public b2b saas companies with more than 1000 employees")
    assert result == {"min_employees": 1000}

def test_regression_revenue_picks_nearest_number():
    query = "european marketplace startups founded after 2018 with revenue under 50 million"
    result = extract_numeric(query)
    assert result.get("max_revenue") == 50_000_000

def test_regression_founded_after_is_min_not_exact():
    result = extract_numeric("founded after 2018")
    assert "min_year_founded" in result
    assert "max_year_founded" not in result
    assert result["min_year_founded"] == 2018


def test_query_1_multi_filter():
    result = extract_numeric("public b2b saas companies in germany with more than 1000 employees")
    assert result == {"min_employees": 1000}

def test_query_8_year_and_employees():
    query = "clean energy startups founded after 2018 with fewer than 200 employees"
    result = extract_numeric(query)
    assert result["min_year_founded"] == 2018
    assert "max_year_founded" not in result
    assert result["max_employees"] == 200

def test_revenue_and_employees_in_same_query():
    query = "revenue over $50 million with more than 100 employees"
    result = extract_numeric(query)
    assert result["min_revenue"] == 50_000_000
    assert result["min_employees"] == 100


def test_empty_query_returns_empty():
    assert extract_numeric("") == {}

def test_query_without_numeric_keywords_returns_empty():
    assert extract_numeric("software companies in germany") == {}

def test_number_without_relevant_keyword_returns_empty():
      assert extract_numeric("there are 1000 companies") == {}