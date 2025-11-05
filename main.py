import click

from digger.seattle import SEA_DATASETS, get_sea_data


@click.group()
def main():
    pass


@main.command()
@click.argument("dataset", type=click.Choice(SEA_DATASETS.keys()))
def download(dataset: str):
    """Download public data from the city of Seattle."""

    dataset_id = SEA_DATASETS[dataset]
    print(f"Downloading data from {dataset}...")
    for item in get_sea_data(dataset_id):
        click.echo(item)


if __name__ == "__main__":
    main()
