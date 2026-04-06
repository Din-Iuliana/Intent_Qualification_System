import pandas as pd
import numpy as np 
from src.utils.data_loader import safe_parse, load_companies

# Tests for safe_parse
def test_safe_parse_valid_dict_string():
    input_str = "{'country_code':'ro', 'town':'Bucharest'}"
    result = safe_parse(input_str)
    assert result == {"country_code":"ro", "town":"Bucharest"}
    assert isinstance(result,dict)


def test_safe_parse_valid_list_string():
    input_str = "['logistic','transport']"
    result = safe_parse(input_str)
    assert result == ["logistic","transport"]
    assert isinstance(result,list)

def test_safe_parse_none_returns_none():
    assert safe_parse(None) is None

def test_safe_parse_nan_returns_none():
    assert safe_parse(np.nan) is None

def test_safe_parse_already_dict():
    input_dict = {"country_code":"de"}
    result = safe_parse(input_dict)
    assert result == input_dict

def test_safe_parse_already_list():
    input_list = ["a","b","c"]
    result = safe_parse(input_list)
    assert result == input_list

def test_safe_parse_invalid_string_returns_none():
    assert safe_parse("not a valid dict") is None

def test_safe_parse_empty_string_returns_none():
    assert safe_parse("") is None        

#Tests for load_companies
def test_load_companies():
    df = load_companies()
    assert isinstance(df,pd.DataFrame)

def test_load_companies_not_empty():
    df = load_companies()
    assert len(df )> 0    

def test_load_companies_has_expected_columns():
    df = load_companies()
    expected_columns = [
        "address_parsed",
        "country_code",
        "naics_parsed",
        "industry_label",
        "naics_code",
        "year_founded"
    ]    
    for col in expected_columns:
        assert col in df.columns, f"Missing column: {col}"

def test_load_companies_country_code_is_string():
    df = load_companies()
    assert df["country_code"].apply(lambda x: isinstance(x,str)).all()

def test_load_companies_industry_label_is_string():
    df = load_companies()
    assert df["industry_label"].apply(lambda x: isinstance(x,str)).all()

def test_load_companies_year_founded_is_int_or_none():
    df = load_companies()                
    for val in df["year_founded"]:
        assert val is None or isinstance(val,int)