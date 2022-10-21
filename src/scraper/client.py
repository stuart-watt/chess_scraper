import requests
import pandas as pd
from scraper.utils import GameProcessor

class ChessClient():

    def __init__(self):
        pass

    def get_user(self, username) -> dict:

        r = requests.get(f"https://api.chess.com/pub/player/{username}")
        response = r.json()

        if r.status_code == 200:
            return response
        
        if r.status_code == 404:
            print(response["message"])
            return False


    def get_user_stats(self, username: str) -> dict:
        if self.get_user(username):

            r = requests.get(f"https://api.chess.com/pub/player/{username}/stats")

            return r.json()

    def get_user_archive_list(self, username: str) -> list:
        if self.get_user(username):

            r = requests.get(f"https://api.chess.com/pub/player/{username}/games/archives")
            r = r.json()

            print(f"Found {len(r['archives'])} archives")

            return r['archives']

    def get_archive_data(self, username: str, file: str, year: int = None, month: int = None) -> pd.DataFrame:
        if self.get_user(username):
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

                processor.archive_cleaner(pd.DataFrame(games)).to_json(file, orient="records")


            else:
                print(f"Collecting games for {username} from {month:02}/{year}")
                url = f"https://api.chess.com/pub/player/{username}/games/{year}/{month:02}"

                r = requests.get(url)
                r = r.json()

                processor.archive_cleaner(pd.DataFrame(r["games"])).to_json(file, orient="records")
