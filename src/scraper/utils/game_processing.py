import pandas as pd
from datetime import datetime

class GameProcessor():

    def __init__(self, username):
        self.username = username

    def get_opponent(self, white: dict, black: dict) -> dict:
        
        if white["username"].lower() == self.username:
            output = {
                "played": "white", 
                "rating": white["rating"],
                "opponent": black["username"],
                "opponent_rating": black["rating"],
                "result": white["result"],
                "info": black["result"]
            }

        else: 
            output = {
                "played": "black", 
                "rating": black["rating"],
                "opponent": white["username"],
                "opponent_rating": white["rating"],
                "result": black["result"],
                "info": white["result"]
            }

        return output

    def get_result(self, result: str, info: str) -> tuple:

        draws = ['agreed', 'repetition', 'stalemate', '50move', 'insufficient', 'timevsinsufficient']

        if result == "win":
            return ("win", info)

        if info == "win":
            return ("loss", result)

        if result == info:
            return ("draw", info)


    def archive_cleaner(self, data: pd.DataFrame) -> pd.DataFrame:

        output = []
        
        for _, row in data.iterrows():

            try:
                start_time = datetime.fromtimestamp(row["start_time"])
            except:
                start_time = None

            try:
                duration = row["end_time"] - row["start_time"]
            except:
                duration = datetime.fromtimestamp(row["start_time"])

            game_data = self.get_opponent(row["white"], row["black"])
            result, info = self.get_result(game_data["result"], game_data["info"])

            output.append({
                "url": row["url"],
                "rated": row["rated"],
                "time_class": row["time_class"],
                "time_control": row["time_control"],
                "start_time": start_time,
                "game_time": duration,
                "played": game_data["played"],
                "rating": game_data["rating"],
                "opponent": game_data["opponent"],
                "opponent_rating": game_data["opponent_rating"],
                "result": result,
                "info": info
            })

        return pd.DataFrame(output)
