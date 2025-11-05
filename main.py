import json
import typing as t

import click

from digger.seattle import SEA_DATASETS, get_sea_data
from digger.writers import dump_data

type Format = t.Literal["jsonl", "csv"]


@click.group()
def main():
    pass


@main.command()
@click.argument("dataset", type=click.Choice(SEA_DATASETS.keys()))
@click.option(
    "--format",
    type=click.Choice(["jsonl", "csv"]),
    default="jsonl",
    help="Output format",
)
def download(dataset: str, format: Format = "jsonl"):
    """Download public data from the city of Seattle."""

    dataset_id = SEA_DATASETS[dataset]
    click.echo(f"Downloading data from '{dataset}'...", err=True)
    items = get_sea_data(dataset_id)
    output = t.cast(t.IO[str], click.get_text_stream("stdout"))
    dump_data(items, output, format)


@main.command()
@click.argument("file_path", type=click.Path(exists=True, dir_okay=False))
def to_csv(file_path: str):
    """Convert a JSONL file to CSV."""
    output = t.cast(t.IO[str], click.get_text_stream("stdout"))
    with open(file_path, "r", encoding="utf-8") as f:
        as_dicts = (json.loads(line) for line in f)
        dump_data(as_dicts, output, "csv")


if __name__ == "__main__":
    main()
