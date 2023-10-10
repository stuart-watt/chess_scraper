import requests
import typing
import pandas as pd


class ChessClient:
    def __init__(self, username: str):
        self.header = {
            "user-agent": "Chess Analytics Application",
        }
        self.check_user(username)

    def check_user(self, username: str):

        r = requests.get(
            url=f"https://api.chess.com/pub/player/{username}",
            headers=self.header,
            timeout=10,
        )

        response = r.json()

        if r.status_code == 200:
            self.username = username

        if r.status_code == 404:
            raise ValueError(response["message"])

    def list_archives(self) -> list:

        r = requests.get(
            f"https://api.chess.com/pub/player/{self.username}/games/archives",
            headers=self.header,
            timeout=10,
        )
        r = r.json()

        print(f"Found {len(r['archives'])} archives")

        return r["archives"]

    def get_archive(self, url: str) -> typing.List[dict]:
        r = requests.get(url, headers=self.header, timeout=10)
        return r.json()["games"]

    def get_archive_data(self) -> pd.DataFrame:

        archives = self.list_archives()

        print("Ingesting...", end="")
        games = [game for url in archives for game in self.get_archive(url)]
        print(f"Done\nFound {len(games)} games")
        return pd.DataFrame(games)
