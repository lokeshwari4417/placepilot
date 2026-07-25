import os

from .base import BaseAIProvider
from .openai_provider import OpenAIProvider

_PROVIDERS = {
    "openai": OpenAIProvider,
    # "gemini": GeminiProvider,   # add when implemented
    # "claude": ClaudeProvider,   # add when implemented
}


def get_ai_provider() -> BaseAIProvider:
    provider_name = os.environ.get("AI_PROVIDER", "openai")
    provider_cls = _PROVIDERS.get(provider_name)
    if provider_cls is None:
        raise ValueError(f"Unknown AI_PROVIDER '{provider_name}'")
    return provider_cls()
