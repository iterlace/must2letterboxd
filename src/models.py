import datetime as dt
from dataclasses import dataclass
from typing import Optional


@dataclass
class Movie:
    must_id: int
    name: str
    released: Optional[dt.date]


@dataclass
class Want:
    movie: Movie
    added: dt.date


@dataclass
class Watched:
    movie: Movie
    added: dt.date
    rate: Optional[int]  # 1-10
    review: Optional[dict] #review dictionary, as a dict, "body" is the review text
