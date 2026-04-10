import re                                                                                                                                                                                                    
from groq import Groq, RateLimitError
import time                                                                                                                                                                                    

from src.llm_verifier.base import BaseLLMVerifier, VerificationResult
from src.llm_verifier.prompts import build_messages


class GroqVerifier(BaseLLMVerifier):
    def __init__(
        self,
        api_key: str,
        model: str,
        temperature: float = 0.0,
        max_tokens: int = 200,
        timeout: int = 30,
        max_retries: int = 2,
        retry_wait: int = 60,
):
        self.client = Groq(api_key=api_key, timeout=timeout)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.max_retries = max_retries
        self.retry_wait = retry_wait

    def verify(
        self,
        query: str,
        company_description: str,
        company_name: str = "",
        structured_context: str = "",
    ) -> VerificationResult:
        messages = build_messages(
            query, company_description, company_name, structured_context
        )

        for attempt in range(self.max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                )
                break
            except RateLimitError:
                if attempt == self.max_retries - 1:
                    raise
                print(f"  [Rate limit] Waiting {self.retry_wait}s... (attempt {attempt + 1}/{self.max_retries})")
                time.sleep(self.retry_wait)

        raw_response = response.choices[0].message.content
        qualified, reason = self._parse(raw_response)

        return VerificationResult(
            qualified=qualified,
            reason=reason,
            raw_response=raw_response,
        )

    @staticmethod
    def _parse(raw_response: str) -> tuple[bool, str]:
        decision_match = re.search(r"DECISION:\s*(YES|NO)", raw_response, re.IGNORECASE)
        reason_match = re.search(r"REASON:\s*(.+)", raw_response, re.IGNORECASE)
        criteria_match = re.search(r"CRITERIA:\s*(.+?)(?=\nDECISION:)", raw_response, re.IGNORECASE | re.DOTALL)

        if decision_match is None:
            return False, f"Parse error: {raw_response[:100]}"

        qualified = decision_match.group(1).upper() == "YES"
        reason = reason_match.group(1).strip() if reason_match else ""

        if criteria_match:
            criteria = criteria_match.group(1).strip()
            reason = f"{criteria} | {reason}"

        return qualified, reason