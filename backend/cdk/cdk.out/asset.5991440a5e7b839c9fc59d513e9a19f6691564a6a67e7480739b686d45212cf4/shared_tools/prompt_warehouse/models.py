from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Prompt:
    """Normalized prompt object used by completions."""
    name: str
    system: str
    user_template: str
    examples: Optional[List[str]] = None
    formatting_notes: Optional[str] = None
    # You can add role/message tuples later if you want multi-turn prompts.
