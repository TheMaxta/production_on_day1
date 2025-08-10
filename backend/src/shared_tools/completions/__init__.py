from typing import Literal
from app_config import AppConfig
from .base import BaseCompletions
from .openai_provider import OpenAICompletions, OpenAISettings
from .anthropic_provider import AnthropicCompletions, AnthropicSettings
from .secrets import load_secret_string

ProviderName = Literal["openai","anthropic"]

def build_completions(cfg: AppConfig) -> BaseCompletions:
    if cfg.provider == "openai":
        key = cfg.openai_key or (cfg.openai_secret_name and load_secret_string(cfg.openai_secret_name, cfg.region)) or ""
        if not key:
            raise RuntimeError("OpenAI API key not configured")
        return OpenAICompletions(OpenAISettings(
            api_key=key,
            small_model=cfg.small_model,
            vlm_model=cfg.vlm_model,
            thinking_model=cfg.thinking_model,
        ))
    if cfg.provider == "anthropic":
        if not cfg.anthropic_key:
            raise RuntimeError("Anthropic API key not configured")
        return AnthropicCompletions(AnthropicSettings(
            api_key=cfg.anthropic_key,
            small_model=cfg.small_model,
            vlm_model=cfg.vlm_model,
            thinking_model=cfg.thinking_model,
        ))
    raise ValueError(f"Unsupported provider: {cfg.provider}")
