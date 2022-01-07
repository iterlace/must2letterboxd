from pathlib import Path
import os

from src.must import MustAccount
from src.exporter import CSVExporter


def main():
    must_username = input("Enter your Must username: ")

    must = MustAccount(must_username)
    wanted = must.get_want_movies()
    watched = must.get_watched_movies()

    root = Path(__file__).parent.resolve()
    want_filepath = os.path.join(root, "want.csv")
    watched_filepath = os.path.join(root, "watched.csv")

    CSVExporter.export_want(want_filepath, wanted)
    print(f"Exported Want list to {want_filepath}")

    CSVExporter.export_watched(watched_filepath, watched)
    print(f"Exported Watched list to {want_filepath}")


if __name__ == '__main__':
    main()
