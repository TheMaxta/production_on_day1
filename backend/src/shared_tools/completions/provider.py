from typing import Optional

class CompletionsClient:
    """
    Abstracts calls to the LLM provider (OpenAI etc.). Stub only.
    """

    def __init__(self, model: str, api_key: Optional[str] = None) -> None:
        self.model = model
        self.api_key = api_key

    def analyze_image_url(self, image_url: str, system: str, user: str) -> str:
        """
        Given an image URL + prompt pieces, return model text output.
        """
        raise NotImplementedError
