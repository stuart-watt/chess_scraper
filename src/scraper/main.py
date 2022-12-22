import os
from scraper import scraper


def main(event: dict = None, context: dict = None):

    scraper.get_data(
        os.environ["USERNAME"],
        "gs://" + os.environ["DATALAKE_BUCKET"] + "/games/",
    )
