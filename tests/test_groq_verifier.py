from src.llm_verifier.groq_verifier import GroqVerifier                                                                                                                                                      
                                                                                                                                                                                                               

def test_parse_yes():
    raw = "DECISION: YES\nREASON: Clear match on both criteria."
    qualified, reason = GroqVerifier._parse(raw)
    assert qualified is True
    assert reason == "Clear match on both criteria."


def test_parse_no():
    raw = "DECISION: NO\nREASON: Company operates in retail, not software."
    qualified, reason = GroqVerifier._parse(raw)
    assert qualified is False
    assert reason == "Company operates in retail, not software."


def test_parse_case_insensitive():
    raw = "decision: yes\nreason: matches the intent."
    qualified, _ = GroqVerifier._parse(raw)
    assert qualified is True


def test_parse_malformed_defaults_to_not_qualified():
    raw = "I think this company is a good match but I'm not sure."
    qualified, reason = GroqVerifier._parse(raw)
    assert qualified is False
    assert "Parse error" in reason


def test_parse_missing_reason():
    raw = "DECISION: YES"
    qualified, reason = GroqVerifier._parse(raw)
    assert qualified is True
    assert reason == ""