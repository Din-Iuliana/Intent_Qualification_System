from src.query_analyzer.number_parser import parse_number

def test_parse_plain_integer():
    assert parse_number("1000") == 1000

def test_parse_comma_separated():
    assert parse_number("1,000") == 1000

def test_parse_with_dollar_sign():
    assert parse_number("$50") == 50

def test_parse_year_like_number():
    assert parse_number("2018") == 2018

def test_parse_thousand_word():
    assert parse_number("5 thousand") == 5000

def test_parse_k_suffix():
    assert parse_number("5k") == 5000


def test_parse_million_word():
    assert parse_number("50 million") == 50_000_000

def test_parse_m_suffix_lowercase():
    assert parse_number("50m") == 50_000_000

def test_parse_m_suffix_uppercase():
    assert parse_number("50M") == 50_000_000

def test_parse_dollar_million():
    assert parse_number("$50 million") == 50_000_000

def test_parse_decimal_million():
    assert parse_number("1.5 million") == 1_500_000


def test_parse_billion_word():
    assert parse_number("2 billion") == 2_000_000_000

def test_parse_b_suffix():
    assert parse_number("2b") == 2_000_000_000

def test_parse_bn_suffix():
    assert parse_number("2bn") == 2_000_000_000