import pandas as pd
import ast 
from src.config import DATA_PATH

def safe_parse(val):
    if isinstance(val,(dict,list)):
        return val
    if pd.isna(val):
        return None
    try:
        return ast.literal_eval(str(val))
    except (ValueError, SyntaxError):
        return None
    
def load_companies(path: str = DATA_PATH) -> pd.DataFrame:
    df = pd.read_json(path,lines=True)

    df["address_parsed"] = df["address"].apply(safe_parse)
    df["country_code"] = df["address_parsed"].apply(lambda x: x.get("country_code","unknown") if isinstance(x,dict) else "unknown")

    df["naics_parsed"] = df["primary_naics"].apply(safe_parse)
    df["industry_label"] = df["naics_parsed"].apply(lambda x: x.get("label","unknown") if isinstance(x,dict) else "unknown")

    df["naics_code"] = df["naics_parsed"].apply(lambda x: x.get("code","unknown") if isinstance(x,dict) else "unknown")

    df["year_founded"] = pd.Series([int(x) if pd.notna(x) else None for x in df["year_founded"]], dtype=object, index=df.index)

    return df