import io
import typing
from datetime import datetime

import pandas as pd
import chess.pgn

class GameProcessor:
    def __init__(self, username):
        self.username = username

    def extract_pgn_data(self, row: pd.DataFrame):
        return chess.pgn.read_game(io.StringIO(row["pgn"]))

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
            return ("Win", info)

        if info == "win":
            return ("Loss", result)

        if result == info:
            return ("Draw", info)

    def get_opening(self, row: pd.DataFrame) -> str:
        """Extracts the opening from the PGN
        the opeinig is extracted from the ECOUrl, which has the form like:
        "https://www.chess.com/openings/Vienna-Game-Zhuravlev-Countergambit"

        In this case, the opeining "Vienna-Game-Zhuravlev-Countergambit"
        """
        
        try:
            opening = self.extract_pgn_data(row).headers["ECOUrl"]
        except KeyError as e:
            opening = None

        return opening

    def get_timestamps(self, row: pd.DataFrame) -> typing.Tuple[datetime, datetime, int]:

        pgn = self.extract_pgn_data(row)
        dt_form = "%Y.%m.%d%H:%M:%S"
        try:
            s_timestamp = datetime.strptime(pgn.headers["UTCDate"]+pgn.headers["StartTime"], dt_form)

        except KeyError as e:
            s_timestamp = None

        try:
            e_timestamp = datetime.strptime(pgn.headers["EndDate"]+pgn.headers["EndTime"], dt_form)

            duration = e_timestamp - s_timestamp
            duration = duration.seconds
        except KeyError as e:
            e_timestamp = None
            duration = None

        return s_timestamp, e_timestamp, duration

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

            start_time, end_time, duration = self.get_timestamps(row)

            game_data = self.get_opponent(row["white"], row["black"])
            result, info = self.get_result(game_data["result"], game_data["info"])
            opening_url = self.get_opening(row)

            output.append(
                {
                    "url": row["url"],
                    "rated": row["rated"],
                    "time_class": self.get_time_class(row),
                    "time_control": row["time_control"],
                    "start_time": start_time,
                    "end_time": end_time,
                    "duration": duration,
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

