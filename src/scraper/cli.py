import click
import pandas as pd

from scraper.client import ChessClient

@click.group()
def cli():
    pass

@cli.command()
@click.option("-u", "--username", required=True, help="Chess.com username")
@click.option("-f", "--file", type=click.Path(), required=True, help="File to dump results (json extension)")
def get_data(username: str, file: str):

    client = ChessClient()

    data = client.get_archive_data(username, file)
