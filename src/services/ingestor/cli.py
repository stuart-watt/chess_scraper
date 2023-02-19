import click
import json

from gcf import main

@click.command()
@click.option("--event")
def cli_main(event: str):
    main(event=json.loads(event))

if __name__ == "__main__":
    cli_main()