import click
import pandas as pd

from scraper.chess_client import ChessClient
from scraper.game_processing import GameProcessor


def get_data(username: str, file: str):

    client = ChessClient(username)
    data = client.get_archive_data()

    data.sample(100).to_json("data/test.json", orient="records")

    processor = GameProcessor(username)
    games = processor.clean_archive(data)

    games.to_csv(file, index=False)
    return


@click.command()
@click.option("-u", "--username", required=True, help="Chess.com username")
@click.option("-f", "--file", required=True, help="Output path (.csv)")
def main(username: str, file: str):
    get_data(username, file)
