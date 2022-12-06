from dataclasses import dataclass


@dataclass
class Event:
    title: str
    homepage: str
    year: int
    acronym: str
