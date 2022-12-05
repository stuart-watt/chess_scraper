import click
import pandas as pd

from scraper.chess_client import ChessClient
from scraper.game_processing import GameProcessor

@click.command()
@click.option("-u", "--username", required=True, help="Chess.com username")
@click.option(
    "-f",
    "--file",
    type=click.Path(),
    required=True,
    help="Filepath to dump results (.csv extension)",
)
def get_data(username: str, file: str):

    client = ChessClient(username)
    data = client.get_archive_data()

    processor = GameProcessor(username)
    games = processor.clean_archive(data)

    games.to_csv(file, index=False)
    return
