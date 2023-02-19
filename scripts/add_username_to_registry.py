import click
from cloudpathlib import GSPath
import json

# CLI command to add a username to the GCS registry


@click.command()
@click.argument("username")
@click.argument("dst")
def add_username_to_registry(username: str, dst: str):

    path = GSPath(dst)
    entry = json.dumps({"username": username})

    users = path.read_text() if path.exists() else ""

    if entry in users.split("\n"):
        print(f"{username} already in registry")
    else:
        entry = users + "\n" + entry
        path.write_text(entry)
        print(f"Successfully added {username} to {dst}")


if __name__ == "__main__":
    add_username_to_registry()
