import pandas as pd
import pytest 
from src.filters import StructuredFilter

@pytest.fixture                                                                                                                                                                                              
def companies_df():                                                                                                                                                                                          
    return pd.DataFrame([                                                                                                                                                                                    
        {
            "operational_name": "AlphaSoft",
            "country_code": "de",
            "is_public": True,
            "business_model": ["Business-to-Business", "Software-as-a-Service"],
            "employee_count": 1500.0,
            "revenue": 200_000_000.0,
            "year_founded": 2010,
        },
        {
            "operational_name": "BetaCorp",
            "country_code": "fr",
            "is_public": False,
            "business_model": ["Business-to-Consumer", "E-commerce"],
            "employee_count": 50.0,
            "revenue": 5_000_000.0,
            "year_founded": 2020,
        },
        {
            "operational_name": "GammaInc",
            "country_code": "us",
            "is_public": True,
            "business_model": ["Business-to-Business", "Manufacturing"],
            "employee_count": 10_000.0,
            "revenue": 1_500_000_000.0,
            "year_founded": 1995,
        },
        {
            "operational_name": "DeltaLLC",
            "country_code": "ro",
            "is_public": False,
            "business_model": ["Service Provider"],
            "employee_count": float("nan"),
            "revenue": float("nan"),
            "year_founded": "unknown",
        },
        {
            "operational_name": "EpsilonAG",
            "country_code": "de",
            "is_public": True,
            "business_model": ["Subscription-Based", "Software-as-a-Service"],
            "employee_count": 800.0,
            "revenue": 80_000_000.0,
            "year_founded": 2018,
        },
    ])


def test_empty_filters_returns_all(companies_df):
    result = StructuredFilter(companies_df).apply({})
    assert len(result) == 5


def test_country_single(companies_df):
    result = StructuredFilter(companies_df).apply({"country": ["de"]})
    assert set(result["operational_name"]) == {"AlphaSoft", "EpsilonAG"}

def test_country_multiple(companies_df):
    result = StructuredFilter(companies_df).apply({"country": ["de", "fr"]})
    assert len(result) == 3


def test_is_public_true(companies_df):
    result = StructuredFilter(companies_df).apply({"is_public": True})
    assert len(result) == 3
    assert all(result["is_public"])

def test_is_public_false(companies_df):
    result = StructuredFilter(companies_df).apply({"is_public": False})
    assert len(result) == 2



def test_business_model_b2b(companies_df):
    result = StructuredFilter(companies_df).apply({"business_model": ["B2B"]})
    assert set(result["operational_name"]) == {"AlphaSoft", "GammaInc"}

def test_business_model_saas(companies_df):
    result = StructuredFilter(companies_df).apply({"business_model": ["SaaS"]})
    assert set(result["operational_name"]) == {"AlphaSoft", "EpsilonAG"}

def test_business_model_subscription(companies_df):
    result = StructuredFilter(companies_df).apply({"business_model": ["subscription"]})
    assert set(result["operational_name"]) == {"EpsilonAG"}

def test_business_model_or_semantics(companies_df):
    result = StructuredFilter(companies_df).apply({"business_model": ["B2B", "SaaS"]})
    assert set(result["operational_name"]) == {"AlphaSoft", "GammaInc", "EpsilonAG"}

def test_business_model_marketplace_skipped(companies_df):
    result = StructuredFilter(companies_df).apply({"business_model": ["marketplace"]})
    assert len(result) == 5

def test_business_model_freemium_skipped(companies_df):
    result = StructuredFilter(companies_df).apply({"business_model": ["freemium"]})
    assert len(result) == 5


def test_min_employees(companies_df):
    result = StructuredFilter(companies_df).apply({"min_employees": 1000})
    assert set(result["operational_name"]) == {"AlphaSoft", "GammaInc"}

def test_max_employees(companies_df):
    result = StructuredFilter(companies_df).apply({"max_employees": 100})
    assert set(result["operational_name"]) == {"BetaCorp"}

def test_employee_nan_excluded(companies_df):
    result = StructuredFilter(companies_df).apply({"min_employees": 1})
    assert "DeltaLLC" not in result["operational_name"].values


def test_min_revenue(companies_df):
    result = StructuredFilter(companies_df).apply({"min_revenue": 100_000_000})
    assert set(result["operational_name"]) == {"AlphaSoft", "GammaInc"}

def test_max_revenue(companies_df):
    result = StructuredFilter(companies_df).apply({"max_revenue": 50_000_000})
    assert set(result["operational_name"]) == {"BetaCorp"}



def test_min_year_founded(companies_df):
    result = StructuredFilter(companies_df).apply({"min_year_founded": 2018})
    assert set(result["operational_name"]) == {"BetaCorp", "EpsilonAG"}

def test_max_year_founded(companies_df):
    result = StructuredFilter(companies_df).apply({"max_year_founded": 2000})
    assert set(result["operational_name"]) == {"GammaInc"}

def test_year_founded_object_dtype_coerce(companies_df):
    result = StructuredFilter(companies_df).apply({"min_year_founded": 1900})
    assert "DeltaLLC" not in result["operational_name"].values


def test_combined_filters(companies_df):
    result = StructuredFilter(companies_df).apply({
        "country": ["de"],
        "is_public": True,
        "business_model": ["SaaS"],
        "min_employees": 1000,
    })
    assert set(result["operational_name"]) == {"AlphaSoft"}

def test_combined_no_matches(companies_df):
    result = StructuredFilter(companies_df).apply({
        "country": ["fr"],
        "min_employees": 1_000_000,
    })
    assert len(result) == 0