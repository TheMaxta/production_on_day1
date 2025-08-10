from dataclasses import dataclass
from .base import BaseCompletions

@dataclass
class AnthropicSettings:
    api_key: str
    small_model: str
    vlm_model: str
    thinking_model: str

class AnthropicCompletions(BaseCompletions):
    """Anthropic provider implementation (stub)."""
    def __init__(self, settings: AnthropicSettings):
        self.settings = settings
        # from anthropic import Anthropic
        # self.client = Anthropic(api_key=settings.api_key)

    def llm(self, system: str, user: str, temperature: float = 0.2) -> str:
        raise NotImplementedError

    def vlm(self, system: str, user: str, image_url: str, temperature: float = 0.2) -> str:
        raise NotImplementedError

    def thinking(self, system: str, user: str, budget_tokens: int = 2048) -> str:
        raise NotImplementedError
