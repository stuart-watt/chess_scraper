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
            opening = pgn.headers["ECOUrl"].split("/")[-1]
        except KeyError as e:
            opening = None
            
        return opening

        
    def clean_archive(self, data: pd.DataFrame) -> pd.DataFrame:
        """Combine all cleaned data points and export as a DataFrame"""

        output = []

        for _, row in data.iterrows():

            try:
                start_time = datetime.fromtimestamp(row["start_time"])
            except:
                start_time = None

            try:
                end_time = datetime.fromtimestamp(row["end_time"])
            except:
                end_time = None

            timestamp = start_time or end_time

            game_data = self.get_opponent(row["white"], row["black"])
            result, info = self.get_result(game_data["result"], game_data["info"])
            opening = self.get_opening(row["pgn"])

            output.append(
                {
                    "url": row["url"],
                    "rated": row["rated"],
                    "time_class": row["time_class"],
                    "time_control": row["time_control"],
                    "timestamp": timestamp,
                    "played": game_data["played"],
                    "rating": game_data["rating"],
                    "opponent": game_data["opponent"],
                    "opponent_rating": game_data["opponent_rating"],
                    "result": result,
                    "info": info,
                    "opening": opening
                }
            )

        return pd.DataFrame(output)
