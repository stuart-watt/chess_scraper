import os
import json
from base64 import b64decode
from scraper import scraper

def main(event: dict = None, context: dict = None):

    if set(event.keys()) == {"username"}:  # Invoked manually.
        pass
    else:  # Invoked via pubsub.
        event = json.loads(b64decode(event["data"]).decode("utf-8"))

    username = event.get("username", None)

    if username is not None:

        scraper.get_data(
            username,
            "gs://" + os.environ["DATALAKE_BUCKET"],
        )

