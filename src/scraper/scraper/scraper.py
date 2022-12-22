import click
import pandas as pd

from scraper.chess_client import ChessClient
from scraper.game_processing import GameProcessor


def get_data(username: str, file_path: str):

    client = ChessClient(username)
    data = client.get_archive_data()

    processor = GameProcessor(username)
    games = processor.clean_archive(data)

    games.to_csv(file_path+"games.csv", index=False)

    ratings = processor.calculate_ratings(games)
    ratings.to_csv(file_path+"ratings.csv", index=False)

    return


@click.command()
@click.option("-u", "--username", required=True, help="Chess.com username")
@click.option("-f", "--file-path", required=True, help="Output path (.csv)")
def main(username: str, file_path: str):
    get_data(username, file_path)
