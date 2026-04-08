from src.query_analyzer.boolean_extractor import extract_boolean

def test_extract_public():
    assert extract_boolean("public companies") == {"is_public": True}

def test_extract_publicly_traded():
    assert extract_boolean("publicly traded companies") == {"is_public": True}

def test_extract_publicly_listed():
    assert extract_boolean("publicly listed companies") == {"is_public": True}

def test_extract_listed():
    assert extract_boolean("listed companies on the stock market") == {"is_public": True}

def test_extract_ipo():
    assert extract_boolean("companies that had an ipo last year") == {"is_public": True}

def test_extract_stock_exchange():
    assert extract_boolean("companies on the stock exchange") == {"is_public": True}

def test_extract_went_public():
    assert extract_boolean("companies that went public") == {"is_public": True}


def test_republican_does_not_match_public():
    assert extract_boolean("republican party software") == {}

def test_private_company_not_public():
    assert extract_boolean("private software companies") == {}

def test_no_keyword_returns_empty():
    assert extract_boolean("software companies in germany") == {}

def test_empty_query_returns_empty():
    assert extract_boolean("") == {}