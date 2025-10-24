import datetime
from typing import TypedDict, Literal


class Post(TypedDict):
    id: int
    content: str
    publication_date: str
    status: Literal["Published", "Draft", "Scheduled"]
    likes: int
    comments: int
    engagement_rate: float
    media_urls: list[str]
    created_at: str