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


if __name__ == "__main__":
    main()
