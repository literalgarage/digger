from urllib.parse import urlencode

import httpx

SEA_DATA_URL_FMT = "https://data.seattle.gov/resource/{dataset_id}.json"


# A collection of well-known datasets that we've given friendly names to.
SEA_DATASETS: dict[str, str] = {
    # Building permits issued by the SDCI
    "building": "76t5-zqzr",
    # Land use applications submitted to the City of Seattle
    "land_use": "ht3q-kdvx",
    # Trade permits issued by the SDCI
    "trade": "c87v-5hwh",
    # Electrical permits issued by the SDCI
    "electrical": "c4tj-daue",
}


def get_sea_data_url(dataset_id: str, *, offset: int = 0, limit: int = 1_000) -> str:
    base_url = SEA_DATA_URL_FMT.format(dataset_id=dataset_id)
    query = urlencode({"$offset": offset, "$limit": limit})
    return f"{base_url}?{query}"


def get_sea_data(dataset_id: str, offset: int, limit: int = 1_000) -> list[dict]:
    url = get_sea_data_url(dataset_id, offset=offset, limit=limit)
    response = httpx.get(url)
    response.raise_for_status()
    maybe = response.json()
    # Sanity checks; if this fails we have a bug or the API has changed.
    if not isinstance(maybe, list):
        raise ValueError(f"Expected a list, got {type(maybe)}: {maybe}")
    if not isinstance(maybe[0], dict):
        raise ValueError(f"Expected a list of dicts, got {type(maybe[0])}: {maybe}")
    return maybe
