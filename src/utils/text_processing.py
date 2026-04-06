def build_company_text(company:dict) -> str:
    parts = []

    if company.get("description"):
        parts.append(company["description"])

    if company.get("core_offerings"):
        offerings= company["core_offerings"]
        if isinstance(offerings,list):
            parts.append("Products and services: " + ", ".join(offerings))

    if company.get("target_markets"):
        markets = company["target_markets"]
        if isinstance(markets,list):
            parts.append("Target markets: " + ", ".join(markets))

    if company.get("industry_label") and company["industry_label"] != "unknown":
        parts.append("Industry: " + company["industry_label"])

    if company.get("business_model"):
        bm = company["business_model"]
        if isinstance(bm,list):
            parts.append("Business model: " + ", ".join(bm))    

    if company.get("address_parsed") and isinstance(company["address_parsed"],dict):
        town = company["address_parsed"].get("town", "")
        region = company["address_parsed"].get("region_name","")
        location = ", ".join(filter(None, [town,region]))
        if location:
            parts.append("Location: " + location)

    return " | ".join(parts)        