from dataclasses import dataclass, asdict


@dataclass
class User:
    id: str
    name: str
    username: str
    followers_count: int

    def __repr__(self):
        return f"{self.username}"

    def __hash__(self):
        return int(self.id)

    dict = asdict


@dataclass
class Tweet:
    id: str
    author: User
    like_count: int
    url: str

    def __hash__(self):
        return int(self.id)

    def __repr__(self):
        return f"@{self.author} {self.id}"

    dict = asdict
