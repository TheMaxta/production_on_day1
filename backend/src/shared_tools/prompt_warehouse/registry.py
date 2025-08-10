from dataclasses import dataclass
from typing import Tuple
from jinja2 import Environment, DictLoader, StrictUndefined
from .prompts import PROMPTS

@dataclass(frozen=True)
class RenderedPrompt:
    name: str
    system: str
    user: str

class PromptRegistry:
    """Jinja-backed prompt loader and renderer."""
    def __init__(self, templates: dict | None = None):
        self._templates = templates or PROMPTS
        # flatten into jinja dict loader keys like "<name>/system" and "<name>/user"
        sources = {}
        for name, parts in self._templates.items():
            sources[f"{name}/system"] = parts.get("system","")
            sources[f"{name}/user"]   = parts.get("user","")
        self.env = Environment(loader=DictLoader(sources), undefined=StrictUndefined, autoescape=False)

    def render(self, name: str, **kwargs) -> RenderedPrompt:
        sys_t = self.env.get_template(f"{name}/system")
        usr_t = self.env.get_template(f"{name}/user")
        return RenderedPrompt(name=name, system=sys_t.render(**kwargs), user=usr_t.render(**kwargs))
