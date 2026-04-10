import os                                                                                                                                                                                                    
from dotenv import load_dotenv

load_dotenv()

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

LLM_MODEL = "llama3"

TOP_K = 50

SIMILARITY_THRESHOLD = 0.3

EUROPEAN_COUNTRIES = {
    "al", "ad", "at", "be", "bg", "hr", "cy", "cz", "dk", "ee",
    "fi", "fr", "de", "gr", "hu", "is", "ie", "it", "lv", "li",
    "lt", "lu", "mt", "md", "mc", "me", "nl", "mk", "no", "pl",
    "pt", "ro", "rs", "sk", "si", "es", "se", "ch", "ua", "gb"
}

SCANDINAVIAN_COUNTRIES = {"se","no","dk","fi"}

DATA_PATH = "data/companies.jsonl"

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_MODEL = "llama-3.1-8b-instant"  
GROQ_TEMPERATURE = 0.0
GROQ_MAX_TOKENS = 200
GROQ_TIMEOUT = 30

LLM_CACHE_PATH = "data/llm_cache.json"