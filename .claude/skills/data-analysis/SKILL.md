---
name: data-analysis
description: "Analyze and explore company datasets in JSONL format. Use when exploring data quality, understanding field distributions, identifying missing data patterns, or profiling the dataset before building ML pipelines."
metadata:
  tags: data-analysis, pandas, JSONL, profiling, missing-data, EDA
  platforms: Claude
---

# Data Analysis for Company Profiles

## When to use this skill
- Exploring the companies.jsonl dataset
- Understanding field distributions and data quality
- Identifying missing data patterns
- Profiling company attributes (industries, locations, sizes)
- Validating data assumptions before building the pipeline

## Instructions

### Step 1: Load and Inspect

```python
import pandas as pd

df = pd.read_json("data/companies.jsonl", lines=True)
print(f"Total companies: {len(df)}")
print(f"Columns: {list(df.columns)}")
print(f"\nData types:\n{df.dtypes}")
```

### Step 2: Missing Data Analysis

```python
# Missing data per field
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(1)
missing_report = pd.DataFrame({"missing": missing, "pct": missing_pct})
print(missing_report.sort_values("pct", ascending=False))
```

Key questions:
- Which fields are most commonly missing?
- Are there companies with almost no data?
- Does missingness correlate with other fields?

### Step 3: Field Distributions

```python
# Categorical fields
for col in ["business_model", "is_public"]:
    print(f"\n{col} distribution:")
    print(df[col].value_counts())

# Numeric fields
for col in ["employee_count", "revenue", "year_founded"]:
    print(f"\n{col} stats:")
    print(df[col].describe())

# Location analysis
print("\nTop countries/regions:")
# Extract country from address field
```

### Step 4: NAICS Code Analysis

```python
# Analyze industry distribution
def extract_naics_label(naics):
    if isinstance(naics, dict):
        return naics.get("label", "Unknown")
    return "Missing"

df["primary_industry"] = df["primary_naics"].apply(extract_naics_label)
print(df["primary_industry"].value_counts().head(20))
```

### Step 5: Text Field Quality

```python
# Description length distribution
df["desc_length"] = df["description"].fillna("").str.len()
print(f"Description length: mean={df['desc_length'].mean():.0f}, "
      f"median={df['desc_length'].median():.0f}, "
      f"zero={sum(df['desc_length']==0)}")

# Core offerings coverage
df["has_offerings"] = df["core_offerings"].apply(lambda x: isinstance(x, list) and len(x) > 0)
print(f"Companies with core offerings: {df['has_offerings'].sum()}/{len(df)}")
```

## Output Format

Always produce:
1. **Summary statistics** — total records, field coverage percentages
2. **Distribution highlights** — key patterns in the data
3. **Data quality issues** — missing data, inconsistencies, outliers
4. **Recommendations** — how findings should influence pipeline design

## Common Data Issues

- **Inconsistent address formats**: "Munich, Germany" vs "DE" vs "Germany, Munich"
- **Nested JSON fields**: primary_naics is a dict, secondary_naics is a list of dicts
- **Mixed types in lists**: business_model and core_offerings may be strings or lists
- **Revenue/employee outliers**: extremely large or small values that may be errors
