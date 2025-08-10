from typing import Dict
from jinja2 import Template
from .models import Prompt

class PromptWarehouse:
    """
    Stores/retrieves Prompt objects and renders Jinja templates (stub).
    """

    def __init__(self) -> None:
        self._prompts: Dict[str, Prompt] = {
            "image.describe": Prompt(
                name="image.describe",
                system="You are a helpful vision assistant. Be concise.",
                user_template="Describe this image. {{ extra | default('') }}"
            )
        }

    def get(self, name: str) -> Prompt:
        """Return a Prompt by name."""
        return self._prompts[name]

    def render_user(self, name: str, **kwargs) -> str:
        """Render the user_template using Jinja with kwargs."""
        p = self.get(name)
        return Template(p.user_template).render(**kwargs).strip()
