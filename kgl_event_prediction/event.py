from dataclasses import dataclass
from typing import Optional

@dataclass
class Event:
    title: str
    year: int
    acronym: str
    homepage: Optional[str] = ""
