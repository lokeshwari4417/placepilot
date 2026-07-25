from abc import ABC, abstractmethod


class BaseAIProvider(ABC):
    """
    Common interface every AI provider adapter must implement, so the
    rest of the app never talks to a provider SDK directly and the
    provider can be swapped via the AI_PROVIDER env var.
    """

    @abstractmethod
    def generate(self, prompt: str, context: dict | None = None) -> str:
        """Return a text completion for the given prompt/context."""
        raise NotImplementedError
