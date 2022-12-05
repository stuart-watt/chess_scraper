import os
from scraper.scraper import get_data

def main(event: dict, context: dict):

    get_data(os.environ["USERNAME"], "gs://" + os.environ["DATALAKE_BUCKET"] + "/games/games.csv")
    return