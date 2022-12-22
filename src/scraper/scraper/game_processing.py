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

    def get_timestamps(
        self, row: pd.DataFrame
    ) -> typing.Tuple[datetime, datetime, int]:

        pgn = self.extract_pgn_data(row)
        dt_form = "%Y.%m.%d%H:%M:%S"
        try:
            s_timestamp = datetime.strptime(
                pgn.headers["UTCDate"] + pgn.headers["StartTime"], dt_form
            )

        except KeyError as e:
            s_timestamp = None

        try:
            e_timestamp = datetime.strptime(
                pgn.headers["EndDate"] + pgn.headers["EndTime"], dt_form
            )

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

    def count_moves(self, row: pd.DataFrame, played: str) -> int:
        pgn = self.extract_pgn_data(row)

        n_moves = len([_ for _ in pgn.mainline()])

        # if the n_moves is even, white and black played the same number of moves
        # else white played one more than black

        return int(n_moves / 2) + 1 if played == "White" else int(n_moves / 2)

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
                    "n_moves": self.count_moves(row, game_data["played"]),
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

    def calculate_ratings(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate a continuous daily rating for each time-class"""

        print("Calculating ratings...", end="")

        data["date"] = data["end_time"].dt.date

        data = data.sort_values(by="end_time")

        date_range = pd.DataFrame(
            pd.date_range(data["date"].min(), datetime.today()), columns=["date"]
        )
        date_range["date"] = date_range["date"].dt.date

        date_class_master = date_range.merge(
            data["time_class"].drop_duplicates(), how="cross"
        )

        ratings = (
            data[["date", "time_class", "rating"]]
            .groupby(["time_class", "date"])
            .last()
            .reset_index()
        )

        ratings = date_class_master.merge(
            ratings, how="left", on=["date", "time_class"]
        )

        ratings["rating"] = ratings.groupby("time_class").fillna(method="ffill")[
            "rating"
        ]

        print("Done!")

        return ratings.dropna().sort_values(by=["date", "time_class"])
