import pandas as pd
from datetime import datetime
import chess.pgn
import io


class GameProcessor:
    def __init__(self, username):
        self.username = username

    def get_opponent(self, white: dict, black: dict) -> dict:
        """Determines the stats of the opponent"""

        if white["username"].lower() == self.username:
            output = {
                "played": "white",
                "rating": white["rating"],
                "opponent": black["username"],
                "opponent_rating": black["rating"],
                "result": white["result"],
                "info": black["result"],
            }

        else:
            output = {
                "played": "black",
                "rating": black["rating"],
                "opponent": white["username"],
                "opponent_rating": white["rating"],
                "result": black["result"],
                "info": white["result"],
            }

        return output

    def get_result(self, result: str, info: str) -> tuple:
        """Standardises the different game results"""

        draws = [
            "agreed",
            "repetition",
            "stalemate",
            "50move",
            "insufficient",
            "timevsinsufficient",
        ]

        if result == "win":
            return ("win", info)

        if info == "win":
            return ("loss", result)

        if result == info:
            return ("draw", info)

    def get_opening(self, pgn: str) -> str:
        """Extracts the opening from the PGN
        the opeinig is extracted from the ECOUrl, which has the form like:
        "https://www.chess.com/openings/Vienna-Game-Zhuravlev-Countergambit"

        In this case, the opeining "Vienna-Game-Zhuravlev-Countergambit"
        """
        pgn = chess.pgn.read_game(io.StringIO(pgn))

        try:
            opening = pgn.headers["ECOUrl"]
        except KeyError as e:
            opening = None

        return opening

    def get_timestamps(self, row: pd.DataFrame) -> tuple:
        try:
            start_time = datetime.fromtimestamp(row["start_time"])
        except ValueError:
            start_time = None

        try:
            end_time = datetime.fromtimestamp(row["end_time"])
        except ValueError:
            end_time = None

        return start_time, end_time

    def get_time_class(self, row: pd.DataFrame) -> str:
        if row["rules"] == "chess":
            time_class = row["time_class"]
        else:
            time_class = row["time_class"] + " - " + row["rules"]

        return time_class.capitalize()

    def clean_archive(self, data: pd.DataFrame) -> pd.DataFrame:
        """Combine all cleaned data points and export as a DataFrame"""
        print("Processing games...", end="")

        output = []

        for _, row in data.iterrows():

            start_time, end_time = self.get_timestamps(row)
            game_data = self.get_opponent(row["white"], row["black"])
            result, info = self.get_result(game_data["result"], game_data["info"])
            opening_url = self.get_opening(row["pgn"])

            output.append(
                {
                    "url": row["url"],
                    "rated": row["rated"],
                    "time_class": self.get_time_class(row),
                    "time_control": row["time_control"],
                    "start_time": start_time,
                    "end_time": end_time,
                    "played": game_data["played"],
                    "rating": game_data["rating"],
                    "opponent": game_data["opponent"],
                    "opponent_rating": game_data["opponent_rating"],
                    "result": result,
                    "info": info,
                    "opening": opening_url.split("/")[-1] if opening_url else None,
                    "opening_url": opening_url,
                }
            )

        print("Done!")

        return pd.DataFrame(output)
