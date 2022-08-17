from dataclasses import dataclass


@dataclass
class User:
    id: str
    name: str
    username: str
    followers_count: str

    def __repr__(self):
        return f"@{self.username}"

    def __hash__(self):
        return int(self.id)


@dataclass
class Tweet:
    id: str
    author_id: str
    like_count: int

    def __hash__(self):
        return int(self.id)

    def __repr__(self):
        return self.id
