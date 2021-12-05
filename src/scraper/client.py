import requests
import pandas as pd
from scraper.utils import GameProcessor

class ChessClient():

    def __init__(self):
        pass

    def get_user(self, username) -> dict:
        r = requests.get(f"https://api.chess.com/pub/player/{username}")

        return r.json()

    def get_user_stats(self, username: str) -> dict:

        r = requests.get(f"https://api.chess.com/pub/player/{username}/stats")

        return r.json()

    def get_user_archive_list(self, username: str) -> list:

        r = requests.get(f"https://api.chess.com/pub/player/{username}/games/archives")
        r = r.json()

        print(f"Found {len(r['archives'])} archives")

        return r['archives']

    def get_archive_data(self, username: str, year: int = None, month: int = None) -> pd.DataFrame:

        processor = GameProcessor(username)
        
        if not year:
            print(f"Collecting all games for {username}")
            archives = self.get_user_archive_list(username)
        
            games = []

            for url in archives:
                r = requests.get(url)
                r = r.json()

                for game in r["games"]:
                    games.append(game)

            print(f"Found {len(games)} games")

            return processor.archive_cleaner(pd.DataFrame(games))


        else:
            print(f"Collecting games for {username} from {month:02}/{year}")
            url = f"https://api.chess.com/pub/player/{username}/games/{year}/{month:02}"

            r = requests.get(url)
            r = r.json()

            return processor.archive_cleaner(pd.DataFrame(r["games"]))
