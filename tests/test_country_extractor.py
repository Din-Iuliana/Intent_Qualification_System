from src.query_analyzer.country_extractor import extract_country                                                                                                                                             

def test_extract_germany():                                                                                                                                                                                  
    assert extract_country("companies in germany") == {"country": ["de"]}                                                                                                                                    
     
def test_extract_france():                                                                                                                                                                                   
    assert extract_country("companies in france") == {"country": ["fr"]}                                                                                                                                     

def test_extract_switzerland():
    assert extract_country("pharmaceutical companies in switzerland") == {"country": ["ch"]}

def test_extract_french_adjective():
    assert extract_country("french startups") == {"country": ["fr"]}

def test_extract_german_adjective():
    assert extract_country("german software companies") == {"country": ["de"]}


def test_extract_usa_alias():
    assert extract_country("usa companies") == {"country": ["us"]}

def test_extract_united_states_multiword():
    assert extract_country("companies in the united states") == {"country": ["us"]}

def test_extract_uk_alias():
    assert extract_country("uk companies") == {"country": ["gb"]}


def test_extract_european_returns_multiple_countries():
    result = extract_country("european companies")
    assert "country" in result
    assert "de" in result["country"]
    assert "fr" in result["country"]
    assert "ro" in result["country"]

def test_extract_eu_abbreviation():
    result = extract_country("eu companies")
    assert "country" in result
    assert "de" in result["country"]

def test_extract_europe_list_is_sorted():
    result = extract_country("european companies")
    assert result["country"] == sorted(result["country"])


def test_extract_scandinavian():
    assert extract_country("scandinavian manufacturers") == {"country": ["dk", "fi", "no", "se"]}

def test_extract_nordic_same_as_scandinavian():
    assert extract_country("nordic startups") == {"country": ["dk", "fi", "no", "se"]}


def test_region_wins_over_country():
    result = extract_country("german companies in europe")
    assert len(result["country"]) > 1
    assert "de" in result["country"]


def test_no_country_returns_empty():
    assert extract_country("software companies with more than 1000 employees") == {}

def test_empty_query_returns_empty():
    assert extract_country("") == {}