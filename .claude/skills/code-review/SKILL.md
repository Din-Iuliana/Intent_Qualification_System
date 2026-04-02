---
name: code-review
description: Conduct thorough, constructive code reviews for quality and security. Use when reviewing pull requests, checking code quality, identifying bugs, or auditing security. Handles best practices, SOLID principles, security vulnerabilities, performance analysis, and testing coverage.
allowed-tools: Read Grep Glob
metadata:
  tags: code-review, code-quality, security, best-practices, PR-review
  platforms: Claude, ChatGPT, Gemini
---


# Code Review

## When to use this skill
- Reviewing pull requests
- Checking code quality
- Providing feedback on implementations
- Identifying potential bugs
- Suggesting improvements
- Security audits
- Performance analysis

## Instructions

### Step 1: Understand the context

**Read the PR description**:
- What is the goal of this change?
- Which issues does it address?
- Are there any special considerations?

**Check the scope**:
- How many files changed?
- What type of changes? (feature, bugfix, refactor)
- Are tests included?

### Step 2: High-level review

**Architecture and design**:
- Does the approach make sense?
- Is it consistent with existing patterns?
- Are there simpler alternatives?
- Is the code in the right place?

**Code organization**:
- Clear separation of concerns?
- Appropriate abstraction levels?
- Logical file/folder structure?

### Step 3: Detailed code review

**Naming**:
- [ ] Variables: descriptive, meaningful names
- [ ] Functions: verb-based, clear purpose
- [ ] Classes: noun-based, single responsibility
- [ ] Constants: UPPER_CASE for true constants
- [ ] Avoid abbreviations unless widely known

**Functions**:
- [ ] Single responsibility
- [ ] Reasonable length (< 50 lines ideally)
- [ ] Clear inputs and outputs
- [ ] Minimal side effects
- [ ] Proper error handling

**Classes and objects**:
- [ ] Single responsibility principle
- [ ] Open/closed principle
- [ ] Liskov substitution principle
- [ ] Interface segregation
- [ ] Dependency inversion

**Error handling**:
- [ ] All errors caught and handled
- [ ] Meaningful error messages
- [ ] Proper logging
- [ ] No silent failures
- [ ] User-friendly errors for UI

**Code quality**:
- [ ] No code duplication (DRY)
- [ ] No dead code
- [ ] No commented-out code
- [ ] No magic numbers
- [ ] Consistent formatting

### Step 4: Security review

**Input validation**:
- [ ] All user inputs validated
- [ ] Type checking
- [ ] Range checking
- [ ] Format validation

**Authentication & Authorization**:
- [ ] Proper authentication checks
- [ ] Authorization for sensitive operations
- [ ] Session management
- [ ] Password handling (hashing, salting)

**Data protection**:
- [ ] No hardcoded secrets
- [ ] Sensitive data encrypted
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] CSRF protection

**Dependencies**:
- [ ] No vulnerable packages
- [ ] Dependencies up-to-date
- [ ] Minimal dependency usage

### Step 5: Performance review

**Algorithms**:
- [ ] Appropriate algorithm choice
- [ ] Reasonable time complexity
- [ ] Reasonable space complexity
- [ ] No unnecessary loops

**Database**:
- [ ] Efficient queries
- [ ] Proper indexing
- [ ] N+1 query prevention
- [ ] Connection pooling

**Caching**:
- [ ] Appropriate caching strategy
- [ ] Cache invalidation handled
- [ ] Memory usage reasonable

**Resource management**:
- [ ] Files properly closed
- [ ] Connections released
- [ ] Memory leaks prevented

### Step 6: Testing review

**Test coverage**:
- [ ] Unit tests for new code
- [ ] Integration tests if needed
- [ ] Edge cases covered
- [ ] Error cases tested

**Test quality**:
- [ ] Tests are readable
- [ ] Tests are maintainable
- [ ] Tests are deterministic
- [ ] No test interdependencies
- [ ] Proper test data setup/teardown

### Step 7: Documentation review

**Code comments**:
- [ ] Complex logic explained
- [ ] No obvious comments
- [ ] TODOs have tickets
- [ ] Comments are accurate

**Function documentation**:
```python
def calculate_total(items: List[Item], tax_rate: float) -> Decimal:
    """
    Calculate the total price including tax.

    Args:
        items: List of items to calculate total for
        tax_rate: Tax rate as decimal (e.g., 0.1 for 10%)

    Returns:
        Total price including tax

    Raises:
        ValueError: If tax_rate is negative
    """
    pass
```

### Step 8: Provide feedback

**Be constructive**:
```
Good:
"Consider extracting this logic into a separate function for better
testability and reusability."

Bad:
"This is wrong. Rewrite it."
```

**Prioritize issues**:
- Critical: Security, data loss, major bugs
- Important: Performance, maintainability
- Nice-to-have: Style, minor improvements

## Common issues

### Anti-patterns

**God class**:
```python
# Bad: One class doing everything
class UserManager:
    def create_user(self): pass
    def send_email(self): pass
    def process_payment(self): pass
    def generate_report(self): pass
```

**Magic numbers**:
```python
# Bad
if user.age > 18:
    pass

# Good
MINIMUM_AGE = 18
if user.age > MINIMUM_AGE:
    pass
```

### Security vulnerabilities

**SQL Injection**:
```python
# Bad
query = f"SELECT * FROM users WHERE id = {user_id}"

# Good
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))
```

**Hardcoded secrets**:
```python
# Bad
API_KEY = "sk-1234567890abcdef"

# Good
API_KEY = os.environ.get("API_KEY")
```

## References

- [Google Code Review Guidelines](https://google.github.io/eng-practices/review/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Clean Code by Robert C. Martin](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)
