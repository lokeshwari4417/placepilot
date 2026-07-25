import os

from .base import BaseAIProvider


class OpenAIProvider(BaseAIProvider):
    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")

    def generate(self, prompt: str, context: dict | None = None) -> str:
        # Placeholder: wire up the OpenAI SDK call here.
        # Kept isolated so swapping providers never touches calling code.
        raise NotImplementedError("Connect the OpenAI client here.")
