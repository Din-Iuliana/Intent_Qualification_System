from src.config import EUROPEAN_COUNTRIES, SCANDINAVIAN_COUNTRIES

COUNTRY_NAMES = {
    "romania": "ro",
    "romanian": "ro",

    "france": "fr",
    "french": "fr",

    "germany": "de",
    "german": "de",
    "deutschland": "de",

    "switzerland": "ch",
    "swiss": "ch",
   
    "united states": "us",
    "usa": "us",
    "u.s.a.": "us",
    "u.s.": "us",
    "america": "us",
    "american": "us",
   
    "united kingdom": "gb",
    "uk": "gb",
    "britain": "gb",
    "british": "gb",
    "england": "gb",
    "english": "gb",

    "italy": "it",
    "italian": "it",

    "spain": "es",
    "spanish": "es",

    "netherlands": "nl",
    "dutch": "nl",
    "holland": "nl",

    "poland": "pl",
    "polish": "pl",

    "sweden": "se",
    "swedish": "se",

    "norway": "no",
    "norwegian": "no",

    "denmark": "dk",
    "danish": "dk",

    "finland": "fi",
    "finnish": "fi",

    "austria": "at",
    "austrian": "at",
    "belgium": "be",
    "belgian": "be",
    "ireland": "ie",
    "irish": "ie",
    "portugal": "pt",
    "portuguese": "pt",
    "greece": "gr",
    "greek": "gr",
    "czech republic": "cz",
    "czech": "cz",
    "hungary": "hu",
    "hungarian": "hu",
}

REGION_NAMES = {
    "europe": EUROPEAN_COUNTRIES,
    "european": EUROPEAN_COUNTRIES,
    "eu": EUROPEAN_COUNTRIES,
    "scandinavia": SCANDINAVIAN_COUNTRIES,
    "scandinavian": SCANDINAVIAN_COUNTRIES,
    "nordic": SCANDINAVIAN_COUNTRIES,
    "nordics": SCANDINAVIAN_COUNTRIES,
}

MIN_OPERATORS = [
    "more than",
    "over",
    "above",
    "greater than",
    "exceeding",
    "at least",
    "minimum of",
    "with over",
    "with at least",
    "no fewer than",
    "no less than",
    "after",
    "since",
    ">",
]

MAX_OPERATORS = [
    "less than",
    "fewer than",
    "under",
    "below",
    "at most",
    "maximum of",
    "no more than",
    "with less than",
    "with fewer than",
    "before",
    "<",
]

NUMERIC_KEYWORDS = {
    "employees": [
        "employees", "employee", "people", "staff",
        "headcount", "workers", "workforce", "team",
        "team members", "personnel", "emps",
    ],
    "revenue": [
        "revenue", "revenues", "sales", "turnover",
        "annual revenue", "yearly revenue", "income",
    ],
    "year_founded": [
        "founded", "established", "founded in", "established in",
        "since", "from", "incorporated", "incorporated in",
    ],
}

BUSINESS_MODELS = [
    "B2B",
    "B2C",
    "SaaS",
    "marketplace",
    "subscription",
    "freemium",
]

PUBLIC_KEYWORDS = [
    "public",
    "publicly traded",
    "publicly listed",
    "listed",
    "ipo",
    "stock exchange",
]