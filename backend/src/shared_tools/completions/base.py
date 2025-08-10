from abc import ABC, abstractmethod

class BaseCompletions(ABC):
    """Abstract interface for LLM, VLM, and thinking models."""

    @abstractmethod
    def llm(self, system: str, user: str, temperature: float = 0.2) -> str:
        raise NotImplementedError

    @abstractmethod
    def vlm(self, system: str, user: str, image_url: str, temperature: float = 0.2) -> str:
        raise NotImplementedError

    @abstractmethod
    def thinking(self, system: str, user: str, budget_tokens: int = 2048) -> str:
        raise NotImplementedError
