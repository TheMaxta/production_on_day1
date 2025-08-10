from dataclasses import dataclass
from .base import BaseCompletions

@dataclass
class OpenAISettings:
    api_key: str
    small_model: str
    vlm_model: str
    thinking_model: str

class OpenAICompletions(BaseCompletions):
    """OpenAI provider implementation."""
    def __init__(self, settings: OpenAISettings):
        from openai import OpenAI
        self.client = OpenAI(api_key=settings.api_key)
        self.model_small = settings.small_model
        self.model_vlm   = settings.vlm_model
        self.model_thinking = settings.thinking_model

    def llm(self, system: str, user: str, temperature: float = 0.2) -> str:
        r = self.client.chat.completions.create(
            model=self.model_small,
            messages=[{"role":"system","content":system},{"role":"user","content":user}],
            temperature=temperature,
        )
        return r.choices[0].message.content.strip() if r.choices else ""

    def vlm(self, system: str, user: str, image_url: str, temperature: float = 0.2) -> str:
        r = self.client.chat.completions.create(
            model=self.model_vlm,
            messages=[
                {"role":"system","content":system},
                {"role":"user","content":[
                    {"type":"text","text":user},
                    {"type":"image_url","image_url":{"url":image_url}}
                ]},
            ],
            temperature=temperature,
        )
        return r.choices[0].message.content.strip() if r.choices else ""

    def thinking(self, system: str, user: str, budget_tokens: int = 2048) -> str:
        r = self.client.chat.completions.create(
            model=self.model_thinking,
            messages=[{"role":"system","content":system},{"role":"user","content":user}],
            max_completion_tokens=budget_tokens,
        )
        return r.choices[0].message.content.strip() if r.choices else ""
