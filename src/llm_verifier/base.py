from abc import ABC, abstractmethod                                                                                                                                                                          
from dataclasses import dataclass                                                                                                                                                                            


@dataclass
class VerificationResult:
    qualified: bool
    reason: str
    raw_response: str


class BaseLLMVerifier(ABC):
    @abstractmethod
    def verify(
        self,
        query: str,
        company_description: str,
        company_name: str = "",
        structured_context: str = "",
    ) -> VerificationResult:
        """Decide whether a company matches the user query."""
        ...