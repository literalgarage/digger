import click

from digger.seattle import SEA_DATASETS


@click.group()
def main():
    pass


@main.command()
@click.argument("dataset", type=click.Choice(SEA_DATASETS.keys()))
def download_sea(dataset: str):
    """Download public data from the city of Seattle."""
    from digger.seattle import get_sea_data_url

    dataset_id = SEA_DATASETS[dataset]
    url = get_sea_data_url(dataset_id)
    print(f"Downloading data from {url}...")
    # Here you would add the code to actually download and process the data.
    # For this example, we'll just print the URL.


if __name__ == "__main__":
    main()
