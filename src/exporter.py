import csv
from typing import List

from .models import Want, Watched


class CSVExporter:

    @classmethod
    def export_want(cls, filepath: str, movies: List[Want]):
        # Letterboxd imports movies in a reverse order
        movies = movies[::-1]

        with open(filepath, "w+", encoding="utf-8") as f:
            writer = csv.DictWriter(f, ["Title", "Year"])
            writer.writeheader()
            for movie in movies:
                writer.writerow({
                    "Title": movie.movie.name,
                    "Year": movie.movie.released.year if movie.movie.released else None,
                })

    @classmethod
    def export_watched(cls, filepath: str, movies: List[Watched]):
        # Letterboxd imports movies in a reverse order
        movies = movies[::-1]

        with open(filepath, "w+", encoding="utf-8") as f:
            writer = csv.DictWriter(f, ["Title", "Year", "Rating10", "WatchedDate", "Review"])
            writer.writeheader()
            for movie in movies:
                writer.writerow({
                    "Title": movie.movie.name,
                    "Year": movie.movie.released.year if movie.movie.released else None,
                    "Rating10": movie.rate,
                    "WatchedDate": movie.added.strftime("%Y-%m-%d"),
                    "Review": movie.review["body"] if type(movie.review) == dict else None, #If reviews exist, add them to the csv file
                })

    