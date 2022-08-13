from typing import Optional
from dataclasses import dataclass


@dataclass
class User:
    id: str
    name: str
    username: str


@dataclass
class Tweet:
    id: str
    author_id: str
    text: Optional[str] = None
