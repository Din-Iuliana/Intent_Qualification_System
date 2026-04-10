import pandas as pd


def build_document(company: pd.Series) -> str:
    parts = []

    if pd.notna(company.get("operational_name")):
        parts.append(company["operational_name"])

    if pd.notna(company.get("description")):
        parts.append(company["description"])

    if pd.notna(company.get("industry_label")):
        parts.append(f"Industry: {company['industry_label']}")

    if isinstance(company.get("core_offerings"), list):
        parts.append(f"Core offerings: {', '.join(company['core_offerings'])}")

    if isinstance(company.get("target_markets"), list):
        parts.append(f"Target markets: {', '.join(company['target_markets'])}")

    return " | ".join(parts)