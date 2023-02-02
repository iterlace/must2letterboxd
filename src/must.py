import datetime as dt
from typing import Dict, Any, List

import requests

from .models import Movie, Want, Watched
from .helpers import generate_batches


class MustAccount:

    def __init__(self, username):
        self.session = requests.Session()
        self.user = self.get_user(username)
        self.user_id = self.user["id"]

    def get_user(self, username) -> Dict[str, Any]:
        response = self.session.get(f"https://mustapp.com/api/users/uri/{username}")
        if response.status_code != 200:
            raise ValueError("Error getting user info")
        return response.json()

    def get_movies(self, ids: List[int]) -> List[Movie]:
        resp = self.session.post(
            url="https://mustapp.com/api/products",
            json={"ids": ids},
        )
        assert resp.status_code == 200, \
            f"Couldn't fetch Movies ({resp.url}): {resp.content}"
        raw_movies = resp.json()

        movies = [
            Movie(
                must_id=m["id"],
                name=m["title"],
                released=(
                    dt.datetime.strptime(m["release_date"], "%Y-%m-%d").date()
                    if m["release_date"]
                    else None
                )
            )
            for m in raw_movies
        ]
        return movies

    def get_user_products(self, ids: List[int]):
        results = []
        step = 100
        for i in range(len(ids) // step + (len(ids) % step != 0)):
            resp = self.session.post(
                url=f"https://mustapp.com/api/users/id/{self.user_id}/products",
                params={"embed": "review"},
                json={"ids": ids[i * step:(i + 1) * step]},
            )
            assert resp.status_code == 200, \
                f"Couldn't fetch User Products ({resp.url}): {resp.content}"

            for item in resp.json():
                results.append(item["user_product_info"])
        return results

    def get_watched_movies(self) -> List[Watched]:
        watched_ids = self.user["lists"]["watched"]
        movies = []
        for ids in generate_batches(watched_ids, 500):
            movies.extend(self.get_movies(ids))

        watched_movies = self.get_user_products(watched_ids)
        results = []

        for m in movies:
            for wm in watched_movies:
                if m.must_id != wm["product_id"]:
                    continue

                review = None
                if wm["review"]:
                    review = wm["review"].get("body", "").strip().replace("\n", "")

                watched = Watched(
                    movie=m,
                    added=dt.datetime.strptime(
                        wm["modified_at"],
                        "%Y-%m-%dT%H:%M:%S.%fZ"
                    ).date(),
                    rate=wm["rate"],
                    review=review,
                )
                results.append(watched)
        return results

    def get_want_movies(self) -> List[Want]:
        want_ids = self.user["lists"]["want"]
        movies = []
        for ids in generate_batches(want_ids, 500):
            movies.extend(self.get_movies(ids))

        want_movies = self.get_user_products(want_ids)
        results = []

        for m in movies:
            for wm in want_movies:
                if m.must_id != wm["product_id"]:
                    continue

                watched = Want(
                    movie=m,
                    added=dt.datetime.strptime(
                        wm["modified_at"],
                        "%Y-%m-%dT%H:%M:%S.%fZ"
                    ).date(),
                )
                results.append(watched)
        return results
