import pandas as pd

def build_document(company: pd.Series) -> str:                                                                                                                                                               
    return company["description"]