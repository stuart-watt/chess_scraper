import click
import pandas as pd

from scraper.client import ChessClient

@click.group()
def cli():
    pass

@cli.command()
@click.option("--username", required=True, help="Chess.com username")
@click.option("--file", type=click.Path(), required=True, help="File to dump results")
def get_data(username: str, file: str):

    client = ChessClient()

    client.get_archive_data(username).to_json(file, orient="records")
