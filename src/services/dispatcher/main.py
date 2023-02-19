import os
import json
import pandas as pd

from google.cloud import pubsub_v1

PUBSUB_TOPIC_ID = os.environ["PUBSUB_TOPIC_ID"]
DATALAKE_BUCKET = os.environ["DATALAKE_BUCKET"]


def main(event=None, context=None):

    client = pubsub_v1.PublisherClient()

    uri = f"gs://{DATALAKE_BUCKET}/users/users.jsonlines"

    print(f"Reading users from {uri}")

    users = pd.read_json(uri, lines=True)

    for user in users.username:
        msg = json.dumps({"username": user}).encode()

        print(f"Publishing message to {PUBSUB_TOPIC_ID}: {msg}")
        client.publish(PUBSUB_TOPIC_ID, msg).result()

    return


if __name__ == "__main__":
    main()
