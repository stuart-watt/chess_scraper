import pandas as pd
import requests
import json
from client import ChessClient

client = ChessClient()

# print(client.get_user("samwise_gambit"))
# print()
# print(client.get_user_stats("samwise_gambit"))
# print()
# print(json.dumps(client.get_user_archive_list("samwise_gambit"), indent=2))

# print()
# print(json.dumps(client.get_user_archive("samwise_gambit", 2021, 11), indent=2))

r = requests.get("https://api.chess.com/pub/player/samwise_gambit/games/2021/12")

# print(json.dumps(r.json(), indent=2))

# blah = client.get_archive_data("samwise_gambit")
blah = client.get_archive_data("samwise_gambit", year=2021, month=11)
print(blah)
# print(client.get_archive_data("samwise_gambit").iloc[0])