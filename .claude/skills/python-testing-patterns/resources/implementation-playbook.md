# Python Testing Patterns Implementation Playbook

This file contains detailed patterns, checklists, and code samples referenced by the skill.

# Python Testing Patterns

Comprehensive guide to implementing robust testing strategies in Python using pytest, fixtures, mocking, parameterization, and test-driven development practices.

## When to Use This Skill

- Writing unit tests for Python code
- Setting up test suites and test infrastructure
- Implementing test-driven development (TDD)
- Creating integration tests for APIs and services
- Mocking external dependencies and services
- Testing async code and concurrent operations
- Setting up continuous testing in CI/CD
- Implementing property-based testing
- Testing database operations
- Debugging failing tests

## Core Concepts

### 1. Test Types
- **Unit Tests**: Test individual functions/classes in isolation
- **Integration Tests**: Test interaction between components
- **Functional Tests**: Test complete features end-to-end
- **Performance Tests**: Measure speed and resource usage

### 2. Test Structure (AAA Pattern)
- **Arrange**: Set up test data and preconditions
- **Act**: Execute the code under test
- **Assert**: Verify the results

### 3. Test Coverage
- Measure what code is exercised by tests
- Identify untested code paths
- Aim for meaningful coverage, not just high percentages

### 4. Test Isolation
- Tests should be independent
- No shared state between tests
- Each test should clean up after itself

## Quick Start

```python
# test_example.py
def add(a, b):
    return a + b

def test_add():
    """Basic test example."""
    result = add(2, 3)
    assert result == 5

def test_add_negative():
    """Test with negative numbers."""
    assert add(-1, 1) == 0

# Run with: pytest test_example.py
```

## Fundamental Patterns

### Pattern 1: Basic pytest Tests

```python
import pytest

class Calculator:
    def add(self, a: float, b: float) -> float:
        return a + b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

def test_addition():
    calc = Calculator()
    assert calc.add(2, 3) == 5
    assert calc.add(-1, 1) == 0

def test_division_by_zero():
    calc = Calculator()
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calc.divide(5, 0)
```

### Pattern 2: Fixtures for Setup and Teardown

```python
import pytest
from typing import Generator

@pytest.fixture
def db() -> Generator:
    database = Database("sqlite:///:memory:")
    database.connect()
    yield database
    database.disconnect()

def test_database_query(db):
    results = db.query("SELECT * FROM users")
    assert len(results) == 1

@pytest.fixture(scope="session")
def app_config():
    return {
        "database_url": "postgresql://localhost/test",
        "api_key": "test-key",
        "debug": True
    }
```

### Pattern 3: Parameterized Tests

```python
import pytest

@pytest.mark.parametrize("email,expected", [
    ("user@example.com", True),
    ("test.user@domain.co.uk", True),
    ("invalid.email", False),
    ("@example.com", False),
    ("", False),
])
def test_email_validation(email, expected):
    assert is_valid_email(email) == expected
```

### Pattern 4: Mocking with unittest.mock

```python
from unittest.mock import Mock, patch

def test_get_user_success():
    client = APIClient("https://api.example.com")

    mock_response = Mock()
    mock_response.json.return_value = {"id": 1, "name": "John Doe"}
    mock_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_response) as mock_get:
        user = client.get_user(1)
        assert user["id"] == 1
        mock_get.assert_called_once_with("https://api.example.com/users/1")
```

### Pattern 5: Testing Exceptions

```python
import pytest

def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

def test_zero_division_with_message():
    with pytest.raises(ZeroDivisionError, match="Division by zero"):
        divide(5, 0)
```

## Advanced Patterns

### Pattern 6: Testing Async Code

```python
import pytest
import asyncio

@pytest.mark.asyncio
async def test_fetch_data():
    result = await fetch_data("https://api.example.com")
    assert result["url"] == "https://api.example.com"
    assert "data" in result
```

### Pattern 7: Monkeypatch for Testing

```python
def test_database_url_custom(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://localhost/test")
    assert get_database_url() == "postgresql://localhost/test"

def test_database_url_not_set(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    assert get_database_url() == "sqlite:///:memory:"
```

### Pattern 8: Temporary Files and Directories

```python
def test_file_operations(tmp_path):
    test_file = tmp_path / "test_data.txt"
    save_data(test_file, "Hello, World!")
    assert test_file.exists()
    data = load_data(test_file)
    assert data == "Hello, World!"
```

### Pattern 9: Custom Fixtures and Conftest

```python
# conftest.py
import pytest

@pytest.fixture(scope="session")
def database_url():
    return "postgresql://localhost/test_db"

@pytest.fixture
def sample_user():
    return {"id": 1, "name": "Test User", "email": "test@example.com"}
```

### Pattern 10: Property-Based Testing

```python
from hypothesis import given, strategies as st

@given(st.text())
def test_reverse_twice_is_original(s):
    assert reverse_string(reverse_string(s)) == s

@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    assert a + b == b + a
```

## Testing Best Practices

### Test Organization

```
tests/
  __init__.py
  conftest.py
  test_query_analyzer.py
  test_structured_filter.py
  test_embedding_ranker.py
  test_llm_qualifier.py
  test_pipeline.py
```

### Test Markers

```python
@pytest.mark.slow
def test_embedding_generation():
    """Mark slow tests (embedding computation)."""
    pass

@pytest.mark.integration
def test_llm_api_call():
    """Mark tests that call external APIs."""
    pass

@pytest.mark.skip(reason="Feature not implemented yet")
def test_future_feature():
    pass
```

### Coverage Reporting

```bash
pip install pytest-cov
pytest --cov=src tests/
pytest --cov=src --cov-report=html tests/
pytest --cov=src --cov-fail-under=80 tests/
```

## Configuration Files

```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --strict-markers
    --tb=short
markers =
    slow: marks tests as slow
    integration: marks integration tests
    unit: marks unit tests
```

## Resources

- **pytest documentation**: https://docs.pytest.org/
- **unittest.mock**: https://docs.python.org/3/library/unittest.mock.html
- **hypothesis**: Property-based testing
- **pytest-asyncio**: Testing async code
- **pytest-cov**: Coverage reporting

## Best Practices Summary

1. **Write tests first** (TDD) or alongside code
2. **One assertion per test** when possible
3. **Use descriptive test names** that explain behavior
4. **Keep tests independent** and isolated
5. **Use fixtures** for setup and teardown
6. **Mock external dependencies** (LLM APIs, embedding models)
7. **Parametrize tests** to reduce duplication
8. **Test edge cases** and error conditions (missing data, empty fields)
9. **Measure coverage** but focus on quality
10. **Run tests in CI/CD** on every commit
