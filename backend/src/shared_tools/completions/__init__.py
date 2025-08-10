from typing import Literal
from app_config import AppConfig
from .base import BaseCompletions
from .openai_provider import OpenAICompletions, OpenAISettings
from .anthropic_provider import AnthropicCompletions, AnthropicSettings

ProviderName = Literal["openai","anthropic"]

def build_completions(cfg: AppConfig) -> BaseCompletions:
    if cfg.provider == "openai":
        return OpenAICompletions(OpenAISettings(
            api_key=cfg.openai_key,
            small_model=cfg.small_model,
            vlm_model=cfg.vlm_model,
            thinking_model=cfg.thinking_model,
        ))
    if cfg.provider == "anthropic":
        return AnthropicCompletions(AnthropicSettings(
            api_key=cfg.anthropic_key,
            small_model=cfg.small_model,
            vlm_model=cfg.vlm_model,
            thinking_model=cfg.thinking_model,
        ))
    raise ValueError(f"Unsupported provider: {cfg.provider}")
