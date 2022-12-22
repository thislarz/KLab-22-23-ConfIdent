from dataclasses import dataclass
from typing import Optional

@dataclass
class Event:
    title: Optional[str] = ""
    year: Optional[int] = 0
    acronym: Optional[str] = ""
    homepage: Optional[str] = ""
    series_id: Optional[str] = ""
