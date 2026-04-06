from src.utils.text_processing import build_company_text

def test_build_text_with_full_company():
    company = {
        "description" : "We sell Software.",
        "core_offerings" : ["CRM","ERP"],
        "target_markets" : ["EU","US"],
        "industry_label" : "Software Publishers",
        "business_model": ["B2B","SaaS"],
        "address_parsed" : {"town":"Berlin","region_name":"Berlin"}
    }
    result = build_company_text(company)

    assert "We sell Software." in result
    assert "Products and services: CRM, ERP" in result
    assert "Target markets: EU, US" in result
    assert "Industry: Software Publishers" in result
    assert "Business model: B2B, SaaS" in result
    assert "Location: Berlin, Berlin" in result

def test_build_text_returns_string():
    company = {"description": "Test"}
    result = build_company_text(company)
    assert isinstance(result,str)    

def test_build_text_empty_dict_returns_empty_string():
    result = build_company_text({})
    assert result  == ""    

def test_build_text_only_description():
    company = {"description":"Just a description"}
    result = build_company_text(company)
    assert result == "Just a description"    

def test_build_text_skips_unknown_industry():
    company = {
        "description": "Test company",
        "industry_label" : "unknown",
    }    
    result = build_company_text(company)
    assert "Industry" not in result
    assert "unknown" not in result

def test_build_text_skips_missing_fields():
    company = {
        "description": "A company",
        "core_offerings" : ["Product A"]
    }    
    result = build_company_text(company)
    assert "A company" in result
    assert "Products and services: Product A" in result
    assert "Target markets" not in result
    assert "Industry" not in result
    assert "Business model" not in result
    assert "Location" not in result

def test_build_text_uses_pipe_separator():
    company = {
        "description": "Desc",
        "core_offerings" : ["X"],
    }
    result = build_company_text(company)
    assert " | " in result

def test_build_text_handles_partial_address():
    company = {
        "description" : "Test",
        "address_parsed" :{"town":"Paris", "region_name" : ""},
    }    
    result = build_company_text(company)
    assert "Location: Paris" in result

def test_build_text_ignore_non_list_offerings():
    company = {
        "description" : "Test",
        "core_offerings" : "not a list",
    }    
    result = build_company_text(company)
    assert "Products and services" not in result
    