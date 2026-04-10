import hashlib
import json
from pathlib import Path

from src.llm_verifier.base import BaseLLMVerifier, VerificationResult


class CachedLLMVerifier(BaseLLMVerifier):
    def __init__(self, verifier: BaseLLMVerifier, cache_path: str, model_id: str):
        self.verifier = verifier
        self.cache_path = Path(cache_path)
        self.model_id = model_id
        self._cache = self._load_cache()

    def verify(
        self,
        query: str,
        company_description: str,
        company_name: str = "",
        structured_context: str = "",
    ) -> VerificationResult:
        key = self._make_key(query, company_description, structured_context)

        if key in self._cache:
            cached = self._cache[key]
            return VerificationResult(
                qualified=cached["qualified"],
                reason=cached["reason"],
                raw_response=cached["raw_response"],
            )

        result = self.verifier.verify(
            query, company_description, company_name, structured_context
        )
        self._cache[key] = {
            "qualified": result.qualified,
            "reason": result.reason,
            "raw_response": result.raw_response,
        }
        self._save_cache()
        return result

    def _make_key(self, query: str, company_description: str, structured_context: str = "") -> str:
        payload = f"{self.model_id}|||{query}|||{company_description}|||{structured_context}"
        return hashlib.sha256(payload.encode()).hexdigest()

    def _load_cache(self) -> dict:
        if not self.cache_path.exists():
            return {}
        with open(self.cache_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_cache(self) -> None:
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.cache_path, "w", encoding="utf-8") as f:
            json.dump(self._cache, f, indent=2, ensure_ascii=False)