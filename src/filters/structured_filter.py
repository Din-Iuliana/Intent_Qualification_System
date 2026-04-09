import pandas as pd                                                                                                                                                                                          
from src.filters.constants import BUSINESS_MODEL_MAPPING                                                                                                                                                                                                               
                                  
                                                                                                                                                                                                               
class StructuredFilter:                                                                                                                                                                                      
    def __init__(self, companies: pd.DataFrame):
        self.companies = companies

    def apply(self, filters: dict) -> pd.DataFrame:
        df = self.companies
        mask = pd.Series(True, index=df.index)

        if "country" in filters:
            mask &= df["country_code"].isin(filters["country"])

        if "is_public" in filters:
            mask &= df["is_public"] == filters["is_public"]

        if "business_model" in filters:
            mapped = [
                BUSINESS_MODEL_MAPPING[m]
                for m in filters["business_model"]
                if m in BUSINESS_MODEL_MAPPING
            ]
            if mapped:
                mask &= df["business_model"].apply(
                    lambda bms: isinstance(bms, list) and any(m in bms for m in mapped)
                )

        if "min_employees" in filters:
            mask &= df["employee_count"] >= filters["min_employees"]
        if "max_employees" in filters:
            mask &= df["employee_count"] <= filters["max_employees"]

        if "min_revenue" in filters:
            mask &= df["revenue"] >= filters["min_revenue"]
        if "max_revenue" in filters:
            mask &= df["revenue"] <= filters["max_revenue"]

        if "min_year_founded" in filters or "max_year_founded" in filters:
            years = pd.to_numeric(df["year_founded"], errors="coerce")
            if "min_year_founded" in filters:
                mask &= years >= filters["min_year_founded"]
            if "max_year_founded" in filters:
                mask &= years <= filters["max_year_founded"]

        return df[mask]